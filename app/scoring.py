from app.utils import extract_skills
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


#  Load MiniLM model
model = SentenceTransformer("all-MiniLM-L6-v2")


#  Skill tiers
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
    "git", "github", "linux", "html", "css",
    "bootstrap", "tailwind css",
    "pytest", "jest", "cypress", "selenium",
    "communication", "leadership", "teamwork"
}


def weight(skill):
    if skill in HIGH_PRIORITY:
        return 2.0
    elif skill in MEDIUM_PRIORITY:
        return 1.5
    elif skill in LOW_PRIORITY:
        return 1.0
    return 1.2


def exact_match(resume_sections, jd_sections):
    resume_skills = extract_skills(resume_sections)
    jd_skills = extract_skills(jd_sections)

    if not jd_skills:
        return 0, [], []

    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)

    matched_score = sum(weight(s) for s in matched)
    total_score = sum(weight(s) for s in jd_skills)

    score = matched_score / total_score

    return score, list(matched), list(missing)


def sections_to_text(sections):
    return " ".join(sections.values())


#  Semantic similarity (MiniLM)
def similarity_score(resume_sections, jd_sections):
    resume_text = sections_to_text(resume_sections)
    jd_text = sections_to_text(jd_sections)

    embeddings = model.encode([resume_text, jd_text])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)


#  Achievement words
ACHIEVEMENT_WORDS = [
    "improved", "increased", "reduced", "optimized",
    "enhanced", "boosted", "achieved", "accelerated"
]


def achievement_score(text):
    text = text.lower()
    score = sum(1 for w in ACHIEVEMENT_WORDS if w in text)
    return min(score / len(ACHIEVEMENT_WORDS), 1)


#  Ownership words
OWNERSHIP_WORDS = [
    "led", "built", "designed", "developed",
    "implemented", "created", "owned", "delivered"
]


def ownership_score(text):
    text = text.lower()
    score = sum(1 for w in OWNERSHIP_WORDS if w in text)
    return min(score / len(OWNERSHIP_WORDS), 1)


#  Final score
def final_score(e, s, a, o):
    return (0.5 * e + 0.25 * s + 0.15 * a + 0.1 * o) * 100