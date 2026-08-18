import json
import time
import logging
from app.ai.state import ComplaintGraphState
from app.ai.llm import llm_service
from app.ai.prompts.complaint_prompts import CLASSIFICATION_SYSTEM_PROMPT

logger = logging.getLogger("aivoa_qms.ai.classify")

CATEGORIES = [
    "Product Quality",
    "Packaging",
    "Labeling",
    "Stability",
    "Contamination",
    "Foreign Matter",
    "Wrong Product",
    "Wrong Strength",
    "Shipping / Distribution",
    "Adverse Event / Patient Safety",
    "Other"
]

def _rule_based_classification(text: str, defect: str) -> str:
    combined = f"{text} {defect or ''}".lower()
    if "adverse" in combined or "side effect" in combined or "hospital" in combined or "overdose" in combined:
        return "Adverse Event / Patient Safety"
    if "wrong strength" in combined or "dose mixup" in combined or "500mg" in combined and "100mg" in combined:
        return "Wrong Strength"
    if "wrong product" in combined or "wrong drug" in combined:
        return "Wrong Product"
    if "foreign matter" in combined or "hair" in combined or "plastic" in combined or "glass" in combined:
        return "Foreign Matter"
    if "contamination" in combined or "mold" in combined or "fungus" in combined or "bacterial" in combined:
        return "Contamination"
    if "label" in combined or "barcode" in combined or "misprint" in combined or "expiry date" in combined:
        return "Labeling"
    if "box" in combined or "carton" in combined or "blister" in combined or "foil" in combined or "seal" in combined or "bottle" in combined:
        return "Packaging"
    if "discolor" in combined or "broken" in combined or "dissolution" in combined or "chipped" in combined or "crumbly" in combined:
        return "Product Quality"
    if "ship" in combined or "temp" in combined or "transit" in combined:
        return "Shipping / Distribution"
    return "Product Quality"


def classify_node(state: ComplaintGraphState) -> ComplaintGraphState:
    logger.info("LangGraph Node: classify_node starting.")
    text = state.get("description", "") or state.get("cleaned_input", "")
    defect = state.get("defect", "")
    
    category = "Product Quality"
    try:
        raw_llm = llm_service.invoke(
            prompt=f"Classify this complaint text:\n{text}\nDefect: {defect}",
            system_prompt=CLASSIFICATION_SYSTEM_PROMPT,
            response_format_json=True
        )
        data = json.loads(raw_llm)
        cat_candidate = data.get("category")
        if cat_candidate in CATEGORIES:
            category = cat_candidate
        else:
            category = _rule_based_classification(text, defect)
    except Exception as e:
        logger.warning(f"LLM classification fallback applied ({e}).")
        category = _rule_based_classification(text, defect)
        
    stages = state.get("processing_stages", [])
    stages.append({
        "stage": "classify_complaint",
        "label": "Classifying complaint",
        "status": "completed",
        "timestamp": time.time()
    })
    
    return {
        **state,
        "category": category,
        "processing_stages": stages
    }
