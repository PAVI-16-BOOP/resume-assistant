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


# Load PDFs
resume_text = extract_text_from_pdf("resume.pdf")
jd_text = extract_text_from_pdf("jd.pdf")


# Split sections
resume_sections = split_sections(resume_text)
jd_sections = split_sections(jd_text)


# Debug skills
print("\nResume Skills:", extract_skills(resume_sections))
print("\nJD Skills:", extract_skills(jd_sections))


# Scores
e, matched, missing = exact_match(resume_sections, jd_sections)
s = similarity_score(resume_sections, jd_sections)

a = achievement_score(resume_text)
o = ownership_score(resume_text)

final = final_score(e, s, a, o)


# Explanation
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


# Output
print("\n--- RESULTS ---")
print("Exact:", round(e, 2))
print("Semantic:", round(s, 2))
print("Achievement:", round(a, 2))
print("Ownership:", round(o, 2))
print("Final:", round(final, 2))

print("\nMatched:", matched)
print("Missing:", missing)

print("\n--- EXPLANATION ---")
for k, v in exp.items():
    print(f"{k}: {v}")

print("\nTier:", tier)