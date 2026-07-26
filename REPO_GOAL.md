# リポジトリの目標

リポジトリ: ai-output-eval-harness
所有者: nexus-ai-2045
現在の目標: コアMVPのv0.1.0リリース候補を人間レビュー可能な状態にする

## 完了レイヤー

- ローカル実装: コアMVPと出力注入対策、`repo-operating-contracts` v0.4.2の管理対象ファイル一式を配置
- ローカル検証: `27 passed`、日本語文書ゲート `3 passed`、actionlint成功、wheel build成功、wheel導入後のCLI smoke成功、依存関係監査で脆弱性なし、利用側契約検査 `ok`
- ブランチ／コミット: `codex/release-v0.1.0-readiness`に未コミットのリリース候補
- push／PR: リリース候補は未push、PR未作成
- merge／外部状態: リポジトリはpublic。公開HEADは`11f4f278`、v0.1.0のtagとGitHub Releaseは未作成
- 後片付け: 専用worktreeを維持
- 無関係な未コミット変更: なし

## 停止線

- 公開: 現在会話での人間レビューと明示承認まで停止
- リポジトリの可視性: リポジトリ単位の明示承認まで変更しない
- 外部送信／投稿／コメント: 明示承認まで停止
- フック／自動化: 配置のみ。インストール／有効化は明示承認まで停止
- 認証／機密情報／本番設定: 明示承認まで変更しない

## 根拠

- Git状態: 公開済み`main`と同期した専用ブランチで作業
- 変更ファイル: CI、README、公開準備文書、リリースノート、リリースメタデータテスト
- 検証: pytest、actionlint、wheel build、CLI smoke、利用側契約検査、依存関係監査、gitleaks、個人パス検査
- 実行済みの外部操作: このリリース候補についてはなし
- 残存リスク: 人間レビュー、PR上のCI、branch protection、merge、tag、GitHub Releaseは未完了
