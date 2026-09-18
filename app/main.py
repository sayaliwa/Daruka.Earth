from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title=os.getenv(
        "APP_NAME",
        "Darukaa Biodiversity Intelligence Engine"
    ),
    description="AI-powered biodiversity and environmental intelligence system",
    version="0.1.0"
)


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