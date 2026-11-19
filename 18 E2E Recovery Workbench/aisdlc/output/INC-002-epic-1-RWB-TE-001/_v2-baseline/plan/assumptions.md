# Assumptions — RWB-TE-001 plan

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-008` | The 21 Tier 1 ACE tables are at the baseline head in DEV/SIT. | E1-069 | BND-6's allowed list may be stale; update the map, not the rule. |
| `ASM-016` | The 30 view names are the allowed source objects in `recovery-modules.yaml`. | E1-069; ADR-010 | Add the missing view; no code change. |
| `L-RCV-03` | No question was asked; BND-6 is taken from E1-069 and ADR-010. | No-question rule | A missing rule would be found at the plan gate. |
| `L-RCV-04` | The existing BND-1..BND-5 implementation is preserved; only BND-6 is new. | Implementation evidence | A re-implementation would need a new plan, not this one. |

No question was asked. Open items go to `docs/open-items.md`.
