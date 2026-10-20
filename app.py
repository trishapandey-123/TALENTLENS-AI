from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="TalentLens AI Engine")

# Frontend (HTML/JS) se communication allow karne ke liye CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- DATA MODELS ----------------- #
class CandidateLogin(BaseModel):
    email: str
    password: str

class CandidateProfile(BaseModel):
    name: str
    target_role: str
    ats_score: int
    match_status: str
    skills_breakdown: Dict[str, int]
    recommended_action: str

class InterviewAnswer(BaseModel):
    question_id: int
    candidate_answer: str

# ----------------- IN-MEMORY STORE / DUMMY ENGINE ----------------- #
# (Baad me yahan resume parsing aur actual AI model add karenge)
DEFAULT_CANDIDATE = {
    "name": "John Doe",
    "target_role": "Full Stack Developer",
    "ats_score": 78,
    "match_status": "Strong Fit",
    "skills_breakdown": {
        "React / Frontend Architecture": 92,
        "Node.js / Express & API Design": 84,
        "Redis & Caching Strategies": 65,
        "Distributed Architecture & System Probing": 70
    },
    "recommended_action": "Technical Validation Round focusing on distributed caching & edge cases."
}

# ----------------- API ROUTES ----------------- #

@app.get("/")
def home():
    return {"message": "TalentLens AI Backend is running successfully!"}

# 1. Login Authentication Endpoint
@app.post("/api/login")
def login(auth: CandidateLogin):
    # Dummy check for now
    if auth.email and auth.password:
        return {
            "status": "success",
            "message": "Authenticated",
            "candidate": DEFAULT_CANDIDATE
        }
    raise HTTPException(status_code=400, detail="Invalid credentials")

# 2. ATS Dashboard Data Endpoint
@app.get("/api/candidate-ats", response_model=CandidateProfile)
def get_ats_metrics():
    return DEFAULT_CANDIDATE

# 3. Real-time Adaptive Probing Engine Endpoint
@app.post("/api/evaluate-response")
def evaluate_answer(submission: InterviewAnswer):
    # Rule-based/NLP simulated adaptive probing
    answer_text = submission.candidate_answer.lower()
    
    if "redis" in answer_text and "cluster" in answer_text:
        follow_up = "How would your Redis pub/sub cluster prevent message loss during a sudden socket pod crash or network partition?"
        hit_points = ["Redis pub/sub", "Decoupled workers"]
    else:
        follow_up = "Could you elaborate on the latency trade-offs of using polling versus WebSockets in this architecture?"
        hit_points = ["WebSockets architecture"]

    return {
        "status": "evaluated",
        "probing_hit": ", ".join(hit_points),
        "follow_up_question": follow_up
    }

# 4. Final Comprehensive Report Scorecard Endpoint
@app.get("/api/final-report")
def get_final_report():
    return {
        "candidate_name": "John Doe",
        "role": "Full Stack Developer",
        "overall_score": 85,
        "verdict": "Qualified",
        "rubric_breakdown": [
            {"domain": "ATS Resume Match", "rating": "★★★★☆", "remark": "Strong React & Node foundation"},
            {"domain": "System Architecture", "rating": "★★★★☆", "remark": "Good Redis pub/sub clustering logic"},
            {"domain": "Adaptive Probing", "rating": "★★★★☆", "remark": "Needs practice on exponential backoff"},
            {"domain": "Project Authenticity", "rating": "★★★★☆", "remark": "Verified hands-on code understanding"},
            {"domain": "STAR Methodology", "rating": "★★★★☆", "remark": "Structured problem & solution flow"},
            {"domain": "Code & Edge Cases", "rating": "★★★★☆", "remark": "Handled reconnects & rate limits"}
        ]
    }