# Increment Card — INC-078-epic-1-RWB-E1-055

**RWB-E1-055 — Proof of delivery capture design with WIN**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-078` |
| Title | Proof of delivery capture design with WIN |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-055` |
| RUN_ID | `INC-078-epic-1-RWB-E1-055` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P6 Communications |
| Story type | User story |
| Priority | Should |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-052, RWB-E1-054, RWB-E1-028, RWB-E1-066 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P6 Communications. **Build group:** P6.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **generated notices sent to WIN for print and registered mail, with the dispatch and the proof of delivery written back on the notice**, so that **the case shows what was sent and when it arrived**.

**Main flow:**
1. JOB-10 WIN outbound notices, daily 16:00: selects notices in a dispatch-eligible state with no sent date.
2. System: builds one INT-14 file: ContractNO of the case's primary account, addressee, address detokenized through the ACE PII service, notice type, template version and document reference; writes the trailer with the record count.
3. System: hands the file to the integration adapters and marks each notice "file sent" with the file ID.
4. Integration adapters: deliver the WIN acknowledgment, which carries per ContractNO the sent date (DDMMYYYY), Barcode and Sent Type (s2t mapping of INT-14).
5. System: sets notice state Sent with sent_date, barcode and sent_type; writes a LETTER entry to the interaction ledger; publishes NoticeDispatched.
6. JOB-09 File loads, weekly Monday 04:00: loads the INT-15 proof of delivery file and runs checks DQ-085 to DQ-091.

**Out of scope:**
- Refused, returned and undeliverable letters, the proof window and the transfer to the owner's queue (RWB-E2-021, R-LIT-08, R-LIT-09).
- The conduct check before dispatch (RWB-E2-021).
- Notice approval before dispatch (RWB-E2-014).
- Statutory sale notices for repossessed assets (FEAT-AST-04, Epic 3).

**Business outcome and value hypothesis:** Proof of delivery is chased by phone today, and a notice period counted from the print date can be challenged in court. This story writes the daily WIN notice file (INT-14), takes back the WIN barcode and the weekly proof of delivery file (INT-15), and publishes the delivery so the notice period timer starts from the delivery date (CTL-15). It serves REQ-OCC-003 and REQ-ILG-004 and the FSD P6 measure "notices with proof of delivery, 100 percent", and fixes the interface contract with WIN that RWB-E2-021 completes.

**Constraints and guardrails:**
- No business value in code: schedule, eligible states, attempt limit, break days and stale period are configuration; file layouts follow the interface specification.
- No personal data in logs, tests or prompts. The address is detokenized only into the outbound file stream and is never logged; the job log holds notice IDs and counts.
- No read of another module's tables. The primary account contract number comes through the P1 and P3 interfaces; the timer is started by P3 on the event.
- Files move only through the integration adapters (REQ-DRI-006); no direct call to WIN.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 055 Proof of delivery capture design with WIN v1.md` |
| Requirement IDs | REQ-OCC-003, REQ-ILG-004 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4; Business Requirements Epic 2, section 4 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs JOB-10 and JOB-09 and writes the outbound file (Litigation U) |
| SY-CASEWF, case workflow module | Consumes NoticeDelivered and starts the timer |
| RW-LITOFF, litigation officer | Reads notice state, dates and barcode (Litigation R); receives the task on repeated failure |
| RW-CASEOWN, case owner | Reads notice state (Litigation R) |
| RW-PLATADM, platform administrator | Reruns JOB-10 from SCR-44; reads REC-05 breaks |
| RW-DATASTEW, data steward | Reads refused files and held records on SCR-45 |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Not used | API is not in scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.comms.win-dispatch-v1`.
- **Critical path:** No; **depends on:** RWB-E1-052, RWB-E1-054, RWB-E1-028, RWB-E1-066.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: schedule, eligible states, attempt limit, break days and stale period are configuration; file layouts follow the interface specification.
  - No personal data in logs, tests or prompts. The address is detokenized only into the outbound file stream and is never logged; the job log holds notice IDs and counts.
  - No read of another module's tables. The primary account contract number comes through the P1 and P3 interfaces; the timer is started by P3 on the event.
  - Files move only through the integration adapters (REQ-DRI-006); no direct call to WIN.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 055 Proof of delivery capture design with WIN v1.md` |
| Specification | `output/INC-078-epic-1-RWB-E1-055/specify/spec.md` |
| Compliance validation | `output/INC-078-epic-1-RWB-E1-055/specify/compliance-validation.md` |
| Agent run log | `output/INC-078-epic-1-RWB-E1-055/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-078-epic-1-RWB-E1-055/plan/` (TBC) |
| Implementation evidence | `output/INC-078-epic-1-RWB-E1-055/implement/` (TBC) |
| API / functional test reports | `output/INC-078-epic-1-RWB-E1-055/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-078-epic-1-RWB-E1-055/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-078-epic-1-RWB-E1-055/specify/compliance-validation.md`) |
| Acceptance criteria | 11 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 055 Proof of delivery capture design with WIN v1.md` |
| Output run | `output/INC-078-epic-1-RWB-E1-055/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
