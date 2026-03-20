from openai import OpenAI
import os


# -------------------------------
# GROQ CLIENT
# -------------------------------
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# -------------------------------
# RULE-BASED GENERATION (YOUR LOGIC, IMPROVED SLIGHTLY)
# -------------------------------
def generate_questions_rule(missing, matched, jd_weights=None):
    questions = []

    # Sort missing skills by importance
    if jd_weights:
        missing = sorted(missing, key=lambda x: jd_weights.get(x, 1), reverse=True)

    # 1. Missing → conceptual
    for skill in missing[:3]:
        questions.append(
            f"Explain the fundamentals of {skill} and its real-world use cases."
        )

    # 2. Matched → project-based
    for skill in matched[:2]:
        if skill in {"communication", "teamwork"}:
            questions.append(
                "Tell me about a situation where you worked in a team."
            )
        else:
            questions.append(
                f"Describe a project where you used {skill}. What challenges did you face?"
            )

    # 3. System design
    if "system design" in matched or "distributed systems" in matched:
        questions.append(
            "Design a scalable system for a real-world application of your choice."
        )

    # 4. Impact
    questions.append(
        "Tell me about a project where you improved performance or efficiency."
    )

    # 5. Optimization
    if matched:
        questions.append(
            f"How would you optimize a solution using {matched[0]}?"
        )

    return questions[:5]


# -------------------------------
# LLM-BASED GENERATION (GROQ)
# -------------------------------
def generate_questions_llm(missing, matched, jd_text, score):
    try:
        # If no API key → skip LLM
        if not os.getenv("GROQ_API_KEY"):
            return None

        prompt = f"""
You are a senior technical interviewer.

Generate exactly 5 high-quality interview questions.

Candidate:
- Score: {round(score, 2)}
- Matched skills: {matched}
- Missing skills: {missing}

Job Description:
{jd_text[:1000]}

Instructions:
- Focus on important missing skills
- Include mix of:
  - conceptual
  - project-based
  - problem-solving
- Adjust difficulty based on score
- Avoid generic questions
- Return ONLY numbered questions (1–5)
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM ERROR: {str(e)}"


# -------------------------------
# MAIN WRAPPER (SMART SWITCH)
# -------------------------------
def generate_questions(missing, matched, jd_weights=None, jd_text=None, score=None):

    # Try LLM first (if inputs available)
    if jd_text and score is not None:
        llm_output = generate_questions_llm(missing, matched, jd_text, score)

        if llm_output:
            return llm_output

    # Fallback → rule-based
    return generate_questions_rule(missing, matched, jd_weights)