import io
import logging
from pypdf import PdfReader

logger = logging.getLogger("aivoa_qms.services.pdf")

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts plain text from standard PDF files using pypdf.
    Structured in isolated service module for future OCR extensions.
    """
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_pages = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_pages.append(text)
        
        full_text = "\n".join(extracted_pages).strip()
        if not full_text:
            raise ValueError("PDF content appears empty or non-text image-based (OCR required).")
        return full_text
    except Exception as e:
        logger.error(f"Error extracting PDF text: {e}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")
