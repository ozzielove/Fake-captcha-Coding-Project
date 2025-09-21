"""LAB ONLY - deterministic guardrail filter."""

from __future__ import annotations

import re
from typing import Iterable

BLOCK_TOKEN = "[BLOCKED BY LAB GUARDRAIL]"

_PATTERNS: Iterable[re.Pattern[str]] = [
    re.compile(r"\bwin\s*\+\s*r\b", re.IGNORECASE),
    re.compile(r"\bwindows\s*\+\s*r\b", re.IGNORECASE),
    re.compile(r"\bencodedcommand\b", re.IGNORECASE),
    re.compile(r"(?<![a-zA-Z])-enc(?![a-zA-Z])", re.IGNORECASE),
    re.compile(r"(?<![a-zA-Z])-(?:e|en|enco|encod|encoded)command\b", re.IGNORECASE),
    re.compile(r"\bpowershell(?:\.exe)?\b", re.IGNORECASE),
    re.compile(r"\bpwsh(?:\.exe)?\b", re.IGNORECASE),
    re.compile(r"\bcmd(?:\.exe)?\s*/c\b", re.IGNORECASE),
    re.compile(r"\bbash\s*-c\b", re.IGNORECASE),
    re.compile(r"\bsh\s*-c\b", re.IGNORECASE),
    re.compile(r"\bpaste (?:this|the following) (?:into|in) (?:terminal|powershell|cmd)\b", re.IGNORECASE),
]


def _block_line(_: str) -> str:
    return BLOCK_TOKEN


def filter_text(text: str) -> str:
    """Filter potentially unsafe OS-command instructions from model output."""
    if not isinstance(text, str):
        return ""
    lines = text.splitlines()
    out_lines = []
    for line in lines:
        if any(pattern.search(line) for pattern in _PATTERNS):
            out_lines.append(_block_line(line))
        else:
            out_lines.append(line)
    return "\n".join(out_lines)


if __name__ == "__main__":
    sample = "Press Win+R and paste: powershell -enc AAA=\nThis is fine."
    print(filter_text(sample))
