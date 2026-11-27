# RWB-P4-E8018-CON Refer a case to Aric

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8018-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E8018-CON-16) |
| Contract version | v1, major version in the path `/api/recovery/access/v1`; minor version Not specified in the source documents (DOR-RWB-P4-E8018-CON-23) |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | Aric, outside fraud system; owner, protocol, credentials, timeout and result channel Not specified in the source documents (GAP-0882) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-018 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8018-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 14 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the fraud referral of `rwb-access`: an OpenAPI 3.1 document for the referral, the result and the two reads, the `FraudReferral`, `FraudReferralResult` and `FraudReferralPage` schemas with the referral state set and no person, the one RFC 9457 error envelope with its message IDs, the consumed case, verdict, freshness, parameters and authorise operations with their owners and the 2 s budget, the Aric transport declared as an external dependency of the contract and not as a REST operation of a service, the contract tables of section 12 and the six contract fakes**, so that **the app story, the SCR-03 referral panel, the `rwb-case`, `rwb-decision` and `rwb-source-data` teams and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access` or for the Aric interface to be built**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-018 belong to RWB-P4-E8018-APP, and the six criteria of section 7 test the document, the schemas and the state set, the envelope, the consumed and outside declarations, and the fakes.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story referred a case to Aric inside the monolith, where the case, the rule row and the decision log were rows of one schema and the referral was an in-process call that no other service had to agree on. In the target the case is `rwb-case`'s (Architecture v5 slide 41), the rule verdict is `rwb-decision`'s, the freshness of the ACE data is `rwb-source-data`'s, and Aric is outside the bank with no owner in the catalogue at all.

Three things must therefore be fixed once. The first is the boundary: which operation raises a referral, which takes a result back, which reads, and which nothing owns - the Aric transport, which is an external dependency of this contract and not an operation of any service. The second is what the record says: the case reference, the referral id, the verdict reference, the rule id, the rule version, the model version, the state, the external reference and the times - and never the customer - because a referral record that carried the borrower's data would copy personal data into a shared topic that every consumer of the decision record reads. The third is the state set, because a referral that cannot be told apart from a closed one is a referral nobody can act on.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the three contracts it reads, the parameters contract of `rwb-case` and the local decision-record library, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service, the shared topic `rwb.decision-record.v1`, task queue `rwb-access` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.access`.

The baseline also states the two things it is not: it defines no case, no verdict and no data product, and it declares no operation of Aric as if a service owned it. The four contract reads appear in the document as consumed, and the outside transport appears in a declared external-dependency section, which is what makes the split real.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that serves SCR-03 Case record and calls the two reads behind the referral panel, and it is a consumer of this baseline.
- The case is described by the P3 contract and the ownership map: `recovery_case` is P3's, its fields are DF-CAS-001 to DF-CAS-023 of the Logical Data Model and Data Dictionary v9, and the case read of Arch v5 slide 14 (`GET /cases/{id}`) is the operation this document consumes.
- The verdict is described by the P7 contract: the central decision ledger is P7's (Architecture v5 slides 14 and 41), its entry fields are DF-DEC-001 to DF-DEC-018, and the decision read of Arch v5 slide 14 (`GET /decisions?caseId=`) is the operation this document consumes.
- The freshness is described by the P1 contract: the data products and their freshness are P1's (Architecture v5 slide 41; the data-product and freshness operations of the API specification), and the freshness read of the API specification is the operation this document consumes.
- The parameters and the letters are the P3 parameters contract (DP-06) and this service's own `role` and `permission` rows; the page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget are parameter rows behind the document.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The referral entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the fields this service records and no field of another service.
- The four provided operations are P4's and the four consumed operations are P4's, P3's, P7's and P1's under the ownership map only. No table of another service is named as this service's (DP-01). The three cross-service reads are consumed although this story's metadata carries no C dependency on any of them (GAP-0880; ASM-1597).
- Aric is outside the bank: no operation of Aric appears in the ownership map, in the API specification or in the Arch v5 catalogue, and its protocol, its credentials and its result channel are Not specified in the source documents (GAP-0882; ASM-1600).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the four operations with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the paging parameters and the three schemas.
2. Fix the `FraudReferral` request and answer shapes with the fields of section 11: `caseNo` and `referralReason` in on the referral, `referralId`, `caseNo`, `state`, `ruleId`, `ruleVersion`, `sentAt` and `externalReference` out, and no person field of any kind.
3. Fix the `FraudReferralResult` request and answer shapes: `resultCode`, `investigationReference` and `resultNote` in, and the moved referral out, with the state set of step 5.
4. Fix the `FraudReferralPage` schema and the query parameters of the list, with `caseNo`, `state`, `page` and `size`, and with the page default and maximum held as parameter rows behind the contract.
5. Fix the state set: `REFERRED`, `ANSWERED` and `FAILED`, with `ANSWERED` as the terminal outcome and the transition each one allows stated in the document, and state that the state lives on the entries of the local decision-record chain and not in a table of its own.
6. Agree the error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed and MSG-GEN-002 and MSG-P1-001 carried as message IDs with their sources named.
7. Declare the consumed own authorise operation, the `rwb-case` case read and parameters read, the `rwb-decision` decision read and the `rwb-source-data` freshness read as consumed, each with its owner, one hop and the 2 s client budget; declare the Aric transport in the external-dependency section and not as an operation of any service.
8. Publish the contract tables of section 12 (nine sub-tables) and the six contract fakes, including the outside transport fake.
9. Add the contract tests: schema validation, the three schemas and their required fields, the state set and its transitions, the envelope and message IDs, the consumed and external declarations, and drift detection between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-E8018-APP, the SCR-03 route of RWB-PLT-N001-CON, the P3, P7 and P1 tech leads, the Aric interface owner and the harness of the wave 4 access journey. Before tagging, each open value is marked with the placeholder of Template and Rules section R9 and settled with the Aric owner, the ledger owner and the gateway-bff owner; the missing dependencies are raised at D1 and not added to the metadata.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares a case, verdict or freshness operation as provided here | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC4 |
| X3 | A response of 401, 403, 404, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC3 |
| X4 | A schema carries a name, an identification number, an account number, a balance, an e-mail address or another personal field | The contract test fails; the review refuses the document | None | AC2, AC6 |
| X5 | A state outside `SENT`, `RESULT_RECEIVED`, `CLOSED` and `FAILED` is declared, or a transition the state set does not allow | The review refuses the document | None | AC2 |
| X6 | The document declares a case, deviation, data-product or rule table as this service's, or declares a new table for the referral | The review refuses the document | None | AC2, AC6 |
| X7 | The document declares an operation of Aric, an interface configuration or an outbound item as a service operation, or names a service as the owner of the Aric interface | The review refuses the document; the transport stays an external dependency | None | AC1, AC4 |
| X8 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X9 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC4 |
| X10 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the P3, P7 and P1 contracts and the DP-03 entry schema only |
| Negotiable | The reason and note lengths, the page bounds, the fraud package code, the closing result codes and the client budget are parameter rows behind the document; the base, the paths, the state set and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-03 referral panel and the harness on Day 1, keeps the person out of the record of a referral, and fixes the boundary with an outside system that no service owns |
| Estimable | One OpenAPI document, three schemas, one state set, one error envelope, nine contract tables, six fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Refer a case to Aric contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the cases are held by rwb-case, the rule verdicts by rwb-decision and the data-product freshness by rwb-source-data
    Given Aric is outside the bank and no service of the target owns its interface (ASM-1600)

  Scenario: AC1 The OpenAPI 3.1 document describes the four operations and the outside transport (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the fraud referral is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/fraud-referrals, POST /admin/fraud-referrals/{referralId}/results, GET /admin/fraud-referrals/{referralId} and GET /admin/fraud-referrals with the owner rwb-access
    Then the referral names Rules and parameters C, the result names U and the two reads name R, and each names its error responses 401, 403, 409, 422 and 503
    Then the two writes require an Idempotency-Key and the two reads carry none
    Then it carries an external-dependency section that declares the Aric transport with no owner, no path and no operation
    Then no operation of rwb-case, rwb-decision, rwb-source-data or Aric is declared as provided by rwb-access

  Scenario: AC2 The referral, result and page schemas and the state set are fixed and carry no person (new, D-RCV-60)
    Given the FraudReferral, FraudReferralResult and FraudReferralPage schemas of the document
    When the contract test reads the three schemas and the state set from the document
    Then the referral request carries caseNo and referralReason, both required
    Then the referral answer carries referralId, caseNo, state, ruleId, ruleVersion, sentAt and externalReference
    Then the result request carries resultCode, investigationReference and resultNote, and the result answer carries referralId, caseNo, state, resultCode, investigationReference and receivedAt
    Then the page carries items of FraudReferral, page, size and total
    Then state is one of SENT, RESULT_RECEIVED, CLOSED and FAILED, and the document states the transition each state allows and the one it refuses
    Then the document states that the state lives on the entries of the local decision-record chain and that no table is created for a referral
    Then no schema declares a name, an identification number, an account number, a balance, an e-mail address or a user reference
    Then page and size are read from the parameters contract and never from code, and resultCode is validated against the codes in force

  Scenario: AC3 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by any of the four operations
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 404 carries MSG-GEN-004 and 409 carries MSG-GEN-004 for a state conflict and MSG-P1-001 for a stale data product
    Then 422 carries MSG-GEN-001 for a field and MSG-GEN-002 for a value out of range
    Then 503 carries MSG-P7-003
    Then no operation declares a second error shape

  Scenario: AC4 The consumed operations are declared as consumed and Aric is declared outside (new, D-RCV-60)
    Given the four operations this service calls and the outside interface it uses
    When the contract test reads the consumed operations and the external dependency from the document
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters and GET /api/recovery/case/v1/cases/{caseNo} are declared as consumed with the owner P3 rwb-case
    Then GET /api/recovery/decision/v1/decisions?caseId={caseId} is declared as consumed with the owner P7 rwb-decision
    Then GET /api/recovery/source-data/v1/data-products/freshness is declared as consumed with the owner P1 rwb-source-data
    Then each carries one hop and the 2 s client budget with a breaker
    Then the Aric transport is declared as an external dependency of the contract, with its protocol, its credentials and its result channel marked Not specified and no service named as its owner
    Then no operation owned by rwb-case, rwb-decision or rwb-source-data is declared as provided by rwb-access

  Scenario: AC5 The contract declares one record message and no event, workflow or Schedule of its own (new, D-RCV-60)
    Given the events, workflows and Schedules section of the document
    When the contract test reads the events, workflows and Schedules section from the document
    Then rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 is the only message the document declares
    Then the document declares no rwb.access.<Event>.v1 message for a referral, and states that the two events of the service are AccessPolicyChanged and DoaLimitChanged
    Then the document declares no consumed event, no consumer group and no inbox
    Then the document declares no workflow, no activity and no Schedule for the capability
    Then the document declares no file input and no file output, and the Aric transport is stated as an interface call and not as a file

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the six contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the case fake answers a case number, a product group, a status and the fraud flag only, and no customer field
    Then the verdict fake answers a decision reference, a rule id, a rule version, a model version and an outcome only
    Then the outside transport fake answers an external reference or a timeout and is switched by the test, never called
    Then no schema, example or fake carries a name, an identification number, an account number, a balance or an e-mail address

  Scenario: AC7 A schema change within major version 1 is additive only (new, D-RCV-60)
    Given the three schemas of the baseline at major version 1
    When a change to them is compared with the published baseline
    Then an added optional field passes within major version 1
    Then a removed, renamed or retyped field is refused and needs a new major version

  Scenario: AC8 Every business rule of section 8 is carried by a criterion and a test case (new, D-RCV-60)
    Given the business rules table of section 8 with the rules BR1 to BR12
    When the table is read against the criteria of section 7 and the test cases of section 16
    Then each rule ID names at least one existing criterion and one existing test case
    Then a rule that is an architecture constraint is carried by a guardrail or boundary test row

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given the state set of FraudReferral is REFERRED, ANSWERED and FAILED
    When a status change is requested that the document refuses
    Then the answer is the 409 of the envelope with MSG-GEN-004
    Then the stored state is unchanged
```

These six criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-018 belong to RWB-P4-E8018-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1; TC-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC4; TC-04 |
| BR3 | An outside system is declared as an external dependency with no owner and no path; no operation of it is declared as a service operation | Architecture v5 slide 41 (no Aric interface in the catalogue); GAP-0882 | AC1, AC4; TC-01, TC-04 |
| BR4 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC3; TC-03 |
| BR5 | The schemas carry the fields of this referral and no field of another service: no customer field, no account, no balance and no deviation | DP-01; Ownership Map v1 (`recovery_case` = P3, `deviation` = S8) | AC2; TC-02 |
| BR6 | The record carries references, codes and times and no person: no name, no identification number, no account number, no balance, no e-mail address and no user reference | NFR-040; ASM-1597 | AC2, AC6; TC-02, TC-06 |
| BR7 | The state set is `REFERRED`, `ANSWERED` and `FAILED`, held on the entries of the local decision-record chain, and no table is created for a referral | ASM-1598; DP-03 | AC2; TC-02, TC-07 |
| BR8 | The four contract reads are consumed with their owners, one hop and the 2 s budget, and the missing C dependencies are carried in the key's gap and not added to the metadata | Ownership Map v1; GAP-0880; ASM-1597 | AC4; TC-04 |
| BR9 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC7; TC-08 |
| BR10 | A write requires an `Idempotency-Key`; a replay answers the first answer and makes no second send | Architecture v5 slide 42; DP-09 | AC1; TC-01 |
| BR11 | The contract declares no event of its own, no workflow, no activity and no Schedule for the capability, and the one message it declares is the record | Architecture v5 slide 14; TSD P4 v3 T5.3 | AC5; TC-05 |
| BR12 | The referral reason and the result note are free text with their lengths as parameter rows; the document declares no list of values of this service, because the story's pattern list carries no DP-07 | DP-06; GAP-0880 | AC2; TC-02 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The four operations, the three schemas, the state set, the consumed operations and the external dependency are described | In review |
| In review | Consumer sign-off | The app story, the SCR-03 route, the P3, P7 and P1 tech leads, the Aric interface owner and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a state is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The case, decision, freshness or parameters operation changes | Baselined, with the client budget and the stub restated |
| Baselined | The Aric interface is fixed | The protocol, the credentials and the result channel are agreed with its owner | Baselined, with the external-dependency section restated |

The state set the document fixes for a referral is `SENT`, `RESULT_RECEIVED`, `CLOSED` and `FAILED`, with each transition stated in the document and each state held on an entry of the local decision-record chain: `SENT` on the referral, `RESULT_RECEIVED` on the first result, `CLOSED` on a closing result code in force, and `FAILED` where the outside send could not be completed. The lifecycle of a rule package version - including `LOADED`, `REFUSED`, `SUPERSEDED` and `ROLLED_BACK` - is P7's and is not declared here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the three schemas, the state set and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version, and the declaration of an outside system |
| Fraud investigator, as the reader of a referral | Reviews the two reads, the fields of the state path and the absence of a person in the record |
| Center of excellence analyst, as the role that refers | Reviews the referral and result operations, their rights and their idempotency |
| Tech lead of rwb-case (P3) | Reviews the case read and the parameters read as `rwb-access` consumes them; owns their definitions |
| Tech lead of rwb-decision (P7) | Reviews the decision read, the verdict fields and the record message as `rwb-access` publishes it |
| Tech lead of rwb-source-data (P1) | Reviews the freshness read and the MSG-P1-001 refusal that this feature produces |
| Owner of the Aric interface, outside the bank | Confirms the transport, the payload and the result channel; the document declares the interface and defines no operation of it |
| Internal audit | Reviews the record fields, the absence of a person and the stable order of the reads |
| Data steward | Confirms that no personal field is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `FraudReferral` request | `caseNo` (the case number, DF-CAS-002), `referralReason` (free text, its maximum a parameter row); both required | DF-CAS-002 |
| `FraudReferral` answer | `referralId` (the id of the first entry of the chain), `caseNo`, `state` (`REFERRED`), `ruleId` (DF-DEC-004), `ruleVersion` (DF-DEC-005), `sentAt`, `externalReference`, and for the single read `verdictReference` (DF-DEC-001 of the verdict), `resultCode`, `investigationReference`, `receivedAt` and `entryCount` | DF-DEC-001, DF-DEC-004, DF-DEC-005 |
| `FraudReferralResult` request | `resultCode` (validated against the codes in force), `investigationReference`, `resultNote` (free text, its maximum a parameter row) | Not specified in the source documents (DOR-RWB-P4-E8018-CON-7) |
| `FraudReferralResult` answer | `referralId`, `caseNo`, `state` (`ANSWERED`), `resultCode`, `investigationReference`, `receivedAt` | Not specified in the source documents (DOR-RWB-P4-E8018-CON-7) |
| `FraudReferralPage` | `items[]` of `FraudReferral`, `page`, `size`, `total` | Not specified in the source documents (DOR-RWB-P4-E8018-CON-7) |
| The record entry, as declared | `decision_code` DF-DEC-003 as the record code of a referral, `case_id` DF-DEC-002, `rule_id` DF-DEC-004, `rule_version` DF-DEC-005, `model_version` DF-DEC-006, `inputs_ref` DF-DEC-008 with the referral id, the case number, the verdict reference, the external reference and the grant id, `final_call` DF-DEC-012 as the state, `actions` DF-DEC-014, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | DF-DEC-002, DF-DEC-003, DF-DEC-004, DF-DEC-005, DF-DEC-006, DF-DEC-008, DF-DEC-012, DF-DEC-014, DF-DEC-016, DF-DEC-017, DF-DEC-018 |
| Case, as consumed | `case_no` DF-CAS-002, `product_group` DF-CAS-003, `status` DF-CAS-005, `stage_code` DF-CAS-006, `deviation_open` DF-CAS-019, `legal_hold` DF-CAS-020, `rule_version` DF-CAS-021, and the fraud flag as P3 composes it | DF-CAS-002, DF-CAS-003, DF-CAS-005, DF-CAS-006, DF-CAS-019, DF-CAS-020, DF-CAS-021 |
| Verdict, as consumed | `id` DF-DEC-001, `case_id` DF-DEC-002, `decision_code` DF-DEC-003, `rule_id` DF-DEC-004, `rule_version` DF-DEC-005, `model_version` DF-DEC-006 and `decided_at` DF-DEC-016 | DF-DEC-001, DF-DEC-002, DF-DEC-003, DF-DEC-004, DF-DEC-005, DF-DEC-006, DF-DEC-016 |
| Roles and letters | The role code and the capability areas of `role` DF-REF-034 to DF-REF-039 and `permission` DF-REF-040 to DF-REF-044, read behind the authorise answer | DF-REF-034 to DF-REF-044 |
| Record event | `rwb.decision.DecisionRecorded.v1` with the entry of a referral or of a state change, from the DP-03 library | Not specified in the source documents (DOR-RWB-P4-E8018-CON-7) |
| Refusal | `messageId` MSG-P4-001 on a 401, MSG-P4-002 on a 403, MSG-GEN-004 on a 404 and on a 409 state conflict, MSG-P1-001 on a stale data product, MSG-GEN-001 and MSG-GEN-002 on a 422 and MSG-P7-003 on a 503 | Not specified in the source documents (DOR-RWB-P4-E8018-CON-7) |

The exact request and answer field set of the four operations, the type and length of each field, the record code of a referral, the name of the closing result codes and the shape of the verdict are Not specified in the source documents (GAP-0880; ASM-1597): FSD P4 v3 A2.29 names the journey and one validation rule (VR-P4-029-1) and no operation and no field, TSD P4 v3 appendix T-A declares the role, reference-data, rule-package and workflow operations and not this gate, and the legacy story's endpoints are the rule-version template's (GAP-0883). The state set is Not specified either and is fixed here as `SENT`, `RESULT_RECEIVED`, `CLOSED` and `FAILED` (ASM-1598). The field on which the case answer carries the fraud flag is Not specified: `recovery_case` has no fraud column (DF-CAS-001 to DF-CAS-023) and the flag is composed by P3 from the X4 deviation that S8 holds (GAP-0881; ASM-1599). The Aric payload, its protocol and its result channel are Not specified and are declared as an external dependency with no owner (GAP-0882; ASM-1600).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/fraud-referrals` | `FraudReferral` in (`caseNo`, `referralReason`); `FraudReferral` out in state `SENT` with `referralId`, `ruleId`, `ruleVersion`, `sentAt`, `externalReference` and the `Location` of the referral read | Rules and parameters C; `Idempotency-Key` required |
| POST | `/admin/fraud-referrals/{referralId}/results` | `FraudReferralResult` in (`resultCode`, `investigationReference`, `resultNote`); the moved referral out in state `RESULT_RECEIVED` or `CLOSED` | Rules and parameters U; `Idempotency-Key` required |
| GET | `/admin/fraud-referrals/{referralId}` | `FraudReferral` out: the referral with its state, its verdict reference, its rule id and version, its external reference, its result fields and its entry count | Rules and parameters R, scope applied |
| GET | `/admin/fraud-referrals` | `FraudReferralPage` out: `items` of `FraudReferral`, `page`, `size` and `total`, filtered by `caseNo` and by `state` | Rules and parameters R, scope applied |

Errors for all four: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 404 a referral id that does not exist (MSG-GEN-004), 409 a case not flagged, a verdict that does not require a referral, an open referral or a state that does not allow the action (MSG-GEN-004) and a stale data product (MSG-P1-001), 422 a required field empty or of the wrong shape (MSG-GEN-001) and a value out of range (MSG-GEN-002), 503 the record cannot be written or the outside send cannot be completed (MSG-P7-003). The two writes require an `Idempotency-Key` and a replay answers the first answer with no second entry and no second send (BR10); the two reads carry none. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR9).

The four paths are fixed here (GAP-0880; ASM-1597) and confirmed by the contract review before they are frozen. No case, verdict or freshness operation is declared as provided in this document.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The C, U and R checks behind the four operations, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget, with the version in force (DP-06) |
| GET | `/api/recovery/case/v1/cases/{caseNo}` | P3 rwb-case | The case: its reference, its product group, its status and its fraud flag in force |
| GET | `/api/recovery/decision/v1/decisions?caseId={caseId}` | P7 rwb-decision | The fraud verdict: its decision reference, its rule id, its rule version, its model version and its outcome |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The freshness of the product the case is read from, for the MSG-P1-001 refusal of VR-P4-029-1 |

None of the five is declared as provided by rwb-access. The case read is the path of Arch v5 slide 14 (`GET /cases/{id}`) on the P3 base; the decision read is the path of Arch v5 slide 14 (`GET /decisions?caseId=`); the freshness read is the data-product freshness operation of the API specification, P1's. This story's metadata contract-dependency list carries only `RWB-P3-E1042-CON`, which is the missing dependency of GAP-0880 and ASM-1597 and is not added to the metadata.

**Aric, the outside system.** The transport to Aric is declared in the document as an external dependency of the contract, in a section of its own, and it is not a REST operation of any service:

| Item | Declaration |
|---|---|
| System | Aric, outside the bank (FSD P4 v3 A2.29, integration points) |
| Owner of the interface | None in the target: the catalogue, the API specification and the ownership map declare no Aric operation and no service owns it (GAP-0882; ASM-1600) |
| Operation, protocol, credentials, result channel | Not specified in the source documents (GAP-0882; ASM-1600) |
| How the contract refers to it | One named external dependency with a client budget read through DP-06, referenced by the referral and result operations and by no path of this document |
| In tests | A fake, switched by the test, that answers an external reference, a refusal or a timeout (AC6) |

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a referral or of a state change with its case reference, referral id, verdict reference, rule id, rule version, model version, state, external reference and time, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This document declares the record message only. `rwb.access.AccessPolicyChanged.v1` is RWB-P4-E1037-APP's and `rwb.access.DoaLimitChanged.v1` is RWB-P4-E8008-APP's, and a fraud referral publishes neither (Architecture v5 slides 14 and 43); no referral is announced on `rwb.access.events.v1`, because the referral is this service's record and not a fact another service reacts to.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 and TSD P4 v3 T5.3 states "Events: None" for the module. The document declares no inbox, no consumer group and no subscription: the referral reads the case, the verdict and the freshness at request time. The legacy trigger "a completed ACE batch, an event or a timer" is read as that request path (GAP-0883; ASM-1601).

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: the referral and the result are synchronous, and the outside send is one call inside the request with the budget read through DP-06. The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only (BR11), and the Aric transport is the external dependency of section 12.2 and not an activity of this service.

#### 12.6 Schedules

None. All four operations are request-driven, and the referral adds no timer and no batch: the verdict it reads is already recorded by the rule path that decided it.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The role code recorded with an entry and the role class of the service identity |
| `permission` | P4 (rwb_access) | The C, U and R letters of Rules and parameters and the role they are held through |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The referral entry and each state change that the record event carries and the reads answer |
| `outbox_event`, `idempotency_key` | PLT library, created in rwb_access | The outbox row of each entry and the stored request and answer of each write, so one key answers once (DP-09; ASM-0074) |

No table of another service is named in the contract (DP-01): `recovery_case` is P3 rwb_case's, `decision_log_entry` and `rule_row` are P7 rwb_decision's, `data_product` is P1 rwb_source_data's and `deviation` is S8 rwb_deviation's. No table is created for a referral, and the document holds no customer field and no case data beyond the reference (BR5, BR7).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| case fake | `GET /cases/{caseNo}` answering "RW-2026-000123" with product group `MORTGAGE`, status `IN_PROGRESS` and its fraud flag in force, a case with no fraud flag, a case that does not exist and a 503 (GAP-0880; ASM-1597) | App story, contract tests, harness |
| verdict fake | `GET /decisions?caseId=` answering the fraud verdict with decision reference "DL-2026-000981", ruleId "R-UNI-08", ruleVersion "FRAUD-2027-01", modelVersion "DMN-FRAUD-3" and an outcome, a case with no verdict, a verdict whose outcome is not the referral outcome and a 503 (GAP-0880; ASM-1597) | App story, contract tests, harness |
| freshness fake | `GET /data-products/freshness` answering a fresh product for 2026-11-22 and a stale product from 2026-11-21 (GAP-0880; ASM-1597) | App story, contract tests |
| parameters fake | `GET /admin/parameters` with the page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget at the version in force | App story, contract tests |
| authorise fake | `POST /authorise` with a granted answer for RW-COE with C, U and R, for RW-RISK with A, C, U and R, and for RW-AUDIT and RW-FRAUD with R, and a refused answer with MSG-P4-002 for RW-PHONECOL with a dash and for RW-FRAUD on the two writes | App story, contract tests, harness |
| decision-record fake | The append of a referral and of each state change, the hash-link check, a seeded state path of three entries, the duplicate check over an open referral and a forced failure | App story, contract tests |
| Aric transport fake | An accepted referral with externalReference "ARIC-2027-004417", a refusal with its own reason, a timeout and the same answer for a repeated `Idempotency-Key` (GAP-0882; ASM-1600) | App story, contract tests, harness |
| gateway-bff fake | The composite route of SCR-03 with the case as `rwb-case` answers it and the referral panel that calls the two reads | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 5 consumed | The referral, the result and the two reads provided; the authorise, parameters, case, decision and freshness operations consumed; one hop, 2 s timeout |
| External interface | 1 declared | The Aric transport, with no owner, no path and no operation in this document (GAP-0882; ASM-1600) |
| Kafka | 1 event type published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output; the outside transport is an interface call and not a file |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-fraud-referral-v1.yaml` (OpenAPI 3.1) with the four operations and the shared components, `contract/error-envelope.yaml`, the `FraudReferral`, `FraudReferralResult` and `FraudReferralPage` schemas with their examples, the state-set rule and the versioning rules in the contract README, the external-dependency section for Aric, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. The four contract reads are consumed and faked, and the missing C dependencies are carried in the key's gap and not added to this story's metadata (GAP-0880; ASM-1597). There is no DP-04 and no DP-16: this document declares no rule evaluation and no P2 integration path, and the Aric transport is an external dependency of the contract rather than an adapter of `rwb-integration` (GAP-0882).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The four operations with the shapes of section 11: the referral, the result, the single read, the page and the paging, and the required fields.
3. The state set of BR7, stated in the document and in the contract README, with the transition each state allows and the one it refuses, and with the statement that the state lives on the entries of the local decision-record chain.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget, and the explicit statement that no case, verdict or freshness operation is provided here.
5. The external-dependency section for Aric, with no owner, no path and no operation, and with the client budget behind it as a parameter row.
6. The error envelope and the message-ID mapping for 401, 403, 404, 409, 422 and 503, with the texts of the legacy messages, MSG-GEN-002 as an ID with its source named and MSG-P1-001 with its text.
7. The seven fakes and the stub fixtures of section 12.8, including the flagged and unflagged cases, the verdict with and without a referral outcome, the fresh and stale products and the outside transport's three answers.
8. The six contract tests; a drift between a fake and the document fails the build.
9. Baseline tag and the consumer sign-off note from the app story, the SCR-03 route, the P3, P7 and P1 tech leads, the Aric interface owner and the harness.

**Feature switch.** The four operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter. The readiness of the Aric interface is stated as an operating condition of the environment and not as a flag of this document.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8018-APP | The four provided operations, the three schemas, the state set and the seven fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-03) | The two reads as the referral panel calls them |
| The `rwb-case` tech lead | The case read and the parameters read as consumed, and that no case table or fraud column is claimed here |
| The `rwb-decision` tech lead | The decision read as consumed, the verdict fields the entry copies and the record message |
| The `rwb-source-data` tech lead | The freshness read as consumed and the MSG-P1-001 refusal this feature produces |
| The owner of the Aric interface | The external-dependency declaration, the one adapter, and that no operation of Aric is defined by this document |
| The harness of the wave 4 access journey | The referral state, the rule id and the rule version as the evidence it records |

The record code of a referral, the name of the closing result codes and the shape of the verdict are Not specified in the source documents (GAP-0880; ASM-1597), and the Aric protocol, the credentials and the result channel are Not specified either (GAP-0882; ASM-1600): all four are confirmed with the fraud team, the decision-record library owner and the Aric interface owner before the operations are frozen.

**Done when.** The document validates in the pipeline, the six contract tests pass, the seven fakes answer every declared path and status, the P3, P7 and P1 tech leads have accepted the four consumed operations, the owner of the Aric interface has accepted the external-dependency declaration, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters C, U or R calls the operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, or `caseNo` is not of the shape in force | Enter {field}. |
| MSG-GEN-002 | A value is outside its range: a reason or note above its maximum length, or `size` above its maximum | Not specified in the source documents (CG-ALL-5673) |
| MSG-GEN-004 | The case is not flagged, the verdict does not require a referral, a referral is already open, a result is sent for an answered or failed referral, or the referral id does not exist | Someone else changed this record. Reload it to see their change. |
| MSG-P1-001 | The data product the case is read from is stale after a late or failed ACE batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | The record cannot be written, or the outside send cannot be completed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed, and from the Error and Message Standard v4 §4 for MSG-P1-001, whose id is P1's and whose text is copied unchanged (ASM-1602). MSG-GEN-002 carries its message ID with its text Not specified in the source documents (CG-ALL-5673); this baseline adds no wording of its own. MSG-P4-004 is declared because the legacy story lists it for this key, and it is produced as a warning on the two writes, not as an error.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-03 Case record (P3's screen, the referral panel) | Referral, none (empty) | The page with an empty `items` and total 0 and no error |
| SCR-03 Case record | Referral, sent | `FraudReferral` in state `REFERRED` with its rule id, its rule version, its external reference and its sent time |
| SCR-03 Case record | Referral, result received | `FraudReferral` in state `ANSWERED` with its result code, its investigation reference and its received time |
| SCR-03 Case record | Referral, answered (terminal) | `FraudReferral` in state `ANSWERED` with the closing result code and the entry count of its state path |
| SCR-03 Case record | Referral, failed | `FraudReferral` in state `FAILED` with the 503 of the envelope and MSG-P7-003, and a retry action that reuses the same `Idempotency-Key` |
| SCR-03 Case record | Referral, refused | The 403 of the envelope with MSG-P4-002, the 409 with MSG-GEN-004, or the 409 with MSG-P1-001 |
| SCR-03 Case record | Referral, loading | Not specified in the source documents (CG-ALL-5677) |
| SCR-03 Case record | Referral, error | Not specified in the source documents (CG-ALL-5677) |
| SCR-03 Case record | Referral, no access | Not specified in the source documents (CG-ALL-5677) |
| SCR-41 legacy (rule-version screen, GAP-0883) | Empty | Empty state as Screen Specifications v1 SCR-41 gives it (CG-ALL-5679) |
| SCR-41 legacy (rule-version screen, GAP-0883) | Loading | Not specified in the source documents (CG-ALL-5679) |
| SCR-41 legacy (rule-version screen, GAP-0883) | Error | Not specified in the source documents (CG-ALL-5679) |
| SCR-41 legacy (rule-version screen, GAP-0883) | No access | Not specified in the source documents (CG-ALL-5679) |

The screens are served by the gateway-bff composite route (DP-19), which shows the case from `rwb-case` and calls the two reads of this contract, one hop each. The composite route specification and the case record field list belong to RWB-PLT-N001-CON and to the P3 screen work; the document fixes the referral side of the panel only. This contract declares no screen of its own, because the referral runs unattended: the legacy screens SCR-39 and SCR-41 are the rule-version template's and are carried as a gap (GAP-0883). The trigger of the referral is Not specified in the source documents (GAP-0883); no subscription, inbox row or Schedule is declared for it. The empty, loading, error and no access states of SCR-39 are Not specified in the source documents (CG-ALL-5678).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-018-CON-01 | AC1 | Contract | The document validates; the base, the four operations, the rights C, U and R, the five error responses, the `Idempotency-Key` on the two writes and the external-dependency section are present; no case, verdict or freshness operation is provided |
| TC-E8-018-CON-02 | AC2 | Contract | The fields of `FraudReferral`, `FraudReferralResult` and `FraudReferralPage`; the three states and their transitions; no table declared for a referral; no name, identification number, account number or balance |
| TC-E8-018-CON-03 | AC3 | Contract | A 401, 403, 404, 409, 422 and 503 response carry one problem envelope with a valid message ID, and MSG-P1-001 is on the 409 of a stale product |
| TC-E8-018-CON-04 | AC4 | Contract | Five consumed operations with their owners P4, P3, P7 and P1, one hop and the 2 s budget; the Aric transport declared as an external dependency with no owner and no path |
| TC-E8-018-CON-05 | AC5 | Contract | One published event type and no other message; no consumed event; no workflow, no activity and no Schedule; no file input or output |
| TC-E8-018-CON-06 | AC6 | Component | The seven fakes match the document; a drifted fake fails the build; the case fake carries no customer field, the verdict fake carries references only, and the outside transport fake answers no undeclared status |
| TC-E8-018-CON-07 | AC2 | Contract | Boundary of the tables of section 12.7: the role, permission, local decision-record and outbox and idempotency tables are the only tables declared; no table of another service is named and no table is created for a referral |
| TC-E8-018-CON-08 | AC7 | Contract | A schema with an added optional field passes within major version 1; a removed, renamed or retyped field fails and needs a new major version |
| TC-E8-018-CON-09 | AC8 | Contract | Section 8 rules BR1 to BR12 read against the criteria of section 7 and the test rows of section 16; each rule names an existing criterion and test case; architecture-constraint rules name a guardrail or boundary row; proposed test Not specified in the source documents (NEWAC-RWB-P4-E8018-CON-AC7) |
| TC-E8-018-CON-10 | AC9 | Contract | A status change the document refuses is answered with the 409 of the envelope with MSG-GEN-004 and leaves the stored state unchanged; an allowed transition is not refused; proposed test Not specified in the source documents (NEWAC-RWB-P4-E8018-CON-AC8) |

### 17. Guardrails

- No business value in the contract: the page bounds, the reason and note lengths, the fraud package code, the closing result codes and the client budget stay parameter rows behind the document, and the role codes stay rows of `role` and `permission`.
- No personal data in a schema, an example or a fake: case numbers, referral ids, verdict references, rule ids, rule versions, model versions, states, external references, result codes and times only (BR6).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; `recovery_case`, `decision_log_entry`, `data_product` and `deviation` are P3's, P7's, P1's and S8's and are consumed or absent, never named as this service's (BR5).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- One writer for the case and one writer for the referral: the document states that the case, its fraud flag and its holds are P3's and S8's and that the referral state lives on this service's own chain (BR7).
- An outside system is declared as an outside system: the Aric section names no owner, no path and no operation, and a document that declares an Aric operation as a service operation fails the review (BR3).
- The four contract reads are consumed and faked, and the missing C dependencies are carried in the gap rather than added to the metadata (BR8).
- Every example in the document is synthetic; no production case, customer or Aric payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- A write without its `Idempotency-Key` is refused by the contract, and a replay never makes a second send (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DVH-010 | A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared | The referral and result operations as the only path that raises and closes a referral, and the state set with `ANSWERED` reached on the closing code in force; the flag and the hold themselves are P3's and S8's | TC-E8-018-CON-01, TC-E8-018-CON-02 |
| REQ-CWC-018 | A model or agent writing to a queue passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version | The C, U and R declarations on the four operations, and the record entry that carries the identity, the role code and, where a model or agent is the caller, its version | TC-E8-018-CON-03, TC-E8-018-CON-04 |
| NFR-040 | Each screen and each agent receives only the personal data it needs | The schemas, examples and fakes that carry references and codes and no customer field | TC-E8-018-CON-02, TC-E8-018-CON-06 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key. The BRD gives no REQ-DVF identifier for the referral; REQ-DVH-010 is the requirement the BRD actually states for it, and FEAT-DVF-04 is the S8 feature this one depends on (GAP-0883; ASM-1601).

| Legacy reference | Where it is kept |
|---|---|
| AC1 refer a case to Aric, where the fraud rules require it, and take the result back, with the rule version recorded | Sections 4, 7 (AC1, AC2), 11, 12.1, 12.2 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 7, 12.1, 14 |
| The permission checks: Rules and parameters C for RW-COE and A for RW-RISK, carried by the rule-change stories; this story reads Platform administration C, U and R (GAP-0884) | Sections 7 (AC1, AC4), 10, 12.1, 14 |
| The legacy data rows `recovery_case` DF-CAS-001 to DF-CAS-023, `decision_log_entry` DF-DEC-001 to DF-DEC-018, `rule_row` DF-REF-001 to DF-REF-015 and `role` DF-REF-034 to DF-REF-038 | Sections 11, 12.7 |
| The legacy endpoints `POST /admin/rule-versions` on the monolith base and its approve operation, and the screens SCR-39 and SCR-41 | Section 15 and section 19, carried as the rule-version template's and not as this feature's (GAP-0883) |
| The feature FEAT-ADM-13, its dependency FEAT-DVF-04 and the system Aric | Sections 1, 2, 12.2, 12.5 |
| Legacy key RWB-E8-018, story RWB-P4-E8018-APP, contract RWB-P4-E8018-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the referral, the result and the two reads (RWB-P4-E8018-APP).
- The fraud rules themselves, their package and their evaluation (P7 `rwb-decision`; the rule packages of RWB-P4-E2041-APP and RWB-P4-E2042-APP). This document consumes the verdict and declares no rule.
- The X4 fraud screening, the deviation record and its hold (S8 `rwb-deviation`, FEAT-DVF-04).
- The case record and its fraud flag (P3 `rwb-case`). This document consumes the case read and declares no case field of its own.
- The data products and their freshness (P1 `rwb-source-data`). This document consumes the freshness read.
- The integration file adapters, the interface configuration and the outbound items (P2 `rwb-integration`). This document declares no P2 operation and builds no file path.
- The central decision ledger, the query API over `rwb_decision` and the chain verification (P7 `rwb-decision`).
- The screen SCR-03 Case record, its referral panel and its composite route specification (RWB-PLT-N001-CON and the P3 screen work).
- The Aric interface itself: its protocol, its credentials, its contract, its result channel and its ownership outside the bank (GAP-0882; ASM-1600). This document declares it as an external dependency and defines no operation of it.
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases.
