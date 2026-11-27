# RWB-P4-E2019-CON Partner identities through the external gateway

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes.**

- Corrected the decision-record event type name to `rwb.decision.DecisionRecorded.v1` (3 places); the topic `rwb.decision-record.v1` is unchanged.
- Readiness decisions: RD-P1-008.
- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-019 for rwb-access — the contract baseline the external gateway calls to resolve a partner identity to Recovery roles, scopes, the masking policy version and an expiry, with no partner table and no token. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P4-E2019-CON-L227). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 16 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E2019-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Wave note | Wave 2 is the story wave; the rwb-partner runtime baseline is wave 4 (Architecture v5); the build uses fakes of the wave 0 and wave 1 platform and of the P3 and P4 contracts |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E2019-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | Major version 1, base `/api/recovery/access/v1` (section 12.1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-034) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-008, RD-P1-004 |

### 1. Story

As a **tech lead of rwb-access with the external gateway owner**, I want **the published contract baseline of the partner identity resolution: an OpenAPI 3.1 document for one POST on the rwb-access base, the claim set the gateway supplies, the answer that carries the roles, a `PLACED` scope, the matrix version, the masking policy version and an expiry, one refusal vocabulary with its statuses and message ids, the statement that rwb-access holds no partner table and no token, the consumed parameters and reference-data reads, the absent events, and the contract fakes**, so that **the app story, the external gateway and the end-to-end proof of the key can build against one fixed, testable contract on Day 1 without waiting for `rwb-access`, `rwb-partner` or `rwb-case` to be built**.

This contract carries no legacy acceptance criterion: AC6 and AC9 of RWB-E2-019 belong to RWB-P4-E2019-APP, the seven other criteria of the key belong to RWB-ITG-E2019-ITG, and the six criteria of section 7 test the document, the claim set, the answer, the refusal vocabulary, the absence of a partner table and a token, and the fakes. It is one of the three stories of the rwb-access slice of the key, and like them it copies no part of a legacy criterion.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story resolved a partner identity inside one process, where the token issuer, the partner role, the binding, the firm status and the scope were whatever the resolver happened to read. In the target the partner identity is authenticated at the external gateway, and rwb-access is asked one question: which Recovery roles, which scope and which policy versions does this partner identity get. The answer has to be a document before three teams can build against it — the rwb-access resolver, the DMZ gateway that calls it, and the end-to-end proof of the key.

**The division is fixed and is the same in all three stories of this legacy key.** **RWB-P4-E2019-APP**, **RWB-P4-E2019-CON** and **RWB-P4-E2019-INF** are the rwb-access slice: the resolution and its answer, this contract, and the DMZ plumbing that carries the call. **RWB-S9-E2019-APP** owns the firm, the partner user, the binding and the instruction, because `partner`, `partner_user` and `partner_instruction` are S9's under the Ownership Map ruling ASM-0072. **RWB-P7-E2019-APP** owns the central ledger entries a partner sign-in and refusal leave behind. **RWB-ITG-E2019-ITG** is the end-to-end proof and carries legacy AC1, AC2, AC3, AC4, AC5, AC7 and AC8. Because the binding moved to S9, the gateway resolves the partner user and the partner role before it calls rwb-access, and it supplies them as claims; this contract therefore fixes the claim set as the boundary and says so explicitly, instead of naming a table rwb-access may not read.

Fixing that boundary once, with faked consumers, buys three things. The rwb-access resolver can be built before rwb-partner is finished, because the only partner facts it needs are claims in a faked request. The gateway can be built and its mTLS hop tested before the resolver exists, because the answer shape is fixed. And the end-to-end proof has one place to look for what was proved and what was not: the token, the firm and the instruction are proved there, and the roles, the scope, the versions and the refusals are proved here.

The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` (declared and deliberately unused), the shared topic `rwb.decision-record.v1` for the record of a resolution, task queue `rwb-access` in namespace `rwb-recovery`, and Java package `th.co.scb.ace.workbench.recovery.access`. The operation path, the claim names, the answer schema and the expiry rule are named by no source, so the baseline fixes them as a stated default and carries the open point as Not specified in the source documents (GAP-0785; ASM-1432) and (GAP-0785; ASM-1438).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published for the staff view of the same records, and RWB-P4-E2019-INF is the DMZ slice that will carry the partner-side call; neither is a build dependency of this document.
- The partner gateway platform and its FAPI 2.0 profile are RWB-PLT-N007-INF's; this baseline assumes a sender-constrained token whose lifetime is 5 minutes, as that story fixes, and carries the expiry rule of section 11 accordingly.
- RWB-P4-E2019-APP is the owner of the resolver that implements this document; the document describes shapes built from the `role`, `permission`, `masking_rule` and `role_conflict` tables as TSD P4 v3 T3.1 publishes them and adds no column.
- The ownership of the tables and paths comes from the Ownership Map only: `role`, `permission`, `masking_rule` and `role_conflict` are P4's, `partner`, `partner_user` and `partner_instruction` are S9's, `decision_log_entry` is P7's and `lov_value` is P3's. No table of another service is named as this service's (DP-01).
- The parameter and reference-data operations this document consumes are P3's, and their shapes are taken from the P3 contracts rather than restated here (DP-06, DP-07).
- The platform error envelope, the CloudEvents 1.0 envelope and the OpenAPI 3.1 conventions are the platform baseline; where this document narrows them it does so explicitly.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The operation path, the claim names, the answer schema and the refusal vocabulary are Not specified in the source documents (GAP-0785; ASM-1432) and (GAP-0785; ASM-1439); this baseline fixes them and the contract review confirms them before they are frozen.

### 4. Flow

1. Draft the OpenAPI 3.1 document with the base `/api/recovery/access/v1`, the security scheme, the problem responses and the shared components of the service.
2. Fix the one operation, `POST /partner-identities/resolve`, with its purpose, its access rule and its `Idempotency-Key` requirement.
3. Fix the request schema of the claim set: the partner identity reference, the partner id, the partner role code or codes, the firm state and contract end, `amr`, the route and the token expiry, each mapped to the DF field it mirrors.
4. Fix the answer schema: the roles with their class and their `PARTNER_PORTAL` letters, the scope descriptor of type `PLACED` with the partner id and the instruction types, the matrix version, the masking policy version and the expiry.
5. Fix the refusal vocabulary: the status, the message id and the reason of each refusal, drawn from the legacy messages and reasons and from the P4 message catalogue. The 400 refusal for a claim set of the wrong shape has no message id in the sources: Not specified in the source documents (CG-ALL-5264).
6. State the negative boundary in the document itself: rwb-access holds no partner table, no session, no password and no token, and the firm, the binding and the instruction remain rwb-partner's.
7. Declare the consumed parameters and reference-data reads as consumed, each with its owner, one hop and the 2 s client budget; declare the instruction read of the owner as not provided here.
8. Declare that the resolution publishes no event and consumes none, and that the record of a resolution leaves through the DP-03 library on `rwb.decision-record.v1`.
9. Publish the nine tables of section 12 and the contract fakes of section 12.8.
10. Add the contract tests: schema validation, the claim and answer field names, the refusal vocabulary, the boundary statement, the consumed declarations, the absent events and the drift between a fake and the document.
11. Tag the baseline and hand it to RWB-P4-E2019-APP, RWB-P4-E2019-INF and RWB-ITG-E2019-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or declares an S9 partner path | The review refuses the document; the partner portal paths stay rwb-partner's | None | AC1, AC5 |
| X3 | A field of the claim set or of the answer has no DF field behind it, or a required field is optional | The contract test fails | None | AC2 |
| X4 | A refusal is declared without a status, a message id or a reason, or a status falls outside the vocabulary | The contract test fails | None | AC3 |
| X5 | The document, an example or a fake names `partner`, `partner_user`, `partner_instruction`, a session store or a token | The review refuses the document | None | AC4 |
| X6 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X7 | An event is declared as published or consumed by the resolution | The review refuses the document | None | AC5 |
| X8 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X9 | An example carries a personal field, a token or a credential | The contract test fails and the example is refused | None | AC6 |
| X10 | The expiry rule of the answer is left open in the document | The review refuses the document; the rule of section 11 is stated | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the Ownership Map, the platform envelopes, the TSD field names, the P4 message texts and the P3 contract names only |
| Negotiable | The path, the claim names, the answer field names and the expiry rule are confirmed with the gateway owner and the S9 owner; the base, the message ids and the boundary statement are fixed by the target architecture |
| Valuable | Unblocks the resolver, the DMZ slice and the end-to-end proof on Day 1, and keeps the partner table and the token out of rwb-access |
| Estimable | One OpenAPI document, two schemas, one refusal vocabulary, nine contract tables, six fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Partner identity resolution contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the partner gateway fronts the partner routes and supplies the partner facts as claims

  Scenario: AC1 The document declares one resolution operation on the rwb-access base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the partner identity resolution is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /partner-identities/resolve with the owner rwb-access and the PARTNER_PORTAL right R
    Then the operation requires an Idempotency-Key and names its error responses 400, 401, 403 and 503
    Then no partner portal path of rwb-partner, no instruction read and no path of another service appears as provided
    Then the document declares no second operation of this capability

  Scenario: AC2 The claim set and the answer carry the fields the resolver needs (new, D-RCV-60)
    Given the request schema PartnerIdentityClaim and the answer schema PartnerIdentityAnswer
    When the contract test checks the claim and answer schemas against the DF fields and the gateway claims
    Then the claim schema carries partnerIdentityRef, partnerId, partnerRoleCodes, firmPanelStatus, firmContractEnd, amr, route and tokenExpiry
    Then partnerIdentityRef, partnerId, partnerRoleCodes and tokenExpiry are required and route is fixed to "partner"
    Then the answer schema carries roles, scope, matrixVersion, maskingVersion, expiry and decision
    Then each role carries roleCode, roleClass and the PARTNER_PORTAL letters
    Then scope carries type "PLACED", the partnerId and instructionTypes
    Then every field maps to DF-REF-035, DF-REF-037, DF-REF-043, DF-REF-044, DF-REF-202, DF-REF-213, DF-REF-214, DF-REF-215, DF-PRT-005 or DF-PRT-006, or to a claim of the gateway
    Then the answer declares expiry as an instant never later than the tokenExpiry of the claim
    Then the answer declares no token, no refresh token and no session identifier

  Scenario: AC3 The refusal vocabulary is fixed with its statuses, messages and reasons (new, D-RCV-60)
    Given the refusal component of the document
    When the contract test checks each refusal case of the component against its status, message id and reason
    Then a bank identity on the partner route answers 401 with MSG-P4-001 and reason "BANK_IDENTITY_ON_PARTNER_ROUTE"
    Then no partner role, an unknown role or a role of class "BANK_USER" answers 401 with MSG-P4-001
    Then no active binding answers 401 with MSG-P4-001 and reason "NO_PARTNER_BINDING"
    Then no second factor in amr answers 401 with MSG-P4-005
    Then two partner roles, or a partner role with a bank role, answers 403 with MSG-P4-006 and reason "ROLE_CONFLICT"
    Then a firm that is suspended, exited or past its contract end answers 403 with MSG-P4-008 and reason "PARTNER_NOT_ACTIVE"
    Then a claim set of the wrong shape answers 400 with the field named and no message id
    Then a record that cannot be written answers 503 with MSG-P7-003
    Then the document declares no refusal status or message outside this list

  Scenario: AC4 The document states that rwb-access holds no partner table and no token (new, D-RCV-60)
    Given the boundary statement of the document
    When the contract test checks the boundary statement, the examples and the fakes
    Then it states that partner, partner_user and partner_instruction are owned by rwb-partner and are never read by rwb-access
    Then it states that the partner facts arrive as claims of the caller and are not stored
    Then it states that no session table, no password, no access token, no refresh token and no client secret is held
    Then the document names role, permission, masking_rule and role_conflict as the only tables of the capability
    Then an example or a fake that names an S9 table, a session store or a token fails the contract test

  Scenario: AC5 The consumed reads are declared and the events are absent (new, D-RCV-60)
    Given the operations the resolver calls and the topics the capability uses
    When the contract test checks each consumed operation and each topic of the capability
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then GET /api/recovery/case/v1/admin/lists/{listCode} is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then no event is declared as published by the resolution
    Then no event is declared as consumed by the resolution
    Then rwb.access.AccessPolicyChanged.v1 and rwb.access.DoALimitChanged.v1 are named as other stories' and not declared here
    Then the record of a resolution is declared as leaving through rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1
    Then the same record is written on the record path of the resolution, which fails closed with 503 and MSG-P7-003, and is published on the topic, consumed centrally within five minutes and deduplicated by the Idempotency-Key

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the six contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the claims use the synthetic identity "P-5101", the firm "LF-0012" and the roles "PT-LAWFIRM" and "PT-VALUER"
    Then no schema, example or fake carries a name, a postal address, a contact detail or an identity number
    Then no schema, example or fake carries a token, a credential or a private key

  Scenario: AC7 The document declares no workflow and keeps schema changes additive (new, D-RCV-60)
    Given the contract document of the capability
    When its operations, schemas and schedules are checked against the rules of the platform
    Then it declares no workflow, no activity and no Schedule
    Then a schema change within major version 1 is additive, and a removed, renamed or retyped field is refused as a new major version

  Scenario: AC8 Each business rule of section 8 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules table of section 8
    When the contract test checks the Covered by column of each rule
    Then each rule BR1 to BR13 names at least one criterion of section 7 and one test case of section 16
    Then a rule without a covering criterion or test case fails the contract test

  Scenario: AC9 The provided operation declares no 404 answer (new, D-RCV-60)
    Given the error responses of the provided operation
    When the contract test checks the error responses against the refusal vocabulary of AC3
    Then the operation declares the statuses 400, 401, 403 and 503 only
    Then a 404 answer or any other status outside that list fails the contract test

  Scenario: AC10 The document declares no status transition (new, D-RCV-60)
    Given the operations and schemas of the capability
    When the contract test checks them for a status field and a transition
    Then the document declares no status field and no transition
    Then a request for a status change matches no declared operation and fails the contract test
```

These ten criteria test the artefact only. No criterion restates a legacy acceptance criterion: AC6 and AC9 of RWB-E2-019 belong to RWB-P4-E2019-APP, and AC1, AC2, AC3, AC4, AC5, AC7 and AC8 belong to RWB-ITG-E2019-ITG.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path, and the partner portal paths stay rwb-partner's | DP-13; Architecture v5 slides 17 and 41 | AC1, AC5 (TC-E2-019-CON-01, TC-E2-019-CON-05) |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the Ownership Map | DP-11; Ownership Map v1 | AC5 (TC-E2-019-CON-05) |
| BR3 | Error responses use one RFC 9457 envelope and one message id per condition; the business texts of the legacy messages are kept unchanged | Architecture v5 slide 11; legacy RWB-E2-019 section 14 | AC3 (TC-E2-019-CON-03) |
| BR4 | The schemas carry the TSD P4 v3 T3.1 field names and the claim names this baseline fixes, and add no field of another service | TSD P4 v3 T3.1, T3.2; DP-01 | AC2 (TC-E2-019-CON-02) |
| BR5 | The partner facts in the claim set mirror the fields rwb-partner owns and are claims, not rows: rwb-access reads no S9 table | Ownership Map ruling ASM-0072; DP-01 | AC4 (TC-E2-019-CON-04, TC-E2-019-CON-07) |
| BR6 | The answer carries roles, a `PLACED` scope, the matrix version, the masking policy version and an expiry, and nothing else | Architecture v5 slide 14; legacy RWB-E2-019 AC1 and AC2 | AC2 (TC-E2-019-CON-02) |
| BR7 | The refusal vocabulary is 400, 401, 403 and 503 with MSG-P4-001, MSG-P4-005, MSG-P4-006, MSG-P4-008 and MSG-P7-003 and the four reasons of the legacy story | legacy RWB-E2-019 sections 5 and 14; FSD P4 AC-EXC-P4-001-03 | AC3 (TC-E2-019-CON-03) |
| BR8 | The expiry of an answer is an instant never later than the token expiry the gateway supplies, and no answer outlives it | Architecture v5 slide 35; RWB-PLT-N007-INF token lifetime | AC2 (TC-E2-019-CON-02) |
| BR9 | The resolution publishes no event and consumes none; the policy events of the service belong to other stories | Architecture v5 slide 14; TSD P4 v3 T5.3 | AC5 (TC-E2-019-CON-05) |
| BR10 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC7 (TC-E2-019-CON-08) |
| BR11 | A POST requires an `Idempotency-Key`; a replay answers the first answer and writes no second record | Architecture v5 slide 11; DP-09 | AC1 (TC-E2-019-CON-01) |
| BR12 | The contract declares no workflow, no activity and no Schedule for the capability | Architecture v5 slide 14; TSD P4 v3 T5.3 | AC7 (TC-E2-019-CON-08) |
| BR13 | No example, fake or event payload carries a personal field, a token or a credential | NFR-040; NFR-052; ADR-010 | AC6 (TC-E2-019-CON-06) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the two schemas, the refusal vocabulary, the boundary statement and the consumed reads are described | In review |
| In review | Consumer sign-off | The resolver, the DMZ slice and the end-to-end proof accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a refusal changes its status | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | The gateway token lifetime changes | RWB-PLT-N007-INF changes the lifetime the expiry rule refers to | Baselined, with the expiry rule restated |

The state set a resolution answer itself runs through — resolved, refused, expired — is the resolver's and is not a resource state of this document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the refusal vocabulary and the fakes; tags the baseline |
| The external gateway owner (RWB-P4-E2019-INF, RWB-PLT-N007-INF) | Reviews the claim set, the operation and the expiry rule as the caller that supplies them |
| The rwb-partner service owner (S9) | Confirms that the partner identity, the firm, the binding and the instruction stay S9's and that the claim set carries them without a table read |
| Solution architect | Approves a breaking change and a new major version, and confirms the boundary statement |
| Security architect | Confirms that no token, credential or personal field is declared, and that the expiry rule matches the FAPI 2.0 token lifetime |
| Data steward | Confirms that no claim or answer field carries a personal field beyond the partner identity reference |
| No delegation of authority level applies | A role, a scope and a masking version are not a credit decision |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `PartnerIdentityClaim` | `partnerIdentityRef` (DF-REF-213 identity_ref), `partnerId` (DF-REF-214 partner_id), `partnerRoleCodes` (DF-REF-215 role_code), `firmPanelStatus` (DF-PRT-005), `firmContractEnd` (DF-PRT-006), `amr`, `route`, `tokenExpiry` | DF-REF-213, DF-REF-214, DF-REF-215, DF-PRT-005, DF-PRT-006; amr, route, tokenExpiry: Not specified in the source documents (DOR-RWB-P4-E2019-CON-7) |
| `PartnerIdentityAnswer` | `roles` with `roleCode` DF-REF-035, `roleClass` DF-REF-037 and `letters` DF-REF-043, `scope` with `type` "PLACED" and `partnerId` DF-REF-214 and `instructionTypes`, `matrixVersion` DF-REF-044, `maskingVersion` DF-REF-202, `expiry`, `decision` | DF-REF-035, DF-REF-037, DF-REF-043, DF-REF-044, DF-REF-202, DF-REF-214; expiry and decision: Not specified in the source documents (DOR-RWB-P4-E2019-CON-7) |
| Refusal | `status` 400, 401, 403 or 503; `messageId` MSG-P4-001, MSG-P4-005, MSG-P4-006, MSG-P4-008 or MSG-P7-003; `reason` `BANK_IDENTITY_ON_PARTNER_ROUTE`, `NO_PARTNER_BINDING`, `ROLE_CONFLICT` or `PARTNER_NOT_ACTIVE` | Not specified in the source documents (DOR-RWB-P4-E2019-CON-7) |
| Scope type | `PLACED`, the legacy scope name, with the partner id and the instruction types; it is a descriptor of a partner session and is not added to `LOV-SCOPE` of TSD P4 v3 T3.2, which holds OWN, TEAM, REGION and ALL | DF-REF-214 for partnerId; type PLACED: Not specified in the source documents (DOR-RWB-P4-E2019-CON-7) |
| Record event | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` with the `AC-SIGN` or `AC-DENY` entry of a resolution, from the DP-03 library | Not specified in the source documents (DOR-RWB-P4-E2019-CON-7) |
| Named and not owned | `partner`, `partner_user` and `partner_instruction` (S9), `decision_log_entry` (P7), `lov_value` (P3) — named in the boundary statement only | None: named only, no field of this contract |

The operation path, the claim names, the answer field names and the refusal vocabulary are Not specified in the source documents (GAP-0785; ASM-1432): TSD P4 v3 appendix T-A lists API-P4-004 to API-P4-021, API Specification v5 declares no `x-module: P4` partner path, and Architecture v5 slide 14 names `/authorise`, `/me/permissions`, `/doa-limits` and `/masking-policies` only. The expiry rule is Not specified in the source documents (GAP-0785; ASM-1438): the only lifetime the sources fix is the gateway token lifetime of RWB-PLT-N007-INF. The mapping of a refusal to a status is Not specified in the source documents (GAP-0785; ASM-1439) and is fixed by AC3. The absence of an event is Not specified in the source documents (GAP-0785; ASM-1440) and is fixed by BR9 and AC5.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/partner-identities/resolve` | `PartnerIdentityClaim` in, `PartnerIdentityAnswer` out, or one problem detail of the refusal vocabulary; `decision` is `RESOLVED` on the answer | PARTNER_PORTAL right R of the gateway workload identity; `Idempotency-Key` required |

Errors: 400 a claim set of the wrong shape with the field named, message id Not specified in the source documents (CG-ALL-5264), 401 MSG-P4-001 for a bank identity on the partner route, no partner role and no binding, 401 MSG-P4-005 for no second factor, 403 MSG-P4-006 for two roles or a partner role with a bank role, 403 MSG-P4-008 for a firm that is not active, 503 MSG-P7-003 where the record cannot be written. Major version 1 sits in the base; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version (BR10). A replay of the same `Idempotency-Key` answers the first answer and writes no second record (BR11).

The path is Not specified in the source documents (GAP-0785; ASM-1432). It follows the base rule of DP-13, it duplicates no path of rwb-partner, and the contract review confirms it before it is frozen.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The instruction types of a partner role and the approval role of the binding, at the version in force (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | `LOV-ROLE-CLASS`, `LOV-CAPABILITY` and `LOV-SCOPE` at the version in force (DP-07) |

Neither is declared as provided by rwb-access, and no operation of rwb-partner, rwb-decision or rwb-case appears in the document as provided.

#### 12.3 Events published

None. The resolution publishes no event of its own; rwb-access publishes `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` from other stories only (BR9). The record of a resolution leaves through the DP-03 library as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, which is the platform library's event and is declared here only to say where the record goes.

#### 12.4 Events consumed

None. The document declares no inbox, no consumer group and no subscription: the versions in force are read at resolution time through the P4 tables and the P3 contracts, and the policy events that refresh a cache elsewhere are not this capability's (BR9, ASM-1440).

#### 12.5 Workflows and activities

None. No workflow, no activity and no signal is part of this contract: the resolution is synchronous, and the `rwb-access` queue carries only the access review Schedule of RWB-P4-AD008-APP (BR12).

#### 12.6 Schedules

None. The resolution is request-driven, and no effective date, refresh or review is a Schedule of this document.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (rwb_access) | The partner role rows of class `PARTNER_USER` behind `roles` |
| `permission` | P4 (rwb_access) | The `PARTNER_PORTAL` letters and the matrix version behind `letters` and `matrixVersion` |
| `masking_rule` | P4 (rwb_access) | The masking version behind `maskingVersion` |
| `role_conflict` | P4 (rwb_access) | The pairs behind the `ROLE_CONFLICT` refusal |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | The `AC-SIGN` and `AC-DENY` entry of a resolution |

**No partner table and no token are declared, owned or read.** `partner`, `partner_user` and `partner_instruction` are S9 rwb-partner's (Ownership Map ruling ASM-0072), `decision_log_entry` and `approval` are P7 rwb-decision's, and `lov_value` is P3 rwb-case's. The contract states that rwb-access resolves a partner identity to P4 roles and scopes from the partner-supplied claims and its own `role`, `permission` and `masking_rule` data, and reads no S9 table (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Claim fake | The claim set of AC6 and AC9 plus the refusal cases | The resolver, the contract tests, the end-to-end proof |
| Answer fake | A resolved answer for `P-5101` with `PT-LAWFIRM`, scope `PLACED` and `LF-0012`, matrix version `PM-2026.11`, masking version `MASK-SIT-01` and a five-minute expiry | The DMZ slice, the resolver, the end-to-end proof |
| Parameters fake (P3) | `GET /admin/parameters` with the instruction types `FILE_SUIT,ENFORCE`, `APPRAISE` and `COLLECT` at version PAR-2026.11 | The resolver, the contract tests |
| Reference-data fake (P3) | `GET /admin/lists/{listCode}` with the three lists at their versions | The resolver, the contract tests |
| rwb-partner contract fake (S9) | Instruction `INS-2027-000431` of `LF-0019` and the firm states of `LF-0012`, `LF-0019` and `VL-0004`, as the end-to-end proof of AC6 needs them | The end-to-end proof, the resolver's AC6 test |
| Decision-record fake (DP-03) | The append of `AC-SIGN` and `AC-DENY`, the reason, and a forced failure | The resolver, the contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | The resolution provided; the parameters and reference-data reads consumed; one hop, 2 s timeout with a breaker |
| Kafka | 0 published, 0 consumed | No topic is declared for the resolution; the record leaves through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract |
| File | None | No file input and no file output |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-partner-identity-v1.yaml` (OpenAPI 3.1) with the one operation and the shared components, the `PartnerIdentityClaim` and `PartnerIdentityAnswer` schemas with their examples, the refusal component, the boundary statement in the contract README, the versioning rules, and the six WireMock mapping sets of section 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The document names the four P4 tables and the S9 tables as not read | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the record of a resolution leaves through it | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. No ACE view appears in this document | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library, declared as consumed | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case, declared as consumed | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library; the answer feeds the guard, which is declared as the same service's | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout, declared on both consumed reads | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the resolution sits on the P4 base and duplicates no S9 path | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_access`; the document adds no migration and no column | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for the staff view of the same records; a partner never uses it | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline (AC1).
2. The one operation with its access rule, its `Idempotency-Key` and its four error responses (AC1).
3. The two schemas with the field names of section 11 and their DF mapping (AC2).
4. The refusal component with the statuses, the message ids and the four reasons (AC3).
5. The boundary statement of AC4 in the document and in the README: no partner table, no session, no token.
6. The consumed reads with their owners, the one-hop rule and the 2 s budget, and the absent events of AC5.
7. The six fakes and the fixtures of section 12.8, including the resolved answer and the refusal cases (AC6).
8. The six contract tests; a drift between a fake and the document fails the build.
9. Baseline tag and the consumer sign-off note of the resolver, the DMZ slice and the end-to-end proof.

**Feature switch.** The operation is switched by the parameter `rwb.access.partner-signin` of RWB-P4-E2019-APP, not by a flag of this document; the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E2019-APP | The operation, the claim and answer schemas, the refusal vocabulary, the expiry rule and the six fakes |
| RWB-P4-E2019-INF | The operation path, the claim transport and the 5-minute expiry the token lifetime gives |
| RWB-ITG-E2019-ITG | The answer shape, the reasons and the record event as the evidence it records for the end-to-end key |

**Done when.** The document validates in the pipeline, the six contract tests pass, the six fakes answer every declared path, the boundary statement is in the document and the README, and the resolver, the DMZ slice and the end-to-end proof have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No partner role, no active binding, a bank identity on the partner route, or an expired answer | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | An action outside the partner role's letters, refused by the guard or by the owner of the action | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | An instruction of another firm, refused by the owner of the instruction against the `PLACED` descriptor | This case is not in your scope. |
| MSG-P4-005 | `amr` holds no second factor | Sign in again with your second factor. The Workbench needs multi-factor authentication. |
| MSG-P4-006 | Two partner roles, or a partner role and a bank role | Your roles {role} and {otherRole} cannot be held together. Access is refused and the security administrator has been told. |
| MSG-P4-008 | The firm is suspended, exited or past its contract end | Your firm's access to the Recovery Workbench has ended. Contact your SCB partner manager. |
| MSG-P7-003 | The record or the outbox row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message ids are contract elements; the texts are the legacy texts unchanged and their Thai text follows DL10. MSG-P4-002 and MSG-P4-003 are declared because the guard and the owner of the instruction answer them, and neither is produced by this operation itself.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| Partner sign-in page | Resolved | The answer with the roles, the `PLACED` scope and the versions; the portal then reads its own home |
| Partner sign-in page | Refused | The 401 of MSG-P4-001 or MSG-P4-005, the 403 of MSG-P4-006 or MSG-P4-008, and no data |
| PRT-01 Partner home | Empty by scope | The scope descriptor of type `PLACED` with the partner id, which the owner applies to return nothing of another firm |
| PRT-01 Partner home | Session ended | The 401 of an expired answer, with a new resolution required |

The partner portal is served by rwb-partner through the partner gateway; this document fixes the resolution side of that flow only, and the staff view of the same records reaches a screen through RWB-PLT-N001-CON.

Two screens consume this contract: the partner sign-in page and PRT-01 Partner home. No other screen consumes it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-019-CON-01 | AC1 | Contract | The document validates; the base, the one POST, the right, the `Idempotency-Key` and the four error responses are present; no S9 or foreign path is declared |
| TC-E2-019-CON-02 | AC2 | Contract | The claim and answer fields map to DF-REF-035, DF-REF-037, DF-REF-043, DF-REF-044, DF-REF-202, DF-REF-213 to DF-REF-215, DF-PRT-005 and DF-PRT-006; the required fields, the fixed route, the `PLACED` scope and the expiry rule |
| TC-E2-019-CON-03 | AC3 | Contract | Every refusal case of AC3 with its status, message id and reason; a refusal outside the list fails the test |
| TC-E2-019-CON-04 | AC4 | Contract | The boundary statement; no S9 table, no session store and no token in the document, the examples or a fake |
| TC-E2-019-CON-05 | AC5 | Contract | The two consumed reads with their owners, one hop and the 2 s budget; no published and no consumed event; the record event named as the library's |
| TC-E2-019-CON-06 | AC6 | Component | The six fakes against the document; a drifted fake fails the build; a personal-field, token or credential scan of the schemas and examples |
| TC-E2-019-CON-07 | AC4 | Contract | The tables of section 12.7 are the only tables declared; a table outside the five of section 12.7, or one owned by another service, fails the test |
| TC-E2-019-CON-08 | AC7 | Contract | The document declares no workflow, activity or Schedule; a schema change that removes, renames or retypes a field is refused as a new major version |
| TC-E2-019-CON-09 | AC8 | Contract | Each rule BR1 to BR13 of section 8 names a criterion of section 7 and a test case of section 16; a rule without one fails the test |
| TC-E2-019-CON-10 | AC9 | Contract | The provided operation declares the statuses 400, 401, 403 and 503 only; a 404 answer fails the test |
| TC-E2-019-CON-11 | AC10 | Contract | The document declares no status field and no transition; a request for a status change matches no declared operation and fails the test |

No test in this story is an integration copy: the document and the fakes are exercised against each other, and no `-ITG` variant belongs to it. The partner gateway test route, the partner directory test tenant, the harness pack and its seeding, the evidence report format and the pass/fail gate are Not specified in the source documents (GAP-0403). The eleven legacy cases of RWB-E2-019 are executed by RWB-P4-E2019-APP and RWB-ITG-E2019-ITG: TC-E2-019-06, TC-E2-019-09, TC-E2-019-10 and TC-E2-019-11 here, and TC-E2-019-01, TC-E2-019-02, TC-E2-019-03, TC-E2-019-04, TC-E2-019-05, TC-E2-019-07 and TC-E2-019-08 in the end-to-end proof, and none is renumbered or restated in this contract.

### 17. Guardrails

- No business value in the contract: the role codes, the instruction types, the versions, the reasons and the statuses stay rows, parameters or values behind the document.
- No personal data in a schema, an example or a fake: the partner identity reference, the partner id, the role codes and the versions only.
- No token, refresh token, secret or private key is declared, and the document states that rwb-access holds none (ADR-010).
- One REST base, one topic and one event-name pattern per service; a document that names another service's base or topic fails the review (DP-13).
- The partner table, the binding and the instruction stay out of this document: they are S9's, and a path or a table of theirs declared here fails the review (ASM-0072).
- The partner portal paths of rwb-partner are never re-declared as this service's.
- Every example is synthetic; no production payload is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-012 | Partners only through the external gateway, with MFA, scoped to their own cases | Epic 2, 3.4; Program 5.4 | FEAT-OCC-13 | 12 Manage partners | BR1 to BR13 | TC-E2-019-CON-01 to TC-E2-019-CON-11 |

| Legacy reference | Where it is kept |
|---|---|
| The identity, the role and the scope of a partner session | Sections 7, 11, 12.1 — as the answer shape |
| The refusal cases of the legacy story | Sections 7 (AC3), 11, 12.1, 14 — as the vocabulary, not as criteria |
| AC6 and AC9 of RWB-E2-019 | Carried verbatim by RWB-P4-E2019-APP |
| AC1, AC2, AC3, AC4, AC5, AC7 and AC8 of RWB-E2-019 | Carried by RWB-ITG-E2019-ITG |
| The firm, the binding and the instruction | RWB-S9-E2019-APP; named only, never read (ASM-0072) |
| The central ledger entry of a partner sign-in and refusal | RWB-P7-E2019-APP; the local record is written through RWB-P4-E1039-APP |
| The DMZ gateway that calls this document | RWB-P4-E2019-INF and RWB-PLT-N007-INF |

The seven criteria of this key that this slice does not own — AC1, AC2, AC3, AC4, AC5, AC7 and AC8 — are carried by **RWB-ITG-E2019-ITG** alone, and no part of them is restated in this contract.

### 19. Out of scope

- The implementation of the resolver and the seed of the role, permission, masking and conflict rows (RWB-P4-E2019-APP).
- The partner gateway, its certificates, its mTLS hop, its network policy and its rate limit (RWB-P4-E2019-INF, RWB-PLT-N007-INF).
- The firm, the partner user, the binding, the instruction and every partner portal operation (`rwb-partner`, S9; RWB-S9-E2019-APP), including `GET /partner/instructions` and its accept, results, invoices, data room and bid paths.
- The central decision ledger and its read (rwb-decision, P7; RWB-P7-E2019-APP), and the access-entry writer itself (RWB-P4-E1039-APP).
- The end-to-end journey of the key and its evidence (RWB-ITG-E2019-ITG).
- The parameter catalogue and the reference-data lists (`rwb-case`, P3), consumed and faked, never defined here.
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
