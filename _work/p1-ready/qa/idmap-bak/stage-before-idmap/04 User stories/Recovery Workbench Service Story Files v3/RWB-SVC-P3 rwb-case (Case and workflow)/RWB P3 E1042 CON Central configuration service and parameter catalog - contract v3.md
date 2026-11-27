# RWB-P3-E1042-CON Central configuration service and parameter catalog - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1042-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-042 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E1042-CON-16) |
| Contract version | v1, from the /v1 path of the REST base in section 1 |
| Readiness decisions | RD-P1-028, RD-P1-042, RD-P1-063 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| Open decisions | DL10, DL11, DL26 remain open, each with its recorded assumptions: DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL11 (ASM-0553, ASM-0703, ASM-1051, ASM-1104); DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-025) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- D-RCV-60 finishing pass: RD-P1-063; Test Cases v9 mappings.
- D-RCV-60 finishing pass, reconciliation: the read by key is open to service workload identities only and answers 404 for a secret key; the open-right wording is removed (RD-P1-063).

- RD-P1-028: `GET /parameters/{key}` declared as the fifth operation; AC1 and AC6 rewritten (finding #1).
- RD-P1-028 and RD-P1-042: the fake serves the five keys rwb-source-data reads; AC9 and AC10 added (finding #2).

**Change log.** D-RCV-60, 22 November 2026: delta slice split from RWB-E1-042 for rwb-case — the parameters and configuration contract of record that the preserved story RWB-P3-E1042-APP implements. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 57 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **consumer of the rwb-case parameters contract**, I want **the contract of record for the parameter catalog in `rwb_case` — the dated read with the value in force per environment, the catalog entry shape, the load, approve and rollback operations with their rights and refusals, the version event, the two tables, the startup requirement, the Flyway step and the fakes**, so that **the app story, the case and timer engines, the reference-data read and the other services build and test a dated, approved parameter read on Day 1 without any of them reading `parameter_catalog` or `parameter_value`**.

This is the contract slice of the delta of legacy RWB-E1-042, and it is the counterpart of the preserved story RWB-P3-E1042-APP, which keeps the legacy acceptance criteria AC1 to AC11 and the runtime behind them. The contract publishes, under the rwb-case base `/api/recovery/case/v1` (DP-13):

- The five operations of the parameters surface with their request, answer, errors and rights: the catalog read, the load of table PARAMETER, the approval, the rollback (Context pack ownership rows; legacy section 12) and the read of one key for a business date that services call (RD-P1-028).
- The dated rule: the approved version with the latest valid from on or before the business date, per environment and product group, answered with the version number and never with a code constant (legacy AC8, AC10 and AC11).
- The catalog entry shape of DF-REF-132 to DF-REF-158, with a secret listed and never served (legacy AC9, BR6).
- The two tables `parameter_catalog` and `parameter_value` as P3 tables of `rwb_case`, and the event `rwb.case.ParameterVersionApproved.v1` that refreshes every cache.
- The startup requirement and the key artefact a caller compiles, and the fakes the app story, the engines and the platform client build against.

The contract serves no reference table value and no rule package. The reference table codes stay with RWB-P3-E1043-CON (DP-07), rule packages with rwb-decision (DP-04, outside this key's pattern set), and the product-specific values with RWB-P3-E1045-APP. The story has no build dependency, is Day 1 by rule and sits in the contract group CG-W1 (Template and Rules §R5.7).

### 2. Business rationale

The legacy module published `ParameterService` inside one application: the catalog rows, the value versions and every caller were in one database and one process, so the shape of a parameter read was never a contract. After the split the two tables sit in `rwb_case` and nineteen services read them across a service boundary, which means the dated read, the entry shape, the refusal set, the right and the refresh have to be agreed before any engine writes its start-up check. Without that agreement each service invents its own projection or — worse — reads `parameter_value` directly, which the schema-per-service rule forbids (DP-01).

**What this contract fixes, and what it leaves.** It fixes the five operations and their answers, the dated rule, the entry shape, the refusal set with its message identifiers, the two tables and their owner, the one event and its topic, and the fakes. It leaves the business values to the rows: `case.entry.dpd` at 90 or 91, `refdata.cache.ttl-seconds` at 30 or 300 and `caselist.export.maxrows` at 10000 are values of a load and appear in this document only as the legacy examples.

**The two unresolved edges, stated once.** The legacy story publishes `ParameterVersionApproved` as a new internal event, and the rwb-case event catalogue carried by the Ownership Map (EV-01 to EV-05, EV-19, EV-29) has no parameter event, so the event keeps the legacy name in the `rwb.case.<Event>.v1` form and its place in the catalogue is a gap (GAP-2212; ASM-3639). The legacy catalog was read in process through a published interface, and no source gives the operation or the right a service principal uses after the split, so the read keeps the only published read of the surface — the key-prefix query of `GET /admin/parameters` — and the assumption is recorded (GAP-2213; ASM-3640).

**The fakes are the Day-1 unblocker.** The first approved value version in SIT arrives later in wave 1. With this document and its fakes, the app story, the engines, the reference-data read and the platform client build and test the dated read on Day 1, and a drift test fails a build when an operation, a field or a refusal changes (Template and Rules §R5.4 class C). Every criterion below is new, tagged `(new, D-RCV-60)`, and tests only the contract deliverable.

### 3. Preconditions

- The naming rules of Template and Rules §R4 are used unchanged: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` (namespace `rwb-recovery`), Java package Not specified in the source documents (CG-ALL-3739).
- The Ownership Map stands: `parameter_catalog` and `parameter_value` are two of the fifteen P3 tables of `rwb_case`, and `GET /admin/parameters`, `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve` and `POST /admin/reference-loads/{loadId}/rollback` are P3 operations.
- The field identifiers DF-REF-132 to DF-REF-146 (parameter_catalog) and DF-REF-147 to DF-REF-158 (parameter_value) are taken from the Technical Specification T3 and the Logical Data Model, character for character.
- The legacy message identifiers MSG-P3-032, MSG-GEN-002, MSG-P1-002, MSG-GEN-001, MSG-P7-002, MSG-P3-015 and MSG-P4-002 are used unchanged in the answers and the examples, with the legacy texts of section 14.
- The rights are the legacy ones: Reference data C for a load, Reference data U for a rollback, Reference data A for an approval and Rules and parameters R for the read, resolved on the authorise model of rwb-access through the guard the service template wires (GAP-2215; ASM-3642).
- The cache time to live is the legacy catalog entry `config.cache.ttl-seconds` = 60 (assumed; DL11), itself a row of the catalog and never a code constant.
- The platform client contract RWB-PLT-E1042-CON consumes the read of this document; this document is its provider and the library declares no operation of its own.
- rwb-source-data reads one parameter with `GET /api/recovery/case/v1/parameters/{key}`, the version in force on the business date, through the client library (RD-P1-028). The read is open to service workload identities only (RD-P1-063); the read path of the other consuming services remains open (GAP-2213; ASM-3640).
- The catalog rows the fake serves for rwb-source-data are `case.entry.dpd`, `recon.tolerance.pct`, `recon.treatment.days`, `recon.payment.days` and `caselist.allocation.wait.until`, as in `06 Data/Recovery Workbench Parameter Catalog v1.csv`.
- No approval is required to publish a Draft contract: the surface is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. The contract author writes the OpenAPI 3.1 document of the four operations, one tag per resource: Parameters, Parameter loads, Parameter load approval, Parameter load rollback.
2. The author writes the dated read: the key-prefix, kind, owner and environment query, the entry shape of DF-REF-132 to DF-REF-158, the version-in-force rule, and the answer without `valueInForce` when `secret` is true.
3. The author writes the three write operations with the legacy request, answer and error rows, `Idempotency-Key` on every POST, and the right of each operation.
4. The author writes the refusal set: range, type or unknown key, empty file, author approves, rollback with no earlier version, missing required value at start-up, and a role without the right — each with its legacy message identifier.
5. The author writes the table section and the event: the two P3 tables of `rwb_case` with their keys, and `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1` through the outbox.
6. The author writes the difference from the legacy contract: the read another service makes, the key artefact a caller compiles, the startup check of every service, the Flyway step, and the absence of a consumed operation.
7. The lint and schema steps run: OpenAPI 3.1 validation, the base-path rule, the operation-id rule, the error-envelope rule, `Idempotency-Key` on every POST, the table-owner rule, the event-name rule and the secret rule.
8. The fakes are generated from the document; the document and the fakes are published, the app story and the platform client pin the version, and a drift test in this story refuses any difference between a fake and section 12.

### 5. Exception paths

| ID | Covered by | Trigger | What happens | Message |
|---|---|---|---|---|
| X1 | AC1 | An operation is published without a 4xx error envelope, or a POST without `Idempotency-Key` | The lint step fails the build and the document is not published | Lint finding, no message id |
| X2 | AC1 | A path is published outside `/api/recovery/case/v1`, or another service's operation is declared as provided | The lint step fails the build | Lint finding, no message id |
| X3 | AC2 | An entry with `secret = true` is published with a value, or the secret store value appears in an example | The secret rule fails the build, and no answer ever carries the value | Lint finding, no message id |
| X4 | AC4 | The event is published outside the `rwb.case.<Event>.v1` form, or on a topic other than `rwb.case.events.v1` | The event-name rule fails the build | Lint finding, no message id |
| X5 | AC7 | A field-level detail of an entry or of the event payload is missing from the source material | The element carries the placeholder, the gap and the assumption rows, and the fake is written to the assumed shape | Not specified in the source documents (GAP-2212; ASM-3639) |
| X6 | AC7 | A fake drifts from the document | The drift test fails the build | Lint finding, no message id |
| X7 | AC1 | The target form of a name the monolith fixed — the Java package, the feature-flag name, the migration file numbers, the `used by` value | The document keeps the legacy name and carries the placeholder with its gap and assumption rows | Not specified in the source documents (GAP-2214; ASM-3641) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and fakes; builds against the platform naming and error baselines only and starts on Day 1 |
| Negotiable | The element order inside an answer, the example values and the fake fixture set are open until the version is frozen; the operations, the dated rule, the refusal set and the rights are fixed |
| Valuable | The app story, the engines, the reference-data read and the platform client build and test the dated read before an approved version exists |
| Estimable | Five provided operations, two tables, one event, seven messages and four fake assets |
| Small | One sprint for the documents, the fakes and the drift test |
| Testable | Each criterion below is one schema, lint or fake assertion in section 16, never a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: rwb-case parameters and configuration contract of record

  Background:
    Given the rwb-case base path is /api/recovery/case/v1, the schema is rwb_case and the contract version is v1
    Given parameter_catalog and parameter_value are P3 tables of rwb_case and PARAMETER is a table code of the reference-load operation

  Scenario: AC1 The five operations and the base path are fixed (new, D-RCV-60)
    Given the operations of section 12.1
    When the document is validated
    Then GET /admin/parameters, POST /admin/reference-loads, POST /admin/reference-loads/{loadId}/approve, POST /admin/reference-loads/{loadId}/rollback and GET /parameters/{key} are the five provided operations and no sixth operation is declared
    Then table PARAMETER is loaded through POST /admin/reference-loads and the other table codes stay with RWB-P3-E1043
    Then every operation carries its request, its answer, its errors 401, 403, 404, 409, 422 and 503, and its right
    Then the legacy monolith base appears only in the as-built section of RWB-P3-E1042-APP and nowhere in this document

  Scenario: AC2 The catalog entry and the value in force are fixed (new, D-RCV-60)
    Given an entry of the catalog and its value versions per environment and product group
    When the document is validated
    Then an entry answers key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, valueInForce, versionNo and validFrom, matching DF-REF-132 to DF-REF-158
    Then a value is in force from its validFrom and a business date before it answers the earlier approved version, with no restart of any instance
    Then the environment and the product group select the row, so 30 in SIT and 300 in PROD are two answers of one key
    Then an entry with secret = true answers its owner, environments and usedBy and no valueInForce in GET /admin/parameters
    And GET /parameters/{key} answers 404 with MSG-P4-003 for that entry
    Then a key with no approved version in force answers its default from the catalog and names it as the default, never as an approved value

  Scenario: AC3 The refusal set and its messages are fixed (new, D-RCV-60)
    Given the seven message identifiers of section 12 and section 14
    When the document is validated
    Then a value outside its range answers 422 with MSG-GEN-002 naming the minimum and the maximum
    Then a value of the wrong type or an unknown key answers 422 with MSG-P1-002 naming the check
    Then an empty load file answers 422 with MSG-GEN-001
    Then an approval by the author answers 409 with MSG-P7-002 and the version stays VALIDATED
    Then a rollback with no earlier approved version answers 409 with MSG-P3-015
    Then a required parameter with no value and no default for the environment answers a failed health check with MSG-P3-032 naming the key and the environment, and the service takes no traffic
    Then a role without the right answers 403 with MSG-P4-002 and nothing changes
    Then a load with any failed check writes no row and the previous load stays in use

  Scenario: AC4 The event, the topic and the refresh are fixed (new, D-RCV-60)
    Given the outbox and inbox library and the naming library
    When the document is validated
    Then rwb.case.ParameterVersionApproved.v1 on rwb.case.events.v1 is the only event the contract declares, written to the outbox in the same transaction as the approval as a CloudEvents envelope
    Then the payload carries paramKeys, versionNo, validFrom and environment, and no personal data and no value of a secret
    Then every instance refreshes on the event and at the latest at the cache time to live, so a missed event delays a refresh and never a value
    Then the topic and the event name follow rwb.<short>.events.v1 and rwb.<short>.<Event>.v1 and no other topic or event form appears

  Scenario: AC5 The two tables, their keys and the Flyway step are fixed (new, D-RCV-60)
    Given parameter_catalog, parameter_value and the rwb-case Flyway sequence
    When the table section is checked against the Ownership Map
    Then parameter_catalog and parameter_value are named as P3 tables of rwb_case and no other table is named as this service's
    Then the primary keys, the reference, the unique constraint on param_key, environment, product_group and version_no, and the partial index on param_key, environment and valid_from are declared
    Then the two tables arrive on the rwb-case Flyway sequence with the schema name from the placeholder, and the contract declares no baseline and no migration of another schema
    Then no other service reads the two tables, and the read is the operation of 12.1

  Scenario: AC6 The startup requirement and the key artefact are fixed (new, D-RCV-60)
    Given the catalog file, the generated keys class and the startup check
    When the document is validated
    Then the contract states that a required parameter with no value and no default for the environment stops the service with MSG-P3-032
    Then the catalog file is the single source of the keys and the generated keys class is the artefact a caller compiles from the platform client
    Then the read rwb-source-data makes is GET /parameters/{key} for a business date, and the read is open to service workload identities only (RD-P1-063)
    Then the cache time to live is the catalog entry config.cache.ttl-seconds at 60 (assumed; DL11) and never a code constant
    Then the platform client and the engines hold no copy of a catalog row and no connection to rwb_case

  Scenario: AC7 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section and the fakes of section 12.8
    When the nine sub-tables are reviewed and the contract test runs
    Then each of 12.1 to 12.9 is present, and an empty one says None with one sentence
    Then every operation sits under /api/recovery/case/v1 and every table and every operation names its owner from the Ownership Map
    Then the fakes answer the dated read, the secret entry, the range refusal, the author-approves refusal, the rollback with no earlier version and the cache time to live
    Then a drift between a fake and this document fails the contract test

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given a version whose status does not allow the requested status change
    When the status change is requested
    Then the status change is refused and the version keeps its status

  Scenario: AC9 The read of one key for a business date is fixed (new, D-RCV-60)
    Given recon.tolerance.pct version 1 is 0.00 and an approved version 2 is 0.10 valid from 2026-12-10
    When the fake is asked GET /api/recovery/case/v1/parameters/recon.tolerance.pct for business date 2026-12-09 and for 2026-12-10
    Then the first answer is 200 with value 0.00 and version 1 and the second is 200 with value 0.10 and version 2
    Then a key the catalog does not list answers 404, a call without a valid identity answers 401 and an unavailable store answers 503

  Scenario: AC10 The fake serves the keys rwb-source-data reads (new, D-RCV-60)
    Given the published parameters fake
    When each of case.entry.dpd, recon.tolerance.pct, recon.treatment.days, recon.payment.days and caselist.allocation.wait.until is read for business date 2026-11-30
    Then the values are 90, 0.00, 2, 1 and 07:15, each with version 1
    Then recon.caselist.tolerance.pct answers 404
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is copied here — AC1 to AC11 of RWB-E1-042 stay with RWB-P3-E1042-APP — and every number, identifier, message and code comes from the legacy story, the Technical Specification, the Ownership Map or Architecture v5, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract serves one service's tables: `parameter_catalog` and `parameter_value` in `rwb_case`, and no table of another service | Ownership Map; DP-01 |
| BR2 | A parameter that a business person may change is a catalog row with an owner and a default, and a value version per environment and product group, never a constant in code | Legacy section 8 BR1, BR2 (REQ-DRI-010) |
| BR3 | The value in force on a business date is the approved version with the latest valid from on or before that date, and the version number travels in every answer | Legacy AC10, AC11; R-UNI-38 |
| BR4 | Only an APPROVED version is served; VALIDATED and ROLLED_BACK are never served, and a key with no approved version answers the catalog default and names it as such | Legacy section 9; Principle 1 |
| BR5 | A load with any failed check is refused in full and the previous load stays in use, and a repeat load of the same content hash writes nothing | Legacy section 8 BR3, AC5; CTL-08 |
| BR6 | The author of a load cannot approve it, and the approve right is resolved on the authorise model of rwb-access through the guard the service template wires | Legacy section 8 BR4; DP-08 default ruling (GAP-2215; ASM-3642) |
| BR7 | A secret is listed in the catalog with `secret = true` and is held only in the ACE secret store; no answer, log or example carries its value | Legacy section 8 BR6 (DL26; REQ-ACA-005) |
| BR8 | A service does not start without every required parameter for its environment, and the check is proved against MSG-P3-032 in every service, not only in rwb-case | Legacy section 8 BR7; AC4 |
| BR9 | One event, on the owner's topic: `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1`, with no personal data and no secret value | DP-09; DP-14; legacy section 12 |
| BR10 | One REST base and one topic per service: this contract declares `/api/recovery/case/v1` as provided and quotes `rwb.case.events.v1` as its only topic | DP-13; DP-14 |
| BR11 | A breaking change raises a new contract version and deprecates the old one; an operation, a field or an event name is never edited in place | Template and Rules §R7.2; §R5.4 class C |

### 9. State transitions

None in this story: a document has no runtime state. The states the document describes are the parameter value version states of RWB-P3-E1042-APP section 9, and this story fixes the answer that accompanies each one.

| From | Event | Answer of the contract | Status |
|---|---|---|---|
| None | Load received, every check passes | 201 with the load id, table, valid from, status VALIDATED and row count | VALIDATED |
| None | Load received, any check fails | 422 with MSG-GEN-002, MSG-P1-002 or MSG-GEN-001 naming the row and the check; nothing written | Refused |
| VALIDATED | Approval by someone other than the author | 200 with the approver and the approval time; in force from valid from | APPROVED |
| VALIDATED | Approval by the author | 409 with MSG-P7-002; the version stays VALIDATED | VALIDATED |
| APPROVED | Rollback with a reason | 200 with the version set to ROLLED_BACK and the version in force for the business date | ROLLED_BACK |
| APPROVED | Rollback with no earlier approved version | 409 with MSG-P3-015; the version stays APPROVED | APPROVED |

The status vocabulary is LOV-VERSION-STATUS (DF-REF-155). A value that is APPROVED but whose valid from is in the future is not yet in force, and the read answers the version that is in force on the requested date (legacy AC11).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fakes |
| The service owner of rwb-case (P3) | Approves a breaking change and freezes a version |
| RWB-P3-E1042-APP and the platform client RWB-PLT-E1042-CON | Consume the document, pin the version and raise a change request rather than a private variant |
| The case, allocation and timer engines and the Drools evaluator | Read values in force through the document; they have no right in it |
| RW-COE | Loads a value version through the operation; owns the catalog |
| RW-RISK | Approves where a threshold or a limit moves |
| RW-PLATADM | Reads the catalog and owns the environment settings |
| RW-TRIBE | Adds catalog entries through a reviewed pull request on the catalog file |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no e-mail address and no credential appears in a document, a schema, an example or a fake; where a caller must be named, the example uses a user identifier such as `U-41` or a role code only.

### 11. Data

| Item | BR Field ID | Value |
|---|---|---|
| Field identifiers published | DF-REF-132 to DF-REF-158 | DF-REF-132 to DF-REF-146 (parameter_catalog), DF-REF-147 to DF-REF-158 (parameter_value) |
| Catalog projection | Not specified in the source documents (DOR-RWB-P3-E1042-CON-7) | key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret |
| Value projection | Not specified in the source documents (DOR-RWB-P3-E1042-CON-7) | valueInForce, versionNo, validFrom, environment, productGroup, status |
| Example values | Not specified in the source documents (DOR-RWB-P3-E1042-CON-7) | `case.entry.dpd` versions 1 (90) and 2 (91) with valid from 2026-12-10, range 1 to 365; `refdata.cache.ttl-seconds` at 30 in SIT and 300 in PROD; `caselist.export.maxrows` at 10000; `config.cache.ttl-seconds` at 60; `ace.db.password` with secret = true; the user identifier `U-41`, all from the legacy story |
| Personal data | Not specified in the source documents (DOR-RWB-P3-E1042-CON-7) | None. No name, no e-mail address, no account number and no national identifier in an example or a fake |
| Load file | Not specified in the source documents (DOR-RWB-P3-E1042-CON-7) | Rows of key, environment and value, sent as multipart on the load operation with table PARAMETER and a valid from date |
| Cache | Not specified in the source documents (DOR-RWB-P3-E1042-CON-7) | One entry per key, environment and business date; the time to live is the catalog entry `config.cache.ttl-seconds` at 60 (assumed; DL11) |

The contract carries no business value of its own: the ranges, defaults and examples are the ones the legacy story names, and every other value is a row of a load. The column set of a load file beyond the three legacy columns is Not specified in the source documents (GAP-2213; ASM-3640).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Request | Answers | Owner |
|---|---|---|---|
| `GET /api/recovery/case/v1/admin/parameters` | Query: key (prefix), kind, owner, environment | 200 with the entries and the value in force per environment as { key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, valueInForce, versionNo, validFrom }, `valueInForce` absent when secret; 401 MSG-P4-001; 403 MSG-P4-002; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads` | `multipart/form-data`: `file` (rows of key, environment, value), `table` = PARAMETER, `validFrom`; `Idempotency-Key` | 201 with the load id, table, valid from, status VALIDATED and row count; 401; 403 MSG-P4-002; 409 when an approved version has this valid from; 413; 422 MSG-GEN-002, MSG-P1-002 or MSG-GEN-001; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | Path load id | 200 with the approved load, its approver and the approval time; 401; 403 MSG-P4-002; 404; 409 MSG-P7-002 when the approver is the author; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | Path load id; reason | 200 with the version set to ROLLED_BACK and the version in force for the business date; 401; 403 MSG-P4-002; 404; 409 MSG-P3-015 when no earlier version exists; 422 an empty reason; 503 | P3 |
| GET /api/recovery/case/v1/parameters/{key} (getParameter, rwb-case.yaml) | Catalog key and business date | Service workload identities only. 200 with the 14 config/parameter-catalog.csv columns and the value in force from parameter_value (valueInForce, versionNo, validFrom). 404 MSG-P4-003 for a missing or secret key. 401 MSG-P4-001, 403 MSG-P4-002 and 503 MSG-GEN-006. One hop, 2 s. | RWB-P3-E1042-CON; RD-P1-063 |

Four of the operations are the legacy endpoints moved to this service with the PARAMETER handler attached to the reference-load operation (Ownership Map; legacy section 12); the read by key is added by RD-P1-028. The rights are the legacy ones — Reference data C, U and A and Rules and parameters R — and are resolved on the authorise model of rwb-access through the guard the service template wires (GAP-2215; ASM-3642).

#### 12.2 REST operations consumed

None. This contract provides; it consumes nothing. The caller side is the platform client of RWB-PLT-E1042-CON, and the reference-load operation is provided by this same service through RWB-P3-E1043-CON; rwb-source-data uses `GET /parameters/{key}` (12.1); the read is open to service workload identities only (RD-P1-063); the path of the other consuming services is Not specified in the source documents (GAP-2213; ASM-3640).

#### 12.3 Events published

| Event | Topic | Payload | Owner |
|---|---|---|---|
| `rwb.case.ParameterVersionApproved.v1` | `rwb.case.events.v1` | paramKeys, versionNo, validFrom, environment; CloudEvents envelope; written to the outbox in the same transaction as the approval; no personal data and no secret value | P3 |

The event is the legacy `ParameterVersionApproved` internal event of legacy section 12, kept in the target event-name form (DP-14) and delivered through the outbox of RWB-PLT-TE006-CON (DP-09). The rwb-case catalogue carried by the Ownership Map has no parameter event, so its place in that catalogue and any further payload field are Not specified in the source documents (GAP-2212; ASM-3639).

#### 12.4 Events consumed

None. Every instance of rwb-case refreshes its cache on the event of section 12.3 through the inbox library of RWB-PLT-TE006-CON (DP-09) and, at the latest, at the cache time to live; no other service's event is consumed by this contract.

#### 12.5 Workflows and activities

None. A read, a load, an approval and a rollback are one synchronous transaction each on the `rwb-case` api deployment, and no activity and no workflow is registered for them on the `rwb-case` task queue.

#### 12.6 Schedules

None. The value takes effect on its valid from date, the refresh is the event of 12.3 or the cache expiry, and a load is an operator action, so no Temporal Schedule and no job is declared.

#### 12.7 Tables owned

| Table | Schema | Key and indexes | Owner | Exposed by |
|---|---|---|---|---|
| parameter_catalog | rwb_case | PK param_key (varchar(100)); the id column of DF-REF-132 also present; one row per parameter, never per environment | P3 | The catalog read |
| parameter_value | rwb_case | PK id; param_key references parameter_catalog; unique on param_key, environment, product_group and version_no; index on param_key, environment and valid_from where status is APPROVED | P3 | valueInForce, versionNo and validFrom of the read; the load, approve and rollback answers |

Both tables arrive on the rwb-case Flyway sequence in `rwb_case` after the V0001 baseline, with the schema name from the Flyway placeholder; the contract declares no migration and no table of another schema (DP-15; RWB-PLT-E1044-CON). Which of `param_key` and `id` is the primary key in the target is Not specified in the source documents (GAP-2214; ASM-3641).

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-case parameters fake (this story) | The five provided operations, with `case.entry.dpd` 90, `recon.tolerance.pct` 0.00, `recon.treatment.days` 2, `recon.payment.days` 1 and `caselist.allocation.wait.until` 07:15 at version 1, a timeout and 503; the dated read, the secret entry, the refusals MSG-GEN-002, MSG-P1-002, MSG-GEN-001, MSG-P7-002, MSG-P3-015 and MSG-P4-002, and `config.cache.ttl-seconds` at 60 | RWB-P3-E1042-APP, the engines, rwb-source-data (RWB-P1-E1011-APP), RWB-PLT-E1042-CON and the integration harness |
| Startup fixture (this story) | A required key with no value and no default for an environment, answered as a failed health check with MSG-P3-032 | AC3 and TC-P3-E1042-CON-04 |
| Build-check fixtures (this story) | A fixture module with a literal 90 in the entry rule, and a fixture that reads `allocation.retry.limit` | AC7 and TC-P3-E1042-CON-07 |
| Drift and lint test assets (this story) | The assertions that compare each fake, each path, each event name and each table owner with section 12 | The contract test of section 16 and every consuming build |

The fake answers from fixtures and carries role codes and user identifiers only; it never carries a secret value, a customer identifier or a copied production payload.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 5 operations under `/api/recovery/case/v1` | 0 | OpenAPI 3.1, one hop, 2 s timeout and a breaker, `Idempotency-Key` on every POST |
| Kafka | 1 event on `rwb.case.events.v1` | 0 | Outbox and inbox, CloudEvents, cache refresh only |
| Temporal | 0 | 0 | The operations are synchronous and no activity is declared |
| File | 0 | 1 | The load file of table PARAMETER (CSV or XLSX) arrives on the load operation; no runtime file exchange |

### 13. Solution plan

**Deliverables.** `openapi/parameters.yaml` (the dated read, the entry shape and the secret rule), `openapi/parameter-loads.yaml` (the load, approve and rollback operations with their errors and the `Idempotency-Key` rule), `parameters-tables.md` (the two tables, their keys and the Flyway step), `parameters-contract.md` (the event, the startup requirement, the key artefact, the read a service makes and the absence of a consumed operation), and the four fake assets of section 12.8 with the drift and lint test.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| parameters.yaml | Document | The dated read, the entry shape, the secret rule and the value-in-force answer (AC2) |
| parameter-loads.yaml | Document | The load, approve and rollback operations with their answers and rights (AC1, AC3) |
| parameters-tables.md | Document | The two P3 tables, their keys and the Flyway step (AC5) |
| parameters-contract.md | Document | The event, the startup requirement, the key artefact and the caller-side read (AC4, AC6) |
| Fake assets | Test asset | The dated read, the secret entry, the refusal set and the startup fixture (AC7) |
| Drift and lint rules | Test asset | Base-path, operation-id, `Idempotency-Key`, table-owner, event-name, secret and drift assertions (AC1 to AC7) |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract names the two tables of `rwb_case` and no table of another schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. A decision that used a parameter records the key and the version number, so the version travels in the decision inputs | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. This document is that contract, `config.cache.ttl-seconds` is a catalog entry, and the platform client is what the other services compile | H RWB-PLT-E1042-CON; this key's own contract |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. Table PARAMETER is a table code of that surface, and the reference table codes stay with RWB-P3-E1043 | H RWB-PLT-E1043-CON; the same-service contract RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. The approval writes ParameterVersionApproved to the outbox | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The legacy in-process `ParameterService` becomes the published read and the client library, and its fake is Day-1 work | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The four operations sit under `/api/recovery/case/v1` and the lint refuses any other base | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The event is `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1` | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The two tables arrive on the rwb-case sequence and the contract declares no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. SCR-39 reads the catalog through gateway-bff in Epic 8; the contract declares no route | H RWB-PLT-N001-CON |

This pattern table is the DP application of the story. It carries the six platform H contracts H RWB-PLT-E1027-CON (DP-03), H RWB-PLT-E1042-CON (DP-06), H RWB-PLT-E1043-CON (DP-07), H RWB-PLT-TE006-CON (DP-09), H RWB-PLT-E1044-CON (DP-15) and H RWB-PLT-N001-CON (DP-19), and the same-service contracts RWB-P3-E1042-CON (DP-06) and RWB-P3-E1043-CON (DP-07), as DP-added. H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON (DP-04) and H RWB-PLT-E1071-CON (DP-10) sit with patterns this key does not apply, so no row of the table carries them. Every row that is carried is either a wave-0 platform contract or a published contract built against as a fake, so no row blocks the story and Ready to start stays Day 1. The metadata rows Depends on (build), Contract dependencies, Integration dependencies and External dependencies stay as the Work Package fixes them and are corrected at the next version of the story set (GAP-1288; GAP-2398).

**Build steps**

1. Write `parameters.yaml` with the query, the read by key, the entry shape, the secret rule and the value-in-force answer (AC2, AC9).
2. Write `parameter-loads.yaml` with the three write operations, their answers, the `Idempotency-Key` rule and the rights of section 12.1 (AC1, AC3).
3. Write `parameters-tables.md` with the two tables, their keys and the Flyway step (AC5).
4. Write `parameters-contract.md` with the event, the startup requirement, the key artefact and the caller-side read, with its placeholder (AC4, AC6).
5. Add the lint rules: base path, operation id, `Idempotency-Key` on every POST, error envelope, table owner, event name and secret (AC1 to AC7).
6. Generate the four fake assets from the documents and write the drift test that compares each fake with section 12 (AC7).
7. Publish v1, notify RWB-P3-E1042-APP and RWB-PLT-E1042-CON, and record the pinned version.
8. Take the event's place in the catalogue and the caller-side read to the baseline review, and rewrite the document when the two rulings land (GAP-2212; GAP-2213).

**Done when.** Both documents validate and pass every lint rule, the four fake assets answer every operation and every refusal, the drift test is green here and in the app story, and the app story and the platform client have pinned version 1.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-032 | A required parameter has no value for the environment at start-up | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-GEN-002 | A loaded value is outside its range | {field} must be between {min} and {max}. |
| MSG-P1-002 | A loaded value has the wrong type or an unknown key | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | The load file has no data rows | Enter {field}. |
| MSG-P7-002 | The approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | A rollback with no earlier approved version | There is no earlier version of {table} to return to. |
| MSG-P4-001 | Not specified in the source documents (DOR-RWB-P3-E1042-CON-9) | Not specified in the source documents (DOR-RWB-P3-E1042-CON-9) |
| MSG-P4-002 | A role without the right calls one of the four operations | You cannot {action} here. Your role does not include it. |

The texts are the legacy ones, character for character, and Thai text for each follows DL10. MSG-P4-001 and MSG-P4-003 are named as error codes by section 12.1 exactly as the as-built contract of RWB-P3-E1042-APP names them; their texts are not in the source material and this contract adds no text of its own.

### 15. Screens and states

None in this story. SCR-39 states empty, loading, error and no access: Not specified in the source documents (CG-ALL-3740). The contract serves the catalog list and the load result that SCR-39 Rules and parameters shows in Epic 8, and that screen reaches the operations through the gateway-bff composite route (DP-19). Until it exists RW-COE loads files through the operation and reads the catalog through the read, and the load result is listed in the daily data quality report (RWB-E1-011).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1042-CON-01 | AC1, BR10, BR11 | Contract | The five provided operations compared with the Ownership Map and RD-P1-028; an operation outside the rwb-case base; a POST without `Idempotency-Key` |
| TC-P3-E1042-CON-02 | AC2, BR3, BR4 | Contract | `case.entry.dpd` versions 1 (90) and 2 (91) with valid from 2026-12-10, read on 2026-12-09 and 2026-12-10; 30 in SIT and 300 in PROD; a secret entry |
| TC-P3-E1042-CON-03 | AC3, BR5, BR6, BR7 | Contract | Range 400 against 1 to 365; the value "ninety"; an empty file; an author approving; a rollback with no earlier version; a role without the right |
| TC-P3-E1042-CON-04 | AC3, BR8 | Component | A required key with no value and no default for one environment; the health check and MSG-P3-032 |
| TC-P3-E1042-CON-05 | AC4, BR9 | Contract | `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1`: envelope, payload, no personal data, and a drifted event name |
| TC-P3-E1042-CON-06 | AC5, AC6, BR1, BR2 | Contract | The two tables and their keys; the Flyway step; the catalog file; `config.cache.ttl-seconds` at 60; the placeholder of the caller-side read |
| TC-P3-E1042-CON-07 | AC7 | Component | The nine sub-tables complete; the four fake assets; a deliberate drift between a fake and the document |
| TC-P3-E1042-CON-08 | 12.7 | Contract | The two tables of 12.7 at the boundaries of their key, unique and index definitions |
| TC-P3-E1042-CON-09 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1042-CON-AC12) |
| TC-P3-E1042-CON-11 | AC9 | Contract | Read by key before and on the valid from date; unknown key |
| TC-P3-E1042-CON-12 | AC10 | Contract | The five keys rwb-source-data reads |
| TC-P3-E1042-CON-10 | AC6 | Contract | AC6 The startup requirement and the key artefact are fixed (new, D-RCV-60) |

### 17. Guardrails

- No business value in the contract: ranges, defaults and examples are the rows the legacy story names, and every other value is a row of a load; the only numbers this document fixes are the documented defaults 90, 300, 10000 and 60.
- No personal data in an example, a fake or a log: role codes and user identifiers only, and no customer identifier in any answer.
- A secret is listed and never served: an entry with `secret = true` carries no `valueInForce` in any answer, example or fake (BR7).
- The contract names rwb-case tables and rwb-case operations as provided and consumes nothing; it never restates another service's operation as its own (DP-01, DP-13).
- The event stays inside `rwb.case.<Event>.v1` on `rwb.case.events.v1`, with no personal data and no secret value, and no second event is invented (DP-14, BR9).
- Every POST carries `Idempotency-Key`, and a repeat load with the same content hash writes nothing.
- The two tables arrive on the rwb-case Flyway sequence with the schema name from the placeholder; the contract declares no baseline and no migration of another schema (DP-15).
- The contract is versioned: a breaking change raises a new version and deprecates the old one in place of editing it.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service, versioned, changed without a release | The four operations, the dated read, the two tables and the event | TC-P3-E1042-CON-01, TC-P3-E1042-CON-02, TC-P3-E1042-CON-06 |
| REQ-ACA-005 | A secret is held in the secret store and never in a table, a log or an answer | The secret rule of 12.1 and 12.3 and the refusal of a value for `ace.db.password` | TC-P3-E1042-CON-02, TC-P3-E1042-CON-05 |
| ADR-014 | Schema and login per service in ACE PostgreSQL | The two tables of `rwb_case` and the declaration that no other service reads them | TC-P3-E1042-CON-06, TC-P3-E1042-CON-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four provided operations with the 2 s client budget and `Idempotency-Key` | TC-P3-E1042-CON-01 |
| ASM-3639 | The parameter event keeps the legacy name in the target form | The one event of 12.3 and its payload | TC-P3-E1042-CON-05 |
| ASM-3640 | A service reads the catalog with a key-prefix query and the Rules and parameters R right | The caller-side read of 12.2 and AC6 | TC-P3-E1042-CON-06 |

The legacy test set TC-E1-042-01 to TC-E1-042-12 is executed by RWB-P3-E1042-APP and is not copied here.

### 19. Out of scope

- The runtime of the four operations — the catalog repository, the value repository, the load checks, the startup check, the cache and the two build checks (RWB-P3-E1042-APP).
- The legacy acceptance criteria AC1 to AC11 and the legacy test cases TC-E1-042-01 to TC-E1-042-12 (RWB-P3-E1042-APP).
- The parameters client library that the other services compile against (RWB-PLT-E1042-CON).
- The reference table codes and their loads (RWB-P3-E1043-CON; RWB-P3-E1043-APP).
- The product-specific parameter values for Mortgage, HP and SSME (RWB-P3-E1045-APP).
- Rule packages and the registry (P7 rwb-decision; RWB-P7-E1073-CON).
- The authorise, role and scope resources of rwb-access (P4 rwb-access).
- The SCR-39 screen (Epic 8) and its gateway-bff route (RWB-PLT-N001-CON).
- The event's place in the rwb-case catalogue and the caller-side read, both with their placeholder (GAP-2212; ASM-3639; GAP-2213; ASM-3640).

### 20. Remaining delivery steps

- Size the story (delivery lead).
- Epic design sign-off (solution architect).
- Contract published with the read by key in rwb-case.yaml and the fake published at a fixed version (rwb-case service owner).
- Consumer acceptance by rwb-source-data (rwb-source-data service owner).
- Test data loaded in DEV and Test Cases v9 rows confirmed (QA lead).
