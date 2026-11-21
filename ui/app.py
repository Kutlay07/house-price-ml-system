import json
import os
import random
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

API_URL = st.secrets.get(
    "API_URL",
    os.getenv(
        "API_URL",
        "http://localhost:8000/predict"
    ),
)


st.title("House Price Prediction")

st.write(
    "Choose an example house, modify its main features, "
    "or generate random variation."
)

BASE_DIR = Path(__file__).resolve().parents[1]

SAMPLE_HOUSES_PATH = (
    BASE_DIR
    / "tests"
    / "fixtures"
    / "sample_houses.csv"
)

df = pd.read_csv(SAMPLE_HOUSES_PATH)

# ------------------
# Session State
# ------------------

if "random_values" not in st.session_state:
    st.session_state.random_values = {}

# ------------------
# Preset House
# ------------------

house_option = st.selectbox(
    "Choose Example House",
    options=list(range(len(df))),
    format_func=lambda i: f"House {i + 1}"
)

selected_row = df.iloc[house_option]

# -------------------
# Random House
# -------------------

if st.button("Generate Random House"):
    st.session_state.random_values = {
        "LotArea": random.randint(5000, 20000),
        "OverallQual": random.randint(3, 9),
        "GrLivArea": random.randint(700, 2500),
        "YearBuilt": random.randint(1950, 2010),
        "FullBath": random.randint(1, 3),
        "GarageCars": random.randint(0, 3),
    }

if st.button("Reset to Preset"):
    st.session_state.random_values = {}

# -----------------
# Defaults
# -----------------

lot_area_default = st.session_state.random_values.get(
    "LotArea",
    int(selected_row["LotArea"])
)

overall_qual_default = st.session_state.random_values.get(
    "OverallQual",
    int(selected_row["OverallQual"])
)

gr_liv_area_default = st.session_state.random_values.get(
    "GrLivArea",
    int(selected_row["GrLivArea"])
)

year_built_default = st.session_state.random_values.get(
    "YearBuilt",
    int(selected_row["YearBuilt"])
)

full_bath_default = st.session_state.random_values.get(
    "FullBath",
    int(selected_row["FullBath"])
)

garage_cars_default = st.session_state.random_values.get(
    "GarageCars",
    int(selected_row["GarageCars"])
)


# ------------------
# Input Layout
# ------------------

col1, col2 = st.columns(2)

with col1:
    lot_area = st.number_input(
        "Lot Area",
        min_value=0,
        value=lot_area_default,
    )

    gr_liv_area = st.number_input(
        "Living Area",
        min_value=0,
        value=gr_liv_area_default,
    )

    full_bath = st.number_input(
        "Full Bathrooms",
        min_value=0,
        value=full_bath_default,
    )

with col2:
    overall_qual = st.slider(
        "Overall Quality",
        min_value=1,
        max_value=10,
        value=overall_qual_default,
    )

    year_built = st.number_input(
        "Year Built",
        min_value=1800,
        max_value=2026,
        value=year_built_default,
    )

    garage_cars = st.number_input(
        "Garage Cars",
        min_value=0,
        value=garage_cars_default,
    )


# -------------------
# Prediction
# -------------------

if st.button("Predict"):
    row = selected_row.drop(labels=["Id"])
    payload = json.loads(row.to_json())

    payload["LotArea"] = lot_area
    payload["OverallQual"] = overall_qual
    payload["GrLivArea"] = gr_liv_area
    payload["YearBuilt"] = year_built
    payload["FullBath"] = full_bath
    payload["GarageCars"] = garage_cars

    try:
        with st.spinner("Predicting house price..."):
            response = requests.post(
                API_URL,
                json=payload,
                timeout=60
            )

        if response.status_code == 200:
            result = response.json()

            st.metric(
                "Predicted Price",
                f"${result['predicted_price']:,.2f}"
            )

        else:
            st.error(
                f"Prediction failed with status code "
                f"{response.status_code}."
            )

    except requests.RequestException:
        st.error(
            "The prediction API may be waking up from sleep. "
            "Please wait a few seconds and try again."
        )
