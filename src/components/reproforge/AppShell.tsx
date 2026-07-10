import { Link } from "@tanstack/react-router";
import { type ReactNode } from "react";
import { ShieldCheck } from "lucide-react";
import { FixtureBanner } from "./FixtureBanner";

export function AppShell({
  children,
  currentStep,
}: {
  children: ReactNode;
  currentStep?: "intake" | "trace" | "passport" | "home";
}) {
  const steps: { id: NonNullable<typeof currentStep>; label: string; to: string }[] = [
    { id: "intake", label: "Intake", to: "/intake" },
    { id: "trace", label: "Trace", to: "/trace" },
    { id: "passport", label: "Passport", to: "/passport" },
  ];

  return (
    <div className="min-h-screen bg-background">
      <FixtureBanner />
      <header className="sticky top-0 z-30 border-b border-border/70 bg-background/80 backdrop-blur">
        <div className="mx-auto flex h-14 max-w-[1400px] items-center justify-between px-6">
          <Link to="/" className="flex items-center gap-2.5">
            <span className="grid h-7 w-7 place-items-center rounded-md bg-primary/15 text-primary ring-1 ring-primary/30">
              <ShieldCheck className="h-4 w-4" />
            </span>
            <span className="font-semibold tracking-tight">
              ReproForge <span className="text-primary">Sentinel</span>
            </span>
            <span className="ml-3 hidden font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground sm:inline">
              claim → evidence
            </span>
          </Link>

          <nav className="hidden items-center gap-1 md:flex">
            {steps.map((s) => (
              <Link
                key={s.id}
                to={s.to}
                className={`rounded-md px-3 py-1.5 text-sm transition-colors ${
                  currentStep === s.id
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {s.label}
              </Link>
            ))}
          </nav>

          <div className="hidden items-center gap-2 font-mono text-[11px] text-muted-foreground md:flex">
            <span className="inline-block h-1.5 w-1.5 rounded-full bg-success" />
            sandbox online
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-[1400px] px-6 py-8">{children}</main>
      <footer className="border-t border-border/60">
        <div className="mx-auto flex max-w-[1400px] flex-col items-start justify-between gap-2 px-6 py-6 font-mono text-[11px] text-muted-foreground md:flex-row md:items-center">
          <span>reproforge-sentinel · fixture build · no live model calls</span>
          <span>policy shadowguard/2026.07-strict</span>
        </div>
      </footer>
    </div>
  );
}
