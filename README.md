# LAB ONLY - Fake CAPTCHA -> Clipboard -> PowerShell (Benign) Blue-Team Lab

**Strictly LAB ONLY.** No malware, no exfiltration, no persistence, no privilege escalation. Payloads are benign (for example launching Notepad or Calc). Unverified details are marked "TODO: VERIFY" per policy.

## Background
This lab demonstrates a HTML smuggling style page that copies a benign PowerShell one-liner to the clipboard after a user gesture. It models a fake CAPTCHA social flow and enables detections for the **rare parent of PowerShell** (for example chrome.exe or msedge.exe -> powershell.exe) and **EncodedCommand** usage in Microsoft Defender for Endpoint and Microsoft Sentinel (KQL-first). Clipboard visibility uses a Sysmon stub that never sends contents off-host.

## Quickstart (LAB ONLY)
Default execution mode is ON. Set `LAB_EXECUTE=0` to disable benign launches.

### Windows (PowerShell)
```powershell
# LAB ONLY
$env:LAB_EXECUTE = "1"  # default ON; use "0" to disable
.\scripts\bootstrap.ps1
```

### Bash (services only; Windows payloads will not run)
```bash
# LAB ONLY
export LAB_EXECUTE=1
(cd fake-captcha-lab && python -m http.server 8080 &)
uvicorn agent-mcp-rbac.server:app --port 8787 --host 127.0.0.1
```

Open http://localhost:8080 and click Verify to copy a benign payload to the clipboard. The page never auto-executes anything.

### GPG Quickstart (exactly two commands)
```
git config --global commit.gpgsign true
git config --global user.signingkey <YOUR_GPG_KEY_ID>
```
Requires a GPG key (URL: TODO: VERIFY).

## Architecture
- `fake-captcha-lab/` - HTML smuggling page with strict CSP, Permissions-Policy, and rotating benign seeds.
- `guardrails/` - Deterministic filter that blocks OS-command instructions; unit tests enforce zero escapes.
- `agent-mcp-rbac/` - Minimal MCP-shaped server (port 8787) enforcing least privilege via `policy.json`. Out-of-scope tool calls or paths return HTTP 403 and log alerts to `agent-mcp-rbac/alerts.log` (SIEM integration TODO: VERIFY).
- `detections/` - Sigma rules and KQL queries (`detections/kql/dashboard_queries.kql`) for Microsoft Defender for Endpoint and Microsoft Sentinel.
- `sysmon/` - Clipboard lab config (schema/event IDs TODO: VERIFY).
- `edr-policies/` - Sample ASR, AppLocker, WDAC, and AMSI guidance (validate before use).
- `browser-policies/` - Chrome and Edge templates allowing clipboard access for localhost (TODO: VERIFY in ADMX).
- `evals/` - Harness that executes benign seeds when `LAB_EXECUTE=1` (Windows only) and writes `results.json`.
- `yara/` - Minimal indicators for EncodedCommand and HTML smuggling markers.
- `ci/` - GitHub Actions workflow (Windows) with optional `pysigma` validation gated by `SIGMA_VALIDATE=1`.

## Target SIEM & Pipeline
Primary pipeline: **Microsoft Defender for Endpoint + Microsoft Sentinel (KQL-first).** Queries are provided in `detections/kql/dashboard_queries.kql` covering rare parent of PowerShell, EncodedCommand patterns, MTTA calculation, and AlertEvidence pivots.

## Acceptance Criteria
- **<= 5s mean time from PowerShell launch to first alert (lab pipeline target; SIEM-timestamped).**
- **>= 95% block rate on rotating one-liner variants (10 seeds; show seeds).**
- **<= 2% false-positive rate on normal admin PowerShell use (document exclusions).**
- **0 instances of LLM output instructing Win+R/paste shell code (guardrail tests green).**
- **Agent/MCP: unscoped tool calls or reads outside sandbox -> DENY + alert (server-enforced).**
- **All changes signed (GPG) and reproducible via one-click script.**
- **Execution mode defaults to ON (benign commands). Set LAB_EXECUTE=0 to disable.**

## Metrics Plan
- MTTA is the time difference (seconds) from PowerShell process start to first alert, computed with KQL in `detections/kql/dashboard_queries.kql`.
- Block and false-positive rates are measured via `evals/run_evals.py` seeds plus SIEM analytics (data capture steps: TODO: VERIFY).

## Privacy & Scope
- Clipboard monitoring is lab-only; contents never leave the host. Sysmon configuration remains a stub with schema TODO: VERIFY.
- No network callbacks, persistence, or privilege escalation are included.

## Evidence Map
| Claim | Artifact | Sources |
| --- | --- | --- |
| HTML smuggling page copies benign payload on gesture | `fake-captcha-lab/index.html`, `fake-captcha-lab/payloads.js` | [S1], [S2] (accessed: TODO: VERIFY) |
| Rare parent of PowerShell is detectable | `detections/kql/dashboard_queries.kql`, `detections/sigma/browser_parent_powershell.yml` | [S3], [S4] (accessed: TODO: VERIFY) |
| EncodedCommand variants are monitored | `detections/kql/dashboard_queries.kql`, `detections/sigma/powershell_encoded_command.yml` | [S5] (accessed: TODO: VERIFY) |
| MTTA measurable in Sentinel and MDE | `detections/kql/dashboard_queries.kql` | [S6] (accessed: TODO: VERIFY) |
| MCP least privilege enforced with 403 DENY | `agent-mcp-rbac/server.py`, `agent-mcp-rbac/policy.json` | [S7] (accessed: TODO: VERIFY) |
| Guardrails block OS-command instructions | `guardrails/src/guardrail_filter.py`, tests in `guardrails/tests` | [S8] (accessed: TODO: VERIFY) |
| Sysmon clipboard visibility achievable in lab | `sysmon/sysmon-clipboard-lab.xml` | [S9] (accessed: TODO: VERIFY) |
| Sigma rules carry UUID and ATT&CK tags | `detections/sigma/*.yml` | [S10] (accessed: TODO: VERIFY) |
| Optional pysigma validation available | `ci/github-actions.yml` | [S11] (accessed: TODO: VERIFY) |
| EDR baselines support containment | `edr-policies/` | [S12] (accessed: TODO: VERIFY) |
| Browser policies allow clipboard on localhost | `browser-policies/*.json` | [S13] (accessed: TODO: VERIFY) |
| YARA indicators cover PowerShell and HTML smuggling cues | `yara/*.yar` | [S14] (accessed: TODO: VERIFY) |
| GPG-signed changes preserve integrity | README section above | [S15] (accessed: TODO: VERIFY) |

## References
- [S1] HTML smuggling overview - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S2] Clipboard API documentation - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S3] Rare parent process analytics - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S4] MDE process events schema - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S5] PowerShell EncodedCommand detection - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S6] Sentinel KQL MTTA examples - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S7] MCP or agent least-privilege patterns - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S8] Safety filters for model outputs - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S9] Sysmon clipboard or change events - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S10] Sigma rule specification - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S11] pysigma validation resources - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S12] ASR, AppLocker, WDAC guidance - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S13] Chrome and Edge policy templates - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S14] YARA language reference - URL: TODO: VERIFY (accessed: TODO: VERIFY)
- [S15] GPG usage guidance - URL: TODO: VERIFY (accessed: TODO: VERIFY)

## Repo Tree
```
fake-captcha-lab/
  index.html
  payloads.js
guardrails/
  guardrails.md
  src/guardrail_filter.py
  tests/test_guardrails.py
agent-mcp-rbac/
  server.py
  policy.json
detections/
  sigma/
    browser_parent_powershell.yml
    powershell_encoded_command.yml
    clipboard_access_labhosts.yml
  kql/
    dashboard_queries.kql
sysmon/
  sysmon-clipboard-lab.xml
edr-policies/
  asr_baseline.json
  applocker_baseline.xml
  amsi_guidance.md
  wdac_baseline.xml
browser-policies/
  chrome_policies.json
  edge_policies.json
scripts/
  bootstrap.ps1
ci/
  github-actions.yml
docs/
  PSA-slide.md
  IR-playbook-2p.md
evals/
  run_evals.py
  results.json
  dashboard-screens/README.md
yara/
  suspicious_ps1_rules.yar
  html_smuggling_indicators.yar
LICENSE
README.md
TUTORIAL.md
```

---

**LAB ONLY.** Do not operate outside controlled environments. All third-party versions or URLs remain TODO: VERIFY until independently confirmed.
