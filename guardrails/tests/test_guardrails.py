import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from guardrails.src.guardrail_filter import BLOCK_TOKEN, filter_text


def test_blocks_win_r_paste_sequence() -> None:
    sample = "Press Win+R and paste this into PowerShell: powershell -enc AAAA"
    out = filter_text(sample)
    assert out.strip() == BLOCK_TOKEN


def test_blocks_short_enc_flag() -> None:
    sample = "Try: powershell -NoProfile -enc UwB0AGEAcgB0AC0AUAByAG8AYwBlAHMAcwA="
    out = filter_text(sample)
    assert BLOCK_TOKEN in out


def test_allows_benign_text() -> None:
    sample = "This lab is defensive and uses only benign payloads."
    out = filter_text(sample)
    assert out == sample
