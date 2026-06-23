import os
import sys
import django
import re

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University, UniversityCourse

def get_clean_name(name):
    """
    Remove location markers like '- Dar es Salaam', ', Morogoro', '(Mbeya)'
    to get the core university name.
    """
    # Ondoa kila kitu kuanzia kwenye -, ( au ,
    clean_name = re.sub(r'[-,\(].*$', '', name).strip().lower()
    return clean_name

def merge_universities():
    unis = list(University.objects.all())
    # Pangilia kuanzia jina fupi (msingi) kwenda jina refu (lenye mkoa)
    unis.sort(key=lambda x: len(x.name))
    
    merged_count = 0
    
    print("Naanza kutafuta na kuunganisha vyuo vinavyofanana...")
    
    for i in range(len(unis)):
        base_uni = unis[i]
        # Hakikisha chuo hiki hakijafutwa kwenye mizunguko iliyopita
        if not University.objects.filter(id=base_uni.id).exists():
            continue
            
        base_clean = base_uni.name.lower().strip()
        
        for j in range(i+1, len(unis)):
            target_uni = unis[j]
            if not University.objects.filter(id=target_uni.id).exists():
                continue
                
            # Safisha jina la target kuondoa mkoa
            target_clean = get_clean_name(target_uni.name)
            
            # Kama jina la msingi linafanana na jina lililosafishwa la target
            if base_clean == target_clean and len(base_clean) > 5:
                print(f"\nNAUNGANISHA: '{target_uni.name}' INAINGIA NDANI YA '{base_uni.name}'")
                
                # 1. Hamishia kozi zote kwenye base_uni
                courses = UniversityCourse.objects.filter(university=target_uni)
                moved_courses = 0
                for course in courses:
                    # Hakikisha hatutengenezi duplicates za kozi chini ya chuo kimoja
                    if not UniversityCourse.objects.filter(university=base_uni, course=course.course, level=course.level).exists():
                        course.university = base_uni
                        course.save()
                        moved_courses += 1
                    else:
                        # Kama kozi tayari ipo kwenye base_uni, futa hii ya target_uni
                        course.delete()
                
                print(f"  -> Kozi {moved_courses} zimehamishiwa.")
                
                # 2. Kama base haina maelezo au mkoa, chukua za target
                updated = False
                if not base_uni.description and target_uni.description:
                    base_uni.description = target_uni.description
                    updated = True
                
                # Hakikisha chuo kinabaki na mkoa
                if not base_uni.region_id and target_uni.region_id:
                    base_uni.region = target_uni.region
                    updated = True
                    
                if updated:
                    base_uni.save()
                
                # 3. Futa target_uni (chuo chenye jina refu/mkoa)
                target_uni.delete()
                print(f"  -> '{target_uni.name}' imefutwa.")
                merged_count += 1
                
    print(f"\nKAZI IMEKAMILIKA! Vyuo {merged_count} vimeunganishwa kwa mafanikio bila kuharibu mfumo.")

if __name__ == '__main__':
    merge_universities()
