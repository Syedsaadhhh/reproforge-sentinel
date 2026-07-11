import type { EvidenceItem } from "@/data/mockPassport";
import { FileText, Radio, Hash, Package, ScrollText } from "lucide-react";

const iconFor = (k: EvidenceItem["kind"]) =>
  k === "file"
    ? FileText
    : k === "log"
      ? ScrollText
      : k === "hash"
        ? Hash
        : k === "network"
          ? Radio
          : Package;

export function EvidenceChain({ items }: { items: EvidenceItem[] }) {
  return (
    <ol className="divide-y divide-border/60 overflow-hidden rounded-md border border-border/70">
      {items.map((it, i) => {
        const Icon = iconFor(it.kind);
        return (
          <li key={it.id} className="flex gap-3 bg-background/40 p-3">
            <span className="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-md bg-muted text-muted-foreground">
              <Icon className="h-4 w-4" />
            </span>
            <div className="min-w-0 flex-1">
              <div className="flex items-center justify-between gap-2">
                <p className="truncate text-sm font-medium text-foreground">{it.label}</p>
                <span className="font-mono text-[10px] uppercase tracking-[0.15em] text-muted-foreground">
                  #{String(i + 1).padStart(2, "0")} · {it.kind}
                </span>
              </div>
              <p className="text-[12px] text-muted-foreground">{it.detail}</p>
              {it.hash && (
                <p className="mt-1 truncate font-mono text-[11px] text-primary/80">{it.hash}</p>
              )}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
