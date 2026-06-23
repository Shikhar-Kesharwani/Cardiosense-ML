import pandas as pd
import numpy as np
import os

print("Processing NHANES 100k dataset...")

extract_path = 'Notebook_Experiments/Data/nhanes_100k/'
output_path = 'Notebook_Experiments/Data/heart_nhanes.csv'

# Read files with specific columns to save memory
demo = pd.read_csv(extract_path + 'demographics_clean.csv', usecols=['SEQN', 'RIDAGEYR', 'RIAGENDR'])
quest = pd.read_csv(extract_path + 'questionnaire_clean.csv', usecols=['SEQN', 'MCQ160C', 'MCQ160E'])
resp = pd.read_csv(extract_path + 'response_clean.csv', usecols=['SEQN', 'BMXBMI', 'BPXSY1', 'BPXDI1', 'LBXTR', 'LBDHDD', 'LBXGLU', 'LBXCRP', 'LBXTC', 'LBXWBCSI'])

# Merge data
df = pd.merge(demo, quest, on='SEQN', how='inner')
df = pd.merge(df, resp, on='SEQN', how='inner')

print(f"Merged shape: {df.shape}")

# Calculate target
def calculate_target(row):
    if row['MCQ160C'] == 1.0 or row['MCQ160E'] == 1.0:
        return 1.0
    elif row['MCQ160C'] == 2.0 and row['MCQ160E'] == 2.0:
        return 0.0
    else:
        return np.nan

df['target'] = df.apply(calculate_target, axis=1)

# Drop those who didn't answer explicitly
df = df.dropna(subset=['target'])
print(f"After dropping missing target: {df.shape}")

# To maintain high clinical validity, we drop rows missing essential lab values
df = df.dropna(subset=['LBXTR', 'LBDHDD', 'BPXSY1', 'BMXBMI', 'LBXGLU', 'LBXCRP', 'LBXTC', 'LBXWBCSI'])
print(f"After dropping missing labs: {df.shape}")

# Select the final columns to match our CustomDataNHANES pipeline
df = df[['RIDAGEYR', 'RIAGENDR', 'BMXBMI', 'BPXSY1', 'BPXDI1', 'LBXTR', 'LBDHDD', 'LBXGLU', 'LBXCRP', 'LBXTC', 'LBXWBCSI', 'target']]

# Rename columns to standard readable names
# df = df.rename(columns={
#     'RIDAGEYR': 'Age',
#     'RIAGENDR': 'Gender',
#     'BMXBMI': 'BMI',
#     'BPXSY1': 'Systolic_BP',
#     'BPXDI1': 'Diastolic_BP',
#     'LBXTR': 'Triglycerides',
#     'LBDHDD': 'HDL'
# })


df.to_csv(output_path, index=False)
print(f"Exported to {output_path} with shape {df.shape}")

# Display quick metrics
pos = df['target'].sum()
neg = len(df) - pos
print(f"Total: {len(df)}")
print(f"Heart Disease (Positive): {pos} ({(pos/len(df))*100:.2f}%)")
print(f"Healthy (Negative): {neg} ({(neg/len(df))*100:.2f}%)")

