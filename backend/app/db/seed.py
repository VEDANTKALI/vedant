import logging
from datetime import datetime, timedelta
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.complaint import Complaint
from app.models.risk_assessment import RiskAssessment
from app.models.audit import AuditLog

logger = logging.getLogger("aivoa_qms.db.seed")

SAMPLE_COMPLAINTS = [
    {
        "complaint_number": "CMP-2026-0001",
        "received_date": datetime.utcnow() - timedelta(days=2),
        "customer_name": "St. Jude Regional Hospital / Dr. Sarah Jenkins",
        "product_name": "Amoxicillin 250mg Capsules",
        "product_type": "FDF",
        "batch_number": "AMX-2026-402",
        "market": "US",
        "category": "Product Quality",
        "description": "Hospital pharmacy reported finding 3 discolored, brownish capsules inside a sealed 100-count HDPE bottle of Amoxicillin 250mg Capsules. Remaining capsules appear normal.",
        "defect": "Discolored Capsule",
        "quantity_affected": 3,
        "patient_impact": "Potential",
        "medical_safety_concern": False,
        "severity": "Major",
        "risk_level": "Medium",
        "investigation_required": True,
        "status": "UNDER_INVESTIGATION",
        "completeness_score": 100.0,
        "missing_fields": "[]",
        "risk_assessment": {
            "severity": "Major",
            "probability": "Possible",
            "detectability": "Medium",
            "risk_level": "Medium",
            "rationale": "Discoloration indicates localized oxidation or thermal degradation during capping process. Moderate impact on active chemical assay.",
            "recommended_actions": [
                "Issue CAPA ticket INV-2026-089.",
                "Pull retains for Batch AMX-2026-402 for HPLC potency assay.",
                "Request physical sample return from hospital QA department."
            ]
        }
    },
    {
        "complaint_number": "CMP-2026-0002",
        "received_date": datetime.utcnow() - timedelta(days=1),
        "customer_name": "MetroCare Pharmacy Group",
        "product_name": "Paracetamol 500mg Tablets",
        "product_type": "FDF",
        "batch_number": "PRT-2026-881",
        "market": "EU",
        "category": "Packaging",
        "description": "Retail pharmacist observed micro pin-hole tear on aluminum foil backing of blister card #4 in box. Product exposed to ambient humidity.",
        "defect": "Blister Seal Pin-hole",
        "quantity_affected": 10,
        "patient_impact": "None",
        "medical_safety_concern": False,
        "severity": "Minor",
        "risk_level": "Low",
        "investigation_required": True,
        "status": "NEW",
        "completeness_score": 87.5,
        "missing_fields": "[\"Customer Name / Reporter\"]",
        "risk_assessment": {
            "severity": "Minor",
            "probability": "Unlikely",
            "detectability": "High",
            "risk_level": "Low",
            "rationale": "Mechanical pinhole defect occurred during blister heat-sealing. No microbial contamination detected.",
            "recommended_actions": [
                "Inspect heat-sealing temperature logs for Blistering Line 3.",
                "Replace sealing die gasket."
            ]
        }
    },
    {
        "complaint_number": "CMP-2026-0003",
        "received_date": datetime.utcnow(),
        "customer_name": "GlobalMed Wholesalers / Quality Compliance",
        "product_name": "Metformin Extended Release 500mg",
        "product_type": "FDF",
        "batch_number": "STR-2026-993",
        "market": "US",
        "category": "Wrong Strength",
        "description": "URGENT SAFETY REPORT: Retail distributor reported receiving outer carton labeled 100mg, but internal blister foils are printed Metformin 500mg Tablets. Severe labeling mix-up risk.",
        "defect": "Wrong Strength Packaging Mix-up",
        "quantity_affected": 500,
        "patient_impact": "Confirmed",
        "medical_safety_concern": True,
        "severity": "Critical",
        "risk_level": "Critical",
        "investigation_required": True,
        "status": "ESCALATED",
        "completeness_score": 100.0,
        "missing_fields": "[]",
        "risk_assessment": {
            "severity": "Critical",
            "probability": "Likely",
            "detectability": "Low",
            "risk_level": "Critical",
            "rationale": "Mismatch between outer carton dose labeling and primary blister strength presents severe risk of accidental patient overdose and acute hypoglycemic reaction.",
            "recommended_actions": [
                "Immediate Class I Recall notification to regulatory authorities (FDA/EMA).",
                "Quarantine all distributed inventory for Batch STR-2026-993.",
                "Initiate emergency Executive QMS Board meeting and line clearance audit."
            ]
        }
    }
]


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Complaint).count() == 0:
            logger.info("Seeding initial QMS customer complaints...")
            for comp_data in SAMPLE_COMPLAINTS:
                risk_data = comp_data.pop("risk_assessment")
                complaint = Complaint(**comp_data)
                db.add(complaint)
                db.flush()

                risk = RiskAssessment(
                    complaint_id=complaint.id,
                    severity=risk_data["severity"],
                    probability=risk_data["probability"],
                    detectability=risk_data["detectability"],
                    risk_level=risk_data["risk_level"],
                    rationale=risk_data["rationale"],
                    recommended_actions=risk_data["recommended_actions"]
                )
                db.add(risk)

                audit = AuditLog(
                    entity_name="Complaint",
                    entity_id=complaint.id,
                    action="CREATE",
                    details={"seeded": True, "number": complaint.complaint_number}
                )
                db.add(audit)

            db.commit()
            logger.info("Sample database seeding completed successfully.")
        else:
            logger.info("Database already contains complaints. Skipping seed.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
