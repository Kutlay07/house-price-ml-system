import math
import json

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict(client):
    df = pd.read_csv("tests/fixtures/sample_houses.csv")

    row = df.drop(columns=["Id"]).iloc[0]

    payload = json.loads(row.to_json())

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "predicted_price" in data
    assert data["predicted_price"] > 0
    assert math.isfinite(data["predicted_price"])
