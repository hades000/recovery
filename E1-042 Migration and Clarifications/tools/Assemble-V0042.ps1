# =============================================================================
# RWB-E1-042 - assemble the D-RCV-28 compliant single migration
# =============================================================================
# Concatenates the review-copy split files into one migration with one story
# key, so the migration lint has one file per story.
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Assemble-V0042.ps1
# =============================================================================

[CmdletBinding()]
param(
    [string]$DdlPath,
    [string]$SeedPath,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
if ([string]::IsNullOrWhiteSpace($DdlPath))    { $DdlPath    = Join-Path $scriptRoot '..\sql\V042_1__parameter_catalog.sql' }
if ([string]::IsNullOrWhiteSpace($SeedPath))   { $SeedPath   = Join-Path $scriptRoot '..\sql\V042_2__parameter_seed.sql' }
if ([string]::IsNullOrWhiteSpace($OutputPath)) { $OutputPath = Join-Path $scriptRoot '..\sql\V0042__rwb_e1_042_parameter_catalog_and_seed.sql' }

$ddl = Get-Content -LiteralPath $DdlPath -Raw
$seed = Get-Content -LiteralPath $SeedPath -Raw

$ddlStart = $ddl.IndexOf('CREATE TABLE IF NOT EXISTS')
if ($ddlStart -lt 0) { throw "DDL body not found in $DdlPath" }
$ddlBody = $ddl.Substring($ddlStart)

$seedStart = $seed.IndexOf('-- Seed provenance.')
if ($seedStart -lt 0) { throw "Seed body not found in $SeedPath" }
$seedBody = $seed.Substring($seedStart)

$header = @'
-- Story: RWB-E1-042
-- Migration: parameter catalog, parameter value table and catalog seed
-- Schema: ${recoverySchema}
--
-- Consolidated per D-RCV-28: one migration file for RWB-E1-042. It contains the
-- DDL from V042_1__parameter_catalog.sql and the generated seed from
-- V042_2__parameter_seed.sql. The split files are review copies only; commit this
-- file unless a migration-lint exception is approved for the split.
--
-- Definition source: Recovery Workbench Physical Schema v4.sql, parameter_catalog and
-- parameter_value. Parameter keys are the business names; no key is a table name.
--
-- Baseline note. RWB-E1-001 V0001__rwb_e1_001_recovery_schema.sql is written from the
-- Physical Schema and already creates both tables. This file is therefore guarded: it
-- creates what is absent and then adds the E1-042 constraints, foreign key, uniqueness
-- rules and indexes only when they are absent. On a schema built without the baseline it
-- creates the complete E1-042 definition. The drift check remains the control that an
-- environment matches the migrations.

'@

$output = $header + $ddlBody.TrimEnd() + "`r`n`r`n" + $seedBody.TrimStart()
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path (Resolve-Path -LiteralPath (Split-Path -Parent $OutputPath)).Path (Split-Path -Leaf $OutputPath)), $output, $utf8NoBom)

Write-Host "Assembled $OutputPath"
Write-Host "  bytes: $((Get-Item -LiteralPath $OutputPath).Length)"
