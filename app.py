from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/test')
def test_data():
    return {"value": 'This is just response from Back End'}