import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from api.schemas import HouseFeatures
from src.predict import load_model, predict_price


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(house: HouseFeatures , request: Request):
    model = request.app.state.model

    house_dict = house.model_dump(by_alias=True)
    raw_df = pd.DataFrame([house_dict])

    prediction = predict_price(model, raw_df)

    return {"predicted_price": float(prediction[0])}
