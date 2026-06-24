import pdfplumber
import pandas as pd
import re
import os

pdf_path = "nacte_guidebook.pdf"
output_excel = "nacte_data.xlsx"
all_data = []

print("Kuanza kusoma PDF ya NACTE, tafadhali subiri...")

with pdfplumber.open(pdf_path) as pdf:
    current_university = "Unknown University"
    current_region = "Unknown Region"
    ownership = "Unknown"
    current_row_data = None
    
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables(table_settings={"text_x_tolerance": 1.5, "text_y_tolerance": 1.5})
        for table in tables:
            if not table or len(table) < 2:
                continue
                
            for row in table:
                cleaned_row = [str(cell).replace('\n', ' ').strip() if cell else "" for cell in row]
                filled_cells = [c for c in cleaned_row if c.strip()]
                
                if not filled_cells:
                    continue
                    
                first_filled = filled_cells[0]
                
                # Check for University header: Needs to contain ' - Private' or ' - Public', 
                # OR be a long uppercase string.
                if "S/N" not in first_filled and "Program Name" not in first_filled and len(filled_cells) <= 2:
                    if "District" in first_filled or "Municipal" in first_filled or "City" in first_filled or "Council" in first_filled:
                        pass
                    elif " - " in first_filled or (first_filled.isupper() and len(first_filled) > 10):
                        if '-' in first_filled:
                            current_region = first_filled.split('-')[-1].strip()
                            clean_text = first_filled.split('\n')[0]
                            parts = clean_text.split('-')
                            if len(parts) > 1:
                                ownership = parts[1].strip()
                                current_university = parts[0].strip()
                        else:
                            current_university = first_filled.strip()
                        continue
                
                # Valid Data Row
                if len(cleaned_row) >= 6 and cleaned_row[0].replace('.', '').isdigit():
                    if current_row_data:
                        all_data.append(current_row_data)
                        
                    programme = cleaned_row[1]
                    code = cleaned_row[2]
                    duration = cleaned_row[3]
                    capacity = cleaned_row[4]
                    fee = cleaned_row[5]
                    
                    # Clean capacity and fee
                    cap_clean = 0
                    if capacity.isdigit():
                        cap_clean = int(capacity)
                        
                    fee_clean = 0
                    fee_str = re.sub(r'[^\d]', '', fee.split('Foreign')[0] if 'Foreign' in fee else fee)
                    if fee_str:
                        fee_clean = int(fee_str)
                        
                    current_row_data = {
                        "University": current_university,
                        "Region": current_region,
                        "Ownership": ownership,
                        "Programme": programme,
                        "Code": code,
                        "Duration": duration,
                        "Capacity": cap_clean,
                        "Fee": fee_clean,
                        "Requirements": ""
                    }
                    
                # Continuation row for requirements or programme name
                elif current_row_data and len(cleaned_row) >= 3 and not cleaned_row[0].replace('.', '').isdigit():
                    # Check if this row is just continuing the programme name (col 1) or reqs (col 2)
                    if cleaned_row[1]:
                        current_row_data["Programme"] += " " + cleaned_row[1]
                    if cleaned_row[2]:
                        current_row_data["Requirements"] += " " + cleaned_row[2]
                        
                    if len(cleaned_row) > 3 and cleaned_row[3]:
                        if current_row_data["Duration"] and current_row_data["Duration"] != cleaned_row[3]:
                             current_row_data["Duration"] = cleaned_row[3]
                             
                    if len(cleaned_row) > 5 and cleaned_row[5] and current_row_data["Fee"] == 0:
                        fee = cleaned_row[5]
                        fee_str = re.sub(r'[^\d]', '', fee.split('Foreign')[0] if 'Foreign' in fee else fee)
                        if fee_str:
                            current_row_data["Fee"] = int(fee_str)
                            
    if current_row_data:
        all_data.append(current_row_data)

        if (i+1) % 50 == 0:
            print(f"Peeji {i+1} zimesomwa...")

df = pd.DataFrame(all_data)
df.to_excel(output_excel, index=False)

print(f"Imekamilika! Faili limehifadhiwa kama {output_excel}")
print(f"Jumla ya kozi zilizopatikana: {len(df)}")
