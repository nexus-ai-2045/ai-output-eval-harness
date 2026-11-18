from pathlib import Path


WORKFLOW = Path(__file__).parents[1] / ".github" / "workflows" / "ci.yml"


def test_ci_declares_read_only_token_permissions() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    permissions = workflow.index("permissions:")
    jobs = workflow.index("jobs:")

    assert permissions < jobs
    assert "permissions:\n  contents: read\n" in workflow
