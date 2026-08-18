from app.schemas.complaint import ComplaintCreate
from app.schemas.risk import RiskAssessmentBase
from app.schemas.ai import StructuredExtractedComplaint

def test_complaint_create_schema():
    payload = ComplaintCreate(
        product_name="Paracetamol 500mg",
        category="Packaging",
        description="Blister pinhole defect",
        risk_level="Low",
        severity="Minor"
    )
    assert payload.product_name == "Paracetamol 500mg"
    assert payload.product_type == "FDF"

def test_risk_assessment_schema():
    risk = RiskAssessmentBase(
        severity="Major",
        risk_level="Medium",
        rationale="Oxidation detected in formulation",
        recommended_actions=["Pull retains", "Inspect seal"]
    )
    assert risk.severity == "Major"
    assert len(risk.recommended_actions) == 2
