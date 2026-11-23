# RWB-S6-E5025-APP Prepare the masked data tape

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E5025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP19 |
| Parallel lane | L-S6-C |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the masked-tape slice of RWB-E5-025 split out for rwb-debtsale. The three legacy acceptance criteria this story owns are kept word for word with their origin tag. The step is one activity of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`: it evaluates R-DS-10 on an approved lot, reads the personal facts of the accounts on the rwb-source-data data product, masks them under a versioned rule set and scans the tape for an unmasked identifier under R-DS-11 and R-DS-12. It stores the masked tape as a claim-check file of rwb-document (P5), records the outcome through the local decision-record library before anything is stored (DP-03) and answers the case move `TAPE_PREPARED` or `TAPE_REJECTED` to rwb-case (P3). It serves no REST operation of its own; SCR-25 reaches it through the gateway-bff composite route (DP-19). The masking rule set, the tape layout, the tape's storage reference and the mapping of the FSD's "PII service" are given by no source, and the plan's empty C row does not name the four consumed contracts, so one combined gap and six default rulings are recorded (GAP-3014; ASM-4990 to -6). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer (RW-DEBTSALE)**, I want **the Workbench to build the data tape with personal data masked under PDPA, ready for the data room**, so that **debt sales run on approved lots and masked data**.

This is the masked-tape slice of legacy RWB-E5-025. It owns:

- the three legacy acceptance criteria (AC1, AC2 and AC3), copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one step of `DebtSaleWorkflow` on task queue `rwb-debtsale` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case and as the saga step that follows the committee approval and precedes the data room;
- the evaluation of R-DS-10 on an approved lot: the trigger `TAPE_BUILD_RUN`, the tape built under the PII masking rules and the case-move answer `TAPE_PREPARED`;
- the masking check of R-DS-11 and the rebuild of R-DS-12 on the tape this step has just built, so that an unmasked identifier stops the tape before any buyer can see it (REQ-S6-003);
- the read of the account and borrower facts the tape carries on the rwb-source-data data product, masked inside the step and never written to `rwb_debtsale` (GAP-3014; ASM-4991);
- the read of the masking rule set at its version as reference data, with no masking pattern in code (BR-S6-003) (GAP-3014; ASM-4990);
- the decision record of the outcome, written through the local decision-record library before the tape is stored (DP-03);
- the tape itself as a claim-check file of rwb-document (P5), with its document reference, checksum and masking-check result (GAP-3014; ASM-4992);
- the answer to rwb-case for the case move `TAPE_PREPARED` or `TAPE_REJECTED`, with the rule ID and the version that produced it;
- the tape-prepared indication of SCR-25 Lot builder behind the gateway-bff composite route (DP-19).

It does not own: any REST operation, because the lot read is API-S6-002 of RWB-S6-E5024-APP and the data-room read is API-S6-004 of RWB-S6-E5026-APP, and the published shapes of those two reads and their elements are RWB-S6-E5024-CON and RWB-S6-E5026-CON; the selection, the lot build and the price estimate, which are RWB-S6-E5023-APP and RWB-S6-E5024-APP; the committee approval, the reserve decision and the route state `LOT_APPROVED`, which are RWB-S6-E6001-APP's; opening the data room under R-DS-13, the buyer qualification, the bids and the award, which are RWB-S6-E5026-APP, RWB-S6-E6002-APP and the later stories of this service; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the personal facts and the 30 `v_ace_*` views, which are rwb-source-data's (P1); the document store, the WORM retention and the claim-check mechanics, which are rwb-document's (P5); the masking rule rows and the closed lists, which are reference data read with their version; the DEBTSALE package, which is authored and approved in rwb-decision (P7); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-025 gave the Workbench one unattended step that turned an approved lot's accounts into a data tape whose personal data was masked under PDPA, and wrote the decision log entry. The FSD keeps the objective and the metric unchanged: the debt sale turnaround is measured on the decision log and the Workbench records, reviewed monthly, against a target of 45 days (FSD S6 A2.3.1). The program keeps the requirement: REQ-S6-003, "The data room holds a masked data tape, and no unmasked personal data leaves the bank", Must, E5 (FSD S6 Requirements served). The problem the feature answers is unchanged: debt sales run on spreadsheets with no baseline turnaround (FSD S6 A1.3).

What D-RCV-60 changes is who owns the tape, the personal facts, the masking rules, the case and the file.

- **the tape is this service's step and rwb-document's document.** R-DS-10 names the Workbench as the actor and PII service, Recovery Data Store and Document Hub as the systems; in the target the tape is built here and stored as a claim-check file of rwb-document (P5) on Blob with WORM, with the document reference held in the decision record because `rwb_debtsale` owns two tables and none of them carries a tape reference (GAP-3014; ASM-4992).
- **the personal facts stay with rwb-source-data (P1).** The legacy feature reads the ACE database in-process; in the target only rwb-source-data holds the 30 `v_ace_*` views, so the account and borrower facts arrive on the owner's data product with the as-of date and this service holds no grant (GAP-3014; ASM-4991).
- **the masking rules are reference data with a version.** BR-S6-003 forbids a value a business person may change from being written in code, so the rule set is read at its version and applied as data, never as a branch of the build (GAP-3014; ASM-4990).
- **the "PII service" has no row among the 19.** Its two duties, the masking rules and the masking check, are the versioned reference-data read and a check executed inside this service, and the absent mapping is recorded rather than invented (GAP-3014; ASM-4993).
- **the case stays with rwb-case (P3).** `recovery_case` and the route states `LOT_APPROVED`, `TAPE_PREPARED`, `TAPE_REJECTED` and `DATA_ROOM_OPEN` are P3's; this step evaluates the rule, records the outcome, stores the tape and **answers** the case move.
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the tape's document reference, which is what legacy AC1's second `Then` asks for and what legacy AC3 tests.
- **no second copy and no data lake.** The tape exists once, in the document hub, and reaches a buyer only through the data-room read of RWB-S6-E5026-APP; the retired data-lake path of DP-17 is not reintroduced and no event carries an account fact.

No business value moves: the masking rule set, the tape spec version, the closed lists `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK`, the `Any` condition of R-DS-10 and its 3-working-day timer are read with their version. Where the sources give none of those values, the story says so instead of inventing one (GAP-3014; ASM-4990, ASM-4994).

### 3. Preconditions

- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, is hash-linked, and a failed write stops the action with MSG-P7-003, so the tape reference and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-25 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The lot and its accounts exist in `rwb_debtsale` from RWB-S6-E5024-APP and its status stands at `OFFERED` or later of `LOV-LOT-STATUS`, and the case of its accounts is in `LOT_APPROVED` after R-DS-06 of RWB-S6-E6001-APP. This story's H row carries no service contract story because the step serves no REST operation and publishes no element: it is reached on the workflow boundary only.
- The rwb-source-data data-product contract that carries the account and borrower facts of a lot, with its as-of date, is published with its fake; its operation name is Not specified in the source documents (GAP-3014; ASM-4995), and the row is not in this story's contract-dependency list, which is None.
- The rwb-document contract that stores a claim-check file and answers its document reference, size, checksum and masking-check metadata is published with its fake; its operation name is Not specified in the source documents (GAP-3014; ASM-4995).
- The rwb-case contract is published with its fake for the case state read and for the case-move answer of `TAPE_PREPARED` and `TAPE_REJECTED`; no source names a published operation that moves a case state on behalf of a stage, so on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-3014; ASM-4995).
- The reference-data contract of rwb-case returns the PII masking rule set at its version and the tape spec version (the DP-07 default ruling, not a pattern row of this key); the operation name is Not specified in the source documents (GAP-3014; ASM-4990), and the row is not in this story's contract-dependency list either (ASM-4995).
- The DEBTSALE rule package is in force at its version, with R-DS-10, R-DS-11 and R-DS-12 among its 41 rules over 29 states (TSD S6 T4); it is authored, tested and approved in rwb-decision (P7) and read here on its package read, whose operation name is Not specified in the source documents (GAP-3014; ASM-4995).
- FEAT-RDF-15, the reference-data prerequisite the legacy story names, is in place, so the run holds the masking rule set and the four closed lists at their versions (legacy RWB-E5-025 Depends on; GAP-3014; ASM-4990).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on `rwb_debtsale`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_*` or `rwb_case` is refused by the database and fails the boundary test (GAP-3014; ASM-4991).
- No approval is needed to build against a Draft contract baseline; the platform contracts are tagged by their owners when their tests pass.

### 4. Flow

1. The lot reaches `LOT_APPROVED` on the case of its accounts after R-DS-06 (RWB-S6-E6001-APP), and the case of a lot's accounts is therefore readable in `LOT_APPROVED` on rwb-case. The tape step of `DebtSaleWorkflow` on queue `rwb-debtsale` receives the trigger of R-DS-10, `TAPE_BUILD_RUN` under the condition `Any` (Business Rules and Routing Logic v4; FSD S6 A2.3.2 step 1). FSD S6 A2.3.4.4 declares no background event, so the trigger is the approval answer the parent forwards and not a schedule of this service.
2. The step reads its own lot and accounts from `rwb_debtsale` and writes no row: `lot_no` (DF-SAL-021), `cut_off_date` (DF-SAL-022), `segment` (DF-SAL-023), `reserve_price` (DF-SAL-024), `buyer_class` (DF-SAL-026), `payment_terms` (DF-SAL-029) and `status` (DF-SAL-030) from `debt_sale_lot`, and `account_id` (DF-SAL-033), `borrower_code` (DF-SAL-034), `outstanding` (DF-SAL-035), `selling_price` (DF-SAL-036) and `put_back_status` (DF-SAL-037) from `debt_sale_account`.
3. The step reads the DEBTSALE package version in force and the PII masking rule set at its version, both as data and both recorded with the outcome; no masking pattern, no list value and no account rule is compiled into the build (BR-S6-003; GAP-3014; ASM-4990).
4. The step reads the account and borrower facts the tape carries on the rwb-source-data data product: the account reference, the borrower facts and the balances the tape spec names, with the as-of date of the data product, one hop with a 2 s budget and a breaker (GAP-3014; ASM-4991). A data product that is stale after a late or failed ACE batch holds the step with VR-S6-003-1 and MSG-P1-001.
5. `TapeBuilder` lays the tape out under the tape spec version in force: the lot facts, one row per account of the lot and the personal field set of the spec. The column list, the file format and the spec version are fixed by no source and are read from the spec rather than coded (GAP-3014; ASM-4994).
6. `PiiMaskingEngine` replaces every personal value of the row set with its masked form under the rule set, before the row exists outside the step. The unmasked values live in the activity's memory only: they are never written to a log, the decision record, the workflow input, an event or `rwb_debtsale` (BR7).
7. `MaskingCheck` scans the built tape for an unmasked identifier (R-DS-11). A tape with none passes and is released to the record; a tape that carries one is rejected and never stored for the data room, and R-DS-12 returns the rebuilt tape to the check.
8. `TapeDecisionRecordWriter` writes one decision record through the local decision-record library, **before the tape is stored**: the case references, the lot reference, the rule ID R-DS-10 with its package version (or R-DS-11 and R-DS-12 for a rejected tape), the masking rule set version, the tape spec version, the account count, the tape checksum and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC2).
9. `TapeDocumentWriter` stores the masked tape as a claim-check file through the rwb-document contract on Blob with WORM, in the same transaction as the decision record and the idempotency row, and keeps the document reference, the checksum, the size and the masking-check result (GAP-3014; ASM-4992).
10. `CaseMoveAnswer` answers rwb-case with `TAPE_PREPARED` for the happy path and `TAPE_REJECTED` for a tape that failed the check, for every case of the lot, with the rule ID and the version. rwb-case writes the `recovery_case` row and its route state; this service writes neither.
11. A repeated trigger for the same lot and the same tape spec version writes no second tape, no second document and no second record; the repeat is counted and the tape that exists is answered, so a second buyer release can never read a half-built file (§12.3, X8).
12. SCR-25 Lot builder shows the approved lot with its tape-prepared indication from this service through the gateway-bff composite route, read only, next to the case state of rwb-case (DP-19). The data-room screen PRT-05 and the rule R-DS-13 that opens it are RWB-S6-E5026-APP's.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction stores nothing: no tape, no document reference and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E5-025-03, TC-E5-025-05 |
| X2 | The role does not hold the Debt sale right of the action | 403 before any read of the lot or of the personal facts; nothing changes and no decision record is written | MSG-P4-002 | TC-E5-025-04 |
| X3 | The masking check finds an unmasked identifier on the tape (R-DS-11) | The tape is rejected and is not stored for the data room; the rebuild of R-DS-12 returns it to the check, and the case moves to `TAPE_REJECTED` when the rebuild does not pass | None; the check result is on the record | AC2, TC-E5-025-02 |
| X4 | The personal-facts data product is stale after a late or failed ACE batch (VR-S6-003-1) | The step holds, builds nothing and shows the data date; the build resumes on the next fresh answer | MSG-P1-001 | AC1, X5 |
| X5 | The rwb-source-data, rwb-document, rwb-case or rwb-decision contract does not answer inside its budget, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is stored and no case move is answered, and the caller sees 503 with the platform error envelope | None | AC1 |
| X6 | The masking rule set or the tape spec is not in force at a version | The step holds and stores nothing; an unversioned rule set is never applied, and the missing version is reported to the parent | None | AC1, X5 |
| X7 | The case is not in `LOT_APPROVED` when the trigger arrives | 409 and nothing is built; a tape is never built on a lot the committee has not approved | None | AC2 |
| X8 | The same trigger, or the same lot and tape spec version, arrives twice | One tape, one document, one record and one answer; the repeat is counted | None | AC1 |
| X9 | A component, a statement or a test reaches an ACE table or a `v_ace_*` view, another service's schema, or writes an unmasked personal value | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR7 |

X1 and X2 are the exception paths of RWB-E5-025 carried onto the split; X3 is the masking branch of R-DS-11 and R-DS-12 that the legacy criteria do not spell out; X4 to X6 are the freshness, call-type and version paths; X7 and X8 are the state and repeat paths; X9 is the ACE, schema and personal-data boundary. MSG-S6-001 is carried in section 14 because it is in the message set of the feature, and no path of this story raises it: an account with an open deviation is excluded by R-DS-02 in RWB-S6-E5023-APP, before the lot this step receives exists.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-PLT-E1027-CON, RWB-PLT-N001-CON, the rwb-source-data, rwb-document, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P5 or P7 |
| Negotiable | The activity name, the decision code per rule, the tape spec version and the shape of the stage outcome are this story's choice; the rules, the messages, the screen and the lot and account columns are fixed |
| Valuable | An approved lot reaches a masked tape whose unmasked identifiers are proven absent, with the decision recorded and the case moved in the service that owns it, so REQ-S6-003 is met and the 45-day turnaround stays measurable |
| Estimable | One workflow step, one tape builder, one masking engine, one check, one record write, one file write, four clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots and personal fact sets through the contract fakes, plus the component cases of the access answer, the forced record failure and the masking reject and rebuild |

### 7. Acceptance criteria

```gherkin
Feature: Prepare the masked data tape

  Background:
    Given case "RC-2026-001207" is one of the accounts of lot "DS-2026-0007" in segment "RETAIL" at cut-off date "2026-11-30"
    Given the DEBTSALE rule package is in force at its version and carries R-DS-10, R-DS-11 and R-DS-12
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Prepare the masked data tape (legacy RWB-E5-025 AC1)
    Given the rwb-source-data contract mock returns the account and borrower facts of lot "DS-2026-0007" with as-of date "2026-11-30"
    Given the rwb-document contract mock accepts the masked data tape of lot "DS-2026-0007" and returns its document reference
    Given the rwb-case contract mock returns the case state "LOT_APPROVED" and accepts the move "TAPE_PREPARED" for "RC-2026-001207"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the data tape with personal data masked under PDPA, ready for the data room
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-10 (legacy RWB-E5-025 AC2)
    Given the rwb-case reference-data contract mock returns the PII masking rule set at its version in force
    Given the rwb-case contract mock returns the case state "LOT_APPROVED" and accepts the move "TAPE_PREPARED" for "RC-2026-001207"
    Given a case in state LOT_APPROVED
    When tape build run
    Then build the masked data tape under the PII masking rules
    Then the case moves to TAPE_PREPARED

  Scenario: AC3 Not recorded (legacy RWB-E5-025 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E5-025 word for word, with their origin tag added and nothing else changed: the legacy feature line, the legacy scenario names `AC1 Prepare the masked data tape`, `AC2 Rule R-DS-10` and `AC3 Not recorded`, the legacy wording of `its trigger arrives`, `tape build run`, `the action is taken`, `builds` without a subject and the repetition of `Then` all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and AC2 two; those added `Given` lines are the only additions to the legacy text, and AC3 needs none because the decision-record library is local. What the legacy lines describe happens in four places in the target: rwb-source-data answers the account and borrower facts the legacy feature read from the ACE database; the masking rules and the check are the versioned rule set of ASM-4990 and ASM-4993; this story builds the tape, masks it, checks it, stores it as a document of rwb-document, records the decision and answers the case move; and rwb-case writes the route state `TAPE_PREPARED`. The `decision log` the legacy text names is the local decision record of DP-03 in `rwb_debtsale`, with the central `decision_log_entry` ledger of rwb-decision behind it. R-DS-11, R-DS-12 and R-DS-13 are tabled in section 8; the reject and rebuild of R-DS-11 and R-DS-12 are the branch of AC2 that X3 exercises, and R-DS-13's own criterion, "Open the data room to buyers who have signed the non-disclosure agreement", is RWB-S6-E5026-APP's because it opens the room and moves the case to `DATA_ROOM_OPEN` (GAP-3014; ASM-4992).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-10 | Debt sale | D8.4 | LOT_APPROVED | TAPE_BUILD_RUN | Any | Build the masked data tape under the PII masking rules | TAPE_PREPARED | Workbench | PII service, Recovery Data Store, Document Hub | 3 working days |
| R-DS-11 | Debt sale | D8.4 | TAPE_PREPARED | MASKING_CHECK_FAILED | an unmasked identifier is found on the tape | Reject the tape and rebuild it | TAPE_REJECTED | Workbench | PII service, Document Hub | None |
| R-DS-12 | Debt sale | D8.4 | TAPE_REJECTED | TAPE_REBUILT | masking check passes | Return the tape for data room release | TAPE_PREPARED | Workbench | PII service | None |
| R-DS-13 | Debt sale | D8.4 | TAPE_PREPARED | MASKING_CHECK_PASSED | no unmasked identifier | Open the data room to buyers who have signed the non-disclosure agreement | DATA_ROOM_OPEN | Debt sale officer | buyer portal, Document Hub | per cycle |

The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: "Workbench" is this service's step, the "PII service" is the versioned masking rule set and the check of this step because the target has no PII service row among the 19, the "Recovery Data Store" is `rwb_debtsale` and the "Document Hub" is rwb-document (P5); the case moves these rows name are written by rwb-case on this story's answer. R-DS-13 is tabled because this step produces the `TAPE_PREPARED` state it reads, and its own action and criterion belong to RWB-S6-E5026-APP (GAP-3014; ASM-4993). The validation rule VR-S6-003-1, "Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`)", is carried with its message MSG-P1-001 in section 14 and raises X4.

| ID | Rule | Source |
|---|---|---|
| BR1 | The tape is built here and stored as one document of rwb-document (P5) on Blob with WORM; no second copy exists and no buyer reads the tape except through the data-room read of RWB-S6-E5026-APP | TSD S6 T5.1 (INT-25 Debt buyers, file through the data room); FSD S6 A2.3.2; R-DS-10; GAP-3014; ASM-4992 |
| BR2 | The decision is recorded before the tape is stored, with the rule ID and the package version in force; a failed write stores nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2 ("writes the decision log entry before any change"); legacy RWB-E5-025 AC1 and AC3 |
| BR3 | The account and borrower facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the fact on the owner's data product only, with the as-of date | FSD S6 A1.1 constraints (source data only through `recovery.v_ace_*`, landed by ACE); GAP-3014; ASM-4991 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states `LOT_APPROVED`, `TAPE_PREPARED`, `TAPE_REJECTED` and `DATA_ROOM_OPEN` are rwb-case's, and this story sends the move with the rule and its version | TSD S6 T5.2; GAP-3014; ASM-4995 |
| BR5 | Every value a business person may change is reference data or a rule row read with its version: the PII masking rule set, the tape spec, `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` | FSD S6 BR-S6-003; TSD S6 T3.2; legacy Guardrails; ASM-4990 |
| BR6 | An unmasked identifier stops the tape: the check of R-DS-11 runs on the built tape before the document reference is written, and a failed tape is never stored for the data room | REQ-S6-003; FSD S6 A2.3.1 ("personal data masked under PDPA"); R-DS-11 and R-DS-12 |
| BR7 | No unmasked personal value enters a log, an event, a workflow input, the decision record or `rwb_debtsale`: the activity receives the lot reference and reads the facts itself, the masking happens before the row leaves the step, and `borrower_code` is a code and not an identity | Template and Rules v1 §R7.2 (s17); REQ-S6-003; FSD S6 A2.3.3.3 |
| BR8 | One tape per lot and tape spec version: a repeated trigger or the same lot twice writes one record, one document and one answer | TSD S6 T-A.2 (idempotency); FSD S6 A2.3.4.4 (no background event); X8 |
| BR9 | The tape spec version, the masking rule set version and the package version are recorded with the outcome, so a later audit reproduces the tape from the same three versions | TSD S6 T2 and T4; FSD S6 BR-S6-003; legacy AC1 ("with the rule version") |

### 9. State transitions

The case route state is rwb-case's and this story does not change it: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the tape branch of the step.

| From (`recovery_case`, owner P3) | Event | Condition | To | Answered by |
|---|---|---|---|---|
| LOT_APPROVED | TAPE_BUILD_RUN | R-DS-10, condition `Any` | TAPE_PREPARED | This story |
| TAPE_PREPARED | MASKING_CHECK_FAILED | an unmasked identifier is found on the tape | TAPE_REJECTED | This story |
| TAPE_REJECTED | TAPE_REBUILT | the rebuilt tape passes the check | TAPE_PREPARED | This story |
| TAPE_PREPARED | MASKING_CHECK_PASSED | no unmasked identifier | DATA_ROOM_OPEN | RWB-S6-E5026-APP |
| LOT_APPROVED, TAPE_PREPARED | A repeated trigger for the same lot and tape spec version | X8 | Unchanged, the repeat is counted | This story |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The approval answer for a lot in `LOT_APPROVED` arrives | The package and the rule set are read at their versions | Reading |
| Reading | The lot and its accounts are read and the personal facts arrive fresh | VR-S6-003-1 does not fire | Building |
| Reading | The personal-facts data product is stale | X4 | Held, until a fresh answer |
| Building | The tape is laid out under the tape spec version | The masking engine has replaced every personal value | Checking |
| Checking | The masking check finds no unmasked identifier | R-DS-11 does not fire | Applying |
| Checking | The masking check finds an unmasked identifier | X3, R-DS-11 | Rejected, rebuilt under R-DS-12 |
| Applying | The decision record and the document reference are written and the case-move answer is sent | The transaction commits | Waiting for the next cycle |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing stored |

The route states are those of the DEBTSALE machine of TSD S6 T4, and they live on the case of record. The tape's own state is carried by the decision record, the document metadata and the record's checksum, because `rwb_debtsale` owns no tape table and no tape column (GAP-3014; ASM-4992).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the primary role of the feature when a person acts, reading the tape-prepared state on SCR-25 and correcting a lot before the tape run |
| RW-NPAMGR, NPA and asset manager | Debt sale R: reads the lot and its tape-prepared state |
| RW-SALEOFF, sale officer | Debt sale R: reads the lot and its tape-prepared state |
| RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| RW-PRODHEAD, RW-HEADASL | Debt sale RA: read, and approve through the approval path where the delegation reaches them |
| PT-BUYER, PT-RAMC | Debt sale RU or R as the TSD S6 T6.1 matrix gives it: the partner reads the released tape through the data room of RWB-S6-E5026-APP and never the build decision |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-debtsale service identity | Runs the step unattended, reads the package, the rule set and the personal facts, masks and checks the tape, writes the decision record and the document reference and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S6 T6.1 and nothing wider. FSD S6 A2.3.3.3 says the feature "runs unattended" with the debt sale officer as also-user, and both statements hold: the step runs under the service identity with no officer task on the happy path, and the debt sale officer is the primary role of the feature when a person does act. DP-08 is not in this story's pattern set: the capability area and the right are declared per action and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-021 to DF-SAL-024, DF-SAL-026, DF-SAL-029, DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no, cut_off_date, segment, reserve_price, buyer_class, payment_terms, status | Read; which of them the buyer tape carries is fixed by the tape spec (GAP-3014; ASM-4994) |
| DF-SAL-025, DF-SAL-027, DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id, signing_date, approval_authority | Read; they belong to the buyer, award and approval stories and are carried on no tape by this story |
| DF-SAL-033 to DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | account_id, borrower_code, outstanding, selling_price, put_back_status | Read, one row per account of the lot; `borrower_code` is carried masked on the tape |
| DF-SAL-031, DF-SAL-032 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id | Read, the key of each account row |
| Standard columns | both tables (S6, `rwb_debtsale`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Read only; this story changes no business row and takes no optimistic lock |
| The masked personal field set | the tape (spec version, S6) | the personal fields of the account and borrower, in their masked form | Write, on the tape only; the field IDs and the column list are Not specified in the source documents (GAP-3014; ASM-4994) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the tape is stored |
| Tape reference and checksum | decision record and rwb-document (P5) | document reference, size, checksum, masking-check result, rule-set version, tape spec version | Write; no column of `rwb_debtsale` carries them (GAP-3014; ASM-4992) |
| `v_ace_*` and the ACE tables (P1) | the account and borrower facts | number, name, address, contact values and the balances | Not read: this service holds no `v_ace_*` grant, and the fact arrives on the rwb-source-data data product (BR3). Field IDs Not specified in the source documents (GAP-3014; ASM-4991) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the case state arrives on the rwb-case answer |
| decision_log_entry, rule_row (P7) | the central decision ledger and the rule rows | id, decision_code, rule_id, rule_version and the rest | Not written and not read here: the local record is this service's and the rule rows are governed in rwb-decision |
| `document`, `document_version` (P5) | the tape file and its metadata | id, version, size, checksum, retention class | Not read as a table: the file is written and referenced on the rwb-document contract |

Field IDs are those of the TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v8, and the ACE and document rows are the rows the legacy story and the FSD name, with their owners changed to P1 and P5 by the target. **No new table, no new column and no migration**: `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, this story writes no row of either, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_debtsale` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**Personal data.** The tape carries personal fields in their masked form; unmasked values exist in the activity's memory only, are never persisted, never logged and never put in the workflow input, the decision record, an event or a message. The fixture data of the tests is synthetic, and no real personal value is read, written or shown by this story.

### 12. Contract

#### 12.1 REST operations provided

None. This step is a workflow activity behind `DebtSaleWorkflow` and serves no operation of its own: the lot read is API-S6-002 and the data-room read is API-S6-004, declared and built by RWB-S6-E5024-APP and RWB-S6-E5026-APP on base `/api/recovery/debtsale/v1`. The tape reaches a buyer only through the data-room read, and SCR-25 reads this service through the gateway-bff composite route (DP-19) and not through an operation of this story. A build that adds a REST operation to this story fails the absence test.

#### 12.2 REST operations consumed

| Operation | Base or owner | Owner | Use |
|---|---|---|---|
| The read of the account and borrower facts data product (operation name Not specified in the source documents (GAP-3014; ASM-4995)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The account and borrower facts the tape carries, with the as-of date of the data product; faked |
| The write of the masked tape as a claim-check file and the answer with its reference (operation name Not specified in the source documents (GAP-3014; ASM-4995)) | `/api/recovery/document/v1` | P5 rwb-document | The file on Blob with WORM, its document reference, size, checksum and the masking-check metadata; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state of the lot's accounts, to confirm `LOT_APPROVED` and take the case references; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3014; ASM-4995)) | rwb-case (P3) | P3 rwb-case | `TAPE_PREPARED` or `TAPE_REJECTED` with the rule and its version, one answer per case; on the workflow boundary it is the stage outcome the parent applies; faked |
| The reference-data read of the PII masking rule set and the tape spec (operation name Not specified in the source documents (GAP-3014; ASM-4995)) | `/api/recovery/case/v1` | P3 rwb-case | The masking rule set and the tape spec at their versions (DP-07 default ruling, not a pattern row of this key); faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3014; ASM-4995)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEBTSALE package at its version with R-DS-10, R-DS-11 and R-DS-12; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-3014 with ASM-4995.

#### 12.3 Events published

None. The service publishes `LotAwarded` and `AccountsTransferred` on `rwb.debtsale.events.v1`, and neither belongs to this step: the lot is not awarded here and no account is transferred, and R-DS-10 publishes no event of its own. This story therefore declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic `rwb.debtsale.events.v1` carries the retry and `.dlt` topics of the platform (DP-14).

#### 12.4 Events consumed

None. The trigger of the step is the approval answer the parent forwards and the lot of its own schema, and FSD S6 A2.3.4.4 declares no background event for the feature; no consumed event is named for the tape by any source. This story holds no consumer group, no subscription and no inbox row of its own, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per sale cycle, the child of `CaseWorkflow`, a saga whose pivot is the transfer, continues-as-new at each stage end | `rwb-debtsale` in namespace `rwb-recovery` | Input: the sale cycle, the lot references and the rule and rule-set versions in force; signals: the approval answer, the masking-check result and the case state. This step sits before the pivot, so it needs no compensation |
| `prepareMaskedTape` | Activity, the one tape step of this story | `rwb-debtsale` | The lot reference, the tape spec version and the rule-set version in; the rule ID with its package version, the document reference, the checksum, the masking-check result, the account count and the case move out, with the decision record and the document reference written in one transaction. Personal facts are read inside the activity and never passed in |

No child workflow for the case and no workflow for the money exists in this service. The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the approval answer of R-DS-10, because the FSD declares no background event (FSD S6 A2.3.4.4).

#### 12.6 Schedules

None. The step runs from the approval answer and the case signal the parent forwards, and owns no Temporal Schedule and no legacy Quartz job. R-DS-10's 3-working-day timer is the timer column of the route rule and not a Schedule of this service, and no Job of the Batch and Scheduling Design is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot; this story reads the row and writes no column |
| debt_sale_account | S6 (`rwb_debtsale`) | An account in the lot; this story reads the rows and writes no column |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03); it carries the tape reference, checksum and check result |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | Present in the schema as the library object; this step writes no row to it because it publishes no event (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view and ACE table (P1), `document` and `document_version` (P5), `decision_log_entry` and `rule_row` (P7), and the bid, data-room, award and transfer tables of the later stories of this service. No foreign key leaves the schema; `account_id` and the document reference are identifiers, not foreign keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data account and borrower facts fake | The facts of the accounts of lot `DS-2026-0007` with as-of date `2026-11-30`, including the unmasked personal values; a stale product with its date; no answer beyond 2 s | AC1, AC2, X4, X5 |
| rwb-document tape fake | The document reference, size, checksum and masking-check metadata of the tape of lot `DS-2026-0007`; a refused write | AC1, X1 |
| rwb-case case-state fake | The case state `LOT_APPROVED` of case `RC-2026-001207`; a case that has not been approved | AC1, AC2, X7 |
| rwb-case case-move fake | `TAPE_PREPARED` and `TAPE_REJECTED` accepted for each case of the lot; a move refused because the case is not in the state the rule expects | AC1, AC2 |
| rwb-case reference-data fake | The PII masking rule set and the tape spec at their versions in force; a rule set with no version | AC2, X6 |
| rwb-decision rule-package fake | The DEBTSALE package at its version in force with R-DS-10, R-DS-11 and R-DS-12 | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-25 answer for lot `DS-2026-0007` with its tape-prepared indication | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the source-data read, the document write, the case-move answer, the reference-data read and the package read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3014; ASM-4995).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-source-data facts read, the rwb-document file write, the rwb-case state read, the case-move answer, the reference-data read and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of the tape; `LotAwarded` and `AccountsTransferred` belong to the award and transfer stories |
| Temporal | 1 workflow and 1 activity | `DebtSaleWorkflow` and `prepareMaskedTape` on `rwb-debtsale`; no Schedule |
| File | 1 written | The masked data tape as a claim-check file of rwb-document on Blob with WORM; no file is read |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `tape`, Java package `th.co.scb.ace.workbench.recovery.debtsale.tape`; front end `src/modules/recovery/debtsale/LotBuilder.tsx`, the fragment SCR-25 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the document reference and the idempotency row commit together or not at all, and the record is written before the tape is stored. DP-19 is how SCR-25 reaches this service, one hop through the gateway. The two rows are the whole pattern set of this key and the story adds no third: DP-07 (reference data), DP-05 (ACE data through rwb-source-data) and DP-13 (the per-service base) are real relations of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3014; ASM-4990, ASM-4991, ASM-4995). DP-13 moves no base here because this story serves no operation, and DP-09 is not needed because it publishes no event.

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies of this story, and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (ASM-4995). The reference-data contract of DP-07 would add `RWB-PLT-E1043-CON` as H and `RWB-P3-E1043-CON` as C and is read as data without being added. The plan's H row is kept exactly as it stands.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` tape branch | Workflow | The stage step that waits for the approval answer, carries the tape spec and rule-set versions and reports the outcome to the parent |
| `prepareMaskedTape` | Activity | The one step: read the lot, read the facts, build, mask, check, record, store and answer, in one transaction |
| `TapeBuilder` | Service | Lays the tape out under the tape spec version: the lot facts, one row per account and the personal field set |
| `PiiMaskingEngine` | Library adapter | Replaces every personal value with its masked form under the rule set at its version; pure, in memory, no persistence |
| `MaskingCheck` | Service | Scans the built tape for an unmasked identifier (R-DS-11) and drives the rebuild of R-DS-12 |
| `TapeDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID, the package, the rule-set and tape spec versions, the checksum and the case move before the tape is stored (DP-03) |
| `TapeDocumentWriter` | Client | Stores the tape as a claim-check file through rwb-document and takes its reference, size and checksum, in the same transaction |
| `SourceDataFactsClient` | Client | The read of the account and borrower facts of rwb-source-data, one hop, 2 s, breaker, with the as-of date |
| `ReferenceDataClient` | Client | The masking rule set and the tape spec at their versions, cached by version and never by value |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case |
| `DebtSaleTapeController` | Controller | The read-only fragment the composite route calls for the tape-prepared indication, with the problem mapping of 401, 403, 404 and 503 |
| `LotBuilder` | React component | Shows the tape-prepared indication and its refusal, stale-data and rejected states on SCR-25, read only |

**Database and migrations.** No Flyway file. `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service and this story writes no row of either; the decision record and the idempotency key are library objects created in `rwb_debtsale` by the library's migration (DP-03). No column is added for the tape: its reference, checksum and check result live in the decision record and on the document (ASM-4992).

**Configuration and reference data.**

- The PII masking rule set and the tape spec at their versions in force, read as reference data and never as constants; their content is given by no source (GAP-3014; ASM-4990, ASM-4994).
- `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` at their versions (TSD S6 T3.2), read and never copied.
- The DEBTSALE package at its version, authored, tested and approved in rwb-decision; the rule rows themselves are not a build item of this story.
- The capability area "Debt sale" and its rights are access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the retention class of the tape is the WORM policy of rwb-document.

**Build steps**

1. The tape branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale` as the stage child of `CaseWorkflow`, with the approval answer as its trigger and no personal value in the input (BR7).
2. `SourceDataFactsClient` against its fake, with the 2 s budget, the breaker, the stale-data path and the no-answer path (AC1, X4, X5).
3. `ReferenceDataClient` for the masking rule set and the tape spec by version, with the unversioned-rule-set path (AC2, X6).
4. `TapeBuilder` over the lot and account rows and the spec version (AC1, X7).
5. `PiiMaskingEngine` against the rule set, with a synthetic personal fixture that proves no unmasked value survives in memory output, log or record (AC1, AC2, X9).
6. `MaskingCheck` and the rebuild of R-DS-12, with a tape seeded with an unmasked identifier (AC2, X3).
7. `TapeDecisionRecordWriter` against the library stub, with the failed-write path (AC3, X1).
8. `TapeDocumentWriter` against its fake, in the same transaction, with the refused-write path (AC1, X1).
9. `CaseStateClient` and the case-move answers `TAPE_PREPARED` and `TAPE_REJECTED` per case of the lot (AC1, AC2).
10. The repeat test: the same lot and tape spec version twice writes one tape, one document and one record (X8).
11. The boundary test: no statement outside `rwb_debtsale`, no `v_ace_*` read, no write to `rwb_case`, `rwb_document` or `rwb_decision`, and no unmasked personal value in a log (X9, BR3, BR7).
12. `LotBuilder` and SCR-25 through the composite route fake (AC1).

**Feature flag.** `rwb.debtsale.tape-v1`, read as a flag of the platform library; off means the step holds the approved lot, builds nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic approved lot in SIT, R-DS-10 produces its record, its tape and its move, R-DS-11 rejects a seeded tape and R-DS-12 returns it, a repeated trigger writes once, a forced record failure stores nothing, no unmasked personal value and no `v_ace_*` read exists in the build, and SCR-25 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an account with an open deviation, which is excluded by R-DS-02 in RWB-S6-E5023-APP before this lot exists, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the lot, of the account rows or of the tape spec is absent or invalid (X6, X7) | Enter {field}. |
| MSG-P4-002 | A role without the Debt sale right takes the action (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the tape is stored (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The personal-facts data product is stale after a late or failed ACE batch (X4, VR-S6-003-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The five message IDs are those of the legacy message set and of FSD S6 A2.3.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The masking reject of X3 raises no message: its result is a recorded state and not a user-facing error.

### 15. Screens and states

SCR-25 Lot builder in its approved state, with the tape-prepared indication, is served through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot and its tape-prepared indication, rwb-case for the case and its route state and rwb-document for the tape's reference and check result; this story fixes the rwb-debtsale fragment only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the tape-prepared indication of the approved lot and the rejected indication of a tape that failed the masking check; the draft and priced states belong to RWB-S6-E5024-APP and the approved decision to RWB-S6-E6001-APP. The refusal, not-recorded, stale-data and rejected states the screen shows read the messages of section 14. PRT-05 Data room and the buyer's view of the released tape belong to RWB-S6-E5026-APP and read the tape through the data-room read; no screen shows an unmasked value.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-025-01 | AC1 | Component | The synthetic lot `DS-2026-0007` of case `RC-2026-001207` with its personal fact set on the fake; the tape, the document reference, the decision record and the `TAPE_PREPARED` answer asserted, and no unmasked value in the tape, the record or the log |
| TC-E5-025-02 | AC2 | Component | A case in `LOT_APPROVED`, the rule set at its version and the DEBTSALE package in force; the tape built under the rules, the check passed and the `TAPE_PREPARED` answer; a seeded unmasked identifier answered as `TAPE_REJECTED` |
| TC-E5-025-03 | AC3 | Component | The decision-record stub stopped; no tape, no document reference and MSG-P7-003 shown |
| TC-E5-025-04 | Access | Component | A role without the Debt sale right; 403 with MSG-P4-002 and no read of the personal facts |
| TC-E5-025-05 | Principle 5 | Component | A forced decision log write failure at the moment of the document write; no tape, no reference and no answer |

The five legacy cases are the legacy cases of RWB-E5-025 in their legacy order, with the Level column added: the legacy `System` level maps to `Component` where the step is tested on its fakes, and the access and forced-failure cases map to `Component` for the same reason. The full test, with its Given, When and Then, stays in the test case workbook of the run under the same test case ID; no `-ITG` copy of these cases is written by this story, and the cross-service journey of the legacy key belongs to the wave 3 harness.

### 17. Guardrails

- No business value in code: the masking rule set, the tape spec, the closed lists and the rule rows stay data or reference data with a version, never a constant, a default pattern or a branch of the build.
- No unmasked personal data in `rwb_debtsale`, in the decision record, in a workflow input, in an event or in a log: the activity reads the facts itself, masks them in memory, and every fixture is synthetic (BR7).
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR3).
- An unmasked identifier stops the tape before the document reference is written; a build that stores a tape the check has not passed fails the review (BR6).
- The case stays with rwb-case and the file with rwb-document: no `recovery_case` row, no second copy of the tape and no tape table are written here (BR1, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no data-lake export of the tape and no second event on the topic.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S6-003 | The data room holds a masked data tape, and no unmasked personal data leaves the bank (FSD S6 Requirements served, Must, E5); the split plan carries no requirement id for this slice (GAP-3014; ASM-4990) | The tape build, the masking, the check, the document and the case move | TC-E5-025-01, TC-E5-025-02, TC-E5-025-05 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the tape step | TC-E5-025-01 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login, with no `v_ace_*` grant | TC-E5-025-01 |
| ADR-019 | Edge: gateway-bff and partner gateway | SCR-25 through the composite route, the tape to buyers through the data room | TC-E5-025-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget | TC-E5-025-01 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the tape is stored | TC-E5-025-03, TC-E5-025-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-025, disposition Split (rework); feature FEAT-DBS-03; priority Must; legacy Depends on FEAT-RDF-15 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story; R-DS-13's criterion is RWB-S6-E5026-APP's |
| Source text | FSD S6 Debt sale v3 A2.3, TSD S6 Debt sale v2 T3 to T6 and T-A, the Business Rules and Routing Logic v4 rows R-DS-10 to R-DS-13, the Epics 3 to 8 Specification v3 row FEAT-DBS-03 and the legacy story |
| Test cases | TC-E5-025-01 to TC-E5-025-05 |
| Feature and screens | FEAT-DBS-03, SCR-25 Lot builder; PRT-05 Data room is RWB-S6-E5026-APP's |
| Rules | R-DS-10, R-DS-11, R-DS-12 and R-DS-13, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-019, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the lot read and the data-room read, their elements, the error set and the fakes: RWB-S6-E5024-CON and RWB-S6-E5026-CON.
- The selection of the sale population and the exclusion of an account with an open deviation under R-DS-01 and R-DS-02: RWB-S6-E5023-APP.
- The lot build and the price estimate: RWB-S6-E5024-APP.
- The committee approval, the reserve decision and the route state `LOT_APPROVED`: RWB-S6-E6001-APP.
- Opening the data room, the rule R-DS-13, the buyer qualification, the bids and the award: RWB-S6-E5026-APP, RWB-S6-E6002-APP and the later stories of this service.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes.
- The account and borrower facts, the ACE tables and the 30 `v_ace_*` views: rwb-source-data (P1) (GAP-3014; ASM-4991).
- The document store, the claim-check mechanics and the WORM retention class: rwb-document (P5) (GAP-3014; ASM-4992).
- The authoring, testing, approval and versioning of the DEBTSALE package and of the rule rows of R-DS-10 to R-DS-13: rwb-decision (P7).
- The content of the PII masking rule set, the tape column list, its file format and the tape spec version, which no source gives (GAP-3014; ASM-4990, ASM-4994).
- The mapping of the FSD's "PII service" onto a service of the target: no service row exists for it (GAP-3014; ASM-4993).
- The gateway-bff composite route and the screen field list of SCR-25: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
