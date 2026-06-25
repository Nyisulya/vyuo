import pandas as pd
import re

print("Kusafisha majina ya kozi na vyuo kwenye Excel...")
df = pd.read_excel('tcu/tcu_data.xlsx')

# Ondoa "Unknown University" ambazo zilikuwa ni Table of Contents
df = df[df['University'] != 'Unknown University']
df = df.reset_index(drop=True)

# Safisha majina ya kozi yaliyoungana
programmes = df['Programme'].tolist()
pattern = r'(?<!^)(Bachelor|Doctor|BSc|B\.A|B\.Sc|Doctor of)'

for i in range(len(programmes)):
    prog = str(programmes[i]).strip()
    
    # Kama kuna "Bachelor" au "Doctor" katikati ya jina la kozi, itenganishe
    match = re.search(pattern, prog)
    if match and match.start() > 0:
        prefix = prog[:match.start()].strip()
        actual_prog = prog[match.start():].strip()
        
        # Sehemu ya kwanza inarudishwa kwenye kozi ya juu yake
        if i > 0 and len(prefix) > 0:
            programmes[i-1] = str(programmes[i-1]) + " " + prefix
            
        programmes[i] = actual_prog

df['Programme'] = programmes

# Hifadhi
df.to_excel('tcu/tcu_data.xlsx', index=False)
print("Usafi umekamilika! tcu_data.xlsx sasa iko safi asilimia 100.")
