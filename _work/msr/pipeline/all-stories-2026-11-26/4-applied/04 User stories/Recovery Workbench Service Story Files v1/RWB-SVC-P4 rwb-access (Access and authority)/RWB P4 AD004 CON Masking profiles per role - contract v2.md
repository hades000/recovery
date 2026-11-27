# RWB-P4-AD004-CON Masking profiles per role - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: new contract story split from RWB-AD-004 for rwb-access — the published profile of `masking_rule` per role and per personal field, its dated version, the unmask answer and its record. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD004-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP07, DP08, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **consumer of the access service** — the enforcement point, the two administration screens and any service that shows a personal field — I want **one published masking-profile contract for `rwb-access`, with the profile, its version in force, the masked-by-default invariant and the unmask answer**, so that **every consumer masks the same way from Day 1 and none of them reads `masking_rule` or guesses what a mask looks like**.

This is the contract half of legacy RWB-AD-004. It publishes three operations and their schemas and declares nothing else:

- **Service facts.** REST base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1`, event names `rwb.access.<Event>.v1`, task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`. The document is OpenAPI 3.1 and its major version is in the base path.
- **The three operations.** `GET /admin/masking-profiles` (the rows of the version in force for the roles and fields asked), `POST /admin/masking-profile-versions` (write a dated version) and `POST /admin/masking-profiles/{roleCode}/unmask` (one field in clear, with one PII record). None of the three has an ownership row or an operation id in TSD P4 v3 — **Not specified in the source documents (GAP-2267; ASM-3736)**.
- **The row and the version.** `MaskingProfileRow` carries `roleCode`, `fieldId`, `unmasked`, `maskingVersion`, `validFrom`, `validTo`, `view` and `column`; `MaskingProfilePage` adds the page and `versionInForce`. The `view` and `column` are resolved from the field id and are not columns of `masking_rule` (TSD P4 v3 T3.1) — **Not specified in the source documents (GAP-2267; ASM-3738)**.
- **Masked by default, in the schema.** `unmasked` defaults to false, a field with no row is stated as masked, and the document states that the masked value comes from `v_ace_customer.id_no_masked` or `v_ace_contact.contact_value_masked`, or from the masker shape where the view has none. The FSD shapes are kept: `XXXXXXXXX1234`, `XXXXXX5678`, `XXXX-XX-XX`.
- **The unmask answer.** `UnmaskedField` carries `fieldId`, `value`, `maskingVersion` and `piiRecordId`; the document states that the record is written before the value is answered, so a record that cannot be written answers nothing — **Not specified in the source documents (GAP-2267; ASM-3737)**.
- **The rights.** Reference data R for the read, Reference data C for the write, and the row's own `unmasked` flag for the unmask (TSD P4 v3 T6.1). The approval right A is RW-COMPLY's and belongs to the approve gate of RWB-P4-AD010-APP, which this document refers to and does not declare (ASM-3739).
- **No business event.** The ownership rows give `rwb-access` no event; the only publication is the decision-record message of the local library on `rwb.decision-record.v1` (DP-03), and a masking change travels on the profile read and the access log (ASM-3741).
- **Consumers.** The enforcement point of RWB-P4-E1037-APP, SCR-47 Personal data and SCR-43 Roles and access through the gateway-bff composite route (DP-19), and every service that shows a personal field through the guard of RWB-PLT-E1037-CON.
- **The fake.** One profile fake with the SIT rows of `MASK-SIT-01`, the version in force and the refusals, and a drift job that fails the build when an answer and the document disagree.

### 2. Business rationale

The profile is only worth holding as data if every reader reads it the same way. Without a published contract a consumer guesses what the profile read returns, whether a rule names a view and a column or only a field id, what an unmask answers, which right it needs and what the PII record holds — and the guesses drift at the first profile change, in the one place where a drift shows a personal field in clear. With the contract, the app story and the enforcement point compile and test from Day 1 against a fake, and neither of them can quietly read `masking_rule` because the contract gives it no connection to do so.

This is the pattern of the whole realignment: a contract-first service answers one hop from its own schema, and the consumer builds against the published shape and its fake (ADR-020). The contract also fixes the two things a data change must never move: the masked-by-default invariant and the ban on the clear identity number. A version that names it is refused at the write, and the schema says so.

The story is Day 1 work with no build dependency, so the enforcement point and the screens are not blocked by the profile implementation. That is the point of a contract group: the four stories of wave 4 that touch a personal field start against this document on day one.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| The service row and naming rules of the context pack | The base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, task queue `rwb-access`, Java package, epic RWB-SVC-P4 |
| TSD P4 v3 T3.1 and T3.2 | `masking_rule` and its seven fields (DF-REF-198 to DF-REF-204); `LOV-ROLE` and `LOV-VERSION-STATUS` |
| TSD P4 v3 T6.1 and T6.2 | The Reference data letters R, C and A per role, and the rule that each endpoint declares its capability area and right |
| Legacy RWB-AD-004 | The three criteria, the five messages, the two screens and the guardrail that a rule names a view column and never the clear identity number |
| FSD P4 v3 A2.5 | FEAT-ACA-05, BR-P4-005 and the mask shapes of the three examples |
| The ownership rows of P4 | The four operations the service already provides (`GET /admin/access-log`, `GET /admin/roles`, `GET /me/session`, `POST /admin/break-glass-grants`) and the five tables it owns; the profile operations are not among them — **Not specified in the source documents (GAP-2267; ASM-3736)** |
| The error catalogue | MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001 and MSG-P7-003, as the legacy story names them |

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three operations under the base `/api/recovery/access/v1`, with the components the service's other operations use, and pin it at version 1.
2. Declare `MaskingProfileRow`, `MaskingProfilePage`, `MaskingProfileVersion`, `MaskingProfileVersionRow`, `UnmaskRequest`, `UnmaskedField` and the shared error envelope, with the example values of the FSD.
3. Declare the rights per operation from TSD T6.1: Reference data R for the read, Reference data C for the write, and the row's `unmasked` flag for the unmask, which the document describes as a data condition and not as a letter.
4. Declare the errors: 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003, 409 a version label already in force or a stale `If-Match`, 422 MSG-GEN-001 or a version refused whole, 503 MSG-P7-003.
5. Declare the two consumed operations for the reader: the case read of P3 and the ACE view read of P1, one hop each, 2 s budget, mock only (DP-05, DP-11).
6. Write the invariants as document text and as schema constraints: masked by default, `unmasked` false unless a row says otherwise, the clear identity number in no field and in no example, the PII record written before the value is answered.
7. Publish the profile fake: the `MASK-SIT-01` rows, the version in force on a date, an allowed unmask and a refused one, and a forced decision-record failure.
8. Add the drift job: the fake's answers are compared with the document on every build, and a change to one without the other fails the pipeline.
9. Hand the document and the fake to RWB-P4-AD004-APP, RWB-P4-E1037-APP and RWB-P4-E1037-CON; publish no message of its own.

### 5. Exception paths

| Exception | Answer in the document | Why it matters to a consumer |
|---|---|---|
| A consumer calls a path on the monolith base `/api/recovery/v1` | Not declared; 404 from the edge | The one-hop rule has one base per service (DP-13) |
| A consumer asks with no session or no Workbench role | 401 MSG-P4-001 | The consumer must not treat a 401 as an empty profile |
| A consumer's role holds no Reference data R | 403 MSG-P4-002 | A profile read is never answered empty as a fallback |
| A field with no row in the version in force | `unmasked` false and the masked column named | The absence of a rule never widens a view |
| A version naming the clear identity number or repeating a role and field pair | 422 and the whole version refused | The invariant is enforced at the boundary, not at each consumer |
| A version label already in force or a stale `If-Match` | 409 | A retry is safe and writes no second version |
| The record or the PII record cannot be written | 503 MSG-P7-003 | The consumer must show nothing rather than an unrecorded value |
| The P1 view read fails | 503; no clear fallback is declared | Fail closed on a personal field |

### 6. INVEST check

| Letter | Finding |
|---|---|
| Independent | No build dependency; the document and the fake stand on their own |
| Negotiable | The schema names and the example values are the document's; the paths follow the service base and the legacy capability |
| Valuable | Every consumer of a personal field builds and tests against one published shape from Day 1 |
| Estimable | One document, six schemas, one fake, one drift job |
| Small | No code beyond the fake and the drift check; no workflow, no schedule, no event |
| Testable | Each criterion is a Contract check on the document or on the fake's answer |

### 7. Acceptance criteria

```gherkin
Feature: Masking profiles per role - contract

  Scenario: AC1 The document declares exactly three profile operations on the service base (new, D-RCV-60)
    Given the published OpenAPI 3.1 document of rwb-access
    When its operation list is read
    Then exactly three operations carry the paths /admin/masking-profiles, /admin/masking-profile-versions and /admin/masking-profiles/{roleCode}/unmask under /api/recovery/access/v1
    And no operation of this capability carries the path /api/recovery/v1
    And each of the three names its right from TSD P4 v3 T6.1

  Scenario: AC2 The profile read answers the version in force with its view and its column (new, D-RCV-60)
    Given the contract fake is started with the rows of MASK-SIT-01
    When a consumer calls GET /admin/masking-profiles with roleCode RW-CASEOWN and validOn 2026-12-03
    Then the answer is a MaskingProfilePage whose versionInForce is MASK-SIT-01
    And every row carries roleCode, fieldId, unmasked, maskingVersion, validFrom, validTo, view and column
    And the row of the identity number names the column id_no_masked of the view v_ace_customer

  Scenario: AC3 The unmask answer carries the value and the record reference (new, D-RCV-60)
    Given the contract fake is started with a row of RW-CASEOWN whose unmasked is true for the contact value
    When a consumer calls POST /admin/masking-profiles/RW-CASEOWN/unmask with case RW-2026-000123 and that field id
    Then the answer is an UnmaskedField with that fieldId, the value from v_ace_contact.contact_value, the maskingVersion and a piiRecordId
    And the document states that no value is answered when the PII record cannot be written

  Scenario: AC4 Masked by default and the clear identity number are declared as invariants (new, D-RCV-60)
    Given the published document and its examples
    When the schemas and the examples are scanned
    Then a row with unmasked false, and a field with no row, are declared masked with the column named
    And no schema, field or example carries the clear identity number
    And the document states the mask shapes XXXXXXXX1234 for an identity number, XXXXXX5678 for a phone and XXXX-XX-XX for a date

  Scenario: AC5 Every failure is one envelope with one message (new, D-RCV-60)
    Given a caller whose role holds no Reference data R
    When it calls the profile read on the fake
    Then the answer is 403 with MSG-P4-002 in the one error envelope
    And the document declares 401 with MSG-P4-001, 404 with MSG-P4-003, 422 with MSG-GEN-001 and 503 with MSG-P7-003 on the operations where each can occur

  Scenario: AC6 The fake matches the document and carries no personal data (new, D-RCV-60)
    Given the fake and the drift job of the build
    When the fake's answers are compared with the document
    Then every declared operation, status and message id is answered as declared
    And a change to one side without the other fails the build
    And no personal value, and no case number beyond the example, appears in the fake or in the examples
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One base per service: `/api/recovery/access/v1`, with the major version in the path | DP-13; ADR-020 |
| BR2 | A personal field is masked unless a row of the version in force says `unmasked` true for a role the caller holds | Legacy AC1 |
| BR3 | A masking rule names the view column the masked value comes from, and no rule returns the clear identity number | Legacy guardrail; ADR-010 |
| BR4 | The version in force on a date is the latest `valid_from` not after it; an applied version is never edited | TSD T4 |
| BR5 | The PII record is written before the value is answered; a record that cannot be written answers nothing | Legacy AC2; ASM-3737 |
| BR6 | An error is one envelope with one message id from the catalogue, and a refusal changes nothing | FSD VR-P4-005-1 |
| BR7 | No personal data in an example, a fake, a schema or a message | Legacy guardrail; NFR-040 |

### 9. State transitions

| From | Trigger | To | What the document must say |
|---|---|---|---|
| (none) | `POST /admin/masking-profile-versions` passes every check | LOADED | The answer carries the version, its status and its id; 409 if the label is already in force |
| LOADED | the approve gate of RWB-P4-AD010-APP | APPROVED | Declared by that contract, referred to here and not declared |
| APPROVED | `valid_from` arrives | IN_FORCE | `versionInForce` of the read changes on that date with no deployment |
| IN_FORCE | a later version reaches IN_FORCE | SUPERSEDED | `validTo` of the earlier version is the day before the later `validFrom` |
| IN_FORCE | a rollback of the reference version | ROLLED_BACK | Declared by the rollback operation of AD010, and the earlier version is answered again |
| LOADED | a check fails | REFUSED | 422 and no row of the version stored |

### 10. Authority

| Capability area | Right | Roles | Operation |
|---|---|---|---|
| Reference data | R | every role of TSD P4 v3 T6.1 | `GET /admin/masking-profiles` |
| Reference data | C | RW-COE, RW-REFADM | `POST /admin/masking-profile-versions` |
| Reference data | A | RW-COMPLY | the approve gate of RWB-P4-AD010-APP, referred to and not declared |
| the row's own `unmasked` flag | — | the roles a row names with `unmasked` true | `POST /admin/masking-profiles/{roleCode}/unmask` |

Every operation declares its capability area and its right, as TSD T6.2 requires; a service identity (SY-AGENT, SY-CASEWF) is subject to the same rows as a person (NFR-051).

### 11. Data

| Table or view | Schema | Fields (BR Field IDs) | Contracted use |
|---|---|---|---|
| `masking_rule` | `rwb_access` | `id` DF-REF-198, `role_code` DF-REF-199, `field_id` DF-REF-200, `unmasked` DF-REF-201, `masking_version` DF-REF-202, `valid_from` DF-REF-203, `valid_to` DF-REF-204 | The row the read answers and the write creates |
| `role` | `rwb_access` | `role_code` DF-REF-034 to `default_scope` DF-REF-038 | The role codes a row may name, and their letters |
| `permission` | `rwb_access` | `role_id`, `capability_area`, `letters` | The caller's Reference data letters |
| `v_ace_customer` | ACE, read-only view | `id_no_masked`, `id_no_last4` and the rest — DF-ACE-055 to DF-ACE-074 | Named as the source of the masked identity number |
| `v_ace_contact` | ACE, read-only view | `contact_value`, `contact_value_masked` and the rest — DF-ACE-075 to DF-ACE-083 | Named as the source of the masked and the clear contact value |

The document names no table of another service. `decision_log_entry` is P7's and is reached only through the local library (DP-03); `lov_value` and `reference_row` are P3's (DP-07). The field-to-view-and-column map is not a column of `masking_rule` — **Not specified in the source documents (GAP-2267; ASM-3738)**.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Schemas | Right |
|---|---|---|---|
| GET | `/admin/masking-profiles` | query `roleCode`, `fieldId`, `validOn`, `page`, `size`; answer `MaskingProfilePage` of `MaskingProfileRow` | Reference data R |
| POST | `/admin/masking-profile-versions` | `MaskingProfileVersion` in, with `Idempotency-Key`; answer the written version with status and id | Reference data C |
| POST | `/admin/masking-profiles/{roleCode}/unmask` | `UnmaskRequest` in, with `Idempotency-Key`; answer `UnmaskedField` | the row's `unmasked` flag |

Errors: 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003, 409 a version label already in force or a stale `If-Match`, 422 MSG-GEN-001 or a version refused whole, 503 MSG-P7-003. Schemas: `MaskingProfileRow` (`roleCode`, `fieldId`, `unmasked`, `maskingVersion`, `validFrom`, `validTo`, `view`, `column`), `MaskingProfilePage` (items, page, size, total, `versionInForce`), `MaskingProfileVersion` (`maskingVersion`, `validFrom`, rows of `roleCode`, `fieldId`, `unmasked`), `MaskingProfileVersionRow`, `UnmaskRequest` (`caseId`, `fieldId`), `UnmaskedField` (`fieldId`, `value`, `maskingVersion`, `piiRecordId`) and the shared error envelope. The three paths are fixed here because no source names them — **Not specified in the source documents (GAP-2267; ASM-3736)**.

The session read `GET /me/session` and the role catalogue `GET /admin/roles` are the service's own operations of RWB-P4-E1037-CON and RWB-P4-E1019-APP; this document neither restates nor changes them.

#### 12.2 REST operations consumed

| Operation | Owner | What the document declares | Class |
|---|---|---|---|
| `GET /api/recovery/case/v1/cases/{caseId}` | P3 `rwb-case` | The case whose personal fields the profile masks; one hop, 2 s, mock at test level | mock only; no C |
| the ACE-view read of `rwb-source-data` for `v_ace_customer` and `v_ace_contact` | P1 `rwb-source-data` | The masked and the clear columns of the two views (DP-05) | mock only |

The P1 operation path is not named in the source documents — **Not specified in the source documents (GAP-2267; ASM-3736)**; the fake answers it on the P1 base `/api/recovery/source-data/v1`.

#### 12.3 Events published

| Event | Topic | Owner | Content |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library (DP-03), consumer P7 `rwb-decision` | Entry id, decision code (`AC-UNMSK`, `AC-DENY`), role code, field ids and their masked flags, masking version, time |

No business event is declared for this capability: the ownership rows give `rwb-access` no event, and a masking change reaches a consumer on the profile read and the access log (ASM-3741). CloudEvents 1.0 envelope; no personal value in any message.

#### 12.4 Events consumed

None. The document declares no subscription; the profile is answered from `rwb_access`.

#### 12.5 Workflows and activities

None. The three operations are synchronous; the six-monthly access-review Schedule (JOB-18) is RWB-P4-AD008-CON's.

#### 12.6 Schedules

None. `valid_from` and `valid_to` are dates the read compares with; no job moves a version into force.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `masking_rule` | P4 (`rwb_access`) | The profile row and its version |
| `role`, `permission` | P4 (`rwb_access`) | Read only; the role codes and the caller's letters |
| `decision_log_entry` | P7 (`rwb_decision`) | Referred to through the library; no column of it is in the contract |
| `v_ace_customer`, `v_ace_contact` | ACE, read-only views | Named as the source of a masked or clear value, never written |

#### 12.8 Contract fakes

| Fake | Owner of the fake | What it answers |
|---|---|---|
| Profile fake | RWB-P4-AD004-CON (this story) | The three operations with the `MASK-SIT-01` rows, the version in force, an allowed unmask, a refused unmask and a forced record failure |
| Reference-data fake | RWB-PLT-E1043-CON | `LOV-ROLE` and `LOV-VERSION-STATUS` at the version in force |
| Decision-record fake | RWB-PLT-E1027-CON | The entry id and a forced failure |
| Guard and masker fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The caller's roles and letters, and the mask shape of a field with no masked column |
| Case fake | P3 contract | The case read for `RW-2026-000123` |
| ACE-view fake | P1 contract | The two views and their masked columns |

#### 12.9 Call-type summary

| Call type | Out | In |
|---|---|---|
| REST | 2 consumed (P3 case, P1 ACE views) | 3 provided |
| Kafka | 1 published (decision-record, through the library) | none |
| Temporal | none | none |
| File | none | none |

### 13. Solution plan

**Deliverables.** `api/access-v1.yaml` (OpenAPI 3.1) published at version 1, the profile fake, the drift job, and the change note the service's contract group reviews.

| DP | Legacy marker | What this contract does | Dependency |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Declares the local entry through the library on the shared topic | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*` | Declares the two views as the only source of a masked or clear value, through P1 | none |
| DP-07 | Reference data, LOV | Declares `LOV-ROLE` and `LOV-VERSION-STATUS` at the version in force | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Declares the caller's roles, letters and the masker as the guard's answer | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | Every path on `/api/recovery/access/v1` | none |
| DP-19 | Screen, ace-web | Declares SCR-47 and SCR-43 as gateway-bff composite routes | H RWB-PLT-N001-CON |

1. Draft the document with the base, the three operations, the six schemas and the error envelope; pin it at version 1.
2. Declare the rights and the errors per operation, each message with its catalogue id.
3. Declare the two consumed operations as mocks with the one-hop and 2 s rule.
4. Write the invariants as document text and as schema constraints: masked by default, no clear identity number, the PII record before the value.
5. Generate the fake from the document, then add the SIT rows and the scripted refusals.
6. Add the drift job to the pipeline, so a document change and a fake change cannot pass apart.
7. Run the scan that no personal value and no clear identity number appears in an example or in the fake.
8. Publish and hand over; the app story for this legacy key and the enforcement point build against the fake.

### 14. Validation and messages

| ID | Type | Message | Declared on |
|---|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. | 401 on all three operations |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | 403 no right; 403 a role with no `unmasked` row |
| MSG-P4-003 | Error | This case is not in your scope. | 404 the case of an unmask request |
| MSG-GEN-001 | Error | Enter {field}. | 422 a missing `maskingVersion`, `validFrom`, `roleCode`, `fieldId` or `caseId` |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 the record or the PII record not written |

The envelope carries a code, a message id, a message text and the field list; a consumer keys on the message id and never on the text. No new message id is invented for this capability.

### 15. Screens and states

| Screen | States | What the contract gives it |
|---|---|---|
| SCR-47 Personal data | Loading; list; masked; unmasked by the rule; refused | The profile page and the unmask answer, with the version on each |
| SCR-43 Roles and access | List; access log; masked by role | The `maskingVersion` and the field flags a read record carries |

Both are gateway-bff composite routes (DP-19): the contract declares the two reads the route merges, and no screen chains a call.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-004-CON-01 | AC1 | Contract | The document validates as OpenAPI 3.1; the base, the three operations, the rights and the six schemas are present; no path on `/api/recovery/v1` |
| TC-AD-004-CON-02 | AC2 | Contract | The `MASK-SIT-01` rows answer `versionInForce`, the eight row fields and the `id_no_masked` column of `v_ace_customer`; a `validOn` before the first `valid_from` answers the earlier version |
| TC-AD-004-CON-03 | AC3 | Contract | The unmask answer carries the four fields; the document states the record-before-value rule; a forced failure answers 503 and no value |
| TC-AD-004-CON-04 | AC4 | Contract | The schema sets `unmasked` false by default; a field with no row is masked; the scan finds no clear identity number and no personal value in a schema or an example; the three mask shapes are the FSD's |
| TC-AD-004-CON-05 | AC5 | Contract | The five message ids with their statuses answer in one envelope; a consumer keying on the text fails the test on purpose |
| TC-AD-004-CON-06 | AC6 | Component | The drift job fails on a document change alone and on a fake change alone; the fake answers every declared status; the pipeline scans the fake for personal data |

### 17. Guardrails

- No business value in the document as a constant: role codes, field ids, versions and mask shapes are data, and the examples are marked as examples.
- No PII in an example, a fake, a log or a message; the identity number is masked before the service and no schema carries it clear.
- ACE data only through the P1 contract or a `v_ace_*` view; the document declares no `public` table and no other service's table.
- One base per service and one hop per call, 2 s timeout; no consumer is invited to chain two calls.
- The contract declares no message id that is not in the catalogue, and no event name the ownership rows do not support.
- Secrets never in the document, the fake or the examples.

### 18. Traceability

| Source | What it contributes |
|---|---|
| RWB-AD-004 (Administration Stories v4) | The story statement, AC1 to AC3 of the app side, the Data rows, the rights and the five messages this document declares |
| FSD P4 v3 A2.5 and A2.4 | FEAT-ACA-05, BR-P4-005, the mask shapes and the refusal messages |
| TSD P4 v3 T3.1, T3.2, T6.1, T6.2, T7 | `masking_rule` and its fields, the two lists of values, the rights per role, the endpoint rule and NFR-039 to NFR-042 |
| Arch v5 slides 8, 10 and 13 | gateway-bff as the only entry for staff screens; each service authorises the object itself with cached permission data from `rwb-access` |
| ADR-010, ADR-020, DL26 | The ACE database and the read-only views; contract-first REST with one hop; the masking plan |
| Related stories | RWB-P4-AD004-APP (the app side), RWB-P4-E1037-APP and -CON, RWB-P4-E1019-APP, RWB-P4-AD010-APP, RWB-P4-AD007-APP, RWB-P4-E1039-APP |
| Registers | GAP-2267; ASM-3736 to -6 |

### 19. Out of scope

- The implementation of the profile, the version write and the unmask — RWB-P4-AD004-APP.
- The enforcement point and the permission matrix — RWB-P4-E1037-APP and RWB-P4-E1037-CON.
- The approve gate, the verify and the rollback of a reference version — RWB-P4-AD010-APP.
- The role catalogue and the scope — RWB-P4-E1019-APP and RWB-P4-AD003.
- The access-log search, the export and the break-glass grant — RWB-P4-AD007-APP and RWB-P4-E1039-APP.
- The views and ACE ingestion — P1 rwb-source-data.
- The ledger and its query — P7 rwb-decision.
- The PII log implementation — the ACE Common audit and PII path (INT-22).
