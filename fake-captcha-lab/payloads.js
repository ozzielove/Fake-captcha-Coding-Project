// LAB ONLY. Rotating benign PowerShell seeds.
// These commands are intentionally harmless (for example launching Notepad or Calc) to exercise detections for
// HTML smuggling and rare parent of PowerShell telemetry. Do not modify for malicious purposes.

const LAB_SEEDS = [
  { description: "Start Notepad (plain)", command: "powershell -NoProfile -Command Start-Process notepad.exe" },
  { description: "Start Notepad (hidden benign)", command: "powershell -NoProfile -WindowStyle Hidden -Command Start-Process notepad.exe" },
  { description: "Start Calc (plain)", command: "powershell -NoProfile -Command Start-Process calc.exe" },
  { description: "Start Notepad (encoded UTF-16LE base64)", command: "powershell -NoProfile -EncodedCommand SQBFAFoAIAAtAE4AbwBQAHIAbwBmAGkAbABlACAALQBDAG8AbQBtAGEAbgBkACAAUwB0AGEAcgB0AC0AUABSAE8AQwBFAFMAUwAgAG4AbwB0AGUAcABhAGQALgBlAHgAZQA=" },
  { description: "Write-Host benign banner", command: "powershell -NoProfile -Command Write-Host 'LAB ONLY - benign action'" },
  { description: "Start Notepad (quoted)", command: "powershell -NoProfile -Command \"Start-Process 'notepad.exe'\"" },
  { description: "Start Notepad (call operator)", command: "powershell -NoProfile -Command & { Start-Process notepad.exe }" },
  { description: "Start Notepad (working directory)", command: "powershell -NoProfile -Command Start-Process notepad.exe -WorkingDirectory $env:TEMP" },
  { description: "Start Notepad (alias saps)", command: "powershell -NoProfile -Command saps notepad.exe" },
  { description: "Start Notepad (CMD parent)", command: "cmd /c powershell -NoProfile -Command Start-Process notepad.exe" }
];

let labSeedIndex = 0;
function nextLabSeed() {
  const seed = LAB_SEEDS[labSeedIndex % LAB_SEEDS.length];
  labSeedIndex += 1;
  return seed;
}
