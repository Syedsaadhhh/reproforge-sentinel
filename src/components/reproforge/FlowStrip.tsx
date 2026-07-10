import { ArrowRight } from "lucide-react";

const steps = ["Claim", "ShadowGuard", "Gemma", "AMD / Fireworks", "Passport"];

export function FlowStrip() {
  return (
    <div className="flex flex-wrap items-center gap-2 rounded-lg border border-border/70 bg-card/40 p-3 font-mono text-[11px] uppercase tracking-[0.16em] text-muted-foreground">
      {steps.map((s, i) => (
        <div key={s} className="flex items-center gap-2">
          <span
            className={
              i === 0 || i === steps.length - 1
                ? "text-primary"
                : i === 3
                  ? "text-amd"
                  : "text-foreground"
            }
          >
            {s}
          </span>
          {i < steps.length - 1 && <ArrowRight className="h-3 w-3 opacity-60" />}
        </div>
      ))}
    </div>
  );
}
