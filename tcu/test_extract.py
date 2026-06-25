import pdfplumber

pdf_path = "Admission Guidebook for Holders of Secondary School Qualifications_2025_2026.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[26] # Page 27
    text = page.extract_text(layout=True)
    print("LAYOUT MODE:")
    for line in text.split('\n')[:20]:
        print(line)
