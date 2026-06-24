import pandas as pd
import re

print("Kusafisha majina ya kozi na sifa (Requirements) kwenye Excel...")
df = pd.read_excel('tcu_data_new.xlsx')

# Ondoa vyuo vyenye majina yaliyoharibika kutokana na PDF extraction parsing errors
corrupted_unis = [
    'College of Education (MUCE)',
    'College of Engineering and Technology (SJCET)',
    'Mbeya Campus College (MUMCCo)',
    'Mizengo Pinda Campus College'
]
df = df[~df['University'].isin(corrupted_unis)]
df = df.reset_index(drop=True)

# 1. Safisha Programmes
programmes = df['Programme'].tolist()
prog_pattern = r'(?<!^)(Bachelor|Doctor|BSc|B\.A|B\.Sc|Doctor of)'

for i in range(len(programmes)):
    prog = str(programmes[i]).strip()
    match = re.search(prog_pattern, prog)
    if match and match.start() > 0:
        prefix = prog[:match.start()].strip()
        actual_prog = prog[match.start():].strip()
        if i > 0 and len(prefix) > 0:
            programmes[i-1] = str(programmes[i-1]) + " " + prefix
        programmes[i] = actual_prog

df['Programme'] = programmes

# 2. Safisha Requirements
requirements = df['Requirements'].tolist()
# Pattern ya kuanza kwa requirement (case insensitive)
req_pattern = re.compile(r'(?<!^)(Two principal passes|Three principal passes|Two Principal level passes|A principal pass|Holders of|Any two principal|A minimum of|Certificate of Secondary)', re.IGNORECASE)

for i in range(len(requirements)):
    req = str(requirements[i]).strip()
    match = req_pattern.search(req)
    if match and match.start() > 0:
        prefix = req[:match.start()].strip()
        actual_req = req[match.start():].strip()
        if i > 0 and len(prefix) > 0:
            requirements[i-1] = str(requirements[i-1]) + " " + prefix
        requirements[i] = actual_req

df['Requirements'] = requirements

# Hifadhi
df.to_excel('tcu/tcu_data_cleaned.xlsx', index=False)
print("Usafi wa Requirements umekamilika!")
