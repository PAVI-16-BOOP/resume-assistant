import pdfplumber
import re

# -------------------------------
# PDF content extractor
# -------------------------------
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
    except Exception as e:
        print(f"[WARN] PDF read error: {e}")
    return text


# -------------------------------
# Section patterns
# -------------------------------
SECTION_PATTERNS = {
    "skills": re.compile(r"\b(skills?|technical skills|key skills|skills\s*&\s*tools)\b", re.I),
    "experience": re.compile(r"\b(experience|work experience|professional experience)\b", re.I),
    "education": re.compile(r"\b(education|academic background)\b", re.I),
    "projects": re.compile(r"\b(projects?)\b", re.I),
    "achievements": re.compile(r"\b(achievements|awards)\b", re.I),
    "summary": re.compile(r"\b(summary|profile|objective)\b", re.I),
}


# -------------------------------
# Helpers
# -------------------------------
def _normalize_line(line: str) -> str:
    line = line.strip().lower()
    line = re.sub(r"[^a-z0-9\s/&]", " ", line)
    line = re.sub(r"\s+", " ", line)
    return line


def _is_header(line: str) -> bool:
    if not line:
        return False
    if len(line) > 60:
        return False
    if len(line.split()) > 6:
        return False
    return True


# -------------------------------
# Section splitter
# -------------------------------
def split_sections(text: str) -> dict:
    sections = {key: [] for key in SECTION_PATTERNS}
    sections["other"] = []

    current = "other"

    # 🔥 IMPORTANT FIX: handle single-line inputs (API case)
    if "\n" not in text:
        sections["other"].append(text.strip())
        return {k: "\n".join(v).strip() for k, v in sections.items()}

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue

        line_norm = _normalize_line(line)

        found_header = False

        if _is_header(line_norm):
            for sec, pattern in SECTION_PATTERNS.items():
                if pattern.search(line_norm):
                    current = sec
                    found_header = True
                    break

        if found_header:
            continue

        sections[current].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}