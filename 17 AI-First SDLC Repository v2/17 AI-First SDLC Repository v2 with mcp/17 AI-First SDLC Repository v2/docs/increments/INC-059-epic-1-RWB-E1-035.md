# Increment Card — INC-059-epic-1-RWB-E1-035

**RWB-E1-035 — Case record view v1.1 with documents and history timeline**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-059` |
| Title | Case record view v1.1 with documents and history timeline |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-035` |
| RUN_ID | `INC-059-epic-1-RWB-E1-035` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Should |
| Build order | 59 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-021, RWB-E1-023, RWB-E1-027 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **a timeline on the case record view with contacts, documents, assignments, transfers and status changes in time order, each with who or which rule caused it**, so that **I see what happened to the case without asking anyone**.

**Business outcome:** A case that changes owner today arrives with no history except what the last owner remembers. This story adds a timeline panel to SCR-03 that merges the interaction ledger, the documents, the assignments and the decision log entries for the case in time order, and shows the person or the rule and version behind each event, including the coded reason of a manual transfer. It meets REQ-CWC-016 (every workflow event carries its rule ID and version, now visible) and REQ-OCC-007 (contact history and documents on the case view).

**Main flow:**
1. Case owner: opens SCR-03 for case RW-2026-000801 and selects the Timeline panel.
2. TimelinePanel: calls GET /cases/{caseId}/timeline with page 0 and size 50.
3. CaseAndWorkflowController: checks Case record R and the scope.
4. TimelineService: reads interactions and assignments from P3 tables, documents through the P5 interface and decision log entries through the P7 interface, for the case.
5. TimelineService: maps each record to a TimelineItem with time, type, summary, by and reference.
6. TimelineService: sorts by time, then by a fixed type order for equal times, then by record ID, and returns the page with the total.

**Acceptance criteria:**
- AC1: Timeline order
- AC2: Transfer reason
- AC3: Decision log unavailable
- AC4: A new case shows only its creation
- AC5: Events at the same time
- AC6: More than 50 events
- AC7: Case outside the scope

**Out of scope:**
- The full timeline screen with filters and queue history (RWB-E2-016).
- The full case record view with collateral, decisions and timers (Epic 2, FEAT-WKM-08).
- Communications and notices on the timeline (Epic 2, P6).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-035-case-record-view-v1-1-with-documents-and-history-timeline-v1.md` |
| Requirement IDs | REQ-CWC-016, REQ-OCC-007 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 3.6; Business Requirements Program, sections 5.3 and 5.6 |
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
| RW-CASEOWN | Reads the timeline of own cases (Case record R) |
| RW-TEAMMGR | Reads the timeline of team cases |
| RW-CONDUCT, RW-AUDIT | Read the timeline of every case |
| RW-REFADM | No Case record right; refused |

## Contract extract

**GET /api/recovery/v1/cases/{caseId}/timeline** | Item | Value | |---|---| | Request | Path caseId (uuid); query type, from, to; page and size (new query parameters, see additions) | | Response | TimelinePage of TimelineItem: at, type, summary, by, reference, and the new fields reasonCode, fromQueueCode, toQueueCode and ruleId (recorded with RWB-E2-016) | | Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 P3 store unavailable | | Authorization | Case record, right R, scope applied | | Idempotency | Not applicable | The endpoint is first listed for E2 in api.yaml; this story delivers it in E1 behind the flag. **Published interfaces used** ```java // P7 (RWB-E1-027) public interface DecisionLogQuery { List<DecisionLogSummary> entriesForCase(UUID caseId, Instant from, Instant to); } // P5 (RWB-E1-024) public interface DocumentQu…

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

- No business value in code: the type order and labels are data. - No personal data in logs, tests or prompts; contact summaries follow masking by role. - No read of another module's tables: documents through DocumentQuery (P5), decisions through DecisionLogQuery (P7). - The timeline never writes; it shows records as they were written.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-035-case-record-view-v1-1-with-documents-and-history-timeline-v1.md` |
| Specification | `output/INC-059-epic-1-RWB-E1-035/specify/spec.md` |
| Compliance validation | `output/INC-059-epic-1-RWB-E1-035/specify/compliance-validation.md` |
| Agent run log | `output/INC-059-epic-1-RWB-E1-035/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-059-epic-1-RWB-E1-035/plan/` |
| Implementation evidence | `output/INC-059-epic-1-RWB-E1-035/implement/` |
| API / functional test reports | `output/INC-059-epic-1-RWB-E1-035/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-059-epic-1-RWB-E1-035/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-035-case-record-view-v1-1-with-documents-and-history-timeline-v1.md` |
| Output run | `output/INC-059-epic-1-RWB-E1-035/` |

