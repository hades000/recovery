# RWB-S4-E5012-CON Recommend the next litigation step - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5012-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-012 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the next-step step of rwb-litigation, split from RWB-E5-012. It fixes the recommendation element with its reasons and its cost and effect, the vocabulary of the proposed step as a versioned reference value, the seven consumed facts (the case and the case-stage answer on rwb-case, the notice, its template status and the generation hold on rwb-comms, the pack index on rwb-document, the LITIGATION package on rwb-decision, the cost and effect on rwb-agent), the decision-record element of DP-03, the three rule clocks of `LitigationWorkflow` and the fakes. It declares no provided operation, because the ownership rows give this service five operations and none of them proposes a step (GAP-2793; ASM-4631); the signals are not Kafka subscriptions (GAP-2794; ASM-4632); the template status, the pack element and the step vocabulary have no source specification (GAP-2795; ASM-4633). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5012-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the next-step step of rwb-litigation — the recommendation element with its reasons, its cost and its effect, the step vocabulary as a versioned reference value, the shape of the case read and the case-stage answer of rwb-case, the notice and template status of rwb-comms and its generation hold, the pack index of rwb-document, the rule package of rwb-decision and the cost-and-effect read of rwb-agent with the rule fallback, the decision-record element, the three rule clocks, the error set and the fakes**, so that **the app story, the screens and the wave 3 harness build against one fixed, testable contract on Day 1 and a proposal, a reason, a cost, a move or a clock can never drift between rwb-litigation, rwb-case, rwb-comms, rwb-document, rwb-decision and rwb-agent without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy step of RWB-E5-012 crossed five boundaries in one process: a case state with its task, a notice with its template, a pack of documents, a rule row and a decision log row. The target splits them: the case of record, its route state, the case-stage timer and the officer task are rwb-case (P3), the notice and its template are rwb-comms (P6), the pack is rwb-document (P5), the rule package is rwb-decision (P7), the cost and the effect of a proposed step are rwb-agent (P10), and the evaluation, the proposal and the decision record are rwb-litigation (S4). Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_litigation`, base `/api/recovery/litigation/v1`, topic `rwb.litigation.events.v1` with retry and `.dlt` topics, task queue `rwb-litigation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.litigation`. It records that the proposal is not a business row — no owned table of this service carries it — so the element is fixed as a decision-record view and not as a column.

Three points are carried as gaps and assumptions rather than decided quietly: the recommendation has no table, no operation and no vocabulary in any source (GAP-2793), the template status of R-LIT-04 and the pack index of R-LIT-16 have no owner field and no published operation (GAP-2795), and the rule package that decides the three rules has no dependency row because DP-04 is not in the pattern set (GAP-2797).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the idempotency rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `hearing` and `legal_action` are S4's, `notice` is P6's, `recovery_case` and `task` are P3's, `document` is P5's, `rule_row` and `decision_log_entry` are P7's. This document never declares another service's operation as provided.
- The four consumed owner contracts are named as documents and built against their fakes: the case read and answer on rwb-case, the notice and its template on rwb-comms, the pack index on rwb-document and the rule package on rwb-decision. No source read for this key names their operations, so all four carry the placeholder (GAP-2794, GAP-2795, GAP-2797; ASM-4632, ASM-4633, ASM-4568).
- The cost-and-effect read of rwb-agent is declared under DP-20 with its fake and its no-answer path, and the rule's own proposal stands when the agent answers nothing (GAP-2793; ASM-4631).
- The LITIGATION rule package, its rows for R-LIT-04, R-LIT-16 and R-LIT-36 and its D7 route set are governed in rwb-decision (P7); this baseline consumes them and declares none of them.
- The `legal_action` and `hearing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract description of the step: its seven consumed facts, its own decision record, its three rule clocks and its nine error conditions.
2. Fix the recommendation element: the proposed step, the reasons, the cost and effect with its source, the deciding role and the rule ID with its package version. Fix the step vocabulary as a versioned reference value.
3. Fix the case read and the case-stage answer of rwb-case: the route states that gate the rules, the move, the case-stage timer, the officer task and the rule version.
4. Fix the notice and template read of rwb-comms and the generation hold of R-LIT-04, and mark the template-status element with the placeholder.
5. Fix the pack-index read of rwb-document: the documents of the case and the defect list items of R-LIT-16, with the placeholder on the element.
6. Fix the rule package read of rwb-decision and the cost-and-effect read of rwb-agent, with the fallback rule of R-LIT-36 written into the document.
7. Fix the decision-record element of DP-03, written before anything changes, and the three rule clocks of `LitigationWorkflow`.
8. Publish the contract tables of section 12 and the seven contract fakes.
9. Add the contract tests: element shapes, vocabulary, placeholders, error envelope, the absence of a provided operation beyond the five owned ones, the absence of a cross-schema write, the absence of an event and of a Schedule, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S4-E5012-APP, the screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body of a consumed fact or of the answer fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC7, AC9 |
| X2 | A field of a consumed fact is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC2, AC3, AC4 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC8 |
| X4 | A consumed fact has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4, AC5 |
| X5 | The document declares another service's operation as provided, a cross-schema write or a property of `recovery_case`, `notice`, `document` or `rule_row` | The review fails the baseline; the absence test fails the build | None | AC9 |
| X6 | The agent answer is absent, below the threshold or malformed | The document declares the fallback: the rule's proposal stands and the record states the source of the cost and effect | None | AC5, AC8 |
| X7 | The same signal is replayed for the same case, state and payload | The step answers with the stored answer and describes no second effect | None | AC1, AC6 |
| X8 | A required field of the answer is absent in an example | The example test fails the build | MSG-GEN-001 | AC1, AC7 |
| X9 | The step vocabulary of the proposal changes | The reference version changes; the contract test on the version fails the build | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the Ownership Map and the published owner documents only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the vocabulary, the base, the topic, the queue and the clocks are fixed |
| Valuable | Unblocks RWB-S4-E5012-APP, SCR-18 and SCR-19 and the wave 3 harness on Day 1, and the rwb-case, rwb-comms, rwb-document, rwb-decision and rwb-agent teams on the same day |
| Estimable | One contract document with its AsyncAPI absence note, nine contract tables, seven fakes and five contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the next-step step of rwb-litigation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of hearing and legal_action is S4, of notice is P6, of recovery_case and task is P3, of document is P5 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The recommendation element, its reasons and its cost and effect are fixed as data (new, D-RCV-60)
    Given the recommendation section of the baseline
    When it is compared with FSD S4 A2.12, with R-LIT-04, R-LIT-16 and R-LIT-36 and with the answer of API-S4-003
    Then the element is declared with the proposed step, the reasons (the rule ID, its condition and the facts that satisfied it), the cost and effect with its source, the deciding role and the package version in force
    Then the vocabulary of the proposed step is declared as a versioned reference value and is Not specified in the source documents (GAP-2793; ASM-4631), and no step name is written in the schema or in the code
    Then the deciding role is declared as the litigation officer under R-LIT-04 and R-LIT-16 and the approver at D7.4 under R-LIT-36
    Then the element is declared as a view of the decision record answered on API-S4-003 `GET /legal-actions/{legalActionId}` and no column of `legal_action` or `hearing` is added

  Scenario: AC2 The case read and the case-stage answer of rwb-case are declared (new, D-RCV-60)
    Given the case boundary of the baseline
    When it is compared with rwb-case as the owner of recovery_case and task
    Then the read is declared with the case, its route state (NOTICE_GENERATED, PACK_ASSEMBLY, IN_HEARING and the other LIT states), its stage and its legal action
    Then the answer is declared with the move NOTICE_BLOCKED or PACK_VERIFIED, the case-stage timer, the officer task, the rule ID and the package version
    Then the document declares no recovery_case property, no route-state column, no timer row and no task row of its own
    Then the operation names are Not specified in the source documents (GAP-2794; ASM-4632) and both rows carry the placeholder

  Scenario: AC3 The notice, its template status and the generation hold of rwb-comms are declared (new, D-RCV-60)
    Given the notice section of the baseline
    When it is compared with the notice row DF-LEG-015 to DF-LEG-023 and with rwb-comms as its owner
    Then the notice is declared as consumed with id, case_id, document_id, notice_type, sent_date, barcode and the template status R-LIT-04 needs
    Then the hold of generation is declared as a request that names the case, the rule and its version, and the document declares no write of a notice, a template, a status or a barcode from rwb-litigation
    Then the template-status field identifier is Not specified in the source documents (GAP-2795; ASM-4633) and the row carries the placeholder
    Then the three notice fields the legacy table leaves unnamed are not invented and the row names only the six it gives

  Scenario: AC4 The pack-index read of rwb-document is declared (new, D-RCV-60)
    Given the pack section of the baseline
    When it is compared with TSD S4 T5.2 and with the defect list item of R-LIT-16
    Then the pack index is declared as consumed from P5 rwb-document with the documents of the case and the defect list items it holds
    Then the document declares no document, blob, custody or retention property and no read of a document body
    Then the operation name and the element are Not specified in the source documents (GAP-2793; ASM-4631) and the row carries the placeholder
    Then every call on the row is one hop with a 2 s budget and a breaker (DP-11, ADR-020)

  Scenario: AC5 The rule package and the cost-and-effect read are declared with the rule fallback (new, D-RCV-60)
    Given the rule and agent sections of the baseline
    When they are compared with the LITIGATION package of rwb-decision, with R-LIT-36 and with DP-20
    Then the package is declared as consumed from P7 rwb-decision at its version in force with R-LIT-04, R-LIT-16 and R-LIT-36
    Then the cost and effect are declared as consumed from P10 rwb-agent, with the step, the cost, the effect and the confidence of the answer
    Then when the agent answers nothing or fails the threshold, the document declares that the rule's own proposal stands and the source of the cost and effect is recorded as the rule
    Then neither row declares a rule, a package, a model or a prompt of this service's own, and both carry the placeholder on their operation names (GAP-2797, GAP-2793; ASM-4568, ASM-4631)

  Scenario: AC6 The decision-record element and the three rule clocks are declared (new, D-RCV-60)
    Given the decision and clock sections of the baseline
    When they are compared with the local decision-record library of DP-03 and with LitigationWorkflow
    Then one decision record is declared per proposal with the case and legal-action references, the rule ID, the package version in force, the inputs reference, the proposal, the cost and effect with its source and the case move
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything changes, and a failed write leaves the case, the notice and the task unchanged with MSG-P7-003
    Then the clocks are declared as durable timers of LitigationWorkflow of 1 working day under R-LIT-04, 2 working days under R-LIT-16 and 3 working days under R-LIT-36, answered to rwb-case as the case-stage timer
    Then the document declares no timer row, no Temporal Schedule and no Quartz job and no event of its own for the record

  Scenario: AC7 The error envelope, the messages and the rights are fixed (new, D-RCV-60)
    Given the error, message and access sections of the baseline
    When they are compared with TSD S4 T-A.2, TSD S4 T6.1 and the legacy message set of RWB-E5-012
    Then a malformed or invalid body answers 400 with MSG-GEN-001, a role without the Litigation right answers 403 with MSG-P4-002, an unknown case, notice or pack answers 404, a case in a state no rule names answers 409, a field the answer needs answers 422, and an owner that does not answer answers 503
    Then the six messages of the legacy set are carried unchanged, including MSG-S4-001, MSG-S4-002 and MSG-P1-001, and no new message text is authored
    Then the reads declare Litigation right R, the case-stage answer and the notice hold declare the right the owner documents give them, and the decision of the proposal declares right A with scope applied
    Then RW-LITOFF holds Litigation CRUA, RW-ENFORCE holds CRU, RW-LEGAL and RW-PRODHEAD and RW-HEADLIT hold RA, PT-LAWFIRM holds RU and every other role of TSD S4 T6.1 holds R

  Scenario: AC8 The seven contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the case fake answers NOTICE_GENERATED, PACK_ASSEMBLY, another state, an accepted move to NOTICE_BLOCKED and to PACK_VERIFIED and a refused move
    Then the comms fake answers the notice of the case with a withdrawn and with a current template, a hold accepted and an unknown notice
    Then the document fake answers the pack index with every defect list item present, with one missing and no answer beyond 2 s
    Then the decision fake answers the LITIGATION package with the three rules and a second version, and the agent fake answers a cost and effect, a low-confidence answer and no answer
    Then the decision-record stub answers a healthy chain and a stopped chain, the composite route fake answers the merged SCR-18 and SCR-19 model, and the drift test fails the build on any difference

  Scenario: AC9 The naming baseline, the absence of a provided operation and the no-cross-schema boundary are fixed (new, D-RCV-60)
    Given the naming, data and boundary sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_litigation, the login is rwb_litigation, the topic is rwb.litigation.events.v1, the queue is rwb-litigation and the Java package is th.co.scb.ace.workbench.recovery.litigation
    Then the document declares zero provided operations and names the five operations of the service as the sibling stories' (API-S4-001 to API-S4-005), and a sixth operation fails the review
    Then the tables named as this service's are legal_action and hearing, which the step writes none of, and recovery_case, task, notice, document, rule_row and decision_log_entry are named as other owners' and consumed only through their contracts
    Then the document declares no grant on another rwb_* schema, no event published, no event consumed and no Schedule, and the absence test fails a build that adds one
```

These nine criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S4-E5012-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The next-step step of the litigation journey is rwb-litigation's, and the contract declares its proposal element, its reasons, its cost and effect, its record, its clocks and the facts it consumes and nothing else | Context pack (workflow `LitigationWorkflow`, queue `rwb-litigation`); Architecture v5 slide 41; FSD S4 A2.12.3.1 |
| BR2 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S4 T2; legacy RWB-E5-012 AC1 and AC4 |
| BR3 | The case, its route state, the case-stage timer and the officer task stay with rwb-case: the contract declares the read and the answer and declares no `recovery_case` or `task` property | Context pack; TSD S4 T5.2; GAP-2794 |
| BR4 | The notice, its template and its template status stay with rwb-comms: the contract declares them consumed and the hold as a request, and describes no notice write | Context pack (ownership rows of S4); Architecture v5 slide 10; GAP-2795 |
| BR5 | The pack and its documents stay with rwb-document: the contract declares the index read and no document body, custody or retention property | TSD S4 T5.2; FSD S4 A2.12 |
| BR6 | The proposal is never a schema constant: the step vocabulary, the three clocks and the agent threshold are reference values with a version | FSD S4 A2.12.3.1 (BR-S4-012); Template and Rules v1 §R7.2 (s17) |
| BR7 | The agent supplies the cost and the effect and never the proposal: when it answers nothing the rule's proposal stands and the record says so | Business Rules and Routing Logic v4 R-LIT-36; Architecture v5 slide 5; GAP-2793 |
| BR8 | No personal data in a fact, an answer, an example or a fake: identifiers, dates, list values, step names and a rule version only | Template and Rules v1 §R7.2 (s17); FSD S4 A2.12 field catalogue |
| BR9 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A change is additive within major version 1; a breaking change is a new major version, and a change of the step vocabulary is a new reference version and a contract test | Architecture v5 slide 42 notes (BACKWARD compatibility); AC9 |
| BR11 | The document lists only operations owned by rwb-litigation, and this step owns none beyond the five of TSD S4 T-A.1 | Ownership rows of S4; TSD S4 T-A.1; GAP-2793 |
| BR12 | The rule rows of R-LIT-04, R-LIT-16 and R-LIT-36, the D7 route set and the package version are governed in rwb-decision and named here, never declared here | GAP-2797; ASM-4568 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The seven consumed facts, the proposal element, the record and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the rwb-case, rwb-comms, rwb-document, rwb-decision and rwb-agent owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new error code | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a move, a clock or the deciding role changes | New major version drafted |
| Baselined | Vocabulary change | The step vocabulary changes at a new reference version and the contract test fails | In review |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC9 fails: a provided operation beyond the five, a cross-schema write, an event or a Schedule | In review |

The state machine of the case is the app story's: `NOTICE_GENERATED` to `NOTICE_BLOCKED` under R-LIT-04, `PACK_ASSEMBLY` to `PACK_VERIFIED` under R-LIT-16 and `IN_HEARING` to `SETTLEMENT_OFFERED_AT_COURT` under R-LIT-36, and the state is written by rwb-case on this baseline's answer shape.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-litigation | Owns the contract document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, a new reference version of the vocabulary, and the correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, the screens, the wave 3 harness and the owners of rwb-case, rwb-comms, rwb-document, rwb-decision, rwb-agent and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the idempotency rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in a fact, an answer, an example or a fake |

The per-service login behind the security scheme is named "the rwb-litigation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Proposal element | The proposed step, the reasons (rule ID, condition, facts), the cost and effect with its source, the deciding role and the package version; not a column of `legal_action` or `hearing` (GAP-2793; ASM-4631) |
| Step vocabulary | Versioned reference values; the content is Not specified in the source documents (GAP-2793; ASM-4631) |
| Case answer | The route state, the move, the case-stage timer start and expiry, the officer task, the rule ID and the package version, all P3's rows and columns |
| Notice element | The notice row DF-LEG-015 to DF-LEG-023 of `notice` in `rwb_comms`, read only, with the template status whose field identifier is Not specified in the source documents (GAP-2795; ASM-4633) |
| Pack element | The document index of the case and its defect list items, P5's objects, read only; the element has no published identifier (GAP-2793; ASM-4631) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Clocks | The durable timers of `LitigationWorkflow`: 1 working day under R-LIT-04, 2 working days under R-LIT-16, 3 working days under R-LIT-36; the `timer` row DF-WRK-027 to DF-WRK-036 is P3's and is not declared here |
| Rule rows | DF-REF-001 to DF-REF-015 of `rule_row` in `rwb_decision`, read as the package in force (GAP-2797) |
| Not written here | `legal_action` and `hearing` (S4, the sibling stories'), `recovery_case` and `task` (P3), `notice` (P6), `document` (P5), every `v_ace_*` view (P1) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC1 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. The ownership rows give rwb-litigation five operations (API-S4-001 to API-S4-005, TSD S4 T-A.1) and none of them proposes a step: API-S4-001 `POST /notices/{noticeId}/approve` is the dispatch approval, and API-S4-002 to API-S4-005 are the legal-action operations of the sibling stories. The proposal is answered as an element of API-S4-003 `GET /legal-actions/{legalActionId}`, whose shape the legal-action story fixes, so this baseline declares no provided operation and fixes only what the step consumes, what it holds and what it answers; a sixth operation fails the review of AC9 (BR11; GAP-2793; ASM-4631).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2794; ASM-4632)) | `/api/recovery/case/v1` | P3 rwb-case | The case, its route state, its stage and its legal action; faked |
| The case-stage answer (operation name Not specified in the source documents (GAP-2794; ASM-4632)) | rwb-case (P3) | P3 rwb-case | The move, the case-stage timer, the officer task and the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The notice and template read (operation name Not specified in the source documents (GAP-2795; ASM-4633)) | `/api/recovery/comms/v1` | P6 rwb-comms | The notice of the case and its template status for R-LIT-04; faked |
| The notice hold (operation name Not specified in the source documents (GAP-2795; ASM-4633)) | `/api/recovery/comms/v1` | P6 rwb-comms | The hold on generation for the case, with the rule and its version; faked |
| The pack-index read (operation name Not specified in the source documents (GAP-2793; ASM-4631)) | `/api/recovery/document/v1` | P5 rwb-document | The document index of the case and the defect list items of R-LIT-16; faked |
| The rule package read (operation name Not specified in the source documents (GAP-2797; ASM-4568)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-04, R-LIT-16 and R-LIT-36; faked |
| The cost-and-effect read (operation name Not specified in the source documents (GAP-2793; ASM-4631)) | `/api/recovery/agent/v1` | P10 rwb-agent | The cost and the effect of the proposed step under R-LIT-36, with the rule fallback; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All seven rows are contract dependencies of class C in fact that the plan's C row does not carry, and the absence is recorded as GAP-2793, GAP-2794, GAP-2795 and GAP-2797 with their assumptions.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. This baseline declares no event, adds no outbox row and widens no topic; the decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service (GAP-2794; ASM-4632).

#### 12.4 Events consumed

None. `TEMPLATE_WITHDRAWN`, `PACK_COMPLETE` and `SETTLEMENT_PROPOSED` are the event names of R-LIT-04, R-LIT-16 and R-LIT-36 in the state machine and the names of the workflow signals, not Kafka subscriptions: the service publishes and consumes nothing, DP-09 is not in the pattern set of this key, and the facts arrive on the contracts of 12.2. This baseline declares no consumer group, no subscription and no inbox of its own (GAP-2794; ASM-4632).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | The stage that hosts the step; its signals and its outcome for the parent are declared, not built; it holds the three rule clocks |
| `recommendNextStep` | Activity, the one next-step step | `rwb-litigation` | The case, the notice, the pack index and the agent answer in; the proposal, the cost and effect with its source, the rule ID with its package version and the case move out |

The activity name and the state names of the step are target design choices and are fixed by no source; the trigger is read as the arrival of a pack-complete or a template-withdrawn signal for a case in `PACK_ASSEMBLY` or `NOTICE_GENERATED`, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2794; ASM-4632). No activity is registered by this story.

#### 12.6 Schedules

None. The clocks of the step are durable timers of `LitigationWorkflow`: 1 working day under R-LIT-04, 2 working days under R-LIT-16 and 3 working days under R-LIT-36. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 is owned or moved here (GAP-2794; ASM-4632).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | This service's action row; read for the case reference and the pack, the proposal adds no column |
| hearing | S4 (`rwb_litigation`) | This service's hearing row; not touched by the step |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the proposal (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated signal |

`recovery_case` and `task` (P3), `notice` (P6), `document` (P5), `rule_row` and `decision_log_entry` (P7) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case fake | Case `RC-2026-001212` in `NOTICE_GENERATED`, in `PACK_ASSEMBLY` and in another state; the moves `NOTICE_BLOCKED` and `PACK_VERIFIED` accepted and a move refused | AC2, AC8 |
| rwb-comms fake | Notice `NTC-2026-001212` of the case with a withdrawn and with a current template, the hold accepted, and an unknown notice | AC3, AC8 |
| rwb-document fake | The pack index with every defect list item present, with one item missing, and no answer beyond 2 s | AC4, AC8 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-04, R-LIT-16 and R-LIT-36, and a second version | AC5, AC8 |
| rwb-agent fake | The cost and the effect of the proposed step, a low-confidence answer and no answer | AC5, AC8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC6, AC8 |
| gateway-bff composite route fake | The merged SCR-18 and SCR-19 model for case `RC-2026-001212` | AC8 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the seven consumed rows, the template-status field, the pack element and the step vocabulary are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2793, GAP-2794, GAP-2795, GAP-2797).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 7 consumed | The case read, the case-stage answer, the notice and template read, the notice hold, the pack-index read, the rule package read and the agent read; one hop, 2 s |
| Kafka | None declared | No event published and none consumed by this step; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered, 3 clocks | `LitigationWorkflow`, `recommendNextStep`, the 1-, 2- and 3-working-day clocks; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no case, no notice, no pack and no rule. What it publishes is one contract description, one AsyncAPI absence note that declares no event, nine contract tables and seven fakes.

**Deliverables.** The contract document `contracts/rwb-litigation-next-step.v1.yaml` for the consumed and answered elements, the step vocabulary and the three clocks as published reference values, the proposal element of the legal-action answer, the decision-record element of the library, the contract README rows for the consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the baseline fixes: the record, the answer and the hold commit together or not at all. DP-13 fixes the base of the service and this step provides no operation on it. DP-19 is behind SCR-18 and SCR-19, whose screen model is the edge contract's. DP-09 and DP-14 are outside the pattern set, which is why no event is declared in 12.3 or 12.4; DP-20 is outside it as well, and the agent row of 12.2 is a consumed contract the C row does not carry (GAP-2793).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan already carries for the app story. The seven consumed contracts are C dependencies in fact and not in the metadata row, which is None (GAP-2793, GAP-2794, GAP-2795, GAP-2797).

**Build steps**

1. Write the proposal element, its reasons and the cost-and-effect element of AC1, with the vocabulary as a reference version.
2. Write the case read and the case-stage answer of AC2 with their placeholders.
3. Write the notice and template row and the hold of AC3 with their placeholders and the absence test for a notice write.
4. Write the pack-index row of AC4 with its placeholder and the no-document-body test.
5. Write the rule-package and agent rows and the fallback rule of AC5.
6. Write the decision-record element and the three clocks of AC6 and validate them against the library schema and the workflow contract.
7. Write the error envelope, the messages and the rights of AC7.
8. Publish the seven fakes of AC8 and the drift test.
9. Record the naming baseline, the absence of a provided operation and the boundary of AC9, then tag the baseline and collect the consumer sign-off.

**Done when.** The contract tests pass, the vocabulary and the three clocks are published as reference values, the seven fakes answer every consumed path and the drift test is green, the absence test blocks a sixth operation, a cross-schema write, an event and a Schedule, and the app story, the screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a read or an answer is absent or invalid, or a body fails schema validation (X1, X8) | Enter {field}. |
| MSG-P4-002 | The role lacks the Litigation right the row declares (AC7) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes (AC6) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-012-1 of the FSD; the check is the owner's and this service holds no ACE batch status read | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and no path of this service raises it.

### 15. Screens and states

The contract serves SCR-18 Notice approval in its generated, approved, sent and blocked states and SCR-19 Litigation workspace in its pack, instructed, filed, hearing and judgment states, all through the gateway-bff composite route (DP-19). The route calls rwb-litigation for the proposal, rwb-case for the case and its route state and rwb-comms for the notice; this baseline fixes the rwb-litigation side only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refused, not-recorded, agent-unavailable and stale-data states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-012-01 | AC1, AC5 | Contract | The proposal of case `RC-2026-001212` with its reasons, its cost and effect and the package version; the contract half answers the element and the fallback |
| TC-E5-012-02 | AC2, AC8 | Contract | Case `RC-2026-001212` in `NOTICE_GENERATED` and in `PACK_ASSEMBLY`; the contract half answers the case read and the move to `NOTICE_BLOCKED` |
| TC-E5-012-03 | AC3, AC8 | Contract | The notice of the case with a withdrawn template and the pack index with every defect list item present; the contract half answers the template row and the move to `PACK_VERIFIED` |
| TC-E5-012-04 | AC7, AC9 | Contract | A role without the Litigation right and a malformed fact; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E5-012-05 | AC7, AC9 | Contract | RW-LITOFF holds CRUA, RW-ENFORCE holds CRU and RW-LEGAL holds RA; the contract half answers the rights and the absence of a sixth operation |
| TC-E5-012-06 | AC6, AC8 | Contract | The decision-record stub stopped and a signal that satisfies no rule; the contract half answers the MSG-P7-003 path and the fakes |
| TC-S4-E5012-CON-01 | AC1, AC5 | Contract | The proposal element, the reasons, the cost and effect, the vocabulary version, the rule-package row and the agent fallback validate with their placeholders |
| TC-S4-E5012-CON-02 | AC2, AC3, AC4 | Contract | The case answer, the notice and template row, the hold and the pack-index row validate with their placeholders and one hop with a 2 s budget |
| TC-S4-E5012-CON-03 | AC6, AC7 | Contract | The decision-record element, the three clocks, the error envelope, the messages and the rights validate |
| TC-S4-E5012-CON-04 | AC8, AC9 | Contract | The seven fakes match the document and a drifted fake fails the build; the absence test for a sixth operation, a cross-schema write, an event and a Schedule |

The six legacy cases are the legacy cases of RWB-E5-012 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S4-E5012-APP. The legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S4-E5012-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the step vocabulary, the three clocks, the agent threshold and the message texts stay reference rows and rule rows, never schema defaults or enumeration members of the code.
- No personal data in a fact, an answer, an example or a fake: identifiers, dates, list values, step names and a rule version only; every example is synthetic.
- The case stays with rwb-case, the notice with rwb-comms and the pack with rwb-document: the document declares no property of theirs as owned and no write to their schemas (BR3, BR4, BR5).
- The rules stay with rwb-decision and the model with rwb-agent: the document declares no rule, package, model or prompt of this service's own, and no prompt text appears in an example (BR7, BR12).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14, BR9).
- No provided operation beyond the five of the ownership rows: a sixth operation fails the review and the absence test (BR11).
- No retired element is reintroduced: the absence test of AC9 fails a build that declares an event, a Schedule, a Quartz row or a shared job table.
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-2796; ASM-4634) | The legacy story master carries no requirement ID and the FSD S4 requirements table names no requirement for this feature; the nearest reading is REQ-S4-005, "Court state, hearing dates, deadlines and fees are tracked on the case without a person reading an email", whose facts the step reads (FSD S4 requirements served; Business Requirements Program v5) | The proposal element, the reasons, the cost and effect, the case answer and the three clocks | TC-E5-012-01, TC-S4-E5012-CON-01, TC-S4-E5012-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed rows with their budget and breaker | TC-S4-E5012-CON-02 |
| ADR-022 | Local decision record with the central ledger | The record element and the shared `rwb.decision-record.v1` | TC-S4-E5012-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-012, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S4-E5012-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S4-E5012-CON-01 to -04 |
| Feature and screens | FEAT-LIT-12, SCR-18 Notice approval and SCR-19 Litigation workspace |
| Rules | R-LIT-04, R-LIT-16 and R-LIT-36, named from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2797) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal with durable timers), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the step, the evaluation of R-LIT-04, R-LIT-16 and R-LIT-36, the decision record, the clocks and the answers: RWB-S4-E5012-APP.
- The case of record, its route state, the case-stage timer and the officer task: rwb-case (P3) (GAP-2794; ASM-4632).
- The notice, its template, its status and the generation the hold requests: rwb-comms (P6) (GAP-2795; ASM-4633).
- The pack, its documents, its custody and its defect list: rwb-document (P5).
- The authoring, testing and approval of the LITIGATION package and its three rows: rwb-decision (P7) (GAP-2797; ASM-4568).
- The model, the prompt, the confidence threshold and the evaluation of the agent: rwb-agent (P10) and its contract (GAP-2793; ASM-4631).
- The step vocabulary as business content: the reference-data owner of rwb-case and the business owner of S4; the baseline fixes only its shape and its version (GAP-2793; ASM-4631).
- The settlement, its approval and the booking of the treatment under R-LIT-36: FEAT-LIT-13 and RWB-S4-E5013-APP of this module.
- The tracking of hearings, deadlines and fees that feeds the proposal: FEAT-LIT-11 and RWB-S4-E5011-APP.
- The decision of the officer or the approver and the authority behind it: rwb-access (P4) and the approver screens of the edge.
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-18 and SCR-19: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
