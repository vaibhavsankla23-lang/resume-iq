import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from .database import Base

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    job_title = Column(String)
    overall_score = Column(Float)
    tfidf_score = Column(Float)
    semantic_score = Column(Float)
    matched_skills = Column(Text)  # Saved as JSON string
    missing_skills = Column(Text)  # Saved as JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)