import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data: Any, num_questions: int) -> list[dict]:
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON list.")

    cleaned = []
    for item in data[:num_questions]:
        if not isinstance(item, dict):
            continue

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            continue
        options = [str(option).strip() for option in options]
        if not answer or answer not in options:
            continue

        cleaned.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            }
        )

    if len(cleaned) != num_questions:
        raise ValueError(
            f"Gemini returned {len(cleaned)} valid questions; expected {num_questions}."
        )

    return cleaned


def generate_quiz(topic: str, num_questions: int = 3) -> list[dict]:
    prompt = f"""Create a multiple-choice educational quiz about:
{topic}

Create exactly {num_questions} questions.
Each question must have exactly four options.
The answer must exactly match one of the four option strings.

Return ONLY valid JSON in this format:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct option text",
    "explanation": "Short explanation"
  }}
]
"""
    raw = generate_text(
        prompt,
        system_instruction="You generate strict JSON for educational quizzes. Never add Markdown or commentary outside the JSON.",
        temperature=0.2,
        max_output_tokens=3000,
    )

    try:
        data = json.loads(clean_json_block(raw))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini returned invalid quiz JSON: {exc}") from exc

    return _validate_quiz(data, num_questions)
