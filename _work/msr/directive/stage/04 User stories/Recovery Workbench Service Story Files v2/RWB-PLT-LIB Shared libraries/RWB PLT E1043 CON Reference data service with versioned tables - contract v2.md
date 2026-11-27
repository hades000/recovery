# RWB-PLT-E1043-CON Reference data service with versioned tables - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: delta slice split from RWB-E1-043 for the platform library RWB-PLT-LIB — the published contract of the reference-data client library. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 67 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1043-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-043 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP04, DP05, DP06, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| DP-added dependencies (build-against, from the DP rows of this story) | H RWB-PLT-E1072-CON (DP-04); H RWB-PLT-E1042-CON (DP-06; C RWB-P3-E1042-CON); H RWB-PLT-E1037-CON and C RWB-P4-E1037-CON (DP-08); H RWB-PLT-TE006-CON (DP-09); H RWB-PLT-E1047-CON (DP-14); H RWB-PLT-E1044-CON (DP-15); H RWB-PLT-N001-CON (DP-19). All are platform CON stories or published contracts built against as fakes, so Ready to start stays Day 1. |
| Model version in force (owner) | Reference data read through RWB-P3-E1043-CON and owned by rwb-case (P3); the rule package registry stays with rwb-decision (P7). Table name per the R9 placeholder. |
| Contract version | v1 (published to the contract registry, build step 9); owner contract versions not specified in the source documents (DOR-RWB-PLT-E1043-CON-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-020) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **platform contract owner**, I want **the published contract of the reference-data client — the client interface and its records, the version and row data contract with the legacy field ids, the list operation it consumes, the LOV-REF-TABLE code set with the rule-table exclusion, the no-version-in-force exception with its message id and the cache and TTL rule, plus the fakes — instead of the monolith's `recovery.casewf.refdata.api` package that read `reference_version` and `reference_row` in the same database** — so that **all 19 services read a dated, approved version through one frozen contract while the tables stay with P3**.

This is the contract slice of the delta of legacy RWB-E1-043. The legacy module published `ReferenceVersionRegistry` and `ReferenceDataService` inside `recovery.casewf.refdata.api` and read the two tables in the same database; here the registry and the tables stay with rwb-case (P3), and only the read side becomes a platform library contract that a service compiles against. The contract publishes:

- The client interface `ReferenceDataClient` with `rows`, `versionInForce` and `versions`, and the records `ReferenceVersion` and `VersionedRows`, taken from the legacy published interface with the same method signatures and the same fields.
- The typed refusal `NoVersionInForceException(tableCode, businessDate)` carrying the message identifier MSG-P3-027, and the caller's rule that an engine does not run on a missing or stale value.
- The version and row data contract with the legacy field identifiers DF-REF-159 to DF-REF-171 and DF-REF-181 to DF-REF-184, and the status vocabulary VALIDATED, APPROVED and ROLLED_BACK.
- The two consumed operations of rwb-case (P3), the list operation that reads a list with its versions and the parameters operation that carries the cache time to live, each one hop with a 2 s timeout.
- The LOV-REF-TABLE code set of twelve reference table codes, with the rule-package exclusion and the holiday-calendar exclusion written as testable sentences.
- The cache and TTL rule, the fakes and the drift test that every consuming service runs in its own build.

The library is platform, not one of the 19 services: it has no `rwb_<short>` schema, no topic, no task queue and no REST base. It has no build dependency and starts on Day 1, so the app story and the 19 services can build and test their read before any approved version is loaded.

### 2. Business rationale

The legacy module could assume that the version and its rows were in the same database and that the caller was in the same process, so the shape of what a caller receives was never a contract. After the split the value arrives over a service boundary and is read by 19 services, which means the interface, the refusal, the code set and the cache rule have to be agreed before any engine writes its start-up hook — otherwise each service reads a different projection or, worse, reads `reference_version` directly, which the schema-per-service rule forbids (DP-01, Architecture v5 slide 29).

**The division is fixed.** The two versioned tables `reference_version` and `reference_row`, the reference version registry, the read service, the load and approve operations and the cache stay with **RWB-P3-E1043-APP** and this story's owner pair **RWB-P3-E1043-CON**, and the legacy acceptance criteria AC1 to AC10 of RWB-E1-043 stay with RWB-P3-E1043-APP. This contract publishes only the read side that every service binds: `RWB-PLT-E1043-CON` and `RWB-PLT-E1043-APP` deliver the reference-data client library and nothing of the store.

The contract is also what makes the audit promise achievable. "Every engine can say which version it used" only holds if the value arrives with its version number, if the version in force is derived from a business date the caller passes, and if a missing version is a refusal rather than a default. Writing those three things down once keeps the log lines, the decision records and the data quality report readable across the migration, and it keeps the legacy message identifier MSG-P3-027 unchanged.

The fakes are the Day-1 unblocker; the Day-1 fakes cover RWB-PLT-E1027-CON (decision record), RWB-PLT-TE006-CON (outbox and inbox), RWB-PLT-E1071-CON (workflow kit) and RWB-PLT-N001-CON (gateway-bff route), and each is replaced by its published contract in the same iteration. The first approved version of each table is loaded in rwb-case later in wave 1; with the client fake and the owner fakes, all 19 services and the integration harness build and test their read against the same document, and the drift test fails a build when a field, the refusal or the code set changes (Template and Rules §R5.4, class C). The acceptance criteria below are new, tagged `(new, D-RCV-60)`, and test only the contract deliverable: no legacy acceptance criterion is copied into this story.

### 3. Preconditions

- The Ownership Map default ruling stands: `reference_version`, `reference_row` and `lov_value` are P3 rwb-case tables, and `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 rwb-decision tables (Template and Rules §R3; Ownership Map). This contract declares no table and no migration.
- The list operation and the parameters operation are named by Architecture v5 slide 14 (rwb-case owns the case, the queues, the tasks and the reference data) and by the Ownership Map; their paths follow the naming rule of Template and Rules §R4 under the rwb-case base.
- The field identifiers DF-REF-159 to DF-REF-171 and DF-REF-181 to DF-REF-184 are taken from the Logical Data Model and Data Dictionary, character for character.
- The legacy message identifiers MSG-P3-027 and MSG-P4-002 are used unchanged in the refusal and in the permission example.
- The twelve reference table codes are the ones LOV-REF-TABLE carries in legacy section 8 BR1; the set is data and changes by a load, not by a contract version.
- The rules side is fixed: rule packages are governed in rwb-decision (P7) and evaluated through the embedded kit (DP-04; Architecture v5 slides 27 and 14; Temporal and Drools design slide 15), so a rule package code is never a reference table code.
- The holiday calendar is ACE data under `v_ace_holiday`, read by rwb-source-data (P1) and by no library (DP-05); the contract states the exclusion and serves none of it.
- The cache time to live is the value the legacy story carries, `refdata.cache.ttl-seconds` = 300 (assumed; DL11). The catalog entry that carries it is a named entry of the rwb-case parameter catalog; the entry key is Not specified in the source documents (GAP-1409).
- No approval is required to publish a Draft contract: the surface is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. The contract author writes the interface document: the three methods, the two records, the checked refusal and the rule that no repository, table or schema type crosses a published signature.
2. The author writes the version and row data contract from the legacy field identifiers, with the status vocabulary, one worked example using EXPOSURE_BAND versions 3 and 4 and one using QUEUE version 7.
3. The author writes the two consumed operations with their owner, their response projection and the 2 s timeout, and fixes that the list operation reads a list with its versions.
4. The author writes the code set: the twelve LOV-REF-TABLE codes, the rule-package exclusion and the holiday-calendar exclusion, each as a testable sentence.
5. The author writes the refusal section: MSG-P3-027, the table code and the business date in the exception, the non-retryable rule and the caller's no-run rule.
6. The author writes the cache and TTL rule: one entry per table code and business date, the time to live read through the parameters operation, and the refresh by expiry because no event exists.
7. The lint and schema steps run: the signatures compared with the legacy published interface, a mandatory message identifier on the refusal, the twelve codes and the two exclusions asserted, and a personal-data scan over every example.
8. The client fake and the three owner fakes are generated from the document, the drift test is wired into the build of every consuming service, and v1 is published to the contract registry.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published signature exposes a repository, a table or a schema type | The lint step fails the build and the document is not published | Lint finding, no message id | AC1 |
| X2 | The refusal is published without the message identifier MSG-P3-027, or as a retryable failure | The lint step fails the build; the refusal keeps the identifier and stays non-retryable | Lint finding, no message id | AC4 |
| X3 | A code outside the twelve reference table codes is published as a valid code | The lint step fails the build; the code set is the twelve and a rule package code is named as refused | Lint finding, no message id | AC5 |
| X4 | The holiday calendar is published as a table code or a served read | The lint step fails the build; the calendar is ACE data read through `v_ace_holiday` by P1 | Lint finding, no message id | AC5 |
| X5 | An example carries a customer name, an account number, a national identifier or an email address | The scan rejects the example; codes, user identifiers and role codes only | Review finding | AC3 |
| X6 | A breaking change is made to a published signature, a record field or the refusal | The change raises v2 and marks v1 deprecated; v1 is never edited in place | Deprecation notice | AC6 |
| X7 | A value the consumers need is named by no source — the artefact coordinates, the catalog entry of the TTL, the published client surface | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1410; ASM-2460) | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and a fake; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | Field order inside a row projection, the example values and the fake fixture set are open until the version is frozen; the signatures, the refusal, the code set and the cache rule are fixed |
| Valuable | All 19 services and the integration harness can build and test their reference read before any approved version exists |
| Estimable | One interface, two records, one refusal, two consumed operations, one code set, one cache rule and the fakes |
| Small | One sprint for the documents, the fakes and the lint rules |
| Testable | Each criterion below is one schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the reference-data client contract

  Background:
    Given the library is platform, not one of the 19 services, and publishes no REST base, no topic and no queue of its own
    Given reference_version, reference_row and lov_value stay with rwb-case and the rule tables stay with rwb-decision

  Scenario: AC1 The interface, the records and the refusal are published (new, D-RCV-60)
    Given the published contract document of the reference-data client at version 1
    When it is validated and linted
    Then it publishes ReferenceDataClient.rows(String tableCode, LocalDate businessDate), versionInForce(String tableCode, LocalDate businessDate) and versions(String tableCode)
    Then VersionedRows carries tableCode, versionNo, validFrom and rows
    Then ReferenceVersion carries id, tableCode, versionNo, validFrom, validTo, status, authorUserId, approverUserId, approvedAt, rowCount and contentHash
    Then ReferenceDataClient declares NoVersionInForceException as its checked refusal and no other thrown type
    Then no published signature mentions a repository, a table, a schema or a connection

  Scenario: AC2 The two consumed operations and their owner are published (new, D-RCV-60)
    Given the consumed-operation section of the contract
    When it is validated against the Ownership Map
    Then exactly two operations are declared: GET /api/recovery/case/v1/admin/lists/{listCode} and GET /api/recovery/case/v1/admin/parameters
    Then both are owned by rwb-case (P3) and read through one hop with a 2 s timeout and a breaker
    Then the list operation reads a list with its versions, so the approved version in force and its rows arrive in that answer
    Then the parameters operation carries the cache time to live as a catalog entry
    Then the library declares no path, no topic and no queue of its own

  Scenario: AC3 The version and row data contract carries the legacy field ids and the status vocabulary (new, D-RCV-60)
    Given the version and row data contract of the contract document
    When it is cross-checked with the Logical Data Model and Data Dictionary
    Then the version contract carries DF-REF-159 to DF-REF-171
    Then the row contract carries DF-REF-181 to DF-REF-184
    Then the status vocabulary is VALIDATED, APPROVED and ROLLED_BACK, and no other status is accepted
    Then the payload carries the table code, the version number, the valid from and valid to, the row count, the content hash and the rows
    Then the payload carries no rule field and no holiday field
    Then no example carries a customer name, an account number, a national identifier or an email address

  Scenario: AC4 The refusal carries MSG-P3-027 and the caller's no-run rule (new, D-RCV-60)
    Given the refusal section of the contract document
    When it is linted against the message catalogue
    Then NoVersionInForceException carries messageId MSG-P3-027 together with the table code and the business date
    Then the dated read with no approved version in force is refused with MSG-P3-027 naming the table code and the business date, the status code is Not specified in the source documents (GAP-0698), and never an older version, a default row or an empty list
    Then the document states that an engine does not run on a missing or stale value and raises its own alert to the platform administrator
    Then the refusal is declared non-retryable and is never a default value and never a silent fallback to an older version

  Scenario: AC5 The code set, the rule-package exclusion and the holiday exclusion are published (new, D-RCV-60)
    Given the code-set section of the contract document
    When it is validated against LOV-REF-TABLE and the two owner sources
    Then the code set is PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD and PRODUCT_PARAMETER
    Then a rule package code is not accepted, and the document names rwb-decision (P7) and the rules kit as the owner of rule packages
    Then the holiday calendar is not served, and the working-day calculator reads v_ace_holiday through the P1 query
    Then LOV-REF-TABLE carries no rule table code and no holiday code

  Scenario: AC6 The fakes and the drift test of every consuming service are published (new, D-RCV-60)
    Given the fakes of the contract and the drift test of every consuming service
    When the contract test runs against the published artefact
    Then the client fake answers a version in force with its rows and a no-version answer with MSG-P3-027
    Then the list fake answers the twelve codes and the parameters fake answers the time to live at 300
    Then the kit boundary fake proves that no rule package code and no rule row reaches the client
    Then the drift test of each consuming service fails the build on any difference from section 12
    Then a breaking change raises v2 and deprecates v1, and no consumer sees an edited v1

  Scenario: AC7 The cache refresh is by expiry and no event is declared (new, D-RCV-60)
    Given the cache and TTL section of the contract document
    When it is validated against the consumed operations
    Then a version change reaches a consumer by cache expiry of the time to live
    Then the library declares no event, no topic and no queue of its own

  Scenario: AC8 The version in force is chosen by date and only an APPROVED version is served (new, D-RCV-60)
    Given the version selection and status rule of the contract document
    When the contract test runs against the client fake
    Then the version in force is chosen from the caller's business date and the valid from and valid to dates
    Then the chosen version number travels in the answer
    Then only an APPROVED version is served, and a VALIDATED or ROLLED_BACK version is never served

  Scenario: AC9 Every business rule has a criterion and a test (new, D-RCV-60)
    Given the business rules of section 8
    When the Covered by column is checked against sections 7 and 16
    Then each rule BR1 to BR11 names at least one criterion of section 7 and one test case of section 16
    Then the architecture rule BR2 is also held by the boundary test TC-PLT-E1043-CON-01

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the status vocabulary of AC3 and the version selection of AC8
    When a status change that the model does not allow is requested
    Then the change is refused and the stored version keeps its status
    Then no version is served under a refused status
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here — AC1 to AC10 of RWB-E1-043 belong to RWB-P3-E1043-APP — and every number and identifier comes from the legacy story, the Ownership Map or Architecture v5, character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The contract publishes three read methods and two records, and nothing else: `ReferenceDataClient`, `ReferenceVersion` and `VersionedRows` | RWB-E1-043 section 12; RWB-PLT-E1043-APP section 1 | AC1; TC-PLT-E1043-CON-01 |
| BR2 | No repository, table, schema or connection type crosses a published signature: the client reads the owner's contract and holds no table | DP-01; Architecture v5 slide 29 | AC1; TC-PLT-E1043-CON-01 |
| BR3 | The version in force is chosen from the caller's business date and the valid from and valid to dates, and the chosen version number travels in the answer | RWB-E1-043 section 8 BR3 (R-UNI-38) | AC8; TC-PLT-E1043-CON-06 |
| BR4 | A missing approved version is the refusal `NoVersionInForceException` with MSG-P3-027, non-retryable, and never a default value | RWB-E1-043 section 8 BR9; Principle 5; NFR-033 | AC4; TC-PLT-E1043-CON-04 |
| BR5 | The code set is the twelve LOV-REF-TABLE codes; a rule package code is not a reference table code and is refused | RWB-E1-043 section 8 BR1 and section 12; DP-04 | AC5; TC-PLT-E1043-CON-04 |
| BR6 | The holiday calendar is not served: it is ACE data under `v_ace_holiday`, read by rwb-source-data (P1) | RWB-E1-043 section 2 and section 12; DP-05 | AC5; TC-PLT-E1043-CON-04 |
| BR7 | The cache time to live is a catalog entry read through the parameters operation, never a code constant; the legacy value is 300 (assumed; DL11) | DP-06; RWB-E1-043 section 13 | AC2, AC6; TC-PLT-E1043-CON-02, TC-PLT-E1043-CON-05 |
| BR8 | A version change reaches a consumer by cache expiry, because the legacy design publishes no event and this contract declares none | RWB-E1-043 section 12 | AC7; TC-PLT-E1043-CON-06 |
| BR9 | The status vocabulary is VALIDATED, APPROVED and ROLLED_BACK, and only an APPROVED version is served | RWB-E1-043 section 9 and section 17 | AC8; TC-PLT-E1043-CON-06 |
| BR10 | A breaking change raises a new version and deprecates v1; a published signature is never edited in place | Template and Rules §R7.2; §R5.4 class C | AC6; TC-PLT-E1043-CON-05 |
| BR11 | The message identifier MSG-P3-027 is kept unchanged although the tables now sit with rwb-case | RWB-E1-043 section 14; ASM-2460 | AC4; TC-PLT-E1043-CON-04 |

**Open decisions.** DL10 carries the assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863, and DL11 carries ASM-0553, ASM-0703, ASM-1051 and ASM-1104. Each assumption is confirmed by the directive; each decision stays open with its owner until it is recorded.

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are fixed here so that the two documents agree; the runtime behind them is specified in RWB-PLT-E1043-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Cache entry of a read | ABSENT | No entry is held for that table code and business date |
| Cache entry of a read | CACHED | The approved version in force and its rows are held for the time to live |
| Cache entry of a read | EXPIRED | The time to live elapsed and the next read reloads |
| Cache entry of a read | EVICTED | The version was rolled back or the code was refused; the entry never serves a read |
| Reference version, owner states | VALIDATED, APPROVED, ROLLED_BACK | rwb-case's states; this contract reads only the one in force for a date |

The owner states are named here only so that the contract and the store agree on the vocabulary; the transitions among them and the effective dating are the business of RWB-P3-E1043-APP section 9.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the interface document, the data contract, the code set, the refusal, the cache rule and the fakes |
| The platform owner of the library | Approves a breaking change and freezes a version |
| The service teams of the 19 services | Consume the contract, pin the version and raise a change request rather than a private variant |
| The rwb-case owner (P3) | Confirms the two operations, the version and row projection, the twelve codes and the status vocabulary |
| The rwb-decision owner (P7) | Confirms that rule packages and the registry are outside this contract |
| The rwb-source-data owner (P1) | Confirms the holiday-calendar exclusion and the `v_ace_holiday` read |
| RW-REFADM, RW-RISK, RW-COE | Load and approve values in rwb-case; have no right in the contract |
| RW-PLATADM | Receives the incident a caller raises when no version is in force |
| No delegation of authority level applies | A library contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in a document, a schema, an example or the fake. Where a caller must be named, the example uses the user identifier `U-REF-01` or a role code only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes signatures, field identifiers, codes, status values and one message identifier; no customer, account, case or document value appears | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |
| Version projection | Table code, version number, valid from, valid to, status, author, approver, approved at, row count, content hash, load identifier | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |
| Row projection | Row key and row data, as the two row fields DF-REF-183 and DF-REF-184 carry them | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |
| Example values | EXPOSURE_BAND versions 3 and 4 with bands "E1" to "E5", QUEUE version 7, the content hash "a1b2" and the user identifiers "U-REF-01" and "U-RSK-01", all from the legacy story | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |
| Personal data | None. No name, no email address, no account number and no national identifier in a schema, an example or the fake | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |
| Tables published | None. The two reference tables stay with rwb-case (P3) and the rule tables with rwb-decision (P7); the contract declares no table and no migration | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |
| Field identifiers | DF-REF-159 to DF-REF-171 and DF-REF-181 to DF-REF-184, from the Logical Data Model and Data Dictionary | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |
| Retention | None at the contract: a document keeps no data, and the fake holds only the examples it publishes | Not specified in the source documents (DOR-RWB-PLT-E1043-CON-7) |

The version projection is the one place where a value could leak into the contract, so the document fixes that the rows travel as row key and row data and that no rule content and no holiday row is part of the projection (Architecture v5 slides 27 and 29).

### 12. Contract

#### 12.1 REST operations provided
None. The library is a Java artefact: it publishes an interface and two records, not an OpenAPI document, and it has no REST base of its own. The reference read, the list read, the parameters read, the reference-load and the approve operations belong to rwb-case (P3); the reference data screens reach them through the gateway-bff composite route of RWB-PLT-N001-CON, which this contract names and does not declare (DP-19).

#### 12.2 REST operations consumed
| Operation | Provider | Why the contract needs it | Pattern |
|---|---|---|---|
| GET /api/recovery/case/v1/admin/lists/{listCode} | rwb-case (P3) | The list read with its versions: the twelve LOV-REF-TABLE codes, and for a table code the approved version in force with its rows | DP-07, DP-11 |
| GET /api/recovery/case/v1/admin/parameters | rwb-case (P3) | The cache time to live as a catalog entry, so the bound is data and not a code constant | DP-06, DP-11 |

Two consumption rows, both one hop, with a 2 s timeout and a breaker per provider (Architecture v5 slide 11). The list operation reads a list with its versions, which is the legacy contract's own wording, so the version and rows of a table code arrive in that answer and no third call is needed. The cache-time-to-live catalog entry is Not specified in the source documents (GAP-1410; ASM-2461); the legacy value 300 (assumed; DL11) is the default the document publishes and is read through this operation, never hard-coded.

#### 12.3 Events published
None. The library publishes no event and the legacy design publishes no event for a version change; the contract states it so that no consumer waits for one.

#### 12.4 Events consumed
None. The legacy design publishes no event for a version change and this contract declares none: a new approved version reaches a consumer at its next cache expiry. A later owner event would be consumed through the inbox library of RWB-PLT-TE006-CON, and the contract would then be raised to a new version.

#### 12.5 Workflows and activities
None. The contract declares no workflow, no activity and no task queue: the client is called inside the caller's own activity or start-up hook on that service's queue `rwb-<short>`, and never from workflow code.

#### 12.6 Schedules
None. The contract declares no Schedule and no job; the refresh is the cache expiry of section 9, and no job of the legacy design belongs to the library.

#### 12.7 Tables owned
None. `reference_version`, `reference_row` and `lov_value` stay with rwb-case (P3) under the Ownership Map default ruling and are named here only as the source of the read; `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` stay with rwb-decision (P7) and are not named as a source at all. The document declares no table, no column and no migration, and no consumer of it may read a reference table or a rule table (DP-01).

#### 12.8 Contract fakes
| Fake | Serves | Used by |
|---|---|---|
| Client fake (this story) | `ReferenceDataClient.rows`, `versionInForce` and `versions`, answered from the owner fakes below | RWB-PLT-E1043-APP, every service's read test and the integration harness |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | The version and rows of the list operation | The version-in-force answer with EXPOSURE_BAND versions 3 and 4 and QUEUE version 7, and the no-version answer for TEAM on 2026-11-30 (AC1, AC3, AC6) |
| rwb-case list fake (RWB-P3-E1043-CON) | `GET /api/recovery/case/v1/admin/lists/{listCode}` | The twelve codes, a rule package code that is absent from the list, and a 403 for a role without Reference data R (AC2, AC5) |
| rwb-case parameter fake (RWB-P3-E1042-CON) | `GET /api/recovery/case/v1/admin/parameters` | The cache time to live at 300, raised and missing (AC2, AC6) |
| Rules kit boundary fake (RWB-PLT-E1072-CON) | The kit's evaluator boundary | A call proving that no rule package code and no rule row reaches the client (AC5, AC6) |

The client fake answers from the owner fakes rather than from copied payloads, so a change in rwb-case shows up as a contract-test failure in every consuming service rather than as a surprise at run time.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)
| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the contract publishes interfaces, not operations | 2 operations over 1 provider | OpenAPI 3.1 at rwb-case, one hop, 2 s timeout, breaker per provider, GET only |
| Kafka | 0 published | 0 consumed | No event exists for a version change; the refresh is the cache expiry |
| Temporal | 0 | 0 | The client runs inside the caller's activity and owns no queue |
| File | 0 | 0 | A reference load file belongs to the reference data administrator and rwb-case; no file crosses this contract |

### 13. Solution plan

**Package.** Shared library contract artefact of the platform, the interface and the records in `th.co.scb.ace.workbench.recovery.platform.refdata.api`, the document, the fakes and the drift test; the implementation is RWB-PLT-E1043-APP. The library is not one of the 19 services and declares no schema, topic, queue or REST base.

**Hardware and software change.** The contract records the move of the reference read from an in-process service call against a shared schema to a published library interface compiled into 19 services (Architecture v5 slides 20 and 29): the two tables stay with rwb-case (P3) in the existing ACE PostgreSQL server, and the library owns no schema, the client keeps a small heap cache and one log line per table read, and no new hardware is implied. The software change is that a service no longer needs a grant on a reference table, and that the version number of every value an engine used is visible in its logs.

**Deliverables.** The interface document; the version and row data contract with the field identifiers; the operation rows; the code set with the two exclusions; the refusal section; the cache and TTL section; the client fake and the owner fakes it composes; the drift test and the lint rules.

**Screens and states.** The library has no screen and no route (DP-19), so screens SCR-39, SCR-40 and SCR-42 and their empty, loading, error and no-access states are not part of this contract and are not in this story's scope; the story that owns each screen carries them.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract fixes that the client reads the owner's two tables through the rwb-case contract only | none; referred to, and the consuming story RWB-PLT-E1043-APP carries the dependency |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision. The registry stays with rwb-decision (P7) and the contract fixes that this client serves no rule table | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-E1072-CON and C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. The contract fixes that the ACE views are read by rwb-source-data (P1) and never by this library | none; referred to, and the consuming story RWB-PLT-E1043-APP carries the dependency |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The cache time to live is a catalog entry of that contract | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-E1042-CON and C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. This contract is that dependency for every other story, and it is built against the owner contract it documents | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. A permission failure on the consumed read is surfaced by the caller's guard and the contract requires the client to fail closed | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-E1037-CON and C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. The contract declares no event, because no version-change event exists | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The legacy in-process `ReferenceDataService` is the published interface with its fake | none (C from the legacy dependency); referred to, and the consuming story carries it |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The two consumed paths sit under `/api/recovery/case/v1`, and the library declares no path | none; referred to, and the consuming story RWB-PLT-E1043-APP carries the dependency |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The contract states that the library has no topic and follows the caller's queue name only | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The contract declares no migration; each consuming service applies its own baseline | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. The reference data screens read the tables through gateway-bff in Epic 8; the contract declares no route | referred to; the consuming story RWB-PLT-E1043-APP carries the dependency H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Interface document | Document | The three methods, the two records, the checked refusal and the no-repository rule (AC1) |
| Version and row data contract | Document | The field identifiers, the status vocabulary and the projections (AC3) |
| Operation rows | Document | The two consumed operations, their owner, their projection and the timeout (AC2) |
| Code set | Document | The twelve LOV-REF-TABLE codes, the rule-package exclusion and the holiday exclusion (AC5) |
| Refusal section | Document | MSG-P3-027, the exception fields, the non-retryable rule and the caller's no-run rule (AC4) |
| Cache and TTL section | Document | One entry per read, the time to live from the catalog, the refresh by expiry (BR7, BR8) |
| Client fake and owner fakes | Test asset | The answers every consuming service builds and tests against (AC6) |
| Drift test and lint rules | Test asset | The assertions that fail a build on any difference from section 12 (AC1 to AC6) |

**Build steps**

1. Write the interface document with the three methods, the two records and the checked refusal, taken from the legacy published interface character for character (AC1).
2. Write the version and row data contract from DF-REF-159 to DF-REF-171 and DF-REF-181 to DF-REF-184, with the status vocabulary (AC3).
3. Write the operation rows for the list operation and the parameters operation, with their owner, their projection and the 2 s timeout (AC2).
4. Write the code set with the twelve codes, the rule-package exclusion and the holiday exclusion, each as a testable sentence (AC5).
5. Write the refusal section with MSG-P3-027, the exception fields and the no-run rule (AC4).
6. Write the cache and TTL section, with the time to live as a catalog entry and the refresh by expiry (BR7, BR8).
7. Add the lint rules: no repository or table type in a signature, a mandatory message identifier, the twelve codes asserted, the two exclusions asserted, and a personal-data scan over every example.
8. Generate the client fake over the three owner fakes and write the drift test that pins the signatures, the fields, the refusal and the message identifier.
9. Publish v1 to the contract registry, notify RWB-PLT-E1043-APP and the consuming services, and record the version each one pins.

**Done when.** The document validates, every lint rule passes, the fake answers the version-in-force and no-version cases and the two consumed operations, the drift test is green on the build of this story and in at least one consuming service, and v1 is recorded as the pinned version.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-027 | No approved version of the table is in force for the caller's business date, or the code is not a reference table code | The {table} load was refused: {check}. Version {version} stays in force. | `NoVersionInForceException`, messageId MSG-P3-027, non-retryable in the caller |
| MSG-P4-002 | The caller holds no Reference data R right for the consumed list or parameters read | You cannot {action} here. Your role does not include it. | The caller's own 403; the contract requires the client to fail closed |

The two texts are the legacy ones, character for character, and Thai text for each follows decision DL10. The refusal keeps the message identifier MSG-P3-027 unchanged although the tables now sit with rwb-case; no source renumbers it, and renumbering would break every log line, data quality report and decision record that cites it (ASM-2460).

### 15. Screens and states

No screen in this story, and the contract declares none. The library has no user interface: it answers inside an activity or a start-up hook and the screens read the result through the owning service. The reference data screens SCR-39, SCR-40 and SCR-42 come in Epic 8 and read the tables through the gateway-bff composite route against the rwb-case contract; the screen is out of scope here. This story fixes the four cache-entry states of section 9 so that the app story's operability view has one vocabulary. The screen states empty, loading, error and no access of SCR-39, SCR-40 and SCR-42 are Not specified in the source documents (CG-ALL-1375, CG-ALL-1376, CG-ALL-1377), because Screen Specifications v1 does not specify them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1043-CON-01 | AC1 | Contract | The document validated and linted; the three signatures and the two records compared with section 13; the checked refusal; no repository or table type in any published signature |
| TC-PLT-E1043-CON-02 | AC2 | Contract | The two operation rows compared with the Ownership Map and Architecture v5 slide 11; the list operation's version projection; the parameters projection; the 2 s timeout |
| TC-PLT-E1043-CON-03 | AC3 | Contract | The version and row contract compared field by field with DF-REF-159 to DF-REF-171 and DF-REF-181 to DF-REF-184; the three status values; a personal-data scan |
| TC-PLT-E1043-CON-04 | AC4, AC5 | Contract | The refusal carrying MSG-P3-027 and the no-run rule; the twelve codes; a rule package code refused; the holiday calendar refused, and this library reads no ACE view (the calendar is read by P1 only) |
| TC-PLT-E1043-CON-05 | AC6 | Component | The client fake over the reference-data, list, parameter and kit boundary fakes; the version-in-force and no-version answers; the drift test; a breaking change raises v2 and deprecates v1 |
| TC-PLT-E1043-CON-06 | AC7, AC8 | Component | The cache refresh by expiry with no event declared; the version in force chosen by business date; only an APPROVED version served |
| TC-PLT-E1043-CON-07 | AC9 | Contract | Each rule BR1 to BR11 checked against its Covered by criterion in section 7 and test case in section 16; the boundary test of BR2 in TC-PLT-E1043-CON-01 |
| TC-PLT-E1043-CON-08 | AC10 | Component | A status change the model does not allow is refused and the stored version keeps its status; test data Not specified in the source documents (NEWAC-RWB-PLT-E1043-CON-AC12) |

The legacy set TC-E1-043-01 to TC-E1-043-11 is executed by RWB-P3-E1043-APP and is not copied here.

### 17. Guardrails

- No business value in the contract: table codes, versions, bands, limits and periods are rows of rwb-case, and the only number this document fixes is the documented default 300 of the cache time to live.
- No personal data in a schema, an example, a fake or a log: codes, user identifiers and role codes only, and the scan fails the build otherwise.
- No table and no migration in this contract: the reference tables are rwb-case's and the rule tables are rwb-decision's, and a consumer that reads either breaks DP-01.
- No repository, table, schema or connection type in a published signature; the interface is the whole surface.
- A missing version is a refusal with MSG-P3-027 and never a default value or a silent fallback.
- Only an APPROVED version is served; VALIDATED and ROLLED_BACK are named so that a consumer can never serve them.
- No rule package code is accepted and no holiday row is served; the rules kit and rwb-source-data are named as the owners of those reads.
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.
- No event is invented for a version change; the refresh is the cache expiry, and an owner event would arrive through the inbox library and a new contract version.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-011 | Reference data service with versioned tables, valid from and to, author and approver | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-PLT-E1043-CON-01 to TC-PLT-E1043-CON-05 |
| REQ-CWC-006 | Roles, teams, queues and capacity as versioned reference data | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-PLT-E1043-CON-04 |
| REQ-CWC-016 | Every engine logs the table code and version of every table it reads | Cited in RWB-E1-043 section 8 BR7; Not specified in the source documents (GAP-1410; ASM-2461) | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-PLT-E1043-CON-01, TC-PLT-E1043-CON-03 |
| TC-E1-043-01, TC-E1-043-02, TC-E1-043-03, TC-E1-043-04, TC-E1-043-05, TC-E1-043-06, TC-E1-043-07, TC-E1-043-08, TC-E1-043-09, TC-E1-043-10, TC-E1-043-11 | The whole legacy test set of RWB-E1-043, executed by RWB-P3-E1043-APP | RWB-E1-043 section 16 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | Executed by RWB-P3-E1043-APP |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1043-APP | App development | H consumer: implements the interface, the cache, the logger and the code set against this contract and its fakes |
| RWB-P3-E1043-APP, RWB-P3-E1043-CON | App development, Contract | C: the owning-service pair that keeps the tables, the registry, the read service and the load and approve operations, and owns the legacy acceptance criteria |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | Contract | Referred to by the app story: the parameters client and the catalog entry of the cache time to live; also the C rows behind the second consumed operation |
| RWB-PLT-E1072-CON, RWB-P7-E1073-CON | Contract | Referred to by the app story: the rules kit contract and the rwb-decision governance contract that own rule packages, which this client refuses |
| RWB-PLT-E1037-CON, RWB-P4-E1037-CON | Contract | Referred to by the app story: the access guard library and the authorise contract behind a permission failure |
| RWB-PLT-TE006-CON | Contract | Referred to by the app story: the outbox and inbox library, which carries no reference event |
| RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | Referred to by the app story: the naming library, the per-service Flyway baseline and the gateway-bff route |
| RWB-P1-DM014-APP | App development | C: extracts the versions, rows and lists of values and hands them to rwb-case through this contract; writes no reference row of its own; rule rows go to rwb-decision |

### 19. Out of scope

- The two versioned tables `reference_version` and `reference_row`, `lov_value`, the registry, the read service, the load and approve operations and the cache: rwb-case (P3), RWB-P3-E1043-APP and RWB-P3-E1043-CON.
- The rule packages, the rule registry and their load, validation, approval and rollback: rwb-decision (P7), RWB-P7-E1073 and the kit contract RWB-PLT-E1072-CON.
- The holiday calendar: ACE data under `v_ace_holiday`, read by rwb-source-data (P1); the contract serves none of it.
- The reference data screens SCR-39, SCR-40 and SCR-42: Epic 8.
- The permission matrix, its masking policy and the access guard library: RWB-E1-037 and P4 rwb-access.
- The library implementation, its cache, its logger and its tests: RWB-PLT-E1043-APP.
- The artefact coordinates and the publication channel of the library: the platform library baseline and RWB-PLT-TPL, recorded in GAP-1410 with ASM-2460.
