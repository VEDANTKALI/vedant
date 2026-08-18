import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.complaint import Complaint
from app.models.risk_assessment import RiskAssessment
from app.models.document import ComplaintDocument
from app.models.ai_run import AIRun
from app.models.audit import AuditLog
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate


class ComplaintRepository:
    def __init__(self, db: Session):
        self.db = db

    def generate_complaint_number(self) -> str:
        count = self.db.query(func.count(Complaint.id)).scalar() or 0
        return f"CMP-2026-{(count + 1):04d}"

    def create_complaint(self, data: ComplaintCreate) -> Complaint:
        comp_num = data.complaint_number or self.generate_complaint_number()
        
        missing_str = json.dumps(data.missing_fields) if isinstance(data.missing_fields, list) else data.missing_fields
        
        complaint = Complaint(
            complaint_number=comp_num,
            received_date=data.received_date,
            customer_name=data.customer_name,
            product_name=data.product_name,
            product_type=data.product_type or "FDF",
            batch_number=data.batch_number,
            market=data.market,
            category=data.category,
            description=data.description,
            defect=data.defect,
            quantity_affected=data.quantity_affected,
            patient_impact=data.patient_impact or "None",
            medical_safety_concern=data.medical_safety_concern,
            severity=data.severity or "Minor",
            risk_level=data.risk_level or "Low",
            investigation_required=data.investigation_required,
            status=data.status or "NEW",
            completeness_score=data.completeness_score or 0.0,
            missing_fields=missing_str
        )
        self.db.add(complaint)
        self.db.flush()  # assign ID

        # Create Risk Assessment if present
        if data.risk_assessment:
            risk = RiskAssessment(
                complaint_id=complaint.id,
                severity=data.risk_assessment.severity,
                probability=data.risk_assessment.probability,
                detectability=data.risk_assessment.detectability,
                risk_level=data.risk_assessment.risk_level,
                rationale=data.risk_assessment.rationale,
                recommended_actions=data.risk_assessment.recommended_actions,
                model_name=data.risk_assessment.model_name or "gemma2-9b-it"
            )
            self.db.add(risk)

        # Audit Log
        audit = AuditLog(
            entity_name="Complaint",
            entity_id=complaint.id,
            action="CREATE",
            details={"complaint_number": comp_num, "product": data.product_name, "risk": data.risk_level}
        )
        self.db.add(audit)

        self.db.commit()
        self.db.refresh(complaint)
        return complaint

    def get_by_id(self, complaint_id: int) -> Optional[Complaint]:
        return self.db.query(Complaint).filter(Complaint.id == complaint_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, category: Optional[str] = None, risk_level: Optional[str] = None, search: Optional[str] = None) -> List[Complaint]:
        query = self.db.query(Complaint)
        if category:
            query = query.filter(Complaint.category == category)
        if risk_level:
            query = query.filter(Complaint.risk_level == risk_level)
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (Complaint.complaint_number.ilike(search_pattern)) |
                (Complaint.product_name.ilike(search_pattern)) |
                (Complaint.batch_number.ilike(search_pattern)) |
                (Complaint.customer_name.ilike(search_pattern))
            )
        return query.order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()

    def update_complaint(self, complaint_id: int, data: ComplaintUpdate) -> Optional[Complaint]:
        complaint = self.get_by_id(complaint_id)
        if not complaint:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "missing_fields" in update_data and isinstance(update_data["missing_fields"], list):
            update_data["missing_fields"] = json.dumps(update_data["missing_fields"])

        for field, value in update_data.items():
            setattr(complaint, field, value)

        # Update associated risk level if severity updated
        if complaint.risk_assessment:
            if "severity" in update_data:
                complaint.risk_assessment.severity = update_data["severity"]
            if "risk_level" in update_data:
                complaint.risk_assessment.risk_level = update_data["risk_level"]

        # Audit Log
        audit = AuditLog(
            entity_name="Complaint",
            entity_id=complaint.id,
            action="UPDATE",
            details=update_data
        )
        self.db.add(audit)

        self.db.commit()
        self.db.refresh(complaint)
        return complaint

    def delete_complaint(self, complaint_id: int) -> bool:
        complaint = self.get_by_id(complaint_id)
        if not complaint:
            return False
        
        self.db.delete(complaint)
        self.db.commit()
        return True

    def log_ai_run(self, complaint_id: Optional[int], workflow_name: str, model_name: str, status: str, duration_ms: float, raw_input: str, raw_output: dict) -> AIRun:
        ai_run = AIRun(
            complaint_id=complaint_id,
            workflow_name=workflow_name,
            model_name=model_name,
            execution_status=status,
            processing_time_ms=duration_ms,
            raw_input=raw_input,
            raw_output=raw_output
        )
        self.db.add(ai_run)
        self.db.commit()
        self.db.refresh(ai_run)
        return ai_run

    def get_dashboard_summary(self) -> dict:
        total = self.db.query(func.count(Complaint.id)).scalar() or 0
        open_c = self.db.query(func.count(Complaint.id)).filter(Complaint.status != "CLOSED").scalar() or 0
        high_risk = self.db.query(func.count(Complaint.id)).filter(Complaint.risk_level.in_(["High", "Critical"])).scalar() or 0
        under_inv = self.db.query(func.count(Complaint.id)).filter(Complaint.status == "UNDER_INVESTIGATION").scalar() or 0
        
        avg_comp = self.db.query(func.avg(Complaint.completeness_score)).scalar() or 0.0

        # Risk distribution
        risk_dist = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        risk_rows = self.db.query(Complaint.risk_level, func.count(Complaint.id)).group_by(Complaint.risk_level).all()
        for r_level, count in risk_rows:
            if r_level in risk_dist:
                risk_dist[r_level] = count
            elif r_level:
                risk_dist[r_level] = count

        # Category distribution
        cat_dist = {}
        cat_rows = self.db.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
        for cat, count in cat_rows:
            if cat:
                cat_dist[cat] = count

        # Recent complaints
        recent = self.db.query(Complaint).order_by(Complaint.created_at.desc()).limit(5).all()

        return {
            "total_complaints": total,
            "open_complaints": open_c,
            "high_risk_complaints": high_risk,
            "under_investigation": under_inv,
            "avg_completeness_score": round(float(avg_comp), 1),
            "risk_distribution": risk_dist,
            "category_distribution": cat_dist,
            "recent_complaints": recent
        }
