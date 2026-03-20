import json
import re
import os

# -------------------------------
# Load skill map (safe path)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_PATH = os.path.join(BASE_DIR, "skill_map.json")

with open(SKILL_PATH, "r") as f:
    SKILL_MAP = json.load(f)


# -------------------------------
# Normalize text
# -------------------------------
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------------
# Build regex pattern
# -------------------------------
def build_pattern(variant):
    parts = variant.split()
    pattern = r"\b" + r"\s+".join(map(re.escape, parts)) + r"\b"
    return re.compile(pattern)


# -------------------------------
# Precompile patterns
# -------------------------------
PATTERNS = {
    skill: [build_pattern(v) for v in variants]
    for skill, variants in SKILL_MAP.items()
}


# -------------------------------
# FINAL SKILL EXTRACTION
# -------------------------------
def extract_skills(sections):
    if not sections:
        return []

    # Combine all sections
    text = " ".join(sections.values())
    text = normalize_text(text)

    found = set()

    for skill, patterns in PATTERNS.items():

        # Handle single-character skills safely (e.g., "c", "r")
        if len(skill) == 1:
            if re.search(rf"\b{re.escape(skill)}\b", text):
                found.add(skill)
            continue

        # Word-boundary match for normal skills
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)
            continue

        # Regex fallback for variants
        for pattern in patterns:
            if pattern.search(text):
                found.add(skill)
                break

    return sorted(found)