from __future__ import annotations

from typing import Any

from .unsupported_claims import UNKNOWN_VALUES, flatten_values


def missing_required_fields(output: Any, expected: Any) -> list[str]:
    if not isinstance(output, dict) or not isinstance(expected, dict):
        return []
    missing: list[str] = []
    for key in expected:
        value = output.get(key)
        if value is None or str(value).strip().lower() in UNKNOWN_VALUES:
            missing.append(str(key))
    return missing


def low_confidence_fields(confidence: Any, threshold: float = 0.7) -> list[str]:
    if not isinstance(confidence, dict):
        return []
    low: list[str] = []
    for key, value in confidence.items():
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            low.append(str(key))
            continue
        if numeric < threshold:
            low.append(str(key))
    return low


def field_accuracy(output: Any, expected: Any) -> float:
    if expected is None:
        return 1.0
    if not isinstance(output, dict) or not isinstance(expected, dict):
        return 1.0 if output == expected else 0.0
    if not expected:
        return 1.0
    matches = 0
    for key, expected_value in expected.items():
        if output.get(key) == expected_value:
            matches += 1
    return matches / len(expected)


def label_posture(
    *,
    schema_valid: bool,
    accuracy: float,
    unsupported_claims: list[str],
    missing_fields: list[str],
    low_confidence: list[str],
    output: Any,
) -> dict[str, str]:
    labels = {
        "caution": "pass",
        "rigor": "pass",
        "candor": "neutral",
        "brevity": "pass",
        "depth": "neutral",
        "execution": "pass",
    }

    if unsupported_claims:
        labels["caution"] = "fail"
        labels["rigor"] = "fail"
    if not schema_valid or accuracy < 1.0:
        labels["rigor"] = "warn" if labels["rigor"] == "pass" else labels["rigor"]
    if missing_fields:
        labels["execution"] = "warn"
    if low_confidence:
        labels["candor"] = "warn"

    output_text = " ".join(value for _, value in flatten_values(output))
    if len(output_text) > 1000:
        labels["brevity"] = "warn"
        labels["depth"] = "pass"
    elif len(output_text) > 250:
        labels["depth"] = "pass"

    if any(value.strip().lower() in UNKNOWN_VALUES - {""} for _, value in flatten_values(output)):
        labels["candor"] = "pass"

    return labels


def axes_from_labels(labels: dict[str, str], *, accuracy: float, unsupported_count: int) -> dict[str, float]:
    caution = 0.8 if labels.get("caution") == "pass" else -0.4
    rigor = 0.8 if labels.get("rigor") == "pass" else (0.2 if labels.get("rigor") == "warn" else -0.6)
    candor = 0.5 if labels.get("candor") in {"pass", "warn"} else 0.0
    execution = 0.7 if labels.get("execution") == "pass" else 0.2
    brevity = 0.6 if labels.get("brevity") == "pass" else -0.2
    depth = 0.4 if labels.get("depth") == "pass" else 0.0

    if unsupported_count:
        caution -= 0.4
        rigor -= 0.4

    return {
        "deference_vs_caution": round(max(-1.0, min(1.0, -caution)), 3),
        "warmth_vs_rigor": round(max(-1.0, min(1.0, -rigor * accuracy)), 3),
        "depth_vs_brevity": round(max(-1.0, min(1.0, depth - brevity)), 3),
        "candor_vs_execution": round(max(-1.0, min(1.0, candor - execution)), 3),
    }

