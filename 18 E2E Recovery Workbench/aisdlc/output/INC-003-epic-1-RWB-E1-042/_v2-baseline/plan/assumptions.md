# Assumptions — RWB-E1-042 plan

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-009` | The 10 November 2026 migration pack is the build baseline. | Preserved evidence | Re-run the spec and plan; do not rewrite the SQL. |
| `ASM-011` | The four extension-table names are not used by this story. | D-RCV-35 U3 | None; this story touches only parameter tables. |
| `ASM-015` | Decision-log retention is 10 years. | Controls Catalog v3 | A compliance change, not a code change. |
| `L-RCV-03` | The six Temporal/Drools parameters come from D-RCV-36 §3.1. | No-question rule | A missing key fails the catalog-completeness check; fix the catalog. |

No question was asked. Open items go to `docs/open-items.md`.
