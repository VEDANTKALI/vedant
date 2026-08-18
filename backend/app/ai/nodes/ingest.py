import time
import logging
from app.ai.state import ComplaintGraphState

logger = logging.getLogger("aivoa_qms.ai.ingest")

def ingest_node(state: ComplaintGraphState) -> ComplaintGraphState:
    """
    Ingests and normalizes raw text or extracted PDF content.
    """
    logger.info("LangGraph Node: ingest_node starting.")
    start_time = time.time()
    
    raw = state.get("raw_input", "") or ""
    cleaned = " ".join(raw.split())  # normalize whitespace
    
    stages = state.get("processing_stages", [])
    stages.append({
        "stage": "ingest_input",
        "label": "Reading complaint",
        "status": "completed",
        "timestamp": time.time()
    })
    
    return {
        **state,
        "cleaned_input": cleaned,
        "processing_stages": stages
    }
