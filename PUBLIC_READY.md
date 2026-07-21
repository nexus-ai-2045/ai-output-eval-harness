# 公開準備状況

## 現在の判定

`local_checks_passed / blocked_github_ci_and_visibility_approval`

実装、ローカル検証、公開内容の人間レビューは完了しています。公開先のアカウント、private repositoryの操作履歴、組織内の承認記録はこの公開候補から分離し、管理側の非公開台帳で扱います。

## 確認済み

- [x] README、MIT License、SECURITY.md、CONTRIBUTING.md
- [x] Python 3.11 / 3.13用CI定義
- [x] regression tests: `22 passed`
- [x] editable install
- [x] pipeline smoke test
- [x] generated reportsをGit管理対象から除外
- [x] secret pattern scan
- [x] personal path scan
- [x] dependency vulnerability scan: known vulnerabilityなし
- [x] sample dataと価値観カタログの再配布レビュー
- [x] commit historyの公開用identityレビュー
- [x] README、source、tests、sample dataの人間レビュー
- [x] repo operating contract check、hook未有効化

## 公開前に必要な確認

- [ ] 現在の対象HEADでGitHub Actionsが成功している
- [ ] repository固有のpublic visibility変更が承認されている

## 公開時に見えるもの

source、tests、schema、sample data、価値観カタログ、ドキュメント、全commit履歴、commit author情報がWebから見えるようになります。

## 未完了項目

現在差分のGitHub Actions成功とrepository固有の明示承認が完了するまで、visibility変更、release、告知、外部共有を行いません。
