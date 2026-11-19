# =============================================================================
# RWB-E1-042 - ParameterSeedGenerator (reference implementation)
# =============================================================================
# Reads config/parameter-catalog.csv and writes V042_2__parameter_seed.sql.
# The production build uses the Java ParameterKeysGenerator / ParameterSeedGenerator;
# this PowerShell script is the reproducible reference used for this pack.
#
# Usage:
#   pwsh -File .\tools\Generate-ParameterSeed.ps1
#   pwsh -File .\tools\Generate-ParameterSeed.ps1 -CatalogPath ..\config\parameter-catalog.csv
# =============================================================================

[CmdletBinding()]
param(
    [string]$CatalogPath,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
if ([string]::IsNullOrWhiteSpace($CatalogPath)) {
    $CatalogPath = Join-Path $scriptRoot '..\config\parameter-catalog.csv'
}
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $scriptRoot '..\sql\V042_2__parameter_seed.sql'
}

function ConvertTo-SqlString {
    param([AllowNull()][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return 'NULL' }
    return "'" + $Value.Trim().Replace("'", "''") + "'"
}

function ConvertTo-SqlNullableString {
    param([AllowNull()][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return 'NULL' }
    return ConvertTo-SqlString $Value
}

function ConvertTo-SqlBool {
    param([AllowNull()][string]$Value)
    if ($null -ne $Value -and $Value.Trim().ToLowerInvariant() -eq 'true') { return 'true' }
    return 'false'
}

$requiredColumns = @(
    'key','kind','value_type','unit','min_value','max_value','default_value','scope',
    'required','owner_role','environments','used_by','secret','description'
)

if (-not (Test-Path -LiteralPath $CatalogPath)) {
    throw "Catalog file not found: $CatalogPath"
}

$rows = @(Import-Csv -LiteralPath $CatalogPath)
if ($rows.Count -eq 0) { throw "Catalog file has no data rows: $CatalogPath" }

$header = @($rows[0].PSObject.Properties.Name)
foreach ($column in $requiredColumns) {
    if ($header -notcontains $column) { throw "Catalog file is missing column '$column'." }
}

$seen = @{}
foreach ($row in $rows) {
    $key = [string]$row.key
    if ([string]::IsNullOrWhiteSpace($key)) { throw 'A catalog row has an empty key.' }
    if ($seen.ContainsKey($key)) { throw "Duplicate catalog key: $key" }
    $seen[$key] = $true

    if ($row.scope -notin @('GLOBAL','PRODUCT')) { throw "Invalid scope '$($row.scope)' for $key." }
    if ($row.kind -notin @('BUSINESS','ENVIRONMENT')) { throw "Invalid kind '$($row.kind)' for $key." }
    if ($row.value_type -notin @('STRING','INTEGER','DECIMAL','BOOLEAN','DATE','TIME','DURATION','CODE','CODE_LIST','JSON')) {
        throw "Invalid value_type '$($row.value_type)' for $key."
    }
    if ($row.required -notin @('true','false')) { throw "Invalid required '$($row.required)' for $key." }
    if ($row.secret -notin @('true','false')) { throw "Invalid secret '$($row.secret)' for $key." }
    if ($row.secret -eq 'true' -and -not [string]::IsNullOrWhiteSpace($row.default_value)) {
        throw "Secret $key must not have a default_value."
    }
}

$nilUuid = '00000000-0000-0000-0000-000000000000'
$validFrom = '2026-11-30'
$approvedAt = '2026-11-30 00:00:00+07'

$catalogBlocks = New-Object System.Collections.Generic.List[string]
foreach ($row in $rows) {
    $catalogBlocks.Add(@"
    ($(ConvertTo-SqlString $row.key),
     $(ConvertTo-SqlString $row.kind), $(ConvertTo-SqlString $row.value_type), $(ConvertTo-SqlNullableString $row.unit), $(ConvertTo-SqlNullableString $row.min_value), $(ConvertTo-SqlNullableString $row.max_value), $(ConvertTo-SqlNullableString $row.default_value),
     $(ConvertTo-SqlString $row.scope), $(ConvertTo-SqlBool $row.required), $(ConvertTo-SqlString $row.owner_role), $(ConvertTo-SqlNullableString $row.environments),
     $(ConvertTo-SqlNullableString $row.used_by), $(ConvertTo-SqlBool $row.secret),
     $(ConvertTo-SqlString $row.description),
     '$nilUuid'::uuid)
"@)
}

$valueRows = New-Object System.Collections.Generic.List[string]
foreach ($row in $rows) {
    if ($row.scope -ne 'GLOBAL') { continue }
    if ($row.secret -eq 'true') { continue }
    if ([string]::IsNullOrWhiteSpace($row.default_value)) { continue }
    if ([string]::IsNullOrWhiteSpace($row.environments)) { continue }

    foreach ($environment in ($row.environments -split ',')) {
        $env = $environment.Trim()
        if ([string]::IsNullOrWhiteSpace($env)) { continue }
        $valueRows.Add("    ($(ConvertTo-SqlString $row.key), $(ConvertTo-SqlString $env), $(ConvertTo-SqlString $row.default_value))")
    }
}

$sql = New-Object System.Text.StringBuilder
[void]$sql.AppendLine('-- Story: RWB-E1-042')
[void]$sql.AppendLine('-- Migration: parameter catalog seed (generated)')
[void]$sql.AppendLine('-- Schema: ${recoverySchema}')
[void]$sql.AppendLine('--')
[void]$sql.AppendLine('-- REVIEW COPY. D-RCV-28 requires one migration per story named')
[void]$sql.AppendLine('-- V<seq>__<story>_<name>.sql. Commit the consolidated')
[void]$sql.AppendLine('-- V0042__rwb_e1_042_parameter_catalog_and_seed.sql unless a migration-lint')
[void]$sql.AppendLine('-- exception is approved for the split. See section 2 of the clarification pack.')
[void]$sql.AppendLine('--')
[void]$sql.AppendLine('-- Generated from config/parameter-catalog.csv by tools/Generate-ParameterSeed.ps1.')
[void]$sql.AppendLine('-- Do not edit by hand: change the catalog CSV and regenerate this file.')
[void]$sql.AppendLine('--')
[void]$sql.AppendLine('-- Seed provenance. These rows are deployment defaults, not a maker-checker approval')
[void]$sql.AppendLine('-- by a person. The author is the system seed account (the nil UUID); approver_user_id')
[void]$sql.AppendLine('-- stays NULL and approved_at records the release date. The first human load through')
[void]$sql.AppendLine('-- POST /admin/reference-loads with table PARAMETER starts at version 2.')
[void]$sql.AppendLine('--')
[void]$sql.AppendLine('-- Seed set. This bootstrap file carries the rows RWB-E1-042 itself defines, the two')
[void]$sql.AppendLine('-- RWB-E1-002 parameters that precede it, the service-level status list RWB-E1-045')
[void]$sql.AppendLine('-- needs, and the five PRODUCT-scope catalog entries RWB-E1-045 defines. It is not a')
[void]$sql.AppendLine('-- claim to be the full Epic 1 catalog; that is config/parameter-catalog.csv and is')
[void]$sql.AppendLine('-- tracked as OI-E1-042-003. Product-scope rows carry no default by design: their')
[void]$sql.AppendLine('-- values are PRODUCT_PARAMETER rows, not parameter_value rows.')
[void]$sql.AppendLine('')
[void]$sql.AppendLine('INSERT INTO ${recoverySchema}.parameter_catalog')
[void]$sql.AppendLine('    (param_key, kind, value_type, unit, min_value, max_value, default_value,')
[void]$sql.AppendLine('     scope, required, owner_role, environments, used_by, secret, description, created_by)')
[void]$sql.AppendLine('VALUES')
[void]$sql.AppendLine(($catalogBlocks -join ",`r`n"))
[void]$sql.AppendLine('ON CONFLICT (param_key) DO NOTHING;')
[void]$sql.AppendLine('')
[void]$sql.AppendLine('-- Default values, one row per environment the catalog line lists. A repeated run')
[void]$sql.AppendLine('-- inserts nothing: the NOT EXISTS test treats the NULL product_group as one value.')
[void]$sql.AppendLine('INSERT INTO ${recoverySchema}.parameter_value')
[void]$sql.AppendLine('    (param_key, environment, param_value, product_group, version_no, valid_from, valid_to,')
[void]$sql.AppendLine('     status, author_user_id, approver_user_id, approved_at, created_by)')
[void]$sql.AppendLine('SELECT')
[void]$sql.AppendLine('    v.param_key,')
[void]$sql.AppendLine('    v.environment,')
[void]$sql.AppendLine('    v.param_value,')
[void]$sql.AppendLine('    NULL,')
[void]$sql.AppendLine('    1,')
[void]$sql.AppendLine("    DATE '$validFrom',")
[void]$sql.AppendLine('    NULL,')
[void]$sql.AppendLine("    'APPROVED',")
[void]$sql.AppendLine("    '$nilUuid'::uuid,")
[void]$sql.AppendLine('    NULL,')
[void]$sql.AppendLine("    TIMESTAMPTZ '$approvedAt',")
[void]$sql.AppendLine("    '$nilUuid'::uuid")
[void]$sql.AppendLine('FROM (VALUES')
[void]$sql.AppendLine(($valueRows -join ",`r`n"))
[void]$sql.AppendLine(') AS v (param_key, environment, param_value)')
[void]$sql.AppendLine('WHERE NOT EXISTS (')
[void]$sql.AppendLine('    SELECT 1')
[void]$sql.AppendLine('    FROM ${recoverySchema}.parameter_value pv')
[void]$sql.AppendLine('    WHERE pv.param_key = v.param_key')
[void]$sql.AppendLine('      AND pv.environment = v.environment')
[void]$sql.AppendLine('      AND pv.product_group IS NULL')
[void]$sql.AppendLine(');')
[void]$sql.AppendLine('')
[void]$sql.AppendLine('-- Deployment guard. Every required GLOBAL parameter that is not a secret must have')
[void]$sql.AppendLine('-- an approved value for every environment it lists. This is not a substitute for')
[void]$sql.AppendLine('-- ParameterStartupCheck: it catches a missing seed row before the service starts.')
[void]$sql.AppendLine('DO $$')
[void]$sql.AppendLine('DECLARE')
[void]$sql.AppendLine('    missing text;')
[void]$sql.AppendLine('BEGIN')
[void]$sql.AppendLine("    SELECT string_agg(c.param_key || ':' || e.environment, ', ' ORDER BY c.param_key, e.environment)")
[void]$sql.AppendLine('    INTO missing')
[void]$sql.AppendLine('    FROM ${recoverySchema}.parameter_catalog c')
[void]$sql.AppendLine("    CROSS JOIN LATERAL unnest(string_to_array(c.environments, ',')) AS e(environment)")
[void]$sql.AppendLine('    WHERE c.required')
[void]$sql.AppendLine("      AND c.scope = 'GLOBAL'")
[void]$sql.AppendLine('      AND NOT c.secret')
[void]$sql.AppendLine('      AND c.environments IS NOT NULL')
[void]$sql.AppendLine("      AND c.environments <> ''")
[void]$sql.AppendLine('      AND NOT EXISTS (')
[void]$sql.AppendLine('          SELECT 1')
[void]$sql.AppendLine('          FROM ${recoverySchema}.parameter_value pv')
[void]$sql.AppendLine('          WHERE pv.param_key = c.param_key')
[void]$sql.AppendLine('            AND pv.environment = e.environment')
[void]$sql.AppendLine('            AND pv.product_group IS NULL')
[void]$sql.AppendLine("            AND pv.status = 'APPROVED'")
[void]$sql.AppendLine('      );')
[void]$sql.AppendLine('    IF missing IS NOT NULL THEN')
[void]$sql.AppendLine("        RAISE EXCEPTION 'RWB-E1-042 seed incomplete: required parameter has no approved value for %', missing;")
[void]$sql.AppendLine('    END IF;')
[void]$sql.AppendLine('END;')
[void]$sql.AppendLine('$$;')

$directory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $directory)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Resolve-Path -LiteralPath $directory).Path + [System.IO.Path]::DirectorySeparatorChar + (Split-Path -Leaf $OutputPath), $sql.ToString(), $utf8NoBom)

Write-Host "Generated $OutputPath"
Write-Host "  catalog rows : $($rows.Count)"
Write-Host "  value rows   : $($valueRows.Count)"
