from app.parser import extract_text_from_pdf, split_sections
from app.scoring import exact_match, similarity_score, final_score
from app.utils import extract_skills   # 👈 ADD THIS IMPORT


# STEP 1: Load PDFs
resume_text = extract_text_from_pdf("resume.pdf")
jd_text = extract_text_from_pdf("jd.pdf")


# STEP 2: Split into sections
resume_sections = split_sections(resume_text)
jd_sections = split_sections(jd_text)


# ADD DEBUG HERE (exactly here)
print("\nResume Skills:", extract_skills(resume_sections))
print("\nJD Skills:", extract_skills(jd_sections))


# STEP 3: Compute scores
e, matched, missing = exact_match(resume_sections, jd_sections)
s = similarity_score(resume_sections, jd_sections)

final = final_score(e, s, 0.5, 0.5)


# STEP 4: Print results
print("\n--- RESULTS ---")
print("Exact Match Score:", round(e, 2))
print("Semantic Score:", round(s, 2))
print("Final Score:", round(final, 2))

print("\nMatched Skills:", matched)
print("\nMissing Skills:", missing)