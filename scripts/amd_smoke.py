"""Small real ROCm/PyTorch workload that emits judge-readable JSON metrics."""

import argparse
import json
import statistics
import time

import torch


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=4096)
    parser.add_argument("--repeats", type=int, default=12)
    args = parser.parse_args()

    if not torch.cuda.is_available() or not torch.version.hip:
        raise SystemExit("A ROCm-backed PyTorch GPU is required; refusing to emit fake AMD proof.")

    device = torch.device("cuda:0")
    torch.cuda.reset_peak_memory_stats(device)
    left = torch.randn((args.size, args.size), device=device, dtype=torch.float16)
    right = torch.randn((args.size, args.size), device=device, dtype=torch.float16)
    for _ in range(2):
        torch.matmul(left, right)
    torch.cuda.synchronize(device)

    samples = []
    for _ in range(args.repeats):
        started = time.perf_counter()
        torch.matmul(left, right)
        torch.cuda.synchronize(device)
        samples.append((time.perf_counter() - started) * 1000)

    median_ms = statistics.median(samples)
    operations = 2 * (args.size**3)
    result = {
        "proof_status": "LIVE_ROCM_VERIFIED",
        "workload": "fp16_matrix_multiplication",
        "device": torch.cuda.get_device_name(device),
        "rocm_version": torch.version.hip,
        "pytorch_version": torch.__version__,
        "matrix_size": args.size,
        "repeats": args.repeats,
        "latency_ms_median": round(median_ms, 3),
        "throughput_tflops": round(operations / (median_ms / 1000) / 1e12, 3),
        "peak_memory_mb": round(torch.cuda.max_memory_allocated(device) / 1024**2, 2),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
