import os
import sys
import django
from django.db import transaction, IntegrityError

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Course, UniversityCourse

def determine_course_level(course_name):
    name_lower = course_name.lower().strip()
    words = name_lower.split()
    if not words:
        return 'Diploma'
        
    first_word = words[0]
    
    # Degree indicators
    degree_prefixes = ('bachelor', 'bsc', 'b.sc', 'doctor', 'md', 'phd', 'master', 'postgraduate')
    if first_word.startswith(degree_prefixes) or first_word in ('ba', 'b.a'):
        return 'Degree'
        
    # Check if contains 'degree' (e.g. "undergraduate degree in...")
    if 'degree' in name_lower:
        return 'Degree'
        
    # Certificate indicators
    if 'certificate' in name_lower or 'astastahiki' in name_lower:
        return 'Certificate'
        
    return 'Diploma'

def update_levels():
    print("Inaanza kusahihisha level za kozi zilizopo kwenye database...")
    
    courses = UniversityCourse.objects.select_related('course', 'university').all()
    total_checked = 0
    total_updated = 0
    
    for uc in courses:
        total_checked += 1
        new_level = determine_course_level(uc.course.name)
        
        if uc.level != new_level:
            print(f"Inabadilisha: {uc.university.name} - {uc.course.name}")
            print(f"   Kutoka Level: '{uc.level}' kwenda '{new_level}'")
            
            # Check for unique_together constraint conflict
            duplicate = UniversityCourse.objects.filter(
                university=uc.university,
                course=uc.course,
                level=new_level
            ).first()
            
            if duplicate:
                print(f"   [!] Conflict: Kozi hii yenye level '{new_level}' tayari ipo. Inafuta ya zamani ili kuweka mpya...")
                # Keep the one with fee or requirements if present
                if not uc.fee and duplicate.fee:
                    uc.fee = duplicate.fee
                if not uc.requirements and duplicate.requirements:
                    uc.requirements = duplicate.requirements
                duplicate.delete()
            
            uc.level = new_level
            try:
                uc.save()
                total_updated += 1
            except Exception as e:
                print(f"   [Error] Imeshindikana kusave: {e}")
                
    print(f"\nUrekebishaji umekamilika! Zilizochekiwa: {total_checked}, Zilizorekebishwa: {total_updated}")

if __name__ == '__main__':
    update_levels()
