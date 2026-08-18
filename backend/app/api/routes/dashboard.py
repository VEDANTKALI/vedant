from fastapi import APIRouter, Depends
from app.schemas.dashboard import DashboardSummary
from app.repositories.complaint_repository import ComplaintRepository
from app.api.dependencies import get_complaint_repo

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(repo: ComplaintRepository = Depends(get_complaint_repo)):
    """
    Returns live aggregated QMS metrics from the database.
    """
    return repo.get_dashboard_summary()
