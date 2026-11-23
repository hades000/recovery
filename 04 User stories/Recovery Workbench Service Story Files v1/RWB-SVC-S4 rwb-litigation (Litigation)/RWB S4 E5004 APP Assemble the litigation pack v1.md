# RWB-S4-E5004-APP Assemble the litigation pack

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-E |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5004-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-004 for rwb-litigation (S4). The pack is built from the document index of rwb-document and the case facts of rwb-case, presented for verification on base `/api/recovery/litigation/v1` (DP-13); the decision is written through the local decision-record library before any state changes (DP-03); the two screens are read through the gateway-bff composite route (DP-19); the case states, the task and the document index stay with rwb-case and rwb-document and are consumed and faked. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the Workbench to build the litigation pack from the document index and the case facts, ready for the officer to verify — holding the notice when its template is withdrawn, presenting the pack once every pack item is present, and writing one decision record with the rule version before either state moves**, so that **cases reach court faster with complete packs, and the document index, the case and its states, the task and the decision ledger stay with the services that own them**.

This story owns the pack assembly of a litigation case, and nothing else:

- the pack composition of a case: the pack item list read from the document index of rwb-document and the case facts of rwb-case, held in memory for the officer and never written as a table of its own;
- the evaluation of R-LIT-04 from `NOTICE_GENERATED` on `TEMPLATE_WITHDRAWN` — hold generation and raise a task to the litigation officer, to `NOTICE_BLOCKED` (FSD S4 v3 A2.4.3.1; Business Rules and Routing Logic v4);
- the evaluation of R-LIT-16 from `PACK_ASSEMBLY` on `PACK_COMPLETE` — present the pack to the litigation officer for verification, to `PACK_VERIFIED`;
- one decision record per evaluation through the local decision-record library, with the rule ID and the version in force, written before the pack is presented or the state announced (DP-03, legacy AC1 and AC4);
- the announcement of the two state facts to rwb-case, and the task raise to the litigation officer on the case contract; both are consumed and faked;
- the read surface of SCR-18 Notice approval and SCR-19 Litigation workspace, through the gateway-bff composite route (DP-19).

It does not own the documents, the case, the notice, the states or the ledger. `document`, `document_field` and the checklist are rwb-document's (P5); `recovery_case`, its stage, its states and `task` are rwb-case's (P3); `notice` and the demand notice itself are rwb-comms's (P6); the decision store and the central ledger are the platform library's and rwb-decision's (P7); the rule packages are rwb-decision's. It does not check the pack against the defect list (`RWB-S4-E5005-APP`), recover a missing document (`RWB-S4-E5006-APP`) or approve the filing (`RWB-S4-E5007-APP`). No component of this story writes a `recovery_case`, `task`, `document`, `notice`, `decision_log_entry` or `rule_row` row, and none reads a `v_ace_*` view.

### 2. Business rationale

Litigation takes 21 days to file, packs are incomplete and law-firm progress is not tracked (FSD S4 v3 A1.3 and A2.4.1). The pack is the first place that delay is created: the officer rebuilds it by hand from the document shelf, and a withdrawn template is found out after the pack has been sent. The legacy key assembled the pack inside one process against one `recovery` schema, with the case, the documents, the notice, the task and the decision log entry all in reach.

In the target that work is cut four ways. The documents and their index are rwb-document's and are read on API-P5-002 and API-P5-008. The case, its stage, its states and its tasks are rwb-case's and are read on API-P3-002 and moved on an announcement. The notice and its template status are rwb-comms's and rwb-case's reference data. The decision record is the platform library's element on the shared `rwb.decision-record.v1`. What is left — and what this story builds — is the composition, the two rule evaluations and the announcement.

The state facts matter more than the rows. R-LIT-04's `NOTICE_BLOCKED` and R-LIT-16's `PACK_VERIFIED` are **not** values of LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`), so they are states of the case of record and not the status of a legal action; this story announces them and writes no case row (TSD S4 T3.2; GAP-2754; ASM-4584).

The pack itself has no table in the Ownership Map and no row in TSD S4 T3.1, whose two objects are `legal_action` and `hearing`. The pack is therefore derived on every read from the document index and the case facts, and the only persisted traces of an assembly are the decision record and the state the case of record holds. That is carried as a gap and not decided quietly (GAP-2753; ASM-4583), as is the missing trigger of AC1 (GAP-2756; ASM-4586).

The three patterns are applied where the legacy components sat: DP-03 for the `DecisionLogWriter` that becomes the local decision-record library, DP-13 for the `/api/recovery/v1` base that becomes `/api/recovery/litigation/v1`, and DP-19 for the screens that become gateway-bff composite routes. The four reads this story consumes — the document index, the case facts, the case move and the reference lists — carry no C row in the plan, which is recorded once (GAP-2751; ASM-4581).

It serves FEAT-LIT-04 "Assemble the litigation pack", holds the FSD S4 measure "litigation turnaround, 6 days", and keeps the legacy prerequisite FEAT-DCM-02 as a consumed read of the P5 index instead of a local index. The legacy master and the Epics 3 to 8 specification carry no requirement identifier for the key, so the story traces to the feature until the PRD adds them (GAP-2752; ASM-4582).

### 3. Preconditions

- `RWB-S4-E5004-CON` is published: the three legal-action operations on `/api/recovery/litigation/v1`, the `LegalAction`, `LegalActionRequest` and `LegalActionUpdate` schemas, the error envelope, the `Idempotency-Key` rule and the fake. This is the first build dependency and the story starts against it on Day 1.
- The `legal_action` and `hearing` tables exist in schema `rwb_litigation` with the columns of TSD S4 T3.1 and the standard columns of T3.0. This story creates no table and adds no column.
- The document index of rwb-document (P5) is live and faked: `GET /cases/{caseId}/documents` (API-P5-002) for the pack items, and `GET /cases/{caseId}/document-checklist` (API-P5-008) for the checklist the pack is measured against. Both are built in Epic 1 (FEAT-DCM-02). No C row carries them (GAP-2751; ASM-4581).
- The case contract of rwb-case answers the case facts on `GET /cases/{caseId}` (API-P3-002). The case move and the task raise are described in prose and have no published operation, so both carry the placeholder `Not specified in the source documents (GAP-2751; ASM-4581)`.
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`), and the record it writes is hash-linked on `rwb.decision-record.v1`. The story builds against its fake until the platform contract story publishes.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-18 and SCR-19, so the two read surfaces are available from Day 1 (DP-19).
- LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read as values in force with their version, on the reference data of rwb-case. DP-07 is not in this story's pattern set and that read carries no dependency row either (GAP-2751; ASM-4581).
- The caller holds a Workbench role with the Litigation right of the operation it calls (TSD S4 T6.1). DP-08 is not in the pattern set: the right is enforced at the edge for the screen path and on the write paths by this story's validator.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02), with no grant on another `rwb_*` schema and none on a `v_ace_*` view.

### 4. Flow

1. The litigation officer opens SCR-19 Litigation workspace for a case through the gateway-bff composite route (DP-19). The workspace answers the legal actions of the case on `GET /legal-actions/{legalActionId}` of `/api/recovery/litigation/v1` (API-S4-003).
2. `PackIndexReader` reads the pack item list on `GET /cases/{caseId}/documents` (API-P5-002) and the checklist the pack is measured against on `GET /cases/{caseId}/document-checklist` (API-P5-008). One hop each, 2 s timeout, breaker per downstream; nothing of the document is copied into `rwb_litigation`.
3. `CaseFactsReader` reads the case facts on `GET /cases/{caseId}` (API-P3-002): case number, product group, stage code, the parties by reference and the dates the pack needs. No case field is written here.
4. `PackComposer` composes the pack in memory: every document the checklist names, matched to an index entry by document type and date, with the case facts that fill the pack's cover sheet. A missing entry is named and not invented; the pack is presented as complete or as holding the missing items.
5. The trigger of the assembly is read as the case state and the template status in force. Where the template is `withdrawn`, `TemplateWithdrawalCheck` evaluates R-LIT-04 and the pack is not generated.
6. `PackDecisionWriter` evaluates the rule in force with the package version returned for the route set, and writes one decision record through the local decision-record library **before** anything is presented or announced: the rule ID (`R-LIT-04` or `R-LIT-16`), the version in force, the inputs reference, the inputs hash, the answer and the decision code read from LOV-DECISION.
7. On R-LIT-04, `CaseTaskClient` raises a task to the litigation officer on the case contract — the case reference, the task code for the pack hold, the capability area, the rule ID and its version — and `CaseStateClient` announces the state fact `NOTICE_BLOCKED`. The task row and the case state are rwb-case's.
8. On R-LIT-16, `PackPresenter` returns the composed pack to SCR-19 with `GET /legal-actions/{legalActionId}` (API-S4-003) and the workspace shows it for verification; `CaseStateClient` announces the state fact `PACK_VERIFIED`.
9. On an officer rejection at verification, R-LIT-21 returns the pack to the legal document agent and the state returns to `PACK_ASSEMBLY`. The evaluation and the announcement are the same two components; the rework itself is `RWB-S4-E5006-APP`'s and the defect check is `RWB-S4-E5005-APP`'s.
10. Where the pack opens a legal action, the officer writes it on `POST /cases/{caseId}/legal-actions` (API-S4-002) with `actionType = CIVIL_CASE` of LOV-LEGAL-TYPE, and records the court references as they arrive on `PATCH /legal-actions/{legalActionId}` (API-S4-004). The row stays `OPEN` until a filing date is written.
11. The same request twice, or the same `Idempotency-Key` twice, writes one row, writes one decision record and sends one announcement; the repeat is counted under R-UNI-40.
12. SCR-18 Notice approval and SCR-19 read the case state from rwb-case and the notice state from rwb-comms next to the pack of this service, read only, through the composite route.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document index does not answer inside 2 s, or its breaker is open | The pack is not composed and nothing is presented; nothing is written, because no decision has been taken | None | AC1 |
| X2 | The case facts do not answer inside 2 s, or the case is outside the caller's scope | The answer is 404 for an out-of-scope case and 503 for a timeout; nothing is written | None | AC1 |
| X3 | A checklist item has no index entry | The pack is composed with the item named as missing; it is presented as incomplete and never as complete, and R-LIT-16 does not fire | MSG-S4-001 | AC3 |
| X4 | `template_status = withdrawn` for the product and notice type | Generation is held, a task is raised to the litigation officer and the state fact `NOTICE_BLOCKED` is announced; no pack is presented | None | AC2 |
| X5 | The case state is not `NOTICE_GENERATED` when the template is withdrawn | R-LIT-04 does not fire; nothing is written and no task is raised | None | AC2 |
| X6 | The case state is not `PACK_ASSEMBLY` when the pack completes | R-LIT-16 does not fire; nothing is presented and nothing is announced | None | AC3 |
| X7 | The local decision-record write fails | The transaction writes nothing: no pack is presented, no task is raised and no state fact leaves the service | MSG-P7-003 | AC4 |
| X8 | The case contract refuses the state fact | The refusal is recorded for the case owner and the caller reads the contract answer unchanged; this service does not move the case itself | None | AC2, AC3 |
| X9 | The task raise fails after the decision record is written | The record keeps the decision and the task raise is retried with the same `Idempotency-Key`; no second record is written | None | AC2 |
| X10 | A data product the pack reads is stale after a late or failed ACE batch | The staleness is shown with the product and its date and the pack is not certified as current | MSG-P1-001 | AC1 |
| X11 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | BR6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5004-CON`, the decision-record library and the composite route; the document index and the case contract are consumed and faked, and the missing dependency rows are recorded (GAP-2751) |
| Negotiable | The trigger, the pack item list, the template status and the state facts are versioned reference data or the case of record's; the story fixes the behaviour, not the values |
| Valuable | A complete pack is presented once, with the withdrawn template caught before generation, which is the module's 21-day to 6-day turnaround |
| Estimable | One composer, two readers, two rule evaluations, one library write, two clients and two read-only screen fragments |
| Small | Fits one sprint with its tests, as the app slice of the legacy key |
| Testable | Each of the four criteria is one test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S4-E5004-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Assemble the litigation pack, in rwb-litigation

  Background:
    Given the case "RC-2026-000604" is in the litigation route of rwb-litigation (S4)
    Given the rule package of the litigation route set is in force at its version, and LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Assemble the litigation pack (legacy RWB-E5-004 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-document contract mock returns the document index of "RC-2026-000604" with the pack items of FEAT-DCM-02
    Given the rwb-case contract mock returns the case facts of "RC-2026-000604"
    When its trigger arrives
    Then builds the pack from the document index and the case facts, ready for the officer to verify
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-04 (legacy RWB-E5-004 AC2)
    Given a case in state NOTICE_GENERATED
    Given the rwb-case contract mock returns the case state "NOTICE_GENERATED" for "RC-2026-000604"
    Given the rwb-case contract mock returns the task raised to the litigation officer and the case in state "NOTICE_BLOCKED"
    When template withdrawn
    Then hold generation and raise a task to the litigation officer
    Then the case moves to NOTICE_BLOCKED

  Scenario: AC3 Rule R-LIT-16 (legacy RWB-E5-004 AC3)
    Given a case in state PACK_ASSEMBLY
    Given the rwb-document contract mock returns the document index of "RC-2026-000604" with every pack item present
    Given the rwb-case contract mock returns the case in state "PACK_VERIFIED"
    When pack complete
    Then present the pack to the litigation officer for verification
    Then the case moves to PACK_VERIFIED

  Scenario: AC4 Not recorded (legacy RWB-E5-004 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

These four criteria are the legacy criteria of RWB-E5-004, copied word for word: not one legacy line is reworded, shortened or renumbered, and every value of the source (`NOTICE_GENERATED`, `NOTICE_BLOCKED`, `PACK_ASSEMBLY`, `PACK_VERIFIED`, MSG-P7-003) is kept character for character. The only additions are the origin tag on each `Scenario:` line and, inside AC1 to AC3, the `Given the <service> contract mock returns <x>` lines that stand in for the three consumed answers: the document index, the case facts and the case state facts of rwb-case. The two state facts are states of the case of record and are announced by this service; the status of a legal action is a different vocabulary and is not used for them (section 9). The end-to-end journey across the three services is not claimed here and belongs to the wave 3 harness.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| R-LIT-04 | Litigation · D7 · from `NOTICE_GENERATED` · event `TEMPLATE_WITHDRAWN` · condition `template_status = withdrawn` · action "hold generation and raise a task to the litigation officer" · to `NOTICE_BLOCKED` · owner Litigation officer · service level 1 working day | Business Rules and Routing Logic v4 (R-LIT-04); TSD S4 T4 |
| R-LIT-16 | Litigation · D7 · from `PACK_ASSEMBLY` · event `PACK_COMPLETE` · condition "every defect list item present" · action "present the pack to the litigation officer for verification" · to `PACK_VERIFIED` · owner Litigation officer · service level 2 working days | Business Rules and Routing Logic v4 (R-LIT-16); TSD S4 T4 |
| R-LIT-15 | Litigation · D7 · from `WITH_CUSTOMER_NOTICE_PERIOD` · event `NOTICE_PERIOD_EXPIRED` · condition "no cure and no dispute at `period_expires_at`" · action "open pack assembly" · to `PACK_ASSEMBLY` · service level 3 working days | Business Rules and Routing Logic v4 (R-LIT-15) |
| R-LIT-17 | Litigation · D7 · from `PACK_ASSEMBLY` · event `PACK_INCOMPLETE` · condition "one or more defect list items missing" · action "raise retrieval requests and hold the pack" · to `PACK_DEFECT_HOLD` · service level 5 working days | Business Rules and Routing Logic v4 (R-LIT-17) |
| R-LIT-21 | Litigation · D7 · from `PACK_VERIFIED` · event `OFFICER_REJECTED_PACK` · condition "the officer rejects the pack at verification" · action "return the pack to the legal document agent for rework" · to `PACK_ASSEMBLY` · service level 1 working day | Business Rules and Routing Logic v4 (R-LIT-21) |
| BR1 | The pack is derived, not stored: it is composed on every read from the document index of rwb-document and the case facts of rwb-case, and this service writes no pack row and no pack column | TSD S4 T3.1 (two objects only: `legal_action`, `hearing`); Ownership Map v1 (GAP-2753) |
| BR2 | The decision is written before anything is presented or announced: one record through the local decision-record library with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); R-UNI-39; legacy AC1 and AC4 |
| BR3 | The case states are announced, not written: `NOTICE_BLOCKED` and `PACK_VERIFIED` are states of the case of record, and this service announces the fact with the rule and its version and accepts the answer | R-LIT-04, R-LIT-16; TSD S4 T3.2; GAP-2754 |
| BR4 | The notice and its template status are read, never written: the notice is rwb-comms's and the template status is reference data read with its version | FSD S4 A2.4.3.1; TSD S4 T5.2 |
| BR5 | The same request twice, or the same `Idempotency-Key` twice, writes one record, presents one pack and sends one announcement; the repeat is counted | R-UNI-40; TSD S4 T-A.1 (API-S4-002, API-S4-004 header) |
| BR6 | No ACE read and no cross-schema read: this story reads no `v_ace_*` view, no ACE table and no other `rwb_*` schema, and its login holds no such grant | DP-01, DP-05 as a prohibition; Architecture v5 slide 8 notes |
| BR7 | No personal data: the pack, the decision record, the log and every call carry identifiers, document references, list values, dates and amounts only; no name, address, identity number or account number enters this service | TSD S4 T3.1; Architecture v5 slide 8 notes |
| BR8 | No business value is written in code: the pack item list, the template status, the proof and filing windows, the task code and the state names are versioned reference data or the case of record's | FSD S4 A2.4.3.1 (BR-S4-004); Template and Rules section R7.2 (s17) |

The defect list that R-LIT-16's condition names is `RWB-S4-E5005-APP`'s and is not defined by any source read for this key, so the check this story performs is "every checklist item of API-P5-008 has an index entry", read as a versioned reference row set and never as code (GAP-2757; ASM-4587).

### 9. State transitions

Two vocabularies are moved here and they are never used one for the other.

**Case states of the case of record** — announced by this service, written by rwb-case:

| From | Event | Condition | To |
|---|---|---|---|
| `NOTICE_GENERATED` | `TEMPLATE_WITHDRAWN` | `template_status = withdrawn` for the product and notice type | `NOTICE_BLOCKED`, with the task raised to the litigation officer |
| `WITH_CUSTOMER_NOTICE_PERIOD` | `NOTICE_PERIOD_EXPIRED` | no cure and no dispute at `period_expires_at` | `PACK_ASSEMBLY` (R-LIT-15, announced by the notice-period story) |
| `PACK_ASSEMBLY` | `PACK_COMPLETE` | every checklist item has an index entry and the decision record is written | `PACK_VERIFIED` |
| `PACK_ASSEMBLY` | `PACK_INCOMPLETE` | one or more checklist items have no index entry | `PACK_DEFECT_HOLD`, with the retrieval requests raised |
| `PACK_DEFECT_HOLD` | `DOCUMENT_RETRIEVED` | the missing item is supplied | `PACK_ASSEMBLY` |
| `PACK_VERIFIED` | `OFFICER_REJECTED_PACK` | the officer rejects the pack at verification | `PACK_ASSEMBLY`, returned to the legal document agent for rework |

**`legal_action.status`** — the values of LOV-LEGAL-STATUS (TSD S4 T3.2), moved by this service only where the officer opens or updates the action:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The action is opened on API-S4-002 | `actionType = CIVIL_CASE` and the request validates | `OPEN` |
| `OPEN` | The court references are recorded on API-S4-004 | `filedDate` is written | `FILED` |
| `FILED` | The judgment is recorded | `judgmentDate` and `judgmentAmount` are written | `JUDGMENT` |
| `OPEN` or `FILED` | The action is withdrawn | The closing step of the case of record | `WITHDRAWN` |

`NOTICE_BLOCKED`, `PACK_ASSEMBLY`, `PACK_VERIFIED` and `PACK_DEFECT_HOLD` appear nowhere in LOV-LEGAL-STATUS and are therefore never written to `legal_action.status`; the six status values above are the whole list and no seventh is added (GAP-2754; ASM-4584).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Litigation officer (RW-LITOFF) | Verifies the presented pack, rejects it at verification, and holds or releases the notice generation task |
| Legal counsel (RW-LEGAL) | Reads the pack and the legal action next to the officer |
| Head of Litigation (RW-HEADLIT) | Reads the pack of the cases in scope; the filing approval itself is `RWB-S4-E5007-APP`'s |
| Tech lead of rwb-litigation | Owns the composer, the two evaluations and the clients; tags the build |
| Solution architect | Approves a change to a consumed shape and the correction of an Ownership Map row |
| Business analyst of S4 | Confirms that the pack item list, the template status and the state names are reference data and not code |
| Data steward | Confirms that no personal data enters the pack view, the decision record or a log |
| Case owner (rwb-case, P3) | Owns the case, its states and its tasks; answers or refuses every announcement of this story |
| Document owner (rwb-document, P5) | Owns the index and the checklist this story reads |

The rights are the Litigation capability area of TSD S4 T6.1: C on API-S4-002, R on API-S4-003 and U on API-S4-004. This story defines no role code, no level and no mask; the role lists are rwb-access data.

### 11. Data

| Entity | Fields | BR Field IDs | Owner |
|---|---|---|---|
| recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 | P3 rwb-case, read on API-P3-002 |
| task | id, case_id, task_code, element_type, discretion, status and 4 more | DF-WRK-017 to DF-WRK-026 | P3 rwb-case, raised on its contract |
| legal_action | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | DF-LEG-001 to DF-LEG-014 | S4, written by this story |
| notice | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | DF-LEG-015 to DF-LEG-023 | P6 rwb-comms, read |
| document | id, case_id, person_key, document_type, source, storage_ref and 5 more | DF-DOC-001 to DF-DOC-011 | P5 rwb-document, read on API-P5-002 and API-P5-008 |
| decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 | P7 rwb-decision and the platform library, written through DP-03 |

The legacy Data block is copied as it stands, with the owner of each entity added from the Ownership Map. This story writes one entity of its own — `legal_action` — and one library row, `decision_record`, in its own schema. `recovery_case`, `task`, `notice`, `document`, `decision_log_entry` and `rule_row` are other owners' and are reached on their contracts only (DP-01, DP-05).

**No new table and no new column.** The pack is composed in memory from the two reads and has no row (BR1); the pack item list and the checklist are rwb-document's; the state facts are rwb-case's. The index set of `legal_action` beyond its primary key, and the source of the defect-list items, are `Not specified in the source documents (GAP-2757; ASM-4587)`.

**No personal data.** The pack is a list of document references, types and dates; the case facts that fill the cover sheet are the case number, the product group and the court references. The borrower and the guarantor are reached by the services that need them through rwb-source-data and never through this build.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | `LegalActionRequest`; `caseId` from the path | 201 with `LegalAction` in status `OPEN` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | None | 200 with `LegalAction` and the pack item references of the read | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | `LegalActionUpdate`; the court references and the filing date | 200 with `LegalAction` | Litigation U, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |

The purpose, entities, rights, idempotency and error statuses are those of TSD S4 T-A.1 and T-A.2 for the three operations, with the base renamed by DP-13 and the bodies fixed in `RWB-S4-E5004-CON`. API-S4-001 `POST /notices/{noticeId}/approve` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` are named by the legacy endpoint block and the TSD inventory of this service but are not declared here: the notice approval is the notice stories' and the hearing is `RWB-S4-E5011-APP`'s (GAP-2755; ASM-4585).

#### 12.2 REST operations consumed

| Operation | Owner | Used for | In the dependency rows |
|---|---|---|---|
| `GET /api/recovery/document/v1/cases/{caseId}/documents` (API-P5-002) | P5 rwb-document | The document index the pack is built from | No: no C row; consumed and faked (GAP-2751) |
| `GET /api/recovery/document/v1/cases/{caseId}/document-checklist` (API-P5-008) | P5 rwb-document | The checklist the pack is measured against | No: no C row; consumed and faked (GAP-2751) |
| `GET /api/recovery/case/v1/cases/{caseId}` (API-P3-002) | P3 rwb-case | The case facts of the pack and the state the rule fires from | No: no C row; consumed and faked (GAP-2751) |
| The case state announcement and its answer | P3 rwb-case | `NOTICE_BLOCKED` and `PACK_VERIFIED` | No: the operation name is Not specified in the source documents (GAP-2751; ASM-4581) |
| The task raise for the litigation officer | P3 rwb-case | The pack hold of R-LIT-04 | No: the operation name is Not specified in the source documents (GAP-2751; ASM-4581) |

Every call is one hop with a 2 s timeout and a breaker per downstream (DP-11, ADR-020). The reference lists are read as values in force with their version and carry no dependency row (GAP-2751).

#### 12.3 Events published

None. The service owns no event in the Ownership Map (Events: 0), DP-09 is not in this story's pattern set, and the pack assembly raises no business event. The catalogue names `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` on `rwb.litigation.events.v1`, and no source ties the assembly of a pack to any of them (GAP-2756; ASM-4586). The decision record reaches the shared `rwb.decision-record.v1` through the local library of DP-03, and that element is the library's, not this story's payload.

#### 12.4 Events consumed

None. The document index, the case facts, the state facts and the task are synchronous answers of their contracts, so this story declares no subscription and no inbox. `NoticeDelivered` and `PartnerResultSubmitted`, the two inputs the catalogue gives rwb-litigation, belong to the notice and firm-result stories.

#### 12.5 Workflows and activities

`LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery` carries the pack step: the assembly is an activity of the litigation workflow and not a workflow of its own.

| Item | Value |
|---|---|
| Workflow | `LitigationWorkflow` (S4) |
| Step | The pack assembly of the case, one step of the litigation route |
| Activities | `EvaluateRules` and `RecordAndApply`, the platform pattern of the service; the assembly activity name is `Not specified in the source documents (GAP-2756; ASM-4586)` |
| Queue | `rwb-litigation`, polled by this service's worker only |
| Timers | None: R-LIT-04's 1 working day and R-LIT-16's 2 working days are service levels of the case task, not timers of this step |

#### 12.6 Schedules

None. The service owns no job and no Temporal Schedule; the pack assembly is event-started from the case state and the template status, not scheduled from this service.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| legal_action | `rwb_litigation` | S4 | Written by this story: DF-LEG-001 to DF-LEG-014, the standard columns and no cross-schema key (DP-01, DP-15) |
| hearing | `rwb_litigation` | S4 | Owned by the service; not written by this story (`RWB-S4-E5011-APP`) |
| decision_record | `rwb_litigation` | PLT library object applied in this schema | Named only: the shape is `RWB-PLT-E1027-CON`'s and the row is written in the caller's transaction (DP-03) |
| idempotency_key | `rwb_litigation` | PLT library object applied in this schema | Named only: the stored answer of the two write operations |

`recovery_case` and `task` (P3), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are other owners' and appear only as consumed shapes.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Document-index fake | API-P5-002 and API-P5-008 | A complete checklist, a checklist with one item missing, an empty index, a 404 for an out-of-scope case and a delayed answer |
| Case-facts fake | API-P3-002 | A case in `NOTICE_GENERATED`, one in `PACK_ASSEMBLY`, one in `PACK_VERIFIED`, a 404 and a delayed answer |
| Case-state fake | The announcement of `NOTICE_BLOCKED` and `PACK_VERIFIED` | The fact accepted from the expected state, the refusal from another state, and a delayed answer |
| Task fake | The task raise of R-LIT-04 | The task created with its identifier, the refusal for a role without the right, and a delayed answer |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Reference-data fake | LOV-LEGAL-TYPE, LOV-LEGAL-STATUS, the template status and the pack item list | The values in force with their version, and a stale version |

The case-state and task fakes are stubbed from the P3 document and carry the placeholder until the two operation names are confirmed (GAP-2751).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed, 2 hand-overs | API-S4-002, API-S4-003 and API-S4-004 provided; API-P5-002 and API-P3-002 consumed; the case state and the task raise handed over |
| Kafka | None | No event published and none consumed; the decision record is the library's element (12.3) |
| Temporal | 1 workflow | `LitigationWorkflow` with the pack step and the two platform activities |
| File | None | The pack is composed from the index; no file is read or written by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation.pack`: the composer, the two readers, the two evaluations, the two clients, the read model of the two screens and the tests.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PackIndexReader` | Client | Reads the index and the checklist on API-P5-002 and API-P5-008; one hop, 2 s timeout, no copy of a document (BR1) |
| `CaseFactsReader` | Client | Reads the case facts and the state on API-P3-002 (BR3) |
| `PackComposer` | Service | Composes the pack in memory, matches every checklist item to an index entry and names what is missing (BR1, X3) |
| `TemplateWithdrawalCheck` | Service | Evaluates R-LIT-04 on the template status in force (BR4) |
| `PackDecisionWriter` | Service | Writes the decision record through the local library before any change, with the rule ID and version (BR2, DP-03) |
| `CaseStateClient` | Client | Announces `NOTICE_BLOCKED` and `PACK_VERIFIED` and accepts the answer (BR3) |
| `CaseTaskClient` | Client | Raises the pack-hold task to the litigation officer (BR3) |
| `LegalActionController` | REST | The three operations of 12.1, validation, the problem answers and the `Idempotency-Key` rule (BR5) |
| `PackWorkspaceModel` | Read model | The pack, the states and the case facts as SCR-18 and SCR-19 read them (DP-19) |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1` | None |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-18 and SCR-19 | H `RWB-PLT-N001-CON` |

DP-13 renames the base and adds nothing. DP-01 and DP-15 stand behind the `legal_action` table as the schema and migration rules and add no dependency row. DP-05 is applied as a prohibition: nothing of ACE is read. DP-06, DP-07, DP-08, DP-09, DP-10 and DP-11 are **not** in this story's pattern set although the story reads reference data, enforces a right and calls two services; each read is consumed and faked and none adds a row (GAP-2751; ASM-4581).

**Configuration and reference data.** The pack item list, the template status, the task code, the state names and the two service levels are versioned reference rows in force, read through the reference-data contract; none is written in code. The decision code is read from LOV-DECISION.

**Build steps**

1. Build the two readers against their fakes, with the timeout, the breaker and the 404 rule (AC1).
2. Build the composer and its missing-item naming; assert that an incomplete pack is never presented as complete (AC1, AC3).
3. Build the two evaluations with the rule package version in force and the decision record written before any change (AC1, AC2, AC4).
4. Build the two clients and assert one hop, the 2 s timeout and the retry with the same key (AC2, AC3).
5. Build the three operations on the published contract with the `Idempotency-Key` rule and the problem answers (AC1).
6. Build the read model of SCR-18 and SCR-19 through the route and the two state reading fragments (AC2, AC3).
7. Run the boundary test: no other `rwb_*` schema, no `v_ace_*` view, no ACE table (BR6).

**Feature flag.** `rwb.litigation.pack-assembly`.

**Done when.** The four criteria pass against the contract fakes, a withdrawn template blocks generation and raises the task, an incomplete pack is refused as complete, a failed decision write changes nothing, and the boundary test is green.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-S4-001 | A checklist item has no index entry (X3) | 409 on the write paths and the incomplete-pack state on the screen, with `messageId` MSG-S4-001 and the item named | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the filing window | Warning on SCR-19, with the date, blocking nothing | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field is missing, or a value is outside its list (X1) | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written (X7) | 503, problem body with `messageId` MSG-P7-003; nothing changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | A data product the pack reads is stale after a late or failed ACE batch (X10) | Warning with the product and its date | {product} is from {date}. Today's ACE batch has not arrived. |

The first five texts are the legacy message set of RWB-E5-004 and are copied unchanged; `MSG-P1-001` is the FSD S4 validation rule VR-S4-004-1 of the same feature. No message is reworded and no identifier is added. The 400, 401, 404 and 409 carry the platform problem document, and the 409's business text is `MSG-S4-001`; no other text is stated for it in any source read for this key (GAP-2757; ASM-4587).

### 15. Screens and states

Both screens are read through the gateway-bff composite route (DP-19); this story builds the pack fragment of each and nothing of their layout.

| Screen | States | What this story serves |
|---|---|---|
| SCR-18 Notice approval | Generated; approved; sent; delivered; unserved | The pack hold of R-LIT-04 in state `NOTICE_BLOCKED`, next to the notice state of rwb-comms |
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing; judgment | The composed pack in `PACK_ASSEMBLY`, the presented pack in `PACK_VERIFIED`, the missing items of `PACK_DEFECT_HOLD` and the rework return of R-LIT-21 |

The five states of SCR-18 and the five of SCR-19 are the ones the legacy screen block gives, copied unchanged. The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`; the state transitions behind each state are the app stories of this service and of rwb-case.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-004-01 | AC1 | Component | The document-index and case-facts fakes at their complete, incomplete and missing answers; a pack composed with every checklist item present |
| TC-E5-004-02 | AC2 | Component | R-LIT-04: `template_status = withdrawn`, the task raise and the `NOTICE_BLOCKED` announcement from `NOTICE_GENERATED` |
| TC-E5-004-03 | AC3 | Component | R-LIT-16: every checklist item present, the pack presented and the `PACK_VERIFIED` announcement from `PACK_ASSEMBLY` |
| TC-E5-004-04 | AC4 | Component | The stopped decision-record chain: nothing presented, no task, no announcement, 503 with MSG-P7-003 |
| TC-E5-004-05 | Access | Component | A role without the Litigation right refused at 403 with MSG-P4-002 on each of the three operations |
| TC-E5-004-06 | Principle 5 | Component | A forced decision-record write failure stops the presentation and the announcement; the outbox row is absent |

The six identifiers are the legacy identifiers of RWB-E5-004 in their legacy order. The pack assembly has no queue-level copy here: the cross-service journey across rwb-document, rwb-case and rwb-litigation is the wave 3 harness's and is not claimed by these cases. The contract half of each surface is tested in `RWB-S4-E5004-CON`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the pack item list, the template status, the state names, the task code, the two service levels and the decision code are reference data or the case of record's.
- No personal data in logs, events, workflow inputs or tests: identifiers, document references, list values, dates and amounts only.
- No cross-schema read and no ACE read: the only table this story writes is `legal_action` in `rwb_litigation`, and the pack is composed from the two contracts (DP-01, DP-05).
- One base and one login per service: no path of this story serves `/api/recovery/v1` and no component opens a second schema (DP-02, DP-13).
- The decision record is written before anything is presented or announced; a failed write leaves the case and the pack exactly as they were (DP-03, R-UNI-39).
- Every consumed answer comes from a published contract and is answered by its fake; no direct read of `document`, `recovery_case`, `task` or `notice` is introduced.
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the pack trigger, the case-state and task operation names, and the index set.
- Every test fixture is synthetic; no production document, payload or file is copied into a test, a log or a prompt.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-2752; ASM-4582) | The pack is built from the document index and the case facts, ready for the officer to verify | FEAT-LIT-04 | 08 Litigate and enforce | The three operations, the composer and the two announcements | TC-E5-004-01 to TC-E5-004-06 |
| FEAT-LIT-04 | Assemble the litigation pack | FEAT-LIT-04 | 08 Litigate and enforce | `PackComposer`, the decision record and the pack fragment of SCR-19 | TC-E5-004-01, TC-E5-004-03 |
| FEAT-DCM-02 | Index documents by case, type, date and extracted fields | FEAT-LIT-04 | 08 Litigate and enforce | The consumed read of API-P5-002 and API-P5-008 | TC-E5-004-01, TC-E5-004-03 |
| R-LIT-04 | A withdrawn template holds generation, raises a task and moves the case to `NOTICE_BLOCKED` | FEAT-LIT-04 | 08 Litigate and enforce | `TemplateWithdrawalCheck`, the task raise and the state announcement | TC-E5-004-02 |
| R-LIT-16 | A complete pack is presented for verification and the case moves to `PACK_VERIFIED` | FEAT-LIT-04 | 08 Litigate and enforce | `PackPresenter`, the decision record and the state announcement | TC-E5-004-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-004, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, copied word for word in section 7 |
| Legacy test cases | TC-E5-004-01 to TC-E5-004-06 |
| Requirement | The legacy master and the Epics 3 to 8 specification carry no REQ identifier for this feature, so the story traces to FEAT-LIT-04 until the Epics 3 to 8 PRD adds them (GAP-2752) |
| Screens | SCR-18 Notice approval and SCR-19 Litigation workspace, through the gateway-bff composite route (DP-19) |
| Sibling slice | RWB-S4-E5004-CON: the three operations, the schemas, the DDL template, the hand-over shapes and the fakes |
| Sibling stories of the service | `RWB-S4-E5005-APP` (defect list), `RWB-S4-E5006-APP` (lost document), `RWB-S4-E5007-APP` (verify and approve filing), `RWB-S4-E5011-APP` (hearings) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The contract baseline of the three operations, the schemas, the DDL template, the hand-over shapes and the fakes: `RWB-S4-E5004-CON`.
- The document index and the checklist, their retention and their custody: rwb-document (P5).
- The case, its stage, its states, its tasks and its timers: rwb-case (P3); this story announces and reads them.
- The demand notice, its dispatch, its delivery and its template: rwb-comms (P6) and the notice stories of this service.
- The check of the pack against the defect list: `RWB-S4-E5005-APP`.
- The recovery of a missing or lost document: `RWB-S4-E5006-APP`.
- The verification of the pack and the approval of the filing: `RWB-S4-E5007-APP`; the panel and the instruction: `RWB-S4-E5008-APP` and `RWB-S4-E5009-APP`.
- The court filing, the hearings, the judgment and the enforcement steps: their own stories of this service.
- The decision-record library and its chain: `RWB-PLT-E1027-CON`; the central ledger, the rule packages and their approval: rwb-decision (P7).
- The roles, rights, scope and masking data: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-18 and SCR-19: `RWB-PLT-N001-CON`.
- The deployment of this build, the chart values, the schema, the login and the flag: its own OPS story.
- The cross-service proof against the live owners: the wave 3 integration harness.
