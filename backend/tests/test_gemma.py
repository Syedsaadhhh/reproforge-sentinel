import asyncio

from app import gemma


def _result(*, used: bool, provider: str) -> dict:
    return {
        "text": f"{provider} explanation",
        "used": used,
        "provider": provider,
        "model": "configured-model",
        "runtime_mode": provider,
        "proof_status": "real" if used else "pending",
        "latency_ms": 10,
        "tokens_used": 20 if used else None,
    }


def test_google_is_used_when_fireworks_fails(monkeypatch) -> None:
    monkeypatch.setenv("FIREWORKS_API_KEY", "private-fireworks-key")
    monkeypatch.setenv("FIREWORKS_MODEL", "accounts/test/deployments/reproforge-gemma")
    monkeypatch.setenv("GEMMA_API_KEY", "private-google-key")

    async def failed_fireworks(*args, **kwargs):
        return _result(used=False, provider="fireworks")

    async def successful_google(*args, **kwargs):
        return _result(used=True, provider="google-gemini-api")

    monkeypatch.setattr(gemma, "_fireworks_explanation", failed_fireworks)
    monkeypatch.setattr(gemma, "_google_explanation", successful_google)

    result = asyncio.run(gemma.explain_evidence("claim text", [], ["sealed output"]))

    assert result["used"] is True
    assert result["provider"] == "google-gemini-api"


def test_successful_fireworks_remains_preferred(monkeypatch) -> None:
    monkeypatch.setenv("FIREWORKS_API_KEY", "private-fireworks-key")
    monkeypatch.setenv("FIREWORKS_MODEL", "accounts/test/deployments/reproforge-gemma")
    monkeypatch.setenv("GEMMA_API_KEY", "private-google-key")

    async def successful_fireworks(*args, **kwargs):
        return _result(used=True, provider="fireworks")

    async def unexpected_google(*args, **kwargs):
        raise AssertionError("Google fallback should not run after Fireworks succeeds")

    monkeypatch.setattr(gemma, "_fireworks_explanation", successful_fireworks)
    monkeypatch.setattr(gemma, "_google_explanation", unexpected_google)

    result = asyncio.run(gemma.explain_evidence("claim text", [], ["sealed output"]))

    assert result["used"] is True
    assert result["provider"] == "fireworks"
