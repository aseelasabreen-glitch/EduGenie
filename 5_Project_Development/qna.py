from gemini_client import generate_text


SYSTEM_PROMPT = """You are EduGenie, a helpful educational assistant.
Answer academic questions accurately and clearly.
Prefer concise explanations suitable for students.
If the question is ambiguous, state the assumption briefly.
Do not invent facts. Use headings or bullet points when useful.
"""


def answer_question(question: str) -> str:
    prompt = f"""Answer the following student's question.

Question:
{question}

Give a direct answer first, followed by a short explanation or example when useful.
"""
    return generate_text(
        prompt,
        system_instruction=SYSTEM_PROMPT,
        temperature=0.3,
        max_output_tokens=1800,
    )
