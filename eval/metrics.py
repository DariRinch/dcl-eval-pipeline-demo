from dataclasses import dataclass
from typing import Optional

@dataclass
class EvalResult:
    prompt_id: str
    score: float
    passed: bool
    reason: Optional[str] = None

def score_consistency(response: str, expected_keywords: list) -> EvalResult:
    """Check if response contains expected keywords."""
    matches = sum(1 for kw in expected_keywords if kw.lower() in response.lower())
    score = matches / len(expected_keywords) if expected_keywords else 0.0
    return EvalResult(
        prompt_id="consistency_check",
        score=round(score, 2),
        passed=score >= 0.7,
        reason=f"Matched {matches}/{len(expected_keywords)} keywords"
    )

def score_length(response: str, min_len: int = 50, max_len: int = 1000) -> EvalResult:
    """Check if response length is within expected range."""
    length = len(response)
    passed = min_len <= length <= max_len
    score = 1.0 if passed else 0.0
    return EvalResult(
        prompt_id="length_check",
        score=score,
        passed=passed,
        reason=f"Response length: {length} chars"
    )

def score_anomaly(response: str, forbidden_patterns: list) -> EvalResult:
    """Detect anomalous patterns in agent response."""
    found = [p for p in forbidden_patterns if p.lower() in response.lower()]
    score = 1.0 if not found else 0.0
    return EvalResult(
        prompt_id="anomaly_check",
        score=score,
        passed=not found,
        reason=f"Anomalies found: {found}" if found else "No anomalies detected"
    )