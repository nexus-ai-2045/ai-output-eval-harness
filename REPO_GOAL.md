# リポジトリの目標

リポジトリ: ai-output-eval-harness
所有者: nexus-ai-2045
現在の目標: 公開済みAI出力評価ハーネスのセキュリティ設定と公開後検証を完了する

## 完了レイヤー

- ローカル実装: コアMVPと出力注入対策、`repo-operating-contracts` v0.4.2の管理対象ファイル一式を配置
- ローカル検証: `26 passed`、日本語文書ゲート `3 passed`、CI権限ゲート `1 passed`、依存関係監査で脆弱性なし、利用側契約検査 `ok`、Git識別情報 `matched`
- ブランチ／コミット: `main`に公開候補コミットを作成（`git log -1`を参照）
- push／PR: `main`へpush済み、GitHub Actions成功
- merge／外部状態: リポジトリはpublic、匿名Webアクセス確認済み
- 後片付け: 専用worktreeを維持
- 無関係な未コミット変更: なし

## 停止線

- 公開: 現在会話での人間レビューと明示承認まで停止
- リポジトリの可視性: リポジトリ単位の明示承認まで変更しない
- 外部送信／投稿／コメント: 明示承認まで停止
- フック／自動化: 配置のみ。インストール／有効化は明示承認まで停止
- 認証／機密情報／本番設定: 明示承認まで変更しない

## 根拠

- Git状態: `main`のローカル2コミットを起点に専用ブランチを作成
- 変更ファイル: `AGENTS.md`、`REPO_GOAL.md`、README、管理対象ファイル一式
- 検証: `python -m pytest -q`、`python .repo-operating-contracts\check.py`、Git識別情報検査
- 実行済みの外部操作: リポジトリの可視性を承認済み操作でpublicへ変更
- 残存リスク: CodeQLの再解析によるmediumアラート解消確認、branch protection、フック／実行時スキルのインストールは未完了
