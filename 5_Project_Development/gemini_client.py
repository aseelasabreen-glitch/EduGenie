from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


class GeminiClientError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not settings.gemini_api_key:
        raise GeminiClientError(
            "GEMINI_API_KEY is not configured. Create a .env file and add your Gemini API key."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
) -> str:
    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )

    text = getattr(response, "text", None)
    if not text:
        raise GeminiClientError("Gemini returned an empty response.")

    return text.strip()
