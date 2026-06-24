"""
Script ya kuongeza vyuo vilivyokosekana kwenye extraction ya PDF ya TCU.
Vyuo hivi vipo kwenye orodha rasmi ya TCU lakini havikupatikana wakati wa kusoma PDF.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import Region, University

def add_missing_unis():
    missing_unis = [
        {
            'name': 'Dar es Salaam Institute of Technology (DIT), Dar es Salaam',
            'region': 'Dar es Salaam',
            'type': 'Institute',
            'umiliki': 'Goverment',
            'website': 'www.dit.ac.tz',
            'email': '',
        },
        {
            'name': 'Dar es Salaam Institute of Technology (DIT), Mwanza Campus',
            'region': 'Mwanza',
            'type': 'Institute',
            'umiliki': 'Goverment',
            'website': 'www.dit.ac.tz',
            'email': '',
        },
        {
            'name': 'Dr. Salim Ahmed Salim Centre for Foreign Relations (CFR), Dar es Salaam',
            'region': 'Dar es Salaam',
            'type': 'Institute',
            'umiliki': 'Goverment',
            'website': '',
            'email': '',
        },
    ]

    added = 0
    for uni_data in missing_unis:
        region, _ = Region.objects.get_or_create(name=uni_data['region'])
        uni, created = University.objects.get_or_create(
            name=uni_data['name'],
            defaults={
                'region': region,
                'type': uni_data['type'],
                'umiliki': uni_data['umiliki'],
                'website': uni_data.get('website', ''),
                'email': uni_data.get('email', ''),
                'is_active': True,
            }
        )
        if created:
            print(f"✓ Imeongezwa: {uni.name} (Mkoa: {region.name})")
            added += 1
        else:
            print(f"  Tayari ipo: {uni.name}")

    print(f"\nJumla ya vyuo vipya vilivyoongezwa: {added}")

if __name__ == '__main__':
    add_missing_unis()
