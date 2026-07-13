"""Capture a workload plus AMD/ROCm telemetry into a hash-linked proof artifact."""

import argparse
import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def capture(command: list[str], timeout: int) -> dict:
    started = time.perf_counter()
    completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    return {
        "command": command,
        "exit_code": completed.returncode,
        "latency_ms": round((time.perf_counter() - started) * 1000, 3),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def optional_command(command: list[str]) -> dict:
    if not shutil.which(command[0]):
        return {"available": False, "command": command, "reason": "not installed"}
    try:
        return {"available": True, **capture(command, 20)}
    except (OSError, subprocess.SubprocessError) as error:
        return {"available": False, "command": command, "reason": type(error).__name__}


def parse_workload_result(workload: dict[str, Any]) -> dict[str, Any]:
    try:
        result = json.loads(workload.get("stdout", ""))
    except (json.JSONDecodeError, TypeError):
        return {}
    return result if isinstance(result, dict) else {}


def command_succeeded(result: dict[str, Any]) -> bool:
    return bool(result.get("available") and result.get("exit_code") == 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/amd-run.json")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("provide a workload after --")

    workload = capture(command, args.timeout)
    workload_result = parse_workload_result(workload)
    amd_smi_static = optional_command(["amd-smi", "static", "--json"])
    amd_smi_metrics = optional_command(["amd-smi", "metric", "--json"])
    rocminfo = optional_command(["rocminfo"])
    gates = {
        "workload_exit_zero": workload["exit_code"] == 0,
        "workload_declares_live_rocm": workload_result.get("proof_status") == "LIVE_ROCM_VERIFIED",
        "amd_device_present": bool(workload_result.get("device")),
        "rocm_version_present": bool(workload_result.get("rocm_version")),
        "pytorch_version_present": bool(workload_result.get("pytorch_version")),
        "latency_measured": isinstance(workload_result.get("latency_ms_median"), (int, float)),
        "throughput_measured": isinstance(workload_result.get("throughput_tflops"), (int, float)),
        "peak_memory_measured": isinstance(workload_result.get("peak_memory_mb"), (int, float)),
        "amd_smi_static_succeeded": command_succeeded(amd_smi_static),
        "amd_smi_metrics_succeeded": command_succeeded(amd_smi_metrics),
        "rocminfo_succeeded": command_succeeded(rocminfo),
    }
    proof = {
        "schema_version": "reproforge.amd-proof.v1",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "proof_status": "LIVE_ROCM_VERIFIED" if all(gates.values()) else "AMD_UNAVAILABLE",
        "acceptance_gates": gates,
        "workload": workload,
        "amd_smi_static": amd_smi_static,
        "amd_smi_metrics": amd_smi_metrics,
        "rocminfo": rocminfo,
    }
    canonical = json.dumps(proof, sort_keys=True).encode()
    proof["artifact_sha256"] = hashlib.sha256(canonical).hexdigest()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(proof, indent=2), encoding="utf-8")
    print(output)
    print(proof["artifact_sha256"])
    return workload["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
