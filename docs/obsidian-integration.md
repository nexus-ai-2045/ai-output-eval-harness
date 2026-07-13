# Obsidian連携

## 方針

このリポジトリでは、Obsidian vaultへ直接書き込む前に、まずvault-readyなMarkdownを生成する。

理由:

- リポ単体で再現できる
- Git管理しやすい
- vaultの場所や命名規則に依存しない
- 公開/共有境界を越えない

## コマンド

```powershell
python -m ai_output_eval obsidian-export `
  --title "Value Profile Report" `
  --summary reports/summary.md `
  --comparison reports/value-comparison.md `
  --reduction reports/value-reduction.md `
  --out reports/obsidian/value-profile-report.md
```

vaultへ直接置く場合:

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

生成されるMarkdownには、Obsidian用のfrontmatter、タグ、callout、各レポート本文が含まれる。

vaultに取り込む場合は、生成ファイルをvault配下へ移すか、Obsidian CLIが使える環境で `obsidian create` などに渡す。
