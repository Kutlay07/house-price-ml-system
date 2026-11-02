import pandas as pd

from src.features import prepare_features


def test_prepares_features_adds_engineered_columns():
    df = pd.read_csv("tests/fixtures/sample_houses.csv")
    df = df.drop(columns=["Id"])

    prepared = prepare_features(df)

    assert "HasGarage" in prepared.columns
    assert "TotalSF" in prepared.columns
    assert "HouseAge" in prepared.columns
    assert "RemodAge" in prepared.columns
    assert "GarageAge" in prepared.columns
    assert "TotalBathrooms" in prepared.columns
    assert len(prepared) == len(df)
