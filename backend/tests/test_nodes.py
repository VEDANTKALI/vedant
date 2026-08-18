from app.ai.nodes.ingest import ingest_node
from app.ai.nodes.extract import extract_node
from app.ai.nodes.classify import classify_node
from app.ai.nodes.completeness import check_completeness_node

def test_ingest_node():
    state = {"raw_input": "Customer complaint  for   Amoxicillin", "processing_stages": []}
    result = ingest_node(state)
    assert result["cleaned_input"] == "Customer complaint for Amoxicillin"

def test_completeness_node():
    state = {
        "product_name": "Amoxicillin",
        "batch_number": "AMX-123",
        "category": "Product Quality",
        "description": "Discolored tablet",
        "processing_stages": []
    }
    result = check_completeness_node(state)
    assert result["completeness_score"] > 0
    assert "Customer Name / Reporter" in result["missing_fields"]
