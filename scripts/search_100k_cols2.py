import pandas as pd
extract_path = 'Notebook_Experiments/Data/nhanes_100k/'

try:
    resp = pd.read_csv(extract_path + 'response_clean.csv', nrows=1)
    cols = resp.columns
    print("BMI matches:", [c for c in cols if 'bmi' in c.lower()])
    print("BP matches:", [c for c in cols if 'bp' in c.lower()])
    print("Triglycerides matches:", [c for c in cols if 'tr' in c.lower() or 'lbx' in c.lower()])
    print("HDL matches:", [c for c in cols if 'hdl' in c.lower() or 'lbdhdd' in c.lower()])
except Exception as e:
    print(e)
