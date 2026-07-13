# 価値姿勢の軸

このリポジトリでは、AI出力の姿勢をラベル化し、比較用の軸スコアに変換します。

## 軸

| 軸 | 正方向 | 負方向 |
| --- | --- | --- |
| deference_vs_caution | deference | caution |
| warmth_vs_rigor | warmth | rigor |
| depth_vs_brevity | depth | brevity |
| candor_vs_execution | candor | execution |

## 初期実装の考え方

MVPでは、軸スコアは完全な心理測定ではありません。ローカル評価を始めるための粗いメタ指標です。

- 根拠なし主張がある場合、cautionとrigorを下げる
- 期待値不一致がある場合、rigorを下げる
- 低confidenceや不明表現がある場合、candorを上げる
- 出力が短く、必要項目を満たす場合、brevityとexecutionを上げる

この定義は、プロジェクトごとの評価方針に合わせて調整できます。

