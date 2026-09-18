# Darukaa Biodiversity Intelligence AI

An AI-powered environmental intelligence system for biodiversity assessment and evidence-backed ecological recommendations.

## Current Status

Stage 1 - Backend foundation

## Technology

- Python
- FastAPI
- Pydantic
- Uvicorn

## Current Features

- FastAPI backend
- Health check endpoint
- Environment configuration
- API documentation through Swagger

## Planned Features

- Environmental state modeling
- Scientific knowledge base
- RAG pipeline
- Vector database
- Multi-metric environmental reasoning
- Evidence-backed recommendations
- Conversational memory
- Streamlit interface
- Docker deployment

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload