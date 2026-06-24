import os
import sys
import django
import pandas as pd
import re

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Region, University, Course, Requirement, UniversityCourse

def clean_uni_name(name):
    # This should be the same logic as cleanup_nacte_vps.py
    # But for seed, we probably want to keep the name readable (with punctuation)
    # However, to avoid creating new duplicates if one exists without punctuation, 
    # the best way is to lookup the DB by the normalized name. 
    # If a match is found, we use the DB's existing name. 
    # If no match, we use the raw readable name (with REG removed).
    
    name = str(name).strip()
    name = re.sub(r'\([^\)]+\)$', '', name).strip()
    name = re.sub(r'\(REG/[^\)]+\)', '', name).strip()
    return name[:150]

def normalize_name_for_search(name):
    name = str(name).strip().upper()
    name = re.sub(r'\([^\)]+\)$', '', name).strip()
    name = re.sub(r'\(REG/[^\)]+\)', '', name).strip()
    name = name.replace('(IAA)', '')
    name = name.replace('(IFM)', '')
    name = name.replace('(KCDI)', '')
    name = name.replace('(NCT)', '')
    name = name.replace('(TPSC)', '')
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if name == 'TABORA EA POLYTECHNIC COLLEGE':
        name = 'TABORA EAST AFRICA POLYTECHNIC COLLEGE'
    return name

def get_or_create_university(raw_name, region, ownership):
    readable_clean_name = clean_uni_name(raw_name)
    normalized_name = normalize_name_for_search(readable_clean_name)
    
    # Try to find existing university by normalized name
    all_unis = University.objects.all()
    for u in all_unis:
        if normalize_name_for_search(u.name) == normalized_name:
            # Found a match! Return it to avoid duplicating.
            return u, False
            
    # If not found, create it using the readable clean name
    university, created = University.objects.get_or_create(
        name=readable_clean_name,
        defaults={
            'region': region,
            'type': 'Institute', 
            'umiliki': ownership
        }
    )
    return university, created

def seed_nacte_data(excel_path):
    print(f"Tunasoma data kutoka: {excel_path} ...")
    df = pd.read_excel(excel_path)
    
    # Tunahesabu ili kujua ngapi zimeingia au kusasishwa
    added = 0
    updated = 0

    for index, row in df.iterrows():
        # Hakikisha majina yamekamilika
        raw_uni_name = str(row['University']).strip()
        region_name = str(row['Region']).strip()[:70]
        prog_name = str(row['Programme']).strip()[:140]
        req_desc = str(row['Requirements']).strip()
        ownership = str(row['Ownership']).strip()[:30]
        duration = str(row['Duration']).strip()[:10]
        
        # Kuhakikisha fee haina makosa kama ni NaN (Not a Number)
        fee_value = row['Fee']
        if pd.isna(fee_value) or fee_value == "":
            fee_value = 0
            
        if raw_uni_name == "Unknown University" or prog_name == "nan" or prog_name == "":
            continue # Ruka mistari ambayo haina data kamili
            
        # 1. Pata au Tengeneza Mkoa
        region, _ = Region.objects.get_or_create(name=region_name)
        
        # 2. Pata au Tengeneza Chuo (Kwa kutumia normalized search kuzuia ST vs ST.)
        university, uni_created = get_or_create_university(raw_uni_name, region, ownership)
        
        # 3. Pata au Tengeneza Kozi
        course, _ = Course.objects.get_or_create(
            name=prog_name
        )
        
        # 4. Pata au Tengeneza Vigezo (Requirements)
        requirement, _ = Requirement.objects.get_or_create(
            description=req_desc
        )
        
        # 5. Unganisha Chuo na Kozi (UniversityCourse)
        uc, uc_created = UniversityCourse.objects.update_or_create(
            university=university,
            course=course,
            level='Diploma',
            defaults={
                'duration': duration,
                'fee': fee_value,
                'requirements': requirement
            }
        )
        
        if uc_created:
            added += 1
        else:
            updated += 1
            
    print(f"KAZI IMEKAMILIKA!")
    print(f"Kozi mpya zilizoongezwa: {added}")
    print(f"Kozi zilizofanyiwa update (Zilikuwepo): {updated}")

if __name__ == '__main__':
    excel_file = 'nacte_data2.xlsx'
    if not os.path.exists(excel_file):
        # We need the absolute path just in case they run it from root dir
        current_dir = os.path.dirname(os.path.abspath(__file__))
        excel_file = os.path.join(current_dir, 'nacte_data2.xlsx')
        
    if not os.path.exists(excel_file):
        print(f"Faili la Excel '{excel_file}' halipo. Tafadhali run 'extract_nacte2.py' kwanza.")
    else:
        seed_nacte_data(excel_file)
