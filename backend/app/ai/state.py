from typing import TypedDict, Optional, List, Dict, Any


class ComplaintGraphState(TypedDict):
    raw_input: str
    source_type: str  # text or pdf
    
    # Ingestion stage
    cleaned_input: Optional[str]
    
    # Extraction stage
    customer_name: Optional[str]
    product_name: Optional[str]
    product_type: Optional[str]  # FDF or API
    batch_number: Optional[str]
    market: Optional[str]
    description: Optional[str]
    defect: Optional[str]
    quantity_affected: Optional[int]
    
    # Classification stage
    category: Optional[str]
    
    # Risk Assessment stage
    patient_impact: Optional[str]
    medical_safety_concern: Optional[bool]
    severity: Optional[str]
    probability: Optional[str]
    detectability: Optional[str]
    risk_level: Optional[str]
    investigation_required: Optional[bool]
    rationale: Optional[str]
    recommended_actions: List[str]
    
    # Summary & Completeness
    summary: Optional[str]
    completeness_score: Optional[float]
    missing_fields: List[str]
    
    # Execution Tracking & Audit
    processing_stages: List[Dict[str, Any]]
    errors: List[str]
    processing_time_ms: Optional[float]
