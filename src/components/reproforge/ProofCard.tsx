import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

export function ProofCard({
  title,
  eyebrow,
  children,
  className,
  action,
}: {
  title: string;
  eyebrow?: string;
  children: ReactNode;
  className?: string;
  action?: ReactNode;
}) {
  return (
    <section
      className={cn(
        "rounded-lg border border-border bg-card/60 p-5 shadow-[0_1px_0_0_rgba(255,255,255,0.02)_inset]",
        className,
      )}
    >
      <header className="mb-3 flex items-start justify-between gap-3">
        <div>
          {eyebrow && (
            <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
              {eyebrow}
            </p>
          )}
          <h3 className="mt-1 text-sm font-semibold text-foreground">{title}</h3>
        </div>
        {action}
      </header>
      {children}
    </section>
  );
}
