from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.features import prepare_features


MODEL_PATH = Path("models/house_price_pipeline.joblib")


def load_model():
    model = joblib.load(MODEL_PATH)
    return model


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
