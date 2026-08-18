from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class AIAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw text of customer complaint or email")
    source_type: Optional[str] = Field("text", description="text or pdf")


class StructuredExtractedComplaint(BaseModel):
    customer_name: Optional[str] = Field(None, description="Customer or healthcare provider name if available")
    product_name: Optional[str] = Field(None, description="Drug or pharmaceutical product name")
    product_type: str = Field("FDF", description="FDF (Finished Dosage Form) or API")
    batch_number: Optional[str] = Field(None, description="Lot or batch number (e.g. BNT-2026-001)")
    market: Optional[str] = Field(None, description="Country or market destination (e.g. US, EU, India)")
    category: str = Field("Product Quality", description="QMS complaint category")
    description: str = Field(..., description="Normalized complaint narrative")
    defect: Optional[str] = Field(None, description="Specific defect (e.g. discolored tablet, seal failure)")
    quantity_affected: Optional[int] = Field(None, description="Quantity or count of affected units")
    patient_impact: str = Field("None", description="None, Potential, Confirmed")
    medical_safety_concern: bool = Field(False, description="True if patient health risk present")
    severity: str = Field("Minor", description="Minor, Major, Critical")
    risk_level: str = Field("Low", description="Low, Medium, High, Critical")
    investigation_required: bool = Field(True, description="Whether QMS root cause investigation is required")
    recommended_actions: List[str] = Field(default_factory=list, description="Recommended CAPA actions")
    missing_fields: List[str] = Field(default_factory=list, description="Fields missing from input")


class AIAnalysisResponse(BaseModel):
    success: bool
    complaint: StructuredExtractedComplaint
    summary: str
    completeness_score: float
    missing_fields: List[str]
    processing_time_ms: float
    model_name: str = "gemma2-9b-it"
    processing_stages: List[Dict[str, Any]] = Field(default_factory=list)
