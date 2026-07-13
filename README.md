# ai-output-eval-harness

AIの出力を、正誤だけでなく「根拠」「慎重さ」「厳密さ」「率直さ」まで含めてローカルで評価するための最小ハーネスです。

## 目的

このリポジトリは、AI出力を次の観点でJSONLとして評価・集計します。

- schema validity: 出力JSONが期待スキーマに合っているか
- unsupported claims: 根拠にない主張が出ていないか
- field accuracy: 期待値と抽出値が一致しているか
- value posture: 回答姿勢が慎重・厳密・率直に扱えているか
- axes: 価値姿勢を比較しやすい軸スコアに変換する

## 最小CLI

初回だけ、ローカル編集可能インストールを行います。

```powershell
python -m pip install -e .
```

```powershell
python -m ai_output_eval run --input examples/sample-output.jsonl --out reports/eval.jsonl
python -m ai_output_eval summarize --input reports/eval.jsonl --out reports/summary.md
```

## 入力形式

1行1ケースのJSONLです。詳しくは [docs/evaluation-schema.md](docs/evaluation-schema.md) を参照してください。

```json
{
  "case_id": "case-001",
  "model": "example-model",
  "language": "ja",
  "task_type": "document_extraction",
  "output": {"invoice_id": "INV-001", "total": "1200"},
  "expected": {"invoice_id": "INV-001", "total": "1200"},
  "evidence": ["INV-001", "1200"],
  "confidence": {"invoice_id": 0.98, "total": 0.96}
}
```

## 現在のスコープ

MVPでは、ローカルで再現可能な決定的チェックを優先します。

- スキーマチェック
- 期待値とのフィールド一致
- 文字列根拠に基づくunsupported claim検出
- confidenceと空欄/不明表現に基づく姿勢ラベル
- Markdown集計

LLM judgeや外部モデル評価は、後続で追加します。
