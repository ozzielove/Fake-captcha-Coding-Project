# IR Playbook (2-page) - LAB ONLY

## 1. Trigger
- Alerts fire on the rare parent of PowerShell pattern and EncodedCommand usage.
- Source tables: DeviceProcessEvents, SecurityAlert, AlertEvidence (see `detections/kql/dashboard_queries.kql`).

## 2. Triage
- Validate process tree: chrome.exe or msedge.exe -> powershell.exe or pwsh.exe.
- Check the CommandLine for benign lab seeds (for example Start-Process notepad.exe).
- Confirm there is no persistence, network activity, or credential access (lab design).

## 3. Contain (Lab)
- Document ASR, AppLocker, WDAC baselines (samples under `edr-policies/`).
- Verify the MCP server denies out-of-scope requests with HTTP 403 and logs to `agent-mcp-rbac/alerts.log`.

## 4. Remediate
- No remediation needed beyond closing benign processes. Capture telemetry for dashboards.

## 5. Lessons Learned
- Tune false positives to stay below the 2 percent target.
- Keep evidence and access dates in README Evidence Map (URLs remain TODO: VERIFY until validated).
