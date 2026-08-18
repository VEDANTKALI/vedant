from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskAssessmentBase(BaseModel):
    severity: str = Field(..., description="Minor, Major, Critical")
    probability: Optional[str] = Field("Possible", description="Unlikely, Possible, Likely, Frequent")
    detectability: Optional[str] = Field("Medium", description="High, Medium, Low")
    risk_level: str = Field(..., description="Low, Medium, High, Critical")
    rationale: str = Field(..., description="Technical & clinical reasoning for risk level")
    recommended_actions: List[str] = Field(default_factory=list, description="Immediate & CAPA recommendations")
    model_name: Optional[str] = "gemma2-9b-it"


class RiskAssessmentCreate(RiskAssessmentBase):
    pass


class RiskAssessmentResponse(RiskAssessmentBase):
    id: int
    complaint_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
