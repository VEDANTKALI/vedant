import time
import logging
from app.ai.state import ComplaintGraphState

logger = logging.getLogger("aivoa_qms.ai.completeness")

REQUIRED_FIELDS = [
    ("product_name", "Product Name"),
    ("batch_number", "Batch / Lot Number"),
    ("customer_name", "Customer Name / Reporter"),
    ("market", "Market / Destination"),
    ("defect", "Defect Type"),
    ("quantity_affected", "Quantity Affected"),
    ("category", "Complaint Category"),
    ("description", "Detailed Narrative")
]

def check_completeness_node(state: ComplaintGraphState) -> ComplaintGraphState:
    logger.info("LangGraph Node: check_completeness_node starting.")
    
    missing = []
    present_count = 0
    
    for field_key, field_label in REQUIRED_FIELDS:
        val = state.get(field_key)
        if val is not None and str(val).strip() != "" and str(val).strip().lower() != "null":
            present_count += 1
        else:
            missing.append(field_label)
            
    score = round((present_count / len(REQUIRED_FIELDS)) * 100, 1)

    stages = state.get("processing_stages", [])
    stages.append({
        "stage": "check_completeness",
        "label": "Checking completeness",
        "status": "completed",
        "timestamp": time.time()
    })

    return {
        **state,
        "completeness_score": score,
        "missing_fields": missing,
        "processing_stages": stages
    }
