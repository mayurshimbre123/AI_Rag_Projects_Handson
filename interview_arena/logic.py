"""Prompt design and deterministic rubric. No secret application state."""
ROLE_TOPICS = {
    "AI Engineer": ["RAG evaluation", "agent tools", "latency and cost"],
    "ML Engineer": ["feature leakage", "model monitoring", "deployment"],
    "Data Scientist": ["experimental design", "forecasting", "business metrics"],
}
RUBRIC = {"correctness": 40, "causal_explanation": 30, "tradeoffs": 20, "clarity": 10}

def build_question_prompt(role: str, difficulty: str, topic: str) -> str:
    if role not in ROLE_TOPICS: raise ValueError("Unknown role")
    return (f"You are conducting a {difficulty} technical interview for {role}. "
            f"Ask ONE precise question about {topic}; do not answer the question. "
            "Avoid personal questions. Respond with just the question.")

def build_feedback_prompt(question: str, answer: str) -> str:
    return ("Evaluate this technical answer. Give concise feedback under four headings: "
            "Correctness (0-40), causal explanation (0-30), trade-offs (0-20), "
            "clarity (0-10). Explain evidence for each score and list one follow-up. "
            "The evaluation is formative and not an objective hiring decision.\n"
            f"Question: {question}\nCandidate's answer: {answer}")
