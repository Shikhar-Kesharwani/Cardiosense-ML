import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import os

def check_real_accuracy(dataset_type):
    print(f"--- Checking {dataset_type.upper()} ---")
    data_path = f"Notebook_Experiments/Data/heart_{dataset_type}.csv"
    if not os.path.exists(data_path):
        print(f"File {data_path} not found.")
        return

    df = pd.read_csv(data_path)
    
    if 'target' not in df.columns:
        if 'HeartDiseaseorAttack' in df.columns:
            target_col = 'HeartDiseaseorAttack'
        elif 'cardio' in df.columns:
            target_col = 'cardio'
        else:
            print("Target column not found.")
            return
    else:
        target_col = 'target'
        
    y = df[target_col]
    X = df.drop(columns=[target_col])
    
    total = len(y)
    positives = y.sum()
    negatives = total - positives
    
    print(f"Total records: {total}")
    print(f"Positives (Heart Disease): {positives} ({(positives/total)*100:.2f}%)")
    print(f"Negatives (Healthy): {negatives} ({(negatives/total)*100:.2f}%)")
    
    # Let's also check the actual trained model if it exists
    model_path = f"Artifacts/Model_{dataset_type}.pkl"
    preprocessor_path = f"Artifacts/Preprocessor_{dataset_type}.pkl"
    
    if os.path.exists(model_path) and os.path.exists(preprocessor_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(preprocessor_path, 'rb') as f:
            preprocessor = pickle.load(f)
            
        try:
            # We will just evaluate on the whole dataset to see what the model learned
            X_transformed = preprocessor.transform(X)
            y_pred = model.predict(X_transformed)
            
            acc = accuracy_score(y, y_pred)
            prec = precision_score(y, y_pred, zero_division=0)
            rec = recall_score(y, y_pred, zero_division=0)
            f1 = f1_score(y, y_pred, zero_division=0)
            cm = confusion_matrix(y, y_pred)
            
            print(f"\nModel Evaluation on Full Data:")
            print(f"Accuracy:  {acc:.4f}")
            print(f"Precision: {prec:.4f}")
            print(f"Recall:    {rec:.4f}")
            print(f"F1 Score:  {f1:.4f}")
            print("Confusion Matrix:")
            print(cm)
            print("\n")
        except Exception as e:
            print(f"Could not evaluate model: {e}")
            
for ds in ['cdc', 'clinical', 'nhanes', 'brfss']:
    check_real_accuracy(ds)
