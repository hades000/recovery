# RWB-P4-AD003-CON Scope per role

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-003 for rwb-access — the contract of the scope value per role as data, its read and its change, the scope predicate every service applies, the refusal with MSG-P4-003 and the access-policy event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD003-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD003-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP08, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **tech lead**, I want **the published contract baseline of the role scope: an OpenAPI 3.1 document for the scope read and the scope change, the `RoleScope`, `RoleScopeChange` and `RoleScopePage` schemas with the `LOV-SCOPE` values, the scope predicate shape that every service applies with `scope`, `teamCode`, `regionCode` and `caseOwnerRef`, the statement that a scope change is a data change and never a code change, the refusal with MSG-P4-003 and its decision-record entry, the `rwb.access.AccessPolicyChanged.v1` declaration with change kind `SCOPE`, one RFC 9457 error envelope with its message IDs, the contract tables of section 12 and the contract fakes**, so that **the app story builds on Day 1 against a fixed, testable contract, and every service that authorises a record learns exactly which bound it applies, which answer a record outside it receives and what is recorded when one is refused**.

The deliverable is the scope **as data and as predicate**: the read and the change of a role's scope, the shape of the bound every query applies, and the refusal that bound produces. What a role may do is not contracted here — the permission matrix and the masking are RWB-P4-E1037-CON's — the role catalogue is RWB-P4-E1019-APP's, the sign-in is RWB-P4-E1022-CON's, and the guard, the scope descriptor type and their fakes are RWB-PLT-E1037-CON's. This document declares the data side of the bound and the rule of the answer, and refers to those three contracts without restating them.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020), and one guard library every service binds is the second (DP-08). The legacy story held the scope rule inside one package over one database: the same connection that read `role` and `permission` also filtered the case query and answered the refusal, so there was one shape because there was one process. In the target the scope stays with one owner (DP-01) and the enforcement moves into a platform library that every service binds, so a consumer now depends on two published artefacts and must find in each exactly what it needs: the library gives it the guard, the descriptor type and the annotation; the access owner gives it the scope value, the three codes of the record and the rule of the refusal.

That is the gap this document closes. Without a published data-side contract a consumer guesses what a scope value is called, whether the bound carries a team code, a region code or a queue, what an out-of-scope record receives — a 403, an empty page or a 404 — and whether the refusal is counted, recorded and shown. Those guesses drift at the first scope change, and a wrong guess is a data leak or a hidden case. With it, a consumer compiles and tests from Day 1 against fakes, and cannot quietly read a P4 table because the contract gives it no connection to do so.

Three consequences shape the document. The first is that the bound is four values and no fifth: `LOV-SCOPE` is `OWN`, `TEAM`, `REGION`, `ALL` (TSD P4 v3 T3.2), and the predicate that carries them is the same shape for all four, so a service writes one comparison and not four. The second is that the refusal is indistinguishable from an absence: a record outside the scope is answered 404 with MSG-P4-003, never 403 and never a count, because a 403 confirms that the record exists and a count tells the caller how much was hidden (FSD P4 v3 VR-P4-014-1 and AC-EXC-P4-014-01; REQ-ACA-009). The third is that a scope change is a data change with one event: `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, the one access-policy name the architecture gives this service (Architecture v5 slides 14, 20 and 43), with change kind `SCOPE`; a second name would add a contract without a consumer, because every service that caches permission data already refreshes on that one.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the base path, the topic and the event names follow the platform rule rather than a local choice.
- Architecture v5 slide 14 gives `rwb-access` the operations `POST /authorise` (role, scope, DoA), `GET /me/permissions`, `GET /doa-limits` and `/masking-policies`, and the two events `AccessPolicyChanged` and `DoaLimitChanged` on `rwb.access.events.v1`; slide 41 keeps Recovery roles as data, scope, masking policy, the DoA table and the access log in `rwb_access`; slide 10 fixes that each service authorises the object itself with cached permission data from `rwb-access`.
- TSD P4 v3 T3.1 fixes the column this document contracts: `role.default_scope` (DF-REF-038, `LOV`, varchar(8), required), and T3.2 fixes its list `LOV-SCOPE` = `OWN`, `TEAM`, `REGION`, `ALL`.
- TSD P4 v3 T6.2 fixes the rule behind the predicate: "scope filters every query". T6.1 fixes the rights matrix the two operations read: RW-SECADM CRUDA, RW-PLATADM CRUD, RW-AUDIT R, RW-COE R, RW-DATASTEW R and RW-COMPLY R in Platform administration.
- RWB-P4-E1037-CON is the access contract that publishes the authorise answer of which the scope predicate is an element; this document declares the shape of that element and does not restate the operation (ASM-1462).
- RWB-PLT-E1037-CON is the guard library: the `AccessGuard`, `ScopeGuard` and `MaskApplier` interfaces, the `@PersonalData` annotation, the scope descriptor type and the fakes every service binds. This document names the descriptor as the library's and fixes only the data that fills it.
- The two scope operations have no row in the ownership map and none in TSD P4 v3 appendix T-A, where the only role read is API-P4-007 `GET /admin/roles` — **Not specified in the source documents (GAP-0792; ASM-1461)**.
- The scope predicate has no operation of its own in any source: slide 14 names the inputs of the authorise operation as "role, scope, DoA" and TSD P4 v3 T-A gives no path for a scope answer — **Not specified in the source documents (GAP-0792; ASM-1462)**.
- The case owner, team and region columns the predicate is compared with are P3's: DF-CAS-009 `owner_user_id`, DF-CAS-011 `team_code` (`LOV-TEAM`) and DF-CAS-012 `region_code` (`LOV-REGION`) of `rwb_case` (TSD P3 v3 T3.1). This document names them and owns none of them.
- The failure-message convention is the platform one: RFC 9457 problem details (Architecture v5 slide 11, "RFC 9457 problem details"), and the legacy texts are copied unchanged where the message already exists.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), and it holds in Contract group CG-W4 because the business epic EP08 is wave 4 in the W-MAP (§R5.6).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the two scope operations under the base `/api/recovery/access/v1`, with the shared components the `rwb-access` operations use.
2. Draft the three schemas: `RoleScope` for one role and its scope value, `RoleScopeChange` for the posted value, and `RoleScopePage` for the paged read, with the `LOV-SCOPE` values declared once as an enumeration and used by both the schema and the validation.
3. State the invariant: one scope value per role, required, drawn from `LOV-SCOPE`; a role with no scope cannot exist because the column is required (DF-REF-038).
4. State the change rule: the change writes `default_scope` of one role row under `If-Match` and an `Idempotency-Key`; there is no version row and no effective date, so the history of a scope is the decision record and not a table (ASM-1460).
5. Declare the scope predicate: `scope`, `teamCode`, `regionCode` and `caseOwnerRef`, its meaning for each of the four values, and the statement that the guard of RWB-PLT-E1037-CON applies it in the owning service's own query and that the library returns no record.
6. State the refusal: a record outside the predicate is 404 with MSG-P4-003, with no field of the record and no count of the excluded records, and one decision-record entry with decision code `AC-DENY` and reason code `OUT_OF_SCOPE`; where the entry cannot be written the answer is 503 with MSG-P7-003 and no record.
7. State the rights: Platform administration R for the read and C for the change, with an active role required on every call, and the 401 and 403 of the default deny rule.
8. Agree the error envelope and the message mapping for 401, 403, 404, 409, 422 and 503, with the business texts copied unchanged from the legacy story where the message already exists.
9. Declare the event `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with change kind `SCOPE` and its payload, and the decision-record type on the shared topic `rwb.decision-record.v1`; declare no third event name and leave `rwb.access.DoaLimitChanged.v1` to the delegation contract.
10. Publish the contract tables of section 12 (nine sub-tables) and the contract fakes, then add the contract tests: schema validation, the four values, the predicate shape, the refusal, the rights, the envelope, the owner declarations and the drift between a fake and the document.
11. Tag the baseline and hand it to RWB-P4-AD003-APP, to RWB-PLT-E1037-CON and to every service that applies the predicate.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A schema declares a scope value outside `LOV-SCOPE`, or declares the four values twice with two spellings | The review fails and the enumeration is corrected | None | AC2 |
| X3 | A schema declares a person's name, an e-mail address or a case number | The review fails and the property is removed; the rule is a lint item of the document | None | AC2 |
| X4 | The predicate declares a field the sources do not support, or a field of another service's table | The review fails: the four names of the predicate are the contract and no fifth is added | None | AC3 |
| X5 | The document declares the refusal as 403, as an empty page, or with a count of the excluded records | The review fails: the refusal is 404 with MSG-P4-003 and no count | None | AC4 |
| X6 | The document declares an event name other than the two of the service, or a second access event name for a scope change | The review fails and the event is declared under `rwb.access.AccessPolicyChanged.v1` with change kind `SCOPE` | None | AC5 |
| X7 | The document declares an operation or a table of another service as provided | The review fails; the role catalogue, the authorise answer, the case columns and the library descriptor are documented as referred to and not as provided | None | AC1, AC6 |
| X8 | An error response carries no `messageId`, or a `messageId` not in the agreed set | The contract test fails and the merge is blocked | None | AC6 |
| X9 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC7 |
| X10 | A consumer applies the predicate and the access owner does not answer inside the 2 s budget | The consumer answers 503 with MSG-GEN-006 for that read and never answers a record it could not bound; the document declares the 503 | MSG-GEN-006 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it reads the ownership map, the platform envelopes, the TSD P4 v3 columns and lists, and refers to RWB-P4-E1037-CON and RWB-PLT-E1037-CON without restating them |
| Negotiable | The field-level detail of the three schemas and the payload of the event are settled with the app story and with the guard library; the four values, the predicate names, the refusal and the envelope are fixed by the target architecture and the Workbench |
| Valuable | Unblocks the app story and every service that authorises a record on Day 1 with a written answer to "which bound applies, and what does a record outside it receive", and keeps the catalogue, the matrix, the masking and the session out of the scope contract |
| Estimable | One document, three schemas, one error envelope with six message ids, one event declaration, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: The role scope contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given a scope is the "default_scope" of a role row of "rwb_access" and its values are "OWN", "TEAM", "REGION" and "ALL"
    Given the guard of RWB-PLT-E1037-CON applies the scope predicate in the owning service and returns no record

  Scenario: AC1 The OpenAPI 3.1 document describes the two scope operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares GET /admin/role-scopes and PATCH /admin/role-scopes/{roleCode} with the owner rwb-access
    Then the read declares Platform administration with the right R, and the change declares Platform administration with the right C
    Then every operation declares 401, 403, 404, 409, 422 and 503
    Then the change declares the Idempotency-Key header and the If-Match header, and the read declares neither
    Then the role catalogue GET /admin/roles, the session GET /me/session and the authorise operation POST /authorise are documented as referred to and not as provided, with their owners

  Scenario: AC2 The three schemas carry the role, the scope value and its list (new, D-RCV-60)
    Given the schemas RoleScope, RoleScopeChange and RoleScopePage of the document
    Then RoleScope carries roleCode, roleName, roleClass, scope, scopeValues, rowVersion and updatedAt
    Then RoleScopeChange carries scope and the If-Match version
    Then RoleScopePage carries items, page, size and total with a default of 50 and a maximum of 200
    Then scope is declared as an enumeration of OWN, TEAM, REGION and ALL, and no fifth value appears anywhere in the document
    Then the document states that a scope is the "default_scope" of a role row in "rwb_access" (DF-REF-038) and that it is required
    Then no schema, no parameter and no example declares a person's name, an e-mail address, an identity number or a case number

  Scenario: AC3 The scope predicate is declared once and applied by the guard (new, D-RCV-60)
    Given the scope predicate described in the document
    Then it carries scope, teamCode, regionCode and caseOwnerRef and no fifth field
    Then scope is the value of "LOV-SCOPE" of the role, teamCode and regionCode are the case team and region codes DF-CAS-011 and DF-CAS-012 of rwb-case, and caseOwnerRef is compared with the case owner DF-CAS-009
    Then the document states that OWN matches the case owner, TEAM the case team, REGION the case region and ALL every case, and that a scope with no team or region code matches no record of that dimension and never widens to ALL
    Then the document states that the guard of RWB-PLT-E1037-CON applies the predicate in the owning service's own query and that the library runs no query and returns no record
    Then the descriptor type of the predicate is declared as RWB-PLT-E1037-CON's and is not redefined here

  Scenario: AC4 The refusal is one message, one status and one entry (new, D-RCV-60)
    Given the refusal section of the document
    Then a record outside the predicate is declared as 404 with MSG-P4-003 "This case is not in your scope."
    Then the document states that no field of the record and no count of the excluded records is returned in the status, the body, a header or a metric
    Then the document states that one decision-record entry with decision code AC-DENY and reason code OUT_OF_SCOPE is written through the library of DP-03 and published on rwb.decision-record.v1
    Then the document states that where the entry cannot be written the answer is 503 with MSG-P7-003 and the record is not returned
    Then the two legacy criteria are named as RWB-P4-AD003-APP's and no legacy value of them is restated as a criterion of this document

  Scenario: AC5 A scope change is a data change published as the access-policy event (new, D-RCV-60)
    Given the change operation and the events section of the document
    Then the change updates default_scope of one role row and answers the role with its new scope and the decision-record entry reference
    Then the document states that a scope change needs no deployment, no restart and no code change, and that the history of a scope is the decision record and not a table
    Then rwb.access.AccessPolicyChanged.v1 is declared on the topic rwb.access.events.v1 with change kind SCOPE, the role code, the new scope value and the time
    Then rwb.decision-record.DecisionRecorded.v1 is declared on the shared topic rwb.decision-record.v1 for the entry of the change and of the refusal
    Then no other event name is declared for this capability, and rwb.access.DoaLimitChanged.v1 is declared as the delegation contract's and not as this one's
    Then no payload carries a person, a case, a case count or a personal field

  Scenario: AC6 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by either of the two operations
    Then the body carries the code, the message, the messageId, the traceId and the field list, with the problem media type
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 404 and 409 carry MSG-GEN-004, 422 carries MSG-GEN-001 other than the out-of-scope refusal, and 503 carries MSG-P7-003
    Then the out-of-scope refusal is 404 with MSG-P4-003 and is declared once, with the reason code OUT_OF_SCOPE
    Then the message texts are the legacy texts where the message already exists and the legacy criterion AC2 of RWB-AD-003 is not reworded by this document

  Scenario: AC7 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the four contract fakes of section 12.8
    When a fake is compared with the document
    Then the role-scope fake answers the two paths of 12.1 with four roles of the four LOV-SCOPE values, one change of OWN to TEAM, 409 on a stale If-Match, 422 on a value outside the list and 403 with MSG-P4-002
    Then the scope predicate fake answers a predicate of each of the four values and no record
    Then the rwb-case case-list mock answers the 12 cases owned by the caller and the case RW-2026-000456 in team MTG-NE under another owner, with 404 and MSG-P4-003 for the out-of-scope case
    Then the decision-record fake answers the AC-CHG and AC-DENY appends and the 503 with MSG-P7-003
    Then a contract test fails on any drift between a fake and the document, and no fake carries a name, an e-mail address or a case number
```

These seven criteria test the artefact only. No criterion restates a legacy acceptance criterion: the two legacy criteria of RWB-AD-003 are owned by RWB-P4-AD003-APP and are listed with their tests in section 16 as the cases this contract is the ground of, exactly as the brief of this key fixes.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path, table or event | DP-13; Architecture v5 slides 14 and 41 |
| BR2 | A scope is the `default_scope` of a role row of `rwb_access` (DF-REF-038), one value per role, required, drawn from `LOV-SCOPE` = `OWN`, `TEAM`, `REGION`, `ALL` and from no other list | TSD P4 v3 T3.1 and T3.2; legacy RWB-AD-003 Data table |
| BR3 | The predicate carries four fields and no fifth: `scope`, `teamCode`, `regionCode`, `caseOwnerRef`; the case columns behind the last three are P3's and are named, not owned | TSD P3 v3 T3.1 (DF-CAS-009, DF-CAS-011, DF-CAS-012); FSD P4 v3 A2.14; ASM-1462 |
| BR4 | The guard of RWB-PLT-E1037-CON applies the predicate in the owning service's own query and returns no record; the descriptor type is the library's and is not redefined here | Architecture v5 slides 10 and 35; RWB-PLT-E1037-CON BR3; ASM-1462 |
| BR5 | A record outside the predicate is 404 with MSG-P4-003, with no field of the record and no count of the excluded records in any status, body, header or metric | FSD P4 v3 VR-P4-014-1 and AC-EXC-P4-014-01; legacy RWB-AD-003 AC2; REQ-ACA-009 |
| BR6 | A refusal writes one decision-record entry with decision code `AC-DENY` and reason code `OUT_OF_SCOPE`; where the entry cannot be written the answer is 503 with MSG-P7-003 and the record is not returned | DP-03; legacy RWB-AD-003 TC-AD-003-04; ASM-1463 |
| BR7 | A scope change writes `default_scope` of one role under `If-Match` and an `Idempotency-Key`; it writes no version row and no effective date, because no such column exists, and the history is the decision record | TSD P4 v3 T3.1; DP-15; ASM-1460 |
| BR8 | The scope read needs Platform administration R and the scope change needs C; an active Workbench role is required on every call, and the default deny rule answers 401 and 403 | TSD P4 v3 T6.1 and API-P4-007; legacy RWB-AD-003 Permission checks; FSD P4 v3 VR-P4-001-1 |
| BR9 | This capability publishes one event, `rwb.access.AccessPolicyChanged.v1`, with change kind `SCOPE`; `rwb.access.DoaLimitChanged.v1` belongs to the delegation table and no third name exists | Architecture v5 slides 14, 20 and 43; ASM-1464 |
| BR10 | The contract declares no table of another service: `recovery_case`, `assignment`, `queue` and `queue_member` are P3's, `lov_value` is P3's, `decision_log_entry` is P7's and `partner_user` is S9's | DP-01; ownership map |
| BR11 | The `LOV-SCOPE` values are carried as this service's own enumeration in the document and in its schema, not read from P3's `lov_value`, because this key applies no reference-data contract; a fifth value is a new major version and a migration | TSD P4 v3 T3.2; ownership map; ASM-1465 |
| BR12 | Error responses use one envelope and one message id per condition, the business texts are copied unchanged from the legacy story where the message exists, and a schema change is additive within major version 1 | Architecture v5 slides 11 and 42; Template and Rules §R7.2 s14 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | The two operations, the three schemas, the predicate, the refusal and the event are described | The document validates and the contract tests pass | In review |
| In review | Consumer sign-off | RWB-P4-AD003-APP, RWB-PLT-E1037-CON and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change, or a fifth `LOV-SCOPE` value | A field is removed, renamed or retyped, or the enumeration grows | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

A scope value has its own states — the four values of `LOV-SCOPE` — and they are the app story's data states, not states of this document. This document declares no version state for a scope, because `role` carries no version column (BR7).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document, the three schemas, the predicate declaration, the event declaration and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version, including a fifth scope value |
| Security administrator and the audit representative | Review and sign off the rights, the predicate and the refusal |
| Tech lead of the guard library RWB-PLT-E1037-CON | Reviews the predicate and the descriptor boundary, because every service applies the predicate through that library |
| Tech lead of the access contract RWB-P4-E1037-CON | Reviews the scope element of the authorise answer, because that answer carries the predicate |
| Tech lead of P3 rwb-case | Reviews the naming of the case owner, team and region columns the predicate is compared with, and the 404 the case read renders |
| Data steward | Confirms that no personal data property is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Scope of a role | `roleCode` (DF-REF-035), `roleName` (DF-REF-036), `roleClass` (DF-REF-037), `scope` (DF-REF-038, one of `OWN`, `TEAM`, `REGION`, `ALL`), `scopeValues`, `rowVersion`, `updatedAt` |
| Scope change | `scope`, the `If-Match` version and the `Idempotency-Key` header; the answer is the role with its new scope and the decision-record entry reference |
| Scope page | `items[]` of the scope of a role, `page`, `size` (default 50, maximum 200), `total` |
| Scope predicate | `scope`, `teamCode`, `regionCode`, `caseOwnerRef`; no record, no query and no count |
| Case columns named behind the predicate | DF-CAS-009 `owner_user_id`, DF-CAS-011 `team_code` (`LOV-TEAM`), DF-CAS-012 `region_code` (`LOV-REGION`), of P3 `rwb_case` (TSD P3 v3 T3.1); named only |
| Lists | `LOV-SCOPE` = `OWN`, `TEAM`, `REGION`, `ALL` (TSD P4 v3 T3.2); `LOV-ROLE-CLASS` = `BANK_USER`, `PARTNER_USER`, `NON_HUMAN_ACTOR` for the class the read answers |
| Refusal | 404, MSG-P4-003 "This case is not in your scope.", the reason code `OUT_OF_SCOPE`, and no case number, owner or count |
| Event payloads | The role code, the scope value and the time; no person, no case and no personal field |
| Decision-record entry | The change entry and the refusal entry, written through the library of DP-03; their fields are the library's and are not redefined here |

Three values the sources do not fix are this baseline's decision and are carried as placeholders. The two operation paths and their rights have no row in the ownership map and none in TSD P4 v3 appendix T-A — **Not specified in the source documents (GAP-0792; ASM-1461)**. The predicate has no operation and no field list of its own in any source — **Not specified in the source documents (GAP-0792; ASM-1462)**. A scope change has no version and no effective date on `role` — **Not specified in the source documents (GAP-0792; ASM-1460)**.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/role-scopes` | `RoleScopePage`: query `scope`, `roleClass`, `page`, `size` (default 50, max 200); every role in force with its scope value and the four values of `LOV-SCOPE` | Platform administration R |
| PATCH | `/admin/role-scopes/{roleCode}` | `RoleScopeChange` in, with the `Idempotency-Key` and `If-Match` headers; the written role out with its new scope and the decision-record entry reference | Platform administration C |

Errors for both: 401 no session or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 an unknown role code (MSG-GEN-004), 409 a stale `If-Match` or a repeated key answered differently (MSG-GEN-004), 422 a value outside `LOV-SCOPE` or a missing field (MSG-GEN-001), 503 the record entry not written (MSG-P7-003). The change is idempotent by `Idempotency-Key`; the same key returns the first answer and writes no second change. Major version 1 sits in the path (BR12).

The role catalogue `GET /admin/roles` (API-P4-007), the session `GET /me/session` (API-P4-012) and the authorise answer `POST /authorise` are the service's own operations of RWB-P4-E1019-APP, RWB-P4-E1037-APP and RWB-P4-E1037-CON; this document refers to them, declares the scope element each of them carries, and neither restates nor changes them (ASM-1462).

#### 12.2 REST operations consumed

None. This document declares no consumed operation and no consumed table, because the scope is answered from `rwb_access` and from the session, and the guard runs in the consumer's own process against its own tables.

| Called by | What it uses | Owner |
|---|---|---|
| Every service that authorises a record | The scope predicate in the access answer, and the guard of RWB-PLT-E1037-CON that applies it in its own query | P4 `rwb-access` for the data, RWB-PLT-E1037-CON for the library |
| P3 rwb-case | The case owner, team and region columns DF-CAS-009, DF-CAS-011 and DF-CAS-012 of its own `recovery_case`, compared with the predicate | P3, its own table and its own query (named only here) |

The case read of the app story's AC1 is P3's `GET /cases` (RWB-P3-E1018-CON) and is exercised through its contract mock at test level only; this document declares no dependency on it and the app story carries none (ASM-1466).

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | Change kind `SCOPE`, the role code, the new scope value and the time |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code (`AC-CHG` for a change, `AC-DENY` for a refusal with reason code `OUT_OF_SCOPE`), the role code, the scope value and the time |

Both messages use the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype. No message carries a person, a case, a case count, a name, an e-mail address or an identity number. `rwb.access.DoaLimitChanged.v1` is declared as the delegation contract's event and is not declared for a scope change, and no second name exists for one (BR9, ASM-1464).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this capability adds no subscription.

#### 12.5 Workflows and activities

None. The two operations are synchronous REST answers in the caller's thread with no workflow, no activity and no signal. The six-monthly access review Schedule (JOB-18) is RWB-P4-AD008-CON's; the scope is applied inside a request and never by a workflow.

#### 12.6 Schedules

None. Nothing about a scope runs on a clock: the scope is a value the read answers and the change writes.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (`rwb_access`) | `default_scope` (DF-REF-038) is the scope; the role code, name and class travel with it; the optimistic-lock version is the `If-Match` of the change |
| `permission` | P4 (`rwb_access`) | The Platform administration letters R and C of the caller (DF-REF-040 to DF-REF-044); read only |
| `recovery_case` | P3 (`rwb_case`) | Appears nowhere as a table; DF-CAS-009, DF-CAS-011 and DF-CAS-012 are named as the columns the predicate is compared with, in P3's own query |
| `assignment`, `queue`, `queue_member` | P3 (`rwb_case`) | Appear nowhere; the predicate does not use the assignment window and this capability reads no queue row |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | Appear nowhere; `LOV-SCOPE` is the document's own enumeration (BR11, DP-01) |
| `decision_log_entry` | P7 (`rwb_decision`) | Appears nowhere; the local entry is the library's and the central ledger is P7's |
| `partner_user` | S9 (`rwb_partner`) | Appears nowhere; the ownership map gives partner users to S9 |

No foreign key crosses a schema, and the contract names no table outside `rwb_access`.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb-access` role-scope WireMock | The two paths of 12.1: four roles of the four `LOV-SCOPE` values, one change of `OWN` to `TEAM` with its entry reference, the stored answer for a repeated `Idempotency-Key`, 409 for a stale `If-Match`, 422 with MSG-GEN-001, 404 with MSG-GEN-004, 403 with MSG-P4-002 and 503 with MSG-P7-003 | App story, contract tests, wave 4 harness |
| Scope predicate fake (with RWB-PLT-E1037-CON) | A predicate of each of the four values with `teamCode`, `regionCode` and `caseOwnerRef`, the `TEAM` predicate of a session with no team code, and no record | App story, contract tests, every consuming service |
| `rwb-case` case-list mock (RWB-P3-E1018-CON) | `GET /cases` with the 12 cases owned by the caller and the case `RW-2026-000456` in team `MTG-NE` under another owner; `GET /cases/{caseId}` answering 404 with MSG-P4-003 for the out-of-scope case | App story, contract tests |
| Decision-record fake (RWB-PLT-E1027-CON) | The `AC-CHG` and `AC-DENY` appends, the hash-chain check and the 503 with MSG-P7-003 | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | The scope read and the scope change provided; the predicate travels in the access answer of RWB-P4-E1037-CON and is applied by the consumer, one hop, 2 s timeout |
| Kafka | 2 published, 0 consumed | `rwb.access.AccessPolicyChanged.v1` and `rwb.decision-record.DecisionRecorded.v1` |
| Temporal | None | No workflow, activity or Schedule in this contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-role-scope-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, the three schemas, the `contract/error-envelope.yaml` with the agreed message ids, the predicate declaration with its four fields and its four meanings, the event declaration for `rwb.access.AccessPolicyChanged.v1` with change kind `SCOPE`, the stub that names the P3 case columns and the library descriptor as referred to, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

A contract story adds no build dependency of its own: each DP above is **referred to; the consuming story carries the dependency**, and that story is RWB-P4-AD003-APP, whose H row carries RWB-PLT-E1027-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON and RWB-PLT-N001-CON. DP-03 is contracted as the entry the document declares on `rwb.decision-record.v1`. DP-05 is contracted as the boundary the document keeps and not as a read: `role` is the ACE RBAC extension in `rwb_access`, the caller's identity arrives in the ACE sign-in claim, the case owner, team and region are P3's columns named only, and the document declares no `v_ace_*` read. DP-08 is the predicate and the guard that applies it, with the descriptor type named as the library's. DP-13 is the base of the document. DP-19 is the composite route that serves SCR-43.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline (AC1).
2. The two operations and the three schemas of section 11, with the enumeration of `LOV-SCOPE` declared once (AC1, AC2).
3. The invariant and the change rule in the description of the two operations: one value per role, required, `If-Match`, `Idempotency-Key`, no version row and no effective date (AC2, AC5).
4. The predicate declaration with its four fields, its four meanings and the library boundary (AC3).
5. The refusal declaration: 404 with MSG-P4-003, no count, the `AC-DENY` entry with reason code `OUT_OF_SCOPE`, and the 503 with MSG-P7-003 (AC4).
6. The rights of the read and of the change, and the 401 and 403 of the default deny rule (AC6).
7. The error envelope and the message-id mapping, with the legacy texts copied unchanged (AC6).
8. The event declaration and the decision-record type, with the change kind and the payload, and the statement that no third name exists (AC5).
9. The four fakes and the stub fixtures of section 12.8 (AC7).
10. The seven contract tests; a drift between a fake and the document fails the build. Baseline tag and the consumer sign-off note of the app story and of the guard library (AC1 to AC7).

**Feature switch.** The contract carries no switch. The two operations are operations of the service and the change is a data change guarded by the C letter; nothing about a scope is behind a flag.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD003-APP | The two provided operations, the three schemas, the predicate, the refusal, the event declaration and the four fakes |
| RWB-PLT-E1037-CON and RWB-PLT-E1037-APP, the guard library | The predicate's four fields, their meanings and the statement that the guard applies them and returns no record |
| RWB-P4-E1037-CON, the access contract that carries the predicate | The scope element of the authorise answer, and the refusal status and message it produces |
| RWB-P3-E1018-CON, the case read | The 404 with MSG-P4-003 a case outside the predicate receives, and the naming of DF-CAS-009, DF-CAS-011 and DF-CAS-012 |
| The wave 4 harness | The fakes of 12.8 and the case-list stub |

The deprecation window of a published field and the retention of the contract fakes are Not specified in the source documents (GAP-0792; ASM-1461).

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the four fakes answer every provided path and every refusal, and the app story, the guard library, the access contract and the case read have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-003 | A record outside the predicate of the caller | This case is not in your scope. |
| MSG-P4-001 | No session, no Workbench role, or a sign-in that resolves no role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller without Platform administration R for the read, or without C for the change | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A value outside `LOV-SCOPE`, a missing field or a role that is not active | Enter {field}. |
| MSG-GEN-004 | An unknown role code, a stale `If-Match`, or a repeated key answered differently | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision-record entry could not be written, on a change or on a refusal | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The access owner does not answer inside the 2 s budget of a consumer | The reference data is not available. Try again later. |

The message ids are contract elements; the text is the agreed text, taken from the legacy story where the message already existed. The one legacy criterion this document must not reword is AC2 of RWB-AD-003, "the system does not find the response and the refusal is logged", which RWB-P4-AD003-APP copies word for word; this document fixes only the status, the message id, the reason code and the entry it names. For MSG-P4-002 the {action} value names the action the caller tried and never a case fact or the scope of another person.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | List | The scope read with every role in force, its class and its scope value, and the four `LOV-SCOPE` values as a filter |
| SCR-43 Roles and access | Change | The change request, the `If-Match` version and the field-level 422 answers of the checks |
| SCR-43 Roles and access | Changed | The written role with its new scope, its version and the decision-record entry reference |
| SCR-43 Roles and access | Unchanged | The role unchanged, because the posted value equals the value in force, with no entry and no event |
| SCR-43 Roles and access | Refused | The 403 with MSG-P4-002 and no row, and the 401 with MSG-P4-001 |
| SCR-43 Roles and access | Conflict | The 409 with MSG-GEN-004 for a stale `If-Match`, with the reload advice |
| SCR-43 Roles and access | Not available | The 503 with MSG-P7-003 |
| The case list and the case record of P3, consumed through the composite route | Out of scope | The 404 with MSG-P4-003 and no count of the records excluded |

The screens are served by the gateway-bff composite route (DP-19), which calls the scope read and the access-log read in parallel, one hop each, and merges the answers. The composite route specification, the screen field list and the column order are Not specified in the source documents (GAP-0792; ASM-1461); the document fixes the scope side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-003-01 | AC1 | Contract | Legacy test "Own scope" on the contract side: the document declares the scope read and the scope change, the value `OWN` of `RW-CASEOWN` and the predicate of the four values; the read answers it, so the case list of P3 can be filtered with it; the behaviour itself is tested by RWB-P4-AD003-APP at End to end |
| TC-AD-003-02 | AC2 | Contract | Legacy test "Out of scope" on the contract side: the document declares the 404 with MSG-P4-003, the reason code `OUT_OF_SCOPE` and the entry, and the fake answers the out-of-scope case `RW-2026-000456` in team `MTG-NE` with that status and that message; no case number and no count appears in any answer |
| TC-AD-003-03 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": a caller with no Platform administration letter is declared refused on both operations, and the document declares the 403 with MSG-P4-002 and the refusal entry |
| TC-AD-003-04 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the document declares the 503 with MSG-P7-003 on a change and on a refusal, and the fake answers it, so no consumer treats a refused change or a refused reach as taken |

The four legacy test cases are kept with their IDs and their legacy Covers values, and the legacy test name is written in the Data column. The Level column follows Template and Rules §R7.2: the two operations and the predicate are tested against the artefact at Contract, the legacy Access row stays Component, and the legacy Resilience row of Principle 5 stays NFR. The behaviour of each case in the running service is RWB-P4-AD003-APP's at End to end, and the full test with its Given, When and Then is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD003-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in the contract: the role codes and the four scope values are source values and the document declares the list once; the parameter-level detail of a future fifth value is a major version and not a code constant (BR2, BR11).
- No personal data in a schema, an example or a fake: a scope is a role and one of four values, a predicate is a role's scope and three codes, and a name, an e-mail address or a case number in the document fails the review.
- The contract names only `rwb-access` tables and no operation of another service as provided (DP-01, BR10); the catalogue, the session, the authorise answer, the case columns and the library descriptor are declared as referred to.
- The predicate has four fields and no fifth, and the document states it once so that no consumer invents a fifth bound (BR3).
- The refusal is never a 403 and never a count: a record outside the predicate is indistinguishable from one that does not exist (BR5).
- One REST base, one topic and one event name for the capability, and the shared record type on `rwb.decision-record.v1`; a document that names another service's base, topic or event fails the review (DP-13, BR9).
- The guard and the descriptor are the library's: the document fixes the data and the rule and never a second implementation (BR4).
- Every example and every fake is synthetic; no production role, person, case or entitlement is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

No requirement ID is recorded for legacy RWB-AD-003 in TSD P4 v3 T8, and the Work Package carries the requirement list of this key as empty. The key serves FEAT-ACA-14 (scope a user's cases by team and region, FSD P4 v3 A2.14) and REQ-ACA-009 ("A user sees only the cases and queues their role and scope allow", Must); TSD P4 v3 T8 records REQ-ACA-009 against FEAT-ACA-01 and RWB-E1-022, which is read as the sign-in's use of the same requirement (ASM-1467).

| Feature | Contract element | Test cases |
|---|---|---|
| FEAT-ACA-14, scope a user's cases by team and region | The scope value of `default_scope`, the four values of `LOV-SCOPE` and the predicate of 12.1 and 12.7 | TC-AD-003-01, TC-AD-003-02 |
| REQ-ACA-009, a user sees only the cases and queues their role and scope allow | The predicate applied by the guard before the permission check, and the 404 with MSG-P4-003 and no count | TC-AD-003-01, TC-AD-003-02 |
| The default deny rule and the recorded refusal | The 403 and the 401 of 12.1, the `AC-DENY` entry with reason code `OUT_OF_SCOPE` and the decision-record type of 12.3 | TC-AD-003-02, TC-AD-003-03 |
| The record-before-change rule | The 503 with MSG-P7-003 and the entry reference of the written change | TC-AD-003-04 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy AC1 and AC2, with `Own`, `Team`, `cases` and the refusal | The behaviour of RWB-P4-AD003-APP; this contract carries the elements they are tested against, and section 16 keeps their test cases |
| The Data table: `role` DF-REF-034 to DF-REF-038, and `recovery_case`, `assignment`, `decision_log_entry` as the legacy sources of the case owner, team, region and the ledger | Sections 11, 12.7 |
| The permission check Platform administration R and the roles that hold it | Section 12.1, section 8 (BR8) |
| MSG-P4-003, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-004, MSG-P7-003 | Section 14, exception paths |
| Screen SCR-43 Roles and access | Section 15 |
| The LOV-SCOPE values `OWN`, `TEAM`, `REGION`, `ALL` | Sections 2, 7, 11 (AC2) |
| Legacy test cases TC-AD-003-01 to TC-AD-003-04 | Section 16 |

### 19. Out of scope

- The implementation of the two operations, the migration, the checks, the predicate assembler, the record entries and the event: RWB-P4-AD003-APP.
- The role catalogue, the role rows, their class and their maintenance, and the catalogue operation API-P4-007 `GET /admin/roles`: RWB-P4-E1019-APP. This contract declares the scope as one field of that answer and restates no part of it.
- The permission matrix, the letters, the matrix and masking versions, the masking enforcement and the scope descriptor inside the session answer: RWB-P4-E1037-APP and RWB-P4-E1037-CON.
- The guard, the scope descriptor type, the masker, the `@PersonalData` annotation and their fakes: RWB-PLT-E1037-CON and RWB-PLT-E1037-APP. This document declares the data that fills the predicate and no interface of the library.
- The sign-in, the token, the multi-factor check and the resolution of a person's roles, team and region: RWB-P4-E1022-CON and RWB-P4-E1022-APP.
- The group-to-role mapping: RWB-P4-AD001-CON and RWB-P4-AD001-APP.
- The case, its owner, its team, its region, its queues and its assignment: P3 rwb-case under the ownership map. The columns are named, the table is never read, and the case list of AC1 is a test mock of RWB-P3-E1018-CON.
- The case list and the case record themselves, and the status a screen renders for an out-of-scope case beyond the 404 and MSG-P4-003 this document fixes: P3's screens and operations.
- The access log, its search and its export: RWB-P4-AD007-CON and RWB-P4-AD007-APP; the access review list and its Schedule (JOB-18): RWB-P4-AD008-CON and RWB-P4-AD008-APP; the break-glass grant: RWB-P4-AD006-CON and RWB-P4-AD006-APP.
- The reference data of the estate and its loads — `lov_value`, `reference_row` and `reference_version` — and the parameters: P3 rwb-case under DP-06 and DP-07, neither of which this key applies; `LOV-SCOPE` is declared here as the document's own enumeration (BR11).
- The delegation of authority table and its limits: RWB-P4-E1038-APP and RWB-P4-E2013-APP; `rwb.access.DoaLimitChanged.v1` is theirs.
- The central decision ledger and its query: P7 rwb-decision; the local entry is the library's.
- `partner_user`: S9 rwb-partner under the ownership map.
- The deployment of the capability: the Helm values, the topic creation, the dashboards and the runbook.
- The integration harness and its evidence, and the `-ITG` copies of the test cases: RWB-ITG-AD003-ITG.
- The field-level completeness of the three schemas beyond what section 11 fixes (GAP-0792; ASM-1461).
