from app.parser import extract_text_from_pdf, split_sections
from app.scoring import exact_match, similarity_score, final_score


# STEP 1: Load PDFs
resume_text = extract_text_from_pdf("resume.pdf")
jd_text = extract_text_from_pdf("jd.pdf")

# 🔍 Debug (optional)
print("Resume text length:", len(resume_text))
print("JD text length:", len(jd_text))


# STEP 2: Split into sections
resume_sections = split_sections(resume_text)
jd_sections = split_sections(jd_text)

# 🔍 Debug sections
print("\nResume sections keys:", resume_sections.keys())
print("JD sections keys:", jd_sections.keys())


# STEP 3: Compute scores
e, matched, missing = exact_match(resume_sections, jd_sections)
s = similarity_score(resume_sections, jd_sections)

# Combine scores
final = final_score(e, s, 0.5, 0.5)


# STEP 4: Print results
print("\n--- RESULTS ---")

print(f"Exact Match Score: {round(e, 2)}")
print(f"Semantic Score: {round(s, 2)}")
print(f"Final Score: {round(final, 2)}")

print("\nMatched Skills:")
for skill in matched:
    print("✔", skill)

print("\nMissing Skills:")
for skill in missing:
    print("✘", skill)