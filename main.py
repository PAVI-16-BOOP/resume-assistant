from fastapi import FastAPI
from app.parser import extract_text_from_pdf, split_sections
from app.scoring import (
    exact_match,
    similarity_score,
    final_score,
    achievement_score,
    ownership_score,
    get_jd_weights,
    explain,
    classify
)
from app.utils import extract_skills
from app.questions import generate_questions

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Resume Assistant API running"}


# -------------------------------
# CORE LOGIC (your existing code wrapped)
# -------------------------------
def process(resume_text, jd_text):

    # PARSE
    resume_sections = split_sections(resume_text)
    jd_sections = split_sections(jd_text)

    # SKILLS
    resume_skills = extract_skills(resume_sections)
    jd_skills = extract_skills(jd_sections)

    # SCORING
    e, matched, missing = exact_match(resume_sections, jd_sections)
    s = similarity_score(resume_sections, jd_sections)

    a = achievement_score(resume_text)
    o = ownership_score(resume_text)

    final = final_score(e, s, a, o)

    # EXPLAINABILITY
    jd_weights = get_jd_weights(jd_sections)

    exp = explain(
        matched,
        missing,
        final,
        s,
        jd_weights,
        a,
        o
    )

    tier = classify(final)

    # QUESTIONS
    questions = generate_questions(
        missing,
        matched,
        jd_weights=jd_weights,
        jd_text=jd_text,
        score=final
    )

    return {
        "score": round(final, 2),
        "tier": tier,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "explanation": exp,
        "questions": questions
    }


# -------------------------------
# API ENDPOINT
# -------------------------------
@app.post("/evaluate")
def evaluate(resume: str, jd: str):
    return process(resume, jd)


# -------------------------------
# (OPTIONAL) KEEP YOUR OLD LOCAL TEST
# -------------------------------
if __name__ == "__main__":
    resume_text = extract_text_from_pdf("resume.pdf")
    jd_text = extract_text_from_pdf("jd.pdf")

    result = process(resume_text, jd_text)

    print("\n================ RESULTS =================")
    for k, v in result.items():
        print(f"{k}: {v}")