from ai_output_eval.catalog import ValueDefinition, load_catalog
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



def test_reduce_value_matrix_retries_when_seed_is_orthogonal_to_variance():
    catalog = [
        ValueDefinition(
            id=value_id,
            label=value_id,
            ja_label=value_id,
            cluster="rigor",
            axis="warmth_vs_rigor",
            pole="rigor",
            keywords=(value_id,),
        )
        for value_id in ("a", "b", "c")
    ]
    labels = [
        {"case_id": f"case-{index}", "value_ids": ["a", "b"] if index % 2 == 0 else ["c"]}
        for index in range(20)
    ]

    result = reduce_value_matrix(labels, catalog, components=1)

    assert result["components"]


def test_reduce_value_matrix_returns_the_dominant_component_first():
    catalog = [
        ValueDefinition(
            id=value_id,
            label=value_id,
            ja_label=value_id,
            cluster="rigor",
            axis="warmth_vs_rigor",
            pole="rigor",
            keywords=(value_id,),
        )
        for value_id in ("a", "b", "c")
    ]
    patterns = [
        [value_id for bit, value_id in zip((first, second, third), ("a", "b", "c")) if bit]
        for first in (0, 1)
        for second in (0, 1)
        for third in (0, 1)
    ]
    value_sets = patterns + patterns + [["a", "b"], ["c"]]
    labels = [{"case_id": f"case-{index}", "value_ids": value_ids} for index, value_ids in enumerate(value_sets)]

    result = reduce_value_matrix(labels, catalog, components=1)

    component = result["components"][0]
    loadings = {item["value_id"]: item["loading"] for item in component["top_loadings"]}
    assert component["eigenvalue"] > 0.3
    assert loadings["a"] * loadings["b"] > 0
    assert loadings["a"] * loadings["c"] < 0
