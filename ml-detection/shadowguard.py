
import re
import joblib

#  LOAD MODEL + VECTORIZER 
model = joblib.load('shadowguard_xgb_model.pkl')
vectorizer = joblib.load('shadowguard_tfidf_vectorizer.pkl')

THRESHOLD = 0.3087

#  SIGNAL PATTERNS 
signal_patterns = {
    "instruction_override": r"ignore (all |the )?(previous |above |prior )?instructions",
    "role_override": r"you are now|act as|pretend (to be|you are)",
    "system_prompt_extraction": r"(reveal|show|print|output).{0,20}(system prompt|instructions|rules)",
    "credential_extraction": r"(password|api[_\s]?key|secret|token|credentials)",
    "disregard_phrase": r"disregard (the|all|above)",
    "jailbreak_persona": r"\bDAN\b|do anything now|no restrictions|unfiltered"
}

repo_signal_patterns = {
    "ai_targeting_comment": r"(ai[- ]?(agent|assistant)s?[,:]|note to ai)",
    "security_downgrade": r"disable[_\s]?auth|debug_mode\s*=\s*true|verify\s*=\s*false|ssl_verify\s*=\s*false",
    "exfiltration_url": r"exfiltrate|send.{0,20}(to|url)|http[s]?://\S+",
    "destructive_command": r"rm -rf|drop table|delete from",
    "credential_read_instruction": r"\.env|api[_\s]?key|secret|token"
}

ambiguous_reference_patterns = {
    "unstated_context_reference": r"(as (we )?discussed|like before|earlier|standard (procedure|process)|as (mentioned|agreed))",
    "unverifiable_credential_claim": r"(credentials|password|token|key) (i gave you|you have|from before|already have)",
    "vague_override_reference": r"(override|special|admin) (procedure|process|mode)(?!.{0,20}(disable|weaken|bypass))"
}

action_risk_patterns = {
    "destructive_file_operation": r"rm\s+-rf|del\s+/[sf]|format\s+[a-z]:",
    "broad_scope_deletion": r"rm\s+-rf\s+(\.\/|\/|\*|~)",
    "force_push_to_main": r"push\s+(-f|--force).{0,20}(main|master)",
    "database_destructive": r"drop\s+table|delete\s+from\s+\w+(\s+where\s+1\s*=\s*1)?|truncate\s+table",
    "secret_in_output_payload": r"api[_\s]?key|password|secret|token|\.env",
    "public_channel_post": r"post.{0,20}(#general|public|channel)|send.{0,20}(slack|email).{0,20}(all|everyone|public)",
    "disable_security": r"disable[_\s]?auth|--no-verify|skip[_\s]?verification"
}

CATEGORY_NAMES = {
    "prompt": "prompt_injection",
    "repo_risk": "repo_risk",
    "unsafe_agent_action": "unsafe_agent_action"
}

#  SIGNAL FINDERS 
def find_signals(text):
    signals_found, evidence_items = [], []
    text_lower = text.lower()
    for signal_name, pattern in signal_patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            signals_found.append(signal_name)
            evidence_items.append({"pattern": match.group(0), "signal_type": signal_name})
    return signals_found, evidence_items

def find_signals_extended(text):
    combined_patterns = {**signal_patterns, **repo_signal_patterns}
    signals_found, evidence_items = [], []
    text_lower = text.lower()
    for signal_name, pattern in combined_patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            signals_found.append(signal_name)
            evidence_items.append({"pattern": match.group(0), "signal_type": signal_name})
    return signals_found, evidence_items

def find_ambiguous_signals(text):
    matches = []
    text_lower = text.lower()
    for signal_name, pattern in ambiguous_reference_patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            matches.append((signal_name, match.group(0)))
    return matches

def check_action_safety(planned_action_command, output_payload=""):
    combined_text = f"{planned_action_command} {output_payload}".lower()
    findings, evidence_items = [], []
    for risk_type, pattern in action_risk_patterns.items():
        match = re.search(pattern, combined_text)
        if match:
            findings.append(risk_type)
            evidence_items.append({"planned_action": planned_action_command, "matched_pattern": match.group(0), "risk_type": risk_type})
    return findings, evidence_items

#  OUTPUT HELPERS 
def get_risk_level(risk_score):
    if risk_score >= 0.75:
        return "high"
    elif risk_score >= 0.4:
        return "medium"
    return "low"

def compute_confidence(proba, threshold, signals_found):
    distance = abs(proba - threshold)
    base_confidence = min(0.5 + distance, 0.99)
    if len(signals_found) >= 2:
        base_confidence = min(base_confidence + 0.1, 0.99)
    return round(base_confidence, 4)

def simplify_output(case_id, category, input_text, claim, signals_found, risk_score, verdict, reason, confidence, expected_label=None):
    return {
        "case_id": case_id, "category": category, "input": input_text, "claim": claim,
        "signals_found": signals_found, "risk_score": risk_score, "risk_level": get_risk_level(risk_score),
        "verdict": verdict, "expected_label": expected_label, "missing_evidence": verdict == "uncertain",
        "confidence": confidence, "reason": reason
    }

#  MAIN ANALYZER FUNCTIONS 
def analyze_prompt(text, case_id=None, expected_label=None, threshold=THRESHOLD):
    vec = vectorizer.transform([text])
    proba = float(model.predict_proba(vec)[0][1])
    signals_found, _ = find_signals(text)
    ambiguous_matches = find_ambiguous_signals(text)
    model_says_attack = proba >= threshold
    is_ambiguous = len(ambiguous_matches) > 0 and len(signals_found) < 2
    is_borderline = 0.25 <= proba <= 0.45

    if not model_says_attack and (is_borderline or is_ambiguous) and len(signals_found) < 2:
        verdict = "uncertain"
        reason = "Input references unverifiable prior context or is borderline confidence; insufficient evidence to determine intent."
        if ambiguous_matches:
            reason += f" Ambiguous reference(s): {chr(44).join(m[1] for m in ambiguous_matches)}."
        signals_found = signals_found + [m[0] for m in ambiguous_matches]
    elif model_says_attack:
        verdict = "attack"
        reason = f"Model flagged this as an attack (score={proba:.2f})"
        reason += f", supported by matched pattern(s): {chr(44).join(signals_found)}." if signals_found else ", though no explicit rule-based pattern matched."
    elif len(signals_found) >= 2:
        verdict = "attack"
        reason = f"Model score ({proba:.2f}) was below threshold, but {len(signals_found)} explicit attack pattern(s) matched."
    else:
        verdict = "benign"
        reason = "Model score is below the attack threshold and no attack patterns were found."

    confidence = compute_confidence(proba, threshold, signals_found)
    return simplify_output(case_id, CATEGORY_NAMES["prompt"], text,
        "Is this input a prompt injection or manipulation attempt?",
        signals_found, round(proba, 4), verdict, reason, confidence, expected_label)

def analyze_repo_content(text, case_id=None, expected_label=None, threshold=THRESHOLD):
    vec = vectorizer.transform([text])
    proba = float(model.predict_proba(vec)[0][1])
    signals_found, _ = find_signals_extended(text)
    model_says_attack = proba >= threshold

    if model_says_attack or len(signals_found) >= 1:
        verdict = "attack"
        reason = f"Repo content flagged (model score={proba:.2f})"
        reason += f", matched pattern(s): {chr(44).join(signals_found)}." if signals_found else ""
    else:
        verdict = "benign"
        reason = "Model score below threshold, no repo-risk patterns matched."

    confidence = compute_confidence(proba, threshold, signals_found)
    return simplify_output(case_id, CATEGORY_NAMES["repo_risk"], text,
        "Does the repo content contain an indirect prompt injection targeting the agent?",
        signals_found, round(proba, 4), verdict, reason, confidence, expected_label)

def analyze_agent_action(planned_action_command, output_payload="", case_id=None, expected_label=None):
    findings, _ = check_action_safety(planned_action_command, output_payload)
    if findings:
        verdict = "unsafe_action"
        risk_score = min(0.7 + 0.1 * len(findings), 0.98)
        reason = f"Planned action matched {len(findings)} risk pattern(s)."
        confidence = 0.9
    else:
        verdict = "safe_action"
        risk_score = 0.05
        reason = "Planned action did not match any known unsafe action patterns."
        confidence = 0.95

    return simplify_output(case_id, CATEGORY_NAMES["unsafe_agent_action"], planned_action_command,
        "Is the agent about to take an unsafe or destructive action?",
        findings, round(risk_score, 4), verdict, reason, confidence, expected_label)

# ============ ROUTER ============
def shadowguard_analyze(input_type, **kwargs):
    if input_type == "prompt":
        return analyze_prompt(kwargs["text"], case_id=kwargs.get("case_id"), expected_label=kwargs.get("expected_label"))
    elif input_type == "repo_content":
        return analyze_repo_content(kwargs["text"], case_id=kwargs.get("case_id"), expected_label=kwargs.get("expected_label"))
    elif input_type == "agent_action":
        return analyze_agent_action(kwargs["planned_action_command"], kwargs.get("output_payload", ""), case_id=kwargs.get("case_id"), expected_label=kwargs.get("expected_label"))
    else:
        raise ValueError(f"Unknown input_type: {input_type}")
