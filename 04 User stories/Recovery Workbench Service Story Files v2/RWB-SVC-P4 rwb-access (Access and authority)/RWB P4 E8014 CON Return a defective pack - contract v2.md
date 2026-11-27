# RWB-P4-E8014-CON Return a defective pack

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8014-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P4-E8014-CON-16) |
| Contract version | v1 (major version 1, `/api/recovery/access/v1`, section 12.1) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-014 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the pack check and return gate of `rwb-access`: an OpenAPI 3.1 document for the check and the read, the `PackCheck`, `PackRow`, `DefectItem`, `PackCheckAnswer` and `PackCheckSummary` schemas with the three check codes PC-ENT, PC-SCP and PC-MSK and the two verdicts, one RFC 9457 error envelope with its message IDs, the consumed authorise and parameters operations with their owners and the 2 s budget, the contract tables of section 12 and the four contract fakes**, so that **the app story, the SCR-39 route and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-case` or the matrix stories of this service to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-014 belong to RWB-P4-E8014-APP, and the nine criteria of section 7 test the document, the schemas and the check codes, the verdict set, the envelope, the consumed declarations, the fakes, the change rule, the 404 answer and the repeat decision.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story checked a pack inside a screen of the monolith, where the rows it read and the decision log it wrote were tables of one schema and no other consumer existed. In the target the rows are this service's and the record is a shared topic, and the screen is a route of the gateway that no longer shares a process with the check.

Two things must therefore be fixed once. The first is the vocabulary of a verdict: what a defect is, what a check code names, and which field of which table a rule reference points at — because the app story, the screen and the harness all have to agree on it, and a defect that is named differently in two places is a defect an owner cannot act on. The second is the boundary: the check answers a verdict and applies nothing, and the load of a matrix version stays with the administration stories of this service (BR9).

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the parameters contract of `rwb-case` and the local decision-record library, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also states the one thing it is not: it defines no matrix version, no masking profile, no role and no pack content. Those rows are other stories' of this service, and this document only names them in a rule reference.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path and the topic follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the two operations behind SCR-39 Rules and parameters, and it is a consumer of this baseline.
- The rows the document names are described by TSD P4 v3 T3.1: `role` DF-REF-034 to DF-REF-039, `permission` DF-REF-040 to DF-REF-044 (`capability_area` DF-REF-042, `letters` DF-REF-043, `matrix_version` DF-REF-044) and `masking_rule` DF-REF-198 to DF-REF-204 (`role_code`, `field_id`, `unmasked`, `masking_version`). This document names those fields in a rule reference and defines none of them.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The verdict entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the fields the entry carries and no field of another service.
- The operations and their owners are taken from the ownership map only: the two operations of this document are P4's, the authorise operation is P4's and the parameters read is P3's. The three check codes and the two verdicts are Not specified in the source documents (GAP-2288; ASM-3789) and are fixed here.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the check and the read with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters and the five schemas.
2. Fix the `PackCheck` request: `packVersion`, `ownerRole`, `capabilityArea` and `rows[]` of `PackRow`, with `rowType` one of `PERMISSION`, `SCOPE` and `MASKING`, `rowNo`, `roleCode` and the fields the row type carries — `capabilityArea` and `letters` for a permission row, `scope` for a scope row, `fieldId` and `unmasked` for a masking row.
3. Fix the `PackCheckAnswer`: `packCheckId`, `packVersion`, `ownerRole`, `capabilityArea`, `state`, `ruleVersion`, `defectCount`, `defects[]` of `DefectItem`, `decidedAt`, and the warning of a break-glass grant where one is active.
4. Fix the `DefectItem`: `checkCode` one of PC-ENT, PC-SCP and PC-MSK, `rowRef` with the row type, the row number and the role code, `field` and `ruleRef` — the reference of the row in force or of the parameter row the defect breaks — and no message ID, because a defect is not a catalogue message (GAP-2288; ASM-3789).
5. Fix the `PackCheckSummary` and the query of the read, with the page default and maximum held as parameter rows behind the contract.
6. Fix the verdict set: `ACCEPTED` and `RETURNED`, and state in the document that a check applies nothing, that a `RETURNED` pack is not stored as a version, and that a decided `packVersion` of an owner role is never decided twice.
7. Agree the error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed and MSG-GEN-002 and MSG-GEN-004 carried as message IDs only.
8. Declare the consumed own authorise operation and the `rwb-case` parameters read as consumed, each with its owner, one hop and the 2 s client budget, and declare that no matrix, masking, role or rule-package operation is provided or consumed here.
9. Publish the contract tables of section 12 (nine sub-tables) and the four contract fakes.
10. Add the contract tests: schema validation, the five schemas and their required fields, the three check codes and the two verdicts, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
11. Tag the baseline and hand it to RWB-P4-E8014-APP, the SCR-39 route of RWB-PLT-N001-CON and the harness of the wave 4 administration journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares a matrix, masking or role operation as provided here | The review refuses the document; the operation is declared as neither provided nor consumed | None | AC1, AC5 |
| X3 | A response of 401, 403, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A schema carries a name, an e-mail address or a user reference in a defect, a row or an answer | The contract test fails; the review refuses the document | None | AC2, AC6 |
| X5 | A check code outside PC-ENT, PC-SCP and PC-MSK, or a verdict outside `ACCEPTED` and `RETURNED`, is declared | The review refuses the document | None | AC3 |
| X6 | The document declares a matrix version, a masking profile or a role as written by the check, or declares a pack as stored | The review refuses the document | None | AC3, AC5 |
| X7 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the TSD P4 field set and the P3 and P4 contracts only |
| Negotiable | The pack version label shape, the personal-area parameter and the page bounds are parameter rows behind the document; the base, the paths, the check codes and the envelope are fixed |
| Valuable | Unblocks the app story, the SCR-39 route and the harness on Day 1, and fixes what a named defect is before two teams name it differently |
| Estimable | One OpenAPI document, one error envelope, nine contract tables, four fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Return a defective pack contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access model is held by rwb-access and the pack check applies nothing
  Given the pack check is request-driven: it runs on the submission of a pack through the administration screen, starts no workflow and owns no Schedule
  Given the freshness of an ACE data product is left to rwb-source-data and VR-P4-025-1 is not implemented in rwb-access

  Scenario: AC1 The OpenAPI 3.1 document describes the check and the read (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the pack check and return gate is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/pack-checks and GET /admin/pack-checks with the owner rwb-access
    Then the check names Rules and parameters C and the read names Rules and parameters R, the holder of each being Not specified in the source documents (GAP-2290), both name their error responses 401, 403, 409, 422 and 503, and no operation carries an approve leg
    Then the check requires an Idempotency-Key and the read is a read that carries none
    Then no operation of another service is declared as provided by rwb-access

  Scenario: AC2 The five schemas are fixed and carry no person (new, D-RCV-60)
    Given the PackCheck, PackRow, DefectItem, PackCheckAnswer and PackCheckSummary schemas of the document
    When the contract tests run against the schemas of the document
    Then the request carries packVersion, ownerRole, capabilityArea and rows, all required, and each row carries rowType, rowNo and roleCode
    Then a PERMISSION row carries capabilityArea and letters, a SCOPE row carries scope, and a MASKING row carries fieldId and unmasked
    Then the answer carries packCheckId, packVersion, ownerRole, capabilityArea, state, ruleVersion, defectCount, defects, decidedAt
    Then a DefectItem carries checkCode, rowRef of row type, row number and role code, field and ruleRef, and no message ID
    Then the summary carries the same verdict fields and page, size and total
    Then no schema declares a name, an e-mail address or a user reference, and page and size are read from the parameters contract and never from code

  Scenario: AC3 The check codes and the verdict set are fixed and the check applies nothing (new, D-RCV-60)
    Given the check codes and the verdict set of the document
    When the contract tests run against the check codes and the verdict set of the document
    Then checkCode is one of PC-ENT, PC-SCP and PC-MSK
    Then state is one of ACCEPTED and RETURNED
    Then the three codes are defined in the document as: an entitlement defect, a scope defect and a masking-coverage defect
    Then the document states that a check writes no permission, role or masking_rule row and stores no pack
    Then the document states that a decided packVersion of an owner role answers 409 and is never decided twice
    Then the document names no capability area, no role code, no letter, no scope and no personal-area value
    Then no workflow and no Schedule is declared for the capability

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 409 carries MSG-GEN-004, 422 carries MSG-GEN-001 and MSG-GEN-002, and 503 carries MSG-P7-003
    Then no operation declares a second error shape and no message ID outside this list is declared
    Then the wording of MSG-GEN-002 and MSG-GEN-004 is Not specified in the source documents (GAP-2291), and a defect item carries no message ID

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation and the parameters read this service calls
    When the contract tests run against the consumed declarations of the document
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then no matrix, masking, reference-data, delegation, rule-package or case operation appears as provided or consumed
    Then no operation owned by rwb-case, rwb-decision, rwb-document or rwb-litigation is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the four contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the decision-record fake answers an appended verdict, a replayed key and a forced failure
    Then no schema, example or fake carries a name, an e-mail address or a user reference

  Scenario: AC7 A schema change is additive within major version 1 (new, D-RCV-60)
    Given the schemas of the document at major version 1
    When a change to a schema is proposed
    Then a change that adds a field is additive within major version 1
    Then a removed, renamed or retyped field is declared as a new major version

  Scenario: AC8 An answer of 404 from either provided operation is one problem envelope (new, D-RCV-60)
    Given the 404 response of the POST and GET operations of the document
    When a 404 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then the messageId of the 404 is Not specified in the source documents (NEWAC-RWB-P4-E8014-CON-AC8)

  Scenario: AC9 A decision the model does not allow is refused with 409 (new, D-RCV-60)
    Given a pack version of an owner role that is already decided
    When a second decision is submitted for that packVersion
    Then the answer is 409 of the one problem envelope carrying MSG-GEN-004
    Then the first verdict of that packVersion stands and no second verdict is recorded
```

These nine criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-014 belong to RWB-P4-E8014-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1; TC-E8-014-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5; TC-E8-014-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4; TC-E8-014-CON-04 |
| BR4 | The schemas carry the fields of this gate and no field of another service: no case, no document, no rule package and no delegation limit | DP-01; Ownership Map v1 | AC2; TC-E8-014-CON-02 |
| BR5 | A defect names a check code, a row, a field and the rule it breaks, and never a person and never a message | RWB-E8-014 AC1; ASM-3789 | AC2; TC-E8-014-CON-02 |
| BR6 | The verdict set is `ACCEPTED` and `RETURNED`; a check applies nothing and stores no pack | FSD P4 v3 A2.25; ASM-3789 | AC3; TC-E8-014-CON-03 |
| BR7 | A decided pack version of an owner role is never decided twice; the repeat is a 409 and the corrected pack is a new version | ASM-3789 | AC3; TC-E8-014-CON-03 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC7; TC-E8-014-CON-07 |
| BR9 | A write requires an `Idempotency-Key`; a replay answers the first answer and appends no second entry | Architecture v5 slide 42; DP-09 | AC1; TC-E8-014-CON-01 |
| BR10 | The contract declares no workflow, no activity and no Schedule for the capability | Architecture v5 slide 14; TSD P4 v3 T5.3 | AC3; TC-E8-014-CON-03 |
| BR11 | The role codes, capability areas, letters and scopes a row names are values of the model tables and left to the app story; this document declares their shape and no value | TSD P4 v3 T3.1 and T3.2; ASM-3791 | AC3; TC-E8-014-CON-03 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the five schemas, the three check codes and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the SCR-39 route and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a check code or a verdict is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The parameters read or the authorise answer changes | Baselined, with the client budget and the stub restated |

The verdict set the document fixes is `ACCEPTED` and `RETURNED`, written once per pack version. The lifecycle of a pack before its check and the lifecycle of a matrix version after it — including the load, the approval and the rollback — are other stories' of this service and are not declared here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the five schemas, the check codes and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator | Reviews the two rights, the three check codes and the verdict set as the owner of the matrix |
| Compliance and PDPA officer | Reviews the masking-coverage check code and the absence of a person in a defect |
| Tech lead of rwb-case (P3) | Reviews the parameters read as `rwb-access` uses it; owns its definition |
| Internal audit | Reviews the verdict fields, the rule version and the stable order of the read |
| Data steward | Confirms that no name, e-mail address or user reference is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `PackCheck` request | `packVersion` (a label of the shape in force), `ownerRole` (a role code), `capabilityArea` (an area code of the matrix), `rows[]` of `PackRow`; all required | BR4 |
| `PackRow` | `rowType` (`PERMISSION`, `SCOPE` or `MASKING`), `rowNo` (a whole number), `roleCode`; and `capabilityArea` and `letters` for a permission row, `scope` for a scope row, `fieldId` and `unmasked` for a masking row | BR11 |
| `DefectItem` | `checkCode` (`PC-ENT`, `PC-SCP` or `PC-MSK`), `rowRef` of row type, row number and role code, `field`, `ruleRef` | BR5 |
| `PackCheckAnswer` | `packCheckId`, `packVersion`, `ownerRole`, `capabilityArea`, `state` (`ACCEPTED` or `RETURNED`), `ruleVersion`, `defectCount`, `defects[]`, `decidedAt` | BR6 |
| `PackCheckSummary` | `items[]` of the verdict fields above with `defects[]`, `page`, `size`, `total` | BR6 |
| Rows as consumed by a rule reference | `role` DF-REF-034 to DF-REF-039, `permission` DF-REF-040 to DF-REF-044, `masking_rule` DF-REF-198 to DF-REF-204 | BR11 |
| Record event | `rwb.decision.DecisionRecorded.v1` with the entry of a verdict, from the DP-03 library | BR6 |
| Refusal | `messageId` MSG-P4-001 on a 401, MSG-P4-002 on a 403, MSG-GEN-004 on a 409, MSG-GEN-001 and MSG-GEN-002 on a 422 and MSG-P7-003 on a 503 | BR3 |

The exact field set of `ruleRef`, the shape of the pack version label and the record code of a verdict are Not specified in the source documents (GAP-2288; ASM-3789): FSD P4 v3 A2.25 names the intent and two rules (VR-P4-025-1, BR-P4-025) and no operation and no field, the legacy story names the rule-version endpoints of other keys, and TSD P4 v3 T-A declares no pack operation. The personal capability areas the masking-coverage check needs are a parameter row and are named in no source either (GAP-2288; ASM-3791): the document declares the parameter and not its value; the three check codes and the verdict set are fixed in section 7 (AC3).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/pack-checks` | `Idempotency-Key` header in; `PackCheck` in; `PackCheckAnswer` out in state `ACCEPTED` or `RETURNED` with `packCheckId`, `ruleVersion`, `defectCount`, `defects` and the `Location` of the read | Rules and parameters C; `Idempotency-Key` required |
| GET | `/admin/pack-checks` | `PackCheckSummary` out: `items` of one owner role with `packVersion`, `capabilityArea`, `state`, `ruleVersion`, `decidedAt`, `defectCount` and `defects`, paged, filtered by `ownerRole` and `state` | Rules and parameters R, scope applied |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 409 the pack version of the owner role is already decided (MSG-GEN-004), 422 a required field empty, a label of the wrong shape or `rows` above the pack row limit (MSG-GEN-001, MSG-GEN-002), 503 the parameters read fails or the verdict entry cannot be written (MSG-P7-003). The check is a write of a verdict and not of a row of the model, so every request carries an `Idempotency-Key` and a replay answers the first answer with no second entry (BR9); the read carries none. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The C check behind the submit and the R check behind the read, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The personal capability areas, the pack row limit, the page bounds and the check rule-set label, with the version in force (DP-06) |

Neither is declared as provided by rwb-access. No matrix, masking, reference-data, delegation, rule-package or case operation appears in this document as provided or consumed.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a verdict with its pack version, owner role, capability area, verdict, rule version and defect list, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This document declares the record message only. `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's and `rwb.access.DoaLimitChanged.v1` is RWB-P4-E8008-APP's, and a pack check publishes neither: a check changes no row of the model, so there is nothing for the service to announce.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, and the two operations of this contract need no subscription. The document declares no inbox and no consumer group, and no case, document or rule-package event is consumed.

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: the check is synchronous and short, and the returned-packs list of the screen is not a workflow task (BR10).

#### 12.6 Schedules

None. Both operations are request-driven, and the access review Schedule of `rwb-access` (JOB-18) belongs to RWB-P4-AD008-APP and not to this document.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code, class and default scope a rule reference names |
| `permission` | P4 (rwb_access) | The capability area, letters and `matrix_version` a rule reference names |
| `masking_rule` | P4 (rwb_access) | The masking profile a rule reference names |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The verdict entry the record event carries and the list the read answers |
| `idempotency_key` | PLT library, created in rwb_access | The stored request and answer of a check, so one key answers one verdict (DP-09; ASM-0074) |

No table of another service is named in the contract (DP-01): `lov_value`, `reference_version` and `reference_row` are P3 rwb_case's; `delegation_limit` and `role_conflict` are this service's but belong to RWB-P4-AD016-APP and RWB-P4-AD005-APP and are named on no path of this document; `case`, `document` and `rule_package_version` are named nowhere (BR4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` with a granted answer for RW-COE with C and for RW-AUDIT and RW-LITOFF with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-PHONECOL with a dash | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the personal capability areas, the pack row limit, the page bounds and the check rule-set label at the version in force, and a 503 | App story, contract tests |
| decision-record fake | The append of a verdict, the hash-link check, a seeded chain of packs "AP-2027.03" and "AP-2027.06", the replay of a stored key and a forced failure | App story, contract tests |
| gateway-bff fake | The composite route of SCR-39 with the returned packs of the owner role, the pack form and the defect panel | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The check and the read provided; the authorise and parameters operations consumed; one hop, 2 s timeout |
| Kafka | 1 event type published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | A pack is a JSON body of rows; no file input and no file output |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-pack-check-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml`, the five schemas with their examples, the check-code and verdict rule and the versioning rules in the contract README, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two operations with the shapes of section 11: the request with its three row types, the answer with its defect list, and the paged read.
3. The check codes and the verdict set of BR5 and BR6, stated in the document and in the contract README, with the meaning of each code and the rule that a check applies nothing.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget, and the explicit statement that no model operation is provided here.
5. The error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the texts of the legacy messages and MSG-GEN-002 and MSG-GEN-004 as IDs only.
6. The four fakes and the stub fixtures of section 12.8, including the seeded chain and the forced record failure.
7. The six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note from the app story, the SCR-39 route and the harness.

**Feature switch.** Both operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8014-APP | The two provided operations, the five schemas, the three check codes and the four fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-39) | The check and the read as the pack form and the defect panel call them |
| The harness of the wave 4 administration journey | The verdict, the defect list, the rule version and the times, as the evidence it records |

The shape of `ruleRef` and the record code of a verdict are Not specified in the source documents (GAP-2288; ASM-3789) and are confirmed with the security administrator and the decision-record library owner before the operations are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the four fakes answer every declared path, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters C submits, or a role without R reads | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, or `packVersion` is not of the shape in force | Enter {field}. |
| MSG-GEN-002 | `rows` is above the pack row limit, or `size` is above the page maximum | Not specified in the source documents (GAP-2291; ASM-3795) |
| MSG-GEN-004 | The pack version of the owner role is already decided | Not specified in the source documents (GAP-2291; ASM-3795) |
| MSG-P7-003 | The parameters read fails, or the verdict entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed. MSG-GEN-002 and MSG-GEN-004 carry a message ID and no text in this baseline, because no source read for this work package states their wording; the message catalogue supplies it before the operations are frozen.

Epic design sign-off for EP08 is not recorded in the source documents: Not specified in the source documents (DOR-RWB-P4-E8014-CON-14). Confirm the sign-off in the epic design record before the story leaves Draft status.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Returned packs, list | The read of `state=RETURNED` with the pack version, the verdict and the defect count |
| SCR-39 Rules and parameters | Returned pack, defects | The `defects` of one check with the check code, the row, the field and the rule |
| SCR-39 Rules and parameters | Accepted packs, list | The read of `state=ACCEPTED` with the rule version of each verdict |
| SCR-39 Rules and parameters | Pack, form | `PackCheck` with the three row types and the `Idempotency-Key` of the submit |
| SCR-39 Rules and parameters | Pack, refused | The 403 of the envelope with MSG-P4-002 |
| SCR-39 Rules and parameters | Pack, malformed | The 422 of the envelope with MSG-GEN-001 or MSG-GEN-002 |
| SCR-39 Rules and parameters | Pack, already decided | The 409 of the envelope with MSG-GEN-004 and a reload action |
| SCR-39 Rules and parameters | Not recorded | The 503 of the envelope with MSG-P7-003 and a retry that reuses the same `Idempotency-Key` |
| SCR-39 Rules and parameters | List, empty | An empty `items` with total 0 and no error |

The screens are served by the gateway-bff composite route (DP-19), which shows the returned packs of the caller's owner role and calls the two operations of this contract, one hop each. The composite route specification, the panel split and the screen field list belong to RWB-PLT-N001-CON; the document fixes the check side of the merge only. The load and the approval of a matrix version are other stories' and are not part of this document.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-014-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the rights C and R, the five error responses, the `Idempotency-Key` on the write and the absence of a provided foreign operation are present |
| TC-E8-014-CON-02 | AC2 | Contract | The five schemas and their required fields; the three row types and their own fields; the `DefectItem` fields; no name, e-mail address or user reference |
| TC-E8-014-CON-03 | AC3 | Contract | The three check codes, the two verdicts, the statement that a check applies nothing, the decided-version 409 and the absence of a workflow and a Schedule |
| TC-E8-014-CON-04 | AC4 | Contract | A 401, 403, 409, 422 and 503 response carry one problem envelope with a valid message ID, and no other message ID is declared |
| TC-E8-014-CON-05 | AC5 | Contract | Two consumed operations with their owners P4 and P3, one hop and the 2 s budget; no model operation declared as provided or consumed |
| TC-E8-014-CON-06 | AC6 | Component | The four fakes match the document; a drifted fake fails the build; no schema or fake carries a name or a user reference |
| TC-E8-014-CON-07 | AC7 | Contract | The schema change rule is stated; an added field is additive and a removed, renamed or retyped field is a new major version |
| TC-E8-014-CON-08 | AC5 | Contract | The five tables of section 12.7 each carry their P4 owner and contracted use; no table of another service is named on any path or in any row |
| TC-E8-014-CON-09 | AC8 | Contract | A 404 from either provided operation carries one problem envelope; its message ID is Not specified in the source documents (NEWAC-RWB-P4-E8014-CON-AC8) |
| TC-E8-014-CON-10 | AC9 | Contract | A second decision of a decided packVersion answers 409 with MSG-GEN-004 and the first verdict stands |

The ten cases test the baseline and only the baseline. The legacy test cases of this key, TC-E8-014-01 to TC-E8-014-04, and the five new application cases TC-E8-014-05 to TC-E8-014-09, are owned by RWB-P4-E8014-APP and are not repeated here.

### 17. Guardrails

- No business value in the contract: the personal capability areas, the pack row limit and the page bounds stay parameter rows behind the document, and the role codes, capability areas, letters and scopes stay rows of the model tables (BR11).
- No personal data in a schema, an example or a fake: role codes, row references, check codes, field ids, labels and times only, and no user reference in any answer (BR5).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; a case, a document, a rule package and the delegation table are absent, never named as this service's (BR4).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- A check applies nothing: the document states that no permission, role or masking row is written and that no pack is stored (BR6).
- A decided pack version is never decided twice, and the repeat is a declared 409 rather than an undeclared second verdict (BR7).
- Every example in the document is synthetic; no matrix version, no pack and no production payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `Idempotency-Key` is refused by the contract, and a replay never appends a second entry.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ACA-003 | The role to permission matrix is the only source of what a role may see and do | The PC-ENT check code, the `ruleRef` of a defect and the `matrix_version` of the verdict | TC-E8-014-CON-02, TC-E8-014-CON-03, TC-E8-014-CON-08 |
| REQ-ACA-005 | Personal data is masked by role on every screen | The PC-MSK check code and the `unmasked` field of a masking row | TC-E8-014-CON-02, TC-E8-014-CON-03 |
| REQ-ACA-007 | Access outside the authority matrix is refused and the refusal is recorded | The `RETURNED` verdict with its defect list as the declared refusal, and the record event of section 12.3 | TC-E8-014-CON-01, TC-E8-014-CON-04 |
| REQ-ACA-009 | A user sees only what the role and scope allow | The PC-SCP check code and the `scope` field of a scope row | TC-E8-014-CON-02, TC-E8-014-CON-03 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The two operations as the SCR-39 route consumes them, with the refusal shapes | TC-E8-014-CON-04, TC-E8-014-CON-05 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold and name, versioned | The consumed parameters read and the `ruleVersion` label of every verdict | TC-E8-014-CON-05, TC-E8-014-CON-06 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 return a defective pack and the record of the result with its rule version | Sections 4, 7 (AC1, AC3), 11, 12.1, 12.3 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7 (AC4), 12.1, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 7 (AC1, AC5), 10, 12.1, 14 |
| The legacy data rows `decision_log_entry`, `rule_row` and `role` | Section 11, with `role` kept as a rule reference and the others named as their owners' |
| The legacy screens SCR-39 and SCR-41 as the story named them | Section 15, carried to SCR-39 Rules and parameters |
| Legacy key RWB-E8-014, story RWB-P4-E8014-APP, contract RWB-P4-E8014-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the check and the read (RWB-P4-E8014-APP).
- The load, the approval and the rollback of a permission matrix version (RWB-P4-AD002-APP, RWB-P4-AD010-APP, RWB-P4-AD013-APP), the scope table (RWB-P4-AD003-APP) and the masking profile load (RWB-P4-AD004-APP).
- The separation-of-duty check at sign-in and the `role_conflict` table (RWB-P4-AD005-APP).
- The delegation of authority table, its load and its lookup (RWB-P4-AD016-APP and the delegation stories).
- The rule package store, the rule-version load and approval (RWB-P4-AD011-APP, RWB-P4-AD012-APP) and the change checklist of TSD P4 v3 T6.3.
- The screen SCR-39 Rules and parameters, its other panels and its composite route specification (RWB-PLT-N001-CON).
- The central decision ledger, the query API over `rwb_decision` and the chain verification (P7 `rwb-decision`).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the authorise operation and the `rwb-case` parameters read are consumed and faked, never defined here.
- The pack's own content and the litigation pack of FEAT-LIT-05 (P4 litigation and P5 `rwb-document`).
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
