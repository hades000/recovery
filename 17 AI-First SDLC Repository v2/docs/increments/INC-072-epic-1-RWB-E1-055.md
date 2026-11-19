# Increment Card — INC-072-epic-1-RWB-E1-055

**RWB-E1-055 — Proof of delivery capture design with WIN**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-072` |
| Title | Proof of delivery capture design with WIN |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-055` |
| RUN_ID | `INC-072-epic-1-RWB-E1-055` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Should |
| Build order | 72 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-052, RWB-E1-054, RWB-E1-028, RWB-E1-066 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **generated notices sent to WIN for print and registered mail, with the dispatch and the proof of delivery written back on the notice**, so that **the case shows what was sent and when it arrived**.

**Business outcome:** Proof of delivery is chased by phone today, and a notice period counted from the print date can be challenged in court. This story writes the daily WIN notice file (INT-14) and reads back the WIN barcode and the weekly proof of delivery that ACE ingests into `pod_receipt`, through `v_ace_pod` by `notice_ref`. It publishes the delivery so the notice period timer starts from the delivery date (CTL-15). It serves REQ-OCC-003 and REQ-ILG-004 and the FSD P6 measure "notices with proof of delivery, 100 percent", and fixes the interface contract with WIN that RWB-E2-021 completes. The Workbench writes no WIN delivery fact of its own: ACE holds the proof of delivery, as it holds every other source record (D-RCV-35 U1).

**Main flow:**
1. JOB-10 WIN outbound notices, daily 16:00: selects notices in a dispatch-eligible state with no sent date.
2. System: builds one INT-14 file: ContractNO of the case's primary account, addressee, address read from `v_ace_contact` by `person_key`, notice type, template version and document reference; writes the trailer with the record count.
3. System: hands the file to the integration adapters and marks each notice "file sent" with the file ID.
4. Integration adapters: deliver the WIN acknowledgment, which carries per ContractNO the sent date (DDMMYYYY), Barcode and Sent Type (s2t mapping of INT-14).
5. System: sets notice state Sent with sent_date, barcode and sent_type; writes a LETTER entry to the interaction ledger; publishes NoticeDispatched.
6. System: reads the WIN proof of delivery that ACE ingested into `pod_receipt`, through `v_ace_pod`, for the notice's business date.

**Acceptance criteria:**
- AC1: Dispatched
- AC2: Proof of delivery
- AC3: Interface contract agreed with WIN
- AC4: File not acknowledged
- AC5: The WIN batch fails its check in ACE
- AC6: Unknown reference held
- AC7: The same proof of delivery read twice
- AC8: Repeated dispatch run
- AC9: Barcode missing after three days
- AC10: Repeated delivery record
- AC11: Proof of delivery batch late

**Out of scope:**
- Refused, returned and undeliverable letters, the proof window and the transfer to the owner's queue (RWB-E2-021, R-LIT-08, R-LIT-09).
- The conduct check before dispatch (RWB-E2-021).
- Notice approval before dispatch (RWB-E2-014).
- Statutory sale notices for repossessed assets (FEAT-AST-04, Epic 3).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-055-proof-of-delivery-capture-design-with-win-v1.md` |
| Requirement IDs | REQ-OCC-003, REQ-ILG-004 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4; Business Requirements Epic 2, section 4 |
| Decision | D7.1 |
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
| SY-DATALOAD, data load | Runs JOB-10 and the proof of delivery read and writes the outbound file (Litigation U) |
| SY-CASEWF, case workflow module | Consumes NoticeDelivered and starts the timer |
| RW-LITOFF, litigation officer | Reads notice state, dates and barcode (Litigation R); receives the task on repeated failure |
| RW-CASEOWN, case owner | Reads notice state (Litigation R) |
| RW-PLATADM, platform administrator | Reruns JOB-10 from SCR-44; reads REC-05 breaks |
| RW-DATASTEW, data steward | Reads refused files and held records on SCR-45 |

## Contract extract

**Job JOB-10 WIN outbound notices** | Item | Value | |---|---| | Trigger | Quartz, daily 16:00 Asia/Bangkok | | Input | Notices in a dispatch-eligible state with no sent date | | Output | INT-14 file: ContractNO, addressee, address, notice type, template version, document reference; trailer with record count | | Events published | NoticeDispatched (EV-14) per acknowledged notice | | Idempotency key | Notice ID and file date; a notice already in an unacknowledged file of the same date is skipped | | Restart | A failed run is rerun from SCR-44; notices already in a file of that date are not written again | **Read path: v_ace_pod (ACE ingestion of INT-15)** | Item | Value | |---|---| | Trigger | A daily read at 06:00, after v_ace_batch_status shows source WIN COMPLETE for the business date | | Input | v_ace_pod rows by notice_ref: barcode, sent_date, callback_date, delivery_status, sent_ty…

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

- No business value in code: schedule, eligible states, attempt limit, break days and stale period are configuration; file layouts follow the interface specification. - No personal data in logs, tests or prompts. The address is read from `v_ace_contact` only into the outbound file stream and is never logged; the job log holds notice IDs and counts. - No read of another module's tables. The primary account contract number and the address come through the P1 query; the timer is started by P3 on the event; the delivery is read from `v_ace_pod`. - Files move only through the integration adapters (REQ-DRI-006); no direct call to WIN.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-055-proof-of-delivery-capture-design-with-win-v1.md` |
| Specification | `output/INC-072-epic-1-RWB-E1-055/specify/spec.md` |
| Compliance validation | `output/INC-072-epic-1-RWB-E1-055/specify/compliance-validation.md` |
| Agent run log | `output/INC-072-epic-1-RWB-E1-055/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-072-epic-1-RWB-E1-055/plan/` |
| Implementation evidence | `output/INC-072-epic-1-RWB-E1-055/implement/` |
| API / functional test reports | `output/INC-072-epic-1-RWB-E1-055/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-072-epic-1-RWB-E1-055/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-055-proof-of-delivery-capture-design-with-win-v1.md` |
| Output run | `output/INC-072-epic-1-RWB-E1-055/` |

