import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.Heart.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.Heart.utils.utils import save_object
from sklearn.compose import ColumnTransformer
from src.Heart.exception import customexception
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE


class DataTransformationConfig:
    def __init__(self, dataset_type):
        self.preprocessor_obj_file_path=os.path.join('models',f'Preprocessor_{dataset_type}.pkl')
        self.dataset_type = dataset_type


class DataTransformation:
    def __init__(self, dataset_type):
        self.data_transformation_config=DataTransformationConfig(dataset_type)
    
    def engineer_features(self, df):
        if self.data_transformation_config.dataset_type == 'cdc':
            # Create Risk Score
            df['Risk_Score'] = df['HighBP'] + df['HighChol'] + df['Smoker'] + df['Diabetes']
        elif self.data_transformation_config.dataset_type == 'clinical':
            # Clinical features
            # BMI = weight (kg) / (height (m) )^2
            df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)
            # MAP = (systolic + 2*diastolic)/3
            df['MAP'] = (df['ap_hi'] + 2 * df['ap_lo']) / 3
            # Drop height and weight
            df = df.drop(columns=['height', 'weight'])
        return df

    def get_data_transformation(self):
        try:
            logging.info(f'Data Transformation initiated for {self.data_transformation_config.dataset_type}')

            if self.data_transformation_config.dataset_type == 'cdc':
                numerical_cols = ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 'Diabetes', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income', 'Risk_Score']
            elif self.data_transformation_config.dataset_type == 'clinical':
                numerical_cols = ['age', 'gender', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'BMI', 'MAP']
            elif self.data_transformation_config.dataset_type == 'uci':
                numerical_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
            elif self.data_transformation_config.dataset_type == 'brfss':
                numerical_cols = ['BPHIGH4', 'TOLDHI2', 'CHOLCHK', 'SMOKE100', 'CVDSTRK3', 'DIABETE3', '_TOTINDA', '_FRTLT1', '_VEGLT1', 'HLTHPLN1', 'MEDCOST', 'GENHLTH', 'MENTHLTH', 'PHYSHLTH', 'DIFFWALK', 'SEX', '_AGEG5YR', 'EDUCA', 'INCOME2', 'ASTHMA3', 'CHCSCNCR', 'CHCOCNCR', 'CHCCOPD1', 'HAVARTH3', 'ADDEPEV2', 'CHCKIDNY', 'WEIGHT2', 'HEIGHT3', 'ALCDAY5', 'EXERANY2', 'SEATBELT', 'FLUSHOT6', 'PNEUVAC3', 'HIVTST6', 'QSTVER', 'QSTLANG', '_STATE', 'MSCODE', 'MARITAL', 'VETERAN3', 'DECIDE', 'DIFFALON']
            elif self.data_transformation_config.dataset_type == 'nhanes':
                numerical_cols = ['RIDAGEYR', 'RIAGENDR', 'BMXBMI', 'BPXSY1', 'BPXDI1', 'LBXTR', 'LBDHDD', 'LBXGLU', 'LBXCRP', 'LBXTC', 'LBXWBCSI']

            logging.info('Numerical Pipeline Initiated')
            
            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())])

            preprocessor = ColumnTransformer([('num_pipeline',num_pipeline,numerical_cols)])
            return preprocessor 
                
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")
            raise customexception(e,sys)
            
    
    def initialize_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("read train and test data complete")
            
            # Feature Engineering
            train_df = self.engineer_features(train_df)
            test_df = self.engineer_features(test_df)
            
            logging.info(f'Train Dataframe Head after engineering: \n{train_df.head().to_string()}')
            
            preprocessing_obj = self.get_data_transformation()
            
            target_column_name = 'target'
            drop_columns = [target_column_name]
            
            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]          
            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]
            logging.info("Splitting input and target features complete")
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            logging.info("Applying preprocessing object on training and testing datasets.")
            
            # Apply SMOTE to training data only
            logging.info("Applying SMOTE to handle class imbalance in training set.")
            smote = SMOTE(random_state=42)
            input_feature_train_arr, target_feature_train_df = smote.fit_resample(input_feature_train_arr, target_feature_train_df)
            logging.info("SMOTE applied successfully.")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj)
            
            logging.info("preprocessing pickle file saved")
            return (train_arr,test_arr)
            
        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")
            raise customexception(e,sys)