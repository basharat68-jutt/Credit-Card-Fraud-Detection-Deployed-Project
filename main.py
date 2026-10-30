import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated,Literal
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model_path = BASE_DIR / "credit_card_fraud_detection.pkl"

model = joblib.load(model_path)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


#A New Pydantic Model
class CardData(BaseModel):
     amount : float = Field(..., ge=0)
     transaction_hour : int = Field(..., ge=0)
     foreign_transaction : int = Field(..., ge=0)
     location_mismatch : int = Field(..., ge=0)
     device_trust_score : int = Field(..., ge=0)
     velocity_last_24h : int = Field(..., ge=0)
     cardholder_age : int = Field(...,ge=0)
     merchant_category : Literal['Electronics', 'Travel', 'Grocery', 'Food', 'Clothing']


#Describe What We Send Back
class PredictionResponse(BaseModel):
    is_fraud : int


@app.get('/')
def greet():
    return {'Wellcome to Model'}

@app.post('/predict', response_model=PredictionResponse)
def predict(data: CardData):
    input_row = pd.DataFrame([{
        'amount' : data.amount,
        'transaction_hour' : data.transaction_hour,
        'foreign_transaction' : data.foreign_transaction,
        'location_mismatch' : data.location_mismatch,
        'device_trust_score' : data.device_trust_score,
        'velocity_last_24h' : data.velocity_last_24h,
        'cardholder_age' : data.cardholder_age,
        'merchant_category' : data.merchant_category
    }])

    prediction = model.predict(input_row)[0]
    return PredictionResponse(is_fraud=prediction)

