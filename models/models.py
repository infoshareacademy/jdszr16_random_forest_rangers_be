from pydantic import BaseModel

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