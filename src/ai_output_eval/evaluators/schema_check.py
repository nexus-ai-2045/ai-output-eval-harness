from __future__ import annotations

from typing import Any


def check_case_schema(case: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not isinstance(case.get("case_id"), str) or not case.get("case_id"):
        errors.append("case_id")
    if "output" not in case:
        errors.append("output")
    if "confidence" in case and not isinstance(case["confidence"], dict):
        errors.append("confidence")
    if "evidence" in case:
        evidence = case["evidence"]
        if not isinstance(evidence, list) or not all(isinstance(item, str) for item in evidence):
            errors.append("evidence")
    return not errors, errors

