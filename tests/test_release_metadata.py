import tomllib
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_release_version_matches_project_and_readme() -> None:
    with (ROOT / "pyproject.toml").open("rb") as file:
        version = tomllib.load(file)["project"]["version"]

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    release_notes = ROOT / "docs" / "releases" / f"v{version}.md"

    assert f"現在のバージョン: `{version}`" in readme
    assert release_notes.is_file()
    assert release_notes.read_text(encoding="utf-8").startswith(
        f"# v{version} リリースノート\n"
    )
