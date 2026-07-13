from __future__ import annotations

from collections import defaultdict
from typing import Any

from ai_output_eval.catalog import ValueDefinition
from ai_output_eval.evaluators.unsupported_claims import flatten_values


AXES = (
    "deference_vs_caution",
    "warmth_vs_rigor",
    "depth_vs_brevity",
    "candor_vs_execution",
)


def case_text(case: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("prompt", "input", "output", "rationale", "notes"):
        if key in case:
            parts.extend(value for _, value in flatten_values(case[key]))
    return "\n".join(parts).lower()


def label_values(case: dict[str, Any], catalog: list[ValueDefinition]) -> dict[str, Any]:
    text = case_text(case)
    present_values: list[dict[str, Any]] = []
    cluster_counts: dict[str, int] = defaultdict(int)
    pole_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for value in catalog:
        matched = sorted({keyword for keyword in value.keywords if keyword and keyword in text})
        if not matched:
            continue
        present_values.append(
            {
                "id": value.id,
                "label": value.label,
                "ja_label": value.ja_label,
                "cluster": value.cluster,
                "axis": value.axis,
                "pole": value.pole,
                "matched_keywords": matched,
            }
        )
        cluster_counts[value.cluster] += 1
        pole_counts[value.axis][value.pole] += 1

    return {
        "case_id": str(case.get("case_id", "")),
        "model": case.get("model", ""),
        "language": case.get("language", ""),
        "task_type": case.get("task_type", ""),
        "present_values": present_values,
        "value_ids": [value["id"] for value in present_values],
        "cluster_counts": dict(sorted(cluster_counts.items())),
        "axis_scores": axis_scores(pole_counts),
    }


def axis_scores(pole_counts: dict[str, dict[str, int]]) -> dict[str, float]:
    scores: dict[str, float] = {}
    pole_pairs = {
        "deference_vs_caution": ("deference", "caution"),
        "warmth_vs_rigor": ("warmth", "rigor"),
        "depth_vs_brevity": ("depth", "brevity"),
        "candor_vs_execution": ("candor", "execution"),
    }
    for axis, (positive, negative) in pole_pairs.items():
        counts = pole_counts.get(axis, {})
        pos_count = int(counts.get(positive, 0))
        neg_count = int(counts.get(negative, 0))
        total = pos_count + neg_count
        scores[axis] = 0.0 if total == 0 else round((pos_count - neg_count) / total, 6)
    return scores


def value_matrix_rows(labels: list[dict[str, Any]], catalog: list[ValueDefinition]) -> tuple[list[str], list[dict[str, Any]]]:
    value_ids = [value.id for value in catalog]
    columns = ["case_id", "model", "language", "task_type", *value_ids]
    rows: list[dict[str, Any]] = []
    for row in labels:
        present = set(row.get("value_ids", []))
        matrix_row = {
            "case_id": row.get("case_id", ""),
            "model": row.get("model", ""),
            "language": row.get("language", ""),
            "task_type": row.get("task_type", ""),
        }
        for value_id in value_ids:
            matrix_row[value_id] = 1 if value_id in present else 0
        rows.append(matrix_row)
    return columns, rows

