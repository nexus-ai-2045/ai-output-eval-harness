# リポジトリの目標

リポジトリ: ai-output-eval-harness
所有者: nexus-ai-2045
現在の目標: コアMVPのv0.1.0リリースを完了し、公開状態を正本へ反映する

## 測定メタデータ

- `schema_version`: `fact-provenance/v1`
- `recorded_at`: `2026-07-26T10:41:44+09:00`
- `recorded_by`: `codex`
- `source`: GitHub API、GitHub Actions、GitHub未ログイン状態でのHTTPアクセス、ローカルGit
- `actor`: `nexus-ai-2045`、GitHub Actions、`codex`
- `event_time`: `2026-07-26T10:35:34+09:00`から`2026-07-26T10:40:24+09:00`
- `observed_at`: `2026-07-26T10:41:44+09:00`
- `scope`: `nexus-ai-2045/ai-output-eval-harness` v0.1.0

## 完了レイヤー

- ローカル実装: コアMVPと出力注入対策、`repo-operating-contracts` v0.4.2の管理対象ファイル一式を配置
- ローカル検証: `27 passed`、日本語文書ゲート `3 passed`、actionlint成功、wheel build成功、wheel導入後のCLI smoke成功、依存関係監査で脆弱性なし、利用側契約検査 `ok`
- ブランチ／コミット: PR #2をrebase mergeし、公開mainは`a0cd421`
- push／PR: PR #2のCIとCodeQLが成功し、merge済み
- merge／外部状態: `v0.1.0`tagとGitHub Releaseを公開し、GitHub未ログイン状態から閲覧可能
- 後片付け: 専用worktreeを維持
- 無関係な未コミット変更: なし

## 停止線

- 公開: 現在会話での人間レビューと明示承認まで停止
- リポジトリの可視性: リポジトリ単位の明示承認まで変更しない
- 外部送信／投稿／コメント: 明示承認まで停止
- フック／自動化: 配置のみ。インストール／有効化は明示承認まで停止
- 認証／機密情報／本番設定: 明示承認まで変更しない

## 根拠

- Git状態: 公開済み`main`と同期したcloseoutブランチで作業
- 変更ファイル: 公開準備文書とREPO_GOALのリリース後状態
- 検証: pytest、actionlint、wheel build、CLI smoke、利用側契約検査、依存関係監査、gitleaks、個人パス検査
- 実行済みの外部操作: PR #2のrebase merge、`v0.1.0`tag push、GitHub Release公開
- 残存リスク: branch protection、作業branchの削除、告知、フック／実行時スキルのインストールは未完了
