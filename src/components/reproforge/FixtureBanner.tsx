export function FixtureBanner() {
  return (
    <div className="border-b border-warning/30 bg-warning/10">
      <div className="mx-auto flex max-w-[1400px] items-center gap-2 px-6 py-1.5 font-mono text-[11px] text-warning">
        <span className="inline-block h-1.5 w-1.5 rounded-full bg-warning" />
        GUIDED FIXTURE · proof_status=fixture_until_backend · connect VITE_API_BASE_URL for live API
      </div>
    </div>
  );
}
