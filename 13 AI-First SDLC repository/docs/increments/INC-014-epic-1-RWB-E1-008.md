# Increment Card — INC-014-epic-1-RWB-E1-008

**RWB-E1-008 — Decision log store v1, append only and hash chained**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-014` |
| Title | Decision log store v1, append only and hash chained |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-008` |
| RUN_ID | `INC-014-epic-1-RWB-E1-008` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P7 Decision center and log |
| Story type | User story |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-E1-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P7 Decision center and log. **Build group:** P7.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **an append-only decision log store holding the seven field groups of every decision, with each entry hashed to the one before it**, so that **every decision from Epic 1 is recorded once, cannot be changed or deleted, and any change to a stored entry is found by recomputing the chain**.

**Main flow:**
1. Writer (SY-DECLOG, built in RWB-E1-027): calls DecisionLogStore.append with a validated record inside the caller's transaction, as its last statement.
2. Store (DecisionLogStore): takes the chain lock (a PostgreSQL transaction advisory lock on the key "decision_log_chain").
3. Store: reads the chain_seq and entry_hash of the last entry; sets chain_seq to last plus 1 and prev_hash to the last entry_hash, or 64 zeros for the first entry.
4. Store: builds the canonical form of the entry and sets entry_hash to its SHA-256 in lower-case hexadecimal.
5. Store: inserts the row; the caller's transaction commits the action and the entry together and releases the lock.
6. Store: on any failure, raises DecisionLogUnavailableException; the caller's transaction rolls back and the action does not happen.

**Out of scope:**
- Validation of entries and the publish of DecisionRecorded (RWB-E1-027).
- The nightly schedule of the chain check and its daily report (RWB-TE-008, JOB-14).
- The copy of the log to the data lake (RWB-E1-014, JOB-13).
- Audit queries by approver, rule version and date, and the query screen (RWB-E2-005).
- Retention periods (DL26).

**Business outcome and value hypothesis:** Documentation and audit trail findings (5 of 29 in the audit summary behind CTL-06) show that why a route was chosen, who approved it and on what figures is spread across e-mails and files. This story builds the store that every later decision writes to: one record per decision with inputs, versions, recommendation, approver, final call, actions and outcome; refusal of every update and delete in the database; a single hash chain; and a verifier that finds a break. It meets REQ-DRI-001, REQ-DRI-002 and REQ-DRI-003 and implements ADR-009. The measure is every decision reproducible from the log (NFR-033).

**Constraints and guardrails:**
- No business value in code; the genesis hash and the notification group are configuration.
- No personal data in logs, tests or prompts. Entries hold references (inputs_ref, case ID, user references), not customer names or identity numbers.
- No read of another module's tables; other modules write only through the P7 writer.
- No update or delete method in the repository, and no database grant for either.
- One canonical form implementation for writing and verifying.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 008 Decision log store v1 append only and hash chained v1.md` |
| Requirement IDs | REQ-DRI-001, REQ-DRI-002, REQ-DRI-003 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 |
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
| SY-DECLOG Decision log writer | Appends entries (Decision log C) |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-OCR, SY-AGENT | Write through the writer only (Decision log C) |
| RW-AUDIT Internal audit | Reads entries (Decision log R) |
| RW-COMPLY Compliance and PDPA officer | Reads entries; receives break reports |
| RW-COE Center of excellence analyst | Reads entries |
| Every bank role holding Decision log R | Reads entries inside its scope |
| RW-PLATADM Platform administrator | Receives the incident on a break or a failed append |
| No role | May update or delete an entry |

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
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.decision.log-store`.
- **Critical path:** No; **depends on:** RWB-E1-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code; the genesis hash and the notification group are configuration.
  - No personal data in logs, tests or prompts. Entries hold references (inputs_ref, case ID, user references), not customer names or identity numbers.
  - No read of another module's tables; other modules write only through the P7 writer.
  - No update or delete method in the repository, and no database grant for either.
  - One canonical form implementation for writing and verifying.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 008 Decision log store v1 append only and hash chained v1.md` |
| Specification | `output/INC-014-epic-1-RWB-E1-008/specify/spec.md` |
| Compliance validation | `output/INC-014-epic-1-RWB-E1-008/specify/compliance-validation.md` |
| Agent run log | `output/INC-014-epic-1-RWB-E1-008/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-014-epic-1-RWB-E1-008/plan/` (TBC) |
| Implementation evidence | `output/INC-014-epic-1-RWB-E1-008/implement/` (TBC) |
| API / functional test reports | `output/INC-014-epic-1-RWB-E1-008/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-014-epic-1-RWB-E1-008/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-014-epic-1-RWB-E1-008/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 008 Decision log store v1 append only and hash chained v1.md` |
| Output run | `output/INC-014-epic-1-RWB-E1-008/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
