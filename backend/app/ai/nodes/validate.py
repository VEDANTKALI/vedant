import time
import logging
from app.ai.state import ComplaintGraphState

logger = logging.getLogger("aivoa_qms.ai.validate")

def validate_node(state: ComplaintGraphState) -> ComplaintGraphState:
    logger.info("LangGraph Node: validate_node starting.")
    errors = state.get("errors", [])
    
    # Check minimum required information
    if not state.get("product_name"):
        errors.append("Product name could not be identified.")
    if not state.get("description"):
        errors.append("Complaint description is empty.")
        
    stages = state.get("processing_stages", [])
    stages.append({
        "stage": "validate_complaint",
        "label": "Validating information",
        "status": "completed",
        "timestamp": time.time()
    })
    
    return {
        **state,
        "errors": errors,
        "processing_stages": stages
    }
