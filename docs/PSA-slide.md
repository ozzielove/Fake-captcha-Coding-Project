# PSA: LAB ONLY (Benign HTML Smuggling -> Clipboard -> PowerShell)

- Purpose: Blue-team training to detect HTML smuggling and rare parent of PowerShell patterns.
- Payloads are benign (open Notepad or Calc). No exfiltration, persistence, or privilege escalation.
- Target SIEM: Microsoft Defender for Endpoint plus Microsoft Sentinel (KQL-first); queries live in `detections/kql/dashboard_queries.kql`.
- Clipboard visibility is lab-only; contents never leave the host.
- Versions or links: TODO: VERIFY.
