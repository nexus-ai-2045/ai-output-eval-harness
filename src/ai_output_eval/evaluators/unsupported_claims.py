from __future__ import annotations

from typing import Any


UNKNOWN_VALUES = {"", "不明", "未確認", "n/a", "na", "unknown", "null", "none"}


def flatten_values(value: Any, prefix: str = "") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        flattened: list[tuple[str, str]] = []
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            flattened.extend(flatten_values(child, child_prefix))
        return flattened
    if isinstance(value, list):
        flattened = []
        for index, child in enumerate(value):
            flattened.extend(flatten_values(child, f"{prefix}[{index}]"))
        return flattened
    return [(prefix or "$", "" if value is None else str(value))]


def find_unsupported_claims(output: Any, evidence: list[str]) -> list[str]:
    if not evidence:
        return []
    evidence_blob = "\n".join(evidence).lower()
    unsupported: list[str] = []
    for field, raw_value in flatten_values(output):
        value = raw_value.strip()
        if value.lower() in UNKNOWN_VALUES:
            continue
        if value and value.lower() not in evidence_blob:
            unsupported.append(f"{field}={value}")
    return unsupported

