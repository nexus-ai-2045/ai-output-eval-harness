from ai_output_eval.catalog import load_catalog
from ai_output_eval.evaluators.value_labeler import label_values, value_matrix_rows


def test_label_values_detects_multiple_catalog_values():
    catalog = load_catalog()
    result = label_values(
        {
            "case_id": "case-001",
            "model": "strict-model",
            "language": "ja",
            "task_type": "review",
            "output": "根拠を確認し、正確に検証します。ただしリスクがあります。",
        },
        catalog,
    )

    assert {"transparency", "accuracy", "caution"}.issubset(set(result["value_ids"]))
    assert result["axis_scores"]["warmth_vs_rigor"] < 0
    assert result["axis_scores"]["deference_vs_caution"] < 0


def test_value_matrix_rows_emits_case_by_value_columns():
    catalog = load_catalog()
    labels = [
        {
            "case_id": "case-001",
            "model": "m",
            "language": "ja",
            "task_type": "review",
            "value_ids": ["accuracy", "caution"],
        }
    ]

    columns, rows = value_matrix_rows(labels, catalog)

    assert columns[:4] == ["case_id", "model", "language", "task_type"]
    assert "accuracy" in columns
    assert rows[0]["accuracy"] == 1
    assert rows[0]["encouragement"] == 0
