# Assumptions — CONTEXT-20261116

The user asked that the context, specify and plan phases run without questions. This register records
every ambiguity and the default that was taken. A later decision or a named owner can replace any row;
none blocks the run.

| ID | Ambiguity | Default taken | Basis | Owner who can change it |
|---|---|---|---|---|
| `ASM-001` | AMIS, RPS, LIT, WIN, GL and COLLINS scores may not all be ingested by ACE yet | Treat as ACE-ingested (Tier 2); `RWB-ACE-001` lists them | D-RCV-35 §2.1 assumption | ACE team lead |
| `ASM-002` | Temporal server and SDK versions are not pinned in the set | Record the approved pinned release at build; no version invented here | ADR-011 | SCB IT |
| `ASM-003` | Temporal closed-workflow retention is 30 days | Use 30 days; confirm with DL26 | D-RCV-36 §3.1 | Compliance |
| `ASM-004` | Availability, RPO/RTO and retention are not signed | Use the NFR v3 design baseline (99.5%, RPO 15 min, RTO 4 h) | NFR v3 | Product Owner |
| `ASM-005` | Thai labels and messages are proposed | English canonical; Thai resource draft | DL10 | BA |
| `ASM-006` | Per-story Jira keys are not all assigned | Local story keys are authoritative; Jira import later | INDEX note | Product Owner |
| `ASM-007` | `RWB-E1-036` has no story file | Do not create it; not in the build sequence | v7/v6 story sets | BA |
| `ASM-008` | The 21 Tier 1 ACE tables may not be at the baseline head in DEV/SIT | Assume they are; E1-069 checks before compiling views | E1-069 precondition | ACE team |
| `ASM-009` | `RWB-E1-042` is the implemented story; `RWB-TE-001` is the implemented enabler | Preserve both and re-specify both | Implementation evidence | Recovery tech lead |
| `ASM-010` | The old 78 specs predate the 16 Nov baseline | Archive them; do not treat them as current | D-RCV-35/36 | Product Owner |
| `ASM-011` | The exact four extension-table names are not final in the narrative | Use the ACE Data Tier Map names; confirm against V0001 | D-RCV-35 U3 | Data architect |
| `ASM-012` | `receipt` and `notice` dispatch channels are not fully specified for Epic 1 | Implement the letter path; SMS/LINE in Epic 2 | RWB-E2-022 | BA |
| `ASM-013` | Figma is not available | Use the screen inventory and screen specifications; mark visual values approximate | Known limit | UX |
| `ASM-014` | The test count for a Drools package is a parameter, not a fixed number in the story | Use `rules.testcases.min=50` | D-RCV-36 §3.1 | Risk |
| `ASM-015` | The decision-log retention period is open | Use 10 years for case and decision records | Controls Catalog v3 | Compliance |
