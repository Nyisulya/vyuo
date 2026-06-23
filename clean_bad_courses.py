import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Course, UniversityCourse

def clean_courses():
    bad_keywords = [
        'University', 'College', 'Institute', 'Academy', 'window', 
        'Publication', 'Announcement', 'Centre', 'Campus', 'Cooperation'
    ]
    
    courses_to_delete = []
    
    # We must be careful not to delete real courses. 
    # Usually, real courses start with "Bachelor", "Diploma", "Certificate", "Ordinary", "Technician", "Master", "PhD", "BSc", "BA"
    good_prefixes = ['bachelor', 'diploma', 'certificate', 'ordinary', 'technician', 'master', 'phd', 'bsc', 'ba', 'md', 'doctor', 'b.']
    
    all_courses = Course.objects.all()
    
    for c in all_courses:
        name_lower = c.name.lower()
        
        # If it has a bad keyword
        has_bad_keyword = any(kw.lower() in name_lower for kw in bad_keywords)
        
        # If it doesn't start with a good prefix
        starts_with_good = any(name_lower.startswith(pfx) for pfx in good_prefixes)
        
        if has_bad_keyword and not starts_with_good:
            courses_to_delete.append(c)
        elif 'window' in name_lower or 'announcement' in name_lower or 'publication' in name_lower or 'admission' in name_lower:
            # Delete these unconditionally if they don't look like a course at all
            if c not in courses_to_delete:
                courses_to_delete.append(c)

    print(f"Tumepata kozi {len(courses_to_delete)} ambazo zinaonekana kuwa ni majina ya vyuo au matangazo.")
    for c in courses_to_delete:
        print(f" - Inafutwa: {c.name}")
        
        # Futa UniversityCourse zilizounganishwa nayo
        UniversityCourse.objects.filter(course=c).delete()
        # Futa kozi yenyewe
        c.delete()
        
    print("\nUsafishaji umekamilika!")

if __name__ == '__main__':
    clean_courses()
