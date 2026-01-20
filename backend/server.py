import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict
import os

from app.validator import validate_user_input

app = FastAPI(title="LLM Validator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "web"))
if os.path.isdir(web_dir):
    app.mount("/ui", StaticFiles(directory=web_dir, html=True), name="ui")

@app.get("/")
async def root() -> Dict[str, str]:
    return {"status": "ok", "ui": "/ui/"}

@app.post("/validate")
async def validate(payload: Dict[str, Any]) -> Dict[str, Any]:
    return validate_user_input(payload)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
