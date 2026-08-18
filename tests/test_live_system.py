import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_live_system():
    print("=" * 60)
    print("RUNNING LIVE END-TO-END SYSTEM TEST (Backend + LangGraph + DB)")
    print("=" * 60)

    # 1. Health Check
    res = requests.get(f"{BASE_URL}/health")
    print(f"1. Health Check Status: {res.status_code}")
    print(f"   Payload: {res.json()}")
    assert res.status_code == 200

    # 2. Test Text Complaint AI Analysis
    with open(r"C:\Users\Vedant_kali\.gemini\antigravity-ide\scratch\aivoa-qms-complaints\samples\sample_complaint.txt", "r", encoding="utf-8") as f:
        txt_content = f.read()

    print("\n2. Testing AI Analysis on Sample Complaint Text...")
    analyze_res = requests.post(
        f"{BASE_URL}/complaints/analyze",
        json={"text": txt_content, "source_type": "text"}
    )
    print(f"   Status Code: {analyze_res.status_code}")
    data_txt = analyze_res.json()
    assert analyze_res.status_code == 200
    assert data_txt["success"] is True
    
    comp_txt = data_txt["complaint"]
    print(f"   [OK] Extracted Product: {comp_txt['product_name']}")
    print(f"   [OK] Extracted Batch: {comp_txt['batch_number']}")
    print(f"   [OK] Extracted Market: {comp_txt['market']}")
    print(f"   [OK] Category: {comp_txt['category']}")
    print(f"   [OK] Risk Level: {comp_txt['risk_level']}")
    print(f"   [OK] Completeness Score: {data_txt['completeness_score']}%")
    print(f"   [OK] Processing Stages ({len(data_txt['processing_stages'])} steps): {[s['label'] for s in data_txt['processing_stages']]}")
    print(f"   [OK] Duration: {data_txt['processing_time_ms']} ms")

    # 3. Save Text Complaint into DB
    save_payload = {
        "customer_name": comp_txt["customer_name"] or "Dr. Robert Vance",
        "product_name": comp_txt["product_name"],
        "product_type": comp_txt["product_type"],
        "batch_number": comp_txt["batch_number"],
        "market": comp_txt["market"],
        "category": comp_txt["category"],
        "description": comp_txt["description"],
        "defect": comp_txt["defect"],
        "quantity_affected": comp_txt["quantity_affected"] or 50,
        "patient_impact": comp_txt["patient_impact"],
        "medical_safety_concern": comp_txt["medical_safety_concern"],
        "severity": comp_txt["severity"],
        "risk_level": comp_txt["risk_level"],
        "investigation_required": comp_txt["investigation_required"],
        "status": "UNDER_INVESTIGATION",
        "completeness_score": data_txt["completeness_score"],
        "risk_assessment": {
            "severity": comp_txt["severity"],
            "probability": "Possible",
            "detectability": "Medium",
            "risk_level": comp_txt["risk_level"],
            "rationale": "Blister seal break exposes drug product to ambient humidity.",
            "recommended_actions": comp_txt["recommended_actions"]
        }
    }
    save_res = requests.post(f"{BASE_URL}/complaints", json=save_payload)
    print(f"\n3. Save Complaint Status: {save_res.status_code}")
    saved_item_1 = save_res.json()
    print(f"   [OK] Saved Complaint Number: {saved_item_1['complaint_number']} (ID: {saved_item_1['id']})")
    assert save_res.status_code == 201

    # 4. Test PDF Upload & Text Extraction
    pdf_path = r"C:\Users\Vedant_kali\.gemini\antigravity-ide\scratch\aivoa-qms-complaints\samples\sample_complaint.pdf"
    print("\n4. Testing PDF Upload & Text Extraction...")
    with open(pdf_path, "rb") as f:
        pdf_res = requests.post(f"{BASE_URL}/complaints/upload-pdf", files={"file": ("sample_complaint.pdf", f, "application/pdf")})
    print(f"   Status Code: {pdf_res.status_code}")
    pdf_data = pdf_res.json()
    assert pdf_res.status_code == 200
    print(f"   [OK] Extracted {pdf_data['char_count']} chars from PDF '{pdf_data['filename']}'")

    # 5. Test AI Analysis on Extracted PDF Text
    print("\n5. Testing AI Analysis on Extracted PDF Content...")
    pdf_analyze_res = requests.post(
        f"{BASE_URL}/complaints/analyze",
        json={"text": pdf_data["extracted_text"], "source_type": "pdf"}
    )
    print(f"   Status Code: {pdf_analyze_res.status_code}")
    data_pdf = pdf_analyze_res.json()
    assert pdf_analyze_res.status_code == 200
    comp_pdf = data_pdf["complaint"]
    print(f"   [OK] Extracted Product: {comp_pdf['product_name']}")
    print(f"   [OK] Extracted Batch: {comp_pdf['batch_number']}")
    print(f"   [OK] Category: {comp_pdf['category']}")
    print(f"   [OK] Risk Level: {comp_pdf['risk_level']}")
    print(f"   [OK] Completeness Score: {data_pdf['completeness_score']}%")

    # 6. Save PDF Complaint into DB
    pdf_save_payload = {
        "customer_name": comp_pdf["customer_name"] or "GlobalMed Wholesalers / Dr. Alexander Vance",
        "product_name": comp_pdf["product_name"],
        "product_type": comp_pdf["product_type"],
        "batch_number": comp_pdf["batch_number"],
        "market": comp_pdf["market"] or "US",
        "category": comp_pdf["category"],
        "description": comp_pdf["description"],
        "defect": comp_pdf["defect"],
        "quantity_affected": comp_pdf["quantity_affected"] or 500,
        "patient_impact": comp_pdf["patient_impact"],
        "medical_safety_concern": comp_pdf["medical_safety_concern"],
        "severity": comp_pdf["severity"],
        "risk_level": comp_pdf["risk_level"],
        "investigation_required": comp_pdf["investigation_required"],
        "status": "ESCALATED",
        "completeness_score": data_pdf["completeness_score"],
        "risk_assessment": {
            "severity": comp_pdf["severity"],
            "probability": "Likely",
            "detectability": "Low",
            "risk_level": comp_pdf["risk_level"],
            "rationale": "Outer carton dose mismatch creates acute patient safety risk.",
            "recommended_actions": comp_pdf["recommended_actions"]
        }
    }
    pdf_save_res = requests.post(f"{BASE_URL}/complaints", json=pdf_save_payload)
    print(f"\n6. Save PDF Complaint Status: {pdf_save_res.status_code}")
    saved_item_2 = pdf_save_res.json()
    print(f"   [OK] Saved Complaint Number: {saved_item_2['complaint_number']} (ID: {saved_item_2['id']})")
    assert pdf_save_res.status_code == 201

    # 7. Test Dashboard Summary Metrics
    print("\n7. Fetching Dashboard Summary Metrics from DB...")
    dash_res = requests.get(f"{BASE_URL}/dashboard/summary")
    print(f"   Status Code: {dash_res.status_code}")
    dash_summary = dash_res.json()
    assert dash_res.status_code == 200
    print(f"   [OK] Total Complaints in DB: {dash_summary['total_complaints']}")
    print(f"   [OK] Open Complaints: {dash_summary['open_complaints']}")
    print(f"   [OK] High/Critical Risk Complaints: {dash_summary['high_risk_complaints']}")
    print(f"   [OK] Average Completeness Score: {dash_summary['avg_completeness_score']}%")
    print(f"   [OK] Risk Level Distribution: {dash_summary['risk_distribution']}")

    print("\n" + "=" * 60)
    print("ALL LIVE SYSTEM TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_live_system()
