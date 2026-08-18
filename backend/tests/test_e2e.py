from fastapi.testclient import TestClient
from app.main import app
from app.db.session import engine
from app.db.base import Base

# Ensure all tables are created in test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_e2e_complaint_lifecycle():
    # 1. Health check
    resp = client.get("/api/health")
    assert resp.status_code == 200

    # 2. Analyze complaint via AI workflow
    raw_text = "Hospital Dr. Adams from US reported broken foil seal on Batch #AMX-2026-99 in Amoxicillin 250mg. 5 units affected."
    analyze_resp = client.post("/api/complaints/analyze", json={"text": raw_text, "source_type": "text"})
    assert analyze_resp.status_code == 200
    ai_data = analyze_resp.json()
    assert ai_data["success"] is True
    assert ai_data["complaint"]["product_name"] is not None

    # 3. Create complaint in database
    comp_payload = {
        "customer_name": ai_data["complaint"]["customer_name"] or "Dr. Adams",
        "product_name": ai_data["complaint"]["product_name"],
        "product_type": "FDF",
        "batch_number": "AMX-2026-99",
        "market": "US",
        "category": ai_data["complaint"]["category"],
        "description": ai_data["complaint"]["description"],
        "defect": ai_data["complaint"]["defect"],
        "quantity_affected": 5,
        "patient_impact": ai_data["complaint"]["patient_impact"],
        "medical_safety_concern": ai_data["complaint"]["medical_safety_concern"],
        "severity": ai_data["complaint"]["severity"],
        "risk_level": ai_data["complaint"]["risk_level"],
        "investigation_required": True,
        "status": "NEW",
        "completeness_score": ai_data["completeness_score"],
        "risk_assessment": {
            "severity": ai_data["complaint"]["severity"],
            "probability": "Possible",
            "detectability": "Medium",
            "risk_level": ai_data["complaint"]["risk_level"],
            "rationale": "Blister seal break exposes drug product to humidity.",
            "recommended_actions": ai_data["complaint"]["recommended_actions"]
        }
    }
    create_resp = client.post("/api/complaints", json=comp_payload)
    assert create_resp.status_code == 201
    created_item = create_resp.json()
    complaint_id = created_item["id"]
    assert created_item["complaint_number"].startswith("CMP-")

    # 4. Get complaint by ID
    get_resp = client.get(f"/api/complaints/{complaint_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == complaint_id

    # 5. Check dashboard summary metrics
    dash_resp = client.get("/api/dashboard/summary")
    assert dash_resp.status_code == 200
    summary = dash_resp.json()
    assert summary["total_complaints"] >= 1
