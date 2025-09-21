# Guardrails (Lab Output Safety)

LAB ONLY. This repository includes deterministic guardrails that remove or block Large Language Model outputs which instruct users to execute operating system commands (for example "Press Win+R and paste" or "powershell -enc"). The goal is to ensure tutorials and agents stay defensive and avoid instructing real-world execution.

## What is blocked?
- OS hotkey launch instructions (for example "Win+R" or "Windows+R").
- Shell invocation with short or long EncodedCommand flags (case-insensitive): -enc, -e, -EncodedCommand.
- Direct CLI execution strings for common shells (powershell, cmd, pwsh, bash, sh) and copy or paste patterns.
- "Paste this in terminal" style instructions.

The filter leaves benign prose intact and replaces blocked patterns with `[BLOCKED BY LAB GUARDRAIL]`.

## Rationale (KQL-first Blue Team)
- The lab demonstrates HTML smuggling and rare parent of PowerShell telemetry for Microsoft Defender for Endpoint and Microsoft Sentinel.
- Clipboard monitoring is lab-only and contents never leave the host. References are captured in the README Evidence Map with placeholder citations `[S1]` to `[S15]` (accessed: TODO: VERIFY).

## Notes
- No versions or external links are invented. Where uncertain, we keep TODO: VERIFY markers.
- The guardrails are deterministic and covered by unit tests in `guardrails/tests/test_guardrails.py`.
