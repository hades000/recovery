# RWB-S4-E5009-CON Instruct the firm through the portal - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5009-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the firm-instruction step of rwb-litigation, split from RWB-E5-009. It fixes the instruction element and the pack reference set, the 2-working-day partner clock and its breach fact, the two provided operations API-S4-002 and API-S4-003, the four consumed facts (the case and its answer on rwb-case, the firm and the instruction on rwb-partner, the pack on rwb-document, the rule package on rwb-decision), the decision-record element of DP-03, the durable-timer element of `LitigationWorkflow`, the error set and the fakes. The partner rows, the portal operation and the working-day calendar have no source specification and are declared as the working read of the assumptions (GAP-2781 to -5; ASM-4615 to -5). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5009-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the firm-instruction step of rwb-litigation — the instruction element and the pack reference set, the 2-working-day partner clock and its breach fact, the two provided operations with their rights, the firm and instruction shape of rwb-partner, the pack shape of rwb-document, the case read and case-stage answer of rwb-case, the rule package read of rwb-decision, the decision-record element, the error set and the fakes**, so that **the app story, the two screens and the wave 3 harness build against one fixed, testable contract on Day 1 and an instruction field, a clock, a pack reference or an answer shape can never drift between rwb-litigation, rwb-partner, rwb-document and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-009 crossed four boundaries in one process: a case row with a timer, a partner row with an instruction row, a pack of documents, and a decision log row. The target splits them: the case of record, its route state, the case-stage timer and the task are rwb-case (P3); the panel firm, the `partner_instruction` row and the portal transport are rwb-partner (S9); the pack items and their index are rwb-document (P5); the rule evaluation, the instruction composition, the partner clock and the decision record are rwb-litigation (S4). Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that rwb-litigation holds no `v_ace_*` grant, so DP-05 is declared as a prohibition and no ACE fact is consumed by this step.

Three points are carried as gaps and assumptions rather than decided quietly: the instruction row and the portal operation have no published home or name and the pack is another owner's (GAP-2781), the `FIRM_MATCHED`, `FIRM_NOMINATED` and `FIRM_BREACHED_SLA` of the state machine are not Kafka subscriptions because the service publishes and consumes nothing while the case answer has no operation name (GAP-2782), and the home of the 2-working-day clock, the working-day calendar and the instruction types have no source specification (GAP-2783).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the idempotency rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `hearing` and `legal_action` are S4's, `partner` and `partner_instruction` are read or written on the partner-management contract of S9, `recovery_case`, `timer` and `task` are P3's, `document` and its index are P5's, `decision_log_entry` and `rule_row` are P7's. This document never declares another service's operation as provided.
- The four consumed owner contracts are named as documents and built against their fakes. No source read for this key names the partner read, the instruction request, the case-stage answer or the rule package read, so all four carry the placeholder (GAP-2781, GAP-2782, GAP-2785; ASM-4615, ASM-4616, ASM-4568).
- The LITIGATION rule package, its rows for R-LIT-24, R-LIT-26 and R-LIT-28 and its D7 route set are governed in rwb-decision (P7); this baseline consumes them and declares none of them.
- The working-day calendar and the instruction types are versioned reference rows whose content no source gives (GAP-2783; ASM-4617).
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its two provided operations, its four consumed facts, its own clock and decision record, and its error conditions.
2. Fix the instruction element — the case, its number, the firm, the action of the case, the instruction type, the pack reference set, the instruction reference, `instructed_at` and `due_at` — and mark the fields no source gives with the placeholder.
3. Fix the pack reference set: document references only, of the pack items that the pack stories verified on rwb-document.
4. Fix the firm and instruction element of rwb-partner: the firm, its panel status, its contract end, its coverage of the court region and case type, the conflict result, and the instruction it accepts.
5. Fix the case read and the case-stage answer of rwb-case: the route state that gates the rules, the move, the case-stage timer, the task and the rule version.
6. Fix the rule package read of rwb-decision and the decision-record element of DP-03, written before anything changes.
7. Fix the partner clock of 2 working days on the calendar in force, its start at `instructed_at` and the breach fact of R-LIT-28.
8. Publish the contract tables of section 12 and the six contract fakes.
9. Add the contract tests: the instruction element, the clock, the two provided operations and their rights, the placeholders, the error envelope, the absence of a `v_ace_*` read and of a partner, case or document write, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S4-E5009-APP, the screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a consumed fact, of an answer or of the instruction fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field of an element is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2, AC3, AC4 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X4 | A consumed fact has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC4 |
| X5 | A provided operation carries a right, an error status or an idempotency rule that TSD S4 T-A.2 does not give | The review fails the baseline and the absence test fails the build | None | AC5, AC8 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `partner` property or a `recovery_case` property | The review fails the baseline; the boundary test fails the build | None | AC8 |
| X7 | The same case and firm signal, or the same `Idempotency-Key`, arrives twice | The step answers with the stored answer and describes no second instruction and no second clock | None | AC6 |
| X8 | The partner clock is declared without a calendar, or a business value is declared as a constant | The reference-data test fails the build | None | AC1, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the two operations, the rights, the clock and the base are fixed |
| Valuable | Unblocks RWB-S4-E5009-APP, SCR-19 and SCR-20 and the wave 3 harness on Day 1, and the rwb-partner, rwb-document, rwb-case and rwb-decision teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, six fakes and five contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the firm-instruction step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of hearing and legal_action is S4, of recovery_case, timer and task is P3, of document is P5, of rule_row is P7 and of partner and partner_instruction is the partner-management contract
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The instruction element and the 2-working-day partner clock are fixed as data (new, D-RCV-60)
    Given the instruction and clock sections of the baseline
    When they are compared with R-LIT-24, R-LIT-26 and R-LIT-28 of the Business Rules and Routing Logic v4
    Then the instruction element is declared with the case, its number, the firm, the action of the case, the instruction type, the pack reference set, the instruction reference, instructed_at and due_at
    Then the fields no source gives are marked Not specified in the source documents (GAP-2781; ASM-4615)
    Then the partner clock is declared as 2 working days, the timer column of R-LIT-24 and R-LIT-26, started at instructed_at and measured on a working-day calendar that is a versioned reference row
    Then the expiry of the clock is declared as the breach fact of R-LIT-28 and neither the duration nor the calendar is a constant of the code

  Scenario: AC2 The firm and instruction shape of rwb-partner is declared and never written here (new, D-RCV-60)
    Given the partner section of the baseline
    When it is compared with partner DF-PRT-001 to DF-PRT-007 and partner_instruction DF-PRT-008 to DF-PRT-016 of the legacy data table
    Then the firm is declared as consumed with its panel status, its contract end and its coverage of the court region and case type, and the instruction as requested and answered with its reference, instructed_at and due_at
    Then the operation names are Not specified in the source documents (GAP-2781; ASM-4615) and both rows carry the placeholder
    Then the document declares no partner property, no instruction property and no instruction status as owned by rwb-litigation
    Then the three partner_instruction fields the legacy table leaves unnamed are not invented and the row names only the six it gives

  Scenario: AC3 The pack reference set of rwb-document is declared and no document is copied (new, D-RCV-60)
    Given the pack section of the baseline
    When it is compared with document DF-DOC-001 to DF-DOC-011 and with rwb-document as its owner
    Then the pack of the instruction is declared as a set of document references read on API-P5-002 with the document id, its type and its version
    Then the document declares no document body, no storage reference and no checklist row in rwb_litigation
    Then the pack is declared as the verified pack of the pack stories and not as a new checklist (DP-05 prohibition on ACE data holds here)

  Scenario: AC4 The case read and the case-stage answer of rwb-case are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case, timer and task
    Then the read is declared on API-P3-002 with the case facts and the route state, which must be FIRM_SELECTION for R-LIT-24 or FIRM_ESCALATED for R-LIT-26
    Then the answer is declared with the move FIRM_INSTRUCTED or FIRM_BREACHED_SLA, the case-stage timer, the task, the rule ID and the package version
    Then the document declares no recovery_case property, no route-state column, no timer row and no task row of its own
    Then the answer operation name is Not specified in the source documents (GAP-2782; ASM-4616) and its row carries the placeholder

  Scenario: AC5 The two provided operations, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the provided-operation and error sections of the baseline
    When they are compared with TSD S4 T-A.1 and T-A.2
    Then API-S4-002 POST /cases/{caseId}/legal-actions is declared with LegalActionRequest, a 201 with LegalAction in status OPEN, right C, a required Idempotency-Key and the errors 401, 403, 404, 409, 422 and 503
    Then API-S4-003 GET /legal-actions/{legalActionId} is declared with no request body, a 200 with LegalAction, right R, no idempotency header and the errors 401, 403, 404 and 503
    Then a malformed body answers 400 with MSG-GEN-001, a role without the Litigation right answers 403 with MSG-P4-002 and an owner that does not answer answers 503
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R
    Then no third operation is declared and the absence of API-S4-001 and API-S4-005 fails no criterion of this baseline

  Scenario: AC6 The decision-record element, the clock and the idempotency rule are declared (new, D-RCV-60)
    Given the decision and clock sections of the baseline
    When they are compared with the local decision-record library of DP-03 and with LitigationWorkflow
    Then one decision record is declared per rule outcome with the case reference, the firm reference, the rule ID, the package version in force, the inputs reference, the pack reference, the clock start and the case move
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything changes, and a failed write leaves the firm, the pack and the case unchanged with MSG-P7-003
    Then the partner clock is declared as a durable timer of LitigationWorkflow started at instructed_at and as the source of the R-LIT-28 breach fact
    Then the same signal or the same Idempotency-Key twice answers once and starts one clock
    Then the document declares no timer row, no Temporal Schedule and no Quartz job and no event of its own for the record

  Scenario: AC7 The six contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the partner fake answers the panel firm LF-2026-0009 covering the court region and case type with a passing conflict check, a firm off panel, a conflicted firm, an instruction accepted with reference INS-2026-0009, instructed_at 2026-12-08 and due_at 2026-12-10, an instruction refused, a breach mark accepted and no answer beyond 2 s
    Then the document fake answers the three pack items of case RC-2026-000609 and an empty pack
    Then the case fake answers the states FIRM_SELECTION and FIRM_ESCALATED, another state, and an accepted and a refused move
    Then the rule-package fake answers the LITIGATION package with R-LIT-24, R-LIT-26 and R-LIT-28 and a second version
    Then the decision-record library stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged SCR-19 and SCR-20 model
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC8 The naming baseline, the no-v_ace_ boundary and the empty call types are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the tables named as this service's are legal_action and hearing, and partner, partner_instruction, recovery_case, timer, task, document, rule_row and decision_log_entry are named as other owners' and consumed only through their contracts
    Then the document declares no read of a v_ace_* view, no grant on another rwb_* schema, no event published, no event consumed and no Schedule, and the absence test fails a build that adds one
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5009-APP and they copy no criterion of the legacy story, whose three criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The firm-instruction step of the litigation journey is rwb-litigation's, and the contract declares its instruction element, its pack reference set, its clock, its decision record and the facts it consumes and nothing else | Context pack (workflow `LitigationWorkflow`, queue `rwb-litigation`); Architecture v5 slide 3; FSD S4 A2.9 |
| BR2 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-009 AC4 |
| BR3 | The panel, the firm and the instruction stay with rwb-partner: the contract declares them as consumed or requested, declares no partner property as owned and describes no instruction status | Context pack (ownership rows of S4); Architecture v5 slides 4 and 8; GAP-2781 |
| BR4 | The pack stays with rwb-document: the contract declares document references and declares no body, no storage reference and no checklist row | Architecture v5 slide 10; FSD S4 A2.9.2; GAP-2781 |
| BR5 | The case move, the route state, the case-stage timer and the task stay with rwb-case: the contract declares the answer and declares no `recovery_case`, `timer` or `task` property | Context pack; TSD S4 T5.2; GAP-2782 |
| BR6 | No ACE view and no ACE table is read: the service holds no `v_ace_*` grant and this step consumes no ACE fact | DP-05; context pack (ACE data only through the owner's contract or `v_ace_*` views) |
| BR7 | The clock is 2 working days on a versioned calendar and the duration is a reference value, not a schema constant | Business Rules and Routing Logic v4 (R-LIT-24, R-LIT-26, R-LIT-28); BR-S4-009; GAP-2783 |
| BR8 | No personal data in a fact, an answer, an example or a fake: identifiers, dates, list values and a rule version only | Template and Rules v1 §R7.2 (s17); FSD S4 A2.9 field catalogue |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | The document lists only operations owned by rwb-litigation: the two of the legacy endpoints block, with the forms of TSD S4 T-A.1 | Legacy RWB-E5-009 endpoints table; TSD S4 T-A.1; GAP-2781 |
| BR12 | The rule rows of R-LIT-24, R-LIT-26 and R-LIT-28, the D7 route set and the working-day calendar are governed in rwb-decision and in reference data and are named here, never declared here | GAP-2785; ASM-4568; GAP-2783 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The instruction, the pack references, the clock, the two operations and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-partner, rwb-document, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the clock duration or a right changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a third operation, a `v_ace_*` read, a partner, case or document property, an event or a Schedule | In review |

The state machine of the case itself is the app story's: `FIRM_SELECTION` or `FIRM_ESCALATED` to `FIRM_INSTRUCTED` under R-LIT-24 and R-LIT-26, and `FIRM_INSTRUCTED` to `FIRM_BREACHED_SLA` under R-LIT-28, and the state is written by rwb-case on this baseline's answer shape.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, the two screens, the wave 3 harness and the owners of rwb-partner, rwb-document, rwb-case and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Partner-management owner | Confirms the firm and instruction element against the panel and the portal |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Instruction element | The case and its number, the firm, the action of the case with its `action_type` of LOV-LEGAL-TYPE, the instruction type, the pack reference set, the instruction reference, `instructed_at` and `due_at`; the last three are answered by rwb-partner |
| Pack reference set | The document references of the verified pack, read on API-P5-002; the document row DF-DOC-001 to DF-DOC-011 stays with P5 |
| Firm element | The firm of `partner` DF-PRT-001 to DF-PRT-007 as read: its panel status, its contract end, its coverage of the court region and case type and the conflict result; the operation name is Not specified in the source documents (GAP-2781; ASM-4615) |
| Instruction row | `partner_instruction` DF-PRT-008 to DF-PRT-016 of S9, requested and answered; the three fields the legacy table does not name are not declared here |
| Case answer | The route state, the move, the case-stage timer start and expiry, the task, the rule ID and the package version, all P3's rows and columns (GAP-2782; ASM-4616) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Clock | The durable timer of `LitigationWorkflow` of 2 working days from `instructed_at`, on a working-day calendar whose content is Not specified in the source documents (GAP-2783; ASM-4617); the `timer` row DF-WRK-027 to DF-WRK-036 is P3's and is not declared here |
| Rule rows | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force (GAP-2785) |
| Not written here | `partner` and `partner_instruction` (S9), `recovery_case`, `timer` and `task` (P3), `document` (P5), every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the two operations of AC5 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). The two operations are the endpoints block of the legacy story and rows of TSD S4 T-A.1, re-based on the service path.

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | `LegalActionRequest`; `caseId` from the path | 201 with `LegalAction` in status `OPEN` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | None | 200 with `LegalAction` with pack, instruction, hearings and judgment | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |

The purposes are TSD S4 T-A.2's: API-S4-002 opens a legal action and its pack, and API-S4-003 reads a legal action with its pack, instruction, hearings and judgment. API-S4-001 `POST /notices/{noticeId}/approve` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` are the notice and hearing stories' and a third operation here fails the review of AC8 (BR11).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` (API-P3-002) | `/api/recovery/case/v1` | P3 rwb-case | The case facts and the route state that gates the two rules; faked |
| The case-stage answer (operation name Not specified in the source documents (GAP-2782; ASM-4616)) | rwb-case (P3) | P3 rwb-case | The move, the case-stage timer, the task and the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The firm read and the instruction request (operation name Not specified in the source documents (GAP-2781; ASM-4615)) | `/api/recovery/partner/v1` | P9 rwb-partner | The firm with its panel status, contract end, coverage and conflict result, and the instruction request answered with its reference, `instructed_at` and `due_at`; faked |
| `GET /cases/{caseId}/documents` (API-P5-002) | `/api/recovery/document/v1` | P5 rwb-document | The pack item references; faked |
| The rule package read (operation name Not specified in the source documents (GAP-2785; ASM-4568)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-24, R-LIT-26 and R-LIT-28; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four cross-service rows are contract dependencies of class C in fact that the plan's C row does not carry, and the absence is recorded as GAP-2781, GAP-2782 and GAP-2785 with their assumptions.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service (GAP-2782; ASM-4616).

#### 12.4 Events consumed

None. `FIRM_MATCHED` and `FIRM_NOMINATED` are the event names of R-LIT-24 and R-LIT-26 in the state machine, not a Kafka subscription: the service publishes and consumes nothing, DP-09 is not in the pattern set of this key, and the firm arrives on a workflow signal and is read on the P9 contract of 12.2. This baseline declares no consumer group, no subscription and no inbox of its own (GAP-2782; ASM-4616).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the step; its signals and its outcome for the parent are declared, not built; it holds the partner clock |
| `instructFirm` | Activity, the one firm-instruction step | `rwb-litigation` | The case, the firm and the pack references in; the rule ID with its package version, the instruction reference, `instructed_at`, `due_at`, the clock fact and the case move out |

The activity name and the state names of the step are target design choices and are fixed by no source; the trigger is read as the arrival of the firm signal for a case whose pack is verified, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2782; ASM-4616). No activity is registered by this story.

#### 12.6 Schedules

None. The clock of the step is a durable timer of `LitigationWorkflow` of 2 working days from `instructed_at`, and it fires the breach fact of R-LIT-28. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 is owned or moved here (GAP-2783; ASM-4617).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | This service's action row, opened on API-S4-002 and read on API-S4-003 |
| hearing | S4 (`rwb_litigation`) | This service's hearing row; not touched by the step |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated signal and of the repeated POST |

`partner` and `partner_instruction` (S9), `recovery_case`, `timer` and `task` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner panel and instruction fake | The panel firm `LF-2026-0009` covering the court region and case type with a passing conflict check; a firm off panel and a conflicted firm; an instruction accepted with reference `INS-2026-0009`, `instructed_at` 2026-12-08 and `due_at` 2026-12-10; an instruction refused; a breach mark accepted; no answer beyond 2 s | AC2, AC7 |
| rwb-document pack fake | The three pack items of `RC-2026-000609` with their document ids, types and versions; an empty pack | AC3, AC7 |
| rwb-case fake | The states `FIRM_SELECTION` and `FIRM_ESCALATED` and another state; an accepted move to `FIRM_INSTRUCTED` and to `FIRM_BREACHED_SLA`; a refused move | AC4, AC7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-24, R-LIT-26 and R-LIT-28, and a second version | AC6, AC7 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC7 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 model for case `RC-2026-000609` | AC7 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three unnamed consumed rows, the instruction fields and the working-day calendar are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2781, GAP-2782, GAP-2783, GAP-2785).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | API-S4-002 and API-S4-003 provided; the case read, the case-stage answer, the firm read and instruction request, the pack read and the rule package read consumed; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered, 1 durable timer | `LitigationWorkflow`, `instructFirm` and the 2-working-day clock; no Schedule |
| File | None | The portal is a REST contract of S9 and the pack is a set of references; no file is declared here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no partner, case, pack or timer. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and six fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-instruction.v1.yaml` for the two provided operations, the consumed and answered elements, the instruction element and the clock element of `LitigationWorkflow`, the contract README rows for the consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the app story obeys: the record is written before the instruction is requested. DP-13 fixes the base of the two provided operations. DP-19 is behind SCR-19 and SCR-20, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan already carries for the app story. The four consumed contracts are C dependencies in fact and not in the metadata row, which is None (GAP-2781, GAP-2782, GAP-2785).

**Build steps**

1. Write the instruction element and the pack reference set of AC1 and AC3 with their placeholders and validate them in the pipeline.
2. Write the two provided operations of AC5 with their rights, idempotency and error statuses, and the absence test for a third operation.
3. Write the partner element of AC2 and its absence test for a partner write.
4. Write the case read and the case-stage answer of AC4 with their placeholders.
5. Write the decision-record, clock and idempotency elements of AC6 and validate them against the library schema and the workflow contract.
6. Publish the six fakes of AC7 and the drift test.
7. Record the naming baseline, the empty call types and the boundary of AC8, then tag the baseline and collect the consumer sign-off.

**Done when.** The contract tests pass, the two operations and their rights match TSD S4 T-A.2, the six fakes answer every consumed path and the drift test is green, the absence test blocks a third operation, a `v_ace_*` read, a partner, case or document write and a Schedule, and the app story, the two screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | The pack items the instruction needs are missing, a path the app story owns | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim of the case is close to expiry, a warning the app story shows | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of an element, of an answer or of the instruction is absent or invalid | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the row declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | Carried from the message set of this feature, whose VR-S4-009-1 tests the freshness of the ACE batch of the source; the check is the owner's and no path of this step raises it (GAP-2781; ASM-4615) | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its pack, instructed and breached states and SCR-20 Enforcement workspace in its states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the instruction facts, rwb-partner for the firm and the instruction, rwb-document for the pack and rwb-case for the case and its route state; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The pack-defect, refusal and not-recorded states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-009-02 | AC1, AC5 | Contract | The instruction of case `RC-2026-000609` to firm `LF-2026-0009`; the contract half answers the instruction element, the two operations and the 2-working-day clock |
| TC-E5-009-03 | AC1, AC4 | Contract | The state `FIRM_ESCALATED` and a nominated firm; the contract half answers the clock and the move to `FIRM_INSTRUCTED` |
| TC-E5-009-04 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element |
| TC-E5-009-05 | AC5, AC8 | Contract | RW-LITOFF holds CRUA and RW-ENFORCE holds CRU; the contract half answers the rights and the absence of a third operation |
| TC-E5-009-06 | AC6, AC7 | Contract | The library stub stopped and a signal that fires no rule; the contract half answers the failure path and the fakes |
| TC-S4-E5009-CON-01 | AC1, AC3 | Contract | The instruction element, the pack reference set and the clock with its calendar validate; no document body and no constant duration is declared |
| TC-S4-E5009-CON-02 | AC2, AC4 | Contract | The partner element over DF-PRT-001 to DF-PRT-016 and the case answer validate with their placeholders and one hop with a 2 s budget |
| TC-S4-E5009-CON-03 | AC5, AC6 | Contract | The error envelope, the rights, the idempotency rule, the decision-record element and the clock validate |
| TC-S4-E5009-CON-04 | AC7, AC8 | Contract | The six fakes match the document and a drifted fake fails the build; the absence test for a third operation, a `v_ace_*` read, a partner, case or document property, an event and a Schedule |

The five legacy cases are the legacy cases of RWB-E5-009 that the app story carries, in their legacy order, carried here as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5009-APP. TC-E5-009-01 covers legacy AC1, which the plan places in RWB-ITG-E5009-ITG, so it is not carried here. The legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5009-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the 2 working days, the working-day calendar, the instruction types, the D7 route set and the message texts stay reference rows and rule rows, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: identifiers, dates, list values and a rule version only; every example is synthetic.
- The partner stays with rwb-partner and the case with rwb-case: the document declares no partner property as owned, no instruction status, no `recovery_case` property, no timer row and no task row (BR3, BR5).
- The pack stays with rwb-document: the document declares document references only and no body, storage reference or checklist row (BR4).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on ACE, and the boundary test fails a build that adds one (DP-05).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR9).
- Two provided operations only, both of TSD S4 T-A.1: a third operation fails the review and the absence test (BR11).
- No retired element is introduced: the absence test of AC8 fails a build that declares an event, a Schedule, a Quartz row or a shared job table.
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal; the contract fixes the instruction element, the pack reference set, the clock and the consumed facts on which the instruction is issued (FSD S4 requirements served); the legacy story master carries no requirement ID (GAP-2784; ASM-4618) | The instruction element, the pack reference set, the two provided operations and the clock | TC-E5-009-02, TC-S4-E5009-CON-01, TC-S4-E5009-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two provided operations and the five consumed rows with their budget and breaker | TC-S4-E5009-CON-02, TC-S4-E5009-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-009, disposition Split (rework) |
| Legacy criteria | AC2, AC3 and AC4 owned word for word by RWB-S4-E5009-APP, and AC1 by RWB-ITG-E5009-ITG; this baseline copies none of them |
| Test cases | The five legacy cases carried by the app story as the contract half, and the four new contract cases TC-S4-E5009-CON-01 to -04 |
| Feature and screens | FEAT-LIT-09, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-24, R-LIT-26 and R-LIT-28, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2785) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal with durable timers), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the step, the evaluation of R-LIT-24, R-LIT-26 and R-LIT-28, the instruction request, the clock and the case answer: RWB-S4-E5009-APP.
- The panel, the firm, the `partner_instruction` row, the instruction status and the portal transport: rwb-partner (S9) and the partner-management stories (GAP-2781; ASM-4615).
- The pack items, their index, the checklist and the document bodies: rwb-document (P5) and the pack stories of this service.
- The case of record, its route states, the parent `CaseWorkflow`, the case-stage timer and the task: rwb-case (P3) and its slice of this legacy key (GAP-2782; ASM-4616).
- The firm selection out of the panel and the escalation: FEAT-LIT-08 and the firm-selection story of this service.
- The authoring, testing, approval and versioning of the LITIGATION package and of the rule rows of R-LIT-24, R-LIT-26 and R-LIT-28: rwb-decision (P7) (GAP-2785; ASM-4568).
- The working-day calendar and the instruction types as values: the business owner of S4 and the reference-data owner (GAP-2783; ASM-4617).
- The rights, roles, scope and masking data themselves, and the composite route and screen field list of SCR-19 and SCR-20: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence, including legacy AC1: the wave 3 harness and RWB-ITG-E5009-ITG, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
