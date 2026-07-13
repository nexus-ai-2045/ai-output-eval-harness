from pathlib import Path

from ai_output_eval.cli import main


def test_cli_run_and_summarize(tmp_path: Path):
    eval_path = tmp_path / "eval.jsonl"
    summary_path = tmp_path / "summary.md"

    assert main(["run", "--input", "examples/sample-output.jsonl", "--out", str(eval_path)]) == 0
    assert eval_path.exists()

    assert main(["summarize", "--input", str(eval_path), "--out", str(summary_path)]) == 0
    summary = summary_path.read_text(encoding="utf-8")
    assert "AI Output Eval Summary" in summary
    assert "cases: 3" in summary
