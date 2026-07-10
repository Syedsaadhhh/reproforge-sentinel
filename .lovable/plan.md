# ReproForge Sentinel — Build Plan (v2)

Rebuild the uploaded Areeba HTML mockup as a proper TanStack Start + Tailwind v4 + shadcn app. Reference only — no raw HTML copy.

## Design System (src/styles.css)

Extend tokens in `@theme` + `:root` (oklch equivalents):

- `--bg-primary` #0D0E10, `--bg-app` #08090A, `--panel` #121417, `--card` #15181D
- `--border` #252A31, `--cyan` #21F5F5, `--amd-orange` #FF8A3D
- `--success` #35D07F, `--warning` #F5C542, `--danger` #FF4D4F
- Text: `--text-primary` #E8EDF2, `--text-secondary` #B2BAC7, `--text-muted` #8A94A6
- Load Inter + JetBrains Mono via `<link>` in `__root.tsx` head; register `--font-sans` and `--font-mono` in `@theme`
- Map shadcn tokens (`--color-background`, `--color-card`, `--color-primary`, ...) onto the dark graphite palette
- Set `<html class="dark">` in RootShell

## Routes

```
src/routes/
  __root.tsx      updated head, fonts, dark class
  index.tsx       Judge Landing (/)
  intake.tsx      Claim Intake (/intake)
  trace.tsx       Live Sandbox Trace (/trace)
  passport.tsx    Reproducibility Passport (/passport)
```

Each leaf sets its own `head()`. Navigation via `<Link>`.

## Shared Components (src/components/reproforge/)

AppShell, StatusBadge, ProofCard, AMDProofCard, GemmaProofCard, TerminalWindow, Timeline + TimelineStep, EvidenceChain, RiskSignalList, MetricCard, PassportHeader, ExportButtons, FlowStrip, FixtureBanner.

## Screens

**/ Landing** — Hero: "Verify AI claims with sandboxed evidence." + subtext. CTAs: `Run Sample Verification` → `/trace?sample=1`, `Enter Custom Repo` → `/intake`. Small proof preview card + FlowStrip (Claim → ShadowGuard → Gemma → AMD/Fireworks → Passport). No fake metrics.

**/intake** — Two-column: left inputs (repo URL, sample claim text prefilled, claim type, runtime target, sandbox policy toggles, verification mode). Right parsed assertion + risk checklist preview. `Generate Verification Plan` → `/trace`.

**/trace** — 3-column. Left Timeline (ingest → scan → shadowguard → detect signal → gemma → passport), animated active step. Center TerminalWindow streaming the 6 spec log lines with delay; header shows run_id, live status, `Pause Run`, `Kill Switch`, `View Raw Logs`. Right stack: ShadowGuard score, RiskSignalList, missing evidence, blocked action example, AMDProofCard, GemmaProofCard. `View Passport` CTA only appears after run completes.

**/passport** — Calm audit-report layout. PassportHeader. Metric row (verdict, risk_score, reproducibility_score). Sections: Claim Summary, ShadowGuard Result, Gemma Explanation, EvidenceChain, Missing Evidence, Security Notes, AMD+Gemma Proof, Hashes (execution/environment/log). ExportButtons.

## Sample-run simulation (critical)

`Run Sample Verification` never jumps straight to the finished passport. It routes to `/trace?sample=1` which:

1. Calls `verifyClaim(sampleInput)` → `{ run_id }`
2. Streams timeline + terminal logs on a timer (~9–11s total, matching the [00:00]…[00:09] spec)
3. Progressively reveals ShadowGuard, signals, Gemma, proof cards as each step completes
4. Only after the final step enables `View Passport` → `/passport?run_id=…`

Same simulation is reused when arriving from `/intake`.

## Data + API layer

`src/data/mockPassport.ts` — typed `mockPassport` with all spec fields. `amd_gemma_proof`:

```ts
{
  gemma_used: true,
  gemma_task: "risk_explanation",
  model_provider: "fireworks",
  model_family: "gemma",
  model_name: "accounts/fireworks/models/gemma-2-9b-it",
  runtime_mode: "fireworks",
  amd_proof_status: "AMD_PATH_CONFIGURED",
  proof_status: "fixture_until_backend",
  latency_ms: 842,
  tokens_used: 318,
}
```

`src/lib/api.ts` — async stubs (mock delays), ready to swap for real backend. No keys, no direct Fireworks calls from frontend.

```ts
submitClaim(input): { run_id }
startVerification(run_id): { run_id, status: "running" }
getRunStatus(run_id): { status, step, logs[], timeline[] }
getPassport(run_id): Passport
verifyClaim(input): { run_id }   // future POST /verify; currently returns mock run_id
```

## Honesty guardrails (updated)

- Allowed proof states in UI: `AMD_PATH_CONFIGURED`, `AMD_AWARE_SIMULATED`, `fixture_until_backend`, `real_api_call`.
- **`FIREWORKS_GEMMA_ACTIVE` is hidden in fixture mode.** It only renders when `proof_status === "real_api_call"` AND backend confirms a real Fireworks response (flag `fireworks_confirmed: true` on the proof payload). Otherwise the Gemma card shows `proof_status: fixture_until_backend` and no "active" badge.
- **`LIVE_ROCM_VERIFIED` never rendered** unless real ROCm telemetry present (not in this build).
- Fixture banner visible globally in fixture mode.

## Technical notes

- Log/timeline streaming via `useEffect` + `setInterval` walking the fixture array; guarded so navigating away cancels timers
- Timeline active step derived from current log index
- shadcn primitives (button, card, badge, separator, toggle, select, textarea, input) added via `bunx shadcn@latest add`, restyled via tokens
- ExportButtons: JSON download works via Blob; PDF + Share show toast placeholder

## Out of scope

Real backend, real ROCm telemetry, real Fireworks calls, auth, PDF generation.
