import os
import sys
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from xgboost import XGBClassifier
from dataclasses import dataclass
from src.Heart.logger import logging
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from src.Heart.exception import customexception
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from src.Heart.utils.utils import save_object, evaluate_model


class ModelTrainerConfig:
    def __init__(self, dataset_type):
        self.trained_model_file_path = os.path.join('models',f'Model_{dataset_type}.pkl')
        self.dataset_type = dataset_type
    
    
class ModelTrainer:
    def __init__(self, dataset_type):
        self.model_trainer_config = ModelTrainerConfig(dataset_type)
    
    def initate_model_training(self,train_array,test_array):
        try:
            logging.info(f'Splitting Dependent and Independent variables from train and test data for {self.model_trainer_config.dataset_type}')
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1])
            
            from sklearn.ensemble import StackingClassifier
            estimators = [
                ('rf', RandomForestClassifier(random_state=12)),
                ('xgb', XGBClassifier(seed=27, booster='gbtree')),
                ('dt', DecisionTreeClassifier(random_state=0))
            ]
            stacking_clf = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression(max_iter=1000), n_jobs=-1)

            if self.model_trainer_config.dataset_type in ['brfss', 'uci', 'nhanes']:
                models = {
                    'Random Forest Classfier':RandomForestClassifier(random_state=12),
                    'XG Boost':XGBClassifier(seed=27, booster='gbtree', use_label_encoder=False, eval_metric='logloss')
                }
                params={
                    "Random Forest Classfier":{
                        'n_estimators': [50, 100, 200],
                        'max_depth': [5, 10, 15, 20],
                        'min_samples_split': [2, 5, 10],
                        'min_samples_leaf': [1, 2, 4]
                    },
                    "XG Boost":{
                        'learning_rate': [0.01, 0.05, 0.1, 0.2],
                        'n_estimators': [50, 100, 200],
                        'max_depth': [3, 5, 7, 10],
                        'subsample': [0.8, 1.0],
                        'colsample_bytree': [0.8, 1.0]
                    }
                }
            else:
                models = {
                    'Logistic Regression':LogisticRegression(max_iter=1000),
                    'Naive Bayes':GaussianNB(),
                    'Random Forest Classfier':RandomForestClassifier(random_state=12),
                    'XG Boost':XGBClassifier(seed=27, booster='gbtree'),
                    'K Nearest Neighbors':KNeighborsClassifier(),
                    'Decision Tree':DecisionTreeClassifier(random_state=0),
                    'Support Vector Machine':SVC(),
                    'Stacking Classifier': stacking_clf
                    }
                
                params={
                    "Logistic Regression":{},
                    "Decision Tree": {
                        'criterion':['gini', 'entropy', 'log_loss'],
                        'max_depth':[3,5,7,10]
                    },
                    "Random Forest Classfier":{
                        'n_estimators': [50, 100],
                        'max_depth': [5, 10, 15]
                    },
                    "XG Boost":{
                        'learning_rate':[0.01, 0.05, 0.1],
                        'n_estimators': [50, 100],
                        'max_depth': [5, 10]
                    },
                    "K Nearest Neighbors": {
                        'n_neighbors': [5, 10, 15]
                    },
                    "Support Vector Machine": {},
                    "Naive Bayes": {},
                    "Stacking Classifier": {}
                }
            
            model_report = evaluate_model(X_train, y_train, X_test, y_test, models, param=params)
            print(model_report)
            print('\n====================================================================================\n')
            logging.info(f'Model Report: {model_report}')

            # To get the best model score from the dictionary
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            print(f'Best Model Found for {self.model_trainer_config.dataset_type}, Model Name: {best_model_name}, Accuracy Score: {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found for {self.model_trainer_config.dataset_type}, Model Name: {best_model_name}, Accuracy Score: {best_model_score}')

            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
            )
          
        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise customexception(e,sys)