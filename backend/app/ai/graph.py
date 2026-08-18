import time
import logging
from langgraph.graph import StateGraph, START, END
from app.ai.state import ComplaintGraphState
from app.ai.nodes.ingest import ingest_node
from app.ai.nodes.extract import extract_node
from app.ai.nodes.validate import validate_node
from app.ai.nodes.classify import classify_node
from app.ai.nodes.risk import assess_risk_node
from app.ai.nodes.summary import generate_summary_node
from app.ai.nodes.completeness import check_completeness_node

logger = logging.getLogger("aivoa_qms.ai.graph")


def build_complaint_graph():
    """
    Constructs the typed LangGraph StateGraph for QMS complaint processing:
    START -> ingest_input -> extract_complaint -> validate_complaint -> classify_complaint -> assess_risk -> generate_summary -> check_completeness -> END
    """
    workflow = StateGraph(ComplaintGraphState)

    # Add nodes
    workflow.add_node("ingest_input", ingest_node)
    workflow.add_node("extract_complaint", extract_node)
    workflow.add_node("validate_complaint", validate_node)
    workflow.add_node("classify_complaint", classify_node)
    workflow.add_node("assess_risk", assess_risk_node)
    workflow.add_node("generate_summary", generate_summary_node)
    workflow.add_node("check_completeness", check_completeness_node)

    # Define execution edge workflow sequence
    workflow.add_edge(START, "ingest_input")
    workflow.add_edge("ingest_input", "extract_complaint")
    workflow.add_edge("extract_complaint", "validate_complaint")
    workflow.add_edge("validate_complaint", "classify_complaint")
    workflow.add_edge("classify_complaint", "assess_risk")
    workflow.add_edge("assess_risk", "generate_summary")
    workflow.add_edge("generate_summary", "check_completeness")
    workflow.add_edge("check_completeness", END)

    return workflow.compile()


# Compiled LangGraph app
complaint_app = build_complaint_graph()


def run_complaint_workflow(text: str, source_type: str = "text") -> ComplaintGraphState:
    """
    Executes the compiled LangGraph workflow synchronously.
    Calculates execution duration and logs processing state.
    """
    start_time = time.time()
    
    initial_state: ComplaintGraphState = {
        "raw_input": text,
        "source_type": source_type,
        "cleaned_input": None,
        "customer_name": None,
        "product_name": None,
        "product_type": "FDF",
        "batch_number": None,
        "market": None,
        "description": None,
        "defect": None,
        "quantity_affected": None,
        "category": None,
        "patient_impact": "None",
        "medical_safety_concern": False,
        "severity": "Minor",
        "probability": "Possible",
        "detectability": "Medium",
        "risk_level": "Low",
        "investigation_required": True,
        "rationale": None,
        "recommended_actions": [],
        "summary": None,
        "completeness_score": 0.0,
        "missing_fields": [],
        "processing_stages": [],
        "errors": [],
        "processing_time_ms": 0.0
    }
    
    logger.info(f"Executing LangGraph complaint workflow (source: {source_type})")
    final_state = complaint_app.invoke(initial_state)
    
    duration = (time.time() - start_time) * 1000.0
    final_state["processing_time_ms"] = round(duration, 2)
    logger.info(f"LangGraph execution finished in {final_state['processing_time_ms']} ms")
    
    return final_state
