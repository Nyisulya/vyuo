"""
Script ya kuongeza kozi za vyuo vilivyokosekana:
1. Dr. Salim Ahmed Salim Centre for Foreign Relations (CFR), Dar es Salaam
2. Dar es Salaam Institute of Technology (DIT), Dar es Salaam
3. Dar es Salaam Institute of Technology (DIT), Mwanza Campus

Data imetolewa kutoka kwenye kitabu cha TCU (Admission Guidebook 2025/2026).

MAELEKEZO: Endesha hii kwenye VPS:
  python add_dit_cfr_courses.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Region, University, Course, Requirement, UniversityCourse


def add_courses():
    # ==========================================
    # 1. CFR - Centre for Foreign Relations
    # ==========================================
    cfr_region, _ = Region.objects.get_or_create(name="Dar es Salaam")
    cfr_uni, cfr_created = University.objects.get_or_create(
        name="Dr. Salim Ahmed Salim Centre for Foreign Relations (CFR), Dar es Salaam",
        defaults={
            'region': cfr_region,
            'type': 'Non University',
            'umiliki': 'Goverment',
            'is_active': True,
        }
    )
    if cfr_created:
        print(f"✓ Chuo kimeongezwa: {cfr_uni.name}")
    else:
        print(f"  Chuo tayari kipo: {cfr_uni.name}")

    cfr_courses = [
        {
            'name': 'Bachelor Degree in International Relations and Diplomacy',
            'code': 'CFR01',
            'requirements': 'Two principal passes in the following subjects: History, Geography, Kiswahili, English Language, Literature in English, French, Arabic, Fine Arts, Economics, Commerce, Accountancy, Physics, Chemistry, Biology, Advanced Mathematics, Agriculture, Computer Science or Nutrition.',
            'duration': '3',
        },
        {
            'name': 'Bachelor Degree in Governance and Strategic Leadership',
            'code': 'CFR02',
            'requirements': 'Two principal passes in the following subjects: History, Geography, Kiswahili, English Language, Literature in English, French, Arabic, Fine Arts, Economics, Commerce, Accountancy, Physics, Chemistry, Biology, Advanced Mathematics, Agriculture, Computer Science or Nutrition.',
            'duration': '3',
        },
    ]

    # ==========================================
    # 2. DIT Dar es Salaam
    # ==========================================
    dit_region, _ = Region.objects.get_or_create(name="Dar es Salaam")
    dit_uni, dit_created = University.objects.get_or_create(
        name="Dar es Salaam Institute of Technology (DIT), Dar es Salaam",
        defaults={
            'region': dit_region,
            'type': 'Institute',
            'umiliki': 'Goverment',
            'website': 'www.dit.ac.tz',
            'is_active': True,
        }
    )
    if dit_created:
        print(f"✓ Chuo kimeongezwa: {dit_uni.name}")
    else:
        print(f"  Chuo tayari kipo: {dit_uni.name}")

    dit_dar_courses = [
        {
            'name': 'Bachelor of Engineering in Civil Engineering',
            'code': 'DT001',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
            'duration': '4',
        },
        {
            'name': 'Bachelor of Engineering in Computer Engineering',
            'code': 'DT002',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
            'duration': '4',
        },
        {
            'name': 'Bachelor of Engineering in Electrical Engineering',
            'code': 'DT003',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
            'duration': '4',
        },
        {
            'name': 'Bachelor of Engineering in Electronics and Telecommunication Engineering',
            'code': 'DT004',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
            'duration': '4',
        },
        {
            'name': 'Bachelor of Engineering in Mechanical Engineering',
            'code': 'DT005',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
            'duration': '4',
        },
        {
            'name': 'Bachelor of Engineering in Oil and Gas Engineering',
            'code': 'DT006',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics.',
            'duration': '4',
        },
        {
            'name': 'Bachelor of Technology in Laboratory Science',
            'code': 'DT007',
            'requirements': 'Two principal passes in the following subjects: Advanced Mathematics, Physics, Chemistry and Biology, with not less than four passes at O-Level including Basic Mathematics and Physics with an institutional minimum point of 4.0.',
            'duration': '3',
        },
        {
            'name': 'Bachelor of Mining Engineering',
            'code': 'DT008',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics.',
            'duration': '4',
        },
        {
            'name': 'Bachelor of Engineering in Biomedical Engineering',
            'code': 'DT009',
            'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant MUST HAVE at least a pass in Basic Mathematics and Physics at O-Level.',
            'duration': '4',
        },
    ]

    # ==========================================
    # 3. DIT Mwanza Campus
    # ==========================================
    mwanza_region, _ = Region.objects.get_or_create(name="Mwanza")
    dit_mwanza, dit_mwanza_created = University.objects.get_or_create(
        name="Dar es Salaam Institute of Technology (DIT), Mwanza Campus",
        defaults={
            'region': mwanza_region,
            'type': 'Institute',
            'umiliki': 'Goverment',
            'website': 'www.dit.ac.tz',
            'is_active': True,
        }
    )
    if dit_mwanza_created:
        print(f"✓ Chuo kimeongezwa: {dit_mwanza.name}")
    else:
        print(f"  Chuo tayari kipo: {dit_mwanza.name}")

    dit_mwanza_courses = [
        {
            'name': 'Bachelor of Technology in Laboratory Science',
            'code': 'DTM001',
            'requirements': 'Two principal passes in the following subjects: Advanced Mathematics, Physics, Chemistry and Biology.',
            'duration': '3',
        },
    ]

    # ==========================================
    # IMPORT FUNCTION
    # ==========================================
    def import_courses(university, courses_data):
        count = 0
        for c in courses_data:
            # Course
            course, _ = Course.objects.get_or_create(name=c['name'][:140])

            # Requirement
            req_title = f"Sifa za kujiunga {c['name']}"[:100]
            requirement = Requirement.objects.create(
                title=req_title,
                description=c['requirements']
            )

            # UniversityCourse
            uc, uc_created = UniversityCourse.objects.get_or_create(
                university=university,
                course=course,
                level="Degree",
                defaults={
                    'duration': c['duration'],
                    'requirements': requirement,
                }
            )
            if uc_created:
                print(f"  ✓ Kozi imeongezwa: {c['name']} ({c['code']})")
                count += 1
            else:
                # Update requirements
                uc.requirements = requirement
                uc.duration = c['duration']
                uc.save()
                print(f"  ↻ Kozi imesasishwa: {c['name']} ({c['code']})")
                count += 1
        return count

    total = 0
    print(f"\n--- Kuingiza kozi za CFR ---")
    total += import_courses(cfr_uni, cfr_courses)

    print(f"\n--- Kuingiza kozi za DIT Dar es Salaam ---")
    total += import_courses(dit_uni, dit_dar_courses)

    print(f"\n--- Kuingiza kozi za DIT Mwanza ---")
    total += import_courses(dit_mwanza, dit_mwanza_courses)

    print(f"\n{'='*60}")
    print(f"IMEKAMILIKA! Jumla ya kozi zilizoingizwa: {total}")
    print(f"{'='*60}")


if __name__ == '__main__':
    add_courses()
