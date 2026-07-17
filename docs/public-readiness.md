# 公開準備チェック

このリポジトリをpublic化する前の確認リストです。

## 現在の状態

- ローカル実装: あり
- テスト: あり
- README: public向けに整理済み
- CI: pytest用GitHub Actionsあり
- SECURITY.md: あり
- CONTRIBUTING.md: あり
- LICENSE: MIT
- Versioning: `pyproject.toml` をSSOTにした `version` コマンドあり
- 生成物: `reports/` は `.gitignore` 対象
- GitHub作成/push: `nexus-ai-2045/ai-output-eval-harness` へprivateで実施済み
- public visibility変更/release/告知/外部共有: 未実施
- secret pattern scan: 全9 commitsをgitleaksで走査し、検出なし（2026-07-17）
- personal path scan: 全9 commitsと現行tracked filesを走査し、検出なし（2026-07-17）
- Git履歴の作者情報: `nexus_ai <nexus.ai.2045@gmail.com>` の1種。Web公開可否は人間レビューが必要

## 公開前に必要な判断

- サンプルデータを公開してよいか
- READMEの言語を日本語中心にするか、英語版も併記するか
- PyPI公開を目指すか、GitHubリポだけにするか

## 公開前チェック

- `python -m pytest`
- secret scan
- personal path scan
- `reports/` やローカル生成物が追跡されていないこと
- GitHub上でSecurity Advisoriesを有効化するか確認
- GitHub Actionsが新規環境でテスト依存を導入できること
- release tag運用を決める

## 人間レビュー境界

private repositoryの作成と初回pushは完了済み。今後の追加push、visibility変更、public化、release、外部共有は、現在会話で対象repo、外から見える内容、正確な操作を明示し、人間レビューと承認を得た後に行う。
