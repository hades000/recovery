# RWB-S9-E6031-CON Allocate work by measured return - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S9-E6031-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E6031-CON-16) |
| Contract version | v1 (the `/api/recovery/partner/v1` path) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the placement slice of rwb-partner, split from RWB-E6-031. It fixes the three operations on `/api/recovery/partner/v1` (DP-13) — the placement, the firm's instruction read and the panel read — the `InstructionRequest`, `Instruction` and `Partner` elements, the decision-record element of DP-03 with the scorecard and rule versions, the consumed rows of rwb-case, rwb-source-data, rwb-decision and rwb-access, the one event of the placement, the rights, the error envelope, the tables and the fakes. It declares no enumeration for the instruction status and no body that a source publishes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S9-E6031-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the placement slice of rwb-partner — the three operations on `/api/recovery/partner/v1`, the request and answer elements, the instruction event, the decision record with its rule and scorecard versions, the four consumed rows, the rights, the error envelope and the fakes**, so that **the app story, SCR-35, the firm-facing portal and the wave 4 harness build against one fixed, testable contract on Day 1, and a property, a consumed row or an answer shape can never drift between rwb-partner, rwb-case, rwb-source-data, rwb-decision and rwb-access without a failing build**.

It is the contract half of legacy RWB-E6-031. It owns:

- the OpenAPI 3.1 document of the placement slice and the naming baseline of the service;
- the `InstructionRequest`, `Instruction` and `Partner` elements, their required lists and their limits;
- the decision-record element, with the rule ID, the rule version and the scorecard version as required properties;
- the four consumed rows and the placeholder wherever a source gives no operation name;
- `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1` with its outbox rule;
- the rights of each operation and the error envelope with one message ID per condition;
- the tables the slice touches and the seven fakes;
- the contract tests: schema validation, the additive rule, the drift test, the absence tests and the boundary test.

It does not own the behaviour behind the operations, which is RWB-S9-E6031-APP; the panel data of FEAT-PRM-02; the override of FEAT-PRM-04; the accept, result and invoice operations of the later stories; the case, the products, the rule package, the ledger and the right, which belong to P3, P1, P7 and P4; and the composite route of SCR-35, which is RWB-PLT-N001-CON.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy feature touched five boundaries at once — the panel, the scorecard, the score, the decision log and a screen — inside one module. The target splits them: rwb-case owns the case, rwb-source-data owns the measured return and the score, rwb-decision owns the rule package and the ledger, rwb-access owns the right, and rwb-partner owns the panel, the instruction and the pick. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

Three properties make the baseline worth its own story. The **scorecard version** is required in the record: a pick recorded against "current" cannot be replayed, and the panel and the scorecard are versioned data (BR-S9-003). The **rank order** is answerable, so a pick can be defended without the app exposing its internals. And the **partner is absent from the request**: the caller says what work it is and the service picks; naming a partner is the override of FEAT-PRM-04 and never the default path, which keeps rotation and favouritism out of the contract itself.

The baseline also fixes the naming the checks require: schema and login `rwb_partner`, base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with its retry and `.dlt` topics, task queue `rwb-partner` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and the score and the measured return are consumed on the owner's contract only.

Five points are carried as gaps and assumptions rather than decided quietly: the plan's C row is None while the slice consumes four rows, and DP-04, DP-07, DP-08, DP-09 and DP-10 are absent from the pattern set although the slice evaluates a rule, reads versioned reference data, checks a right, publishes a fact and starts a workflow (ASM-5374, ASM-5375); no source publishes the placement request body or the instruction's property names (ASM-5372, ASM-5373); no source publishes a status vocabulary for an instruction (GAP-3111); and the error set of the three operations beyond the legacy messages is not published (ASM-5376).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `partner`, `partner_instruction` and `partner_user` are S9's, `recovery_case` and the work assignment are P3's, every `v_ace_*` view and the two products are P1's, `decision_log_entry` and `rule_row` are P7's, the capability area and the right are P4's. This document never declares another service's table or operation as its own.
- The rwb-case, rwb-source-data, rwb-decision and rwb-access rows of §12.2 are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3111; ASM-5374).
- The panel of FEAT-PRM-02 is populated and versioned; the scorecard and the panel carry the version the record requires (ASM-5371).
- The rule package of rwb-decision carries the scorecard rule with its ID and version in force (ASM-5374).
- The three tables arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The outbox and inbox library (DP-09) and the workflow kit (DP-10) are the platform dependencies of the event and the clock this baseline declares, and neither is in the plan's H row (ASM-5375).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-partner for this slice: the three operations with their requests, answers, rights and error responses.
2. Fix the `InstructionRequest` and `Instruction` elements, with the scorecard version and the rule version in the record, and with no partner in the request (ASM-5372, ASM-5373).
3. Fix the `Partner` element against the panel fields DF-PRT-001 to DF-PRT-006, and carry DF-PRT-007 as a gap rather than a guessed property.
4. Fix the decision-record element of DP-03, written before the instruction exists and carrying the rank order behind the pick.
5. Fix the four consumed rows and mark with the placeholder every operation name a source does not give.
6. Declare the one event of the placement, its topic, its key and its payload, and declare that nothing is consumed.
7. Record the naming baseline, the tables, the capability area and the rights, and that no value of the scorecard is a property.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests of section 16, including the drift test against the fakes and the absence tests.
10. Tag the baseline and hand it to RWB-S9-E6031-APP, SCR-35, SCR-34, the partner gateway and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or answer body fails schema validation | The schema lint fails the build; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed or removed inside major version 1 | The contract test fails; the change needs a new major version | None | AC2, AC7 |
| X3 | A fake drifts from the document | The drift test fails and the merge is blocked | None | AC7 |
| X4 | A consumed row carries a field list or an operation name no source gives | The row carries the placeholder and the fake is derived from the published document | None | AC3 |
| X5 | The document declares a property the sources do not publish, such as a score, a weight, a threshold, a partner share, a rotation position or a status enumeration | The review fails the baseline and the absence test fails the build | None | AC2, AC5 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` path, a `recovery_case` property or a rule row | The review fails the baseline and the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares a second event of this slice, a subscription or a Schedule | The absence test fails the build | None | AC5 |
| X8 | The rights of the operations are not the ones the API sheet and the legacy permission table give | The access test fails the build | MSG-P4-002 | AC6 |
| X9 | A partner is named in the placement request | The review fails the baseline: the pick is the service's and naming a partner is the override story | None | AC2 |

X1 to X3 are the shape and drift paths, X4 and X5 are the "no invented value" rule, X6 and X7 are the ownership and the call-type boundary, and X8 and X9 are the access and the anti-override rules.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the API sheet, the legacy story and the published owner contracts of rwb-case, rwb-source-data, rwb-decision and rwb-access only |
| Negotiable | The example values and the fake fixtures are settled in the baseline review; the operations, the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S9-E6031-APP, SCR-35, the firm-facing portal and the wave 4 harness on Day 1, and the four owner teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the placement slice of rwb-partner

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of partner, partner_instruction and partner_user is S9, of recovery_case is P3, of every v_ace_* view and the two products is P1, of decision_log_entry and rule_row is P7 and of the right is P4
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The three operations are declared on the partner base with their rights and errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-partner is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/instructions with the case reference in the path and status 201 on success, GET /partner/instructions and GET /partners, under the base /api/recovery/partner/v1 and owned by rwb-partner
    Then the placement declares the Idempotency-Key header and the repeated key answering the first instruction, and declares no partner in its body
    Then the answers 401, 403, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of accept, decline, result, invoice, override, panel maintenance or scorecard publication is declared by this document

  Scenario: AC2 The request, instruction and partner elements are fixed and no scorecard value is a property (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with the legacy Data table, the API sheet and the panel fields
    Then the InstructionRequest element declares the instruction type, the placement type and the rule version the caller expects, and nothing else; the placement request carries no partner
    Then the Instruction element declares the instruction reference, the case reference, the partner reference, the partner code, the instruction type, the status, instructed_at and due_at
    Then the Partner element declares partner code, partner name, partner type, panel status, contract end and the capacity state
    Then no element declares a score, a weight, a threshold, a partner share, a rotation position or a rank as a number of its own, and the rank order is returned as evidence and never accepted as input
    Then no enumeration is declared for the instruction status, because no source read for this WP publishes one (GAP-3111; ASM-5373)
    Then the property names the sources do not give are Not specified in the source documents (GAP-3111; ASM-5372) and are fixed by this baseline as design, not as a business value

  Scenario: AC3 The four consumed rows are declared and the facts stay with their owners (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case read is declared as consumed from P3 rwb-case, with the case reference, its state, its placement requirement and the assignment reference
    Then the measured return, the score and the freshness are declared as consumed from P1 rwb-source-data as DP08, DP11 and the freshness read, with the business date and the load time of each product
    Then the scorecard rule and its version are declared as consumed from P7 rwb-decision, and the session and the right from P4 rwb-access
    Then the operation names of the four rows are Not specified in the source documents (GAP-3111; ASM-5374) and each row carries the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The decision-record element is declared with its rule and scorecard versions (new, D-RCV-60)
    Given the decision and data sections of the baseline
    When they are compared with the library schema and the tables of S9
    Then one decision record is declared per placement, written through the local library on the shared rwb.decision-record.v1 before the instruction exists, and a failed write leaves nothing placed with MSG-P7-003
    Then the record requires the rule ID, the rule version, the scorecard version, the case reference, the instruction type, the candidate set with each partner's measured return, the pick and the decided-at time
    Then the record carries no personal data and no scorecard value as a literal
    Then the document declares the three tables of S9 and the library objects created in rwb_partner, and creates no table, column or migration
    Then the scorecard and the panel are declared as versioned reference data of the service, and the absence of DP-07 from the pattern set is recorded rather than added (ASM-5371, ASM-5374)

  Scenario: AC5 The instruction event is declared once on the partner topic and nothing is consumed (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with the naming rule, the ownership rows and the call-type rules
    Then rwb.partner.InstructionIssued.v1 is declared as the one event of the slice, on rwb.partner.events.v1, keyed by the case reference
    Then its payload carries dueon, instructionid, partnerid and type, and no customer data
    Then the event is written through the outbox in the placement transaction, one per placement, and its legacy identifier is EV-20 or EV-21 with the mapping Not specified in the source documents (GAP-3111; ASM-5375)
    Then the document declares no subscription of this slice and no Temporal Schedule, because the placement is commanded by the issueInstruction activity and S9 owns no job
    Then the workflow InstructionWorkflow is declared with its partner clock on queue rwb-partner in namespace rwb-recovery

  Scenario: AC6 The rights and the error envelope are fixed per operation (new, D-RCV-60)
    Given the access sections of the baseline
    When they are compared with the API sheet and the legacy permission table
    Then POST /cases/{caseId}/instructions declares the capability area Partner portal with right C and the scope applied
    Then GET /partner/instructions and GET /partners declare right R, and the accept, result and invoice rights of the module are not declared here
    Then the roles of the legacy permission table are carried unchanged and the C holders are read from its U row, which is recorded as an assumption (ASM-5377)
    Then a role without the right is described as refused with MSG-P4-002, and the envelope carries one message ID per condition

  Scenario: AC7 The seven fakes, the drift test and the absence tests close the baseline (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the document and the document with the ownership map
    Then seven fakes answer the document, including the case, the two products with freshness, the rule, the session, the decision-record stub and the two edge routes
    Then a property added, renamed or removed inside major version 1 fails a contract test
    Then a declared score, weight, threshold, rank input, status enumeration, second event, subscription, Schedule, v_ace_* path or recovery_case property fails an absence test
    Then the partner gateway is declared as the edge for the firm-facing read and gateway-bff for the staff screen, and neither is declared as provided by this service (ASM-5378)

  Scenario: AC8 Every business rule of section 8 is answered by a criterion or a test (new, D-RCV-60)
    Given the business rules BR1 to BR9 of section 8
    When each rule is compared with the criteria of this section and the rule coverage line of section 8
    Then each of BR1 to BR9 is answered by a criterion of this section or by the test named for it in the rule coverage line
    Then a rule that is an architecture constraint is kept in a guardrail or boundary test and not declared as a property

  Scenario: AC9 The provided operations declare the 404 answer with the envelope (new, D-RCV-60)
    Given the three operations of the baseline
    When their declared answers are compared with the answers of AC1
    Then each of the three operations declares the answer 404 with the envelope of AC1
    Then the message ID of the 404 answer is Not specified in the source documents (NEWAC-RWB-S9-E6031-CON-AC9)
```

The seven criteria are new and test only the contract. The four legacy criteria of RWB-E6-031 are not copied here: they are owned by RWB-S9-E6031-APP and RWB-ITG-E6031-ITG, and the four legacy cases appear in section 16 as the contract half of the surfaces they exercise.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract is the only place the shape is fixed; the app story, the screens and the harness build against it and never against a service's internal type | ADR-020; Template and Rules §R5.4 |
| BR2 | The base is `/api/recovery/partner/v1`, the topic `rwb.partner.events.v1`, the queue `rwb-partner`, the schema `rwb_partner` and the package `th.co.scb.ace.workbench.recovery.partner`; no document names another service's base or topic as its own | DP-13, DP-14; context pack |
| BR3 | The pick is the service's: the placement request carries no partner, and naming one is the override of FEAT-PRM-04 | R-WO-30; legacy RWB-E6-031; ASM-5372 |
| BR4 | The record requires the rule ID, the rule version and the scorecard version, written before the instruction exists | DP-03; BR-S9-003 |
| BR5 | The measured return, the score, the case, the rule and the right stay with their owners: the document declares them as consumed, never as provided, and no `v_ace_*` property exists | DP-05, DP-01; context pack slide 8 |
| BR6 | No score, weight, threshold, share, rotation position or status enumeration enters the document; every such value is reference data or a rule row | Legacy Guardrails; ASM-5373, ASM-5376 |
| BR7 | One event per placement, through the outbox, with identifiers only; nothing in this slice consumes an event or registers a Schedule | ADR-015; ASM-5375 |
| BR8 | Within major version 1 the document is additive only; a rename or a removal needs a new major version | ADR-020 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, a type, a status, two timestamps and a version only | Template and Rules §R7.2 (s17) |

The rule rows the slice answers to are those of R-WO-30 (place the account with the agency chosen on measured return and send the instruction the same day), R-WO-31 (no agency on the panel has capacity: hold and escalate), R-UNI-29 (a conduct breach suspends allocation) and R-UNI-45 (re-select on the scorecard, re-issue and restart the clock), governed in rwb-decision and copied character for character in RWB-S9-E6031-APP section 8. This baseline names them and declares none of them as a property.

Rule coverage: BR1 and BR2 by TC-S9-E6031-CON-01; BR3 by TC-S9-E6031-CON-02; BR4 by TC-E6-031-04 and TC-S9-E6031-CON-04; BR5 and BR9 by TC-S9-E6031-CON-03 and TC-S9-E6031-CON-05; BR6 by TC-S9-E6031-CON-02; BR7 by TC-S9-E6031-CON-04 and TC-S9-E6031-CON-05; BR8 by TC-S9-E6031-CON-07.

### 9. State transitions

The contract fixes the values an instruction may carry, not the machine that moves them.

| Element | Property | Fixed by the baseline |
|---|---|---|
| Instruction | status | A string, with `SENT` as the value the placement writes; no enumeration, because no source read for this WP publishes the vocabulary (GAP-3111; ASM-5373) |
| Instruction | instructed_at | Required, set by the service at the placement, never by the caller |
| Instruction | due_at | Required, derived from the service level of the instruction type and the partner type |
| Instruction | partner reference and code | Required on the answer, absent from the request |
| Partner | panel status and capacity | Read-only on the panel answer; the values are reference data of the panel story |

The transitions themselves belong to the app story and to the accept, decline, result and recall stories of the module; a baseline that published a state machine would publish a vocabulary no source holds.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The tech lead of rwb-partner | Publishes the baseline, owns the document and the fakes, and tags the contract when the tests pass |
| The owners of rwb-case, rwb-source-data, rwb-decision and rwb-access | Confirm the four consumed rows and their operation names; the placeholder stands until each confirms |
| rwb-access | Confirms the capability area "Partner portal" and the rights C and R of the three operations |
| RWB-S9-E6031-APP | Consumes the baseline; a change it needs is a change of this document, not a private variant |
| RWB-ITG-E6031-ITG | Consumes the baseline as the stub set of the wave 4 run |

No right is exercised through this document: it declares the rights of operations that the app story builds and the guard of RWB-PLT-E1037-CON enforces. DP-08 is not in this story's pattern set, and the absence is recorded (ASM-5374). The authorise check of rwb-access that the three operations call is Not specified in the source documents (DOR-RWB-S9-E6031-CON-6).

### 11. Data

| Element or field ID | Entity (owner) | Contract property | Note |
|---|---|---|---|
| DF-PRT-001 | partner (S9, `rwb_partner`) | id, as the partner reference | Required on the instruction answer |
| DF-PRT-002 | partner (S9, `rwb_partner`) | partnerCode | Required on the instruction and the panel answer |
| DF-PRT-003 | partner (S9, `rwb_partner`) | partnerName | Required on the panel answer |
| DF-PRT-004 | partner (S9, `rwb_partner`) | partnerType | Required on the panel answer; with the instruction type it selects the service level |
| DF-PRT-005 | partner (S9, `rwb_partner`) | panelStatus | Required on the panel answer, read only |
| DF-PRT-006 | partner (S9, `rwb_partner`) | contractEnd | Required on the panel answer, read only |
| DF-PRT-007 | partner (S9, `rwb_partner`) | the seventh field of the legacy list | Not specified in the source documents (GAP-3111; ASM-5372) |
| partner_instruction | partner_instruction (S9, `rwb_partner`) | instruction reference, case reference, partner reference, instruction type, status, instructed_at, due_at | The column list and its field IDs are Not specified in the source documents (GAP-3111; ASM-5372) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_partner`) | rule id, rule version, scorecard version, candidate set, outcome, decided at | Required; written before the instruction |
| DF-WRK-009 to DF-WRK-016 | assignment (P3 rwb-case) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Consumed on the case row, never declared as a property of this service |
| DF-ACE-270 to DF-ACE-279 | v_ace_score (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value and 4 more | Not declared: the score arrives on the DP11 row, and no `v_ace_*` property exists |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Not declared: the rule and its version arrive on the rule row |

The baseline declares shapes and writes nothing. It creates no table, no column and no migration; the three tables and the library objects arrive with the DB story and the library's own migration (DP-03, DP-09). No example, fixture or schema carries a personal value: the instruction names a partner organisation, never a customer.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). Frozen by this baseline.

| Method | Path | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/cases/{caseId}/instructions` | `InstructionRequest`: instruction type, placement type, rule version; no partner | `Instruction`, status 201 | Partner portal C, scope applied | `Idempotency-Key` header |
| GET | `/partner/instructions` | Filters by status and instruction type, paged | A page of `Instruction`, the firm's own only | Partner portal R | None, a safe read |
| GET | `/partners` | Filters by partner type, panel status and capacity, paged | A page of `Partner` | Partner portal R | None, a safe read |

The operations are the three the API sheet gives the module on this path family (Epics 3 to 8 Specification v3: "Issue an instruction to a partner by rule", "List the instructions placed with the caller's firm", and the panel read of the ownership rows). The error set is 401, 403 with MSG-P4-002, 404 for an unknown case, 409 for a replay that conflicts, 422 with MSG-GEN-001, 503 when a consumed contract or the library does not answer, and the data-freshness answer of MSG-P1-001 where the score product is behind its business date.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3111; ASM-5374)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its state, its placement requirement and the assignment reference |
| DP08 Partner performance, DP11 Scores and route economics and the freshness read (operation names Not specified in the source documents (GAP-3111; ASM-5374)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The measured return per partner, the score behind the pick, the business date and load time of each product |
| The scorecard rule read in force (operation name Not specified in the source documents (GAP-3111; ASM-5374)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule, its version and the ledger confirmation of the record |
| The session and the right of the caller (operation name Not specified in the source documents (GAP-3111; ASM-5377)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area and the right of the caller |

Each row is one hop with a 2 s budget, a breaker and a GET retried once with jitter (ADR-020). The rows are class C dependencies in fact while this story's C row is None; the story declares them, fakes them and records the absence (GAP-3111; ASM-5374).

#### 12.3 Events published

| Event | Topic | Key | Payload | Delivery |
|---|---|---|---|---|
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | the case reference | dueon, instructionid, partnerid, type | Outbox in the placement transaction, relayed after the commit, one per placement, CloudEvents envelope |

Its legacy identifier is EV-20 or EV-21 and the mapping of the two identifiers to their names is Not specified in the source documents (GAP-3111; ASM-5375); the name follows the naming rule of §R4. DP-09 is not in this key's pattern set, and the outbox and inbox library it requires is recorded (ASM-5375).

#### 12.4 Events consumed

None. The placement is a command and the result is needed, so the call type is the `issueInstruction` activity of §12.5 (context pack, slide 12 notes). The baseline therefore declares no subscription, and a stub set that subscribes to the write-off topic to learn of a placement fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction | `rwb-partner` | Input: the instruction reference, the partner, the partner type, the instruction type and the due date; signals: accept, decline, result and recall; query: the remaining partner clock |
| `issueInstruction` | Activity | `rwb-partner` | The case reference, the instruction type, the placement type and the rule version in; the `Instruction` out. The activity name is the one the context pack's call-type notes give |

Workflow ID form: Not specified in the source documents (CG-ALL-11829). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-11829). DP-10 is not in this key's pattern set and the workflow kit RWB-PLT-E1071-CON is recorded (ASM-5375).

#### 12.6 Schedules

None. S9 owns no job, so the baseline registers no Temporal Schedule and no Quartz row; the partner clock of §12.5 is a timer, not a schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| partner | S9 (`rwb_partner`) | The panel; read by this slice and written by the panel story |
| partner_instruction | S9 (`rwb_partner`) | The instruction of one placement; its columns are Not specified in the source documents (GAP-3110) |
| partner_user | S9 (`rwb_partner`) | The portal user of a firm; named for the ownership record, not touched here |
| decision_record | PLT library, created in `rwb_partner` | The local decision record of the pick (DP-03) |
| idempotency_key | PLT library, created in `rwb_partner` | The replay key and the answer it holds |
| outbox_event | PLT library, created in `rwb_partner` | The row of `InstructionIssued` |

Not owned and never declared as a property: `recovery_case` and `assignment` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6). No foreign key leaves the schema (DP-01), and no table is created by this baseline.

Reference data: this slice reads no parameter or list of its own. The values that BR6 keeps out of the document are read under DP-06 and DP-07 by RWB-S9-E6031-APP; no parameter key is named here.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-read fake | Case `RW-2027-000831` at `PLACEMENT_DECIDED` with an instruction requirement; a case that has moved on; a 2 s timeout | AC3, AC7 |
| rwb-source-data DP08 fake | The measured return of four eligible partners for business date `2027-04-30`, ranking `PRT-SYN-0031-A` first | AC3, AC7 |
| rwb-source-data DP11 and freshness fake | The score behind each pick, the business date, the load time, and a product behind its date | AC1, AC3 |
| rwb-decision rule fake | The scorecard rule at its version in force, with its rows | AC3, AC4 |
| rwb-access session fake | A caller holding Partner portal C, and a caller holding R only | AC6, AC7 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, AC7 |
| gateway-bff composite route fake and partner gateway fake | The merged SCR-35 answer, and the firm-facing read behind FAPI 2.0 | AC7 |

The fakes are test-only, are derived from the published document and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-3111; ASM-5374).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | The three operations on `/api/recovery/partner/v1`; the case, the two products with freshness, the rule and the session reads; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.partner.InstructionIssued.v1` on `rwb.partner.events.v1` through the outbox; no subscription |
| Temporal | 1 workflow and 1 activity, 0 schedules | `InstructionWorkflow` with the partner clock and `issueInstruction` on `rwb-partner` |
| File | None | No file is part of this slice; the instruction and its pack travel on the document and edge contracts |

### 13. Solution plan

**Artefacts.** One OpenAPI 3.1 document `rwb-partner.openapi.v1.yaml` for the placement slice, one JSON Schema library for the three elements and the two event rows, one fake set and one contract test suite. Java package `th.co.scb.ace.workbench.recovery.partner`; no business code is written here.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 fixes the record element and the transaction rule; DP-05 is declared as a prohibition, because the service holds no `v_ace_*` grant and takes the score and the measured return on the P1 contract; DP-13 fixes the base of the three operations; DP-19 fixes the two edges, gateway-bff for the staff screen and the partner gateway for the firm-facing read. DP-04, DP-06, DP-07, DP-08, DP-09 and DP-10 are absent from the pattern set although the slice names a rule, versioned reference data, a right, an event and a workflow; each absence is recorded (ASM-5374, ASM-5375, ASM-5377).

**Components of the baseline**

| Component | Responsibility |
|---|---|
| OpenAPI document | The three operations, their parameters, their bodies, their answers and their error responses |
| Element library | `InstructionRequest`, `Instruction`, `Partner` and the decision-record element, with their required lists and limits |
| Event schema | `InstructionIssued` and the envelope of the topic |
| Fake set and stub generator | Seven fakes derived from the document |
| Contract test suite | Schema lint, additive rule, drift, absence and boundary tests |
| Naming and access annex | The base, the topic, the queue, the schema, the package, the capability area and the rights |

**Contract tests.** Schema validation of every request and answer; the additive rule inside major version 1; the drift test of each fake against the document; the absence tests for a score, a weight, a threshold, a rank input, a status enumeration, a second event, a subscription, a Schedule, a `v_ace_*` path and a `recovery_case` property; the boundary test that no operation of another owner is declared as provided; and the access test that the rights are the ones the API sheet and the legacy permission table give.

**Configuration and reference data.** The examples and the fixtures are synthetic and are configuration of the test suite, never of the document. The scorecard weights, the panel thresholds, the capacity rule, the instruction types and the service levels stay reference data and rule rows of their owners; the document declares none of them.

**Done when.** The document validates, the nine contract tables of section 12 are complete, the seven fakes match it, the drift and absence tests pass, the four owners have confirmed their rows or their placeholder stands, and the baseline is tagged and handed to RWB-S9-E6031-APP, SCR-35, the partner gateway and the wave 4 harness.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request, a case or a panel row is absent or invalid | Enter {field}. |
| MSG-P4-002 | A role without the right of the operation calls it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the instruction exists | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | Data product stale after a late or failed load | Not specified in the source documents (GAP-3111; ASM-5376) |

The first three IDs and their text are the legacy message set of RWB-E6-031, copied unchanged. MSG-P1-001 is the data-freshness message of the Error and Message Standard v4, used here with the standard's meaning; its text is Not specified in the source documents (GAP-3111; ASM-5376).

### 15. Screens and states

The baseline fixes no screen. SCR-35 Placement and allocation (states: loading; empty, error and no access: Not specified in the source documents (CG-ALL-11833)) reads the placement answer through the gateway-bff composite route and SCR-34 Partner list (states: loading; empty, error and no access: Not specified in the source documents (CG-ALL-11832)) reads the panel; the field list of both belongs to RWB-PLT-N001-CON, and the composite route is declared here only as a consumed edge (DP-19). The firm-facing view is `GET /partner/instructions` behind the partner gateway (FAPI 2.0), and its route table is the edge story's (ASM-5378).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-031-01 | AC1, AC2 | Contract | The placement path, the three operations and the elements; the document answers the legacy placement surface |
| TC-E6-031-02 | AC4 | Contract | The decision-record element and the stopped stub; the record shape fixes the MSG-P7-003 path |
| TC-E6-031-03 | AC6 | Contract | The rights of the legacy permission table; 403 with MSG-P4-002 and the envelope |
| TC-E6-031-04 | AC4, AC7 | Contract | The record written before the instruction; the absence of a row, an event and a clock on failure |
| TC-S9-E6031-CON-01 | AC1 | Contract | The document validates; the three operations, the base, the `Idempotency-Key` and the six error answers are present |
| TC-S9-E6031-CON-02 | AC2 | Contract | The three elements validate with their properties and required lists; no score, weight, threshold, rank input or enumeration |
| TC-S9-E6031-CON-03 | AC3 | Contract | The four consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-foreign-grant boundary |
| TC-S9-E6031-CON-04 | AC4, AC5 | Contract | The record element matches the library schema; the event schema, the topic, the key and the outbox rule |
| TC-S9-E6031-CON-05 | AC5, AC7 | Contract | No subscription and no Schedule; the seven fakes match the document and a drifted fake fails the build |
| TC-S9-E6031-CON-06 | AC3 | Contract | The six owned tables of 12.7 in rwb_partner and the PLT library; no other table, no foreign key leaving the schema, no table created by this baseline |
| TC-S9-E6031-CON-07 | AC1 | Contract | The additive rule of major version 1: a rename or a removal fails the build; a new optional property passes |
| TC-S9-E6031-CON-08 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S9-E6031-CON-AC8) |
| TC-S9-E6031-CON-09 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S9-E6031-CON-AC9) |

The four legacy cases are those of RWB-E6-031 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, and the business outcome of each is proved by RWB-S9-E6031-APP and, for legacy AC1, by RWB-ITG-E6031-ITG with the `-ITG` copies. The legacy level maps to `Contract` here because the artefact under test is the contract. The five `TC-S9-E6031-CON-` cases are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in the contract: no score, weight, threshold, share, rotation position, instruction-type value or status enumeration appears in the document or in a schema default.
- No personal data in a schema, an example or a fake: identifiers, a type, a status, two timestamps and a version only, and every example is synthetic.
- The score and the measured return stay with rwb-source-data, the case with rwb-case, the rule with rwb-decision and the right with rwb-access: the document declares them as consumed and never as provided, and no `v_ace_*` path exists (BR5).
- The partner is never an input: the request carries the work, not the partner, and the override is a separate contract (BR3).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- Nothing is consumed and nothing is scheduled by this slice: an event subscription or a Schedule in the document fails the absence test (BR7).
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them and never redefines them.
- Within major version 1 the document is additive only; a rename or a removal opens a new major version (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S9-003 | Work is allocated to partners by measured return against a scorecard, not by a fixed share (FSD S9 Requirements served; the split plan carries no requirement id for this slice and the S9 FSD and TSD are not in this WP's extract set (GAP-3111)) | The placement operation, the elements and the record with its versions | TC-E6-031-01, TC-S9-E6031-CON-01, TC-S9-E6031-CON-02 |
| ADR-014 | Schema and login per service | `rwb_partner` and its own login | TC-S9-E6031-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `InstructionIssued` schema and the outbox rule | TC-S9-E6031-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the additive rule | TC-S9-E6031-CON-03, TC-S9-E6031-CON-05 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-E6-031-02, TC-S9-E6031-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-031, disposition Split (rework); feature FEAT-PRM-03 |
| Legacy criteria | None owned here: AC2 is RWB-S9-E6031-APP's and AC1 is RWB-ITG-E6031-ITG's |
| Source text | Legacy RWB-E6-031; Epics 3 to 8 Specification v3 (feature row FEAT-PRM-03, API rows for S9, integrations sheet); Business Rules and Routing Logic v4 rows R-WO-30, R-WO-31, R-UNI-29, R-UNI-45; context pack S9 |
| Test cases | TC-E6-031-01 to TC-E6-031-04, TC-S9-E6031-CON-01 to TC-S9-E6031-CON-05 |
| Feature and screens | FEAT-PRM-03, SCR-35 Placement and allocation, SCR-34 Partner list |
| Rules | R-WO-30, R-WO-31, R-UNI-29, R-UNI-45, named and not declared |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the three operations, the ranker and the record write: RWB-S9-E6031-APP.
- The panel and the fee schedule as data and the scorecard version's own governance: RWB-S9-E6030-APP.
- The override with a reason and its extra properties: RWB-S9-E6032-APP. The accept, decline, result and invoice operations: the later stories of this service.
- The case of record and the work assignment: rwb-case (P3). The measured return, the score and the freshness: rwb-source-data (P1). The rule package and the ledger: rwb-decision (P7). The capability area and the right: rwb-access (P4).
- The composite route and the screen field lists of SCR-35 and SCR-34: RWB-PLT-N001-CON. The partner gateway route table and its FAPI 2.0 profile: the edge stories of the same epic.
- The cross-service journey and its evidence: RWB-ITG-E6031-ITG.
- The deployment of the service, its flag, its dashboards and its runbook: the operations story of this legacy key.
