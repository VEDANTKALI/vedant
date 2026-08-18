from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.db.session import Base


class AIRun(Base):
    __tablename__ = "ai_runs"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="SET NULL"), nullable=True)
    
    workflow_name = Column(String(100), default="complaint_analysis_workflow")
    model_name = Column(String(100), default="gemma2-9b-it")
    timestamp = Column(DateTime, default=datetime.utcnow)
    execution_status = Column(String(50), default="SUCCESS")  # SUCCESS, FAILED, PARTIAL
    processing_time_ms = Column(Float, nullable=True)
    
    raw_input = Column(Text, nullable=True)
    raw_output = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    complaint = relationship("Complaint", back_populates="ai_runs")
