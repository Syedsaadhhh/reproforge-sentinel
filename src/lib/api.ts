/**
 * ReproForge Sentinel — client API stubs.
 *
 * These functions return fixture data today. When the backend ships,
 * swap the bodies for real fetch() calls against /verify, /runs/:id, etc.
 *
 * NEVER put Fireworks / Gemma API keys in this file. The backend proxies
 * all model calls. The frontend only ever sees the sanitized proof payload.
 */

import { mockPassport, fixtureLogLines, type Passport } from "../data/mockPassport";

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));
const apiBase = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, "");

export const runtimeMode = apiBase ? "backend" : "fixture";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!apiBase) throw new Error("Backend is not configured");
  const response = await fetch(`${apiBase}${path}`, {
    ...init,
    headers: { "content-type": "application/json", ...init?.headers },
  });
  if (!response.ok) throw new Error(`ReproForge API ${response.status}: ${await response.text()}`);
  return response.json() as Promise<T>;
}

export interface ClaimInput {
  repo_url: string;
  claim_text: string;
  claim_type: string;
  runtime_target: string;
  policies?: string[];
  verification_mode?: "fast" | "deep";
}

export interface RunHandle {
  run_id: string;
  status: "queued" | "running" | "complete" | "failed";
}

export interface RunStatus {
  run_id: string;
  status: RunHandle["status"];
  step: number;
  logs: { t: string; line: string; step: number }[];
}

export async function submitClaim(input: ClaimInput): Promise<RunHandle> {
  if (apiBase) {
    return request<RunHandle>("/verify", { method: "POST", body: JSON.stringify(input) });
  }
  await delay(220);
  void input;
  return { run_id: mockPassport.run_id, status: "queued" };
}

export async function startVerification(run_id: string): Promise<RunHandle> {
  await delay(150);
  return { run_id, status: "running" };
}

export async function getRunStatus(run_id: string): Promise<RunStatus> {
  if (apiBase) return request<RunStatus>(`/runs/${encodeURIComponent(run_id)}`);
  await delay(120);
  return {
    run_id,
    status: "complete",
    step: fixtureLogLines.length - 1,
    logs: fixtureLogLines,
  };
}

export async function getPassport(run_id: string): Promise<Passport> {
  if (apiBase) return request<Passport>(`/passport/${encodeURIComponent(run_id)}`);
  await delay(180);
  return { ...mockPassport, run_id };
}

/**
 * Future canonical entry point: POST /verify.
 * Returns a run handle the client can subscribe to.
 */
export async function verifyClaim(input: ClaimInput): Promise<RunHandle> {
  const handle = await submitClaim(input);
  return apiBase ? handle : startVerification(handle.run_id);
}
