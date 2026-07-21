# ai-output-eval-harness

Current version: `0.1.0`

AI出力のJSONLをローカルで読み込み、基本指標を集計してMarkdown・JSON・CSVへ出力する小さな評価ハーネスです。

Anthropicの[価値観分析研究](https://www.anthropic.com/research/claude-values-models-languages)を参考に、出力に表れる傾向を `present/absent` ラベル、ケース x 価値観行列、軸スコア、比較レポートとして扱える形を目指しています。このrepositoryは研究データや公式実装の複製ではありません。

## コアMVP

- JSONL入力から評価結果を生成する
- 期待値との一致率を出す
- 根拠にない主張を検出する
- 低confidenceフィールドを検出する
- 評価結果をJSONL、集計をMarkdown、行列をCSVで保存する
- 必須フィールドとJSONL形式を最小限検証する

高度な次元削減、監視、公開自動化はコアMVPの対象外です。価値観分析とObsidian出力は実験的な拡張として同梱しています。

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

まず評価と集計を実行します。

```powershell
python -m ai_output_eval run --input examples/sample-output.jsonl --out reports/eval.jsonl
python -m ai_output_eval summarize --input reports/eval.jsonl --out reports/summary.md
```

価値観ラベルをCSV行列へ出す最小例です。

```powershell
python -m ai_output_eval label-values --input examples/sample-output.jsonl --out reports/value-labels.jsonl
python -m ai_output_eval matrix --input reports/value-labels.jsonl --out reports/value-matrix.csv
```

## 生成物

上のコアコマンドは次の成果物を生成します。

```text
reports/
  eval.jsonl
  summary.md
  value-labels.jsonl
  value-matrix.csv
```

`pipeline` コマンドを使うと、これらに加えて実験的な比較・次元削減・Obsidian向け出力と `manifest.json` を一括生成できます。

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

## 入力と出力の制約

- 1行は1つのJSON objectでなければなりません。
- `case_id` と `output` は必須です。`evidence` は文字列の配列、`confidence` はobjectとして検証します。
- CSVの文字列セルが `=`, `+`, `-`, `@` で始まる場合、表計算ソフトで式として実行されないよう先頭に `'` を付けます。
- Markdownへ埋め込む識別子のパイプと改行は、表や見出しを壊さないようエスケープします。
- 入力サイズとネスト深度には固定上限を設けていません。信頼できない巨大入力は、OSや実行環境側でメモリ・時間を制限してください。

## コマンド一覧

正誤・根拠チェック:

```powershell
python -m ai_output_eval run --input examples/sample-output.jsonl --out reports/eval.jsonl
python -m ai_output_eval summarize --input reports/eval.jsonl --out reports/summary.md
```

価値観ラベルと行列:

```powershell
python -m ai_output_eval label-values --input examples/sample-output.jsonl --out reports/value-labels.jsonl
python -m ai_output_eval matrix --input reports/value-labels.jsonl --out reports/value-matrix.csv
```

実験的な成分抽出と比較:

```powershell
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

同梱カタログは、このrepositoryで管理する小規模なルールセットです。Anthropic研究の339 valuesや会話データは収録していません。サンプルとカタログの扱いは [データ由来と利用条件](docs/data-provenance.md) を参照してください。

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

コアMVPはローカルで動作します。

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
- [データ由来と利用条件](docs/data-provenance.md)
- [Versioning](docs/versioning.md)

## Contributing / Security

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)

## 公開前の確認

公開やreleaseの前には [docs/public-readiness.md](docs/public-readiness.md) を確認してください。自動検査だけで公開可否を判断せず、公開されるファイルとcommit履歴を人が目視確認します。

`repo-operating-contracts` v0.4.2のmanaged bundleを試験導入しています。hookは配置のみで、install / enableしていません。bundle整合性は `python .repo-operating-contracts\check.py` で確認できます。
