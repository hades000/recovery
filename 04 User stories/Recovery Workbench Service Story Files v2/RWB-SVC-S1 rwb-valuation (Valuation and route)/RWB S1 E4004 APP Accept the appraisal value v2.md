# RWB-S1-E4004-APP Accept the appraisal value

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-D |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S1-E4004-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-S1-E4004-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-S1-E4004-APP-23); the /v1 base paths are the only contract reference |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Screen states (SCR-13) | Empty, loading and error states: Not specified in the source documents (DOR-RWB-S1-E4004-APP-10); no-access state: 403 with MSG-P4-002 (TC-E4-004-03) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-004 split out for rwb-valuation. Both legacy criteria of the key (AC1 and AC2) are copied word for word with their origin tags. The acceptance becomes the `acceptAppraisalValue` step of `RouteDecisionWorkflow` on task queue `rwb-valuation`: it reads the appraisal, its outlier flag and its acceptance state on the rwb-source-data data product (DP-05), fixes the band from the accepted value and the band in force, writes the decision record through the local library before anything is answered (DP-03), answers the case move to rwb-case, and returns the band on the route operation at base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). No event is published, because the ownership rows give S1 none. The acceptance has no durable home and no owner publishes its write (GAP-2603; ASM-4304); the five consumed rows and the case move publish no operation name and the plan carries no C row (GAP-2604; ASM-4305); the band, its boundaries and the rule id of the step are not published and no S1 rule package is in force (GAP-2605; ASM-4306). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S1-E4004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to let the case owner accept the value, which fixes the band the route decision runs on**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-004. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the rules, messages and screen they name;
- the acceptance step `acceptAppraisalValue` of `RouteDecisionWorkflow` on `rwb-valuation`, run when the case owner submits the route decision of a case whose value is presented for acceptance;
- the acceptance elements of the route command and the band of its answer on `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, with its right and its `Idempotency-Key` (API-S1-001; DP-13);
- the read of the appraisal, its outlier flag and its acceptance state on the rwb-source-data data product, one hop, 2 s, read only, with no `v_ace_*` grant of this service (DP-05);
- the band fixed by the accepted value against the band in force, read with its version and never written in code, and the acceptance marker `accepted_at` that the routing logic tests;
- the decision record of the acceptance, written through RWB-PLT-E1027-CON in the caller's transaction before the answer, with the rule id and the version in force (DP-03);
- the states of SCR-13 Route decision that this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the consumed rows, the acceptance element set, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4004-CON; the outlier flag and the appraisal intake of FEAT-VAL-02 and FEAT-VAL-03, which are the sibling appraisal stories of this service; the COLLINS return, the payoff and settlement range, the route agent, the approvals and the route-flow start of FEAT-VAL-05 to FEAT-VAL-12, which are the sibling route stories; the ACE appraisal, collateral and freshness facts, which are rwb-source-data's (P1); the case of record, its valuation states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows, the package version and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the band policy administered by the product head under FEAT-ADM-04, which is rwb-access's; the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The route decision chooses between restructure, settlement, guarantee claim, litigation, asset sale, debt sale and write-off. Every one of those choices is priced off the value of the security, so the band the decision runs on is fixed by the value the case owner has accepted and not by the latest figure a valuer returned. The FSD keeps the feature as FEAT-VAL-04 in module S1: the case owner accepts the value, which fixes the band the route decision runs on, and the step writes its result to the decision log with its rule version.

Under D-RCV-60 the ownership of the four facts changes, and that is what this story carries.

- **the value is ACE's, not this service's.** `v_ace_valuation` is ACE's and only rwb-source-data reads the `recovery.v_ace_*` views, so the appraisal, its type, its value, its date, the outlier flag of FEAT-VAL-03 and the acceptance state arrive on the owner's data product with its freshness stamp and are never read as a table here (DP-05).
- **the acceptance is a decision, not a row.** The ownership rows give S1 no table, so the acceptance is recorded as a decision record with the appraisal key, the accepted value, the band and the rule version, and the case carries the state; where a durable acceptance column would live is not fixed and is recorded, not invented (GAP-2603; ASM-4304).
- **the band is policy data.** BR-S1-004 of the FSD forbids writing a value a business person may change in code, and the bands, floors and ranges per product are set by the product head under FEAT-ADM-04. The step therefore reads the band in force with its version and asserts no boundary (GAP-2605; ASM-4306).
- **the case stays with rwb-case.** `VALUATION_ACCEPTED` and the move that follows `VALUE_ACCEPTED` are case states of the D6.4 route set (R-DIL-09, R-DIL-12); this story answers the move and writes no case row.
- **the decision is recorded first.** Legacy AC2 makes the step trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the acceptance, and R-UNI-39 forbids any action that is not logged.
- **nothing is published.** The ownership rows give S1 no event, so the acceptance adds no name to `rwb.valuation.events.v1`; its outward facts are the route answer, the case move and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4309).

The measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records. The requirement the step serves is REQ-S1-008, that a change in the exposure band, the valuation or the classification after a route decision triggers a fresh decision, which only works if the band and the accepted value are recorded with the version they were decided under.

### 3. Preconditions

- RWB-S1-E4004-CON is published: the route operation with the acceptance elements, the five consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story. The element set of `RouteRequest` and `Approval` is Not specified in the source documents beyond its two type names (GAP-2606; ASM-4307).
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-source-data data product that carries the appraisal of `v_ace_valuation`, the outlier flag and the acceptance state of `valuation_ext` is published with its fake and its freshness stamp; its operation name is Not specified in the source documents (GAP-2604; ASM-4305) and the row is not in this story's contract-dependency list, which is None.
- The rwb-case case-state read and case-move answer are available for their fakes, and the rwb-decision rule-in-force read and ledger read are available for theirs; their operation names carry the placeholder (GAP-2604; ASM-4305).
- The band in force is read as a value of reference data or of a rule row with its version, administered under FEAT-ADM-04; no source names its identifiers, its boundaries, the row that carries it or the rule id of this step, and no S1 rule package is in force (GAP-2605; ASM-4306).
- The value has been flagged by FEAT-VAL-03 and is presented for acceptance; where the appraisal is an unflagged outlier the step presents it and refuses the acceptance until the flag is cleared, as R-DIL-09 requires before the state `VALUATION_ACCEPTED`.
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_valuation`, `recovery.valuation_ext` or `rwb_case` is refused by the database and fails the boundary test (DP-01, DP-05).
- Where the accepted value, `accepted_at` and `accepted_by` are persisted after the split is not fixed: the ownership rows give S1 no table, TSD S1 T3.1 puts `accepted` on a NEW `valuation` table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2603; ASM-4304).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4004-CON when its tests pass.

### 4. Flow

1. The case is at the route decision and the value has been presented for acceptance; the case owner opens SCR-13 Route decision through the gateway-bff composite route and submits the acceptance through `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1` (API-S1-001; DP-13, DP-19).
2. The controller checks the capability area Treatment and offer and its right U against the caller's scope, and forwards the command with its `Idempotency-Key`; the command starts `RouteDecisionWorkflow` on task queue `rwb-valuation` in namespace `rwb-recovery`.
3. The acceptance step `acceptAppraisalValue` reads the appraisal of the asset on the rwb-source-data data product, one hop with a 2 s budget and a breaker: the valuation key, the asset key, the appraisal number, the type, the appraised value, the forced sale value, the appraisal date, the outlier flag, the acceptance state and the freshness stamp (DP-05; GAP-2604).
4. The step validates the command against VR-S1-004-1: the valuation key, the asset key, the accepted value and the appraisal date are required, and an absent or invalid element is refused with MSG-GEN-001 naming the field, with nothing written.
5. The step compares the submitted value with the appraisal on the data product; a value that does not match the appraisal of the asset on the case is refused with MSG-GEN-001 and no record is written, because an acceptance is of a value the valuer returned and not of a typed figure.
6. Where the data product is stale after a late or failed ACE batch, the step holds, writes nothing and shows MSG-P1-001 with the data date; it resumes on the next fresh answer (FSD S1 A1.4).
7. Where the appraisal is flagged as an outlier and the flag is not cleared, the step presents the value and refuses the acceptance with its reason, and the case stays where it was; the flag and its clearance are FEAT-VAL-03's.
8. The step fixes the band from the accepted value and the band in force: the band policy is read as a value with its version and applied as data, so the same accepted value and the same policy version always give the same band, and no boundary, threshold or default is compiled into the build (BR-S1-004; GAP-2605).
9. Before anything is answered, `AcceptanceDecisionRecordWriter` writes one decision record through the local library: the case, the valuation key, the accepted value, the appraisal date, the band with the policy version, the rule id where the source provides one, the acceptance marker `accepted_at` and the outcome. A failed write stops the step with nothing changed and nothing answered (DP-03; AC2, R-UNI-39).
10. The step answers the workflow with the acceptance; rwb-case applies the move from `VALUATION_ACCEPTED` on `VALUE_ACCEPTED` to the state its own route set names (R-DIL-09, R-DIL-12), and this service writes no case row.
11. The route operation answers `Approval` with the band, the accepted value and the appraisal elements of the baseline, which are optional elements of API-S1-001 with no second operation (GAP-2606), and a repeat of the same `Idempotency-Key` returns the stored answer and records no second acceptance (R-UNI-40).
12. The decision record reaches `rwb.decision-record.v1` through the library of DP-03, keyed by the case, with no personal data on it; this service publishes no event of its own (ASM-4309).
13. SCR-13 Route decision shows the accepted value, the band, the appraisal date and the overridden or submitted state, read only through the composite route; a later change of the value or of the band reopens the route decision as a fresh decision with a fresh record (REQ-S1-008).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, no acceptance is answered and the case does not move | MSG-P7-003 | AC2, TC-E4-004-02, TC-E4-004-04 |
| X2 | The caller does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | AC3, TC-E4-004-03 |
| X3 | A required element of the command is absent or invalid | Nothing is written and the field is named | MSG-GEN-001 | AC4, TC-S1-E4004-APP-05 |
| X4 | The submitted value does not match the appraisal of the asset on the case | The acceptance is refused with the reason and no record is written | MSG-GEN-001 | AC5, TC-S1-E4004-APP-06 |
| X5 | The appraisal is a flagged outlier whose flag is not cleared | The value is presented and the acceptance is refused; the case does not move | None (reason on the record) | AC6, TC-S1-E4004-APP-07 |
| X6 | The ACE data product is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on a fresh answer | MSG-P1-001 | AC7, TC-S1-E4004-APP-08 |
| X7 | The case is not at the route decision, or the appraisal is not on the case | The step does not run, nothing is accepted and the state is reported to the parent | None | AC8, TC-S1-E4004-APP-09 |
| X8 | rwb-source-data, rwb-case or rwb-decision does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 in the platform envelope | None | AC9, TC-S1-E4004-APP-10 |
| X9 | The same acceptance is submitted twice with the same `Idempotency-Key` | One record, one answer and no second move; the repeat is counted | None | AC10, TC-S1-E4004-APP-11 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC11, TC-S1-E4004-APP-01 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X9 are the paths the target call types and the acceptance add, and X10 is the DP-05 and DP-01 boundary. No band, threshold or limit is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4004-CON, the rwb-source-data, rwb-case, rwb-decision and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or P4 |
| Negotiable | The activity names, the decision code and the shape of the step outcome are this story's choice; the operation, the rules, the messages, the screen and the acceptance elements are fixed by the baseline |
| Valuable | The case owner accepts a value once and the route decision runs on a band that can be defended, with the record showing why |
| Estimable | One workflow step, two activities, four clients, one record write, one case move answer and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic appraisals through the contract fakes, plus the stopped record write, the stale product, the unmatched value, the uncleared flag and the duplicate command |

### 7. Acceptance criteria

```gherkin
Feature: Accept the appraisal value

  Scenario: AC1 Accept the appraisal value (legacy RWB-E4-004 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-source-data contract mock returns the appraisal "APR-2026-000404" of asset "AST-2026-000404" with outlier flag clear, no acceptance yet and a fresh stamp
    Given the rwb-case contract mock returns the case state "VALUATION_ACCEPTED" for "RC-2026-000404"
    Given the rwb-decision contract mock returns the band policy of the product group at its version in force
    When the user acts on the screen
    Then lets the case owner accept the value, which fixes the band the route decision runs on
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-004 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Access without the right (exception X2) (new, D-RCV-60)
    Given the rwb-access contract mock returns no Treatment and offer right for the caller
    When the caller calls the route operation
    Then the call is refused with 403 before any read or write and the user sees MSG-P4-002
    Then no decision record is written

  Scenario: AC4 A required element is absent (exception X3) (new, D-RCV-60)
    Given the route command for case "RC-2026-000404" omits a required element
    When the caller submits the acceptance
    Then nothing is written and the missing field is named with MSG-GEN-001

  Scenario: AC5 The value does not match the appraisal (exception X4) (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the appraisal "APR-2026-000404" of asset "AST-2026-000404" with a different value
    When the caller submits the acceptance
    Then the acceptance is refused with the reason and no decision record is written

  Scenario: AC6 A flagged outlier is not cleared (exception X5) (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the appraisal "APR-2026-000404" with its outlier flag set and not cleared
    When the caller submits the acceptance
    Then the value is presented, the acceptance is refused and the case does not move

  Scenario: AC7 The data product is stale (exception X6) (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the appraisal "APR-2026-000404" with a stale stamp after a late or failed batch
    When the caller submits the acceptance
    Then the step holds, writes nothing and shows MSG-P1-001 with the data date
    Then it resumes on a fresh answer

  Scenario: AC8 The case is not at the route decision (exception X7) (new, D-RCV-60)
    Given the rwb-case contract mock returns a case state other than the route decision for "RC-2026-000404"
    When the caller submits the acceptance
    Then the step does not run, nothing is accepted and the state is reported to the parent

  Scenario: AC9 rwb-source-data does not answer (exception X8) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer inside 2 s
    When the caller submits the acceptance
    Then the step waits and retries on the workflow schedule and nothing is written
    Then the caller sees 503 in the platform envelope

  Scenario: AC10 The same acceptance is submitted twice (exception X9) (new, D-RCV-60)
    Given the same acceptance is submitted twice with the same Idempotency-Key
    When the second submission arrives
    Then one record and one answer exist and no second move is made

  Scenario: AC11 A component reaches a v_ace view or another schema (exception X10) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row or another service's schema
    When the build runs its boundary test
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC12 The business rules of section 8 hold (BR1 to BR10) (new, D-RCV-60)
    Given the rules BR1 to BR10 of section 8 are in force for the build
    When the build runs its rule checks
    Then each rule of BR1 to BR10 holds and a failing rule fails the build

  Scenario: AC13 The route operation answers 401 and 403 (error answers of the provided operations) (new, D-RCV-60)
    Given the caller is not authenticated for the route operation
    When the caller calls the route operation
    Then the call is refused with 401 and nothing is written
    Then a caller without the right is refused with 403 as in AC3

  Scenario: AC14 A write is replayed with the same idempotency key (exception X9, replay) (new, D-RCV-60)
    Given the same acceptance was written once with an Idempotency-Key
    When the same command is replayed with that same Idempotency-Key
    Then the stored answer is returned and no second decision record is written

  Scenario: AC15 An activity is retried or times out (exception X8, retry) (new, D-RCV-60)
    Given an activity of the acceptance times out or is retried on the workflow's own schedule
    When the retry runs
    Then at most one decision record is written and no second move is made

  Scenario: AC16 A consumed call fails or does not answer (exception X8) (new, D-RCV-60)
    Given rwb-source-data, rwb-case or rwb-decision fails or does not answer
    When the caller submits the acceptance
    Then nothing is written, the case does not move and the caller sees 503 in the platform envelope

  Scenario: AC17 A status change the model does not allow is refused (status change of rwb-case) (new, D-RCV-60)
    Given the rwb-case contract mock refuses the move to VALUE_ACCEPTED with its reason
    When the caller submits the acceptance
    Then the acceptance is refused with the reason and no decision record is written
```

The two criteria are the legacy criteria of RWB-E4-004 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the user acts on the screen`, `the action is taken`, `the decision record cannot be written` and `lets the case owner accept the value` all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and those lines are the only additions to the legacy text. AC1 says the value "fixes the band the route decision runs on": in the target the band is read from the policy in force and recorded with its version, and the case move is answered to rwb-case; AC2 says the result is written "to the decision record with the rule version", which is the local decision record of DP-03 on its way to `rwb.decision-record.v1`. Neither criterion carries a business value: the band, its boundaries and the appraisal types are data in force (GAP-2605; ASM-4306). AC3 to AC11 are the criteria of the exception paths of section 5, AC12 is the criterion of the business rules of section 8, AC13 is the criterion of the error answers of the route operation, and AC14 to AC17 are the criteria of the replay, retry, failed-call and disallowed-transition paths, and AC3 to AC17 carry no legacy tag.

### 8. Business rules

| ID | BR ID | Rule | Message |
|---|---|---|---|
| VR-S1-004-1 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-4) | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-004 | BR12 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-38 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-4) | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-4) | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-4) | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |

The two VR and BR rows are the rows of FSD S1 A2.4.3.1, copied character for character. The three universal rules are the rows of the Business Rules and Routing Logic v4 that this step depends on; R-UNI-38 is why the record carries the band policy and the rule version in force on the business date.

| ID | Rule | Source |
|---|---|---|
| BR1 | The appraisal, its value, its date, its type and its outlier flag are ACE's and are read only on the rwb-source-data data product; this service holds no `v_ace_*` grant, keeps no copy and reads no appraisal row as a table | DP-05; Ownership Map rows of S1 |
| BR2 | The band is fixed from the accepted value and the policy in force, read with its version; no band, boundary, threshold or default is a constant of the build | FSD S1 A2.4.3.1 BR-S1-004; FEAT-ADM-04 |
| BR3 | An acceptance is of a value the valuer returned: the submitted value must match the appraisal of the asset on the case, and an unflagged outlier is not accepted | FSD S1 A2.4.2; R-DIL-09 |
| BR4 | The acceptance is recorded before anything is answered, with the case, the valuation key, the accepted value, the appraisal date, the band, the rule id and the version in force; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC2 |
| BR5 | The case is not this service's: no `recovery_case`, `assignment`, `task`, `timer` or `valuation` row is written here, and the case move is answered and not applied | Ownership Map (`recovery_case` owner P3) |
| BR6 | The band policy is administered by the product head under FEAT-ADM-04 and is read as data; this story neither sets nor approves a band | FEAT-ADM-04; BR-S1-004 |
| BR7 | One acceptance per case per value: a repeated command with the same `Idempotency-Key`, and a repeated fact with the same key, raise no second record and no second move | API-S1-001; R-UNI-40 |
| BR8 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the asset, the appraisal and the band are identifiers of other owners' facts | DP-01; TSD S1 T3.3 |
| BR9 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows; ASM-4309 |
| BR10 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input; the accepting user is an identifier, and it is held by the case, not here | Template and Rules v1 §R7.2 (s17); GAP-2603 |

### 9. State transitions

The case state is rwb-case's and is not changed by this story: the step reports its outcome and rwb-case applies it to the case of record (BR5). What this story owns is the state of the acceptance step, and the states the sources publish for it are the valuation states of the D6.4 route set: R-DIL-09 moves `AWAITING_VALUER` to `VALUATION_ACCEPTED` when the value is presented for acceptance, and R-DIL-12 moves `VALUATION_ACCEPTED` to the route's own next state on `VALUE_ACCEPTED` when `accepted_at` is set and the appraisal is within the age limit.

| From (case, on rwb-case) | Event | Condition | To |
|---|---|---|---|
| AWAITING_VALUER | VALUATION_RECEIVED | The report is attached and the value extracted | VALUATION_ACCEPTED, the value presented for acceptance |
| VALUATION_ACCEPTED | VALUE_ACCEPTED | The value is accepted by the case owner, `accepted_at` is set and the age is within the limit | The route's next state, and the band is fixed for the route decision |
| VALUATION_ACCEPTED | VALUE_NOT_ACCEPTED | The value is a flagged outlier or the command was refused | Unchanged, with the reason on the decision record (X4, X5) |
| VALUATION_ACCEPTED | The record cannot be written | X1 | Unchanged, nothing answered and no record (AC2) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The route command of a case at the route decision | The workflow is started on `rwb-valuation` | Reading the appraisal |
| Reading the appraisal | The data product answers fresh | The outlier flag is clear | Validating the command |
| Validating the command | The command matches the appraisal | The band policy in force is loaded | Fixing the band |
| Fixing the band | The band is fixed from the value and the policy version | The record is written and the transaction commits | Waiting, with the case move answered |
| Any | The record write, the transaction or a consumed row fails | X1, X8 | Waiting, nothing changed |

The state names are the rows of the D6.4 route set and live on the case of record. No S1 rule row is in force for this step, because the S1 package is Phase 2 (GAP-2605; ASM-4306).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the acceptance and read the appraisal, the band and the record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area, and the legacy table gives the case owner the primary use and the sale officer also uses it |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: they approve a route and they set the bands under FEAT-ADM-04, which is not this step |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step, reads the data product, answers the case move, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, forced_sale_value, appraisal_date | Read only, on the rwb-source-data data product (DP-05) |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` (P1 extension, read through rwb-source-data) | valuation_key, accepted, accepted_at, accepted_by, stale_flag, age_days | Read through the data product only; this service never writes the source-data schema. The acceptance is recorded in this service's decision record, and the extension has no published write (GAP-2603; ASM-4304). P1 open question OQ-P1-05 (who writes stale_flag and age_days, P1 or S1) stays open, and the stale flag and appraisal age get one writer once it is answered (GAP-1678) |
| The outlier flag of the appraisal (no Field ID published) | The flag that FEAT-VAL-03 sets and clears, on the appraisal of the data product | Its field id and its owner row are Not specified in the source documents (GAP-2604; ASM-4305) | Read on the data product |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | rule id, rule version, inputs reference, outcome, decided at | Write, one record per acceptance, before anything is answered |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule and its version arrive on the rwb-decision row |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read or written: the case state arrives on the rwb-case row and the move is answered |
| DF-WRK-009 to DF-WRK-016 | `assignment` (P3) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at | Not read or written: no task is raised by the acceptance |
| DF-COL-018 to DF-COL-027, DF-COL-043 and DF-COL-044 | `valuation` as TSD S1 T3.1 declares it | appraisal_no, appraisal_type, appraised_value, appraisal_date, accepted, stale_flag, age_days | Not written here: the store of the acceptance is not fixed (GAP-2603; ASM-4304) |
| The band and its policy version | The policy administered under FEAT-ADM-04 (P4) | the band fixed by the accepted value, and the version of the policy it was fixed under | Consumed as data, recorded in the decision record, never stored as a column |

Field IDs are those of the Logical Data Model and Data Dictionary v9, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. The IDs DF-COL-018, DF-COL-027, DF-COL-043 and DF-COL-044 are as TSD S1 T3.1 declares them, and their presence in the Logical Data Model v9 is open with its owner. `decision_record` is a PLT library object, not a field or entity of the Logical Data Model v9 or of Data Classification v5; the decision-log wording of AC2 is the decision record of DP-03. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). Where the data owner confirms a `valuation` table or an acceptance column, the DB story adds it and this story's writer fills it; until then the accepted value, the band and the marker live in the decision record and in the answer to the case.

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and a rule version. The identity of the accepting user is an identifier held by the case and the access layer; no name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, an interface input or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy Endpoints table names, and its shape is baselined by RWB-S1-E4004-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the acceptance of the valuation key with its value and the band in the answer, plus the override reason where the answer departs from the recommendation (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second acceptance is recorded |

The element list of `RouteRequest` and `Approval` is not published: TSD S1 T-A.2 names the two types and no field table (GAP-2606; ASM-4307). The acceptance adds no operation of its own; where the accepted value needs a write of its own, no owner publishes one and the baseline declares none (GAP-2603; ASM-4304). The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid or unmatched element, and 503 when the decision library or a consumed row does not answer. The two valuation operations of the map belong to the appraisal-intake slice of RWB-S1-E4002-CON and are not touched here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal, outlier-flag and acceptance data-product read (operation name Not specified in the source documents (GAP-2604; ASM-4305)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The appraisal, its value, its date, its type, the outlier flag, the acceptance state and the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the asset link, checked before an acceptance is recorded; read only; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2604; ASM-4305)) | `/api/recovery/case/v1` | P3 rwb-case | The move from `VALUATION_ACCEPTED` on `VALUE_ACCEPTED`, applied by the case of record; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2604; ASM-4305)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force, the band policy element where it is carried there, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The band policy is administered under FEAT-ADM-04 and no source says whether its row travels on the rule-in-force answer, on a reference-data answer or through rwb-access; the step reads it on the answer its owner publishes and asserts no boundary (GAP-2605; ASM-4306). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2604 with ASM-4305.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR9). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. The acceptance is started by the case owner's command on the route operation and by nothing else; the ownership rows give S1 no event and no job, FSD S1 A2.4.4.4 declares no background event for the feature, and no source publishes a name for a value-accepted notice (ASM-4309). A duplicate of the command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new; started by CaseWorkflow as a child; workflow ID form: Not specified in the source documents (CG-ALL-8004); duplicate-start policy: Not specified in the source documents (CG-ALL-8004) | `rwb-valuation` | Input: the case, the asset key, the valuation key, the route set and the rule package in force; signals: the freshness answer and the case-move answer |
| `acceptAppraisalValue` | Activity, the acceptance of this story | `rwb-valuation` | The valuation key, the asset key, the submitted value, the appraisal date and the band policy in force in; the band, the acceptance marker and the step outcome out |
| `recordAcceptance` | Activity, the record of this story | `rwb-valuation` | The decision record, the idempotency row and the case-move answer out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The step runs inside the workflow from the case owner's command and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job. No reminder or re-review timer is built here: the review of a held route decision belongs to FEAT-VAL-10 and to rwb-case's timers.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the store of the accepted value, `accepted_at` and the band is not fixed (GAP-2603; ASM-4304) |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per acceptance (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `valuation` as TSD S1 declares it, every `v_ace_*` view and `valuation_ext` (P1). No foreign key leaves `rwb_valuation`: the case, the asset, the appraisal and the band are identifiers, not keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | Appraisal `APR-2026-000404` of asset `AST-2026-000404` with its value, type, date and a fresh stamp, outlier flag clear and no acceptance yet; the same asset with the flag still open; the same asset already accepted; a stale product with its date; no answer beyond 2 s | AC1, X5, X6 |
| rwb-case case-state fake | Case `RC-2026-000404` at `VALUATION_ACCEPTED` with its asset link; a case in another state | X7 |
| rwb-case move-answer fake | The move from `VALUATION_ACCEPTED` on `VALUE_ACCEPTED` accepted with its reference, and refused with its reason | TC-E4-004-01 |
| rwb-decision rule and log fake | The rule id and the band policy at their version in force for the business date; the record the ledger holds | AC1, TC-E4-004-01 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-004-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000404`, with the appraisal, the band and the route elements read once | AC1, TC-E4-004-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2604; ASM-4305).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data product, the rwb-case case-state and move rows, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `acceptAppraisalValue` and `recordAcceptance` on `rwb-valuation`; no Schedule |
| File | None of this service | The appraisal arrives through ACE ingestion and the rwb-source-data data product, and this service writes no file (DP-05) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `acceptance`, Java package `th.co.scb.ace.workbench.recovery.valuation.acceptance`; front end `src/modules/recovery/valuation/RouteAcceptance.tsx`, the fragment SCR-13 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant and reads no ACE view and no ACE table, and the appraisal and its flag are the ones the rwb-source-data contract answers. DP-03 is the transaction rule of the step: the record, the idempotency row and the case-move answer commit together or not at all. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2604 (ASM-4305). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added. DP-06 and DP-07 are not in this story's pattern set, so the band policy adds no dependency and its row is read on the answer its owner publishes (GAP-2605).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` acceptance branch | Workflow | Waits for the command, runs the acceptance, answers the case move and reports the outcome to the parent |
| `acceptAppraisalValue` | Activity | Reads the appraisal on the data product, validates the command against it, tests the outlier flag and fixes the band from the policy in force |
| `recordAcceptance` | Activity | Writes the decision record and the idempotency row, answers the case move and returns the band and the outcome |
| `SourceDataProductClient` | Client | The appraisal, outlier-flag and acceptance read of rwb-source-data, one hop, 2 s, breaker, with the stale path |
| `CaseStateClient` | Client | The case state, the asset link and the move answer of rwb-case, one hop, 2 s |
| `RuleInForceClient` | Client | The rule id and the band policy at their version in force, from rwb-decision, one hop, 2 s |
| `AccessClient` | Client | The capability area, the right and the scope of the caller, one hop, 2 s |
| `AcceptanceDecisionRecordWriter` | Library adapter | Writes one record per acceptance before anything else changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteAcceptance` | React component | Shows the accepted value, the band, the appraisal date and the refused, held and stale states on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the accepted value, `accepted_at` or the band: they are recorded in the decision record and answered to the case, and the store is GAP-2603 until its owner names it.

**Configuration and reference data.**

- The band policy, the appraisal types of `LOV-APPRAISAL` and the route codes of `LOV-ROUTE` at their version in force (TSD S1 T3.2), read as data and never as constants.
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- The consumer of the library's topic `rwb.decision-record.v1` is the ledger's; this service only writes the record.
- No parameter is named in the sources for the band or for the step, and no S1 rule package is in force (GAP-2605; ASM-4306).
- Parameter and reference-data reads: the parameter names are Not specified in the source documents (DOR-RWB-S1-E4004-APP-20).

**Build steps**

1. The acceptance branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the route command as its trigger.
2. `SourceDataProductClient` against its fake, with the 2 s budget, the breaker, the stale path and the no-answer path (X6, X8).
3. `AccessClient` and the right check, with the refused path (X2).
4. `acceptAppraisalValue` with the required-element, unmatched-value and uncleared-flag paths (X3, X4, X5).
5. `RuleInForceClient` and the band fixed from the policy in force, with its version recorded (BR2).
6. `recordAcceptance` and `AcceptanceDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
7. The idempotency row and the repeat of the same command (X9).
8. `CaseStateClient` and the state guard of the step (X7).
9. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-004-03).
10. `RouteAcceptance` and SCR-13 through the composite route fake (TC-E4-004-01).
11. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to another service's schema, and no outbox row (X10, BR8, BR9).

**Feature flag.** `rwb.valuation.acceptance-v1`, read as a flag of the platform library; off means the acceptance is refused with its reason and the route decision stays on the value it holds.

**Done when.** The tests of section 16 pass, an acceptance fixes one band with its policy version in SIT, a refused or unmatched value writes nothing, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the command is absent or invalid, or the submitted value does not match the appraisal (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the acceptance changes anything (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the appraisal is stale after a late or failed batch (X6) | {product} is from {date}. Today's load has not arrived. |

The three messages of the legacy key are copied unchanged from its message set, and MSG-P1-001 is the module's freshness message of FSD S1 A2.1.3.1, cited here because FSD S1 A1.4 makes the freshness of every data product a precondition. No message is reworded and no new one is added.

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the acceptance part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Empty: Not specified in the source documents (CG-ALL-8011); loading; recommendation; overridden; submitted; error: Not specified in the source documents (CG-ALL-8011); no access: refused with MSG-P4-002 | Loading while the appraisal is read; recommendation with the value, its appraisal date, its outlier state and the band it would fix; overridden with the owner's reason; submitted with the accepted value and the band. Plus refused with MSG-P4-002, not recorded with MSG-P7-003, invalid or unmatched with MSG-GEN-001, stale data with MSG-P1-001, and held while the outlier flag is not cleared |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the acceptance element list and the five service states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-004-01 | AC1: the acceptance fixes the band and records it with the rule version; an unmatched value, an uncleared flag and a stale product write nothing; BR2, BR6 and BR12 | Component | Case `RC-2026-000404`, asset `AST-2026-000404`, appraisal `APR-2026-000404`, an unmatched value, an open outlier flag and a stale product |
| TC-E4-004-02 | AC2: the decision record cannot be written; BR4 | Component | The decision-record stub stopped; nothing written, no case move and MSG-P7-003 shown |
| TC-E4-004-03 | AC3: access, a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-004-04 | Principle 5: a forced decision record write failure; BR9 | NFR | A forced failure at the moment of the acceptance; no record, no move and no event |
| TC-S1-E4004-APP-01 | AC11, BR1 and BR9: the boundary: no `v_ace_*` read, no foreign schema write and no published event | Component | The build scan of step 11, plus an outbox that must stay empty |
| TC-S1-E4004-APP-02 | Idempotency: the same command twice under one key records one acceptance and answers the stored answer; BR7 | Component | The same command repeated within the key's life, and a second command under a new key |
| TC-S1-E4004-APP-03 | Contract: the operations, events and activities of §12 answer their documented shapes, with the route operation and the rwb-source-data, rwb-case and rwb-decision reads | Contract | The contract mocks of §13 and the route command for `RC-2026-000404` |
| TC-S1-E4004-APP-04 | BR5 and BR8: the tables of §12.7 are the only tables written here, and no case, assignment, task, timer or other owner's table is written or read | Component | The build scan of step 11 against the tables listed in §12.7 |
| TC-S1-E4004-APP-05 | AC4: a required element of the command is absent; nothing is written and the field is named with MSG-GEN-001 | Component | The route command for `RC-2026-000404` without one required element |
| TC-S1-E4004-APP-06 | AC5 and BR3: the submitted value does not match the appraisal `APR-2026-000404`; the acceptance is refused with the reason and nothing is written | Component | An unmatched value for asset `AST-2026-000404` |
| TC-S1-E4004-APP-07 | AC6 and BR3: a flagged outlier whose flag is not cleared; the value is presented, the acceptance is refused and the case does not move | Component | Appraisal `APR-2026-000404` with its outlier flag set and not cleared |
| TC-S1-E4004-APP-08 | AC7: the ACE data product is stale after a late or failed batch; the step holds, writes nothing and shows MSG-P1-001 | Component | A stale stamp on appraisal `APR-2026-000404` |
| TC-S1-E4004-APP-09 | AC8: the case is not at the route decision; the step does not run, nothing is accepted and the state is reported to the parent | Component | Case `RC-2026-000404` in a state other than the route decision |
| TC-S1-E4004-APP-10 | AC9: rwb-source-data does not answer inside 2 s or its breaker is open; the step retries, writes nothing and the caller sees 503 | Component | A no-answer fake for rwb-source-data |
| TC-S1-E4004-APP-11 | AC10: the same acceptance is submitted twice with the same `Idempotency-Key`; one record, one answer and no second move | Component | The same command repeated under one key |
| TC-S1-E4004-APP-12 | BR10: no person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input | Component | Synthetic fixtures only; the accepting user as an identifier |
| TC-S1-E4004-APP-13 | AC12, BR1 to BR10: the business rules of section 8 hold | Component | Not specified in the source documents (NEWAC-RWB-S1-E4004-APP-AC12) |
| TC-S1-E4004-APP-14 | AC13: the route operation answers 401 and 403 as the error answers of the provided operations | Component | Not specified in the source documents (NEWAC-RWB-S1-E4004-APP-AC13) |
| TC-S1-E4004-APP-15 | AC14: a write replayed with the same `Idempotency-Key` returns the stored answer and writes nothing new; BR7 | Component | The same command repeated within the key's life |
| TC-S1-E4004-APP-16 | AC15: an activity is retried or times out; at most one record is written and no second move is made | Component | A timed-out fake for a workflow activity |
| TC-S1-E4004-APP-17 | AC16: a consumed call to rwb-source-data, rwb-case or rwb-decision fails or does not answer; nothing is written, the case does not move and the caller sees 503 | Component | A no-answer fake for rwb-case |
| TC-S1-E4004-APP-18 | AC17: a status change the model does not allow is refused with its reason; no record is written | Component | A rwb-case move-answer fake refusing the move to `VALUE_ACCEPTED` |

The four legacy case IDs are the legacy cases of RWB-E4-004 in their legacy order, with the Level column added. TC-E4-004-01 is Component because the step is tested on its fakes; the legacy wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the band, its boundaries, the appraisal types and the route codes stay reference data or a rule row read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the move is answered and not applied (BR5).
- The decision is recorded before the change and the command is idempotent; a build that answers a move before its record fails the review (DP-03, BR4, BR7).
- The band is not set, approved or overridden here: a build that writes a band or a floor fails the review (BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.

### 18. Traceability

| Source | Reference | L3 process | Used in |
|---|---|---|---|---|
| Legacy story | RWB-E4-004, disposition Split (rework); AC1 and AC2 owned word for word by this story | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 1, 7, 16 |
| Feature | FEAT-VAL-04 Accept the appraisal value, module S1, epic E4, depends on FEAT-VAL-03; the band policy is FEAT-ADM-04 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 1, 2, 3, 8 |
| FSD S1 v3 | A1.4 preconditions; A2.4.2 steps and integration points; A2.4.3.1 VR-S1-004-1 and BR-S1-004; A2.4.3.2 field catalog; A2.4.3.3 roles; A2.4.4.1 to A2.4.4.4; REQ-S1-002, REQ-S1-003 and REQ-S1-008; SCR-13 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 2, 3, 4, 5, 8, 11, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 `LOV-APPRAISAL` and `LOV-ROUTE`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 3, 10, 11, 12, 13, 16 |
| Logical data model | DF-ACE-187 to DF-ACE-195, DF-EXT-036 to DF-EXT-049, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-COL-018 to DF-COL-027 and DF-COL-043 to DF-COL-044 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 11 |
| Routing logic | R-UNI-38, R-UNI-39 and R-UNI-40; R-DIL-09 and R-DIL-12 and the valuation states of the D6.4 route set; no S1 route rule is in force, because the S1 package is Phase 2 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 4, 8, 9, 14 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 13 |
| Gaps and assumptions | GAP-2603, -2 and -3; GAP-1678; ASM-4304, -2, -3 and -6; the contract gaps GAP-2606 and -5 belong to RWB-S1-E4004-CON and are cited here where the element set is read | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | 1, 3, 4, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | Not specified in the source documents (DOR-RWB-S1-E4004-APP-2) | all |

### 19. Out of scope

- The published shape of the route operation, the acceptance element set, the five consumed rows, the decision-record element, the workflow elements, the error set and the fakes: RWB-S1-E4004-CON.
- The appraisal intake of FEAT-VAL-02 and the outlier flag of FEAT-VAL-03: the sibling appraisal stories of this service, and the `POST /assets/{assetId}/valuations` and `POST /assets/{assetKey}/valuations` operations of RWB-S1-E4002-CON.
- The COLLINS return by route, the payoff and settlement range, the route agent, the approvals inside and above the limit, the hold and the reconsideration, and the route-flow start of FEAT-VAL-05 to FEAT-VAL-12: the sibling route stories of this service.
- The ACE appraisal, collateral and acceptance facts and the freshness of the data product: rwb-source-data (P1). The store of the accepted value, `accepted_at` and the band: the data owner of this service (GAP-2603).
- The band policy, its identifiers and its boundaries, and the administration of bands, floors and ranges per product: rwb-access and the product head under FEAT-ADM-04 (GAP-2605).
- The case of record, its valuation states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
