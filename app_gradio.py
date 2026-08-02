import os
import pandas as pd
import gradio as gr
from src.Heart.pipeline.Prediction_pipeline import CustomDataCDC, CustomDataClinical, CustomDataNHANES, PredictPipeline

def predict_clinical(age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active):
    try:
        data = CustomDataClinical(
            age=int(age), gender=int(gender), height=int(height), weight=float(weight),
            ap_hi=int(ap_hi), ap_lo=int(ap_lo), cholesterol=int(cholesterol), gluc=int(gluc),
            smoke=int(smoke), alco=int(alco), active=int(active)
        )
        final_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_data, dataset_type='clinical')
        prob = round(float(pred[0]), 4)
        status = "High Risk of Cardiovascular Disease" if prob > 0.5 else "Low Risk of Cardiovascular Disease"
        return f"{status} (Score: {prob})"
    except Exception as e:
        return f"Error: {str(e)}"

def predict_nhanes(age, gender, bmi, sys_bp, dia_bp, trig, hdl, glucose, crp, total_chol, wbc):
    try:
        data = CustomDataNHANES(
            RIDAGEYR=float(age), RIAGENDR=float(gender), BMXBMI=float(bmi),
            BPXSY1=float(sys_bp), BPXDI1=float(dia_bp), LBXTR=float(trig),
            LBDHDD=float(hdl), LBXGLU=float(glucose), LBXCRP=float(crp),
            LBXTC=float(total_chol), LBXWBCSI=float(wbc)
        )
        pred_df = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df, "nhanes")
        return "High Risk of Heart Disease" if results[0] == 1 else "Low Risk of Heart Disease"
    except Exception as e:
        return f"Error: {str(e)}"

# Clinical Diagnosis Interface
clinical_inputs = [
    gr.Number(label="Age (years)", value=45),
    gr.Radio(choices=[(1, "Female"), (2, "Male")], label="Gender", value=1),
    gr.Number(label="Height (cm)", value=165),
    gr.Number(label="Weight (kg)", value=70),
    gr.Number(label="Systolic Blood Pressure (ap_hi)", value=120),
    gr.Number(label="Diastolic Blood Pressure (ap_lo)", value=80),
    gr.Radio(choices=[(1, "Normal"), (2, "Above Normal"), (3, "Well Above Normal")], label="Cholesterol Level", value=1),
    gr.Radio(choices=[(1, "Normal"), (2, "Above Normal"), (3, "Well Above Normal")], label="Glucose Level", value=1),
    gr.Radio(choices=[(0, "No"), (1, "Yes")], label="Smoker", value=0),
    gr.Radio(choices=[(0, "No"), (1, "Yes")], label="Alcohol Intake", value=0),
    gr.Radio(choices=[(0, "No"), (1, "Yes")], label="Physical Activity", value=1),
]

nhanes_inputs = [
    gr.Number(label="Age (years)", value=50),
    gr.Radio(choices=[(1, "Male"), (2, "Female")], label="Gender", value=1),
    gr.Number(label="BMI", value=26.5),
    gr.Number(label="Systolic BP (mm Hg)", value=125),
    gr.Number(label="Diastolic BP (mm Hg)", value=82),
    gr.Number(label="Triglycerides (mg/dL)", value=150),
    gr.Number(label="HDL Cholesterol (mg/dL)", value=50),
    gr.Number(label="Fasting Glucose (mg/dL)", value=95),
    gr.Number(label="C-Reactive Protein (mg/dL)", value=1.2),
    gr.Number(label="Total Cholesterol (mg/dL)", value=195),
    gr.Number(label="White Blood Cell Count (1000 cells/uL)", value=6.5),
]

demo = gr.TabbedInterface(
    [
        gr.Interface(fn=predict_clinical, inputs=clinical_inputs, outputs="text", title="Clinical Diagnosis AI Model"),
        gr.Interface(fn=predict_nhanes, inputs=nhanes_inputs, outputs="text", title="NHANES Biomarker AI Model"),
    ],
    tab_names=["Clinical Prediction", "NHANES Biomarker Analysis"],
    title="❤️ CardioSense AI — Heart Disease Risk Prediction Platform"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
