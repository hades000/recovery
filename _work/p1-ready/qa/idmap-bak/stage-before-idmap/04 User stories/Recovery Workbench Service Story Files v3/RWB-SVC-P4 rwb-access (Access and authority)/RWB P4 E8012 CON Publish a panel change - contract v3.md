# RWB-P4-E8012-CON Publish a panel change

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8012-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P4-E8012-CON-16) |
| Depends on (build) | None |
| Contract dependencies | Not specified in the source documents (GAP-2281) |
| Contract version | 1 (major version 1 in the path; REST base /api/recovery/access/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-008, RD-P1-004 |

**Version 3 changes.**

- Corrected the decision-record event type name to `rwb.decision.DecisionRecorded.v1` (1 place); the topic `rwb.decision-record.v1` is unchanged.
- Readiness decisions: RD-P1-008.
- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-012 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 9 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **RW-TRIBE Tribe lead and squad members**, I want **the published contract baseline of the publication gate of `rwb-access`: an OpenAPI 3.1 document for the publication and the list, the `ConfigVersion` and `ConfigVersionPage` schemas with the three version labels, the dates and the publishing role code and no person, the state set of LOV-VERSION-STATUS with its two derived states, one RFC 9457 error envelope with its message IDs, the consumed authorise and parameters operations with their owners and the 2 s budget, the contract tables of section 12 and the five contract fakes**, so that **the app story, the SCR-43 route, the `rwb-case` team and the integration harness can build against a fixed, testable contract on Day 1 without waiting for `rwb-access` or `rwb-case` to be built**.

This contract carries no legacy acceptance criterion: AC1 of RWB-E8-012 belongs to RWB-ITG-E8012-ITG and AC2 to RWB-P4-E8012-APP, and the six criteria of section 7 test the document, the schemas and the state set, the envelope, the consumed declarations and the fakes.

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, the shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two operations provided, and nothing else: the write `POST /admin/config-versions/{versionId}/publish`, which puts a configuration version in force from a date and answers it; and the read `GET /admin/config-versions`, which answers the configuration versions this service holds with the state each of them is in today.
- A **configuration version** is a label triple over rows this service already owns: `permission.matrix_version` (DF-REF-044), `masking_rule.masking_version` (DF-REF-202) and `delegation_limit.limit_version` (DF-REF-055), with the `valid_from` and `valid_to` those rows carry. No table is created for it and the document declares none: `versionId` is the identity this contract gives the triple, and the scheme that builds it is fixed here because no source defines one (GAP-0872; ASM-1583).
- The state set is LOV-VERSION-STATUS of TSD P4 v3 T3.2: `LOADED`, `VALIDATED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED`. `IN_FORCE` and `SUPERSEDED` are derived from the rows' `valid_from` and `valid_to`; the other five are read from the decision-record entry of the version, because the three tables carry no state column in TSD P4 v3 T3.1. The document states which of the seven this service writes and which the calendar produces (GAP-0872; ASM-1583).
- The "panel" of this key is the **access panel**: roles, permission letters, default scope, masking rows and limits. The **partner panel, the partner firm, the partner users, the fee schedule and the partner service levels are S9's** — the ownership map gives `partner`, `partner_user` and `partner_instruction` to `rwb-partner` — and their operations appear in this document as neither provided nor consumed (GAP-0872; ASM-1583).
- **No Schedule and no workflow** is declared for the capability. The version in force is resolved at read time by `POST /authorise` as the version whose `valid_from` ≤ today < `valid_to`, so an effective date needs no promotion job, and the six-monthly access review list (JOB-18) stays the only Schedule of the service (ASM-1584).
- The publication is reached from SCR-43 Roles and access through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON); this document fixes the two operations the route calls and no screen surface.
- The document declares two messages as contract elements: `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, the one business event of the capability, which Architecture v5 slide 43 gives every service as a consumer with the note "cache refresh"; and `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1`, the entry of the publication appended to the local chain of DP-03. Neither payload carries a person (BR5, BR10).

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story published a panel change inside a screen of the monolith, where the panel, its approval and the decision log were rows of one schema, the change was a screen in the same module and the only way to date it was to release. In the target the panel is `rwb-access`'s, the date is data, and every other service has to agree on what "in force from a date" means before anything is built.

Two things must therefore be fixed once. The first is the boundary: which operation writes the window and the record (this publication), which operation reads the version in force (the own `authorise` operation), and which operations belong to another service and are only consumed or absent. The second is what the answer and the record say: the three labels, the effective date, the window, the publishing **role code** and the time — and never the person — because a publication is the evidence that REQ-DRI-011 asks for, and a record that carried the publisher's name would copy personal data into a shared topic that every consumer of the decision record reads.

Fixing the field-level contract once, with faked consumers, lets the app story build in parallel with the parameters contract of `rwb-case` and the local decision-record library, and it catches a drift between a fake and the document in a contract test rather than in an integration window. The baseline also fixes the naming the checks require, so that no path, topic, queue or package is a local choice.

The baseline also states the one thing it is not: it defines no configuration-version table, no partner row and no Schedule. The two `rwb-partner` capabilities that the legacy key shared a name with — the partner panel and FEAT-PRM-02 — are absent from the document, which is what makes the split real and what lets S9 build its own panel without waiting for this gate.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that calls the two operations behind SCR-43 Roles and access, and it is a consumer of this baseline.
- TSD P4 v3 appendix T-A declares the administration operations of the module and **no configuration-version operation at all**: its inventory runs from API-P4-004 to API-P4-021 and declares the reference-load, rule-package, session, access-log and smoke operations only, so neither the publication nor the list is among them. Both paths are therefore fixed by this document (GAP-0872; ASM-1583).
- The fields the schemas carry are those of TSD P4 v3 T3.1: `permission` DF-REF-034 to DF-REF-044, `masking_rule` DF-REF-198 to DF-REF-204 with `valid_from` DF-REF-203 and `valid_to` DF-REF-204, `delegation_limit` DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 with `valid_from` DF-REF-025 and `valid_to` DF-REF-026, and `role` DF-REF-034 to DF-REF-039. The state list is T3.2 LOV-VERSION-STATUS and the lifecycle is T4.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The publication entry is a decision-record entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the fields this gate records and no field of another service.
- The operations and their owners are taken from the ownership map and from Architecture v5 slide 14 and slide 41 only: the two operations of this document are P4's, the authorise operation is P4's first path, the parameters read is P3's, and `partner`, `partner_user` and `partner_instruction` are S9's. No table of another service is named as this service's (DP-01).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7) and sits in contract group CG-W4.

### 4. Flow

1. Draft the OpenAPI 3.1 document for the publication and the list with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope, the `Idempotency-Key` header, the paging parameters and the two schemas.
2. Fix the request and answer of the publication with the fields of section 11: `effectiveFrom`, `reason` and `note` in, and `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state`, `validFrom`, `validTo`, `supersedesVersionId`, `publishedAt` and `publishedByRole` out — and no person field of any kind.
3. Fix the `ConfigVersionPage` schema and the query parameters of the list: the `status` filter over the seven states, and `page` and `size` with their default and maximum held as parameter rows behind the contract.
4. Fix the state set of BR6: the seven values of LOV-VERSION-STATUS, the two that the rows' dates derive, the five that the record carries, and the statement that only `APPROVED` may be published; declare no Schedule, no workflow and no activity.
5. Agree the error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, with the business texts taken from the legacy story where the message already existed, and MSG-P4-004 as the break-glass warning of the answer.
6. Declare the consumed own authorise operation and the `rwb-case` parameters read as consumed, each with its owner, one hop and the 2 s client budget; declare the partner panel, partner firm, partner user and fee-schedule operations of `rwb-partner` as neither provided nor consumed.
7. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes.
8. Add the contract tests: schema validation, the two schemas and their required fields, the state set and its derivations, the envelope and message IDs, the consumed declarations, and drift detection between a fake and the document.
9. Tag the baseline and hand it to RWB-P4-E8012-APP, the SCR-43 route of RWB-PLT-N001-CON, the `rwb-case` tech lead and the harness of the wave 4 access journey.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner, or a partner panel, partner firm, partner user or fee-schedule operation is declared as provided here | The review refuses the document; the operation is declared as consumed or is absent | None | AC1, AC5 |
| X3 | A response of 401, 403, 409, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A schema, an example or a fake carries a name, an e-mail address, a user reference or a partner panel field | The contract test fails; the review refuses the document | None | AC2, AC6 |
| X5 | A state outside the seven of LOV-VERSION-STATUS is declared, or `IN_FORCE` or `SUPERSEDED` is declared as written by a process | The review refuses the document | None | AC3 |
| X6 | The document declares a Schedule, a workflow or an activity for the capability | The review refuses the document | None | AC3 |
| X7 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X8 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |
| X9 | A field of the answer has no source definition | The field is marked with the placeholder and the gap is carried | None | AC2 |

No exception path of this document changes a case, a task, a partner row or a rule package: the document describes this service's own three tables, its own record and its own event, and the only rows its app story writes are the dates of those tables.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, TSD P4 v3 T3.1, T3.2, T4 and T-A, the DP-03 entry schema and the P3 and P4 contracts only |
| Negotiable | The `versionId` scheme, the effective-date bounds and the page bounds are parameter rows and a rule behind the document; the base, the paths, the state set and the envelope are fixed by the target architecture |
| Valuable | Unblocks the app story, the SCR-43 route and the harness on Day 1, and keeps the person out of the record and out of the event of a publication |
| Estimable | One OpenAPI document, one error envelope, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Publish a panel change contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access panel is held by rwb-access as permission, masking_rule and delegation_limit rows with their version labels and date windows, and the partner panel is held by rwb-partner and is absent from this document

  Scenario: AC1 The OpenAPI 3.1 document describes the publication and the list (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the publication gate is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/config-versions/{versionId}/publish and GET /admin/config-versions with the owner rwb-access
    Then the publication names Rules and parameters A, the list names Rules and parameters R, and both name their error responses 401, 403, 409, 422 and 503
    Then the publication requires an Idempotency-Key and the list is a read that carries none
    Then no operation of another service is declared as provided by rwb-access

  Scenario: AC2 The request and answer schemas are fixed and carry no person (new, D-RCV-60)
    Given the ConfigVersion and ConfigVersionPage schemas of the document
    When the build checks the schemas against the document
    Then the request carries effectiveFrom, reason and note, with effectiveFrom and reason required
    Then the answer carries versionId, matrixVersion, maskingVersion, limitVersion, state, validFrom, validTo, supersedesVersionId, publishedAt and publishedByRole
    Then the list carries items of versionId, matrixVersion, maskingVersion, limitVersion, state, validFrom, validTo, publishedAt and publishedByRole, with page, size and total
    Then publishedByRole is a role code and no schema declares a name, an e-mail address or a user reference
    Then the effective-date bounds and the page bounds are read from the parameters contract and never from code
    Then a change of these schemas within major version 1 is additive only

  Scenario: AC3 The state set is fixed and no Schedule and no workflow is declared (new, D-RCV-60)
    Given the state set of a configuration version in the document
    When the state set is checked against LOV-VERSION-STATUS and the document
    Then state is one of LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED of LOV-VERSION-STATUS
    Then IN_FORCE and SUPERSEDED are stated as derived from the valid_from and valid_to of the rows, and the other five as read from the record
    Then only a version in APPROVED is published, and a publication of a version in any other state is a 409
    Then the document declares no Schedule, no workflow and no activity for the capability
    Then the document names no configuration-version, partner, partner_user or partner_instruction table as this service's

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 409, 422 or 503 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001 and 403 carries MSG-P4-002
    Then 409 carries MSG-GEN-004, 422 carries MSG-GEN-001 and 503 carries MSG-P7-003
    Then the break-glass warning of the publication answer carries MSG-P4-004
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed and the partner operations are absent (new, D-RCV-60)
    Given the authorise operation and the parameters read this service calls
    When the build compares the operations of the document with the ownership map
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then the partner panel, partner firm, partner user and fee-schedule operations of rwb-partner appear as neither provided nor consumed here
    Then no operation owned by rwb-case, rwb-partner or rwb-decision is declared as provided by rwb-access

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the five contract fakes of the baseline
    When they are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then the access-panel fixture carries version labels, date windows and state only, and no partner row
    Then no schema, example or fake carries a name, an e-mail address or a personal field, and no answer of this service carries a user reference

  Scenario: AC7 A replay answers the first answer and the publication announces one event and one record entry (new, D-RCV-60)
    Given a publication has been sent with an Idempotency-Key
    When the same request is sent again with the same Idempotency-Key
    Then the answer is the first answer and no second event is published
    Then the publication announces exactly one rwb.access.AccessPolicyChanged.v1 on rwb.access.events.v1 and records exactly one entry on rwb.decision-record.v1
    Then neither payload carries a person

  Scenario: AC8 Each business rule of section 8 is covered by a criterion and a test (new, D-RCV-60)
    Given the business rules BR1 to BR13 of section 8 with their Covered by column
    When the rules are traced to the criteria of section 7 and the test cases of section 16
    Then every rule BR1 to BR13 names at least one criterion of section 7 and one test case of section 16
    Then every criterion named in the Covered by column exists in section 7
    Then no rule is left without a criterion, and an architecture rule is also carried by the boundary test TC-E8-012-CON-07

  Scenario: AC9 A 404 answer of a provided operation is one problem envelope (new, D-RCV-60)
    Given the error envelope component of the document
    When either operation of the document answers 404
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then the message ID of the 404 answer is Not specified in the source documents (NEWAC-RWB-P4-E8012-CON-AC8)
```

These nine criteria test the artefact only. No criterion restates a legacy acceptance criterion: AC1 of RWB-E8-012 — publish a panel change, put the change in force with an effective date and write the result to the decision log with the rule version — is owned by RWB-ITG-E8012-ITG, and AC2 is owned by RWB-P4-E8012-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1 (TC-01) |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5 (TC-05) |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are taken from the legacy story where the message already existed | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4 (TC-04) |
| BR4 | The schemas carry the fields of this gate and no field of another service: no partner panel row, no partner user, no fee schedule and no rule package | DP-01; Ownership Map v1 (`partner`, `partner_user`, `partner_instruction` = S9) | AC2, AC6 (TC-02, TC-06) |
| BR5 | The publishing role is a role code; no schema, example, fake or entry of this contract carries a name, an e-mail address or a user reference | NFR-040; ASM-1585 | AC2, AC6 (TC-02, TC-06) |
| BR6 | The state set of a configuration version is the seven values of LOV-VERSION-STATUS; `IN_FORCE` and `SUPERSEDED` are derived from the rows' dates and the other five are read from the record, and only `APPROVED` may be published | TSD P4 v3 T3.2; T4; GAP-0872; ASM-1583 | AC3 (TC-03) |
| BR7 | A configuration version is a label triple over `permission`, `masking_rule` and `delegation_limit`; no table, view or copy is created or named for it | TSD P4 v3 T3.1 DF-REF-044, DF-REF-202, DF-REF-055; GAP-0872; ASM-1583 | AC3 (TC-03, TC-07) |
| BR8 | The effective-date bounds and the page bounds are parameter rows of `rwb-case` read through DP-06; no bound and no default is a constant in the document or in code | DP-06; FSD P4 v3 A2.23.3.1 VR-P4-023-1; GAP-0872; ASM-1583 | AC2 (TC-02) |
| BR9 | A write requires an `Idempotency-Key`; a replay answers the first answer and publishes no second event | Architecture v5 slide 42; DP-09 | AC1, AC7 (TC-01, TC-08) |
| BR10 | The publication announces exactly one `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` and records exactly one entry on `rwb.decision-record.v1`; neither payload carries a person | Architecture v5 slide 14, slide 41, slide 43; ASM-1585 | AC7 (TC-08) |
| BR11 | The contract declares no workflow, no activity and no Schedule for the capability; the effective date is resolved at read time by the own authorise operation | Architecture v5 slide 14; TSD P4 v3 T4; ASM-1584 | AC3 (TC-03) |
| BR12 | The partner panel, the partner firm, the partner users, the fee schedule and the partner service levels are S9's and appear as neither provided nor consumed; FEAT-PRM-02 is not a prerequisite of this contract | Ownership Map v1; Architecture v5 slide 41; GAP-0872; ASM-1583 | AC5 (TC-05) |
| BR13 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC2 (TC-02) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the state set and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the SCR-43 route, the `rwb-case` tech lead and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a state is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A consumed operation changes | The parameters read or the authorise operation changes | Baselined, with the client budget and the stub restated |

The state set the document fixes for a configuration version is the seven values of LOV-VERSION-STATUS, and the document states the writer of each: `IN_FORCE` and `SUPERSEDED` are produced by the calendar from the `valid_from` and `valid_to` of the rows and are written by no process; `LOADED`, `VALIDATED`, `APPROVED`, `ROLLED_BACK` and `REFUSED` are recorded on the decision-record entry of the version by the administration stories that prepare and approve it, because the three tables carry no state column (GAP-0872; ASM-1583). The lifecycle of a rule package version in TSD P4 v3 T4 — `LOADED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED` — is P7's capability and is not declared here; the names are shared because both use LOV-VERSION-STATUS, and the objects are not.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the state set and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Risk and model risk officer (RW-RISK) | Publishes a configuration version with Rules and parameters A in the target, and is the role the answer records as `publishedByRole` (TSD P4 v3 T6.1) |
| Center of excellence analyst (RW-COE) | Holds `CRUD` in Rules and parameters and cannot publish; the maker half of the separation, and the role the document never grants A |
| Tech lead of rwb-case (P3) | Reviews the parameters read as `rwb-access` uses it; owns the bounds and the page limits |
| Tech lead of rwb-partner (S9) | Confirms that no partner panel, partner firm, partner user or fee-schedule operation appears in this document |
| Internal audit | Reviews the list fields, the absence of a person in the answer and the event, and the stable order of the read |
| Data steward | Confirms that no name, e-mail address, personal field or user reference is declared in a schema, an example or a fake |

The maker-checker separation is a pair of letters and not a state: RW-COE prepares with C and U, RW-RISK publishes with A, and no single role holds both in Rules and parameters. The document therefore declares no four-eyes message of its own and no state that only a second person can move; a caller without A is refused with the ordinary 403 and MSG-P4-002.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `ConfigVersionPublication` request | `versionId` in the path; `effectiveFrom` (a date, DF-REF-025 and DF-REF-203 shape), `reason` and `note` (optional) in the body; `effectiveFrom` and `reason` required | DF-REF-025, DF-REF-203 |
| `ConfigVersion` answer | `versionId`, `matrixVersion` (DF-REF-044 shape), `maskingVersion` (DF-REF-202 shape), `limitVersion` (DF-REF-055 shape), `state` (one of LOV-VERSION-STATUS), `validFrom` (DF-REF-025, DF-REF-203), `validTo` (DF-REF-026, DF-REF-204), `supersedesVersionId`, `publishedAt`, `publishedByRole` (a role code, DF-REF-035) | DF-REF-044, DF-REF-202, DF-REF-055, DF-REF-025, DF-REF-203, DF-REF-026, DF-REF-204, DF-REF-035 |
| `ConfigVersionPage` | `items[]` of `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state`, `validFrom`, `validTo`, `publishedAt`, `publishedByRole`, plus `page`, `size`, `total` | DF-REF-044, DF-REF-202, DF-REF-055, DF-REF-025, DF-REF-203, DF-REF-026, DF-REF-204, DF-REF-035 |
| Query parameters of the list | `status` (one of the seven states), `page` and `size`, with the default and the maximum held as parameter rows read through DP-06 | Not specified in the source documents (DOR-RWB-P4-E8012-CON-7) |
| Configuration version, as the rows hold it | `permission` DF-REF-040 to DF-REF-044 with `matrix_version` DF-REF-044; `masking_rule` DF-REF-198 to DF-REF-204 with `masking_version` DF-REF-202, `valid_from` DF-REF-203 and `valid_to` DF-REF-204; `delegation_limit` DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 with `limit_version` DF-REF-055, `valid_from` DF-REF-025 and `valid_to` DF-REF-026 | DF-REF-016 to DF-REF-026, DF-REF-040 to DF-REF-044, DF-REF-055 to DF-REF-062, DF-REF-198 to DF-REF-204 |
| Roles and letters | The publishing role code and the capability areas of `role` DF-REF-034 to DF-REF-039 and `permission` DF-REF-040 to DF-REF-044, read behind the authorise answer | DF-REF-034 to DF-REF-039, DF-REF-040 to DF-REF-044 |
| Record event | `rwb.decision.DecisionRecorded.v1` with the entry of a publication: the three labels, the effective date, the reason, the note, the publishing role code, the version superseded and the time | Not specified in the source documents (DOR-RWB-P4-E8012-CON-7) |
| Refusal | `messageId` MSG-P4-001 on a 401, MSG-P4-002 on a 403, MSG-GEN-004 on a 409, MSG-GEN-001 on a 422 and MSG-P7-003 on a 503, with MSG-P4-004 as the break-glass warning of the answer | Not specified in the source documents (DOR-RWB-P4-E8012-CON-7) |

The configuration-version object, the scheme that builds `versionId` from the three labels, the date columns of the matrix label, the effective-date bounds and the record code of a publication are Not specified in the source documents (GAP-0872; ASM-1583): no source defines a configuration-version object, TSD P4 v3 appendix T-A declares no configuration-version operation, and `permission` carries `matrix_version` and no date column. The document fixes them and states each one as fixed here rather than derived. `supersedesVersionId` names the version the publication closes on the day before; RWB-P4-E8012-APP describes the same field as the version superseded, and the name this document declares is the one the contract test enforces.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/config-versions/{versionId}/publish` | `versionId` in the path; `Idempotency-Key` header; `effectiveFrom`, `reason`, `note` (optional) in the body; `ConfigVersion` out with `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state` `IN_FORCE` from `effectiveFrom`, `validFrom`, `validTo`, `supersedesVersionId`, `publishedAt`, `publishedByRole` | Rules and parameters A, scope applied; `Idempotency-Key` required |
| GET | `/admin/config-versions` | `ConfigVersionPage` out: `items[]` of `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state`, `validFrom`, `validTo`, `publishedAt`, `publishedByRole`, plus `page`, `size`, `total`; query `status`, `page`, `size` | Rules and parameters R, scope applied |

Errors for both: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 409 the version is not `APPROVED` or its window is already open (MSG-GEN-004), 422 a required field empty, a `versionId` that names no complete triple, or an `effectiveFrom` outside the bounds in force (MSG-GEN-001), 503 the dates, the entry, the outbox row or the idempotency row cannot be written (MSG-P7-003). The answer of the publication carries MSG-P4-004 as a warning when a break-glass grant is active. The publication is a write, so every request carries an `Idempotency-Key` and a replay answers the first answer (BR9); the list is a read and carries none. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR13).

The two paths are fixed here (GAP-0872; ASM-1583) and confirmed by the contract review before they are frozen. No configuration-version operation appears in TSD P4 v3 appendix T-A, and no operation of another service is declared as provided in this document.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access (own service) | The A check behind the publication and the R check behind the list, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The earliest and the latest effective date and the page default and maximum, with the version in force (DP-06) |

None of the two is declared as provided by rwb-access. The own authorise operation is the first path of `rwb-access` in Architecture v5 slide 14 and slide 41, and this document declares it as consumed and never defines it. The parameters read is P3's under the default ruling of Template and Rules §R3 and is consumed with its owner. No other operation of `rwb-case`, `rwb-decision`, `rwb-partner` or `rwb-document` is called, and the partner panel, partner firm, partner user and fee-schedule operations of `rwb-partner` appear nowhere in this document as provided or consumed (BR12).

#### 12.3 Events published

| Event | Topic | Owner | Key | Contract element |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | `versionId` | `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `effectiveFrom`, `supersedesVersionId`, `publishedByRole`, `reason` |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | The entry of a publication with the three labels, the effective date, the reason, the note, the publishing role code and the time, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

`AccessPolicyChanged` is one of the two events of `rwb-access` in Architecture v5 slide 14 and slide 41, and slide 43 gives it every service as a consumer with the note "cache refresh"; the document states that consumer list and the key, so that the cache refresh after the commit is part of the contract and not of an implementation. Its payload carries labels, a date, a role code and a reason, and no name, no e-mail address, no user reference and no personal field (BR5, BR10). `rwb.access.DoaLimitChanged.v1` belongs to RWB-P4-E8008-APP and is not declared here, even though a limit label travels in the payload.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, and a publication of its own tables needs no subscription. The document declares no inbox, no consumer group and no `processed_event` row, and no access-policy or limit event of another producer is consumed.

#### 12.5 Workflows and activities

None. The publication is synchronous and the maker-checker separation is a pair of letters, not a state: the document declares no workflow, no activity and no signal on the `rwb-access` queue. `ApprovalWorkflow` of the workflow kit belongs to `rwb-decision` (P7) and is not used for an administration change of this service.

#### 12.6 Schedules

None, and the absence is declared. The effective date of a version is resolved at read time by `POST /authorise` as the version whose `valid_from` ≤ today < `valid_to`, so the document declares no promotion job, no Temporal Schedule and no clock of its own (ASM-1584). The six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP; the rule-promotion Schedule of `rwb-decision` is P7's and promotes rule packages, not an access panel.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `permission` | P4 (rwb_access) | The rows of a version, the `matrix_version` label and the A and R letters of the caller |
| `masking_rule` | P4 (rwb_access) | The rows of a version, the `masking_version` label and the `valid_from` and `valid_to` that date it |
| `delegation_limit` | P4 (rwb_access) | The rows of a version, the `limit_version` label and the `valid_from` and `valid_to` that date it |
| `role` | P4 (rwb_access) | The role code the answer records as `publishedByRole` |
| the local decision-record table of the DP-03 library | P4, in rwb_access | The entry of a publication, and the recorded state of a version that the list answers |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in rwb_access | The two outbox rows of a publication and its idempotency row; no inbox row, because no event is consumed (DP-09; ASM-0074) |

No table of another service is named in the contract (DP-01): `partner`, `partner_user` and `partner_instruction` are S9 `rwb_partner`'s and their operations are absent; `decision_log_entry`, `rule_package_version` and `rule_row` are P7 `rwb_decision`'s; `case`, `task`, `lov_value` and the parameter tables are P3 `rwb_case`'s and arrive behind the consumed parameters read. No configuration-version table, view or copy is created, named or implied by the document (BR7), and no foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` with a granted answer for RW-RISK with A, for RW-COE with C, U and R and for RW-AUDIT with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-CASEOWN with R only | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the earliest and the latest effective date and the page bounds at the version in force, including a window that makes 2026-11-01 out of bounds and 2027-01-01 inside them | App story, contract tests |
| decision-record fake | The append of a publication, the hash-link check, the recorded state of "CFG-2026.11", "CFG-2027.01" and "CFG-2027.02", the seeded entries of the two earlier versions and a forced failure | App story, contract tests |
| access-panel fixture | The three tables with the rows of "CFG-2026.11" in force from 30 November 2026 and the rows of "CFG-2027.01" without a window, so a publication has a version to put in force and a version to supersede; no partner row and no person | App story, contract tests, harness |
| gateway-bff fake | The composite route of SCR-43 with the version list panel, the publication form and the states of section 15 | Screen route, harness |

Every fake answers only paths, statuses and payloads this document declares, and a fake that drifts fails the build (AC6). The fixture is synthetic: it carries version labels, date windows and states, and no production panel row is copied into a schema, a fake or a test.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The publication and the list provided; the authorise operation and the parameters read consumed; one hop, 2 s timeout each |
| Kafka | 2 event types published, 0 consumed | `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` and `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | None in this contract; the access review Schedule of RWB-P4-AD008-APP is not declared here |
| File | None | No file input and no file output; the load of a version's rows is the administration stories' |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-config-version-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml`, the `ConfigVersionPublication` request, the `ConfigVersion` answer and the `ConfigVersionPage` schema with their examples, the state-set rule, the `versionId` scheme and the versioning rules in the contract README, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. The parameters read is consumed and faked, and the bounds and the page limits stay parameter rows behind the document (GAP-0872; ASM-1583).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses, the `Idempotency-Key` header and the shared components; schema lint in the pipeline.
2. The two operations with the shapes of section 11: the request and the answer of the publication, the list, its `status` filter and its paging, and the required fields.
3. The state set of BR6, stated in the document and in the contract README, with the writer of each value named: the two derived states from the rows' dates, and the five recorded states from the decision-record entry.
4. The consumed operations with their owners, the one-hop rule and the 2 s client budget, and the explicit statement that no partner panel, partner firm, partner user or fee-schedule operation is provided or consumed here.
5. The error envelope and the message-ID mapping for 401, 403, 409, 422 and 503, and MSG-P4-004 as the break-glass warning of the answer.
6. The five fakes and the stub fixtures of section 12.8, including the two versions "CFG-2026.11" and "CFG-2027.01" and the state "CFG-2027.02".
7. The ten test cases of section 16; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note from the app story, the SCR-43 route, the `rwb-case` tech lead and the harness.

**Feature switch.** Both operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of this contract; the document declares no 404 branch of its own and adds no parameter.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-E8012-APP | The two provided operations, the two schemas, the state set, the event payload and the five fakes |
| RWB-PLT-N001-CON (gateway-bff and SCR-43) | The list and the publication as the version panel and the publication form call them |
| The `rwb-case` tech lead | The parameters read as consumed, with the bound names and the page limits, and that no table of the P3 rwb-case service is claimed here |
| The harness of the wave 4 access journey | The publishing role code, the effective date and the window, as the evidence it records |

The `versionId` scheme, the effective-date bounds and the record code of a publication are Not specified in the source documents (GAP-0872; ASM-1583): the scheme and the bounds are confirmed with the `rwb-case` owner and the record code with the decision-record library owner before the operations are frozen.

The SIT environment, base hosts, fixture layout, synthetic panel and partner keys, reference load key, stub answer shapes, effective date, shape of the panel reference row, evidence format and retention, and pass or fail gate of RWB-ITG-E8012-ITG are Not specified in the source documents (GAP-0478); none is hard-coded here.

**Done when.** The document validates in the pipeline, the test cases of section 16 pass, the five fakes answer every declared path, the `rwb-case` tech lead has accepted the parameters read, and the app story, the screen route and the harness have accepted the baseline.

Screen states for SCR-39, SCR-41 and SCR-43 are listed in section 15; each is marked Not specified where the sources give no value.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without Rules and parameters A publishes, or a role without R reads the list | You cannot {action} here. Your role does not include it. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |
| MSG-GEN-001 | A required field is empty, `effectiveFrom` is not a date, `versionId` names no complete triple, or `effectiveFrom` is outside the bounds in force | Enter {field}. |
| MSG-GEN-004 | The version is not in state `APPROVED`, or it is already in force and its window cannot be moved again | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The dates, the entry, the outbox row or the idempotency row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story where the message already existed, and MSG-GEN-004 is the platform text of the record that someone else changed, carried unchanged as a platform value and not as a new business text. No named-person four-eyes message is declared, because the separation of the preparer and the publisher is held by the C and A letters of TSD P4 v3 T6.1 and not by a comparison of two people on one act. MSG-P3-022, the missing checklist item of a rule package version, is declared on no response of this document, and MSG-P4-003, the legacy scope message, is declared on no response either, because a configuration version is not a case and this gate scopes no case.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | Versions, list | `ConfigVersionPage` with the three labels, the state and the window of each version, paged and filtered by `status` |
| SCR-43 Roles and access | Versions, in force | The item whose window contains today in state `IN_FORCE`, and the versions before it in `SUPERSEDED` with their `validTo` |
| SCR-43 Roles and access | Publication, form | `ConfigVersionPublication` with `effectiveFrom`, `reason` and `note`, and the bounds from the parameters read shown beside the field |
| SCR-43 Roles and access | Publication, recorded | The answer in state `IN_FORCE` with the three labels, `validFrom`, `publishedAt`, `publishedByRole` and `supersedesVersionId` |
| SCR-43 Roles and access | Publication, not approved | The 409 of the envelope with MSG-GEN-004 and a reload action |
| SCR-43 Roles and access | Publication, date outside the bounds | The 422 of the envelope with MSG-GEN-001 naming `effectiveFrom` |
| SCR-43 Roles and access | Publication, refused | The 403 of the envelope with MSG-P4-002 for a role without the A letter |
| SCR-43 Roles and access | Publication, not recorded | The 503 of the envelope with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-43 Roles and access | List, empty | An empty `items` with total 0 and no error |
| SCR-39 Rules and parameters (carried to SCR-43) | Empty, loading, error, no access | Not specified in the source documents (CG-ALL-5554) |
| SCR-41 Delegation of authority (carried to SCR-43) | Empty as stated in Screen Specifications v1, section SCR-41; loading, error, no access | Not specified in the source documents (CG-ALL-5555) |
| SCR-43 Roles and access | Loading, error, no access (empty as in the list row above) | Not specified in the source documents (CG-ALL-5556) |

The screens are served by the gateway-bff composite route (DP-19), which calls the two operations of this contract, one hop each, and shows the delegation-of-authority panel and the masking panel through the operations of the stories that own them. The composite route specification, the panel field lists and the screen states belong to RWB-PLT-N001-CON and to the screen work of the administration stories; this document fixes the version list and the publication form only, and the legacy screen names SCR-39 Rules and parameters and SCR-41 Delegation of authority are carried to SCR-43 Roles and access.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-012-CON-01 | AC1 | Contract | The document validates; the base, the two operations, the rights A and R, the five error responses and the `Idempotency-Key` on the write are present; no operation of another service is provided |
| TC-E8-012-CON-02 | AC2 | Contract | The request fields `effectiveFrom`, `reason` and `note` with their required flags; the answer fields `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state`, `validFrom`, `validTo`, `supersedesVersionId`, `publishedAt` and `publishedByRole`; the page `items[]`, `page`, `size` and `total`; `publishedByRole` as a role code; no name, e-mail address or user reference; the bounds read from the parameters contract |
| TC-E8-012-CON-03 | AC3 | Contract | The seven states of LOV-VERSION-STATUS, the two derived from the rows' dates, the five read from the record, the single publishable state `APPROVED`, no Schedule and no workflow, and no configuration-version or partner table named as this service's |
| TC-E8-012-CON-04 | AC4 | Contract | A 401, 403, 409, 422 and 503 response carry one problem envelope with a valid message ID, 403 carries MSG-P4-002, the answer carries MSG-P4-004 on a break-glass grant, and no second error shape exists |
| TC-E8-012-CON-05 | AC5 | Contract | Two consumed operations with their owners P4 and P3, one hop and the 2 s budget; the partner panel, partner firm, partner user and fee-schedule operations declared as neither provided nor consumed |
| TC-E8-012-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build; the fixture carries labels, dates and states only, and no schema or fake carries a name, a personal field or a partner row |
| TC-E8-012-CON-07 | AC3, AC5 | Contract | Boundary of the tables of section 12.7: the three version tables, the role table and the local decision-record table are the only tables named as this service's; no table of another service is named |
| TC-E8-012-CON-08 | AC7 | Contract | A replay with the same Idempotency-Key answers the first answer with no second event; one AccessPolicyChanged.v1 on rwb.access.events.v1 and one entry on rwb.decision-record.v1; neither payload carries a person |
| TC-E8-012-CON-09 | AC8 | Contract | The rules BR1 to BR13 of section 8, each traced to a criterion of section 7 and to a test case of this section; the boundary of TC-E8-012-CON-07 carries the architecture rules |
| TC-E8-012-CON-10 | AC9 | Contract | A 404 answer of each provided operation carries one problem envelope with type, title, status, detail, instance, messageId and traceId; its message ID is Not specified in the source documents (NEWAC-RWB-P4-E8012-CON-AC8) |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. No `-ITG` copy of a test case is written here: the journey of this key is RWB-ITG-E8012-ITG, which owns legacy AC1 and its own copies.

### 17. Guardrails

- No business value in the contract: the effective-date bounds and the page bounds stay parameter rows behind the document, and the role codes stay rows of `role` and `permission` (BR8).
- No personal data in a schema, an example or a fake: version labels, dates, role codes, reasons and times only, and no user reference in any answer, entry or event (BR5, BR10).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; `partner`, `partner_user` and `partner_instruction` are S9's and are absent, never named as this service's (BR4, BR12).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- No table is created for a configuration version: the document declares the triple of labels over the three existing tables and no configuration-version object (BR7).
- No clock of its own: the document declares no Schedule, no workflow and no promotion job, and the effective date is resolved at read time (BR11, ASM-1584).
- A write without its `Idempotency-Key` is refused by the contract, and a replay never publishes a second event (BR9).
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.
- Every example in the document is synthetic; no production panel row is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-011 | A reference data service holds every versioned table with its valid from and valid to dates, author and approver | The three version labels, `validFrom` and `validTo` in the answer and the list, and the entry that records the publication and the version superseded | TC-E8-012-CON-02, TC-E8-012-CON-03, TC-E8-012-CON-07 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do | The `matrixVersion` label as part of the version identity, and the A and R letters behind the two operations | TC-E8-012-CON-01, TC-E8-012-CON-02 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | The two operations as the SCR-43 route consumes them, with the refusal shapes and the break-glass warning | TC-E8-012-CON-04, TC-E8-012-CON-05 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key. The versioned reference-data requirement is the P7 one in the Program BRD and is served here by the panel version rather than by the rule registry, which is P7's.

| Legacy reference | Where it is kept |
|---|---|
| AC1 publish a panel change, the change put in force with an effective date and the result written to the decision log with the rule version | Owned by RWB-ITG-E8012-ITG and kept there; named in sections 7 and 16, and carried in this contract as sections 4, 8 and 12.1 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Owned by RWB-P4-E8012-APP; the 503 of the envelope is declared here in section 12.1 and section 14 |
| The permission check: Rules and parameters C for the preparer and A for the publisher | Sections 3, 7 (AC1, AC5), 8 (BR5), 10, 12.1 |
| MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001, MSG-GEN-004, MSG-P7-003 | Section 14, and the error list of section 12.1 |
| The legacy data rows `partner` DF-PRT-001 to DF-PRT-007 and `partner_user` DF-REF-212 to DF-REF-217 | Moved with the partner capability to S9 `rwb-partner`; sections 1, 8 (BR12) and 12.7 record that no row and no operation is read or written here |
| The legacy data rows `decision_log_entry` DF-DEC-001 to DF-DEC-018 and `rule_row` DF-REF-001 to DF-REF-015 | The local record of DP-03 in sections 11 and 12.3, and the rule registry of P7; the "rule version" of AC1 is read here as the version of the panel |
| The legacy data rows `role` DF-REF-034 to DF-REF-038, `permission` DF-REF-040 to DF-REF-044, `masking_rule` DF-REF-198 to DF-REF-204 and `delegation_limit` DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | Sections 11, 12.7 |
| The state set of LOV-VERSION-STATUS and the lifecycle of TSD P4 v3 T4 | Sections 1, 8 (BR6), 9, 12.1 |
| The legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority as the story named them | Section 15, carried to SCR-43 Roles and access with its delegation and masking panels |
| Legacy key RWB-E8-012, contract RWB-P4-E8012-CON, app story RWB-P4-E8012-APP | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the publication and the list (RWB-P4-E8012-APP).
- The partner panel, the partner firm, the partner users, the fee schedule and the partner service levels: S9 `rwb-partner` under the ownership map, and FEAT-PRM-02 is that service's feature and not a prerequisite of this contract.
- The preparation, load and approval of a configuration version: RWB-P4-E1037-APP for the matrix, RWB-P4-AD004-APP for masking and RWB-P4-E1038-APP for the limits; this document fixes the state a publication reads and not how it is reached.
- The authorise operation itself and the version-in-force resolution it performs: RWB-P4-E1037-APP and its own contract.
- The rollback of a version in force and the change report of a version (RWB-P4-AD013-APP).
- The rule package registry, its promotion at 00:01 and the central decision ledger with its query API and chain verification (P7 `rwb-decision`).
- Reference-data loads and the list of values (P3 `rwb-case`), and the parameters rows themselves, which this contract consumes and does not define.
- The screen SCR-43 Roles and access, its panels and its composite route specification (RWB-PLT-N001-CON and the screen work of the administration stories).
- The deployment, the Helm chart, the topic subscription, the dashboards and the runbook (an OPS story of this legacy key).
- The cross-service journey harness and its evidence, and the `-ITG` copies of the test cases (RWB-ITG-E8012-ITG).
