# RWB-P3-E2041-CON Rule change governance and audit report

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E2041-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Contract version | v1 (major version in the path `/api/recovery/case/v1`; document `openapi/rwb-case-v1.yaml`) |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-041 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E2041-CON-16) |
| Depends on (build) | None; RWB-PLT-E1027-CON; RWB-PLT-E1072-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-E1037-CON; RWB-PLT-E1047-CON; RWB-PLT-E1044-CON; RWB-PLT-N001-CON |
| Contract dependencies | RWB-P7-E1073-CON; RWB-P3-E1042-CON; RWB-P3-E1043-CON; RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-026, FR-P3-027, FR-P3-028, FR-P3-029) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-041 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 24 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **tech lead**, I want **the published contract baseline of the case-side half of the rule change governance journey: an OpenAPI 3.1 document for the queue case list, the case resource and the new case-side rule-change audit read, an AsyncAPI document for the two consumed event types under a CloudEvents envelope, the error envelope and message mapping, the rule that a package version not in force is refused, the contract tables of section 12 and the contract fakes for rwb-decision and rwb-access**, so that **the app story, the operations story and the integration harness can build against a fixed, testable contract on Day 1 without waiting for rwb-case, rwb-decision or rwb-access to be built**.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story governed a rule package inside the monolith: the checklist, the approval, the effect counts and the report were columns and cursors in the recovery schema. In the target the registry is central in rwb-decision (P7) and the case side is rwb-case's, so the case side needs a contract of its own that says exactly three things to the outside: the open-case count an impact summary speaks about, the pinned package version a case reads back, and the audit read of what the case decisions did under each package version — including the version each open case keeps under R-UNI-38.

If that field-level contract is agreed once and faked for the five consumed rwb-decision operations and the authorise operation, the app story builds in parallel with P7 and P4, and a change in either is caught in a contract test rather than in an integration window. The baseline fixes the naming the checks require: schema rwb_case, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` for the service, the consumed topics `rwb.decision.events.v1` and `rwb.decision-record.v1`, task queue `rwb-case` in namespace rwb-recovery and Java package `th.co.scb.ace.workbench.recovery.case`.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions (DP-15). RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19).
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The operations and their owners are taken from the ownership map only. The case-side audit read has no row in that map, so its owner, path, right and response are carried as a gap and an assumption (GAP-0718; ASM-1265).
- The registry half — `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, the change checklist DF-REF-295, the approval and the change report — is P7 rwb-decision's under ASM-0069; this document consumes it and never defines it.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three case-side operations with the shared components used across the sixteen rwb-case operations.
2. Draft the AsyncAPI document for the two consumed event types with their topics, owners and the shared CloudEvents 1.0 envelope.
3. Agree the error envelope, the message mapping and the refusal contract for a package version that is not in force (MSG-P3-027).
4. State the audit read query, the entry schema, the CSV column order and the reconciliation rule with the decision log.
5. State the one-hop rule and the 2 s client budget for the six consumed operations.
6. Publish the contract tables of section 12 (nine sub-tables) and the two contract fakes.
7. Add the contract tests: schema validation, envelope validation, error mapping, the refusal mapping and drift detection between a fake and the document.
8. Tag the baseline and hand it to RWB-P3-E2041-APP, RWB-P7-E2041-APP, RWB-ITG-E2041-ITG and every consumer of the case side.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request body or query fails schema validation | 400 with the error envelope and the failing pointer | MSG-P3-030 | AC3 |
| X2 | A reader holds no Rules and parameters right | 403 with the error envelope and the refusal code | MSG-P4-002 | AC3 |
| X3 | The audit read period ends before it starts | 422 with the error envelope naming `to` and `from`; no read is made | MSG-GEN-003 | AC3, AC4 |
| X4 | A caller reads a case outside its scope | 404 with the error envelope; the case is not named | MSG-P4-003 | AC3 |
| X5 | No package version is in force on the business date | The contract declares `NoPackageInForce` as a non-retryable activity failure carrying MSG-P3-027; nothing is written | MSG-P3-027 | AC5 |
| X6 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X7 | A field of the audit read has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |
| X8 | A consumed rwb-decision operation does not answer inside the REST budget | The call answers 503 for that read; the case-side audit read still answers from rwb_case alone and the contract declares the 503 | None | AC4 |
| X9 | A caller asks the audit read for a package code the service does not evaluate | 422 with the error envelope naming `packageCode`; no read is made | MSG-P3-030 | AC1, AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes and the P7 and P4 contracts only |
| Negotiable | The field-level detail of the audit entry is settled with audit and the integration harness; the operations, the topics, the envelope and the refusal are fixed by the target architecture |
| Valuable | Unblocks the app story, the operations story and the wave 2 harness on Day 1, and keeps the P7 registry out of the rwb-case contract |
| Estimable | Two documents, one error envelope, one refusal contract, nine contract tables, two fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Case-side rule change audit contract baseline for rwb-case

  Background:
    Given the service naming rule of the platform library is in force
    Given the case-side half of the legacy journey is the open-case count, the pinned package version and the case-side audit read

  Scenario: AC1 The OpenAPI 3.1 document describes the case-side operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-case is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/case/v1
    Then it declares GET /queues/{queueId}/cases, GET /cases/{caseId} and GET /admin/rule-change-audit with the owner rwb-case
    Then the audit read declares the query from, to, packageCode, format, page and size with the page default 50 and the maximum 200
    Then every operation names its security right and its error responses 401, 403, 404 and 503

  Scenario: AC2 The audit read answers one entry per package version (new, D-RCV-60)
    Given the CaseRuleChangeAuditEntry schema of the document
    When the audit read answers a request for the period
    Then it carries packageCode, versionLabel, versionStatus, decisions, casesAffected, firstDecisionAt, lastDecisionAt, openCasesAtVersion and openCasesKeepingVersion
    Then the page carries items, page, size and total
    Then the CSV answer declares the same columns in the same order with one header row
    Then no property of the schema and no CSV column is a case number, a party key or a case-level row

  Scenario: AC3 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 422 or 503 response is produced by a case-side operation
    Then the body carries the code, the message, the messageId, the traceId and the field list
    Then 403 carries MSG-P4-002 and 401 carries MSG-P4-001
    Then 422 carries MSG-GEN-003 naming "to" and "from" for the audit read period
    Then the response carries the problem media type and the trace identifier

  Scenario: AC4 The six consumed operations are declared as consumed (new, D-RCV-60)
    Given the five rwb-decision operations and the rwb-access authorise operation
    When the document is reviewed against the ownership map
    Then each is declared in the consumed section with its owner P7 or P4, one hop and the 2 s client budget
    Then the document declares no operation owned by rwb-decision or rwb-access as provided by rwb-case
    Then the decision record read is declared as the reconciliation source of the audit read

  Scenario: AC5 The two consumed events and the three tasks are contracted (new, D-RCV-60)
    Given the AsyncAPI document of rwb-case and the activity contract jar
    When the contracts are reviewed
    Then rwb.decision.RulePackageInForce.v1 is declared on rwb.decision.events.v1 with the owner rwb-decision
    Then rwb.decision.DecisionRecorded.v1 is declared on rwb.decision-record.v1 with the owner rwb-decision
    Then both messages use the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype
    Then no message carries a personal data field
    Then the contract names CaseWorkflow, EvaluateRules and RecordAndApply on task queue rwb-case with their input and output shapes and ruleId and packageVersion in the output
    Then EvaluateRules declares NoPackageInForce as a non-retryable failure carrying MSG-P3-027

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the ownership map
    Then 12.7 names recovery_case, queue and case_account and no rule table
    Then the rwb-decision and rwb-access fakes answer the paths and payloads of 12.2 and 12.8
    Then a contract test fails on any drift between a fake and the document

  Scenario: AC7 The business rules of section 8 are each covered by a criterion (new, D-RCV-60)
    Given the business rules BR1 to BR8 of section 8 are in force
    When the contract baseline is reviewed against them
    Then BR1 holds: one REST base /api/recovery/case/v1 and no other service path
    Then BR2 holds: every consumed operation is described as consumed with its owner
    Then BR3 holds: events are named rwb.<short>.<Event>.v1 and carry the CloudEvents 1.0 envelope
    Then BR4 holds: the contract declares no rule table
    Then BR5 holds: each error response carries one envelope and one message ID
    Then BR6 holds: a package version not in force is declared as a non-retryable failure
    Then BR7 holds: the audit entry carries counts and times only
    Then BR8 holds: a schema change is additive within a major version

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the consumed operations of section 12 include one that changes a rule package version status
    When the document is reviewed against the ownership map
    Then a disallowed status change is declared as a consumed refusal with a message ID Not specified in the source documents (NEWAC-RWB-P3-E2041-CON-AC8)
    Then the document declares no operation that changes a package version status as provided by rwb-case
```

These eight criteria test the artefact only. No criterion restates a legacy acceptance criterion; the ten legacy criteria of RWB-E2-041 belong to RWB-P3-E2041-APP and RWB-P7-E2041-APP. The scope is rule package versions; the reference-data checklist and its report stay with RWB-E1-043.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/case/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | Events are named `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics, and carry the CloudEvents 1.0 envelope | DP-14; Template and Rules §R4 |
| BR4 | The contract declares no rule table and no rule registry of rwb-case, because the registry is P7's | DP-01; ASM-0069 |
| BR5 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR6 | A package version that is not in force is declared as a non-retryable failure, so no caller retries a case into a version that does not exist | DP-04; R-UNI-38; MSG-P3-027 |
| BR7 | The audit entry carries counts and times only: no case number, no party key and no case-level row, in JSON or in CSV | REQ-DRI-011; Architecture v5 slide 43 |
| BR8 | A schema change is additive within a major version; a breaking change is a new major version, and the registry rejects a backward-incompatible schema | Architecture v5 slide 42 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three case-side operations, the two events and the six consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the operations story and the wave 2 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-case | Owns the document, the AsyncAPI file, the activity contract and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Audit representative and the integration and QA team | Review and sign off the audit read shape, the CSV columns and the reconciliation rule |
| Tech lead of rwb-decision (P7) | Reviews the five consumed operations and the two consumed event types; owns their definitions |
| Tech lead of rwb-access (P4) | Reviews the authorise operation and the refusal mapping |
| Data steward | Confirms that no personal data field is declared in an event or in the audit entry |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Queue case page | `items[]` of the case resource with `id`, `caseNo`, `productGroup`, `status`, `queueId`, `ownerReference`, `entryDate`, `packageVersion`; `page`, `size`, `total` | Not specified in the source documents (DOR-RWB-P3-E2041-CON-7) |
| Case resource | `id`, `caseNo`, `productGroup`, `primaryPersonKey`, `status`, `entryDate`, `dpdAtEntry`, `exposureBand`, `totalOutstandingAtEntry`, `deviationOpen`, `legalHold`, plus `packageVersion` as the label of the version the case is pinned to, from `recovery_case` fields DF-CAS-001 to DF-CAS-023 | DF-CAS-001 to DF-CAS-023 |
| Case account link | `id`, `caseId`, `accountKey`, `isPrimary`, `linkedFrom`, `linkedTo`, from `case_account` fields DF-CAS-024 to DF-CAS-029 | DF-CAS-024 to DF-CAS-029 |
| Rule change audit entry | `packageCode`, `versionLabel`, `versionStatus`, `decisions`, `casesAffected`, `firstDecisionAt`, `lastDecisionAt`, `openCasesAtVersion`, `openCasesKeepingVersion`, from `rule_package` DF-REF-275, `rule_package_version` DF-REF-281 and DF-REF-282, and the decision record `rule_id` DF-DEC-004, `rule_version` DF-DEC-005 and `decided_at` DF-DEC-016 | DF-REF-275, DF-REF-281, DF-REF-282, DF-DEC-004, DF-DEC-005, DF-DEC-016 |
| Event payloads | IDs, codes, dates and counts only; no name, address, identity number or contact point | Not specified in the source documents (DOR-RWB-P3-E2041-CON-7) |
| Refusal | `code` "RULE_PACKAGE_NOT_IN_FORCE", `messageId` MSG-P3-027, the package code and the business date | Not specified in the source documents (DOR-RWB-P3-E2041-CON-7) |

The exact field-level schema of the case resource, of the queue case page and of the audit entry — types, lengths, required flags, the sort parameters and the CSV header order — is Not specified in the source documents (GAP-0718; ASM-1265). This baseline fixes the field names above and leaves the field-level detail to the review.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-case (P3); base `/api/recovery/case/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/queues/{queueId}/cases` | CasePage: query `productGroup`, `status`, `page`, `size` (default 50, max 200); items with the case fields of section 11 and the page total used as the impact count | Case record R, scope applied |
| GET | `/cases/{caseId}` | Case with `packageVersion`, the label of the version the case is pinned to | Case record R, scope applied |
| GET | `/admin/rule-change-audit` | CaseRuleChangeAuditPage: query `from` (required), `to` (required), `packageCode`, `format` (`json` default or `csv`), `page`, `size` (default 50, max 200); one entry per package version | Rules and parameters R |

Errors for all three: 400 bad query (MSG-P3-030), 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 404 case not found or out of scope (MSG-P4-003), 422 period end before start (MSG-GEN-003), 503 store down. The audit read answers `text/csv` when `format=csv`, with one header row and one row per package version and no case-level row.

The three operations are reads, so the Idempotency-Key rule that applies to every POST does not apply here, and the baseline states it so that no consumer sends the header. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/change-report` | P7 rwb-decision | The change report of a period and a package, as JSON or CSV |
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The package version load with its change checklist |
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | P7 rwb-decision | The four-eyes approval and its refusal with MSG-P3-022 |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The version in force, its status, its dates and its checksum |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decisions the case-side audit read is reconciled with, by `ruleId` and `ruleVersion` |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters right check behind every operation |

The five rwb-decision operations are P7's registry half and the authorise operation is P4's. None of the six is declared as provided by rwb-case.

#### 12.3 Events published

None. rwb-case publishes no event type for this story; the local decision-record library writes the record row and its `DecisionRecorded` message in the same transaction as the state change (DP-03), and the type belongs to P7.

#### 12.4 Events consumed

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Package code, version label, checksum, valid-from date; drops the cached KieBase and refreshes the version in force |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (ledger); every service publishes its own record | Decision record reference, `ruleId`, `ruleVersion`, final call, `decidedAt`; the audit read reconciles its counts against it |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = `case-{caseId}` | `rwb-case` | Input and signal schemas; search attributes CaseId, Stage, ProductGroup, QueueCode; the pinned `packageVersion` on the case |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Package code, facts and business date in; `ruleId`, `packageVersion` and outputs out; `NoPackageInForce` declared non-retryable with MSG-P3-027 |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Decision record with `ruleId` and `packageVersion`, the state change and the outbox row in one transaction |

#### 12.6 Schedules

None. The audit read and the impact count are request-driven; the rule promotion at 00:01 and the chain check at 02:00 are Schedules of rwb-decision and are not part of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| recovery_case | P3 (rwb_case) | Case resource, the queue case page and the pinned `packageVersion` |
| queue | P3 (rwb_case) | The queue of the case page the impact count is read from |
| case_account | P3 (rwb_case) | The account link counted as a case affected |

No rule table is named in the contract and no table of another service is read (DP-01). `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `approval` and `decision_log_entry` stay P7 rwb-decision's under ASM-0069 and appear only as consumed shapes.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock | `GET /admin/rule-packages/change-report`, `POST /admin/rule-packages/{packageCode}/versions`, `POST /admin/rule-package-versions/{versionId}/approve`, `GET /admin/rule-packages/{packageCode}/versions` and `GET /decision-log`; ALLOCATION "ALLOC-2026.11" in force with 24 rows loaded by "U-41" and approved by "U-51"; "ALLOC-2026.12" loaded with the checklist and approved on 2026-12-09, valid from 2026-12-10; "ALLOC-2026.13" loaded and never approved; RESTRUCTURE "RES-2026.12" with no rollback plan; PAYMENT_MATCH "PMT-2026.12" with test result FAILED; "ALLOC-2026.14" with verify date before the load; checksum "9f2c...e1b4"; 1 row changed, 0 added, 0 removed; 96 and 1,204 decisions, "ALLOC-031" 700 and "ALLOC-032" 600; a CSV answer; an empty answer with total 0; 409 for MSG-P3-022 and 422 for MSG-GEN-003 | App story, contract tests, wave 2 harness |
| rwb-access WireMock | `POST /authorise` with a granted answer for RW-COE, RW-RISK, RW-AUDIT and RW-PLATADM with Rules and parameters R, and a refused answer with MSG-P4-002 for RW-CASEOWN | App story, contract tests, wave 2 harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 6 consumed | Queue case page, case resource and audit read provided; five rwb-decision operations and the authorise operation consumed; one hop, 2 s timeout |
| Kafka | 0 published, 2 consumed | `rwb.decision.RulePackageInForce.v1` and `rwb.decision.DecisionRecorded.v1` |
| Temporal | 1 workflow, 2 activities | CaseWorkflow; EvaluateRules and RecordAndApply |
| File | None | The CSV answer is a REST response; no file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-case-v1.yaml` (OpenAPI 3.1) with the three operations (GET /admin/rule-change-audit included, published by this story) and the shared components, `asyncapi/rwb-case-consumed-v1.yaml` (AsyncAPI 3) with the two consumed message schemas, `contract/error-envelope.yaml`, the activity contract jar for CaseWorkflow, EvaluateRules and RecordAndApply, the refusal contract, the idempotency and versioning rules in the contract README, and the two WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The three case-side operations with the shapes of section 11; the audit entry, the page and the CSV column order.
3. The six consumed operations with their owners, the one-hop rule and the 2 s client budget.
4. AsyncAPI 3 document with the two consumed event types, their topics, the CloudEvents envelope and the registry versioning rule.
5. The refusal contract: `NoPackageInForce`, its `code`, its message ID and the non-retryable declaration on EvaluateRules.
6. Error envelope and the message-ID mapping, with the business texts copied unchanged from the legacy story.
7. The two fakes and the stub fixtures of section 12.8.
8. The six contract tests; a drift between a fake and the document fails the build.
9. Baseline tag and the consumer sign-off note from the app story, the wave 2 harness and the P7 and P4 owners.

**Feature switch.** The audit read is switched by the parameter `rwb.p3.rule-change-report` read through the parameters contract; off means the operation answers 404 and the contract declares the 404 response. The version pin, the impact count and the refusal are not a report and are not switched.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P3-E2041-APP | The three provided operations, the audit entry and the two fakes |
| RWB-ITG-E2041-ITG | The queue case page used as the impact count, the decision log read used as the reconciliation source and the two fakes |
| RWB-P7-E2041-APP (P7 rwb-decision) | The five consumed operations as rwb-case uses them; no P7 operation is claimed as provided |
| RWB-P4-E2041-APP (P4 rwb-access) | The authorise operation and the refusal mapping with MSG-P4-002 |

The deprecation window of a published field and the retention of the contract fakes are Not specified in the source documents (GAP-0720; ASM-1267).

**Done when.** The OpenAPI and AsyncAPI documents validate in the pipeline, the six contract tests pass, the two fakes answer every consumed path, and the app story, the operations story and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-030 | A request body or query fails schema validation | The request could not be read: {detail}. |
| MSG-GEN-003 | The audit read period ends before it starts | {field} cannot be before {other}. |
| MSG-P3-027 | No version is in force for a table an engine needs | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |
| MSG-P4-001 | No session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without the right reads an operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A case outside the reader's scope | This case is not in your scope. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-P3-022 and MSG-P7-003 are answered by rwb-decision and rwb-case under the registry contract and are declared here only as mapped responses.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Report list | The change report entries and the case-side audit entry of the period, with the counts and the two decision times |
| SCR-39 Rules and parameters | Export | The CSV answer with one header row and one row per package version, and no case-level row |
| SCR-39 Rules and parameters | No changes in the period | An empty list with total 0 and no error |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (CG-ALL-4385) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-4385) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (CG-ALL-4385) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (CG-ALL-4385) |
| SCR-02 Case list | List, filtered | The queue case page with `productGroup` and `status`, whose total is the impact count |
| SCR-02 Case list | Empty | Not specified in the source documents (CG-ALL-4384) |
| SCR-02 Case list | Loading | Not specified in the source documents (CG-ALL-4384) |
| SCR-02 Case list | Error | Not specified in the source documents (CG-ALL-4384) |
| SCR-02 Case list | No access | Not specified in the source documents (CG-ALL-4384) |

The screens are served by the gateway-bff composite route (DP-19), which calls the case operations and the rwb-decision operations in parallel, one hop each, and merges the answers. The composite route specification, the screen field list and the masking of customer fields are Not specified in the source documents (GAP-0720; ASM-1267); the document fixes the case side of the merge only. The audit read and its CSV export are kept as long as the decision records they summarise; the deprecation window of a published field and the retention of contract fakes are Not specified in the source documents (GAP-0720).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E2041-CON-01 | AC1 | Contract | The OpenAPI 3.1 document validates; the three case-side operations and their error responses are present |
| TC-P3-E2041-CON-02 | AC2 | Contract | The audit entry, the page and the CSV column order; no case number, party key or case-level row |
| TC-P3-E2041-CON-03 | AC3 | Contract | 401, 403, 404, 422 and 503 responses carry one envelope and a valid message ID |
| TC-P3-E2041-CON-04 | AC4 | Contract | The six consumed operations carry their owner, one hop and the 2 s budget; no P7 or P4 operation is declared as provided |
| TC-P3-E2041-CON-05 | AC5 | Contract | The two consumed events, the CloudEvents envelope, no personal data field, and the three task contracts with `NoPackageInForce` non-retryable |
| TC-P3-E2041-CON-06 | AC6 | Component | The nine contract tables are complete and each fake matches its consumed path; a drifted fake fails the build |
| TC-P3-E2041-CON-07 | AC6 | Component | Boundary: the three tables of 12.7 are owned by rwb_case; a read of a P7 rule table is refused at the boundary |
| TC-P3-E2041-CON-08 | AC7 | Contract | Each business rule BR1 to BR8 of section 8 has a contract check that passes on the baseline |
| TC-P3-E2041-CON-09 | AC8 | Contract | A disallowed status change is declared as a consumed refusal with a message ID Not specified in the source documents (NEWAC-RWB-P3-E2041-CON-AC8); no operation changes a version status as provided |

### 17. Guardrails

- No business value in the contract: the checklist items, the impact summary, the rollback plan, the package codes and the statuses stay data in rwb-decision, the parameters and the reference tables.
- No personal data in an event schema, an audit entry, an example or a fake: staff user IDs, counts and times only.
- The contract names only rwb-case tables and only operations owned by rwb-case; the registry tables and the five rwb-decision operations are consumed and documented as consumed (DP-01, ASM-0069).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13, DP-14).
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- A package version that is not in force is a declared failure, never a silent fallback to an older version (DP-04, R-UNI-38).
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | Rule change by validated package version with a checklist and rollback | The five consumed rwb-decision operations, the two consumed events, the pinned `packageVersion` on the case and the counts of the audit entry; the checklist itself is P7's | TC-P3-E2041-CON-01, TC-P3-E2041-CON-04, TC-P3-E2041-CON-05 |
| REQ-DRI-011 | Versioned tables with author and approver, and a count of decisions per version | The audit entry `versionLabel`, `decisions`, `casesAffected`, `openCasesAtVersion`, `openCasesKeepingVersion`; the decision record read as the reconciliation source | TC-P3-E2041-CON-02, TC-P3-E2041-CON-04, TC-P3-E2041-CON-06 |

### 19. Out of scope

- The implementation of the version pin, the impact count and the audit read (RWB-P3-E2041-APP).
- The registry half: the checklist, the approval checks, the effect counts, the change report and the rule package tables (RWB-P7-E2041-APP; ASM-0069).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the rwb-decision and rwb-access contracts are consumed and faked, never defined here.
- The reference table checklist fields and their report (RWB-E1-043); this contract covers rule package versions only, following the legacy key and the test cases although the FSD A2.16 examples use a reference-data version (GAP-0719; ASM-1266).
- The remaining rwb-case operations beyond the three this capability needs; they are published in the same service API file by their own stories.
- Deployment of this capability: the Helm values, the event subscription, the topics, the dashboards and the runbook. No deployment story is split from this legacy key, so the platform and DevOps stories of wave 2 carry them.
- The cross-service journey harness and its evidence (RWB-ITG-E2041-ITG).
- The field-level completeness of the audit entry and the CSV header (GAP-0718).
