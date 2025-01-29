from typing import Union

from fastapi import FastAPI, Request, Depends, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api_calls.get_illness_info import get_illness_info
from api_calls.get_illness_treatment_plan import get_illness_treatment_plan
from dotenv import load_dotenv
# import eli5
# from eli5.sklearn import PermutationImportance

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# min_max_scaler = MinMaxScaler()

# Odczyt z pliku scalera
# with open('./models/scaler_info.pkl', 'rb') as file:
#     scaler_info = pickle.load(file)  # Load the scaler_info dictionary
# scaler = scaler_info['scaler']  # Pobranie skalera z pliku
# scaled_columns = scaler_info['scaled_columns']  # Pobranie listy skalowanych kolumn
# print('scaled_columns', scaled_columns)



# Lista kolumn w kolejności, jakiej oczekuje model
FEATURE_COLUMNS = [
    'sex', 'age', 'education', 'cigsPerDay', 'BPMeds', 'prevalentStroke',
    'prevalentHyp', 'diabetes', 'totChol', 'sysBP', 'diaBP', 'BMI', 'glucose'
]


with open('./models/calibrated_pipeline.pkl', 'rb') as file:
    model = pickle.load(file)



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
class Choroba(BaseModel):
    choroba_name: str


class InputData(BaseModel):
    sex: int
    age: int
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
def predict(data: InputData):

    try:

        input_vector = np.array([
            int(data.sex),
            data.age,
            int(data.education),
            data.cigsPerDay,
            int(data.BPMeds),
            int(data.prevalentStroke),
            int(data.prevalentHyp),
            int(data.diabetes),
            data.totChol,
            data.sysBP,
            data.diaBP,
            data.BMI,
            data.glucose,
        ]).reshape(1, -1)  # Konwersja do formatu (1, n_features)


        input_df = pd.DataFrame([data.dict()], columns=FEATURE_COLUMNS)

        # Model wykonuje preprocessing wewnętrznie
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]  # Prawdopodobieństwo klasy pozytywnej

        return {
            "prediction": int(prediction),
            "probability": float(probability)
        }


    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Nieprawidłowy format danych: {e}")


