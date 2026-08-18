from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.db.session import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, AI_ANALYZE
    performed_by = Column(String(100), default="System AI / Quality Manager")
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
