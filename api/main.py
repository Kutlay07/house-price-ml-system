import json

import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from fastapi.responses import Response

from api.schemas import HouseFeatures
from src.predict import load_model, predict_price
from api.logging import logger, register_logging_middleware
from api.metrics import (
    PREDICTION_VALUE,
    LOT_AREA,
    OVERALL_QUAL,
    GR_LIV_AREA,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()

    yield


app = FastAPI(lifespan=lifespan)

register_logging_middleware(app)

MODEL_VERSION = "v1"

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(house: HouseFeatures , request: Request):
    model = request.app.state.model

    LOT_AREA.observe(house.LotArea)
    OVERALL_QUAL.observe(house.OverallQual)
    GR_LIV_AREA.observe(house.GrLivArea)

    house_dict = house.model_dump(by_alias=True)
    raw_df = pd.DataFrame([house_dict])

    prediction = predict_price(model, raw_df)

    PREDICTION_VALUE.observe(float(prediction[0]))

    logger.info(
        json.dumps(
            {
                "event": "prediction",
                "request_id": request.state.request_id,
                "model_version": MODEL_VERSION,
                "predicted_price": float(prediction[0])
            }
        )
    )

    return {"predicted_price": float(prediction[0])}


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
