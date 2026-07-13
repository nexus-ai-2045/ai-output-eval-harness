from pathlib import Path

from ai_output_eval.cli import main


def test_value_profile_cli_pipeline(tmp_path: Path):
    labels_path = tmp_path / "labels.jsonl"
    matrix_path = tmp_path / "matrix.csv"
    compare_path = tmp_path / "compare.md"

    assert main(["label-values", "--input", "examples/sample-output.jsonl", "--out", str(labels_path)]) == 0
    assert labels_path.exists()

    assert main(["matrix", "--input", str(labels_path), "--out", str(matrix_path)]) == 0
    matrix = matrix_path.read_text(encoding="utf-8")
    assert "case_id,model,language,task_type" in matrix
    assert "accuracy" in matrix

    reduction_path = tmp_path / "reduction.md"
    assert main(["reduce", "--input", str(labels_path), "--out", str(reduction_path)]) == 0
    reduction = reduction_path.read_text(encoding="utf-8")
    assert "Value Matrix Reduction" in reduction

    assert main(["compare", "--input", str(labels_path), "--out", str(compare_path)]) == 0
    compare = compare_path.read_text(encoding="utf-8")
    assert "Value Profile Comparison" in compare
    assert "By model" in compare
