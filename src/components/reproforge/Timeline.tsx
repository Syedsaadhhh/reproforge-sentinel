import { cn } from "@/lib/utils";
import { Check, Loader2 } from "lucide-react";

export interface TimelineStepData {
  id: number;
  label: string;
}

export function Timeline({
  steps,
  currentStep,
  complete,
}: {
  steps: TimelineStepData[];
  currentStep: number;
  complete: boolean;
}) {
  return (
    <ol className="relative space-y-1">
      {steps.map((s, i) => {
        const state =
          complete || i < currentStep ? "done" : i === currentStep ? "active" : "pending";
        return (
          <li key={s.id} className="relative flex gap-3 pb-4 last:pb-0">
            {i !== steps.length - 1 && (
              <span
                className={cn(
                  "absolute left-[11px] top-6 h-full w-px",
                  state === "done" ? "bg-primary/40" : "bg-border",
                )}
              />
            )}
            <span
              className={cn(
                "relative z-10 mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full ring-1",
                state === "done" && "bg-primary/15 text-primary ring-primary/50",
                state === "active" && "bg-primary/10 text-primary ring-primary",
                state === "pending" && "bg-muted text-muted-foreground ring-border",
              )}
            >
              {state === "done" ? (
                <Check className="h-3 w-3" />
              ) : state === "active" ? (
                <Loader2 className="h-3 w-3 animate-spin" />
              ) : (
                <span className="font-mono text-[10px]">{s.id + 1}</span>
              )}
            </span>
            <div className="pt-0.5">
              <p
                className={cn(
                  "text-sm",
                  state === "pending" ? "text-muted-foreground" : "text-foreground",
                )}
              >
                {s.label}
              </p>
              <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
                step {String(s.id + 1).padStart(2, "0")} · {state}
              </p>
            </div>
          </li>
        );
      })}
    </ol>
  );
}
