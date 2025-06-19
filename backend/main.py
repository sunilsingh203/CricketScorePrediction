import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.predict import router as predict_router  # Import prediction router

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:5174",  # Your frontend
    "http://localhost:8000",  # For testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict_router)  # Prediction endpoints

# Health check endpoint
@app.get("/api/healthchecker")
def health_check():
    return {
        "status": "healthy",
        "message": "Cricket Score Predictor API is running",
        "endpoints": {
            "prediction": "/api/predict (POST)",
            "health": "/api/healthchecker (GET)"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload during development
    )