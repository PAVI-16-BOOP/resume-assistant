import pdfplumber
import re

### PDF content extractor
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text


### Section splitter
SECTION_PATTERNS = {
    "skills": r"\b(skills?|technical skills|key skills|skills\s*&\s*tools)\b",
    "experience": r"\b(experience|work experience|professional experience)\b",
    "education": r"\b(education|academic background)\b",
    "projects": r"\b(projects?)\b",
    "achievements": r"\b(achievements|awards)\b",
    "summary": r"\b(summary|profile|objective)\b"
}

def split_sections(text):
    sections = {key: [] for key in SECTION_PATTERNS}
    sections["other"] = []

    current = "other"

    for line in text.split("\n"):
        line_clean = line.strip().lower()

        if not line_clean:
            continue

        found_header = False

        if len(line_clean) < 60:
            for sec, pattern in SECTION_PATTERNS.items():
                if re.search(pattern, line_clean):
                    current = sec
                    found_header = True
                    break

        if found_header:
            continue

        sections[current].append(line.strip())

    return {k: "\n".join(v).strip() for k, v in sections.items()}