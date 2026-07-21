import csv
from pathlib import Path

from ai_output_eval.evaluators.aggregate import summarize_results
from ai_output_eval.evaluators.reducer import reduction_report
from ai_output_eval.evaluators.value_compare import compare_value_labels
from ai_output_eval.io import write_csv


def test_write_csv_neutralizes_spreadsheet_formulas(tmp_path: Path):
    output = tmp_path / "report.csv"

    write_csv(
        output,
        ["equals", "plus", "minus", "at", "safe", "number"],
        [
            {
                "equals": "=1+1",
                "plus": "+cmd",
                "minus": "-2+3",
                "at": "@SUM(A1:A2)",
                "safe": "plain text",
                "number": 42,
            }
        ],
    )

    with output.open(encoding="utf-8", newline="") as fh:
        row = next(csv.DictReader(fh))

    assert row == {
        "equals": "'=1+1",
        "plus": "'+cmd",
        "minus": "'-2+3",
        "at": "'@SUM(A1:A2)",
        "safe": "plain text",
        "number": "42",
    }


def test_markdown_reports_escape_table_and_line_break_injection():
    comparison = compare_value_labels(
        [
            {
                "model": "model|name\n## injected",
                "language": "ja",
                "task_type": "test",
                "axis_scores": {},
                "value_ids": ["value|id\n- injected"],
            }
        ]
    )
    summary = summarize_results(
        [
            {
                "case_id": "case|id\n## injected",
                "schema_valid": False,
                "field_accuracy": 0.0,
                "unsupported_claims": [],
                "missing_required_fields": [],
                "low_confidence_fields": [],
            }
        ]
    )
    reduction = reduction_report(
        {
            "cases": 1,
            "values": 1,
            "components": [
                {
                    "component": 1,
                    "eigenvalue": 1.0,
                    "top_loadings": [
                        {"value_id": "value|id\n## injected", "loading": 1.0, "mean_presence": 1.0}
                    ],
                }
            ],
        }
    )

    assert "model\\|name<br>## injected" in comparison
    assert "value\\|id<br>- injected" in comparison
    assert "case\\|id<br>## injected" in summary
    assert "value\\|id<br>## injected" in reduction
    assert "model|name\n## injected" not in comparison
    assert "case|id\n## injected" not in summary
