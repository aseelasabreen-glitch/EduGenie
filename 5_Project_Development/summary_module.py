from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty.")

    prompt = f"""Summarize the following educational text.

Requirements:
- Keep the important facts and ideas.
- Remove repetition and unnecessary details.
- Use simple language.
- Use short paragraphs or bullet points.
- Make the result useful for quick revision.

TEXT:
{text}
"""
    return generate_text(
        prompt,
        system_instruction="You are an educational summarization assistant. Preserve important meaning and do not invent information.",
        temperature=0.25,
        max_output_tokens=2500,
    )
