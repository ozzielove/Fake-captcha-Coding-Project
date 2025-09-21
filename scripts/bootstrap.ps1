<#!
.SYNOPSIS
  LAB ONLY bootstrap for the fake CAPTCHA lab.

.DESCRIPTION
  - Sets LAB_EXECUTE (default ON). Use -NoExecute to set OFF.
  - Starts static site on port 8080 and MCP server on port 8787.
  - Benign by design. No exfiltration, no persistence, no privilege escalation.

.PARAMETER NoExecute
  Optional switch to disable execution mode (LAB_EXECUTE=0).

.NOTES
  Versions or package locations are TODO: VERIFY.
#>

param(
  [switch]$NoExecute
)

Write-Host "=== LAB ONLY BOOTSTRAP ===" -ForegroundColor Yellow
if ($NoExecute) {
  $env:LAB_EXECUTE = "0"
} else {
  $env:LAB_EXECUTE = "1"
}
Write-Host "LAB_EXECUTE set to $($env:LAB_EXECUTE)"

$root = Join-Path $PSScriptRoot "..\fake-captcha-lab"
Push-Location $root
Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList "-m", "http.server", "8080"
Pop-Location
Write-Host "Static site at http://localhost:8080 (LAB ONLY)"

$apiRoot = Join-Path $PSScriptRoot "..\agent-mcp-rbac"
Push-Location $apiRoot
Start-Process -WindowStyle Hidden -FilePath "uvicorn" -ArgumentList "agent-mcp-rbac.server:app", "--port", "8787", "--host", "127.0.0.1"
Pop-Location
Write-Host "MCP server at http://127.0.0.1:8787 (LAB ONLY)"

Write-Host "Bootstrap complete. Open the lab page in a local browser." -ForegroundColor Green
