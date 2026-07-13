import json
from pathlib import Path

from ai_output_eval.cli import main


def test_pipeline_writes_full_report_bundle(tmp_path: Path):
    out_dir = tmp_path / "bundle"

    assert main(["pipeline", "--input", "examples/sample-output.jsonl", "--out-dir", str(out_dir)]) == 0

    expected_files = [
        "eval.jsonl",
        "summary.md",
        "value-labels.jsonl",
        "value-matrix.csv",
        "value-reduction.md",
        "value-reduction.json",
        "value-comparison.md",
        "obsidian/value-profile-report.md",
        "obsidian/value-profile-reports.base",
        "manifest.json",
    ]
    for relative_path in expected_files:
        assert (out_dir / relative_path).exists(), relative_path

    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "ok"
    assert manifest["cases"] == 3
    assert manifest["catalog_values"] >= 10

