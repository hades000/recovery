# Increment Card — INC-019-epic-1-RWB-E1-014

**RWB-E1-014 — Decision log copy to the data lake**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-019` |
| Title | Decision log copy to the data lake |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-014` |
| RUN_ID | `INC-019-epic-1-RWB-E1-014` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Should |
| Build order | 19 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-056, RWB-E1-017 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **the decision log copied to the data lake each night, with a retention rule applied to the copy**, so that **reporting reads the log without touching the live log and nothing in the copy is kept longer than its rule**.

**Business outcome:** Reporting, audit sampling and model feedback need the full decision history, and queries against the live log slow the write path that every action depends on (ADR-009). A nightly copy that matches the live log on row count and last hash gives Power BI and audit one checked source (REC-08). The copy carries its own retention rule, so the lake does not keep decisions longer than the bank schedule allows. Serves REQ-DRI-009 and REQ-RDF-013; measure: copy matched on count and last hash on 99 percent of days (FSD P1 A2.20.1).

**Main flow:**
1. Quartz: starts JOB-13 Decision log copy at 01:00 for business date D (the previous calendar day).
2. DecisionLogLakeCopyService: reads the watermark (last copied entry hash and cumulative count) from lake_copy_watermark.
3. DecisionLogLakeCopyService: calls DecisionLogExport.head() and fixes the cut-off: the live count and last entry hash at start.
4. DecisionLogLakeCopyService: calls DecisionLogExport.entriesAfter(watermarkHash, 5000) in chain order until it reaches the cut-off hash.
5. LakeFileWriter: writes the entries to `decision-log/business_date=D/` as Parquet files and writes `_manifest.json` with the row count, first hash, last hash and cumulative count.
6. LakeCopyReconciler: reads the manifest back from the lake and compares the cumulative count and last hash with the cut-off (REC-08, tolerance zero).

**Acceptance criteria:**
- AC1: Daily copy
- AC2: Retention rule
- AC3: A copy that does not match is not published
- AC4: A repeat run for the same date writes no duplicates
- AC5: The decision log interface is unavailable
- AC6: A day with no new decisions
- AC7: Two runs at the same time
- AC8: A partition exactly at its retention age is kept

**Out of scope:**
- Retention of the live decision log (NFR-030, DL26) and the hash chain check (JOB-14, RWB-TE-008).
- Operations reports built on the copy (FEAT-RPT-04, Epic 2).
- Logging each read of the lake copy to the access log (REQ-ACA-006, RWB-E1-039).
- The retention rule table and the data store retention job (RWB-E1-017).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-014-decision-log-copy-to-the-data-lake-v1.md` |
| Requirement IDs | REQ-DRI-009, REQ-RDF-013 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-DRI-009, REQ-RDF-013) |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load | Runs JOB-13, reads through DecisionLogExport, writes the lake files and the watermark |
| SY-DECLOG, decision log writer | Owns the live log; not called for writes in this story |
| RW-PLATADM, platform administrator | Reruns JOB-13 (Platform administration U) |
| RW-DATASTEW, data steward | Reads the job result and the break (Platform administration R) |
| RW-COE, RW-AUDIT, RW-COMPLY | Read the job monitor (Platform administration R); read the lake copy in Power BI |
| RW-BIANAL, reporting and BI analyst | Reads the lake copy for reporting |

## Contract extract

**Job** | Item | Value | |---|---| | Trigger | Quartz cron `0 0 1 * * ?`, Asia/Bangkok | | Job name | JOB-13 Decision log copy | | Schedule | Nightly 01:00; before JOB-15 at 01:30 and JOB-14 at 02:00 | | Input | Decision log entries after the watermark hash, up to the head at job start, through DecisionLogExport | | Output | Parquet files and `_manifest.json` under `decision-log/business_date=YYYY-MM-DD/` in the INT-19 intake container; the watermark row; checks on the job run (rows, REC-08 result, partitions archived, rule version) | | Events published | None. JOB-13 publishes no event in events.txt | | Idempotency key | Business date. A rerun for a date rewrites the same partition from the same chain range | | Restart behavior | A failed run leaves the watermark unchanged; the next run or a manual rerun starts from the watermark. Quartz `@DisallowConcurrentExecution` | **Published int…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: the retention period, page size, file size and lake path are data rows or properties. - No personal data in logs, tests or prompts. Test entries use synthetic case IDs and synthetic hashes; inputs_ref holds references only. - No read of another module's tables: decision_log_entry is read only through DecisionLogExport. - The job never writes, updates or deletes a live decision log entry.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-014-decision-log-copy-to-the-data-lake-v1.md` |
| Specification | `output/INC-019-epic-1-RWB-E1-014/specify/spec.md` |
| Compliance validation | `output/INC-019-epic-1-RWB-E1-014/specify/compliance-validation.md` |
| Agent run log | `output/INC-019-epic-1-RWB-E1-014/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-019-epic-1-RWB-E1-014/plan/` |
| Implementation evidence | `output/INC-019-epic-1-RWB-E1-014/implement/` |
| API / functional test reports | `output/INC-019-epic-1-RWB-E1-014/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-019-epic-1-RWB-E1-014/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-014-decision-log-copy-to-the-data-lake-v1.md` |
| Output run | `output/INC-019-epic-1-RWB-E1-014/` |

