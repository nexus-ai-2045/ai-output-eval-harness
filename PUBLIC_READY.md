# 公開準備状況

## 測定メタデータ

- `schema_version`: `fact-provenance/v1`
- `recorded_at`: `2026-07-26T10:51:07+09:00`
- `recorded_by`: `codex`
- `source`: GitHub API、GitHub Actions、GitHub ruleset API、GitHub未ログイン状態でのHTTPアクセス、ローカルGit
- `actor`: `nexus-ai-2045`、GitHub Actions、`codex`
- `event_time`: `2026-07-26T10:35:34+09:00`から`2026-07-26T10:50:55+09:00`
- `observed_at`: `2026-07-26T10:51:07+09:00`
- `scope`: `nexus-ai-2045/ai-output-eval-harness` v0.1.0

## 現在の判定

`public / v0.1.0_released / main_ruleset_active`

2026-07-26（日本時間）にv0.1.0をリリースしました。tagは公開mainの`a0cd421`を指し、GitHub ReleaseはGitHub未ログイン状態から閲覧できることを確認しています。

## 確認済み

- [x] README、MITライセンス、SECURITY.md、CONTRIBUTING.md
- [x] Python 3.11 / 3.13用CI定義
- [x] 回帰テスト、日本語文書ゲート、CI権限ゲート: `27 passed`
- [x] actionlint v1.7.12（配布物のSHA-256を照合）
- [x] wheelのビルドと隔離環境へのインストール
- [x] wheelから導入した`ai-eval`のCLI簡易動作確認
- [x] 編集可能形式でのインストール
- [x] パイプラインの簡易動作確認
- [x] 生成レポートをGit管理対象から除外
- [x] 機密情報パターン検査
- [x] 個人環境パス検査
- [x] 依存関係の脆弱性検査: 既知の脆弱性なし
- [x] サンプルデータと価値観カタログの再配布レビュー
- [x] コミット履歴の公開用識別情報レビュー
- [x] README、ソース、テスト、サンプルデータの人間レビュー
- [x] リポジトリ運用契約検査、フック未有効化
- [x] 現在の公開HEAD `a0cd421` のGitHub Actions成功
- [x] リポジトリの可視性: `PUBLIC`
- [x] GitHub未ログイン状態から閲覧可能: リポジトリ、README、LICENSE、SECURITY.md、PUBLIC_READY.mdでHTTP 200

## 公開後に必要な確認

- [x] CodeQLの既定設定
- [x] 脆弱性アラート／Dependabotセキュリティ更新
- [x] 機密情報スキャン／push protection
- [x] CodeQL open alert: `0`
- [x] `main-pr-and-ci` ruleset（PR、CI最新化、5チェック、削除／force push禁止、bypassなし）

## 公開時に見えるもの

現在、ソース、テスト、スキーマ、サンプルデータ、価値観カタログ、ドキュメント、全コミット履歴、コミット作成者情報、`v0.1.0`tag、リリース名、リリースノートがWebから見えます。

## 未完了項目

追加リリース、告知、外部共有、branch削除は、それぞれ正確な操作を提示して明示承認を得るまで行いません。
