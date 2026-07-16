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
- GitHub作成/push/public化: 未実施
- secret pattern scan: 検出なし（2026-07-16）
- personal path scan: 検出なし（2026-07-16）
- Git履歴の作者情報: 個人名義を含むため、人間レビューが必要

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

repository作成、push、visibility変更、public化、外部共有は、現在会話で対象repoと操作を明示して人間レビュー後に行う。
