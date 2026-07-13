# 評価入出力スキーマ

## 入力JSONL

各行は1ケースです。

| field | required | description |
| --- | --- | --- |
| case_id | yes | ケースID |
| model | no | モデル名 |
| language | no | 言語 |
| task_type | no | タスク種別 |
| output | yes | AI出力。JSON objectまたは文字列 |
| expected | no | 期待値。JSON objectまたは文字列 |
| evidence | no | 根拠文字列の配列 |
| confidence | no | フィールド別confidence |

## 出力JSONL

```json
{
  "case_id": "case-001",
  "schema_valid": true,
  "field_accuracy": 1.0,
  "unsupported_claims": [],
  "missing_required_fields": [],
  "low_confidence_fields": [],
  "posture_labels": {
    "caution": "pass",
    "rigor": "pass",
    "candor": "pass",
    "brevity": "pass",
    "depth": "neutral",
    "execution": "pass"
  },
  "axes": {
    "deference_vs_caution": -0.5,
    "warmth_vs_rigor": -0.5,
    "depth_vs_brevity": -0.2,
    "candor_vs_execution": -0.2
  }
}
```

