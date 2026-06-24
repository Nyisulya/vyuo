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
    Get clean name for comparison, ignoring parentheses with acronyms
    but keeping location/campus markers to avoid merging branches.
    """
    # Ondoa tu acronyms zilizo kwenye mabano kama (SAUT), (CBE) lakini baki na mikoa/kampasi
    clean_name = re.sub(r'\([A-Z\s]+\)', '', name)
    # Safisha nafasi zilizozidi
    clean_name = re.sub(r'\s+', ' ', clean_name).strip().lower()
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
            
            is_match = False
            # 1. Exact match ya jina lililosafishwa
            if base_clean == target_clean:
                is_match = True
            
            # 2. Substring match (Kama moja inaingia ndani ya nyingine na ni ndefu kiasi)
            if not is_match and len(base_clean) > 15:
                if base_clean in target_clean or target_clean in base_clean:
                    is_match = True
                    
            # 3. Fuzzy match kwa majina yanayokaribiana sana (kama tofauti ni the/of/abbreviations)
            if not is_match:
                import difflib
                similarity = difflib.SequenceMatcher(None, base_clean, target_clean).ratio()
                if similarity > 0.88:
                    is_match = True
            
            # Kama imekidhi vigezo vyote
            if is_match and len(base_clean) > 5:
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
