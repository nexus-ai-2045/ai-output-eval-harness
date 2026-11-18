from __future__ import annotations

from statistics import mean
from typing import Any

from ai_output_eval.formatting import markdown_inline


def summarize_results(rows: list[dict[str, Any]]) -> str:
    total = len(rows)
    if total == 0:
        return "# AI Output Eval Summary\n\nNo rows.\n"

    schema_pass = sum(1 for row in rows if row.get("schema_valid") is True)
    unsupported_total = sum(len(row.get("unsupported_claims", [])) for row in rows)
    missing_total = sum(len(row.get("missing_required_fields", [])) for row in rows)
    low_conf_total = sum(len(row.get("low_confidence_fields", [])) for row in rows)
    accuracy = mean(float(row.get("field_accuracy", 0.0)) for row in rows)

    lines = [
        "# AI Output Eval Summary",
        "",
        f"- cases: {total}",
        f"- schema pass: {schema_pass}/{total}",
        f"- average field accuracy: {accuracy:.3f}",
        f"- unsupported claims: {unsupported_total}",
        f"- missing required fields: {missing_total}",
        f"- low confidence fields: {low_conf_total}",
        "",
        "## Failures",
        "",
    ]

    failures = [
        row
        for row in rows
        if row.get("schema_valid") is not True
        or row.get("unsupported_claims")
        or row.get("missing_required_fields")
        or row.get("field_accuracy", 1.0) < 1.0
    ]
    if not failures:
        lines.append("No failures.")
    else:
        for row in failures:
            lines.append(
                f"- {markdown_inline(row.get('case_id', ''))}: "
                f"accuracy={row.get('field_accuracy')}, unsupported={len(row.get('unsupported_claims', []))}"
            )

    return "\n".join(lines) + "\n"

