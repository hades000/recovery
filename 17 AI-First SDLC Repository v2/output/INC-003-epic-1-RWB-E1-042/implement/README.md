# Preserved implementation — RWB-E1-042 (INC-003)

| Field | Value |
|---|---|
| Story | `RWB-E1-042` Central configuration service and parameter catalog |
| Original pack | `E1-042 Migration and Clarifications`, 10 November 2026 |
| Preserved on | 16 November 2026 |
| Status | Implemented — migration applied and tested |
| Baseline fit | The pack uses `${recoverySchema}` and schema `recovery`, which is correct for document set v14. No change is needed for D-RCV-35. |

## Files

| Path | Purpose |
|---|---|
| `sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` | The D-RCV-28 single migration: DDL plus seed |
| `sql/V042_1__parameter_catalog.sql` | Review copy (DDL split) — not committed |
| `sql/V042_2__parameter_seed.sql` | Review copy (seed split) — not committed |
| `config/parameter-catalog.csv` | Bootstrap catalog input, 13 rows |
| `config/messages-e1-042.csv` | Fixed message catalog for the temporary resolver |
| `tests/test_migrations.sh` | PostgreSQL verification: clean install, re-run, baseline overlap, negative tests, deployment guard |
| `evidence/migration-test-output.txt` | Verification output |
| `tools/Generate-ParameterSeed.ps1` | Regenerates the seed from the CSV |
| `tools/Assemble-V0042.ps1` | Builds the consolidated migration |

## Evidence summary

- The consolidated migration is the one to commit. The two split files fail the D-RCV-28 one-file-per-story
  rule; they are review copies only.
- The migration is guarded with `CREATE TABLE IF NOT EXISTS` and `DO` blocks because V0001 already
  creates `parameter_catalog` and `parameter_value` from Physical Schema v6.
- The schema is `${recoverySchema}` throughout; the Flyway property is
  `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}`.
- The pack's open items (`OI-E1-042-001..004`, `-009`) are carried into the story's spec clarification
  log and `docs/open-items.md`; none blocks the build.

## What the v2 run adds

`../specify/spec.md` and `../plan/plan.md` re-state the story against the 16 November baseline
(D-RCV-35/36, schema `recovery`, 72-story index). The implementation files above are the evidence; the
new spec/plan do not rewrite them.
