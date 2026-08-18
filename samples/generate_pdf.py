import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf():
    pdf_path = r"C:\Users\Vedant_kali\.gemini\antigravity-ide\scratch\aivoa-qms-complaints\samples\sample_complaint.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "PHARMACEUTICAL CUSTOMER COMPLAINT REPORT")
    
    c.setFont("Helvetica", 11)
    c.drawString(50, 720, "Reporter: GlobalMed Wholesalers / Dr. Alexander Vance")
    c.drawString(50, 700, "Market: US")
    c.drawString(50, 680, "Product Name: Metformin Extended Release 500mg")
    c.drawString(50, 660, "Batch Number: STR-2026-993")
    c.drawString(50, 640, "Category: Wrong Strength")
    c.drawString(50, 620, "Quantity Affected: 500 units")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 580, "Complaint Narrative:")
    
    c.setFont("Helvetica", 10)
    text_lines = [
        "URGENT SAFETY REPORT: Retail distributor reported receiving outer carton labeled 100mg,",
        "but internal blister foils are printed Metformin 500mg Tablets. Mismatch between outer carton",
        "labeling and primary blister strength presents severe risk of accidental patient overdose",
        "and acute hypoglycemic reaction. Immediate batch quarantine requested."
    ]
    y = 560
    for line in text_lines:
        c.drawString(50, y, line)
        y -= 18
        
    c.save()
    print(f"Generated PDF at {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
