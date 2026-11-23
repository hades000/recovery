# RWB-P3-E1031-CON Queue and owner on the case list with filters

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1031-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-009, FR-P3-011) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-031 and published as the rwb-case contract baseline of the case list and its export. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract of the rwb-case case list and its export - `GET /api/recovery/case/v1/cases` with the queue, team and status filters and the queue and owner columns, and `GET /api/recovery/case/v1/cases/export` with its row limit, its access-log entry and its masked workbook - together with the row and page shape, the filter set and the AND rule, the stable order, the error envelope and its message codes, the right each answer requires, the 2 s one-hop budget, the nine contract tables and the contract fakes**, so that **the app, test and gateway stories build on Day 1 against a fixed, testable contract, and a column, a filter or a refusal can never drift between rwb-case, the composite route and the screen**.

The legacy key is split with rework, not moved: the two operations keep their behaviour, their filters, their messages and their values, and this story adds the contract form of them. The owner is rwb-case, the base is its own, and the right, the scope, the masking rules and the access log are consumed from rwb-access and never republished here (DP-08, DP-11).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The case list is the most-read surface of rwb-case, and the route merges its answers with those of other services (DP-19). Four things drift silently without a contract: the row fields and the blank owner of AC7, the filter set with the team filter the legacy flow uses, the paging and order that make "page 2" mean the same to two readers, and the order between the access-log entry and the file.

The baseline also fixes the naming the checks require: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, task queue `rwb-case` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.case`. It records that the two answers are reads, that no operation of this contract writes, and that the only write on the export path is the access-log entry of rwb-access (DP-09 not applied).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path and the schema name follow the platform rule and not a local choice.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); this document narrows the first for its two operations and publishes no event schema.
- The parameters contract of rwb-case (RWB-P3-E1042-CON, DP-06) and its reference-data contract (RWB-P3-E1043-CON, DP-07) are published, so `caselist.export.maxrows` and LOV-CASE-STATUS and LOV-TEAM are declared as data and never as values in this document.
- The rwb-access authorise and access-log contracts (RWB-P4-E1037-CON, RWB-P4-E1039-CON) are the consumed answers; this document names them and republishes nothing of them (DP-08, DP-11).
- The Ownership Map gives `GET /cases` and `GET /cases/export` to P3 rwb-case; this document declares no other service's operation as provided.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. The contract author writes the OpenAPI 3.1 document `caselist.yaml` for the two read operations, one tag `Case list`.
2. The author fixes the row shape `CaseListRow` from the legacy `Case` fields, with `ownerUserId` optional and `queueCode` and `queueName` beside `queueId`.
3. The author fixes the filter set `queue`, `team`, `status`, `owner`, `product`, `stage` and the AND rule, and states the team filter as an additive optional parameter (ASM-3624).
4. The author fixes paging `page` and `size` with `total`, the default and maximum size read as parameter rows, and the order that ends on the case number.
5. The author fixes the export: the same filters without paging, the spreadsheet content type, the 422 above the row limit and the 503 when the access-log entry cannot be written, and states that the entry precedes the file.
6. The author records the two consumed operations of rwb-access with their use, the 2 s budget and the message ids of the 403 and the 503, and the masking rule that travels in the authorise answer.
7. The lint, schema and example steps run; the fake is generated from the document and answers every operation and every example of section 14.
8. The document and the fake are published; RWB-P3-E1031-APP, RWB-P3-E2033-APP, RWB-P3-E2011-APP, the gateway-bff stories and RWB-ITG-E1031-ITG pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message |
|---|---|---|---|
| X1 | An operation is published without a 4xx error envelope | The lint step fails the build and the document is not published | Lint finding, no message id |
| X2 | A path is published outside `/api/recovery/case/v1` | The lint step fails the build; the monolith base is never republished | Lint finding, no message id |
| X3 | The row schema adds a field no source defines | The field is not invented: the example carries the placeholder and the gap row is cited | GAP-2209 |
| X4 | An example carries a personal name, an account number or an identity number | The review step rejects the example; only user references and case numbers appear | Review finding |
| X5 | A filter is published without its list in force | The lint step fails: every enumerated value names its LOV or its parameter row | Lint finding, no message id |
| X6 | A consumer needs a filter or a column the legacy story does not fix | The change is raised as a request against v2; v1 is not edited in place | Review finding |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and a fake; builds nothing and depends on no build |
| Negotiable | Field order, example values and the detail layout of the problem body are open until the version is frozen |
| Valuable | The app, the queue views, the gateway and the integration harness start on Day 1 against one document and one fake |
| Estimable | Two operations, one row schema, one page envelope, four message ids, nine tables, one fake |
| Small | One sprint for the document, the fake and the contract test |
| Testable | Each criterion is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: rwb-case contract baseline for the case list and its export

  Background:
    Given the rwb-case base path is /api/recovery/case/v1 and the schema is rwb_case
    Given the contract version is v1

  Scenario: AC1 The case-list operation is published with its owner (new, D-RCV-60)
    Given the OpenAPI 3.1 document for the Case list tag
    When it is validated and linted
    Then it declares GET /cases and GET /cases/export under /api/recovery/case/v1
    Then every operation names rwb-case (P3) as its owner and declares no operation of rwb-access
    Then GET /cases answers 200, 401, 403, 422 and 503

  Scenario: AC2 The row shape and the owner column are fixed (new, D-RCV-60)
    Given the schema CaseListRow
    When it is compared with the DF-CAS fields published in section 11 and with DF-WRK-001 to DF-WRK-004
    Then it carries caseNo, productGroup, status, stageCode, queueId, queueCode, queueName, ownerUserId, teamCode, regionCode and entryDate
    Then ownerUserId is optional, so a case with no owner is one row with the field absent and never a missing row
    Then no field carries a customer name, an identity number, an address or an account number

  Scenario: AC3 The filter set and the AND rule are published (new, D-RCV-60)
    Given the parameters of GET /cases and GET /cases/export
    When the document is validated
    Then both operations carry queue, team, status, owner, product and stage
    Then the team parameter is optional and additive on GET /cases, as the legacy flow and the export operation state it
    Then every enumerated filter names its list in force: LOV-CASE-STATUS for status, the queues in force for queue, LOV-PRODUCT for product, LOV-STAGE for stage
    Then the description states that the filters combine with AND inside the caller's scope

  Scenario: AC4 Paging and the stable order are fixed (new, D-RCV-60)
    Given the page and size parameters of GET /cases
    When the document is validated
    Then the response envelope carries items, page, size and total
    Then the default and maximum size are named as parameter rows and not as numbers in the schema
    Then the order is stated and ends on the case number, so a walk of pages neither repeats nor skips a case
    Then no cursor token is published, because no source gives one

  Scenario: AC5 The export contract and its refusals are fixed (new, D-RCV-60)
    Given the operation GET /cases/export
    When it is validated and linted
    Then it takes the same filters without page and size
    Then it answers 200 with the spreadsheet content type, one row per matching case and the columns masked for the caller's role
    Then it answers 422 above caselist.export.maxrows and 503 when the access-log entry cannot be written, and in both cases no file is produced
    Then the description states that the access-log entry AC-EXPT is written before the workbook is built

  Scenario: AC6 The right, the scope and the error envelope are published (new, D-RCV-60)
    Given the problem schema shared by both operations
    When the error examples are validated
    Then the envelope carries type, title, status, detail, instance and an errors list with field
    Then the examples carry MSG-P4-002 on 403, MSG-P3-021 on 422, MSG-P7-003 on 503 and MSG-P3-020 as the empty page text
    Then every operation requires the Case record right R and states that the scope is applied

  Scenario: AC7 The two consumed answers and the 2 s budget are recorded (new, D-RCV-60)
    Given the consumed operations of section 12.2
    When the document is reviewed
    Then the authorise answer of rwb-access is named with the right, the scope and the masking rules it returns
    Then the access-log write of rwb-access is named with the AC-EXPT fields of the legacy story
    Then both are one hop with a 2 s timeout and a breaker, and no operation of this document chains a call

  Scenario: AC8 The nine contract tables and the fakes agree (new, D-RCV-60)
    Given the nine tables of section 12 and the published document
    When the contract test runs
    Then every table and index named in section 12 sits in rwb_case with its P3 owner
    Then the fake answers every operation and every example, including the 403, 422 and 503 of section 14
    Then a breaking change raises v2 and deprecates v1 instead of editing it
```

These criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here, and every business value in the examples comes from the legacy story or the technical specification character for character. The legacy criteria AC1 to AC8 are owned and proved by RWB-P3-E1031-APP against this document.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract publishes rwb-case resources only; the right, the scope, the masking rules and the access log are rwb-access | DP-08; ownership map |
| BR2 | The list holds only cases inside the caller's scope (Own, Team, Region, All) and the filters combine with AND | Legacy BR1, BR2; REQ-ACA-009 |
| BR3 | The export is refused above `caselist.export.maxrows` before anything is written | Legacy BR5; DL11 |
| BR4 | The access-log entry is written before the workbook is built, and a failure of the entry produces no file | Legacy BR3; REQ-ACA-006 |
| BR5 | Export columns follow the masking rules for the caller's role, which arrive in the authorise answer | Legacy BR4; REQ-ACA-005; DL26 |
| BR6 | The order of a page is total and ends on the case number | Legacy AC1 and AC7; paging |
| BR7 | A case with no owner is a row with `ownerUserId` absent, never a row hidden | Legacy AC7 |
| BR8 | Both operations are reads: no POST, no event, no workflow, no lock, and the export declares no Idempotency-Key because it stores nothing of its own | Legacy section 9; DP-09 not applied |
| BR9 | Every value a business person may change is a parameter or reference row with its version in force | Legacy BR5; DP-06, DP-07 |

### 9. State transitions

None in this story: a document has no runtime state. The states the document exposes are the case statuses of LOV-CASE-STATUS in the `status` filter and in the row, and the case and queue transitions themselves belong to RWB-P3-E1020-APP and RWB-P3-E1021-APP. This document fixes only the HTTP status that accompanies each refusal: 401 no session, 403 no Case record right, 422 a value outside its list or an export above its limit, 503 the store or the access log unavailable.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fake |
| The service owner of rwb-case | Approves a breaking change and a version freeze |
| The consumer teams (app, queue views, gateway, integration harness) | Read the document, pin a version, raise a change request |
| rwb-access (P4) | Owns the authorise and access-log contracts this document consumes and never republishes |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

Role names appear in the examples as role codes only, resolved by rwb-access at run time (DP-08). No personal name, no email address and no credential appears in the document or an example; an owner appears as a staff user reference, and the display name is not published (GAP-2209; ASM-3630).

### 11. Data

| Item | Value |
|---|---|
| Field identifiers published | DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-005, DF-CAS-006, DF-CAS-009, DF-CAS-010, DF-CAS-011, DF-CAS-012, DF-CAS-013 (recovery_case); DF-WRK-001 to DF-WRK-004 (queue) |
| Field identifiers referenced, not published | The parameter rows behind `caselist.export.maxrows` and the reference rows behind LOV-CASE-STATUS and LOV-TEAM: read in process through RWB-P3-E1042-CON and RWB-P3-E1043-CON, never joined in SQL and never republished as values |
| Field identifiers with no source | The display name of an owner, the page-size default and maximum as parameter keys, and the parameter field identifiers themselves: Not specified in the source documents (GAP-2209; ASM-3630) |
| Personal data in examples | None. Owners appear as staff user references (U-71, U-11) and cases as case numbers (RW-2026-000601) |
| Values in examples | 64 cases in "DIL-BKK-CO", 20 in "DIL-BKK-OVF", 51 filtered cases, 10,000 and 10,001 rows, 10,000 as the limit, all copied from the legacy story |

The document carries no value that no source holds. Where a consumer needs a field or a key that neither the legacy story nor the technical specification defines, the schema carries the placeholder text and the change waits for the gap to close; this is a draft baseline, so a new version can add the field without breaking a consumer.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Operation | Document | Request | Responses | Owner |
|---|---|---|---|---|
| GET /api/recovery/case/v1/cases | caselist.yaml | Query: queue (uuid), team, status, owner, product, stage, page, size, sort | 200 CaseListPage (items, page, size, total); 401 MSG-P4-001; 403 MSG-P4-002; 422 a value outside its list; 503 | P3 |
| GET /api/recovery/case/v1/cases/export | caselist.yaml | The same query without page and size | 200 application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; 401 MSG-P4-001; 403 MSG-P4-002; 422 MSG-P3-021 above the row limit; 503 MSG-P7-003 access log unavailable | P3 |

`CaseListRow` carries `caseNo`, `productGroup`, `status`, `stageCode`, `queueId`, `queueCode`, `queueName`, `ownerUserId` (optional), `teamCode`, `regionCode` and `entryDate`. `queueCode` and `queueName` are joined from `queue` for the column and the filter labels; `regionCode` is published because the scope of BR2 needs it. The exact name of the envelope, of the row schema and of the sort token, and the page-size keys, are this story's proposal (GAP-2209; ASM-3630). The team parameter is additive and optional on `GET /cases` (ASM-3624).

#### 12.2 REST operations consumed

| Operation | Provider | Why this document needs it | Pattern |
|---|---|---|---|
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | The 403 example, the scope rule of BR2, and the masking rules of BR5 arrive in this answer, cached per request | DP-08, DP-11 |
| POST /api/recovery/access/v1/access-events | rwb-access (P4) | The 503 example and the ordering rule of BR4: the AC-EXPT entry with the user, the time, the filters and the row count, written before the file | DP-11 |

Both are one hop with a 2 s timeout and a breaker; no operation of this document calls a service that calls another (ADR-020). The parameter and reference reads of DP-06 and DP-07 are in-process library reads of rwb-case and are not rows of this table.

#### 12.3 Events published

None. No operation of this document publishes an event and the export writes no outbox row. `rwb.case.events.v1` and the names `rwb.case.CaseCreated.v1`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.case.TimerBreached.v1` are contracted by the stories that own their behaviour under DP-14; the access event AC-EXPT is not a Kafka event but the rwb-access call of 12.2.

#### 12.4 Events consumed

None. The list is read from the rows per request and no projection or inbox row stands behind it, so this contract declares no subscription and no event schema.

#### 12.5 Workflows and activities

None. Neither operation starts, signals or reads a workflow. `CaseWorkflow` on task queue `rwb-case` in namespace `rwb-recovery` is the case lifecycle and is declared by the stories that own it; this document names the task queue only as the service's naming baseline.

#### 12.6 Schedules

None. No Temporal Schedule and no batch window belongs to these operations: the list is read on request and the export is officer-driven.

#### 12.7 Tables owned

| Table | Schema | Key and indexes to publish in the baseline file | Owner | Rows exposed |
|---|---|---|---|---|
| recovery_case | rwb_case | PK id; unique case_no; ix_case_status_queue (status, queue_id); ix_case_owner_status (owner_user_id, status); ix_case_team_status (team_code, status) | P3 | GET /cases, read only |
| queue | rwb_case | PK id; unique queue_code; team_code | P3 | queueCode, queueName and the queue filter values |
| parameter_catalog, parameter_value | rwb_case | PK id; unique parameter key per environment; version in force | P3 | caselist.export.maxrows and the page-size bounds, through DP-06 |
| reference_row, reference_version | rwb_case | PK id; version_id to reference_version; unique table code and version number | P3 | LOV-CASE-STATUS and LOV-TEAM, through DP-07 |
| lov_value | rwb_case | PK id; unique list code and value code | P3 | The list values of the filter pickers |

The tables arrive on the per-service Flyway sequence after the V0001 baseline (DP-15; RWB-PLT-E1044-CON); `ix_case_team_status` is the index the legacy story asked for and it is published here as part of this legacy key (ASM-3631). This document adds no table outside `rwb_case` and no reference to a table in `rwb_access`.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-case case-list fake (this story) | The two operations, the row and page shape and the problem bodies | RWB-P3-E1031-APP, RWB-P3-E2033-APP, RWB-P3-E2011-APP, gateway-bff stories, RWB-ITG-E1031-ITG |
| rwb-access authorise fake (P4) | POST /authorise | The 403 example, the scope example and the masking rules of the app story |
| rwb-access access-log fake (P4) | The AC-EXPT write | The 503 example and the export tests |
| gateway-bff route stub | The SCR-02 composite route (DP-19) | The screen assertions of the app story |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations under `/api/recovery/case/v1` | 2 operations, both to rwb-access | OpenAPI 3.1, one hop, 2 s timeout, a breaker per downstream |
| Kafka | 0 | 0 | No event schema is published by this document |
| Temporal | 0 | 0 | Declared by the stories that own the workflows |
| File | 1 (the xlsx of the export in the response) | 0 | No claim-check store and nothing written to Blob |

### 13. Solution plan

**Deliverables.** `caselist.yaml` (OpenAPI 3.1, tag `Case list`, the schemas `CaseListRow` and `CaseListPage` and the shared problem schema); `schema-baseline.sql` with the five table groups of section 12 (for reference only, the executable migration belongs to the DB work); the contract fake; the contract test.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_case`; the document names no other service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library: the export limit and the page bounds are parameter rows, not schema constants | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case: every enumerated filter names its list in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library; the 403 and the scope rule are consumed, never republished | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with a mock, one hop, 2 s timeout: the two rwb-access answers | none (C from the legacy dependencies RWB-P4-E1037-CON and RWB-P4-E1039-CON) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1` and `rwb.case.<Event>.v1`; naming library, no channel published | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_case`; the baseline file names the tables and the three indexes | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-02 | H RWB-PLT-N001-CON |

This is a CON story: it documents the patterns of the legacy key and adds no build dependency of its own, so it is Day 1. DP-11 is the row that matters here, because the legacy in-process `AccessEventPublisher` is exactly the call that becomes a REST answer with a fake.

**Build steps**

1. Write `caselist.yaml` with the two operations, the `CaseListRow` and `CaseListPage` schemas and the shared problem schema.
2. Fix the filter set with the enumerated values and their lists in force, and the additive team parameter of BR2 and AC3.
3. Fix paging, the page-size parameters and the order that ends on the case number; declare no cursor.
4. Fix the export: content type, the row limit of BR3, the 422 and 503 of AC5 and the ordering rule of BR4.
5. Add the examples of section 14 with the four message ids and synthetic data only.
6. Write `schema-baseline.sql` from section 12 and cross-check every column against DF-CAS and DF-WRK identifiers.
7. Generate the fake and the contract test; wire both into the build of RWB-P3-E1031-APP and into a nightly run with RWB-P3-E2033-APP and RWB-ITG-E1031-ITG.
8. Publish v1 to the contract registry and notify the consumers.

**Done when.** The document validates, the lint rules pass, the fake answers every operation and every example, and the contract test runs green on the build of this story.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-020 | No case meets the filters | No cases match these filters. Change a filter to see more. | 200 with an empty page; the text is the screen's empty state |
| MSG-P3-021 | The export is above its row limit | The export holds at most {max} rows. Narrow the filters and try again. | 422 with the errors list naming the limit |
| MSG-P7-003 | The access-log entry cannot be written at export | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503, and no file |
| MSG-P4-002 | The role does not hold the Case record right | You cannot {action} here. Your role does not include it. | 403 |
| MSG-P4-001 | No valid session | Not specified in the source documents (GAP-2209; ASM-3630) | 401 |

The identified texts and identifiers are the legacy ones and no identifier is renumbered. Request validation is published as schema constraints where a source defines the value (queue as a uuid, status from LOV-CASE-STATUS, product from LOV-PRODUCT, stage from LOV-STAGE, page and size bounded by their parameter rows) and as the placeholder where no source does (the filter labels, the sort token and the page-token shape - GAP-2209; ASM-3630).

### 15. Screens and states

No screen in this story: it publishes the answers a screen binds to. The states the answers expose are the seven of SCR-02 in RWB-P3-E1031-APP - Loading, List, Filtered, Empty, Export refused, Export failed and Refused - and each is produced by a status of section 12.1: 200 for List and Filtered, 200 with an empty page for Empty, 403 for Refused, 422 for Export refused and 503 for Export failed. The route path, the screen model and the layout belong to RWB-PLT-N001-CON and the designer (DL31).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-031-01 | AC1, AC3 | Contract | caselist.yaml validated and linted; the two paths under /api/recovery/case/v1; AC1 of the app story asserted against the fake |
| TC-E1-031-02 | AC2 | Contract | CaseListRow compared field by field with the DF-CAS fields of section 11 and DF-WRK-001 to DF-WRK-004; ownerUserId optional |
| TC-E1-031-03 | AC3 | Contract | Every enumerated filter names its list in force; the team parameter is optional and additive |
| TC-E1-031-04 | AC4 | Contract | Envelope items, page, size and total; the order ends on caseNo; no cursor token |
| TC-E1-031-05 | AC5, AC6 | Contract | The export answers 200 with the spreadsheet type, 422 with MSG-P3-021 above 10,000 rows and 503 with MSG-P7-003 |
| TC-E1-031-06 | AC6 | Contract | The problem schema and the four message ids in the examples |
| TC-E1-031-07 | AC2, AC6 | Contract | The row with no owner: ownerUserId absent, the row still returned |
| TC-E1-031-08 | AC5, AC6 | Contract | Exactly 10,000 rows accepted; 10,001 refused |
| TC-E1-031-09 | AC6, AC1 | Contract | A call without a session answers 401; a role without the Case record right answers 403 with MSG-P4-002 |

The nine legacy identifiers are kept and are asserted here at contract level, against the document and the fake; the same identifiers run as behaviour tests in RWB-P3-E1031-APP, where the Given, When and Then of the full test in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, are applied. No identifier carries an `-ITG` suffix here: the integration copy is RWB-ITG-E1031-ITG, which owns its own copies.

### 17. Guardrails

- No business value in a schema as a constant: the export limit and the page bounds are published as parameter-row references and every enumerated filter names its list (DP-06, DP-07).
- No personal data in examples, events or logs: an owner is a staff user reference and a case is a case number; no name, identity number, address or account number appears.
- No cross-schema reference: the document names `rwb_case` tables only and consumes the rwb-access answers without republishing them (DP-01, DP-08).
- One hop and a 2 s timeout for every consumed operation; a timeout is published as 503 and never as a stale answer.
- The base path is `/api/recovery/case/v1` and the monolith base is never republished (DP-13).
- The export cannot be made without its access-log entry, and the document says so in the operation description (BR4).
- The document is versioned: a breaking change raises v2 and deprecates v1 rather than editing v1 in place.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-CWC-007 | Every case has a queue and an owner by rule, visible on the case list | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-19 | BR2, BR6, BR7 | TC-E1-031-01 to TC-E1-031-04, TC-E1-031-07 |
| REQ-ACA-009 | A user sees only the cases their scope allows | Epic 1, 3.4; Program, 5.4 | FEAT-CWC-19 | BR1, BR2 | TC-E1-031-03, TC-E1-031-09 |
| REQ-ACA-006 | Every read of the case store is written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-CWC-19 | BR4 | TC-E1-031-05 |
| REQ-ACA-005 | An export carries only the columns the caller's role may see | Epic 1, 3.4; Program, 5.4 | FEAT-CWC-19 | BR5 | TC-E1-031-02, TC-E1-031-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1031-APP | App development | H consumer: builds against this contract and its fake and owns AC1 to AC8 |
| RWB-P3-E2033-APP, RWB-P3-E2011-APP | App development | Consumers of the row shape and the paging that extend the same base |
| RWB-P4-E1037-CON, RWB-P4-E1039-CON | Contract | C: the authorise and access-log answers this document consumes and never republishes |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | The parameter and reference-data contracts the filters and the limit reference |
| RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON | Contract | H: naming library, Flyway sequence and the gateway-bff composite route |
| RWB-ITG-E1031-ITG | Integration | Proves the same answers with every service live |

The legacy reference is kept in full: the two operations, the eight criteria, the five messages, the fourteen fields, the nine test cases and the feature flag `rwb.p3.caselistqueue` are the ones this baseline publishes, and the wider list, the queue views and the masking policy stay with the stories section 19 names.

### 19. Out of scope

- Any implementation, repository, migration or deployment: this story publishes a document, a baseline file and a fake only.
- The right, the scope, the masking policy and the access log: rwb-access, RWB-P4-E1037-CON and RWB-P4-E1039-CON.
- The parameter and reference-data contracts themselves, and the values they serve: RWB-P3-E1042-CON and RWB-P3-E1043-CON.
- The case-list screen and its states: RWB-P3-E1031-APP; the wider list with ageing: RWB-P3-E2033-APP; the queue views: RWB-P3-E2011-APP.
- The gateway-bff composite route and its screen model: RWB-PLT-N001-CON.
- Every event schema and every workflow declaration: the stories that own the case, allocation, transfer, state and timer behaviour.
- The masking rules themselves and the label standard: DL26 and DL10.
