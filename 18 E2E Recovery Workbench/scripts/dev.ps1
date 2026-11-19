<#
.SYNOPSIS
  Local Recovery Workbench stack: one entry point for the day-to-day commands.

.EXAMPLE
  ./scripts/dev.ps1 up            # Postgres, Temporal, Temporal UI, Azurite, mock Entra ID
  ./scripts/dev.ps1 up -App       # ... plus the backend and frontend containers
  ./scripts/dev.ps1 backend       # bootRun against the stack (profile local)
  ./scripts/dev.ps1 frontend      # Vite dev server on :5173
  ./scripts/dev.ps1 test          # backend unit tests + frontend typecheck, lint, coverage
  ./scripts/dev.ps1 it            # recovery Testcontainers integration tests (needs Docker)
  ./scripts/dev.ps1 e2e           # API e2e (Gradle) + browser e2e (Playwright) against the stack
  ./scripts/dev.ps1 status        # container state and the platform health checks
  ./scripts/dev.ps1 down          # stop, keep data
  ./scripts/dev.ps1 reset         # stop and delete the database and Blob volumes
#>
param(
  [Parameter(Position = 0)]
  [ValidateSet("up", "down", "reset", "status", "backend", "frontend", "test", "it", "e2e", "logs")]
  [string]$Command = "up",
  [switch]$App
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$EnvFile = Join-Path $Root ".env"

function Initialize-EnvFile {
  if (-not (Test-Path $EnvFile)) {
    Copy-Item (Join-Path $Root ".env.example") $EnvFile
    Write-Host "Created .env from .env.example"
  }
  $content = Get-Content $EnvFile -Raw
  if ($content -notmatch "(?m)^RWB_TEMPORAL_CODEC_KEY=.+") {
    $bytes = New-Object byte[] 32
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    $key = [Convert]::ToBase64String($bytes)
    $content = $content -replace "(?m)^RWB_TEMPORAL_CODEC_KEY=.*\r?\n?", ""
    Set-Content -Path $EnvFile -Value ($content.TrimEnd() + "`nRWB_TEMPORAL_CODEC_KEY=$key`n") -Encoding utf8 -NoNewline
    Write-Host "Generated a local RWB_TEMPORAL_CODEC_KEY in .env"
  }
}

function Import-EnvFile {
  foreach ($line in Get-Content $EnvFile) {
    if ($line -match "^\s*#" -or $line -notmatch "=") { continue }
    $name, $value = $line -split "=", 2
    [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
  }
}

# Windows PowerShell 5.1 turns native stderr into a terminating error under "Stop"; docker, gradle
# and npm write progress there. Native calls run under "Continue" and are checked by exit code.
function Invoke-Native {
  param([scriptblock]$Block)
  $previous = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try { & $Block } finally { $ErrorActionPreference = $previous }
}

function Invoke-Compose {
  param([string[]]$Arguments)
  Invoke-Native { & docker compose --project-directory $Root --env-file $EnvFile @Arguments 2>&1 | ForEach-Object { "$_" } }
  if ($LASTEXITCODE -ne 0) { throw "docker compose $($Arguments -join ' ') failed" }
}

function Invoke-Gradle {
  param([string[]]$Arguments)
  Push-Location (Join-Path $Root "backend")
  try {
    Invoke-Native { & ./gradlew.bat @Arguments }
    if ($LASTEXITCODE -ne 0) { throw "gradle $($Arguments -join ' ') failed" }
  } finally { Pop-Location }
}

function Invoke-Npm {
  param([string[]]$Arguments)
  Push-Location (Join-Path $Root "frontend")
  try {
    if (-not (Test-Path node_modules)) { Invoke-Native { & npm ci --no-audit --no-fund }; if ($LASTEXITCODE -ne 0) { throw "npm ci failed" } }
    Invoke-Native { & npm @Arguments }
    if ($LASTEXITCODE -ne 0) { throw "npm $($Arguments -join ' ') failed" }
  } finally { Pop-Location }
}

Initialize-EnvFile
Import-EnvFile

switch ($Command) {
  "up" {
    $composeArgs = @("up", "-d", "--wait")
    if ($App) { $composeArgs = @("--profile", "app") + $composeArgs + @("--build") }
    Invoke-Compose $composeArgs
    Write-Host ""
    Write-Host "Postgres      localhost:$($env:POSTGRES_HOST_PORT) (database ace)"
    Write-Host "Temporal      localhost:7233   UI http://localhost:8233"
    Write-Host "Azurite Blob  http://localhost:10000"
    Write-Host "Mock Entra ID http://localhost:8090/entra/.well-known/openid-configuration"
    if ($App) { Write-Host "Backend       http://localhost:8080   Frontend http://localhost:5173" }
    else { Write-Host "Next: ./scripts/dev.ps1 backend   and   ./scripts/dev.ps1 frontend" }
  }
  "down" { Invoke-Compose @("--profile", "app", "down") }
  "reset" { Invoke-Compose @("--profile", "app", "down", "-v") }
  "logs" { Invoke-Compose @("--profile", "app", "logs", "-f", "--tail", "100") }
  "status" {
    Invoke-Compose @("--profile", "app", "ps")
    try { Invoke-RestMethod http://localhost:8080/actuator/health | ConvertTo-Json -Depth 4 } catch { Write-Host "Backend not reachable on :8080" }
  }
  "backend" {
    $env:SPRING_PROFILES_ACTIVE = "local"
    Invoke-Gradle @("bootRun")
  }
  "frontend" { Invoke-Npm @("run", "dev") }
  "test" {
    Invoke-Gradle @("test")
    Invoke-Npm @("run", "check")
  }
  "it" { Invoke-Gradle @("recoveryIntegrationTest") }
  "e2e" {
    Invoke-Gradle @("e2eTest")
    Invoke-Npm @("run", "e2e")
  }
}
