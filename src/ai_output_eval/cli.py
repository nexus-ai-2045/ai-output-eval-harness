from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .evaluators.aggregate import summarize_results
from .evaluators.posture_labeler import (
    axes_from_labels,
    field_accuracy,
    label_posture,
    low_confidence_fields,
    missing_required_fields,
)
from .evaluators.schema_check import check_case_schema
from .evaluators.unsupported_claims import find_unsupported_claims
from .io import read_jsonl, write_jsonl, write_text


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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))

