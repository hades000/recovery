# Increment Card — INC-011-epic-1-RWB-E1-007

**RWB-E1-007 — Integration adapters for outbound files**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-011` |
| Title | Integration adapters for outbound files |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-007` |
| RUN_ID | `INC-011-epic-1-RWB-E1-007` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | User story |
| Priority | Must |
| Build order | 11 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-069, RWB-E1-015 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P2 Integration.

## Scope

**Story:** As a **platform administrator (RW-PLATADM)**, I want **one adapter pattern for every outbound file, with the data it reads taken from the ACE views, retry on a schedule held as data and an exception queue with a named owner**, so that **every later outbound file follows one pattern and a failed file is found on the day it fails**.

**Business outcome:** The Workbench loads no source data; ACE ingests every source and the Workbench only sends (D-RCV-35 U1). What remains in P2 is one outbound path for the WIN registered-mail notice file, the reporting extract to the data lake and Power BI, the decision and outcome feed to COLLINS through the lake, and the debt buyer data tape. Each outbound file is built from Workbench tables and the `recovery.v_ace_*` views, sent through the outbox, acknowledged, retried on the schedule held in its interface row, and moved to the exception queue with a task for a named owner after the retry limit. It meets REQ-DRI-006, REQ-DRI-007 and REQ-DRI-008 and serves the FSD P2 measure "outbound items in the exception queue over one day: zero".

**Main flow:**
1. Owning module: writes an outbound file request through `OutboundFiles.enqueue`, for example JOB-10 for the daily WIN notice file (INT-14).
2. System: reads the interface configuration row in force, which names the target, the transport, the attempts, the retry intervals and the owner role.
3. System: builds the file from Workbench tables and, where the file needs source data, from the `recovery.v_ace_*` views; the addressee and address come from `v_ace_contact` by `contact_key`.
4. System: checks `v_ace_batch_status` that the ACE batch for the file's business date is COMPLETE; if it is not, the item is held and no file is built.
5. recovery_svc: writes one outbound_item with an idempotency key, in the same transaction as the request, and stores the built file in the document store.
6. Scheduler: JOB-11 runs every minute; the OutboundSender sends each due item over SFTP and marks it SENT, then ACKNOWLEDGED when the acknowledgment file arrives.

**Acceptance criteria:**
- AC1: One outbound pattern
- AC2: Outbound file reads ACE only through the views
- AC3: Retry and exception queue
- AC4: Outbound file held while the ACE batch is not complete
- AC5: Duplicate application event ignored
- AC6: Two senders pick the same item
- AC7: Resend from the exception queue

**Out of scope:**
- The record-level checks and the stale marker: P1, RWB-E1-015 and RWB-E1-016.
- The run books and job monitoring: RWB-E1-056.
- Inbound source ingestion, its schedules, its checks and the ACE team sign-off: RWB-ACE-001.
- The full SCR-44 interface and job monitor: Epic 2 and Epic 8.
- The WIN notice content and template: RWB-E2-021.
- GL write-off posting (read back through `v_ace_write_off`) and the SOC log (ACE logging, INT-22).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-007-integration-adapters-for-file-loads-and-outbound-files-v1.md` |
| Requirement IDs | REQ-DRI-006, REQ-DRI-007, REQ-DRI-008 |
| BRD section | Business Requirements Epic 1, section 3.2; Business Requirements Program, section 5.2 |
| Decision | D-RCV-35 (U1, U4); ADR-010 |
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
| recovery_svc, recovery service identity | Builds files, reads the views, writes outbound items, sends files |
| SY-CASEWF, case workflow module | Moves the route state on SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED and OUTBOUND_FAILED and raises the task |
| RW-PLATADM, platform administrator | Lists exception items and resends one (Platform administration, U) |
| RW-DATASTEW, data steward | Receives the held-file alert; reads run state (Platform administration, R) |
| RW-REFADM, reference data administrator | Loads a new interface configuration version |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Read run state and exception items (Platform administration, R) |

## Contract extract

**Jobs** | Job | Trigger | Input | Output | Idempotency and restart | |---|---|---|---|---| | JOB-10 WIN outbound notices | Quartz, daily 16:00, after the ACE batch is complete | Approved notices from P6 through `OutboundFiles.enqueue`; addressee from `v_ace_contact` | one outbound_item for the day's file; the file in the document store | key "INT-14:" + business date; a second run adds nothing | | JOB-11 Outbox sender | Quartz, every minute | outbound_item rows with status PENDING or RETRY and next_attempt_at at or before now, read with `FOR UPDATE SKIP LOCKED` | SFTP transfer; item status; outbox_delivery rows | an item in SENT without acknowledgment after 30 minutes (assumed; DL11) is retried | | JOB-13 Decision log copy | Quartz, nightly 01:00 | decision_log_entry and outcomes changed that day | file to the data lake (INT-20) | key INT-20 plus business date; the next night picks up…

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

- No business value in code: retry counts, intervals, folders, patterns, owners and check tolerances are read from tables. - No personal data in logs, tests or prompts; file contents are never logged, only names, counts, hashes and check results. - No read of another module's tables; records reach the owning module only through its published interface. - ACE data only through `recovery.v_ace_*` views; a direct `public.*` read is a defect and fails the boundary test. - Only SftpTransport opens a connection to another system; the boundary test fails the build on any other call. - Outbound items carry case IDs and business keys, never addresses, names or identity numbers. - No inbound adapter, no inbound folder and no sign-off is built, and no interface row has direction INBOUND.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-007-integration-adapters-for-file-loads-and-outbound-files-v1.md` |
| Specification | `output/INC-011-epic-1-RWB-E1-007/specify/spec.md` |
| Compliance validation | `output/INC-011-epic-1-RWB-E1-007/specify/compliance-validation.md` |
| Agent run log | `output/INC-011-epic-1-RWB-E1-007/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-011-epic-1-RWB-E1-007/plan/` |
| Implementation evidence | `output/INC-011-epic-1-RWB-E1-007/implement/` |
| API / functional test reports | `output/INC-011-epic-1-RWB-E1-007/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-011-epic-1-RWB-E1-007/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-007-integration-adapters-for-file-loads-and-outbound-files-v1.md` |
| Output run | `output/INC-011-epic-1-RWB-E1-007/` |

