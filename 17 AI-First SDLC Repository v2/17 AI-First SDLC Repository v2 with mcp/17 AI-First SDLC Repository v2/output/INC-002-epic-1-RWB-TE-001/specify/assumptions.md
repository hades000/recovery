# Assumptions — RWB-TE-001 specification

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-008` | The 21 Tier 1 ACE tables are at the baseline head in DEV/SIT. | E1-069 precondition | BND-6's view allow-list may miss a view; update the map, not the rule. |
| `ASM-011` | The four extension-table names come from the ACE Data Tier Map. | D-RCV-35 U3 | The map's extension list changes; no code change in this story. |
| `ASM-016` | The 30 view names are the allowed source objects in `recovery-modules.yaml`. | E1-069; ADR-010 | The BND-6 allow-list is incomplete; update it with the view story. |
| `L-RCV-03` | No question was asked; BND-6 is taken from E1-069 and ADR-010. | No-question rule | A missing rule would be found at the spec gate; add it there. |

No question was asked. Any further ambiguity goes to `docs/open-items.md`.
