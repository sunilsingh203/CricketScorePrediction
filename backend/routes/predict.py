# backend/routes/predict.py
from fastapi import APIRouter, HTTPException, Request
import joblib
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Load your ML model
try:
    model = joblib.load("ML_Models/RF_regressor_cricket.pkl")
except FileNotFoundError:
    raise RuntimeError("ML model file not found!")


# Define request model matching your form fields
class CricketPredictionInput(BaseModel):
    powerPlay: int
    AverageScore: float
    delivery_left: int
    Score: int
    CurrentRunRate: float
    wicketsLeft: int
    Run_In_Last5: int
    Wickets_In_Last5: int
    innings: int


@router.post("/api/predict")
async def predict_score(request: Request):
    """
    Predicts final T20 score based on form inputs.

    Expects form-data with these exact fields:
    - powerPlay (int)
    - AverageScore (float)
    - delivery_left (int)
    - Score (int)
    - CurrentRunRate (float)
    - wicketsLeft (int)
    - Run_In_Last5 (int)
    - Wickets_In_Last5 (int)
    - innings (int)
    """
    try:
        form_data = await request.form()

        # Prepare input features in exact order expected by your model
        features = [
            [
                int(form_data['powerPlay']),
                float(form_data['AverageScore']),
                int(form_data['delivery_left']),
                int(form_data['Score']),
                float(form_data['CurrentRunRate']),
                int(form_data['wicketsLeft']),
                int(form_data['Run_In_Last5']),
                int(form_data['Wickets_In_Last5']),
                int(form_data['innings'])
            ]
        ]

        # Get prediction
        prediction = model.predict(features)[0]

        return {
            "predicted_score": float(prediction),
            "input_data": {k: float(v) if k in ['AverageScore', 'CurrentRunRate'] else int(v)
                           for k, v in form_data.items()},
            "timestamp": datetime.now().isoformat()
        }

    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required field: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid data type: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )