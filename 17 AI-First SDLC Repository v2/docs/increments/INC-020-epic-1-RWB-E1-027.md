# Increment Card — INC-020-epic-1-RWB-E1-027

**RWB-E1-027 — Decision log writer v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-020` |
| Title | Decision log writer v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-027` |
| RUN_ID | `INC-020-epic-1-RWB-E1-027` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P7 Decision center and log |
| Story type | User story |
| Priority | Must |
| Build order | 20 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-008, RWB-E1-056 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P7 Decision center and log.

## Scope

**Story:** As the **case workflow module (SY-CASEWF)**, I want **one writer that validates and records case created, owner assigned, case transferred and document attached, with the rule ID and version used, in the same transaction as the action**, so that **the first decision records exist in Epic 1 and no action proceeds without its record**.

**Business outcome:** Without one writer, each module would build its own record and some actions would go unrecorded. This story gives every module one published interface that checks each record against the seven field groups, refuses an incomplete record, writes it in the caller's transaction so that a failed write stops the action, ignores a repeated event and publishes DecisionRecorded. It meets REQ-DRI-004 and REQ-DRI-005 and is the automated part of control CTL-06. The measure is decisions with a log entry: target 100 percent, and no action without one (NFR-034).

**Main flow:**
1. Calling module (for example SY-CASEWF in the morning allocation): builds a DecisionLogRecord with the case, the event, the rule ID and version, the inputs reference, the actor and an idempotency key, inside its own transaction.
2. Calling module: calls DecisionLogWriter.write as the last step before commit.
3. Writer (DecisionLogWriterService): checks that a transaction is open; refuses the call if not.
4. Writer: checks the idempotency key; for a key already written, returns the first entry reference and counts the repeat.
5. Writer (DecisionLogRecordValidator): checks the required fields and the version group; refuses an incomplete record with the missing field named.
6. Writer: calls DecisionLogStore.append (RWB-E1-008).

**Acceptance criteria:**
- AC1: Record per event
- AC2: Schema enforced
- AC3: A rule ID with no rule version is refused
- AC4: A failed write stops the action
- AC5: A repeated event gives one entry
- AC6: A write outside a transaction is refused
- AC7: An unknown decision code is refused

**Out of scope:**
- The store, the hash chain and the verifier (RWB-E1-008).
- Approval records with the limit applied (RWB-E2-013).
- Access events (RWB-E1-039).
- The copy to the data lake (RWB-E1-014).
- The recommendation service with reasons for the route decision (Epic 4, API-P7-001).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-027-decision-log-writer-v1-v1.md` |
| Requirement IDs | REQ-DRI-004, REQ-DRI-005 |
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
| SY-DECLOG Decision log writer | Writes entries (Decision log C) |
| SY-CASEWF Case workflow module | Calls the writer for case created, owner assigned and case transferred (Decision log C) |
| SY-OCR OCR and extraction pipeline | Calls the writer for document attached (Decision log C) |
| SY-RULES, SY-DATALOAD, SY-AGENT | Call the writer for their own decisions (Decision log C) |
| RW-AUDIT, RW-COE and every role holding Decision log R | Read the entries |
| RW-PLATADM Platform administrator | Receives the incident when a write fails |

## Contract extract

**Published interface DecisionLogWriter** (package recovery.decision.writer), the only way any module writes to the decision log: ```java @Transactional(propagation = Propagation.MANDATORY) DecisionLogEntryRef write(DecisionLogRecord record) throws DecisionLogRecordInvalidException, // messageId MSG-P7-009, field DecisionLogUnavailableException; // messageId MSG-P7-003 // DecisionLogRecord: idempotencyKey, caseId, decisionCode, ruleId, ruleVersion, modelVersion, agentVersion, inputsRef, // recommendation, approverUserId, approvalLevel, finalCall, overrideReason, actions, outcome, decidedAt, // actorUserRef, correctsEntryId // DecisionLogEntryRef: entryId, chainSeq, entryHash, repeated (boolean) ``` **Event published:** EV-08 DecisionRecorded, payload entryId, caseId, decisionCode, approver; written to the outbox in the same transaction; consumers ledger and reporting. **GET /api/recover…

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

- No business value in code: decision codes per event are parameters and list values. - No personal data in logs, tests or prompts; a refused record is logged with its case ID and field name only. - No read of another module's tables; callers pass the values in the record. - No write path to decision_log_entry other than this interface, checked by an architecture test. - No retry inside the writer; the caller's job or request retries.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-027-decision-log-writer-v1-v1.md` |
| Specification | `output/INC-020-epic-1-RWB-E1-027/specify/spec.md` |
| Compliance validation | `output/INC-020-epic-1-RWB-E1-027/specify/compliance-validation.md` |
| Agent run log | `output/INC-020-epic-1-RWB-E1-027/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-020-epic-1-RWB-E1-027/plan/` |
| Implementation evidence | `output/INC-020-epic-1-RWB-E1-027/implement/` |
| API / functional test reports | `output/INC-020-epic-1-RWB-E1-027/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-020-epic-1-RWB-E1-027/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-027-decision-log-writer-v1-v1.md` |
| Output run | `output/INC-020-epic-1-RWB-E1-027/` |

