from typing import List, Dict
from pydantic import BaseModel
from app.schemas.complaint import ComplaintResponse


class DashboardSummary(BaseModel):
    total_complaints: int
    open_complaints: int
    high_risk_complaints: int
    under_investigation: int
    avg_completeness_score: float
    risk_distribution: Dict[str, int]  # {"Low": x, "Medium": y, "High": z, "Critical": w}
    category_distribution: Dict[str, int]
    recent_complaints: List[ComplaintResponse]
