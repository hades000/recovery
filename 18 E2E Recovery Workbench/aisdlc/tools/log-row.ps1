<#
.SYNOPSIS
  Appends one timeline row to AI-SDLC-BUILD-LOG.md with the current local time.
.EXAMPLE
  ./aisdlc/tools/log-row.ps1 -Story RWB-E1-001 -Stage Specify -Actor technical-specifier -Group P1 -Outcome STARTED -Note "RUN_ID INC-009-epic-1-RWB-E1-001"
#>
param(
  [Parameter(Mandatory)][string]$Story,
  [Parameter(Mandatory)][string]$Stage,
  [Parameter(Mandatory)][string]$Actor,
  [string]$Group = "-",
  [Parameter(Mandatory)][string]$Outcome,
  [string]$Note = ""
)
$log = Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) "AI-SDLC-BUILD-LOG.md"
$time = (Get-Date).ToString("yyyy-MM-ddTHH:mm:sszzz")
$row = "| $time | $Story | $Stage | $Actor | $Group | $Outcome | $($Note -replace '\|', '/') |`n"
# .NET API: UTF-8 without BOM, no re-encoding of the existing file (Windows PowerShell 5.1 safe).
[System.IO.File]::AppendAllText($log, $row, (New-Object System.Text.UTF8Encoding $false))
$row.Trim()
