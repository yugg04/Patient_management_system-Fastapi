from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import os

app = FastAPI(title="Carelytics API")

# ----------------------------
# Paths (RENDER SAFE)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "patients.json")

# ----------------------------
# CORS (REQUIRED)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Serve Frontend
# ----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return FileResponse("static/index.html")

# ----------------------------
# Models
# ----------------------------
class Patient(BaseModel):
    id: Annotated[str, Field(...)]
    name: str
    city: str
    age: Annotated[int, Field(gt=0, lt=120)]
    gender: Literal["male", "female", "others"]
    height: Annotated[float, Field(gt=0)]
    weight: Annotated[float, Field(gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        return "Obese"

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal["male", "female", "others"]] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

# ----------------------------
# Helpers
# ----------------------------
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------------------------
# Routes
# ----------------------------
@app.get("/view")
def view_all_patients():
    return load_data()

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created"})

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, updates: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    record = data[patient_id]
    for k, v in updates.model_dump(exclude_unset=True).items():
        record[k] = v

    record["id"] = patient_id
    validated = Patient(**record)
    data[patient_id] = validated.model_dump(exclude={"id"})
    save_data(data)
    return {"message": "Patient updated"}

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return {"message": "Patient deleted"}
