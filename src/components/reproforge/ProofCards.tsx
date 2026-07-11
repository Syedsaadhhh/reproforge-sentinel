import { ProofCard } from "./ProofCard";
import { StatusBadge } from "./StatusBadge";
import type { AmdGemmaProof } from "@/data/mockPassport";

export function AMDProofCard({ proof }: { proof: AmdGemmaProof }) {
  return (
    <ProofCard
      eyebrow="AMD runtime"
      title="Sandbox execution path"
      action={<StatusBadge tone="amd">{proof.amd_proof_status}</StatusBadge>}
    >
      <dl className="grid grid-cols-2 gap-x-4 gap-y-2 font-mono text-[11px]">
        <Row k="runtime_mode" v={proof.runtime_mode} />
        <Row k="proof_status" v={proof.proof_status} />
        <Row k="policy" v="shadowguard/2026.07-strict" />
        <Row k="telemetry" v="rocm=not_attached" />
      </dl>
      <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
        AMD-aware execution contract is configured. Live ROCm telemetry is not attached in this
        build, so the UI does not claim{" "}
        <span className="font-mono text-foreground">LIVE_ROCM_VERIFIED</span>.
      </p>
    </ProofCard>
  );
}

export function GemmaProofCard({ proof }: { proof: AmdGemmaProof }) {
  const isReal = proof.proof_status === "real_api_call" && proof.fireworks_confirmed;
  return (
    <ProofCard
      eyebrow="Gemma explanation"
      title="Model provider proof"
      action={
        isReal ? (
          <StatusBadge tone="success">FIREWORKS_GEMMA_ACTIVE</StatusBadge>
        ) : (
          <StatusBadge tone="warning">fixture_until_backend</StatusBadge>
        )
      }
    >
      <dl className="grid grid-cols-2 gap-x-4 gap-y-2 font-mono text-[11px]">
        <Row k="provider" v={proof.model_provider} />
        <Row k="family" v={proof.model_family} />
        <Row k="model_name" v={proof.model_name} />
        <Row k="gemma_task" v={proof.gemma_task} />
        <Row k="latency_ms" v={String(proof.latency_ms)} />
        <Row k="tokens_used" v={String(proof.tokens_used)} />
      </dl>
      {!isReal && (
        <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
          Fireworks call not confirmed by the backend. The proof status stays fixture-only; the UI
          never displays <span className="font-mono text-foreground">FIREWORKS_GEMMA_ACTIVE</span>{" "}
          unless the backend attaches a verified response.
        </p>
      )}
    </ProofCard>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <>
      <dt className="text-muted-foreground">{k}</dt>
      <dd className="truncate text-foreground">{v}</dd>
    </>
  );
}
