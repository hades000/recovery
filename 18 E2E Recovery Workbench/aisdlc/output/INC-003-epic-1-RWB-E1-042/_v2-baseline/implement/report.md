# Implementation evidence — RWB-E1-042

| Field | Value |
|---|---|
| Story | `RWB-E1-042` Central configuration service and parameter catalog |
| Source | `E1-042 Migration and Clarifications`, 10 November 2026 |
| Preserved | 16 November 2026 |
| Status | Implemented — migration applied and tested |
| Baseline | Schema `recovery`, `${recoverySchema}`, Physical Schema v6 |

## Evidence

| Evidence | Path | Result |
|---|---|---|
| Consolidated migration | `sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` | 24,495 bytes; one file; `-- Story: RWB-E1-042` |
| Catalog input | `config/parameter-catalog.csv` | 13 rows (plus 6 v2 rows in the plan) |
| Message catalog | `config/messages-e1-042.csv` | Fixed text for the temporary resolver |
| Migration test script | `tests/test_migrations.sh` | Clean, re-run, baseline overlap, 8 negatives, deployment guard |
| Test output | `evidence/migration-test-output.txt` | Green |
| Seed generator | `tools/Generate-ParameterSeed.ps1` | Regenerates the seed from the CSV |
| Assembler | `tools/Assemble-V0042.ps1` | Builds the consolidated migration |

## What the evidence proves

- The migration applies on an empty database and on a simulated V0001 baseline.
- The migration is idempotent on re-run.
- The split review files (`V042_1`, `V042_2`) are not committed; the consolidated file meets
  D-RCV-28.
- The schema placeholder is `${recoverySchema}`; the Flyway property is
  `spring.flyway.placeholders.recoverySchema=${RWB_SCHEMA}`.
- The negative cases fail with the expected message, not a generic error.

## Open items (non-blocking)

| ID | Item | Owner |
|---|---|---|
| `OI-E1-042-001` | TC-E1-042-12 is Blocked until E1-022/E1-037 deliver the 403 path; do not mock a role. | QA |
| `OI-E1-042-002` | The two-file split is a review copy; if the team requires it, record a lint exception. | Recovery tech lead |
| `OI-E1-042-003` | The full Epic 1 catalog replaces the bootstrap CSV; rerun both tools. | RW-COE |
| `OI-E1-042-004` | The message table is unowned; the fixed-text resolver is temporary. | BA |
| `OI-E1-042-009` | The Flyway property must be `recoverySchema`, not `schema`. | ACE platform |

## v2 note

The 16 November re-baseline (D-RCV-35/36) does not invalidate this evidence. The story has no source
load, no view, no Temporal call and no Drools call. The six new parameters are catalog rows added by
the plan; the migration's seed is regenerated from the CSV, so no SQL is hand-edited.
