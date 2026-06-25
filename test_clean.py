import pandas as pd
import re

df = pd.read_excel('tcu/tcu_data.xlsx')
print("Original Courses:")
print(df['Programme'].head(20).tolist())

def clean_programmes(df):
    programmes = df['Programme'].tolist()
    
    # Common prefixes that indicate a new course starts
    # We use regex to find these if they are in the middle of a string
    pattern = r'(?<!^)(Bachelor|Doctor|BSc|B\.A|B\.Sc|Doctor of)'
    
    for i in range(len(programmes)):
        prog = str(programmes[i]).strip()
        
        # If it has a prefix in the middle of the string
        match = re.search(pattern, prog)
        if match and match.start() > 0:
            # Found a merged string!
            prefix = prog[:match.start()].strip()
            actual_prog = prog[match.start():].strip()
            
            # Append the prefix to the previous course (if exists)
            if i > 0 and len(prefix) > 0:
                programmes[i-1] = str(programmes[i-1]) + " " + prefix
                
            programmes[i] = actual_prog
            
    df['Programme'] = programmes
    return df

df_cleaned = clean_programmes(df)
print("\nCleaned Courses:")
print(df_cleaned['Programme'].head(20).tolist())
