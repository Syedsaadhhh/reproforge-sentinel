import { useEffect, useRef } from "react";
import { cn } from "@/lib/utils";

export interface TerminalLine {
  t: string;
  line: string;
}

export function TerminalWindow({
  title = "sandbox/run.log",
  lines,
  className,
}: {
  title?: string;
  lines: TerminalLine[];
  className?: string;
}) {
  const scrollRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [lines.length]);

  return (
    <div
      className={cn(
        "flex h-full flex-col overflow-hidden rounded-lg border border-border bg-[#08090A]",
        className,
      )}
    >
      <div className="flex items-center justify-between border-b border-border/80 px-3 py-2">
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-danger/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-warning/70" />
          <span className="h-2.5 w-2.5 rounded-full bg-success/70" />
          <span className="ml-2 font-mono text-[11px] text-muted-foreground">{title}</span>
        </div>
        <span className="font-mono text-[10px] uppercase tracking-[0.15em] text-muted-foreground">
          live
        </span>
      </div>
      <div
        ref={scrollRef}
        className="flex-1 overflow-auto px-4 py-3 font-mono text-[12px] leading-6"
      >
        {lines.length === 0 && <div className="text-muted-foreground">waiting for sandbox…</div>}
        {lines.map((l, i) => (
          <div key={i} className="flex gap-3">
            <span className="shrink-0 text-muted-foreground">[{l.t}]</span>
            <span className="text-foreground">{l.line}</span>
          </div>
        ))}
        {lines.length > 0 && (
          <span className="inline-block h-3 w-1.5 animate-pulse bg-primary/80 align-middle" />
        )}
      </div>
    </div>
  );
}
