import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University, Course, Requirement, UniversityCourse

def wipe_all():
    print("Inafuta data zote kwenye database (Vyuo, Kozi, Sifa, na Viungo vyake)...")
    
    # Futa data zote
    UniversityCourse.objects.all().delete()
    Requirement.objects.all().delete()
    Course.objects.all().delete()
    University.objects.all().delete()
    
    print("Database yako ni NYEUPE sasa (Hakuna data iliyobaki)!")

if __name__ == "__main__":
    user_input = input("Onyo: Hii itafuta data zote (Vyuo, Kozi) ulizoingiza kwa mkono. Je, unakubali? (ndio/hapana): ")
    if user_input.lower() == 'ndio':
        wipe_all()
    else:
        print("Imesitishwa. Hakuna kilichofutwa.")
