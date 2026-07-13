from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai_output_eval.catalog import ValueDefinition
from ai_output_eval.evaluators.aggregate import summarize_results
from ai_output_eval.evaluators.reducer import reduce_value_matrix, reduction_report
from ai_output_eval.evaluators.value_compare import compare_value_labels
from ai_output_eval.evaluators.value_labeler import label_values, value_matrix_rows
from ai_output_eval.io import write_csv, write_json, write_jsonl, write_text
from ai_output_eval.obsidian_export import build_obsidian_base, build_obsidian_note


def run_pipeline(
    *,
    cases: list[dict[str, Any]],
    eval_results: list[dict[str, Any]],
    catalog: list[ValueDefinition],
    out_dir: Path,
    title: str,
    source_url: str | None = None,
    components: int = 4,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    obsidian_dir = out_dir / "obsidian"

    paths = {
        "eval_jsonl": out_dir / "eval.jsonl",
        "summary_md": out_dir / "summary.md",
        "value_labels_jsonl": out_dir / "value-labels.jsonl",
        "value_matrix_csv": out_dir / "value-matrix.csv",
        "value_reduction_md": out_dir / "value-reduction.md",
        "value_reduction_json": out_dir / "value-reduction.json",
        "value_comparison_md": out_dir / "value-comparison.md",
        "obsidian_note_md": obsidian_dir / "value-profile-report.md",
        "obsidian_base": obsidian_dir / "value-profile-reports.base",
        "manifest_json": out_dir / "manifest.json",
    }

    value_labels = [label_values(case, catalog) for case in cases]
    matrix_columns, matrix_rows = value_matrix_rows(value_labels, catalog)
    reduction = reduce_value_matrix(value_labels, catalog, components=components)

    write_jsonl(paths["eval_jsonl"], eval_results)
    write_text(paths["summary_md"], summarize_results(eval_results))
    write_jsonl(paths["value_labels_jsonl"], value_labels)
    write_csv(paths["value_matrix_csv"], matrix_columns, matrix_rows)
    write_text(paths["value_reduction_md"], reduction_report(reduction))
    write_json(paths["value_reduction_json"], reduction)
    write_text(paths["value_comparison_md"], compare_value_labels(value_labels))
    write_text(
        paths["obsidian_note_md"],
        build_obsidian_note(
            title=title,
            summary_path=paths["summary_md"],
            comparison_path=paths["value_comparison_md"],
            reduction_path=paths["value_reduction_md"],
            source_url=source_url,
        ),
    )
    write_text(paths["obsidian_base"], build_obsidian_base())

    manifest = {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "title": title,
        "source_url": source_url or "",
        "cases": len(cases),
        "catalog_values": len(catalog),
        "components_requested": components,
        "outputs": {key: str(path) for key, path in paths.items() if key != "manifest_json"},
        "manifest": str(paths["manifest_json"]),
        "status": "ok",
    }
    write_json(paths["manifest_json"], manifest)
    return manifest
