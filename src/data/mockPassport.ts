export type ProofStatus = "mock" | "pending" | "real" | "fixture_until_backend" | "real_api_call";

export type AmdProofStatus = "AMD_PATH_CONFIGURED" | "AMD_AWARE_SIMULATED" | "LIVE_ROCM_VERIFIED";

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
  gemma_task?: string | null;
  gemma_tasks: string[];
  model_provider: "fireworks" | "google-gemini-api" | "local_mock" | "local";
  model_family: "gemma";
  model_name: string | null;
  runtime_mode: string;
  amd_status: "pending" | "active";
  amd_proof_status: AmdProofStatus;
  proof_status: ProofStatus;
  fireworks_confirmed: boolean;
  run_id: string | null;
  timestamp: string | null;
  latency_ms: number | null;
  tokens_used: number | null;
  amd_telemetry?: Record<string, unknown>;
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
  hashes: Record<string, string>;
  security_notes: string[];
}

export const sampleClaim = {
  repo_url: "https://github.com/example/agentic-rag-benchmark",
  claim_text: "Our agent claims 92.4% pass@1 on SWE-bench Verified using a 7B open-weights model.",
  claim_type: "benchmark_result",
  runtime_target: "linux/x86_64 · ROCm · AMD-aware pending",
};

export const mockPassport: Passport = {
  passport_id: "pp_fixture_01",
  run_id: "run_fixture_01",
  created_at: "2026-07-12T00:00:00Z",
  claim_text: sampleClaim.claim_text,
  repo_url: sampleClaim.repo_url,
  claim_type: sampleClaim.claim_type,
  runtime_target: sampleClaim.runtime_target,
  verdict: "partial",
  shadowguard_result: {
    risk_score: 0.72,
    reproducibility_score: 0.42,
    policy_version: "shadowguard/2026.07-strict",
    blocked_actions: ["shell exec policy: curl|bash and wget|bash"],
  },
  signals_found: [
    {
      id: "sig-fixture-1",
      severity: "high",
      label: "Metric requires independent reproduction",
      detail: "Guided fixture: the quantitative claim does not include a sealed execution result.",
    },
    {
      id: "sig-fixture-2",
      severity: "medium",
      label: "Dataset and seed provenance missing",
      detail:
        "Guided fixture: the submitted metadata does not identify a dataset manifest or seed.",
    },
  ],
  evidence_items: [
    {
      id: "ev-fixture-claim",
      kind: "artifact",
      label: "Submitted claim",
      detail: sampleClaim.claim_text,
      hash: "sha256:fixture-claim-hash",
    },
    {
      id: "ev-fixture-policy",
      kind: "log",
      label: "Guided policy evaluation",
      detail: "One restricted command class configured; no repository code executed.",
      hash: "sha256:fixture-policy-hash",
    },
  ],
  missing_evidence: ["Independent sealed execution output.", "Dataset and seed provenance."],
  gemma_explanation:
    "This guided fixture identified a quantitative claim without independent execution evidence. The narrative is deterministic fallback text; no external Gemma request was made.",
  amd_gemma_proof: {
    gemma_used: false,
    gemma_task: null,
    gemma_tasks: [],
    model_provider: "local_mock",
    model_family: "gemma",
    model_name: null,
    runtime_mode: "mock",
    amd_status: "pending",
    amd_proof_status: "AMD_PATH_CONFIGURED",
    proof_status: "pending",
    fireworks_confirmed: false,
    run_id: null,
    timestamp: null,
    latency_ms: null,
    tokens_used: null,
    amd_telemetry: { available: false, reason: "guided fixture" },
  },
  hashes: {
    execution_hash: "sha256:fixture-execution-hash",
    environment_hash: "sha256:fixture-environment-hash",
    log_hash: "sha256:fixture-log-hash",
  },
  security_notes: [
    "Guided fixture mode: no external repository code was executed.",
    "No external model request or live GPU telemetry is claimed.",
  ],
};

export const fixtureLogLines: { t: string; line: string; step: number }[] = [
  { t: "00:00", line: "fixture: guided demo mode active · no repository executed", step: 0 },
  { t: "00:01", line: "policy-engine: submitted claim metadata evaluated", step: 1 },
  { t: "00:03", line: "evidence: independent run and dataset provenance missing", step: 2 },
  { t: "00:05", line: "gemma: no external call · deterministic fallback used", step: 3 },
  { t: "00:07", line: "amd: runtime proof pending", step: 4 },
  { t: "00:09", line: "passport: fixture artifact sealed · verdict=partial", step: 5 },
];

export const timelineSteps = [
  { id: 0, label: "Accept claim" },
  { id: 1, label: "Evaluate policy" },
  { id: 2, label: "Map evidence gaps" },
  { id: 3, label: "Generate explanation" },
  { id: 4, label: "Attach runtime proof" },
  { id: 5, label: "Seal Passport" },
];
