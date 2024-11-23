from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pozwala na żądania ze wszystkich domen. Zmień na listę domen, jeśli chcesz to ograniczyć.
    allow_credentials=True,
    allow_methods=["*"],  # Pozwala na wszystkie metody (GET, POST, PUT, DELETE itd.)
    allow_headers=["*"],  # Pozwala na wszystkie nagłówki
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/test')
def test_data():
    return {"value": 'This is just response from Back End'}