import pandas as pd
import sys
import html

try:
    df = pd.read_excel('mari.xlsx')
    print('EXCEL WORKED:', len(df))
except Exception as e:
    print('EXCEL ERROR:', e)
    
try:
    df = pd.read_csv('mari.xlsx')
    print('CSV WORKED:', len(df))
    print(df.columns.tolist())
except Exception as e:
    print('CSV ERROR:', e)
    
try:
    with open('mari.xlsx', 'r', encoding='utf-8', errors='ignore') as f:
        head = f.read(100)
    print("FILE HEADER:")
    print(head)
except Exception as e:
    print('TEXT ERROR:', e)
