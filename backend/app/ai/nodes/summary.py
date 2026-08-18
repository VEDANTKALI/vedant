import json
import time
import logging
from app.ai.state import ComplaintGraphState
from app.ai.llm import llm_service
from app.ai.prompts.complaint_prompts import SUMMARY_SYSTEM_PROMPT

logger = logging.getLogger("aivoa_qms.ai.summary")

def generate_summary_node(state: ComplaintGraphState) -> ComplaintGraphState:
    logger.info("LangGraph Node: generate_summary_node starting.")
    product = state.get("product_name", "Product")
    batch = state.get("batch_number", "Unspecified Batch")
    category = state.get("category", "Complaint")
    defect = state.get("defect", "Defect reported")
    risk = state.get("risk_level", "Low")
    
    summary = f"Customer complaint regarding {product} (Batch #{batch or 'N/A'}). Classified as {category} issue ({defect or 'unspecified defect'}) with a calculated risk level of {risk}."
    
    try:
        raw_llm = llm_service.invoke(
            prompt=f"Generate summary for:\nProduct: {product}\nBatch: {batch}\nCategory: {category}\nRisk: {risk}\nDescription: {state.get('description', '')}",
            system_prompt=SUMMARY_SYSTEM_PROMPT,
            response_format_json=True
        )
        data = json.loads(raw_llm)
        if data.get("summary"):
            summary = data.get("summary")
    except Exception as e:
        logger.warning(f"LLM summary fallback applied ({e}).")

    stages = state.get("processing_stages", [])
    stages.append({
        "stage": "generate_summary",
        "label": "Generating summary",
        "status": "completed",
        "timestamp": time.time()
    })

    return {
        **state,
        "summary": summary,
        "processing_stages": stages
    }
