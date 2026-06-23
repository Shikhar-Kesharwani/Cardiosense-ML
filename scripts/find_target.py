import pandas as pd

df = pd.read_csv('Notebook_Experiments/Data/nhanes_100k/dictionary_nhanes.csv')
print("Dictionary columns:", df.columns.tolist())

# Assuming column 0 is name and column 1 is desc
col_name = df.columns[0]
col_desc = df.columns[1]

heart_desc = df[df[col_desc].astype(str).str.contains('heart|coronary|attack|stroke', na=False, case=False)]
print("\nVariables with heart in description:")
for idx, row in heart_desc.iterrows():
    print(row[col_name], "->", row[col_desc])
