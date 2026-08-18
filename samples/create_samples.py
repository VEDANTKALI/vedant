import os
from pypdf import PdfWriter
from pypdf.annotations import FreeText

def create_sample_files():
    sample_dir = r"C:\Users\Vedant_kali\.gemini\antigravity-ide\scratch\aivoa-qms-complaints\samples"
    os.makedirs(sample_dir, exist_ok=True)

    # 1. Text File
    txt_path = os.path.join(sample_dir, "sample_complaint.txt")
    txt_content = """CUSTOMER COMPLAINT REPORT — PHARMACEUTICAL QMS
Reporter: MetroCare Health System / Dr. Robert Vance
Market: US
Product: Amoxicillin 250mg Capsules
Batch Number: AMX-2026-774
Quantity Affected: 50 units

Description:
Retail pharmacy received a shipment of Amoxicillin 250mg Capsules (Batch #AMX-2026-774). Upon inspection, 2 blister packs exhibited pin-hole tears in the primary aluminum foil seal. The capsules were exposed to ambient humidity causing clumping. Immediate quarantine required.
"""
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)

    print(f"Created {txt_path}")

if __name__ == "__main__":
    create_sample_files()
