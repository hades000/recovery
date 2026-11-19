# Technical Specification — RWB-E1-035 Case record view v1.1 with documents and history timeline

| Field | Value |
|---|---|
| Story | RWB-E1-035 — Case record view v1.1 with documents and history timeline |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-062-epic-1-RWB-E1-035` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-010); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 035 Case record view v1 1 with documents and history timeline v1.md` |
| Upstream IDs | BRD-RWB-003; FR-RWB-010; REQ-CWC-016, REQ-OCC-007; US-RWB-E1-035; CTX-FEATURE-003, CTX-FEATURE-005, CTX-FEATURE-007; NFR-070 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-03 Case record gains the Timeline panel with paging, item detail, Loading, read only and error states. |
| Logic In Scope | `YES` — four-source merge, type order, stable tie-break, paging, partial result, masking and scope. |
| API In Scope | `YES` — `GET /cases/{caseId}/timeline` is delivered in E1 behind the flag; it gains `page`/`size` and the response gains `unavailableSources`, `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId`. |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `CaseAndWorkflowController`; `CaseAndWorkflowRepository`; `interaction`, `assignment`; API-P3-003; `DecisionLogQuery` (P7); `DocumentQuery` (P5); `FieldMasker` (P4); SCR-03. |
| New Nodes Required | `YES` — `TimelineService`, `TimelineItemMapper`, `TimelinePanel`. |
| Inherited Existing Behavior | Read-only case record (RWB-E1-023); transfers with reason and rule (RWB-E1-021); decision log query (RWB-E1-027); document hub (RWB-E1-024); masking rules (RWB-E1-037). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Events show in time order; equal times follow the type order decision, status change, assignment, transfer, contact, document, then record ID. | SPEC-RWB-E1-035-002 | DIRECT | Comparator: `at`, then `typeOrder`, then `recordId`. | COVERED |
| BR2 | An event caused by a rule shows the rule ID and version; an event by a person shows the person. | SPEC-RWB-E1-035-004 | DIRECT | `TimelineItemMapper` per source; `by` is either the user or `ruleId vVersion`. | COVERED |
| BR3 | A manual transfer shows its transfer reason. | SPEC-RWB-E1-035-005 | DIRECT | `reasonCode` from `assignment.transfer_reason_code`; label from LOV-TRANSFER-REASON. | COVERED |
| BR4 | Only cases in the caller's scope open. | SPEC-RWB-E1-035-008 | DIRECT | Scope check before the four reads; 404 MSG-P4-003. | COVERED |
| BR5 | Personal fields in a contact summary follow the masking rules. | SPEC-RWB-E1-035-004 | DIRECT | `FieldMasker` on the interaction summary; no rule means masked. | COVERED |
| BR6 | The timeline reads in under 2 seconds at the ledger's 2031 size. | SPEC-RWB-E1-035-012 | DIRECT | NFR-070; indexed reads; paging; source timeout. | COVERED |
| AC1 | Transfer 08:10, demand letter 10:30, title deed next day 09:00 and status change 11:15 show in that order; the transfer shows TRF-007/TRF-2026.11 and the status change U-81. | SPEC-RWB-E1-035-001, -002, -004 | DIRECT | Merge and sort; `by` from the source. | COVERED |
| AC2 | A manual transfer at 2026-12-04 14:00 shows R04 Owner absent, the from and to owner, and TRF-2026.11. | SPEC-RWB-E1-035-005 | DIRECT | Assignment plus decision log detail. | COVERED |
| AC3 | When the decision log query times out, interactions, documents and assignments show and the panel shows MSG-P3-023 for Decisions. | SPEC-RWB-E1-035-006 | DIRECT | Partial result; `unavailableSources`. | COVERED |
| AC4 | A new case shows one item "Case created" with the entry rule version. | SPEC-RWB-E1-035-007 | DIRECT | Decision log creation entry. | COVERED |
| AC5 | A decision log entry and an assignment at the same time show the decision first, stably on every opening. | SPEC-RWB-E1-035-002 | DIRECT | Type order; record ID tie-break. | COVERED |
| AC6 | A case with 132 events shows 50 on the first page and 32 on the third page, total 132. | SPEC-RWB-E1-035-003 | DIRECT | Page size 50; total; page numbering from the most recent end. | COVERED |
| AC7 | A case outside scope returns 404 with MSG-P4-003. | SPEC-RWB-E1-035-008 | DIRECT | Scope predicate. | COVERED |
| X1 | The decision log query does not answer. | SPEC-RWB-E1-035-006 | DIRECT | Section message. | COVERED |
| X2 | The case has only its creation entry. | SPEC-RWB-E1-035-007 | DIRECT | One item. | COVERED |
| X3 | Two events have the same time. | SPEC-RWB-E1-035-002 | DIRECT | Type order then record ID. | COVERED |
| X4 | The case has more than 50 events. | SPEC-RWB-E1-035-003 | DIRECT | Paged by 50. | COVERED |
| X5 | The case is outside the user's scope. | SPEC-RWB-E1-035-008 | DIRECT | 404. | COVERED |
| X6 | A role without Case record R opens the timeline. | SPEC-RWB-E1-035-010 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **a timeline on the case record view with contacts, documents,
assignments, transfers and status changes in time order, each with who or which rule caused it**, so that **I
see what happened to the case without asking anyone**.

The story adds one panel to SCR-03. It does not add the full timeline screen with filters (SCR-04,
RWB-E2-016), the full case record with collateral, decisions and timers (Epic 2, FEAT-WKM-08) or
communications and notices on the timeline (Epic 2, P6).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | The user opens SCR-03 for a case and selects the Timeline panel. |
| Preconditions | RWB-E1-023 done (read-only case record); RWB-E1-021 done (transfer reason and rule); RWB-E1-027 done (decision log query); P5 document hub lists documents by case; the user holds Case record R and the case is in scope. |
| Input | `caseId`; `type`, `from`, `to`; `page`, `size` (default 50, max 200). |
| Output | `TimelinePage` with `items`, `page`, `size`, `total`, `unavailableSources`. |
| Feature flag | `rwb.p3.timeline`. Off: SCR-03 hides the Timeline panel and the endpoint returns 404. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `interaction` | `occurred_at`, `channel`, `direction`, `contact_result`, `summary` | P3 interaction row | Read only; summary masked | Source EFS or Workbench |
| `assignment` | `assigned_at`, `ended_at`, `assignee_user_id`, `reason`, `rule_id`, `transfer_reason_code` | P3 assignment row | Read only | Transfer detail from the assignment and decision log |
| `document` | `stored_at`, `document_type`, `source` | P5 interface | Read only | No content, metadata only |
| `decision_log_entry` | `decided_at`, `decision_code`, `rule_id`, `rule_version`, `final_call`, `approver_user_id` | P7 interface | Read only | Creation entry included |
| `TimelineItem` | `at`, `type`, `summary`, `by`, `reference` | Mapper | Read only | `by` is a person or a rule with version |
| `TimelineItem` | `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId` | Transfer detail | Read only | Null for non-transfer items |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Any case status | Timeline opened | Case in scope | Unchanged | Read only; no write; no event |

This story does not change a case status. It reads the records of past changes.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Decision log query exceeds 3 seconds or fails | Other sources render; the panel shows the section message; `unavailableSources` names Decisions | MSG-P3-023 |
| X2 | Only the creation entry exists | One item "Case created" with the entry rule version | None |
| X3 | Two events at the same time | Fixed type order, then record ID; stable on every opening | None |
| X4 | More than 50 events | Paged by 50; total returned | None |
| X5 | Case outside scope | 404; no data | MSG-P4-003 |
| X6 | Caller lacks Case record R | 403 before any read | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` |
| Existing endpoint changed | `GET /api/recovery/v1/cases/{caseId}/timeline` (API-P3-003) is listed for E2 and is delivered in E1 behind the flag. Adds `page` (default 0) and `size` (default 50, 1–200); `TimelinePage` adds `unavailableSources`; `TimelineItem` adds `reasonCode`, `fromQueueCode`, `toQueueCode`, `ruleId`. |
| Contract delta | Additive only; no field removed or renamed. |
| Backward compatibility | Compatible; the E2 consumer receives the same fields plus the additions. |
| Authorization | Case record R with scope. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 503 P3 store unavailable; a single source failure is a partial result, not a 5xx. |
| Versioning | No version bump; additive parameters and fields. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-016, REQ-OCC-007; SPEC-RWB-E1-035-003..014 | New `TimelinePanel` with paging, item detail and Loading, read only and error states. | Items render in order; paging and total; transfer detail; section message; creation-only case; masked summary; no personal data in fixtures. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-016, REQ-OCC-007; SPEC-RWB-E1-035-001..012 | New merge service, four mappers, controller changes and two published-interface calls. | Merge order; type order and record-ID tie-break; paging boundaries; each source timeout; scope; masking; creation-only case; 2-second read at 500 events. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `CaseAndWorkflowController` | Controller | `GET /cases/{caseId}/timeline`; access check; scope; problem responses. |
| `TimelineService` | Service | Reads four sources, maps to `TimelineItem`, sorts by BR1, pages. |
| `TimelineItemMapper` | Service | One mapper per source; rule ID and version or person in `by`. |
| `CaseAndWorkflowRepository` | Repository | `interaction` and `assignment` by case (`ix_interaction_case_time`, `ix_assignment_case_id`). |
| `TimelinePanel` | React component | Panel on SCR-03 with paging, item detail and section messages. |

### Merge and paging algorithm

1. Check Case record R; resolve the caller's scope; an out-of-scope case returns 404.
2. Read interactions and assignments from P3; documents through `DocumentQuery` (P5); decisions through `DecisionLogQuery` (P7).
3. Map each record to `TimelineItem` with `at`, `type`, `summary`, `by` and `reference`; mask the interaction summary.
4. Sort by `at`, then `typeOrder`, then `recordId`; `typeOrder` is decision, status change, assignment, transfer, contact, document.
5. Page from the most recent end: page 0 holds the 50 most recent items, ordered ascending within the page; the third page holds the oldest items. This satisfies AC1 (ascending within a page) and AC6 (page 0 shows the 50 most recent).
6. Return `TimelinePage` with `total` and `unavailableSources`; a source that times out is named and the rest is returned.

### Data and migration

- Reads `interaction` and `assignment` only; no migration.
- Uses `ix_interaction_case_time` and `ix_assignment_case_id`.
- Documents and decisions are read through their published interfaces; no P5 or P7 table is read.
- No write. The timeline never changes a record.

### Events

None. The timeline is a read model over records written by RWB-E1-018 to RWB-E1-028; it publishes no event
and writes no decision log entry.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-CASEOWN | Case record R | Own |
| RW-TEAMMGR | Case record R | Team |
| RW-CONDUCT, RW-AUDIT | Case record R | All |
| RW-REFADM | No Case record right; refused | — |

Every request uses Spring Security method security with the capability area and right. Scope filters the
case read; the timeline inherits the case scope.

### Observability and operations

- Metrics: timeline reads; page count; items per source; source timeouts; masked summaries; p95 latency.
- Alerts: p95 above 2 seconds; source timeout rate; P5/P7 error rate.
- Run book entry under RWB-E1-056.

### Performance

- Target: under 2 seconds at the ledger's 2031 size (NFR-070); the SIT test uses 500 events.
- Indexed reads by case and time; paging avoids materialising the full history; per-source timeout of 3 seconds.
- The merge is in memory over the page window, not over the whole case.

### Feature flag and rollback

- `rwb.p3.timeline`. Off: SCR-03 hides the Timeline panel; the endpoint returns 404.
- Rollback: turn the flag off; no migration to reverse.

## Screens and design evidence

SCR-03 Case record gains the Timeline panel. The layout is specified in
`requirement/legacy/07-screens-and-experience/recovery-workbench-screen-specifications-v1.md` (SCR-03) and
the local prototype `recovery-workbench-screen-prototype-v1-html.md`; there is no Figma source. States:
Loading (skeleton rows), read only (items in time order with type, summary, by and time; a new case shows its
creation item) and error (MSG-P3-023 for the missing source).

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-035-01 | AC1, BR1, BR2 | System | Transfer, two documents and a status change | Order transfer, demand letter, title deed, status change; TRF-007/TRF-2026.11; U-81 |
| TC-E1-035-02 | AC2, BR3 | System | Manual transfer with R04 | R04 Owner absent; from/to owner; TRF-2026.11 |
| TC-E1-035-03 | AC3, X1 | System | Decision log query times out | Interactions, documents and assignments show; MSG-P3-023 for Decisions |
| TC-E1-035-04 | AC4, X2 | System | Case with only its creation entry | One "Case created" item with the entry rule version |
| TC-E1-035-05 | AC5, X3 | System | Two records at 07:00:00 | Decision before assignment; stable order |
| TC-E1-035-06 | AC6, X4 | System | 132 events | First page 50 most recent; third page 32; total 132 |
| TC-E1-035-07 | AC7, X5 | System | Case of another team | 404 MSG-P4-003 |
| TC-E1-035-08 | X6 | Security | RW-REFADM calls the timeline | 403 MSG-P4-002 |
| TC-E1-035-09 | BR6 | Performance | Case with 500 events | Under 2 seconds |
| TC-E1-035-10 | UI states | Unit | Loading, read only, error, transfer detail | Correct state and message; masked summary; no personal data in fixtures |

## Guardrails

- No business value in code: the type order and labels are data.
- No personal data in logs, tests or prompts; contact summaries follow masking by role.
- No read of another module's tables: documents through `DocumentQuery` (P5), decisions through `DecisionLogQuery` (P7).
- The timeline never writes; it shows records as they were written.

## Out of scope

- The full timeline screen with filters and queue history (RWB-E2-016).
- The full case record view with collateral, decisions and timers (Epic 2, FEAT-WKM-08).
- Communications and notices on the timeline (Epic 2, P6).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC1, AC6; SPEC-003 | AC1 expects ascending time order, while AC6 says the first page shows the 50 most recent events. How are pages numbered? | Determines what the user sees first. | Pages are counted from the most recent end: page 0 holds the 50 most recent items, ordered ascending within the page; the third page holds the oldest 32. This satisfies both ACs. | RESOLVED | SPEC-003 |
| CLAR-002 | BR1; SPEC-002 | What is the fixed type order for equal times? | Determines stable ordering. | Decision, status change, assignment, transfer, contact, document, then record ID (story BR1). | RESOLVED | SPEC-002 |
| CLAR-003 | AC3; SPEC-006 | How is a missing source represented? | Determines the response and the panel. | `unavailableSources` names the source; the panel shows MSG-P3-023 for that section; the rest renders. | RESOLVED | SPEC-006 |
| CLAR-004 | X2; SPEC-007 | Does the creation entry come from the decision log? | Determines the first item of a new case. | Yes; the CaseCreated decision log entry is the "Case created" item with its rule version. | RESOLVED | SPEC-007 |
| CLAR-005 | API; SPEC-009 | The timeline is listed for E2; is delivering it in E1 a contract change? | Determines API impact. | The endpoint is already specified; E1 delivers it behind `rwb.p3.timeline` with additive page/size and response fields. No version bump. | RESOLVED | SPEC-009 |
| CLAR-006 | BR5; SPEC-004 | Which fields are masked in a contact summary? | Determines PDPA behaviour. | The interaction summary is personal and follows the masking rules; channel, direction, result and time are not masked. | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the API specification or the
architecture. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] — SCR-03 Case record and its Timeline panel are specified in the screen inventory and the local screen specification/prototype; no Figma source is claimed.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New SCR-03 timeline panel; existing timeline endpoint delivered in E1 with additive paging and response fields.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: new SCR-03 panel plus additive timeline paging and item fields]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 7 acceptance criteria and 6 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
