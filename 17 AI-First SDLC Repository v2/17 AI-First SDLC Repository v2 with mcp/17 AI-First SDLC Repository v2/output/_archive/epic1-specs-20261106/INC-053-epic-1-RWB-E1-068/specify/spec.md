# Technical Specification — RWB-E1-068 Interaction ledger read interface

| Field | Value |
|---|---|
| Story | RWB-E1-068 — Interaction ledger read interface |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-053-epic-1-RWB-E1-068` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-ILG-003, 006, 014); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 068 Interaction ledger read interface v1.md`; FSD P1 A2.18 context; TSD P1 T3.1, T5.2 |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1 and 4; REQ-ILG-003, REQ-ILG-006, REQ-ILG-014; FEAT-ILG-03; US-RWB-E1-068; CTL-09, CTL-11; DL26; NFR-070 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — a new history panel (`CaseHistoryPanel`) is added to SCR-03 Case record with channel, actor and date filters, paging, Loading, Empty and Error states. |
| Logic In Scope | `YES` — filter validation, scope check, ordered paged query, masking and PII access logging. |
| API In Scope | `YES` — the existing `GET /api/recovery/v1/cases/{caseId}/interactions` (API-P3-014) is extended with the `actor` query parameter and new response fields. |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `interaction` (read); `recovery_case` (scope via P3); `ix_interaction_case_time` (existing); new index (`case_id`, `actor_ref`); SCR-03 history panel (new). |
| New Nodes Required | `YES` — `InteractionLedgerReader`, `LedgerReadService`, `InteractionRepository` read query, `CaseHistoryPanel`; P3 `InteractionsHandler` extension. |
| Inherited Existing Behavior | Ledger store and writer (RWB-E1-066); masking interface (RWB-E1-037); `CaseScopeQuery` (RWB-E1-016); SCR-03 (RWB-E1-023 read only). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The ledger reads back in one ordered sequence, by occurred time and then case sequence. | SPEC-RWB-E1-068-001 | DIRECT | `ORDER BY occurred_at, case_seq`. | COVERED |
| BR2 | The ledger can be filtered by channel, actor and date range through one interface. | SPEC-RWB-E1-068-002 | DIRECT | Optional `channel`, `actor`, `from`, `to`. | COVERED |
| BR3 | Entries carry channel, who or what was reached, and the outcome where the interaction had one. | SPEC-RWB-E1-068-001, 007 | DIRECT | Response fields from `interaction`. | COVERED |
| BR4 | Personal data in the ledger is masked by role on the same rules as the case record. | SPEC-RWB-E1-068-005 | DIRECT | `MaskingPolicy` on `summary`; default `MASKED`. | COVERED |
| BR5 | A case outside the caller's scope is refused. | SPEC-RWB-E1-068-004 | DIRECT | `CaseScopeQuery`; 404 MSG-P4-003. | COVERED |
| BR6 | No consumer queries the interaction table directly. | SPEC-RWB-E1-068-009 | DIRECT | Architecture test; only `InteractionLedgerReader`. | COVERED |
| AC1 | Nine entries return ordered earliest first; each names its source system and reference. | SPEC-RWB-E1-068-001, 007 | DIRECT | Order and source fields. | COVERED |
| AC2 | Three filtered reads return 3 calls, 2 visits and 4 Workbench entries. | SPEC-RWB-E1-068-002 | DIRECT | Channel, actor and date filters. | COVERED |
| AC3 | The SCR-03 history panel shows the 9 entries; no class outside the ledger package queries the table. | SPEC-RWB-E1-068-009, 012 | DIRECT | Panel calls the reader; architecture test. | COVERED |
| AC4 | `from` after `to`: 422 MSG-GEN-003 for "to" and "from". | SPEC-RWB-E1-068-002, 010 | DIRECT | Filter validation before query. | COVERED |
| AC5 | A case outside the caller's scope: 404 MSG-P4-003. | SPEC-RWB-E1-068-004 | DIRECT | Scope check before read. | COVERED |
| AC6 | No masking rule for `summary`: summary `MASKED`; channel, result, promise amount and date in full. | SPEC-RWB-E1-068-005 | DIRECT | Only personal fields masked. | COVERED |
| AC7 | Size 200 returns 9 entries; size 201 returns 422 MSG-GEN-002 for "size" between 1 and 200. | SPEC-RWB-E1-068-003, 010 | DIRECT | Property-driven bounds. | COVERED |
| AC8 | A case with no entries returns 0 items and total 0; the panel shows Empty. | SPEC-RWB-E1-068-006, 012 | DIRECT | Empty page and Empty state. | COVERED |
| X1 | `from` is after `to`. | SPEC-RWB-E1-068-002 | DIRECT | 422 MSG-GEN-003. | COVERED |
| X2 | Case outside the caller's scope. | SPEC-RWB-E1-068-004 | DIRECT | 404 MSG-P4-003. | COVERED |
| X3 | No masking rule allows the summary. | SPEC-RWB-E1-068-005 | DIRECT | Summary `MASKED`. | COVERED |
| X4 | Page size above 200. | SPEC-RWB-E1-068-003 | DIRECT | 422 MSG-GEN-002. | COVERED |
| X5 | The case has no entries. | SPEC-RWB-E1-068-006 | DIRECT | 200 with empty page; Empty state. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **to read a case's ledger in one ordered sequence, filtered by channel, actor or date range**, so that **I can see what has happened to it before I decide anything**.

The story delivers one read path and the SCR-03 history panel. Every consumer — the case record, later
timeline screens and reports — reads through `InteractionLedgerReader`, so ordering and masking are
defined once. The panel is read only; recording remains RWB-E1-066/067 and the full timeline screen
SCR-04 is Epic 2.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | SCR-03 history panel loads, or a client calls `GET /cases/{caseId}/interactions` with optional filters. |
| Preconditions | RWB-E1-066 ledger fields exist; P4 masking interface available (rules may be empty, DL26); P3 `CaseScopeQuery` published; caller holds Case record R. |
| Input | Path `caseId`; query `channel`, `actor`, `from`, `to`, `page`, `size`; caller roles and scope. |
| Output | `InteractionPage` (items, page, size, total); PII access log entry when a personal field is returned unmasked. |
| Feature flag | `rwb.dataengine.ledger-read`. Off: the panel shows the prior case-record history path. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `interaction` | `occurred_at` | Stored | Read only | Sort key, earliest first |
| `interaction` | `case_seq` | Stored | Read only | Tie-break after `occurred_at` |
| `interaction` | `event_code` | Stored | Read only | Returned as `eventCode` |
| `interaction` | `channel` | Stored | Read only | Filter; must be in `LOV-CHANNEL` when supplied |
| `interaction` | `actor_ref` | Stored | Read only | Filter; exact match |
| `interaction` | `contact_result` | Stored | Read only | Returned where present |
| `interaction` | `promise_amount`, `promise_date` | Stored | Read only | Returned in full; not personal |
| `interaction` | `summary` | Stored | Read only | Personal; masked by role |
| `interaction` | `source_system`, `source_ref` | Stored | Read only | Returned on each entry |
| `interaction` | `decision_log_id` | Stored | Read only | Returned as `decisionLogEntryId` |
| Query | `page` | Request | User sets | 0-based; default 0 |
| Query | `size` | Request | User sets | 1–200; default 50 |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| Read request | — | Valid request in scope | Returned | Page of entries; PII log when unmasked personal data returned |
| Read request | — | Invalid filter or size | Refused | 422; nothing read |
| Read request | — | Case out of scope | Refused | 404; nothing read |
| Read request | — | Store unavailable | Refused | 503 MSG-GEN-006 |
| Ledger entry | Stored | Any read | Unchanged | The read changes nothing |

No case status changes. The story reads and changes nothing.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | `from` after `to` | 422; nothing returned | MSG-GEN-003 |
| X2 | Case outside the caller's scope | 404 | MSG-P4-003 |
| X3 | No masking rule allows the summary | Summary `MASKED` | None |
| X4 | Page size above 200 | 422 | MSG-GEN-002 |
| X5 | Case has no entries | 200 with an empty page; panel Empty state | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` |
| Existing endpoint changed | `GET /api/recovery/v1/cases/{caseId}/interactions` (API-P3-014). |
| Contract delta | New query parameter `actor`; `Interaction` gains `eventCode`, `caseSeq`, `actorType`, `actorRef`, `sourceRef`, `decisionLogEntryId`; `summary` masked by role. |
| Backward compatibility | Additive for readers; existing fields keep their meaning. A client that ignores the new fields is unaffected. |
| Authorization | Case record R with scope. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 422 MSG-GEN-001/002/003; 503 MSG-GEN-006. |
| Versioning | No version bump; additive change within v1. Contract tests from the API specification (RWB-TE-003). |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-ILG-006; SPEC-RWB-E1-068-012 | New `CaseHistoryPanel` with filters, paging, Loading, Empty and Error states on SCR-03. | Filter changes issue the right query; paging; empty state; error message; masked summary rendering; no personal data in test fixtures. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-ILG-003, 006, 014; SPEC-RWB-E1-068-001..011 | New reader, read service, repository query, index and P3 handler extension. | Ordering; each filter; combined filters; size boundaries; invalid date range; scope denial; masking; empty page; 2-second read at 5,000 entries. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `InteractionLedgerReader` | Published interface | The one read path for the ledger. |
| `LedgerReadService` | Service | Scope check, filter validation, ordered query, masking, PII log. |
| `InteractionRepository` | Repository | Read by case and filter, ordered by `occurred_at`, `case_seq`. |
| `InteractionsHandler` | Controller (P3) | API-P3-014; adds `actor`; delegates to the reader. |
| `CaseHistoryPanel` | React component | SCR-03 history panel with filters, paging, Loading, Empty, Error. |

Package `recovery.dataengine.ledger.read`. The panel uses TanStack Query and the generated client type;
no hand-written duplicate of the API type.

### Data and migration

No new table. Query on `interaction` by `case_id` with optional `channel`, `actor_ref` and
`occurred_at` range, ordered by `occurred_at`, `case_seq`, using `ix_interaction_case_time`. A Flyway
migration adds index (`case_id`, `actor_ref`) for the actor filter. No column change.

### Read algorithm

1. The P3 handler checks Case record R through the ACE access check.
2. Check the case is in scope through `CaseScopeQuery`.
3. Validate: `channel` in `LOV-CHANNEL`, `from` not after `to`, `size` 1–200, `page` >= 0.
4. Query the page ordered by `occurred_at`, then `case_seq`.
5. Mask `summary` through `MaskingPolicy`; no rule means `MASKED`.
6. Write the PII access log when a personal field is returned unmasked; field names, not values.
7. Return `InteractionPage` with `total`.

**Transaction.** The read is read-only; the only write is the PII access log, which must succeed before
the response is returned. No event is published by this story.

### UI behaviour

SCR-03 Case record, read-only history panel: entries earliest first, each with time, event, actor,
channel, outcome and source. Filters: channel, actor and date range. Paging with the default 50 and the
maximum 200. States: Loading (skeleton rows), Empty (a sentence that no interaction is recorded on the
case), Error (message above the panel). The panel is read only; no edit or delete affordance.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-CASEOWN | Case record R | Own |
| RW-TEAMMGR | Case record R | Team |
| RW-CONDUCT, RW-AUDIT and other roles with Case record R | Case record R | Their scope |
| RW-REFADM | No Case record right; may not read | — |
| RW-COMPLY | Owns the masking rules (DL26) | — |

### Observability and operations

- Metrics: reads per filter; empty results; masked summaries; PII log writes; read latency p95.
- Alerts: read latency above 2 seconds; store unavailable.
- Audit: PII access log for unmasked personal reads.
- Run book entry under RWB-E1-056.

### Performance

- Target: one case history read under 2 seconds at 2031 size (NFR-070; DL11).
- Indexed access by case and time; optional actor index; paging avoids full materialisation.
- Test with 5,000 entries for one case.

### Feature flag and rollback

`rwb.dataengine.ledger-read`. Off: the panel falls back to the prior case-record history path. Rollback:
turn the flag off; the added index remains and is harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-068-01 | AC1, BR1, BR3 | System | Case RW-2026-000401 with 9 entries from EFS, Workbench and owner | 9 entries earliest first; each names source system and reference |
| TC-E1-068-02 | AC2, BR2 | System | Filters channel CALL, actor u-owner-04, 2026-12-01 to 2026-12-06 | 3, 2 and 4 entries respectively |
| TC-E1-068-03 | AC3, BR6 | System | SCR-03 panel; architecture test | 9 entries shown; no class outside the ledger package queries `interaction` |
| TC-E1-068-04 | AC4, X1 | System | `from` 2026-12-06, `to` 2026-12-01 | 422 MSG-GEN-003 |
| TC-E1-068-05 | AC5, BR5 | System | RW-CASEOWN u-owner-05, case not owned | 404 MSG-P4-003 |
| TC-E1-068-06 | AC6, BR4 | System | No masking rule for `summary` | Summary `MASKED`; channel, result, promise in full |
| TC-E1-068-07 | AC7, X4 | System | Size 200 and 201 | 200 returns 9 entries; 201 returns 422 MSG-GEN-002 |
| TC-E1-068-08 | AC8, X5 | System | Case RW-2026-000402 with no entries | 0 items; total 0; Empty state |
| TC-E1-068-09 | X2 | System | Case outside scope | 404 MSG-P4-003 |
| TC-E1-068-10 | Access | Security | RW-REFADM reads the ledger | 403 MSG-P4-002 |
| TC-E1-068-11 | NFR-070 | Performance | One case with 5,000 entries | Read under 2 seconds |
| TC-E1-068-12 | UI states | Unit | Loading, Empty, Error, masked summary | Correct state and message; no personal data in fixtures |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC7; SPEC-003 | Are the page-size limits properties or constants? | Determines configurability. | Properties: default 50, maximum 200 (story §13). | RESOLVED | SPEC-003 |
| CLAR-002 | BR4; SPEC-005 | What is masked? | Determines field coverage. | `interaction.summary` is personal; channel, result, promise amount and date are not (AC6). | RESOLVED | SPEC-005 |
| CLAR-003 | API; SPEC-007 | Is the endpoint new? | Determines API impact. | Existing API-P3-014; additive `actor` parameter and response fields. | RESOLVED | SPEC-007 |
| CLAR-004 | AC3; SPEC-012 | Does the story build SCR-03 or only the panel? | Determines UI scope. | The panel only; SCR-03 is read only from RWB-E1-023. | RESOLVED | SPEC-012 |
| CLAR-005 | BR1; SPEC-001 | What is the tie-break when times are equal? | Determines stable ordering. | `occurred_at`, then `case_seq`; story BR1. | RESOLVED | SPEC-001 |
| CLAR-006 | Error handling; SPEC-010 | What happens when the PII log write fails on a read? | Determines response. | Follows RWB-E1-016 BR4: a read that cannot be logged is refused; 503 MSG-GEN-006. The API description's MSG-P7-003 reference is a copy error. | RESOLVED | SPEC-005, 010 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the API specification or
RWB-E1-016. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] — SCR-03 Case record and its read-only history panel are specified in the screen inventory and FSD Appendix B; no Figma source is claimed.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: Existing ledger read endpoint extended and a new SCR-03 history panel added; additive contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: actor filter and new response fields on API-P3-014 plus the SCR-03 panel]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria and 5 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
