import pdfplumber
import pandas as pd
import os

pdf_path = "Admission Guidebook for Holders of Secondary School Qualifications_2025_2026.pdf"
output_excel = "tcu_data.xlsx"

all_data = []

print("Kuanza kusoma PDF, tafadhali subiri... (Hii inaweza kuchukua dakika kadhaa)")

def fix_cell_text(text):
    if not text:
        return ""
    lines = [line.strip() for line in str(text).split('\n') if line.strip()]
    if len(lines) > 1:
        for idx, line in enumerate(lines):
            if idx > 0 and line.startswith(('Bachelor', 'Master', 'Doctor', 'Diploma', 'Certificate', 'Ordinary', 'BSc', 'BA', 'BEd')):
                front = lines.pop(idx)
                lines.insert(0, front)
                break
    return " ".join(lines)

with pdfplumber.open(pdf_path) as pdf:
    current_university = "Unknown University"
    current_row_data = None
    
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables(table_settings={"text_x_tolerance": 1.5})
        for table in tables:
            if not table or len(table) < 2:
                continue
                
            for row in table:
                cleaned_row = [fix_cell_text(cell) for cell in row]
                
                # Check if this row is a University Header
                if len(cleaned_row) > 0 and any(kw in cleaned_row[0] for kw in ["University", "College", "Institute", "Centre", "Center", "Academy", "Training"]) and "Programme" not in cleaned_row[0]:
                    current_university = cleaned_row[0]
                    continue
                
                # Check if it's the column header row, skip it
                if len(cleaned_row) > 1 and "Programme" in cleaned_row[1]:
                    continue
                
                # If it's a valid data row (S/N is usually a number)
                if len(cleaned_row) >= 4 and cleaned_row[0].strip().replace('.', '').isdigit():
                    if current_row_data:
                        all_data.append(current_row_data)
                        
                    programme = cleaned_row[1]
                    code = cleaned_row[2]
                    requirements = cleaned_row[3]
                    duration = cleaned_row[-1] if len(cleaned_row) > 4 else ""
                    
                    current_row_data = {
                        "University": current_university,
                        "Programme": programme,
                        "Code": code,
                        "Requirements": requirements,
                        "Duration": duration
                    }
                # Continuation row (no S/N)
                elif current_row_data and len(cleaned_row) >= 4 and not cleaned_row[0].strip().replace('.', '').isdigit():
                    # If this row has some data but no S/N, it belongs to the previous course
                    if cleaned_row[1]:
                        current_row_data["Programme"] += " " + cleaned_row[1]
                    if cleaned_row[2]:
                        current_row_data["Code"] += " " + cleaned_row[2]
                    if cleaned_row[3]:
                        current_row_data["Requirements"] += " " + cleaned_row[3]
                        
    if current_row_data:
        all_data.append(current_row_data)

        if (i+1) % 50 == 0:
            print(f"Peeji {i+1} zimesomwa...")

df = pd.DataFrame(all_data)
df.to_excel(output_excel, index=False)

print(f"Imekamilika! Faili limehifadhiwa kama {output_excel}")
print(f"Jumla ya kozi zilizopatikana: {len(df)}")
