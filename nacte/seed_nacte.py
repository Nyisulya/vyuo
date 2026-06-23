import os
import sys
import django
import pandas as pd

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Region, University, Course, Requirement, UniversityCourse

def seed_nacte_data(excel_path):
    print(f"Tunasoma data kutoka: {excel_path} ...")
    df = pd.read_excel(excel_path)
    
    # Tunahesabu ili kujua ngapi zimeingia au kusasishwa
    added = 0
    updated = 0

    for index, row in df.iterrows():
        # Hakikisha majina yamekamilika
        uni_name = str(row['University']).strip()
        region_name = str(row['Region']).strip()
        prog_name = str(row['Programme']).strip()
        req_desc = str(row['Requirements']).strip()
        ownership = str(row['Ownership']).strip()
        duration = str(row['Duration']).strip()
        
        # Kuhakikisha fee haina makosa kama ni NaN (Not a Number)
        fee_value = row['Fee']
        if pd.isna(fee_value) or fee_value == "":
            fee_value = 0
            
        if uni_name == "Unknown University" or prog_name == "nan" or prog_name == "":
            continue # Ruka mistari ambayo haina data kamili
            
        # 1. Pata au Tengeneza Mkoa
        region, _ = Region.objects.get_or_create(name=region_name)
        
        # 2. Pata au Tengeneza Chuo (Haitengenezi kama kipo)
        university, uni_created = University.objects.get_or_create(
            name=uni_name,
            defaults={
                'region': region,
                'type': 'Institute', # By default
                'umiliki': ownership
            }
        )
        
        # 3. Pata au Tengeneza Kozi (Itabaki kama "Ordinary Diploma in...")
        course, _ = Course.objects.get_or_create(
            name=prog_name
        )
        
        # 4. Pata au Tengeneza Vigezo (Requirements)
        requirement, _ = Requirement.objects.get_or_create(
            description=req_desc
        )
        
        # 5. Unganisha Chuo na Kozi (UniversityCourse)
        # Hapa update_or_create inazuia duplication!
        uc, uc_created = UniversityCourse.objects.update_or_create(
            university=university,
            course=course,
            level='Diploma', # Tunaweka Diploma kama default kwa kozi hizi
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
    excel_file = 'nacte_data.xlsx'
    if not os.path.exists(excel_file):
        print(f"Faili la Excel '{excel_file}' halipo. Tafadhali run 'extract_nacte.py' kwanza.")
    else:
        seed_nacte_data(excel_file)
