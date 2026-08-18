from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.complaint_repository import ComplaintRepository

def get_complaint_repo(db: Session = Depends(get_db)) -> ComplaintRepository:
    return ComplaintRepository(db)
