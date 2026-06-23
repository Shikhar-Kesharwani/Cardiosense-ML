import pandas as pd
from sklearn.metrics import accuracy_score
import pickle
import os

def check_real_accuracy(dataset_type):
    data_path = f"Notebook_Experiments/Data/heart_{dataset_type}.csv"
    if not os.path.exists(data_path):
        return

    df = pd.read_csv(data_path)
    
    # Target column mapping
    if 'target' not in df.columns:
        if 'HeartDiseaseorAttack' in df.columns:
            target_col = 'HeartDiseaseorAttack'
        elif 'cardio' in df.columns:
            target_col = 'cardio'
        else:
            return
    else:
        target_col = 'target'
        
    # Feature Engineering exactly like Data_transformation.py
    if dataset_type == 'cdc':
        df['Risk_Score'] = df['HighBP'] + df['HighChol'] + df['Smoker'] + df['Diabetes']
    elif dataset_type == 'clinical':
        df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)
        df['MAP'] = (df['ap_hi'] + 2 * df['ap_lo']) / 3
        df = df.drop(columns=['height', 'weight'])
        
    y = df[target_col]
    X = df.drop(columns=[target_col])
    
    model_path = f"Artifacts/Model_{dataset_type}.pkl"
    preprocessor_path = f"Artifacts/Preprocessor_{dataset_type}.pkl"
    
    if os.path.exists(model_path) and os.path.exists(preprocessor_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(preprocessor_path, 'rb') as f:
            preprocessor = pickle.load(f)
            
        try:
            X_transformed = preprocessor.transform(X)
            
            if dataset_type == 'nhanes':
                probs = model.predict_proba(X_transformed)
                y_pred = (probs[:, 1] >= 0.30).astype(int)
            else:
                y_pred = model.predict(X_transformed)
                
            acc = accuracy_score(y, y_pred)
            print(f"Mode - {dataset_type.upper()}: {acc*100:.2f}%")
            
            if dataset_type == 'nhanes':
                from sklearn.metrics import recall_score, precision_score, confusion_matrix
                rec = recall_score(y, y_pred)
                prec = precision_score(y, y_pred)
                cm = confusion_matrix(y, y_pred)
                print(f"  Recall (Sick Patients Caught): {rec*100:.2f}%")
                print(f"  Precision: {prec*100:.2f}%")
                print(f"  Confusion Matrix:\n{cm}")
        except Exception as e:
            print(f"Mode - {dataset_type.upper()}: Error - {e}")
            
for ds in ['cdc', 'clinical', 'nhanes', 'brfss']:
    check_real_accuracy(ds)
