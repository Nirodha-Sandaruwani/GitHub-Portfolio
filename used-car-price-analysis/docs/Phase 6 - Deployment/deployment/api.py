from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import json
import numpy as np
import pandas as pd
from typing import Dict, Any

MODEL_PATH = "model.joblib"
FEATURES_PATH = "feature_columns.json"
MAPPINGS_PATH = "mappings.json"

LOG_TARGET = True  # model trained on price_log


# ---------- Load artifacts ----------
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Could not load model from {MODEL_PATH}: {e}")

try:
    FEATURE_COLS = json.load(open(FEATURES_PATH, "r", encoding="utf-8"))
except Exception as e:
    raise RuntimeError(f"Could not load feature columns from {FEATURES_PATH}: {e}")

try:
    MAPPINGS: Dict[str, Dict[str, int]] = json.load(open(MAPPINGS_PATH, "r", encoding="utf-8"))
except Exception as e:
    raise RuntimeError(f"Could not load mappings from {MAPPINGS_PATH}: {e}")


def labels_sorted_by_code(col: str):
    m = MAPPINGS.get(col, {})
    return [k for k, v in sorted(m.items(), key=lambda kv: int(kv[1]))]


def encode(col: str, value: str) -> int:
    mapping = MAPPINGS.get(col, {})
    if value not in mapping:
        valid = ", ".join(mapping.keys())
        raise HTTPException(status_code=400, detail=f"Invalid {col}: '{value}'. Valid: {valid}")
    return int(mapping[value])


# ---------- API ----------
app = FastAPI(title="Used Car Price Prediction API (Phase 6 Demo)")

# Optional but helpful when Streamlit runs on another port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CarInput(BaseModel):
    year: int = Field(..., ge=1980, le=2026)
    combined_fuel_economy: float = Field(..., ge=0)
    mileage: float = Field(..., ge=0)

    fuel_type: str
    transmission: str
    body_type: str
    engine_type: str
    wheel_system: str

    # Accept 0/1 or true/false
    has_incidents: int = Field(0, ge=0, le=1)

    horsepower: float = Field(..., ge=0)
    torque: float = Field(..., ge=0)
    legroom: float = Field(..., ge=0)
    maximum_seating: int = Field(..., ge=1, le=10)
    size_of_vehicle: float = Field(..., ge=0)
    major_options_count: float = Field(..., ge=0)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "n_features": len(FEATURE_COLS),
        "log_target": LOG_TARGET,
        "feature_columns": FEATURE_COLS,
    }


@app.get("/codes")
def codes():
    return {
        "fuel_type": labels_sorted_by_code("fuel_type"),
        "transmission": labels_sorted_by_code("transmission"),
        "body_type": labels_sorted_by_code("body_type"),
        "engine_type": labels_sorted_by_code("engine_type"),
        "wheel_system": labels_sorted_by_code("wheel_system"),
        "has_incidents": [0, 1],
    }


@app.post("/predict")
def predict(x: CarInput) -> Dict[str, Any]:
    encoded_row = {
        "year": int(x.year),
        "combined_fuel_economy": float(x.combined_fuel_economy),
        "mileage": float(x.mileage),

        "fuel_type": encode("fuel_type", x.fuel_type),
        "transmission": encode("transmission", x.transmission),
        "body_type": encode("body_type", x.body_type),
        "engine_type": encode("engine_type", x.engine_type),
        "wheel_system": encode("wheel_system", x.wheel_system),

        "horsepower": float(x.horsepower),
        "torque": float(x.torque),
        "legroom": float(x.legroom),
        "maximum_seating": int(x.maximum_seating),
        "size_of_vehicle": float(x.size_of_vehicle),
        "major_options_count": float(x.major_options_count),

        "has_incidents": int(x.has_incidents),
    }

    # Ensure correct order
    X = pd.DataFrame([[encoded_row[c] for c in FEATURE_COLS]], columns=FEATURE_COLS)

    pred_log = float(model.predict(X)[0])

    if LOG_TARGET:
        pred_price = float(np.exp(pred_log))
        return {
            "predicted_price": pred_price,
            "predicted_log_price": pred_log,
            "encoded_inputs": encoded_row,
        }

    return {"prediction": pred_log, "encoded_inputs": encoded_row}
