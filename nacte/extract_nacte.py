import pdfplumber
import pandas as pd
import re
import os

# Jina la PDF yako ya NACTE. Hakikisha umeweka file hili kwenye folder hili la 'nacte'
pdf_path = "nacte_guidebook.pdf"
output_excel = "nacte_data.xlsx"

all_data = []

print("Kuanza kusoma PDF ya NACTE, tafadhali subiri...")

# Kama file halipo, toa taarifa
if not os.path.exists(pdf_path):
    print(f"KOSA: Sioni faili la '{pdf_path}'. Tafadhali weka PDF ya NACTE kwenye folder hili.")
    exit()

with pdfplumber.open(pdf_path) as pdf:
    current_university = "Unknown University"
    current_region = "Unknown Region"
    ownership = "Unknown"
    
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables(table_settings={"text_x_tolerance": 1.5})
        for table in tables:
            if not table or len(table) < 2:
                continue
                
            for row in table:
                # Safisha row kwa kutoa newline na None
                cleaned_row = [str(cell).replace('\n', ' ').strip() if cell else "" for cell in row]
                
                # Angalia kama ni row ya Chuo (Mara nyingi NACTE inaweka jina la chuo kama heading inayochukua mstari mzima)
                # Mfano: "ABDULRAHMAN AL- SUMAIT UNIVERSITY (U/TLF/11) - Private"
                first_cell = cleaned_row[0] if len(cleaned_row) > 0 else ""
                
                # Check kama ni header ya table yenyewe (tuiruke)
                if len(cleaned_row) > 1 and "Program Name" in cleaned_row[1]:
                    continue
                
                # Kama cell ya kwanza haina namba ya S/N na ina maneno mengi, huenda ikawa ni taarifa ya chuo
                if first_cell and not first_cell.replace('.', '').isdigit():
                    if "UNIVERSITY" in first_cell.upper() or "COLLEGE" in first_cell.upper() or "INSTITUTE" in first_cell.upper() or "CENTRE" in first_cell.upper():
                        # Inaweza kuwa jina la chuo limetenganishwa na aina ya umiliki kwa "-"
                        parts = first_cell.split('-')
                        if len(parts) > 1:
                            current_university = parts[0].strip()
                            ownership = parts[-1].strip() # Mfano: "Private" au "FBO" au "Government"
                        else:
                            current_university = first_cell.strip()
                        continue
                    elif "District" in first_cell or "Region" in first_cell or "Council" in first_cell:
                        # Mstari unaofuata baada ya jina la chuo kawaida ni Wilaya na Mkoa
                        # Mfano: "Magharibi District - Zanzibar Urban/West"
                        parts = first_cell.split('-')
                        if len(parts) > 1:
                            current_region = parts[-1].strip()
                        else:
                            current_region = first_cell.strip()
                        continue

                # Kama ni row ya data (S/N ni namba)
                if len(cleaned_row) >= 6 and cleaned_row[0].replace('.', '').isdigit():
                    programme = cleaned_row[1] # Ordinary Diploma in...
                    requirements = cleaned_row[2]
                    duration = cleaned_row[3]
                    capacity = cleaned_row[4]
                    fee = cleaned_row[5]
                    
                    # Kusafisha fee, kutoa "TSH." na "/=" au "USD" nk.
                    # Mfano: "Local Fee: TSH. 750,000/="
                    fee_clean = 0
                    if "750,000" in fee: # Mfano tu wa kutengeneza logic, unaweza kuboresha na regex
                        fee_str = re.sub(r'[^\d]', '', fee.split('Foreign')[0]) # Chukua local fee pekee (namba tu)
                        if fee_str:
                            fee_clean = int(fee_str)
                    else:
                        # Regex ya kuchukua namba zote kabla ya "Foreign"
                        local_fee_part = fee.split('Foreign')[0] if 'Foreign' in fee else fee
                        fee_str = re.sub(r'[^\d]', '', local_fee_part)
                        if fee_str:
                            fee_clean = int(fee_str)

                    all_data.append({
                        "University": current_university,
                        "Region": current_region,
                        "Ownership": ownership,
                        "Programme": programme, # Tunaiacha hivyo hivyo "Ordinary Diploma..."
                        "Requirements": requirements,
                        "Duration": duration,
                        "Capacity": capacity,
                        "Fee": fee_clean
                    })

        if (i+1) % 50 == 0:
            print(f"Kurasa {i+1} zimesomwa...")

df = pd.DataFrame(all_data)
df.to_excel(output_excel, index=False)

print(f"\nImekamilika! Faili limehifadhiwa kama {output_excel}")
print(f"Jumla ya kozi zilizopatikana: {len(df)}")
