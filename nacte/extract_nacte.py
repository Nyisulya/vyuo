import pdfplumber
import pandas as pd
import re
import os

pdf_path = "nacte_guidebook.pdf"
output_excel = "nacte_data.xlsx"

all_data = []

print("Kuanza kusoma PDF ya NACTE (iliyoboreshwa), tafadhali subiri...")

if not os.path.exists(pdf_path):
    print(f"KOSA: Sioni faili la '{pdf_path}'.")
    exit()

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
                first_cell = cleaned_row[0] if len(cleaned_row) > 0 else ""
                
                # Check for table header
                if len(cleaned_row) > 1 and "Program Name" in cleaned_row[1]:
                    continue
                
                filled_cells = [c for c in cleaned_row if c.strip()]
                
                # Check for University header (anything that doesn't start with a number, has <= 2 cols)
                if first_cell and not re.match(r'^\d+', first_cell.strip()):
                    if "GMT+" in first_cell or "Time)" in first_cell or "Page" in first_cell:
                        continue
                    elif "S/N" not in first_cell and "Program" not in first_cell and len(filled_cells) <= 2:
                        # Extract university name. Since some cells contain "Uni Name - Private\nRegion", we split by newline and dash
                        clean_text = first_cell.split('\n')[0]
                        parts = clean_text.split('-')
                        if len(parts) > 1:
                            current_university = parts[0].strip()
                        else:
                            current_university = clean_text.strip()
                        continue

                # Kama ni row mpya ya data (Ina S/N)
                if len(cleaned_row) >= 6 and cleaned_row[0].replace('.', '').isdigit():
                    # Save the previous row before starting a new one
                    if current_row_data:
                        all_data.append(current_row_data)
                        
                    fee = cleaned_row[5]
                    fee_clean = 0
                    fee_str = re.sub(r'[^\d]', '', fee.split('Foreign')[0] if 'Foreign' in fee else fee)
                    if fee_str:
                        fee_clean = int(fee_str)

                    current_row_data = {
                        "University": current_university,
                        "Region": current_region,
                        "Ownership": ownership,
                        "Programme": cleaned_row[1],
                        "Requirements": cleaned_row[2],
                        "Duration": cleaned_row[3],
                        "Capacity": cleaned_row[4],
                        "Fee": fee_clean
                    }
                # Kama ni muendelezo wa row iliyopita (Haina S/N lakini ina data)
                elif current_row_data and len(cleaned_row) >= 3 and not first_cell:
                    # Append text to existing fields
                    if cleaned_row[1]:
                        current_row_data["Programme"] += " " + cleaned_row[1]
                    if cleaned_row[2]:
                        current_row_data["Requirements"] += " " + cleaned_row[2]
                    # Update other fields if they exist
                    if len(cleaned_row) > 3 and cleaned_row[3]:
                        if current_row_data["Duration"] and current_row_data["Duration"] != cleaned_row[3]:
                             current_row_data["Duration"] += f" / {cleaned_row[3]}"
                        else:
                             current_row_data["Duration"] = cleaned_row[3]
                    if len(cleaned_row) > 5 and cleaned_row[5] and current_row_data["Fee"] == 0:
                        fee = cleaned_row[5]
                        fee_str = re.sub(r'[^\d]', '', fee.split('Foreign')[0] if 'Foreign' in fee else fee)
                        if fee_str:
                            current_row_data["Fee"] = int(fee_str)

    # Save the very last row
    if current_row_data:
        all_data.append(current_row_data)

df = pd.DataFrame(all_data)
df.to_excel(output_excel, index=False)

print(f"\nImekamilika! Faili limehifadhiwa kama {output_excel}")
print(f"Jumla ya kozi zilizopatikana: {len(df)}")
