"""
Script kwa ajili ya kusafisha database kwenye VPS kabla ya ku-run seed scripts mpya.
1. Inafuta "Unknown University" na kozi zake (zitaingizwa upya na seed_nacte.py)
(Imeondolewa sehemu ya ku-merge ili kulinda data)

MALEKEZO: Endesha hii kwenye VPS kabla ya seed scripts
  python cleanup_nacte_vps.py
"""
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University, UniversityCourse

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
    print("KAZI IMEKAMILIKA! Data zako ziko salama.")
    print("Sasa unaweza ku-run: python nacte/seed_nacte.py")
    print("na python nacte/seed_nacte2.py")
    print("=" * 60)

if __name__ == '__main__':
    run_cleanup()
