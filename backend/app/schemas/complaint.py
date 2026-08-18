from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.risk import RiskAssessmentBase, RiskAssessmentResponse


class ComplaintBase(BaseModel):
    customer_name: Optional[str] = None
    product_name: str
    product_type: str = "FDF"
    batch_number: Optional[str] = None
    market: Optional[str] = None
    category: str
    description: str
    defect: Optional[str] = None
    quantity_affected: Optional[int] = None
    patient_impact: str = "None"
    medical_safety_concern: bool = False
    severity: str = "Minor"
    risk_level: str = "Low"
    investigation_required: bool = True
    status: str = "NEW"


class ComplaintCreate(ComplaintBase):
    complaint_number: Optional[str] = None
    received_date: Optional[datetime] = None
    completeness_score: Optional[float] = 0.0
    missing_fields: Optional[List[str]] = None
    risk_assessment: Optional[RiskAssessmentBase] = None


class ComplaintUpdate(BaseModel):
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    product_type: Optional[str] = None
    batch_number: Optional[str] = None
    market: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    defect: Optional[str] = None
    quantity_affected: Optional[int] = None
    patient_impact: Optional[str] = None
    medical_safety_concern: Optional[bool] = None
    severity: Optional[str] = None
    risk_level: Optional[str] = None
    investigation_required: Optional[bool] = None
    status: Optional[str] = None
    completeness_score: Optional[float] = None
    missing_fields: Optional[List[str]] = None


class ComplaintResponse(ComplaintBase):
    id: int
    complaint_number: str
    received_date: datetime
    completeness_score: float
    missing_fields: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    risk_assessment: Optional[RiskAssessmentResponse] = None

    class Config:
        from_attributes = True
