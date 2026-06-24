import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vyuofinder.settings')
django.setup()

from universitysite.models import University

def normalize_name(name):
    # Convert to uppercase
    name = str(name).upper()
    # Remove REG info
    name = re.sub(r'\(REG/[^\)]+\)', '', name)
    # Remove punctuation
    name = re.sub(r'[^\w\s]', '', name)
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

all_unis = University.objects.all()
norm_to_unis = {}

for u in all_unis:
    norm = normalize_name(u.name)
    if norm not in norm_to_unis:
        norm_to_unis[norm] = []
    norm_to_unis[norm].append(u)

with open('Ripoti_ya_Vyuo_Vinavyofanana.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RIPOTI YA VYUO VINAVYOONEKANA KUFANANA LAKINI VINA MAJINA TOFAUTI\n")
    f.write("="*80 + "\n\n")
    
    count = 0
    for norm, unis in norm_to_unis.items():
        if len(unis) > 1:
            count += 1
            f.write(f"Kundi {count}: (Jina linalofanana: {norm})\n")
            for u in unis:
                f.write(f"  - {u.name} (Mkoa: {u.region.name})\n")
            f.write("\n")
            
    f.write("="*80 + "\n")
    f.write(f"Jumla ya makundi yaliyopatikana: {count}\n")
    f.write("Unaweza kurekebisha majina haya moja kwa moja kupitia Admin Panel (Django Admin)\n")
    f.write("ili yawe na jina moja endapo ni chuo kimoja (au uyaache kama ni matawi tofauti).\n")
    
print("Ripoti imetengenezwa! Soma faili la 'Ripoti_ya_Vyuo_Vinavyofanana.txt'")
