# 📄 ResumeIQ - AI-Powered Resume & Job Matching Engine

ResumeIQ is an intelligent enterprise job-matching and resume analysis platform. It leverages Hybrid Natural Language Processing (combining TF-IDF keyword extraction and Transformer-based Semantic Embeddings) to evaluate candidate resumes against target job descriptions, calculate compatibility scores, perform skill gap analysis, and persist historical logs in PostgreSQL.

---

## 🚀 Key Features

- **📄 Automated Resume Parsing**: Extracts text cleanly from PDF resumes.
- **⚡ Hybrid AI Matching Engine**: 
  - **TF-IDF Keyword Matching**: Evaluates hard-skill overlap and exact vocabulary alignment.
  - **Semantic Vector Embeddings**: Utilizes Sentence-Transformers to understand context, underlying experience, and related skill domain proximity.
- **🎯 Skill Gap Analysis**: Automatically isolates matched skills vs. missing candidate skills.
- **💡 Actionable AI Recommendations**: Delivers targeted insights for candidate resume optimization.
- **📊 Persisted Analysis History**: Stores every analysis run with timestamps and compatibility metrics in a PostgreSQL database.
- **🐳 Full Containerization**: Standardized deployment across microservices using Docker Compose.

---

## 🏗 System Architecture & Tech Stack

### **Backend**
- **Framework**: Python 3.10+, FastAPI (Asynchronous REST API)
- **NLP & AI Engine**: Sentence-Transformers, Scikit-learn (TF-IDF & Cosine Similarity), PyPDF2
- **Database**: PostgreSQL 15 managed via SQLAlchemy ORM
- **Server**: Uvicorn ASGI

### **Frontend**
- **Framework**: React 18, Vite
- **UI Components**: Modern Dark Theme with CSS / Tailwind styling
- **HTTP Client**: Axios

### **Infrastructure & Orchestration**
- **Containerization**: Docker & Docker Compose

---

## 🛠️ Project Structure

```text
resume-iq/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI Entry Point & REST Routes
│   │   ├── database.py        # PostgreSQL Connection & Engine setup
│   │   ├── models.py          # SQLAlchemy Database Models
│   │   ├── schemas.py         # Pydantic Request/Response Schemas
│   │   └── analyzer.py        # NLP, TF-IDF & Semantic Matching Engine
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React UI Component
│   │   └── main.jsx           # Vite Mount Point
│   ├── index.html
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
