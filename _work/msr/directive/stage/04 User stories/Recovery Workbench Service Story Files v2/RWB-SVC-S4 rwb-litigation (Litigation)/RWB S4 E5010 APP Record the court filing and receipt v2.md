# RWB-S4-E5010-APP Record the court filing and receipt

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5010-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-S4-K |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; no size value in the source documents |
| Depends on (build) | RWB-S4-E5010-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version | v1 (path `/api/recovery/litigation/v1`) |
| Contract dependencies | rwb-document, rwb-payment and rwb-agent contracts, built against their fakes, whose published version is Not specified in the source documents (DOR-RWB-S4-E5010-APP-22) (GAP-1737) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-010 for rwb-litigation (S4). The filing facts are the `legal_action` row of schema `rwb_litigation`, written on the legal-action update of base `/api/recovery/litigation/v1` (DP-13); the two rule outcomes R-LIT-30 and R-LIT-31 write one decision record through the local decision-record library before the row changes (DP-03); the filing clock of R-LIT-30 is a durable timer of `LitigationWorkflow` and not a `timer` row of the case service; the case state, the two moves, the pack and the firm's portal receipt stay with rwb-case, rwb-document and rwb-partner and are consumed on their contracts; the two workspaces read the filing state through the gateway-bff composite route (DP-19). The LIT lawsuit read of FEAT-LIT-10 (`v_ace_lawsuit`) is rwb-source-data's and not this service's (GAP-2786; ASM-4619). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 17 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **law firm user (PT-LAWFIRM)**, I want **the filing confirmation and the court case number taken from the firm onto the case, with the rule version that decided it recorded before the case moves**, so that **cases reach court faster with complete packs, and a rejected filing returns the pack for rework instead of stalling the case**.

This story owns the filing of a legal action and nothing else:

- the filing slice of the `legal_action` row of schema `rwb_litigation`: `black_case_no` DF-LEG-006 as the court case number, `lawsuit_no` DF-LEG-005, `filed_date` DF-LEG-010 and `status` DF-LEG-014 of LOV-LEGAL-STATUS, written through `PATCH /legal-actions/{legalActionId}` (API-S4-004) on base `/api/recovery/litigation/v1`, keeping its legacy operation identity (DP-13; TSD S4 T-A.1 and T-A.2);
- the two rule outcomes of the LITIGATION route set: R-LIT-30 (`FIRM_INSTRUCTED` on `CASE_FILED` to `FILED_IN_COURT`, "write the court case number to the Legal Action and set the hearing timers") and R-LIT-31 (`FILED_IN_COURT` on `COURT_REJECTED_FILING` to `FILING_REJECTED`, "record the defect and return the pack for rework"), evaluated with the rule rows at their version in force;
- one decision record per outcome, written through the local decision-record library on `rwb.decision-record.v1` **before** the row changes (DP-03), with the rule ID, the version in force, the inputs reference and the court case number;
- the filing service-level clock of R-LIT-30 as a durable timer of `LitigationWorkflow` on task queue `rwb-litigation` (ADR-016); the hearing timers that the same rule names are armed on the hearing stage of the same workflow by `RWB-S4-E5011-APP`, and no `timer` row is written here;
- the receipt of the filing and of the court case number from the panel firm through the partner portal, consumed on the rwb-partner contract;
- the match of the filing to the LIT lawsuit that FEAT-LIT-10 names, read on the rwb-source-data contract and never through an ACE view of this service (GAP-2786; ASM-4619);
- the order of the operation inside the legacy endpoint pair: `POST /cases/{caseId}/legal-actions` (API-S4-002) opens the action that the filing completes.

It does not own the case, the pack, the receipt document, the firm or the rule rows. `recovery_case`, its route states `FILED_IN_COURT` and `FILING_REJECTED`, its clocks and the officer task are rwb-case's (P3). The pack, the defect list and the receipt document are rwb-document's (P5). The instruction, the portal upload and the partner clock are rwb-partner's (S9). The LIT lawsuit and the court facts ingested from LIT are rwb-source-data's (P1). The LITIGATION package and its rows are rwb-decision's (P7). No component of this story writes a `recovery_case`, `timer`, `task`, `document`, `notice` or `decision_log_entry` row, and none reads a `v_ace_*` view.

### 2. Business rationale

The module's own problem is the measurement behind the feature: "Litigation takes 21 days to file; packs are incomplete and law firm progress is not tracked", and the module target is a litigation turnaround of six days measured on the decision log and Workbench records (FSD S4 A1.3, A2.10.1). The filing is the step where the turnaround is won or lost: a receipt that is not recorded, or a court rejection that is not returned to the pack, is a case that sits.

In the legacy build the step wrote the case, the timer, the legal action, the document index and the decision log entry in one process against one `recovery` schema. The target cuts the same step at four boundaries. The court case number and the filing date are litigation's, because `legal_action` is S4's row (Ownership Map; Architecture v5 slide 41). The case state and the two route moves are the case of record's, because `recovery_case` and `timer` are P3's. The pack and the receipt are P5's, because the document hub holds custody and the WORM store. The firm's upload arrives through the partner gateway that fronts rwb-partner, not through a Workbench table.

Three consequences are written into the story instead of hidden. First, FEAT-LIT-10 says the filing is "matched to the LIT lawsuit read through `v_ace_lawsuit`" (Epics 3 to 8 Specification v3), while this service holds no `v_ace_*` grant and DP-05 is not in the pattern set of this key, so the LIT read is rwb-source-data's and its operation and element are placeholders (GAP-2786; ASM-4619). Second, R-LIT-30's timer column reads "Filing service level by task" and R-LIT-31's reads "5 working days" with no window design, no working-day calendar and no owner of the clock in any source read, so the clock is a versioned reference row whose content is a placeholder (GAP-2786; ASM-4620). Third, the state `FILING_REJECTED` is a case route state, not a value of LOV-LEGAL-STATUS, so the legal action returns to `OPEN` with the defect kept in the decision record and no list value is invented (GAP-2786; ASM-4624).

It serves FEAT-LIT-10 "Record the court filing and receipt", it carries the module measure by making every filing and every rejection one owned row plus one decision record, and it holds the legacy prerequisite FEAT-LIT-09 through the instruction that `RWB-S4-E5009-APP` records. The four legacy criteria AC1 to AC4 belong to this story and are copied word for word in section 7. The requirement identifiers of the key are absent from the legacy master, from the Epics 3 to 8 specification and from TSD S4 T8, so the story traces to the feature and to OBJ-3 until the PRD adds them (GAP-2786; ASM-4623).

### 3. Preconditions

- `RWB-S4-E5010-CON` is published: the two provided operations on `/api/recovery/litigation/v1`, the `LegalActionUpdate` element of the filing, the error envelope, the element mapping of AC6 there and the fakes. It is the first build dependency of this story, so the story starts on Day 1.
- The `legal_action` table exists in schema `rwb_litigation` with DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and the standard columns of T3.0; the action the filing completes is opened by `POST /cases/{caseId}/legal-actions` (API-S4-002). No table and no column is created by this story.
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`) and the record is hash-linked on `rwb.decision-record.v1`; the story builds against its fake until the platform contract story publishes.
- `LitigationWorkflow` runs on task queue `rwb-litigation` in namespace `rwb-recovery`, started by `CaseWorkflow`, and it is the host of the filing clock (Temporal design slide 20; context pack workflow row). The workflow kit `RWB-PLT-E1071-CON` is not in this story's dependency rows; the absence is part of GAP-2786 with ASM-4620.
- The case read that answers the route state `FIRM_INSTRUCTED` or `FILED_IN_COURT`, the prescription date and the move, is consumed on rwb-case, operation `Not specified in the source documents (GAP-2786; ASM-4622)`; it is consumed and faked, not built.
- The pack read and the pack-return request are consumed on rwb-document, operation `Not specified in the source documents (GAP-2786; ASM-4622)`.
- The firm's filing receipt and court case number are consumed on rwb-partner (S9) through the partner gateway, operation `Not specified in the source documents (GAP-2786; ASM-4622)`.
- The LIT lawsuit match is consumed on rwb-source-data (P1), operation and element `Not specified in the source documents (GAP-2786; ASM-4619)`.
- LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2 is read as values in force with their version on the reference data of rwb-case; DP-07 is not in this story's pattern set and the read carries no dependency row of its own (GAP-2786; ASM-4622).
- The caller holds a Workbench role with the Litigation right on the operation it calls (TSD S4 T6.1). DP-08 is not in this story's pattern set: the right of the screen path is enforced at the edge and the guard on the write path is this story's design.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02) and holds no grant on another `rwb_*` schema and no `v_ace_*` grant.

### 4. Flow

1. The firm files the case at court and uploads the filing receipt and the court case number through the partner portal; the upload arrives as a partner result on the rwb-partner contract (operation not specified: GAP-2786, ASM-4622).
2. The law firm user opens SCR-19 Litigation workspace in its instructed state through the gateway-bff composite route (DP-19) and reads the action, its status, its court fields and its pack on `GET /legal-actions/{legalActionId}` (API-S4-003, the shared read of the sibling stories).
3. The user records the filing on `PATCH /legal-actions/{legalActionId}` (API-S4-004) with `LegalActionUpdate`: `status` `FILED` and `courtCaseNo`, where `courtCaseNo` is read as `legal_action.black_case_no` (GAP-2787); the update is guarded by the status of the action and not by an idempotency key, because the API specification declares none for this operation.
4. `FilingValidator` checks the action reference and its status `OPEN`, the presence of the court case number and of the receipt reference, the length of the case number against DF-LEG-006, the caller's scope and, under R-LIT-30, the LIT lawsuit match of the case. A failed check answers 404, 409 or 422 and nothing is written.
5. `FilingDecisionWriter` evaluates R-LIT-30 or R-LIT-31 of the LITIGATION route set with the rule rows at their version in force — the from-state `FIRM_INSTRUCTED` or `FILED_IN_COURT`, an event of `CASE_FILED` or `COURT_REJECTED_FILING`, and the rules' own conditions — and writes one decision record through the local decision-record library **before** the row changes (DP-03, legacy AC1 and AC3).
6. `FilingWriter` writes, in one `rwb_litigation` transaction, `black_case_no`, `lawsuit_no` where the lawsuit reference is present, `filed_date` whose source is Not specified in the source documents (GAP-2787), `status` `FILED` and the standard columns of the row.
7. `FilingClock` returns the filing service-level deadline to the workflow, which arms one durable timer on queue `rwb-litigation` with the reference row of R-LIT-30; the workflow then hands the case to the hearing stage, where the hearing timers of the same rule are armed by `RWB-S4-E5011-APP`. This service writes no `timer` row and registers no Schedule (GAP-2786; ASM-4620).
8. `CaseStateClient` announces the move: `FILED_IN_COURT` with the court case number, the filing date, the rule ID and the package version (operation not specified: GAP-2786, ASM-4622). The case row is written by rwb-case and by nobody else.
9. When the court returns the filing for a defect, the officer records the rejection on the same patch. R-LIT-31 writes its decision record with the defect in the inputs reference, keeps the action `OPEN` with no `filed_date`, asks rwb-document to return the pack to rework and announces `FILING_REJECTED` to the case of record (legacy AC2).
10. A repeated filing with the same court case number on the same action writes once, returns the stored answer and counts the repeat under R-UNI-40; a filing recorded on an action that is already `FILED` with a different case number is refused with 409 and nothing changes.
11. SCR-19 and SCR-20 read the filing state, the court case number and the rejection through the composite route, read only, next to the case route state of rwb-case. While the composite route answers, both screens show a loading state; the empty, error and no-access states are Not specified in the source documents (CG-ALL-9226; CG-ALL-9227), and the 503 and 403 answers keep the message IDs of section 12.1.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no court case number, or a case number longer than DF-LEG-006 allows | The answer is 422 and nothing is read past the validator; no decision record and no row | MSG-GEN-001 | AC1 |
| X2 | The action ID names no row in the caller's scope | The answer is 404 and nothing is written; an out-of-scope action cannot be told from a missing one | None | AC1 |
| X3 | The action is not `OPEN` for a first filing, or is already `FILED` with a different court case number | The answer is 409 and nothing changes; the stored answer is returned for a repeat of the same case number | None | AC1 |
| X4 | The pack is not acknowledged as filed, or the defect list names a missing item | The answer is 422 with the missing item and the filing is not recorded | MSG-S4-001 | AC1 |
| X5 | The claim expiry of the case falls inside the warning window | The MSG-S4-002 warning is shown with its date and the filing is not blocked; the prescription date is a fact of the case of record | MSG-S4-002 | AC1 |
| X6 | A role without the Litigation C or U right records or reads a filing | Refused before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1 |
| X7 | The local decision-record write fails | The transaction writes nothing: the row, the clock and the case announcement do not happen | MSG-P7-003 | AC4 |
| X8 | The rwb-case move does not answer inside 2 s or its breaker is open | The filing stays written, because it is this service's own; the hand-off is retried by the workflow and the officer sees the pending marker | None | AC1 |
| X9 | The rwb-document pack read or the pack-return request does not answer | The rejection keeps its own decision record and state, and the return is retried; the pack is never rebuilt here | MSG-P1-001 | AC2 |
| X10 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5010-CON`, the decision-record library, the composite route and the fakes of rwb-case, rwb-document, rwb-partner, rwb-source-data and rwb-decision; no C dependency blocks the build |
| Negotiable | The clock windows, the defect codes and the warning horizon are versioned reference rows; the story fixes the shape and the behaviour, not the values |
| Valuable | Every filing and every court rejection lands on one owned row with the court case number and one decision record, which is the evidence the six-day turnaround is measured on |
| Estimable | Two operations, one validator, one rule evaluation, one library write, one repository write, one workflow clock, four clients and one read-only workspace fragment |
| Small | Fits two weeks with its tests, as the primary slice of the legacy key |
| Testable | Each criterion of section 7 is one end-to-end test with the cross-service answers stubbed in the fakes; the contract half is tested in `RWB-S4-E5010-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Record the court filing and receipt, in rwb-litigation

  Background:
    Given the legal action "LA-2026-001010" exists on case "RC-2026-001010" with status "OPEN"
    Given the rule package of the LITIGATION route set is in force at its version, and LOV-LEGAL-STATUS is read with its version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Record the court filing and receipt (legacy RWB-E5-010 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns the case "RC-2026-001010" at route state "FIRM_INSTRUCTED" with its prescription date
    Given the rwb-source-data contract mock returns the LIT lawsuit of case "RC-2026-001010" with its court case number
    When the user acts on the screen
    Then takes the filing confirmation and the court case number from the firm onto the case
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-LIT-31 (legacy RWB-E5-010 AC2)
    Given a case in state FILED_IN_COURT
    Given the rwb-document contract mock returns the pack of case "RC-2026-001010" as returned for rework
    When court rejected filing
    Then record the defect and return the pack for rework
    Then the case moves to FILING_REJECTED

  Scenario: AC3 Rule R-LIT-30 (legacy RWB-E5-010 AC3)
    Given a case in state FIRM_INSTRUCTED
    Given the rwb-partner contract mock returns the filing receipt uploaded by the panel firm of "LA-2026-001010"
    When case filed
    Then write the court case number to the Legal Action and set the hearing timers
    Then the case moves to FILED_IN_COURT

  Scenario: AC4 Not recorded (legacy RWB-E5-010 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 No ACE read and no cross-schema read (exception X10) (new, D-RCV-60)
    Given the rwb-litigation build carries the grant set of its own login and the boundary test of section 16
    When a component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table
    Then the grant refuses the statement and the boundary test fails the build
    Then nothing is released

  Scenario: AC6 Replay of the same court case number (new, D-RCV-60)
    Given the legal action "LA-2026-001010" is FILED with the court case number of the first filing
    When the same court case number is filed again on the same action
    Then the filing is written once and the stored answer is returned
    Then the repeat is counted under R-UNI-40

  Scenario: AC7 Activity retry and timeout (new, D-RCV-60)
    Given the recordFiling activity of LitigationWorkflow times out
    When the activity is retried
    Then the legal action is written once
    Then the retry count and the timeout value are Not specified in the source documents (NEWAC-RWB-S4-E5010-APP-AC11)

  Scenario: AC8 Consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-case contract mock does not answer
    When the user acts on the screen
    Then the platform error envelope is displayed as it is (X8)

  Scenario: AC9 Rules BR1 to BR8 as architecture and data constraints (new, D-RCV-60)
    Given the rwb-litigation build and its local decision-record library are in place
    When the filing facts are written
    Then the court case number and the filing facts are written on the legal_action columns black_case_no, lawsuit_no, filed_date and status of this service only
    Then no recovery_case, timer or task row is written and no ACE view or other rwb_* schema is read
    Then the filing clock is a durable timer of LitigationWorkflow and the pack and receipt stay with rwb-document
    Then status takes only the values of LOV-LEGAL-STATUS in force and no personal data is written to the row, the decision record, the log or any call

  Scenario: AC10 Error answers of the provided operations (new, D-RCV-60)
    Given a request to a provided operation carries no valid login
    When the request is sent
    Then the answer is 401 and nothing is read or written
    Then a role without the Litigation C or U right gets 403 with MSG-P4-002 and nothing changes (X6)
    Then an action ID that names no row in the caller's scope gets 404 and nothing is written (X2)
```

These four criteria are the legacy criteria of RWB-E5-010, copied word for word: no legacy line is reworded, shortened or renumbered and every value of the source (`MSG-P7-003`, `FILED_IN_COURT`, `FIRM_INSTRUCTED`, `FILING_REJECTED`) is kept character for character. The only additions are the origin tag on each `Scenario:` line and, inside AC1 to AC3, the `Given` lines that name the cross-service answers the contract fakes supply: the case of record, the LIT lawsuit, the returned pack and the firm's receipt. The court case number is written on `legal_action.black_case_no`, the hearing timers are durable timers of `LitigationWorkflow` armed on the hearing stage by `RWB-S4-E5011-APP`, and the filing clock of R-LIT-30 is armed here. The end-to-end journey across the four services is not claimed by this story; its contract half is tested in `RWB-S4-E5010-CON`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The court case number and the filing facts are `legal_action` columns of this service — `black_case_no`, `lawsuit_no`, `filed_date`, `status` — written on that row and nowhere else | TSD S4 T3.1; Architecture v5 slide 41 |
| BR2 | The decision is written before the row changes: one record through the local decision-record library with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2; legacy AC1 and AC4 |
| BR3 | The case state, `FILED_IN_COURT`, `FILING_REJECTED` and the officer task are rwb-case's: this story announces the move and writes no `recovery_case`, `timer` or `task` row | Context pack ownership rows; GAP-2786; ASM-4622 |
| BR4 | No ACE read: no `v_ace_*` view, no ACE table and no other `rwb_*` schema is read, and the login holds no such grant; the LIT lawsuit is consumed on the rwb-source-data contract | DP-01, DP-05 as a prohibition; Architecture v5 slide 29; GAP-2786; ASM-4619 |
| BR5 | A filing clock is a durable timer of `LitigationWorkflow`; no `timer` row, no Quartz job and no Schedule is written or registered here | ADR-016; Temporal design slide 20; GAP-2786; ASM-4620 |
| BR6 | The pack, the receipt document and the defect list stay with rwb-document: the return for rework is a request to P5 and never a rebuild here | Context pack; FSD S4 A2.10.2 (integration points "Partner portal, LIT"); ASM-4622 |
| BR7 | Closed vocabulary: `status` takes only the values of LOV-LEGAL-STATUS in force and the clock windows and defect codes are versioned reference rows, never code | TSD S4 T3.2; FSD S4 A2.10.3.1 (BR-S4-010); Template and Rules §R7.2 (s17) |
| BR8 | No personal data: the row, the decision record, the log and every call carry identifiers, list values, amounts and dates only | TSD S4 T3.1; Architecture v5 slides 42 and 43 notes |
| BR9 | From `FIRM_INSTRUCTED`, on `CASE_FILED`, when "the firm uploads the receipt and the court case number", the court case number is written to the legal action and the hearing timers are set; the case moves to `FILED_IN_COURT`; the clock is "filing service level by task" | Business Rules and Routing Logic v4 (R-LIT-30) |
| BR10 | From `FILED_IN_COURT`, on `COURT_REJECTED_FILING`, when "the court returns the filing for a defect", the defect is recorded and the pack returned for rework; the case moves to `FILING_REJECTED`; the clock is 5 working days | Business Rules and Routing Logic v4 (R-LIT-31) |
| BR11 | An action whose decision cannot be recorded does not proceed and nothing moves | Business Rules and Routing Logic v4 (R-UNI-39); legacy AC4 |
| BR12 | The same event or the same request twice produces one effect, and the repeat is counted | Business Rules and Routing Logic v4 (R-UNI-40) |

Coverage of the twelve rules by criterion and test case: BR1 with AC1 and TC-E5-010-01; BR2 with AC1 and AC4 and TC-E5-010-01, -04 and -06; BR3 and BR6 with AC2 and AC3 and TC-E5-010-02 and -03; BR4 with AC5 and TC-E5-010-07; BR5 and BR9 with AC3 and TC-E5-010-03; BR7 and BR8 with TC-E5-010-08 and -09; BR10 and BR11 with AC2 and AC4 and TC-E5-010-02 and -04; BR12 with AC6 and TC-E5-010-10; BR1 to BR8 also with AC9 and TC-E5-010-13.

The value behind "filing service level by task" of R-LIT-30 and the working-day calendar behind the 5 days of R-LIT-31 have no number in the legacy story, in FSD S4 A2.10, in TSD S4 or in the routing workbook read for this key. They are therefore versioned reference rule rows of the business and never code, and their content is `Not specified in the source documents (GAP-2786; ASM-4620)`. The re-file that R-LIT-32 names (`FILING_REJECTED` on `PACK_REWORKED` to `PACK_ASSEMBLY`, 3 working days) is the pack-rework story's and is named here, never built.

### 9. State transitions

This story moves its own `legal_action.status` and announces a case route move that rwb-case owns. The two are different objects and are never used one for the other.

**`legal_action.status`** — the values of LOV-LEGAL-STATUS (TSD S4 T3.2), moved by this service:

| From | Event | Condition | To |
|---|---|---|---|
| `OPEN` | The firm's filing is recorded under R-LIT-30 | The court case number and the receipt reference are present, the LIT lawsuit matches, the decision record is written | `FILED`, with `black_case_no`, `lawsuit_no` where present, and `filed_date` set |
| `OPEN` | The court returns the filing under R-LIT-31 | The defect is recorded and the decision record is written | `OPEN`, with no `filed_date`, the defect in the decision record's inputs reference and the pack returned to P5 |
| `FILED` | The same filing is recorded twice | The court case number repeats | `FILED` unchanged; the repeat is counted and no second decision record is written (R-UNI-40) |
| `FILED` | A different court case number arrives on the same action | The action is already `FILED` | Refused with 409; no write |

`FILING_REJECTED` is not a value of LOV-LEGAL-STATUS and this story adds no value to that closed list: it is the case route state that rwb-case holds, and a list value for it is not invented here (GAP-2786; ASM-4624).

**The filing clock** is the workflow's, not a table's:

| From | Event | Condition | To |
|---|---|---|---|
| Armed | The filing is recorded under R-LIT-30 | The reference row of the filing service level and the filing date | The timer waits on queue `rwb-litigation` |
| Waiting | The timer fires | The firm has filed and the case is in `FILED_IN_COURT` | The reminder fact is raised to the officer's task list on the rwb-case contract; one decision record is written |
| Waiting | The filing is rejected under R-LIT-31 | The action returns to `OPEN` | The timer completes with no fact and no second decision record |

The hearing timers that R-LIT-30 names are armed on the hearing stage of the same workflow by `RWB-S4-E5011-APP` from the hearing date; this story arms the filing clock only and arms no hearing timer.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| PT-LAWFIRM, law firm user | Partner gateway, Litigation RU on the rows of its own instructed cases (TSD S4 T6.1); it records the filing receipt and the court case number of its own filings and reads nothing else |
| RW-LITOFF, litigation officer | Litigation CRUA: records the filing and the rejection, reads the action and the decision record |
| RW-ENFORCE, enforcement owner | Litigation CRU: records and reads the filing of its own enforcement actions |
| RW-LEGAL, RW-PRODHEAD, RW-HEADLIT | Litigation RA: read the filing and acknowledge it; they record no filing |
| SY-DATALOAD, data load from LIT | Litigation U on the filing fields, for the court facts that arrive from LIT; it does not move the case state |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read the action, its status and its court fields only |
| rwb-litigation service identity | Validates, evaluates R-LIT-30 and R-LIT-31, writes the decision record, the row and the clock, and calls the case, document, partner and source contracts; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-case (P3) | Owns the case, the route state and the officer task; answers the case read and applies the move |
| rwb-document (P5) | Owns the pack, the defect list and the receipt document; answers the pack read and receives the return for rework |
| rwb-partner (S9) | Owns the instruction, the portal and the partner clock; answers the firm's filing receipt and court case number |
| rwb-source-data (P1) | Owns the ACE and LIT data; answers the LIT lawsuit read |
| rwb-decision (P7) | Owns the LITIGATION package and the central ledger; answers the rule package read |

The rights above are the rows of TSD S4 T6.1 and the legacy permission table of RWB-E5-010 and nothing wider: Litigation C for RW-LITOFF and RW-ENFORCE, Litigation U for RW-LITOFF, RW-ENFORCE, PT-LAWFIRM and SY-DATALOAD. DP-08 is not in this story's pattern set: the declared right of the screen path is enforced at the edge and the guard on the write path is this story's design. A refusal keeps MSG-P4-002 and changes nothing. The authorise check of the write path is Not specified in the source documents (DOR-RWB-S4-E5010-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-006 | legal_action (S4, `rwb_litigation`) | black_case_no | Write on the filing; the court case number of R-LIT-30 |
| DF-LEG-005 | legal_action (S4, `rwb_litigation`) | lawsuit_no | Write when the LIT lawsuit read carries one; read on every answer |
| DF-LEG-010 | legal_action (S4, `rwb_litigation`) | filed_date | Write on the filing from the receipt date of the firm, and from the business date where the receipt carries none |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write, a value of LOV-LEGAL-STATUS |
| DF-LEG-001, DF-LEG-002, DF-LEG-003, DF-LEG-004, DF-LEG-008 | legal_action (S4, `rwb_litigation`) | id, case_id, law_firm_id, action_type, court_name | Read only; no column is written by this story; `case_id` is a varchar(255) business key with no foreign key (DP-01) |
| DF-LEG-011, DF-LEG-012, DF-LEG-013 | legal_action (S4, `rwb_litigation`) | judgment_date, judgment_amount, lit_status | Not touched; the judgment is `RWB-S4-E5016-APP`'s and `lit_status` arrives from LIT |
| Standard columns | legal_action (S4, `rwb_litigation`) | state, version, created_at, created_by, updated_at, updated_by, is_active | Written by the service identity (TSD S4 T3.0) |
| DF-DEC-003, DF-DEC-004, DF-DEC-005, DF-DEC-008, DF-DEC-012, DF-DEC-016, DF-DEC-017, DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule ID, rule version, inputs reference, final call, decided at, the two hashes | Write through the local library, before the row changes |
| DF-CAS-001, DF-CAS-002 and the route and prescription facts | recovery_case (P3, `rwb_case`) | id, case_no, route state, prescription date, product group | Read on the case contract and stored nowhere here |
| DF-DOC-001 to DF-DOC-011 | document (P5, `rwb_document`) | id, case_id, person_key, document_type, source, storage_ref and 5 more | Read on the document contract as the pack and the receipt; the pack return is a request |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule id, version, route set, from state, event code and 9 more | Read as the package in force; never written here |

Field IDs are those of TSD S4 v2 T3.1, the standard columns of T3.0 and the decision record identifiers of the legacy data table, which the Logical Data Model and Data Dictionary v9 shares. **No new table, no new column and no migration:** `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5010-CON`, which the service's own Flyway applies (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration (DP-03).

**Not written, not read as a table, and named here so that a reviewer can check the absence:** `recovery_case` DF-CAS-* and `timer` DF-WRK-027 to DF-WRK-036 and `task` DF-WRK-017 to DF-WRK-026 (P3), `document` DF-DOC-001 to DF-DOC-011 (P5), `notice` DF-LEG-015 to DF-LEG-023 (P6), `decision_log_entry` DF-DEC-001 to DF-DEC-018 and `rule_row` DF-REF-001 to DF-REF-015 of the central ledger (P7), `proceeds` DF-FIN-001 to DF-FIN-009 (P8), and every `v_ace_*` view (P1). Every cross-service reference is an identifier, not a foreign key across schemas (DP-01, BR4).

**No personal data.** The row this story writes carries identifiers, list values, amounts and dates. The borrower, the guarantor, the address and the identity number never enter `rwb_litigation`: they are held by ACE and reached only through rwb-source-data, and they are not logged here and not put on any call.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | Record a filing, a rejection, a judgment or an enforcement step (TSD S4 T-A.2) | Litigation U, scope applied | None declared; the status guard answers 409 and a repeat of the same court case number returns the stored answer |
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | Open a legal action and its pack, which the filing completes (TSD S4 T-A.2) | Litigation C, scope applied | `Idempotency-Key` header required |

The two operations, their IDs, rights and error sets are those of TSD S4 T-A.1 and T-A.2, and they are the two of the legacy endpoint table of RWB-E5-010; they differ only in the base, which DP-13 renames. Both are shared surfaces: `RWB-S4-E5021-APP` opens the action of a bankruptcy petition, `RWB-S4-E5011-APP` patches the hearing outcome and `RWB-S4-E5022-APP` patches the enforcement step on the same element, so this story declares the filing slice of it and does not redefine it. Errors: 401 no session; 403 no right (MSG-P4-002); 404 unknown or out-of-scope reference; 409 a status or a court case number that refuses the step; 422 a missing or invalid field, or a pack the defect list names (MSG-GEN-001, MSG-S4-001); 503 the decision-record library or a consumed contract unavailable. The HTTP error 404 carries MSG-P4-003 (PRD P4 rwb-access FR-P4-015) and the HTTP error 503 carries MSG-P7-003 (PRD P4 rwb-access FR-P4-025); the HTTP errors 401 and 409 carry no message ID in this set: Not specified in the source documents (CG-ALL-9214). The shapes are declared by `RWB-S4-E5010-CON`, which this story consumes as its first build dependency.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The case read and the filing move of rwb-case, operation Not specified in the source documents (GAP-2786; ASM-4622), base `/api/recovery/case/v1` | P3 rwb-case | Reads the route state `FIRM_INSTRUCTED` or `FILED_IN_COURT`, the prescription date and the product group, and announces `FILED_IN_COURT` or `FILING_REJECTED` with the rule ID, its version and the officer task |
| The pack read and the pack-return request of rwb-document, operation Not specified in the source documents (GAP-2786; ASM-4622), base `/api/recovery/document/v1` | P5 rwb-document | Reads the pack and the defect list of the action, and asks for the pack to be returned to rework under R-LIT-31; custody and the receipt document stay with P5 |
| The filing receipt and court case number of rwb-partner, operation Not specified in the source documents (GAP-2786; ASM-4622), base `/api/recovery/partner/v1` | S9 rwb-partner | Reads the receipt the panel firm uploaded through the portal and the court case number it carries; the instruction and the partner clock stay with S9 |
| The LIT lawsuit read of rwb-source-data, operation and element Not specified in the source documents (GAP-2786; ASM-4619), base `/api/recovery/source-data/v1` | P1 rwb-source-data | Matches the filing to the LIT lawsuit that FEAT-LIT-10 names; this service holds no `v_ace_lawsuit` grant |
| The rule package read of rwb-decision, operation Not specified in the source documents (GAP-2786; ASM-4621), base `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-30 and R-LIT-31 |
| The reference-data read of LOV-LEGAL-STATUS, `RWB-P3-E1043-CON`, base `/api/recovery/case/v1` | P3 rwb-case | The status values at their version in force; DP-07 is declared here although it is not in this story's pattern set (GAP-2786; ASM-4622) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The first, second, third and fifth rows are consumed contracts in fact that the plan's C row does not carry, which is part of GAP-2786 with ASM-4619 to ASM-4622; the story builds against their fakes on Day 1. No operation of another service is declared as provided here (BR1).

#### 12.3 Events published

None. The service topic is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), the ownership rows of this service publish zero events and TSD S4 T5.3 declares no event for the module. DP-09 is not in the pattern set of this key, so no outbox row and no producer is added. The decision record is relayed by the library of DP-03 on `rwb.decision-record.v1` and is not an event of this service. Whether the filing should raise an event of its own is unsettled by every source read here and is carried as GAP-2786 with ASM-4621.

#### 12.4 Events consumed

None. The firm's receipt, the case state and the pack are synchronous answers of their contracts, not topics. R-LIT-30's `CASE_FILED` and R-LIT-31's `COURT_REJECTED_FILING` are event names of the state machine and not Kafka subscriptions, because the service publishes and consumes nothing and DP-09 is not in its pattern set. No consumer group, no subscription and no inbox is declared here (GAP-2786; ASM-4621).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LitigationWorkflow | Workflow, one run per case stage, the S4 child of CaseWorkflow, continues-as-new | `rwb-litigation` | Hosts the filing stage, its durable filing clock and the transition to the hearing stage (ADR-016; Temporal design slide 20) |
| recordFiling | Activity | `rwb-litigation` | The validator, the R-LIT-30 evaluation and the `legal_action` write of steps 4 to 6 |
| rejectFiling | Activity | `rwb-litigation` | The R-LIT-31 evaluation, the defect record and the pack-return request |
| recordDecision | Activity through the library | `rwb-litigation` | The local decision record and its outbox row, written before the change (DP-03) |
| armFilingClock | Activity | `rwb-litigation` | Arms the filing service-level timer from the versioned reference row and returns the next wake-up to the workflow (BR5) |
| announceFilingMove | Activity | `rwb-litigation` | The `FILED_IN_COURT` or `FILING_REJECTED` move and the officer task on the rwb-case contract |

The workflow name is fixed by the Temporal and Drools design (`LitigationWorkflow` on `rwb-litigation`); the filing is a stage of that workflow and not a workflow of its own, and the activity names are target design choices of this story. No activity is registered by a contract document, and no Schedule is declared. The workflow ID form and its start rule are Not specified in the source documents (CG-ALL-9216; DOR-RWB-S4-E5010-APP-8); the start by CaseWorkflow is as stated in section 3.

#### 12.6 Schedules

None. The filing clock is a durable timer inside `LitigationWorkflow`, started by the filing event and by the reference row of the service level, not by a Temporal Schedule and not by a Quartz job; no Schedule of Architecture v5 is owned, moved or registered here and the retired `TE-007` scheduler has no successor in this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (rwb_litigation) | The action row; this story writes `black_case_no`, `lawsuit_no`, `filed_date` and `status` and reads the rest |
| decision_record | PLT library, created in `rwb_litigation` | The hash-linked record of each filing and rejection, written before the change (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the action create, with the stored answer |

Not owned and never written: `recovery_case` and its route state (P3), `timer` (P3), `task` (P3), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8). `hearing` is S4's and belongs to `RWB-S4-E5011-APP`, which writes it. No `v_ace_*` view and no ACE table is read (BR4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | Case `RC-2026-001010` at route state `FIRM_INSTRUCTED`, at `FILED_IN_COURT` and at `FILING_REJECTED` with its prescription date; an accepted move and a refused move; a delayed answer | AC1, AC2, AC3, X8 |
| rwb-document WireMock | The pack of `RC-2026-001010` as filed and as returned for rework, with the defect list; an absent pack | AC2, X4, X9 |
| rwb-partner WireMock | The filing receipt of `LA-2026-001010` uploaded by the panel firm with its court case number, and an instruction not accepted | AC3 |
| rwb-source-data lawsuit WireMock | The LIT lawsuit of `RC-2026-001010` with its court case number, a case with no lawsuit, and a stale answer | AC1, X9 |
| rwb-decision rule-package WireMock | The LITIGATION package at its version with R-LIT-30, R-LIT-31 and R-LIT-32, and a second version | AC1, AC2 |
| decision-record library stub (RWB-PLT-E1027-CON) | A healthy chain with its outbox row, and a stopped chain for the fail-closed test | AC1, AC4 |
| gateway-bff composite route fake (RWB-PLT-N001-CON) | The merged SCR-19 and SCR-20 answer for `RC-2026-001010`, with the filing state, the court case number and the rejection read once | AC1, AC2 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and `RWB-S4-E5010-CON` or against the case, document, partner and source documents is a build failure. Every fixture identifier is synthetic.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | API-S4-004 and API-S4-002 provided; the case read and move, the pack read and return, the firm receipt, the LIT lawsuit, the rule package and the reference data consumed; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story; the decision record is the library's element on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 5 activities, no child workflow, no Schedule | LitigationWorkflow, its filing activities and its durable filing clock on `rwb-litigation` |
| File | None | No file is read, built or delivered here; the receipt document is rwb-document's and the portal upload is rwb-partner's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `filing`, Java package `th.co.scb.ace.workbench.recovery.litigation.filing`; front end `src/modules/recovery/litigation/Filing.tsx`, the fragment SCR-19 and SCR-20 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1`; the two operations keep API-S4-002 and API-S4-004 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 carries legacy AC1's "writes the result to the decision log with the rule version" and legacy AC4's fail-closed behaviour. DP-13 renames the base and keeps the operation IDs and the two endpoints of the legacy table. DP-19 covers SCR-19 and SCR-20 only, and the screen model and the merge order stay with the edge contract.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the metadata already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, and nothing else. Four capabilities this story leans on have no row at all: the case read and move (P3), the pack read and return (P5), the firm receipt (S9) and the LIT lawsuit (P1), and the rule package (P7) and the reference data (P3) are in the same position. They are consumed and faked, and they are recorded as GAP-2786 with ASM-4619 to ASM-4622. No C dependency blocks the build (Template and Rules §R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FilingController | Controller | API-S4-004 and API-S4-002 with the problem mapping for 401, 403, 404, 409, 422 and 503 |
| FilingValidator | Service | The action reference and its status, the court case number and its length, the receipt reference, the caller's scope and the LIT match |
| FilingDecisionWriter | Library adapter | One hash-linked record with the rule ID and the version in force, before any change; refuses the request when the write fails (DP-03) |
| FilingWriter | Repository | `black_case_no`, `lawsuit_no`, `filed_date`, `status` and the standard columns, in one `rwb_litigation` transaction |
| FilingClock | Workflow activity adapter | The filing service-level deadline from the reference row and the durable timer that carries it |
| CaseMoveClient | Client | The case read and the `FILED_IN_COURT` and `FILING_REJECTED` moves to rwb-case, one hop, 2 s, breaker |
| PackClient | Client | The pack read and the pack-return request of rwb-document, one hop, 2 s, breaker |
| FirmReceiptClient | Client | The filing receipt and court case number of rwb-partner, and the LIT lawsuit read of rwb-source-data, one hop, 2 s, breaker |
| Filing | React component | Shows the filing state, the court case number, the rejection and the pending hand-off on SCR-19 and SCR-20, read only, with the refusal and failure states |

**Database and migrations.** No Flyway file. `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5010-CON`; the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). The index set of `legal_action` is `Not specified in the source documents (GAP-2786; ASM-4620)`; this story needs a lookup by `case_id` and by `black_case_no` for the duplicate check and creates no index beyond what the contract template declares.

**Configuration and reference data.**

- The filing service level of R-LIT-30 and the working-day calendar of R-LIT-31 as versioned reference rule rows. Their content is `Not specified in the source documents (GAP-2786; ASM-4620)`.
- The prescription warning window behind MSG-S4-002, as a versioned reference row. Its value is `Not specified in the source documents (GAP-2786; ASM-4620)`.
- LOV-LEGAL-STATUS at its version in force (TSD S4 T3.2), and the decision code of the filing and rejection decisions read as a value of LOV-DECISION.
- The 2 s budget and the single hop are the platform rule of ADR-020 and not a value of this story.

**Build steps**

1. Build `FilingValidator` and `FilingWriter` over the `legal_action` row and the contract fake; test AC1 and X1 to X3.
2. Build `FilingDecisionWriter` against the library fake, with the stopped chain; test AC1, AC3 and AC4.
3. Build `CaseMoveClient` against the case fake and announce the two moves; test AC1, AC2, AC3 and X8.
4. Build `PackClient` and the pack-return request; test AC2, X4 and X9.
5. Build `FirmReceiptClient` against the partner and lawsuit fakes; test AC1 and AC3.
6. Build `FilingClock` and the workflow activity against a workflow test double; test the timer and the rejection.
7. Build `Filing` and read it through the composite route fake; test AC1 and AC2.
8. Add the boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no `recovery_case`, `timer`, `task`, `document`, `notice` or `proceeds` write; test BR3 to BR6.

**Feature flag.** `rwb.litigation.filing-v1`, read as a flag of the platform library; off means the filing patch answers 404 for the filing fields and the workspace shows the action read only, while the action create and the read are unaffected.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-S4-E5010-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one row per filing, one decision record per outcome, one filing clock per filing, no `timer` or case row written by this service, no `v_ace_*` read in its logs and every rejection returned to the pack.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | The pack is not acknowledged as filed or the defect list names a missing item (X4) | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the warning window (X5) | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the request is missing or invalid (X1) | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the Litigation right of the operation (X6) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the filing changes (X7, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed batch, which is VR-S4-010-1 of the FSD; the check is the owner's (X9) | {product} is from {date}. Today's load has not arrived. |

The five legacy texts are the wording of RWB-E5-010 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the field it names. `MSG-S4-001` names the pack item the defect list reports and is raised on the rejection and on the incomplete pack. `MSG-S4-002` carries the claim expiry date read from the case of record, and the warning window behind it is `Not specified in the source documents (GAP-2786; ASM-4620)`. `MSG-P1-001` is carried by VR-S4-010-1 of the FSD, and the freshness check belongs to rwb-source-data; this service shows the marker. A downstream that does not answer (X8) and a reference that is not found (X2) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-19 Litigation workspace | Instructed | The action, its pack and its court fields with the filing form: the court case number and the receipt reference |
| SCR-19 Litigation workspace | Filed | The court case number, the filing date, the filing clock and the hearing stage that follows |
| SCR-19 Litigation workspace | Pack and hearing and judgment | The same action read only for the filing slice, next to the pack and the calendar |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-9226) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-9226) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-9226) |
| SCR-20 Enforcement workspace | Requested, seized, auctioned, closed | The filing state of the enforcement action, read only |
| SCR-20 Enforcement workspace | Empty | Not specified in the source documents (CG-ALL-9227) |
| SCR-20 Enforcement workspace | Error | Not specified in the source documents (CG-ALL-9227) |
| SCR-20 Enforcement workspace | No access | Not specified in the source documents (CG-ALL-9227) |
| SCR-19 and SCR-20 | Loading | The placeholder while the composite route answers |
| SCR-19 and SCR-20 | Refused | MSG-P4-002, with the right the role lacks named |
| SCR-19 and SCR-20 | Not recorded | MSG-P7-003, with the action unchanged and the retry offered |
| SCR-19 and SCR-20 | Rejected | MSG-S4-001 with the defect and the pack returned for rework |
| SCR-19 and SCR-20 | Stale source | MSG-P1-001 with the stale marker, while the filing itself answers |

The screen field list and the merge order belong to `RWB-PLT-N001-CON`; this story fixes only the answers it provides and the states they carry. No screen calls this service directly, and the firm's path reaches it through the partner gateway and the rwb-partner contract.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-010-01 | AC1 | End to end | Record the court filing and receipt |
| TC-E5-010-02 | AC2 | Component | Rule R-LIT-31 |
| TC-E5-010-03 | AC3 | Component | Rule R-LIT-30 |
| TC-E5-010-04 | AC4 | Component | Not recorded |
| TC-E5-010-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-010-06 | Principle 5 | NFR | A forced decision record write failure stops the action with MSG-P7-003 |
| TC-E5-010-07 | AC5 | Boundary | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table; the build fails |
| TC-E5-010-08 | §12 operations, events and activities | Contract | The provided and consumed operations of §12 match `RWB-S4-E5010-CON` and the fakes |
| TC-E5-010-09 | §12.7 tables | Boundary | Only the tables of §12.7 marked as owned are written, and no table marked not owned is written |
| TC-E5-010-10 | AC6 | Component | Replay of the filing with the same court case number; the write happens once |
| TC-E5-010-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5010-APP-AC11) |
| TC-E5-010-12 | AC8 | Component | The rwb-case call does not answer; the platform error envelope is displayed |
| TC-E5-010-13 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5010-APP-AC8) |
| TC-E5-010-14 | AC10 | Component | A request without a valid login, a role without the right and an action outside the caller's scope; answers 401, 403 and 404 |

The six legacy test case IDs, their Covers and their test intent are kept in order and character for character. The legacy table carries no level column, so the case that exercises the whole step maps to `End to end`, the two rule cases, the not-recorded case and the access case to `Component`, and the forced failure of Principle 5 to `NFR`. The case, document, partner, lawsuit, rule-package, library and composite-route fakes of section 12.8 stand behind every case, and the fixture data — case `RC-2026-001010`, action `LA-2026-001010` and the filing of the receipt — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the filing service level, the working-day calendar, the warning window, the lists and the message texts are values and reference rows with a version; no list value, state name or date appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry identifiers, list values, amounts and dates only, and the test data is synthetic.
- The case stays with rwb-case: no `recovery_case` row, no route state and no `timer` or `task` row is written here (BR3).
- The pack and the receipt stay with rwb-document: no `document` row is written and the return for rework is a request (BR6).
- ACE data only through the owner's contract: no `v_ace_*` view and no ACE table is read, and the boundary test fails a build that adds one (BR4).
- One base, one topic, one queue and one login per service: this story names no other service's base or topic as its own (DP-13, DP-14).
- The error envelope, the idempotency rule and the naming rule come from the platform library; this story narrows them but never redefines them.
- No retired element is reintroduced: no Quartz job, no shared job table and no second scheduler beside the workflow.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| No REQ-S4 identifier is given for this key by any source read: TSD S4 T8 maps REQ-S4-001 to REQ-S4-010 to FEAT-LIT-01, the Epics 3 to 8 specification carries feature IDs only and the legacy master carries none (GAP-2786; ASM-4623) | The filing confirmation and the court case number are taken onto the case (FSD S4 A2.10, FEAT-LIT-10) | The two operations, the `legal_action` filing slice and the two rules | TC-E5-010-01, TC-E5-010-03 | FEAT-LIT-10 | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) |
| OBJ-3 (Business Requirements Epics 3 to 8) | Litigation is instructed, tracked and enforced with one named owner from judgment to the end of enforcement | The filing state, the court case number and the decision record | TC-E5-010-01, TC-E5-010-02 | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) |
| FEAT-LIT-10 | Record the court filing and receipt | The whole story | TC-E5-010-01, TC-E5-010-02, TC-E5-010-03 | FEAT-LIT-10 | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable filing clock on `rwb-litigation` | TC-E5-010-01, TC-E5-010-06 | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-E5-010-05 | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) |
| ADR-022 | Local decision record plus central ledger | The library write before each change | TC-E5-010-04, TC-E5-010-06 | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) | Not specified in the source documents (DOR-RWB-S4-E5010-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-010, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by this story |
| Test cases | TC-E5-010-01 to -06, kept in order |
| Feature and screens | FEAT-LIT-10, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-30 and R-LIT-31, and R-LIT-32 named for the re-file, from the Business Rules and Routing Logic v4 and governed in rwb-decision (GAP-2786; ASM-4621) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal layer), ADR-020 (contract-first REST), ADR-022 (local decision record) |

### 19. Out of scope

- The case of record, its route state, the moves `FILED_IN_COURT` and `FILING_REJECTED` and the officer task: rwb-case (P3), whose case read and move this story consumes and fakes (GAP-2786; ASM-4622).
- The pack, the defect list, the receipt document and its custody: rwb-document (P5); this story reads the pack and asks for its return (BR6).
- The instruction, the partner portal, the partner clock and the firm's decline: rwb-partner (S9) and `RWB-S4-E5009-APP`.
- The LIT lawsuit and the court facts ingested from LIT, and the `v_ace_lawsuit` read: rwb-source-data (P1); this service holds no `v_ace_*` grant (GAP-2786; ASM-4619).
- The authoring, testing, approval and versioning of the LITIGATION package and of the rows of R-LIT-30 to R-LIT-32: rwb-decision (P7) (GAP-2786; ASM-4621).
- The opening of the legal action and its pack in full (`RWB-S4-E5021-APP` reads and patches the same element), the pack assembly and verification (`RWB-S4-E5004-APP` to `RWB-S4-E5007-APP`), the hearing calendar (`RWB-S4-E5011-APP`), the judgment (`RWB-S4-E5016-APP`) and the enforcement step (`RWB-S4-E5022-APP`).
- The filing service level, the working-day calendar, the warning window and the defect codes as business values: the business owner of S4 and the reference-data owner of rwb-case (GAP-2786; ASM-4620).
- The rights, roles, scope and masking data themselves, and the composite route and screen field list of SCR-19 and SCR-20: rwb-access and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
