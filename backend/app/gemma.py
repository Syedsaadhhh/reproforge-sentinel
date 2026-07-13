import json
import os
import time

import httpx


SYSTEM_INSTRUCTION = """You are ReproForge's evidence narrator. Explain only the supplied evidence.
Do not claim that a repository was executed, reproduced, or verified unless the evidence explicitly says so.
Return concise plain text suitable for a technical audit passport."""


async def explain_evidence(claim: str, signals: list[dict], missing: list[str]) -> dict:
    fireworks_key = os.getenv("FIREWORKS_API_KEY")
    fireworks_model = os.getenv("FIREWORKS_MODEL") or "accounts/fireworks/models/gemma-4-26b-a4b-it"
    api_key = os.getenv("GEMMA_API_KEY")
    model = os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")
    fallback = _fallback_explanation(signals, missing)
    prompt = json.dumps({"claim": claim, "signals": signals, "missing_evidence": missing})

    if fireworks_key:
        return await _fireworks_explanation(
            fireworks_key,
            fireworks_model,
            prompt,
            fallback,
        )

    if not api_key:
        return {
            "text": fallback,
            "used": False,
            "provider": "local_mock",
            "model": None,
            "runtime_mode": "mock",
            "proof_status": "pending",
            "latency_ms": None,
            "tokens_used": None,
        }

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
        tokens = usage.get("totalTokenCount")
        return {
            "text": text,
            "used": True,
            "provider": "google-gemini-api",
            "model": model,
            "runtime_mode": "gemini_api",
            "proof_status": "real",
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "tokens_used": int(tokens) if tokens is not None else None,
        }
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError):
        return {
            "text": fallback,
            "used": False,
            "provider": "google-gemini-api",
            "model": model,
            "runtime_mode": "api_error_fallback",
            "proof_status": "pending",
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "tokens_used": None,
        }


async def _fireworks_explanation(api_key: str, model: str, prompt: str, fallback: str) -> dict:
    started = time.perf_counter()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 500,
    }
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                "https://api.fireworks.ai/inference/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
        usage = data.get("usage", {})
        tokens = usage.get("total_tokens")
        return {
            "text": data["choices"][0]["message"]["content"].strip(),
            "used": True,
            "provider": "fireworks",
            "model": model,
            "runtime_mode": "fireworks",
            "proof_status": "real",
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "tokens_used": int(tokens) if tokens is not None else None,
        }
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError):
        return {
            "text": fallback,
            "used": False,
            "provider": "fireworks",
            "model": model,
            "runtime_mode": "api_error_fallback",
            "proof_status": "pending",
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "tokens_used": None,
        }


def _fallback_explanation(signals: list[dict], missing: list[str]) -> str:
    signal_names = ", ".join(signal["label"].lower() for signal in signals) or "no critical risk signals"
    missing_text = ", ".join(item.lower() for item in missing) or "no declared evidence gaps"
    return (
        f"The guided analysis identified {signal_names}. "
        f"Evidence still missing includes {missing_text}. "
        "This result is an evidence assessment, not proof of a successful hardware reproduction."
    )
