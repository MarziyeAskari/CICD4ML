from pathlib import Path
import gradio as gr

from skops.io import get_untrusted_types, load

MODEL_PATH = Path("./Model/drug_pipeline.skops").resolve()

trusted = get_untrusted_types(file=MODEL_PATH)
pipe = load(MODEL_PATH, trusted=trusted)

def predict_drug(age, sex, blood_pressure, cholesterol, na_to_k_ratio):
    """Predict drugs based on patient features."""
    features = [age, sex, blood_pressure, cholesterol, na_to_k_ratio]
    predicted_drug = pipe.predict([features])[0]  # wrap in list
    return f"Predicted Drug: {predicted_drug}"

inputs = [
    gr.Slider(15, 74, step=1, label="Age"),
    gr.Radio(["M", "F"], label="Sex"),
    gr.Radio(["HIGH", "LOW", "NORMAL"], label="Blood Pressure"),
    gr.Radio(["HIGH", "NORMAL"], label="Cholesterol"),
    gr.Slider(6.2, 38.2, step=0.1, label="Na to K Ratio"),
]

outputs = [gr.Label(num_top_classes=3)]

examples = [
    [30, "M", "HIGH", "NORMAL", 15.4],
    [35, "F", "LOW", "NORMAL", 8],
    [50, "M", "HIGH", "HIGH", 34],
]

title = "Drug Classification"
description = "Enter the details to correctly identify Drug type"
article = "This app is a part of the Beginner's Guide to CI/CD for Machine Learning. It teaches how to automate training, evaluation, and deployment of models to Hugging Face using Github Actions."

gr.Interface(
    fn=predict_drug,
    inputs=inputs,
    outputs=outputs,
    title=title,
    description=description,
    article=article,
    examples=examples
).launch(theme=gr.themes.Soft())
