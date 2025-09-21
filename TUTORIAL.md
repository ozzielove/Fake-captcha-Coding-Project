# Tutorial (Step-by-step) - LAB ONLY

Safety notice: This lab is defensive. Payloads are benign (for example Notepad or Calc). No exfiltration, persistence, or privilege escalation. Set `LAB_EXECUTE=0` if you do not want benign processes to launch.

1. **Prerequisites (TODO: VERIFY):**
   - Clean Windows VM with Python 3.11 and ability to install packages.
   - Browser (Chrome or Edge) configured to allow clipboard access on localhost (see `browser-policies/`).
   - Optional Sysmon installation (schema and event IDs in `sysmon/sysmon-clipboard-lab.xml` remain TODO: VERIFY).
2. **Start services:**
   - Run `scripts/bootstrap.ps1`. Without arguments it sets `LAB_EXECUTE=1`, starts the static site on port 8080, and starts the MCP server on port 8787.
   - Use `-NoExecute` to set `LAB_EXECUTE=0` if you only want to review content.
3. **Exercise the flow:**
   - Visit http://localhost:8080, check both boxes (gesture plus clipboard permission), then click **Verify**.
   - The page copies a benign PowerShell seed to the clipboard. It does not execute anything automatically.
   - Modern browsers may prompt for clipboard access; ensure the gesture is allowed.
4. **Detections (KQL-first):**
   - Use the queries in `detections/kql/dashboard_queries.kql` within Microsoft Sentinel or Microsoft Defender for Endpoint.
   - Provided queries cover rare parent of PowerShell, EncodedCommand variants, MTTA calculations, and AlertEvidence pivots.
5. **Guardrails:**
   - The filter in `guardrails/src/guardrail_filter.py` blocks OS-command instructions. Run `pytest` to confirm guardrail tests remain green.
6. **MCP least privilege check:**
   - `agent-mcp-rbac/server.py` enforces `policy.json`. Allowed tools: `echo`, `readfile` within the sandbox path.
   - Out-of-scope requests return HTTP 403 and log to `agent-mcp-rbac/alerts.log`. Integrating the log with a SIEM is TODO: VERIFY.
   - Example deny test (from a separate terminal):
     ```bash
     curl -i http://127.0.0.1:8787/tool/read -d '{"path": "C:/Windows/System32/drivers/etc/hosts"}' -H "Content-Type: application/json"
     ```
     Expect HTTP 403 with the deny message.
7. **Optional Sysmon clipboard visibility:**
   - Review `sysmon/sysmon-clipboard-lab.xml`. Schema and EventID must be validated before use.
   - Ensure clipboard contents never leave the host (LAB ONLY requirement).
8. **YARA and Sigma assets:**
   - YARA rules live in `yara/`. Sigma rules live in `detections/sigma/` and include UUID plus ATT&CK tags.
   - Optional `pysigma` validation runs when `SIGMA_VALIDATE=1` in CI (`ci/github-actions.yml`).
9. **GPG and reproducibility:**
   - Configure commits to be GPG-signed using the two-command quickstart in the README.
   - Keep citations with `(accessed: TODO: VERIFY)` until validated.
10. **Troubleshooting:**
    - Clipboard prompts vary by browser; confirm the site is served from localhost over HTTP and triggered by a user gesture.
    - If services fail to start, ensure Python and uvicorn are on the PATH (versions: TODO: VERIFY).
    - If MTTA queries return no data, generate benign telemetry again and confirm SIEM connectors are ingesting data (details: TODO: VERIFY).

---

LAB ONLY. This tutorial avoids providing real-world OS-command instructions outside the controlled evaluation steps above.
