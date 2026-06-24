"""
Script ya kuongeza courses za DIT na CFR ambazo hazikupatikana kwenye PDF extraction.
Hii script ni READ-ONLY kwanza - inaonyesha itakachofanya kabla ya kutekeleza.

Data imethibitishwa moja kwa moja kutoka PDF ukurasa 60-62 (DIT) na 43-44 (CFR).
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Region, University, Course, Requirement, UniversityCourse

# ============================================================
# DATA ILIYOTHIBITISHWA KUTOKA PDF
# ============================================================

DIT_DAR_COURSES = [
    {
        'programme': 'Bachelor of Engineering in Civil Engineering',
        'code': 'DT001',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
        'duration': '4',
    },
    {
        'programme': 'Bachelor of Engineering in Computer Engineering',
        'code': 'DT002',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
        'duration': '4',
    },
    {
        'programme': 'Bachelor of Engineering in Electrical Engineering',
        'code': 'DT003',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
        'duration': '4',
    },
    {
        'programme': 'Bachelor of Engineering in Electronics and Telecommunication Engineering',
        'code': 'DT004',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
        'duration': '4',
    },
    {
        'programme': 'Bachelor of Engineering in Mechanical Engineering',
        'code': 'DT005',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant must have at least a pass in Basic Mathematics and Physics at O-Level.',
        'duration': '4',
    },
    {
        'programme': 'Bachelor of Engineering in Oil and Gas Engineering',
        'code': 'DT006',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics.',
        'duration': '4',
    },
    {
        'programme': 'Bachelor of Technology in Laboratory Science',
        'code': 'DT007',
        'requirements': 'Two principal passes in Advanced Mathematics, Physics, Chemistry and Biology, with not less than four passes at O-Level including Basic Mathematics and Physics with an institutional minimum point of 4.0.',
        'duration': '3',
    },
    {
        'programme': 'Bachelor of Mining Engineering',
        'code': 'DT008',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics.',
        'duration': '4',
    },
    {
        'programme': 'Bachelor of Engineering in Biomedical Engineering',
        'code': 'DT009',
        'requirements': 'Two principal passes in Physics and Advanced Mathematics. An applicant MUST HAVE at least a pass in Basic Mathematics and Physics at O-Level.',
        'duration': '4',
    },
]

DIT_MWANZA_COURSES = [
    {
        'programme': 'Bachelor of Technology in Laboratory Science',
        'code': 'DTM001',
        'requirements': 'Two principal passes in Advanced Mathematics, Physics, Chemistry and Biology, with not less than four passes at O-Level, including Basic Mathematics and Physics.',
        'duration': '3',
    },
]

CFR_COURSES = [
    {
        'programme': 'Bachelor Degree in International Relations and Diplomacy',
        'code': 'CFR01',
        'requirements': 'Two principal passes in History, Geography, Kiswahili, English Language, Literature in English, French, Arabic, Fine Arts, Economics, Commerce, Accountancy, Physics, Chemistry, Biology, Advanced Mathematics, Agriculture, Computer Science or Nutrition.',
        'duration': '3',
    },
    {
        'programme': 'Bachelor Degree in Governance and Strategic Leadership',
        'code': 'CFR02',
        'requirements': 'Two principal passes in History, Geography, Kiswahili, English Language, Literature in English, French, Arabic, Fine Arts, Economics, Commerce, Accountancy, Physics, Chemistry, Biology, Advanced Mathematics, Agriculture, Computer Science or Nutrition.',
        'duration': '3',
    },
]

UNIVERSITIES_DATA = [
    {
        'name': 'Dar es Salaam Institute of Technology (DIT), Dar es Salaam',
        'region': 'Dar es Salaam',
        'courses': DIT_DAR_COURSES,
    },
    {
        'name': 'Dar es Salaam Institute of Technology (DIT), Mwanza Campus',
        'region': 'Mwanza',
        'courses': DIT_MWANZA_COURSES,
    },
    {
        'name': 'Dr. Salim Ahmed Salim Centre for Foreign Relations (CFR), Dar es Salaam',
        'region': 'Dar es Salaam',
        'courses': CFR_COURSES,
    },
]


def preview_or_import(do_import=False):
    total_courses = sum(len(u['courses']) for u in UNIVERSITIES_DATA)
    print(f"{'KUINGIZA' if do_import else 'PREVIEW (Hakuna kinachowekwa bado)'}")
    print(f"Vyuo: {len(UNIVERSITIES_DATA)}, Kozi: {total_courses}")
    print("="*60)

    for uni_data in UNIVERSITIES_DATA:
        print(f"\nCHUO: {uni_data['name']}")
        print(f"  Mkoa: {uni_data['region']}")
        print(f"  Kozi ({len(uni_data['courses'])}):")

        if do_import:
            region, _ = Region.objects.get_or_create(name=uni_data['region'])
            university, uni_created = University.objects.get_or_create(
                name=uni_data['name'],
                defaults={'region': region, 'type': 'Institute', 'umiliki': 'Goverment', 'is_active': True}
            )
            if uni_created:
                print(f"  [KIPYA] Chuo kimetengenezwa")
            else:
                print(f"  [TAYARI KIPO] Chuo kinapatikana")

        for c in uni_data['courses']:
            print(f"    - [{c['code']}] {c['programme']} (Miaka: {c['duration']})")

            if do_import:
                course, _ = Course.objects.get_or_create(name=c['programme'][:140])
                req, _ = Requirement.objects.get_or_create(
                    description=c['requirements'],
                    defaults={'title': f"Sifa - {c['programme'][:80]}"}
                )
                uc, uc_created = UniversityCourse.objects.get_or_create(
                    university=university,
                    course=course,
                    level='Degree',
                    defaults={
                        'duration': c['duration'],
                        'requirements': req,
                    }
                )
                status = "MPYA" if uc_created else "TAYARI KIPO"
                print(f"      [{status}]")

    print(f"\n{'='*60}")
    if do_import:
        print("KAZI IMEKAMILIKA!")
    else:
        print("PREVIEW TU - Endesha na 'do_import=True' kuingiza kweli.")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--import':
        print("TAHADHARI: Unaingiza data kwenye production database!")
        confirm = input("Je, unataka kuendelea? (ndio/hapana): ")
        if confirm.strip().lower() == 'ndio':
            preview_or_import(do_import=True)
        else:
            print("Imesitishwa.")
    else:
        preview_or_import(do_import=False)
        print("\nKukubaliana na preview, endesha:")
        print("  python add_dit_cfr_courses.py --import")
