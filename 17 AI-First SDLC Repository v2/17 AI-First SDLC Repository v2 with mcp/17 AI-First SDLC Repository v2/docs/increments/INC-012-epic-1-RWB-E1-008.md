# Increment Card — INC-012-epic-1-RWB-E1-008

**RWB-E1-008 — Decision log store v1, append only and hash chained**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-012` |
| Title | Decision log store v1, append only and hash chained |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-008` |
| RUN_ID | `INC-012-epic-1-RWB-E1-008` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P7 Decision center and log |
| Story type | User story |
| Priority | Must |
| Build order | 12 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P7 Decision center and log.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **an append-only decision log store holding the seven field groups of every decision, with each entry hashed to the one before it**, so that **every decision from Epic 1 is recorded once, cannot be changed or deleted, and any change to a stored entry is found by recomputing the chain**.

**Business outcome:** Documentation and audit trail findings (5 of 29 in the audit summary behind CTL-06) show that why a route was chosen, who approved it and on what figures is spread across e-mails and files. This story builds the store that every later decision writes to: one record per decision with inputs, versions, recommendation, approver, final call, actions and outcome; refusal of every update and delete in the database; a single hash chain; and a verifier that finds a break. It meets REQ-DRI-001, REQ-DRI-002 and REQ-DRI-003 and implements ADR-009. The measure is every decision reproducible from the log (NFR-033).

**Main flow:**
1. Writer (SY-DECLOG, built in RWB-E1-027): calls DecisionLogStore.append with a validated record inside the caller's transaction, as its last statement.
2. Store (DecisionLogStore): takes the chain lock (a PostgreSQL transaction advisory lock on the key "decision_log_chain").
3. Store: reads the chain_seq and entry_hash of the last entry; sets chain_seq to last plus 1 and prev_hash to the last entry_hash, or 64 zeros for the first entry.
4. Store: builds the canonical form of the entry and sets entry_hash to its SHA-256 in lower-case hexadecimal.
5. Store: inserts the row; the caller's transaction commits the action and the entry together and releases the lock.
6. Store: on any failure, raises DecisionLogUnavailableException; the caller's transaction rolls back and the action does not happen.

**Acceptance criteria:**
- AC1: Append only
- AC2: Hash chain
- AC3: Seven field groups
- AC4: Hash chain verified daily
- AC5: Two appends at the same moment form one chain
- AC6: A correction is a new entry
- AC7: A failed append leaves nothing behind
- AC8: Reading an entry needs the Decision log right

**Out of scope:**
- Validation of entries and the publish of DecisionRecorded (RWB-E1-027).
- The nightly schedule of the chain check and its daily report (RWB-TE-008, JOB-14).
- The copy of the log to the data lake (RWB-E1-014, JOB-13).
- Audit queries by approver, rule version and date, and the query screen (RWB-E2-005).
- Retention periods (DL26).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-008-decision-log-store-v1-append-only-and-hash-chained-v1.md` |
| Requirement IDs | REQ-DRI-001, REQ-DRI-002, REQ-DRI-003 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, section 5.7 |
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
| SY-DECLOG Decision log writer | Appends entries (Decision log C) |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-OCR, SY-AGENT | Write through the writer only (Decision log C) |
| RW-AUDIT Internal audit | Reads entries (Decision log R) |
| RW-COMPLY Compliance and PDPA officer | Reads entries; receives break reports |
| RW-COE Center of excellence analyst | Reads entries |
| Every bank role holding Decision log R | Reads entries inside its scope |
| RW-PLATADM Platform administrator | Receives the incident on a break or a failed append |
| No role | May update or delete an entry |

## Contract extract

**GET /api/recovery/v1/decision-log/{entryId}** (API-P7-007) | Item | Value | |---|---| | Request | Path: entryId (uuid) | | Response | DecisionLogEntry: id, caseId, decisionCode, ruleId, ruleVersion, modelVersion, agentVersion, inputsRef, recommendation, approverUserId, approvalLevel, finalCall, overrideReason, actions, outcome, decidedAt, prevHash, entryHash | | Errors | 401; 403 no Decision log R (MSG-P4-002); 404 no entry or case out of scope (MSG-P4-003); 503 store unavailable (MSG-GEN-006) | | Authorization | Decision log, right R, scope applied through the entry's case | | Idempotency | Not applicable, read only | **GET /api/recovery/v1/decision-log** (API-P7-006), in this story by caseId only, ordered by chain_seq; page and size; response DecisionLogPage; Decision log R; errors 401, 403, 503. The other filters come in RWB-E2-005. **Interfaces inside P7** (package recovery.decisi…

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

- No business value in code; the genesis hash and the notification group are configuration. - No personal data in logs, tests or prompts. Entries hold references (inputs_ref, case ID, user references), not customer names or identity numbers. - No read of another module's tables; other modules write only through the P7 writer. - No update or delete method in the repository, and no database grant for either. - One canonical form implementation for writing and verifying.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-008-decision-log-store-v1-append-only-and-hash-chained-v1.md` |
| Specification | `output/INC-012-epic-1-RWB-E1-008/specify/spec.md` |
| Compliance validation | `output/INC-012-epic-1-RWB-E1-008/specify/compliance-validation.md` |
| Agent run log | `output/INC-012-epic-1-RWB-E1-008/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-012-epic-1-RWB-E1-008/plan/` |
| Implementation evidence | `output/INC-012-epic-1-RWB-E1-008/implement/` |
| API / functional test reports | `output/INC-012-epic-1-RWB-E1-008/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-012-epic-1-RWB-E1-008/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-008-decision-log-store-v1-append-only-and-hash-chained-v1.md` |
| Output run | `output/INC-012-epic-1-RWB-E1-008/` |

