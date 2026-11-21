import os
import urllib.request
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.features import prepare_features


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "house_price_pipeline.joblib"
)

DEFAULT_MODEL_URL = (
    "https://github.com/Kutlay07/house-price-ml-system/"
    "releases/download/model-v1/house_price_pipeline.joblib"
)

MODEL_URL = os.getenv("MODEL_URL", DEFAULT_MODEL_URL)

def ensure_model():
    if MODEL_PATH.exists():
        return

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading model from {MODEL_URL}...", flush=True)
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Model downloaded successfully.", flush=True)


def load_model():
    ensure_model()
    return joblib.load(MODEL_PATH)


def predict_price(model, raw_df):
    prepared_df = prepare_features(raw_df)

    prediction_log = model.predict(prepared_df)

    prediction = np.expm1(prediction_log)

    return prediction


if  __name__ == "__main__":
    model = load_model()

    raw_df = pd.read_csv("tests/fixtures/sample_houses.csv")

    raw_df = raw_df.drop(columns=["Id"])

    prediction = predict_price(model, raw_df)

    print("Predicted price:", prediction[0])
