# Versioning

## 方針

バージョンは `pyproject.toml` の `[project].version` で一元管理します。

コード側では `ai_output_eval.version.get_version()` がインストール済みパッケージメタデータを優先し、未インストール実行では `pyproject.toml` を読みます。

## 表示箇所

- `python -m ai_output_eval version`
- `ai_output_eval.__version__`
- `pipeline` が生成する `manifest.json` の `tool_version`
- READMEの `Current version`

## 更新手順

1. `pyproject.toml` の `version` を更新する
2. READMEの `Current version` を同じ値に更新する
3. `python -m ai_output_eval version` を確認する
4. `python -m pytest` を実行する

