import hashlib
import json

from app.amd import collect_amd_proof


def _write_artifact(path, *, tamper: bool = False) -> None:
    workload_result = {
        "proof_status": "LIVE_ROCM_VERIFIED",
        "workload": "fp16_matrix_multiplication",
        "device": "AMD Instinct MI300X",
        "rocm_version": "7.2",
        "pytorch_version": "2.9.0",
        "latency_ms_median": 1.25,
        "throughput_tflops": 109.95,
        "peak_memory_mb": 512.0,
    }
    proof = {
        "schema_version": "reproforge.amd-proof.v1",
        "captured_at": "2026-07-13T00:00:00+00:00",
        "proof_status": "LIVE_ROCM_VERIFIED",
        "acceptance_gates": {"capture_passed": True},
        "workload": {
            "command": ["python", "scripts/amd_smoke.py"],
            "exit_code": 0,
            "stdout": json.dumps(workload_result),
            "stderr": "",
        },
        "amd_smi_static": {"available": True, "exit_code": 0, "stdout": "{}", "stderr": ""},
        "amd_smi_metrics": {"available": True, "exit_code": 0, "stdout": "{}", "stderr": ""},
        "rocminfo": {"available": True, "exit_code": 0, "stdout": "Agent 2", "stderr": ""},
    }
    canonical = json.dumps(proof, sort_keys=True).encode()
    proof["artifact_sha256"] = hashlib.sha256(canonical).hexdigest()
    if tamper:
        proof["workload"]["stdout"] = proof["workload"]["stdout"].replace("109.95", "999.99")
    path.write_text(json.dumps(proof), encoding="utf-8")


def test_valid_hash_linked_rocm_artifact_is_accepted(tmp_path, monkeypatch) -> None:
    artifact = tmp_path / "amd-run.json"
    _write_artifact(artifact)
    monkeypatch.setenv("AMD_PROOF_FILE", str(artifact))

    proof = collect_amd_proof()

    assert proof["status"] == "LIVE_ROCM_VERIFIED"
    assert proof["telemetry"]["device"] == "AMD Instinct MI300X"
    assert all(proof["telemetry"]["validation"].values())


def test_tampered_rocm_artifact_is_rejected(tmp_path, monkeypatch) -> None:
    artifact = tmp_path / "amd-run.json"
    _write_artifact(artifact, tamper=True)
    monkeypatch.setenv("AMD_PROOF_FILE", str(artifact))

    proof = collect_amd_proof()

    assert proof["status"] == "AMD_ARTIFACT_REJECTED"
    assert proof["telemetry"]["available"] is False
    assert proof["telemetry"]["validation"]["artifact_hash_valid"] is False
