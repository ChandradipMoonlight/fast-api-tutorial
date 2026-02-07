from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(
    prefix = "/patients",
    tags = ["Patients API"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# PATIENT_FILE = "fastapi-tutorial/app/data/patients.json"
PATIENT_FILE = f"{BASE_DIR}/app/data/patients.json"

def read_patients_data():
    with open(PATIENT_FILE, "r") as file:
        data = json.load(file)
    return data

@router.get("/")
def get_patients_data():
    return read_patients_data();            

@router.get("/file/path")
def get_file_path():
    return {
        "base_dir": BASE_DIR,
        "file_path": PATIENT_FILE
    }
