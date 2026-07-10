export type ProofStatus = "fixture_until_backend" | "real_api_call";

export type AmdProofStatus = "AMD_PATH_CONFIGURED" | "AMD_AWARE_SIMULATED";

export type Verdict = "verified" | "unverified" | "blocked" | "partial";

export interface EvidenceItem {
  id: string;
  kind: "file" | "log" | "hash" | "network" | "artifact";
  label: string;
  detail: string;
  hash?: string;
}

export interface RiskSignal {
  id: string;
  severity: "low" | "medium" | "high" | "critical";
  label: string;
  detail: string;
}

export interface AmdGemmaProof {
  gemma_used: boolean;
  gemma_task: "risk_explanation" | "claim_summary" | "evidence_narrative";
  model_provider: "fireworks";
  model_family: "gemma";
  model_name: string;
  runtime_mode: "fireworks" | "local";
  amd_proof_status: AmdProofStatus;
  proof_status: ProofStatus;
  fireworks_confirmed: boolean;
  latency_ms: number;
  tokens_used: number;
}

export interface ShadowGuardResult {
  risk_score: number;
  reproducibility_score: number;
  policy_version: string;
  blocked_actions: string[];
}

export interface Passport {
  passport_id: string;
  run_id: string;
  created_at: string;
  claim_text: string;
  repo_url: string;
  claim_type: string;
  runtime_target: string;
  verdict: Verdict;
  shadowguard_result: ShadowGuardResult;
  signals_found: RiskSignal[];
  evidence_items: EvidenceItem[];
  missing_evidence: string[];
  gemma_explanation: string;
  amd_gemma_proof: AmdGemmaProof;
  hashes: {
    execution_hash: string;
    environment_hash: string;
    log_hash: string;
  };
  security_notes: string[];
}

export const sampleClaim = {
  repo_url: "https://github.com/example/agentic-rag-benchmark",
  claim_text:
    "Our agent achieves 92.4% pass@1 on SWE-bench Verified using a 7B open-weights model with no test-set leakage.",
  claim_type: "benchmark_result",
  runtime_target: "linux/x86_64 · ROCm 6.x · AMD-aware simulated",
};

export const mockPassport: Passport = {
  passport_id: "pp_01HNXQ7ZKMB4T3RG9E2A",
  run_id: "run_9f31c8a2",
  created_at: "2026-07-10T14:22:11Z",
  claim_text: sampleClaim.claim_text,
  repo_url: sampleClaim.repo_url,
  claim_type: sampleClaim.claim_type,
  runtime_target: sampleClaim.runtime_target,
  verdict: "partial",
  shadowguard_result: {
    risk_score: 0.9037,
    reproducibility_score: 0.42,
    policy_version: "shadowguard/2026.07-strict",
    blocked_actions: [
      "network egress to raw.githubusercontent.com/private/*",
      "shell exec: curl | bash",
    ],
  },
  signals_found: [
    {
      id: "sig-1",
      severity: "critical",
      label: "Test set contamination suspected",
      detail:
        "eval/loader.py reads from data/swe_bench_verified/*.jsonl which overlaps with the training manifest hash a1c4…9e.",
    },
    {
      id: "sig-2",
      severity: "high",
      label: "Non-deterministic scoring path",
      detail: "scorer sets temperature=0.7 but reports pass@1 without seed pinning across 3 runs.",
    },
    {
      id: "sig-3",
      severity: "medium",
      label: "Undeclared network dependency",
      detail: "agent/tools/web.py issues live HTTP calls during eval; results vary by wall-clock.",
    },
  ],
  evidence_items: [
    {
      id: "ev-1",
      kind: "file",
      label: "eval/loader.py",
      detail: "Reads jsonl fixtures matched against training manifest.",
      hash: "sha256:a1c4f2…9e",
    },
    {
      id: "ev-2",
      kind: "log",
      label: "sandbox/run.log",
      detail: "Full stdout+stderr captured under seccomp profile v3.",
      hash: "sha256:7d8b12…04",
    },
    {
      id: "ev-3",
      kind: "hash",
      label: "environment lockfile",
      detail: "uv.lock resolved and hashed at ingest.",
      hash: "sha256:e0219a…b1",
    },
    {
      id: "ev-4",
      kind: "network",
      label: "egress ledger",
      detail: "12 outbound requests denied by ShadowGuard policy.",
    },
  ],
  missing_evidence: [
    "Original training data manifest (referenced but not published).",
    "Seed values for the 3 reported runs.",
    "Independent re-run under sealed environment.",
  ],
  gemma_explanation:
    "The claim cannot be fully reproduced from the published artifacts. The evaluation loader reads fixtures whose hashes overlap with the training manifest, and the scoring path uses stochastic decoding without pinned seeds. Two network-dependent tools further make results non-deterministic. The repository is well-structured and the sandbox executed cleanly, but the reported 92.4% pass@1 is not evidenced by a sealed re-run.",
  amd_gemma_proof: {
    gemma_used: true,
    gemma_task: "risk_explanation",
    model_provider: "fireworks",
    model_family: "gemma",
    model_name: "accounts/fireworks/models/gemma-2-9b-it",
    runtime_mode: "fireworks",
    amd_proof_status: "AMD_PATH_CONFIGURED",
    proof_status: "fixture_until_backend",
    fireworks_confirmed: false,
    latency_ms: 842,
    tokens_used: 318,
  },
  hashes: {
    execution_hash: "sha256:4b2a71b8ef4c2eb2fa4c105682e095e84f4b77fe4186991ce7df9a48e7e3c7f1",
    environment_hash: "sha256:e0219a80183288fa7ec349335d3002f52eb64c18f62a1a5a86cc0f97e6d473b1",
    log_hash: "sha256:7d8b12bd23e4a7ca2b6b788ffbdbb4fa50bbf4df64792d5c04ba4e33d3311204",
  },
  security_notes: [
    "Sandbox executed under seccomp profile v3; no host mounts.",
    "All egress passed through ShadowGuard proxy; denials logged.",
    "No model weights or secrets exfiltrated during the run.",
  ],
};

export const fixtureLogLines: { t: string; line: string; step: number }[] = [
  {
    t: "00:00",
    line: "sentinel: ingesting repo → https://github.com/example/agentic-rag-benchmark",
    step: 0,
  },
  {
    t: "00:01",
    line: "sentinel: static scan complete · 1,284 files · 3 lockfiles resolved",
    step: 1,
  },
  {
    t: "00:03",
    line: "shadowguard: policy=shadowguard/2026.07-strict loaded · risk=0.9037",
    step: 2,
  },
  { t: "00:05", line: "signal: test-set contamination suspected in eval/loader.py", step: 3 },
  {
    t: "00:07",
    line: "gemma: risk_explanation drafted via fireworks/gemma-2-9b-it · 318 tokens",
    step: 4,
  },
  { t: "00:09", line: "passport: pp_01HNXQ7ZKMB4T3RG9E2A sealed · verdict=partial", step: 5 },
];

export const timelineSteps = [
  { id: 0, label: "Ingest repository" },
  { id: 1, label: "Static scan & lockfile hash" },
  { id: 2, label: "ShadowGuard policy eval" },
  { id: 3, label: "Signal detection" },
  { id: 4, label: "Gemma explanation" },
  { id: 5, label: "Seal Reproducibility Passport" },
];
