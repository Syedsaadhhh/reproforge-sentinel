import { ProofCard } from "./ProofCard";
import { StatusBadge } from "./StatusBadge";
import type { AmdGemmaProof } from "@/data/mockPassport";

export function AMDProofCard({ proof }: { proof: AmdGemmaProof }) {
  const telemetryAvailable = proof.amd_telemetry?.available === true;
  const isActive =\n    proof.amd_status === "active" || proof.amd_proof_status === "LIVE_ROCM_VERIFIED";

  return (
    <ProofCard
      eyebrow="AMD runtime"
      title="Verification runtime path"
      action={
        <StatusBadge tone={isActive ? "success" : "amd"}>
          {isActive ? "AMD_ACTIVE" : proof.amd_proof_status}
        </StatusBadge>
      }
    >
      <dl className="grid grid-cols-2 gap-x-4 gap-y-2 font-mono text-[11px]">
        <Row k="runtime_mode" v={proof.runtime_mode} />
        <Row k="amd_status" v={proof.amd_status} />
        <Row k="proof_status" v={proof.proof_status} />
        <Row k="telemetry" v={telemetryAvailable ? "attached" : "not_attached"} />
      </dl>
      <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
        {isActive
          ? "AMD-backed runtime proof is active. Inspect the provider receipt or attached ROCm telemetry for the evidence source."
          : "AMD integration is configured, but live ROCm telemetry or an AMD-hosted provider receipt has not been attached to this Passport."}
      </p>
    </ProofCard>
  );
}

export function GemmaProofCard({ proof }: { proof: AmdGemmaProof }) {
  const isReal =
    (proof.proof_status === "real" || proof.proof_status === "real_api_call") &&
    proof.gemma_used;

  return (
    <ProofCard
      eyebrow="Gemma explanation"
      title="Model provider proof"
      action={
        isReal ? (
          <StatusBadge tone="success">GEMMA_API_ACTIVE</StatusBadge>
        ) : (
          <StatusBadge tone="warning">PROOF_PENDING</StatusBadge>
        )
      }
    >
      <dl className="grid grid-cols-2 gap-x-4 gap-y-2 font-mono text-[11px]">
        <Row k="provider" v={proof.model_provider} />
        <Row k="family" v={proof.model_family} />
        <Row k="model_name" v={proof.model_name} />
        <Row k="gemma_tasks" v={proof.gemma_tasks.join(", ") || null} />
        <Row k="latency_ms" v={proof.latency_ms} />
        <Row k="tokens_used" v={proof.tokens_used} />
        <Row k="run_id" v={proof.run_id} />
        <Row k="timestamp" v={proof.timestamp} />
      </dl>
      {!isReal && (
        <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
          No successful Gemma response is attached. The explanation is deterministic fallback text,
          and unknown measurements remain unrecorded.
        </p>
      )}
    </ProofCard>
  );
}

function Row({
  k,
  v,
}: {
  k: string;
  v: string | number | null | undefined;
}) {
  return (
    <>
      <dt className="text-muted-foreground">{k}</dt>
      <dd className="truncate text-foreground">{v ?? "not_recorded"}</dd>
    </>
  );
}
