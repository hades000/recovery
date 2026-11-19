# Increment Card — INC-024-epic-1-RWB-TE-008

**RWB-TE-008 — Decision log hash chain check**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-024` |
| Title | Decision log hash chain check |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-008` |
| RUN_ID | `INC-024-epic-1-RWB-TE-008` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P7 Decision center and log |
| Story type | Enabler |
| Priority | Must |
| Build order | 24 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-008, RWB-TE-007 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P7 Decision center and log.

## Scope

**Story:** As an **internal auditor (RW-AUDIT)**, I want **a nightly job that recomputes the whole decision log hash chain, records the result with the last hash, and reports a break to Compliance the same day**, so that **a changed entry is found the day it happens and the log can be relied on in audit**.

**Business outcome:** The decision log is evidence only while nobody can change an entry unseen. The database refuses updates and deletes (RWB-E1-008), but a change made outside the service, for example by a database administrator, is found only by recomputing the chain. This story runs that check as JOB-14 every night after the decision log copy, records each run with its last hash, and tells Compliance of a break, an incomplete run or an intact chain. It meets REQ-DRI-003 and NFR-035 and supports control CTL-06. The measure is a daily check with a same-day report: target 100 percent of nights.

**Main flow:**
1. Quartz: fires JOB-14 at 02:00 Asia/Bangkok for the business date of the previous day.
2. Job (HashChainCheckJob): checks that JOB-13 for the same business date has ended; if not, waits and checks again every 5 minutes until 04:00, then runs and records that JOB-13 had not ended.
3. Job: reads the highest chain_seq at the start and fixes it as the end of the run; entries appended later are checked the next night.
4. Job: calls HashChainVerifier over chain_seq 1 to the end in batches of 1,000, recomputing each entry_hash and checking each prev_hash.
5. Job: counts every entry that fails and keeps the first.
6. Job: writes the job run record with type JOB-14, business date, status and checks: entries checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID, failing count.

**Acceptance criteria:**
- AC1: Chain intact
- AC2: Break
- AC3: A run that stops is reported
- AC4: A rerun gives a new record and no second scheduled run
- AC5: An empty log is intact
- AC6: The job waits for the decision log copy
- AC7: Several changed entries
- AC8: Entries written during the run

**Out of scope:**
- The store, the hash computation and the on-demand verifier (RWB-E1-008).
- The check of each entry returned by an audit query (RWB-E2-005).
- The decision log copy to the data lake (RWB-E1-014, JOB-13).
- Detecting a broken chain as a control breach through the administration screens (Epic 8, FEAT-ADM-10).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-008-decision-log-hash-chain-check-v1.md` |
| Requirement IDs | REQ-DRI-003 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, sections 5.7 and 6.6 |
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
| SY-DECLOG Decision log writer | The job runs under this service identity and reads the log (Decision log C and read through the store) |
| RW-COMPLY Compliance and PDPA officer | Receives every report; owns the job (batch.txt) and its parameters |
| RW-AUDIT Internal audit | Reads the run records (Platform administration R); may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts; reruns the job (Platform administration U) |
| RW-SECADM Security administrator | Receives the break incident with Compliance |

## Contract extract

| Item | Value | |---|---| | Trigger | Quartz cron 0 0 2 * * ? in Asia/Bangkok, after JOB-13 for the same business date | | Job name | JOB-14 Hash chain check | | Schedule | Nightly 02:00; latest start 04:00 | | Input | decision_log_entry in chain_seq order, chain_seq 1 to the highest at start | | Output | Job run record: type JOB-14, businessDate, status, startedAt, endedAt, checks (entriesChecked, lastSeq, lastHash, result, breakSeq, breakEntryId, failingCount, rerun, copyJobEndedAt); reports MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group; incident on a break | | Events published | None from events.txt; the report goes through the ACE notification path | | Idempotency key | Business date plus run number; a rerun adds a record and changes nothing else | | Restart | A failed run is not resumed; a rerun starts again from chain_seq 1 | **GET /api/recovery/v1/admin/jobs** (ow…

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

- No business value in code: times and batch size are parameters. - No personal data in logs, tests or prompts; reports name entry IDs and chain_seq only. - No read of another module's tables; the job reads only decision_log_entry. - The job never writes to decision_log_entry and never repairs an entry. - One canonical form implementation, shared with the store.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-008-decision-log-hash-chain-check-v1.md` |
| Specification | `output/INC-024-epic-1-RWB-TE-008/specify/spec.md` |
| Compliance validation | `output/INC-024-epic-1-RWB-TE-008/specify/compliance-validation.md` |
| Agent run log | `output/INC-024-epic-1-RWB-TE-008/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-024-epic-1-RWB-TE-008/plan/` |
| Implementation evidence | `output/INC-024-epic-1-RWB-TE-008/implement/` |
| API / functional test reports | `output/INC-024-epic-1-RWB-TE-008/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-024-epic-1-RWB-TE-008/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-008-decision-log-hash-chain-check-v1.md` |
| Output run | `output/INC-024-epic-1-RWB-TE-008/` |

