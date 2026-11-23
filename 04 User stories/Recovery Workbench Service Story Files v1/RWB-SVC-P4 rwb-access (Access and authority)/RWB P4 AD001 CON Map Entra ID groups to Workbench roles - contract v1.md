# RWB-P4-AD001-CON Map Entra ID groups to Workbench roles

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-001 for rwb-access — the contract of the group-to-role mapping as dated data, its read, its change, its version with effective dates and its access-policy event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **tech lead**, I want **the published contract baseline of the group-to-role mapping: an OpenAPI 3.1 document for the mapping read, the mapping change and the version read, the `RoleMapping`, `RoleMappingVersion` and `RoleMappingPage` schemas with the version label and the effective dates, the statement that a mapping change is a dated data version and never a code change, the `rwb.access.AccessPolicyChanged.v1` declaration with its change kind, one RFC 9457 error envelope with its message IDs, the consumed parameters contract and the read-only ACE group view with their owner and one-hop budget, the contract tables of section 12 and the contract fakes**, so that **the app story builds on Day 1 against a fixed, testable contract, and the sign-in that consumes the mapping learns exactly which rows it reads, at which version and on which date**.

The deliverable is the mapping **as data**: the read, the change and the version-with-effective-date operations, and the event that tells the services a mapping changed. What a role may do is not contracted here — the permission matrix is RWB-P4-E1037-CON's — and how a sign-in resolves a person's groups to roles is RWB-P4-E1022-CON's.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story held the group-to-role mapping as a table the monolith read at sign-in, and a change was a row in a database nobody outside the team could describe. In the target the mapping is a column of P4's own role rows with a version and effective dates, so the answer the sign-in needs — which role this group gives on this date — must be written down once, with its fields, its rights, its versions and its event.

The distinction between this key and RWB-P4-E1022 is fixed and this contract is the data half of it. **RWB-P4-E1022-APP resolves the groups of a signed-in person at sign-in; this story owns the mapping rows as data, their version with a valid-from date, and their maintenance, so a new mapping is a data change and never a code change.** RWB-P4-E1022-APP is the H dependency that consumes the mapping, and this document is what it builds against: it declares the mapping version and its dates, so the sign-in can answer the version in force at the moment of the sign-in and hold it until the session ends, and it declares the event that tells the estate a mapping changed.

Two consequences shape the document. The first is that a mapping change is a dated version and never an edit: the change operation writes a version, the reads answer a version, and an applied version is never rewritten — which is the same rule the reference-data loads and the rule packages of this service follow, so the service has one answer to "which value was in force when". The second is that one event name covers it. `rwb.access.AccessPolicyChanged.v1` is the one access-policy event the architecture gives `rwb-access` (Architecture v5 slides 14 and 43), the services that cache permission data already refresh on it (slide 20), and a mapping change **is** an access-policy change; a second name would add a contract without a consumer, because the only reader of the mapping inside the estate is the sign-in of this same service (ASM-1448).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-E1027-CON is published: the decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), whose entry is the record of every mapping change and of every refusal. The dependency is carried by the app story, RWB-P4-AD001-APP (ASM-1450).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters client library and the parameters contract of rwb-case (DP-06), through which the environment code of the deployment is read. The dependencies are carried by the app story (ASM-1446).
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that serves SCR-43 and merges the mapping read with the access-log read of RWB-P4-AD007-APP. The dependency is carried by the app story.
- The ACE view `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) is granted and contracted by RWB-P1-E1069-APP (DP-05); this document declares it as a read-only consumed read with its `data_as_of`, and the app story names the grant in its preconditions.
- The mapping columns and field IDs are **Not specified in the source documents (GAP-0788; ASM-1444)**: `role` in TSD P4 v3 T3.1 carries `entra_group` (DF-REF-039) and no version or date column, while legacy AC3 needs a mapping version with a valid-from date. This document fixes the field names and the types of the three schemas and leaves the physical column names to the app story.
- The mapping operations have no row in the ownership map and none in TSD P4 v3 appendix T-A, where the only role read is `GET /admin/roles` (API-P4-007): their paths, rights and answers are this document's own decision — **Not specified in the source documents (GAP-0788; ASM-1447)**.
- The mapping lives on the role rows of the environment: `role.entra_group` is the mapping, `v_ace_iam_group` is the read-only reference of the group and not the Workbench mapping (ASM-1445, which takes TSD P4 v3 T3.1 over the FSD P4 v3 field catalog under R-PREC).
- The final group names per environment are the bank IAM decision DL40; the legacy example is the group `RWB-SIT-RW-CASEOWN` on the role `RW-CASEOWN` in SIT.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), and it holds in Contract group CG-W4 because the business epic EP08 is wave 4 in the W-MAP (§R5.6).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three mapping operations under the base `/api/recovery/access/v1`, with the shared components the `rwb-access` operations use.
2. Draft the schemas `RoleMapping`, `RoleMappingVersion` and `RoleMappingPage`: the group name, the role code and name, the environment, the mapping version label, the valid-from and valid-to dates, the author reference, the decision-record entry reference and the page of rows.
3. State the invariant of the mapping in the document: one group gives one role per environment, the mapping version answers whole, and the version in force is the one whose valid-from is the latest not after the date asked.
4. State the change rule: the change writes a new dated version and never edits an applied version; the earlier rows stay readable with their valid-to; a version that fails a check writes nothing.
5. State the rights: Platform administration R for the two reads and C for the change, with an active role required on every call, and the 401 and 403 of the default deny rule.
6. Agree the error envelope and the message mapping for 401, 403, 404, 409, 422 and 503, with the business texts copied unchanged from the legacy story where the message already exists.
7. Declare the event `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with change kind `MAPPING` and its payload, and the decision-record type on the shared topic `rwb.decision-record.v1`; declare no third event name.
8. Declare the consumed parameters contract and the read-only ACE group view with their owners and the one-hop budget, and declare no operation of another service as provided.
9. Publish the contract tables of section 12 (nine sub-tables) and the contract fakes, then add the contract tests: schema validation, the version rule, the rights, the envelope, the owner declarations and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-AD001-APP and to the sign-in contract RWB-P4-E1022-CON and RWB-P4-E1022-APP, whose resolution reads the mapping.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A schema declares a person's name, an e-mail address or a group membership of an individual | The review fails and the property is removed; the rule is a lint item of the document | None | AC2 |
| X3 | A field of the mapping or the version has no source definition | The field is named by this document's own decision and the gap is carried | None | AC2 |
| X4 | The document declares a mapping that is edited in place, or a version with no valid-from | The review fails: a change is a dated version and an applied version is never rewritten | None | AC3 |
| X5 | The document declares an event name other than the two of the service, or a second access event name for a mapping change | The review fails and the event is declared under `rwb.access.AccessPolicyChanged.v1` with change kind `MAPPING` | None | AC4 |
| X6 | The document declares an operation or a table of another service as provided | The review fails; the parameters contract and the ACE view are documented as consumed | None | AC5 |
| X7 | An error response carries no `messageId`, or a `messageId` not in the agreed set | The contract test fails and the merge is blocked | None | AC6 |
| X8 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC7 |
| X9 | The parameters contract or the ACE view does not answer inside the 2 s budget | The call answers 503 for that read and the document declares the 503 | MSG-GEN-006 | AC5, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it reads the ownership map, the platform envelopes, the parameters contract of RWB-P3-E1042-CON and the ACE-view contract of RWB-P1-E1069-APP only |
| Negotiable | The field-level detail of the three schemas and the payload of the event are settled with the app story and the sign-in story; the base, the rights, the event name and the envelope are fixed by the target architecture and the Workbench |
| Valuable | Unblocks the app story and the sign-in story on Day 1 with a written answer to "which role does this group give on this date", and keeps the permission matrix, the reference data and the central ledger out of the mapping contract |
| Estimable | One document, three schemas, one error envelope with seven message IDs, one event declaration, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: The group-to-role mapping contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given a mapping is the "entra_group" of a role row of one environment in "rwb_access"
    Given the legacy example is the group "RWB-SIT-RW-CASEOWN" on the role "RW-CASEOWN" in SIT

  Scenario: AC1 The OpenAPI 3.1 document describes the three mapping operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares GET /admin/role-mappings, POST /admin/role-mappings and GET /admin/role-mapping-versions/{versionId} with the owner rwb-access
    Then the two reads declare Platform administration with the right R, and the change declares Platform administration with the right C
    Then every operation declares 401, 403, 404, 409, 422 and 503
    Then the change declares the Idempotency-Key header and the two reads declare none

  Scenario: AC2 The three schemas carry the group, the role, the version and the dates (new, D-RCV-60)
    Given the schemas RoleMapping, RoleMappingVersion and RoleMappingPage of the document
    Then RoleMapping carries entraGroup, roleCode, roleName, roleClass, defaultScope, environment, mappingVersion, validFrom, validTo and dataAsOf
    Then RoleMappingVersion carries mappingVersion, environment, validFrom, validTo, rowCount, authorReference, decisionRecordEntryRef and the rows
    Then RoleMappingPage carries items, page, size and total with a default of 50 and a maximum of 200
    Then the document states that one group gives one role per environment and that the mapping version answers whole
    Then no schema, no parameter and no example declares a person's name, an e-mail address, an identity number or the group membership of an individual
    Then the version label and the two dates are declared as fields of the mapping and of its version, because no physical column is specified for them in the source documents

  Scenario: AC3 A mapping change is a dated version and never an edit (new, D-RCV-60)
    Given the description of the change operation and of the two reads
    Then the change writes a mapping version with its valid-from date and its rows, and answers the version
    Then the document states that an applied version is never edited and that the rows of the earlier version stay readable with their valid-to
    Then the version read answers the effective dates of one version, and the mapping read answers the version whose valid-from is the latest not after the date asked
    Then the document states that a new mapping needs no deployment, no restart and no code change
    Then the document states that a version that fails a check writes no row and leaves the version in force unchanged

  Scenario: AC4 The mapping change is published as the access-policy event (new, D-RCV-60)
    Given the events section of the document
    Then rwb.access.AccessPolicyChanged.v1 is declared on the topic rwb.access.events.v1 with change kind MAPPING, the environment, the mapping version, the role codes touched, the counts of rows added and closed and the time
    Then rwb.decision-record.DecisionRecorded.v1 is declared on the shared topic rwb.decision-record.v1 for the entry of the change and of the refusal
    Then no other event name is declared for this capability, and no second name for a mapping change appears anywhere in the document
    Then no payload carries a group membership, a user reference or a personal field

  Scenario: AC5 The consumed reads are declared as consumed (new, D-RCV-60)
    Given the consumed section of the document
    Then GET /api/recovery/case/v1/admin/parameters is declared with the owner rwb-case and the parameters contract RWB-P3-E1042-CON
    Then the read-only ACE group view v_ace_iam_group is declared with the owner of RWB-P1-E1069-APP, its fields DF-ACE-301 to DF-ACE-304 and its data_as_of
    Then both are declared one hop, with the 2 s client budget and the 503 when the read does not answer in time
    Then no operation, table or list owned by another service is declared as provided, and the reference-data contract of rwb-case is not declared at all

  Scenario: AC6 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by any of the three operations
    Then the body carries the code, the message, the messageId, the traceId and the field list, with the problem media type
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 404 and 409 carry MSG-GEN-004, 422 carries MSG-GEN-001 or MSG-P1-002 and 503 carries MSG-P7-003 or MSG-GEN-006
    Then the message texts are the legacy texts where the message already exists, and the wording of legacy AC2 is not altered by this document

  Scenario: AC7 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the four contract fakes of section 12.8
    When a fake is compared with the document
    Then the mapping fake answers the three paths of 12.1: the mapping of SIT with the group RWB-SIT-RW-CASEOWN on the role RW-CASEOWN, the version in force with its dates, and the next version with a later valid-from
    Then the parameters fake answers the environment code SIT and one later environment code
    Then the ACE group fake answers the group with its source system and its data_as_of, and one group the view no longer holds
    Then the decision-record fake answers the entry append and the 503 with MSG-P7-003
    Then a contract test fails on any drift between a fake and the document, and no fake carries a name or an e-mail address
```

These seven criteria test the artefact only. No criterion restates a legacy acceptance criterion: the three legacy criteria of RWB-AD-001 are owned by RWB-P4-AD001-APP and are listed with their tests in section 16 as the cases this contract is the ground of, exactly as the brief of this key fixes.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path, table or event | DP-13; Architecture v5 slides 14 and 41 |
| BR2 | A consumed read is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | Events are named `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, the shared record type stays on `rwb.decision-record.v1`, and the envelope is CloudEvents 1.0 | Architecture v5 slides 14, 20 and 43; Template and Rules §R4 |
| BR4 | This capability publishes one event, `rwb.access.AccessPolicyChanged.v1`, with change kind `MAPPING`; `rwb.access.DoaLimitChanged.v1` belongs to the delegation table and no third name exists | Architecture v5 slides 14, 20 and 43; ASM-1448 |
| BR5 | The contract declares no table of another service: `lov_value`, `reference_row` and `reference_version` are P3's, `parameter_catalog` and `parameter_value` are P3's, `decision_log_entry` is P7's and `partner_user` is S9's | DP-01; ownership map |
| BR6 | A mapping change is a dated version and an applied version is never edited; the version in force is the one whose valid-from is the latest not after the date asked | Legacy RWB-AD-001 AC3; TSD P4 v3 T4 (LOV-VERSION-STATUS); ASM-1444 |
| BR7 | The mapping is `role.entra_group` of the environment, and the ACE view is the read-only reference of the group, not the Workbench mapping | TSD P4 v3 T3.1; R-PREC rule 6 over 7; ASM-1445 |
| BR8 | A mapping read and a version read need Platform administration R, and the change needs C; an active role is required on every call, and the default deny rule answers 401 and 403 | TSD P4 v3 T6.1 and API-P4-007; FSD P4 v3 VR-P4-001-1 and VR-P4-004-1 |
| BR9 | The environment code is read as a parameter and never declared as a constant or an enumerated list in the document | DP-06; ASM-1446 |
| BR10 | Error responses use one envelope and one message ID per condition, and the business texts are copied unchanged from the legacy story where the message exists | Architecture v5 slide 11; Template and Rules §R7.2 s14 |
| BR11 | No schema, parameter, example or fake declares a name, an e-mail address, an identity number or the group membership of an individual | REQ-ACA-005; guardrails |
| BR12 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | The three operations, the three schemas, the event and the consumed reads are described | The document validates and the contract tests pass | In review |
| In review | Consumer sign-off | RWB-P4-AD001-APP, RWB-P4-E1022-CON and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

A mapping version has its own states — in force, superseded, refused — and they are the app story's data states, not states of this document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document, the three schemas, the event declaration and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator and the audit representative | Review and sign off the rights, the version rule and the effective dates |
| Tech lead of the sign-in of RWB-P4-E1022 | Reviews the fields and the version rule the sign-in reads, because it is the consumer of the mapping |
| Tech lead of the parameters contract of rwb-case | Reviews the declared parameter read and its budget |
| Data steward | Confirms that no personal data property is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Mapping row | `entraGroup` (DF-REF-039, varchar(120), optional), `roleCode` (DF-REF-035), `roleName` (DF-REF-036), `roleClass` (DF-REF-037), `defaultScope` (DF-REF-038), `environment`, `mappingVersion`, `validFrom`, `validTo`, `dataAsOf` |
| Mapping version | `mappingVersion`, `environment`, `validFrom`, `validTo`, `rowCount`, `authorReference`, `decisionRecordEntryRef`, `rows[]` |
| Mapping page | `items[]` of the mapping row, `page`, `size` (default 50, maximum 200), `total` |
| Change request | `environment`, `mappingVersion`, `validFrom`, and the rows `entraGroup` and `roleCode`; the `Idempotency-Key` header |
| Group reference | `entraGroup`, `roleCode`, `sourceSystem`, `dataAsOf`, from the read-only view `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) |
| Environment | The code of this deployment, read as a parameter through the parameters contract of rwb-case; the parameter code and the codes beyond SIT are Not specified in the source documents (GAP-0788; ASM-1446) |
| Event payloads | IDs, codes, counts and times only; no group membership, no user reference and no personal field |
| Decision-record entry | The change entry and the refusal entry, written through the library of DP-03; their fields are the library's and are not redefined here |

Three values the sources do not fix are this baseline's decision and are carried as placeholders. The mapping version label and the two effective dates have no physical column in TSD P4 v3 T3.1, while legacy AC3 needs them — **Not specified in the source documents (GAP-0788; ASM-1444)**. The operation paths, their rights and their answer shapes have no row in the ownership map or in TSD P4 v3 appendix T-A — **Not specified in the source documents (GAP-0788; ASM-1447)**. The environment codes and the parameter that carries them are **Not specified in the source documents (GAP-0788; ASM-1446)**.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| GET | `/admin/role-mappings` | `RoleMappingPage`: query `entraGroup`, `roleCode`, `validOn`, `page`, `size` (default 50, max 200); the rows in force on `validOn` | Platform administration R |
| POST | `/admin/role-mappings` | `RoleMappingVersion` in, with the `Idempotency-Key` header; the written version out | Platform administration C |
| GET | `/admin/role-mapping-versions/{versionId}` | `RoleMappingVersion`: the effective dates, the row count, the author reference, the decision-record entry reference and the rows | Platform administration R |

Errors for all three: 401 no session or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 unknown version, role or group (MSG-GEN-004), 409 a version label that already exists or a repeated key answered differently (MSG-GEN-004), 422 a missing or invalid field (MSG-GEN-001) or a mapping that breaks the one-group-one-role rule (MSG-P1-002), 503 the record entry not written (MSG-P7-003) or the group reference not readable (MSG-GEN-006). The change is idempotent by `Idempotency-Key`; a same key returns the first answer and writes no second version. Major version 1 sits in the path (BR12).

The role catalogue `GET /admin/roles` (API-P4-007) and the session `GET /me/session` (API-P4-012) are the service's own operations of RWB-P4-E1019-APP and RWB-P4-E1037-CON; this document neither restates nor changes them.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case`, published by RWB-P3-E1042-CON (DP-06) | The environment code of the deployment; the parameter code is Not specified in the source documents (GAP-0788; ASM-1446) |

The ACE group reference is a read-only SQL read and not a REST call: `recovery.v_ace_iam_group` (DF-ACE-301 to DF-ACE-304), owner RWB-P1-E1069-APP (DP-05), one hop in the same database, declared with its `data_as_of` and its 503. Nothing else is consumed: the reference-data contract of rwb-case is not declared, because this capability reads no list of values.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access` | Change kind `MAPPING`, the environment, the mapping version, the role codes touched, the counts of rows added and closed and the time |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code (`AC-CHG` for a change, `AC-DENY` for a refusal), the environment, the mapping version and the time |

Both messages use the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype. No message carries a group membership, a user reference, a name, an e-mail address or an identity number. `rwb.access.DoaLimitChanged.v1` is not declared for this capability, and no second name exists for a mapping change (BR4, ASM-1448).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this capability adds no subscription.

#### 12.5 Workflows and activities

None. The three operations are synchronous REST answers in the caller's thread with no workflow, no activity and no signal. The six-monthly access review Schedule (JOB-18) is RWB-P4-AD008-CON's.

#### 12.6 Schedules

None. Nothing about a mapping runs on a clock: the valid-from date is a row value the read resolves.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role` | P4 (`rwb_access`) | `entra_group` (DF-REF-039) is the mapping; the role code, name, class and scope travel with it; the version and date columns are this key's own decision (GAP-0788; ASM-1444) |
| `permission` | P4 (`rwb_access`) | The Platform administration letters R and C of the caller (DF-REF-040 to DF-REF-044); read only |
| `v_ace_iam_group` | ACE database, read-only view, owner RWB-P1-E1069-APP | The group reference: `entra_group`, `role_code`, `source_system`, `data_as_of`; never written |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | Appear nowhere in the contract; the parameters read is a consumed operation, not a table (DP-01, DP-06) |
| `decision_log_entry` | P7 (`rwb_decision`) | Appears nowhere; the local entry is the library's and the central ledger is P7's |
| `partner_user` | S9 (`rwb_partner`) | Appears nowhere; the ownership map gives partner users to S9 |

No foreign key crosses a schema, and the contract names no table outside `rwb_access` except the read-only ACE view it consumes.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb-access` role-mapping WireMock | The three paths of 12.1: the mapping of SIT with the group `RWB-SIT-RW-CASEOWN` on the role `RW-CASEOWN`, the version in force with its dates, the next version with a later valid-from, the stored answer for a repeated `Idempotency-Key`, 409 for an existing version label, 422 with MSG-GEN-001 and MSG-P1-002, 403 with MSG-P4-002 and 503 with MSG-P7-003 | App story, contract tests, wave 4 harness |
| Parameters fake (RWB-P3-E1042-CON) | The environment code `SIT` and one later environment code | App story, contract tests |
| ACE group fake | The group `RWB-SIT-RW-CASEOWN` with its source system and a `data_as_of`, and one group the view no longer holds | App story, contract tests |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 1 consumed | The mapping read, the mapping change and the version read provided; the parameters read consumed; one hop, 2 s timeout; plus one read-only SQL read of the ACE view |
| Kafka | 2 published, 0 consumed | `rwb.access.AccessPolicyChanged.v1` and `rwb.decision-record.DecisionRecorded.v1` |
| Temporal | None | No workflow, activity or Schedule in this contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-role-mapping-v1.yaml` (OpenAPI 3.1) with the three operations and the shared components, the three schemas, the `contract/error-envelope.yaml` with the agreed message IDs, the event declaration for `rwb.access.AccessPolicyChanged.v1` with its change kind, the parameters stub with its owner, the ACE-view stub with its `data_as_of`, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

A contract story adds no build dependency of its own: each DP above is **referred to; the consuming story carries the dependency**, and that story is RWB-P4-AD001-APP, whose H row carries RWB-PLT-E1027-CON, RWB-PLT-E1042-CON and RWB-PLT-N001-CON and whose C row carries RWB-P3-E1042-CON. DP-03 is contracted as the entry the document declares on `rwb.decision-record.v1`; DP-05 as the statement that the group reference is read read-only through the P1 contract and never through a `public` table; DP-06 as the consumed parameters read that answers the environment code; DP-13 as the base of the document; DP-19 as the composite route that serves SCR-43.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The three operations and the three schemas of section 11, with the page, the version and the dates.
3. The invariant and the change rule in the description of the three operations: one group one role per environment, a dated version, an applied version never edited, the version in force on the date asked (BR6, BR7).
4. The rights of the two reads and of the change, and the 401 and 403 of the default deny rule.
5. The error envelope and the message-ID mapping, with the legacy texts copied unchanged and the wording note of section 14.
6. The event declaration and the decision-record type, with the change kind and the payload, and the statement that no third name exists.
7. The consumed parameters read and the read-only ACE view with their owners, the one-hop rule, the 2 s budget and the 503.
8. The four fakes and the stub fixtures of section 12.8.
9. The seven contract tests; a drift between a fake and the document fails the build.
10. Baseline tag and the consumer sign-off note of the app story and of the sign-in story.

**Feature switch.** The contract carries no switch. The three operations are operations of the service; the change is a data change guarded by the C letter, and nothing about a mapping is behind a flag.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD001-APP | The three provided operations, the three schemas, the version rule, the event declaration and the four fakes |
| RWB-P4-E1022-CON and RWB-P4-E1022-APP, the sign-in | The mapping row, the version in force on the date asked and the effective dates it resolves at sign-in |
| The wave 4 harness | The fakes of 12.8 and the parameters and ACE-view stubs |

The deprecation window of a published field and the retention of the contract fakes are Not specified in the source documents (GAP-0788; ASM-1447).

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the four fakes answer every consumed and every provided path, and the app story and the sign-in story have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, no Workbench role, or a sign-in that resolves no role from the mapping | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller without Platform administration R for a read, or without C for the change | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is empty, the group is too long, the role code is unknown or the valid-from is in the past | Enter {field}. |
| MSG-P1-002 | The same group maps to a second role, or the same role to a second group, in one version | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-004 | The version label exists, or the version, role or group asked for does not exist | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The ACE group reference cannot be read | The reference data is not available. Try again later. |
| MSG-P7-003 | The decision-record entry could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text, taken from the legacy story where the message already existed. The one legacy criterion this document must not reword is AC2 of RWB-AD-001, which RWB-P4-AD001-APP copies word for word together with the note on its wording; this document fixes only the message ID and the refusal it names.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | List | The mapping read with the rows in force, the version and the dates, and the `dataAsOf` of the group reference |
| SCR-43 Roles and access | Change | The change request and the field-level 422 answers of the checks |
| SCR-43 Roles and access | Changed | The written version with its dates, its row count and the decision-record entry reference |
| SCR-43 Roles and access | Access log | The entries of the changes and of the refusals, read through the access-log operation of RWB-P4-AD007-APP on the same composite route |
| SCR-43 Roles and access | Refused | The 403 with MSG-P4-002 and no row, and the 401 with MSG-P4-001 |
| SCR-43 Roles and access | Not available | The 503 with MSG-GEN-006 or MSG-P7-003 |

The screens are served by the gateway-bff composite route (DP-19), which calls the mapping read and the access-log read in parallel, one hop each, and merges the answers. The composite route specification, the screen field list and the column order are Not specified in the source documents (GAP-0788; ASM-1447); the document fixes the mapping side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-001-01 | AC1 | Contract | Legacy test "Group gives the role" on the contract side: the group `RWB-SIT-RW-CASEOWN` and the role `RW-CASEOWN` are the values of the fixtures; the mapping read and the version read answer them with the version in force, so the sign-in of RWB-P4-E1022-APP can hold the role; the behaviour itself is tested there at End to end |
| TC-AD-001-02 | AC2 | Contract | Legacy test "Unmapped group" on the contract side: a group with no mapping row is answered as absent (404 with MSG-GEN-004) and no row is invented; MSG-P4-001 is declared on the sign-in path the document references |
| TC-AD-001-03 | AC3 | Contract | Legacy test "Mapping change" on the contract side: the change operation writes a version with a valid-from and never edits an applied version; the mapping read answers the version in force on the date asked, and a version with a later valid-from answers only from its date |
| TC-AD-001-04 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": a caller with no Platform administration letter is declared refused on all three operations, and the document declares the 403 with MSG-P4-002 and the refusal entry |
| TC-AD-001-05 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the document declares the 503 with MSG-P7-003, and the fake answers it, so no consumer treats a refused change as written |

The five legacy test cases are kept with their IDs and their legacy Covers values, and the legacy test name is written in the Data column. The Level column follows Template and Rules §R7.2: the two reads, the change and the version rule are tested against the artefact at Contract, the legacy Access row stays Component, and the legacy Resilience row of Principle 5 stays NFR. The behaviour of each case in the running service is RWB-P4-AD001-APP's at End to end, and the full test with its Given, When and Then is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD001-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in the contract: the group names are DL40 data rows, the environment is a parameter, and the version labels and dates are rows; the document fixes names and types only.
- No personal data in a schema, an example or a fake: a mapping is a group name and a role code, and a name or an e-mail address in the document fails the review (BR11).
- The contract names only `rwb-access` tables, the read-only ACE view it consumes and operations owned by `rwb-access` or declared as consumed (DP-01, BR5).
- One REST base, one topic and one event name for the capability, and the shared record type on `rwb.decision-record.v1`; a document that names another service's base, topic or event fails the review (DP-13, BR3, BR4).
- A mapping change is a dated version and an applied version is never edited; the document declares the version rule, so no consumer reads "the latest row" as the truth (BR6).
- The ACE view is declared read-only with its `data_as_of`, so no consumer mistakes the bank IAM's reference for the Workbench mapping (BR7).
- Every example and every fake is synthetic; no production group, person or entitlement is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

No requirement ID is recorded for legacy RWB-AD-001 in TSD P4 v3 T8, and the Work Package carries the requirement list of this key as empty; the key serves the features FEAT-ACA-03 (hold roles as data) and FEAT-ADM-01 (run the full administration screens) of the FSD P4 v3, and the epic 8 requirement REQ-ACA-013 is recorded in that specification as written one epic ahead with its test with the story.

| Feature | Contract element | Test cases |
|---|---|---|
| FEAT-ACA-03, hold roles as data | The mapping row, the version and the effective dates of 12.1 and 12.7, and the change that writes a dated version | TC-AD-001-01, TC-AD-001-03 |
| FEAT-ADM-01, the full administration screens | The three operations and the SCR-43 states they feed through the composite route | TC-AD-001-04 |
| The default deny rule and the recorded refusal | The 403 and the 401 of 12.1 and the decision-record type of 12.3 | TC-AD-001-02, TC-AD-001-04 |
| The record-before-change rule | The 503 with MSG-P7-003 and the entry reference of the written version | TC-AD-001-05 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy AC1, AC2 and AC3 | The behaviour of RWB-P4-AD001-APP; this contract carries the elements they are tested against, and section 16 keeps their test cases |
| The group `RWB-SIT-RW-CASEOWN`, the role `RW-CASEOWN`, the environment SIT and the valid-from rule | Sections 3, 7, 11 |
| The Data table: `role` DF-REF-034 to DF-REF-039 and `v_ace_iam_group` DF-ACE-301 to DF-ACE-304 | Sections 11, 12.7 |
| The permission check Platform administration and the roles that hold it | Section 12.1, section 8 (BR8) |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P1-002, MSG-GEN-004, MSG-GEN-006, MSG-P7-003 | Section 14, exception paths |
| Screen SCR-43 Roles and access | Section 15 |
| The decision DL40 and the final group names | Sections 3, 7 |
| Legacy test cases TC-AD-001-01 to TC-AD-001-05 | Section 16 |

### 19. Out of scope

- The implementation of the three operations, the migration, the checks, the group reader, the record entry and the event: RWB-P4-AD001-APP.
- The sign-in, the group claim and the resolution of a person's roles from the mapping: RWB-P4-E1022-CON and RWB-P4-E1022-APP. This contract is what that story reads, and it declares no session field.
- The permission matrix, the masking rows and the role conflicts: RWB-P4-E1037-CON, RWB-P4-E1037-APP and RWB-P4-E1019-APP.
- The matrix and masking loads with their approval and rollback: RWB-P4-AD002-APP, RWB-P4-AD004-APP and RWB-P4-AD010-APP.
- The access review list and its Schedule (JOB-18): RWB-P4-AD008-APP and RWB-P4-AD008-CON; the access-log read is RWB-P4-AD007-CON's.
- The reference data and the parameter values of the estate: P3 rwb-case under DP-06 and its reference-data contract; this contract declares one consumed parameters read and no table of either of either.
- The central decision ledger and its query: P7 rwb-decision; the local entry is the library's.
- `partner_user`: S9 rwb-partner.
- The bank IAM's group administration and the naming decision DL40: Entra ID and the bank IAM (INT-21).
- The deployment of the capability: the Helm values, the topic creation, the dashboards and the runbook.
- The integration harness and its evidence, and the `-ITG` copies of the test cases: RWB-ITG-AD001-ITG.
- The field-level completeness of the three schemas beyond what section 11 fixes (GAP-0788; ASM-1447).
