from config import settings
from gemini_client import generate_text


def _gemini_explanation(topic: str) -> str:
    prompt = f"""Explain the following topic to a beginner.

Topic:
{topic}

Use this structure:
1. Simple definition
2. Main idea
3. Step-by-step explanation
4. Small example
5. Key points to remember

Use simple language and avoid unnecessary jargon.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie. Make difficult concepts simple, accurate, and beginner-friendly.",
        temperature=0.35,
        max_output_tokens=2200,
    )


def _local_explanation(topic: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode requires transformers and torch. "
            "Install the optional requirements or set EXPLANATION_BACKEND=gemini."
        ) from exc

    generator = pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
    )

    prompt = (
        "Explain this educational topic simply for a beginner. "
        "Give a definition, main idea, example, and key points: "
        f"{topic}"
    )
    result = generator(prompt, max_new_tokens=220)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    if settings.explanation_backend == "local":
        return _local_explanation(topic)

    return _gemini_explanation(topic)
