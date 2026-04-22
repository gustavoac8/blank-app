from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.database import get_db
from app.db.models import ActionPlan, Campaign, Diagnosis, FollowUpAttempt, Patient, PipelineStage, User
from app.db.schemas import (
    CampaignCreate,
    CampaignOut,
    DiagnosisCreate,
    DiagnosisOut,
    PatientCreate,
    PatientOut,
    PatientUpdateStage,
    PlanOut,
    Token,
    UserCreate,
    UserOut,
)
from app.services.ads_mock import AdsIntegratorMock
from app.services.ai_orchestrator import AIOrchestrator
from app.services.followup import generate_followup_sequence
from app.services.landing_generator import generate_landing_page

router = APIRouter()


@router.post('/auth/register', response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(400, 'Email já cadastrado')
    user = User(
        organization_id=payload.organization_id,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/auth/token', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, 'Credenciais inválidas')
    return Token(access_token=create_access_token(user.id))


@router.post('/diagnosis', response_model=DiagnosisOut)
def create_diagnosis(
    payload: DiagnosisCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    level = AIOrchestrator.classify_level(payload)
    summary = AIOrchestrator.business_diagnosis(payload, level)
    diagnosis = Diagnosis(
        organization_id=current_user.organization_id,
        **payload.model_dump(),
        ai_summary=summary,
        level=level,
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    plan = ActionPlan(
        diagnosis_id=diagnosis.id,
        organization_id=current_user.organization_id,
        content=AIOrchestrator.generate_action_plan(summary, payload),
    )
    db.add(plan)
    db.commit()
    return diagnosis


@router.get('/plans/latest', response_model=PlanOut)
def get_latest_plan(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = (
        db.query(ActionPlan)
        .filter(ActionPlan.organization_id == current_user.organization_id)
        .order_by(ActionPlan.id.desc())
        .first()
    )
    if not plan:
        raise HTTPException(404, 'Nenhum plano gerado')
    return plan


@router.post('/landing/generate')
def create_landing(
    payload: DiagnosisCreate,
    current_user: User = Depends(get_current_user),
):
    page = generate_landing_page(payload)
    return {'organization_id': current_user.organization_id, 'landing_page': page}


@router.post('/campaigns', response_model=CampaignOut)
def create_campaign(
    payload: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    created = AdsIntegratorMock.create_campaign(payload.channel, payload.name, payload.budget_daily)
    campaign = Campaign(
        organization_id=current_user.organization_id,
        channel=payload.channel,
        name=payload.name,
        budget_daily=payload.budget_daily,
        status=created['status'],
        metrics=created['metrics'],
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get('/campaigns', response_model=list[CampaignOut])
def list_campaigns(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Campaign).filter(Campaign.organization_id == current_user.organization_id).all()


@router.post('/crm/patients', response_model=PatientOut)
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = Patient(organization_id=current_user.organization_id, **payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.patch('/crm/patients/{patient_id}/stage', response_model=PatientOut)
def update_patient_stage(
    patient_id: int,
    payload: PatientUpdateStage,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = db.get(Patient, patient_id)
    if not patient or patient.organization_id != current_user.organization_id:
        raise HTTPException(404, 'Paciente não encontrado')
    patient.stage = payload.stage
    db.commit()
    db.refresh(patient)
    return patient


@router.post('/crm/patients/{patient_id}/follow-up')
def run_followup(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patient = db.get(Patient, patient_id)
    if not patient or patient.organization_id != current_user.organization_id:
        raise HTTPException(404, 'Paciente não encontrado')

    sequence = generate_followup_sequence(patient.full_name)
    for item in sequence:
        attempt = FollowUpAttempt(
            patient_id=patient.id,
            organization_id=current_user.organization_id,
            channel=item['channel'],
            attempt_number=item['attempt'],
            status='sent',
            message=item['message'],
        )
        db.add(attempt)
    patient.stage = PipelineStage.nutricao
    db.commit()
    return {'attempts': sequence, 'final_stage': patient.stage}


@router.get('/dashboard')
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    org = current_user.organization_id
    leads = db.query(func.count(Patient.id)).filter(Patient.organization_id == org).scalar() or 0
    converted = (
        db.query(func.count(Patient.id))
        .filter(Patient.organization_id == org, Patient.stage == PipelineStage.faturamento)
        .scalar()
        or 0
    )
    total_revenue = (
        db.query(func.coalesce(func.sum(Patient.estimated_revenue), 0))
        .filter(Patient.organization_id == org, Patient.stage == PipelineStage.faturamento)
        .scalar()
    )
    campaigns = db.query(Campaign).filter(Campaign.organization_id == org).all()
    total_leads_ads = sum(c.metrics.get('leads', 0) for c in campaigns)
    total_spend = sum(c.metrics.get('cpl', 0) * c.metrics.get('leads', 0) for c in campaigns)
    roi = round((float(total_revenue) / total_spend), 2) if total_spend else 0

    return {
        'leads_gerados': leads + total_leads_ads,
        'taxa_conversao': round((converted / leads) * 100, 2) if leads else 0,
        'custo_por_lead': round(total_spend / total_leads_ads, 2) if total_leads_ads else 0,
        'roi': roi,
        'faturamento_estimado': float(total_revenue),
    }
