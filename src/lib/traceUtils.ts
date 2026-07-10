import { verifyClaim, type ClaimInput } from "./api";
import { sampleClaim } from "@/data/mockPassport";

export { verifyClaim };

export const sampleClaimInput: ClaimInput = {
  repo_url: sampleClaim.repo_url,
  claim_text: sampleClaim.claim_text,
  claim_type: sampleClaim.claim_type,
  runtime_target: sampleClaim.runtime_target,
  verification_mode: "deep",
  policies: ["egress_deny", "exec_pipe_deny", "fs_readonly"],
};

export const claimStorageKey = "reproforge.claim-input.v1";

export function saveClaimInput(input: ClaimInput) {
  window.sessionStorage.setItem(claimStorageKey, JSON.stringify(input));
}

export function loadClaimInput(): ClaimInput {
  if (typeof window === "undefined") return sampleClaimInput;
  try {
    const value = window.sessionStorage.getItem(claimStorageKey);
    return value ? ({ ...sampleClaimInput, ...JSON.parse(value) } as ClaimInput) : sampleClaimInput;
  } catch {
    return sampleClaimInput;
  }
}
