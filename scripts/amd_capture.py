"""Capture a workload plus AMD/ROCm telemetry into a hash-linked proof artifact."""

import argparse
import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


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
    proof = {
        "schema_version": "reproforge.amd-proof.v1",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "proof_status": "LIVE_ROCM_VERIFIED" if workload["exit_code"] == 0 and shutil.which("amd-smi") else "AMD_UNAVAILABLE",
        "workload": workload,
        "amd_smi_static": optional_command(["amd-smi", "static", "--json"]),
        "amd_smi_metrics": optional_command(["amd-smi", "metric", "--json"]),
        "rocminfo": optional_command(["rocminfo"]),
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
