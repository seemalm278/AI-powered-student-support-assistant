from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agent import run_agent

app = FastAPI(
    title="DEVFORGE Student Support AI Agent",
    description="AI-powered learning assistant for DEVFORGE Internship students.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "DEVFORGE Student Support AI Agent",
        "version": app.version
    }


@app.get("/docs-info")
def docs_info():
    return {
        "message": "Interactive API documentation is available at /docs"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        answer = run_agent(request.message)

        return {
            "success": True,
            "question": request.message,
            "response": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )