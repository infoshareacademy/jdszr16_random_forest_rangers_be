from typing import Union

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api_calls.get_illness_info import get_illness_info
from api_calls.get_illness_treatment_plan import get_illness_treatment_plan
from dotenv import load_dotenv

import os


load_dotenv()
app = FastAPI()


# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pozwala na żądania ze wszystkich domen. Zmień na listę domen, jeśli chcesz to ograniczyć.
    allow_credentials=True,
    allow_methods=["*"],  # Pozwala na wszystkie metody (GET, POST, PUT, DELETE itd.)
    allow_headers=["*"],  # Pozwala na wszystkie nagłówki
)

# Model danych
# class Choroba(BaseModel):
#     choroba_name: str

class P(BaseModel):
    difficulty: str
    length:  str


@app.get('/')
def test():
    return {"message": "Odpowiedz z Backend"}


@app.get('/illness_more_info')
def illness_info(is_doctor: bool, length: int, disease: str):
    return get_illness_info(is_doctor, length, disease)

@app.get('/illness_treatment_plan')
def illness_treatment_plan(disease: str):
    return get_illness_treatment_plan(disease)



