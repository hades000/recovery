# RWB-S4-E5010-CON Record the court filing and receipt - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5010-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-010 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the filing step of rwb-litigation, split from RWB-E5-010. It fixes the two provided legal-action operations on base `/api/recovery/litigation/v1` (DP-13), the `LegalActionUpdate` element of the filing and the mapping of its `courtCaseNo` to `legal_action.black_case_no`, the four consumed facts (the case read and move of rwb-case, the pack and pack return of rwb-document, the firm receipt of rwb-partner, the LIT lawsuit of rwb-source-data), the rule package read of rwb-decision, the decision-record element of DP-03, the filing-clock element of `LitigationWorkflow`, the error set and the fakes. The update element names a court case number that the response and the row call `black_case_no` and carries no filing date and no defect field, and no source publishes the filing field list (GAP-2787; ASM-4624). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5010-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the filing step of rwb-litigation — the two legal-action operations and the filing element, the four consumed facts, the rule package read, the decision-record element, the filing clock, the error set and the fakes**, so that **the app story, the two workspaces and the wave 3 harness build against one fixed, testable contract on Day 1, and a court case number, a filing date, a pack return or a case move can never drift between rwb-litigation, rwb-case, rwb-document, rwb-partner and rwb-source-data without a failing build**.

The baseline is the contract half of RWB-E5-010 and nothing more:

- the two operations the legacy endpoint table names, kept with their IDs: `POST /cases/{caseId}/legal-actions` (API-S4-002, Litigation C) and `PATCH /legal-actions/{legalActionId}` (API-S4-004, Litigation U), on base `/api/recovery/litigation/v1`;
- the `LegalActionUpdate` element as the API specification publishes it — `status`, `courtCaseNo`, `judgmentDate`, `judgmentAmount` — with the filing reading of `status` `FILED`, `courtCaseNo` and the row's `filed_date`, and the judgment fields left to `RWB-S4-E5016-CON`;
- the four consumed facts, each on its owner's contract: the case route state and the two moves of rwb-case, the pack and the pack return of rwb-document, the firm's filing receipt of rwb-partner and the LIT lawsuit of rwb-source-data;
- the rule package read of rwb-decision with R-LIT-30 and R-LIT-31 at their version in force;
- the decision-record element of DP-03 and the filing clock as a durable timer of `LitigationWorkflow`;
- the error set of TSD S4 T-A.2, the rights of TSD S4 T6.1 and the closed vocabulary of LOV-LEGAL-STATUS;
- seven fakes and the drift test.

It declares no business outcome: the evaluation of the rules, the write of the row, the clock and the case move belong to RWB-S4-E5010-APP, and the four legacy criteria stay with that story word for word.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-010 crossed four boundaries in one process: a firm's portal upload, a pack, a case state with its timer, and a decision log row. The target splits them: the firm's receipt is rwb-partner (S9), the pack and its return are rwb-document (P5), the case of record and its route state are rwb-case (P3), the LIT lawsuit is rwb-source-data (P1), and the filing facts, the rule evaluation, the decision record and the filing clock are rwb-litigation (S4). Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that rwb-litigation holds no `v_ace_*` grant, so DP-05 is declared as a prohibition and the LIT lawsuit is consumed on the owner's contract only.

Three points are carried as gaps and assumptions instead of being decided quietly: the update element names `courtCaseNo` while the response and the row name `black_case_no`, and it carries neither a filing date nor a defect field (GAP-2787; ASM-4624); the operation names and elements of the four consumed facts and of the rule package are published by no source (GAP-2786; ASM-4619 to ASM-4622); and the filing service level of R-LIT-30 and the working-day calendar of R-LIT-31 have no value (GAP-2786; ASM-4620).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the idempotency rule are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `hearing` and `legal_action` are S4's; `recovery_case`, `timer` and `task` are P3's; `document` is P5's; `notice` is P6's; `rule_row` and `decision_log_entry` are P7's; the partner and its instruction are S9's. This document never declares another service's operation as provided.
- The published element of the update is read from the API specification (`LegalActionUpdate` with `status`, `courtCaseNo`, `judgmentDate`, `judgmentAmount`) and the row from TSD S4 T3.1 (DF-LEG-005, DF-LEG-006, DF-LEG-010, DF-LEG-014). Where the two disagree the baseline states the mapping and carries the gap (GAP-2787; ASM-4624).
- The four consumed owner contracts are named as documents and built against their fakes, each with the placeholder for its operation name (GAP-2786; ASM-4619 to ASM-4622).
- The LITIGATION rule package and its rows for R-LIT-30, R-LIT-31 and R-LIT-32 are governed in rwb-decision (P7); this baseline consumes them and declares none of them (GAP-2786; ASM-4621).
- The filing service level and the working-day calendar are versioned reference rows whose content no source gives (GAP-2786; ASM-4620).
- The `legal_action` table and its columns arrive with the DB work of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its two provided operations, its four consumed facts, its own decision record and filing clock, and its six error conditions.
2. Fix the filing element of `LegalActionUpdate` and the meaning of each of its four properties for this step; mark the mapping of `courtCaseNo` and the two missing fields.
3. Fix the case read and the two moves of rwb-case and mark the placeholder on each operation name.
4. Fix the pack read and the pack-return request of rwb-document, and record that custody stays with P5.
5. Fix the firm receipt element of rwb-partner and the LIT lawsuit element of rwb-source-data, and record that this service reads no `v_ace_*` view.
6. Fix the rule package read of rwb-decision and the decision-record element of DP-03, written before anything changes.
7. Fix the filing clock as a durable timer of `LitigationWorkflow` with its reference row and its two outcomes.
8. Publish the contract tables of section 12 and the seven fakes.
9. Add the contract tests: the element mapping, the placeholders, the error envelope and rights, the closed vocabulary, the decision-record and clock elements, the absence of a `v_ace_*` read and of a `recovery_case`, `timer`, `task` or `document` property, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S4-E5010-APP, the two workspaces and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a consumed fact or of an answer fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC7 |
| X2 | A field of a consumed fact is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2, AC3, AC4, AC5 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |
| X4 | A consumed fact has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC4, AC5, AC6 |
| X5 | A `status` value outside LOV-LEGAL-STATUS appears in the document or in an example | The vocabulary test fails the build | None | AC7 |
| X6 | The document declares a `v_ace_*` read, a `recovery_case`, `timer`, `task` or `document` property, or a third provided operation | The review fails the baseline; the absence test fails the build | None | AC8 |
| X7 | The same filing is replayed with the same court case number | The step answers with the stored answer and describes no second effect | None | AC1 |
| X8 | A required field of an answer is absent in an example | The example test fails the build | MSG-GEN-001 | AC1, AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the API specification and TSD S4 give, the example values and the fake fixtures are settled in the baseline review; the base, the operations, the rights and the vocabulary are fixed |
| Valuable | Unblocks RWB-S4-E5010-APP, SCR-19 and SCR-20 and the wave 3 harness on Day 1, and the rwb-case, rwb-document, rwb-partner and rwb-source-data teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, seven fakes and four contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the filing step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of legal_action and hearing is S4, of recovery_case, timer and task is P3, of document is P5 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two provided operations and the filing element are fixed (new, D-RCV-60)
    Given the provided operations and the element sections of the baseline
    When they are compared with TSD S4 T-A.1, T-A.2 and the API specification
    Then API-S4-002 POST /cases/{caseId}/legal-actions with Litigation right C and API-S4-004 PATCH /legal-actions/{legalActionId} with Litigation right U are declared on base /api/recovery/litigation/v1, and a third operation fails the review
    Then the filing is described inside LegalActionUpdate as status FILED with courtCaseNo, and the judgment properties of the same element are declared as another story's use and not as this step's
    Then courtCaseNo is declared as legal_action.black_case_no DF-LEG-006 and filed_date DF-LEG-010 is declared as the receipt date of the firm, and the mismatch and the absent date field are recorded (GAP-2787; ASM-4624)
    Then no idempotency key is declared for the patch, and a repeat of the same court case number returns the stored answer

  Scenario: AC2 The case read and the two moves of rwb-case are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case, timer and task
    Then the read is declared with the route state FIRM_INSTRUCTED or FILED_IN_COURT and with the prescription date the warning uses
    Then the move is declared with FILED_IN_COURT or FILING_REJECTED, the officer task, the rule ID and the package version
    Then the document declares no recovery_case property, no route-state column, no timer row and no task row of its own
    Then the operation names are Not specified in the source documents (GAP-2786; ASM-4622) and both rows carry the placeholder

  Scenario: AC3 The LIT lawsuit read is declared on rwb-source-data and the no-v_ace_ boundary is fixed (new, D-RCV-60)
    Given the lawsuit section of the baseline
    When it is compared with FEAT-LIT-10 as the Epics 3 to 8 specification states it, "matched to the LIT lawsuit read through v_ace_lawsuit"
    Then the lawsuit is declared as consumed from P1 rwb-source-data with the case reference, the lawsuit reference and the court case number
    Then the element of v_ace_lawsuit is Not specified in the source documents (GAP-2786; ASM-4619) and the row carries the placeholder
    Then the document declares no v_ace_* view, no ACE table and no grant of this service on ACE
    Then every call on the row is one hop with a 2 s budget and a breaker (DP-11, ADR-020)

  Scenario: AC4 The pack read and the pack return of rwb-document are declared and never written here (new, D-RCV-60)
    Given the pack section of the baseline
    When it is compared with the document row DF-DOC-001 to DF-DOC-011 and with rwb-document as its owner
    Then the pack and its defect list are declared as consumed from P5 rwb-document, and the return for rework as a request to P5 under R-LIT-31
    Then the operation names are Not specified in the source documents (GAP-2786; ASM-4622) and both rows carry the placeholder
    Then the document declares no document property as owned, no rebuild of the pack and no write of a receipt

  Scenario: AC5 The firm receipt element of rwb-partner is declared (new, D-RCV-60)
    Given the firm boundary of the baseline
    When it is compared with FSD S4 A2.10.2 (integration points "Partner portal, LIT") and with rwb-partner as the owner of the instruction and the portal
    Then the filing receipt and the court case number uploaded by the panel firm are declared as consumed from S9 rwb-partner through the partner gateway
    Then the operation name and the receipt element are Not specified in the source documents (GAP-2786; ASM-4622) and the row carries the placeholder
    Then the document declares no partner property, no instruction and no partner clock of its own

  Scenario: AC6 The decision-record element and the filing clock are declared (new, D-RCV-60)
    Given the decision and clock sections of the baseline
    When they are compared with the local decision-record library of DP-03 and with LitigationWorkflow
    Then one decision record is declared per rule outcome with the case reference, the action reference, the court case number, the rule ID, the package version in force, the inputs reference and the move
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything changes, and a failed write leaves the row unchanged with MSG-P7-003
    Then the filing clock of R-LIT-30 is declared as a durable timer of LitigationWorkflow on rwb-litigation fed by a versioned reference row, and the hearing timers of the same rule are declared as the hearing stage's and not this step's
    Then the service level and the working-day calendar are Not specified in the source documents (GAP-2786; ASM-4620)
    Then the document declares no timer row, no Temporal Schedule and no Quartz job

  Scenario: AC7 The error envelope, the rights and the closed vocabulary are fixed (new, D-RCV-60)
    Given the error, access and vocabulary sections of the baseline
    When they are compared with TSD S4 T-A.2, T6.1 and T3.2
    Then a malformed or invalid body answers 422 with MSG-GEN-001, a role without the right answers 403 with MSG-P4-002, an unknown or out-of-scope action answers 404, a status that refuses the step answers 409, an incomplete pack answers 422 with MSG-S4-001, a stale source answers with MSG-P1-001 and an owner that does not answer answers 503
    Then each condition carries one envelope and one message ID, and no new message text is authored
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, PT-LAWFIRM holds RU and SY-DATALOAD holds U, and every other role of TSD S4 T6.1 holds R
    Then status is closed over LOV-LEGAL-STATUS and FILING_REJECTED is declared as the case route state and not as a list value

  Scenario: AC8 The seven fakes and the naming baseline answer the document (new, D-RCV-60)
    Given the fakes and the naming sections of the baseline
    When each is compared with the element it serves and the nine sub-tables are reviewed
    Then the case fake answers FIRM_INSTRUCTED, FILED_IN_COURT, FILING_REJECTED, an accepted move and a refused move
    Then the document fake answers the pack as filed and as returned, the partner fake answers the receipt of the panel firm, the lawsuit fake answers the LIT lawsuit, and the rule package fake answers the LITIGATION package with R-LIT-30, R-LIT-31 and R-LIT-32
    Then the decision-record stub answers a healthy and a stopped chain and the composite route fake answers the merged SCR-19 and SCR-20 model
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the document declares no event published, no event consumed, no Schedule and no v_ace_* read, and the absence test fails a build that adds one
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5010-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The filing step of the litigation journey is rwb-litigation's, and the contract declares its two operations, its element, its decision record, its clock and the facts it consumes and nothing else | Context pack (workflow `LitigationWorkflow`, queue `rwb-litigation`, five provided operations); FSD S4 A2.10.3.1; TSD S4 T-A.1 |
| BR2 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-010 AC1 and AC4 |
| BR3 | The case, its route state, the two moves, the case clock and the officer task stay with rwb-case: the contract declares the answer and declares no `recovery_case`, `timer` or `task` property | Context pack; TSD S4 T5.2; GAP-2786 |
| BR4 | The pack, its defect list and the receipt document stay with rwb-document: the contract declares the pack as consumed and the return as a request | Context pack; FSD S4 A2.10.2; ASM-4622 |
| BR5 | The firm's receipt, the instruction and the partner clock stay with rwb-partner, reached through the partner gateway | Architecture v5 slide 8 notes; FSD S4 A2.10.2; ASM-4622 |
| BR6 | No ACE view and no ACE table is read: the LIT lawsuit is consumed on the owner's contract, and the service holds no `v_ace_*` grant | DP-05 as a prohibition; context pack; GAP-2786; ASM-4619 |
| BR7 | The status vocabulary is closed over LOV-LEGAL-STATUS, and `FILING_REJECTED` is a case route state and never a list value invented here | TSD S4 T3.2; Business Rules and Routing Logic v4 (R-LIT-31); GAP-2786; ASM-4624 |
| BR8 | No personal data in a fact, an answer, an example or a fake: identifiers, list values, amounts and dates only | Template and Rules v1 §R7.2 (s17); FSD S4 A2.10.3.2 |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | The rule rows of R-LIT-30 to R-LIT-32 and the filing service level are governed in rwb-decision and in reference data and are named here, never declared here | GAP-2786; ASM-4620; ASM-4621 |

### 9. State transitions

The lifecycle of this document, not of a filing:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the element mapping, the four consumed facts, the clock and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two workspaces, the wave 3 harness and the rwb-case, rwb-document, rwb-partner, rwb-source-data and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the base, an operation ID or a status value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC8 fails: a third operation, a `v_ace_*` read, a `recovery_case`, `timer`, `task` or `document` property, an event or a Schedule | In review |

The state machine of the filing itself is the app story's: `OPEN` to `FILED` under R-LIT-30 and back to `OPEN` under R-LIT-31 with the case route state `FILING_REJECTED`, and the case state is written by rwb-case on this baseline's answer shape.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, the two workspaces, the wave 3 harness and the owners of rwb-case, rwb-document, rwb-partner, rwb-source-data, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Filing element | `LegalActionUpdate` of the API specification: `status` of LOV-LEGAL-STATUS, `courtCaseNo`, and the judgment properties `judgmentDate` and `judgmentAmount`, which are the judgment story's use |
| Row mapping | `courtCaseNo` reads as `legal_action.black_case_no` DF-LEG-006 and `status` as DF-LEG-014; `lawsuit_no` DF-LEG-005 and `filed_date` DF-LEG-010 complete the filing. The mapping and the absent filing date are recorded (GAP-2787; ASM-4624) |
| Case answer | The route state, the move, the case-stage clock, the officer task, the rule ID and the package version, all P3's rows and columns (GAP-2786; ASM-4622) |
| Pack element | The document row DF-DOC-001 to DF-DOC-011 of `document` in `rwb_document`, read only, plus the pack-return request |
| Firm receipt element | The receipt and the court case number the panel firm uploads through the portal; the element is Not specified in the source documents (GAP-2786; ASM-4622) |
| Lawsuit element | The LIT lawsuit reference and the court case number of `v_ace_lawsuit` as FEAT-LIT-10 names it; the element is Not specified in the source documents (GAP-2786; ASM-4619) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Clock | The filing service level of R-LIT-30 as a durable timer of `LitigationWorkflow`; the value is Not specified in the source documents (GAP-2786; ASM-4620) |
| Rule rows | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force (GAP-2786; ASM-4621) |
| Not written here | `legal_action` and `hearing` (S4, the app stories'), `recovery_case`, `timer` and `task` (P3), `document` (P5), `notice` (P6), every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the mapping of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | Open a legal action and its pack, which the filing completes | Litigation C, scope applied | `Idempotency-Key` header required; the answer is stored |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | Record a filing, a judgment or an enforcement step | Litigation U, scope applied | None declared by the API specification; the status guard answers 409 and a repeat of the same court case number returns the stored answer |

The two operations, their IDs, rights and error sets are those of TSD S4 T-A.1 and T-A.2 and the API specification, and they are the two of the legacy endpoint table of RWB-E5-010; they differ only in the base, which DP-13 renames. Both are shared surfaces of this service: `RWB-S4-E5021-APP` opens the action of a bankruptcy petition, `RWB-S4-E5011-APP` patches the hearing outcome and `RWB-S4-E5016-APP` patches the judgment, so this baseline fixes the filing slice and declares the judgment properties of the element as another story's use. A third provided operation fails the review of AC1 and AC8.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in the baseline |
|---|---|---|
| The case read and the two moves, operation Not specified in the source documents (GAP-2786; ASM-4622), base `/api/recovery/case/v1` | P3 rwb-case | The route state `FIRM_INSTRUCTED` or `FILED_IN_COURT`, the prescription date, and the move to `FILED_IN_COURT` or `FILING_REJECTED` with the officer task; faked |
| The pack read and the pack-return request, operation Not specified in the source documents (GAP-2786; ASM-4622), base `/api/recovery/document/v1` | P5 rwb-document | The pack and its defect list, and the return for rework under R-LIT-31; faked |
| The firm receipt read, operation Not specified in the source documents (GAP-2786; ASM-4622), base `/api/recovery/partner/v1` | S9 rwb-partner | The filing receipt and the court case number uploaded by the panel firm through the partner gateway; faked |
| The LIT lawsuit read, operation and element Not specified in the source documents (GAP-2786; ASM-4619), base `/api/recovery/source-data/v1` | P1 rwb-source-data | The lawsuit that FEAT-LIT-10 names as `v_ace_lawsuit`, matched to the case; faked |
| The rule package read, operation Not specified in the source documents (GAP-2786; ASM-4621), base `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-30, R-LIT-31 and R-LIT-32; faked |
| The reference-data read of LOV-LEGAL-STATUS, `RWB-P3-E1043-CON`, base `/api/recovery/case/v1` | P3 rwb-case | The status values at their version in force; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All six rows are contract dependencies of class C in fact that the plan's C row does not carry, and the absence is recorded as GAP-2786 with ASM-4619 to ASM-4622.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), the ownership rows of this service publish zero events and TSD S4 T5.3 declares none. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service (GAP-2786; ASM-4621).

#### 12.4 Events consumed

None. `CASE_FILED` and `COURT_REJECTED_FILING` are event names of the state machine in R-LIT-30 and R-LIT-31, not Kafka subscriptions: the service publishes and consumes nothing, DP-09 is not in the pattern set of this key, and both facts arrive on the REST paths of 12.2. This baseline declares no consumer group, no subscription and no inbox of its own (GAP-2786; ASM-4621).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the filing; its signals and its outcome for the parent are declared, not built; it holds the filing clock |
| `recordFiling` | Activity, the filing step | `rwb-litigation` | The element and the receipt in; the rule ID with its package version, the court case number, the clock fact and the case move out |
| `rejectFiling` | Activity, the rejection step | `rwb-litigation` | The defect in; the rule ID with its version, the pack-return request and the `FILING_REJECTED` move out |
| `recordDecision` | Activity through the library | `rwb-litigation` | The decision record and its outbox row, written before the change (DP-03) |

The activity names and the state names of the step are target design choices and are fixed by no source; the trigger of the step is the firm's filing receipt on the rwb-partner contract, because the legacy story names a law firm user and the FSD declares no background event (GAP-2786; ASM-4622). No activity is registered by this story.

#### 12.6 Schedules

None. The filing clock is a durable timer of `LitigationWorkflow` fed by a versioned reference row. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 is owned or moved here (GAP-2786; ASM-4620).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | This service's action row; the filing element maps to `black_case_no`, `lawsuit_no`, `filed_date` and `status` |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the action create and the stored answer |

`hearing` is S4's and belongs to the hearing stories. `recovery_case`, `timer` and `task` (P3), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as an answer, a rule version or another story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case fake | Case `RC-2026-001010` at route state `FIRM_INSTRUCTED`, at `FILED_IN_COURT` and at `FILING_REJECTED` with its prescription date; an accepted move and a refused move | AC2, AC8 |
| rwb-document pack fake | The pack of `RC-2026-001010` as filed and as returned for rework, with its defect list | AC4, AC8 |
| rwb-partner receipt fake | The filing receipt of `LA-2026-001010` uploaded by the panel firm with its court case number | AC5, AC8 |
| rwb-source-data lawsuit fake | The LIT lawsuit of `RC-2026-001010` with its court case number, and a case with no lawsuit | AC3, AC8 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-30, R-LIT-31 and R-LIT-32, and a second version | AC6, AC8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC8 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 model for `RC-2026-001010` | AC8 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the six consumed rows, the LIT lawsuit element and the filing service level are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2786, GAP-2787).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | API-S4-002 and API-S4-004 provided; the case read and move, the pack read and return, the firm receipt, the LIT lawsuit, the rule package and the reference data consumed; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 3 activities declared, 0 registered, 1 durable clock | `LitigationWorkflow`, `recordFiling`, `rejectFiling`, `recordDecision` and the filing clock; no Schedule |
| File | None | The receipt document is rwb-document's and the portal upload rwb-partner's; no file is declared here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no action, no case and no pack. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and seven fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-filing.v1.yaml` for the provided and consumed elements, the filing element of `LegalActionUpdate` with its mapping, the clock element of `LitigationWorkflow`, the contract README rows for the consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1`; the two operations keep API-S4-002 and API-S4-004 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 fixes the record element that legacy AC1 and AC4 turn on. DP-13 fixes the base of the service and keeps the two operation IDs. DP-19 is behind SCR-19 and SCR-20, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is why no event is declared in 12.3 or 12.4. DP-05 is declared as a prohibition: the document declares no `v_ace_*` read and no ACE grant, because rwb-litigation holds neither (GAP-2786; ASM-4619).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan already carries for the app story. The six consumed contracts are C dependencies in fact and not in the metadata row, which is None (GAP-2786; ASM-4619 to ASM-4622).

**Build steps**

1. Write the two provided operations of AC1 and the mapping of `courtCaseNo`, and add the test for a third operation.
2. Write the case read and the two moves of AC2 with their placeholders and the absence test for a `recovery_case`, `timer` or `task` property.
3. Write the lawsuit row of AC3 with its placeholder and the boundary test against a `v_ace_*` read.
4. Write the pack and pack-return rows of AC4 and the absence test for a document write.
5. Write the firm receipt row of AC5 with its placeholder.
6. Write the decision-record and clock elements of AC6 and validate them against the library schema and the workflow contract.
7. Write the error envelope, the rights and the vocabulary of AC7.
8. Publish the seven fakes and the drift test of AC8, record the naming baseline, then tag the baseline and collect the consumer sign-off.

**Done when.** The contract tests pass, the six consumed rows carry their placeholders and the element mapping is agreed with the API owner, the seven fakes answer every consumed path and the drift test is green, the absence test blocks a third operation, a `v_ace_*` read, a case or document property and a Schedule, and the app story, the two workspaces and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | The pack is not acknowledged as filed or the defect list names a missing item; the app story raises it on the rejection, and the contract carries it as the 422 of the filing element | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the warning window; the contract carries it as the warning answer of the case read | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the element, a fact or an answer is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation C or U right the row declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed batch, which is VR-S4-010-1 of the FSD; the check is the owner's and this service holds no batch status read | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S4-001 and MSG-S4-002 are carried because they are in the message set of this key, and the contract fixes the status and the envelope each one answers with.

### 15. Screens and states

The contract serves SCR-19 Litigation workspace in its instructed, filed, hearing and judgment states and SCR-20 Enforcement workspace in its requested, seized, auctioned and closed states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the filing element, rwb-case for the case and its route state, rwb-document for the pack and rwb-partner for the firm's receipt; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to `RWB-PLT-N001-CON`. The refusal, not-recorded, rejected and stale states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-010-01 | AC1, AC6 | Contract | Action `LA-2026-001010` with a court case number; the contract half answers the element mapping, the decision-record element and the clock |
| TC-E5-010-02 | AC2, AC7 | Contract | Case `RC-2026-001010` at `FILED_IN_COURT` with a rejected filing; the contract half answers the case answer and the 409 and 422 envelopes |
| TC-E5-010-03 | AC1, AC2, AC7 | Contract | Case `RC-2026-001010` at `FIRM_INSTRUCTED` with its receipt; the contract half answers the case read, the move to `FILED_IN_COURT` and the rights |
| TC-E5-010-04 | AC6, AC7 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the status vocabulary |
| TC-E5-010-05 | AC7, AC8 | Contract | RW-LITOFF holds CRUA, RW-ENFORCE holds CRU, PT-LAWFIRM holds RU and SY-DATALOAD holds U; the contract half answers the rights and the absence of a third operation |
| TC-E5-010-06 | AC6, AC8 | Contract | A forced decision-record failure and a drifted fake; the contract half answers the fail-closed path, the fakes and the drift test |
| TC-S4-E5010-CON-01 | AC1, AC7 | Contract | The element mapping, the two operations, the rights and the vocabulary validate; no third operation and no `v_ace_*` read is declared |
| TC-S4-E5010-CON-02 | AC2, AC3, AC4 | Contract | The case answer, the lawsuit element and the pack rows validate with their placeholders and one hop with a 2 s budget |
| TC-S4-E5010-CON-03 | AC5, AC6 | Contract | The firm receipt element, the decision-record element and the filing clock validate; no `timer` row and no Schedule is declared |
| TC-S4-E5010-CON-04 | AC8 | Contract | The seven fakes match the document and a drifted fake fails the build; the absence test for a third operation, a `v_ace_*` read, a case or document property and a Schedule |

The six legacy cases are the legacy cases of RWB-E5-010 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5010-APP. The legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5010-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the status values, the filing service level, the working-day calendar, the message texts and the defect codes stay reference rows and rule rows, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: identifiers, list values, amounts and dates only; every example is synthetic.
- The case stays with rwb-case and the pack with rwb-document: the document declares no `recovery_case`, `timer`, `task` or `document` property and no write of a move or a pack (BR3, BR4).
- The firm and its portal stay with rwb-partner: the receipt is consumed and the instruction is never declared here (BR5).
- ACE data only through the owner's contract: the document declares no `v_ace_*` view and no grant on ACE, and the boundary test fails a build that adds one (BR6).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR9).
- No provided operation beyond the two of the legacy endpoint table; a third operation fails the review and the absence test.
- No retired element is reintroduced: the absence test of AC8 fails a build that declares an event, a Schedule, a Quartz row or a shared job table.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| No REQ-S4 identifier is given for this key by any source read: TSD S4 T8 maps REQ-S4-001 to REQ-S4-010 to FEAT-LIT-01, the Epics 3 to 8 specification carries feature IDs only and the legacy master carries none (GAP-2786; ASM-4623) | The filing confirmation and the court case number are taken onto the case, matched to the LIT lawsuit (FSD S4 A2.10, FEAT-LIT-10) | The two operations, the filing element, the lawsuit element and the decision record | TC-E5-010-01, TC-S4-E5010-CON-01, TC-S4-E5010-CON-02 |
| FEAT-LIT-10 | Record the court filing and receipt | The whole baseline | TC-E5-010-01, TC-E5-010-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S4-E5010-CON-02, TC-S4-E5010-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element of AC6 | TC-E5-010-04, TC-E5-010-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-010, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5010-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5010-CON-01 to -04 |
| Feature and screens | FEAT-LIT-10, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-30, R-LIT-31 and R-LIT-32, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2786; ASM-4621) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal with durable timers), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the step, the evaluation of R-LIT-30 and R-LIT-31, the decision record, the clock and the case move: RWB-S4-E5010-APP.
- The case of record, its route states, the parent `CaseWorkflow`, the case-stage clock and the officer task: rwb-case (P3) and its slice of this legacy key (GAP-2786; ASM-4622).
- The pack, its defect list and the receipt document: rwb-document (P5); the return for rework is a request (BR4).
- The firm, the instruction, the portal and the partner clock: rwb-partner (S9) and `RWB-S4-E5009-CON`.
- The LIT lawsuit and the ACE ingestion, and the `v_ace_lawsuit` element: rwb-integration (P2) and rwb-source-data (P1).
- The authoring, testing, approval and versioning of the LITIGATION package and of the rows of R-LIT-30 to R-LIT-32: rwb-decision (P7) (GAP-2786; ASM-4621).
- The judgment properties of the same element and the judgment step: `RWB-S4-E5016-CON` and `RWB-S4-E5016-APP`.
- The filing service level and the working-day calendar as business values: the business owner of S4 and the reference-data owner of rwb-case (GAP-2786; ASM-4620).
- The rights, roles, scope and masking data themselves, and the composite route and screen field list of SCR-19 and SCR-20: rwb-access and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
