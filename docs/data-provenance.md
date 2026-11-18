# データ由来と利用条件

## 同梱サンプル

`examples/sample-output.jsonl` は動作確認用の合成データです。実在する会話、請求書、人物、組織、model出力を収録していません。

## 価値観カタログ

`catalogs/values_catalog.json` は、このrepositoryで管理する小規模なルールベース評価用カタログです。一般的な概念と日本語・英語の検索語を使っており、Anthropic研究の3,307 values、339 high-level values、会話データを収録していません。

カタログは心理測定尺度や標準化された分類体系ではありません。出力傾向を探索するための初期ルールであり、品質、文化的妥当性、網羅性を保証しません。

## 参考研究

- [Claude’s values across models and languages](https://www.anthropic.com/research/claude-values-models-languages)
- [Values in the wild](https://www.anthropic.com/research/values-wild)

参考研究へのリンクは、研究方法との違いを説明するためのものです。このrepositoryがAnthropicの公式実装または公式データ配布物であることを意味しません。

## 利用者が追加するデータ

実在する会話や評価データを追加する場合は、利用権、個人情報、機密情報、保存期間を利用者自身で確認してください。非公開データと生成レポートはcommitしないでください。
