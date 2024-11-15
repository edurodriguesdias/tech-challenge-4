from tensorflow.keras.models import load_model
import joblib
import json
import requests
import numpy as np
from fastapi import FastAPI
import pickle
from pydantic import BaseModel

class PredictionInput(BaseModel):
    ticker: str
    look_back: int
    dias_para_prever: int

def predict_future_price(ticker, look_back, dias_para_prever):

    modelo = load_model(f'data/{ticker}_modelo.h5')
    scaler = joblib.load(f'data/{ticker}_scaler.pkl')

    predictions = []
    current_input = scaled_data[-look_back:].reshape(1, look_back, 1)
    
    for _ in range(dias_para_prever):
        next_day_prediction = modelo.predict(current_input)
        next_day_prediction = scaler.inverse_transform(next_day_prediction)
        predictions.append(next_day_prediction[0][0])
        
        current_input = np.append(current_input[:, 1:, :], next_day_prediction.reshape(1, 1, 1), axis=1)
    predictions = [int(value) for value in predictions]

    return {"predictions": predictions}

app = FastAPI()
with open("data/scaled_data.pkl", 'rb') as file:
    scaled_data = pickle.load(file)

@app.post("/predict")
def predict(data:PredictionInput):
    return predict_future_price(data.ticker, data.look_back, data.dias_para_prever)