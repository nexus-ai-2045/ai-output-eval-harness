# 仕組み完成条件

このリポジトリでいう「仕組み完成」は、価値観カタログの量や日本語教師データの充実ではなく、分析の流れが一貫して再実行できることを指す。

## 完成条件

- 入力JSONLから正誤評価を生成できる
- 入力JSONLから価値観ラベルを生成できる
- 価値観ラベルからケース x 価値観 行列を生成できる
- 行列からデータ駆動の成分抽出を実行できる
- model / language / task_type 別の比較レポートを生成できる
- Obsidian向けMarkdownとBases indexを生成できる
- 全成果物のmanifestを生成できる
- すべてを `pipeline` で一括再生成できる
- 上記をテストで保証している

## 現在の一括実行

```powershell
python -m ai_output_eval pipeline --input examples/sample-output.jsonl --out-dir reports/full --title "Value Profile Report"
```

## 現在の未完成領域

次は仕組みではなく、研究品質・公開品質の厚みを増やす作業である。

- 日本語価値観カタログの拡張
- gold label datasetの作成
- LLM judgeの追加
- 標準ライブラリによるPCA/SVDオプション
- 実データセットでの比較レポート
- CI、LICENSE、SECURITY.mdなど公開準備

