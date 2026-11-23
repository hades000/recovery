# RWB-P4-AD011-CON Load a rule version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-011 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access-side half of the rule-version load: an OpenAPI 3.1 document for the two console operations of the ingest and the read, the `RuleVersionLoad` and `RuleVersionCheck` schemas, the two states this service produces, the error envelope and the message mapping, the rule-package, authorise and parameters operations declared as consumed with their owners, the statement that no rule table is written here, the contract tables of section 12 and the contract fakes**, so that **the app story and the console build test the gate on Day 1 against a fixed document while the rule registry stays `rwb-decision`'s and no operation of the registry is claimed here**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story governed a rule version inside the monolith: the rule rows, the version and its approval were rows and screens of one module, and nothing outside it could tell what a version was. In the target the registry is central in `rwb-decision` (Architecture v5 slide 27) and the administration ingest is `rwb-access`'s, so the two halves meet on a contract. That contract has to say exactly what the administration service accepts, what it answers, what it refuses and what it does not write.

If that field-level contract is agreed once and faked for the two consumed `rwb-decision` operations, the authorise operation and the parameters read, the app story builds in parallel with P7, a change in the registry is caught in a contract test rather than in an integration window, and the refusal shape of a bad workbook — the check list of the registry — is fixed before either side codes it. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

### 3. Preconditions

- The service template and the naming library are available, so the base, the topic and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the RFC 9457 problem response and the `Idempotency-Key` rule on every POST are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the ownership map only. The rule-package operations are `rwb-decision`'s (ASM-0040) and the two console operations of this contract are `rwb-access`'s; the contract-dependency list of the app story carries no P7 rule-package contract, which is the gap this baseline closes with a fake (GAP-0821; ASM-1522).
- The registry half — `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the compile, the checks, the scenario run, the approval, the promotion and the rollback — is P7 `rwb-decision`'s under ASM-0069; this document consumes it and never defines it.
- The workbook format it declares is the Drools XLS decision-table workbook with the `rule_row` columns of TSD P4 T3.1 plus `test_case_id` on every row; the exact header order is Not specified in the source documents (GAP-0823; ASM-1524).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two console operations of `rwb-access` with the shared components the service uses.
2. Declare the multipart request of the load, its query, its `Idempotency-Key` and its 201 answer with the `Location` of the read.
3. Declare the `RuleVersionLoad` schema, the `RuleVersionCheck` schema, the check list of a refusal and the state set `LOADED` and `REFUSED`.
4. Agree the error envelope and the message mapping: 401, 403, 409, 422 and 503, with one message ID per condition and the 409 shape that carries the registry's check list.
5. Declare the consumed operations with their owners, one hop and the 2 s client budget: the two `rwb-decision` rule-package operations, the own authorise operation and the `rwb-case` parameters read.
6. State what the service does not write: no `rule_package`, no `rule_package_version` and no `rule_row` table, and `test_case_id` required on every row of the workbook.
7. Publish the contract tables of section 12, nine sub-tables, and the contract fakes.
8. Add the contract tests: schema validation, envelope validation, message mapping, the refusal shape, the consumed-operation list, the no-table statement and drift detection between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-AD011-APP and to the P7 and P3 owners whose operations it consumes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request body, query or multipart part fails schema validation | 400 or 422 with the error envelope and the failing pointer | MSG-GEN-001 | AC1, AC3 |
| X2 | A caller without Rules and parameters C on the load, or R on the read | 403 with the error envelope and the refusal code | MSG-P4-002 | AC1, AC3 |
| X3 | The registry refuses the workbook | 409 with the error envelope, `state` `REFUSED` and the check list; the envelope declares the shape | MSG-GEN-004 | AC3 |
| X4 | The registry does not answer inside the 2 s budget | 503 declared on both operations; no version is reported | MSG-P7-003 | AC3, AC4 |
| X5 | A field of the version or of a check has no source definition | The field is marked with the placeholder and carried as a gap in the app story | None | AC2 |
| X6 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X7 | A document or a fake carries a personal data field | The contract test fails: no name, no e-mail address and no personal field is declared | None | AC6 |
| X8 | A caller asks the read for a version that the registry does not hold | 404 with the error envelope; no empty answer is invented | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes and the P7, P3 and own-service contracts only |
| Negotiable | The field names of the check list, the exact multipart part names and the screen field list are settled with the registry owner and the analysts; the operations, the states, the envelope and the no-table statement are fixed |
| Valuable | Unblocks the app story and the console on Day 1 and keeps the rule registry out of the `rwb-access` document |
| Estimable | One OpenAPI document, one envelope, one refusal shape, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access-side rule-version load contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access-side half of the legacy journey is the workbook ingest and the version read

  Scenario: AC1 The OpenAPI 3.1 document describes the two console operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/rule-version-loads and GET /admin/rule-version-loads/{versionId} with the owner rwb-access
    Then the load declares the multipart part file (xlsx) and the query packageCode, routeSet and validFrom, and the Idempotency-Key header
    Then the load names Rules and parameters C and the read names Rules and parameters R
    Then both operations declare 401 and 403, the load declares 409 and 422, the read declares 404, and both declare 503

  Scenario: AC2 The version and the check list are declared once (new, D-RCV-60)
    Given the RuleVersionLoad and RuleVersionCheck schemas of the document
    Then RuleVersionLoad carries versionId, packageCode, versionLabel, validFrom, rowCount, checksum, testResult, dryRunCounts and state
    Then the state property is one of LOADED and REFUSED
    Then RuleVersionCheck carries one entry per check with its check code, its outcome, its rows and its detail
    Then the 409 body carries the check list as items of RuleVersionCheck
    Then no property of either schema is a name, an e-mail address or a personal field

  Scenario: AC3 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by a console operation
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 422 carries MSG-GEN-001 naming the field, the missing column or the row and test_case_id
    Then 409 carries MSG-GEN-004 with the check list, and 503 carries MSG-P7-003
    Then the response carries the problem media type and the trace identifier

  Scenario: AC4 The four consumed operations are declared as consumed (new, D-RCV-60)
    Given the two rwb-decision rule-package operations, the own authorise operation and the rwb-case parameters read
    Then each is declared in the consumed section with its owner P7, P4 or P3, one hop and the 2 s client budget
    Then the load of a version is declared as POST /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions with the owner rwb-decision
    Then the read of a version is declared as GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions/{versionId} with the owner rwb-decision
    Then the document declares no operation owned by rwb-decision, rwb-case or the platform as provided by rwb-access

  Scenario: AC5 The document states that no rule table is written here (new, D-RCV-60)
    Given the contract tables of section 12
    Then the document states that no rule_package, rule_package_version or rule_row table is written by rwb-access and that the registry holds them under ASM-0069
    Then the document states that test_case_id is required on every row of the workbook and that a row without one refuses the version at upload
    Then 12.7 names role, permission and the idempotency table and no rule table
    Then the workbook and the version are the registry's to store, and the document names no blob of its own

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the four contract fakes of section 12.8
    When the contract tests run
    Then each fake answers the paths and payloads of 12.2 and 12.8, including the LOADED answer, the REFUSED answer with its check list and the 503
    Then a contract test fails on any drift between a fake and the document
    Then no schema, example or fake holds a name, an e-mail address or a personal field
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; the two legacy criteria of RWB-AD-011 belong to RWB-P4-AD011-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 14 |
| BR2 | A consumed operation is described as consumed, never as provided, and its owner comes from the ownership map | DP-11; Ownership Map v1; ASM-0040 |
| BR3 | The contract declares no rule table of `rwb-access`, because the registry is P7's | DP-01; ASM-0069 |
| BR4 | `test_case_id` is required on every row of the workbook and a row without one refuses the version at upload, named by row and field | Legacy RWB-AD-011 AC2; GAP-0825; ASM-1526 |
| BR5 | Error responses use one envelope and one message ID per condition; the business texts are copied from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR6 | A refusal is a declared 409 with the registry's check list, never a silent accept and never a fallback to the version in force | REQ-CWC-014; R-UNI-38 |
| BR7 | The state set of this contract is `LOADED` and `REFUSED`; the other values of LOV-VERSION-STATUS are read from the registry and passed through unchanged | TSD P4 T3.2; TSD P4 T4 |
| BR8 | The scenario minimum, the row and file limits and the route sets are parameter rows and list values, never a value in the document | DP-06; TSD P4 T3.2; BR-P4-018 |
| BR9 | No schema, example or fake carries a personal data field | Principle 5; NFR-040 |
| BR10 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the envelope and the four consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the registry owner and the console accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake, or a personal field in a schema or an example | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Tech lead of `rwb-decision` (P7) | Reviews the two consumed rule-package operations and the check list of a refusal; owns their definitions |
| Tech lead of `rwb-case` (P3) | Reviews the parameters read and its version-in-force rule |
| Console lead and the QA team | Review and sign off the screen states of section 15 and the field list they consume |
| Data steward | Confirms that no personal data field is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| `RuleVersionLoad` | `versionId`, `packageCode`, `versionLabel`, `validFrom`, `rowCount`, `checksum`, `testResult`, `dryRunCounts`, `state`; the version fields the registry holds as DF-REF-279, DF-REF-281, DF-REF-286, DF-REF-285, DF-REF-292 and DF-REF-293, and `rowCount` counted from the workbook rows |
| `RuleVersionCheck` | one entry per check: `check` (the registry's check code), `outcome`, `rows[]` (the row numbers the check names), `detail`; the outcome of a compile, overlap, unreachable-row, default-row or scenario-count check |
| Refusal | `code`, `message` with `messageId` MSG-GEN-004, `state` `REFUSED`, `checks[]` of `RuleVersionCheck`, `traceId`, `instance` |
| Request | multipart `file` (xlsx) and the query `packageCode`, `routeSet`, `validFrom`; no personal field, and no caller identity in the body |
| Event payloads | None: this contract declares no event |

The exact field-level names of a check code and the sort of the check list are the registry's and are carried unchanged; where a field of the version has no source definition the app story carries the placeholder (GAP-0824; ASM-1525).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/rule-version-loads` | Multipart `file` (xlsx) and query `packageCode`, `routeSet`, `validFrom`; answers 201 with `RuleVersionLoad` and the `Location` of the read; `Idempotency-Key` required | Rules and parameters C |
| GET | `/admin/rule-version-loads/{versionId}` | Answers `RuleVersionLoad` with the status of the version, its checksum, its test result and its dry-run counts | Rules and parameters R |

Errors: 401 no session (MSG-P4-001) and 403 no right (MSG-P4-002) on both; the load adds 409 refused by the registry with the check list (MSG-GEN-004) and 422 for a missing part, column, test case ID or an unknown route set (MSG-GEN-001); the read adds 404 for a version the registry does not hold; and both declare 503 for a registry that is unavailable (MSG-P7-003). The POST carries the `Idempotency-Key` header and the document states that a repeated key answers the first answer; the GET is a read and carries none.

The two operations sit under this service's base of DP-13. The rule-package operations themselves are `rwb-decision`'s under ASM-0040 and are consumed, never provided, here.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 `rwb-decision` | The workbook load: multipart `file` and `validFrom`; the registry compiles, checks, runs the scenarios and stores the version, or refuses it with its check list |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions/{versionId}` | P7 `rwb-decision` | The version, its status, its checksum, its test result and its dry-run counts |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` | The Rules and parameters C or R check behind both provided operations |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | `rules.testcases.min` and the row and file limits, with the version in force (DP-06) |

None of the four is declared as provided by this document except the authorise operation, which is this service's and is consumed here by its own guard. The two `rwb-decision` operations are the registry half.

#### 12.3 Events published

None. `rwb.access.events.v1` carries only `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1` (Architecture v5 slide 14), and this contract adds no event type. The rule-version event `rwb.decision.RulePackageInForce.v1` (EV-30) is `rwb-decision`'s and is not declared here.

#### 12.4 Events consumed

None. This contract declares no subscription, and the app story's read answers from the registry on request.

#### 12.5 Workflows and activities

None. No workflow and no activity is declared: the promotion at 00:01 is a Temporal Schedule of `rwb-decision` (JOB-20) and is outside this contract.

#### 12.6 Schedules

None. A load is request-driven and the only Schedule of the version lifecycle runs on `rwb-decision`'s queue.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's role and its class behind the C and R letters |
| `permission` | P4 (`rwb_access`) | The letter of the caller's role in Rules and parameters |
| `idempotency_key` | PLT library, created in `rwb_access` | The stored request and answer of a load (DP-09) |

No rule table is named in the contract and no table of another service is read (DP-01). `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` stay P7 `rwb-decision`'s under ASM-0069 and appear only as consumed shapes; `test_case_id` is a required column of the workbook (DF-REF-015) and is stored by the registry, not here.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule-package WireMock | `POST /admin/rule-packages/{packageCode}/versions` answering version "ENTRY-2027.01" in state `LOADED` with checksum "3f9c…", test result `PASS`, 448 rule rows and the SIT report reference; a refusal with `checks[]` naming an overlap at rows 12 and 13, an unreachable row 88, a missing default row and 41 scenarios against the minimum 50; a 503; `GET /admin/rule-packages/{packageCode}/versions/{versionId}` answering the loaded version, the refused one and a 404 | App story, contract tests, console |
| parameters fake | `GET /api/recovery/case/v1/admin/parameters` answering `rules.testcases.min` = 50 and the row and file limits, with the version in force on 15 December 2026 | App story, contract tests |
| authorise and guard fake | `POST /authorise` granting Rules and parameters C to RW-COE and R to RW-RISK, RW-AUDIT and RW-PLATADM, and refusing RW-CASEOWN and RW-REFADM with MSG-P4-002 | App story, contract tests |
| gateway-bff composite route fake | The SCR-39 route calling the load and the read, one hop each, and merging the version fields with the check list of a refused load | Console, app story |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The ingest and the read provided; two `rwb-decision` operations, the own authorise operation and the `rwb-case` parameters read consumed; one hop, 2 s timeout |
| Kafka | 0 published, 0 consumed | No event in this contract |
| Temporal | 0 workflows, 0 activities | The promotion at 00:01 is `rwb-decision`'s |
| File | One xlsx in | The multipart workbook; the version's stored blob is the registry's |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-rule-version-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml` with the message mapping, the `RuleVersionLoad` and `RuleVersionCheck` schemas, the refusal contract, the idempotency and versioning rules in the contract README, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is in this contract's pattern set because the analyst's group resolves through the service's own `v_ace_iam_group` view and no personal field of it is declared here. There is no DP-04: the Drools kit and the evaluation belong to `rwb-decision` and the model-owning services, and this contract claims neither (GAP-0822; ASM-1523).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The two operations with the multipart request, the query, the `Idempotency-Key` and the `Location` of the read.
3. The `RuleVersionLoad` and `RuleVersionCheck` schemas and the state set of BR7.
4. The error envelope and the message-ID mapping, with the business texts copied from the legacy story where they existed.
5. The 409 shape with the check list, and the 404 of an unknown version.
6. The four consumed operations with their owners, the one-hop rule and the 2 s client budget.
7. The four fakes and the stub fixtures of section 12.8.
8. The seven contract tests: schema, envelope, message mapping, refusal shape, consumed list, the no-table statement and drift.
9. Baseline tag and the consumer sign-off note from the app story, the console and the P7 and P3 owners.

**Feature switch.** The document declares no switch: a load that is switched off would leave the old version in force while the screen said nothing, so the refusal path is the control and it is not a flag. The service-level feature flag of the service baseline is outside this contract.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD011-APP | The two provided operations, the two schemas, the refusal shape and the four fakes |
| SCR-39 console build | The states of section 15, the version fields and the check list of a refusal |
| The P7 rule-package owner of `rwb-decision` | The two consumed operations as `rwb-access` uses them, and the check list it returns; no P7 operation is claimed as provided |
| RWB-P3-E1042-CON (P3 `rwb-case`) | The parameters read and its version-in-force rule |

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the four fakes answer every consumed path, and the app story, the console and the P7 and P3 owners have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required part, query field or column is empty, the route set is unknown, a limit is exceeded, or a row carries no test case ID | Enter {field}. |
| MSG-GEN-004 | The registry refuses the workbook | Someone else changed this record. Reload it to see their change. |
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the C or R letter in Rules and parameters | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-P7-003 | The registry could not be reached or could not record the version | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. The catalogue text of MSG-GEN-004 is the platform conflict text, and the refusal is read through `checks[]`, which names each failing check and its rows, so the analyst reads which check failed.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Empty | The read with no version for the package: an empty list and no error |
| SCR-39 Rules and parameters | Checked | The load in flight: the row count of the request and no version yet |
| SCR-39 Rules and parameters | Refused | The 409 with `state` `REFUSED` and `checks[]` of `RuleVersionCheck` |
| SCR-39 Rules and parameters | Loaded, waiting for approval | `RuleVersionLoad` with the version label, the valid-from date, the row count, the checksum, the test result and the dry-run counts |

The screens are served by the gateway-bff composite route (DP-19), which calls the two operations and the registry's version operations in parallel, one hop each, and merges the answers. The composite route specification is the platform's; this document fixes the access side of the merge only, and the approval state is shown as waiting because the approval is `rwb-decision`'s.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-011-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the base, the two operations, the multipart request, the rights and the error responses 401, 403, 409, 422, 503 and 404 |
| TC-AD-011-CON-02 | AC2 | Contract | `RuleVersionLoad` with the nine fields; `RuleVersionCheck` per check; the state set LOADED and REFUSED; no personal field |
| TC-AD-011-CON-03 | AC3 | Contract | The envelope with MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-004 and MSG-P7-003; the 409 with the check list |
| TC-AD-011-CON-04 | AC4 | Contract | The four consumed operations with owner, one hop and the 2 s budget; no P7, P3 or platform operation declared as provided |
| TC-AD-011-CON-05 | AC5 | Contract | The no-rule-table statement, the required `test_case_id` and 12.7 naming no rule table |
| TC-AD-011-CON-06 | AC6 | Contract | The four fakes match the document; a drifted fake and a personal field each fail the build |

### 17. Guardrails

- No business value in the contract: the scenario minimum, the row and file limits, the route sets and the version states stay parameter rows and list values with versions (BR8). The document names the parameter, never its value as a constant.
- No personal data in a schema, an example or a fake: user references, codes, counts and dates only, and a contract test fails on a personal field (BR9).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the registry tables and the two `rwb-decision` operations are consumed and documented as consumed (DP-01, ASM-0069).
- One REST base per service; a document that names another service's base fails the review (DP-13).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- A refused workbook is a declared 409 with its check list, never a silent accept and never a fallback to the version in force (BR6).
- The error envelope and the `Idempotency-Key` rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated load to production with a version stamp and no code release | The load, the version read, the `RuleVersionLoad` schema and the consumed registry operations; the stamp is the registry's version label | TC-AD-011-CON-01, TC-AD-011-CON-02, TC-AD-011-CON-04 |
| REQ-CWC-014 | Rule loads are validated before they take effect | The required `test_case_id`, the check list of a refusal and the 409 shape; the checks themselves are P7's | TC-AD-011-CON-03, TC-AD-011-CON-05 |
| REQ-DRI-010 | A parameter catalog holds every threshold and limit, versioned | The parameters read with the version in force and the document's refusal to hold a value | TC-AD-011-CON-04, TC-AD-011-CON-05 |
| REQ-ACA-013 | Full administration screens are available, with their rights | The C and R letters on the two operations and the four screen states through the composite route | TC-AD-011-CON-01, TC-AD-011-CON-04 |

### 19. Out of scope

- The implementation of the ingest and the read, the workbook parser, the column gate, the row gate and the idempotency store (RWB-P4-AD011-APP).
- The registry half: the compile, the checks, the scenario run, the version states, the approval, the promotion and the rollback (P7 `rwb-decision`; ASM-0069).
- The `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables, and the workbook blob of a version.
- The approval operation and its screen surface; the document shows a loaded version as waiting for approval and declares no approval path.
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook of this capability.
- The operations of other services beyond the four consumed here; the `rwb-decision`, `rwb-case` and platform contracts are consumed and faked, never defined here.
- The cross-service journey evidence: no ITG story is split from this legacy key, so no `-ITG` copy of a test case is written here.
