# Story retirement register

Source decisions: D-RCV-35 (ACE DB alignment, U1–U5) and D-RCV-36 (Temporal and Drools, T8). No retired story is rebuilt in this repository.

| Story | Reason | New home | Evidence |
|---|---|---|---|
| `RWB-E1-003` | Data-load story removed by D-RCV-35 U1 | ACE ingestion (RWB-ACE-001) | `docs/retirements/` and the source change register |
| `RWB-E1-004` | Data-load story removed by D-RCV-35 U1 | ACE ingestion (RWB-ACE-001) | `docs/retirements/` and the source change register |
| `RWB-E1-005` | Tracker story removed by D-RCV-35 U5 | Cutover plan, section 8 | `docs/retirements/` and the source change register |
| `RWB-E1-006` | Data-quality load story removed by D-RCV-35 U1 | ACE ingestion checks; daily gate in RWB-E1-015 | `docs/retirements/` and the source change register |
| `RWB-E1-009` | Data-load story removed by D-RCV-35 U1 | ACE ingestion (RWB-ACE-001) | `docs/retirements/` and the source change register |
| `RWB-E1-010` | Tracker story removed by D-RCV-35 U5 | Cutover plan, section 8 | `docs/retirements/` and the source change register |
| `RWB-E1-012` | Tracker-retirement story removed by D-RCV-35 U5 | Cutover plan, section 8 | `docs/retirements/` and the source change register |
| `RWB-E1-029` | Rule-load story retired by D-RCV-36 T8 | RWB-E1-073 | `docs/retirements/` and the source change register |
| `RWB-E1-048` | Rule audit story retired by D-RCV-36 T8 | RWB-E2-041 | `docs/retirements/` and the source change register |
| `RWB-E1-051` | ADF/Control-M story removed by D-RCV-35 U1 | ACE ingestion (RWB-ACE-001) | `docs/retirements/` and the source change register |
| `RWB-TE-005` | Rule-table harness retired by D-RCV-36 T8 | RWB-E1-073 | `docs/retirements/` and the source change register |

`RWB-E1-007` survives as outbound-only adapters; only its inbound file-load part is removed. `RWB-E1-006` survives only as the daily gate in `RWB-E1-015`.
