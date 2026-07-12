import { createFileRoute, Link } from "@tanstack/react-router";
import { AppShell } from "@/components/reproforge/AppShell";
import { StatusBadge } from "@/components/reproforge/StatusBadge";
import { Timeline } from "@/components/reproforge/Timeline";
import { TerminalWindow } from "@/components/reproforge/TerminalWindow";
import { AMDProofCard, GemmaProofCard } from "@/components/reproforge/ProofCards";
import { RiskSignalList } from "@/components/reproforge/RiskSignalList";
import { ProofCard } from "@/components/reproforge/ProofCard";
import { MetricCard } from "@/components/reproforge/MetricCard";
import { Button } from "@/components/ui/button";
import { fixtureLogLines, mockPassport, timelineSteps } from "@/data/mockPassport";
import { verifyClaim, loadClaimInput, sampleClaimInput } from "@/lib/traceUtils";
import { getPassport, getRunStatus, runtimeMode, type ClaimInput } from "@/lib/api";
import { useEffect, useRef, useState } from "react";
import { ArrowRight, Pause, Play, Square } from "lucide-react";

export const Route = createFileRoute("/trace")({
  validateSearch: (s: Record<string, unknown>) => ({
    sample: s.sample === 1 || s.sample === "1" ? 1 : 0,
  }),
  head: () => ({
    meta: [
      { title: "Live trace · ReproForge Sentinel" },
      {
        name: "description",
        content:
          "Watch the sandbox stream ShadowGuard scoring, signals, and the Gemma explanation.",
      },
    ],
  }),
  component: TracePage,
});

const STEP_DELAY_MS = 1500;

function TracePage() {
  const [step, setStep] = useState(-1);
  const [logs, setLogs] = useState<typeof fixtureLogLines>([]);
  const [paused, setPaused] = useState(false);
  const [killed, setKilled] = useState(false);
  const [runId, setRunId] = useState<string>(mockPassport.run_id);
  const [claimInput, setClaimInput] = useState<ClaimInput>(sampleClaimInput);
  const [rawLogsOpen, setRawLogsOpen] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);
  const [sourceLogs, setSourceLogs] = useState(fixtureLogLines);
  const [passport, setPassport] = useState(mockPassport);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const input = loadClaimInput();
        setClaimInput(input);
        const handle = await verifyClaim(input);
        if (cancelled) return;
        setRunId(handle.run_id);
        if (runtimeMode === "backend") {
          const [status, backendPassport] = await Promise.all([
            getRunStatus(handle.run_id),
            getPassport(handle.run_id),
          ]);
          if (cancelled) return;
          setSourceLogs(status.logs);
          setPassport(backendPassport);
        }
        setStep(0);
      } catch (error) {
        if (!cancelled) setRunError(error instanceof Error ? error.message : "Verification failed");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (step < 0 || paused || killed) return;
    if (step >= sourceLogs.length) return;
    timerRef.current = window.setTimeout(
      () => {
        setLogs((l) => [...l, sourceLogs[step]]);
        setStep((s) => s + 1);
      },
      step === 0 ? 400 : STEP_DELAY_MS,
    );
    return () => {
      if (timerRef.current) window.clearTimeout(timerRef.current);
    };
  }, [step, paused, killed, sourceLogs]);

  const complete = step >= sourceLogs.length;
  const activeStep = Math.min(step < 0 ? 0 : step, timelineSteps.length - 1);
  const currentSignals = passport.signals_found.slice(0, Math.max(0, step - 2));

  return (
    <AppShell currentStep="trace">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <StatusBadge tone="cyan">step 02 · live trace</StatusBadge>
          <h1 className="mt-3 text-2xl font-semibold tracking-tight">
            Sandbox run · <span className="font-mono text-primary">{runId}</span>
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {runError
              ? `Run failed: ${runError}`
              : complete
                ? "Run complete. Reproducibility Passport sealed."
                : killed
                  ? "Run terminated by operator."
                  : paused
                    ? "Run paused."
                    : runtimeMode === "backend"
                      ? "Replaying the completed backend evaluation…"
                      : "Replaying a guided fixture evaluation…"}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-2"
            onClick={() => setPaused((p) => !p)}
            disabled={complete || killed}
          >
            {paused ? <Play className="h-3.5 w-3.5" /> : <Pause className="h-3.5 w-3.5" />}
            {paused ? "Resume" : "Pause"}
          </Button>
          <Button variant="outline" size="sm" onClick={() => setRawLogsOpen((open) => !open)}>
            {rawLogsOpen ? "Hide raw logs" : "View raw logs"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            className="gap-2 text-danger hover:text-danger"
            onClick={() => setKilled(true)}
            disabled={complete || killed}
          >
            <Square className="h-3.5 w-3.5" /> Kill switch
          </Button>
          {complete && (
            <Button asChild size="sm" className="gap-2">
              <Link to="/passport" search={{ run_id: runId } as never}>
                View Passport <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </Button>
          )}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[280px_minmax(0,1fr)_360px]">
        <aside className="rounded-lg border border-border bg-card/40 p-5">
          <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
            verification pipeline
          </p>
          <Timeline steps={timelineSteps} currentStep={activeStep} complete={complete} />
        </aside>

        <div className="h-[540px] space-y-3">
          <div className={rawLogsOpen ? "h-[360px]" : "h-full"}>
            <TerminalWindow title={`sandbox/${runId}.log`} lines={logs} />
          </div>
          {rawLogsOpen && (
            <pre className="h-[168px] overflow-auto rounded-lg border border-border bg-background/80 p-4 font-mono text-[11px] text-muted-foreground">
              {JSON.stringify(
                {
                  run_id: runId,
                  claim: claimInput,
                  status: complete ? "complete" : killed ? "killed" : paused ? "paused" : "running",
                  logs,
                },
                null,
                2,
              )}
            </pre>
          )}
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <MetricCard
              label="risk_score"
              value={step >= 3 ? passport.shadowguard_result.risk_score.toFixed(4) : "—"}
              tone="danger"
              mono
              hint="shadowguard"
            />
            <MetricCard
              label="reproducibility"
              value={complete ? passport.shadowguard_result.reproducibility_score.toFixed(2) : "—"}
              tone="warning"
              mono
            />
          </div>

          <ProofCard eyebrow="signals" title="Risk signals detected">
            {currentSignals.length === 0 ? (
              <p className="font-mono text-[11px] text-muted-foreground">
                awaiting detection pass…
              </p>
            ) : (
              <RiskSignalList signals={currentSignals} />
            )}
          </ProofCard>

          {step >= 3 && (
            <ProofCard eyebrow="blocked" title="ShadowGuard blocked actions">
              <ul className="space-y-1 font-mono text-[11px] text-danger/90">
                {passport.shadowguard_result.blocked_actions.map((a) => (
                  <li key={a}>× {a}</li>
                ))}
              </ul>
            </ProofCard>
          )}

          {step >= 4 && <AMDProofCard proof={passport.amd_gemma_proof} />}
          {step >= 5 && <GemmaProofCard proof={passport.amd_gemma_proof} />}
        </div>
      </div>
    </AppShell>
  );
}
