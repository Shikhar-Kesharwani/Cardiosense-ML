import pandas as pd
import json
import re

extract_path = 'Notebook_Experiments/Data/nhanes_100k/'

def search_cols(file, keywords):
    try:
        df = pd.read_csv(extract_path + file, nrows=1)
        cols = df.columns
        matches = [c for c in cols if any(k.lower() in c.lower() for k in keywords)]
        print(f"--- {file} ---")
        print(f"Matches for {keywords}: {matches[:20]}")
    except Exception as e:
        print(e)

search_cols('demographics_clean.csv', ['age', 'RIDAGEYR', 'gender', 'RIAGENDR', 'sex'])
search_cols('questionnaire_clean.csv', ['MCQ', 'heart', 'coronary', 'attack', 'stroke', 'cardio'])
search_cols('response_clean.csv', ['BMI', 'BMXBMI', 'BPXSY', 'BPXDI', 'blood pressure', 'BP', 'TR', 'triglycerides', 'HDL', 'LBDHDD', 'cholesterol', 'LBX'])
search_cols('chemicals_clean.csv', ['TR', 'triglyceride', 'HDL', 'cholesterol', 'LBX'])
