import { createFileRoute, Link } from "@tanstack/react-router";
import { AppShell } from "@/components/reproforge/AppShell";
import { PassportHeader } from "@/components/reproforge/PassportHeader";
import { MetricCard } from "@/components/reproforge/MetricCard";
import { ProofCard } from "@/components/reproforge/ProofCard";
import { RiskSignalList } from "@/components/reproforge/RiskSignalList";
import { EvidenceChain } from "@/components/reproforge/EvidenceChain";
import { AMDProofCard, GemmaProofCard } from "@/components/reproforge/ProofCards";
import { ExportButtons } from "@/components/reproforge/ExportButtons";
import { StatusBadge } from "@/components/reproforge/StatusBadge";
import { mockPassport } from "@/data/mockPassport";
import { getPassport } from "@/lib/api";
import { loadClaimInput } from "@/lib/traceUtils";
import { useEffect, useState } from "react";

export const Route = createFileRoute("/passport")({
  validateSearch: (search: Record<string, unknown>) => ({
    run_id: typeof search.run_id === "string" ? search.run_id : mockPassport.run_id,
  }),
  head: () => ({
    meta: [
      { title: "Reproducibility Passport · ReproForge Sentinel" },
      {
        name: "description",
        content: "The sealed audit artifact for a verification run: verdict, evidence, and proof.",
      },
    ],
  }),
  component: PassportPage,
});

function PassportPage() {
  const { run_id } = Route.useSearch();
  const [p, setPassport] = useState(() => ({
    ...mockPassport,
    run_id,
    ...loadClaimInput(),
  }));

  useEffect(() => {
    let cancelled = false;
    getPassport(run_id).then((passport) => {
      if (!cancelled) setPassport({ ...passport, ...loadClaimInput(), run_id });
    });
    return () => {
      cancelled = true;
    };
  }, [run_id]);
  return (
    <AppShell currentStep="passport">
      <div className="space-y-6">
        <PassportHeader passport={p} />

        <div className="grid gap-3 md:grid-cols-4">
          <MetricCard label="verdict" value={p.verdict} tone="warning" />
          <MetricCard
            label="risk_score"
            value={p.shadowguard_result.risk_score.toFixed(4)}
            tone="danger"
            mono
          />
          <MetricCard
            label="reproducibility"
            value={p.shadowguard_result.reproducibility_score.toFixed(2)}
            tone="warning"
            mono
          />
          <MetricCard
            label="signals"
            value={p.signals_found.length}
            hint={`${p.shadowguard_result.blocked_actions.length} actions blocked`}
          />
        </div>

        <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
          <div className="space-y-4">
            <ProofCard eyebrow="claim summary" title="What was claimed">
              <p className="text-sm leading-relaxed text-foreground">{p.claim_text}</p>
              <dl className="mt-4 grid grid-cols-2 gap-y-2 font-mono text-[11px]">
                <dt className="text-muted-foreground">repo_url</dt>
                <dd className="truncate text-primary">{p.repo_url}</dd>
                <dt className="text-muted-foreground">claim_type</dt>
                <dd className="text-foreground">{p.claim_type}</dd>
                <dt className="text-muted-foreground">runtime_target</dt>
                <dd className="text-foreground">{p.runtime_target}</dd>
              </dl>
            </ProofCard>

            <ProofCard eyebrow="shadowguard result" title="Policy evaluation">
              <div className="grid gap-3 md:grid-cols-2">
                <StatBox k="policy_version" v={p.shadowguard_result.policy_version} />
                <StatBox
                  k="risk_score"
                  v={p.shadowguard_result.risk_score.toFixed(4)}
                  tone="danger"
                />
                <StatBox
                  k="reproducibility_score"
                  v={p.shadowguard_result.reproducibility_score.toFixed(2)}
                  tone="warning"
                />
                <StatBox
                  k="blocked_actions"
                  v={String(p.shadowguard_result.blocked_actions.length)}
                />
              </div>
              <p className="mt-4 font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
                blocked
              </p>
              <ul className="mt-2 space-y-1 font-mono text-[11px] text-danger/90">
                {p.shadowguard_result.blocked_actions.map((a) => (
                  <li key={a}>× {a}</li>
                ))}
              </ul>
            </ProofCard>

            <ProofCard eyebrow="gemma explanation" title="Model-authored narrative">
              <p className="text-sm leading-relaxed text-foreground">{p.gemma_explanation}</p>
            </ProofCard>

            <ProofCard eyebrow="signals" title="Detected risk signals">
              <RiskSignalList signals={p.signals_found} />
            </ProofCard>

            <ProofCard eyebrow="evidence chain" title="Artifacts collected">
              <EvidenceChain items={p.evidence_items} />
            </ProofCard>

            <ProofCard eyebrow="missing evidence" title="What we could not verify">
              <ul className="space-y-1.5 text-sm text-muted-foreground">
                {p.missing_evidence.map((m) => (
                  <li key={m} className="flex gap-2">
                    <span className="text-warning">▲</span>
                    <span>{m}</span>
                  </li>
                ))}
              </ul>
            </ProofCard>

            <ProofCard eyebrow="security notes" title="Sandbox posture">
              <ul className="space-y-1.5 text-sm text-muted-foreground">
                {p.security_notes.map((s) => (
                  <li key={s} className="flex gap-2">
                    <span className="text-success">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </ProofCard>
          </div>

          <aside className="space-y-4">
            <AMDProofCard proof={p.amd_gemma_proof} />
            <GemmaProofCard proof={p.amd_gemma_proof} />

            <ProofCard eyebrow="hashes" title="Integrity">
              <dl className="grid grid-cols-1 gap-2 font-mono text-[11px]">
                <HashRow k="execution_hash" v={p.hashes.execution_hash} />
                <HashRow k="environment_hash" v={p.hashes.environment_hash} />
                <HashRow k="log_hash" v={p.hashes.log_hash} />
              </dl>
            </ProofCard>

            <ProofCard eyebrow="export" title="Take the passport with you">
              <ExportButtons passport={p} />
              <p className="mt-3 text-[11px] text-muted-foreground">
                JSON exports the full artifact. PDF uses the browser print pipeline; the share
                action copies this run-specific URL.
              </p>
            </ProofCard>

            <div className="flex justify-between">
              <Link
                to="/trace"
                className="font-mono text-[11px] text-muted-foreground hover:text-foreground"
              >
                ← back to trace
              </Link>
              <Link to="/intake" className="font-mono text-[11px] text-primary hover:underline">
                verify another claim →
              </Link>
            </div>
          </aside>
        </div>
      </div>
    </AppShell>
  );
}

function StatBox({ k, v, tone }: { k: string; v: string; tone?: "danger" | "warning" }) {
  return (
    <div className="rounded-md border border-border/70 bg-background/40 p-3">
      <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">{k}</p>
      <p
        className={`mt-1 font-mono text-sm ${
          tone === "danger"
            ? "text-danger"
            : tone === "warning"
              ? "text-warning"
              : "text-foreground"
        }`}
      >
        {v}
      </p>
    </div>
  );
}

function HashRow({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-md border border-border/70 bg-background/40 p-2">
      <span className="text-muted-foreground">{k}</span>
      <span className="truncate text-primary/90">{v}</span>
    </div>
  );
}
