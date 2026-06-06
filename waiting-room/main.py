"""
main.py — Lighthouse Waiting Room
Endpoints:
  POST /auth    — validate header, issue JWT
  POST /chat    — validate JWT, route to best AI model
  GET  /memory  — return MEMORY.md bootstrap (JWT required)
  GET  /health  — model endpoint status (no auth)
"""

import os, time, pathlib
from datetime import datetime, timezone, timedelta

import jwt
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import router as model_router

load_dotenv()

SPRING_TOKEN = os.getenv("SPRING_TOKEN", "")
JWT_SECRET   = os.getenv("JWT_SECRET", "change-me")
JWT_TTL_MIN  = int(os.getenv("JWT_TTL_MINUTES", "15"))
MEMORY_PATH  = pathlib.Path(__file__).parent / "MEMORY.md"

VALID_MODELS = {
    "claude-sonnet-4-6", "claude-haiku-4-5",
    "llama3-local", "groq-llama3", "*",
}

app = FastAPI(title="Lighthouse Waiting Room", version="0.1.0")


def _validate_header(request: Request) -> dict:
    token   = request.headers.get("X-Spring-Token", "")
    model   = request.headers.get("X-AI-Model", "")
    node_id = request.headers.get("X-Node-ID", "unknown")
    if not SPRING_TOKEN:
        raise HTTPException(500, "SPRING_TOKEN not configured")
    if token != SPRING_TOKEN:
        raise HTTPException(401, "Invalid token")
    if model not in VALID_MODELS:
        raise HTTPException(403, f"Model '{model}' not authorized")
    return {"model": model, "node_id": node_id}


def _issue_jwt(model: str, node_id: str) -> str:
    payload = {
        "sub":   node_id,
        "model": model,
        "iat":   int(time.time()),
        "exp":   datetime.now(timezone.utc) + timedelta(minutes=JWT_TTL_MIN),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def _require_jwt(request: Request) -> dict:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Bearer JWT required")
    try:
        return jwt.decode(auth.removeprefix("Bearer "), JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "JWT expired — re-auth at /auth")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid JWT")


@app.post("/auth")
async def authenticate(request: Request):
    """Present X-Spring-Token + X-AI-Model + X-Node-ID. Returns short-lived JWT."""
    identity = _validate_header(request)
    token    = _issue_jwt(identity["model"], identity["node_id"])
    return {
        "jwt":        token,
        "ttl_min":    JWT_TTL_MIN,
        "node_id":    identity["node_id"],
        "model":      identity["model"],
        "issued_at":  datetime.now(timezone.utc).isoformat(),
    }


@app.post("/chat")
async def chat(request: Request, identity: dict = Depends(_require_jwt)):
    """Send prompt. Routes to best available model. Body: {prompt, system}"""
    body   = await request.json()
    prompt = body.get("prompt", "").strip()
    if not prompt:
        raise HTTPException(400, "prompt required")
    system = body.get("system", "You are Patricia, a sovereign AI agent.")
    try:
        result = await model_router.route(prompt, system)
    except RuntimeError as e:
        raise HTTPException(503, str(e))
    return {
        **result,
        "node_id":   identity.get("sub"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/memory")
async def memory(identity: dict = Depends(_require_jwt)):
    """Returns MEMORY.md — DRAM bootstrap layer for authorized agents."""
    if not MEMORY_PATH.exists():
        raise HTTPException(404, "MEMORY.md not found")
    return PlainTextResponse(MEMORY_PATH.read_text(), media_type="text/markdown")


@app.get("/health")
async def health():
    """Public. Reports which model endpoints are reachable."""
    return {
        "status":      "online",
        "models":      await model_router.health_check(),
        "jwt_ttl_min": JWT_TTL_MIN,
        "timestamp":   datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8443, reload=False)
