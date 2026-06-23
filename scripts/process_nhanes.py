import pandas as pd
import numpy as np

def process_nhanes():
    print("Loading NHANES datasets...")
    extract_path = 'Notebook_Experiments/Data/nhanes/'
    demo = pd.read_csv(extract_path + 'demographic.csv')
    labs = pd.read_csv(extract_path + 'labs.csv')
    exam = pd.read_csv(extract_path + 'examination.csv')
    quest = pd.read_csv(extract_path + 'questionnaire.csv')

    print("Merging datasets on SEQN...")
    df = demo.merge(labs, on='SEQN', how='inner')\
             .merge(exam, on='SEQN', how='inner')\
             .merge(quest, on='SEQN', how='inner')

    # Target variable: MCQ160C (Coronary heart disease), MCQ160E (Heart attack)
    # 1 = Yes, 2 = No, 7 = Refused, 9 = Don't Know
    
    # We want 1.0 (Heart Disease) or 0.0 (No Heart Disease)
    def calculate_target(row):
        if row['MCQ160C'] == 1.0 or row['MCQ160E'] == 1.0:
            return 1.0
        elif row['MCQ160C'] == 2.0 and row['MCQ160E'] == 2.0:
            return 0.0
        else:
            return np.nan # Drop ambiguous cases

    df['target'] = df.apply(calculate_target, axis=1)

    cols_to_keep = ['RIDAGEYR', 'RIAGENDR', 'BMXBMI', 'BPXSY1', 'BPXDI1', 'LBXTR', 'LBDHDD', 'target']
    
    # Filter only rows that have the columns we need
    available_cols = [c for c in cols_to_keep if c in df.columns]
    
    if 'target' not in available_cols:
        print("ERROR: Target column was not generated correctly.")
        return
        
    df = df[available_cols]

    # Drop rows without a target
    df = df.dropna(subset=['target'])

    # For clinical indicators, let's fill NaNs with the median to preserve dataset size
    df = df.fillna(df.median())

    print(f"Final shape of NHANES dataset: {df.shape}")
    
    output_path = "Notebook_Experiments/Data/heart_nhanes.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved processed dataset to {output_path}")

if __name__ == "__main__":
    process_nhanes()
