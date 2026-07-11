import { runtimeMode } from "@/lib/api";

export function FixtureBanner() {
  const backend = runtimeMode === "backend";
  return (
    <div
      className={
        backend
          ? "border-b border-primary/30 bg-primary/10"
          : "border-b border-warning/30 bg-warning/10"
      }
    >
      <div
        className={
          backend
            ? "mx-auto flex max-w-[1400px] items-center gap-2 px-6 py-1.5 font-mono text-[11px] text-primary"
            : "mx-auto flex max-w-[1400px] items-center gap-2 px-6 py-1.5 font-mono text-[11px] text-warning"
        }
      >
        <span
          className={
            backend
              ? "inline-block h-1.5 w-1.5 rounded-full bg-primary"
              : "inline-block h-1.5 w-1.5 rounded-full bg-warning"
          }
        />
        {backend
          ? "BACKEND MODE · runtime proof is accepted only from confirmed API fields"
          : "GUIDED FIXTURE · proof_status=fixture_until_backend · connect VITE_API_BASE_URL for live API"}
      </div>
    </div>
  );
}
