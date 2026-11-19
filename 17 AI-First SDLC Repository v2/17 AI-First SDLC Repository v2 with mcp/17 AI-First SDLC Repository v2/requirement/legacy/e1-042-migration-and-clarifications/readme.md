<!-- source: E1-042 Migration and Clarifications/README.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `E1-042 Migration and Clarifications/README.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-042 — migration and clarification pack

Start with **`RWB-E1-042 Clarification Pack.md`**. It answers the review points and explains how to apply the SQL.

## Quick start

1. **Read** `RWB-E1-042 Clarification Pack.md`, sections 1–2.
2. **Commit** `sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` (the D-RCV-28 single migration).
3. **Configure** `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}`.
4. **Verify** with `tests/test_migrations.sh` or the post-migration queries in §8.

The files `sql/V042_1__parameter_catalog.sql` and `sql/V042_2__parameter_seed.sql` are the requested review copies. They fail the D-RCV-28 naming rule because it requires one file per story; see §2.1.

## Regenerate the seed

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Generate-ParameterSeed.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Assemble-V0042.ps1
```

The source is `config/parameter-catalog.csv`. When the full Epic 1 catalog arrives, replace this bootstrap CSV, rerun both commands, and commit the regenerated `V0042`.
