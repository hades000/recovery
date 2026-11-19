# Increment Card — INC-061-epic-1-RWB-E1-057

**RWB-E1-057 — Intake from branches, mailroom, partner SFTP and email**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-061` |
| Title | Intake from branches, mailroom, partner SFTP and email |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-057` |
| RUN_ID | `INC-061-epic-1-RWB-E1-057` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 61 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-049, RWB-TE-012, RWB-E1-041 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **case owner**, I want **scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded**, so that **every document path ends in the document hub**.

**Business outcome:** Documents reach recovery today by courier, shared folders and personal email, and an original that goes to the wrong desk is rebuilt for each audit. This story reads the four inbound paths every 15 minutes into the document intake, records where each file came from, refuses files that are not allowed or come from an unknown partner, and leaves every accepted file for the malware scan and OCR steps, so a document received in the morning is on the case the same day. It meets REQ-DCM-009 and puts every inbound file through the virus scan of REQ-DCM-010, and removes email hand-offs of customer documents (CTL-11).

**Main flow:**
1. Scheduler: JOB-12 Document intake fires every 15 minutes in business hours on one service instance; intakeStep runs first, before scanStep.
2. IntakeStep: lists new files in each branch scanner folder and the mailroom folder, in each partner subfolder of the SFTP inbound folder, and new messages in each recovery mailbox.
3. IntakeStep: for each file or email attachment computes the SHA-256 hash and checks document_intake for the same channel and hash inside the duplicate window.
4. IntakeStep: checks the file type by content and extension, and the size, against the parameters.
5. IntakeStep: for a partner file, reads the partner by the subfolder's partner_code and checks that its panel_status is ACTIVE.
6. IntakeStep: copies an accepted file to the intake container and writes one document_intake row with source, channel code, source reference, file name, size, hash, received time, scanner time (scanner files), partner ID (partner files) or sender address (email), and the run ID; scan_result is left empty for scanStep.

**Acceptance criteria:**
- AC1: Branch scan
- AC2: Partner SFTP
- AC3: Mailbox
- AC4: Mailroom scan
- AC5: A file type not allowed is refused
- AC6: A file above the size limit is refused
- AC7: An unknown or suspended partner is refused
- AC8: A duplicate file is not taken in twice
- AC9: An empty run
- AC10: The intake container does not accept writes
- AC11: Two failed runs raise an alert
- AC12: The job runs once across two instances
- AC13: An email with no usable attachment
- AC14: A file seen again after a failed move
- AC15: Outside business hours
- AC16: An item taken in is scanned before OCR

**Out of scope:**
- The malware scan and quarantine (RWB-E1-041), OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching to a case (RWB-E1-032).
- Uploads from the case documents screen (RWB-E1-026).
- Field app photos and bills (RWB-E2-024).
- Partner uploads through the partner portal (Epic 4, PRT-03; partner access DL03).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-057-intake-from-branches-mailroom-partner-sftp-and-email-v1.md` |
| Requirement IDs | REQ-DCM-009, REQ-DCM-010 |
| BRD section | Business Requirements Epic 1, section 3.5 |
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
| SY-OCR, OCR and extraction pipeline | Runs intakeStep; reads the channels; writes document_intake and the intake container (Documents CRU) |
| RW-PLATADM, platform administrator | Sees runs on SCR-44 and reruns JOB-12 (Platform administration CRUD); sets the channel properties |
| RW-AGENCYMG, partner and agency manager | Keeps the partner codes and panel status that BR4 reads (Partner portal CRUDA) |
| RW-CASEOWN, case owner | Reads documents from intake once attached (Documents R) |

## Contract extract

**Job step** | Item | Value | |---|---| | Job name | JOB-12 Document intake; this story adds intakeStep as the first step | | Trigger | Quartz cron `0 0/15 8-17 ? * MON-FRI` in Asia/Bangkok; bank holidays from the reference data holiday table are skipped | | Schedule | Every 15 minutes in business hours | | Input | Branch scanner folders, the mailroom folder, the partner SFTP inbound folder, the recovery mailboxes | | Output | document_intake rows; files in the intake container; files moved to processed or rejected; emails archived; counts on the job record | | Events published | None. DocumentStored (EV-16) is written when matchStep stores the document (RWB-E1-032) | | Idempotency key | Channel code, source reference and file hash | | Restart | A failed run leaves its files at the channel; the next run or a rerun takes them. A file already committed is a duplicate on the next run (AC14…

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

- No business value in code: folders, mailboxes, types, size limit and windows are properties and parameters. - No personal data in logs, tests or prompts: sender addresses and email file names are not logged; test emails use synthetic senders. - No read of another module's tables: partners come through PartnerDirectory. - A file is never removed from a channel before its document_intake row is committed. - Storage is reached by managed identity only, never by key or shared access signature (RWB-TE-012).

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-057-intake-from-branches-mailroom-partner-sftp-and-email-v1.md` |
| Specification | `output/INC-061-epic-1-RWB-E1-057/specify/spec.md` |
| Compliance validation | `output/INC-061-epic-1-RWB-E1-057/specify/compliance-validation.md` |
| Agent run log | `output/INC-061-epic-1-RWB-E1-057/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-061-epic-1-RWB-E1-057/plan/` |
| Implementation evidence | `output/INC-061-epic-1-RWB-E1-057/implement/` |
| API / functional test reports | `output/INC-061-epic-1-RWB-E1-057/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-061-epic-1-RWB-E1-057/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 16 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-057-intake-from-branches-mailroom-partner-sftp-and-email-v1.md` |
| Output run | `output/INC-061-epic-1-RWB-E1-057/` |

