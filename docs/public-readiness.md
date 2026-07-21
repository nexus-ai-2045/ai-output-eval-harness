# 公開前チェック

この文書は、`ai-output-eval-harness` を公開する前に確認する技術項目をまとめたものです。公開先のアカウント、組織内台帳、承認履歴は公開repositoryへ含めません。

## 自動確認

- `python -m pytest`
- `python .repo-operating-contracts\check.py`
- packageのeditable install
- sample inputを使ったpipeline smoke test
- secret scannerによる現在のファイルと全commit履歴の検査
- personal path scan
- dependency vulnerability scan
- GitHub Actionsの実行結果
- `reports/` とローカル生成物がGit管理対象外であること

## 人間による確認

- READMEとコマンド例が初めての利用者にも理解できる
- sample dataが合成データまたは再配布可能なデータだけで構成されている
- 価値観カタログの出典・制約・ルールベース判定の限界が説明されている
- commit履歴に個人メール、内部パス、非公開情報がない
- GitHubのみで配布するか、package registryにも配布するか決定済み

## GitHub設定

- Security Advisoriesとprivate vulnerability reporting
- dependency alerts
- default branchとbranch保護
- pull request reviewとCI成功を必須にする規則
- release tagの命名とrollback方法

公開操作は、自動検査と人間確認の両方が完了し、対象repositoryと正確な操作について明示承認を得た後に行います。
