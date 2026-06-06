"""
router.py — Model rotation logic for Lighthouse Waiting Room
Priority chain: Claude (paid) -> Ollama (local free) -> Groq (free tier)
"""

import os
import httpx
import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GROQ_KEY      = os.getenv("GROQ_API_KEY", "")
OLLAMA_URL    = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL  = os.getenv("OLLAMA_MODEL", "llama3")
GROQ_MODEL    = os.getenv("GROQ_MODEL", "llama3-70b-8192")

MODEL_CHAIN = [
    {"id": "claude", "type": "paid",       "enabled": bool(ANTHROPIC_KEY)},
    {"id": "ollama", "type": "local_free", "enabled": True},
    {"id": "groq",   "type": "free_tier",  "enabled": bool(GROQ_KEY)},
]


async def _try_claude(prompt: str, system: str) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


async def _try_ollama(prompt: str, system: str) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt},
                ],
                "stream": False,
            },
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]


async def _try_groq(prompt: str, system: str) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt},
                ],
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


_HANDLERS = {
    "claude": _try_claude,
    "ollama": _try_ollama,
    "groq":   _try_groq,
}


async def route(prompt: str, system: str = "You are Patricia, a sovereign AI agent.") -> dict:
    """Try each model in chain. Return first successful response."""
    errors = []
    for model in MODEL_CHAIN:
        if not model["enabled"]:
            continue
        try:
            text = await _HANDLERS[model["id"]](prompt, system)
            return {"response": text, "model_used": model["id"], "model_type": model["type"]}
        except Exception as e:
            errors.append(f"{model['id']}: {e}")
    raise RuntimeError(f"All models failed: {errors}")


async def health_check() -> dict:
    """Check which endpoints are reachable."""
    status = {"claude": bool(ANTHROPIC_KEY)}
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
            status["ollama"] = r.status_code == 200
    except Exception:
        status["ollama"] = False
    status["groq"] = bool(GROQ_KEY)
    return status
