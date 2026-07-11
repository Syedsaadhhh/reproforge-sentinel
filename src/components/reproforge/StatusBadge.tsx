import { cn } from "@/lib/utils";

type Tone = "cyan" | "amd" | "success" | "warning" | "danger" | "muted";

const tones: Record<Tone, string> = {
  cyan: "bg-primary/10 text-primary ring-primary/30",
  amd: "bg-amd/10 text-amd ring-amd/40",
  success: "bg-success/10 text-success ring-success/30",
  warning: "bg-warning/10 text-warning ring-warning/30",
  danger: "bg-danger/10 text-danger ring-danger/30",
  muted: "bg-muted text-muted-foreground ring-border",
};

export function StatusBadge({
  children,
  tone = "muted",
  className,
}: {
  children: React.ReactNode;
  tone?: Tone;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 font-mono text-[10px] uppercase tracking-[0.14em] ring-1 ring-inset",
        tones[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}
