# RWB-P4-E8007-CON Change a decision rule through the administration screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E8007-CON-16) |
| Contract version | Major version 1 in the path `/api/recovery/access/v1`; minor version not specified in the source documents (DOR-RWB-P4-E8007-CON-23) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-007 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 9 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member of the Collections and Recovery Tribe (RW-TRIBE, Tribe lead and squad members)**, I want **the published contract baseline of the rule-change request of `rwb-access`: an OpenAPI 3.1 document for the two operations, the `RuleChange` and `RuleChangeChecklist` schemas, the version state set of the technical specification, one RFC 9457 error envelope with its message IDs, the consumed authorise, parameters and registry reads with their owners, one hop and the 2 s budget, the contract tables of section 12 and the contract fakes**, so that **the app story, the gateway-bff route of SCR-39 and the audit consumer can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-case` or the rule registry of `rwb-decision` to be built, and no party redefines the checklist or the version states**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-007 belong to RWB-P4-E8007-APP, and the six criteria of section 7 test the document, the schemas, the state set, the envelope, the consumed declarations and the fakes.

The baseline is the record side of a rule change only. The registry's own operations — the version load, the version list, the dry run, the approval, the rollback and the change report — are `rwb-decision`'s (ASM-0040) and are declared here as consumed where this story reads them, and not at all where it does not.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy key answered the whole rule-change journey from the monolith's own tables, so the shape of a change, the meaning of a checklist and the set of version states were decided by whichever screen asked. In the target the governance of a rule is central in `rwb-decision` (Architecture v5 slide 27; Temporal and Drools design slide 15), and the administration service keeps the act of the analyst: a dated request that binds a version, its evidence and the role that must approve it. The app story, the SCR-39 route and the audit consumer each need that record to mean the same thing, including which item codes the checklist has and which states a version can be in, or every one of them will invent its own.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the platform library, the parameters contract of `rwb-case` and the registry of P7, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also fixes the two things audit asks of it. First, a change states its evidence as the registry answered it — the version label, the test result and the dry-run counts — so a printed change can be defended years later without re-running a scenario. Second, the version states a change can observe are the seven of the technical specification and no others, so a screen cannot show a state the registry does not have.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the two operations and the registry's version reads, and it is a consumer of this baseline.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The change is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the entry as that library publishes it and adds no field to the library's own schema.
- The version, its state, its label, its checksum, its test result and its dry-run counts are the registry's (`rwb-decision`, P7, ASM-0069); this document declares them as the fields of a consumed operation and names no rule table as this service's.
- The operations and their owners are taken from the ownership map only: the two change operations are P4's, the authorise operation this document consumes is P4's, and the parameters read and the two registry reads are P3's and P7's.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two operations with the shared components used across the `rwb-access` administration operations: the security scheme, the problem envelope, the identifier parameters and the change schema.
2. Fix the `RuleChange` schema and the `RuleChangeChecklist` schema, with the seven item codes of the technical specification as required properties and no optional item.
3. Fix the version state set of TSD P4 v3 T4 as the closed set of `versionState`, and the rule that only `LOADED` is accepted on the create.
4. Agree the error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the business texts copied unchanged from the message tables of the rule-change stories where the message already existed.
5. Declare the consumed operations as consumed, each with its owner, one hop and the 2 s client budget: the own authorise operation, the `rwb-case` parameters read and the two `rwb-decision` reads.
6. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
7. Add the contract tests: schema validation, the change and checklist shapes, the state set, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
8. Tag the baseline and hand it to RWB-P4-E8007-APP, the Epic 8 screen work of RWB-PLT-N001-CON and the audit consumer.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A checklist item is optional, renamed or added | The contract test fails; the set of seven items is closed | None | AC2 |
| X5 | A `versionState` value outside the seven of the technical specification is declared | The contract test fails | None | AC3 |
| X6 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X7 | An example, a fake or a schema carries a name, an e-mail address or a personal field | The review and the pipeline refuse the document | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 entry schema, the `rwb-case` parameters contract and the `rwb-decision` rule-package contract only |
| Negotiable | The field-level placement of the change inside the record entry is settled with audit and with the registry owner; the operations, the item codes, the states and the envelope are fixed |
| Valuable | Unblocks the app story, the SCR-39 route and the audit consumer on Day 1, and keeps the registry's own operations out of the `rwb-access` contract |
| Estimable | One OpenAPI document, one error envelope, two schemas, one state set, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Rule-change request contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the change-request half of the legacy journey is the dated request that binds a registry version, its evidence and its approving role into one record

  Scenario: AC1 The OpenAPI 3.1 document describes the two operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the rule change is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/rule-changes and GET /admin/rule-changes/{changeId} with the owner rwb-access
    Then the write names its security right Rules and parameters C, the read names Rules and parameters R, and each names its error responses: 401, 403, 409, 422 and 503 on the write, and 401, 403, 404 and 503 on the read
    Then no operation of another service is declared as provided by rwb-access

  Scenario: AC2 The change and the checklist are fixed (new, D-RCV-60)
    Given the RuleChange and RuleChangeChecklist schemas of the document
    When a change request is written against the document
    Then RuleChange carries changeId, packageCode, versionId, versionLabel, versionState, testResult, dryRunCounts, validFrom, reason, checklist, state, approverRole, canApprove, authorReference, parameterVersion and recordedAt
    Then state is fixed to REQUESTED and approverRole to RW-RISK
    Then RuleChangeChecklist declares the seven required items request, impact, testResult, approver, load, verify and rollbackPlan, and no item is optional
    Then the 422 of a missing item carries missingItem with the item code
    Then packageCode, versionId, validFrom and reason are required on the write and validFrom is a date

  Scenario: AC3 The version state set is the closed set of the technical specification (new, D-RCV-60)
    Given the versionState property of the document
    When a change request is written to POST /admin/rule-changes, or a change is read through GET /admin/rule-changes/{changeId}
    Then its values are exactly LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED
    Then the write accepts only LOADED and answers 409 with the state named for every other value
    Then the read declares versionState as the state the registry reports at the time of the read
    Then no state of a version is declared as written by rwb-access

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by the operation that declares it
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 409 carries MSG-GEN-004, 422 carries MSG-GEN-001 or MSG-P3-022, and 503 carries MSG-P7-003
    Then the 409 also declares versionState and the 422 of a checklist item also declares missingItem
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the parameters read and the two registry reads this service calls
    When the document is checked for the operations this service calls
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions and GET /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run are declared as consumed with the owner P7 rwb-decision
    Then each carries one hop and the 2 s client budget with a breaker
    Then no operation owned by rwb-case or by rwb-decision is declared as provided by rwb-access, and no rule table is named as this service's

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the registry fake answers a version in LOADED and one in IN_FORCE, and records every call so a refusal can assert that no call was made
    Then no schema, example or fake carries a name, an e-mail address or a personal field

  Scenario: AC7 A schema change is additive within major version 1 (new, D-RCV-60)
    Given the schemas of the document are at major version 1
    When a change is proposed to a schema of the document
    Then an added field keeps major version 1
    Then a removed, renamed or retyped field is declared as a new major version

  Scenario: AC8 Every business rule of section 8 is covered by a criterion and a test (new, D-RCV-60)
    Given the business rules table of section 8 lists the rules BR1 to BR11
    When the criteria of section 7 and the test cases of section 16 are read against that table
    Then each rule ID names at least one criterion and one test case of this story
    Then no rule is left without a criterion

  Scenario: AC9 A replay of a write with the same idempotency key records no second change (new, D-RCV-60)
    Given a change request has been written with an idempotency key
    When the same write is sent again with that same idempotency key
    Then no second change request is recorded
    Then the replay is answered with the outcome of the first write
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-007 belong to RWB-P4-E8007-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1, TC-E8-007-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5, TC-E8-007-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the message tables where the message exists | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4, TC-E8-007-CON-04 |
| BR4 | The change is a decision-record entry of DP-03: the contract describes the fields it carries and adds no field to the library's schema | DP-03; RWB-PLT-E1027-CON | AC2, TC-E8-007-CON-02 |
| BR5 | The contract declares no table of another service and no central ledger: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` are P7's | DP-01; ASM-0069 | AC5, TC-E8-007-CON-05, TC-E8-007-CON-07 |
| BR6 | The seven checklist items of TSD P4 v3 T6.3 are a closed set in the contract, and a missing item is named in the refusal | TSD P4 v3 T6.3; DF-REF-295; ASM-1572 | AC2, TC-E8-007-CON-02 |
| BR7 | The version states are the closed set of TSD P4 v3 T4, and only `LOADED` is accepted on the write | TSD P4 v3 T4 and T3.2 | AC3, TC-E8-007-CON-03 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC7, TC-E8-007-CON-08 |
| BR9 | No personal data in a schema, an example or a fake: references, codes, versions, dates and times only | NFR-040; FSD P4 v3 A2.18.3.2 | AC6, TC-E8-007-CON-06 |
| BR10 | The change states its evidence as the registry answered it: the version label, the test result and the dry-run counts are copied and never recomputed by a consumer | TSD P4 v3 T6.3; GAP-0868; ASM-1571 | AC2, TC-E8-007-CON-02 |
| BR11 | The identifier a consumer quotes is the change id, and the change id is opaque to every consumer but this service | ASM-1573 | AC1, TC-E8-007-CON-01 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the change and checklist schemas, the state set, the envelope and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the SCR-39 route and the audit consumer accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | A checklist item or a version state changes in the technical specification | The closed set changes and the change is reviewed with the registry owner and audit | In review |
| Baselined | Drift in a fake | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the change and checklist schemas, the state set, the envelope and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Audit representative and the centre of excellence | Review and sign off the checklist item codes, the evidence fields and the state set, as the parties that read a change after the fact |
| Tech lead of rwb-decision (P7) | Reviews the two reads as rwb-access uses them and owns the version, its states, its test result and its dry-run counts |
| Tech lead of rwb-case (P3) | Reviews the parameters read as rwb-access uses it; owns its definition |
| Security administrator and the platform owner of the authorise contract | Review the rights of the two operations and the refusal mapping with MSG-P4-002 |
| Data steward | Confirms that no personal data field is declared in the change, the examples or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Change | `changeId`, `packageCode`, `versionId`, `versionLabel`, `versionState`, `testResult`, `dryRunCounts`, `validFrom`, `reason`, `checklist`, `state`, `approverRole`, `canApprove`, `authorReference`, `parameterVersion`, `recordedAt` | BR4, BR11 |
| Checklist | `request`, `impact`, `testResult`, `approver`, `load`, `verify`, `rollbackPlan`, each required, from the seven items of TSD P4 v3 T6.3 and DF-REF-295 | BR6 |
| Version states | `LOADED`, `VALIDATED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED`, from TSD P4 v3 T4 and LOV-VERSION-STATUS; a closed set in the document, owned by P7's contract and never written here | BR7 |
| Registry evidence | `versionLabel` and `testResult` from DF-REF-281 and DF-REF-292, and `dryRunCounts` from DF-REF-293, passed through unchanged | BR10 |
| Refusal | `messageId` MSG-P4-002, MSG-P3-022, MSG-GEN-001 or MSG-GEN-004, with `missingItem` on a checklist refusal, `versionState` on a state refusal, and MSG-P7-003 on a record or registry failure | BR3 |

The field-level shape of `dryRunCounts` beyond what the registry's `DryRunResult` declares, the field-level placement of the change inside the decision record's `inputs_ref`, and the record code an administrative change is written under are Not specified in the source documents (GAP-0868; ASM-1573) and are confirmed with audit and with the registry owner before the baseline is tagged. The seven checklist items and the seven version states are document-sourced and are fixed here as closed sets.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/rule-changes` | `RuleChange` answer: body `packageCode`, `versionId`, `validFrom` (date), `reason` and `checklist` with the seven required items; `Idempotency-Key` required; `Location` of the read | Rules and parameters C |
| GET | `/admin/rule-changes/{changeId}` | The same `RuleChange` with `versionState` as the registry reports it at the time of the read | Rules and parameters R |

Errors on the write: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 409 a version not in `LOADED` with `versionState` named (MSG-GEN-004), 422 a required field empty or `validFrom` not a date (MSG-GEN-001) and a checklist item missing with `missingItem` (MSG-P3-022), 503 the change cannot be recorded or the registry is unavailable (MSG-P7-003). Errors on the read: 401 (MSG-P4-001), 403 (MSG-P4-002), 404 an unknown change id and 503 (MSG-P7-003), and no 409 or 422. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

The write is the only operation of this service that carries an `Idempotency-Key` requirement of its own, and the document states that a replay answers the first answer and creates no second change. A load is not a decision and records nothing (RWB-P4-AD011-APP); a change request records, and this document is the only place that record is described.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters C check of the write and the R check of the read, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameters version in force on the change date, carried on the change (DP-06) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The version of the body: its state, label, checksum, valid-from date, test result and dry-run counts |
| GET | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run` | P7 rwb-decision | The dry-run result of the version, with its counts and its overall test result |

None of the four is declared as provided by rwb-access. The two `rwb-decision` reads are the registry contract this story's metadata does not carry as a C dependency (GAP-0868; ASM-1571): they are declared as consumed against the registry's contract and its fake. The registry's approve, rollback, load and change-report operations appear in the document not at all, because this story calls none of them; the approval is the decision center's with RW-RISK, and an approval by the author is refused there with MSG-P7-002.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a change with its `changeId`, the package code, the version id and label, the test result, the dry-run counts, the valid-from date, the author reference, the approver role and the parameters version, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

The two events of `rwb-access`'s own topic (`AccessPolicyChanged` and `DoaLimitChanged`) belong to other stories of this service, and the rule-version event `rwb.decision.RulePackageInForce.v1` (EV-30) is the registry's promotion. This document declares the record message only, because it is the only event of the two operations.

#### 12.4 Events consumed

None. The state of a version is read on request and the promotion at 00:01 is `rwb-decision`'s Schedule, so the baseline declares no subscription and no inbox row.

#### 12.5 Workflows and activities

None. No workflow and no activity is part of this contract, and the `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only.

#### 12.6 Schedules

None. Both operations are request-driven, and the only Schedule of the rule lifecycle is the registry's promotion at 00:01.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role and class of the caller and of the author |
| `permission` | P4 (rwb_access) | The C and A letters in Rules and parameters |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The entry of a change, read by change id and written once |
| `idempotency_key`, `outbox_event`, `processed_event` | PLT library, created in rwb_access | The idempotency row and the outbox row of an entry; no inbox row |

No rule table is named as this service's and no table of another service is named in the contract (DP-01): `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` are P7 `rwb_decision`'s, `case` and `task` are P3's, and a version arrives as a document of a consumed operation and never as a schema read.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision registry fake | `GET /admin/rule-packages/{packageCode}/versions` answering version "ENTRY-2027.01" in `LOADED` with its label, checksum, test result `PASS` and dry-run counts, and version "ENTRY-2026.11" in `IN_FORCE`; the same version later `APPROVED` then `IN_FORCE`; `GET /admin/rule-package-versions/{versionId}/dry-run` answering the counts and the result; a 503 for the unavailable cases; a call record for the no-call assertion | App story, contract tests, audit consumer |
| authorise fake | `POST /authorise` with a granted answer for RW-COE with C, for RW-AUDIT with R and for RW-RISK with A and R, and a refused answer with MSG-P4-002 for RW-CASEOWN with R only on the write | App story, contract tests |
| parameters fake | `GET /admin/parameters` with the parameters version "PAR-2026.11" in force on 15 December 2026 | App story, contract tests |
| decision-record fake | The append of a change entry, the hash-link check, the read by change id, the replay by `Idempotency-Key` and a forced write failure | App story, contract tests |
| gateway-bff fake | The composite route of SCR-39 with the rule-versions panel, the change form, the checklist state and the change read, calling the two operations and the registry reads | Screen route |

The version labels of the fake follow the document's package-version form and are synthetic; no production payload and no real person reference is copied into a fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The change and its read provided; the authorise, parameters and two registry reads consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-rulechange-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml`, the `RuleChange` and `RuleChangeChecklist` schemas with their examples, the version state set as a named component, the versioning rules of section 12.1, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. There is no DP-04 and no DP-07 in the pattern set on purpose: the Drools kit and the evaluation are the registry's and the model-owning services', and the lists this contract fixes are technical-specification constants rather than a reference-data read.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two operations with the shapes of section 11; the change, the checklist and the identifier parameter.
3. The version state set as a closed enum, and the `LOADED`-only rule stated in the write's 409.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget.
5. The error envelope and the message-ID mapping, with the business texts copied unchanged from the message tables where the message exists.
6. The five fakes and the stub fixtures of section 12.8, including the call record of the registry fake.
7. The six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note from the app story, the screen route and the audit consumer.

**Feature switch.** Neither operation carries a flag of its own; the administration surface is switched by the service baseline of this service, and the document declares no flag, no parameter and no extra branch of its own.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8007-APP | The two operations, the change and checklist schemas, the state set and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-39) | The two operations as the change form and the change read call them, with `missingItem`, `versionState` and `canApprove` for the screen states |
| The audit consumer of the change record | The change fields, the evidence fields and the record message, as the evidence it reads |

The field-level placement of the change inside the record entry — and with it the field list the audit consumer can rely on — is Not specified in the source documents (GAP-0868; ASM-1573); it is settled with audit and with the registry owner, and the deprecation window of a published field is the versioning rule of BR8.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, and the app story, the screen route and the audit consumer have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters C writes, or without R reads | You cannot {action} here. Your role does not include it. |
| MSG-P3-022 | A checklist item is missing or empty | The change cannot be approved: {item} is missing or failed. |
| MSG-GEN-001 | A required field is empty, or `validFrom` is not a date | Enter {field}. |
| MSG-GEN-004 | The version is not in `LOADED` | Someone else changed this record. Reload it to see their change. |
| MSG-P7-002 | The author of the version asks the registry to approve it | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The change cannot be recorded, or the registry is unavailable | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text, taken unchanged from the message tables of the rule-change stories and from TSD P4 v3 T6.3 where the message already existed. MSG-P3-022 carries `{item}` filled with the item code, and MSG-P7-002 is the registry's answer and is declared here only because the screen shows it.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Versions | The registry's version list with the state, the label, the test result and the dry-run counts |
| SCR-39 Rules and parameters | Change form | The `RuleChangeChecklist` item list, the `validFrom` date and the `reason` |
| SCR-39 Rules and parameters | Checklist incomplete | The 422 of the envelope with MSG-P3-022 and `missingItem` |
| SCR-39 Rules and parameters | Not loadable | The 409 of the envelope with MSG-GEN-004 and `versionState` |
| SCR-39 Rules and parameters | Recorded | The `RuleChange` in state `REQUESTED` with `approverRole` `RW-RISK` and `canApprove` |
| SCR-39 Rules and parameters | Change read | The `RuleChange` with `versionState` of the read |
| SCR-39 Rules and parameters | Refused | The 403 of the envelope with MSG-P4-002 and no form |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (CG-ALL-5462) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-5462) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (CG-ALL-5462) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (CG-ALL-5462) |

The screens are served by the gateway-bff composite route (DP-19), which calls the two operations and the registry's version reads in parallel, one hop each, and merges the answers. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the document fixes the change side of the merge only, and the state on the change is what the route renders with.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-007-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the rights C and R and the five error responses are present; no foreign operation is provided |
| TC-E8-007-CON-02 | AC2 | Contract | The change and checklist schemas with the seven required items, `state` fixed to `REQUESTED`, `approverRole` to `RW-RISK`, and the required body fields with `validFrom` as a date |
| TC-E8-007-CON-03 | AC3 | Contract | The seven version states as a closed enum, `LOADED` as the only accepted value on the write, and no state written by rwb-access |
| TC-E8-007-CON-04 | AC4 | Contract | A 401, 403, 409, 422 and 503 response carry one problem envelope with a valid message ID, `missingItem` on a checklist refusal and `versionState` on a state refusal |
| TC-E8-007-CON-05 | AC5 | Contract | Four consumed operations with their owners P4, P3 and P7, one hop and the 2 s budget; none declared as provided; no rule table named |
| TC-E8-007-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; no name, e-mail address or personal field |
| TC-E8-007-CON-07 | AC5 | Contract | The tables of section 12.7 as declared: no rule table and no table of another service named as this service's |
| TC-E8-007-CON-08 | AC7 | Contract | A removed, renamed or retyped field declared without a new major version fails; an added field stays within major version 1 |
| TC-E8-007-CON-09 | AC8 | Contract | Every rule ID BR1 to BR11 of section 8 is named by at least one criterion and one test row of this story; no rule without a criterion |
| TC-E8-007-CON-10 | AC9 | Contract | A write sent twice with the same idempotency key records one change; the replay is answered with the outcome of the first write; idempotency key header name: Not specified in the source documents (NEWAC-RWB-P4-E8007-CON-AC8) |

### 17. Guardrails

- No business value in the contract: the checklist items and the version states are technical-specification constants fixed by the document, and the parameters version stays a read behind it.
- No personal data in a schema, an example or a fake: staff user references, codes, versions, dates and times only (BR9).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the registry, the case, the parameter and the ledger objects are consumed or absent, never named as this service's (DP-01, BR5).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- The registry's own operations are declared as consumed or not at all: the contract adds no approve, load, rollback or change-report operation to `rwb-access`.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake and no real person reference appears in a fixture.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A closed set stays closed: a new checklist item or a new version state is a reviewed contract change and never a value a caller may invent.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated load to production with a version stamp and no code release, and rolls back by one call | The change with its version label, its state and its evidence; the record message that carries them | TC-E8-007-CON-01, TC-E8-007-CON-02 |
| REQ-CWC-014 | A load is validated for schema, overlapping rows, unreachable rows, a missing default row and a set of test cases before it takes effect | The seven-item checklist as a closed set, the `LOADED`-only rule and the test result and dry-run counts on the change | TC-E8-007-CON-02, TC-E8-007-CON-03 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold and limit, versioned | The `rwb-case` parameters read as consumed and the `parameterVersion` on the change | TC-E8-007-CON-05 |
| REQ-ACA-013 | Full administration screens are available to the administrator, with their rights | The two operations and their rights, the refused caller and the screen states of section 15 | TC-E8-007-CON-04, TC-E8-007-CON-05 |

The requirement IDs are the rows this story serves, taken from the Program and Epic 1 BRDs and the FSD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this story.

### 19. Out of scope

- The implementation of the change request and its read (RWB-P4-E8007-APP).
- The registry's own contract: the version load, the version list, the dry run's implementation, the approval, the rollback, the change report, the checksum and the version states as written by their owner (`rwb-decision`, P7, ASM-0040). The two reads this contract consumes are declared as consumed and faked, never defined here.
- The load gate of RWB-P4-AD011-APP and the approval of RWB-P4-AD012-APP; this document repeats neither and adds no path to either.
- The Drools kit, the KieBase and any evaluation of a rule.
- The central ledger `decision_log_entry` and the query API over it.
- The screen SCR-39 itself, its other panels and its composite route specification (RWB-PLT-N001-CON and the Epic 8 screen work).
- The move of a delegation limit on SCR-41 and its contract (RWB-P4-E8008-CON).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The audit consumer's own report and its evidence pack.
- The cross-service journey harness and its evidence.
