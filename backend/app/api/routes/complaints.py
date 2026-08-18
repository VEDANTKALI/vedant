import json
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from app.schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from app.schemas.ai import AIAnalyzeRequest, AIAnalysisResponse, StructuredExtractedComplaint
from app.schemas.risk import RiskAssessmentResponse
from app.repositories.complaint_repository import ComplaintRepository
from app.api.dependencies import get_complaint_repo
from app.ai.graph import run_complaint_workflow
from app.services.pdf_service import extract_text_from_pdf_bytes

logger = logging.getLogger("aivoa_qms.api.complaints")

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.post("/analyze", response_model=AIAnalysisResponse)
def analyze_complaint(payload: AIAnalyzeRequest, repo: ComplaintRepository = Depends(get_complaint_repo)):
    """
    Triggers the LangGraph AI workflow (ingest -> extract -> validate -> classify -> assess_risk -> generate_summary -> check_completeness).
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Complaint text cannot be empty.")

    try:
        graph_state = run_complaint_workflow(text=payload.text, source_type=payload.source_type or "text")
        
        extracted_comp = StructuredExtractedComplaint(
            customer_name=graph_state.get("customer_name"),
            product_name=graph_state.get("product_name") or "Pharmaceutical Product",
            product_type=graph_state.get("product_type") or "FDF",
            batch_number=graph_state.get("batch_number"),
            market=graph_state.get("market"),
            category=graph_state.get("category") or "Product Quality",
            description=graph_state.get("description") or payload.text,
            defect=graph_state.get("defect"),
            quantity_affected=graph_state.get("quantity_affected"),
            patient_impact=graph_state.get("patient_impact") or "None",
            medical_safety_concern=bool(graph_state.get("medical_safety_concern", False)),
            severity=graph_state.get("severity") or "Minor",
            risk_level=graph_state.get("risk_level") or "Low",
            investigation_required=bool(graph_state.get("investigation_required", True)),
            recommended_actions=graph_state.get("recommended_actions") or [],
            missing_fields=graph_state.get("missing_fields") or []
        )

        # Audit AI Run
        repo.log_ai_run(
            complaint_id=None,
            workflow_name="complaint_analysis_workflow",
            model_name="gemma2-9b-it",
            status="SUCCESS",
            duration_ms=graph_state.get("processing_time_ms", 0.0),
            raw_input=payload.text,
            raw_output=extracted_comp.model_dump()
        )

        return AIAnalysisResponse(
            success=True,
            complaint=extracted_comp,
            summary=graph_state.get("summary") or "Complaint analysis completed.",
            completeness_score=graph_state.get("completeness_score", 0.0),
            missing_fields=graph_state.get("missing_fields") or [],
            processing_time_ms=graph_state.get("processing_time_ms", 0.0),
            model_name="gemma2-9b-it",
            processing_stages=graph_state.get("processing_stages", [])
        )
    except Exception as e:
        logger.error(f"Error during AI analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Extracts plain text from uploaded customer complaint PDF file.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        content = await file.read()
        extracted_text = extract_text_from_pdf_bytes(content)
        return {
            "filename": file.filename,
            "extracted_text": extracted_text,
            "char_count": len(extracted_text)
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF extraction error: {str(e)}")


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(payload: ComplaintCreate, repo: ComplaintRepository = Depends(get_complaint_repo)):
    """
    Saves a customer complaint along with its AI risk assessment into PostgreSQL/SQLite.
    """
    try:
        complaint = repo.create_complaint(payload)
        return complaint
    except Exception as e:
        logger.error(f"Failed to create complaint record: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create complaint: {str(e)}")


@router.get("", response_model=List[ComplaintResponse])
def list_complaints(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    risk_level: Optional[str] = None,
    search: Optional[str] = None,
    repo: ComplaintRepository = Depends(get_complaint_repo)
):
    return repo.get_all(skip=skip, limit=limit, category=category, risk_level=risk_level, search=search)


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, repo: ComplaintRepository = Depends(get_complaint_repo)):
    complaint = repo.get_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Complaint ID {complaint_id} not found.")
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(complaint_id: int, payload: ComplaintUpdate, repo: ComplaintRepository = Depends(get_complaint_repo)):
    complaint = repo.update_complaint(complaint_id, payload)
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Complaint ID {complaint_id} not found.")
    return complaint


@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_complaint(complaint_id: int, repo: ComplaintRepository = Depends(get_complaint_repo)):
    deleted = repo.delete_complaint(complaint_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Complaint ID {complaint_id} not found.")
    return None


@router.get("/{complaint_id}/risk-assessment", response_model=RiskAssessmentResponse)
def get_risk_assessment(complaint_id: int, repo: ComplaintRepository = Depends(get_complaint_repo)):
    complaint = repo.get_by_id(complaint_id)
    if not complaint or not complaint.risk_assessment:
        raise HTTPException(status_code=404, detail="Risk assessment not found for this complaint.")
    return complaint.risk_assessment
