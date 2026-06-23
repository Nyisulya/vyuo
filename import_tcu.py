import os
import django
import pandas as pd

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Region, University, Course, Requirement, UniversityCourse

def import_data():
    excel_file = "tcu/tcu_data.xlsx"
    
    print("Ninasoma faili la Excel...")
    df = pd.read_excel(excel_file)
    
    # Hakikisha kuna default Region, kama haipo itengeneze
    default_region, created = Region.objects.get_or_create(name="Tanzania")
    
    total_imported = 0
    
    for index, row in df.iterrows():
        uni_name = str(row.get('University', '')).strip()
        prog_name = str(row.get('Programme', '')).strip()
        req_text = str(row.get('Requirements', '')).strip()
        duration_val = str(row.get('Duration', '')).strip()
        
        # Safisha Duration ibaki namba tu
        try:
            dur_int = int(float(duration_val))
            duration_str = str(dur_int)
            if duration_str not in ['1', '2', '3', '4', '5']:
                duration_str = '3' # Default
        except:
            duration_str = '3' # Default
            
        if not uni_name or not prog_name:
            continue
            
        # 1. Chuo (University)
        university, uni_created = University.objects.get_or_create(
            name=uni_name,
            defaults={'region': default_region}
        )
        
        # 2. Kozi (Course)
        course, course_created = Course.objects.get_or_create(
            name=prog_name
        )
        
        # 3. Requirement
        requirement = Requirement.objects.create(
            title=f"Sifa za kujiunga {prog_name}",
            description=req_text
        )
        
        # 4. UniversityCourse (Kiungo kikubwa)
        # Check if exists first because of unique_together = ['university','course','level']
        uni_course, uc_created = UniversityCourse.objects.get_or_create(
            university=university,
            course=course,
            level="Degree",
            defaults={
                'duration': duration_str,
                'requirements': requirement
            }
        )
        
        # If it already existed, update its requirements and duration
        if not uc_created:
            uni_course.duration = duration_str
            uni_course.requirements = requirement
            uni_course.save()
            
        total_imported += 1
        
        if total_imported % 100 == 0:
            print(f"Kozi {total_imported} zimeingizwa kwenye database...")

    print(f"\nZoezi limekamilika! Jumla ya kozi {total_imported} zimewekwa kwenye database kikamilifu.")

if __name__ == "__main__":
    import_data()
