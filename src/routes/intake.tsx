import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { AppShell } from "@/components/reproforge/AppShell";
import { StatusBadge } from "@/components/reproforge/StatusBadge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useState } from "react";
import { sampleClaim } from "@/data/mockPassport";
import { ArrowRight } from "lucide-react";
import { saveClaimInput } from "@/lib/traceUtils";

export const Route = createFileRoute("/intake")({
  head: () => ({
    meta: [
      { title: "Intake · ReproForge Sentinel" },
      {
        name: "description",
        content: "Submit a repository and claim for sandboxed verification.",
      },
    ],
  }),
  component: IntakePage,
});

function IntakePage() {
  const navigate = useNavigate();
  const [repo, setRepo] = useState(sampleClaim.repo_url);
  const [claim, setClaim] = useState(sampleClaim.claim_text);
  const [claimType, setClaimType] = useState(sampleClaim.claim_type);
  const [runtime, setRuntime] = useState(sampleClaim.runtime_target);
  const [mode, setMode] = useState<"fast" | "deep">("deep");
  const [pol, setPol] = useState({ egress: true, exec: true, fs: true });

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    saveClaimInput({
      repo_url: repo.trim(),
      claim_text: claim.trim(),
      claim_type: claimType,
      runtime_target: runtime.trim(),
      verification_mode: mode,
      policies: [
        pol.egress && "egress_deny",
        pol.exec && "exec_pipe_deny",
        pol.fs && "fs_readonly",
      ].filter(Boolean) as string[],
    });
    navigate({ to: "/trace", search: { sample: 0 } as never });
  };

  return (
    <AppShell currentStep="intake">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <StatusBadge tone="cyan">step 01 · intake</StatusBadge>
          <h1 className="mt-3 text-2xl font-semibold tracking-tight">Submit a claim</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            This MVP evaluates claim metadata and declared policies; arbitrary repositories are not yet
            cloned or executed. Do not submit secrets, keys, or private URLs.
          </p>
        </div>
      </div>

      <form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1.35fr_1fr]">
        <div className="space-y-5 rounded-lg border border-border bg-card/50 p-6">
          <Field label="Repository URL" hint="public git URL or gh: shorthand">
            <Input
              value={repo}
              onChange={(e) => setRepo(e.target.value)}
              placeholder="https://github.com/org/repo"
              className="font-mono text-sm"
            />
          </Field>

          <Field label="Claim text" hint="the exact statement to verify">
            <Textarea
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
              rows={4}
              className="text-sm"
            />
          </Field>

          <div className="grid gap-4 md:grid-cols-2">
            <Field label="Claim type">
              <Select value={claimType} onValueChange={setClaimType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="benchmark_result">benchmark_result</SelectItem>
                  <SelectItem value="capability_claim">capability_claim</SelectItem>
                  <SelectItem value="security_claim">security_claim</SelectItem>
                  <SelectItem value="reproduction">reproduction</SelectItem>
                </SelectContent>
              </Select>
            </Field>
            <Field label="Runtime target">
              <Input
                value={runtime}
                onChange={(e) => setRuntime(e.target.value)}
                className="font-mono text-sm"
              />
            </Field>
          </div>

          <div className="rounded-md border border-border/70 bg-background/40 p-4">
            <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
              sandbox policies
            </p>
            <div className="mt-3 space-y-3">
              <Toggle
                label="Deny outbound network egress"
                checked={pol.egress}
                onChange={(v) => setPol((p) => ({ ...p, egress: v }))}
              />
              <Toggle
                label="Block shell exec of piped scripts"
                checked={pol.exec}
                onChange={(v) => setPol((p) => ({ ...p, exec: v }))}
              />
              <Toggle
                label="Read-only host filesystem"
                checked={pol.fs}
                onChange={(v) => setPol((p) => ({ ...p, fs: v }))}
              />
            </div>
          </div>

          <div className="rounded-md border border-border/70 bg-background/40 p-4">
            <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
              verification mode
            </p>
            <div className="mt-3 flex gap-2">
              {(["fast", "deep"] as const).map((m) => (
                <button
                  key={m}
                  type="button"
                  onClick={() => setMode(m)}
                  className={`rounded-md border px-3 py-1.5 font-mono text-xs uppercase tracking-widest transition-colors ${
                    mode === m
                      ? "border-primary/50 bg-primary/10 text-primary"
                      : "border-border text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center justify-between border-t border-border/60 pt-4">
            <Link to="/" className="text-sm text-muted-foreground hover:text-foreground">
              ← back
            </Link>
            <Button type="submit" size="lg" className="gap-2">
              Generate verification plan <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <aside className="space-y-4">
          <div className="rounded-lg border border-border bg-card/40 p-5">
            <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
              parsed assertion
            </p>
            <p className="mt-2 text-sm text-foreground">{claim}</p>
            <dl className="mt-4 grid grid-cols-2 gap-y-2 font-mono text-[11px]">
              <dt className="text-muted-foreground">claim_type</dt>
              <dd className="text-foreground">{claimType}</dd>
              <dt className="text-muted-foreground">runtime</dt>
              <dd className="truncate text-foreground">{runtime}</dd>
              <dt className="text-muted-foreground">mode</dt>
              <dd className="text-foreground">{mode}</dd>
            </dl>
          </div>

          <div className="rounded-lg border border-border bg-card/40 p-5">
            <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
              pre-flight checklist
            </p>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li>✓ Claim metadata and declared policies will be evaluated</li>
              <li>✓ ShadowGuard policy shadowguard/2026.07-strict attached</li>
              <li>✓ Gemma explanation contract prepared for backend proxy</li>
              <li className="text-warning">! Gemma/AMD proof stays pending unless a configured backend returns verified provenance</li>
            </ul>
          </div>
        </aside>
      </form>
    </AppShell>
  );
}

function Field({
  label,
  hint,
  children,
}: {
  label: string;
  hint?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1.5">
      <Label className="flex items-baseline justify-between text-xs font-medium text-foreground">
        <span>{label}</span>
        {hint && <span className="font-normal text-muted-foreground">{hint}</span>}
      </Label>
      {children}
    </div>
  );
}

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <label className="flex cursor-pointer items-center justify-between gap-3 text-sm">
      <span className="text-foreground">{label}</span>
      <Switch checked={checked} onCheckedChange={onChange} />
    </label>
  );
}
