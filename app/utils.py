import json
import re

with open("app/skill_map.json", "r") as f:
    SKILL_MAP = json.load(f)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[-_/\.]", " ", text)   # handle node.js, machine-learning
    text = re.sub(r"\s+", " ", text)
    return text


def build_pattern(variant):
    parts = variant.split()
    pattern = r"\b" + r"\s+".join(map(re.escape, parts)) + r"\b"
    return re.compile(pattern)


# 🔥 Precompile all patterns (performance boost)
PATTERNS = {
    skill: [build_pattern(v) for v in variants]
    for skill, variants in SKILL_MAP.items()
}


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

    for skill, patterns in PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                found.add(skill)
                break

    return sorted(found)