import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIDE_ROUTE = ROOT / ".repo-operating-contracts" / "side_route_decider.py"
IDENTITY = ROOT / ".repo-operating-contracts" / "workdir_git_identity_check.py"


def _run_python(script: Path, *args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def _init_repo(tmp_path: Path, remote_url: str | None) -> Path:
    repo = tmp_path / "candidate"
    repo.mkdir()
    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    if remote_url:
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=repo, check=True)
    return repo


def _identity_check(repo: Path) -> subprocess.CompletedProcess[str]:
    return _run_python(
        IDENTITY,
        "--cwd",
        str(repo),
        "--expected-repo",
        "ai-output-eval-harness",
        "--expected-owner",
        "nexus-ai-2045",
        "--allow-no-upstream",
    )


def test_risk_flags_string_fails_closed() -> None:
    result = _run_python(
        SIDE_ROUTE,
        "--json",
        json.dumps({"repo_goal": "安全運用", "risk_flags": "publication_boundary"}),
    )

    assert result.returncode != 0
    assert json.loads(result.stdout)["recommendation"] == "stop_for_review"


def test_explicit_risk_flag_fails_closed_at_process_boundary() -> None:
    result = _run_python(
        SIDE_ROUTE,
        "--json",
        json.dumps({"repo_goal": "安全運用", "risk_flags": ["publication_boundary"]}),
    )

    assert result.returncode != 0
    assert json.loads(result.stdout)["recommendation"] == "stop_for_review"


def test_invalid_json_fails_closed() -> None:
    result = _run_python(SIDE_ROUTE, "--json", "{")

    assert result.returncode != 0
    assert json.loads(result.stdout)["recommendation"] == "stop_for_review"


def test_non_string_risk_flag_fails_closed() -> None:
    result = _run_python(
        SIDE_ROUTE,
        "--json",
        json.dumps({"repo_goal": "安全運用", "risk_flags": ["external_action", 1]}),
    )

    assert result.returncode != 0
    assert json.loads(result.stdout)["recommendation"] == "stop_for_review"


def test_similar_repository_name_does_not_match(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "https://github.com/evil/nexus-ai-2045-ai-output-eval-harness.git")

    result = _identity_check(repo)

    assert result.returncode != 0
    assert json.loads(result.stdout)["repo_identity"] == "mismatched"


def test_exact_origin_matches(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "https://github.com/nexus-ai-2045/ai-output-eval-harness.git")

    result = _identity_check(repo)

    assert result.returncode == 0
    assert json.loads(result.stdout)["repo_identity"] == "matched"


def test_exact_ssh_origin_matches(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "git@github.com:nexus-ai-2045/ai-output-eval-harness.git")

    result = _identity_check(repo)

    assert result.returncode == 0
    assert json.loads(result.stdout)["repo_identity"] == "matched"


def test_missing_expected_owner_fails_closed(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "https://github.com/nexus-ai-2045/ai-output-eval-harness.git")

    result = _run_python(
        IDENTITY,
        "--cwd",
        str(repo),
        "--expected-repo",
        "ai-output-eval-harness",
        "--allow-no-upstream",
    )

    assert result.returncode != 0
    assert json.loads(result.stdout)["repo_identity"] == "mismatched"


def test_non_github_host_does_not_match(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "https://evil.example/nexus-ai-2045/ai-output-eval-harness.git")

    result = _identity_check(repo)

    assert result.returncode != 0
    assert json.loads(result.stdout)["repo_identity"] == "mismatched"


def test_missing_origin_is_unknown(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, None)

    result = _identity_check(repo)

    assert result.returncode != 0
    assert json.loads(result.stdout)["repo_identity"] == "unknown"


def test_trusted_non_origin_does_not_override_fake_origin(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "https://github.com/evil/ai-output-eval-harness.git")
    subprocess.run(
        ["git", "remote", "add", "trusted", "https://github.com/nexus-ai-2045/ai-output-eval-harness.git"],
        cwd=repo,
        check=True,
    )

    result = _identity_check(repo)

    assert result.returncode != 0
    assert json.loads(result.stdout)["repo_identity"] == "mismatched"


def test_fake_origin_push_url_does_not_match(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path, "https://github.com/nexus-ai-2045/ai-output-eval-harness.git")
    subprocess.run(
        ["git", "remote", "set-url", "--push", "origin", "https://github.com/evil/ai-output-eval-harness.git"],
        cwd=repo,
        check=True,
    )

    result = _identity_check(repo)

    assert result.returncode != 0
    assert json.loads(result.stdout)["repo_identity"] == "mismatched"
