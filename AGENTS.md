# ai-output-eval-harness Agent Rules

このrepositoryの作業前に `REPO_GOAL.md` と `.repo-operating-contracts/manifest.json` を確認する。

## 言語

ユーザー向け、運用向け、レビュー向け文書は日本語を既定にする。コード識別子、command、API名、既存file名は英語のままでよい。

## 作業場所とscope

- 想定remoteは `nexus-ai-2045/ai-output-eval-harness`。
- 書き込み前にrepo root、remote、branch、upstream、ahead / behind、dirty stateを確認する。
- repo goalが変わる、別repoへ移る、3 file / 3論点以上へ分岐する場合は別task化をすすめる。
- `REPO_GOAL.md` はこのrepoが所有する。managed bundle更新で上書きしない。

## 停止線

現在会話で対象と操作を明示した人間レビューがあるまで、次を実行しない。

- push / PR / release / announcement / broad share
- repository visibility change
- external post / send / comment
- hook install / automation enablement
- auth、secret、production設定の変更

`.repo-operating-contracts/repo-operating-hook.v1.md` は配置済みだが、install / enableしていない。

## 検証

```powershell
python -m pytest -q
python -m pytest -q tests/test_japanese_docs.py
python .repo-operating-contracts\check.py
```
