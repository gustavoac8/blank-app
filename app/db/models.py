from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class PhysicianLevel(str, Enum):
    iniciante = 'iniciante'
    intermediario = 'intermediario'
    avancado = 'avancado'


class PipelineStage(str, Enum):
    lead = 'lead'
    atendimento = 'atendimento'
    agendamento = 'agendamento'
    consulta = 'consulta'
    faturamento = 'faturamento'
    nutricao = 'nutricao'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Diagnosis(Base):
    __tablename__ = 'diagnoses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), index=True)
    physician_name: Mapped[str] = mapped_column(String(255))
    specialty: Mapped[str] = mapped_column(String(120))
    average_ticket: Mapped[float] = mapped_column(Float)
    schedule_capacity_weekly: Mapped[int] = mapped_column(Integer)
    city_region: Mapped[str] = mapped_column(String(255))
    key_differentials: Mapped[str] = mapped_column(Text)
    main_services: Mapped[str] = mapped_column(Text)
    marketing_history: Mapped[str] = mapped_column(Text)
    current_roi: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_summary: Mapped[dict] = mapped_column(JSON)
    level: Mapped[PhysicianLevel] = mapped_column(SQLEnum(PhysicianLevel))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ActionPlan(Base):
    __tablename__ = 'action_plans'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey('diagnoses.id'))
    organization_id: Mapped[str] = mapped_column(String(64), index=True)
    content: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    diagnosis = relationship('Diagnosis')


class Campaign(Base):
    __tablename__ = 'campaigns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), index=True)
    channel: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(40), default='active')
    budget_daily: Mapped[float] = mapped_column(Float)
    metrics: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Patient(Base):
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(64), index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(120))
    stage: Mapped[PipelineStage] = mapped_column(SQLEnum(PipelineStage), default=PipelineStage.lead)
    estimated_revenue: Mapped[float] = mapped_column(Float, default=0)
    notes: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FollowUpAttempt(Base):
    __tablename__ = 'follow_up_attempts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    organization_id: Mapped[str] = mapped_column(String(64), index=True)
    channel: Mapped[str] = mapped_column(String(20))
    attempt_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient = relationship('Patient')
