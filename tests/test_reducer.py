from ai_output_eval.catalog import load_catalog
from ai_output_eval.evaluators.reducer import reduce_value_matrix, reduction_report


def test_reduce_value_matrix_extracts_components():
    catalog = load_catalog()
    labels = [
        {"case_id": "a", "value_ids": ["accuracy", "precision", "caution"]},
        {"case_id": "b", "value_ids": ["accuracy", "transparency", "caution"]},
        {"case_id": "c", "value_ids": ["encouragement", "empathy", "respect_preferences"]},
        {"case_id": "d", "value_ids": ["encouragement", "brevity", "respect_preferences"]},
    ]

    result = reduce_value_matrix(labels, catalog, components=2)

    assert result["cases"] == 4
    assert result["values"] == len(catalog)
    assert result["components"]
    report = reduction_report(result)
    assert "Value Matrix Reduction" in report
    assert "Component 1" in report

