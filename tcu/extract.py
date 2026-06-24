import pdfplumber
import pandas as pd
import os

pdf_path = "Admission Guidebook for Holders of Secondary School Qualifications_2025_2026.pdf"
output_excel = "tcu_data.xlsx"

all_data = []

print("Kuanza kusoma PDF, tafadhali subiri... (Hii inaweza kuchukua dakika kadhaa)")

with pdfplumber.open(pdf_path) as pdf:
    current_university = "Unknown University"
    
    # We skip first 20 pages or so which are usually introductions.
    # Let's process from page 20 to the end just to be safe, or just process all pages.
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables(table_settings={"text_x_tolerance": 1.5})
        for table in tables:
            # table is a list of lists (rows of columns)
            if not table or len(table) < 2:
                continue
                
            for row in table:
                # Clean up row (replace None with empty string and strip newlines)
                cleaned_row = [str(cell).replace('\n', ' ').strip() if cell else "" for cell in row]
                
                # Check if this row is a University Header
                # TCU tables often have the university name in the first row spanning all columns
                # So if the first cell has text and the rest are mostly empty, or it just looks like a header:
                if len(cleaned_row) > 0 and any(kw in cleaned_row[0] for kw in ["University", "College", "Institute", "Centre", "Center", "Academy", "Training"]) and "Programme" not in cleaned_row[0]:
                    current_university = cleaned_row[0]
                    continue
                
                # Check if it's the column header row, skip it
                if len(cleaned_row) > 1 and "Programme" in cleaned_row[1]:
                    continue
                
                # If it's a valid data row (S/N is usually a number)
                if len(cleaned_row) >= 4 and cleaned_row[0].strip().replace('.', '').isdigit():
                    programme = cleaned_row[1]
                    code = cleaned_row[2]
                    requirements = cleaned_row[3]
                    
                    # Some tables might have duration and capacity
                    duration = cleaned_row[-1] if len(cleaned_row) > 4 else ""
                    
                    all_data.append({
                        "University": current_university,
                        "Programme": programme,
                        "Code": code,
                        "Requirements": requirements,
                        "Duration": duration
                    })

        if (i+1) % 50 == 0:
            print(f"Peeji {i+1} zimesomwa...")

# Create DataFrame
df = pd.DataFrame(all_data)

# Save to Excel
df.to_excel(output_excel, index=False)

print(f"Imekamilika! Faili limehifadhiwa kama {output_excel}")
print(f"Jumla ya kozi zilizopatikana: {len(df)}")
