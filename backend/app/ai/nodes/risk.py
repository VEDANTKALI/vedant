import json
import time
import logging
from app.ai.state import ComplaintGraphState
from app.ai.llm import llm_service
from app.ai.prompts.complaint_prompts import RISK_ASSESSMENT_SYSTEM_PROMPT

logger = logging.getLogger("aivoa_qms.ai.risk")


def _rule_based_risk_assessment(category: str, defect: str, text: str) -> dict:
    combined = f"{category} {defect or ''} {text}".lower()
    
    # Critical Risk Scenarios
    if any(k in combined for k in ["wrong strength", "adverse event", "overdose", "contamination", "anaphylaxis", "hospital", "pin-hole", "sterility"]):
        return {
            "patient_impact": "Potential" if "hospital" not in combined else "Confirmed",
            "medical_safety_concern": True,
            "severity": "Critical",
            "probability": "Likely",
            "detectability": "Low",
            "risk_level": "High" if "hospital" not in combined else "Critical",
            "investigation_required": True,
            "rationale": "Direct patient safety implications or potential batch sterility/potency degradation requiring immediate quarantine and CAPA root cause analysis.",
            "recommended_actions": [
                "Quarantine affected batch inventory immediately across distribution centers.",
                "Initiate Level-1 QMS Root Cause Investigation with Quality Assurance and Manufacturing.",
                "Perform retain sample testing and full analytical re-test."
            ]
        }
    
    # Major Risk Scenarios
    if any(k in combined for k in ["discolor", "seal failure", "broken", "labeling", "wrong product", "dissolution"]):
        return {
            "patient_impact": "Potential",
            "medical_safety_concern": False,
            "severity": "Major",
            "probability": "Possible",
            "detectability": "Medium",
            "risk_level": "Medium",
            "investigation_required": True,
            "rationale": "Defect impacts product specification or primary packaging integrity, presenting moderate risk to product efficacy.",
            "recommended_actions": [
                "Issue Quality Investigation ticket (CAPA-INV) within 24 hours.",
                "Inspect packaging line sensor logs and batch production records (BPR).",
                "Request sample return from reporting customer for laboratory evaluation."
            ]
        }

    # Minor Risk
    return {
        "patient_impact": "None",
        "medical_safety_concern": False,
        "severity": "Minor",
        "probability": "Unlikely",
        "detectability": "High",
        "risk_level": "Low",
        "investigation_required": True,
        "rationale": "Minor cosmetic defect on secondary packaging with no impact on product quality, safety, or stability.",
        "recommended_actions": [
            "Log complaint in QMS trend monitoring database.",
            "Notify packaging operator for awareness during next production run."
        ]
    }


def assess_risk_node(state: ComplaintGraphState) -> ComplaintGraphState:
    logger.info("LangGraph Node: assess_risk_node starting.")
    text = state.get("description", "") or state.get("cleaned_input", "")
    category = state.get("category", "Product Quality")
    defect = state.get("defect", "")

    risk_data = None
    try:
        raw_llm = llm_service.invoke(
            prompt=f"Assess QMS Risk for this complaint:\nCategory: {category}\nDefect: {defect}\nDescription: {text}",
            system_prompt=RISK_ASSESSMENT_SYSTEM_PROMPT,
            response_format_json=True
        )
        risk_data = json.loads(raw_llm)
    except Exception as e:
        logger.warning(f"LLM risk assessment fallback applied ({e}).")
        risk_data = _rule_based_risk_assessment(category, defect, text)

    stages = state.get("processing_stages", [])
    stages.append({
        "stage": "assess_risk",
        "label": "Assessing risk",
        "status": "completed",
        "timestamp": time.time()
    })

    return {
        **state,
        "patient_impact": risk_data.get("patient_impact", "None"),
        "medical_safety_concern": bool(risk_data.get("medical_safety_concern", False)),
        "severity": risk_data.get("severity", "Minor"),
        "probability": risk_data.get("probability", "Possible"),
        "detectability": risk_data.get("detectability", "Medium"),
        "risk_level": risk_data.get("risk_level", "Low"),
        "investigation_required": bool(risk_data.get("investigation_required", True)),
        "rationale": risk_data.get("rationale", "Risk evaluated based on QMS guidelines."),
        "recommended_actions": risk_data.get("recommended_actions", []),
        "processing_stages": stages
    }
