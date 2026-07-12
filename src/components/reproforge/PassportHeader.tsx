import type { Passport } from "@/data/mockPassport";
import { StatusBadge } from "./StatusBadge";

const verdictTone: Record<Passport["verdict"], "success" | "warning" | "danger" | "amd"> = {
  verified: "success",
  partial: "warning",
  blocked: "danger",
  unverified: "amd",
};

export function PassportHeader({ passport }: { passport: Passport }) {
  return (
    <div className="rounded-lg border border-border bg-gradient-to-br from-card/80 to-card/40 p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
            reproducibility passport
          </p>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight">{passport.passport_id}</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Sealed {new Date(passport.created_at).toUTCString()}
          </p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <StatusBadge tone={verdictTone[passport.verdict]}>
            verdict · {passport.verdict}
          </StatusBadge>
          <span className="font-mono text-[11px] text-muted-foreground">run {passport.run_id}</span>
        </div>
      </div>
    </div>
  );
}
