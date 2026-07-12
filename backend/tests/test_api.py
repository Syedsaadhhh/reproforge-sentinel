from fastapi.testclient import TestClient

from app.main import app
from app.models import AmdGemmaProof


client = TestClient(app)
claim = {
    "repo_url": "https://github.com/example/reproforge-case",
    "claim_text": "This benchmark achieves 95% accuracy safely.",
    "claim_type": "benchmark_result",
    "runtime_target": "linux/x86_64 · ROCm · AMD-aware pending",
    "policies": ["egress_deny", "exec_pipe_deny", "fs_readonly"],
    "verification_mode": "deep",
}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_project_and_claim_creation() -> None:
    project = client.post("/projects", json={"name": "Judge demo", "description": "MVP"})
    assert project.status_code == 201
    stored_claim = client.post(
        "/claims",
        json={**claim, "project_id": project.json()["id"]},
    )
    assert stored_claim.status_code == 201
    assert stored_claim.json()["project_id"] == project.json()["id"]


def test_verify_run_and_passport(monkeypatch) -> None:
    monkeypatch.delenv("FIREWORKS_API_KEY", raising=False)
    monkeypatch.delenv("FIREWORKS_MODEL", raising=False)
    monkeypatch.delenv("GEMMA_API_KEY", raising=False)

    verify = client.post("/verify", json=claim)
    assert verify.status_code == 200
    run_id = verify.json()["run_id"]
    run = client.get(f"/runs/{run_id}")
    passport = client.get(f"/passport/{run_id}")

    assert run.status_code == 200
    assert run.json()["status"] == "complete"
    assert passport.status_code == 200

    body = passport.json()
    proof = body["amd_gemma_proof"]
    assert body["run_id"] == run_id
    assert proof["proof_status"] == "pending"
    assert proof["gemma_used"] is False
    assert proof["gemma_tasks"] == []
    assert proof["model_provider"] == "local_mock"
    assert proof["model_name"] is None
    assert proof["latency_ms"] is None
    assert proof["tokens_used"] is None
    assert proof["run_id"] is None
    assert proof["timestamp"] is None


def test_real_proof_contract_is_traceable() -> None:
    proof = AmdGemmaProof(
        gemma_used=True,
        gemma_task="evidence_narrative",
        gemma_tasks=["evidence_narrative"],
        model_provider="fireworks",
        model_name="configured-model-id",
        runtime_mode="fireworks",
        amd_status="active",
        amd_proof_status="AMD_PATH_CONFIGURED",
        proof_status="real",
        fireworks_confirmed=True,
        run_id="run_test",
        timestamp="2026-07-12T00:00:00Z",
        latency_ms=120,
        tokens_used=256,
    )
    assert proof.proof_status == "real"
    assert proof.gemma_tasks == ["evidence_narrative"]
    assert proof.run_id == "run_test"
