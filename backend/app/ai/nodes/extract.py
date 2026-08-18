import json
import re
import time
import logging
from app.ai.state import ComplaintGraphState
from app.ai.llm import llm_service
from app.ai.prompts.complaint_prompts import EXTRACTION_SYSTEM_PROMPT

logger = logging.getLogger("aivoa_qms.ai.extract")


def _rule_based_extraction(text: str) -> dict:
    """
    Intelligent fallback parser using regex patterns for pharmaceutical complaints.
    Guarantees deterministic extraction even if LLM service is offline or unconfigured.
    """
    text_lower = text.lower()
    
    # Customer / Hospital / Clinic
    customer = None
    cust_match = re.search(r"(?:customer|from|reporter|clinic|hospital|pharmacy|dr\.|doctor)\s*:\s*([A-Za-z0-9\s,\.-]+)", text, re.IGNORECASE)
    if cust_match:
        customer = cust_match.group(1).split("\n")[0].strip()
    
    # Batch / Lot Number
    batch = None
    batch_match = re.search(r"(?:batch|lot|b/n|l/n)\s*(?:#|no\.?|num)?\s*[:\s]?\s*([A-Za-z0-9\-_]+)", text, re.IGNORECASE)
    if batch_match:
        batch = batch_match.group(1).strip()
    
    # Product Name
    product = "Unknown Pharmaceutical Product"
    prod_match = re.search(r"(?:product|drug|medication|medicine)\s*:\s*([A-Za-z0-9\s\dmg%]+)", text, re.IGNORECASE)
    if prod_match:
        product = prod_match.group(1).split("\n")[0].strip()
    else:
        # Check common pharma terms
        pharma_keywords = ["paracetamol", "amoxicillin", "ibuprofen", "metformin", "ciprofloxacin", "atorvastatin", "aspirin", "insulin", "tablets", "capsules", "injection", "syrup"]
        for kw in pharma_keywords:
            if kw in text_lower:
                product = kw.capitalize()
                break
    
    # Market
    market = None
    market_keywords = ["us", "usa", "uk", "eu", "germany", "france", "india", "japan", "canada", "australia"]
    for m in market_keywords:
        if re.search(r"\b" + m + r"\b", text_lower):
            market = m.upper()
            break
            
    # Defect
    defect = None
    defect_keywords = ["discolored", "seal failure", "broken", "leak", "contamination", "wrong strength", "missing label", "particulate", "crack", "foreign matter"]
    for d in defect_keywords:
        if d in text_lower:
            defect = d.title()
            break

    # Quantity
    quantity = None
    qty_match = re.search(r"(\d+)\s*(?:units|tablets|capsules|bottles|boxes|packs|vials)", text, re.IGNORECASE)
    if qty_match:
        quantity = int(qty_match.group(1))

    return {
        "customer_name": customer,
        "product_name": product,
        "product_type": "API" if "api" in text_lower or "bulk powder" in text_lower else "FDF",
        "batch_number": batch,
        "market": market,
        "description": text[:500],
        "defect": defect,
        "quantity_affected": quantity
    }


def extract_node(state: ComplaintGraphState) -> ComplaintGraphState:
    logger.info("LangGraph Node: extract_node starting.")
    text = state.get("cleaned_input", "") or ""
    
    extracted = None
    try:
        raw_llm = llm_service.invoke(
            prompt=f"Extract structured complaint fields from this complaint text:\n\n{text}",
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            response_format_json=True
        )
        extracted = json.loads(raw_llm)
    except Exception as e:
        logger.warning(f"LLM extraction failed or unconfigured ({e}). Utilizing rule-based QMS fallback.")
        extracted = _rule_based_extraction(text)
        
    stages = state.get("processing_stages", [])
    stages.append({
        "stage": "extract_complaint",
        "label": "Extracting fields",
        "status": "completed",
        "timestamp": time.time()
    })
    
    return {
        **state,
        "customer_name": extracted.get("customer_name"),
        "product_name": extracted.get("product_name") or "Pharmaceutical Product",
        "product_type": extracted.get("product_type") or "FDF",
        "batch_number": extracted.get("batch_number"),
        "market": extracted.get("market"),
        "description": extracted.get("description") or text,
        "defect": extracted.get("defect"),
        "quantity_affected": extracted.get("quantity_affected"),
        "processing_stages": stages
    }
