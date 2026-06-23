from src.Heart.components.Data_ingestion import DataIngestion
from src.Heart.components.Data_transformation import DataTransformation
from src.Heart.components.Model_trainer import ModelTrainer
from src.Heart.components.Model_evaluation import ModelEvaluation

def run_pipeline(dataset_type):
    print(f"\n=============================================\nStarting Pipeline for {dataset_type.upper()} AI\n=============================================\n")
    # Data ingestion Pipeline
    obj = DataIngestion(dataset_type)
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    # Data Transformation Pipeline
    data_transformation = DataTransformation(dataset_type)
    train_arr, test_arr = data_transformation.initialize_data_transformation(train_data_path, test_data_path)

    # Model Training Pipeline
    model_trainer_obj = ModelTrainer(dataset_type)
    model_trainer_obj.initate_model_training(train_arr, test_arr)

    # Model Evaluation Pipeline
    model_eval_obj = ModelEvaluation(dataset_type)
    model_eval_obj.initate_model_evaluation(train_arr, test_arr)

if __name__ == "__main__":
    for dataset_type in ['nhanes']:
        run_pipeline(dataset_type)