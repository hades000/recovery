# Increment Card — INC-070-epic-1-RWB-E1-054

**RWB-E1-054 — Review queue for low-confidence documents**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-070` |
| Title | Review queue for low-confidence documents |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-054` |
| RUN_ID | `INC-070-epic-1-RWB-E1-054` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Must |
| Build order | 70 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-049, RWB-E1-035, RWB-E1-050, RWB-E1-053, RWB-E1-032 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **litigation officer**, I want **a queue of documents with low classification or extraction confidence, each correctable in one screen, with the correction fed back to the labeled set**, so that **no document is attached wrongly and the models improve**.

**Business outcome:** A wrong type or a wrong hearing date on a court notice puts the wrong date on the case and the litigation timers run from it. This story shows in one queue every intake item the pipeline could not type, read or match, and every stored document with a field below its threshold; one officer confirms or corrects the type, the case and the fields on one screen, and each correction is kept as a labeled example for the model evaluations. It meets REQ-DCM-005 and moves the measure "fields extracted without review", because each correction improves the next model version.

**Main flow:**
1. Litigation officer: opens SCR-31 Document review queue.
2. System: lists, oldest first, the intake items with a review_reason and no case that belong to the officer's review team, the intake items whose candidate cases are in the officer's scope, and the stored documents with review_status PENDING on cases in scope; each row shows the reason, the proposed type, the two candidates, confidence and age.
3. Litigation officer: opens an item; the system shows the file, the OCR text, the type with its candidates, the candidate cases and the fields, with fields in REVIEW marked.
4. Litigation officer: keeps the type or chooses another type from the list in force; a new type re-runs extraction for that type and shows the new fields.
5. Litigation officer: chooses the case from the candidates, or enters a case number that the system looks up through CaseDirectory.
6. Litigation officer: confirms each marked field with Confirm, or enters the value with Correct; the system checks it against the field data type and range.

**Acceptance criteria:**
- AC1: Queued
- AC2: Corrected
- AC3: A stored document with a field to check
- AC4: An empty correction is refused
- AC5: A type not in the list is refused
- AC6: A date outside the allowed range is refused
- AC7: Attach with a field still in review is refused
- AC8: A closed case is refused
- AC9: Two officers on the same item
- AC10: A type change re-runs extraction for the new type
- AC11: The file is already on the chosen case
- AC12: Discard an unreadable item
- AC13: Discard without a reason is refused
- AC14: The queue lists items in scope, oldest first
- AC15: An empty queue
- AC16: A document outside the officer's scope
- AC17: The same confirmation sent twice

**Out of scope:**
- Setting the review reasons: OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching (RWB-E1-032).
- The model evaluations that read the labeled examples (RWB-E1-060).
- Assigning review work to named people by queue rules (RWB-E2-011).
- The case checklist on the review screen (RWB-E1-040).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-054-review-queue-for-low-confidence-documents-v1.md` |
| Requirement IDs | REQ-DCM-005 |
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
| RW-LITOFF, litigation officer | Lists, reads, corrects, attaches and discards review items in scope (Documents CRU) |
| RW-CASEOWN, case owner | Lists, reads, corrects and attaches review items of own cases (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the queue for the team (Documents R); cannot correct or attach |
| SY-OCR, OCR and extraction pipeline | Re-runs extraction on a type change (Documents CRU) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry through DocumentStore |
| RW-COE, center of excellence analyst | Reads the labeled examples through the model evaluations (Documents R) |

## Contract extract

**GET /review-items** (new, recorded in the additions file) | Item | Value | |---|---| | Request | Query kind (INTAKE, DOCUMENT or ALL; default ALL), reason, page, size (default REVIEW_PAGE_SIZE) | | Response | ReviewItemPage: items of kind, intakeId or documentId, caseNo, reason, predictedType, candidates, confidence, receivedAt, version | | Errors | 401 (MSG-P4-001); 403 no Documents R (MSG-P4-002); 422 unknown kind or reason (MSG-GEN-002); 503 (MSG-GEN-006) | | Authorization | Documents, right R, scope applied (BR2) | | Idempotency | Not applicable | **GET /intake-items/{intakeItemId}** and **GET /intake-items/{intakeItemId}/content** (new) | Item | Value | |---|---| | Response | IntakeItem: id, source, receivedAt, reviewReason, predictedType, candidates, candidateCases (caseNo, status), pages (page number, text), fields (masked by role), version; content returns the file | | Errors…

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

- No business value in code: the review team, date limits, page size and the type list come from document_hub_parameter and the type table. - No personal data in logs, tests or prompts: field values and OCR text are masked by role and never logged; the labeled examples stay inside the bank. - No read of another module's tables: cases come through CaseDirectory; scope comes from the ACE common access check. - Attach goes only through DocumentStore, so a document never exists without its decision log entry.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-054-review-queue-for-low-confidence-documents-v1.md` |
| Specification | `output/INC-070-epic-1-RWB-E1-054/specify/spec.md` |
| Compliance validation | `output/INC-070-epic-1-RWB-E1-054/specify/compliance-validation.md` |
| Agent run log | `output/INC-070-epic-1-RWB-E1-054/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-070-epic-1-RWB-E1-054/plan/` |
| Implementation evidence | `output/INC-070-epic-1-RWB-E1-054/implement/` |
| API / functional test reports | `output/INC-070-epic-1-RWB-E1-054/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-070-epic-1-RWB-E1-054/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 17 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-054-review-queue-for-low-confidence-documents-v1.md` |
| Output run | `output/INC-070-epic-1-RWB-E1-054/` |

