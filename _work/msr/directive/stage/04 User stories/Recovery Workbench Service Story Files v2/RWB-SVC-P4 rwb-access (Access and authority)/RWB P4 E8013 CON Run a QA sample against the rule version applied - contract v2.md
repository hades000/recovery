# RWB-P4-E8013-CON Run a QA sample against the rule version applied

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E8013-CON-16); the squad sizes it at refinement |
| Contract version | Major version 1 (path `/api/recovery/access/v1`); minor version Not specified in the source documents (DOR-RWB-P4-E8013-CON-23) |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | P7 rwb-decision (Service Contract Catalog v2; rule-model and period reads, to be confirmed with the P7 owner) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-013 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **solution architect**, I want **the published contract baseline of the QA sample of `rwb-access`: an OpenAPI 3.1 document for the run and the read, the `QaSampleRequest`, `QaSampleRun` and `QaSampleItem` schemas with the run state, the verdict and the reason-code sets, one RFC 9457 error envelope with its message IDs, the consumed authorise, parameters and two `rwb-decision` operations with their owners and the 2 s budget, the contract tables of section 12 and the six contract fakes**, so that **the app story, the SCR-39 route, the `rwb-decision` team and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-case` or `rwb-decision` to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-013 belong to RWB-P4-E8013-APP, and the six criteria of section 7 test the document, the schemas and the state and code sets, the envelope, the consumed declarations and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story sampled decisions and read rule versions inside a screen of the monolith, where the decision log, the rule rows and the panel were rows of one schema and no other service had to agree on what "the version that was in force" meant. In the target the ledger and the registry are `rwb-decision`'s (Architecture v5 slides 14 and 41; ADR-017; ADR-022), and an assurance sample of the access service has to reach them as two calls and has to leave a record that audit can read years later.

Two things must therefore be fixed once. The first is the boundary: which service owns the ledger and the versions (P7) and which owns the sample, the verdicts and the run record (this service). The second is what a verdict says: the decision entry it tested, the rule id and rule version that were recorded on it, PASS or FAIL, and **one reason code** — and never a person, a case narrative or a re-evaluation. A record that carried a case narrative would copy case data into a shared topic that every consumer of the decision record reads, and a contract that offered a "re-evaluate" field would invite a second opinion that the owning service is the only party entitled to give.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the `rwb-decision` reads, the parameters contract of `rwb-case` and the local decision-record library, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also states the one thing it is not: it defines no ledger entry, no rule package, no rule row and no rule test case, it declares no rule-version operation, and it names no table of `rwb-decision` as this service's. The two P7 operations appear in the document as consumed, which is what makes the split real — and the missing contract dependency for them is carried in the key's gap row rather than added to the metadata.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the two operations behind SCR-39 Rules and parameters, and it is a consumer of this baseline.
- The `rwb-decision` operations are described by Architecture v5 slide 14 and by the ownership map: the decision-log query and the rule-model read are P7's, and `GET /decision-log` and `GET /decision-log/{entryId}` are P7's api rows. The rule-version paths of the legacy endpoint table are P7's too, under the ruling ASM-0040. This document consumes two of those operations and defines none of them.
- The rule fields the consumed read carries are TSD P4 v3 T3.1 DF-REF-001 to DF-REF-015 and DF-REF-296 to DF-REF-298 for `rule_row`, and DF-REF-279 to DF-REF-295 for `rule_package_version`; those tables are P7's under ASM-0069 and are named here only to say what the consumed answer contains.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The run entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the fields this service records and no field of another service.
- The operations and their owners are taken from the ownership map only: the two operations of this document are P4's, the authorise operation is P4's, the parameters read is P3's and the two ledger and registry operations are P7's. No table of another service is named as this service's (DP-01). The two P7 operations are consumed although this story's metadata carries no P7 contract dependency (GAP-0873; ASM-1586).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the run and the read with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters and the three schemas.
2. Fix the `QaSampleRequest` schema with the fields of section 11: `from`, `to`, `sampleSize` and `reason`, all required, and no field that would let a caller choose a version, a package or a case.
3. Fix the `QaSampleRun` answer with `qaSampleId`, `from`, `to`, `sampleSize`, `draws`, `passed`, `failed`, `state`, `recordedAt` and the paged `items[]`, and the `QaSampleItem` schema with `decisionEntryId`, `caseId`, `decidedAt`, `ruleId`, `ruleVersion`, `verdict` and `reasonCode` — and no person field of any kind.
4. Fix the state set of a run, the verdict set of an item and the reason-code set, and state in the document that a rule version's own states are `rwb-decision`'s and are never written here.
5. Agree the error envelope and the message-ID mapping for 401, 403, 422 and 503, with the business texts taken from the legacy story where the message already existed.
6. Declare the consumed own authorise operation, the `rwb-case` parameters read and the two `rwb-decision` operations as consumed, each with its owner, one hop and the 2 s client budget; declare every rule-version operation of the legacy endpoint table as neither provided nor consumed here, because under ASM-0040 they are P7's.
7. Publish the contract tables of section 12 (nine sub-tables) and the six contract fakes.
8. Add the contract tests: schema validation, the three schemas and their required fields, the state and code sets, the envelope and message IDs, the consumed declarations and drift detection between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-E8013-APP, the SCR-39 route of RWB-PLT-N001-CON, the `rwb-decision` tech lead and the harness of the wave 4 access journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares a P7 operation as provided here | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A schema carries a name, an e-mail address, a user reference or a case narrative | The contract test fails; the review refuses the document | None | AC2, AC6 |
| X5 | A run state outside the fixed set is declared, or a rule version state is declared as written by this service | The review refuses the document | None | AC3 |
| X6 | The document declares a verdict outside PASS and FAIL, or a reason code that is not in the fixed set, or offers a field that would re-evaluate a package | The review refuses the document | None | AC3 |
| X7 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the Architecture v5 P7 contract, the DP-03 entry schema and the P3 and P4 contracts only |
| Negotiable | The sample size, the period bounds, the page bounds and the reason-code set are parameter rows behind the document; the base, the paths, the verdict set and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-39 route and the harness on Day 1, and keeps the person and the case narrative out of the record of a run |
| Estimable | One OpenAPI document, one error envelope, nine contract tables, six fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Run a QA sample against the rule version applied contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the decision log and the rule registry are held by rwb-decision and the QA sample of them is rwb-access's

  Scenario: AC1 The OpenAPI 3.1 document describes the run and the read (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the QA sample is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/qa-samples and GET /admin/qa-samples/{qaSampleId} with the owner rwb-access
    Then the run names Rules and parameters C, the read names Rules and parameters R, and both name their error responses 401, 403, 422 and 503
    Then the run requires an Idempotency-Key and the read carries none
    Then no operation of rwb-decision is declared as provided by rwb-access, and no rule-version operation is declared at all

  Scenario: AC2 The three schemas are fixed and carry no person (new, D-RCV-60)
    Given the QaSampleRequest, QaSampleRun and QaSampleItem schemas of the document
    When the three schemas are validated against the document
    Then the request carries from, to, sampleSize and reason, all required, and no field naming a case, a package or a version
    Then the run carries qaSampleId, from, to, sampleSize, draws, passed, failed, state, recordedAt, items, page, size and total
    Then an item carries decisionEntryId, caseId, decidedAt, ruleId, ruleVersion, verdict and reasonCode
    Then no schema declares a name, an e-mail address, a user reference or a case narrative
    Then page and size are read from the parameters contract and never from code, and from and to are validated against the period bounds in force

  Scenario: AC3 The state, verdict and reason-code sets are fixed and no rule state is written here (new, D-RCV-60)
    Given the state set of a run, the verdict set of an item and the reason-code set in the document
    When the sets are compared with the parameter rows of rwb-case
    Then state is one value of the fixed run state set, and its value is documented as this service's own
    Then verdict is one of PASS and FAIL, and a PASS item carries no reason code
    Then reasonCode is one of RULE_VERSION_NOT_IN_FORCE, RULE_ROW_ABSENT and ANSWER_MISMATCH on a FAIL item
    Then the three codes and the run state set are documented as parameter rows of rwb-case read through DP-06 and never as constants of the contract
    Then the document states that the states of a rule version, LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, are rwb-decision's and are never written by rwb-access
    Then the document declares no field that would evaluate a package, build a KieBase or re-decide a case

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 422 or 503 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 422 carries MSG-GEN-001 and 503 carries MSG-P7-003
    Then no operation declares a second error shape, and the approval messages of a rule package belong to no response of this document

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation, the parameters read and the two rwb-decision operations this service calls
    When the document is validated against the ownership map
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then GET /api/recovery/decision/v1/decision-log and GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel} are declared as consumed with the owner P7 rwb-decision
    Then each carries one hop and the 2 s client budget with a breaker
    Then the document records that the two P7 reads are consumed, and names the gap rows GAP-2284 and GAP-0873 that carry the P7 dependency
    Then no operation owned by rwb-decision, rwb-case or rwb-comms is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the six contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the decision fake answers an entry with its id, case id, decided time, rule id, rule version and recorded answer only, and no case narrative
    Then the rule-model fake answers a version with its valid_from, its valid_to and its rule_row set only, and no package source and no DRL
    Then no schema, example or fake carries a name, an e-mail address or a personal field

  Scenario: AC7 The document declares no workflow and changes only additively (new, D-RCV-60)
    Given the operations and schemas of the document
    When the document is read against the workflow and versioning rules
    Then it declares no workflow, no activity and no Schedule for the capability
    Then a schema change within major version 1 is additive, and a removed, renamed or retyped field is declared as a new major version

  Scenario: AC8 Each business rule BR1 to BR11 is covered by a criterion and a test (new, D-RCV-60)
    Given the business rules of section 8
    When the criteria and the test cases of the document are compared with the rules
    Then every rule BR1 to BR11 is named by at least one criterion of section 7 and one row of section 16
    Then a rule that is an architecture constraint is named by a guardrail or boundary test instead of a contract test

  Scenario: AC9 The provided operations declare a 404 answer in the problem envelope (new, D-RCV-60)
    Given the two provided operations POST /admin/qa-samples and GET /admin/qa-samples/{qaSampleId} of the document
    When a request names a qaSampleId that matches no QA sample run
    Then the document declares a 404 response on both provided operations
    Then the 404 body is the one problem envelope of AC4 with the message ID Not specified in the source documents (NEWAC-RWB-P4-E8013-CON-AC8)
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-013 belong to RWB-P4-E8013-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR4 | The schemas carry the fields of this run and no field of another service: no ledger entry, no rule row, no package source and no DRL | DP-01; Ownership Map v1 (`decision_log_entry`, `rule_row` = P7; ASM-0069) |
| BR5 | The answer carries a verdict and one reason code and never a person, a user reference or a case narrative | NFR-040; ASM-1588 |
| BR6 | The run state set, the verdict set and the reason-code set are fixed here and held as parameter rows behind the document; no value of them is a constant in code | FSD P4 v3 A2.24.3.1 BR-P4-024; ASM-1587 |
| BR7 | The two `rwb-decision` operations are consumed with their owners, one hop and the 2 s budget, and the missing P7 contract dependency is carried in the gap and not added to the metadata | Ownership Map v1; GAP-0873; ASM-1586 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |
| BR9 | A write requires an `Idempotency-Key`; a replay answers the first answer and makes no second read | Architecture v5 slide 42; DP-09 |
| BR10 | The contract declares no workflow, no activity and no Schedule for the capability | Architecture v5 slide 14; TSD P4 v3 T5.3 |
| BR11 | The document declares no rule-version operation: under ASM-0040 the rule-version paths belong to P7, and this service only reads a version through the consumed rule-model read | ASM-0040; GAP-0873; ASM-1586 |

Coverage of the rules: BR1 by AC1 and TC-E8-013-CON-01; BR2 and BR7 by AC5 and TC-E8-013-CON-05; BR3 by AC4 and TC-E8-013-CON-04; BR4 and BR5 by AC2 and TC-E8-013-CON-02; BR6 by AC3 and TC-E8-013-CON-03; BR8 and BR10 by AC7 and TC-E8-013-CON-07; BR9 and BR11 by AC1 and TC-E8-013-CON-01. BR1 to BR11 by AC8 and TC-E8-013-CON-09, and the 404 answer by AC9 and TC-E8-013-CON-10.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the three schemas, the state and code sets and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the SCR-39 route, the `rwb-decision` tech lead and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a verdict or a reason code is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The decision-log query, the rule-model read or the parameters read changes | Baselined, with the client budget and the stub restated |

The state set the document fixes for a run is this service's own, and its values are fixed here and held as parameter rows behind the document; the legacy story and the FSD name no run state, so the values are Not specified in the source documents (GAP-0873; ASM-1586). The state set of a rule version — `LOADED`, `VALIDATED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED` — is `rwb-decision`'s under TSD P4 v3 T3.2 and T4 and is declared here as read-only, because this service never writes it. The verdict set is PASS and FAIL and the reason-code set is RULE_VERSION_NOT_IN_FORCE, RULE_ROW_ABSENT and ANSWER_MISMATCH.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the three schemas, the state and code sets and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Conduct and QA officer, as the primary user of the run | Reviews the run operation, the verdicts and the reason codes |
| Internal audit | Reviews the item fields, the absence of a person and a case narrative in the record, and the stable order of the read |
| Tech lead of rwb-decision (P7) | Reviews the two operations as `rwb-access` consumes them and owns their definitions, the rule version states and the rule-row fields |
| Tech lead of rwb-case (P3) | Reviews the parameters read as `rwb-access` uses it; owns its definition |
| Data steward | Confirms that no name, e-mail address, personal field or case narrative is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `QaSampleRequest` | `from` (a date, inside the period bounds in force), `to` (a date, not earlier than `from`, inside the period bounds), `sampleSize` (a whole number, at most the maximum in force), `reason`; all required | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |
| `QaSampleRun` answer | `qaSampleId`, `from`, `to`, `sampleSize`, `draws`, `passed`, `failed`, `state` (a value of the fixed run state set), `recordedAt`, `items[]`, `page`, `size`, `total` | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |
| `QaSampleItem` | `decisionEntryId`, `caseId`, `decidedAt`, `ruleId`, `ruleVersion`, `verdict` (PASS or FAIL), `reasonCode` (absent on a PASS) | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |
| Decision entry, as consumed | `id` DF-DEC-001, `case_id` DF-DEC-002, `decision_code` DF-DEC-003, `rule_id` and `rule_version`, `decided_at` DF-DEC-016, and the recorded answer the item compares | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |
| Rule model, as consumed | `version_label` DF-REF-281, `status` DF-REF-282, `valid_from` DF-REF-286, `valid_to` DF-REF-287, and the `rule_row` set of that version: `rule_id` DF-REF-002, `rule_version` DF-REF-003, `action_text` DF-REF-008, `valid_from` DF-REF-012, `valid_to` DF-REF-013, `package_version_id` DF-REF-296, `drools_rule_name` DF-REF-297, `outputs` DF-REF-298 | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |
| Roles and letters | The Rules and parameters R letter and the capability areas of `role` DF-REF-034 to DF-REF-039 and `permission` DF-REF-040 to DF-REF-044, read behind the authorise answer | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |
| Record event | `rwb.decision.DecisionRecorded.v1` with the entry of a run, from the DP-03 library | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |
| Refusal | `messageId` MSG-P4-001 on a 401, MSG-P4-002 on a 403, MSG-GEN-001 on a 422 and MSG-P7-003 on a 503 | Not specified in the source documents (DOR-RWB-P4-E8013-CON-7) |

The exact request and answer field set of the two operations, the type and length of each field, the run state set, the reason-code set, the draw rule and the record code of a run are Not specified in the source documents (GAP-0873; ASM-1586): FSD P4 v3 A2.24 names the journey and one validation rule (VR-P4-024-1) and one business rule (BR-P4-024) and no operation and no field, and the legacy story declares no endpoint of this capability. The two `rwb-decision` operations are the P7 operations of Architecture v5 slide 14; the paths this document consumes are the P7 paths and are raised with the P7 owner in the same rows (GAP-0873; ASM-1586). The verdict set and the three reason codes are the contract's own names for the three checks of the app story, and they are confirmed with Internal audit before the operations are frozen (ASM-1587).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/qa-samples` | `QaSampleRequest` in; `QaSampleRun` out with `qaSampleId`, `draws`, `passed`, `failed`, `state`, `recordedAt` and the `Location` of the read | Rules and parameters R; `Idempotency-Key` required |
| GET | `/admin/qa-samples/{qaSampleId}` | `QaSampleRun` out: the run with its counts and its `items[]` of `decisionEntryId`, `caseId`, `decidedAt`, `ruleId`, `ruleVersion`, `verdict` and `reasonCode`, paged | Rules and parameters R |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 422 a required field empty, a value of the wrong shape, a period outside its bounds or a size above the maximum (MSG-GEN-001), 503 `rwb-decision` cannot be reached or the run entry cannot be written (MSG-P7-003). The run is a write, so every request carries an `Idempotency-Key` and a replay answers the first answer with no second read (BR9); the read carries none. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

The two paths are fixed here (GAP-0873; ASM-1586) and confirmed by the contract review before they are frozen. No rule-version operation is declared in this document at all: under ASM-0040 the rule-version paths are P7's, and this service reads a version only through the consumed rule-model read (BR11).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters R check behind both operations, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The default and maximum sample size, the period bounds, the page bounds and the reason-code set, with the version in force (DP-06) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The closed decisions of the period, queried by `from`, `to` and `page`, each entry with its id, case id, decided time, rule id, rule version and recorded answer |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` | P7 rwb-decision | One rule-model version with its `valid_from`, its `valid_to` and its `rule_row` set, read once per drawn version |

None of the four is declared as provided by rwb-access. Of the two `rwb-decision` operations, the decision-log query and the rule-model read are the P7 operations of Architecture v5 slide 14 and of the ownership map; this story's metadata contract-dependency list carries neither, which is the missing dependency of the key and is carried in GAP-0873 and ASM-1586 and not added to the metadata (BR7). The two P7 reads are faked, so the app story, the route and the harness build on Day 1 against a fixed answer.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a run with its run id, period, requested and drawn sizes, passed and failed counts, window and the reason code of each failure, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This document declares the record message only. `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's and `rwb.access.DoaLimitChanged.v1` is RWB-P4-E8008-APP's, and a QA verdict publishes neither (Architecture v5 slide 14): a verdict changes no policy and no limit, and the access service announces no change of its own on `rwb.access.events.v1` for this capability.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14, and the two operations of this contract need no subscription. The document declares no inbox and no consumer group, and `RulePackageInForce` on `rwb.decision.events.v1` is not subscribed to by this contract.

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: the run is synchronous. The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only, and the chain check at 02:00 is P7's (BR10).

#### 12.6 Schedules

None. Both operations are request-driven, and a monthly conduct check is a person's act on the screen and not a Schedule of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code of the caller who ran the sample |
| `permission` | P4 (rwb_access) | The R letter of Rules and parameters and the role it is held through |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The run entry the record event carries |
| the stored item set of a run | P4, in rwb_access | The items and their draw order that the read answers |
| `idempotency_key` | PLT library, created in rwb_access | The stored request and answer of a run, so one key answers one run (DP-09; ASM-0074) |

No table of another service is named in the contract (DP-01): `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 rwb_decision's and their fields arrive in the consumed answers; `case`, `task` and `parameter_value` are P3 rwb_case's. No rule table is created, copied or named as this service's, and the document holds no package source, no DRL and no ledger entry (BR4).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| decision fake | `GET /decision-log` answering the closed decisions of a period with their entry id, case id, decided time, rule id, rule version and recorded answer; an empty period; a 503 (GAP-0873; ASM-1586) | App story, contract tests, harness |
| rule-model fake | `GET /rule-models/{packageCode}/{versionLabel}` answering "ALLOCATION" version "ALLOC-2026.09" with `valid_from` 2026-10-15 and `valid_to` 2026-11-14, version "ALLOC-2026.10" with `valid_from` 2026-10-01 and `valid_to` 2026-10-31 and its `rule_row` set, and a 404 for a version not held | App story, contract tests, harness |
| authorise fake | `POST /authorise` with a granted answer for RW-CONDUCT, RW-COE and RW-AUDIT with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-PHONECOL with no letter | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the default and maximum sample size, the period bounds, the page bounds and the reason-code set at the version in force | App story, contract tests |
| decision-record fake | The append of a run, the hash-link check, a seeded run with its items and a forced failure | App story, contract tests |
| gateway-bff fake | The composite route of SCR-39 with the rule version in force and its evidence, the run form and the run panel | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The run and the read provided; the authorise, parameters and two `rwb-decision` operations consumed; one hop, 2 s timeout |
| Kafka | 1 event type published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output; a run is a request and its report export is not part of this capability |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-qa-sample-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml`, the `QaSampleRequest`, `QaSampleRun` and `QaSampleItem` schemas with their examples, the state, verdict and reason-code rules and the versioning rules in the contract README, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | the monolith REST base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. DP-01, DP-02, DP-09 and DP-11 govern the service baseline, the one base and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. **DP-04 is not applied**: this contract declares no rule evaluation, no embedded Drools kit and no `RWB-PLT-E1072-CON`, because the consistency test reads a recorded version and never runs the engine. The two `rwb-decision` operations are consumed and faked, and the missing P7 contract dependency is carried in the gap row of the key and not added to this story's metadata (GAP-0873; ASM-1586).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two operations with the shapes of section 11: the request, the run answer with its counts, the items and the paging, and the required fields.
3. The state set of a run, the verdict set and the reason-code set, stated in the document and in the contract README, with the ownership of each stated: the run state and the codes as this service's parameter-backed values, and the rule version states as `rwb-decision`'s and read-only.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget, the explicit statement that no rule-version operation is provided here, and the note that the two P7 reads carry no contract dependency in the metadata.
5. The error envelope and the message-ID mapping for 401, 403, 422 and 503, with the texts of the legacy messages, and the explicit statement that the approval messages of a rule package belong to no response of this document.
6. The six fakes and the stub fixtures of section 12.8, including the two rule versions, the three seeded decisions of the app story and the forced failure.
7. The six contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note from the app story, the SCR-39 route, the `rwb-decision` tech lead and the harness.

**Feature switch.** Both operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8013-APP | The two provided operations, the three schemas, the state, verdict and reason-code sets and the six fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-39) | The run and the read as the form and the run panel call them |
| The `rwb-decision` tech lead | The two operations as consumed, with the decision-log query, the rule-model read and the rule-row fields the item compares, and that no ledger or registry table is claimed here |
| The harness of the wave 4 access journey | The verdicts, the reason codes and the run record, as the evidence it records |

The run state values, the reason-code names and the record code of a run are Not specified in the source documents (GAP-0873; ASM-1586): the codes are held as parameter rows and the record code is the library's sample code, and both are confirmed with Internal audit and with the decision-record library owner before the operations are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the six fakes answer every declared path, the `rwb-decision` tech lead has accepted the two consumed operations, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters R runs a sample or reads one | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, `from` or `to` is not a date, `to` is earlier than `from`, `sampleSize` is not a whole number, the period is outside its bounds, or the size is above the maximum | Enter {field}. |
| MSG-P7-003 | `rwb-decision` cannot be reached, or the run entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed, and VR-P4-024-1 of the FSD is the rule behind MSG-GEN-001. The four-eyes message of a rule package approval and the missing-checklist message of a package load are declared on no response of this document, because this contract approves no rule version and carries no author-and-approver rule and no change checklist. MSG-P4-003, the legacy scope message, is declared on no response, because a QA sample addresses a period and not a case.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-39 Rules and parameters | Rule version in force | The version in force and its evidence as `rwb-decision` answers them, with the run panel beside it |
| SCR-39 Rules and parameters | Sample, form | `QaSampleRequest` with `from`, `to`, `sampleSize` and `reason`, the size and the bounds shown from the parameter rows in force |
| SCR-39 Rules and parameters | Sample, recorded | `QaSampleRun` with `qaSampleId`, `draws`, `passed`, `failed`, `state` and `recordedAt` |
| SCR-39 Rules and parameters | Sample, items | `QaSampleItem` rows with the decision entry, case, decided time, rule id, rule version, verdict and reason code, paged |
| SCR-39 Rules and parameters | Sample, all passed | A run with `failed` 0 and every item PASS |
| SCR-39 Rules and parameters | Sample, failures | The FAIL items with their reason codes, and no action offered on the case they belong to |
| SCR-39 Rules and parameters | Sample, refused | The 403 of the envelope with MSG-P4-002 |
| SCR-39 Rules and parameters | Sample, out of bounds | The 422 of the envelope with MSG-GEN-001 naming the field and the bound in force |
| SCR-39 Rules and parameters | Not recorded | The 503 of the envelope with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (DOR-RWB-P4-E8013-CON-10) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (DOR-RWB-P4-E8013-CON-10) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (DOR-RWB-P4-E8013-CON-10) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (DOR-RWB-P4-E8013-CON-10) |

The screen is served by the gateway-bff composite route (DP-19), which shows the rule version in force and its evidence from `rwb-decision` and calls the two operations of this contract, one hop each. The composite route specification and the screen field list belong to RWB-PLT-N001-CON; the document fixes the sample side of the merge only. The FSD P4 screen list names no QA-sample screen — it lists SCR-39, SCR-40, SCR-41, SCR-42, SCR-43 and SCR-47 — so this baseline claims no screen id of its own and the absence is carried in the key's gap row (GAP-0873; ASM-1586).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-013-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the R right, the four error responses and the `Idempotency-Key` on the write are present; no P7 operation and no rule-version operation is provided |
| TC-E8-013-CON-02 | AC2 | Contract | The request, run and item fields; the required fields; no case, package or version field in the request; no name, e-mail address, user reference or case narrative in any schema |
| TC-E8-013-CON-03 | AC3 | Contract | The run state set, the PASS and FAIL verdicts, the three reason codes, the parameter-backed origin of each, and the seven rule version states declared as P7's and read-only |
| TC-E8-013-CON-04 | AC4 | Contract | A 401, 403, 422 and 503 response carry one problem envelope with a valid message ID; the approval and checklist messages of a rule package are on no response |
| TC-E8-013-CON-05 | AC5 | Contract | Four consumed operations with their owners P4, P3 and P7, one hop and the 2 s budget; the missing P7 contract dependency recorded; no P7 operation declared as provided |
| TC-E8-013-CON-06 | AC6 | Component | The six fakes match the document; a drifted fake fails the build; the decision fake carries no case narrative and the rule-model fake carries no package source and no DRL |
| TC-E8-013-CON-07 | AC7 | Contract | No workflow, no activity and no Schedule is declared; a schema change is additive within major version 1 and a removed, renamed or retyped field is a new major version |
| TC-E8-013-CON-08 | §12.7 tables (ASM-3438) | Boundary | Each table of §12.7 is named with its owner P4 or the PLT library; a table of P3 or P7 is named only as consumed, and no table is created here for them |
| TC-E8-013-CON-09 | AC8 | Contract | Each rule BR1 to BR11 traced to a criterion and a test row; the architecture-constraint rules traced to a guardrail or boundary test |
| TC-E8-013-CON-10 | AC9 | Contract | The document declares 404 on POST /admin/qa-samples and GET /admin/qa-samples/{qaSampleId}; a GET of an unknown qaSampleId answers 404 with the AC4 problem envelope and the message ID Not specified in the source documents (NEWAC-RWB-P4-E8013-CON-AC8) |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in the contract: the sample size, the period bounds, the page bounds and the reason-code set stay parameter rows behind the document, and the role codes stay rows of `role` and `permission`.
- No personal data in a schema, an example or a fake: ids, dates, rule ids, rule versions, verdicts, reason codes and counts only, and no user reference and no case narrative in any answer (BR5).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; `decision_log_entry`, `rule_row` and the rule registry are P7's and are consumed or absent, never named as this service's (BR4).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- No rule-version operation in this document: the rule-version paths are P7's under ASM-0040, and this service only reads a version (BR11).
- One writer of a rule version state: the document states that the seven version states are written by `rwb-decision` and never by this service (AC3).
- The two `rwb-decision` operations are consumed and faked, and the missing P7 contract dependency is carried in the gap rather than added to the metadata (BR7).
- Every example in the document is synthetic; no ledger entry, rule package or production payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `Idempotency-Key` is refused by the contract, and a replay never makes a second read.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | The `QaSampleItem` with `decisionEntryId`, `decidedAt`, `ruleId` and `ruleVersion`, and the consumed decision-log query that carries them | TC-E8-013-CON-02, TC-E8-013-CON-05 |
| REQ-DRI-012 | Audit can query the decision log for a population of cases and receive the decision history with inputs, versions, approver and final call | The period query of the run and the paged read of a recorded run, with the stable item order | TC-E8-013-CON-01, TC-E8-013-CON-02 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | The verdict and the three reason codes, and the consumed rule-model read with its `valid_from`, `valid_to` and `rule_row` set | TC-E8-013-CON-03, TC-E8-013-CON-05 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 run a QA sample against the rule version applied, and the record of the result with the rule version | Sections 4, 7 (AC1, AC2), 11, 12.1, 12.2 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7, 12.1, 14 |
| The permission checks of the legacy table, Rules and parameters C for RW-COE and A for RW-RISK, read here as the R letter of the T6.1 matrix | Sections 7 (AC1, AC5), 10, 12.1, 14 |
| The legacy endpoint table's two rule-version paths, which are P7's under ASM-0040 and appear on no response here | Sections 7 (AC1, AC5), 8 (BR11), 12.1, 19 |
| The legacy data rows `decision_log_entry` DF-DEC-001 to DF-DEC-018 and `rule_row` DF-REF-001 to DF-REF-015 | Section 11, section 12.7 |
| The legacy screens SCR-39 and SCR-41 as the story named them | Section 15, carried to SCR-39 Rules and parameters |
| Legacy key RWB-E8-013, story RWB-P4-E8013-APP, contract RWB-P4-E8013-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the run and the read (RWB-P4-E8013-APP).
- The decision log, its entries and its query API: P7 `rwb-decision`. This document consumes one read of it.
- The rule registry, its packages, their versions, their rows and their test cases: P7 `rwb-decision` under ASM-0069. This document consumes one read of a version.
- The Drools evaluation of a package, the rule packages in force and the promotion at 00:01: P7 governance and the local evaluation of the owning service (DP-04). This document declares no evaluation field.
- The chain-integrity check at 02:00 (JOB-14) and the daily ledger seal (P7 and RWB-P4-E8015-APP).
- The publication and the rollback of an access configuration version (RWB-P4-E8012-APP and RWB-P4-E8011-APP).
- The permission matrix, the role administration and the masking policy (RWB-P4-E1037-APP and the Epic 8 administration stories).
- The screen SCR-39 Rules and parameters, its other panels and its composite route specification (RWB-PLT-N001-CON).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The operations of other services: the authorise operation, the `rwb-case` parameters read and the two `rwb-decision` operations are consumed and faked, never defined here.
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
