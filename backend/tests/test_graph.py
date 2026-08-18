from app.ai.graph import run_complaint_workflow

def test_full_langgraph_workflow():
    sample_text = "Customer Dr. Smith reported discolored tablet in Batch #PRT-2026-101 for Paracetamol 500mg."
    final_state = run_complaint_workflow(sample_text, source_type="text")

    assert final_state["product_name"] is not None
    assert final_state["category"] is not None
    assert final_state["risk_level"] is not None
    assert final_state["completeness_score"] > 0
    assert len(final_state["processing_stages"]) == 7
