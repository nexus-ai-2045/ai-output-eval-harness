# Obsidian連携

## 方針

Obsidianは任意です。コア評価、JSONL出力、Markdown集計、CSV行列の生成には必要ありません。

Obsidianを使う場合も、保管庫へ直接書き込む前に、まず取り込み可能なMarkdownを生成します。

理由:

- リポ単体で再現できる
- Git管理しやすい
- 保管庫の場所や命名規則に依存しない
- 公開/共有境界を越えない

## インストール

1. [Obsidian公式ダウンロードページ](https://obsidian.md/download)を開く
2. Windowsでは「Universal」、macOSでは「Universal」、Linuxでは利用環境に合う形式を選ぶ
3. ダウンロードしたインストーラーを実行する
4. Obsidianを起動し、「新しい保管庫を作成」または「保管庫としてフォルダーを開く」を選ぶ

公式の詳しい説明は [Obsidianのインストール手順](https://obsidian.md/help/install) を参照してください。

## コマンド

```powershell
python -m ai_output_eval obsidian-export `
  --title "Value Profile Report" `
  --summary reports/summary.md `
  --comparison reports/value-comparison.md `
  --reduction reports/value-reduction.md `
  --out reports/obsidian/value-profile-report.md
```

保管庫へ直接置く場合:

```powershell
python -m ai_output_eval obsidian-export `
  --title "Value Profile Report" `
  --summary reports/summary.md `
  --comparison reports/value-comparison.md `
  --reduction reports/value-reduction.md `
  --vault-dir "C:\path\to\vault" `
  --note-path "AI Eval/Value Profile Report.md"
```

Obsidian Bases用の一覧ファイルを作る場合:

```powershell
python -m ai_output_eval obsidian-base `
  --vault-dir "C:\path\to\vault" `
  --note-path "Bases/Value Profile Reports.base"
```

Obsidian CLIで作る場合は、生成済みMarkdownを読んで `obsidian create` に渡す。

```powershell
obsidian create name="AI Eval/Value Profile Report" content="$(Get-Content reports/obsidian/value-profile-report.md -Raw)" silent
```

## 出力

生成されるMarkdownには、Obsidian用のフロントマター、タグ、コールアウト、各レポート本文が含まれます。

保管庫に取り込む場合は、生成ファイルを保管庫配下へ移すか、Obsidian CLIが使える環境で `obsidian create` などに渡します。
