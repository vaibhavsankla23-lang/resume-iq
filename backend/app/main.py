import json
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import AnalysisHistory
from .pdf_parser import extract_text_from_pdf
from .nlp_engine import analyze_resume_vs_jd

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ResumeIQ API")

# Allow CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ResumeIQ Backend is live!"}

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_title: str = Form("Target Role"),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Process PDF
    pdf_text = extract_text_from_pdf(file.file)
    if not pdf_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    # NLP Analysis Engine
    result = analyze_resume_vs_jd(pdf_text, job_description)

    # Persist in Database
    history_item = AnalysisHistory(
        filename=file.filename,
        job_title=job_title,
        overall_score=result["overall_score"],
        tfidf_score=result["tfidf_score"],
        semantic_score=result["semantic_score"],
        matched_skills=json.dumps(result["matched_skills"]),
        missing_skills=json.dumps(result["missing_skills"])
    )
    db.add(history_item)
    db.commit()
    db.refresh(history_item)

    result["id"] = history_item.id
    result["filename"] = file.filename
    result["job_title"] = job_title
    return result

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(AnalysisHistory).order_by(AnalysisHistory.created_at.desc()).all()
    out = []
    for r in records:
        out.append({
            "id": r.id,
            "filename": r.filename,
            "job_title": r.job_title,
            "overall_score": r.overall_score,
            "matched_skills": json.loads(r.matched_skills),
            "missing_skills": json.loads(r.missing_skills),
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return out