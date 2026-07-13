import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def _artifact_hash(proof: dict[str, Any]) -> str:
    canonical = {key: value for key, value in proof.items() if key != "artifact_sha256"}
    encoded = json.dumps(canonical, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def _command_succeeded(result: Any) -> bool:
    return bool(isinstance(result, dict) and result.get("available") and result.get("exit_code") == 0)


def _parse_workload_result(workload: Any) -> dict[str, Any]:
    if not isinstance(workload, dict):
        return {}
    try:
        result = json.loads(workload.get("stdout", ""))
    except (json.JSONDecodeError, TypeError):
        return {}
    return result if isinstance(result, dict) else {}


def _collect_artifact_proof(path: Path) -> dict:
    try:
        proof = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "status": "AMD_ARTIFACT_REJECTED",
            "runtime_mode": "amd_rocm_artifact",
            "telemetry": {"available": False, "reason": "artifact_unreadable"},
        }

    workload = proof.get("workload", {})
    workload_result = _parse_workload_result(workload)
    recorded_hash = proof.get("artifact_sha256")
    calculated_hash = _artifact_hash(proof)
    gates = {
        "schema_valid": proof.get("schema_version") == "reproforge.amd-proof.v1",
        "capture_declares_live_rocm": proof.get("proof_status") == "LIVE_ROCM_VERIFIED",
        "artifact_hash_valid": bool(recorded_hash and recorded_hash == calculated_hash),
        "workload_exit_zero": isinstance(workload, dict) and workload.get("exit_code") == 0,
        "workload_declares_live_rocm": workload_result.get("proof_status") == "LIVE_ROCM_VERIFIED",
        "amd_device_present": bool(workload_result.get("device")),
        "rocm_version_present": bool(workload_result.get("rocm_version")),
        "pytorch_version_present": bool(workload_result.get("pytorch_version")),
        "latency_measured": isinstance(workload_result.get("latency_ms_median"), (int, float)),
        "throughput_measured": isinstance(workload_result.get("throughput_tflops"), (int, float)),
        "peak_memory_measured": isinstance(workload_result.get("peak_memory_mb"), (int, float)),
        "amd_smi_static_succeeded": _command_succeeded(proof.get("amd_smi_static")),
        "amd_smi_metrics_succeeded": _command_succeeded(proof.get("amd_smi_metrics")),
        "rocminfo_succeeded": _command_succeeded(proof.get("rocminfo")),
    }
    if not all(gates.values()):
        return {
            "status": "AMD_ARTIFACT_REJECTED",
            "runtime_mode": "amd_rocm_artifact",
            "telemetry": {
                "available": False,
                "reason": "acceptance_gate_failed",
                "artifact_sha256": recorded_hash,
                "validation": gates,
            },
        }

    return {
        "status": "LIVE_ROCM_VERIFIED",
        "runtime_mode": "amd_rocm_artifact",
        "telemetry": {
            "available": True,
            "source": "hash-linked AMD/ROCm proof artifact",
            "captured_at": proof.get("captured_at"),
            "artifact_sha256": recorded_hash,
            "device": workload_result["device"],
            "rocm_version": workload_result["rocm_version"],
            "pytorch_version": workload_result["pytorch_version"],
            "workload": workload_result.get("workload"),
            "latency_ms_median": workload_result["latency_ms_median"],
            "throughput_tflops": workload_result["throughput_tflops"],
            "peak_memory_mb": workload_result["peak_memory_mb"],
            "validation": gates,
        },
    }


def collect_amd_proof() -> dict:
    artifact_path = os.getenv("AMD_PROOF_FILE")
    if artifact_path:
        return _collect_artifact_proof(Path(artifact_path))

    executable = shutil.which("amd-smi")
    if not executable:
        return {
            "status": "AMD_PATH_CONFIGURED",
            "runtime_mode": "amd_aware_pending",
            "telemetry": {"available": False, "reason": "amd-smi not installed"},
        }

    try:
        completed = subprocess.run(
            [executable, "metric", "--json"],
            capture_output=True,
            text=True,
            timeout=8,
            check=True,
        )
        telemetry = json.loads(completed.stdout)
        return {
            "status": "AMD_TELEMETRY_AVAILABLE",
            "runtime_mode": "amd_smi_only",
            "telemetry": {
                "available": True,
                "source": "amd-smi metric --json",
                "proof_verified": False,
                "reason": "telemetry alone does not prove the workload ran",
                "data": telemetry,
            },
        }
    except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as error:
        return {
            "status": "AMD_PATH_CONFIGURED",
            "runtime_mode": "amd_smi_unavailable",
            "telemetry": {"available": False, "reason": type(error).__name__},
        }
