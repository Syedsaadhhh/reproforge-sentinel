# AMD GPU proof runbook

## Hackathon GPU access

1. Confirm FrontierOps is registered as a team on lablab.ai.
2. Open `https://notebooks.amd.com/hackathon` with the same account.
3. Request/claim the event GPU allocation. This is separate from the $100 AMD Developer Cloud credit.
4. Clone this repository inside the notebook environment.

## Run the proof workload

```bash
python scripts/amd_capture.py \
  --output artifacts/amd-run.json \
  -- python scripts/amd_smoke.py --size 4096 --repeats 12
```

Do not edit the resulting JSON manually. Preserve its SHA-256 printed by the capture script.

## Acceptance gate

The run is accepted as live AMD proof only when all are true:

- workload exits with code 0;
- PyTorch reports a non-empty `torch.version.hip`;
- AMD device name is present;
- `amd-smi` is installed and telemetry is captured;
- result includes latency, throughput and peak memory;
- artifact hash is preserved in the Passport.

If any gate fails, keep the UI state as `AMD_UNAVAILABLE` or `AMD_PATH_CONFIGURED`—never `LIVE_ROCM_VERIFIED`.
