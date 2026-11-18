from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any

from ai_output_eval.formatting import markdown_inline


GROUP_FIELDS = ("model", "language", "task_type")
AXIS_FIELDS = ("deference_vs_caution", "warmth_vs_rigor", "depth_vs_brevity", "candor_vs_execution")


def compare_value_labels(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Value Profile Comparison",
        "",
        f"- cases: {len(rows)}",
        "",
    ]
    for group_field in GROUP_FIELDS:
        lines.extend(_group_section(rows, group_field))
    return "\n".join(lines) + "\n"


def _group_section(rows: list[dict[str, Any]], group_field: str) -> list[str]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(group_field, "") or "(blank)")].append(row)

    lines = [f"## By {group_field}", ""]
    lines.append("| group | cases | deference_vs_caution | warmth_vs_rigor | depth_vs_brevity | candor_vs_execution | top values |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for group, group_rows in sorted(groups.items()):
        axis_means = {
            axis: mean(float(row.get("axis_scores", {}).get(axis, 0.0)) for row in group_rows)
            for axis in AXIS_FIELDS
        }
        top_values = _top_values(group_rows)
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_inline(group),
                    str(len(group_rows)),
                    f"{axis_means['deference_vs_caution']:.3f}",
                    f"{axis_means['warmth_vs_rigor']:.3f}",
                    f"{axis_means['depth_vs_brevity']:.3f}",
                    f"{axis_means['candor_vs_execution']:.3f}",
                    ", ".join(markdown_inline(value_id) for value_id in top_values) if top_values else "-",
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def _top_values(rows: list[dict[str, Any]], limit: int = 5) -> list[str]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        for value_id in row.get("value_ids", []):
            counts[str(value_id)] += 1
    return [value_id for value_id, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]]

