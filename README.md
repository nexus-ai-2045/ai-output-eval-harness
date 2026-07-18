# ai-output-eval-harness

Current version: `0.1.0`

AI出力を、正誤だけでなく「根拠」「慎重さ」「厳密さ」「率直さ」「価値観ラベル」まで含めてローカル評価するためのハーネスです。

Anthropic の価値観分析記事のように、出力に表れる傾向を `present/absent` ラベル、ケース x 価値観行列、軸スコア、比較レポートとして扱える形を目指しています。

## できること

- JSONL入力から評価結果を生成する
- 期待値との一致率を出す
- 根拠にない主張を検出する
- 低confidenceフィールドを検出する
- 価値観カタログで出力を複数ラベル化する
- ケース x 価値観 のCSV行列を作る
- 行列からデータ駆動の成分を抽出する
- `model` / `language` / `task_type` 別に比較する
- Obsidian向けMarkdownとBases indexを生成する
- 全工程を `pipeline` で一括再生成する

## インストール

```powershell
python -m pip install -e .
```

Python 3.11以上を想定しています。現在のMVPは外部依存なしで動きます。

## クイックスタート

バージョン確認:

```powershell
python -m ai_output_eval version
```

全工程を一括実行します。

```powershell
python -m ai_output_eval pipeline `
  --input examples/sample-output.jsonl `
  --out-dir reports/full `
  --title "Value Profile Report"
```

同じ出力先を上書きする場合は `--force` を付けます。

```powershell
python -m ai_output_eval pipeline `
  --input examples/sample-output.jsonl `
  --out-dir reports/full `
  --title "Value Profile Report" `
  --force
```

## 生成物

`pipeline` は次の成果物を生成します。

```text
reports/full/
  eval.jsonl
  summary.md
  value-labels.jsonl
  value-matrix.csv
  value-reduction.md
  value-reduction.json
  value-comparison.md
  manifest.json
  obsidian/
    value-profile-report.md
    value-profile-reports.base
```

`manifest.json` には、生成時刻、入力件数、カタログ件数、生成ファイル一覧が記録されます。

## 入力JSONL

1行1ケースです。

```json
{
  "case_id": "case-001",
  "model": "example-model",
  "language": "ja",
  "task_type": "document_extraction",
  "prompt": "請求書から値を抽出してください。",
  "output": {"invoice_id": "INV-001", "total": "1200"},
  "expected": {"invoice_id": "INV-001", "total": "1200"},
  "evidence": ["INV-001", "1200"],
  "confidence": {"invoice_id": 0.98, "total": 0.96}
}
```

詳しくは [docs/evaluation-schema.md](docs/evaluation-schema.md) を参照してください。

## 個別コマンド

正誤・根拠チェック:

```powershell
python -m ai_output_eval run --input examples/sample-output.jsonl --out reports/eval.jsonl
python -m ai_output_eval summarize --input reports/eval.jsonl --out reports/summary.md
```

価値観ラベル、行列、成分抽出、比較:

```powershell
python -m ai_output_eval label-values --input examples/sample-output.jsonl --out reports/value-labels.jsonl
python -m ai_output_eval matrix --input reports/value-labels.jsonl --out reports/value-matrix.csv
python -m ai_output_eval reduce --input reports/value-labels.jsonl --out reports/value-reduction.md
python -m ai_output_eval compare --input reports/value-labels.jsonl --out reports/value-comparison.md
```

Obsidian向け出力:

```powershell
python -m ai_output_eval obsidian-export `
  --title "Value Profile Report" `
  --summary reports/summary.md `
  --comparison reports/value-comparison.md `
  --reduction reports/value-reduction.md `
  --out reports/obsidian/value-profile-report.md

python -m ai_output_eval obsidian-base --out reports/obsidian/value-profile-reports.base
```

vaultへ直接出す場合:

```powershell
python -m ai_output_eval obsidian-export `
  --title "Value Profile Report" `
  --summary reports/summary.md `
  --comparison reports/value-comparison.md `
  --reduction reports/value-reduction.md `
  --vault-dir "C:\path\to\vault" `
  --note-path "AI Eval/Value Profile Report.md"
```

## 価値観カタログ

価値観カタログは [catalogs/values_catalog.json](catalogs/values_catalog.json) にあります。

各valueは次を持ちます。

- `id`: 一意ID
- `label`: 英語ラベル
- `ja_label`: 日本語ラベル
- `cluster`: 上位クラスタ
- `axis`: 比較軸
- `pole`: 軸のどちら側に寄与するか
- `keywords`: ルールベース判定に使う語

カタログ読み込み時に、重複ID、不正なaxis/pole、空のkeywordsは拒否します。

## 現在の位置づけ

仕組みMVPは完成しています。

- 入力から全成果物を再生成できる
- 成果物manifestを残せる
- Obsidian用ノートを生成できる
- pytestで主要な回帰を固定している

まだ研究品質を厚くする余地があります。

- 日本語価値観カタログの拡張
- gold label datasetの作成
- LLM judgeの追加
- PCA/SVDなど標準ライブラリによる次元削減オプション
- 実データセットでの比較レポート

## テスト

```powershell
python -m pytest
```

GitHub Actions用のCI設定も含まれています。

## License

MIT License. See [LICENSE](LICENSE).

## ドキュメント

- [Repo goal](REPO_GOAL.md)
- [仕組み完成条件](docs/mechanism-completion.md)
- [Anthropic型ローカル再現ロードマップ](docs/anthropic-reproduction-roadmap.md)
- [次元削減](docs/dimensionality-reduction.md)
- [Obsidian連携](docs/obsidian-integration.md)
- [価値姿勢の軸](docs/value-posture-axes.md)
- [評価入出力スキーマ](docs/evaluation-schema.md)
- [公開準備チェック](docs/public-readiness.md)
- [Versioning](docs/versioning.md)

## Contributing / Security

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)

## 公開前の注意

このリポジトリはGitHub上にprivateで作成・初回push済みです。public visibilityへの変更、release、告知、外部共有はまだ行っていません。公開前には [docs/public-readiness.md](docs/public-readiness.md) を確認し、人間レビューと明示承認を得てください。

`repo-operating-contracts` v0.2.0のmanaged bundleを試験導入しています。hookは配置のみで、install / enableしていません。bundle整合性は `python .repo-operating-contracts\check.py` で確認できます。
