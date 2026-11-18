from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .catalog import load_catalog
from .evaluators.aggregate import summarize_results
from .evaluators.posture_labeler import (
    axes_from_labels,
    field_accuracy,
    label_posture,
    low_confidence_fields,
    missing_required_fields,
)
from .evaluators.reducer import reduce_value_matrix, reduction_report
from .evaluators.schema_check import check_case_schema
from .evaluators.unsupported_claims import find_unsupported_claims
from .evaluators.value_compare import compare_value_labels
from .evaluators.value_labeler import label_values, value_matrix_rows
from .io import read_jsonl, write_csv, write_jsonl, write_text
from .obsidian_export import build_obsidian_base, build_obsidian_note, resolve_obsidian_output
from .pipeline import run_pipeline
from .version import get_version


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    schema_valid, schema_errors = check_case_schema(case)
    output = case.get("output")
    expected = case.get("expected")
    evidence = case.get("evidence", [])

    accuracy = field_accuracy(output, expected)
    unsupported = find_unsupported_claims(output, evidence)
    missing = sorted(set(schema_errors + missing_required_fields(output, expected)))
    low_conf = low_confidence_fields(case.get("confidence"))
    labels = label_posture(
        schema_valid=schema_valid,
        accuracy=accuracy,
        unsupported_claims=unsupported,
        missing_fields=missing,
        low_confidence=low_conf,
        output=output,
    )

    return {
        "case_id": str(case.get("case_id", "")),
        "model": case.get("model", ""),
        "language": case.get("language", ""),
        "task_type": case.get("task_type", ""),
        "schema_valid": schema_valid,
        "field_accuracy": round(accuracy, 6),
        "unsupported_claims": unsupported,
        "missing_required_fields": missing,
        "low_confidence_fields": low_conf,
        "posture_labels": labels,
        "axes": axes_from_labels(labels, accuracy=accuracy, unsupported_count=len(unsupported)),
    }


def run_command(args: argparse.Namespace) -> int:
    cases = read_jsonl(Path(args.input))
    results = [evaluate_case(case) for case in cases]
    write_jsonl(Path(args.out), results)
    return 0


def summarize_command(args: argparse.Namespace) -> int:
    rows = read_jsonl(Path(args.input))
    write_text(Path(args.out), summarize_results(rows))
    return 0


def label_values_command(args: argparse.Namespace) -> int:
    cases = read_jsonl(Path(args.input))
    catalog = load_catalog(Path(args.catalog) if args.catalog else None)
    labels = [label_values(case, catalog) for case in cases]
    write_jsonl(Path(args.out), labels)
    return 0


def matrix_command(args: argparse.Namespace) -> int:
    labels = read_jsonl(Path(args.input))
    catalog = load_catalog(Path(args.catalog) if args.catalog else None)
    columns, rows = value_matrix_rows(labels, catalog)
    write_csv(Path(args.out), columns, rows)
    return 0


def compare_command(args: argparse.Namespace) -> int:
    labels = read_jsonl(Path(args.input))
    write_text(Path(args.out), compare_value_labels(labels))
    return 0


def reduce_command(args: argparse.Namespace) -> int:
    labels = read_jsonl(Path(args.input))
    catalog = load_catalog(Path(args.catalog) if args.catalog else None)
    result = reduce_value_matrix(labels, catalog, components=args.components)
    write_text(Path(args.out), reduction_report(result))
    return 0


def obsidian_export_command(args: argparse.Namespace) -> int:
    note = build_obsidian_note(
        title=args.title,
        summary_path=Path(args.summary) if args.summary else None,
        comparison_path=Path(args.comparison) if args.comparison else None,
        reduction_path=Path(args.reduction) if args.reduction else None,
        source_url=args.source_url,
    )
    out = resolve_obsidian_output(
        out=Path(args.out) if args.out else None,
        vault_dir=Path(args.vault_dir) if args.vault_dir else None,
        note_path=args.note_path,
    )
    write_text(out, note)
    return 0


def obsidian_base_command(args: argparse.Namespace) -> int:
    out = resolve_obsidian_output(
        out=Path(args.out) if args.out else None,
        vault_dir=Path(args.vault_dir) if args.vault_dir else None,
        note_path=args.note_path,
    )
    if out.suffix.lower() != ".base":
        out = out.with_suffix(".base")
    write_text(out, build_obsidian_base())
    return 0


def pipeline_command(args: argparse.Namespace) -> int:
    cases = read_jsonl(Path(args.input))
    catalog = load_catalog(Path(args.catalog) if args.catalog else None)
    eval_results = [evaluate_case(case) for case in cases]
    manifest = run_pipeline(
        cases=cases,
        eval_results=eval_results,
        catalog=catalog,
        out_dir=Path(args.out_dir),
        title=args.title,
        source_url=args.source_url,
        components=args.components,
        force=args.force,
    )
    print(f"wrote pipeline manifest: {manifest['manifest']}")
    return 0


def version_command(args: argparse.Namespace) -> int:
    print(get_version())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-eval")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="evaluate JSONL cases")
    run_parser.add_argument("--input", required=True, help="input JSONL path")
    run_parser.add_argument("--out", required=True, help="output JSONL path")
    run_parser.set_defaults(func=run_command)

    summary_parser = subparsers.add_parser("summarize", help="write a Markdown summary")
    summary_parser.add_argument("--input", required=True, help="evaluation JSONL path")
    summary_parser.add_argument("--out", required=True, help="summary Markdown path")
    summary_parser.set_defaults(func=summarize_command)

    label_parser = subparsers.add_parser("label-values", help="label outputs with value catalog")
    label_parser.add_argument("--input", required=True, help="input JSONL path")
    label_parser.add_argument("--out", required=True, help="value labels JSONL path")
    label_parser.add_argument("--catalog", help="value catalog JSON path")
    label_parser.set_defaults(func=label_values_command)

    matrix_parser = subparsers.add_parser("matrix", help="write case x value matrix CSV")
    matrix_parser.add_argument("--input", required=True, help="value labels JSONL path")
    matrix_parser.add_argument("--out", required=True, help="matrix CSV path")
    matrix_parser.add_argument("--catalog", help="value catalog JSON path")
    matrix_parser.set_defaults(func=matrix_command)

    reduce_parser = subparsers.add_parser("reduce", help="extract data-driven components from value labels")
    reduce_parser.add_argument("--input", required=True, help="value labels JSONL path")
    reduce_parser.add_argument("--out", required=True, help="reduction Markdown path")
    reduce_parser.add_argument("--catalog", help="value catalog JSON path")
    reduce_parser.add_argument("--components", type=int, default=4, help="number of components to extract")
    reduce_parser.set_defaults(func=reduce_command)

    compare_parser = subparsers.add_parser("compare", help="write value profile comparison Markdown")
    compare_parser.add_argument("--input", required=True, help="value labels JSONL path")
    compare_parser.add_argument("--out", required=True, help="comparison Markdown path")
    compare_parser.set_defaults(func=compare_command)

    obsidian_parser = subparsers.add_parser("obsidian-export", help="write an Obsidian-ready Markdown note")
    obsidian_parser.add_argument("--title", required=True, help="note title")
    obsidian_parser.add_argument("--out", help="output Markdown path")
    obsidian_parser.add_argument("--vault-dir", help="Obsidian vault directory")
    obsidian_parser.add_argument("--note-path", help="note path inside vault, for example Reports/value-profile.md")
    obsidian_parser.add_argument("--summary", help="summary Markdown path")
    obsidian_parser.add_argument("--comparison", help="comparison Markdown path")
    obsidian_parser.add_argument("--reduction", help="reduction Markdown path")
    obsidian_parser.add_argument("--source-url", help="source article URL")
    obsidian_parser.set_defaults(func=obsidian_export_command)

    base_parser = subparsers.add_parser("obsidian-base", help="write an Obsidian Bases index for generated reports")
    base_parser.add_argument("--out", help="output .base path")
    base_parser.add_argument("--vault-dir", help="Obsidian vault directory")
    base_parser.add_argument("--note-path", help="base path inside vault, for example Bases/value-profile-reports.base")
    base_parser.set_defaults(func=obsidian_base_command)

    pipeline_parser = subparsers.add_parser("pipeline", help="run the full local reproduction pipeline")
    pipeline_parser.add_argument("--input", required=True, help="input JSONL path")
    pipeline_parser.add_argument("--out-dir", required=True, help="directory for all generated reports")
    pipeline_parser.add_argument("--title", default="Value Profile Report", help="Obsidian note/report title")
    pipeline_parser.add_argument("--catalog", help="value catalog JSON path")
    pipeline_parser.add_argument("--components", type=int, default=4, help="number of reduction components to extract")
    pipeline_parser.add_argument("--source-url", help="source article URL")
    pipeline_parser.add_argument("--force", action="store_true", help="overwrite an existing pipeline manifest")
    pipeline_parser.set_defaults(func=pipeline_command)

    version_parser = subparsers.add_parser("version", help="print package version")
    version_parser.set_defaults(func=version_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
