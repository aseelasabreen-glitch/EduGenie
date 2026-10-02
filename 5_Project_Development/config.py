import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    explanation_backend: str = os.getenv("EXPLANATION_BACKEND", "gemini").strip().lower()
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    ).strip()
    debug: bool = _bool(os.getenv("DEBUG"), False)
    host: str = os.getenv("HOST", "127.0.0.1").strip()
    port: int = int(os.getenv("PORT", "8000"))

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key)


settings = Settings()
