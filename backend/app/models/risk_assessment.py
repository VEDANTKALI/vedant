from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    severity = Column(String(50), nullable=False)  # Minor, Major, Critical
    probability = Column(String(50), nullable=True)  # Unlikely, Possible, Likely, Frequent
    detectability = Column(String(50), nullable=True)  # High, Medium, Low
    risk_level = Column(String(50), nullable=False)  # Low, Medium, High, Critical
    
    rationale = Column(Text, nullable=False)
    recommended_actions = Column(JSON, nullable=True)  # List of recommended CAPA / immediate actions
    model_name = Column(String(100), default="gemma2-9b-it")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    complaint = relationship("Complaint", back_populates="risk_assessment")
