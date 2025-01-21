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

with open('./models/model.pkl', 'rb') as file:
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
# class Choroba(BaseModel):
#     choroba_name: str

class P(BaseModel):
    age: int
    education: int
    sex: int
    is_smoking: int
    cigsPerDay: int
    BPMeds: int
    prevalentStroke: int
    prevalentHyp: int
    diabetes: int
    totChol: float
    sysBP: float
    diaBP: float
    bmi: float
    heartRate: int
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
        features = np.array([[
            data.age,
            data.education,
            data.sex,
            data.is_smoking,
            data.cigsPerDay,
            data.BPMeds,
            data.prevalentStroke,
            data.prevalentHyp,
            data.diabetes,
            data.totChol,
            data.sysBP,
            data.diaBP,
            data.bmi,
            data.heartRate,
            data.glucose
        ]])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Nieprawidłowy format danych: {e}")

        # Przewidywanie
    prediction = model.predict(features)

    # Zwrócenie wyniku
    return {"prediction": prediction.tolist()}

