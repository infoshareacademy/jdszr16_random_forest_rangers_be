from pydantic import BaseModel

class Choroba(BaseModel):
    choroba_name: str



# Klasa dla `formValues`
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

# Główna klasa dla całego requestu (zawiera `formValues` + `isDoctor`)
class RequestData(BaseModel):
    formValues: InputData
    isDoctor: bool