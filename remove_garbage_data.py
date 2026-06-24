import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University, UniversityCourse, Course

def run_cleanup():
    print("="*60)
    print("INASAFISHA VYUO NA KOZI TAKATAKA...")
    print("="*60)
    
    # 1. Kufuta kozi zilizo 'nusu'
    bad_endings = [' and', ' in', ' of', ' for', ' with', ' or']
    all_uni_courses = UniversityCourse.objects.all()
    deleted_courses = 0
    
    for uc in all_uni_courses:
        c_name = uc.course.name.lower().strip()
        if any(c_name.endswith(end) for end in bad_endings) or len(c_name) < 5:
            print(f"Inafuta kozi nusu: {uc.course.name}")
            uc.delete()
            deleted_courses += 1
            
    print(f"\nJumla ya kozi 'nusu' zilizofutwa: {deleted_courses}\n")
    
    # 2. Kufuta vyuo ambavyo ni 'takataka' (havina maana)
    # Kwa mfano vinaanza na '(ACSEE)' au vina maneno 'pass', 'advantage'
    bad_keywords = ['acsee', 'principal pass', 'subsidiary', 'advantage', 'mathematics', 'administration.', 'subjects.', 'chemistry and biology']
    all_unis = University.objects.all()
    deleted_unis = 0
    
    for u in all_unis:
        u_name = u.name.lower()
        if any(kw in u_name for kw in bad_keywords) or len(u.name.strip()) <= 2:
            print(f"Inafuta chuo takataka: {u.name}")
            u.delete()
            deleted_unis += 1
            
    print(f"\nJumla ya vyuo takataka vilivyofutwa: {deleted_unis}\n")
    
    # 3. Kufuta vyuo visivyo na kozi yoyote
    empty_unis = University.objects.filter(universitycourse__isnull=True)
    empty_count = empty_unis.count()
    if empty_count > 0:
        print(f"Inafuta vyuo {empty_count} visivyo na kozi yoyote...")
        empty_unis.delete()
        
    print("="*60)
    print("USAFI UMEKAMILIKA! Database yako sasa ni safi.")
    print("="*60)

if __name__ == '__main__':
    run_cleanup()
