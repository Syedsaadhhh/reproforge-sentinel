import json
import os
import time

import httpx


SYSTEM_INSTRUCTION = """You are ReproForge's evidence narrator. Explain only the supplied evidence.
Do not claim that a repository was executed, reproduced, or verified unless the evidence explicitly says so.
Return concise plain text suitable for a technical audit passport."""


async def explain_evidence(claim: str, signals: list[dict], missing: list[str]) -> dict:
    api_key = os.getenv("GEMMA_API_KEY")
    model = os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")
    fallback = _fallback_explanation(signals, missing)
    if not api_key:
        return {
            "text": fallback,
            "used": False,
            "provider": "google-gemini-api",
            "model": model,
            "runtime_mode": "fixture",
            "proof_status": "fixture_until_backend",
            "latency_ms": 0,
            "tokens_used": 0,
        }

    prompt = json.dumps({"claim": claim, "signals": signals, "missing_evidence": missing})
    started = time.perf_counter()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 500},
    }
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, params={"key": api_key}, json=payload)
            response.raise_for_status()
            data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        usage = data.get("usageMetadata", {})
        return {
            "text": text,
            "used": True,
            "provider": "google-gemini-api",
            "model": model,
            "runtime_mode": "gemini_api",
            "proof_status": "real_api_call",
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "tokens_used": int(usage.get("totalTokenCount", 0)),
        }
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError):
        return {
            "text": fallback,
            "used": False,
            "provider": "google-gemini-api",
            "model": model,
            "runtime_mode": "api_error_fallback",
            "proof_status": "fixture_until_backend",
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "tokens_used": 0,
        }


def _fallback_explanation(signals: list[dict], missing: list[str]) -> str:
    signal_names = ", ".join(signal["label"].lower() for signal in signals) or "no critical risk signals"
    missing_text = ", ".join(item.lower() for item in missing) or "no declared evidence gaps"
    return (
        f"The guided analysis identified {signal_names}. "
        f"Evidence still missing includes {missing_text}. "
        "This result is an evidence assessment, not proof of a successful hardware reproduction."
    )
