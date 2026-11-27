# RWB-P3-E1043-CON Reference data service with versioned tables - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1043-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-043 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP04, DP05, DP06, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E1043-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-008, FR-P3-012, FR-P3-026, FR-P3-030) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: delta slice split from RWB-E1-043 for rwb-case — the reference-data contract of record that the preserved story RWB-P3-E1043-APP implements. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (31 resolved, 93 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As **RW-REFADM, the reference data administrator**, I want **the contract of record for the versioned reference tables in `rwb_case` — the effective-dated read with `asOf`, the version-in-force rule, the list-of-values read, the load, verify, approve and rollback operations, the rwb-access authorise and DoA reads it consumes, the parameters reuse, the Flyway step and the fakes**, so that **the app story, the case, allocation and timer engines, the Drools evaluator and the other services build and test a dated, approved reference read on Day 1 without any of them reading `reference_version`, `reference_row` or `lov_value`**.

This is the contract slice of the delta of legacy RWB-E1-043, and it is the counterpart of the preserved story RWB-P3-E1043-APP, which keeps the legacy acceptance criteria AC1 to AC10 and the runtime behind them. The contract publishes, under the rwb-case base `/api/recovery/case/v1` (DP-13):

- The five operations of the reference-data surface, with their request shape, their answer, their error answers and their rights: the list read with the `asOf` business date, the load, the verify, the approve and the rollback (Ownership Map; ASM-0041).
- The version-in-force rule: the approved version with the latest valid from on or before the requested date, and nothing else (legacy section 8 BR3 and BR4).
- The three tables of the surface — `reference_row`, `reference_version` and `lov_value` — as P3 tables of `rwb_case`, and the sentence that the DoA table is not one of them (Ownership Map; ASM-0070; ASM-0071).
- The two consumed rwb-access operations of DP-08, the one consumed parameters operation of DP-06, and the Flyway step of DP-15.
- The fakes that the app story, the allocation and timer engines, the evaluator, the platform client of RWB-PLT-E1043-CON and the integration harness build against.

The contract serves no rule table and no holiday row. Rule packages are governed in rwb-decision (P7) through RWB-P7-E1073-CON and the embedded kit of DP-04, and the holiday calendar stays ACE data read through the P1 contract of `v_ace_holiday` (DP-05). The story has no build dependency, is Day 1 by rule and sits in the contract group CG-W1 (Template and Rules §R5.7).

### 2. Business rationale

The legacy module published `ReferenceVersionRegistry` and `ReferenceDataService` inside one application, so the shape of a reference read was never a contract: the version and its rows were in the same database and the caller was in the same process. After the split the tables sit in `rwb_case` (Ownership Map) and nineteen services read them across a service boundary, which means the effective-dated read, the refusal, the rights and the payload have to be agreed before any engine writes its start-up hook. Without that agreement each service invents its own projection or — worse — reads `reference_version` directly, which the schema-per-service rule forbids (DP-01).

**What this contract fixes, and what it leaves.** It fixes the operations and their answers, the version-in-force rule, the four admin operations and their rights, the three tables and their owners, and the fakes. It leaves the business values to the rows: the twelve table codes, their columns, bands, service levels, periods and limits stay data of a load, and no value appears in this document except the ones the legacy story and the technical specification carry.

**The DoA conflict, stated once.** Legacy AC2 and legacy section 8 BR1 load `DELEGATION_LIMIT` through the reference-data service. The Ownership Map ruling keeps `delegation_limit` with P4 rwb-access as the DoA table (ASM-0070) because Architecture v5 slides 14 and 41 give rwb-access the DoA table. The legacy acceptance criterion stays verbatim in RWB-P3-E1043-APP, and the target reading is this contract's: the reference surface of rwb-case serves eleven of the twelve codes, and a caller that needs a delegation limit reads the rwb-access DoA operation (GAP-0696; ASM-1243). Writing the ruling down here is cheaper than discovering it as a missing table in wave 1.

**The fakes are the Day-1 unblocker.** The first approved version of each table is loaded in SIT later in wave 1. With this document and its fakes, the app story, the engines, the evaluator and the platform client build and test the dated read on Day 1, and a drift test fails a build when an operation, a field or the refusal changes (Template and Rules §R5.4 class C). Every criterion below is new, tagged `(new, D-RCV-60)`, and tests only the contract deliverable.

### 3. Preconditions

- The service naming rules of Template and Rules §R4 are used unchanged: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` (namespace `rwb-recovery`), Java package: the service segment is ruled by the solution architect, because `case` is a Java reserved word and `th.co.scb.ace.workbench.recovery.case` does not compile; the ruled segment is Not specified in the source documents (CG-ALL-3751).
- The Ownership Map stands: `reference_row`, `reference_version` and `lov_value` are P3 tables of `rwb_case` (ASM-0071), and `delegation_limit` is a P4 table of `rwb_access` (ASM-0070).
- The legacy cutover extract travels one way: P1 reads the legacy cutover dump once and posts one file per Workbench-owned table code in the load shape of section 12.1; rwb-case owns the three tables, holds the content hash and the approver of a version, verifies and approves each version and serves it from `rwb_case`; the rule rows and their test cases stay in the rwb-decision registry and are not loaded by this story, and the four ACE lists are read only through the named views (GAP-2179).
- The five operations are the Ownership Map rows `GET /admin/lists/{listCode}`, `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/verify`, `POST /admin/reference-loads/{loadId}/approve` and `POST /admin/reference-loads/{loadId}/rollback`, all owner P3 (ASM-0041), read under the rwb-case base.
- The field identifiers DF-REF-159 to DF-REF-171, DF-REF-181 to DF-REF-184, DF-REF-028 and DF-REF-029 are taken from the Logical Data Model and Data Dictionary, character for character.
- The legacy message identifiers MSG-P3-027, MSG-P7-002, MSG-GEN-001, MSG-GEN-004 and MSG-P4-002 are used unchanged in the answers and the examples.
- The list LOV-REF-TABLE carries the twelve table codes of legacy section 8 BR1 and no rule table code; the non-DoA part of that list is served here (ASM-0070).
- The holiday calendar is ACE data under `v_ace_holiday`, read through the P1 contract and by no operation of this document (DP-05).
- The cache time to live is the legacy value `refdata.cache.ttl-seconds` = 300 (assumed; DL11), read as a catalog entry of the parameters contract RWB-P3-E1042-CON (DP-06).
- The platform client contract RWB-PLT-E1043-CON consumes the list read and the parameters read of this document; this document is their provider, and the platform library declares no operation of its own.
- No approval is required to publish a Draft contract: the surface is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.
- The contract version this story builds and publishes is v1: the document is published as v1, RWB-P3-E1043-APP and RWB-PLT-E1043-CON pin version 1, and a breaking change raises a new version (BR12; DOR-RWB-P3-E1043-CON-23).

### 4. Flow

1. The contract author writes the OpenAPI 3.1 document of the five operations, one tag per resource: Lists, Reference loads, Reference load approval, Reference load verification, Reference load rollback.
2. The author writes the effective-dated read: the `asOf` parameter, its default, the version-in-force rule of legacy section 8 BR3 and the refusal when no version applies.
3. The author writes the four admin operations with the legacy request, answer and error rows, with `Idempotency-Key` on every POST and with the rights resolved on the rwb-access authorise operation.
4. The author writes the table section: the three P3 tables of `rwb_case`, their keys and indexes, and the sentence that `delegation_limit` is a P4 table that this contract never names as its own.
5. The author writes the difference from the legacy contract: the authorise and DoA reads consumed, the parameters reuse, the Flyway step and the absence of a reference-data event.
6. The lint and schema steps run: OpenAPI 3.1 validation, the sibling-file rule, the operation-id rule, the error-envelope rule, `Idempotency-Key` on every POST, the base-path rule and the table-owner rule.
7. The fakes are generated from the document: the version in force, the no-version refusal, the four admin answers and the two rwb-access answers.
8. The document and the fakes are published, the app story and the platform client pin the version, and a drift test in this story refuses any difference between a fake and section 12.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An operation is published without a 4xx error envelope, or a POST without `Idempotency-Key` | The lint step fails the build and the document is not published | Lint finding, no message id | AC4 |
| X2 | A path is published outside `/api/recovery/case/v1`, or another service's operation is declared as provided | The lint step fails the build | Lint finding, no message id | AC7 |
| X3 | A read asks for a table code with no approved version in force for the requested date | The read is refused; no older version, no default row and no empty list is returned | MSG-P3-027 | AC2 |
| X4 | The author of a load approves it | The approval is refused and the version stays VALIDATED | MSG-P7-002 | AC4 |
| X5 | A role without the right calls a load, a verify, an approval or a rollback | The call is refused and nothing changes | MSG-P4-002 | AC5 |
| X6 | `delegation_limit`, a rule table or a holiday row appears in the document as a table of this service | The table-owner lint fails the build; the DoA table stays with P4 and the holiday calendar with ACE | Lint finding, no message id | AC1 |
| X7 | A field-level detail of the reference resources is missing from the source material | The element carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | Not specified in the source documents (GAP-0697; ASM-1244) | AC7 |
| X8 | A fake drifts from the document | The drift test fails the build | Lint finding, no message id | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and fakes; builds against the platform naming and error baselines only and starts on Day 1 |
| Negotiable | The element order inside an answer, the example values and the fake fixture set are open until the version is frozen; the operations, the version rule, the refusal and the rights are fixed |
| Valuable | The app story, three engines, the evaluator, the platform client and the harness build and test the dated read before an approved version exists |
| Estimable | Five provided operations, three consumed operations, three tables, nine sub-tables and four fakes |
| Small | One sprint for the documents, the fakes and the drift test |
| Testable | Each criterion below is one schema, lint or fake assertion in section 16, never a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: rwb-case reference-data contract of record

  Background:
    Given the rwb-case base path is /api/recovery/case/v1, the schema is rwb_case and the contract version is v1
    Given reference_row, reference_version and lov_value are P3 tables of rwb_case and delegation_limit is a P4 table of rwb_access

  Scenario: AC1 The three tables and the twelve codes are fixed with their owners (new, D-RCV-60)
    Given the table section of the contract
    When it is checked against the Ownership Map
    Then reference_row, reference_version and lov_value are named as P3 tables of rwb_case and no other table is named as this service's
    Then delegation_limit is named as a P4 rwb-access table and no operation of the contract reads or writes it
    Then no rule table, no rule package and no holiday row appears as an element of the contract
    Then the twelve LOV-REF-TABLE codes of legacy section 8 BR1 are listed, eleven of them are served here and DELEGATION_LIMIT is answered by the rwb-access DoA operation

  Scenario: AC2 The effective-dated read and the version-in-force rule are fixed (new, D-RCV-60)
    Given GET /api/recovery/case/v1/admin/lists/{listCode} with the optional asOf business date
    When the document is validated
    Then the read answers the approved version with the latest valid from on or before asOf, with its version number, valid from, valid to and rows
    Then asOf defaults to the business date of the service and never to the latest version
    Then a read whose date has no approved version in force answers 404 naming the table code and the date and carrying MSG-P3-027, and never an older version, a default row or an empty list
    Then the same refusal is answered for a date before the first approved valid from and for a table code with no version at all
    Then no answer carries a customer identifier and no answer carries a rule row

  Scenario: AC3 One operation serves the list of values and the reference table (new, D-RCV-60)
    Given GET /api/recovery/case/v1/admin/lists/{listCode} for a LOV code and for a reference table code
    When the document is validated
    Then a LOV code answers its values in force with the list code, the value code and the version applied, matching DF-REF-028 and DF-REF-029
    Then a reference table code answers the version in force with its row key and row data, matching DF-REF-183 and DF-REF-184
    Then one operation serves both, so the platform client of RWB-PLT-E1043-CON reads a list with its versions in one hop
    Then an unknown list code answers 404 and a role without Reference data R answers 403 with MSG-P4-002

  Scenario: AC4 The four admin operations are the contract of record (new, D-RCV-60)
    Given POST /admin/reference-loads, POST /admin/reference-loads/{loadId}/verify, POST /admin/reference-loads/{loadId}/approve and POST /admin/reference-loads/{loadId}/rollback
    When the document is validated
    Then the load takes multipart/form-data with file, table and validFrom, requires Idempotency-Key and answers 201 with the load id, table, valid from, status VALIDATED and row count
    Then the verify answers the check result per row and column of the validated load and changes no version number and no row
    Then the approve answers 200 with the approver and the approval time, and answers 409 with MSG-P7-002 when the approver is the author
    Then the rollback answers the version set to ROLLED_BACK with its reason and names the version in force for the business date
    Then every operation answers 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-P3-027 or MSG-GEN-001 and 503
    Then a repeat load with the same table, valid from and content hash returns the first load and writes nothing

  Scenario: AC5 The authorise check and the DoA read are consumed, not provided (new, D-RCV-60)
    Given the two rwb-access operations of section 12.2 and the contract dependency RWB-P4-E1037-CON
    When the rights of the five operations are reviewed
    Then Reference data C, U, A and R are resolved on POST /api/recovery/access/v1/authorise for every operation and never from a local role list
    Then the delegation limit an approval needs is read from GET /api/recovery/access/v1/doa-limits and no column of delegation_limit is named as this service's
    Then a role without the right is refused with MSG-P4-002 and nothing changes
    Then each call is one hop with a 2 s timeout and a breaker, and this contract publishes no role, scope or DoA operation

  Scenario: AC6 The parameters reuse, the Flyway step and the topic rule are fixed (new, D-RCV-60)
    Given the parameters contract RWB-P3-E1042-CON, the Flyway baseline RWB-PLT-E1044-CON and the naming library RWB-PLT-E1047-CON
    When the document is validated
    Then refdata.cache.ttl-seconds and the list of reference table codes are read as catalog entries of GET /api/recovery/case/v1/admin/parameters and never as code constants
    Then the three tables arrive on the rwb-case Flyway sequence in rwb_case, and the contract declares no baseline and no migration of another schema
    Then the contract declares no event on rwb.case.events.v1, because the Arch v5 catalogue carries no reference-data event and no consumer waits for one
    Then the topic rwb.case.events.v1 and the event-name form rwb.case.<Event>.v1 are quoted from the naming library and no topic outside that form appears

  Scenario: AC7 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section and the fakes of section 12.8
    When the nine sub-tables are reviewed and the contract test runs
    Then each of 12.1 to 12.9 is present, and an empty one says None with one sentence
    Then every operation sits under /api/recovery/case/v1 and every table and every operation names its owner from the Ownership Map
    Then the fakes answer the version in force, the no-version refusal, the 403 with MSG-P4-002, the author-approves refusal and the cache time to live
    Then a drift between a fake and this document fails the contract test
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is copied here — AC1 to AC10 of RWB-E1-043 stay with RWB-P3-E1043-APP — and every number, identifier, message and code comes from the legacy story, the Ownership Map or Architecture v5, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract serves the reference tables of rwb-case only: `reference_row`, `reference_version` and `lov_value` in `rwb_case`, and no table of another service | Ownership Map; DP-01 |
| BR2 | The version in force on a requested date is the approved version with the latest valid from on or before that date, and the chosen version number travels in the answer | Legacy section 8 BR3 (R-UNI-38) |
| BR3 | Only an APPROVED version is served; VALIDATED and ROLLED_BACK are never served, and a missing version is a refusal with MSG-P3-027 and never a default | Legacy section 8 BR9, section 17; Principle 5; NFR-033 |
| BR4 | A version takes effect only after an approver who is not the author approves it; the approve right is resolved on the rwb-access authorise operation | Legacy section 8 BR4 (CTL-08); DP-08 |
| BR5 | A load with any failed check is refused in full, and a repeat load of the same table, valid from and content hash writes nothing | Legacy section 8 BR5, AC7 |
| BR6 | A valid from date before the business date is refused, and an open case keeps the version it was decided under | Legacy section 8 BR6 (R-UNI-38) |
| BR7 | The DoA table is not served here: `delegation_limit` is a P4 rwb-access table and a delegation limit is read from the rwb-access DoA operation | ASM-0070; Architecture v5 slides 14 and 41 |
| BR8 | The holiday calendar is not served: it is ACE data under `v_ace_holiday`, read through the P1 contract | Legacy section 2 and section 12; DP-05 |
| BR9 | The cache time to live and the table-code list are catalog entries of the parameters contract, never code constants; the legacy value is 300 (assumed; DL11; assumptions ASM-0553, ASM-0703, ASM-1051, ASM-1104) | DP-06; legacy section 13 |
| BR10 | No event reaches a consumer for a version change: the legacy design publishes none, the Arch v5 catalogue gives rwb-case no reference-data event, and the refresh is the cache expiry | Architecture v5 slide 14; legacy section 12 |
| BR11 | One REST base and one topic per service: this contract declares `/api/recovery/case/v1` as provided and quotes `rwb.case.events.v1` without publishing an event on it | DP-13; DP-14 |
| BR12 | A breaking change raises a new contract version and deprecates the old one; an operation or a field is never edited in place | Template and Rules §R7.2; §R5.4 class C |
| BR13 | A dated read with no approved version in force answers 404 with MSG-P3-027 naming the table code and the date, and never an older version, a default row or an empty list | Legacy section 12 (MSG-P3-003 and MSG-P3-027 rows); Principle 5; NFR-033 |
| BR14 | The verify and the rollback operations of a reference load require the Reference data A right, as the legacy story gives the approval; the separation of duty of section 10 is unchanged | Legacy section 10 (Reference data C, A and R); Ownership Map |

### 9. State transitions

None in this story: a document has no runtime state. The states the document describes are the reference-version states of RWB-P3-E1043-APP section 9 (VALIDATED, APPROVED, ROLLED_BACK, with a refused load never written), and this story fixes the answer that accompanies each one.

| From | Event | Answer of the contract | Status |
|---|---|---|---|
| None | Load received, every check passes | 201 with status VALIDATED and the row count | VALIDATED |
| None | Load received, any check fails | 422 with MSG-P3-027 naming the row and the column, or MSG-GEN-001 for an empty file; nothing written | Refused |
| VALIDATED | Verification recorded | 200 with the check result per row and column; no state change | VALIDATED |
| VALIDATED | Approval by someone other than the author | 200 with the approver and the approval time | APPROVED |
| VALIDATED | Approval by the author | 409 with MSG-P7-002; the version stays VALIDATED | VALIDATED |
| APPROVED | Approval of the same version again | 200 with the same body and no change | APPROVED |
| APPROVED | Rollback with a reason | 200 with the version set to ROLLED_BACK and the version in force for the date | ROLLED_BACK |

The legacy `status` vocabulary of three values is what the read returns. The list LOV-VERSION-STATUS of the technical specification carries the wider set LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED (TSD P3 v3 T3.2), and the values outside the legacy three are never returned by the reference read of this contract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fakes |
| The service owner of rwb-case (P3) | Approves a breaking change and freezes a version |
| The app story RWB-P3-E1043-APP and the platform client RWB-PLT-E1043-CON | Consume the document, pin the version and raise a change request rather than a private variant |
| The allocation, timer and case engines and the Drools evaluator (SY-RULES) | Read the version in force through the document; they have no right in it |
| The rwb-access owner (P4) | Owns the authorise and DoA operations this document consumes, and confirms the rights of the five operations |
| The rwb-decision owner (P7) | Confirms that rule packages and the registry are outside this contract |
| RW-REFADM, RW-COE, RW-RISK, RW-AUDIT | Load, verify, approve, roll back and read through the operations; their rights are resolved by rwb-access |
| RW-PLATADM | Receives the alert an engine raises when no version is in force |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no e-mail address and no credential appears in a document, a schema, an example or a fake; where a caller must be named, the example uses a user identifier such as `U-REF-01` or a role code only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Field identifiers published | DF-REF-159 to DF-REF-171 (reference_version), DF-REF-181 to DF-REF-184 (reference_row), DF-REF-028 and DF-REF-029 (lov_value) | BR1 |
| Field identifiers not published | The `delegation_limit` columns of rwb-access: reached over the rwb-access DoA operation, never in this document (ASM-0070) | BR7 |
| Version projection | Table code, version number, valid from, valid to, status, author, approver, approved at, row count, content hash, load identifier | BR2 |
| Row projection | Row key and row data, as DF-REF-183 and DF-REF-184 carry them | BR1 |
| Example values | EXPOSURE_BAND versions 3 and 4 with bands "E1" to "E5", QUEUE version 7, SERVICE_LEVEL version 2, LEGAL_PERIOD versions 1 and 2, REGION with content hash "a1b2", the user identifiers "U-REF-01", "U-RSK-01" and "U-RSK-02", all from the legacy story | BR2 |
| Personal data | None. No name, no e-mail address, no account number and no national identifier in an example or a fake | Not specified in the source documents (DOR-RWB-P3-E1043-CON-7) |
| Load file | CSV or XLSX with one sheet, sent as multipart on the load operation; the column definitions per reference table code are Not specified in the source documents (GAP-0697; ASM-1244) | BR5 |
| Cache | One entry per table code and business date; the time to live is the catalog entry `refdata.cache.ttl-seconds` at 300 (assumed; DL11), refreshed on expiry only because no change event is published | BR9 |

The contract carries no business value of its own: the twelve codes, the bands, the service levels, the legal periods and the original date are the values the legacy story names, and every other value is a row of a load. The column definitions each table code needs — the required columns, their types and their key columns — have no source field by field, so the load operation carries them as data beside LOV-REF-TABLE and this document names the behaviour, not the columns (GAP-0697; ASM-1244).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Request | Answers | Owner |
|---|---|---|---|
| `GET /api/recovery/case/v1/admin/lists/{listCode}` | Path list code, for example LOV-REF-TABLE; optional `asOf` business date | 200 with the list values, or for a reference table code the approved version in force with its rows; 401; 403 MSG-P4-002; 404 MSG-P3-027 when no version is in force; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads` | `multipart/form-data`: `file`, `table`, `validFrom`; `Idempotency-Key` | 201 with the load id, table, valid from, status VALIDATED and row count; 401; 403 MSG-P4-002; 409 when an approved version has this valid from; 413; 422 MSG-P3-027 or MSG-GEN-001; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/verify` | Path load id; verifier and note | 200 with the check result per row and column of the validated load; 401; 403 MSG-P4-002; 404 unknown load with MSG-P4-003; 409 when the version changed since it was read with MSG-GEN-004; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | Path load id | 200 with the approved load, its approver and the approval time; 401; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P7-002 when the approver is the author, or MSG-GEN-004 when the version changed; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | Path load id; reason | 200 with the version set to ROLLED_BACK and the version in force for the business date; 401; 403 MSG-P4-002; 404 MSG-P4-003; 409 when the version is not APPROVED; 422 an empty reason; 503 | P3 |

The four admin operations are the legacy load and approve operations moved to this service (ASM-0041), with the verify operation of the same ruling and the rollback of legacy section 9. The refusal of a dated read carries the status 404 because the requested dated representation does not exist; the legacy story fixes the message but not the status (GAP-0698; ASM-1245). The rights of the verify and of the rollback are not stated by any source and are taken as Reference data A, the right the legacy story gives the approval (GAP-0698; ASM-1245).

#### 12.2 REST operations consumed

| Operation | Provider | Use in the contract | Pattern |
|---|---|---|---|
| `POST /api/recovery/access/v1/authorise` | P4 rwb-access (RWB-P4-E1037-CON) | The Reference data C, U, A and R right of the five operations | DP-08, DP-11 |
| `GET /api/recovery/access/v1/doa-limits` | P4 rwb-access (RWB-P4-E1037-CON) | The delegation limit an approval needs; this service holds no DoA table | DP-08, DP-11 |
| `GET /api/recovery/case/v1/admin/parameters` | P3 rwb-case (RWB-P3-E1042-CON) | `refdata.cache.ttl-seconds` and the list of reference table codes | DP-06, DP-11 |

Every call is one hop with a 2 s timeout and a breaker per provider (DP-11, ADR-020). The DoA operation is the target reading of legacy AC2: the reference surface of rwb-case does not hold `delegation_limit` (ASM-0070; GAP-0696; ASM-1243).

#### 12.3 Events published

None. The Arch v5 catalogue gives rwb-case the topic `rwb.case.events.v1` with CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged and TimerBreached (Architecture v5 slide 14), and no reference-data event exists in that catalogue; this contract therefore declares none and adds none, so the topic name and the event-name form are quoted and not extended (DP-14).

#### 12.4 Events consumed

None. A new approved version reaches a consumer at its next cache expiry, and no source declares an event for a version change; an owner event added later would arrive through the inbox library of RWB-PLT-TE006-CON (DP-09) and would raise a new contract version.

#### 12.5 Workflows and activities

None. A load, a verify, an approval and a rollback are one synchronous transaction each on the `rwb-case` task queue's service and not in a workflow, and a read is a cached read; the contract declares no workflow, no activity and no task queue of its own.

#### 12.6 Schedules

None. No Temporal Schedule and no job is declared: the refresh is the cache expiry, the loads are operator actions, and the 00:01 rule promotion and the six-monthly access review belong to other owners.

#### 12.7 Tables owned

| Table | Schema | Key and indexes | Owner | Exposed by |
|---|---|---|---|---|
| reference_version | rwb_case | PK id; unique on table_code and version_no; unique on table_code, valid_from and content_hash; partial unique index on table_code, valid_from where status is APPROVED | P3 | The load, verify, approve and rollback answers; the version list of the list read |
| reference_row | rwb_case | PK id; version_id to reference_version; unique on version_id and row_key; index on version_id | P3 | The rows of the version in force in the list read |
| lov_value | rwb_case | PK id; unique on lov_code and value_code | P3 | The list read of a LOV code |

`delegation_limit` is not in this list: it is the P4 rwb-access DoA table (ASM-0070), read through the operation of section 12.2. `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 rwb-decision tables and appear nowhere in this document (DP-04). The three tables arrive on the rwb-case Flyway sequence after the V0001 baseline (DP-15; RWB-PLT-E1044-CON), and this contract declares no migration.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-case reference-data fake (this story) | The five provided operations: the version in force for a date, the rows of that version, the no-version refusal with MSG-P3-027, and the load, verify, approve and rollback answers with their error codes | RWB-P3-E1043-APP, the engines, the evaluator, RWB-PLT-E1043-CON and the integration harness |
| rwb-access WireMock | `POST /authorise` granting Reference data C, U, A and R to RW-REFADM, RW-COE and RW-RISK and refusing with MSG-P4-002; `GET /doa-limits` with the DoA rows | The rights of the five operations and the DoA reading of AC5 |
| rwb-case parameters fake (RWB-P3-E1042-CON) | `GET /admin/parameters` with `refdata.cache.ttl-seconds` at 300 and the eleven table codes without DELEGATION_LIMIT | The cache and the code check of AC6 |
| Drift and lint test assets (this story) | The assertions that compare each fake, each path and each table owner with section 12 | The contract test of section 16 and every consuming build |

The reference-data fake answers from fixtures and not from copied production payloads, and it carries user identifiers and role codes only. A consumer that needs a delegation limit is answered by the rwb-access fake, not by this one.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 5 operations under `/api/recovery/case/v1` | 3 operations over 2 providers | OpenAPI 3.1, one hop, 2 s timeout and a breaker, `Idempotency-Key` on every POST |
| Kafka | 0 | 0 | No reference-data event exists; the topic of the service is quoted, not extended |
| Temporal | 0 | 0 | The operations are synchronous and no activity is declared |
| File | 0 | 1 | The load file of the load operation (CSV or XLSX, one sheet); no runtime file exchange |

### 13. Solution plan

**Deliverables.** `openapi/lists.yaml` (the effective-dated list read, its `asOf` parameter and its refusal), `openapi/reference-loads.yaml` (the four admin operations with their error codes and the `Idempotency-Key` rule), `reference-data-tables.md` (the three tables, their keys and indexes and the DoA exclusion), `reference-data-consumed.md` (the three consumed operations and the 2 s budget), and the four fake assets of section 12.8 with the drift and lint test.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| lists.yaml | Document | The list read, the `asOf` parameter, the version-in-force answer and the 404 refusal (AC2, AC3) |
| reference-loads.yaml | Document | The load, verify, approve and rollback operations with their answers and rights (AC4) |
| reference-data-tables.md | Document | The three P3 tables, their keys and the DoA exclusion (AC1, AC7) |
| reference-data-consumed.md | Document | The two rwb-access operations and the parameters operation, with the 2 s budget (AC5, AC6) |
| Fake assets | Test asset | The version in force, the refusal, the admin answers and the two owner answers (AC7) |
| Drift and lint rules | Test asset | Base-path, operation-id, `Idempotency-Key`, table-owner, error-envelope and drift assertions (AC1 to AC7) |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract names the three tables of `rwb_case` and no table of `rwb_access`, which is the schema of rwb-access and is read only through its operations | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision. The contract serves no rule package and no rule row | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. The holiday calendar is excluded and read through the P1 contract | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. The cache time to live and the table-code list are catalog entries | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. This document is that contract, and it is what the other services and the platform client consume through GET /api/recovery/case/v1/admin/lists/{listCode} | H RWB-PLT-E1043-CON; this key's own contract |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. The four rights are resolved there, and the DoA limit is read there | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. No event is declared, and an owner event added later arrives through the inbox library | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The legacy in-process interface becomes the published read, and its fake is Day-1 work | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The five operations sit under `/api/recovery/case/v1` and the lint refuses any other base | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The contract quotes `rwb.case.events.v1` and `rwb.case.<Event>.v1` and publishes no event | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The three tables arrive on the rwb-case sequence, and the contract declares no migration | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. The reference data screens of Epic 8 reach the read through gateway-bff; the contract declares no route | H RWB-PLT-N001-CON |

Build runs against the fakes of the contracts DP-03, DP-07, DP-09, DP-10 and DP-19 add until each publishes; the plan lists in the header stay as they stand.

The two consumed contract rows C RWB-P3-E1018-CON and C RWB-P4-E1037-CON never block: they are class-C dependencies with a published fake each, so the work they cover is buildable from Day 1 against the two fakes and no build waits for their providers (GAP-2335).

**Build steps**

1. Write `lists.yaml` with the `asOf` parameter, the version-in-force answer and the 404 refusal with MSG-P3-027 (AC2, AC3).
2. Write `reference-loads.yaml` with the four admin operations, their answers, the `Idempotency-Key` rule and the rights of section 12.1 (AC4).
3. Write `reference-data-tables.md` with the three tables, their keys and the two exclusions — the DoA table and the rule tables (AC1, AC7).
4. Write `reference-data-consumed.md` with the two rwb-access operations and the parameters operation, each with the 2 s budget (AC5, AC6).
5. Add the lint rules: base path, operation id, `Idempotency-Key` on every POST, error envelope, table owner and no path of another service (AC1 to AC7).
6. Generate the four fake assets from the documents and write the drift test that compares each fake with section 12 (AC7).
7. Publish v1, notify RWB-P3-E1043-APP and RWB-PLT-E1043-CON, and record the pinned version.
8. Agree the column definitions per table code with the reference data administrator and hand them to the app story as data, not as schema (GAP-0697; ASM-1244).

**Done when.** Both documents validate and pass every lint rule, the four fake assets answer every operation, the drift test is green here and in the app story, and the app story and the platform client have pinned version 1.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A load check fails, the valid from is before the business date, or no approved version is in force for the requested date | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P7-002 | The author of a load approves it | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | The load file has no data rows | Enter {field}. |
| MSG-GEN-004 | Two approvals of one version at once, or the version changed since it was read | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without the right calls a load, a verify, an approval, a rollback or the list read | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Named as an error code by section 12.1 as the as-built contract of RWB-P3-E1043-APP names it | Not specified in the source documents (DOR-RWB-P3-E1043-CON-9) |

The texts are the legacy ones, character for character, and Thai text for each follows DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863). MSG-P4-001 and MSG-P4-003 are named as error codes by section 12.1 exactly as the as-built contract of RWB-P3-E1043-APP names them; their texts are not in the source material and this contract adds no text of its own.

### 15. Screens and states

None in this story. The contract serves the version list and the load result that SCR-39, SCR-40 and SCR-42 show in Epic 8, and those screens reach the operations through the gateway-bff composite route (DP-19). Until those screens exist the reference data administrator loads files through the operation, and the load result is returned in the answer and listed in the daily data quality report (RWB-E1-011).

SCR-39: empty, loading, error and no access states: Not specified in the source documents (CG-ALL-3752). SCR-40: empty, loading, error and no access states: Not specified in the source documents (CG-ALL-3753). SCR-42: empty, loading, error and no access states: Not specified in the source documents (CG-ALL-3754).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1043-CON-01 | AC1, BR1, BR7 | Contract | The three P3 tables and the twelve codes compared with the Ownership Map; `delegation_limit` absent and answered by rwb-access; no rule or holiday element |
| TC-P3-E1043-CON-02 | AC2, BR2, BR3, BR6 | Contract | The list read at 2026-11-30, at 2026-12-01, before the first valid from and with no version in force; the 404 and MSG-P3-027 |
| TC-P3-E1043-CON-03 | AC3, BR3 | Contract | A LOV code and a reference table code answered by one operation; an unknown list code; a role without Reference data R |
| TC-P3-E1043-CON-04 | AC4, BR4, BR5 | Contract | The four admin operations with 201, 200, 404, 409 for an author approving, 422, and the repeat load with the same hash |
| TC-P3-E1043-CON-05 | AC5, BR4, BR7 | Component | The authorise answers C, U, A and R and the refusal with MSG-P4-002; the DoA read; the 2 s budget and the breaker |
| TC-P3-E1043-CON-06 | AC6, BR9, BR10, BR11 | Contract | The parameters entry at 300; the Flyway step in `rwb_case`; the absence of a reference-data event; the topic and event names |
| TC-P3-E1043-CON-07 | AC7, BR12 | Component | The nine sub-tables complete; the four fake assets; a deliberate drift between a fake and the document |
| TC-P3-E1043-CON-08 | ASM-3438 | Contract | Boundary values of the key and index columns of the three tables in section 12.7 (ASM-3438) |
| TC-P3-E1043-CON-09 | AC8, BR8 | Contract | The table section and the consumed operations checked against the Ownership Map; no holiday table and no `v_ace_holiday` operation of this contract; the calendar read only through the P1 contract |

### 17. Guardrails

- No business value in the contract: codes, columns, bands, service levels, periods and limits are rows of a load, and the only number this document fixes is the documented default 300 of the cache time to live.
- No personal data in an example, a fake or a log: user identifiers and role codes only, and no customer identifier in any answer.
- The contract names rwb-case tables and rwb-case operations as provided, and the three consumed operations as consumed; it never restates another service's operation as its own (DP-01, DP-13).
- `delegation_limit` is a P4 rwb-access table and appears here only as a consumed read; a document that declares it as this service's table fails the table-owner lint (ASM-0070).
- No rule table, no rule package and no holiday row appears as an element of the contract (DP-04, DP-05).
- Only an APPROVED version is served, and a missing version is a refusal with MSG-P3-027, never a default value, an older version or an empty list.
- Every POST carries `Idempotency-Key`, and a repeat load with the same hash writes nothing.
- No event is invented for a version change; the topic of the service is quoted and not extended, and an owner event added later arrives through the inbox library and a new contract version.
- The contract is versioned: a breaking change raises a new version and deprecates the old one in place of editing it.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-011 | Reference data service with versioned tables, valid from and to, author and approver | The five operations, the version-in-force rule, the three tables and the refusal | TC-P3-E1043-CON-01, TC-P3-E1043-CON-02, TC-P3-E1043-CON-04 |
| REQ-CWC-006 | Roles, teams, queues and capacity as versioned reference data | The list read of a reference table code and its version, and the QUEUE and SERVICE_LEVEL codes of the examples | TC-P3-E1043-CON-01, TC-P3-E1043-CON-03 |
| REQ-CWC-016 | Every engine logs the table code and version of every table it reads | The version number and table code that travel in every read answer | TC-P3-E1043-CON-02, TC-P3-E1043-CON-03 |
| ADR-012 | Versioned reference data with valid from, author and approver; rule packages separate | The status vocabulary, the four-eyes approval and the rule-table exclusion | TC-P3-E1043-CON-01, TC-P3-E1043-CON-04 |
| ADR-014 | Schema and login per service in ACE PostgreSQL | The three tables of `rwb_case` and the DoA exclusion | TC-P3-E1043-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed operations with the 2 s client budget and the breaker | TC-P3-E1043-CON-05 |
| D-RCV-36 T3, T4, T8 | Reference tables and rule packages governed separately | The rule-table and rule-package exclusions of section 12.7 | TC-P3-E1043-CON-01 |
| ASM-0070 | `delegation_limit` is the P4 DoA table | The consumed DoA read and the DoA exclusion of section 12.7 | TC-P3-E1043-CON-01, TC-P3-E1043-CON-05 |
| ASM-0041 | The list and reference-load paths are rwb-case operations | The five provided operations and their base path | TC-P3-E1043-CON-04 |
| ASM-3438 | Not specified in the source documents (DOR-RWB-P3-E1043-CON-12) | The tables of section 12.7 and their boundary values | TC-P3-E1043-CON-08 |

The legacy test set TC-E1-043-01 to TC-E1-043-11 is executed by RWB-P3-E1043-APP and is not copied here.

### 19. Out of scope

- The runtime of the five operations — the registry, the read service, the cache, the logger and the migration (RWB-P3-E1043-APP).
- The legacy acceptance criteria AC1 to AC10 and the legacy test cases TC-E1-043-01 to TC-E1-043-11 (RWB-P3-E1043-APP).
- The reference-data client library that the other services compile against (RWB-PLT-E1043-CON; RWB-PLT-E1043-APP).
- The rule packages, their registry, their load, approval and rollback, and the embedded kit (P7 rwb-decision; RWB-P7-E1073-CON; RWB-PLT-E1072-CON).
- The authorise, role, scope, masking and DoA resources of rwb-access (P4 rwb-access; RWB-P4-E1037-CON; RWB-E1-038).
- The holiday calendar: ACE data under `v_ace_holiday`, read by rwb-source-data (P1).
- The reference data screens SCR-39, SCR-40 and SCR-42 (Epic 8) and their gateway-bff route (RWB-PLT-N001-CON).
- The column definitions of the twelve table codes as a field-by-field schema (GAP-0697; ASM-1244) and the status of the dated read and the rights of the verify and the rollback (GAP-0698; ASM-1245).
