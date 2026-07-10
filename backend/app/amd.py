import json
import shutil
import subprocess


def collect_amd_proof() -> dict:
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
            "status": "LIVE_ROCM_VERIFIED",
            "runtime_mode": "amd_smi",
            "telemetry": {"available": True, "source": "amd-smi metric --json", "data": telemetry},
        }
    except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as error:
        return {
            "status": "AMD_PATH_CONFIGURED",
            "runtime_mode": "amd_smi_unavailable",
            "telemetry": {"available": False, "reason": type(error).__name__},
        }
