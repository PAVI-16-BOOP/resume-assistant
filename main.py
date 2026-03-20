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


# -------------------------------
# LOAD INPUT FILES
# -------------------------------
resume_path = "resume.pdf"
jd_path = "jd.pdf"

resume_text = extract_text_from_pdf(resume_path)
jd_text = extract_text_from_pdf(jd_path)


# -------------------------------
# PARSE SECTIONS
# -------------------------------
resume_sections = split_sections(resume_text)
jd_sections = split_sections(jd_text)


# -------------------------------
# DEBUG: EXTRACTED SKILLS
# -------------------------------
resume_skills = extract_skills(resume_sections)
jd_skills = extract_skills(jd_sections)

print("\n================ SKILLS =================")
print("Resume Skills:", resume_skills)
print("JD Skills:", jd_skills)


# -------------------------------
# SCORING
# -------------------------------
e, matched, missing = exact_match(resume_sections, jd_sections)
s = similarity_score(resume_sections, jd_sections)

a = achievement_score(resume_text)
o = ownership_score(resume_text)

final = final_score(e, s, a, o)


# -------------------------------
# EXPLAINABILITY
# -------------------------------
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


# -------------------------------
# RESULTS
# -------------------------------
print("\n================ RESULTS =================")
print(f"Exact Match Score      : {round(e, 2)}")
print(f"Semantic Similarity    : {round(s, 2)}")
print(f"Achievement Score      : {round(a, 2)}")
print(f"Ownership Score        : {round(o, 2)}")
print(f"Final Score            : {round(final, 2)}")

print("\nMatched Skills :", matched)
print("Missing Skills :", missing)

print("\nCandidate Tier :", tier)


# -------------------------------
# RULE-BASED EXPLANATION
# -------------------------------
print("\n================ EXPLANATION =================")

for k, v in exp.items():
    if k != "llm_explanation":
        print(f"{k}: {v}")


# -------------------------------
# LLM EXPLANATION (GROQ)
# -------------------------------
print("\n================ LLM INSIGHTS =================")

llm_text = exp.get("llm_explanation")

if not llm_text or "LLM unavailable" in llm_text:
    print("LLM not available. Showing rule-based insights only.")
else:
    print(llm_text)


# -------------------------------
# QUESTION GENERATION
# -------------------------------
print("\n================ INTERVIEW QUESTIONS =================")

# 🔥 future-ready (LLM + fallback supported)
questions = generate_questions(
    missing,
    matched,
    jd_weights=jd_weights,
    jd_text=jd_text,
    score=final
)

# Handle both string (LLM) and list (rule-based)
if isinstance(questions, str):
    print(questions)
else:
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")