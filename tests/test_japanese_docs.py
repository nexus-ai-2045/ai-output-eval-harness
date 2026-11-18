import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).parents[1]
PUBLIC_DOCUMENTS = [
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "PUBLIC_READY.md",
    ROOT / "REPO_GOAL.md",
    *sorted((ROOT / "docs").glob("*.md")),
]
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
ALLOWED_IDENTIFIER_HEADINGS = {"# ai-output-eval-harness"}
FORBIDDEN_USER_FACING_PHRASES = {
    "Current version",
    "## License",
    "## Contributing / Security",
    "# Versioning",
}


def test_public_document_headings_are_japanese() -> None:
    failures: list[str] = []

    for path in PUBLIC_DOCUMENTS:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not line.startswith("#") or line in ALLOWED_IDENTIFIER_HEADINGS:
                continue
            if not JAPANESE_TEXT.search(line):
                failures.append(f"{path.relative_to(ROOT)}:{line_number}: {line}")

    assert not failures, "日本語を含まない利用者向け見出しがあります:\n" + "\n".join(failures)


def test_known_english_user_facing_phrases_are_absent() -> None:
    failures: list[str] = []

    for path in PUBLIC_DOCUMENTS:
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_USER_FACING_PHRASES:
            if phrase in text:
                failures.append(f"{path.relative_to(ROOT)}: {phrase}")

    assert not failures, "英語の利用者向け定型句が残っています:\n" + "\n".join(failures)


def test_package_description_is_japanese() -> None:
    with (ROOT / "pyproject.toml").open("rb") as file:
        description = tomllib.load(file)["project"]["description"]

    assert JAPANESE_TEXT.search(description), "パッケージ説明には日本語が必要です"
