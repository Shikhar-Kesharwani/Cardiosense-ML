import pandas as pd
import json

extract_path = 'Notebook_Experiments/Data/nhanes/'
demo = pd.read_csv(extract_path + 'demographic.csv')
labs = pd.read_csv(extract_path + 'labs.csv')
exam = pd.read_csv(extract_path + 'examination.csv')
quest = pd.read_csv(extract_path + 'questionnaire.csv')

# Find heart disease in questionnaire (MCQ160B: congestive heart failure, MCQ160C: coronary heart disease, MCQ160E: heart attack)
# Or maybe the dataset has renamed them.
target_cols = [c for c in quest.columns if 'MCQ' in c or 'heart' in c.lower() or 'cvd' in c.lower()]
print("Possible targets:", target_cols)

# We want a manageable subset of labs and exam features, e.g.
# LBXTR: Triglycerides
# LBDHDD: HDL Cholesterol
# BPXSY1: Systolic BP
# BPXDI1: Diastolic BP
# BMXBMI: BMI
# BMXWAIST: Waist Circumference

df = demo.merge(labs, on='SEQN').merge(exam, on='SEQN').merge(quest, on='SEQN')
print(f"Merged Shape: {df.shape}")

# Sample columns to pick
cols = ['SEQN', 'RIAGENDR', 'RIDAGEYR', 'BMXBMI', 'BPXSY1', 'BPXDI1', 'LBXTR', 'LBDHDD', 'LBXGLU', 'MCQ160C', 'MCQ160E']
available_cols = [c for c in cols if c in df.columns]
print("Available common NHANES columns:", available_cols)
