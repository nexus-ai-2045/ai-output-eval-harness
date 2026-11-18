import json
from pathlib import Path

import pytest

import ai_output_eval
from ai_output_eval.catalog import DEFAULT_CATALOG_PATH, load_catalog


def test_catalog_rejects_duplicate_ids(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps(
            {
                "values": [
                    {
                        "id": "same",
                        "label": "A",
                        "ja_label": "A",
                        "cluster": "rigor",
                        "axis": "warmth_vs_rigor",
                        "pole": "rigor",
                        "keywords": ["a"],
                    },
                    {
                        "id": "same",
                        "label": "B",
                        "ja_label": "B",
                        "cluster": "warmth",
                        "axis": "warmth_vs_rigor",
                        "pole": "warmth",
                        "keywords": ["b"],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    try:
        load_catalog(path)
    except ValueError as exc:
        assert "duplicate value ids" in str(exc)
    else:
        raise AssertionError("expected duplicate ids to fail")


def test_catalog_rejects_invalid_axis_pole_pair(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps(
            {
                "values": [
                    {
                        "id": "bad",
                        "label": "Bad",
                        "ja_label": "Bad",
                        "cluster": "rigor",
                        "axis": "warmth_vs_rigor",
                        "pole": "caution",
                        "keywords": ["bad"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    try:
        load_catalog(path)
    except ValueError as exc:
        assert "pole caution is invalid" in str(exc)
    else:
        raise AssertionError("expected invalid axis/pole pair to fail")


def test_default_catalog_is_shipped_inside_the_package():
    package_root = Path(ai_output_eval.__file__).resolve().parent

    assert DEFAULT_CATALOG_PATH.is_relative_to(package_root)
    assert load_catalog()


def test_catalog_rejects_reserved_value_ids(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps(
            {
                "values": [
                    {
                        "id": "model",
                        "label": "A",
                        "ja_label": "A",
                        "cluster": "rigor",
                        "axis": "warmth_vs_rigor",
                        "pole": "rigor",
                        "keywords": ["a"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="reserved value ids"):
        load_catalog(path)
