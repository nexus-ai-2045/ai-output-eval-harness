from __future__ import annotations

from math import sqrt
from typing import Any

from ai_output_eval.catalog import ValueDefinition


def reduce_value_matrix(
    labels: list[dict[str, Any]],
    catalog: list[ValueDefinition],
    *,
    components: int = 4,
    iterations: int = 80,
) -> dict[str, Any]:
    value_ids = [value.id for value in catalog]
    matrix = _binary_matrix(labels, value_ids)
    if not matrix:
        return {"cases": 0, "values": len(value_ids), "components": []}

    centered, means = _center_columns(matrix)
    covariance = _covariance(centered)
    extracted: list[dict[str, Any]] = []
    working = [row[:] for row in covariance]

    max_components = min(components, len(value_ids))
    for index in range(max_components):
        vector = _power_iteration(working, iterations=iterations)
        eigenvalue = _quadratic_form(working, vector)
        if abs(eigenvalue) < 1e-12:
            break
        loadings = [
            {
                "value_id": value_id,
                "loading": round(vector[column_index], 6),
                "mean_presence": round(means[column_index], 6),
            }
            for column_index, value_id in enumerate(value_ids)
        ]
        loadings.sort(key=lambda item: (-abs(float(item["loading"])), item["value_id"]))
        extracted.append(
            {
                "component": index + 1,
                "eigenvalue": round(eigenvalue, 6),
                "top_loadings": loadings[: min(10, len(loadings))],
            }
        )
        _deflate(working, eigenvalue, vector)

    return {
        "cases": len(labels),
        "values": len(value_ids),
        "components": extracted,
    }


def reduction_report(result: dict[str, Any]) -> str:
    lines = [
        "# Value Matrix Reduction",
        "",
        f"- cases: {result.get('cases', 0)}",
        f"- values: {result.get('values', 0)}",
        "",
    ]
    components = result.get("components", [])
    if not components:
        lines.append("No components extracted.")
        return "\n".join(lines) + "\n"

    for component in components:
        lines.extend(
            [
                f"## Component {component['component']}",
                "",
                f"- eigenvalue: {component['eigenvalue']}",
                "",
                "| value | loading | mean presence |",
                "| --- | ---: | ---: |",
            ]
        )
        for loading in component["top_loadings"]:
            lines.append(
                f"| {loading['value_id']} | {loading['loading']:.6f} | {loading['mean_presence']:.6f} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def _binary_matrix(labels: list[dict[str, Any]], value_ids: list[str]) -> list[list[float]]:
    rows: list[list[float]] = []
    for label in labels:
        present = set(str(value_id) for value_id in label.get("value_ids", []))
        rows.append([1.0 if value_id in present else 0.0 for value_id in value_ids])
    return rows


def _center_columns(matrix: list[list[float]]) -> tuple[list[list[float]], list[float]]:
    row_count = len(matrix)
    column_count = len(matrix[0]) if matrix else 0
    means = [sum(row[column] for row in matrix) / row_count for column in range(column_count)]
    centered = [[row[column] - means[column] for column in range(column_count)] for row in matrix]
    return centered, means


def _covariance(centered: list[list[float]]) -> list[list[float]]:
    row_count = len(centered)
    column_count = len(centered[0]) if centered else 0
    denom = max(1, row_count - 1)
    covariance = [[0.0 for _ in range(column_count)] for _ in range(column_count)]
    for i in range(column_count):
        for j in range(i, column_count):
            value = sum(row[i] * row[j] for row in centered) / denom
            covariance[i][j] = value
            covariance[j][i] = value
    return covariance


def _power_iteration(matrix: list[list[float]], *, iterations: int) -> list[float]:
    size = len(matrix)
    seed = [float(index + 1) for index in range(size)]
    seed_norm = sqrt(sum(value * value for value in seed))
    vector = [value / seed_norm for value in seed]
    for _ in range(iterations):
        next_vector = _matvec(matrix, vector)
        norm = sqrt(sum(value * value for value in next_vector))
        if norm < 1e-12:
            return vector
        vector = [value / norm for value in next_vector]
    return vector


def _matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[index] * vector[index] for index in range(len(vector))) for row in matrix]


def _quadratic_form(matrix: list[list[float]], vector: list[float]) -> float:
    multiplied = _matvec(matrix, vector)
    return sum(vector[index] * multiplied[index] for index in range(len(vector)))


def _deflate(matrix: list[list[float]], eigenvalue: float, vector: list[float]) -> None:
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] -= eigenvalue * vector[i] * vector[j]
