"""LAB ONLY - Evaluation harness for benign PowerShell seeds."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import time
from pathlib import Path

LAB_SEEDS = [
    {"desc": "Start Notepad (plain)", "cmd": ["powershell", "-NoProfile", "-Command", "Start-Process notepad.exe"]},
    {"desc": "Start Notepad (hidden benign)", "cmd": ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", "Start-Process notepad.exe"]},
    {"desc": "Start Calc (plain)", "cmd": ["powershell", "-NoProfile", "-Command", "Start-Process calc.exe"]},
    {"desc": "Write-Host benign", "cmd": ["powershell", "-NoProfile", "-Command", "Write-Host 'LAB ONLY - benign action'"]},
    {"desc": "Start Notepad (alias saps)", "cmd": ["powershell", "-NoProfile", "-Command", "saps notepad.exe"]},
    {"desc": "Start Notepad (cmd parent)", "cmd": ["cmd", "/c", "powershell", "-NoProfile", "-Command", "Start-Process notepad.exe"]},
    {"desc": "Start Notepad (working dir)", "cmd": ["powershell", "-NoProfile", "-Command", "Start-Process notepad.exe -WorkingDirectory $env:TEMP"]},
    {"desc": "Start Notepad (call operator)", "cmd": ["powershell", "-NoProfile", "-Command", "& { Start-Process notepad.exe }"]},
    {"desc": "Start Notepad (quoted)", "cmd": ["powershell", "-NoProfile", "-Command", "Start-Process 'notepad.exe'"]},
    {"desc": "Write-Host banner", "cmd": ["powershell", "-NoProfile", "-Command", "Write-Host 'LAB ONLY'"]},
]

RESULTS_PATH = Path(__file__).with_name("results.json")


def is_enabled() -> bool:
    return os.environ.get("LAB_EXECUTE", "1") == "1"


def run_seed(seed: dict[str, object]) -> dict[str, object]:
    start = time.time()
    status = "skipped_non_windows"
    if platform.system() == "Windows":
        try:
            subprocess.Popen(seed["cmd"], shell=False)
            status = "executed"
        except Exception as exc:
            status = f"error:{type(exc).__name__}"
    elapsed_ms = int((time.time() - start) * 1000)
    return {"desc": seed["desc"], "status": status, "elapsed_ms": elapsed_ms}


def main() -> None:
    results: dict[str, object] = {
        "lab_only": True,
        "lab_execute": "1" if is_enabled() else "0",
        "platform": platform.system(),
        "runs": [],
    }
    if is_enabled():
        for seed in LAB_SEEDS:
            results["runs"].append(run_seed(seed))
    else:
        results["runs"] = [
            {"desc": seed["desc"], "status": "disabled", "elapsed_ms": 0}
            for seed in LAB_SEEDS
        ]
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
