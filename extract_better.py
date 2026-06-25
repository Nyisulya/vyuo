import pdfplumber
import pandas as pd
import os
import re

pdf_path = "tcu/Admission Guidebook for Holders of Secondary School Qualifications_2025_2026.pdf"
output_excel = "tcu_data_new.xlsx"

all_data = []

with pdfplumber.open(pdf_path) as pdf:
    current_university = "Unknown University"
    
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables(table_settings={"text_x_tolerance": 1.5})
        for table in tables:
            if not table or len(table) < 2:
                continue
                
            for row in table:
                cleaned_row = [str(cell).replace('\n', ' ').strip() if cell else "" for cell in row]
                
                # Filter out completely empty rows
                non_empty = [c for c in cleaned_row if c != ""]
                if not non_empty:
                    continue
                
                # Check for University header
                first_cell = non_empty[0]
                if len(non_empty) <= 2 and len(first_cell) > 10 and "Programme" not in first_cell:
                    # Check if it has keyword
                    if any(kw in first_cell for kw in ["University", "College", "Institute", "Centre", "Academy", "School", "Agency"]):
                        current_university = first_cell
                        continue
                
                if len(cleaned_row) > 1 and "Programme" in cleaned_row[1]:
                    continue
                
                # Check if it's a course row
                if len(cleaned_row) >= 4 and cleaned_row[0].strip().replace('.', '').isdigit():
                    programme = cleaned_row[1]
                    code = cleaned_row[2]
                    requirements = cleaned_row[3]
                    duration = cleaned_row[-1] if len(cleaned_row) > 4 else ""
                    
                    all_data.append({
                        "University": current_university,
                        "Programme": programme,
                        "Code": code,
                        "Requirements": requirements,
                        "Duration": duration
                    })

df = pd.DataFrame(all_data)
# Filter out "Unknown University" which are usually table of contents
df = df[df['University'] != 'Unknown University']
df = df.reset_index(drop=True)

# Save
df.to_excel(output_excel, index=False)
print(f"Jumla ya kozi zilizopatikana: {len(df)}")
print(f"Jumla ya vyuo: {df['University'].nunique()}")
