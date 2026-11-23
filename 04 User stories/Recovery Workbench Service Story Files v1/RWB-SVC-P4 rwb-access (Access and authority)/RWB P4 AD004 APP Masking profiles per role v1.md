# RWB-P4-AD004-APP Masking profiles per role

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-004 for rwb-access — the masking profile held as dated `masking_rule` rows per role and per personal field, the version in force, the masked-by-default read, and the unmask path with the read it records. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD004-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-P4-D |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-AD004-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-P4-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **Compliance and PDPA officer**, I want **a masking profile per role and per personal field held as data, naming the view column the masked value comes from**, so that **personal data is shown only to the roles allowed to see it and the clear identity number never leaves ACE**.

This is the rwb-access slice of legacy RWB-AD-004, and the profile half of that legacy key: the `masking_rule` rows as a dated version per role and per field, masked by default, the unmask path that fills one field from the ACE view and records the read, and the version in force carried on the read record of the access log.

- **Service facts.** REST base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1`, event names `rwb.access.<Event>.v1`, task queue `rwb-access` in namespace `rwb-recovery` (not used here — this story starts no workflow), Java package `th.co.scb.ace.workbench.recovery.access`.
- **The profile row.** One `masking_rule` row is one role and one personal field in one masking version (TSD P4 v3 T3.1): `id` (DF-REF-198), `role_code` (DF-REF-199, LOV-ROLE), `field_id` (DF-REF-200), `unmasked` (DF-REF-201), `masking_version` (DF-REF-202), `valid_from` (DF-REF-203) and `valid_to` (DF-REF-204). `unmasked` says whether that role sees that field in clear in that version; a false value, or no row at all, means masked.
- **The naming rule.** The legacy guardrail is that a masking rule names the view column the masked value comes from, and `masking_rule` carries the field id only. The field id is resolved to its view and column through the P1 field registry, and no view-name column is added to `masking_rule` — **Not specified in the source documents (GAP-2266; ASM-3738)**. What a rule reports is the view and the column: `v_ace_customer.id_no_masked` and `id_no_last4`, `v_ace_contact.contact_value` and `contact_value_masked`.
- **The views.** `v_ace_customer` (DF-ACE-055 to DF-ACE-074) and `v_ace_contact` (DF-ACE-075 to DF-ACE-083) are read read-only through the P1 ACE-view contract (DP-05): the clear contact value only on the unmask path, the masked identity number and the masked contact value everywhere else. Neither view exposes the clear identity number and no rule may name it.
- **Masked by default.** A field with no rule in the version in force, or with a rule whose `unmasked` is false for every role the caller holds, is answered from the masked view column named by its field id; where the view holds no masked column, the value is masked by the masker of RWB-PLT-E1037-CON. The FSD fixes the shapes: `XXXXXXXXX1234` for the identity number, `XXXXXX5678` for the phone and `XXXX-XX-XX` for a date (FSD P4 v3 AC-ALT-P4-004-01, AC-EXC-P4-004-05).
- **The three operations of this story** are the profile read by role and by field with the version in force, the profile version write, and the unmask request and its record, at the paths the contract baseline RWB-P4-AD004-CON fixes on the service base. None of the three has a row in the ownership map and none has an operation id in TSD P4 v3 — **Not specified in the source documents (GAP-2266; ASM-3736)**.
- **The version.** A profile is written as a new dated version with its `masking_version` label and its `valid_from`; the version in force on a date is the one whose `valid_from` is the latest not after that date; the `valid_to` of the earlier version closes on the day before a later `valid_from`; a version in force is never edited (DP-15; ASM-3741).
- **The unmask record.** An unmask fills one field from `v_ace_contact.contact_value` for a role whose rule has `unmasked` true, and writes the read to the PII log. The PII log is the ACE Common audit and PII Kafka path to the SOC (TSD P4 v3 T5.1 INT-22) and not a table of `rwb_access`; its producer, record name and field list are **Not specified in the source documents (GAP-2266; ASM-3737)**.
- **The version on the record.** Every read of a personal field carries the masking version in force, the field ids and their masked flags on the read record; the access-entry writer of RWB-P4-E1039-APP writes the entry and this story supplies the version and the flags, so a profile change is visible in the access log from its `valid_from` date (ASM-3740).
- **The boundary, once.** This story owns the masking-profile version and the unmask record; RWB-P4-E1037-APP owns the enforcement point that reads the profile, the permission matrix that decides who may unmask, and the endpoint enforcement of masking. Neither story redefines the other's shape.
- **Not this story.** The reference-load path (load, approve, verify, rollback) is RWB-P4-AD010-APP's and RWB-P4-E1037-APP's; the role catalogue is RWB-P4-E1019-APP's; the access-log search, the export and the break-glass grant are RWB-P4-AD007-APP's and RWB-P4-E1039-APP's; `lov_value`, `reference_row` and `reference_version` are P3's (DP-07); `decision_log_entry` is P7's (DP-03); `partner_user` is S9's. This story writes no row of any of them.
- **Screens.** SCR-47 Personal data (loading; list; masked and unmasked states) and SCR-43 Roles and access (list; access log) are served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), which reads the profile and the logged reads in parallel.

### 2. Business rationale

PDPA and the bank's own data controls say that a personal field is shown to a person only when their role needs it. The monolith answered that with one masker, one set of rules and the identity number masked inside ACE. The realignment keeps the answer and gives the rule a home: the profile is `masking_rule` rows of `rwb_access`, one row per role and per personal field, written as a dated version, so an audit can say which role could see which field on a given date and a change of masking is a data change with a Compliance approval and not a release. That is FEAT-ACA-05 of FSD P4 v3, measured by rule and limit changes made without a code release.

Masking by default is the rule, not the exception. A field with no rule is masked, and a rule that is absent, false or not in the version in force never widens what a person sees. The profile therefore only ever grants; it never leaves a field open by omission. The values come from the columns ACE already masks — `id_no_masked` and `contact_value_masked` — so the identity number is masked before the Workbench comes into it, and `id_no_last4` is the clearest identity value any rule can reach. The clear contact value is the one exception the notices and the calls need, and it is reached only through the unmask path, with the read recorded.

The boundary with the enforcement point is the profile read. RWB-P4-E1037-APP asks this story for the rows of a session's roles in the version in force and applies them on every screen, every API answer and every agent call; this story answers the version, the fields and the columns, and applies nothing. A profile version that names the clear identity number, a field id that is not a personal field, or a role code the role table does not hold is refused whole, so a mistake in one row never half-applies.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD004-CON (same service, its own contract story) | The published profile contract: the three operations, `MaskingProfile`, `MaskingProfileRow`, `MaskingProfileVersion`, `MaskingProfilePage` and `UnmaskedField`, the naming rule, the masked-by-default invariant, the error envelope and the contract fakes this story builds against from Day 1 |
| RWB-PLT-E1037-CON and RWB-P4-E1037-CON | The guard and masker library and this service's own access contract (DP-08): the masker for a field with no masked view column and the permission answer that resolves the caller's roles and their Reference data letters. The DP row's C for the guard is carried as H because E1037 is a contract of this same service |
| RWB-P4-E1037-APP | The enforcement point that reads the profile; the consumer of the profile read, and the owner of the permission matrix and of the endpoint enforcement of masking |
| RWB-PLT-E1043-CON and RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of rwb-case (DP-07): `LOV-ROLE` and `LOV-VERSION-STATUS` at the version in force. This story builds against the fake and never against the rwb-case build |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a profile version write and of every refusal |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-47 and SCR-43 and merges the profile read with the logged reads |
| The `masking_rule`, `role` and `permission` tables of `rwb_access` | The profile rows (DF-REF-198 to DF-REF-204), the active role codes (DF-REF-034 to DF-REF-038) and the caller's Reference data letters, from the service baseline. This story adds no table; its migration adds the version index and the SIT seed only |
| The two ACE views and their SELECT grants | `v_ace_customer` and `v_ace_contact`, read read-only through the P1 ACE-view contract (DP-05) with their masked columns. The views are never written and never joined to a `public` table |
| The profile versions of the environment | `MASK-SIT-01` in SIT, in which only RW-CASEOWN may see the contact value in clear, and `MASK-2026.11` in production with no unmasked row until Compliance supplies the rules |
| The profile operations | The three paths and their rights, fixed on `/api/recovery/access/v1` — **Not specified in the source documents (GAP-2266; ASM-3736)** |
| The PII log | The ACE Common audit and PII Kafka path to the SOC. Its producer, record name and field list are **Not specified in the source documents (GAP-2266; ASM-3737)** |
| The Compliance approval of a version | The approve gate of RWB-P4-AD010-APP on the reference-load path, with the approver role RW-COMPLY. This story writes the version and never approves it (ASM-3739) |

### 4. Flow

1. A reader's session arrives at the Workbench with its roles from the session answer of RWB-P4-E1037-APP; the Workbench knows the case that is on screen.
2. The enforcement point calls `GET /api/recovery/access/v1/admin/masking-profiles` with the caller's role codes, the field ids of the personal fields on the screen and `validOn` set to the business date. The answer is the rows of the version in force on that date.
3. For each personal field the answer decides one of two outcomes: a row with `unmasked` true for one of the caller's roles means the field may be unmasked on request; anything else means masked.
4. A masked field is answered from the masked view column its field id resolves to — `v_ace_customer.id_no_masked`, `v_ace_contact.contact_value_masked` — read read-only through the P1 ACE-view contract. Where the view holds no masked column, the PLT masker's shape answers (`XXXX-XX-XX` for a date).
5. A caller whose rule allows the unmask calls `POST /api/recovery/access/v1/admin/masking-profiles/{roleCode}/unmask` with the case reference and the field id. The rule is re-read for that role, that field and the date; a role with no such rule is refused before any value is read.
6. On an allowed unmask the one field is filled from `v_ace_contact.contact_value`, one PII record is written with the actor, the role code, the field id, the case reference, the masking version and the time, and the answer carries the field with its value and the record reference.
7. A profile change is written with `POST /api/recovery/access/v1/admin/masking-profile-versions`: the version label, the `valid_from` and the rows of role code, field id and `unmasked`. The version is validated whole, written with status LOADED, and the version it closes takes its `valid_to` as the day before the new `valid_from`.
8. From the `valid_from` date every read answers the new version, and every read record carries `maskingVersion` — so AC3 holds with no deployment: the responses use the new version and the access log carries the version in force.
9. Each write and each refusal writes one decision-record entry through the local library (DP-03), and the entry and the PII record are written in the same transaction window as the change they describe.

### 5. Exception paths

| Exception | Answer | What is left unchanged |
|---|---|---|
| A caller with no Workbench role | 401 with MSG-P4-001 (session refused upstream) | Nothing is read, nothing is written |
| A caller whose roles hold no Reference data R | 403 with MSG-P4-002 naming the action, before any row is read | The profile and the case are untouched |
| An unmask for a role whose rule is absent or false in the version in force | 403 with MSG-P4-002; no value is fetched and no PII record is written | The clear value never leaves ACE |
| A case outside the caller's scope | 404 with MSG-P4-003 | No field, no count and no case number in the answer |
| A field id that is not a personal field, a role code not in the role table, or a missing field | 422 with MSG-GEN-001 | Nothing is written |
| A version whose rows name the clear identity number or repeat a role and field pair | 422; the whole version is refused and no row of it is stored | The version in force stays in force |
| A version label already in force, or a stale `If-Match` | 409 (the envelope of the contract baseline) | The version in force stays in force |
| The decision record cannot be written | 503 with MSG-P7-003 and an incident to the platform administrator queue | The version is not written and the unmask answers nothing (FSD AC-EXC-P4-007-03 pattern) |
| The PII record cannot be written | 503 with MSG-P7-003; the field value is not answered | The read is not recorded, so the value is not shown (ASM-3737) |
| The masked view read is unavailable | 503; the field is not answered in clear as a fallback | Fail closed: no unmasked value |

### 6. INVEST check

| Letter | Finding |
|---|---|
| Independent | Buildable against the published contract of RWB-P4-AD004-CON and the fakes of every H dependency; no other story must ship first |
| Negotiable | The version labels, the SIT seed and the mask shapes are configuration and data; the paths are the contract baseline's |
| Valuable | FEAT-ACA-05 and NFR-039: personal fields are shown by role, and the identity number is never in clear |
| Estimable | Three operations, one table, one version rule, one unmask path; the sources fix the rows and the messages |
| Small | No workflow, no schedule, no event of its own, no screen of its own; one package |
| Testable | Every criterion is a Component or Contract check on a case, a role and a version with fixed values |

### 7. Acceptance criteria

```gherkin
Feature: Masking profiles per role

  Scenario: AC1 Masked by default (legacy RWB-AD-004 AC1)
    Given the rwb-case contract mock returns the case read for case RW-2026-000123
    And a role with no unmasked rule in the version in force
    When it reads a case
    Then the identity number shows from v_ace_customer.id_no_masked
    And the phone number shows from v_ace_contact.contact_value_masked

  Scenario: AC2 Unmask is logged (legacy RWB-AD-004 AC2)
    Given the rwb-source-data contract mock returns contact_value and contact_value_masked for the phone number
    And a role allowed to unmask the contact value
    When it unmasks the phone number on a case
    Then the system fills the field from v_ace_contact.contact_value and writes the read to the PII log
    And the identity number is still shown from id_no_masked, never in clear

  Scenario: AC3 Profile change (legacy RWB-AD-004 AC3)
    Given a new masking_rule version approved by Compliance
    When its valid from date arrives
    Then responses use the new version and the access log carries the version in force
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A personal field is masked unless a row of the version in force says `unmasked` true for a role the caller holds | Legacy AC1; FSD A2.5 |
| BR2 | A masking rule names the view column the masked value comes from, and no rule returns the clear identity number | Legacy guardrail; ADR-010 |
| BR3 | `unmasked` true is granted per role and per field, and every unmask writes one PII record | Legacy AC2 |
| BR4 | A version applies from its `valid_from`; the version in force on a date is the latest `valid_from` not after it; an applied version is never edited | TSD T4; LOV-VERSION-STATUS |
| BR5 | Every read record carries `maskingVersion`, so the access log shows the version in force at the read | Legacy AC3; RWB-P4-E1039-APP |
| BR6 | No value a business person may change is written in code; it is a versioned data row | FSD BR-P4-005; VR-P4-005-1 |
| BR7 | An action outside the caller's rights is refused with MSG-P4-002 and nothing changes | FSD VR-P4-005-1, VR-P4-005-3 |
| BR8 | A version, a refusal or an unmask that cannot be recorded does not take effect | FSD AC-EXC-P4-005-07; MSG-P7-003 |

### 9. State transitions

| From | Trigger | To | Side effect |
|---|---|---|---|
| (none) | `POST /admin/masking-profile-versions` passes every check | LOADED | Rows written; decision-record entry; one PII-free version summary |
| LOADED | Compliance approves through the gate of RWB-P4-AD010-APP | APPROVED | Approver and time recorded by AD010, not here |
| APPROVED | `valid_from` arrives | IN_FORCE | The read answers these rows from this date; `maskingVersion` on every read record |
| IN_FORCE | a later version reaches IN_FORCE | SUPERSEDED | `valid_to` set to the day before the later `valid_from` |
| IN_FORCE | a rollback of the reference version (AD010's operation) | ROLLED_BACK | The earlier version is in force again; recorded by AD010 |
| LOADED | a check fails | REFUSED | No row stored; the version in force unchanged; one entry |
| any | a read of a field | any | Masked or unmaskable, decided per role and field; nothing else changes |

### 10. Authority

| Capability area | Right | Roles | Where used in this story |
|---|---|---|---|
| Reference data | R | every role of TSD P4 v3 T6.1 (RW-CASEOWN, RW-PHONECOL, RW-TEAMMGR and the rest) | the profile read |
| Reference data | C | RW-COE, RW-REFADM | the profile version write |
| Reference data | A | RW-COMPLY | the approval, held by RWB-P4-AD010-APP and not by this story |
| the row's own `unmasked` flag | — | the roles a row names with `unmasked` true | the unmask request |
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | the access-log panel of SCR-43, served by RWB-P4-AD007-APP |

A caller holding no right in Reference data is refused with MSG-P4-002 before any row is read; a service identity (SY-AGENT, SY-CASEWF) is subject to the same rows as a person (NFR-051).

### 11. Data

| Table or view | Schema | Fields (BR Field IDs) | Use |
|---|---|---|---|
| `masking_rule` | `rwb_access` | `id` DF-REF-198, `role_code` DF-REF-199, `field_id` DF-REF-200, `unmasked` DF-REF-201, `masking_version` DF-REF-202, `valid_from` DF-REF-203, `valid_to` DF-REF-204 | Owned: the profile row and its version |
| `role` | `rwb_access` | `role_code` DF-REF-034 to `default_scope` DF-REF-038 | Read only: the role codes a row may name |
| `permission` | `rwb_access` | `role_id`, `capability_area`, `letters` | Read only: the caller's Reference data letters (TSD T6.1) |
| `v_ace_customer` | ACE, read-only view | `cif_no`, `person_key`, `first_name`, `last_name`, `id_no_masked`, `id_no_last4` and 14 more — DF-ACE-055 to DF-ACE-074 | Read through P1: the masked identity number |
| `v_ace_contact` | ACE, read-only view | `contact_type`, `contact_key`, `person_key`, `contact_value`, `contact_value_masked` and 4 more — DF-ACE-075 to DF-ACE-083 | Read through P1: the masked contact value everywhere, the clear value on the unmask path only |

The story writes `masking_rule` and nothing else. `decision_log_entry` is P7's, written through the local library (DP-03). `lov_value`, `reference_row` and `reference_version` are P3's (DP-07). The field-to-view-and-column map is not a column of `masking_rule` — **Not specified in the source documents (GAP-2266; ASM-3738)**.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Request and answer | Right | Idempotency |
|---|---|---|---|---|
| GET | `/admin/masking-profiles` | Query `roleCode`, `fieldId`, `validOn`, `page` (default 50, max 200), `size`; answer `MaskingProfilePage` — items of `MaskingProfileRow` with `roleCode`, `fieldId`, `unmasked`, `maskingVersion`, `validFrom`, `validTo`, `view`, `column`, and the page's `versionInForce` | Reference data R | Read only |
| POST | `/admin/masking-profile-versions` | `MaskingProfileVersion` in (`maskingVersion`, `validFrom`, rows of role code, field id and `unmasked`); answer the written version with its status and its id | Reference data C | `Idempotency-Key`; the same key returns the first answer and writes no second version |
| POST | `/admin/masking-profiles/{roleCode}/unmask` | `UnmaskRequest` in (`caseId`, `fieldId`); answer `UnmaskedField` (`fieldId`, `value`, `maskingVersion`, `piiRecordId`) | the `unmasked` rule of the version in force for that role and that field | `Idempotency-Key`; the same key answers the first call and writes no second PII record |

Errors for all three: 401 no session or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 case out of scope (MSG-P4-003), 409 a version label already in force or a stale `If-Match`, 422 a missing field (MSG-GEN-001) or a version refused whole, 503 the record entry or the PII record not written (MSG-P7-003). Major version 1 sits in the base. The three paths have no ownership row and no operation id in TSD P4 v3 — **Not specified in the source documents (GAP-2266; ASM-3736)**.

#### 12.2 REST operations consumed

| Operation | Owner | What it gives | Class |
|---|---|---|---|
| `GET /api/recovery/case/v1/cases/{caseId}` | P3 `rwb-case` | The case and its person keys, whose personal fields are masked by this profile | Mock at test level only; the story declares no C for it |
| the ACE-view read of `rwb-source-data` for `v_ace_customer` and `v_ace_contact` (P1) | P1 `rwb-source-data` | The masked identity number, the masked contact value, and the clear contact value on the unmask path (DP-05) | Mock at test level only |

The P1 operation path is not named in the source documents — **Not specified in the source documents (GAP-2266; ASM-3736)**; the mock answers it on the P1 base `/api/recovery/source-data/v1`.

#### 12.3 Events published

| Event | Topic | Owner | Content |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library (DP-03), ledger consumer P7 `rwb-decision` | Entry id, decision code (`AC-UNMSK` for an unmask, `AC-DENY` for a refusal), role code, field ids and their masked flags, masking version, case reference, time |

`rwb-access` declares no business event of its own: the ownership rows give the service no event, and a masking change travels on the profile read and on the access log rather than on a topic (ASM-3741). Every message uses the CloudEvents 1.0 envelope and carries no person, name, e-mail address, case number or identity number.

#### 12.4 Events consumed

None. The service holds the profile and reads it locally; it subscribes to nothing to answer a masking question.

#### 12.5 Workflows and activities

None. All three operations are synchronous REST answers in the caller's thread: no workflow, no activity, no signal, no child.

#### 12.6 Schedules

None. Nothing about a profile runs on a clock: `valid_from` and `valid_to` are dates the read compares with.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `masking_rule` | P4 (`rwb_access`) | The profile row and its version (DF-REF-198 to DF-REF-204) |
| `role` | P4 (`rwb_access`) | Read only; the active role codes a row may name |
| `permission` | P4 (`rwb_access`) | Read only; the caller's Reference data letters |
| `decision_log_entry` | P7 (`rwb_decision`) | Appears nowhere; the local entry is the library's and the ledger is P7's |
| `v_ace_customer`, `v_ace_contact` | ACE, read-only views | Named, never written and never joined to a `public` table |

No foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | From | What it answers |
|---|---|---|
| Profile fake | RWB-P4-AD004-CON | The three operations with the `MASK-SIT-01` rows, the version in force and the two refusals |
| Reference-data fake | RWB-PLT-E1043-CON, RWB-P3-E1043-CON | `LOV-ROLE` and `LOV-VERSION-STATUS` at the version in force |
| Decision-record fake | RWB-PLT-E1027-CON | The entry id and the outbox row on `rwb.decision-record.v1`, and a forced failure |
| Masker and guard fake | RWB-PLT-E1037-CON, RWB-P4-E1037-CON | The mask shape of a field with no masked column, and the caller's roles and letters |
| Case fake | P3 | The case read for `RW-2026-000123` |
| ACE-view fake | P1 | `id_no_masked`, `id_no_last4`, `contact_value_masked` and, on the unmask path only, `contact_value` |

#### 12.9 Call-type summary

| Call type | Out | In |
|---|---|---|
| REST | 2 consumed (P3 case, P1 ACE views) | 3 provided |
| Kafka | 1 published (decision-record, through the library) | none |
| Temporal | none | none |
| File | none | none |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.masking`, module `masking`, under the service root `th.co.scb.ace.workbench.recovery.access`.

| DP | Legacy marker | What this story does | Dependency |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Writes the local entry through the library and the shared topic, with the profile version on it | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*` | Reads the two views through the P1 contract; the clear contact value only on the unmask path | none |
| DP-07 | Reference data, LOV | `LOV-ROLE` and `LOV-VERSION-STATUS` through the reference-data contract and its library | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | The caller's roles, letters and the masker come from the guard contract of this service | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | Every path sits on `/api/recovery/access/v1` | none |
| DP-19 | Screen, ace-web | SCR-47 and SCR-43 are served by the gateway-bff composite route | H RWB-PLT-N001-CON |

1. Flyway in `rwb_access`: the version index on `masking_rule` (`role_code`, `field_id`, `masking_version`, `valid_from`) and the SIT seed `MASK-SIT-01`; no new table.
2. Domain: `MaskingProfile` (rows of a version), `MaskingPolicy` (the version in force on a date), `resolveViewColumn(fieldId)` through the P1 field registry, `Masked`/`Unmaskable` value objects.
3. Read service: `GET /admin/masking-profiles` — rights from the guard, rows in force for the role codes asked, `view` and `column` resolved per row.
4. Write service: `POST /admin/masking-profile-versions` — validate the whole version (role codes exist, field ids are personal fields, no row names the clear identity number, no repeated role and field pair), close the earlier version, write LOADED, one decision-record entry.
5. Unmask service: `POST /admin/masking-profiles/{roleCode}/unmask` — re-read the rule for the role, field and date; refuse without a rule; fetch the clear value through P1; write the PII record; answer the field.
6. Wire the profile read into the enforcement point of RWB-P4-E1037-APP through the masker interface; the mask shapes of a field with no masked column come from the PLT masker.
7. Tests: unit for the version-in-force rule and for the resolution; component for the three operations with the fakes; contract drift for the answers against RWB-P4-AD004-CON; an NFR check that no personal value appears in a log, an event or a workflow input.

### 14. Validation and messages

| ID | Type | Message | Where |
|---|---|---|---|
| MSG-P4-001 | Error | You have no Recovery Workbench role. Ask your team manager to request one. | 401 on all three operations |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | 403 no right; 403 an unmask for a role with no rule |
| MSG-P4-003 | Error | This case is not in your scope. | 404 the case of an unmask request is out of the caller's scope |
| MSG-GEN-001 | Error | Enter {field}. | 422 a missing `maskingVersion`, `validFrom`, `roleCode`, `fieldId` or `caseId` |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 record entry or PII record not written |

Field validation: `unmasked` is boolean; `valid_from` and `valid_to` are dates with `valid_to` after `valid_from`; `masking_version` is a label of at most 20 characters; `field_id` is a BR Field ID of a personal field; `role_code` is one of `LOV-ROLE` in force. A version that fails one row fails whole.

### 15. Screens and states

| Screen | States | What this story gives it |
|---|---|---|
| SCR-47 Personal data | Loading; list; masked; unmasked by the row's rule; refused | The profile rows of a role and a field with their version, and the unmask answer with its version |
| SCR-43 Roles and access | List; access log; masked by role | The `maskingVersion` and the field flags that the access-log row carries |

Both screens are gateway-bff composite routes (DP-19): the profile read and the logged reads load in parallel and no screen chains a call.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-004-01 | AC1 | Component | SIT profile `MASK-SIT-01`; role RW-PHONECOL with no unmasked rule; case `RW-2026-000123` from the P3 fake; asserts `XXXXXXXXX1234` from `id_no_masked` and `XXXXXX5678` from `contact_value_masked` |
| TC-AD-004-02 | AC2 | Component | RW-CASEOWN with `unmasked` true for the contact value; PII adapter stub asserts one record with actor, role, field id, case, version and time; the identity number still from `id_no_masked` |
| TC-AD-004-03 | AC3 | Component | Version `MASK-2026.11` closed and `MASK-2026.12` from its `valid_from`; the read answers the new version and the access-log row carries `maskingVersion` |
| TC-AD-004-04 | Access (legacy covers) | Contract | RW-PHONECOL without Reference data U on the unmask path: 403 with MSG-P4-002, no value and no PII record |
| TC-AD-004-05 | Principle 5 (legacy covers) | Component | Forced decision-record failure on the version write and on the unmask: 503 with MSG-P7-003, no version and no value |
| TC-AD-004-06 | AC1 | Component | A field with no masked view column (`v_ace_customer.date_of_birth` in `MASK-SIT-01`): `XXXX-XX-XX` from the masker; masked by default holds |
| TC-AD-004-07 | AC2 | Unit | The version-in-force rule: latest `valid_from` not after the date, the earlier version closed the day before, an applied version not editable |
| TC-AD-004-08 | AC3 | Component | A version naming the clear identity number or repeating a role and field pair: 422, the whole version refused, `MASK-2026.11` still in force |

### 17. Guardrails

- No business value in code: role codes, field ids, versions and mask shapes are data rows.
- No PII in events, workflow inputs, logs or test data: the identity number is masked before the service, and `id_no_last4` is the clearest identity value reachable.
- ACE data only through the P1 contract or a `v_ace_*` view; no `public` table is read and no service reads another's tables.
- The clear contact value is fetched only on the unmask path, for a role with an `unmasked` true row, and only with a PII record written; a failure to record answers nothing.
- No rule, schema or example names the clear identity number.
- Secrets in the key store only; no secret in configuration, code or prompt.
- The service owns one schema, one login and one Flyway sequence (DP-01, DP-02, DP-15).

### 18. Traceability

| Source | What it contributes |
|---|---|
| RWB-AD-004 (Administration Stories v3) | Story statement, AC1 to AC3, TC-AD-004-01 to -05, the Data rows, the permission checks, the five messages and the guardrail on the clear identity number |
| FSD P4 v3, A2.5 FEAT-ACA-05 and A2.4 FEAT-ACA-04 | Masked-by-default behaviour, the mask examples, AC-ALT-P4-004-01, AC-EXC-P4-004-05, BR-P4-005, VR-P4-005-1 to -3 |
| TSD P4 v3 T3.1, T4, T6.1, T6.2, T7 | `masking_rule` and its fields, the version lifecycle, the rights, the masking rule on every endpoint, NFR-039 and NFR-040 |
| Arch v5 slides 8, 10 and 13 | gateway-bff as the only entry for staff screens; each service authorises the object itself with cached permission data from `rwb-access` |
| ADR-010 and DL26 | The ACE database and the read-only views; the identity number never in clear; the plan for masking |
| Related stories | RWB-P4-E1037-APP and -CON (enforcement, matrix, authorise), RWB-P4-E1019-APP (roles), RWB-P4-AD010-APP (approval and rollback), RWB-P4-AD007-APP and RWB-P4-E1039-APP (access log), RWB-P1 (views) |
| Registers | GAP-2266; ASM-3736 to -6 |

### 19. Out of scope

- The reference-load path: load, approve, verify and rollback of a reference file — RWB-P4-AD010-APP and RWB-P4-E1037-APP.
- The permission matrix, its letters and the endpoint enforcement of masking — RWB-P4-E1037-APP and RWB-P4-E1037-CON.
- The role catalogue, roles classes and scopes — RWB-P4-E1019-APP.
- The access-log search, the export and the break-glass grant — RWB-P4-AD007-APP and RWB-P4-E1039-APP.
- The separation-of-duty table and the sign-in refusal — RWB-P4-AD005.
- The delegation of authority table — RWB-P4-AD016 and RWB-P4-E1038-APP.
- ACE ingestion and the views themselves — P1 rwb-source-data.
- The ledger, its hash chain and its query — P7 rwb-decision.
- The PII log implementation in ACE Common — the shared audit and PII path (INT-22).
