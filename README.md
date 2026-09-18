# 🌱 Darukaa.Earth — AI Biodiversity Intelligence Engine

An AI-powered environmental intelligence system that analyzes environmental conditions, identifies relationships between multiple biodiversity metrics, retrieves scientific evidence using RAG, and generates actionable recommendations.

---

## 🎯 Problem Statement

Environmental information such as soil, climate, land use, biodiversity, pollution, and deforestation is often fragmented across different datasets and scientific sources.

Darukaa.Earth integrates these factors to provide a unified environmental assessment and evidence-backed biodiversity recommendations.

---

## 🎯 Objectives

- Analyze environmental conditions
- Identify multi-metric environmental relationships
- Connect soil, water, climate, land use and biodiversity
- Retrieve scientific evidence using RAG
- Generate evidence-backed recommendations
- Support conversational follow-up questions
- Provide structured environmental insights

---

## ✨ Key Features

- 🌱 Environmental assessment
- 🔗 Multi-metric reasoning
- 📚 Scientific RAG
- 🔎 Evidence-backed recommendations
- 💬 Conversational AI with session memory
- 📊 Structured JSON input
- 🗺️ Location-based environmental data

---

## 🏗️ Architecture

```text
User
 ↓
Streamlit Frontend
 ↓
FastAPI Backend
 ↓
Environmental State Engine
 ↓
Multi-Metric Reasoning
 ↓
 ┌───────────────┐
 │               │
 ▼               ▼
Rules           RAG
                 ↓
             ChromaDB
                 ↓
          Scientific Sources
                 ↓
                LLM
                 ↓
       Recommendation
                 ↓
              User
```

---
### 📚 RAG Pipeline

```text
Scientific PDF Documents
          ↓
     PDF Extraction
          ↓
      Text Chunking
          ↓
       Embeddings
          ↓
       ChromaDB
          ↓
      User Query
          ↓
    Query Embedding
          ↓
  Similarity Retrieval
          ↓
Relevant Scientific Evidence
          ↓
          LLM
          ↓
Scientific Explanation
```

---

## 📚 Scientific Knowledge Base

The RAG knowledge base currently uses environmental documents from:

- FAO
- IPCC
- IPBES

Documents are processed as:

```text
PDF → Text Extraction → Chunking → Embeddings → ChromaDB → Retrieval
```

Each retrieved document stores:

- Source
- Organization
- Page
- Chunk
- Evidence text

---

## 📊 Environmental Metrics

The system works with:

| Category       | Metrics                             |
| -------------- | ----------------------------------- |
| Soil           | pH, Organic Carbon, Moisture        |
| Climate        | Temperature, Rainfall               |
| Land           | Land Use, Tree Cover                |
| Biodiversity   | Species Richness, Habitat Diversity |
| Human Pressure | Pollution, Deforestation            |

> **Note:** The included environmental dataset contains demonstration/sample observations and is not intended to represent verified field measurements.

---

## 🛠️ Technology Stack

- Python
- FastAPI
- Streamlit
- Pandas
- ChromaDB
- Sentence Transformers
- pypdf
- OpenAI API
- Git & GitHub

---

## 📁 Project Structure

text
Daruka.Earth/
│
├── app/
│   │
│   ├── api/
│   │   ├── chat.py
│   │   └── assessment.py
│   │
│   ├── conversation/
│   │   ├── memory.py
│   │   └── chat.py
│   │
│   ├── rag/
│   │   ├── embeddings.py
│   │   ├── ingestion.py
│   │   ├── chunking.py
│   │   ├── vectorstore.py
│   │   └── retriever.py
│   │
│   ├── models/
│   │   └── input_models.py
│   │
│   ├── data_loader.py
│   ├── environmental_state.py
│   ├── multi_metric.py
│   ├── recommendations.py
│   ├── llm.py
│   └── main.py
│
├── knowledge/
│   ├── documents/
│   │   ├── fao/
│   │   ├── ipcc/
│   │   ├── ipbes/
│   │   └── papers/
│   │
│   ├── environmental_rules.json
│   └── vector_db/
│
├── data/
│   └── environmental_metrics.csv
│
├── frontend/
│   └── app.py
│
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

---

## 🚀 Local Setup

### 1. Clone

```bash
git clone https://github.com/sayaliwa/Daruka.Earth.git
cd Daruka.Earth
```

### 2. Create Environment

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o
```

> Do not commit the real API key.

### 5. Start Backend

```bash
uvicorn app.main:app --reload
```

API available at: `http://127.0.0.1:8000`

### 6. Start Frontend

```bash
streamlit run frontend/app.py
```

---

## 🔌 API Endpoints

| Endpoint      | Purpose                              |
| ------------- | ------------------------------------ |
| GET /health   | Backend health check                 |
| POST /assess/ | Environmental assessment             |
| POST /chat/   | Conversational biodiversity analysis |

FastAPI documentation: `http://127.0.0.1:8000/docs`

---

## 💬 Example Questions

- What is the biodiversity condition?
- What should I improve first?
- Why is soil moisture important?
- How does soil organic carbon affect biodiversity?
- How does land use affect habitat diversity?

---

## 🧪 Testing

The project has been tested for:

- Environmental assessment
- Multi-metric reasoning
- Scientific RAG retrieval
- Conversational memory
- JSON input
- API endpoints
- Streamlit frontend

---

## 🔐 Security

- API keys are stored in `.env`
- `.env` should not be committed to GitHub
- Use `.env.example` for required environment variables
- No private credentials should be included in the repository

---

## ⚠️ Limitations

- Current environmental dataset is demonstration data
- Confidence and priority values are heuristic
- Chat memory is currently stored in application memory
- Advanced GIS and real-time environmental data are future enhancements

---

## 🔮 Future Scope

- GIS and satellite-data integration
- Real-time environmental APIs
- Biodiversity databases
- Environmental forecasting
- Persistent conversation storage
- Cloud deployment
- Automated CI/CD
- Advanced geospatial reasoning

---

## 📌 Project Status

**Working Prototype — Hackathon Submission**

The system integrates:

```text
Environmental Data
+ Multi-Metric Reasoning
+ Scientific RAG
+ ChromaDB
+ LLM
+ Conversational AI
```

---
## 🔄 CI/CD

**CI/CD configuration will be added as part of the final deployment setup**

The project currently uses:

- Git
- GitHub
- Version-controlled source code

- The final repository will document the CI/CD workflow once configured.

## 🔗 Links

- **GitHub:** https://github.com/sayaliwa/Daruka.Earth.git
- **Live Demo:** Coming soon
- **API Docs:** http://127.0.0.1:8000/docs (when running locally)

---

## 👤 Project

**Darukaa.Earth — AI Biodiversity Intelligence Engine**  
Environmental Data + AI + RAG + Multi-Metric Reasoning + Scientific Evidence
