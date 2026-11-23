# Recovery Workbench Release Plan v5 — content record (B-DELIVDOC-45, scratch)

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Output: `11 Delivery and operations/Recovery Workbench Release Plan v5.xlsx`, built from
`Recovery Workbench Release Plan v4.xlsx` by `office_write.py copy` and `build_v5.py`.
The source file is not edited. All 1,112 source cells of the five source sheets compare equal
between v4 and v5; version 5 only adds sheets and appends rows.

## Version 5 change

| # | Change | Where | Basis |
|---|---|---|---|
| 1 | Header lines of Template and Rules §R8.1, version, status Draft, tool line | New "Read me" sheet, rows 1-7 | Template and Rules R8.1 |
| 2 | Change log, v4 source row and v5 row "22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" | "Read me" sheet, rows 9-12 | Template and Rules R8.1 |
| 3 | Delivery waves 0 to 4 with business epics, releases, tentative dates, services created, counts, entry and exit | New "Waves" sheet | Architecture v5 slide 38; Template and Rules R5.6 |
| 4 | The 19 services with wave, version 4 release text, first release date, schema, REST base, topic, queue | New "Services by release" sheet | Ownership Map v1 Services sheet; version 4 Modules by release |
| 5 | Gate G7 Contract published | "Gates" sheet, row 11 | Architecture v5 slide 11; R5.4 class C |
| 6 | Release rules 8 to 11: tentative date, wave of each release, one creation per service, contract first | "Release rules" sheet, rows 12-15 | Architecture v5 slides 11, 38; U7; DL48 |
| 7 | Note rows: tentative dates, waves, owners, counts | "Releases" rows 13-16; "Modules by release" row 24; "Calendar" row 53 | DL48; AGENTS.md rule 4 |

Kept unchanged: the eight releases E1 to E8 and every date; the Features, Stories, Status and
"Roles that receive real users" values; the 19 module rows and their "Delivered in" text; gates
G1 to G6; the 48 calendar rows; release rules 1 to 7.

## Wave map used

| Wave | Business epics | Releases | Release dates (tentative) | Services created | Count |
|---|---|---|---|---|---|
| 0 | Platform and NF | None, before E1 | Before the E1 go decision, 27 November 2026 | None (seven platform epics) | 0 |
| 1 | EP01 | E1 | 30 November 2026 | P1, P2, P3, P4, P5, P6, P7, P9, P10 | 9 |
| 2 | EP02, EP03 | E2, E3 | 31 December 2026; 31 January 2027 | P8, S2, S5, S8 | 4 |
| 3 | EP04, EP05 | E4, E5 | 28 February 2027; 31 March 2027 | S1, S3, S4, S6 | 4 |
| 4 | EP06, EP07, EP08 | E6, E7, E8 | 30 April 2027; 31 May 2027; 30 June 2027 | S7, S9 | 2 |

The horizon of U7 holds: eight monthly releases from 30 November 2026 to 30 June 2027, which is
eight calendar months, and all five waves land inside it.

## Open points raised by this work package

| ID | Point | Severity |
|---|---|---|
| CG-B-DELIVDOC-45-1 / ASM-B-DELIVDOC-45-1 | Wave boundary against monthly releases | P2 |
| CG-B-DELIVDOC-45-2 / ASM-B-DELIVDOC-45-2 | No Wave 0 row or platform completion date | P2 |
| CG-B-DELIVDOC-45-3 / ASM-B-DELIVDOC-45-3 | No contract gate and no named contract approver | P2 |
| CG-B-DELIVDOC-45-4 / ASM-B-DELIVDOC-45-4 | Monolith-era feature and story counts | P3 |
| CG-B-DELIVDOC-45-5 / ASM-B-DELIVDOC-45-5 | No owner per release | P3 |
| CG-B-DELIVDOC-45-6 / ASM-B-DELIVDOC-45-6 | No status or approval | P3 |
| CG-B-DELIVDOC-45-7 / ASM-B-DELIVDOC-45-7 | No change log or tool line in the source | P3 |
| CG-B-DELIVDOC-45-8 / ASM-B-DELIVDOC-45-8 | S4 notice approval in E2 against Wave 3 creation | P2 |

## Sources read

- `11 Delivery and operations/Recovery Workbench Release Plan v4.xlsx`
- `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, R3, R5, R8, R9)
- `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 11, 38, 39, 41)
- `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`
- `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` and `_work/msr/plan/ownership.json`
- `_work/msr/plan/split_plan.json` (stats), `_work/msr/plan/ids.json`
