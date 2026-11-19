# Preserved historical run — RWB-E1-043 (INC-008)

| Field | Value |
|---|---|
| Story | `RWB-E1-043` Reference data service with versioned tables |
| Original run | 10 November 2026, recovery repository (original folder `INC-009-epic-1-RWB-E1-043`) |
| Preserved on | 16 November 2026 |
| Status | **Planned, not built.** The spec and plan are kept for history. |
| Baseline warning | The plan predates D-RCV-35/36 and the 16 November schema reversal. **Re-run the spec and plan before build** (`OPEN-036`). |

## Preserved files

| Path | Content |
|---|---|
| `specify/spec.md` | 10 Nov 2026 specification |
| `specify/compliance-validation.md` | Spec gate |
| `plan/plan.md` | 10 Nov 2026 plan |
| `plan/tasks.md` | Tasks |
| `plan/data-model.md` | Data model |
| `plan/tests/scenarios.md` | Scenarios |
| `plan/review/plan-gate-review.md` | Plan gate |

## Notes

- The original run ID was `INC-009`; the v2 index numbers by Build Sequence v6, where `RWB-E1-043` is
  item 8. The old path is recorded here and in the traceability matrix.
- The reference-data service is unchanged in principle: versioned tables, effective dates,
  maker-checker, load/rollback. The schema and read path are re-based by D-RCV-35.
