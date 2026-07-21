from __future__ import annotations

from typing import Any


def markdown_inline(value: Any) -> str:
    """Render untrusted data without allowing Markdown table/line injection."""
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "<br>").replace("\r", "<br>").replace("\n", "<br>")

