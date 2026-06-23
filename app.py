from flask import Flask, request, render_template
from src.Heart.pipeline.Prediction_pipeline import CustomDataCDC, CustomDataClinical, CustomDataNHANES, CustomDataBRFSS, PredictPipeline

app = Flask(__name__)

# Define the home route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict_cdc", methods=["POST"])
def predict_cdc():
    try:
        # Validate and convert form data to CustomDataCDC object
        data = CustomDataCDC(
            HighBP=request.form.get("HighBP"),
            HighChol=request.form.get("HighChol"),
            CholCheck=request.form.get("CholCheck"),
            BMI=request.form.get("BMI"),
            Smoker=request.form.get("Smoker"),
            Stroke=request.form.get("Stroke"),
            Diabetes=request.form.get("Diabetes"),
            PhysActivity=request.form.get("PhysActivity"),
            Fruits=request.form.get("Fruits"),
            Veggies=request.form.get("Veggies"),
            HvyAlcoholConsump=request.form.get("HvyAlcoholConsump"),
            AnyHealthcare=request.form.get("AnyHealthcare"),
            NoDocbcCost=request.form.get("NoDocbcCost"),
            GenHlth=request.form.get("GenHlth"),
            MentHlth=request.form.get("MentHlth"),
            PhysHlth=request.form.get("PhysHlth"),
            DiffWalk=request.form.get("DiffWalk"),
            Sex=request.form.get("Sex"),
            Age=request.form.get("Age"),
            Education=request.form.get("Education"),
            Income=request.form.get("Income")
        )

        final_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_data, dataset_type='cdc')
        result = round(pred[0], 2)
        return render_template("result.html", final_result=result, mode="Public Health Survey")

    except Exception as e:
        error_message = f"Error during CDC prediction: {str(e)}"
        return render_template("error.html", error_message=error_message)

@app.route("/predict_clinical", methods=["POST"])
def predict_clinical():
    try:
        data = CustomDataClinical(
            age=request.form.get("age"),
            gender=request.form.get("gender"),
            height=request.form.get("height"),
            weight=request.form.get("weight"),
            ap_hi=request.form.get("ap_hi"),
            ap_lo=request.form.get("ap_lo"),
            cholesterol=request.form.get("cholesterol"),
            gluc=request.form.get("gluc"),
            smoke=request.form.get("smoke"),
            alco=request.form.get("alco"),
            active=request.form.get("active")
        )

        final_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_data, dataset_type='clinical')
        result = round(pred[0], 2)
        return render_template("result.html", final_result=result, mode="Clinical Diagnosis")

    except Exception as e:
        error_message = f"Error during Clinical prediction: {str(e)}"
        return render_template("error.html", error_message=error_message)

@app.route('/predict_nhanes', methods=['POST'])
def predict_nhanes():
    try:
        data = CustomDataNHANES(
            RIDAGEYR=float(request.form.get('RIDAGEYR')),
            RIAGENDR=float(request.form.get('RIAGENDR')),
            BMXBMI=float(request.form.get('BMXBMI')),
            BPXSY1=float(request.form.get('BPXSY1')),
            BPXDI1=float(request.form.get('BPXDI1')),
            LBXTR=float(request.form.get('LBXTR')),
            LBDHDD=float(request.form.get('LBDHDD')),
            LBXGLU=float(request.form.get('LBXGLU')),
            LBXCRP=float(request.form.get('LBXCRP')),
            LBXTC=float(request.form.get('LBXTC')),
            LBXWBCSI=float(request.form.get('LBXWBCSI'))
        )
        pred_df = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df, "nhanes")
        prediction_text = "High Risk of Heart Disease" if results[0] == 1 else "Low Risk of Heart Disease"
        return render_template('index.html', results_nhanes=prediction_text, active_tab='nhanes')
    except Exception as e:
        error_message = f"Error during NHANES prediction: {str(e)}"
        return render_template("error.html", error_message=error_message)

@app.route("/predict_brfss", methods=["POST"])
def predict_brfss():
    try:
        kwargs = {k: request.form.get(k) for k in request.form.keys()}
        data = CustomDataBRFSS(**kwargs)
        final_data = data.get_data_as_dataframe()
        
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_data, dataset_type='brfss')
        result = round(pred[0], 2)
        return render_template("result.html", final_result=result, mode="Deep Lifestyle Analysis")

    except Exception as e:
        error_message = f"Error during BRFSS prediction: {str(e)}"
        return render_template("error.html", error_message=error_message)

# Execution begins
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
