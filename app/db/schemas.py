from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr

from app.db.models import PhysicianLevel, PipelineStage


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserCreate(BaseModel):
    organization_id: str
    full_name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    organization_id: str
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class DiagnosisCreate(BaseModel):
    physician_name: str
    specialty: str
    average_ticket: float
    schedule_capacity_weekly: int
    city_region: str
    key_differentials: str
    main_services: str
    marketing_history: str
    current_roi: float | None = None


class DiagnosisOut(BaseModel):
    id: int
    physician_name: str
    specialty: str
    level: PhysicianLevel
    ai_summary: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class PlanOut(BaseModel):
    id: int
    content: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class CampaignCreate(BaseModel):
    channel: str
    name: str
    budget_daily: float


class CampaignOut(BaseModel):
    id: int
    channel: str
    name: str
    status: str
    budget_daily: float
    metrics: dict[str, Any]

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    source: str
    estimated_revenue: float = 0
    notes: str = ''


class PatientUpdateStage(BaseModel):
    stage: PipelineStage


class PatientOut(BaseModel):
    id: int
    full_name: str
    phone: str
    email: EmailStr
    source: str
    stage: PipelineStage
    estimated_revenue: float

    class Config:
        from_attributes = True
