from typing import Union

from fastapi import FastAPI, Request, Depends, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api_calls.get_illness_info import get_illness_info
from api_calls.get_illness_treatment_plan import get_illness_treatment_plan
from dotenv import load_dotenv

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Odczyt z pliku scalera
with open('./models/scaler_info.pkl', 'rb') as file:
    scaler_info = pickle.load(file)  # Load the scaler_info dictionary
scaler = scaler_info['scaler']  # Pobranie skalera z pliku
scaled_columns = scaler_info['scaled_columns']  # Pobranie listy skalowanych kolumn
print('scaled_columns', scaled_columns)

with open('./models/model.pkl', 'rb') as file:
    model = pickle.load(file)

# min_max_scaler = MinMaxScaler()

load_dotenv()
app = FastAPI()


# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jdszr16-random-forest-rangers-fe.onrender.com", "http://localhost:3000", "*"],  # Allow
    allow_credentials=True,
    allow_methods=["*"],  # Pozwala na wszystkie metody (GET, POST, PUT, DELETE itd.)
    allow_headers=["*"],  # Pozwala na wszystkie nagłówki
)

# Model danych
# class Choroba(BaseModel):
#     choroba_name: str

class P(BaseModel):
    age: int
    sex: int
    education: int
    cigsPerDay: int
    BPMeds: int
    prevalentStroke: int
    prevalentHyp: int
    diabetes: int
    totChol: float
    sysBP: float
    diaBP: float
    BMI: float
    glucose: int


@app.get('/')
def test():
    return {"message": "Odpowiedz z Backend"}

@app.get('/illness_more_info')
def illness_info(is_doctor: bool, length: int, disease: str):
    return get_illness_info(is_doctor, length, disease)

@app.get('/illness_treatment_plan')
def illness_treatment_plan(disease: str):
    return get_illness_treatment_plan(disease)

@app.post('/predict')
def predict(data: P):
    try:
        # Konwersja danych wejściowych na DataFrame
        data_dict = data.dict()
        print('data_dict', data_dict)
        input_data = pd.DataFrame([data_dict])

        # Skalowanie wybranych kolumn
        input_data[scaled_columns] = scaler.transform(input_data[scaled_columns])


        transformed_data = input_data.values
        prediction = model.predict_proba(transformed_data)
        print('transformedData', transformed_data)

        # Odwracanie skalowania
        # original_data = scaler.inverse_transform(transformed_data)
        # print('originData', original_data)



        return {
            "prediction": prediction.tolist(),

        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Nieprawidłowy format danych: {e}")
