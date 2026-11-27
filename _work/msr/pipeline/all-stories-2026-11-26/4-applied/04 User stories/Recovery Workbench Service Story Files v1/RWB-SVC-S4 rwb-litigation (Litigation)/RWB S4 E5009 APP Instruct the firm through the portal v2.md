# RWB-S4-E5009-APP Instruct the firm through the portal

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5009-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-S4-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5009-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-009 for rwb-litigation. The three legacy acceptance criteria this slice owns (AC2, AC3 and AC4) are kept word for word with their origin tag and now run as one step of `LitigationWorkflow` on task queue `rwb-litigation`; the panel firm, the instruction row and the portal transport are rwb-partner (S9), the pack items and their index are rwb-document (P5), the case route state, its timer and its task are rwb-case (P3) and the rule package is rwb-decision (P7), all read or answered on their contracts and faked; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before anything changes (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19); the partner clock, the portal operation and the home of the instruction row have no source specification and are declared as the working read of the assumptions (GAP-2781 to -5; ASM-4615 to -5). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer**, I want **the Workbench to send the instruction and the pack to the firm and start the partner clock**, so that **cases reach court faster with complete packs**.

This is the application slice of legacy RWB-E5-009 and it owns:

- the three legacy acceptance criteria this slice owns (AC2, AC3 and AC4), copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the firm-instruction step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-24 and R-LIT-26 on the firm that the panel rule picked, and of R-LIT-28 on the partner clock, with the LITIGATION package version in force;
- the composition of the instruction and of the pack reference set — the case, the firm, the action, the document references and the deadlines — handed once to the partner portal, with no document and no partner row copied into `rwb_litigation`;
- the partner clock of 2 working days as one durable timer of `LitigationWorkflow`, started at the instruction and answered as the breach fact when it expires;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before anything changes (DP-03);
- the answers to rwb-case for the case move `FIRM_INSTRUCTED` under R-LIT-24 and R-LIT-26, for `FIRM_BREACHED_SLA` under R-LIT-28, for the case-stage timer and for the officer task the rules name;
- the behaviour behind the two operations of the legacy endpoints block, `POST /cases/{caseId}/legal-actions` (API-S4-002, right C) and `GET /legal-actions/{legalActionId}` (API-S4-003, right R), on base `/api/recovery/litigation/v1` (DP-13);
- the two surfaces SCR-19 Litigation workspace and SCR-20 Enforcement workspace, in the states this step sets, as this service's answers through the gateway-bff composite route (DP-19).

It does not own: the shape of the consumed facts, the instruction element, the rights, the errors and the fakes, which are RWB-S4-E5009-CON; the firm selection out of the panel, which is FEAT-LIT-08 and its own slice of this service; the partner panel, the `partner` and `partner_instruction` rows, the instruction status and the portal transport, which are rwb-partner (S9); the pack items, their index and the checklist, which are rwb-document (P5); the case of record, its route state, the case-stage timer and the task row, which are rwb-case (P3); the rule package and the rule rows, which are rwb-decision (P7); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-009 closed the gap between a chosen firm and a firm at work: the pack was verified, a panel firm was picked, and the instruction with the pack went out through the partner portal with a clock on the firm's acceptance. The functional specification keeps the objective and its metric: the feature "sends the instruction and the pack to the firm and starts the partner clock", against a filing that takes 21 days today, with packs that are incomplete and firm progress that is not tracked; the target is a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly (FSD S4 A2.9.1).

What D-RCV-60 changes is who owns each fact of the step. In the monolith the case row, the timer, the partner row, the instruction row and the decision log row sat in one `recovery` schema and one process. In the target:

- **the panel and the instruction are rwb-partner (S9).** `partner` (DF-PRT-001 to DF-PRT-007) and `partner_instruction` (DF-PRT-008 to DF-PRT-016) are partner-management rows, the panel is FEAT-PRM-02 of S9 that FEAT-LIT-08 names as its prerequisite, and the portal is the partner gateway fronting S9. This story reads the firm it instructs and asks S9 to issue the instruction; it writes neither row;
- **the pack is rwb-document (P5).** This step sends references to the pack items that the pack stories verified; no document body, no storage reference and no checklist is copied into `rwb_litigation`;
- **the case and its clock are rwb-case (P3).** `recovery_case` and the `timer` row are P3's; this story answers the move, the case-stage timer and the officer task, and starts no case row;
- **the partner clock is this service's.** R-LIT-24 and R-LIT-26 are litigation route-set rules of 2 working days and R-LIT-28 fires when that window passes with no filing, so the clock is a durable timer of `LitigationWorkflow`, the workflow that carries the years of a litigation journey (context pack, Temporal and Drools Design slide 7), and not a row of the partner service;
- **the decision is recorded first**, in the same transaction as the instruction request, the timer and the answer, which is what legacy AC4 tests.

The step is not carried by an event. The pack gives this service zero events, DP-09 is not in its pattern set, and the `FIRM_MATCHED`, `FIRM_NOMINATED` and `FIRM_BREACHED_SLA` of the state machine are the names of workflow signals and not Kafka subscriptions (GAP-2782; ASM-4616). The 2 working days is a value in force (Business Rules and Routing Logic v4, timer column of R-LIT-24, R-LIT-26 and R-LIT-28), and the instruction itself is a shape of this service's contract baseline; its fields beyond the ones the legacy data table names carry the placeholder (GAP-2781; ASM-4615).

### 3. Preconditions

- RWB-S4-E5009-CON is published: the instruction element, the pack reference set, the partner-clock element, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-partner panel read and the instruction request are available with their fakes: the firm, its panel status, its contract end, its coverage of the court region and case type, the conflict result, and the instruction it accepts with its reference and its due date. No operation name is published for either, so both carry the placeholder (GAP-2781; ASM-4615).
- The rwb-document pack read is available with its fake: the pack items of the case as document references on `GET /cases/{caseId}/documents` (API-P5-002), the index the pack stories verified.
- The rwb-case case read is available with its fake on `GET /cases/{caseId}` (API-P3-002): the case number, the product group, the stage, the parties by reference and the route state. The case-stage answer — the move, the timer and the task — has no published operation and carries the placeholder (GAP-2782; ASM-4616).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 and SCR-20 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The LITIGATION rule package is in force at its version with R-LIT-24, R-LIT-26 and R-LIT-28 in it; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce` (GAP-2785; ASM-4568).
- The firm has been selected out of the panel and the pack verified: the case is in `FIRM_SELECTION` under R-LIT-23 or in `FIRM_ESCALATED` under R-LIT-25, which are the sibling stories of this service.
- The working-day calendar that a 2-working-day clock is measured on, and the instruction types of the portal, are versioned reference rows of the business; their content is Not specified in the source documents (GAP-2783; ASM-4617).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_partner.partner_instruction` or on `rwb_case` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5009-CON when its tests pass.

### 4. Flow

1. The sibling selection step ends with the firm picked on the panel rule and the pack verified; the case stands in `FIRM_SELECTION` and the parent `CaseWorkflow` signals `FIRM_MATCHED` to the litigation stage. A firm nominated by the Head of Litigation after an escalation signals `FIRM_NOMINATED` with the case in `FIRM_ESCALATED` (GAP-2782; ASM-4616).
2. `instructFirm` on queue `rwb-litigation` reads the case on `GET /cases/{caseId}` (API-P3-002): case number, product group, stage, parties by reference and route state. The state must be `FIRM_SELECTION` for R-LIT-24 or `FIRM_ESCALATED` for R-LIT-26.
3. `PackReader` reads the pack items of the case on `GET /cases/{caseId}/documents` (API-P5-002) and keeps their references only: the document id, the type and the version the pack stories verified. No document body, storage reference or checklist row is copied into this schema.
4. `FirmReader` reads the firm on the rwb-partner contract: the firm reference, its panel status, its contract end, the court regions and case types it covers and the conflict result. The panel row is S9's and is never written here (GAP-2781; ASM-4615).
5. `InstructionEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates the rule whose condition the fact satisfies: a panel firm that covers the court region and case type and passes the conflict check (R-LIT-24), or a firm the Head of Litigation nominated after widening the panel (R-LIT-26).
6. The evaluation answers the rule ID, the package version, the action of the rule and the case move the rule names.
7. `InstructionDecisionRecordWriter` writes one decision record through the local decision-record library **before any change**: the case reference, the firm reference, the rule ID with its version, the inputs reference, the pack reference, the clock start and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC2, AC3 and AC4).
8. `PartnerInstructionClient` asks rwb-partner to issue the instruction with the pack through the portal: the case and its number, the firm, the action of the case, the pack reference set, the instruction type from reference data and the request for the due date. S9 writes its `partner_instruction` row and answers the instruction reference, the firm, `instructed_at` and `due_at`; this story writes none of those fields (GAP-2781; ASM-4615).
9. The partner clock starts as a durable timer of 2 working days of `LitigationWorkflow`, measured on the working-day calendar in force, at `instructed_at` as S9 answered it; the workflow state becomes `FIRM_INSTRUCTED`.
10. `CaseAnswer` answers rwb-case in one call: the case move `FIRM_INSTRUCTED`, the case-stage timer with its start and expiry for the instruction, the officer task only where a person is needed, and the rule ID with its version. rwb-case writes `recovery_case`, its route state and its own timer and task rows; this service writes none of them (GAP-2782; ASM-4616).
11. When the clock expires with no filing, R-LIT-28 fires: the step marks the instruction breached on the rwb-partner contract, answers `FIRM_BREACHED_SLA` to rwb-case with the partner-and-agency-manager task, and writes the decision record of the breach. The re-selection that follows is the firm-selection story's, and the notification of the partner manager is rwb-comms' (GAP-2783; ASM-4617).
12. A repeated signal for the same case and the same firm writes nothing, requests no second instruction, starts no second clock and sends no second answer, and the repeat is counted.
13. SCR-19 Litigation workspace shows the pack and instructed states and SCR-20 Enforcement workspace shows its states, both read only through the gateway-bff composite route, and `POST /cases/{caseId}/legal-actions` (API-S4-002) and `GET /legal-actions/{legalActionId}` (API-S4-003) answer the action and the pack of the instructed case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no instruction is requested, no clock starts, no case move is answered and the firm keeps its state | MSG-P7-003 | AC4, TC-E5-009-04, TC-E5-009-06 |
| X2 | A role without the Litigation right calls API-S4-002 or reads the step outcome | The call is refused at the edge before any change; nothing is instructed and nothing moves | MSG-P4-002 | TC-E5-009-05 |
| X3 | The case is not in `FIRM_SELECTION` for R-LIT-24, or not in `FIRM_ESCALATED` for R-LIT-26 | 409 on the call; no rule is evaluated, nothing changes and no decision record is written | None | AC2, AC3 |
| X4 | The firm is unknown to rwb-partner, off panel, or outside the caller's scope | 404 or 409 on the read; the step stops and nothing is written | None | AC2, AC3 |
| X5 | The pack items of the case are not found, or the pack reference set is empty | The instruction is held: MSG-S4-001 names the missing item and nothing is requested | MSG-S4-001 | AC2 |
| X6 | A required field of the instruction is absent or invalid | MSG-GEN-001 names the field; the instruction is not requested and no clock starts | MSG-GEN-001 | AC2, AC3 |
| X7 | The claim of the case expires before the instruction is accepted | The warning is shown on the screen and the instruction stands; the prescription review is the head-of-litigation path of this service | MSG-S4-002 | AC3 |
| X8 | A consumed contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered | None | AC2, AC3 |
| X9 | The same case and firm signal arrives twice | One record, one instruction request, one clock and one answer; the repeat is counted | None | AC2, AC3 |
| X10 | The partner clock expires with no filing | R-LIT-28 fires: the instruction is marked breached, `FIRM_BREACHED_SLA` is answered with the partner-manager task and the breach is recorded | None | AC3 |
| X11 | A component, a statement or a test reaches a `partner_instruction` row, a `recovery_case` row, a document body, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5 |

X1 to X7 are the exception paths of RWB-E5-009 and of FSD S4 A2.9.4.3 carried onto the split, X8 to X11 are the paths the target call types and the clock add. The 2 working days of X10 is a value in force and not a constant of the code.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5009-CON and the fakes of rwb-partner, rwb-document, rwb-case and rwb-decision, on its own schema, and needs no live service |
| Negotiable | The activity name, the state names of the step and the shape of the case answer are this story's choice; the rules, the messages, the screens, the clock and the instruction element are fixed |
| Valuable | The instruction and the pack reach the firm in one recorded step on the day the firm is picked, and a firm that does not act is visible on a clock rather than in a spreadsheet |
| Estimable | One workflow step, one evaluator, one record write, one instruction client, one durable clock, one answer client and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases, firms and packs through the contract fakes, plus the component cases of the refused right and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Instruct the firm through the portal

  Background:
    Given case "RC-2026-000609" carries the verified litigation pack "PACK-2026-000609" of three documents
    Given the LITIGATION rule package is in force at its version and carries R-LIT-24, R-LIT-26 and R-LIT-28
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC2 Rule R-LIT-24 (legacy RWB-E5-009 AC2)
    Given the rwb-case contract mock returns the case state "FIRM_SELECTION" for "RC-2026-000609"
    Given the rwb-partner contract mock returns the panel firm "LF-2026-0009" covering the court region and the case type and passing the conflict check
    Given the rwb-document contract mock returns the three pack items of "RC-2026-000609"
    Given a case in state FIRM_SELECTION
    When firm matched
    Then issue the instruction with the pack through the portal
    Then the case moves to FIRM_INSTRUCTED

  Scenario: AC3 Rule R-LIT-26 (legacy RWB-E5-009 AC3)
    Given the rwb-case contract mock returns the case state "FIRM_ESCALATED" for "RC-2026-000609"
    Given the rwb-partner contract mock returns the firm "LF-2026-0009" nominated by the Head of Litigation after the panel was widened
    Given the rwb-document contract mock returns the three pack items of "RC-2026-000609"
    Given a case in state FIRM_ESCALATED
    When firm nominated
    Then issue the instruction with the pack through the portal
    Then the case moves to FIRM_INSTRUCTED

  Scenario: AC4 Not recorded (legacy RWB-E5-009 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E5-009 that this slice owns, word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written` and `firm matched` all stand. The cross-service parts are mocked, so AC2 and AC3 each carry three `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions. Legacy AC1, the unattended main flow of the feature, is owned by RWB-ITG-E5009-ITG and is not copied here. What the legacy lines describe happens in four places in the target: rwb-case holds the route state and writes the move, rwb-partner holds the panel and the instruction, rwb-document holds the pack, and this story evaluates the rule, writes the record, requests the instruction, starts the clock and answers the case.

### 8. Business rules

| Rule ID | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-24 | Litigation | D7 | FIRM_SELECTION | FIRM_MATCHED | panel firm covers the court region and case type and passes the conflict check | Issue the instruction with the pack through the portal | FIRM_INSTRUCTED | Panel law firm | Partner Portal | 2 working days |
| R-LIT-26 | Litigation | D7 | FIRM_ESCALATED | FIRM_NOMINATED | the Head of Litigation nominates a firm or widens the panel | Issue the instruction with the pack through the portal | FIRM_INSTRUCTED | Panel law firm | Partner Portal | 2 working days |
| R-LIT-28 | Litigation | D7 | FIRM_INSTRUCTED | FIRM_BREACHED_SLA | the instruction is past due with no filing | Mark the instruction breached, notify the partner manager and re-select | FIRM_DECLINED | Partner and agency manager | Partner Portal | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. The owner column is a business role: the `Panel law firm` owner of R-LIT-24 and R-LIT-26 is the party that is instructed and holds the clock, and the `Partner and agency manager` owner of R-LIT-28 is the role of the task that the breach raises. The systems column maps as follows: Partner Portal is rwb-partner (S9) and its portal, and the `Workbench` of the FSD feature is this service and the screens. The 2 working days is read as reference data with a version and is never a constant.

| ID | Rule | Source |
|---|---|---|
| BR1 | The firm-instruction step of the litigation journey is this service's: the evaluation of R-LIT-24, R-LIT-26 and R-LIT-28, the composition of the instruction and of the pack reference set, the partner clock and the decision record are `rwb_litigation` objects and workflow state, and no other service evaluates them | Architecture v5 slide 3 (litigation: court, judgment, enforcement); context pack ownership rows (workflow `LitigationWorkflow`, queue `rwb-litigation`); FSD S4 A2.9 |
| BR2 | The decision is recorded before anything changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-009 AC4 |
| BR3 | The panel firm, its status, its coverage and conflict result, the `partner_instruction` row and the portal transport stay with rwb-partner (S9); this story reads the firm and requests the instruction, and writes none of those rows | Context pack (ownership rows of S4 name `hearing` and `legal_action` only); Architecture v5 slides 4 and 8 (partner management S9, partner gateway FAPI 2.0); Epics 3 to 8 Specification v3 (FEAT-LIT-08 depends on FEAT-PRM-02, the S9 panel); GAP-2781 |
| BR4 | The pack items and their index stay with rwb-document (P5): the instruction carries document references and no document body, storage reference or checklist row enters `rwb_litigation` | Architecture v5 slide 10 (documents and pack at one hop from their owner); FSD S4 A2.9.2 ("Integration points: Partner portal, LIT"); GAP-2781 |
| BR5 | The case move, the route states `FIRM_SELECTION`, `FIRM_ESCALATED`, `FIRM_INSTRUCTED` and `FIRM_BREACHED_SLA`, the case-stage timer and the task stay with rwb-case (P3); this story answers them and writes no case row | Context pack (case of record owned by P3); TSD S4 T5.2 ("P3 for the case"); GAP-2782 |
| BR6 | No ACE view and no ACE table is read or written here, and no cross-schema join is made: this service holds no `v_ace_*` grant, and every fact arrives on its owner's contract | DP-05; context pack (ACE data only through the owner's contract or `v_ace_*` views) |
| BR7 | The same case and firm signal twice writes once, requests one instruction, starts one clock, answers once and counts the repeat | TSD S4 T-A.2 (idempotency rule of the write paths); Architecture v5 slide 11 |
| BR8 | The partner clock is 2 working days on the calendar in force, and its expiry is R-LIT-28's breach; the working-day calendar and the instruction types are reference rows and neither is a constant of the code | Business Rules and Routing Logic v4 (R-LIT-24, R-LIT-26, R-LIT-28 timer column); BR-S4-009 (FSD S4 A2.9.3.1); GAP-2783 |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case and firm references, document references, codes, dates and a rule version | Template and Rules v1 §R7.2 (s17); FSD S4 A2.9 field catalogue |

**Where each rule lives in the target.** R-LIT-24 and R-LIT-26 compose one instruction, request it on the partner contract, start the clock at `instructed_at` and ask the case for `FIRM_INSTRUCTED`; R-LIT-28 fires on the clock, marks the breach on the partner contract and asks the case for `FIRM_BREACHED_SLA` with the partner-and-agency-manager task, whose re-selection is the firm-selection story's. VR-S4-009-1 of the FSD tests the freshness of the ACE batch of the source and raises MSG-P1-001; this service holds no ACE batch status read and no ACE-sourced fact in this step, so the check belongs to the owner of the data product and the message is carried in section 14 without a path here (GAP-2781; ASM-4615).

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR5).

| From (case route state) | Event | Condition | To (answered, written by rwb-case) |
|---|---|---|---|
| FIRM_SELECTION | FIRM_MATCHED under R-LIT-24 | panel firm covers the court region and case type and passes the conflict check | `FIRM_INSTRUCTED`, with the case-stage timer of the instruction |
| FIRM_ESCALATED | FIRM_NOMINATED under R-LIT-26 | the Head of Litigation nominates a firm or widens the panel | `FIRM_INSTRUCTED`, with the case-stage timer of the instruction |
| FIRM_INSTRUCTED | FIRM_BREACHED_SLA under R-LIT-28 | the instruction is past due with no filing | `FIRM_DECLINED`, with the partner-and-agency-manager task answered |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The selection step signals the firm of the case | The case state and the pack are read | Evaluating |
| Evaluating | The rule fires | The decision record is written | Instructing |
| Instructing | The partner contract accepts the instruction | The clock is started and the case answer is accepted | Waiting for the filing |
| Waiting for the filing | The clock of 2 working days expires with no filing | R-LIT-28 fires | Breached, with the answer and the record |
| Instructing | The record write, the instruction request, the clock or the answer fails | X1, X8, X10 | Waiting, nothing changed |

No column of this service changes in this story: the step has no business row of its own, and its durable state is the workflow state and the partner clock. The `partner_instruction` row of rwb-partner and the route state and timer rows of rwb-case are read or answered, never written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-litigation service identity | Runs the step, evaluates the rules, writes the decision record, requests the instruction, starts the clock and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix and the also-user of the FSD feature: reads the pack and instructed states on SCR-19 and can open and read the legal action on API-S4-002 and API-S4-003 |
| RW-ENFORCE, enforcement owner | Litigation CRU: reads the instructed state on SCR-19 and SCR-20 |
| RW-LEGAL, RW-PRODHEAD, RW-HEADLIT | Litigation RA: read the instruction, the pack and the decision record; RW-HEADLIT is the nominating role of R-LIT-26 |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF and 22 more | Litigation R: read only, as the legacy permission table gives it |
| PT-LAWFIRM, law firm user | Litigation RU as TSD S4 T6.1 gives it: receives the instruction in the portal; no part of this step is taken by a firm user |
| RW-AGENCYMG, partner and agency manager | The owner of R-LIT-28: receives the breach task and the re-selection, which the firm-selection story runs |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Litigation R or U as the TSD S4 T6.1 matrix gives it; the service identities run the step and are subject to the same checks |

The FSD declares the feature "runs unattended" with the litigation officer as also-user, and both statements hold: the step runs under the service identity when the selection signals the firm, and no officer approval is asked for the instruction itself. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation on the contract, and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Read on API-P3-002 as the facts of the instruction, and answered as the move; never written |
| DF-WRK-027 to DF-WRK-036 | timer (P3, `rwb_case`) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read and not written as a table: the partner clock is a durable timer of `LitigationWorkflow`, and the case-stage timer and the task are answered to rwb-case |
| DF-PRT-001 to DF-PRT-007 | partner (S9, `rwb_partner`) | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | Read only, on the P9 contract: the firm reference, its panel status, its contract end and its coverage of the court region and case type; never written, joined or stored here |
| DF-PRT-008 to DF-PRT-016 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | Written by S9 on the instruction request and answered back with the reference, `instructed_at` and `due_at`; this story stores none of the fields and copies no row |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before anything changes |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | id, rule_id, rule_version, route_set and 11 more | Read as the LITIGATION package in force, never written |
| DF-DOC-001 to DF-DOC-011 | document (P5, `rwb_document`) | id, case_id, person_key, document_type, source, storage_ref and 5 more | Read as references only on API-P5-002; the document body, the storage reference and the index row stay with P5 |
| DF-LEG-001 to DF-LEG-014 | legal_action (S4, `rwb_litigation`) | the 14 action fields | Read on API-S4-003 and opened on API-S4-002 with `action_type` of LOV-LEGAL-TYPE; the instruction writes no action column of its own |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1 and the legacy data table of RWB-E5-009. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). `partner`, `partner_instruction`, `recovery_case`, `timer`, `document`, `decision_log_entry` and `rule_row` are not created, not written and not read as tables.

**No personal data.** The instruction carries a case number, a firm reference, document references, an action type, dates and a rule version. No name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input; the fixture of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). The two operations are the endpoints block of the legacy story and rows of TSD S4 T-A.1, re-based on the service path; this story supplies their behaviour for the instructed case and adds no operation of its own.

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | `LegalActionRequest`; `caseId` from the path | 201 with `LegalAction` in status `OPEN` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | None | 200 with `LegalAction` with pack, instruction, hearings and judgment | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |

The purpose, rights, idempotency and error statuses are those of TSD S4 T-A.1 and T-A.2, with the base renamed by DP-13 and the bodies fixed in RWB-S4-E5009-CON. API-S4-001 `POST /notices/{noticeId}/approve` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` are the notice and hearing stories' of this service: the instruction opens no notice and no hearing.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` (API-P3-002) | `/api/recovery/case/v1` | P3 rwb-case | The case facts of the instruction and the route state that gates R-LIT-24 and R-LIT-26; faked |
| The case-stage answer (operation name Not specified in the source documents (GAP-2782; ASM-4616)) | rwb-case (P3) | P3 rwb-case | The move `FIRM_INSTRUCTED` or `FIRM_BREACHED_SLA`, the case-stage timer, the task and the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The firm read and the instruction request (operation name Not specified in the source documents (GAP-2781; ASM-4615)) | `/api/recovery/partner/v1` | P9 rwb-partner | The firm, its panel status, its contract end, its coverage and the conflict result; and the instruction with the pack, answered with the instruction reference, `instructed_at` and `due_at`; faked |
| `GET /cases/{caseId}/documents` (API-P5-002) | `/api/recovery/document/v1` | P5 rwb-document | The pack item references the instruction carries; no body and no storage reference is copied; faked |
| The rule package read (operation name Not specified in the source documents (GAP-2785; ASM-4568)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-24, R-LIT-26 and R-LIT-28; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four cross-service rows are contract dependencies of class C in fact that this story's metadata row does not carry, because the plan's C row is None; the two platform rows of the pattern set (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are its only H rows beside its own contract (GAP-2781, GAP-2782, GAP-2785; ASM-4615, ASM-4616, ASM-4568).

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. DP-09 is not in this story's pattern set, so it writes no outbox row and widens no topic; the only record it relays is the local decision record on the shared `rwb.decision-record.v1` of DP-03, which is the library's topic and not an event of this service (GAP-2782; ASM-4616).

#### 12.4 Events consumed

None. The `FIRM_MATCHED` and `FIRM_NOMINATED` of the state machine are the names of the signals that start the step, not a Kafka subscription: this service has no consumer group, no subscription and no inbox of its own. The firm arrives on the workflow signal and is read on the P9 contract of 12.2, and the case state on the rwb-case read (GAP-2782; ASM-4616).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4 and the firm; signals: the firm of the selection step, the case state answered by rwb-case, the rule package in force, the filing fact of the filing story; the partner clock of 2 working days |
| `instructFirm` | Activity, the one firm-instruction step of this story | `rwb-litigation` | The case, the firm and the pack references in; the rule ID with its package version, the instruction reference, `instructed_at`, `due_at`, the clock fact and the case move out, with the decision record written in the same transaction |

The activity name and the workflow state names are target design choices of this story and are fixed by no source document; the trigger of the step is read as the arrival of the firm signal for a case whose pack is verified, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2782; ASM-4616). `JOB-10` of the notice dispatch belongs to the notice story, and no job of Architecture v5 is owned or registered here.

#### 12.6 Schedules

None. The partner clock is a durable timer of `LitigationWorkflow` of 2 working days started at `instructed_at` under R-LIT-24 and R-LIT-26, and it fires R-LIT-28 when it expires with no filing. No Temporal Schedule, no Quartz row and no shared job table is declared, and no batch window is read or set by this story (GAP-2783; ASM-4617).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | This service's action row, opened or read on API-S4-002 and API-S4-003; the instruction writes no column of its own |
| hearing | S4 (`rwb_litigation`) | This service's hearing row; not touched by this story |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated signal and of the repeated POST |

Not owned and never read as a table: `partner` and `partner_instruction` (S9), `recovery_case`, `timer` and `task` (P3), `document` and its index (P5), `decision_log_entry` and `rule_row` (P7), and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner panel and instruction fake | The panel firm `LF-2026-0009` covering the court region and case type with a passing conflict check; a firm off panel and a conflicted firm; an instruction accepted with reference `INS-2026-0009`, `instructed_at` 2026-12-08 and `due_at` 2026-12-10; an instruction refused; a breach mark accepted; no answer beyond 2 s | AC2, AC3, X4, X8, X10 |
| rwb-document pack fake | The three verified pack items of `RC-2026-000609` with their document ids, types and versions; an empty pack | AC2, AC3, X5 |
| rwb-case fake | The case `RC-2026-000609` in `FIRM_SELECTION`, in `FIRM_ESCALATED` and in another state; the moves `FIRM_INSTRUCTED` and `FIRM_BREACHED_SLA` accepted, and a move refused | AC2, AC3, X3, X10 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-24, R-LIT-26 and R-LIT-28, and a package at a second version | AC2, X9 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 answer for case `RC-2026-000609`, with the instruction facts of this service read once | AC2, AC3 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the two unnamed consumed rows and the fields of the instruction element that no source gives are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2781, GAP-2782, GAP-2785; ASM-4615, ASM-4616, ASM-4568).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The case read, the case-stage answer, the firm read and instruction request, the pack read and the rule package read; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity, 1 durable timer | `LitigationWorkflow`, `instructFirm` and the partner clock; no Schedule |
| File | None | The portal is a REST contract of S9 and the pack is a set of references; no file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `instruction`, Java package `th.co.scb.ace.workbench.recovery.litigation.instruction`; front end `src/modules/recovery/litigation/FirmInstruction.tsx`, the fragment SCR-19 and SCR-20 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the instruction request, the clock and the case answer commit together or not at all. DP-13 is the base of the two operations this story provides. DP-19 is how SCR-19 and SCR-20 reach this service, one hop through the gateway. DP-01, DP-02 and DP-14 are stated as the naming rules this story obeys — one schema and one login for the service, and the topic of the owner — and add no dependency (GAP-2781; ASM-4615).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan already carries. The four consumed contracts are class C in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-2781, GAP-2782, GAP-2785).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` instruction branch | Workflow | The stage that waits for the firm, holds the partner clock and the breach signal, and reports the outcome to the parent |
| `instructFirm` | Activity | The one step: read the case, the firm and the pack, evaluate R-LIT-24 or R-LIT-26, write the record, request the instruction, start the clock and answer the case |
| `InstructionEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the coverage and conflict conditions and the breach rule |
| `InstructionComposer` | Service | Builds the instruction element and the pack reference set; no document body and no partner row is copied |
| `InstructionDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before anything changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `PartnerClock` | Workflow timer | Starts the 2-working-day clock at `instructed_at` on the calendar in force and fires R-LIT-28 on expiry |
| `PartnerInstructionClient` | Client | The firm read and the instruction request on the P9 contract, one hop, 2 s, breaker, and the breach mark |
| `PackReader` | Client | The pack item references on the P5 contract, one hop, 2 s, breaker |
| `CaseFactClient` and `CaseAnswer` | Client and signal reporter | The case read and the case-stage answer to rwb-case; it reports, it never changes a case row |
| `FirmInstruction` | React component | Shows the pack and instructed states on SCR-19 and the enforcement states on SCR-20, read only, with the refusal, pack-defect, breach and failure states |

**Database and migrations.** No Flyway file of its own. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). This story writes no business row, so no column is added for the instruction reference, `instructed_at` or `due_at`: those are facts of the partner row, of the record and of the clock, and storing them would copy another service's fact into this schema (GAP-2781, GAP-2783).

**Configuration and reference data.**

- The working-day calendar and the instruction types, read as versioned reference rows; their content is Not specified in the source documents (GAP-2783; ASM-4617).
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`.
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The instruction branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the firm signal as its trigger (GAP-2782; ASM-4616).
2. `CaseFactClient` and `PackReader` against their fakes, with the 2 s budget, the breaker and the missing-pack path (AC2, X5, X8).
3. `PartnerInstructionClient` and `InstructionComposer` against the panel and instruction fake, with the off-panel and conflicted paths (AC2, AC3, X4, X6).
4. `InstructionEvaluator` over the LITIGATION package, with the three rules, the 2 working days and the no-fire path (AC2, AC3, X3).
5. `InstructionDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `PartnerClock`, the calendar read and the breach answer, with the expiry path and the missing-calendar path (X10, X7).
7. `CaseAnswer` with the move, the case-stage timer and the task (AC2, AC3, X10).
8. `FirmInstruction` and the two screens through the composite route fake (AC2, AC3).
9. The boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no write to `rwb_partner`, `rwb_case`, `rwb_document` or `rwb_decision` (X11, BR3, BR4).

**Feature flag.** `rwb.litigation.firm-instruction-v1`, read as a flag of the platform library; off means the step holds the firm signal and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic firm signal in SIT, each of the three rules produces its record, its instruction request, its clock state and its move, a repeated signal writes once, a forced record failure changes nothing, no `partner_instruction` row and no `recovery_case` row is written from this service, and SCR-19 and SCR-20 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | The pack items the instruction needs are missing (X5) | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim of the case is close to expiry when the instruction is issued (X7) | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the instruction is absent or invalid (X6) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right calls API-S4-002 or reads the step outcome (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | Carried from the message set of this feature, whose VR-S4-009-1 tests the freshness of the ACE batch of the source. This service holds no ACE batch status read and no ACE fact in this step, so the check is the owner's and no path here raises it (GAP-2781; ASM-4615) | {product} is from {date}. Today's ACE batch has not arrived. |

The six texts are the legacy wording of RWB-E5-009 section 14 and of the FSD S4 A2.9 message list, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X8), a firm that is not found (X4) and a case in the wrong state (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it evaluates, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-19 Litigation workspace | Pack | The verified pack of the case and the firm picked out of the panel, read only, owned by the pack and selection stories |
| SCR-19 Litigation workspace | Instructed | The instruction reference, `instructed_at`, `due_at` and the partner clock, with the decision record of R-LIT-24 or R-LIT-26 |
| SCR-19 Litigation workspace | Filed, Hearing, Judgment | The later states of the same surface, read only and owned by the filing and hearing stories |
| SCR-19 Litigation workspace | Breached | The clock expired with no filing, the breach of R-LIT-28 and the partner-and-agency-manager task |
| SCR-20 Enforcement workspace | Requested, Seized, Auctioned, Closed | The later enforcement states of the same case, read only and owned by the enforcement stories |
| SCR-19 Litigation workspace | Pack defect | The instruction is held and MSG-S4-001 names the missing item (X5) |
| SCR-19 Litigation workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | Claim expiring | MSG-S4-002 with the expiry date of the claim, and the instruction still standing |

The route merges the answer of this service with rwb-case for the case and its route state, rwb-partner for the firm and the instruction and rwb-document for the pack; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here. The two state lists are the legacy lists of RWB-E5-009 ("pack; instructed; filed; hearing; judgment" and "requested; seized; auctioned; closed") with the breach, pack-defect, refusal and failure states this story adds.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-009-02 | AC2 | End to end | Rule R-LIT-24 |
| TC-E5-009-03 | AC3 | End to end | Rule R-LIT-26 |
| TC-E5-009-04 | AC4 | Component | Not recorded |
| TC-E5-009-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-009-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The five legacy test case IDs, their Covers and their Data are kept in order and character for character; TC-E5-009-01 covers legacy AC1, which the plan places in RWB-ITG-E5009-ITG, so it is not carried here. The legacy table carries no level column, so a case that exercises the whole step maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The fakes and the stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000609`, pack `PACK-2026-000609` of three documents, firm `LF-2026-0009`, instruction `INS-2026-0009`, instruction on 2026-12-08 and due on 2026-12-10 — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the 2 working days, the working-day calendar, the instruction types and the message texts are values and reference rows with a version; no day count, list value, state name or date appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the step carries references, dates, codes and a rule version only, and the test data is synthetic. The firm is a reference and its users are portal identities of S9, never carried here.
- The panel and the instruction stay with rwb-partner: no `partner` row, no `partner_instruction` row and no instruction status is written here (BR3; DP-01).
- The pack stays with rwb-document: the instruction carries document references only, and no body, storage reference or checklist row is copied into `rwb_litigation` (BR4).
- The case stays with rwb-case: no `recovery_case` row, no route state, no case-stage timer row and no task row is written here, and the move is answered with the rule and its version (BR5).
- ACE data only through the owner's contract: no component of this story reads a `v_ace_*` view or an ACE table, and the service holds no `v_ace_*` grant (DP-05).
- No read of another service's tables and no cross-schema join: `partner`, `partner_instruction`, `recovery_case`, `timer`, `document`, `rule_row` and `decision_log_entry` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second instruction.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing, consumes nothing and registers no job, and the catalogue of the service is not widened (12.3, 12.4, 12.6).
- The two screens are read only; SCR-19 posts nothing and its actions are the operations of the sibling stories.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal, which this story does by composing the instruction and the pack, requesting it on the partner contract, starting the clock and answering the case move (FSD S4 requirements served); the legacy story master carries no requirement ID (GAP-2784; ASM-4618) | FEAT-LIT-09 | 08 Litigate and enforce | R-LIT-24, R-LIT-26, R-LIT-28 | TC-E5-009-02, TC-E5-009-03 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-009 | The three legacy criteria this slice owns word for word, the three rules, the two screens, the messages and the five test cases; the `partner`, `partner_instruction`, `timer` and `recovery_case` writes of the legacy data table are retired to their owners |
| RWB-S4-E5009-CON | H: the instruction element, the pack reference set, the clock, the rights, the errors and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 and SCR-20 |
| rwb-partner (P9), rwb-document (P5), rwb-case (P3) and rwb-decision (P7) contracts | C in fact and not in the metadata row: the firm and the instruction, the pack, the case read and answer, and the rule package, all faked (GAP-2781, GAP-2782, GAP-2785) |
| RWB-S4-E5009-APP and RWB-S4-E5009-CON siblings of this key, and RWB-ITG-E5009-ITG | The application and contract halves of the same legacy key, and the integration slice that owns legacy AC1 |
| FEAT-LIT-08, FEAT-LIT-09, SCR-19, SCR-20 | The predecessor feature, this feature and the two screens of the legacy story |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-02, DP-14 | The owner's schema, the per-service login and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the event platform this story adds no producer or consumer to, Temporal with durable timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-partner, rwb-document and rwb-case, with the `-ITG` copies of the legacy cases |

### 19. Out of scope

- The published shape of the instruction and of the pack reference set, the rights, the errors and the fakes: RWB-S4-E5009-CON.
- The panel, the panel status, the conflict result, the `partner` and `partner_instruction` rows, the instruction status and the portal transport: rwb-partner (S9) and the partner-management stories (FEAT-PRM-01 to FEAT-PRM-04) (GAP-2781; ASM-4615).
- The pack items, their index, the checklist and the document bodies: rwb-document (P5) and the pack stories RWB-S4-E5004-APP and RWB-S4-E5005-APP.
- The case of record, its route state `FIRM_INSTRUCTED` or `FIRM_BREACHED_SLA`, the parent `CaseWorkflow`, the case-stage timer and the task: rwb-case (P3) and its slice of this legacy key (GAP-2782; ASM-4616).
- The selection of the firm out of the panel under R-LIT-23 and the escalation under R-LIT-25: FEAT-LIT-08 and the firm-selection story of this service.
- The re-selection after a breach under R-LIT-29 and the decline under R-LIT-27: the firm-selection story, which R-LIT-28 hands to.
- The notification of the partner manager and of the firm on a breach: rwb-comms (P6).
- The filing confirmation and the court case number of the firm: FEAT-LIT-10 and the filing story of this service.
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-24, R-LIT-26 and R-LIT-28: rwb-decision (P7), with the embedded runtime as a service-template capability (GAP-2785; ASM-4568).
- The working-day calendar and the instruction types as values: the business owner of S4 and the reference-data owner; the story reads the rows and carries the placeholder (GAP-2783; ASM-4617).
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19 and SCR-20: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence, including legacy AC1: the wave 3 harness and RWB-ITG-E5009-ITG.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
