# RWB-S4-E5014-APP Decide and manage an appeal

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5014-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E5-014 for rwb-litigation (S4). An appeal is a legal action of action type `APPEAL` of LOV-LEGAL-TYPE on base `/api/recovery/litigation/v1` (DP-13); the appeal decision, its grounds, its D7.4 approval and its filing are recorded on that row and tracked to the hearing calendar, with one decision record written through the local decision-record library before anything changes (DP-03); SCR-18 and SCR-19 are read through the gateway-bff composite route (DP-19). The case route states of the appeal, the delegation of authority and the firm stay with rwb-case, rwb-decision and rwb-partner, are consumed and faked, and are recorded as gaps. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the appeal decision, its grounds and its approval recorded on a legal action of action type `APPEAL`, one decision record written with the rule version before the row moves, the firm instructed to appeal when the approver at D7.4 grants it, and the appeal tracked from the appeal window to its hearing**, so that **a dismissed case reaches the appeal court inside the window instead of outside it, and the case route state, the delegation of authority and the firm stay with the services that own them**.

This story owns the appeal legal action and the evaluation of R-LIT-45 to R-LIT-49, and nothing else:

- the three legal-action operations of TSD S4 T-A on base `/api/recovery/litigation/v1`: API-S4-002 create, API-S4-003 read and API-S4-004 patch, keeping their legacy operation IDs (DP-13);
- the `legal_action` row of schema `rwb_litigation` with its columns DF-LEG-001 to DF-LEG-014 and the appeal as one value of `action_type`, `APPEAL` of LOV-LEGAL-TYPE (TSD S4 T3.1 and T3.2);
- the evaluation of R-LIT-45 (dismissal opens the appeal window), R-LIT-46 (the appeal decision), R-LIT-47 (approved, instruct the firm and reset the hearing timers), R-LIT-48 (the appeal hearing is set) and R-LIT-49 (declined, route to write-off), and the one decision record written before each move, with the rule ID and the version in force (DP-03);
- the durable timer of the appeal window on `LitigationWorkflow`, and the hearing timers it resets on a granted appeal;
- the call that takes the appeal to the approver at D7.4 on the approval contract of rwb-decision, the call that announces each route fact to rwb-case, and the call that asks rwb-partner for the firm instruction; all three are consumed and faked.

It does not own the case, the approval, the pack, the firm or the hearing records. The case and its route states `JUDGMENT_DISMISSED`, `APPEAL_DECISION`, `APPEAL_FILED`, `IN_HEARING` and `TO_WRITE_OFF` are rwb-case's (P3) — they are **case** route states, not the status of this service's legal action. The approval item, its D7.4 limit and the Head of Litigation's above-limit approval are rwb-decision's (P7). The firm, its instruction and its result are rwb-partner's (S9) and, inside this service, `RWB-S4-E5009-APP`'s. The judgment that opens the window is `RWB-S4-E5016-APP`'s; the hearings are `RWB-S4-E5011-APP`'s (API-S4-005); the pack is rwb-document's (P5). No component of this story writes a `recovery_case`, `decision_log_entry`, `rule_row`, `document`, `partner`, `notice` or `hearing` row, and none reads a `v_ace_*` view.

### 2. Business rationale

An appeal is the one litigation step that is lost to the clock. Litigation takes 21 days to file, packs are incomplete and law-firm progress is not tracked (FSD S4 v3 A2.14.1), and an appeal adds a legal window that no person can extend: R-LIT-45 opens it on a dismissal, R-LIT-46 decides inside it and R-LIT-47 files before the deadline, with the service level of each stated as "to the window end" and "to the filing deadline". The legacy story recorded the decision, the grounds and the approval against one `recovery` schema with the case, the log and the panel all in reach (legacy Data and Endpoints blocks).

In the target the same step is cut in five: the appeal legal action, its court references and the filing facts are litigation's; the case and the route states are the case of record's; the approval and its limit are the decision centre's; the firm and its result are the partner service's; and the judge's dismissal that opens the window is the judgment story's. This story is the litigation slice: it opens the appeal, evaluates the rule at each fork, writes the decision record first, and tells the case of record what happened.

Three facts drive the cut. The decision log of the monolith is now a local record plus a central ledger (DP-03, ADR-022): the record is written in this service's own transaction **before** the row changes, and a failed write changes nothing — that is legacy AC2 and the old `DecisionLogWriter` position in TSD S4 T2 ("writes the decision log entry before any change"). The case route state is not this service's to write: R-LIT-45 to R-LIT-49 name states of a 38-state litigation machine that rwb-case holds, so the service announces the fact and accepts the answer. And the approval is not a screen here: the D7.4 approver, the limit and the Head of Litigation's above-limit right are rwb-decision's data and decision, reached on the approval contract.

Two values the legacy criterion names have no home in any source read for this key. The appeal **grounds** are not a column of `legal_action` (TSD S4 T3.1, DF-LEG-001 to DF-LEG-014) and not a field of the FSD field catalog (A2.14.3.2); the **appeal window end** is a condition of R-LIT-46 but no column and no reference row carries it; and its length is given by no source (GAP-2802; GAP-2805). Neither is invented here; both are carried as gaps with their assumptions, and the vocabulary the story may use is only the six values of LOV-LEGAL-STATUS in force (GAP-2804).

It serves FEAT-LIT-14 "Decide and manage an appeal", it carries the FSD measure "litigation turnaround, 6 days" by putting the decision, the approval and the filing on one tracked legal action, and it holds the legacy prerequisite FEAT-LIT-12 by reading the next-step proposal the recommendation story produces rather than re-implementing it. The two legacy criteria AC1 and AC2 belong to this story and are copied word for word in section 7. The requirement identifiers of the key are absent from the legacy master and from the Epics 3 to 8 specification, so the story traces to the feature until the PRD adds them (GAP-2803; ASM-4643).

### 3. Preconditions

- `RWB-S4-E5014-CON` is published: the three operations on `/api/recovery/litigation/v1`, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the appeal sub-shape, the error envelope, the `Idempotency-Key` rule and the fake. It is the first build dependency of the story, so the story starts on Day 1.
- The `legal_action` table exists in schema `rwb_litigation` with the columns DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and the standard columns of T3.0; no new table and no new column is created by this story. A column for the appeal grounds or the window end exists in no source and is not added here (GAP-2802; ASM-4642).
- The local decision-record library and the shared record format of DP-03 are live (`RWB-PLT-E1027-CON`), and the record is hash-linked on the shared topic `rwb.decision-record.v1`; the story builds against its fake until the platform contract story publishes.
- The approval contract of rwb-decision is published and faked at the D7.4 level, with the Head of Litigation above the limit. It carries no dependency row in the plan's metadata and its raise operation is named by no source read here (GAP-2801; ASM-4641).
- The case contract of rwb-case that reads the route state and answers the route fact, and the partner contract of rwb-partner that asks for a firm instruction, are published and faked; neither carries a dependency row and neither operation name is given by a source, so both carry the placeholder `Not specified in the source documents (GAP-2801; ASM-4641)`.
- The gateway-bff composite route `RWB-PLT-N001-CON` serves SCR-18 Notice approval and SCR-19 Litigation workspace; it is in the build list (DP-19), so both read surfaces are available from Day 1.
- LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`) and LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`) of TSD S4 T3.2 are read as values in force with their version. DP-07 is not in this story's pattern set and the read carries no dependency row either (GAP-2801; ASM-4641).
- The caller holds a Workbench role with a Litigation right on the operation it calls (TSD S4 T6.1). DP-08 is not in this story's pattern set: the declared right is enforced at the edge for the screen path, and the right on the write paths is this story's design.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant.

### 4. Flow

1. The litigation officer opens SCR-19 Litigation workspace through the gateway-bff composite route (DP-19); the workspace answers the legal actions of the case on `GET /legal-actions/{legalActionId}` of base `/api/recovery/litigation/v1` (API-S4-003): `action_type`, `status`, `court_name`, `claim_amount`, `law_firm_id`, `filed_date` and the court references.
2. On a dismissal the judgment story writes the judgment and rwb-case moves the case to `JUDGMENT_DISMISSED` under R-LIT-45 ("record the dismissal and open the appeal window", owner litigation officer, service level to the appeal window end). This service reads that route state from the case contract and starts its own durable window timer on `LitigationWorkflow` (the window length is `Not specified in the source documents (GAP-2805; ASM-4645)`).
3. On `APPEAL_WINDOW_OPEN` the officer opens the appeal on `POST /cases/{caseId}/legal-actions` (API-S4-002) with `LegalActionRequest`: `actionType = APPEAL`, `courtName`, `claimAmount`, `lawsuitNo` and `blackCaseNo` where the firm already knows them.
4. `AppealValidator` checks the case reference, the value of `actionType` against LOV-LEGAL-TYPE, the required fields of an appeal and the caller's scope; a failed check answers 422 or 404 and nothing is written.
5. `AppealDecisionRule` evaluates R-LIT-46 — from `JUDGMENT_DISMISSED`, event `APPEAL_WINDOW_OPEN`, condition "appeal_window_ends is in the future", action "the agent proposes appeal or accept with cost and effect", to `APPEAL_DECISION`, owner "Approver at D7.4", service level "to the window end" — and `AppealDecisionWriter` writes one decision record through the local library **before** the row changes: rule ID, version in force, the inputs reference that carries the grounds, the final call and the decision code read from LOV-DECISION.
6. `LegalActionWriter` writes, in one `rwb_litigation` transaction, the `legal_action` row with status `OPEN`, `action_type = APPEAL`, `court_name`, `claim_amount`, `law_firm_id` where it was given, plus the idempotency row of the request.
7. `AppealApprovalClient` takes the decision to the approver at D7.4 on the approval contract: case reference, legal action reference, decision code, capability area, product group, the amount the limit is read against, `sourceType`, `sourceRef`, rule ID and version, `Idempotency-Key`; one hop, 2 s, breaker per downstream. R-LIT-47 grants inside the limit or on the Head of Litigation's approval above it.
8. On a granted answer `FirmInstructionClient` asks rwb-partner to instruct the firm to appeal, and `HearingTimerReset` resets the hearing timers of `LitigationWorkflow`. `CaseRouteClient` announces `APPEAL_FILED` with rule R-LIT-47 and its version; rwb-case writes the case and this service writes no case row.
9. When the firm confirms the filing, the officer records it on `PATCH /legal-actions/{legalActionId}` (API-S4-004) with `LegalActionUpdate`: `filedDate`, `courtName`, `blackCaseNo`, `lawsuitNo`. The row moves to `FILED` in the same transaction; the update is idempotent on its `Idempotency-Key`.
10. On `APPEAL_HEARING_SET` the court date is written by the hearing story on `hearing` (API-S4-005) and R-LIT-48 returns the case to `IN_HEARING`; this service announces the fact to rwb-case and holds the new timer. On `APPEAL_DECLINED` R-LIT-49 records the reason on the decision record, the legal action moves to `WITHDRAWN` and the case is announced for `TO_WRITE_OFF`, which the write-off stories carry.
11. A repeated create with the same case, action type and amount, or with the same `Idempotency-Key`, writes nothing and sends no second approval request; the repeat is counted under R-UNI-40.
12. SCR-19 and SCR-18 read the legal action, its states and the warnings from this service through the composite route, read only, next to the case route state of rwb-case and the approval of rwb-decision.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no `actionType`, no `courtName`, or a value of `actionType` that is not in LOV-LEGAL-TYPE | The answer is 422 and nothing is read beyond the validator; no decision record and no row | MSG-GEN-001 | AC1 |
| X2 | The case ID names no case in the caller's scope, or the legal action ID names no row | The answer is 404 and nothing is written; an out-of-scope case cannot be told from a missing one | None | AC1 |
| X3 | The legal action is not in status `OPEN`, or `actionType` is not a value of LOV-LEGAL-TYPE | The answer is 409 and nothing changes | None | AC1 |
| X4 | The claim expiry of the case falls inside the filing window | The MSG-S4-002 warning is shown with the date, and nothing is blocked; the prescription date is a fact of the case of record | MSG-S4-002 | AC1 |
| X5 | The case route state is not `JUDGMENT_DISMISSED` when the appeal is proposed, or the window has already ended | R-LIT-46 does not fire; the answer is 409, nothing is written and no approval is requested | None | AC1 |
| X6 | A role without the Litigation right records, reads or patches the appeal | Refused before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1 |
| X7 | The local decision-record write fails | The transaction writes nothing: the legal action keeps its previous status and its empty filing facts, no approval is requested and no case fact leaves the service | MSG-P7-003 | AC2 |
| X8 | The approval is refused at D7.4, or the approver accepts the judgment | R-LIT-49 records the reason on the decision record, the legal action moves to `WITHDRAWN`, no instruction is asked and the case is announced for write-off | None | AC1 |
| X9 | The approval, the case or the partner contract does not answer inside 2 s, or its breaker is open | The legal action keeps what it wrote, because that fact is true and this service's own; the answer is 503 with the platform error envelope and the hand-off is re-run by repeating the same `Idempotency-Key` | None | AC1 |
| X10 | The case answer refuses the route fact | The legal action keeps what it wrote, the refusal is recorded for the case owner and the caller reads the answer of the case contract unchanged; this service does not move the case itself | None | AC1 |
| X11 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | BR4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5014-CON`, the decision-record library and the composite route; the approval, case, partner and reference-data contracts are consumed and faked, and the missing dependency rows are recorded (GAP-2801) |
| Negotiable | The appeal window length, the D7.4 limit, the grounds and the list values are versioned reference data; the story fixes the behaviour and the shapes, not the values |
| Valuable | The appeal is decided, approved, filed and tracked on one legal action with a decision record before it moves, which is the window that R-LIT-45 to R-LIT-49 exist to protect |
| Estimable | Three operations, one validator, four rule evaluations, one library write, one repository write, three clients, one durable timer and one read-only screen fragment |
| Small | Fits two weeks with its tests, as the primary slice of the legacy key |
| Testable | Each of the two criteria of section 7 is one end-to-end test with the cross-service answers stubbed in the contract fakes; the contract half is tested in `RWB-S4-E5014-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Decide and manage an appeal, in rwb-litigation

  Background:
    Given the appeal legal action "LA-2026-000714" exists on case "RC-2026-000714" with action type "APPEAL"
    Given the rule package of R-LIT-45 to R-LIT-49 is in force at its version, and LOV-LEGAL-TYPE and LOV-LEGAL-STATUS are read with their version in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Decide and manage an appeal (legacy RWB-E5-014 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-decision contract mock returns the approval granted at D7.4 for "LA-2026-000714"
    Given the rwb-case contract mock returns the case state "JUDGMENT_DISMISSED" for "RC-2026-000714"
    Given the rwb-partner contract mock returns the appeal instruction accepted for "LA-2026-000714"
    When the user acts on the screen
    Then records the appeal decision, the grounds and the approval, and tracks it to its end
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E5-014 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

These two criteria are the legacy criteria of RWB-E5-014, copied word for word: not one legacy line is reworded, shortened or renumbered, and every value of the source (MSG-P7-003, the decision log, the rule version) is kept character for character. The only additions are the origin tag on each `Scenario:` line and, inside AC1, one `Given` line per cross-service answer that a source does not give in process: the approval at D7.4 of rwb-decision, the case route state `JUDGMENT_DISMISSED` of rwb-case and the firm instruction of rwb-partner are answered by their contract fakes; every other line and every value is unchanged. The route states of AC1 (`JUDGMENT_DISMISSED`, `APPEAL_DECISION`, `APPEAL_FILED`, `IN_HEARING`, `TO_WRITE_OFF`) are case route states of rwb-case, moved by rwb-case on the announcement of this service (BR3); the status of the appeal legal action itself takes only LOV-LEGAL-STATUS values (section 9). The grounds and the appeal window are values no source stores (GAP-2802; GAP-2805). The contract half of these surfaces is tested in `RWB-S4-E5014-CON`, and the end-to-end journey across the services is not claimed here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| R-LIT-45 | Litigation · D7 · from `IN_HEARING` · event `JUDGMENT_AGAINST_THE_BANK` · condition "judgment_type = dismissed" · action "record the dismissal and open the appeal window" · to `JUDGMENT_DISMISSED` · owner "Litigation officer" · channel "LIT, Partner Portal" · service level "to the appeal window end" | Business Rules and Routing Logic v4 (R-LIT-45); FSD S4 A2.16.3.1 |
| R-LIT-46 | Litigation · D7 · from `JUDGMENT_DISMISSED` · event `APPEAL_WINDOW_OPEN` · condition "appeal_window_ends is in the future" · action "the agent proposes appeal or accept with cost and effect" · to `APPEAL_DECISION` · owner "Approver at D7.4" · channel "Workbench, Committee View" · service level "to the window end" | Business Rules and Routing Logic v4 (R-LIT-46) |
| R-LIT-47 | Litigation · D7 · from `APPEAL_DECISION` · event `APPEAL_APPROVED` · condition "inside the limit, or the Head of Litigation approves above it" · action "instruct the firm to appeal and reset the hearing timers" · to `APPEAL_FILED` · owner "Panel law firm" · channel "Partner Portal, LIT" · service level "to the filing deadline" | Business Rules and Routing Logic v4 (R-LIT-47) |
| R-LIT-48 | Litigation · D7 · from `APPEAL_FILED` · event `APPEAL_HEARING_SET` · condition "the court sets the appeal hearing" · action "return the case to the hearing calendar" · to `IN_HEARING` · owner "Panel law firm" · channel "LIT, Workbench scheduler" · service level "to the hearing date" | Business Rules and Routing Logic v4 (R-LIT-48) |
| R-LIT-49 | Litigation · D7 · from `APPEAL_DECISION` · event `APPEAL_DECLINED` · condition "the approver accepts the judgment, or the window has passed" · action "record the reason and route the case to write-off" · to `TO_WRITE_OFF` · owner "Write-off team with Credit Administration" · channel "Workbench" · service level None | Business Rules and Routing Logic v4 (R-LIT-49) |
| BR1 | The appeal is a `legal_action` row of this service: `action_type` takes the value `APPEAL` of LOV-LEGAL-TYPE, and the court references, the claim amount and the filing facts are written on that row and nowhere else | TSD S4 T3.1, T3.2; legacy Data block; FSD S4 A2.14.3.2 |
| BR2 | The decision is written before the legal action changes: one record through the local decision-record library with the rule ID and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 |
| BR3 | The case move is answered, not written: `JUDGMENT_DISMISSED`, `APPEAL_DECISION`, `APPEAL_FILED`, `IN_HEARING` and `TO_WRITE_OFF` are route states of rwb-case, so this service announces the fact with the rule and its version and accepts the answer; no `recovery_case` row is written and no case rule is evaluated here | R-LIT-45 to R-LIT-49; legacy Data block (recovery_case, owner P3) |
| BR4 | No ACE read: this story reads no `v_ace_*` view, no ACE table and no other `rwb_*` schema, and its login holds no such grant | DP-01 and DP-05 used as a prohibition; TSD S4 T3.1 (DF-LEG-013 arrives through the owner) |
| BR5 | The same request twice, or the same `Idempotency-Key` twice, writes once, sends no second approval request and counts the repeat | R-UNI-40; TSD S4 T-A.1 (API-S4-002 `Idempotency-Key` header) |
| BR6 | Closed vocabulary: `action_type` and `status` take only the values of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS in force, read with their version; the window length, the filing deadline and the limit are versioned reference rows and are never written in code | TSD S4 T3.2; FSD S4 A2.14.3.1 (BR-S4-014); Template and Rules section R7.2 (s17) |
| BR7 | No personal data: the row, the decision record, the log and every call carry identifiers, list values, court references, dates and amounts only | TSD S4 T3.1; FSD S4 A2.14.3.2 (Personal data: No) |
| R-UNI-39 | An action whose decision cannot be recorded does not proceed and nothing moves | Business Rules and Routing Logic v4 (R-UNI-39); legacy AC2 |
| R-UNI-40 | The same event or the same request twice produces one effect, and the repeat is counted | Business Rules and Routing Logic v4 (R-UNI-40) |

Two values R-LIT-46 to R-LIT-49 depend on have no definition in any source read for this key and are therefore evaluated as versioned reference rows, never as code: the length of the appeal window and the filing deadline (`Not specified in the source documents (GAP-2805; ASM-4645)`), and the appeal grounds, which travel in the inputs reference of the decision record (`Not specified in the source documents (GAP-2802; ASM-4642)`).

### 9. State transitions

This story moves the status of its own legal action and announces route facts of the case. The two are different objects and are never used one for the other.

**`legal_action.status`** — the six values of LOV-LEGAL-STATUS (TSD S4 T3.2), moved by this service:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The appeal is opened on API-S4-002 | `actionType = APPEAL`, the request validates and the decision record is written | `OPEN` |
| `OPEN` | The approval at D7.4 is granted under R-LIT-47 | The firm is instructed and the hearing timers are reset | `OPEN`, with the approval and the instruction on the record |
| `OPEN` | The filing is recorded on API-S4-004 | `filedDate` and the court references are written | `FILED` |
| `OPEN` | The approval is refused, or the approver accepts the judgment under R-LIT-49 | The reason is on the decision record and the case is announced for write-off | `WITHDRAWN` |
| `FILED` | The appeal judgment is recorded | `judgmentDate` and `judgmentAmount` are written | `JUDGMENT` |
| `JUDGMENT` | Enforcement of the appeal judgment opens | The enforcement step is recorded | `ENFORCING` |
| `ENFORCING` or `FILED` | The case is closed or the appeal withdrawn | The closing step of the case of record | `CLOSED` or `WITHDRAWN` |

No value of LOV-LEGAL-STATUS names an appeal decision or a refused appeal, so the decision and the refusal live on the decision record and the row uses `OPEN`, `FILED` and `WITHDRAWN` only; that ruling is carried as (GAP-2804; ASM-4644).

**Case route states** — rwb-case's, announced by this story and written there (BR3):

| From (rwb-case) | Rule | To (rwb-case) | Owner of the move |
|---|---|---|---|
| `IN_HEARING` | R-LIT-45, on `JUDGMENT_AGAINST_THE_BANK` with judgment_type dismissed | `JUDGMENT_DISMISSED` | rwb-case, with the judgment story `RWB-S4-E5016-APP` |
| `JUDGMENT_DISMISSED` | R-LIT-46, on `APPEAL_WINDOW_OPEN` while the window is in the future | `APPEAL_DECISION` | rwb-case, on the announcement of this service |
| `APPEAL_DECISION` | R-LIT-47, on `APPEAL_APPROVED` | `APPEAL_FILED` | rwb-case, with the firm instruction of rwb-partner |
| `APPEAL_FILED` | R-LIT-48, on `APPEAL_HEARING_SET` | `IN_HEARING` | rwb-case, with the hearing story `RWB-S4-E5011-APP` |
| `APPEAL_DECISION` | R-LIT-49, on `APPEAL_DECLINED` | `TO_WRITE_OFF` | rwb-case, with the write-off stories |

Neither the case row nor its route state is read as a table or written here; the case read and the announcements of 12.2 are the only paths by which they move (GAP-2801; ASM-4641).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA (TSD S4 T6.1): opens, reads and patches the appeal, records the decision, its grounds and the filing; the primary role of FSD S4 A2.14.3.3 |
| RW-ENFORCE, enforcement owner | Litigation CRU: opens, reads and patches the appeal in scope |
| RW-HEADLIT, Head of Litigation | Litigation RA, and the above-limit approval of R-LIT-47, which is taken on the approval contract of rwb-decision and not here |
| RW-LEGAL, legal counsel | Litigation RA: reads the appeal and its facts; approves nothing here |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read the appeal and its facts only |
| RW-PRODHEAD, product head | Litigation RA: read, with the acknowledgement right the matrix gives |
| rwb-litigation service identity | Validates, evaluates R-LIT-45 to R-LIT-49, writes the decision record and the row, holds the durable timers, and calls the approval, case and partner contracts; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-decision (P7) service identity | Owns the approval item, the D7.4 limit and the above-limit approval of the Head of Litigation; answers granted or refused |
| rwb-case (P3) service identity | Owns the case of record and the five route states of section 9; answers the route facts |
| rwb-partner (S9) service identity | Owns the panel, the firm instruction and the firm's result; answers the instruction request |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The D7.4 approver that R-LIT-46 routes to holds its right in rwb-decision and rwb-access, and the role code of that approver is `Not specified in the source documents (GAP-2804; ASM-4644)`. DP-08 is not in this story's pattern set: the declared right of each operation is enforced at the edge for the screen path, and the guard on the write paths is this story's design. A refusal keeps MSG-P4-002 and changes nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Write on create; read as the reference of every call and answer |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Write on create; read and sent on the approval, case and partner calls |
| DF-LEG-003 | legal_action (S4, `rwb_litigation`) | law_firm_id | Write when the panel selected the firm; read |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Write, `APPEAL` of LOV-LEGAL-TYPE |
| DF-LEG-005 | legal_action (S4, `rwb_litigation`) | lawsuit_no | Write on the filing step |
| DF-LEG-006 | legal_action (S4, `rwb_litigation`) | black_case_no | Write on the filing step |
| DF-LEG-007 | legal_action (S4, `rwb_litigation`) | red_case_no | Write on the filing step where the appeal court issues one |
| DF-LEG-008 | legal_action (S4, `rwb_litigation`) | court_name | Write on create and on the filing step |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Write on create; the amount the D7.4 limit is read against |
| DF-LEG-010 | legal_action (S4, `rwb_litigation`) | filed_date | Write on the filing step; its presence moves the status to `FILED` |
| DF-LEG-011 | legal_action (S4, `rwb_litigation`) | judgment_date | Write when the appeal judgment is recorded; read before |
| DF-LEG-012 | legal_action (S4, `rwb_litigation`) | judgment_amount | Write with the appeal judgment; read before |
| DF-LEG-013 | legal_action (S4, `rwb_litigation`) | lit_status | Read only; the court status that arrives from LIT through COLLINS and rwb-source-data |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write, against LOV-LEGAL-STATUS (`OPEN`, then `FILED` or `WITHDRAWN`) |
| Standard columns | legal_action (S4, `rwb_litigation`) | state, version, created_at, created_by, updated_at, updated_by, is_active | Written by the service identity (TSD S4 T3.0) |
| Decision record elements | decision record (PLT library, created in `rwb_litigation`) | decision code, rule ID, rule version, inputs reference, final call, decided at, the two hashes | Write through the local library, before the legal action changes (DP-03) |
| Approval elements | approval (P7, `rwb_decision`) | the item the appeal raises: case, legal action, decision code, capability area, level, limit version, product group, amount, preparer, due time, source type and reference, rule and version | Sent on the approval call and stored nowhere here |

Field IDs are those of TSD S4 v2 T3.1 and the standard columns of T3.0; the decision-record and approval elements are named by their contracts and no field of another owner is restated. **No new table, no new column and no migration:** `legal_action` arrives with the S4 schema of this service and its contract story `RWB-S4-E5014-CON` publishes the DDL template, which the service's own Flyway applies (DP-15); `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's migration (DP-03). The appeal grounds and the appeal window end have no column in this row and are not added (GAP-2802; ASM-4642).

**Not written, not read as a table, and named so that a reviewer can check the absence:** `recovery_case` and its route state, DF-CAS-001 to DF-CAS-023 (P3 rwb-case); `decision_log_entry` and `rule_row`, DF-DEC-001 to DF-DEC-018 and DF-REF-001 to DF-REF-015 (P7 rwb-decision); `document` (P5 rwb-document); `partner` (S9 rwb-partner); `notice` (P6 rwb-comms); `hearing`, DF-LEG-024 to DF-LEG-029 (S4, owned by the hearing story `RWB-S4-E5011-APP`); and every `v_ace_*` view (P1 rwb-source-data). `legal_action.case_id` and `law_firm_id` are identifiers, not foreign keys across schemas (DP-01, BR4).

**No personal data.** The row this story writes carries identifiers, list values, court references, dates and one amount. The borrower, the guarantor, the address and the identity number never enter `rwb_litigation`: they are held by ACE and reached only through rwb-source-data by the services that need them, and they are not logged and not put on any call.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13).

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S4-002 | POST | `/cases/{caseId}/legal-actions` | Open the appeal: the legal action of action type `APPEAL` and the decision record of R-LIT-46 (TSD S4 T-A.2) | Litigation C, scope applied | `Idempotency-Key` header required; the answer is stored and a repeat returns it |
| API-S4-003 | GET | `/legal-actions/{legalActionId}` | Read the legal action with its pack, instruction, hearings and judgment (TSD S4 T-A.2) | Litigation R, scope applied | Not applicable |
| API-S4-004 | PATCH | `/legal-actions/{legalActionId}` | Record the filing of the appeal, its judgment or an enforcement step (TSD S4 T-A.2) | Litigation U, scope applied | `Idempotency-Key` header required |

The three operations and their IDs, rights and error sets are those of TSD S4 T-A.1 and T-A.2; they keep their legacy IDs and differ only in the base, which DP-13 renames. Errors: 401 no session; 403 no right (MSG-P4-002); 404 unknown or out-of-scope reference; 409 a status or an action type that refuses the step, or a case that is not in `JUDGMENT_DISMISSED`; 422 a missing or invalid field (MSG-GEN-001); 503 the decision-record library or a consumed contract unavailable. The hearing operation API-S4-005 and the notice approval API-S4-001 belong to other stories of this service and are not served here. The request and answer shapes are declared by `RWB-S4-E5014-CON`, which this story consumes as its first build dependency.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The approval request and its answer of the rwb-decision approval contract, base `/api/recovery/decision/v1` | P7 rwb-decision | Takes the appeal decision to the approver at D7.4 and reads the granted, refused or delayed answer of R-LIT-47. The operation that raises an item is `Not specified in the source documents (GAP-2801; ASM-4641)` |
| The case read and the route facts of rwb-case, operation `Not specified in the source documents (GAP-2801; ASM-4641)` | P3 rwb-case | Reads the route state, the product group and the claim expiry the warning shows, and announces `APPEAL_DECISION`, `APPEAL_FILED`, `IN_HEARING` and `TO_WRITE_OFF` with the rule and its version |
| The firm instruction request of rwb-partner, operation `Not specified in the source documents (GAP-2801; ASM-4641)` | S9 rwb-partner | Asks for the instruction to appeal on a granted decision; the instruction, its pack and its result are `RWB-S4-E5009-APP`'s and the partner stories' |
| The reference-data read of LOV-LEGAL-TYPE and LOV-LEGAL-STATUS | P3 rwb-case | The two list codes at their version in force (DP-07, declared here although the pattern is not in this story's set; GAP-2801) |

Every row is one hop with a 2 s timeout and a breaker per downstream (ADR-020). Each carries the missing dependency of GAP-2801 and is built against its fake. No operation of another service is declared as provided here (BR1).

#### 12.3 Events published

None. The ownership rows of rwb-litigation carry no event of its own, and DP-09 is not in this story's pattern set, so this story adds no outbox row and no producer. The decision record is written through the local decision-record library of DP-03, which publishes `DecisionRecorded` on the shared `rwb.decision-record.v1`; that element is the library's and this service declares no payload of its own. The service topic `rwb.litigation.events.v1` with its retry and `.dlt` topics is reserved by the naming rule and stays unpublished by this story.

#### 12.4 Events consumed

None. The approval answer, the case answer and the partner answer are synchronous answers of their contracts, not topics, so this story subscribes to no topic, holds no consumer and uses no inbox of its own. The rule events of R-LIT-45 to R-LIT-49 (`JUDGMENT_AGAINST_THE_BANK`, `APPEAL_WINDOW_OPEN`, `APPEAL_APPROVED`, `APPEAL_HEARING_SET`, `APPEAL_DECLINED`) are evaluated in this service from its own facts and the case read, not consumed from a topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LitigationWorkflow | Workflow, one run per case stage, the S4 child of CaseWorkflow | `rwb-litigation` | Holds the appeal window timer, the filing deadline and the reset hearing timers; started by CaseWorkflow on rwb-case |
| openAppeal | Activity | `rwb-litigation` | The validator, the R-LIT-46 evaluation and the row write of steps 3 to 6 |
| recordDecision | Activity through the library | `rwb-litigation` | The local decision record and its outbox row, written before the change (DP-03) |
| requestApproval | Activity | `rwb-litigation` | The D7.4 approval call to rwb-decision and the answer it returns |
| instructFirm | Activity | `rwb-litigation` | The instruction request to rwb-partner and its answer |
| recordFiling | Activity | `rwb-litigation` | The filing fact of API-S4-004 and the status move to `FILED` |
| announceCaseRoute | Activity | `rwb-litigation` | The route fact to rwb-case and its answer |
| appealApproval | Child workflow, owner rwb-decision | `rwb-decision` | The D7.4 approval and its clock, built against its fake (GAP-2801; ASM-4641) |

The workflow name is fixed by the temporal design (`LitigationWorkflow` on `rwb-litigation`); the appeal step is a step of that workflow and not a workflow of its own, and no activity is registered by a contract document. The child workflow's own type name, workflow ID and queue registration are given by no source read here (GAP-2801; ASM-4641).

#### 12.6 Schedules

None. The appeal window and the filing deadline are durable timers of `LitigationWorkflow`, started when the case read answers `JUDGMENT_DISMISSED` and cleared when the appeal is filed or declined. No Temporal Schedule and no Quartz job is owned, moved or registered here, and their lengths are the reference rows of GAP-2805.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (rwb_litigation) | The appeal row, its court references, its filing facts and its status DF-LEG-014 |
| decision_record | PLT library, created in `rwb_litigation` | The hash-linked record of each R-LIT-46 to R-LIT-49 answer, written before the change (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the create and of the patch, with the stored answer |

Not owned and never written: `recovery_case` and its route state (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `partner` (S9), `notice` (P6) and `hearing` (S4, the hearing story's). No `v_ace_*` view and no ACE table is read (BR4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision approval WireMock | The D7.4 item for `LA-2026-000714` at the level the limit gives, granted, refused with a reason, approved above the limit by the Head of Litigation, and delayed beyond 2 s | AC1, X8, X9 |
| rwb-case WireMock | Case `RC-2026-000714` at route state `JUDGMENT_DISMISSED` with its product group and claim expiry; each route fact accepted, a refusal from the wrong state, and a delayed answer | AC1, X5, X10 |
| rwb-partner WireMock | The appeal instruction of `LA-2026-000714` accepted with the firm reference, and a refusal for a firm outside the panel | AC1, X9 |
| decision-record library stub | A healthy chain with its outbox row, and a stopped chain for the fail-closed test | AC1, AC2 |
| reference-data WireMock | LOV-LEGAL-TYPE and LOV-LEGAL-STATUS at their version in force, and the window-length and filing-deadline rows at theirs | AC1, X5 |
| gateway-bff composite route fake | The merged SCR-18 and SCR-19 answer for `RC-2026-000714`, with the legal action read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and `RWB-S4-E5014-CON` or against the approval, case and partner documents is a build failure.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | API-S4-002, API-S4-003 and API-S4-004 provided; the approval, the case read and route facts, the firm instruction and the reference data consumed; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story; `DecisionRecorded` is the library's element (12.3) |
| Temporal | 1 workflow, 6 activities, 1 child workflow, no Schedule | LitigationWorkflow, its six activities, the appeal window timer and the approval child on `rwb-decision` |
| File | None | No file is read, built or delivered here; the pack and the grounds document are rwb-document's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `appeal`, Java package `th.co.scb.ace.workbench.recovery.litigation.appeal`; front end `src/modules/recovery/litigation/Appeal.tsx`, the fragment SCR-19 and SCR-18 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/litigation/v1`; the three operations keep API-S4-002, API-S4-003 and API-S4-004 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 carries legacy AC1's "writes the result to the decision log with the rule version" and legacy AC2's fail-closed behaviour. DP-13 renames the base and keeps the operation IDs, which is why the legacy endpoint block names two of the three operations and this story serves all three. DP-19 covers the two screens only, and the screen model and merge order stay with the edge contract.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the metadata also carries and nothing else. Four consumed surfaces have no row at all: the approval contract (P7), the case contract that reads the route state and answers it (P3), the partner instruction contract (S9) and the reference-data read of DP-07, with DP-08's declared right in the same position; the four are recorded once as GAP-2801 with ASM-4641. The story builds against their fakes on Day 1 and no C dependency blocks the build (Template and Rules section R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| LegalActionController | Controller | API-S4-002, API-S4-003 and API-S4-004 with the problem mapping for 401, 403, 404, 409, 422 and 503 |
| AppealValidator | Service | The case and the caller's scope, the `actionType` value of LOV-LEGAL-TYPE, the required appeal fields and the status the step needs |
| AppealDecisionRule | Service through the embedded Drools kit | R-LIT-45 to R-LIT-49 on the case route state and the reference rows in force; the version is pinned and recorded |
| AppealDecisionWriter | Library adapter | One hash-linked record per decision with the rule ID and the version in force, before any change; refuses the request when the write fails (DP-03) |
| LegalActionWriter | Repository | The `legal_action` row, its status and the idempotency row, in one `rwb_litigation` transaction |
| AppealApprovalClient | Client | The D7.4 approval call, one hop, 2 s, breaker, no retry of its own |
| FirmInstructionClient | Client | The instruction request to rwb-partner, one hop, 2 s, breaker; the instruction itself is not built here |
| CaseRouteClient | Client | The case read and the four route facts to rwb-case, one hop, 2 s, breaker |
| HearingTimerReset | Service | The reset of the hearing timers of R-LIT-47 and the new timer of R-LIT-48 on `LitigationWorkflow` |
| LitigationWorkflow | Workflow | The stage on `rwb-litigation` and its appeal step, window timer and filing deadline |
| Appeal | React component | Shows the appeal, its status, the court references, the approval state and the grounds reference on SCR-19 and SCR-18, read only |

**Database and migrations.** No Flyway file of its own. `legal_action` arrives with the S4 schema and the DDL template of `RWB-S4-E5014-CON`; the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). This story needs a lookup by `case_id` for the workspace read and by `id` for the two single-row operations, and creates no index beyond what the contract template declares.

**Configuration and reference data.**

- The appeal window length and the filing deadline of R-LIT-46 and R-LIT-47, as versioned reference rows read with their version. Their content is `Not specified in the source documents (GAP-2805; ASM-4645)`.
- The D7.4 limit and the above-limit approval of the Head of Litigation are rwb-decision's rows and are not configured here.
- LOV-LEGAL-TYPE and LOV-LEGAL-STATUS at their version in force (TSD S4 T3.2).
- The decision codes of the appeal decisions, read as values of LOV-DECISION at its version in force.
- The 2 s budget and the single hop are the platform rule of ADR-020 and not a value of this story.

**Build steps**

1. Build `AppealValidator` and `LegalActionWriter` over the `legal_action` row and the contract fake; test AC1 and X1 to X3.
2. Build `AppealDecisionRule` and `AppealDecisionWriter` against the library fake, with the stopped chain; test AC1, AC2 and X5.
3. Build `AppealApprovalClient` against the approval fake, with the 2 s budget, the breaker, the above-limit approval, the refusal and the delayed answer; test AC1, X8 and X9.
4. Build `CaseRouteClient` against the case fake, with the four route facts, the refusal and the delayed answer; test AC1, X5 and X10.
5. Build `FirmInstructionClient`, `HearingTimerReset` and the filing step of API-S4-004; test AC1.
6. Build the window timer and its reference rows on `LitigationWorkflow`; test X5.
7. Build `Appeal` and read the legal action through the composite route fake; test AC1.
8. Add the boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision`, `rwb_document`, `rwb_partner`, `rwb_comms` or `rwb_litigation.hearing`; test X11.

**Feature flag.** `rwb.litigation.appeal-v1`, read as a flag of the platform library; off means the appeal create answers 404 and the litigation workspace shows no appeal action, while the read and patch of an existing legal action are unaffected.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-S4-E5014-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one appeal per dismissal, one approval per appeal, one instruction per granted appeal, one filing fact per filing, one decision record per fork, no write of a case, ledger, partner or hearing row from this service, and no `v_ace_*` read in its logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, and the pack check that raises it is a pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim expiry of the case falls inside the filing window (X4) | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the request is missing (X1) | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the Litigation right of the operation (X6) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes (X7, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-014 section 14 and are copied unchanged; no message is reworded and no message identifier is added. `MSG-GEN-001` is displayed with the field it names. `MSG-S4-001` is authored by the pack stories of this service and is carried here because it is the message set of the key; this story raises it on no path. `MSG-S4-002` carries the claim expiry date read from the case of record, and the filing window behind it is `Not specified in the source documents (GAP-2805; ASM-4645)`. A downstream that does not answer (X9) and a reference that is not found (X2) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-18 Notice approval | Generated | The notices of the case, read only; the appeal does not generate one |
| SCR-18 Notice approval | Approved, Sent, Delivered, Unserved | The notice states of the case, read only, from the notice stories of this service |
| SCR-18 Notice approval | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | Pack | The dismissed case with the appeal window open and the proposal of R-LIT-46 to appeal or accept, with its cost and effect |
| SCR-19 Litigation workspace | Instructed | The appeal decided and approved at D7.4, the firm instructed and the hearing timers reset, with the approval level and its due date |
| SCR-19 Litigation workspace | Filed | The filing date, the court name and the black and red case numbers on the legal action, and the status `FILED` |
| SCR-19 Litigation workspace | Hearing | The appeal hearing on the calendar, read only, from the hearing story of this service |
| SCR-19 Litigation workspace | Judgment | The appeal judgment date and amount, read only |
| SCR-19 Litigation workspace | Not recorded | MSG-P7-003, and the legal action unchanged with no approval requested |
| SCR-19 Litigation workspace | Declined | The reason of R-LIT-49 on the decision record, the status `WITHDRAWN` and the case announced for write-off |
| SCR-19 Litigation workspace | Failed | A 503 when a consumed contract did not answer; the legal action keeps what it wrote |

The states are the ones the legacy screen block of RWB-E5-014 gives, copied unchanged: SCR-18 carries Generated, approved, sent, delivered and unserved, and SCR-19 carries Pack, instructed, filed, hearing and judgment. The appeal appears on SCR-19 from the moment the window opens and moves through the same five states, with `Declined` and `Not recorded` carried from legacy AC1 and AC2. Neither screen moves the case, and the route state of the case of record stays rwb-case's (BR3). The route merges this service's answer with the case of rwb-case and the approval of rwb-decision; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON`, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-014-01 | AC1 | End to end | Appeal `LA-2026-000714` on case `RC-2026-000714`, action type `APPEAL`; the approval fake granted at D7.4; the partner fake accepting the instruction; the filing recorded with its date and court numbers; the case fake at `JUDGMENT_DISMISSED`; rule ID and version on the decision record |
| TC-E5-014-02 | AC2 | End to end | The decision-record library stubbed to stop the chain; the legal action unchanged, no approval requested and MSG-P7-003 on the screen |
| TC-E5-014-03 | Access | Component | A role without the Litigation right sends API-S4-002 and reads API-S4-003; refused with MSG-P4-002 and nothing written |
| TC-E5-014-04 | Principle 5 | NFR | A forced decision-record write failure on 10 appeals; no legal action changes, no approval leaves the service and the incident is raised under R-UNI-39 |

The four identifiers are the legacy identifiers of RWB-E5-014 in their legacy order, with their legacy covers. The legacy level of the first two maps to `End to end` here, because the behaviour they prove crosses the case, the decision centre and the partner; the access case keeps its legacy `Access` cover at `Component`, and the forced-failure case keeps its legacy `Principle 5` cover at `NFR`. The contract half of every surface they touch is tested in `RWB-S4-E5014-CON` and the cross-service journey is not claimed here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the window length, the filing deadline, the list values and the decision codes are data with a version; no role, list value, state name, court name or amount appears in Java (BR6, FSD S4 BR-S4-014).
- No personal data in logs, tests, workflow inputs or prompts: the row carries identifiers, list values, court references, dates and amounts, and the customer's identity never enters this service or its history (BR7).
- ACE data only through the owner's contract or the owner's `v_ace_*` views: no component of this story reads an ACE view or an ACE table, and the service identity holds no `v_ace_*` grant (BR4).
- No read of another service's tables and no cross-schema join: the case, the approval, the firm, the pack and the notice are reached only on their contracts and their fakes (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; a hand-off is re-run by repeating the same `Idempotency-Key` and never by a silent resend.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the request with nothing changed (DP-03, R-UNI-39, MSG-P7-003).
- No event, no topic and no outbox row of this service: the decision record is the library's element, and the appeal's dates are durable timers of `LitigationWorkflow`, not Schedules (12.3, 12.4, 12.6).
- The two screens are read only; SCR-19 posts the appeal and the filing through the operations of section 12.1, and SCR-18 is a read.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Screens | Test cases |
|---|---|---|---|---|---|---|---|
| No requirement ID in the legacy master (GAP-2803; ASM-4643) | The appeal decision, its grounds and its approval are recorded and the appeal is tracked to its end | Epics 3 to 8 specification, E5 S4 row; FSD S4 v3 A2.14 | FEAT-LIT-14 | 08 Litigate and enforce | R-LIT-45, R-LIT-46, R-LIT-47, R-LIT-48, R-LIT-49, R-UNI-39, R-UNI-40, BR1 to BR7 | SCR-18, SCR-19 | TC-E5-014-01, TC-E5-014-02, TC-E5-014-03 |
| FEAT-LIT-14 | Decide and manage an appeal | Business Rules and Routing Logic v4 (R-LIT-45 to R-LIT-49) | FEAT-LIT-14 | 08 Litigate and enforce | R-LIT-46, R-LIT-47, R-LIT-49 | SCR-19 | TC-E5-014-01 to TC-E5-014-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-014, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned by this story and copied word for word in section 7 |
| Legacy test cases | TC-E5-014-01 to TC-E5-014-04, kept in legacy order |
| Requirement | The legacy master of RWB-E5-014 and the Epics 3 to 8 specification carry no REQ identifier for this feature, so the story traces to FEAT-LIT-14 until the PRD adds the identifiers (GAP-2803) |
| Contract half | RWB-S4-E5014-CON: the three operations, the appeal shape, the error envelope, the `Idempotency-Key` rule, the `legal_action` columns and the fakes |
| Sibling slices | RWB-S4-E5016-APP (the judgment and the dismissal), RWB-S4-E5011-APP (the hearings), RWB-S4-E5012-APP (the next-step proposal), RWB-S4-E5009-APP (the firm instruction) |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Temporal layer), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The case of record, its route states `JUDGMENT_DISMISSED`, `APPEAL_DECISION`, `APPEAL_FILED`, `IN_HEARING` and `TO_WRITE_OFF`, the case clock and the case decision record: rwb-case (P3) and the case-side story of this legacy family.
- The dismissal that opens the window and the judgment itself: `RWB-S4-E5016-APP`.
- The approval item, the D7.4 limit, the Head of Litigation's above-limit approval and their clock: rwb-decision (P7) and its approval contract story. The operation that raises an approval item is not published there (GAP-2801).
- The firm instruction itself, its pack, its lifecycle and the firm's result: `RWB-S4-E5009-APP` and rwb-partner (S9); this story asks for the instruction and records the filing.
- The hearings of the appeal and the `hearing` table (API-S4-005, DF-LEG-024 to DF-LEG-029): `RWB-S4-E5011-APP`.
- The next-step proposal of R-LIT-46 that the agent produces: `RWB-S4-E5012-APP`; this story reads it.
- The pack, its documents, its checklist, its custody and the document that carries the appeal grounds: rwb-document (P5) and the pack stories of this service, which also raise MSG-S4-001.
- The notices and their approval: rwb-comms (P6), the notice stories and API-S4-001.
- The court status that arrives from LIT through COLLINS and rwb-source-data: rwb-source-data (P1) and rwb-integration (P2).
- The write-off that R-LIT-49 routes to: the write-off stories of S7 (rwb-writeoff).
- The contract document itself: `RWB-S4-E5014-CON`.
- The roles, rights, scope and masking data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-18 and SCR-19: `RWB-PLT-N001-CON` and the edge stories.
- The deployment of this build, its flag, its dashboards, its alerts and its runbook: its own OPS story.
- The cross-service journey of the appeal across rwb-litigation, rwb-case and rwb-decision with live owners: the wave 3 integration harness.
