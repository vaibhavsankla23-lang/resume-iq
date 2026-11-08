import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Lazy-loaded model instance to prevent global startup RAM spikes & port timeouts
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading AI Model on demand...")
        _model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        print("AI Model Loaded Successfully!")
    return _model

PRESET_SKILLS = [
    "python", "javascript", "typescript", "react", "fastapi", "django", 
    "postgresql", "postgres", "docker", "git", "github", "machine learning", 
    "nlp", "scikit-learn", "tensorflow", "pytorch", "rest api", "rest apis", 
    "restful api", "html", "css", "sql", "aws", "kubernetes", "c++", "java", "node.js"
]

def extract_skills(text: str):
    if not text:
        return []
    text_lower = text.lower()
    found_skills = set()
    for skill in PRESET_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            display_name = skill.title()
            if "rest api" in skill:
                display_name = "REST API"
            elif skill == "postgresql" or skill == "postgres":
                display_name = "PostgreSQL"
            found_skills.add(display_name)
    return list(found_skills)

def calculate_tfidf_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(similarity)

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0
    model = get_model()  # Loads model only when needed
    embeddings = model.encode([text1, text2])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(similarity)

def analyze_resume_vs_jd(resume_text: str, jd_text: str):
    tfidf_score = round(calculate_tfidf_similarity(resume_text, jd_text) * 100, 2)
    semantic_score = round(calculate_semantic_similarity(resume_text, jd_text) * 100, 2)
    overall_score = round((tfidf_score * 0.3) + (semantic_score * 0.7), 2)

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    matched_skills = list(resume_skills.intersection(jd_skills))
    missing_skills = list(jd_skills - resume_skills)

    recommendations = []
    if missing_skills:
        recommendations.append(f"Add experience or mention keywords for: {', '.join(missing_skills)}.")
    if overall_score < 60:
        recommendations.append("Tailor your summary and experience section using keywords directly from the job description.")
    else:
        recommendations.append("Strong alignment! Ensure your impact metrics and achievements are clearly visible.")

    return {
        "overall_score": overall_score,
        "tfidf_score": tfidf_score,
        "semantic_score": semantic_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }