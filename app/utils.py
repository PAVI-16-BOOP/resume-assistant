import json
import re

# Load skill map
with open("app/skill_map.json", "r") as f:
    SKILL_MAP = json.load(f)


#  Normalize text (standardize case, remove special chars)
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # remove all special chars
    text = re.sub(r"\s+", " ", text)
    return text.strip()


#  Build flexible regex pattern
def build_pattern(variant):
    parts = variant.split()
    pattern = r"\b" + r"\s+".join(map(re.escape, parts)) + r"\b"
    return re.compile(pattern)


#  Precompile patterns for all skills
PATTERNS = {
    skill: [build_pattern(v) for v in variants]
    for skill, variants in SKILL_MAP.items()
}


#  FINAL SKILL EXTRACTION
def extract_skills(sections):
    text = " ".join([
        sections.get("skills", ""),
        sections.get("experience", ""),
        sections.get("projects", ""),
        sections.get("summary", ""),
        sections.get("other", "")
    ])

    text = normalize_text(text)

    found = set()

    #  word-level matching (NEW)
    words = set(text.split())

    for skill, patterns in PATTERNS.items():

        #  Direct match (fast + effective)
        if skill in words:
            found.add(skill)
            continue

        #  Regex match (for phrases)
        for pattern in patterns:
            if pattern.search(text):
                found.add(skill)
                break

    return sorted(found)