from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CATALOG_PATH = Path(__file__).resolve().parents[2] / "catalogs" / "values_catalog.json"


@dataclass(frozen=True)
class ValueDefinition:
    id: str
    label: str
    ja_label: str
    cluster: str
    axis: str
    pole: str
    keywords: tuple[str, ...]


def load_catalog(path: Path | None = None) -> list[ValueDefinition]:
    catalog_path = path or DEFAULT_CATALOG_PATH
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    values = raw.get("values")
    if not isinstance(values, list):
        raise ValueError(f"{catalog_path}: values must be a list")
    return [_parse_value_definition(item, catalog_path) for item in values]


def _parse_value_definition(item: Any, catalog_path: Path) -> ValueDefinition:
    if not isinstance(item, dict):
        raise ValueError(f"{catalog_path}: each value definition must be an object")
    required = ["id", "label", "ja_label", "cluster", "axis", "pole", "keywords"]
    missing = [key for key in required if key not in item]
    if missing:
        raise ValueError(f"{catalog_path}: missing fields: {', '.join(missing)}")
    keywords = item["keywords"]
    if not isinstance(keywords, list) or not all(isinstance(keyword, str) for keyword in keywords):
        raise ValueError(f"{catalog_path}: keywords must be a string list")
    return ValueDefinition(
        id=str(item["id"]),
        label=str(item["label"]),
        ja_label=str(item["ja_label"]),
        cluster=str(item["cluster"]),
        axis=str(item["axis"]),
        pole=str(item["pole"]),
        keywords=tuple(keyword.lower() for keyword in keywords),
    )

