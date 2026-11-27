# RWB-P4-E2042-APP Epic 2 rule packages in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2042-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-042 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AY |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E2042-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2042-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E2042-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CWC-013, REQ-CWC-014) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-042 for rwb-access, authority slice. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2042-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 37 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE), a risk and model risk officer (RW-RISK), and the access service that answers who may change a rule package version**, I want **every load, approval, rollback and dry run of an Epic 2 rule package version decided against the versioned role and permission matrix, the author of a version refused the right to approve it, a running service identity entitled to evaluate a package only for the capability area it holds, and every answer written to the access log**, so that **a rule change stays a four-eyes, dated, auditable data change inside `rwb-decision`, and no rule-package work in `rwb-access` can load, approve, roll back or evaluate a package outside the authority the matrix grants**.

Inside `rwb-access` this is the authority slice of the legacy story RWB-E2-042:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the rule-package part of the existing `POST /api/recovery/access/v1/authorise`, which answers whether one caller may `LOAD`, `APPROVE`, `ROLLBACK`, `DRY_RUN` or `EVALUATE` one package version, and names the matrix version it used; and the access-log entry of each of those answers.
- No new path, no table, no workflow, no Schedule, no screen and no rule content. The operation this story extends is the service baseline's, and it is published by the authorise contract of the P4 service (RWB-P4-E1037-CON).
- Screen SCR-39 of P3 is not built by this story; its empty, loading, error and no-access states are Not specified in the source documents (DOR-RWB-P4-E2042-APP-10) and belong to the screen owner.
- The registry stays in `rwb-decision` (P7) under ASM-0069 and Architecture v5 slides 27 and 41: the workbook, the compile to DRL and the KieBase, the checksum, the compile, schema, overlap, unreachable row, default row, scenario and dry run checks, the at-least-50 scenario gate, the four-eyes approval record, the promotion at 00:01 by JOB-20 with `RulePackageInForce` (EV-30), the one-call rollback and the dry run counts. This story does none of it, and it holds no rule table.
- The package content and the evaluation itself are outside this slice. The embedded Drools kit of DP-04 is how a service evaluates a package inside activity code; this story decides only whether a service identity is entitled to evaluate a package for a capability area. The evaluation, the model read, the checksum check and the cache of KieBase instances are the owning service's and `rwb-decision`'s.
- The service builds against `RWB-P3-E2042-CON` and its fakes: the workbook Rows and Tests schema, the Blob object naming and metadata, the five consumed `rwb-decision` operations, the `RulePackageInForce` consumption contract, the `EvaluateRules` activity contract, the cache and swap rules, and the `rwb-decision` WireMock.
- The TSD P4 v3 T3.1 gives P4 the four rule tables (`rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`) and T6.1 gives P4 the rights over them. Architecture v5 slides 27 and 41 and the R-PREC default ruling put the registry in P7, so this slice reads the ruling as P7 and the authority as P4 — Not specified in the source documents (GAP-0968; ASM-1702). The four tables are P7's tables, and their declarations in the P4 and P3 TSDs are recorded at GAP-1301.
- The action vocabulary, the request and answer shape of the rule-package part of the authorise operation and the access-log decision code of a rule-package change are Not specified in the source documents (GAP-0966; ASM-1700); this story fixes them as its own contract and raises them for confirmation.
- The scope of the `rwb-decision` service identity, and of any running service identity, inside `rwb-access` is Not specified in the source documents (GAP-0967; ASM-1701).

### 2. Business rationale

Rule changes are an audit finding on two counts: a rule that reaches production without a second person, and a person who approves their own change. D-RCV-36 T4 puts the four-eyes rule into the target design, Architecture v5 slide 27 keeps governance central in `rwb-decision`, and the permission matrix of TSD P4 v3 T6.1 splits the rights: RW-COE uploads, lists, dry-runs and rolls back, RW-RISK approves and the author cannot approve. The split is only a control if the engine that owns the change asks one service who may make it, and if the answer is the same answer for every load, approval, rollback and dry run.

Legacy RWB-E2-042 loaded three workbooks through the monolith loader and relied on the in-process `RecoveryAccessGuard` for the right and on a service-level check for the author. In the target the registry is `rwb-decision`'s and the authority is `rwb-access`'s, so `rwb-decision` can accept a workbook, refuse an approval and roll a version back without ever holding a role row, the letter or the matrix version. This story gives it that answer, and nothing else.

This story meets REQ-CWC-013 and REQ-CWC-014 on the authority side: a rule change is made by a validated load under a version, and the second pair of eyes is a decision of a service that is not the loader. It supports the measure that rule and limit changes are made without a code release at 100 percent (FSD P4 v3 A2.1 and A2.4), because a matrix change is a new version of `permission` and no build. It puts the four-eyes control and the separation of duties within reach of the P7 registry and of every service that evaluates a package.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2042-CON | The published contract of the legacy key: the workbook Rows and Tests schema (RuleSet = package code, NAME = rule ID, the default row last), the Blob object naming and metadata, the five `rwb-decision` operations, `RulePackageInForce`, the `EvaluateRules` activity contract with `RuleResult` and `NoPackageInForce`, the cache and swap rules, and the `rwb-decision` and `rwb-access` fakes. This story builds against that document and those fakes |
| RWB-P7-E2042-APP (same legacy key, another service) | The registry: `rule_package` and `rule_package_version`, the three package rows, the compile, the checks, the scenario run, the dry run, the four-eyes approval record, JOB-20 and the rollback (ASM-0069). This story answers the authority and writes no row of it |
| RWB-P4-E1037-CON (same service, its own contract story) | The authorise contract: the base `/api/recovery/access/v1`, the `POST /authorise` operation, the role and permission tables behind it, the guard library, and the ADR refusal shape with MSG-P4-002. This story adds the rule-package action to that operation; it adds no path |
| The role and permission tables of the service baseline | `role` (DF-REF-034 to DF-REF-039) and `permission` (DF-REF-040 to DF-REF-044) with the matrix version in force, created and loaded by the legacy RWB-E1-022 and RWB-E1-037 slices of this service. This story reads them and writes no row |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the access-log entry of every load, approval, rollback and dry run |
| RWB-PLT-E1072-CON, RWB-P7-E1073-CON | The embedded Drools kit and the registry's model-read contract (DP-04). This story embeds no kit and reads no model; it decides whether a service identity may |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06), for the lifetime of the cached authorise answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-CAPABILITY, LOV-ROLE and LOV-VERSION-STATUS with the version in force |
| RWB-PLT-E1047-CON | The topic and event naming library (DP-14) |
| RWB-PLT-E1071-CON | The workflow kit in namespace `rwb-recovery` (DP-10); this story starts no workflow. JOB-20 runs in `rwb-decision` and the six-monthly access review JOB-18 in this service's own story |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15); this story owns no migration |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19); no screen of this story is served through it |

Business preconditions carried from RWB-E2-042:

- Package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are seeded with owner role RW-COE; the three version labels RES-2026.12, PMT-2026.12 and BKG-2026.12 are valid from 15 December 2026.
- The workbooks carry 38 rows and 62 scenarios, 3 rows and 58 scenarios, and 21 rows and 54 scenarios, and `rules.testcases.min` is 50.
- Matrix version PM-2026.11 is in force in SIT and gives RW-COE "CRUD", RW-RISK "RA", RW-AUDIT "R" and RW-REFADM "R" in Rules and parameters (TSD P4 v3 T6.1).
- RW-COE and RW-RISK are two different people, and the same person never holds both (the `role_conflict` rows of the service baseline).
- The matrix version loaded, approved and in force is a version of `permission` like any other reference load; this story reads it and never writes it.
- The capability area of the PAYMENT_MATCH and BOOKING_MATCH packages is Not specified in the source documents (GAP-0967; ASM-1701); RESTRUCTURE serves TREATMENT_AND_OFFER.

### 4. Flow

1. `rwb-decision` (P7), on the load, approve, rollback or dry run operation it owns, calls `POST /api/recovery/access/v1/authorise` through the guard library with the caller's user reference taken from the session, `action`, `packageCode`, `versionLabel`, `authorRef` (required on `APPROVE`), `capabilityArea` and `right`.
2. `RulePackageAuthorityController` validates the request: `action`, `packageCode`, `capabilityArea` and `right` are required, and `authorRef` is required when the action is `APPROVE`; an empty one is 422 with MSG-GEN-001 naming the field.
3. `ActionCatalog` resolves the action to the letter it needs: `LOAD` to C, `APPROVE` to A, `ROLLBACK` to U, `DRY_RUN` to R and `EVALUATE` to R. An action outside the five is 422 with MSG-GEN-001 naming the action, and a request whose `right` does not match the action is 422 as well, so a caller cannot ask for a weaker letter than the action needs.
4. `PermissionReader` reads the caller's effective letters: the union of the `permission` rows of every role the caller holds, in the capability area of the request and with the matrix version in force on the business date. A caller with several roles gets the union and never the intersection (FSD P4 v3 AC-ALT-P4-001-02).
5. Authority decision on `LOAD`: the caller must carry C in Rules and parameters. A caller without it is refused, and nothing is loaded.
6. Authority decision on `APPROVE`: the caller must carry A in Rules and parameters, and the caller must not be the author of the version. `SeparationOfDutiesCheck` compares `authorRef` with the caller reference and refuses the approval with `AUTHOR_IS_APPROVER` and MSG-P7-002 when they are equal, whatever letters the caller holds. The approval that is granted is therefore always a second person (BR2).
7. Authority decision on `ROLLBACK`: the caller must carry U in Rules and parameters. The reason, the pointer to the earlier version and the state change are `rwb-decision`'s; this service answers the right and no more.
8. Authority decision on `DRY_RUN`: the caller must carry R in Rules and parameters. The dry run counts are the registry's; this service answers the right, and the counts are read by the caller (BR4).
9. Authority decision on `EVALUATE`: the caller is a running service identity, and it must carry R in Rules and parameters and R in the capability area the package serves. A package whose area the identity holds no letter in is refused, so a service cannot use a rule package to decide in an area it may not act in (BR5).
10. The answer is `authorised` true with `reason` `ALLOWED`, `matrixVersion`, `area`, `right` and `entryRef`, or `authorised` false with `reason` `NO_LETTER`, `AUTHOR_IS_APPROVER` or `NO_PACKAGE_AREA` and the message id; a refusal is 403 with an RFC 9457 problem response and `messageId` set.
11. Every answer appends one entry to the access log before it leaves the service: a decision-record entry of the local library of DP-03 with the caller reference, the action, the package code, the version label, the area, the right, the matrix version and the time. A load, an approval and a rollback carry decision code "AC-CHG", a dry run and an evaluation carry "AC-READ" and a refusal carries "AC-DENY". The entry carries no name, no e-mail address and no personal field (BR6).
12. Where the entry cannot be written the answer is not returned: the call fails with 503 and MSG-P7-003, and the caller loads nothing, approves nothing, rolls nothing back and evaluates nothing (BR6, AC9).
13. The answer is cached per identity, area, right, action, package code and matrix version, and the cache is dropped when a new matrix version becomes in force through `rwb.access.AccessPolicyChanged.v1`. The lifetime of the cached answer is a parameter row of `rwb-case` read through DP-06, and its value is Not specified in the source documents (GAP-0969; ASM-1703).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, or `authorRef` is missing on an approval | 422, nothing is decided and no entry is written | MSG-GEN-001 | AC1 |
| X2 | The action is outside the five, or the `right` does not match the action | 422 naming the action, nothing decided | MSG-GEN-001 | AC1 |
| X3 | The caller holds no C in Rules and parameters and asks to load | 403, no load authorised, one "AC-DENY" entry | MSG-P4-002 | AC1 |
| X4 | The caller holds no A and asks to approve, as RW-COE does | 403, no approval authorised, one "AC-DENY" entry | MSG-P4-002 | AC3 |
| X5 | The caller holds A but is the author of the version | 403 with `AUTHOR_IS_APPROVER`, whatever the letters are | MSG-P7-002 | AC2 |
| X6 | The caller holds no U and asks to roll back | 403, no rollback authorised; the version stays in force | MSG-P4-002 | AC4 |
| X7 | The caller holds no R and asks for a dry run | 403, no dry run authorised and no count read | MSG-P4-002 | AC5 |
| X8 | A service identity holds R in Rules and parameters but no letter in the package's capability area | 403 with `NO_PACKAGE_AREA`, and no model is read and nothing is evaluated | MSG-P4-002 | AC6 |
| X9 | The decision record cannot be written | 503 and no answer; the load, approval, rollback or evaluation is not given | MSG-P7-003 | AC9 |
| X10 | The same check arrives twice with the same parameters | Both are answered and each writes its own entry, because a decision is an event and not a state change | None | AC7 |
| X11 | The version named is not in the state the action allows, for example an approval of a REFUSED version | This service answers the authority and reads no version state; the refusal is `rwb-decision`'s 409 on its own operation | None (rwb-decision) | AC3 |

No exception path of this story changes a version, a package, a case or a task: this service answers and records, and the version state machine is `rwb-decision`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the authorise contract of RWB-P4-E1037-CON and the fakes of RWB-P3-E2042-CON; it reads `role` and `permission` in its own schema and calls nothing cross-service |
| Negotiable | Roles, letters, areas, matrix versions, packages and version labels are rows; the five actions are the contract of section 12.1 and nothing else is fixed |
| Valuable | One answer replaces a per-module guard copy, and the four-eyes rule becomes a decision of a service that is not the loader |
| Estimable | One extended operation, one permission reader, one separation-of-duties check, one entitlement check, one record appender and one cache |
| Small | Fits two weeks with its tests; no table, no migration, no workflow and no screen of its own |
| Testable | Each criterion has a test case in section 16 and the registry side is stubbed in the `rwb-decision` fake |

### 7. Acceptance criteria

```gherkin
Feature: Epic 2 rule packages in Drools, authority slice

  Background:
    Given the environment is SIT
    Given matrix version "PM-2026.11" is in force and gives RW-COE "CRUD", RW-RISK "RA", RW-AUDIT "R" and RW-REFADM "R" in Rules and parameters
    Given package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH are seeded with owner role RW-COE
    Given rules.testcases.min is 50 and the business date is 10 December 2026
    Given test user "U-41" holds RW-COE and test user "U-51" holds RW-RISK, and they are two different people

  Scenario: AC1 A loader with C in Rules and parameters may load a version (new, D-RCV-60)
    Given the rwb-decision contract mock returns package "RESTRUCTURE" with version "RES-2026.12" LOADED, authored by "U-41", valid from 15 December 2026, 38 rows and the test result "62 of 62 scenarios passed"
    When "U-41" is checked through POST /api/recovery/access/v1/authorise for action "LOAD", package "RESTRUCTURE", version "RES-2026.12", area "RULES_AND_PARAMETERS" and right "C"
    Then the response is 200 with authorised true, reason "ALLOWED", right "C", area "RULES_AND_PARAMETERS", matrixVersion "PM-2026.11" and an entryRef
    Then rwb-decision accepts the workbook under its own checks and stores version "RES-2026.12" as LOADED with 38 rows and 62 of 62 scenarios passed
    Then this service writes no rule row, no checksum and no test result, and holds no rule table

  Scenario: AC2 The author of a version cannot approve it (new, D-RCV-60)
    Given the rwb-decision contract mock returns version "RES-2026.12" LOADED and authored by "U-41"
    Given "U-41" also holds a role that carries the A letter in Rules and parameters
    When "U-41" is checked through POST /api/recovery/access/v1/authorise for action "APPROVE", version "RES-2026.12", area "RULES_AND_PARAMETERS" and authorRef "U-41"
    Then the response is 403 with authorised false, reason "AUTHOR_IS_APPROVER" and message MSG-P7-002
    Then one entry is written with decision code "AC-DENY", the caller "U-41", the action "APPROVE" and version "RES-2026.12"
    Then rwb-decision leaves version "RES-2026.12" LOADED and nothing is in force

  Scenario: AC3 Only the A letter approves, and RW-COE carries no A (new, D-RCV-60)
    Given the rwb-decision contract mock returns version "PMT-2026.12" LOADED, valid from 15 December 2026 (value of RWB-E2-042; reconciliation with RWB-E2-027 open), authored by "U-41", with 3 rows and "58 of 58 scenarios passed"
    Given test user "U-54" also holds RW-COE and is not the author of version "PMT-2026.12"
    When "U-54" is checked for action "APPROVE" on version "PMT-2026.12" with authorRef "U-41"
    Then the response is 403 with message MSG-P4-002, because RW-COE carries no A in Rules and parameters, and no approval is authorised
    When "U-51" is checked for the same action on the same version with authorRef "U-41"
    Then the response is 200 with authorised true, right "A" and matrixVersion "PM-2026.11"
    Then two entries are written, one "AC-DENY" for "U-54" and one "AC-CHG" for "U-51", and neither carries a name or an e-mail address

  Scenario: AC4 A rollback needs U, and a read-only role is refused (new, D-RCV-60)
    Given the rwb-decision contract mock returns version "BKG-2026.12" IN_FORCE from 15 December 2026 with 21 rows and "54 of 54 scenarios passed"
    Given "U-52" holds RW-AUDIT, whose only letter in Rules and parameters is R
    When "U-52" is checked for action "ROLLBACK" on version "BKG-2026.12" and right "U"
    Then the response is 403 with message MSG-P4-002 and no rollback is authorised
    When "U-41" is checked for the same action and right
    Then the response is 200 with authorised true and right "U"
    Then version "BKG-2026.12" stays IN_FORCE until rwb-decision acts, and this service changes no version state

  Scenario: AC5 A dry run needs R and reads open cases without changing one (new, D-RCV-60)
    Given the rwb-decision contract mock returns version "RES-2026.12" LOADED with dry run counts of 412 decisions over 412 open cases
    When "U-52" is checked for action "DRY_RUN" on version "RES-2026.12" and right "R"
    Then the response is 200 with authorised true, right "R" and matrixVersion "PM-2026.11"
    Then one entry is written with decision code "AC-READ", the version label and the dry run action, and no case ID and no personal field
    Then no case, task or decision of the 412 open cases is changed by the dry run

  Scenario: AC6 A running service identity evaluates a package only for its own area (new, D-RCV-60)
    Given the rwb-decision contract mock returns package "RESTRUCTURE" version "RES-2026.12" in force from 15 December 2026 with packageArea "TREATMENT_AND_OFFER"
    Given the service identity of rwb-treatment carries R in Rules and parameters and R in Treatment and offer
    Given the service identity of rwb-debtsale carries R in Rules and parameters and no letter in Treatment and offer
    When the rwb-treatment service identity is checked for action "EVALUATE", package "RESTRUCTURE" and area "TREATMENT_AND_OFFER"
    Then the response is 200 with authorised true, right "R", area "RULES_AND_PARAMETERS" and packageArea "TREATMENT_AND_OFFER"
    When the rwb-debtsale service identity is checked for the same action, package and area
    Then the response is 403 with authorised false, reason "NO_PACKAGE_AREA" and message MSG-P4-002
    Then no model is read and nothing is evaluated for that identity

  Scenario: AC7 Every load, approval, rollback and dry run leaves one access-log entry (new, D-RCV-60)
    Given the decision-record store is available and its hash chain verifies
    When one load, one approval, one rollback and one dry run are authorised in that order
    Then four entries are appended, each with the caller reference, the action, the package code, the version label, the area, the right, the matrix version and the time
    Then the load, the approval and the rollback carry decision code "AC-CHG", which is Not specified in the source documents (GAP-0966; ASM-1700) and is the default this story uses for a rule-package change, and the dry run carries "AC-READ"
    Then neither entry carries a name, an e-mail address or any personal field, and each is appended before the answer is returned

  Scenario: AC8 The answer names the matrix version and a new version changes it with no deployment (new, D-RCV-60)
    Given matrix version "PM-2026.11" gives RW-REFADM the single letter "R" in Rules and parameters
    Given matrix version "PM-2026.12" is approved and in force from 1 January 2027 and gives RW-REFADM "CR" in Rules and parameters
    Given test user "U-53" holds RW-REFADM
    When "U-53" is checked for action "LOAD" on 31 December 2026
    Then the response is 403 with message MSG-P4-002 and matrixVersion "PM-2026.11"
    When the same check is made on 1 January 2027
    Then the response is 200 with authorised true and matrixVersion "PM-2026.12"
    Then no build, no configuration file and no restart is involved, and the matrix version that decided is the version named in the answer and in the entry

  Scenario: AC9 An answer that cannot be recorded is not given (new, D-RCV-60)
    Given the decision-record store is unavailable
    When a load is checked through POST /api/recovery/access/v1/authorise
    Then the call returns 503 with message MSG-P7-003 and no authorised answer
    Then rwb-decision does not accept the workbook and no version row is created
    Then the same holds for an approval, a rollback, a dry run and an evaluation

  Scenario: AC10 Error answers 401 and 404 are given for the provided operations and never an authorised answer (new, D-RCV-60)
    Given the caller holds no valid credential for POST /api/recovery/access/v1/authorise
    When the authorise operation is called without a valid credential
    Then the response is 401 with no authorised answer
    When the authorise operation is called on a path that the provided operations do not contain
    Then the response is 404 with no authorised answer
    Then no access-log entry is written for either call

  Scenario: AC11 A redelivered event is applied once (new, D-RCV-60)
    Given an event is consumed once by this service, with the event name Not specified in the source documents (NEWAC-RWB-P4-E2042-APP-AC12)
    Given the same event is delivered again
    When the duplicate delivery is consumed
    Then the duplicate changes no state and writes no second access-log entry
    Then the answer already given for the first delivery stands unchanged

  Scenario: AC12 No business value sits in code, and no statement of this service reads the rule-package family (new, D-RCV-60)
    Given a new role, a new capability area value and a new matrix version are each added as a row in Rules and parameters
    When the authorise operation is called for each of them
    Then the answer changes with the rows, and no code, configuration file or build is changed
    Then no statement of this service reads or writes `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case`
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a caller holding the C letter in Rules and parameters may load a version, and the permission row of the caller's roles with the matrix version in force is the only authority | REQ-CWC-013; TSD P4 v3 T6.1; FSD P4 v3 A2.4 |
| BR2 | The author of a version never approves it, even when the author holds the A letter; the approval is always a second person | D-RCV-36 T4; TSD P4 v3 T6.3; MSG-P7-002; REQ-CWC-014 |
| BR3 | Only a caller holding the A letter in Rules and parameters may approve; RW-RISK is the role that holds it and RW-COE holds no A | TSD P4 v3 T6.1; FSD P4 v3 AC-EXC-P4-004-03 |
| BR4 | A rollback needs U and a dry run needs R; a caller without the letter is refused and no version is rolled back and no count is read | TSD P4 v3 API-P4-017, API-P4-018 and API-P4-019; FSD P4 v3 A2.4 |
| BR5 | A running service identity reads a model only with R in Rules and parameters, and evaluates a package only in a capability area in which it holds R | Arch v5 slide 41 (service identities); TSD P4 v3 T6.1 (SY-RULES R) and T6.2; NFR-051; DP-04 |
| BR6 | Every load, approval, rollback, dry run and evaluation appends one access-log entry before the answer leaves the service, with no personal data, and an answer that cannot be recorded is not returned | Principle 5; R-UNI-39; FSD P4 v3 A2.7 and A2.8 |
| BR7 | No business value in code: roles, letters, areas, matrix versions, packages and version labels are rows and reference values, and the only fixed vocabulary is the five actions of the authorise contract | BR-P4-004; FSD P4 v3 A2.4; Template and Rules §R7.2 s17 |
| BR8 | The registry rows, the workbook, the checks, the scenario run, the four-eyes record, the promotion and the rollback belong to `rwb-decision`; this service answers the authority and holds no package | ASM-0069; Arch v5 slides 27 and 41; RWB-P3-E2042-CON BR5 |
| BR9 | The answer names the matrix version it used, so an approval can be explained after a later matrix is in force | REQ-CWC-013; FSD P4 v3 A2.4 and AC-P4-004-01 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1, BR3, BR4 and BR5 are one read: the union of the `permission` rows of the caller's roles, in the requested capability area, with the matrix version in force on the business date. There is no second copy of a letter and no role list in code, so a new role or a changed letter is a new `permission` version and a wave of cache drops.
- BR2 cannot be delegated away: `SeparationOfDutiesCheck` runs before the letter check on an approval, so a person who loaded a version and also holds A is still refused, and the refusal carries `AUTHOR_IS_APPROVER` rather than a right.
- BR5 is the two-area test of AC6, and it is the reason the entitlement is decided here rather than in the evaluating service: a service that cannot act in an area must not evaluate a package that decides in it.
- BR6 is the record appender of DP-03 inside the transaction that produces the answer. There is no separate access-log table in `rwb_access`, so the access log and the decision log are queried together (legacy FEAT-ACA-08).
- BR7 is checked by test: a new role, a new area value or a new matrix version is a row, and the build changes nothing.
- BR8 is the boundary: the `rule_package` family of DF-REF-274 to DF-REF-299 is read by `rwb-decision` and by no statement of this service.

### 9. State transitions

This service holds no package, version, case or task state. The states it answers are the outcomes of an authority decision, and the lifecycle of a version belongs to `rwb-decision`.

| From | Event | Condition | To |
|---|---|---|---|
| No decision | An authorise call for LOAD, APPROVE, ROLLBACK, DRY_RUN or EVALUATE | The caller holds the letter the action needs, and on an approval is not the author | Answer `ALLOWED`, one "AC-CHG" or "AC-READ" entry |
| No decision | An authorise call | The caller holds no letter for the action | Answer `REFUSED` with `NO_LETTER`, 403 MSG-P4-002, one "AC-DENY" entry |
| No decision | An authorise call for APPROVE | The caller is the author of the version | Answer `REFUSED` with `AUTHOR_IS_APPROVER`, 403 MSG-P7-002, one "AC-DENY" entry |
| No decision | An authorise call for EVALUATE | The identity holds R in Rules and parameters but no letter in the package's area | Answer `REFUSED` with `NO_PACKAGE_AREA`, 403 MSG-P4-002, one "AC-DENY" entry |
| No decision | An authorise call | The decision record cannot be written | No answer, 503 MSG-P7-003 |
| A cached answer | A new matrix version becomes in force | The answer was cached under the earlier version | The cache entry is dropped and the next call reads the new version |

| Command | Condition | Outcome |
|---|---|---|
| Load a version | C in Rules and parameters | `ALLOWED`; `rwb-decision` stores the version LOADED or REFUSED under its own checks |
| Approve a version | A in Rules and parameters and not the author | `ALLOWED`; `rwb-decision` records the approval and the version becomes APPROVED |
| Roll back a version | U in Rules and parameters | `ALLOWED`; `rwb-decision` moves the pointer to the earlier version with the caller's reason |
| Dry run a version | R in Rules and parameters | `ALLOWED`; `rwb-decision` answers the counts |
| Evaluate a package | R in Rules and parameters and R in the package's area | `ALLOWED`; the owning service reads the model and evaluates it under DP-04 |

The version moves LOADED to APPROVED to IN_FORCE and then to SUPERSEDED or ROLLED_BACK in `rwb-decision`, and a load that fails a check is REFUSED there. This story holds no copy of that state and changes none of it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Load a version, list it, dry-run it and roll a version back under C and U in Rules and parameters (TSD P4 v3 T6.1). Holds no A, so it never approves |
| RW-RISK, risk and model risk officer | Approve a version under A, and only a version it did not load. Holds RA in Rules and parameters |
| RW-AUDIT, internal audit | Read the package list, the versions, the dry run counts and the change report under R; this story answers R and nothing more |
| RW-REFADM, reference data administrator | Prepares the change checklist and the load file; it holds no C, no U and no A, so it uploads nothing, approves nothing and rolls nothing back |
| RW-PLATADM and RW-SECADM | Read under R; neither loads, approves nor rolls back |
| SY-RULES and the service identities of the nineteen services | Evaluate a package under R in Rules and parameters and R in the package's capability area. The exact scope of each identity inside `rwb-access` is Not specified in the source documents (GAP-0967; ASM-1701) |
| The `rwb-decision` service identity | Calls `POST /api/recovery/access/v1/authorise` for every load, approval, rollback and dry run, and reads the answer. Its own scope is Not specified in the source documents (GAP-0967; ASM-1701) |
| `rwb-access` itself | Reads `role` and `permission` in its own schema; writes the access-log entry and nothing else |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set, MSG-P4-002 for an absent or insufficient letter and MSG-P7-002 with `reason` `AUTHOR_IS_APPROVER` for the author of a version. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | `role` | id | Read |
| DF-REF-035 | `role` | role_code | Read |
| DF-REF-036 | `role` | role_name | Read |
| DF-REF-037 | `role` | role_class | Read |
| DF-REF-038 | `role` | default_scope | Read |
| DF-REF-039 | `role` | entra_group | Read |
| DF-REF-040 | `permission` | id | Read |
| DF-REF-041 | `permission` | role_id | Read |
| DF-REF-042 | `permission` | capability_area | Read |
| DF-REF-043 | `permission` | letters | Read |
| DF-REF-044 | `permission` | matrix_version | Read |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | LOV-CAPABILITY, LOV-ROLE and LOV-VERSION-STATUS with the version in force | Read through the reference-data contract |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the access-log entry of a load, an approval, a rollback, a dry run or an evaluation | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and its `DecisionRecorded` row | Write |
| (inbox) | `processed_event` | the inbox row of `rwb.access.AccessPolicyChanged.v1`, keyed by the matrix version | Write |
| DF-REF-274 to DF-REF-299 | `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` of `rwb_decision` | package code, version label, status, author, approver, checksum, test result and dry run counts | Not read and not written: they are `rwb-decision`'s under ASM-0069, and the facts this service needs arrive in the request (GAP-0968; ASM-1702) |

No row of `role`, `permission` or any reference table is written in this story: they are loaded and approved by the legacy RWB-E1-022 and RWB-E1-037 slices of this service. No row of `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case` is read or written, and no foreign key crosses a schema (DP-01). The access-log field IDs are DF-DEC-001 to DF-DEC-018 of the Logical Data Model and Data Dictionary v9; the record is the append-only chain of DP-03 and there is no separate access-log table.

The decision code of a rule-package change is Not specified in the source documents (GAP-0966; ASM-1700): FSD P4 v3 A2.7 and A2.8 name `AC-READ`, `AC-EXPT` and `AC-DENY` only, so this story uses `AC-CHG` for a load, an approval and a rollback, `AC-READ` for a dry run and an evaluation, and `AC-DENY` for a refusal, and the value is confirmed with the access-log owner before the story is done.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | Body: `action` (LOAD, APPROVE, ROLLBACK, DRY_RUN, EVALUATE), `packageCode`, `versionLabel`, `authorRef` (required on APPROVE), `capabilityArea`, `right`, `caseRef` (optional, for an evaluation) | `authorised`, `reason` (ALLOWED, NO_LETTER, AUTHOR_IS_APPROVER, NO_PACKAGE_AREA), `matrixVersion`, `area`, `right`, `packageArea`, `entryRef` | 401; 403 no letter (MSG-P4-002); 403 author is approver (MSG-P7-002); 422 missing field, unknown action or mis-matched right (MSG-GEN-001); 503 record not written (MSG-P7-003) | The letter of the caller's roles in the area of the request, read from `permission`; called by `rwb-decision` and by the service identities through the guard library | Not keyed: a repeat is answered and writes a second entry, because a decision is an event and not a state change (X10) |

The operation is the one Architecture v5 slide 14 names first for `rwb-access` (`POST /authorise` with role, scope and DoA) under the base `/api/recovery/access/v1` of DP-13, and it is the operation of RWB-P4-E1037-CON. This story adds the rule-package action to it and adds no path. The action vocabulary, the request fields and the answer fields of the rule-package part are Not specified in the source documents (GAP-0966; ASM-1700): they are fixed here so that `rwb-decision` and the test stories can build on Day 1, and the contract review confirms or renames them before the operation is frozen.

#### 12.2 REST operations consumed

None. This story calls no REST operation. The registry facts it needs arrive in the request of `rwb-decision`, and the reference lists are read in process through the client library of DP-07.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained access-log entry of one authority decision, with the action, the package code, the version label, the area, the right and the matrix version, and no personal data |

CloudEvents 1.0 envelope with the retry path and the `.dlt` topic of the library; the payload carries no name, no e-mail address and no personal field. No `rwb.access.*` event type is added by this story: an authority answer changes no access policy, and the matrix change that does is published as `rwb.access.AccessPolicyChanged.v1` by the permission-matrix slice of this service (legacy RWB-E1-037). This story subscribes to it for the cache drop of step 13 of section 4 and publishes nothing on it.

#### 12.4 Events consumed

| Event | Topic | Owner | Use in this story |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | Drops the cached authorise answers, so the next call reads the new matrix version. Consumed through the inbox of DP-09 and keyed by the matrix version |

The event is this service's own and is produced by the permission-matrix slice; no other subscription is added. A `RulePackageInForce` message is `rwb-case`'s and the other evaluating services' business and is not consumed here.

#### 12.5 Workflows and activities

None. This story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. JOB-20, the 00:01 promotion, is a Temporal Schedule in `rwb-decision`, and `RuleModelSwap` and `EvaluateRules` are `rwb-case`'s and the owning services' under RWB-P3-E2042-CON.

#### 12.6 Schedules

None for this story. The six-monthly access review list (JOB-18) is a Schedule of `rwb-access` and belongs to the service's own access-review story (RWB-P4-AD008-APP), not to the rule-package authority.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role code and class of the caller |
| `permission` | P4 (`rwb_access`) | Read only: the letters of the caller's roles in the requested area, with the matrix version |
| `role_conflict` | P4 (`rwb_access`) | Not read: the mutual exclusion of RW-COE and RW-RISK is enforced at sign-in by the service baseline |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the record and the inbox row of `AccessPolicyChanged` (DP-09) |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written: the registry is `rwb-decision`'s under ASM-0069 (GAP-0968; ASM-1702) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger entry is `rwb-decision`'s and the local record goes on `rwb.decision-record.v1` |

`lov_value` and the reference tables are reference data of P3 under the ownership ruling and are read through DP-07; no table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision rule-package WireMock | RWB-P3-E2042-CON | Package "RESTRUCTURE" with version "RES-2026.12" LOADED, author "U-41", valid from 15 December 2026, 38 rows and "62 of 62 scenarios passed"; "PMT-2026.12" with 3 rows and "58 of 58 scenarios passed"; "BKG-2026.12" IN_FORCE with 21 rows and "54 of 54 scenarios passed"; a load that answers 201, 409 and 422; an approve that answers 200, 403 and 409; a dry run with 412 decisions over 412 open cases |
| decision-record fake | RWB-PLT-E1027-CON | The record append, the hash chain check and the forced failure of AC9 |
| authorise and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The permission answer behind the letter, including the refusal for a role without it and the DoA part that this story leaves alone |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY with the fourteen areas, LOV-ROLE and LOV-VERSION-STATUS with their versions |
| parameters fake | RWB-P3-E1042-CON | The lifetime of the cached authorise answer, read through DP-06 (GAP-0969; ASM-1703) |
| permission fixture | the service baseline | Matrix version PM-2026.11 with RW-COE "CRUD", RW-RISK "RA", RW-AUDIT "R", RW-REFADM "R" and RW-PLATADM "R", and PM-2026.12 for AC8 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1 extended (`POST /authorise`, no new path); consumed 0 | Base `/api/recovery/access/v1` |
| Kafka | Published 1 event type (`DecisionRecorded`); consumed 1 (`AccessPolicyChanged`) | `rwb.decision-record.v1` and `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | JOB-20 is `rwb-decision`'s and JOB-18 is this service's own story |
| File | None | No file input and no file output; a workbook is `rwb-decision`'s |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/rules`, Java package `th.co.scb.ace.workbench.recovery.access.rules`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process `RecoveryAccessGuard` right check, which becomes this service's own authorise contract with the rule-package action added, and the monolith `RuleEvaluator` (DP-04: the kit stays, and the package comes from the registry). DP-05 is applied by holding to no ACE read at all: the group-to-role mapping is the service baseline's `v_ace_iam_group` read at sign-in, and this story reads only its own `role` and `permission` rows. DP-10 and DP-19 are carried by the legacy key and their work sits with `rwb-decision` (JOB-20, and SCR-39 through gateway-bff); this story starts no workflow and serves no screen. DP-14 is applied to the two topics of section 12.3 and 12.4 through the naming library, and DP-15 is carried because the `role` and `permission` migrations of the service baseline are the sequence this story reads.

This secondary slice adds no new build dependency of its own (metadata "Depends on (build)" is None): the libraries, the per-service Flyway baseline, the kit, the registry contract and the gateway route are already build dependencies of the P4 service's own stories, in particular RWB-P4-E1037-CON, and this story builds against the published contracts and their fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RulePackageAuthorityController | Controller | `POST /authorise` for the five actions: validation, error mapping to RFC 9457 problem responses, `reason` and `matrixVersion` in the answer |
| RulePackageAuthorityService | Service | BR1 to BR5: the letter the action needs, the separation of duties on an approval, the two-area entitlement of a service identity |
| ActionCatalog | Service | The five actions and the letter each needs, as the contract of 12.1 with a contract test; an unknown action is refused, and no role or area value lives here |
| PermissionReader | Service | The union of the caller's `permission` letters in the requested area, with the matrix version in force on the business date |
| SeparationOfDutiesCheck | Service | BR2: `authorRef` against the caller reference on an approval, whatever letters the caller holds |
| ServiceIdentityEntitlement | Service | BR5: R in Rules and parameters plus R in the package's capability area, for a running service identity |
| AccessLogWriter | Service | The decision-record entry of every answer in the transaction that produces it, with the outbox row (DP-03, DP-09) |
| AuthorityCache | Service | The answer keyed by identity, area, right, action, package code and matrix version, dropped on `AccessPolicyChanged` |

**Database and migrations**

- This story creates no table and owns no Flyway version of its own. `role` and `permission` are created, indexed and loaded by the service baseline in the per-service sequence of DP-15, and this story reads them through the repository.
- The read predicates are `role_id`, `capability_area` and `matrix_version`. If the SIT query plan needs an index that the creating story does not have, the index is added to that story's migration, not to a new one here.
- No write statement exists in the repository: the class exposes no save, update or delete, so an authority answer can never change a role, a letter or a matrix version.
- The outbox row and the record row commit in one transaction with nothing else to write; a failure rolls them back and the answer is not returned (MSG-P7-003).

**Configuration and reference data**

- LOV-CAPABILITY with its fourteen values, including `RULES_AND_PARAMETERS` and `TREATMENT_AND_OFFER`, LOV-ROLE and LOV-VERSION-STATUS are read through the reference-data contract of DP-07 with the version in force (RWB-P3-E1043-CON); no area code, role code or letter is a constant in code beyond the five action names of 12.1.
- The capability area each package serves is `rwb-decision`'s data and arrives as `packageArea` in the request; RESTRUCTURE serves `TREATMENT_AND_OFFER`, and the area of PAYMENT_MATCH and BOOKING_MATCH is Not specified in the source documents (GAP-0967; ASM-1701).
- The lifetime of a cached authorise answer is a parameter row of `rwb-case` read through DP-06, and its value is Not specified in the source documents (GAP-0969; ASM-1703); the tests fix the version-keyed drop rather than the clock, so the behaviour holds whatever value is agreed.
- The matrix versions, their rows and their letters are rows of `permission` in `rwb_access`; PM-2026.11 is the version in force in SIT and PM-2026.12 is the version of AC8.

**Build steps**

1. `PermissionReader` over `role` and `permission` with the matrix version in force on a fixed clock; test the union of two roles and the version switch of AC8.
2. `ActionCatalog` with the five actions and their letters, and the contract test that a request whose right does not match its action is refused with MSG-GEN-001 (X2).
3. `RulePackageAuthorityService` for LOAD, ROLLBACK and DRY_RUN; tests for AC1, AC4 and AC5, including the refusal for RW-AUDIT on a rollback.
4. `SeparationOfDutiesCheck` ahead of the letter check on APPROVE; tests for AC2 with an author who also holds A, and for AC3 with RW-COE refused for want of A.
5. `ServiceIdentityEntitlement` for EVALUATE with the two-area test of AC6, including the refusal with `NO_PACKAGE_AREA`.
6. `AccessLogWriter` with the record append and the outbox row in one transaction; tests for AC7 and for the 503 of AC9.
7. `AuthorityCache` keyed by the matrix version, with the drop on `AccessPolicyChanged`; test that a cached allowed answer cannot survive a new matrix version.
8. The contract-fake run of the whole story against the `rwb-decision` and `rwb-access` fakes of RWB-P3-E2042-CON, so the story builds before the registry exists in the environment.
9. The denial test through the guard library for a role without the letter, and the service-identity test of section 10.

**Feature switch.** The authority answer is a read path and carries no switch of its own. The service-level feature flag of RWB-P4-E1037-CON governs the service baseline, and a new matrix version needs no flag and no restart; this story removes nothing when a matrix version is rolled back, because the answer always reads the version in force.

**Done when.** The tests in section 16 pass; a load by RW-COE is allowed with "PM-2026.11" named; an approval by the author is refused with MSG-P7-002 even when the author holds A; an approval by RW-RISK is allowed and an approval by RW-COE is refused with MSG-P4-002; a rollback by RW-COE is allowed and by RW-AUDIT refused; a dry run is allowed under R and leaves one "AC-READ" entry; a service identity without the package's area is refused; a new matrix version changes the answer with no deployment; and an answer that cannot be recorded is not given.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-GEN-001 | A required field is empty, `authorRef` is missing on an approval, or the action is outside the five | Enter {field}. | This story, on the authorise call |
| MSG-P4-002 | The caller holds no letter for the action, or holds no letter in the package's area | You cannot {action} here. Your role does not include it. | This story, on the authorise call; `rwb-decision` returns the same text on its own operation |
| MSG-P7-002 | The caller is the author of the version it asks to approve | You prepared this decision, so you cannot approve it. | This story, with `reason` `AUTHOR_IS_APPROVER` |
| MSG-P7-003 | The access-log entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer |
| MSG-P3-022 | The change checklist is incomplete, so the version cannot be approved | Text not specified in the source documents (GAP-0966; ASM-1700); the message reports the missing checklist item of TSD P4 v3 T6.3 | `rwb-decision`, before it asks this service |
| MSG-P3-027 | A load check failed: compile, schema, overlap, unreachable row, default row or scenario | The {table} load was refused: {check}. The version in force is unchanged. | `rwb-decision`, after this service allows the load |
| MSG-GEN-004 | The version label is already loaded | Someone else changed this record. Reload it to see their change. | `rwb-decision`, after this service allows the load |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. A refusal also carries `reason`, `area` and `right`, so the caller can name the letter without a second lookup; it carries no role list and no matrix row.

### 15. Screens and states

No screen is built in this story. The answer is consumed by `rwb-decision` and by the guard library of the services that evaluate a package; the screens that show a version belong to other stories.

| Screen | State | Where it is |
|---|---|---|
| SCR-39 Rules and parameters | Version list, loaded, approved, in force, refused, rolled back; empty, loading, error, no access: Not specified in the source documents (CG-ALL-5423) | `rwb-decision` and the P4 administration slice (RWB-P4-E8007-APP, legacy RWB-AD-011); shows the versions this answer allowed |
| The route-set workbook load | Uploaded, accepted, refused, handed to the registry | `rwb-access` (RWB-P4-AD011-APP, EP08); calls the same answer |
| Access audit query | List over a period | `rwb-access` (legacy RWB-E1-039; RWB-P4-AD007-APP) |

The gateway-bff composite route of DP-19 is not used by this story: no screen calls the answer directly, and the screen calls `rwb-decision`, which calls this service in one hop with a 2 s timeout and caches the answer. The lifetime of a cached answer is a parameter row of the DP-06 contract, fixed at the wave 2 design review (GAP-0969); the cache is keyed by the matrix version.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-042-01 | AC1, AC7, BR1, BR6 | Component | RESTRUCTURE RES-2026.12, 38 rows and 62 scenarios, loaded by "U-41" holding RW-COE under "PM-2026.11", with one record entry |
| TC-E2-042-02 | AC2, BR2 | Component | RES-2026.12 authored by "U-41", who also holds a role carrying A; the approval is refused with MSG-P7-002 and the version stays LOADED |
| TC-E2-042-03 | AC3, AC8, BR3, BR9 | Contract | PMT-2026.12, 3 rows and 58 scenarios; "U-54" holding RW-COE refused for want of A and "U-51" holding RW-RISK allowed; the answer names "PM-2026.11", and "PM-2026.12" changes the answer on 1 January 2027 |
| TC-E2-042-04 | AC4, BR4 | Component | BKG-2026.12, 21 rows and 54 scenarios, in force; RW-AUDIT refused for want of U and "U-41" holding RW-COE allowed |
| TC-E2-042-05 | AC5, AC6, BR4, BR5 | Contract | RES-2026.12 with 412 decisions over 412 open cases for the dry run; the rwb-treatment identity allowed for TREATMENT_AND_OFFER and the rwb-debtsale identity refused with NO_PACKAGE_AREA |
| TC-E2-042-06 | AC6, BR6 | NFR | The decision-record write forced to fail during a load, an approval, a rollback, a dry run and an evaluation; four entries on the happy path |
| TC-E2-042-07 | AC12, BR8; §12.7 tables | Contract | Read and write boundary over the §12.7 tables: no row of `rule_package`, `rule_package_version`, `rule_row` or `rule_test_case` is read or written; `role` and `permission` are read only; `role_conflict` is not read |
| TC-E2-042-08 | AC12, BR7 | Component | A new role, a new capability area value and a new matrix version added as rows; the authorise answer changes with the rows and no code is changed |
| TC-E2-042-09 | AC10 | Contract | POST /api/recovery/access/v1/authorise called with no valid credential (401) and on a path outside the provided operations (404); no authorised answer and no access-log entry in either case |
| TC-E2-042-10 | AC11 | Component | An event consumed once is delivered again; the duplicate changes no state, writes no second access-log entry and the first answer stands |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, and the legacy level Schema maps to Component. The six legacy test cases are kept because the legacy key carries them, and each is re-aimed at the authority deliverable of this slice: the compile, the checks, the 50-scenario gate, the priority order, the catalog read and the absent `payment_match_rule` table are tested by RWB-P7-E2042-APP and RWB-P3-E2042-CON, and the tests whose rule lives in `rwb-decision` use this story's answer and the contract fake for the rest. The ITG copy of the whole set is the integration harness of the legacy key and is not written here, so no `-ITG` id appears in this table. AC1 to AC3 of this story are proven against the rwb-decision contract mock here and against the real service in RWB-ITG-E2042-ITG; the registry work is RWB-P7-E2042-APP's.

### 17. Guardrails

- No business value in code: roles, letters, areas, matrix versions, packages, version labels and the dry run counts are rows and reference values (BR7). A test proves that a new role, a new area value and a new matrix version need no build.
- No personal data anywhere: the answer, the entry and the event carry user references, package codes, version labels, areas, rights and matrix versions only; no name, no e-mail address and no personal field, and no test data or prompt holds one.
- No read of another service's tables (DP-01): `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` are `rwb-decision`'s, and no foreign key crosses a schema. The registry facts arrive in the request and never by a schema read.
- ACE data only through the owner's contract or its own `v_ace_*` views: this story reads no ACE data at all; the group-to-role mapping is the service baseline's sign-in read.
- One writer per thing: `rwb-decision` writes a version and its state, the service baseline writes `role` and `permission`, and this story writes the access-log entry and nothing else. Its repository has no write method, so an answer cannot change a letter.
- No answer without its record: the entry commits with the answer, and the answer is withheld with MSG-P7-003 when it cannot be written (BR6).
- The separation of duties is checked before the letter: a person who loaded a version cannot approve it by holding A, by a second role or by a delegation.
- A refused caller learns the reason and nothing else: the refusal carries `reason`, `area` and `right`, and no role list, no matrix row and no package content, so it cannot be used to map the matrix.
- The answer is a pure function of the rows, the lists and the request, so a retry answers the same and writes a second entry, as a decision must.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version and rollback by one call | Epic 1, 4 (legacy pointer 3.3 is stale against BRD Epic 1 v4); Epic 2, 3.2 and 3.8 (legacy pointer, stale against BRD Epic 2 v2); Program, 5.3 | FEAT-CWC-14, FEAT-ADM-02 | 14 Set strategy, policy and decision rules | BR1, BR4, BR8, BR9; R-UNI-38 | TC-E2-042-01, TC-E2-042-04, TC-E2-042-06, TC-E2-042-07 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and scenario checks before a rule takes effect, and a second pair of eyes on the version | Epic 1, 4 (legacy pointer 3.3 is stale against BRD Epic 1 v4); Epic 2, 3.2 and 3.8 (legacy pointer, stale against BRD Epic 2 v2); Program, 5.3 | FEAT-CWC-14, FEAT-ADM-02 | 14 Set strategy, policy and decision rules | BR2, BR3, BR5, BR6, BR7; R-UNI-39 | TC-E2-042-02, TC-E2-042-03, TC-E2-042-05, TC-E2-042-06, TC-E2-042-08 |

| Legacy reference | Where it is kept |
|---|---|
| Package codes RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH with owner role RW-COE | Sections 3, 7, 12.8, 13 |
| Version labels RES-2026.12, PMT-2026.12 and BKG-2026.12 valid from 15 December 2026; 38, 3 and 21 rows; 62, 58 and 54 scenarios; `rules.testcases.min` 50 | Sections 3, 7, 12.8, 16 |
| RW-COE loads and rolls back, RW-RISK approves, the author cannot approve | Sections 4, 7, 8, 10 |
| MSG-P4-002, MSG-P7-002, MSG-P7-003, MSG-P3-022, MSG-P3-027, MSG-GEN-001, MSG-GEN-004 | Section 14, exception paths |
| Rule IDs R-UNI-38 and R-UNI-39; D-RCV-36 T4 and T5 | Sections 2, 8, 17 |
| Legacy key RWB-E2-042, story RWB-P4-E2042-APP, contract RWB-P3-E2042-CON | Metadata, sections 3, 12 |
| Field IDs DF-REF-034 to DF-REF-044 and DF-DEC-001 to DF-DEC-018 | Section 11 |

### 19. Out of scope

- The registry slices RWB-P7-E2042-APP and the `rwb-decision` contract family: `rule_package` and `rule_package_version`, the three package seed rows, the workbook compile and the KieBase, the checksum, the compile, schema, overlap, unreachable row, default row, scenario and dry run checks, the 50-scenario gate, the four-eyes approval record, JOB-20 and the one-call rollback.
- The package content and the evaluation: the three workbooks, the Rows and Tests tabs, the route-set rows and the `RuleScenarioBuildGate` run, which are the legacy RWB-E2-042 application slice and the P7 story.
- The embedded Drools kit wiring and the model cache of DP-04: the kit, the `EvaluateRules` activity, the KieBase cache of at most 20 versions, the checksum check and the atomic swap, which are `RWB-PLT-E1072-CON`, `RWB-P7-E1073-CON` and RWB-P3-E2042-CON.
- The workbook ingest `POST /api/recovery/access/v1/admin/rule-version-loads` and the SCR-39 administration surface of the legacy RWB-AD-011 (EP08, RWB-P4-AD011-APP); this story answers the authority that either surface calls.
- The permission-matrix load, approval and rollback of the legacy RWB-E1-037, which create the matrix this story reads, and the sign-in and role-conflict rules of RWB-E1-022.
- The access audit query and the decision log search screen (legacy RWB-E1-039; RWB-P4-AD007-APP), which read the entries this story writes.
- `payment_match_rule` and DF-REF-261 to DF-REF-273: retired by D-RCV-36 T10, with no table, no column and no field here.
- The integration harness of the legacy key and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of the legacy key).
