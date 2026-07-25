# ai-output-eval-harness

AI出力のJSONLをローカルで評価し、結果をJSONL・Markdown・CSVで保存するコマンドラインツールです。外部APIは使いません。

- 期待値との一致率
- 根拠にない出力
- 信頼度（`confidence`）の低い項目

現在のバージョン: `0.1.0` · Python 3.11以上 · MITライセンス

## 最短実行

```powershell
python -m pip install -e .
python -m ai_output_eval run --input examples/sample-output.jsonl --out reports/eval.jsonl
python -m ai_output_eval summarize --input reports/eval.jsonl --out reports/summary.md
```

| ファイル | 内容 |
| --- | --- |
| `reports/eval.jsonl` | ケース別の評価結果 |
| `reports/summary.md` | 基本指標の集計 |

## 入力

入力は1行1ケースのJSONLです。必須フィールドは `case_id` と `output` です。

```json
{
  "case_id": "case-001",
  "output": {"invoice_id": "INV-001", "total": "1200"},
  "expected": {"invoice_id": "INV-001", "total": "1200"},
  "evidence": ["INV-001", "1200"],
  "confidence": {"invoice_id": 0.98, "total": 0.96}
}
```

全フィールドの定義は [評価入出力スキーマ](docs/evaluation-schema.md) を参照してください。

## 価値観ラベル

同梱カタログによる実験的なルールベース判定です。

```powershell
python -m ai_output_eval label-values --input examples/sample-output.jsonl --out reports/value-labels.jsonl
python -m ai_output_eval matrix --input reports/value-labels.jsonl --out reports/value-matrix.csv
```

このリポジトリはAnthropicの研究データや公式実装の複製ではありません。由来と制約は [データ由来と利用条件](docs/data-provenance.md) に記載しています。

## Obsidian連携は任意

コア評価にObsidianは不要です。生成したレポートをObsidianの保管庫で読みたい場合だけ使用します。

1. [Obsidian公式サイト](https://obsidian.md/download)からアプリをインストールする
2. Obsidianで保管庫を作成または開く
3. `obsidian-export` に保管庫のパスを渡す

詳しい手順とコマンド例は [Obsidian連携](docs/obsidian-integration.md) を参照してください。

## 制約

- 1行は1つのJSONオブジェクトでなければなりません。
- CSVの数式注入とMarkdownの構造崩れを防ぐエスケープを行います。
- 入力サイズとネスト深度には固定上限がありません。信頼できない巨大入力には、実行環境側でメモリ・時間制限を設けてください。
- 価値観ラベルは研究品質のLLM評価器や正解ラベルデータセットを使用していません。

## 開発と確認

```powershell
python -m pytest -q
python .repo-operating-contracts\check.py
```

- [コントリビューションガイド](CONTRIBUTING.md)
- [セキュリティポリシー](SECURITY.md)
- [公開準備チェック](docs/public-readiness.md)
- [その他のドキュメント](docs/)

## ライセンス

[MITライセンス](LICENSE)
