from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="AI Applicant Selection Tool")

# -------- DATA MODEL --------
class Applicant(BaseModel):
    name: str
    years_experience: float
    skills_score: float
    education_level: str   # e.g. "Bachelor", "Master", "PhD"
    portfolio_score: float # rating from 0–10
    soft_skills: float     # rating from 0–10

# -------- EDUCATION WEIGHTING --------
education_weights = {
    "High School": 0.5,
    "Diploma": 0.7,
    "Bachelor": 1.0,
    "Master": 1.2,
    "PhD": 1.5
}

# -------- SMART SCORING MODEL --------
def ai_score(applicant: Applicant):
    # Normalize scores
    exp_weight = min(applicant.years_experience / 10, 1.0)
    skill_weight = applicant.skills_score / 10
    portfolio_weight = applicant.portfolio_score / 10
    soft_skill_weight = applicant.soft_skills / 10
    edu_weight = education_weights.get(applicant.education_level, 1.0)

    # Compute AI score
    final_score = (
        (exp_weight * 0.25) +
        (skill_weight * 0.25) +
        (portfolio_weight * 0.2) +
        (soft_skill_weight * 0.15)
    ) * edu_weight

    # Convert to percentage
    return round(final_score * 100, 2)

# -------- ROUTES --------
@app.get("/")
def home():
    return {"message": "AI Applicant Selection Tool is running with Smart Scoring"}

@app.post("/rank_applicant")
def rank_applicant(applicant: Applicant):
    try:
        score = ai_score(applicant)
        result = {
            "applicant_name": applicant.name,
            "education_level": applicant.education_level,
            "AI_score": score,
            "recommendation": "Highly Recommended" if score >= 75 else "Consider with Review" if score >= 50 else "Not Recommended"
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------- EXAMPLE --------
# Test with JSON:
# {
#   "name": "Jane Doe",
#   "years_experience": 5,
#   "skills_score": 8,
#   "education_level": "Master",
#   "portfolio_score": 9,
#   "soft_skills": 7
# }
