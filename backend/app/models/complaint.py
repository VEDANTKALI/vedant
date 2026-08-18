from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_number = Column(String(50), unique=True, index=True, nullable=False)
    received_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Customer & Product Details
    customer_name = Column(String(255), nullable=True)
    product_name = Column(String(255), nullable=False)
    product_type = Column(String(50), default="FDF")  # FDF (Finished Dosage Form), API (Active Pharmaceutical Ingredient)
    batch_number = Column(String(100), nullable=True, index=True)
    market = Column(String(100), nullable=True)
    
    # Classification & Details
    category = Column(String(100), nullable=False, index=True)  # Product Quality, Packaging, Labeling, Contamination, etc.
    description = Column(Text, nullable=False)
    defect = Column(String(255), nullable=True)
    quantity_affected = Column(Integer, nullable=True)
    
    # Risk & Assessment Summary
    patient_impact = Column(String(50), default="None")  # None, Potential, Confirmed
    medical_safety_concern = Column(Boolean, default=False)
    severity = Column(String(50), default="Minor")  # Minor, Major, Critical
    risk_level = Column(String(50), default="Low", index=True)  # Low, Medium, High, Critical
    investigation_required = Column(Boolean, default=True)
    
    # Status & Completeness
    status = Column(String(50), default="NEW", index=True)  # NEW, UNDER_INVESTIGATION, ESCALATED, CLOSED
    completeness_score = Column(Float, default=0.0)  # Percentage 0-100
    missing_fields = Column(Text, nullable=True)  # JSON or comma separated missing fields
    
    # System timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    risk_assessment = relationship("RiskAssessment", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    documents = relationship("ComplaintDocument", back_populates="complaint", cascade="all, delete-orphan")
    ai_runs = relationship("AIRun", back_populates="complaint", cascade="all, delete-orphan")
