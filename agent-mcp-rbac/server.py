"""LAB ONLY - Minimal MCP-shaped server enforcing least privilege."""

from __future__ import annotations

import datetime
import json
import pathlib
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

POLICY_PATH = pathlib.Path(__file__).with_name("policy.json")
ALERT_LOG = pathlib.Path(__file__).with_name("alerts.log")


def load_policy() -> Dict[str, Any]:
    try:
        with open(POLICY_PATH, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return {
            "allowed_tools": [],
            "sandbox_root": "./sandbox",
            "deny_message": "Policy not loaded (TODO: VERIFY)",
        }


def log_alert(event: Dict[str, Any]) -> None:
    ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)
    event["ts"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(ALERT_LOG, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")


app = FastAPI(title="LAB ONLY MCP Server", version="VERIFY")


class EchoReq(BaseModel):
    text: str


class ReadReq(BaseModel):
    path: str


@app.middleware("http")
async def policy_banner(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-LAB-ONLY"] = "true"
    return response


@app.get("/healthz")
def healthz() -> Dict[str, Any]:
    return {"ok": True, "lab_only": True}


@app.post("/tool/echo")
def tool_echo(req: EchoReq) -> Dict[str, Any]:
    policy = load_policy()
    if "echo" not in policy.get("allowed_tools", []):
        log_alert({"type": "deny", "reason": "tool_not_allowed", "tool": "echo"})
        raise HTTPException(status_code=403, detail="DENY: tool not allowed by policy")
    return {"echo": req.text, "lab_only": True}


@app.post("/tool/read")
def tool_read(req: ReadReq) -> Dict[str, Any]:
    policy = load_policy()
    if "readfile" not in policy.get("allowed_tools", []):
        log_alert({"type": "deny", "reason": "tool_not_allowed", "tool": "readfile"})
        raise HTTPException(status_code=403, detail="DENY: tool not allowed by policy")
    sandbox_root = pathlib.Path(policy.get("sandbox_root", "./sandbox")).resolve()
    target = pathlib.Path(req.path).resolve()
    try:
        target.relative_to(sandbox_root)
    except Exception:
        log_alert(
            {
                "type": "deny",
                "reason": "path_out_of_scope",
                "attempt": str(target),
                "sandbox_root": str(sandbox_root),
            }
        )
        raise HTTPException(status_code=403, detail="DENY: path outside sandbox")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    with open(target, "r", encoding="utf-8", errors="ignore") as handle:
        data = handle.read()
    return {
        "path": str(target),
        "bytes": len(data),
        "preview": data[:256],
        "lab_only": True,
    }
