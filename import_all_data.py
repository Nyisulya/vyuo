import os
import django
import pandas as pd

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Region, University, Course, UniversityCourse

def import_data():
    excel_file = "all.xlsx"
    
    print(f"Ninasoma faili la Excel: {excel_file}...")
    df = pd.read_excel(excel_file)
    
    total_imported = 0
    total_skipped = 0
    
    for index, row in df.iterrows():
        uni_name = str(row.get('Jina la chuo', '')).strip()
        region_name = str(row.get('Mkoa', '')).strip()
        umiliki = str(row.get('Umiliki (private/government)', '')).strip()
        course_name = str(row.get('Courses', '')).strip()
        req_text = str(row.get('Requirements', '')).strip()
        duration_val = str(row.get('Duration', '')).strip()
        uni_type = str(row.get('Type (university/institute)', '')).strip()
        
        # Skip empty rows
        if uni_name == 'nan' or not uni_name or course_name == 'nan' or not course_name:
            total_skipped += 1
            continue
            
        # Clean duration
        try:
            if duration_val != 'nan' and duration_val:
                dur_int = int(float(duration_val))
                duration_str = str(dur_int)
                if duration_str not in ['1', '2', '3', '4', '5']:
                    duration_str = '3'
            else:
                duration_str = '3'
        except:
            duration_str = '3'
            
        # 1. Mkoa (Region)
        if region_name and region_name != 'nan':
            region_name_clean = region_name[:70]
        else:
            region_name_clean = "Tanzania"
            
        region, _ = Region.objects.get_or_create(name=region_name_clean)
        
        # 2. Chuo (University)
        uni_name_clean = uni_name[:150]
        uni_type = uni_type[:40] if uni_type != 'nan' else None
        
        # Fix Umiliki strings (e.g. "Public" instead of "Government" if present)
        umiliki = umiliki[:30] if umiliki != 'nan' else None
        if umiliki and umiliki.lower() == 'public':
            umiliki = 'Goverment' # Based on models.py TYPE_UNIVER
        
        university, uni_created = University.objects.get_or_create(
            name=uni_name_clean,
            defaults={
                'region': region,
                'type': uni_type,
                'umiliki': umiliki
            }
        )
        
        # Update existing university if needed
        if not uni_created:
            updated = False
            if uni_type and not university.type:
                university.type = uni_type
                updated = True
            if umiliki and not university.umiliki:
                university.umiliki = umiliki
                updated = True
            if region and university.region != region:
                university.region = region
                updated = True
            if updated:
                university.save()
        
        # 3. Kozi (Course)
        course_name_clean = course_name[:140]
        course, course_created = Course.objects.get_or_create(
            name=course_name_clean
        )
        
        # 4. UniversityCourse
        req_text = req_text if req_text != 'nan' else ""
        
        # Try to get or create
        uni_course, uc_created = UniversityCourse.objects.get_or_create(
            university=university,
            course=course,
            level="Degree",
            defaults={
                'duration': duration_str,
                'requirements': req_text
            }
        )
        
        if not uc_created:
            # Update
            uni_course.duration = duration_str
            uni_course.requirements = req_text
            uni_course.save()
            
        total_imported += 1
        
        if total_imported % 100 == 0:
            print(f"Kozi {total_imported} zimeingizwa kwenye database...")

    print(f"\nZoezi limekamilika! Jumla ya kozi {total_imported} zimesomwa/zimewekwa kikamilifu. Skipped: {total_skipped}")

if __name__ == "__main__":
    import_data()
