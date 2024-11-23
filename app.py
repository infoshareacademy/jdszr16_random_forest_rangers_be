from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
class User(BaseModel):
    username: str

@app.post('/test')
def test_data(user: User):
    # Rozdzielenie na imię i nazwisko
    parts = user.username.split()
    if len(parts) == 2:  # Sprawdzamy, czy jest dokładnie imię i nazwisko
        reversed_name = f"{parts[1]} {parts[0]}"  # Zamiana kolejności
    else:
        reversed_name = user.username  # Jeśli brak nazwiska, zwróć bez zmian

    return {"message": "Odpowiedz z Backend " + reversed_name}