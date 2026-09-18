import os
import sys
import mlflow
import pickle
import numpy as np
import mlflow.sklearn
from urllib.parse import urlparse
from src.Heart.utils.utils import load_object
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class ModelEvaluation:
    def __init__(self, dataset_type):
        self.dataset_type = dataset_type

    def eval_metrics(self,actual,pred):
        accuracy = accuracy_score(actual,pred)
        precision = precision_score(actual,pred)
        recall = recall_score(actual,pred)
        f1 = f1_score(actual,pred)
        return accuracy, precision, recall, f1
    

    def initate_model_evaluation(self, train_array, test_array):
        try:
            X_test,y_test=(test_array[:,:-1], test_array[:,-1])
            model_path=os.path.join("models",f"Model_{self.dataset_type}.pkl")
            model=load_object(model_path)

            try:
                mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "https://dagshub.com/placeholder/Heart-Disease-Prediction.mlflow")
                mlflow.set_registry_uri(mlflow_uri)
                tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
                
                print(tracking_url_type_store)

                with mlflow.start_run(run_name=f"run_{self.dataset_type}"):

                    predicted_qualities = model.predict(X_test)

                    (accuracy, precision, recall, f1) = self.eval_metrics(y_test,predicted_qualities)

                    mlflow.log_metric(f"Testing Accuracy_{self.dataset_type}", accuracy)
                    mlflow.log_metric(f"Precision Score_{self.dataset_type}", precision)
                    mlflow.log_metric(f"Recall Score_{self.dataset_type}", recall)
                    mlflow.log_metric(f"F1 Score_{self.dataset_type}", f1)

                    if tracking_url_type_store != "file":
                        mlflow.sklearn.log_model(model, "Model", registered_model_name=f"ml_model_{self.dataset_type}", serialization_format="cloudpickle")
                    else:
                        mlflow.sklearn.log_model(model, "Model", serialization_format="cloudpickle")
            except Exception as ml_e:
                print("MLflow logging failed, but bypassing to allow pipeline to continue.")
                
        except Exception as e:
            raise e
