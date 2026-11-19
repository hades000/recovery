# Assumptions — RWB-E1-042 specification

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-009` | The 10 November 2026 migration pack is the implemented evidence for this story. | `E1-042 Migration and Clarifications`; preserved under `../implement/` | Re-specify from the source story. |
| `ASM-011` | The four extension-table names are not used by this story. | D-RCV-35 U3 | None; this story touches only parameter tables. |
| `ASM-015` | Decision-log retention is 10 years; this story does not set it. | Controls Catalog v3 | None; a compliance change, not a code change. |
| `L-RCV-03` | The six Temporal/Drools parameters are taken from D-RCV-36 §3.1. | D-RCV-36 | A missing key would fail the catalog-completeness build check; fix the catalog, not the code. |

No question was asked. Any further ambiguity goes to `docs/open-items.md`, not to the user.
