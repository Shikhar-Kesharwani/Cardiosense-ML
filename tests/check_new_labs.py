import pandas as pd

extract_path = 'Notebook_Experiments/Data/nhanes_100k/'
resp = pd.read_csv(extract_path + 'response_clean.csv', usecols=['SEQN', 'LBXGLU', 'LBXCRP', 'LBXTC', 'LBXWBCSI', 'LBXTR', 'LBDHDD'])
print(f"Total rows in response_clean: {len(resp)}")

for col in ['LBXGLU', 'LBXCRP', 'LBXTC', 'LBXWBCSI', 'LBXTR', 'LBDHDD']:
    valid_count = resp[col].notna().sum()
    print(f"{col}: {valid_count} non-null values ({(valid_count/len(resp))*100:.2f}%)")

# Check how many rows we have if we drop all missing
merged_cols = resp[['SEQN', 'LBXGLU', 'LBXCRP', 'LBXTC', 'LBXWBCSI', 'LBXTR', 'LBDHDD']].dropna()
print(f"Total rows if ALL 6 labs are required: {len(merged_cols)}")
