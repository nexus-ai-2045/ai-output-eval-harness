# 公開準備状況

最終ローカル確認日: 2026-07-16

## 判定

`private-ready / public-pending-human-review`

実装とローカル検証は公開候補としてレビューできる状態です。GitHub repository作成、push、公開範囲変更、告知、外部共有は実行していません。

## 確認済み

- README: 用途、導入、実行例、制約を記載
- License: MIT
- Security policy: あり
- Contribution guide: あり
- CI: Python 3.11 / 3.13でpackageとtest依存を導入してpytestを実行
- Test: `20 passed`
- Editable install: 成功
- Pipeline smoke: 成功
- Secret pattern scan: 検出なし
- Personal path scan: 検出なし
- Generated reports: `.gitignore`対象

## 人間レビューが必要な項目

- 公開先候補を `nexus-ai-2045/ai-output-eval-harness` としてよいか
- repositoryを最初からpublicで作るか、privateで作成して最終確認後にpublicへ変更するか
- 既存commit historyの作者名・メールアドレスをWeb公開してよいか
- 日本語中心のREADMEで公開してよいか
- サンプルデータと価値観カタログを再配布してよいか
- GitHub Security Advisoriesを有効化するか
- GitHubのみで公開し、現時点ではPyPI公開を行わない方針でよいか

## 公開操作の停止線

対象repository、公開されるファイルとcommit history、実行する正確なコマンドを提示し、現在会話で明示承認を得るまで、repository作成、push、visibility変更、release、告知を行いません。
