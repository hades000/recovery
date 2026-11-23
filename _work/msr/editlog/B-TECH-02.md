# Edit log — WP B-TECH-02 (Recovery Workbench Target Architecture next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Target Architecture v6.pptx` (all 18 slides), the converted text
under `_work/msr/extract/` (`B-TECH-01-ta6/Recovery Workbench Target Architecture v6.md`), `22 Microservice Realignment/Recovery
Workbench Microservice Story Template and Rules v1.md` (§R1, §R3, §R5, §R8, §R9), `_work/msr/plan/ownership.json`,
`22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` (Read me, Services, Tables, Endpoints,
Events, Workflows and activities, Jobs, Parameters, Rulings), `22 Microservice Realignment/Recovery Workbench Architecture v5
Text Extract v1.md` (slides 2 to 13, 20 to 25, 29 to 34, 38 to 44), `22 Microservice Realignment/Recovery Workbench Temporal and
Drools Design Text Extract v1.md` (slides 11 to 13), `_work/msr/plan/split_plan.json` (stats and legacy only) and
`_work/msr/plan/ids.json`. Nothing read was edited; the v6 deck was opened read-only and copied, never written.

## Files written

- 05 Technical architecture/Recovery Workbench Target Architecture v7.pptx
- _work/msr/gaps/B-TECH-02.jsonl
- _work/msr/assumptions/B-TECH-02.jsonl
- _work/msr/editlog/B-TECH-02.md

Scratch files under `_work/msr/docs/B-TECH-02/` (build and verification only, not outputs of the run):

- _work/msr/docs/B-TECH-02/source-v6-pptx-text.txt
- _work/msr/docs/B-TECH-02/slides.md
- _work/msr/docs/B-TECH-02/polish.py
- _work/msr/docs/B-TECH-02/verify-order.txt
- _work/msr/docs/B-TECH-02/verify-text.txt

## 1. How the next version was produced

`Recovery Workbench Target Architecture v6.pptx` was copied to v7 with `compat/office_write.py copy`, and the copy was the
only file changed. The eleven new slides were added to the copy with `compat/office_write.py pptx-append` from
`_work/msr/docs/B-TECH-02/slides.md`, and `polish.py` then set the layout of the new slides to the deck's own style (title
24 pt bold Aptos in 4E297F at the geometry of the source title, the same hairline rule under the title, body 12 pt Aptos)
and moved the read-me slide to position 2 so that the header of Template and Rules §R8.1 stands at the front. Page footers
were renumbered 2 to 29 so that no number repeats. No slide of the source was deleted, reordered or reworded.

**Header, change log and status.** Slide 2 of v7 carries, as its first two lines, the header
`SCB Collections and Recovery. Henka Group, 22 November 2026.` and `(C) Siam Commercial Bank and Henka Pte Ltd`, then the
change-log row `7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`, the
version 6 row that it follows (`6, 16 November 2026, D-RCV-36`), what the version adds, the tentative-dates rule and the
status (Draft, no approval recorded — ASM-3212).

## 2. Fidelity to version 6

The eighteen source slides are present and unchanged, with one exception: the footer number in each (2 to 18 became 3 to 19
because the read-me slide was placed second). Every table, ID, number, date and word of slides 1 to 18 is otherwise as it was,
checked slide by slide in `source-v6-pptx-text.txt` against the deck after the build:

| Source slide | Content | In v7 |
|---|---|---|
| 1 | title, `Henka Group, 16 November 2026` | slide 1, unchanged |
| 2 | the architecture on one page | slide 3, unchanged |
| 3 | goals and constraints, 5 goals and 8 constraints | slide 4, unchanged |
| 4 | 8 architecture principles | slide 5, unchanged |
| 5 | 10 context rows | slide 6, unchanged |
| 6 | the modular monolith, 3 modules and 5 boundary rules | slide 7, unchanged |
| 7 | the ten platform modules, P1 to P10 | slide 8, unchanged |
| 8 | the nine stage modules, S1 to S9 | slide 9, unchanged |
| 9 | case workflow, six steps, CMMN counts 10/30/150/53/448/12 | slide 10, unchanged |
| 10 | the rules engine, 7 rows | slide 11, unchanged |
| 11 | four data tiers, 92 tables, 30 views, 1,366 fields | slide 12, unchanged |
| 12 | security and access, 9 controls, 54 roles | slide 13, unchanged |
| 13 | the agent runtime, 6 parts, L0 to L4 | slide 14, unchanged |
| 14 | environments, DEV/SIT/UAT/PROD, nine pipeline gates | slide 15, unchanged |
| 15 | what each epic adds, E1 to E8 with their dates | slide 16, unchanged |
| 16 | quality targets, 9 rows | slide 17, unchanged |
| 17 | risks, 7 rows | slide 18, unchanged |
| 18 | open architecture decisions, DL03 to DL43 | slide 19, unchanged |

The version 6 statements that the realignment supersedes (one service, one repository, one front end; the modular monolith;
92 tables; the data lake row in the context) therefore stay readable exactly as approved, and each is answered on the new
slides. That reading rule is ASM-3213.

## 3. What version 7 adds (slides 20 to 29)

1. **What the realignment changes, and the ADRs that carry it.** The ten changes of Architecture v5 slide 37 with the ADR
   that carries each: ADR-013 19 services, ADR-014 schema and login per service, ADR-015 Kafka with outbox and inbox,
   ADR-016 the reusable Temporal layer, ADR-017 embedded Drools with the registry in rwb-decision, ADR-018 no data lake,
   ADR-019 the edge, ADR-020 contract-first REST, ADR-021 per-service Flyway, ADR-022 the local decision record plus the
   central ledger, ADR-023 observability per service.
2. **The platform services P1 to P5 and P6 to P10, and what each owns.** One line per service with its code, its name, its
   wave, and the resources its code owns in the Ownership Map (tables, REST operations, events, workflows, jobs), plus the
   naming facts of Rules §R4. The counts are the Map's own: P1 18/18/2/3, P2 3/11, P3 15/22/7/CaseWorkflow/3, P4 5/4/1,
   P5 12/17/2/DocumentIntakeWorkflow/2, P6 3/11/3/NoticeDispatchWorkflow/1, P7 6/19/3/ApprovalWorkflow/3, P8 1/2/3/2,
   P9 3/1/1, P10 8/11/1/AgentRunWorkflow.
3. **The stage services S1 to S9.** The same shape, with the workflow each one owns and the wave of the Ownership Map:
   wave 2 for S2, S5 and S8; wave 3 for S1, S3, S4 and S6; wave 4 for S7 and S9.
4. **Runtime: one case workflow, with a child for each stage.** CaseWorkflow with workflow ID case-{caseId}, the eight stage
   children, the four steps (receive, EvaluateRules, RecordAndApply, wait), the case router and signalWithStart, the kit
   ApprovalWorkflow on rwb-decision, Continue-As-New at each stage end and at least every 28 days, parent close policy
   ABANDON, rules only inside activities, and case state in rwb_case (T1).
5. **The Temporal layer: five levels.** L1 cluster, L2 namespaces, L3 kit, L4 activity contracts, L5 domain workflows, with
   the owner of each level and the six Schedules that replace Quartz. The owner is the Platform team for L1 to L3 through
   RWB-PLT-WF and RWB-PLT-LIB (ASM-3211, GAP-1990).
6. **Kafka.** One topic per service, the shared rwb.decision-record.v1, 12 partitions with replication factor 3 and 7-day
   retention keyed on caseId, CloudEvents 1.0 binary mode, outbox and inbox in one transaction, the retry ladder and the
   dead-letter topic, the bank Kafka platform and the Event Hubs Premium fallback. The shared topic settings are the §R9
   placeholder (GAP-1985; ASM-3206).
7. **The edge.** gateway-bff with the Redis session and the 15-minute idle timeout, the App Gateway routes, one hop with a
   2 s timeout and a breaker per service, and the partner gateway with FAPI 2.0. The owner of the two edge components is
   the placeholder (GAP-1986; ASM-3207).
8. **Data.** One ACE PostgreSQL server, the 30 v_ace_* views read only by rwb-source-data, 19 schemas with one login each,
   no cross-schema joins or keys, Flyway per service, no data lake (INT-19 and INT-20 removed), Blob with WORM, and both
   table counts (GAP-1984; ASM-3205).
9. **Delivery.** Wave 0 and waves 1 to 4 with the nine, four, four and two services of Architecture v5 slide 38 and the
   19 service epics of Rules §R5.1, every release date as the source gives it and marked tentative (ASM-3214),
   and the three open points of this version (GAP-1988, 6 and 7), plus the new Decision Log rows DL44 to DL49
   (ASM-3216).

No value is invented. Every owner is the code of the Ownership Map v1 and `_work/msr/plan/ownership.json` (ASM-3215);
every identifier is copied character for character from Architecture v5, the Temporal and Drools design, Rules §R4, §R5 and
§R8.4, or `ids.json` (ADR-013 to ADR-023, DL44 to DL49).

## 4. Registers

- Gap rows written: **7** candidate rows, `GAP-1984` to `GAP-1990`, in `_work/msr/gaps/B-TECH-02.jsonl`
  (2 Conflict, 1 Ambiguous, 4 Missing; 3 of severity P2 and 4 of P3).
- Assumption rows written: **12** candidate rows, `ASM-3205` to `ASM-3216`, in
  `_work/msr/assumptions/B-TECH-02.jsonl` (9 High, 3 Medium).
- Every one of the 7 gap rows names its assumption, and every citation in the deck resolves to a row: the deck cites
  CG-1 to CG-7 and ASM-1 to ASM-12.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## 5. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-02 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

Report written by the check script: `22 Microservice Realignment/checks/reports/wp-B-TECH-02-20261122-212041.md`
(with the `.json` of the same stamp).
C12 finds no person name and no email address in the files of this WP; C13 finds no issue-tracker reference; C18 finds no
write outside the "Write only" list and no change to a story master. The v6 deck is unchanged on disk.

## 6. Status and boundaries

The deck is issued in **Draft**: no approval is recorded for this run (ASM-3212). No later lifecycle stage was
started. No issue tracker, wiki, repository, Figma or web call was made and no commit was created. The v6 `.docx` of the
same family is outside this work package and was not touched.
