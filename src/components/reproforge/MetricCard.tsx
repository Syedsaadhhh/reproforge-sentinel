import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

export function MetricCard({
  label,
  value,
  hint,
  tone,
  mono,
}: {
  label: string;
  value: ReactNode;
  hint?: string;
  tone?: "cyan" | "amd" | "success" | "warning" | "danger";
  mono?: boolean;
}) {
  const accent =
    tone === "cyan"
      ? "text-primary"
      : tone === "amd"
        ? "text-amd"
        : tone === "success"
          ? "text-success"
          : tone === "warning"
            ? "text-warning"
            : tone === "danger"
              ? "text-danger"
              : "text-foreground";
  return (
    <div className="rounded-lg border border-border bg-card/60 p-4">
      <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
        {label}
      </p>
      <p className={cn("mt-2 text-2xl font-semibold", mono && "font-mono", accent)}>{value}</p>
      {hint && <p className="mt-1 text-[11px] text-muted-foreground">{hint}</p>}
    </div>
  );
}
