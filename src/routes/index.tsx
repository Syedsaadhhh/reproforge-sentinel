import { createFileRoute, Link } from "@tanstack/react-router";
import { AppShell } from "@/components/reproforge/AppShell";
import { FlowStrip } from "@/components/reproforge/FlowStrip";
import { AMDProofCard, GemmaProofCard } from "@/components/reproforge/ProofCards";
import { StatusBadge } from "@/components/reproforge/StatusBadge";
import { Button } from "@/components/ui/button";
import { mockPassport } from "@/data/mockPassport";
import { ArrowRight, ShieldCheck, Terminal, FileCheck2 } from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "ReproForge Sentinel — Verify AI claims with sandboxed evidence" },
      {
        name: "description",
        content:
          "Submit a repo and claim. ReproForge Sentinel runs ShadowGuard scoring, drafts a Gemma explanation, and seals a Reproducibility Passport.",
      },
    ],
  }),
  component: LandingPage,
});

function LandingPage() {
  return (
    <AppShell currentStep="home">
      <section className="grid gap-10 pb-14 pt-8 lg:grid-cols-[1.15fr_1fr] lg:gap-14 lg:pt-14">
        <div>
          <StatusBadge tone="cyan">AMD ACT II · hackathon build</StatusBadge>
          <h1 className="mt-5 text-4xl font-semibold tracking-tight text-foreground md:text-5xl">
            Verify AI claims with <span className="text-primary">sandboxed evidence</span>.
          </h1>
          <p className="mt-5 max-w-xl text-[15px] leading-relaxed text-muted-foreground">
            ReproForge Sentinel is a claim-to-evidence verification layer. This guided MVP turns a
            curated repository claim into a sealed Reproducibility Passport with ShadowGuard risk
            scoring, an evidence chain, and a Gemma-ready explanation contract.
          </p>

          <div className="mt-7 flex flex-wrap gap-3">
            <Button asChild size="lg" className="gap-2">
              <Link to="/trace" search={{ sample: 1 } as never}>
                Run sample verification <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="gap-2">
              <Link to="/intake">Enter custom repo</Link>
            </Button>
          </div>

          <div className="mt-10">
            <FlowStrip />
          </div>

          <div className="mt-10 grid gap-4 sm:grid-cols-3">
            <Feature
              icon={<ShieldCheck className="h-4 w-4" />}
              title="ShadowGuard"
              body="Deterministic policy engine gates every sandboxed action."
            />
            <Feature
              icon={<Terminal className="h-4 w-4" />}
              title="Live trace"
              body="Every evaluation step is replayed from the backend result or a clearly labeled fixture."
            />
            <Feature
              icon={<FileCheck2 className="h-4 w-4" />}
              title="Passport"
              body="One sealed artifact: claim, verdict, evidence, and explicit proof status."
            />
          </div>
        </div>

        <aside className="space-y-4">
          <div className="rounded-lg border border-border bg-card/60 p-5">
            <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
              guided fixture · pp_01HNXQ7ZKMB4T3RG9E2A
            </p>
            <h3 className="mt-2 text-lg font-semibold">
              Agentic RAG benchmark · 92.4% pass@1 claim
            </h3>
            <p className="mt-2 text-sm text-muted-foreground">
              ShadowGuard flagged test-set contamination and non-deterministic scoring. Verdict:{" "}
              <span className="text-warning">partial</span>.
            </p>
            <dl className="mt-4 grid grid-cols-2 gap-3 font-mono text-[11px]">
              <div>
                <dt className="text-muted-foreground">risk_score</dt>
                <dd className="text-danger">0.9037</dd>
              </div>
              <div>
                <dt className="text-muted-foreground">reproducibility</dt>
                <dd className="text-warning">0.42</dd>
              </div>
              <div>
                <dt className="text-muted-foreground">signals</dt>
                <dd className="text-foreground">3</dd>
              </div>
              <div>
                <dt className="text-muted-foreground">blocked_actions</dt>
                <dd className="text-foreground">2</dd>
              </div>
            </dl>
          </div>
          <AMDProofCard proof={mockPassport.amd_gemma_proof} />
          <GemmaProofCard proof={mockPassport.amd_gemma_proof} />
        </aside>
      </section>
    </AppShell>
  );
}

function Feature({ icon, title, body }: { icon: React.ReactNode; title: string; body: string }) {
  return (
    <div className="rounded-lg border border-border/70 bg-card/40 p-4">
      <span className="grid h-7 w-7 place-items-center rounded-md bg-primary/10 text-primary ring-1 ring-primary/30">
        {icon}
      </span>
      <p className="mt-3 text-sm font-semibold text-foreground">{title}</p>
      <p className="mt-1 text-[12px] leading-relaxed text-muted-foreground">{body}</p>
    </div>
  );
}
