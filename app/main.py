from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.api.chat import router as chat_router
from app.api.assessment import router as assessment_router
load_dotenv()

app = FastAPI(
    title=os.getenv(
        "APP_NAME",
        "Darukaa Biodiversity Intelligence Engine"
    ),
    description="AI-powered biodiversity and environmental intelligence system",
    version="0.1.0"
)

app.include_router(chat_router)
app.include_router(assessment_router)

@app.get("/")
def root():
    return {
        "message": "Darukaa Biodiversity Intelligence Engine is running",
        "status": "ok",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }