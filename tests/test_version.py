import json
from pathlib import Path

from ai_output_eval import __version__
from ai_output_eval.cli import main
from ai_output_eval.version import get_version


def test_version_reads_project_version():
    assert get_version() == "0.1.0"
    assert __version__ == "0.1.0"


def test_version_command_prints_version(capsys):
    assert main(["version"]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "0.1.0"


def test_pipeline_manifest_includes_tool_version(tmp_path: Path):
    out_dir = tmp_path / "bundle"

    assert main(["pipeline", "--input", "examples/sample-output.jsonl", "--out-dir", str(out_dir)]) == 0

    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["tool_version"] == "0.1.0"

