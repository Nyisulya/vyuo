import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University, Course, Requirement, UniversityCourse

def undo_import():
    print("Inafuta data zilizojirudia kutoka kwenye TCU script...")
    
    # 1. Futa Requirements zote zilizoingizwa na script
    # (Zilikuwa na title inayoanza na "Sifa za kujiunga")
    reqs = Requirement.objects.filter(title__startswith="Sifa za kujiunga ")
    reqs_count = reqs.count()
    reqs.delete() # Hii itafuta pia UniversityCourse zote zilizokuwa linked na hizi requirements (kwa sababu ya on_delete=CASCADE)
    
    # 2. Futa Vyuo (Universities) vilivyobaki tupu (Havina kozi yoyote)
    empty_unis = University.objects.filter(unicourse__isnull=True)
    unis_count = empty_unis.count()
    empty_unis.delete()
    
    # 3. Futa Kozi (Courses) zilizobaki tupu
    empty_courses = Course.objects.filter(program__isnull=True)
    courses_count = empty_courses.count()
    empty_courses.delete()
    
    print(f"Imefanikiwa! Imefuta:")
    print(f"- Requirements (na UniversityCourses zake): {reqs_count}")
    print(f"- Vyuo vipya vilivyokuwa vimejirudia: {unis_count}")
    print(f"- Kozi mpya zilizokuwa zimejirudia: {courses_count}")
    print("Database yako imerudi kama ilivyokuwa mwanzo safi kabisa!")

if __name__ == "__main__":
    undo_import()
