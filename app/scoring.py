from app.utils import extract_skills
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load MiniLM model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Skill tiers
HIGH_PRIORITY = {
    "machine learning", "deep learning", "natural language processing",
    "computer vision", "data science",
    "large language models", "generative ai", "retrieval augmented generation",
    "langchain", "llamaindex",
    "python", "java", "sql",
    "system design", "distributed systems",
    "spark", "hadoop", "kafka", "data engineering",
    "aws", "azure", "google cloud"
}

MEDIUM_PRIORITY = {
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "keras", "xgboost", "lightgbm",
    "node.js", "react", "django", "flask", "fastapi",
    "docker", "kubernetes", "ci/cd", "jenkins",
    "mongodb", "postgresql", "mysql", "redis",
    "rest api", "graphql"
}

LOW_PRIORITY = {
    "git", "linux", "html", "css",
    "bootstrap", "tailwind css",
    "pytest", "jest", "cypress", "selenium",
    "communication", "leadership", "teamwork"
}


# Dynamic JD weighting
def get_jd_weights(jd_sections):
    jd_skills = extract_skills(jd_sections)
    text = " ".join(jd_sections.values()).lower()

    weights = {}

    for skill in jd_skills:
        if skill in HIGH_PRIORITY:
            base = 2.5
        elif skill in MEDIUM_PRIORITY:
            base = 2.0
        elif skill in LOW_PRIORITY:
            base = 1.5
        else:
            base = 1.8

        if f"required {skill}" in text or f"must have {skill}" in text:
            base += 0.5
        elif f"preferred {skill}" in text or f"nice to have {skill}" in text:
            base -= 0.3

        weights[skill] = max(base, 1.0)

    return weights


# Exact match
def exact_match(resume_sections, jd_sections):
    resume_skills = extract_skills(resume_sections)
    jd_skills = extract_skills(jd_sections)

    if not jd_skills:
        return 0, [], []

    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)

    jd_weights = get_jd_weights(jd_sections)

    matched_score = sum(jd_weights[s] for s in matched)
    total_score = sum(jd_weights[s] for s in jd_skills)

    score = matched_score / total_score

    return score, list(matched), list(missing)


# Convert sections to text
def sections_to_text(sections):
    return " ".join(sections.values())


# Semantic similarity
def similarity_score(resume_sections, jd_sections):
    resume_text = sections_to_text(resume_sections)
    jd_text = sections_to_text(jd_sections)

    embeddings = model.encode([resume_text, jd_text])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)


# Achievement score
ACHIEVEMENT_WORDS = [
    "improved", "increased", "reduced", "optimized",
    "enhanced", "boosted", "achieved", "accelerated"
]


def achievement_score(text):
    text = text.lower()
    score = sum(1 for w in ACHIEVEMENT_WORDS if w in text)
    return min(score / len(ACHIEVEMENT_WORDS), 1)


# Ownership score
OWNERSHIP_WORDS = [
    "led", "built", "designed", "developed",
    "implemented", "created", "owned", "delivered"
]


def ownership_score(text):
    text = text.lower()
    score = sum(1 for w in OWNERSHIP_WORDS if w in text)
    return min(score / len(OWNERSHIP_WORDS), 1)


# Final score
def final_score(e, s, a, o):
    return (0.5 * e + 0.25 * s + 0.15 * a + 0.1 * o) * 100


# Explainability
def explain(matched, missing, score, semantic_score, jd_weights=None, a=None, o=None):
    explanation = {}

    explanation["matched_skills"] = matched
    explanation["missing_skills"] = missing
    explanation["score"] = round(score, 2)
    explanation["semantic_score"] = round(semantic_score, 2)

    explanation["summary"] = f"{len(matched)} skills matched, {len(missing)} missing"

    if jd_weights:
        important_missing = sorted(
            missing,
            key=lambda x: jd_weights.get(x, 1),
            reverse=True
        )[:3]
        explanation["critical_gaps"] = important_missing

    if semantic_score < 0.65:
        explanation["reason_detail"] = (
            "Low semantic similarity indicates weak contextual alignment. "
            "Resume may lack detailed project descriptions or relevant keywords."
        )

    # Achievement interpretation
    if a is not None:
        explanation["achievement_score"] = round(a, 2)

        if a < 0.4:
            explanation["achievement_feedback"] = (
                "Low impact: add measurable results (%, speed, performance improvements)."
            )
        elif a < 0.7:
            explanation["achievement_feedback"] = (
                "Moderate impact: improve with more quantified achievements."
            )
        else:
            explanation["achievement_feedback"] = "Strong impact demonstrated"

    # Ownership interpretation
    if o is not None:
        explanation["ownership_score"] = round(o, 2)

        if o < 0.4:
            explanation["ownership_feedback"] = (
                "Low ownership: use action verbs like led, built, designed."
            )
        elif o < 0.7:
            explanation["ownership_feedback"] = (
                "Moderate ownership: clarify contributions."
            )
        else:
            explanation["ownership_feedback"] = "Strong ownership demonstrated"

    # Interpretation
    if score >= 80:
        explanation["interpretation"] = "Strong match"
    elif score >= 65:
        explanation["interpretation"] = "Moderate match"
    else:
        explanation["interpretation"] = "Low match"

    return explanation


# Tier classification
def classify(score):
    if score >= 85:
        return "Tier S"
    elif score >= 75:
        return "Tier A"
    elif score >= 65:
        return "Tier B"
    elif score >= 50:
        return "Tier C"
    else:
        return "Tier D"