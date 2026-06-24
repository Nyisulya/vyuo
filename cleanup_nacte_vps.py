"""
Script kwa ajili ya kusafisha database kwenye VPS kabla ya ku-run seed scripts mpya.
1. Inafuta "Unknown University" na kozi zake (zitaingizwa upya na seed_nacte.py)
2. Ina-merge vyuo vilivyo duplicate (mf. ST. JOSEPH na ST JOSEPH, au vyenye (REG/...)) kwenda kwenye jina kuu

MALEKEZO: Endesha hii kwenye VPS kabla ya seed scripts
  python cleanup_nacte_vps.py
"""
import os
import sys
import django
import re

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University, UniversityCourse

def clean_uni_name(name):
    name = str(name).strip().upper()
    
    # Remove REG/... or other parenthetical stuff at the end or anywhere
    name = re.sub(r'\([^\)]+\)$', '', name).strip()
    name = re.sub(r'\(REG/[^\)]+\)', '', name).strip()
    
    # Remove common abbreviations that cause duplicates
    name = name.replace('(IAA)', '')
    name = name.replace('(IFM)', '')
    name = name.replace('(KCDI)', '')
    name = name.replace('(NCT)', '')
    name = name.replace('(TPSC)', '')
    
    # Remove punctuation (like periods, commas)
    name = re.sub(r'[^\w\s]', '', name)
    
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Custom fixes for known hard duplicates
    if name == 'TABORA EA POLYTECHNIC COLLEGE':
        name = 'TABORA EAST AFRICA POLYTECHNIC COLLEGE'
        
    return name

def run_cleanup():
    print("=" * 60)
    print("1. KUFUTA 'Unknown University'")
    print("=" * 60)
    
    try:
        unknown = University.objects.get(name="Unknown University")
        courses_count = UniversityCourse.objects.filter(university=unknown).count()
        print(f"Imekutwa 'Unknown University' yenye kozi {courses_count}.")
        unknown.delete()
        print("✓ 'Unknown University' imefutwa kikamilifu!")
    except University.DoesNotExist:
        print("✓ Hakuna 'Unknown University' kwenye database.")
        
    print("\n" + "=" * 60)
    print("2. KU-MERGE VYUO DUPLICATE VYA NACTE")
    print("=" * 60)
    
    # Tunatafuta vyuo vyote vya NACTE (vyenye Institute au Non University au ambavyo sio vya TCU)
    all_unis = University.objects.all()
    
    # Group by clean name
    clean_to_unis = {}
    for u in all_unis:
        cleaned = clean_uni_name(u.name)
        if cleaned not in clean_to_unis:
            clean_to_unis[cleaned] = []
        clean_to_unis[cleaned].append(u)
        
    # Tafuta yenye duplicates
    merged_count = 0
    for cleaned_name, unis in clean_to_unis.items():
        if len(unis) > 1:
            print(f"\nDuplicate zimekutwa kwa: '{cleaned_name}'")
            # Chagua chuo kimoja kama "Base". 
            # Tunapendelea chenye jina fupi au kisicho na (REG)
            unis.sort(key=lambda x: len(x.name))
            
            # Kama kuna "ST." kwenye kimoja, pengine tunataka hicho kiwe base kwasababu ni rasmi zaidi, 
            # Lakini for now the shortest one is usually the cleanest.
            base_uni = unis[0]
            duplicates = unis[1:]
            
            print(f"  Base Uni: {base_uni.name}")
            
            for dup in duplicates:
                dup_courses = UniversityCourse.objects.filter(university=dup)
                count = dup_courses.count()
                print(f"  Kuhamisha kozi {count} kutoka '{dup.name}' kwenda kwa Base...")
                
                # Update course university
                for uc in dup_courses:
                    # Check if base already has this course at this level to avoid unique constraint
                    exists = UniversityCourse.objects.filter(
                        university=base_uni, 
                        course=uc.course, 
                        level=uc.level
                    ).exists()
                    
                    if exists:
                        # Kama tayari ipo, futa hii ya duplicate
                        uc.delete()
                    else:
                        # Kama haipo, hamishia kwa base
                        uc.university = base_uni
                        uc.save()
                        
                # Futa chuo duplicate
                dup.delete()
                merged_count += 1
                print(f"  ✓ Duplicate '{dup.name}' imefutwa!")
                
    print(f"\n{'=' * 60}")
    print(f"KAZI IMEKAMILIKA! Jumla ya vyuo duplicates {merged_count} vime-mergiwa.")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    run_cleanup()
