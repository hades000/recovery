# Edit log — B-REQ-SPEC-27

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Work package: B-REQ-SPEC-27, Recovery Workbench Functional Specifications by Module, next version.
Decision: D-RCV-60 microservice realignment.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.
Agent: aisdlc-msr-worker. Fanout 0, no subagents used.

## Files written

- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P1 Recovery data engine v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P2 Integration v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P3 Case and workflow v5.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P4 Access and administration v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P5 Document hub v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P6 Communications v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P7 Decision center and log v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P8 Payments and posting v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P9 Reporting v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD P10 Agent runtime v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S1 Valuation and route v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S2 TDR, settlement and deed in lieu v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S3 Guarantees and guarantors v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S4 Litigation and enforcement v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S5 Assets and auction v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S6 Debt sale v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S7 Write-off and recovery v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S8 Deviation handling v4.md`
- `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v7/Recovery Workbench FSD S9 Partner management v4.md`
- `_work/msr/docs/B-REQ-SPEC-27/analyse.py`
- `_work/msr/docs/B-REQ-SPEC-27/analysis.json`
- `_work/msr/docs/B-REQ-SPEC-27/dp_evidence.py`
- `_work/msr/docs/B-REQ-SPEC-27/dp.json`
- `_work/msr/docs/B-REQ-SPEC-27/build_fsd_v7.py`
- `_work/msr/docs/B-REQ-SPEC-27/verify.py`
- `_work/msr/gaps/B-REQ-SPEC-27.jsonl`
- `_work/msr/assumptions/B-REQ-SPEC-27.jsonl`
- `_work/msr/editlog/B-REQ-SPEC-27.md`

No source file was edited. `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6`
was read only; the whole folder was copied into the v7 folder with `compat/office_write.py copy`, and the 19 new
file versions were then written inside the copy. The v7 folder therefore holds the v6 text of every module next to
its new version, as the Technical Specifications by Module v6 folder does.

## What was done

1. Read Template and Rules sections R1, R3, R5, R8 and R9, the Architecture v5 text extract (slides 13, 14 and 41),
   the Temporal and Drools text extract, `plan/ownership.json`, the Ownership Map v1 workbook (Services, Tables,
   Endpoints, Events, Workflows and activities, Jobs, Parameters and Rulings sheets), `plan/split_plan.json` (stats
   and legacy) and `plan/ids.json`. No new decision ID was needed: D-RCV-60, ADR-013 to ADR-023 and DL44 to DL49
   already cover the realignment.
2. Copied the v6 folder to `… by Module v7` with `compat/office_write.py copy`, then wrote 19 new file versions:
   v3 to v4 for 18 files and v4 to v5 for FSD P3, which is the version the source folder carries.
3. Each file starts with the two header lines of Template and Rules R8.1 and keeps the whole source text below them.
   The only changes are additions:
   - `| Service | <code> <service name> |` inserted in the document control table, and `| Change | <version>,
     22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |` appended to it;
   - `Document ID` and `Version` advanced to the new version and `Status` set to Draft (no approval is recorded:
     ASM-3046);
   - one `### Note, Architecture v5 (D-RCV-60)` block before `## Existing capability check`, with the service
     identity from the Ownership Map v1 Services sheet and Architecture v5 slide 41 (service, what it owns in
     Architecture v5, service epic, wave, schema, REST base, Kafka topic, event names, task queue, Java package),
     the ownership ruling wording of Template and Rules §R3, and the DP-17 and DP-10 sentences where the module
     text still carries a data-lake or Quartz marker.
4. `verify.py` compares every new file with its source: the two header lines and the note block removed, and the
   five document control rows projected out, the two texts are identical. Result: 19 of 19 files OK, no other line
   changed, added or lost.
5. Nothing was invented: every service value comes from the Ownership Map v1 Services sheet and Template and Rules
   R4, the "owns" phrase from Architecture v5 slide 41, every owner reference from the map and its rulings, and the
   missing approval and the two stale mechanisms are recorded as gap and assumption rows.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-SPEC-27 --quick` — see `## Check result`.

## Registers

- Gap rows written: 3 (`GAP-1860` to `GAP-1862`).
- Assumption rows written: 7 (`ASM-3046` to `ASM-3052`).
- Gaps cited in the module files: `GAP-1861` (data lake, seven modules), `GAP-1862`
  (Quartz, five modules). `GAP-1860` is carried by ASM-3049.
- Assumptions cited in the module files: `ASM-3046` (Draft status).

## Check result

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-SPEC-27 --quick` on 22 November 2026:

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

The wider checks were also run over the 48 files this work package writes: C01, C14, C16, C17 and C20 pass with no
findings. C19 is a run-wide queue check and reports other work packages that have not run yet; it reports nothing for
B-REQ-SPEC-27 — both planned outputs (the v7 folder and this log) exist and every file of the folder carries the
D-RCV-60 change row.
