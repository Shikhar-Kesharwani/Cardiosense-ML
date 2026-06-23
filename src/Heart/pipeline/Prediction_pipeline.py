import os
import sys
import pandas as pd
from src.Heart.logger import logging
from src.Heart.utils.utils import load_object
from src.Heart.exception import customexception

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features, dataset_type):
        try:
            preprocessor_path = os.path.join("models", f"Preprocessor_{dataset_type}.pkl")
            model_path = os.path.join("models", f"Model_{dataset_type}.pkl")
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)
            scaled_data = preprocessor.transform(features)
            
            if dataset_type == 'nhanes':
                probs = model.predict_proba(scaled_data)
                pred = (probs[:, 1] >= 0.30).astype(int)
            else:
                pred = model.predict(scaled_data)
                
            return pred

        except Exception as e:
            raise customexception(e,sys)
    
class CustomDataCDC:
    def __init__(self,
                 HighBP:int, HighChol:int, CholCheck:int, BMI:int, Smoker:int, Stroke:int,
                 Diabetes:int, PhysActivity:int, Fruits:int, Veggies:int, HvyAlcoholConsump:int,
                 AnyHealthcare:int, NoDocbcCost:int, GenHlth:int, MentHlth:int, PhysHlth:int,
                 DiffWalk:int, Sex:int, Age:int, Education:int, Income:int):
        self.HighBP = HighBP
        self.HighChol = HighChol
        self.CholCheck = CholCheck
        self.BMI = BMI
        self.Smoker = Smoker
        self.Stroke = Stroke
        self.Diabetes = Diabetes
        self.PhysActivity = PhysActivity
        self.Fruits = Fruits
        self.Veggies = Veggies
        self.HvyAlcoholConsump = HvyAlcoholConsump
        self.AnyHealthcare = AnyHealthcare
        self.NoDocbcCost = NoDocbcCost
        self.GenHlth = GenHlth
        self.MentHlth = MentHlth
        self.PhysHlth = PhysHlth
        self.DiffWalk = DiffWalk
        self.Sex = Sex
        self.Age = Age
        self.Education = Education
        self.Income = Income
                
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'HighBP':[self.HighBP], 'HighChol':[self.HighChol], 'CholCheck':[self.CholCheck],
                'BMI':[self.BMI], 'Smoker':[self.Smoker], 'Stroke':[self.Stroke],
                'Diabetes':[self.Diabetes], 'PhysActivity':[self.PhysActivity], 'Fruits':[self.Fruits],
                'Veggies':[self.Veggies], 'HvyAlcoholConsump':[self.HvyAlcoholConsump],
                'AnyHealthcare':[self.AnyHealthcare], 'NoDocbcCost':[self.NoDocbcCost],
                'GenHlth':[self.GenHlth], 'MentHlth':[self.MentHlth], 'PhysHlth':[self.PhysHlth],
                'DiffWalk':[self.DiffWalk], 'Sex':[self.Sex], 'Age':[self.Age],
                'Education':[self.Education], 'Income':[self.Income]
            }
            df = pd.DataFrame(custom_data_input_dict)
            df = df.astype(float) 
            
            # Feature Engineering
            df['Risk_Score'] = df['HighBP'] + df['HighChol'] + df['Smoker'] + df['Diabetes']
            
            logging.info('CDC Dataframe Gathered and Engineered')
            return df
        except Exception as e:
            raise customexception(e,sys)

class CustomDataClinical:
    def __init__(self,
                 age:int, gender:int, height:int, weight:float, ap_hi:int, ap_lo:int,
                 cholesterol:int, gluc:int, smoke:int, alco:int, active:int):
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.ap_hi = ap_hi
        self.ap_lo = ap_lo
        self.cholesterol = cholesterol
        self.gluc = gluc
        self.smoke = smoke
        self.alco = alco
        self.active = active

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'age': [self.age],
                'gender': [self.gender],
                'height': [self.height],
                'weight': [self.weight],
                'ap_hi': [self.ap_hi],
                'ap_lo': [self.ap_lo],
                'cholesterol': [self.cholesterol],
                'gluc': [self.gluc],
                'smoke': [self.smoke],
                'alco': [self.alco],
                'active': [self.active]
            }
            df = pd.DataFrame(custom_data_input_dict)
            df = df.astype(float) 
            
            # Feature Engineering
            df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)
            df['MAP'] = (df['ap_hi'] + 2 * df['ap_lo']) / 3
            df = df.drop(columns=['height', 'weight'])
            
            logging.info('Clinical Dataframe Gathered and Engineered')
            return df
        except Exception as e:
            raise customexception(e,sys)

class CustomDataNHANES:
    def __init__(  self,
        RIDAGEYR: float,
        RIAGENDR: float,
        BMXBMI: float,
        BPXSY1: float,
        BPXDI1: float,
        LBXTR: float,
        LBDHDD: float,
        LBXGLU: float,
        LBXCRP: float,
        LBXTC: float,
        LBXWBCSI: float):

        self.RIDAGEYR = RIDAGEYR
        self.RIAGENDR = RIAGENDR
        self.BMXBMI = BMXBMI
        self.BPXSY1 = BPXSY1
        self.BPXDI1 = BPXDI1
        self.LBXTR = LBXTR
        self.LBDHDD = LBDHDD
        self.LBXGLU = LBXGLU
        self.LBXCRP = LBXCRP
        self.LBXTC = LBXTC
        self.LBXWBCSI = LBXWBCSI

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "RIDAGEYR": [self.RIDAGEYR],
                "RIAGENDR": [self.RIAGENDR],
                "BMXBMI": [self.BMXBMI],
                "BPXSY1": [self.BPXSY1],
                "BPXDI1": [self.BPXDI1],
                "LBXTR": [self.LBXTR],
                "LBDHDD": [self.LBDHDD],
                "LBXGLU": [self.LBXGLU],
                "LBXCRP": [self.LBXCRP],
                "LBXTC": [self.LBXTC],
                "LBXWBCSI": [self.LBXWBCSI]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise customexception(e,sys)

class CustomDataBRFSS:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {k: [v] for k, v in self.kwargs.items()}
            df = pd.DataFrame(custom_data_input_dict)
            df = df.astype(float)
            logging.info('BRFSS Dataframe Gathered')
            return df
        except Exception as e:
            raise customexception(e,sys)
