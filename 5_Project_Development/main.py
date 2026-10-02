from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import settings
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=10000)
    num_questions: int = Field(default=3, ge=1, le=10)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": "EduGenie",
        "gemini_configured": settings.gemini_configured,
    }


@app.post("/qa")
async def qa(payload: TextRequest):
    try:
        return {"success": True, "result": answer_question(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        return {"success": True, "result": explain_topic(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        return {
            "success": True,
            "result": generate_quiz(payload.topic, payload.num_questions),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {"success": True, "result": summarize_text(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):
    try:
        return {
            "success": True,
            "result": get_learning_recommendations(payload.text),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
