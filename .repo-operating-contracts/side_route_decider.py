import argparse
import json
import sys
from typing import Any


REVIEW_RISK_FLAGS = {
    "publication_boundary",
    "external_action",
    "repository_visibility",
    "hook_install",
    "automation_enablement",
    "secret_or_auth",
    "production_change",
}

NEW_CHAT_SCOPES = {
    "new_repo",
    "other_repo",
    "new_skill",
    "skill",
    "new_hook",
    "hook",
    "new_worktree",
    "worktree",
    "new_chat",
}


def _stop_for_review(reason: str, repo_goal: str = "unknown") -> dict[str, Any]:
    return {
        "recommendation": "stop_for_review",
        "reason": reason,
        "suggested_chat_goal": "",
        "main_task_to_preserve": repo_goal,
        "skill": "side-route-chat-router",
    }


def _string_set(payload: dict[str, Any], field: str) -> set[str]:
    value = payload.get(field)
    if value is None:
        return set()
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field} must be an array of strings")
    return set(value)


def decide_side_route(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return _stop_for_review("判定入力がJSON objectではないため停止します。")

    current_repo = str(payload.get("current_repo") or "unknown")
    repo_goal = str(payload.get("repo_goal") or "unknown")
    new_topic = str(payload.get("new_topic") or "")
    try:
        changed_scope = _string_set(payload, "changed_scope")
        risk_flags = _string_set(payload, "risk_flags")
        active_files_value = payload.get("active_files", 0)
        if isinstance(active_files_value, bool) or not isinstance(active_files_value, int) or active_files_value < 0:
            raise ValueError("active_files must be a non-negative integer")
        active_files = active_files_value
    except ValueError as exc:
        return _stop_for_review(f"判定入力が不正です: {exc}", repo_goal)

    if risk_flags & REVIEW_RISK_FLAGS:
        return _stop_for_review("公開、外部操作、hook、automation、auth などの停止線に入っています。", repo_goal)

    if changed_scope & NEW_CHAT_SCOPES:
        return {
            "recommendation": "suggest_new_chat",
            "reason": "repo、skill、hook、worktree のどれかが本線から分岐しています。",
            "suggested_chat_goal": new_topic or f"{current_repo} から分岐した作業を整理する",
            "main_task_to_preserve": repo_goal,
            "skill": "side-route-chat-router",
        }

    if active_files >= 3 or len(changed_scope) >= 3:
        return {
            "recommendation": "suggest_new_chat",
            "reason": "3 file / 3 論点以上に広がっています。",
            "suggested_chat_goal": new_topic or f"{current_repo} の分岐作業を別 task として整理する",
            "main_task_to_preserve": repo_goal,
            "skill": "side-route-chat-router",
        }

    return {
        "recommendation": "continue_here",
        "reason": "現在の repo goal の中で最小 scope として扱えます。",
        "suggested_chat_goal": "",
        "main_task_to_preserve": repo_goal,
        "skill": "side-route-chat-router",
    }


def _load_payload(raw: str | None) -> dict[str, Any]:
    if raw:
        return json.loads(raw)
    data = sys.stdin.read().strip()
    if not data:
        return {}
    return json.loads(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="脇道化した作業を別チャット化すべきか判定します。")
    parser.add_argument("--json", dest="json_payload", help="判定入力 JSON。省略時は stdin から読む。")
    args = parser.parse_args()
    try:
        result = decide_side_route(_load_payload(args.json_payload))
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        result = _stop_for_review(f"判定入力を解釈できません: {exc}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["recommendation"] == "stop_for_review" else 0


if __name__ == "__main__":
    raise SystemExit(main())
