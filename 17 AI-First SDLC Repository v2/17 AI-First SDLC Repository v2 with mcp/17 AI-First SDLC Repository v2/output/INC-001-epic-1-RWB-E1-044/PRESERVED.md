# Preserved historical run — RWB-E1-044 (INC-001)

| Field | Value |
|---|---|
| Story | `RWB-E1-044` Database migrations versioned with parameterized schema names |
| Original run | 10 November 2026, recovery repository |
| Preserved on | 16 November 2026 |
| Status | **Planned, not built.** The spec and plan are kept for history. |
| Baseline warning | The plan was written under D-RCV-47 (schema `ace`, `rwb_` prefix). D-RCV-35 and ADR-010 reinstate schema `recovery` and `${recoverySchema}`. **Re-run the spec and plan before build** (`OPEN-036`). |

## Preserved files

| Path | Content |
|---|---|
| `specify/spec.md` | 10 Nov 2026 specification |
| `specify/compliance-validation.md` | Spec gate |
| `specify/contracts/` | API and frontend contracts |
| `plan/plan.md` | 10 Nov 2026 plan (D-RCV-47 basis) |
| `plan/tasks.md` | Tasks |
| `plan/data-model.md` | Data model |
| `plan/tests/scenarios.md` | Scenarios |
| `review/*.md` | Spec and plan gate reviews |

## v2 alignment note

- Migration naming stays `V<seq>__<story>_<name>.sql` (D-RCV-28).
- The schema placeholder reverts to `${recoverySchema}`; the `rwb_` prefix and `ace` schema are removed.
- The Flyway bean still uses its own history table; the baseline is at 0 and `createSchemas(false)`.
- The 21 Tier 1 ACE tables and the 30 views are the read path (D-RCV-35).
- Re-baseline task: `OPEN-036`. Do not copy this plan into a build without it.
