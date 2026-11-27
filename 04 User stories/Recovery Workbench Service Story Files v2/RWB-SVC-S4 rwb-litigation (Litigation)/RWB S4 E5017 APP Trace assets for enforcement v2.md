# RWB-S4-E5017-APP Trace assets for enforcement

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S4-R |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5017-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-S4-E5017-APP-23) |
| Size | Set by the squad at refinement |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-017 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as the enforcement-trace step of `LitigationWorkflow` on task queue `rwb-litigation`; the ACE asset and data-product read becomes a consumed contract of rwb-source-data (DP-05), the bureau, registry and insurer search a consumed contract of rwb-integration (S4 has no adapter and no external dependency row), and the trace plan a consumed contract of rwb-agent; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the stage moves (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19); the trace result has no table or column of its own and the enforcement decision itself belongs to the writ, deferral and petition stories, so both are declared as the working read of the assumptions (GAP-2815, GAP-2816, GAP-2817, GAP-2818; ASM-4659 to ASM-4664). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 16 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **enforcement owner (RW-ENFORCE)** reading an unattended step, I want **the Workbench to trace the debtor's assets across the bureau, the bank's own data, the registries and the insurers as soon as a judgment is recorded, to record the trace with the rule version in force, and to present the traced assets as the enforcement decision is opened**, so that **enforcement starts on evidence the bank can act on instead of a manual search, and every asset the bank may seize is on the file before the writ is applied for**.

This is the application slice of legacy RWB-E5-017. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the trace step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-50 and R-LIT-52 of the LITIGATION route set — judgment recorded opens enforcement and traces the four sources, one or more traced assets present the enforcement decision — with the package version in force;
- the stage states `ENFORCEMENT_OPENED`, `ASSET_TRACE` and `ENFORCEMENT_DECISION`, reported to the case of record as a case move;
- the read of the ACE asset view `v_ace_npa_asset` and of the batch status behind VR-S4-017-1 through rwb-source-data's contract (DP-05), and the bureau, registry and insurer search through rwb-integration's contract;
- the trace plan of rwb-agent (P10), which decides which sources to search and in what order, read and never computed here;
- the local decision record of every trace outcome, written through RWB-PLT-E1027-CON before the stage moves (DP-03);
- `POST /cases/{caseId}/legal-actions` (API-S4-002) and `GET /legal-actions/{legalActionId}` (API-S4-003) on base `/api/recovery/litigation/v1` under capability area "Litigation" with the rights C and R (DP-13);
- SCR-19 Litigation workspace and SCR-20 Enforcement workspace as this service's answer, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the trace request and answer elements, the error set and the fakes, which are RWB-S4-E5017-CON; the ACE views, their ingestion and the data product, which are rwb-source-data (P1); the NCB, registry and insurer adapters, which are rwb-integration (P2); the trace plan and the model, which are rwb-agent (P10); the case of record and its route state, which are rwb-case (P3); the LITIGATION package and the rule rows, which are rwb-decision (P7); the enforcement decision, the writ, the deferral and the bankruptcy petition, which are the sibling stories of this service; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E5-017 gave the Workbench one unattended step that searched the bureau, registries and insurers, reported what it found, and wrote the result to the decision log with the rule version. The FSD keeps the objective — "Searches the bureau, registries and insurers for assets to enforce against, and reports what it finds" (FSD S4 A2.17.1) — and the same module measure as the rest of S4: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today. It serves **REQ-S4-007**: "Enforcement after judgment has one named owner from judgment to the end of enforcement" (FSD S4 Requirements served).

What D-RCV-60 changes is where the four parts of the trace live. In the monolith one process read the `recovery` schema, held the `v_ace_npa_asset` view, called the bureau and wrote the `decision_log_entry` row in one transaction. In the target:

- **the asset and data-product read is rwb-source-data's.** `v_ace_npa_asset` and `v_ace_batch_status` are ACE views; the architecture makes the views read only by rwb-source-data, and DP-05 lets this service either read its own ACE view or read the owner's contract. No view is granted to S4 and no ACE table is named in its ownership rows, so the read is a consumed contract with a fake (GAP-2815; ASM-4659). VR-S4-017-1 — a data product stale after a late or failed ACE batch — is answered by that owner and reported with MSG-P1-001; the trace does not judge the ACE batch itself.
- **the external search is rwb-integration's.** "NCB, registries, insurers" are outside systems, and S4 owns no adapter, no file and no external dependency row. The search travels on rwb-integration's contract, one row per source, each faked (GAP-2816; ASM-4660). FEAT-AGT-01, the legacy prerequisite, is the rwb-agent trace plan (P10): it says which sources to search, and it is read, never computed here.
- **the case of record stays with rwb-case (P3).** `recovery_case` and its route state are P3's; `ASSET_TRACE` and `ENFORCEMENT_DECISION` are answered, never written here.
- **the litigation stage stays with rwb-litigation (S4).** The stage machine, the legal action and the decision record are this service's, which is what legacy AC2 and AC3 assert.
- **the trace result has no home of its own.** Neither `legal_action` nor `hearing` carries an asset reference, a trace date or a source, no table of this service holds the traced assets, and the legacy data table lists the view and the decision log but no result row (GAP-2818; ASM-4663). The traced assets are therefore recorded in the decision record and answered to the screen as a read model; nothing is invented as a column.
- **the decision is recorded first**, in the same transaction as the stage change, which is what legacy AC1 asked for and what legacy AC4 tested.

The boundary with the sibling stories is fixed by the rules. R-LIT-50 opens enforcement and traces; R-LIT-52 presents the enforcement decision when assets are found; R-LIT-53 presents it with a deferral recommendation when the trace returns nothing, and R-LIT-54, R-LIT-55 and R-LIT-58 act on it. This story stops at `ENFORCEMENT_DECISION` and presents; it does not approve a writ, record a deferral or file a petition (GAP-2818; ASM-4663).

The metric of the feature is unchanged, so no business value moves: the 10 and 5 working-day task timers, the four sources, the state names and the message texts are values in force in reference data and in the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S4-E5017-CON is published: the two operations, the trace request and answer elements, the action type vocabulary, the consumed rows with their placeholders, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data contract is published with its fake, so the ACE asset rows and the current batch status can be read on Day 1. It is not in this story's contract-dependency row, which is None, and the absence is recorded as GAP-2815 with ASM-4659.
- The rwb-integration search contract and the rwb-agent trace plan are available for their fakes. No source names a published operation for either, so their names are Not specified in the source documents (GAP-2816; ASM-4660).
- The rwb-case case-move answer is available for its fake: the parent `CaseWorkflow` applies the move and this service writes no case row (GAP-2818; ASM-4663).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the stage change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 and SCR-20 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` exists in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-014 and the standard record columns of TSD S4 T3.0; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version with R-LIT-50 and R-LIT-52 in it. The package, its rule rows and the 10 and 5 working-day timers are authored, tested and approved in rwb-decision and loaded here on `RulePackageInForce`; this story declares none of them.
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no grant on a `v_ace_*` view, so a statement outside the schema is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5017-CON when its tests pass.

### 4. Flow

1. The judgment is recorded on the case by the sibling judgment story under R-LIT-44, and rwb-case answers the state `JUDGMENT_RECORDED`. That answer starts the trace step of `LitigationWorkflow` on task queue `rwb-litigation`; no source names a publisher, an event or a Schedule, so the trigger is a workflow signal (GAP-2817; ASM-4661).
2. The step reads the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): the action type, `status`, `lawsuit_no`, `black_case_no`, `court_name`, `judgment_date` and `judgment_amount`.
3. The step reads the trace plan of rwb-agent (P10) on its contract: which of the four sources to search and in what order. The plan is read, never computed or re-worded here (GAP-2816; ASM-4660).
4. The internal-data leg reads the ACE asset rows of the debtor and the batch status of that data product through rwb-source-data's contract (DP-05). VR-S4-017-1 is checked on the answer: a stale product is reported with MSG-P1-001 and recorded, and the internal leg is held until a current batch is answered (GAP-2815; ASM-4664).
5. The external legs read the bureau, registry and insurer answers through rwb-integration's contract, one call per source, each one hop with a 2 s budget and a breaker (GAP-2816; ASM-4660).
6. `AssetTraceEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates R-LIT-50: a judgment recorded against the debtor opens enforcement, traces NCB, internal data, registries and insurers, and moves the stage to `ASSET_TRACE` with a durable 10 working-day timer.
7. `TraceDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the sources searched, the answer of each source, the traced assets and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `CaseMoveAnswer` answers rwb-case with the move `ENFORCEMENT_OPENED` and then `ASSET_TRACE`, with the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither (GAP-2818; ASM-4663).
9. When R-LIT-52 fires — one or more assets traced — the traced assets are presented with the enforcement decision to the enforcement owner and the stage moves to `ENFORCEMENT_DECISION`: the asset reference, the asset key, the asset code, the source, the segment and the book value of each asset, with the rule ID and its version. Nothing is decided here.
10. When the trace returns no asset, R-LIT-53's deferral recommendation and the enforcement decision belong to the sibling deferral story; this story records the empty result and leaves the stage with its timer running (GAP-2818; ASM-4663).
11. A repeated trigger or a repeated source answer with the same case, action and trace reference writes nothing, sends no second case-move answer and counts the repeat.
12. SCR-19 and SCR-20 read the action, the stage outcome and the traced assets from this service through the gateway-bff composite route, read only, next to the case of rwb-case and the enforcement steps of the sibling stories (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the stage keeps its state, no case-move answer is sent and no trace answer is presented | MSG-P7-003 | AC4, TC-E5-017-04, TC-E5-017-06 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC5, TC-E5-017-05, TC-E5-017-07 |
| X3 | The legal action does not exist, is outside the scope, or is already `CLOSED` or `WITHDRAWN` | 404 or 409 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC2, AC3, AC9 |
| X4 | The data product behind the ACE asset read is stale (VR-S4-017-1) | The product and its date are reported, the internal leg is held and the condition is recorded; the external legs are still attempted | MSG-P1-001 | AC1 |
| X5 | A source does not answer inside 2 s, its breaker is open, or its fake answers no answer | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2, AC7, AC8 |
| X6 | The trace returns no asset | The empty result is recorded and the stage keeps its timer; R-LIT-53's deferral recommendation and the enforcement decision are the sibling deferral story's | None | AC3 |
| X7 | The same trigger, source answer or trace reference arrives twice | One write, one case-move answer and one decision record; the repeat is counted | None | AC1 |
| X8 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X9 | A component, a statement or a test reads a `v_ace_*` view, a `recovery_case` row, a `rule_row` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC6, TC-E5-017-08, Section 17, BR5, BR8 |

X1 to X3 and X5 are the exception paths of RWB-E5-017 and of the FSD S4 A2.17 exception table carried onto the split, X4 is VR-S4-017-1, X6 is the R-LIT-53 boundary, X7 and X8 are the paths the target call types add, and X9 is the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5017-CON and the five consumed fakes, on the tables of its own schema, and needs no live rwb-source-data, rwb-integration, rwb-agent, rwb-case or rwb-decision |
| Negotiable | The activity names, the decision code per rule, the search order and the shape of the trace answer are this story's choice; the rules, the messages, the screens, the two operations and the state names are fixed |
| Valuable | Every judgment opens enforcement with one unattended trace of the four sources, one decision record and the traced assets on the enforcement workspace |
| Estimable | One workflow branch, one evaluator, one record write, four consumed clients and one case-move answer |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and source answers through the contract fakes, plus the component cases of the access answer and the stale batch, and the NFR case of the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Trace assets for enforcement

  Background:
    Given case "RC-2026-001717" carries the civil-case legal action "LA-2026-001717" with the judgment recorded
    Given the LITIGATION rule package is in force at its version and carries R-LIT-50 and R-LIT-52
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Trace assets for enforcement (legacy RWB-E5-017 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-source-data contract mock returns the ACE asset rows and the current batch status for case "RC-2026-001717"
    Given the rwb-integration contract mock returns the bureau, registry and insurer answers for case "RC-2026-001717"
    Given the rwb-agent contract mock returns the trace plan with its sources for case "RC-2026-001717"
    Given the rwb-case contract mock returns the case state "JUDGMENT_RECORDED" for "RC-2026-001717"
    Given the rwb-decision contract mock returns R-LIT-50 and R-LIT-52 at their version in force
    When its trigger arrives
    Then searches the bureau, registries and insurers for assets to enforce against, and reports what it finds
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-LIT-50 (legacy RWB-E5-017 AC2)
    Given a case in state JUDGMENT_RECORDED
    Given the rwb-source-data contract mock returns the internal asset rows and the current batch status for case "RC-2026-001717"
    Given the rwb-integration contract mock returns the NCB, registry and insurer answers for case "RC-2026-001717"
    Given the rwb-case contract mock returns the case state "JUDGMENT_RECORDED" for "RC-2026-001717"
    When enforcement opened
    Then trace assets across NCB, internal data, registries and insurers
    Then the case moves to ASSET_TRACE

  Scenario: AC3 Rule R-LIT-52 (legacy RWB-E5-017 AC3)
    Given a case in state ASSET_TRACE
    Given the rwb-source-data contract mock returns the traced asset rows of case "RC-2026-001717"
    Given the rwb-integration contract mock returns the traced registry and insurer answers of case "RC-2026-001717"
    Given the rwb-case contract mock returns the case state "ASSET_TRACE" for "RC-2026-001717"
    When assets found
    Then present the enforcement decision with the traced assets
    Then the case moves to ENFORCEMENT_DECISION

  Scenario: AC4 Not recorded (legacy RWB-E5-017 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Role without the Litigation right (exception X2) (new, D-RCV-60)
    Given the caller holds a role without the Litigation right of the operation
    When the caller reads or opens the legal action
    Then the request is refused with 403 before any read or write
    Then nothing changes, no decision record is written and the user sees MSG-P4-002

  Scenario: AC6 Boundary of the ACE read (exception X9) (new, D-RCV-60)
    Given a component, a statement or a test reads a v_ace_* view, a recovery_case row, a rule_row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement and the build fails
    Then nothing is released

  Scenario: AC7 Activity retry and timeout (exception X5) (new, D-RCV-60)
    Given a source does not answer inside 2 s
    When the step runs
    Then the step waits and retries on the workflow's own schedule
    Then nothing is written and no move is answered

  Scenario: AC8 Consumed call fails or does not answer (exception X5) (new, D-RCV-60)
    Given the breaker of a source is open or its fake answers no answer
    When the step runs
    Then nothing is written and no move is answered
    Then the caller sees 503 with the platform error envelope

  Scenario: AC9 Status change the model does not allow (exception X3) (new, D-RCV-60)
    Given the legal action is already CLOSED or WITHDRAWN
    When the step runs
    Then the request is refused with 404 or 409
    Then nothing is written

  Scenario: AC10 Rules BR1 to BR9 of section 8 (no legacy origin) (new, D-RCV-60)
    Given the step runs under the rwb-litigation service identity for a case
    When the step runs
    Then the rules BR1 to BR9 of section 8 hold as written there
    Then each rule is covered by its test case of section 16 (TC-E5-017-09 to TC-E5-017-17)

  Scenario: AC11 Error answers of the provided operations (401, 403, 404; no legacy origin) (new, D-RCV-60)
    Given a caller calls a provided operation of the litigation service
    When the caller has no valid authentication, lacks the Litigation right or names a legal action that does not exist
    Then the request is refused with 401, 403 or 404 respectively
    Then nothing is written and no decision record is written

  Scenario: AC12 Replay of a write with the same idempotency key (BR8; no legacy origin) (new, D-RCV-60)
    Given a write with an Idempotency-Key was already applied for a case
    When the same write is replayed with the same Idempotency-Key
    Then nothing is written again and no move is answered again
    Then the repeat is counted and the first result stands
```

The first four criteria are the legacy criteria of RWB-E5-017 word for word, with their origin tag added and, in AC1 and AC4, the decision log wording replaced by decision record wording: the repetition of `Then`, the lower-case opening of the third `Then`, the legacy wording of `its trigger arrives`, `enforcement opened`, `assets found` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 to AC3 carry the `Given the <service> contract mock returns <x>` lines above, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in five places in the target: rwb-source-data answers the ACE assets and the batch status, rwb-integration answers the bureau, registries and insurers, rwb-agent answers the trace plan, rwb-case answers and applies the case move, and this story evaluates the rules, writes the decision record with the rule version and presents the traced assets. AC5 and AC6 are added by this story for exceptions X2 and X9, and AC7 to AC9 for exceptions X5 and X3; they have no legacy origin and use the same Given, When and Then form.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-50 (BR10) | Litigation | D7 | JUDGMENT_RECORDED | ENFORCEMENT_OPENED | a judgment is recorded against the debtor | Trace assets across NCB, internal data, registries and insurers | ASSET_TRACE | Workbench | NCB, registries, insurers | 10 working days |
| R-LIT-52 (BR11) | Litigation | D7 | ASSET_TRACE | ASSETS_FOUND | one or more assets traced | Present the enforcement decision with the traced assets | ENFORCEMENT_DECISION | Enforcement owner | Workbench | 5 working days |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character, with the BR IDs BR10 and BR11 added to the rule cell. Their owner column is a role of the business and not a service: "Workbench" is the unattended step, and "Enforcement owner" is the person who receives the enforcement decision, not a writer of the stage. The systems column names the external sources, which are reached only through rwb-integration's contract.

| ID | Rule | Source |
|---|---|---|
| BR1 | The trace step, the stage states `ENFORCEMENT_OPENED`, `ASSET_TRACE` and `ENFORCEMENT_DECISION`, and the legal action are this service's; the stage is a state of the LITIGATION machine on `LitigationWorkflow` | FSD S4 A2.17; TSD S4 T4; Ownership Map (legal_action and hearing owner S4) |
| BR2 | The decision is recorded before the stage acts, with the rule ID and the package version in force; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-017 AC1 and AC4 |
| BR3 | ACE data is read only through rwb-source-data's contract: no `v_ace_*` view and no ACE table is queried by this service, and a stale data product is reported with MSG-P1-001 | DP-05; VR-S4-017-1; GAP-2815 |
| BR4 | The external search is rwb-integration's: NCB, registries and insurers are reached through its contract, one hop per source, and no adapter, file or external dependency is built here | FSD S4 A2.17.2 (integration points NCB, Model gateway); GAP-2816 |
| BR5 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); GAP-2818 |
| BR6 | The trace result is recorded in the decision record and presented as a read model; no table, no column and no migration is added for an asset, a trace date or a source | TSD S4 T3.1 (no such column); GAP-2818; GAP-2824 (any later asset reference is an additive change) |
| BR7 | The step runs unattended under the rwb-litigation service identity and is subject to the same role checks as a person; the enforcement owner reads the traced assets and the enforcement decision | FSD S4 A2.17.3.3 (primary "None; runs unattended", also-user Enforcement owner); TSD S4 T6.2; GAP-2817 |
| BR8 | The same trigger, source answer or trace reference twice writes once, sends one case-move answer and one decision record, and counts the repeat | TSD S4 T-A.2 (`Idempotency-Key`); legacy AC1 |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case references, action references, asset references, codes, dates and amounts | Template and Rules v1 §R7.2 (s17); TSD S4 T6.2 |
| BR10 | R-LIT-50: the judgment opens enforcement, the trace of the four sources runs once and the stage moves to ASSET_TRACE, with the record written before the move | Business Rules and Routing Logic v4 R-LIT-50; AC2 |
| BR11 | R-LIT-52: one or more traced assets are presented with the enforcement decision and the stage moves to ENFORCEMENT_DECISION, with the record written before the move | Business Rules and Routing Logic v4 R-LIT-52; AC3 |

**Where each rule lives in the target.** R-LIT-50 is the opening and tracing step: the judgment answer of rwb-case starts it, the plan of rwb-agent orders the four sources, rwb-source-data answers the internal assets and rwb-integration the external ones, the record is written, and the stage and the case move go to `ASSET_TRACE`. R-LIT-52 is the presentation step: one or more traced assets are presented with the enforcement decision, the record is written and the stage and the case move go to `ENFORCEMENT_DECISION`. R-LIT-53 (no asset, deferral recommendation), R-LIT-54 (writ and seizure), R-LIT-55 (deferral) and R-LIT-58 (petition) are the sibling stories' and are named here only as the boundary of this step. VR-S4-017-1 is carried in section 14 and is the only validation rule of the key.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR5). What this story owns is the stage of `LitigationWorkflow` and the state of the step.

| From (stage of `LitigationWorkflow`) | Event | Condition | To |
|---|---|---|---|
| `JUDGMENT_RECORDED` | ENFORCEMENT_OPENED under R-LIT-50 | A judgment is recorded against the debtor, and the trace of the four sources completes | `ASSET_TRACE`, with the case-move answer `ENFORCEMENT_OPENED` then `ASSET_TRACE` and a durable 10 working-day timer |
| `ASSET_TRACE` | ASSETS_FOUND under R-LIT-52 | One or more assets are traced | `ENFORCEMENT_DECISION`, with the case-move answer `ENFORCEMENT_DECISION` and the traced assets presented |
| `ASSET_TRACE` | No asset traced | X6: R-LIT-53 belongs to the sibling deferral story | Unchanged, timer running, empty result recorded |
| Any of the two | Any event | X3: the action is `CLOSED` or `WITHDRAWN`, or the stage is not the one the rule expects | Unchanged, refused with 409 |
| Any of the two | A stale data product | X4: VR-S4-017-1 | Unchanged until a current batch is answered, MSG-P1-001 shown |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The judgment answer arrives for a case at `JUDGMENT_RECORDED` | The package in force is loaded | Evaluating |
| Evaluating | R-LIT-50 fires and the four sources answer | The decision record is written | Applying |
| Applying | The stage moves and the case-move answer leaves the service | The transaction commits | Waiting for the next signal |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Applying | A source does not answer inside 2 s | X5 | Waiting, retried on the workflow's own schedule |

The legal action keeps its status through this step: `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED, WITHDRAWN (TSD S4 T3.2), the action of the judgment stays at the status the judgment story left, and the move to `ENFORCING` and the writ belong to R-LIT-54 and the sibling writ story. This story writes no status value of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-ENFORCE, enforcement owner | Litigation CRU in the TSD S4 T6.1 matrix: the also-user of the FSD and the reader of the traced assets and the enforcement decision; records nothing on the trace path |
| RW-LITOFF, litigation officer | Litigation CRUA: opens the legal action where it has to be opened, reads the action, and works the enforcement workspace |
| RW-HEADLIT, Head of Litigation | Litigation RA: read, and the escalation role of the enforcement route |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Litigation RA: read |
| RW-LEGAL, legal counsel | Litigation RA: reads the action, the trace and the outcome; records none of them |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU: reads the enforcement state and records its own court entries through the partner gateway; records no trace |
| SY-CASEWF, SY-RULES, SY-AGENT | Litigation R or U as the TSD S4 T6.1 matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step unattended, evaluates the rules, reads the consumed contracts, writes the decision record and answers the case move; it holds no grant on another schema and no grant on a `v_ace_*` view |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The FSD makes the step's primary role "None; runs unattended" with the enforcement owner as also-user, while the legacy permission table gives `C` to RW-LITOFF and RW-ENFORCE and `R` to thirty roles. Both statements hold: the unattended step runs under the service identity with no person right, the enforcement owner receives the result, and the `C` row is the right of the operation that opens the legal action, which the sibling stories and this story's POST declare (GAP-2817; ASM-4662). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, and the guard is a service-template capability, so the check is stated here and not built here: each operation calls rwb-access to authorise the capability area and right of this table before any read or write.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the record and the case move |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the case-move answer |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`: the judgment action of this step is `CIVIL_CASE` |
| DF-LEG-005, DF-LEG-006, DF-LEG-008 | legal_action (S4, `rwb_litigation`) | lawsuit_no, black_case_no, court_name | Read, as the court facts the trace is recorded against |
| DF-LEG-009, DF-LEG-011, DF-LEG-012 | legal_action (S4, `rwb_litigation`) | claim_amount, judgment_date, judgment_amount | Read, as the judgment facts that open enforcement |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Read, and **not written on this path**: the action keeps the status the judgment story left |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by`, `is_active` | Not written by this story: no column of the action changes |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset (P1, read through the owner's contract) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Read through rwb-source-data's contract only; never queried as a view and never stored here (BR3) |
| No field ID given | v_ace_batch_status (P1, read through the owner's contract) | the data product and its batch date | Read for VR-S4-017-1 and reported with MSG-P1-001; the field names are Not specified in the source documents (GAP-2815; ASM-4659) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status and 18 more | Not read as a table and not written: the case and its route state come back on the case-move answer (BR5) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the stage changes (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rule package in force and never as a table |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1, the legacy story Data table and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `legal_action` arrives with the DB story of this service, `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03), and the view row of the legacy data table is read through its owner (GAP-2815; ASM-4659). The test fixtures are synthetic: case `RC-2026-001717`, action `LA-2026-001717`, four source answers and one traced asset.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind two operations whose shapes are declared by RWB-S4-E5017-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its court facts, its judgment facts and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The step reads the action on the GET. The POST is the operation through which the civil-case action of the judgment, or the enforcement action of the writ story, is opened by the sibling stories, and this story declares it and does not create an action on the trace path: the trace hangs on the action the judgment story recorded. Errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed, withdrawn or wrong-stage action, 422 with MSG-GEN-001 for a missing or invalid field, and 503 when the decision library, a consumed contract or the rule package does not answer. `PATCH /legal-actions/{legalActionId}` (API-S4-004) records a filing, a judgment or an enforcement step and belongs to the sibling stories; this story patches no column.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The ACE asset and data-product read (operation name Not specified in the source documents (GAP-2815; ASM-4659)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset rows of `v_ace_npa_asset` and the batch status of that data product for VR-S4-017-1; the view and its ingestion are P1's; faked |
| The bureau, registry and insurer search (operation name Not specified in the source documents (GAP-2816; ASM-4660)) | `/api/recovery/integration/v1` | P2 rwb-integration | The NCB, registry and insurer answers for the debtor, one call per source; the adapters are P2's; faked |
| The trace plan (operation name Not specified in the source documents (GAP-2816; ASM-4660)) | `/api/recovery/agent/v1` | P10 rwb-agent | The sources to search and their order, from FEAT-AGT-01; read, never computed here; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2818; ASM-4663)) | rwb-case (P3) | P3 rwb-case | The move `ENFORCEMENT_OPENED`, `ASSET_TRACE` or `ENFORCEMENT_DECISION` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule package in force (operation name Not specified in the source documents) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with R-LIT-50 and R-LIT-52, and the approval answers the sibling stories use; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All five are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2815 and GAP-2816 with ASM-4659 and ASM-4660.

#### 12.3 Events published

None. The service's topic is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its ownership rows list no event of this service (context pack, ownership rows). DP-09 is not in this story's pattern set: the step writes no outbox row, its outputs are the local decision record of DP-03 and the case-move answer. A traced asset on the case is not an event, and a writ filed by the firm is S9's fact on S9's topic.

#### 12.4 Events consumed

None. The ownership rows of this service list no consumed event either, so the judgment answer arrives on the rwb-case contract of 12.2 and the source answers arrive on their owners' contracts (GAP-2817; ASM-4661). This story holds no consumer group, no subscription and no inbox of its own, and a build that adds a consumer to `rwb.litigation.events.v1` or a subscription to another topic fails the absence test of the CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` | Input: the case, the route R4, the legal action and the rule package in force; signals: the judgment answer, the source answers and the rule package in force; outcome: the stage move for the parent; workflow ID and start rule: Not specified in the source documents (CG-ALL-9426) |
| `traceAssets` | Activity, the opening and tracing step of this story | `rwb-litigation` | The case, the legal action and the trace plan in; the source answers, the rule ID with its package version, the traced assets and the case move out |
| `presentEnforcementDecision` | Activity, the presentation step of this story | `rwb-litigation` | The traced assets in; the enforcement decision view, the decision record and the case move out, in one transaction |

The trace plan is not an activity of this service: it is an answer of rwb-agent (P10) read on the owner's contract, and no model call is made here. The activity names are target design choices and are fixed by no source document; the trigger of the step is read as the judgment answer, because the legacy story says the trigger arrives while R-LIT-50 names a recorded judgment (GAP-2817; ASM-4661). No cross-service call is made inside a workflow: each is an activity of the queue below.

#### 12.6 Schedules

None. The step runs from the judgment answer and the source answers. The 10 and 5 working-day task timers of R-LIT-50 and R-LIT-52 are durable timers of the workflow, not a Schedule; this story registers no Temporal Schedule, no Quartz row and no shared job table, and no Job of the batch catalogue is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read by this story and not written: the action keeps the status the judgment story left (BR6) |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated trigger or source answer and the answer it holds |

Not owned and never read as a table: `v_ace_npa_asset` and `v_ace_batch_status` (P1, read through the owner's contract), `recovery_case` (P3), `rule_row` and `decision_log_entry` (P7), `hearing` (S4, the sibling stories'), `document` (P5). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01).
Reference data read by this story: lists or parameters Not specified in the source documents (DOR-RWB-S4-E5017-APP-20); reference-data contract (DP-06, DP-07) Not specified in the source documents (DOR-RWB-S4-E5017-APP-20).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data asset fake | The ACE asset rows of case `RC-2026-001717` and a current batch status; a stale product with its date | AC1, AC2, AC3, X4 |
| rwb-integration search fake | The NCB, registry and insurer answers of case `RC-2026-001717`; an empty answer per source and an answer beyond 2 s | AC1, AC2, AC3, X5 |
| rwb-agent plan fake | The trace plan with its four sources and their order for case `RC-2026-001717` | AC1, AC2 |
| rwb-case case-move fake | The case state `JUDGMENT_RECORDED` and `ASSET_TRACE` of case `RC-2026-001717`; the moves `ENFORCEMENT_OPENED`, `ASSET_TRACE` and `ENFORCEMENT_DECISION` accepted, and a move refused because the case is not in the state the rule expects | AC1, AC2, AC3, X3 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-50 and R-LIT-52 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 answer for case `RC-2026-001717`, with the legal action facts and the traced assets of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The consumed rows carry the placeholder of 12.2 until their owners publish an operation name (GAP-2815, GAP-2816; ASM-4659, ASM-4660).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The create and read of the legal action on `/api/recovery/litigation/v1`; the ACE asset and batch read, the external search, the trace plan, the case-move answer and the rule package; one hop, 2 s each |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 2 activities | `LitigationWorkflow` with `traceAssets` and `presentEnforcementDecision` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `enforcement`, Java package `th.co.scb.ace.workbench.recovery.litigation.enforcement`; front end `src/modules/recovery/litigation/TraceAssetsForEnforcement.tsx`, the fragment SCR-20 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the stage change commit together or not at all, and the record is written before the case move leaves the service. DP-05 is the asset and batch-status read: no view is granted to this service and the owner answers (GAP-2815; ASM-4659). DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-19 and SCR-20 reach this service, one hop through the gateway. DP-09, DP-16 and DP-20 are not in the pattern set of this key, which is why no event is declared, why the external search is a consumed contract of its owner rather than an adapter of this build, and why the trace plan is consumed from P10 rather than computed here (GAP-2816; ASM-4660).

**Dependencies the tables add and the plan does not hold.** The three H rows are the plan's. The five consumed contracts of 12.2 are class C dependencies in fact and are not in the metadata row, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2815 and GAP-2816 with ASM-4659 and ASM-4660.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` trace branch | Workflow | The step that waits for the judgment answer, loads the package in force and reports the stage move to the parent |
| `traceAssets` | Activity | Reads the action, the plan and the four source answers, evaluates R-LIT-50, writes the record and answers the move to `ASSET_TRACE` |
| `presentEnforcementDecision` | Activity | Reads the traced assets, evaluates R-LIT-52, writes the record and answers the move to `ENFORCEMENT_DECISION` |
| `AssetTraceEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the state names of the LITIGATION machine |
| `TraceDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `AceAssetReader` | Client | The asset rows and the batch status of P1, one hop, 2 s, breaker, no retry of its own (DP-05) |
| `ExternalTraceClient` | Client | The NCB, registry and insurer answers of P2, one call per source, one hop each (BR4) |
| `TracePlanClient` | Client | The trace plan of P10, one hop, 2 s |
| `CaseMoveAnswer` | Signal reporter | Answers rwb-case with the move, the rule and the version; it reports, it never changes a case row |
| `LegalActionController` | Controller | The two operations, the capability area and right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `TraceAssetsForEnforcement` | React component | Shows the traced assets and the enforcement decision on SCR-20, read only, with the stale, empty, refused and not-recorded states |

**Database and migrations.** No Flyway file. `legal_action` arrives with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for an asset, a trace date, a source or an enforcement decision: the trace lives in the decision record and the answer, and the enforcement decision moves nothing (BR6; GAP-2818; ASM-4663).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the 10 and 5 working-day timers are values of the package, not of this build.
- The list of sources and their order are the trace plan's, answered by rwb-agent; no source name is a constant of this build.
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The trace branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the judgment answer as its trigger (ASM-4661).
2. `TracePlanClient`, `AceAssetReader` and `ExternalTraceClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, AC2, X5).
3. `AssetTraceEvaluator` over the LITIGATION package, with R-LIT-50 and R-LIT-52, the four sources and the no-fire path (AC2, AC3, X6).
4. `TraceDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. The stale product path of VR-S4-017-1 and MSG-P1-001 (AC1, X4).
6. `CaseMoveAnswer` and the parent signal, with the three moves (AC2, AC3).
7. `LegalActionController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, X2, X3).
8. `TraceAssetsForEnforcement` and SCR-20 through the composite route fake (AC1, AC3).
9. The boundary test: no statement outside `rwb_litigation`, no `v_ace_*` view, no write to another service's schema (X9, BR3, BR5).

**Feature flag.** `rwb.litigation.trace-assets-v1`, read as a flag of the platform library; off means the step holds the judgment answer, searches no source and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic judgment in SIT, R-LIT-50 traces the four sources and records its decision, R-LIT-52 presents the traced assets and moves the stage to `ENFORCEMENT_DECISION`, a stale batch shows MSG-P1-001 and holds the internal leg, a repeated trigger writes once, a forced record failure changes nothing, no `v_ace_*` view and no row of another service's schema is read or written from this service, and SCR-19 and SCR-20 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription story of this service, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-P1-001 | VR-S4-017-1: the data product behind the ACE asset read is stale after a late or failed batch (X4) | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required field of a request is absent or invalid (X3 of the contract) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads the legal action or the trace (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the stage changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The six texts are the legacy wording of RWB-E5-017 section 14, the FSD S4 A2.17 message list and the FSD message for VR-S4-017-1, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names and `MSG-P1-001` with the product and its date. A downstream that does not answer (X5) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No new screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-19 Litigation workspace | Judgment | The judgment date and amount of the sibling judgment story, read only, and the action at the status it left |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9433) |
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-9433) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9433) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-9433) |
| SCR-20 Enforcement workspace | Requested | The enforcement opening of this step, the four sources searched, the rule and its version, and the case at `ASSET_TRACE` |
| SCR-20 Enforcement workspace | Traced | The traced assets of this step — asset reference, asset key, asset code, source, segment and book value — and the case at `ENFORCEMENT_DECISION` |
| SCR-20 Enforcement workspace | Nothing found | The empty result and the deferral recommendation of the sibling deferral story, read only |
| SCR-20 Enforcement workspace | Stale data | MSG-P1-001 with the product and its date, and the internal leg held |
| SCR-20 Enforcement workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-20 Enforcement workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-20 Enforcement workspace | Empty | Not specified in the source documents (CG-ALL-9434) |
| SCR-20 Enforcement workspace | Loading | Not specified in the source documents (CG-ALL-9434) |
| SCR-20 Enforcement workspace | Error | Not specified in the source documents (CG-ALL-9434) |
| SCR-20 Enforcement workspace | No access | Not specified in the source documents (CG-ALL-9434) |

The legacy screen table gives SCR-20 the states requested, seized, auctioned and closed, and SCR-19 the states pack, instructed, filed, hearing and judgment. The trace has no state of its own in that list: the traced assets are shown in the request the enforcement decision opens, and seized, auctioned and closed belong to the writ, auction and proceeds stories. The route merges this service's answer with rwb-case for the case and its route state, rwb-integration for the source answers and rwb-document for the enforcement pack; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-017-01 | AC1 | End to end | Trace assets for enforcement |
| TC-E5-017-02 | AC2 | End to end | Rule R-LIT-50 |
| TC-E5-017-03 | AC3 | End to end | Rule R-LIT-52 |
| TC-E5-017-04 | AC4 | Component | Not recorded |
| TC-E5-017-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-017-07 | Access | Component | A role without the Litigation right is refused with 403 and MSG-P4-002 and nothing is written (AC5) |
| TC-E5-017-08 | Boundary | Build | A statement that reads a v_ace_* view or another service's schema fails the build and nothing is released (AC6, X9) |
| TC-E5-017-09 | Rule | Component | BR1: the trace branch and its stage states run on LitigationWorkflow as this service's |
| TC-E5-017-10 | Rule | Component | BR2: the decision record is written with the rule ID and version before the stage moves |
| TC-E5-017-11 | Rule | Component | BR3: ACE data is read only through the rwb-source-data contract and a stale product shows MSG-P1-001 |
| TC-E5-017-12 | Rule | Component | BR4: NCB, registries and insurers are reached only through the rwb-integration contract, one hop per source |
| TC-E5-017-13 | Rule | Component | BR5: the case move is answered to rwb-case and no recovery_case row is written |
| TC-E5-017-14 | Rule | Component | BR6: the traced result is a read model with no new table, column or migration |
| TC-E5-017-15 | Rule | Component | BR7: the step runs under the rwb-litigation service identity and the enforcement owner reads the result |
| TC-E5-017-16 | Rule | Component | BR8: a repeated trigger, source answer or trace reference writes once, sends one move and counts the repeat |
| TC-E5-017-17 | Rule | Component | BR9: no person name, address, contact value or identity number enters the step, the record or a log |
| TC-E5-017-18 | Rule | Component | BR10: R-LIT-50 fires on ENFORCEMENT_OPENED and moves the stage to ASSET_TRACE (AC2) |
| TC-E5-017-19 | Rule | Component | BR11: R-LIT-52 fires on ASSETS_FOUND and moves the stage to ENFORCEMENT_DECISION (AC3) |
| TC-E5-017-06 | Principle 5 | NFR | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E5-017-26 | §12 operations, events and activities (contract) | Contract | Source, integration, agent, case and rule-package fakes of section 12.8 |
| TC-E5-017-27 | §12.7 tables (ASM-3438), boundary | Component | Boundary values of the tables of section 12.7 |
| TC-E5-017-20 | AC7 | Component | A source does not answer inside 2 s and the step retries on the workflow schedule with nothing written (X5) |
| TC-E5-017-21 | AC8 | Component | A consumed call fails or its breaker is open and the caller sees 503 with nothing written (X5) |
| TC-E5-017-22 | AC9 | Component | A legal action already CLOSED or WITHDRAWN is refused with 404 or 409 and nothing is written (X3) |
| TC-E5-017-23 | AC10 | Component | Rules BR1 to BR9 of section 8, each covered by its row TC-E5-017-09 to TC-E5-017-17 |
| TC-E5-017-24 | AC11 | Component | A call with no valid authentication, without the Litigation right or for an unknown legal action is refused with 401, 403 or 404 and nothing is written |
| TC-E5-017-25 | AC12 | Component | A replayed write with the same Idempotency-Key writes once, sends one move and counts the repeat (BR8) |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 to AC3) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The source, integration, agent, case and rule-package fakes of section 12.8 stand behind every case, and the fixture data — case `RC-2026-001717`, action `LA-2026-001717`, four source answers and one traced asset — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the 10 and 5 working-day timers, the four sources, the lists and the message texts are values and reference rows with a version; no list value, state name, timer or date appears in Java.
- No personal data in logs, workflow inputs, prompts or the fixture: the rows carry case references, action references, asset references, codes, dates and amounts only, and the test data is synthetic.
- ACE data only through its owner: no component of this story queries a `v_ace_*` view or an ACE table, and the asset and batch-status read is the P1 contract (DP-05, BR3).
- The external search stays with rwb-integration: no adapter, no endpoint, no credential and no file for NCB, the registries or the insurers is built here (BR4).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is answered with the rule and its version (BR5).
- No new table and no new column for the trace: the result is the decision record and the answer, and the boundary test fails a build that adds an asset, a trace date or a source column (BR6).
- The trace plan is the agent's: no model call is made here and no source order is computed here.
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second search of a source.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing (12.3, 12.4).
- SCR-19 and SCR-20 are read only; the trace is unattended and the enforcement decision is the sibling stories'.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement, which this story does by opening enforcement at the recorded judgment, tracing the four sources under one named owner and handing the traced assets to that owner (FSD S4 Requirements served) | FEAT-LIT-17 | 08 Litigate and enforce | R-LIT-50, R-LIT-52 | TC-E5-017-01, TC-E5-017-02, TC-E5-017-03 |

The legacy story master of RWB-E5-017 carries no requirement ID; the trace is the requirement the FSD S4 serves for the enforcement owner, which is the feature's own requirement.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-017 | The four legacy criteria word for word, the two rules, the two screens, the six messages and the six test cases; the view row of the legacy data table is read through P1 and no trace row is written here |
| RWB-S4-E5017-CON | H: the two operations, the trace request and answer elements, the error set and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 and SCR-20 |
| rwb-source-data (P1), rwb-integration (P2), rwb-agent (P10), rwb-case (P3) and rwb-decision (P7) contracts | C in fact and not in the metadata row: the ACE assets and batch status, the external search, the trace plan, the case move and the rule package, faked (GAP-2815, GAP-2816) |
| FEAT-LIT-17, SCR-19, SCR-20 | The feature and the two screens of the legacy story |
| DP-03, DP-05, DP-13, DP-19 | The decision record, the ACE owner read, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the Temporal layer with durable step timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-source-data, rwb-integration, rwb-agent, rwb-case and rwb-decision, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the two operations, the trace request and answer elements, the error set and the fakes: RWB-S4-E5017-CON.
- The ACE views, their ingestion from NCB, the registries and the insurers, the data product and its batch status: rwb-source-data (P1), whose contract is consumed here (GAP-2815; ASM-4659).
- The NCB, registry and insurer adapters, their credentials, their files and their schedules: rwb-integration (P2), whose contract is consumed here (GAP-2816; ASM-4660).
- The trace plan, the model gateway and the model that produces it: rwb-agent (P10), whose contract is consumed here and whose build is RWB-P10-TE013-APP.
- The case of record, its route state and the parent `CaseWorkflow`: rwb-case (P3), whose case-move answer this story sends and never writes.
- The enforcement decision itself — the writ and seizure (R-LIT-54), the deferral (R-LIT-53 to R-LIT-57), the petition (R-LIT-58 to R-LIT-60) and the auction ladder (R-LIT-63 to R-LIT-67): the sibling stories of this service. **This story presents the traced assets and decides nothing** (GAP-2818; ASM-4663).
- The enforcement pack and its documents: rwb-document (P5) and the pack stories of this service.
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-50 and R-LIT-52: rwb-decision (P7), with the embedded runtime as a service-template capability.
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19 and SCR-20: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
