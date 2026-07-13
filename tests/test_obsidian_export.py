from pathlib import Path

from ai_output_eval.cli import main
from ai_output_eval.obsidian_export import resolve_obsidian_output


def test_obsidian_export_writes_note(tmp_path: Path):
    summary = tmp_path / "summary.md"
    summary.write_text("# Summary\n\n- cases: 1\n", encoding="utf-8")
    out = tmp_path / "note.md"

    assert main(["obsidian-export", "--title", "Test Report", "--summary", str(summary), "--out", str(out)]) == 0
    note = out.read_text(encoding="utf-8")

    assert "tags:" in note
    assert "ai-eval" in note
    assert "# Test Report" in note
    assert "### Summary" in note


def test_obsidian_base_writes_base_file(tmp_path: Path):
    out = tmp_path / "reports.base"

    assert main(["obsidian-base", "--out", str(out)]) == 0
    content = out.read_text(encoding="utf-8")

    assert "file.hasTag(\"ai-eval\")" in content
    assert "Value Profile Reports" in content


def test_resolve_obsidian_output_rejects_path_escape(tmp_path: Path):
    try:
        resolve_obsidian_output(out=None, vault_dir=tmp_path, note_path="../escape.md")
    except ValueError as exc:
        assert "within vault-dir" in str(exc)
    else:
        raise AssertionError("expected path escape to fail")

