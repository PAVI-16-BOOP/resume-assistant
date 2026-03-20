import sys
import os

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.parser import split_sections
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


def run_test(name, resume, jd):
    print(f"\n================ {name} ================")

    resume_sections = split_sections(resume)
    jd_sections = split_sections(jd)

    resume_skills = extract_skills(resume_sections)
    jd_skills = extract_skills(jd_sections)

    e, matched, missing = exact_match(resume_sections, jd_sections)
    s = similarity_score(resume_sections, jd_sections)
    a = achievement_score(resume)
    o = ownership_score(resume)

    final = final_score(e, s, a, o)

    jd_weights = get_jd_weights(jd_sections)
    exp = explain(matched, missing, final, s, jd_weights, a, o)

    tier = classify(final)

    questions = generate_questions(
        missing,
        matched,
        jd_weights=jd_weights,
        jd_text=jd,
        score=final
    )

    print("Score:", round(final, 2))
    print("Tier:", tier)
    print("Resume Skills:", resume_skills)
    print("JD Skills:", jd_skills)
    print("Matched:", matched)
    print("Missing:", missing)
    print("Summary:", exp.get("summary"))

    print("\nQuestions:")
    if isinstance(questions, str):
        print(questions)
    else:
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")


# -------------------------------
# RUN TESTS
# -------------------------------
if __name__ == "__main__":

    print("\nRUNNING ALL TEST CASES...\n")

    # 1. Empty resume
    run_test("EMPTY RESUME", "", "Looking for Python AWS SQL")

    # 2. No match
    run_test(
        "NO MATCH",
        "Mechanical engineering CAD design",
        "Python AWS Docker"
    )

    # 3. Partial match
    run_test(
        "PARTIAL MATCH",
        "Python SQL data analysis",
        "Python AWS SQL Docker"
    )

    # 4. Strong match
    run_test(
        "STRONG MATCH",
        "Python AWS SQL Docker machine learning",
        "Python AWS SQL Docker machine learning"
    )

    # 5. Achievement-heavy
    run_test(
        "ACHIEVEMENT HEAVY",
        "Improved model accuracy by 30% and built ML pipeline",
        "Machine learning Python"
    )

    # 6. Random noise
    run_test(
        "RANDOM TEXT",
        "asdfgh qwerty zxcvb",
        "Python AWS"
    )

    # 7. Synonym match
    run_test(
        "SYNONYM MATCH",
        "Worked on ML models using Python",
        "Looking for machine learning and python"
    )

    # 8. Soft + technical mix
    run_test(
        "SOFT + TECH MIX",
        "Strong communication and teamwork with Python and SQL projects",
        "Python SQL communication skills required"
    )

    # 9. Overqualified candidate
    run_test(
        "OVERQUALIFIED",
        "Python AWS SQL Docker Kubernetes Spark Hadoop machine learning deep learning",
        "Python AWS SQL"
    )

    # 10. Irrelevant skills
    run_test(
        "IRRELEVANT SKILLS",
        "Graphic design photoshop illustrator UI UX figma",
        "Python AWS machine learning"
    )