import type { RiskSignal } from "@/data/mockPassport";
import { StatusBadge } from "./StatusBadge";

const toneFor = (s: RiskSignal["severity"]) =>
  s === "critical" ? "danger" : s === "high" ? "warning" : s === "medium" ? "amd" : "muted";

export function RiskSignalList({ signals }: { signals: RiskSignal[] }) {
  return (
    <ul className="space-y-2">
      {signals.map((s) => (
        <li key={s.id} className="rounded-md border border-border/70 bg-background/50 p-3">
          <div className="flex items-center justify-between gap-2">
            <p className="text-sm font-medium text-foreground">{s.label}</p>
            <StatusBadge tone={toneFor(s.severity) as never}>{s.severity}</StatusBadge>
          </div>
          <p className="mt-1 text-[12px] leading-relaxed text-muted-foreground">{s.detail}</p>
        </li>
      ))}
    </ul>
  );
}
