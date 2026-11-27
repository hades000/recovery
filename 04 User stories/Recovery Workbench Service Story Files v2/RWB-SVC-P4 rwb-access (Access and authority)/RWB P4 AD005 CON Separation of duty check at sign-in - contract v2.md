# RWB-P4-AD005-CON Separation of duty check at sign-in

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-005 for rwb-access — the contract of the separation-of-duty table as dated data, the check the sign-in calls, the conflict-table and version reads, the refusal rule, the `conflictVersion` field of the session read and the decision-record type. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-AD005-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-AD005-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-AD005-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (major 1 in the path, BR14); the minor version is Not specified in the source documents (DOR-RWB-P4-AD005-CON-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner of rwb-access**, I want **the published contract baseline of the separation-of-duty rule: an OpenAPI 3.1 document for the check that the sign-in calls, the conflict-table read and the conflict-version read, the `RoleConflict`, `RoleConflictVersion`, `SodCheckRequest` and `SodCheckResult` schemas, the statement that a resolved role set holding both halves of a pair refuses the whole session and records the refusal, the `conflictVersion` field the session read carries, the decision-record type with its reason code, one RFC 9457 error envelope with its message IDs, the consumed parameters read and the read-only ACE group view with their owner and one-hop budget, the contract tables of section 12 and the contract fakes**, so that **the app story builds on Day 1 against a fixed, testable contract, and the sign-in of RWB-P4-E1022-APP learns exactly what to ask, what a refusal looks like and which version of the rule it was checked against**.

The deliverable is the rule **as data plus one call**: the check, the read of the pairs of a version, the read of one version with its effective dates, the refusal rule and the field the session answers. What a role may do is not contracted here — the permission matrix is RWB-P4-E1037-CON's — and how the sign-in resolves a person's groups into role codes is RWB-P4-E1022-CON's.

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith the separation-of-duty table was read in the same transaction as the session and the refusal was a line of code in the resolver; nobody outside the team could say which pairs were in force, which message a refused person saw or what was recorded. In the target the check is one published operation of rwb-access and the pairs are rows of `rwb_access` with a conflict version and effective dates, so the answer the sign-in needs — may this set of role codes hold together on this date — must be written down once, with its fields, its negative answer, its record and its version.

The split of this legacy key is fixed and this contract is the rule half of it. **RWB-P4-E1022-CON and RWB-P4-E1022-APP own the sign-in, the token, the group claim and the resolution of a person's roles; this story owns the rule, the version in force, the refusal of the whole session, the refusal record and the `conflictVersion` the session answers.** The sign-in story calls this contract between the resolution and the session answer, and the two meet at one operation, which is what lets each be built and tested against the other's fake from Day 1.

Two consequences shape the document. The first is that the refusal is total and it is written down: a session is refused whole and never in part, the answer names the two role codes and the conflict version, and the same refusal becomes one decision-record entry with reason `ROLE_CONFLICT`, so the security administrator acts on a record and not on a rumour. The second is that the version is part of the answer: a session states the conflict version it was checked against, because a pair that was in force at 09:00 may not be in force at 17:00 and the audit must be able to say which rule governed one sign-in.

The document also has to be honest about what does not exist. The criterion requires an incident to the security administrator and the functional specification requires a refusal event; no source names an incident queue, an incident operation or a target service, and Architecture v5 slide 14 gives rwb-access no such event, so the refusal record is the channel and no queue, event name or operation is invented for it (GAP-0796; ASM-1479, ASM-1482).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-E1027-CON is published: the decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), whose entry is the refusal record this document declares. The dependency is carried by the app story, RWB-P4-AD005-APP (ASM-1486).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters client library and the parameters contract of rwb-case (DP-06), through which the environment code of the deployment is read. The dependencies are carried by the app story (ASM-1485).
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that serves SCR-43 and merges the conflict-table read with the access-log read of RWB-P4-AD007-APP. The dependency is carried by the app story.
- The ACE view `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) is granted and contracted by RWB-P1-E1069-APP (DP-05); this document declares it as a read-only consumed read with its `data_as_of`.
- `role_conflict` exists with its seven fields (DF-REF-205 to DF-REF-211) in TSD P4 v3 T3.1, including `conflict_version`, `valid_from` and `valid_to`, so this key needs no invented column, unlike the mapping of RWB-P4-AD001-CON.
- The check operation has no row in the ownership map and none in TSD P4 v3 appendix T-A, where the P4 inventory holds `GET /admin/roles` (API-P4-007) and `GET /me/session` (API-P4-012) and no separation-of-duty path: the path, the request and the answer are this document's own decision on the base of §R4 and DP-13, under the operation Architecture v5 slide 14 names as `POST /authorise` — **Not specified in the source documents (GAP-0796; ASM-1478)**.
- The two administrative reads of the pairs have no row in the ownership map either; they sit on the `/admin` family TSD P4 v3 gives this service and take the Platform administration R letter of TSD P4 v3 T6.1 — **Not specified in the source documents (GAP-0796; ASM-1481)**.
- The session read `GET /me/session` (API-P4-012) belongs to RWB-P4-E1037-CON; this document adds one field to that answer and restates no operation (ASM-1480).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7), and it holds in Contract group CG-W4 because the business epic EP08 is wave 4 in the W-MAP (§R5.6).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three separation-of-duty operations under the base `/api/recovery/access/v1`, with the shared components the `rwb-access` operations use.
2. Fix the check operation `POST /authorise/separation-of-duty`: the request is the resolved role codes, the subject reference and the time of the sign-in; the answer is `ALLOWED` with the conflict version applied, or `REFUSED` with the two role codes, the conflict version and the reason of the pair.
3. Fix the rule of the answer: the version in force is the one whose `valid_from` is the latest not after the date of the sign-in, one version answers whole, a pair is read both ways, and the whole set is refused and never a part of it.
4. Fix the refusal statement: a refused session answers no role, no scope and no token, the sign-in answers the person MSG-P4-006 naming both role codes, and the refusal is one decision-record entry with reason `ROLE_CONFLICT` addressed to the security administrator.
5. Draft the schemas `RoleConflict` (the seven dictionary fields), `RoleConflictVersion` (the version with its effective dates, its row count, its author reference and the reference of the decision-record entry of its load), `SodCheckRequest` and `SodCheckResult`.
6. Fix the two administrative reads: the pairs in force on a date asked, and one version by its label, both with the Platform administration R letter and the 401 and 403 of the default deny rule.
7. Declare the `conflictVersion` field the session read of RWB-P4-E1037-CON carries, name API-P4-012 as the operation, and state that this document restates no operation of that contract.
8. Declare the record type `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` with decision code `AC-DENY` and reason code `ROLE_CONFLICT`, and declare no access event and no incident operation for the refusal.
9. Agree the error envelope and the message mapping for 401, 403, 404, 409, 422 and 503, with the business texts copied unchanged from the legacy story where the message already exists and the text of MSG-P4-006 left open.
10. Declare the consumed parameters read and the read-only ACE group view with their owners and the one-hop budget, declare no operation of another service as provided, and carry the absence of the incident channel and of the load path as the open points of this key.
11. Publish the contract tables of section 12 (nine sub-tables) and the contract fakes, then add the contract tests: schema validation, the version rule, the refusal rule, the rights, the envelope, the owner declarations and the drift between a fake and the document.
12. Tag the baseline and hand it to RWB-P4-AD005-APP and to the sign-in of RWB-P4-E1022-CON and RWB-P4-E1022-APP, which calls the check.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | The document publishes a separation-of-duty path other than the three of 12.1, or an incident operation nobody owns | The review fails; the three operations are the document's and the incident is not an operation | None | AC1, AC5 |
| X3 | A schema declares a person's name, an e-mail address, a group membership of an individual or a case fact | The review fails and the property is removed; the rule is a lint item of the document | None | AC2 |
| X4 | The check answer declares a partial refusal, or a refusal with one role code only | The review fails: the whole set is refused and both role codes are named | None | AC3 |
| X5 | The document states a version rule other than the valid-from rule, or lets two versions answer at once | The review fails; the version in force is the one whose `valid_from` is the latest not after the date of the sign-in | None | AC3 |
| X6 | The document restates `GET /me/session` or declares a second session operation, or names a session field other than `conflictVersion` | The review fails; the session read is RWB-P4-E1037-CON's and this document adds one field | None | AC4 |
| X7 | The document declares an access event or a second name for the refusal, or a second topic | The review fails; the refusal is the decision record and no access event exists for it | None | AC5 |
| X8 | The document declares an operation or a table of another service as provided | The review fails; the parameters contract and the ACE view are documented as consumed | None | AC6 |
| X9 | An error response carries no `messageId`, or a `messageId` not in the agreed set | The contract test fails and the merge is blocked | None | AC7 |
| X10 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC8 |
| X11 | The parameters contract or the ACE view does not answer inside the 2 s budget | The call answers 503 for that read and the document declares the 503 | MSG-GEN-006 | AC6, AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; it reads the ownership map, the platform envelopes, the parameters contract of RWB-P3-E1042-CON, the ACE-view contract of RWB-P1-E1069-APP and the session contract of RWB-P4-E1037-CON only |
| Negotiable | The field-level detail of the four schemas and the shape of the check answer are settled with the app story and the sign-in story; the base, the rights, the reason code and the envelope are fixed by the target architecture and this revision |
| Valuable | Unblocks the app story and the sign-in story on Day 1 with a written answer to "may these role codes hold together on this date, and what does a refusal record", and keeps the permission matrix, the role catalogue and the central ledger out of this contract |
| Estimable | One document, three operations, four schemas, one error envelope with eight message IDs, one record declaration, nine contract tables, four fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: The separation-of-duty contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given a pair is a "role_conflict" row of one conflict version in "rwb_access"
    Given the check is one operation of "rwb-access" on the base "/api/recovery/access/v1"

  Scenario: AC1 The document describes the check and the two reads (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /authorise/separation-of-duty, GET /admin/role-conflicts and GET /admin/role-conflict-versions/{versionId} with the owner rwb-access
    Then the check declares no capability letter and requires a subject reference, and the two reads declare Platform administration with the right R
    Then every operation declares 401, 403, 404, 422 and 503, and the two reads declare 409
    Then the document declares no incident operation, no incident queue and no session operation of its own

  Scenario: AC2 The four schemas carry the pair, the version and the check (new, D-RCV-60)
    Given the schemas RoleConflict, RoleConflictVersion, SodCheckRequest and SodCheckResult of the document
    When the four schemas are read from the document
    Then RoleConflict carries id, roleCode, conflictsWith, reason, conflictVersion, validFrom and validTo as DF-REF-205 to DF-REF-211
    Then RoleConflictVersion carries conflictVersion, validFrom, validTo, rowCount, authorReference, decisionRecordEntryRef and the rows
    Then SodCheckRequest carries the resolved role codes, the subject reference and the time of the sign-in
    Then SodCheckResult carries the decision ALLOWED or REFUSED, the conflictVersion applied and, on a refusal, roleCode, conflictsWith and reason
    Then no schema, no parameter and no example declares a person's name, an e-mail address, an identity number, a group membership or a case fact

  Scenario: AC3 A refused set refuses the whole session and the refusal is recorded (new, D-RCV-60)
    Given the description of the check operation
    When a sign-in is checked against a role set
    Then the document states that the version in force is the one whose validFrom is the latest not after the date of the sign-in, and that one version answers whole
    Then it states that a pair is read in both orders and that a set holding both halves is REFUSED
    Then a refused answer names roleCode, conflictsWith, conflictVersion and reason, and carries no role list, no scope and no token
    Then the document states that the refusal is one decision-record entry with decision code AC-DENY and reason code ROLE_CONFLICT, addressed to the security administrator
    Then the document states that where the entry cannot be written the session is not answered, and that no pair, reason or version is a constant in code

  Scenario: AC4 The session read carries the conflict version it was checked against (new, D-RCV-60)
    Given the session section of the document
    When the session answer of the document is read
    Then GET /me/session (API-P4-012) is named as the operation of RWB-P4-E1037-CON and is not restated
    Then the document declares exactly one field it adds to that answer: conflictVersion
    Then the document states that a session keeps the conflictVersion it was checked against until it ends
    Then no other field of the session answer is declared, removed or retyped by this document

  Scenario: AC5 The refusal is one record and no new event (new, D-RCV-60)
    Given the events section of the document
    When a sign-in is refused and the events of the document are read
    Then rwb.decision.DecisionRecorded.v1 is declared on the shared topic rwb.decision-record.v1 with decision code AC-DENY and reason code ROLE_CONFLICT
    Then no access event is declared for the refusal, and no second name and no second topic appear anywhere in the document
    Then the loading of a new conflict version is declared as the load path of RWB-P4-E1037-CON and not as an operation of this document
    Then no payload carries a group membership, a user reference, a name or a case fact

  Scenario: AC6 The consumed reads are declared as consumed (new, D-RCV-60)
    Given the consumed section of the document
    When the consumed reads of the document are checked
    Then GET /api/recovery/case/v1/admin/parameters is declared with the owner rwb-case and the parameters contract RWB-P3-E1042-CON, for the environment code only
    Then the read-only ACE group view v_ace_iam_group is declared with the owner of RWB-P1-E1069-APP, its fields DF-ACE-301 to DF-ACE-304 and its data_as_of
    Then both are declared one hop, with the 2 s client budget and the 503 when the read does not answer in time
    Then no operation, table or list owned by another service is declared as provided, and no rule package table appears in the document

  Scenario: AC7 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 404, 409, 422 or 503 response is produced by any of the three operations
    Then the body carries the code, the message, the messageId, the traceId and the field list, with the problem media type
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 404 carries MSG-P4-003 or MSG-GEN-004, 409 carries MSG-GEN-004, 422 carries MSG-GEN-001 and 503 carries MSG-P7-003 or MSG-GEN-006
    Then MSG-P4-006 is declared for the refusal of a session and its text is left open, and the message texts are the legacy texts where the message already exists

  Scenario: AC8 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the four contract fakes of section 12.8
    When a fake is compared with the document
    Then the separation-of-duty fake answers the three paths of 12.1: a version in force with the pair RW-WRITEOFF and RW-WOCOMM, a set with one of the two, and a next version with a later validFrom
    Then the sign-in fake answers a resolved role set and no session
    Then the parameters fake answers the environment code of the deployment
    Then the ACE group fake answers the group of each role code with its data_as_of, and the decision-record fake answers the entry append and the 503 with MSG-P7-003
    Then a contract test fails on any drift between a fake and the document, and no fake carries a name or an e-mail address

  Scenario: AC9 Each business rule of section 8 is carried by the document or by a guardrail (new, D-RCV-60)
    Given the business rules of section 8 from BR1 to BR14
    When the document is checked against each rule
    Then BR1, BR2, BR3 and BR14 hold for every operation, schema and event of the document
    Then BR4, BR5, BR6, BR7, BR8 and BR9 hold for the refusal, the decision record, the pairs and the version rule
    Then BR10, BR11, BR12 and BR13 hold for the check, the reads, the environment code, the personal data rule and the session field

  Scenario: AC10 A replay of a write with the same idempotency key is answered as the document states (new, D-RCV-60)
    Given a write operation of the document that takes an idempotency key
    When a write is replayed with the same idempotency key
    Then the document states the answer to the replay of the write
    Then the answer to the replay is Not specified in the source documents (NEWAC-RWB-P4-AD005-CON-AC10)
```

These ten criteria test the artefact only. No criterion restates a legacy acceptance criterion: the two legacy criteria of RWB-AD-005 are owned by RWB-P4-AD005-APP and are listed with their tests in section 16 as the cases this contract is the ground of. Every value they use is the legacy or the functional-specification value unchanged: the role codes `RW-WRITEOFF` and `RW-WOCOMM`, the message IDs, and the conflict version fields DF-REF-205 to DF-REF-211.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; the document never declares another service's path, table or event | DP-13; Architecture v5 slides 14 and 41 |
| BR2 | A consumed read is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 |
| BR3 | Events are named `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, the shared record type stays on `rwb.decision-record.v1`, and the envelope is CloudEvents 1.0 | Architecture v5 slides 14, 20 and 43; Template and Rules §R4 |
| BR4 | This capability publishes no access event for a refusal and declares no incident operation: the refusal is one decision-record entry with reason `ROLE_CONFLICT`, and the access-policy event belongs to the load path of RWB-P4-E1037-CON | Architecture v5 slide 14; ASM-1479, ASM-1482 |
| BR5 | The contract declares no table of another service: `lov_value`, `reference_row` and `reference_version` are P3's, `parameter_catalog` and `parameter_value` are P3's, `decision_log_entry` and the rule package tables are P7's, and `partner_user` is S9's | DP-01; ownership map |
| BR6 | A pair is two role codes of one conflict version, read in both orders; a pair that forbids one role with any business role is one row per business role | TSD P4 v3 T3.1 (DF-REF-206, DF-REF-207); FSD P4 v3 AC-EXC-P4-001-03; ASM-1490 |
| BR7 | The version in force is the one whose `valid_from` is the latest not after the date of the sign-in, one version answers whole, and a session keeps the version it was checked against until it ends | Legacy RWB-AD-005 AC2; TSD P4 v3 T3.2 (LOV-VERSION-STATUS); ASM-1484 |
| BR8 | A resolved set holding both halves of a pair is refused whole: the answer carries no role list, no scope and no token, and the person receives MSG-P4-006 naming both role codes | Legacy RWB-AD-005 AC1; FSD P4 v3 AC-EXC-P4-001-03 |
| BR9 | The refusal is one decision-record entry through the library of DP-03 with decision code `AC-DENY` and reason code `ROLE_CONFLICT`, and where it cannot be written the session is not answered | DP-03; FSD P4 v3 AC-EXC-P4-001-03 and AC-EXC-P4-001-06; MSG-P7-003 |
| BR10 | The check is called by the sign-in of this service with a subject reference and declares no capability letter; the two administrative reads need Platform administration R, and the default deny rule answers 401 and 403 | TSD P4 v3 T6.1, API-P4-007 and API-P4-012; FSD P4 v3 VR-P4-004-1; ASM-1481 |
| BR11 | The environment code is read as a parameter and never declared as a constant or an enumerated list in the document | DP-06; ASM-1485 |
| BR12 | No schema, parameter, example or fake declares a name, an e-mail address, an identity number, a group membership of an individual or a case fact | REQ-ACA-005; guardrails |
| BR13 | The `conflictVersion` field is the only element this document adds to the session read of RWB-P4-E1037-CON, and that operation is named and not restated | TSD P4 v3 API-P4-012; ASM-1480 |
| BR14 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | The three operations, the four schemas, the refusal rule and the record type are described | The document validates and the contract tests pass | In review |
| In review | Consumer sign-off | RWB-P4-AD005-APP, RWB-P4-E1022-CON and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |

A conflict version has its own states — loaded, approved, in force, superseded, refused — and they are the data states of the load path of RWB-P4-E1037-CON and of the app story, not states of this document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of `rwb-access` | Owns the document, the four schemas, the record declaration and the fakes; tags the baseline |
| Solution architect | Approves a breaking change and a new major version |
| Security administrator and the audit representative | Review and sign off the refusal rule, the reason code, the version rule and the addressee of the refusal |
| Tech lead of the sign-in of RWB-P4-E1022 | Reviews the check request, the refusal answer and the `conflictVersion` field, because it calls the check and answers the person |
| Tech lead of the permission matrix of RWB-P4-E1037 | Reviews the one field this document adds to the session answer and confirms that no operation of that contract is restated |
| Tech lead of the parameters contract of rwb-case | Reviews the declared parameter read and its budget |
| Data steward | Confirms that no personal data property is declared in a schema, an example or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Pair | `id` (DF-REF-205), `roleCode` (DF-REF-206, LOV-ROLE), `conflictsWith` (DF-REF-207, varchar(30)), `reason` (DF-REF-208, varchar(200)), `conflictVersion` (DF-REF-209, varchar(20)), `validFrom` (DF-REF-210, date), `validTo` (DF-REF-211, date, optional) | DF-REF-205 to DF-REF-211 |
| Conflict version | `conflictVersion`, `validFrom`, `validTo`, `rowCount`, `authorReference`, `decisionRecordEntryRef`, `rows[]` | Not specified in the source documents (DOR-RWB-P4-AD005-CON-7) |
| Check request | The resolved role codes, the subject reference and the time of the sign-in; no name, no group and no case | Not specified in the source documents (DOR-RWB-P4-AD005-CON-7) |
| Check answer | The decision `ALLOWED` or `REFUSED`, the `conflictVersion` applied and, on a refusal, `roleCode`, `conflictsWith` and `reason` | Not specified in the source documents (DOR-RWB-P4-AD005-CON-7) |
| Session field | `conflictVersion`, added to the answer of `GET /me/session` (API-P4-012), which is declared by RWB-P4-E1037-CON (ASM-1480) | Not specified in the source documents (DOR-RWB-P4-AD005-CON-7) |
| Environment | The code of this deployment, read as a parameter through the parameters contract of rwb-case; the parameter code is Not specified in the source documents (GAP-0796; ASM-1485) | Not specified in the source documents (DOR-RWB-P4-AD005-CON-7) |
| Record payload | Entry id, decision code `AC-DENY`, reason code `ROLE_CONFLICT`, the two role codes, the conflict version, the environment and the time; no name, no e-mail address and no group membership | Not specified in the source documents (DOR-RWB-P4-AD005-CON-7) |
| Refused person | The subject reference and the pair, carried by the record; MSG-P4-006 to the person | Not specified in the source documents (DOR-RWB-P4-AD005-CON-7) |

Three values the sources do not fix are decided by this revision (GAP-0796). The path and the payloads of the check are this contract's decision, not a source value: POST /authorise/separation-of-duty on /api/recovery/access/v1 with the request and answer shapes of the table above (ASM-1478). The field name `conflictVersion` of the session answer is this document's choice, because API-P4-012 names "conflict versions" in its purpose and declares no field (ASM-1480). The text of MSG-P4-006 is declared by no source — **Not specified in the source documents (GAP-0796; ASM-1479)**.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-access` (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/authorise/separation-of-duty` | `SodCheckRequest` in — the resolved role codes, the subject reference and the time; `SodCheckResult` out — `ALLOWED` with the conflict version, or `REFUSED` with `roleCode`, `conflictsWith`, `conflictVersion` and `reason` | The sign-in of this service with a subject reference; no capability letter |
| GET | `/admin/role-conflicts` | The pairs in force on the date asked: `roleCode`, `conflictsWith`, `reason`, `conflictVersion`, `validFrom`, `validTo`. Query `roleCode`, `validOn`, `conflictVersion`, `page`, `size` (default 50, max 200) | Platform administration R |
| GET | `/admin/role-conflict-versions/{versionId}` | `RoleConflictVersion`: the effective dates, the row count, the author reference, the decision-record entry reference and the rows | Platform administration R |

Errors for all three: 401 no subject or no Workbench role (MSG-P4-001), 403 no right (MSG-P4-002), 404 a path this service does not publish or an unknown version, role or pair (MSG-P4-003, MSG-GEN-004), 409 a version label that does not exist or two versions in force on the date asked (MSG-GEN-004), 422 a missing or invalid field (MSG-GEN-001), 503 the record entry not written (MSG-P7-003) or the group reference not readable (MSG-GEN-006). No operation of 12.1 writes a row: the check answers, and the only write of the call is the refusal entry of the library. Major version 1 sits in the path (BR14). The check declares no idempotency key: the call answers, and its only write is the refusal entry, which carries its own entry id (section 12.3).

The session read `GET /me/session` (API-P4-012) belongs to RWB-P4-E1037-CON and appears in this document as one declared field of its answer, `conflictVersion` (AC4); the contract declares no second session operation and no other session field.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case`, published by RWB-P3-E1042-CON (DP-06) | The environment code of the deployment; the parameter code is Not specified in the source documents (GAP-0796; ASM-1485) |

The ACE group reference is a read-only SQL read and not a REST call: `recovery.v_ace_iam_group` (DF-ACE-301 to DF-ACE-304), owner RWB-P1-E1069-APP (DP-05), one hop in the same database, declared with its `data_as_of` and its 503. Nothing else is consumed: the reference-data contract of rwb-case is not declared, because this capability reads no list of values, and the load path of RWB-P4-E1037-CON is named as the route of a new version and not declared as an operation here.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library, consumed by P7 | Entry id, decision code `AC-DENY`, reason code `ROLE_CONFLICT`, the two role codes, the conflict version, the environment and the time |

The message uses the CloudEvents 1.0 envelope with the attributes id, source, type, specversion, time, subject and datacontenttype. No message carries a group membership, a user reference, a name, an e-mail address or a case fact. No access event of `rwb.access.events.v1` is declared for a refusal: `rwb.access.AccessPolicyChanged.v1` belongs to the load of a matrix, a masking row or a mapping, `rwb.access.DoaLimitChanged.v1` to the delegation table, and the refusal is a decision record (BR4, ASM-1479, ASM-1482).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this capability adds no subscription.

#### 12.5 Workflows and activities

None. The check and the two reads are synchronous REST answers in the caller's thread with no workflow, no activity and no signal. The six-monthly access review Schedule (JOB-18) is RWB-P4-AD008-CON's.

#### 12.6 Schedules

None. Nothing about a pair runs on a clock: the `validFrom` date is a row value the check resolves.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `role_conflict` | P4 (`rwb_access`) | The seven fields DF-REF-205 to DF-REF-211 are the pair and its version; read by the check and both reads, written by the migration seed of the app story and by the load path of RWB-P4-E1037-CON |
| `role` | P4 (`rwb_access`) | An active role code and its name and group (DF-REF-034 to DF-REF-039); read only |
| `permission` | P4 (`rwb_access`) | The Platform administration letters of the caller (DF-REF-040 to DF-REF-044); read only |
| `v_ace_iam_group` | ACE database, read-only view, owner RWB-P1-E1069-APP | The group reference: `entra_group`, `role_code`, `source_system`, `data_as_of`; never written |
| `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` | P3 (`rwb_case`) | Appear nowhere in the contract; the parameters read is a consumed operation, not a table (DP-01, DP-06) |
| `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Appear nowhere; the local entry is the library's and the central ledger and the rule registry are P7's |
| `partner_user` | S9 (`rwb_partner`) | Appears nowhere; the ownership map gives partner users to S9 |

No foreign key crosses a schema, and the contract names no table outside `rwb_access` except the read-only ACE view it consumes.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `rwb-access` separation-of-duty WireMock | The three paths of 12.1: a version in force holding the pair `RW-WRITEOFF` and `RW-WOCOMM`, an `ALLOWED` for a set with one of the two, a `REFUSED` with the pair, the version and the reason, a next version with a later `validFrom`, 403 with MSG-P4-002, 422 with MSG-GEN-001, 503 with MSG-P7-003 and 503 with MSG-GEN-006 | App story, the sign-in story, contract tests, wave 4 harness |
| Sign-in fake (RWB-P4-E1022-CON) | A resolved role set with the two role codes of the pair, and a set with one of them only | App story, contract tests |
| Parameters fake (RWB-P3-E1042-CON) | The environment code of the deployment | App story, contract tests |
| ACE group fake | The group of each role code with its `data_as_of`, and a role code the view no longer holds | App story, contract tests |
| Decision-record fake (RWB-PLT-E1027-CON) | The entry append, the hash-chain check and the 503 with MSG-P7-003 | App story, contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 1 consumed | The check, the conflict-table read and the version read provided; the parameters read consumed; one hop, 2 s timeout; plus one read-only SQL read of the ACE view |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1`; no access event of this capability |
| Temporal | None | No workflow, activity or Schedule in this contract |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-separation-of-duty-v1.yaml` (OpenAPI 3.1) with the three operations and the shared components, the four schemas, the `contract/error-envelope.yaml` with the agreed message IDs, the record declaration for `rwb.decision.DecisionRecorded.v1` with its reason code, the declared `conflictVersion` field of the session answer of RWB-P4-E1037-CON, the parameters stub with its owner, the ACE-view stub with its `data_as_of`, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

A contract story adds no build dependency of its own: each DP above is **referred to; the consuming story carries the dependency**, and that story is RWB-P4-AD005-APP, whose H row carries RWB-PLT-E1027-CON, RWB-PLT-E1042-CON and RWB-PLT-N001-CON and whose C row carries RWB-P3-E1042-CON. DP-03 is contracted as the entry the document declares on `rwb.decision-record.v1`; DP-05 as the statement that the group of a role code is read read-only through the P1 contract and never through a `public` table; DP-06 as the consumed parameters read that answers the environment code; DP-13 as the base of the document; DP-19 as the composite route that serves SCR-43.

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the error responses and the shared components; schema lint in the pipeline.
2. The three operations and the four schemas of section 11, with the page, the version and the dates.
3. The rule of the answer in the description of the check: the version in force, one version whole, a pair read both ways, the whole set refused and never a part (BR6 to BR8).
4. The refusal statement: no role, no scope and no token on a refusal, MSG-P4-006 to the person, one entry with reason `ROLE_CONFLICT` and its addressee (BR8, BR9).
5. The rights of the check and of the two reads, and the 401 and 403 of the default deny rule (BR10).
6. The one `conflictVersion` field of the session answer, with API-P4-012 named and no operation restated (BR13).
7. The record declaration with its decision code and reason code, and the statement that no access event exists for a refusal (BR4).
8. The error envelope and the message-ID mapping, with the legacy texts copied unchanged and the text of MSG-P4-006 left open.
9. The consumed parameters read and the read-only ACE view with their owners, the one-hop rule, the 2 s budget and the 503 (BR2).
10. The five fakes and the stub fixtures of section 12.8.
11. The eight contract tests; a drift between a fake and the document fails the build.
12. Baseline tag and the consumer sign-off note of the app story and of the sign-in story.

**Feature switch.** The contract carries no switch. The check is an operation of the service and a pair is data with a version; nothing about a refusal is behind a flag.

**Consumer sign-off**

| Consumer | What it accepts |
|---|---|
| RWB-P4-AD005-APP | The three provided operations, the four schemas, the refusal rule, the record type and the five fakes |
| RWB-P4-E1022-CON and RWB-P4-E1022-APP, the sign-in | The check request, the refusal answer and the `conflictVersion` field it answers |
| RWB-P4-E1037-CON, the session read | The one field this document adds to its answer, and the statement that it restates no operation |
| The wave 4 harness | The fakes of 12.8 and the parameters and ACE-view stubs |

The load and the approval route of a new conflict version, and the deprecation window of a published field, are the load path of RWB-P4-E1037-CON and are Not specified in the source documents (GAP-0796; ASM-1482).

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the five fakes answer every consumed and every provided path, and the app story, the sign-in story and the session contract have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No subject reference on the check, no session, or no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller without Platform administration R on a read | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A path the document does not publish, or a record outside the caller's scope | This case is not in your scope. |
| MSG-P4-006 | The resolved role set holds both halves of a pair at the conflict version in force | Not specified in the source documents (GAP-0796; ASM-1479); the message ID and the two role codes are fixed, the text is not |
| MSG-GEN-001 | A required field of a read is empty or invalid, or a role code of a pair is not an active role row | Enter {field}. |
| MSG-GEN-004 | The version label, the role code or the pair asked for does not exist, or no version or two versions are in force on the date asked | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The ACE group reference cannot be read | The reference data is not available. Try again later. |
| MSG-P7-003 | The decision-record entry of a refusal could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are contract elements; the text is the agreed text, taken from the legacy story where the message already existed. MSG-P4-006 is named by FSD P4 v3 AC-EXC-P4-001-03 and has no text in any source, so this document declares the ID, the pair it names and the refusal it carries, and leaves the text to the business decision: the sibling story RWB-P4-E1022-APP declares a text for the same ID in this run, and the two must agree before the freeze (GAP-0796; ASM-1479).

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access | List | The conflict-table read with the pairs in force, the reason, the conflict version and the dates |
| SCR-43 Roles and access | Version | The version read with its effective dates, its row count and the reference of the decision-record entry of its load |
| SCR-43 Roles and access | Access log | The refusal entries with reason `ROLE_CONFLICT`, read through the access-log operation of RWB-P4-AD007-APP on the same composite route |
| SCR-43 Roles and access | Refused | The 403 with MSG-P4-002 and no pair, and the 401 with MSG-P4-001 |
| SCR-43 Roles and access | Not available | The 503 with MSG-GEN-006 or MSG-P7-003 |
| SCR-43 Roles and access | Empty | Not specified in the source documents (CG-ALL-4614) |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-4614) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-4614) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-4614) |

The screen a refused person sees is the sign-in screen of RWB-P4-E1022-APP, which answers MSG-P4-006 with the two role codes. The screens of SCR-43 are served by the gateway-bff composite route (DP-19), which calls the conflict-table read and the access-log read in parallel, one hop each; the screen field list and the column order are Not specified in the source documents (GAP-0796; ASM-1481), and the document fixes the conflict side of the merge only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-005-01 | AC1 | Contract | Legacy test "Conflict refused" on the contract side: the check declares `REFUSED` with `RW-WRITEOFF` and `RW-WOCOMM`, the conflict version and the reason, and declares no role list, no scope and no token on a refusal; the record type carries `AC-DENY` and `ROLE_CONFLICT`; the behaviour itself is tested in RWB-P4-AD005-APP at End to end |
| TC-AD-005-02 | AC2 | Contract | Legacy test "Table as data" on the contract side: the version rule is declared — the version whose `validFrom` is the latest not after the date of the sign-in, one version whole — and a version with a later `validFrom` is answered only from its date; the loading of a version is named as the load path of RWB-P4-E1037-CON and not as an operation of this document |
| TC-AD-005-03 | Access | Component | Legacy test "A role without the right is refused with MSG-P4-002": a caller with no Platform administration letter is declared refused on both reads, and the document declares the 403 with MSG-P4-002 and the refusal entry |
| TC-AD-005-04 | Principle 5 | NFR | Legacy test "A forced decision log write failure stops the action with MSG-P7-003": the document declares the 503 with MSG-P7-003 and the fake answers it, so no consumer treats a refused session as answered |
| TC-AD-005-05 | AC3 | Contract | Given the description of the check operation: the version rule, the both-orders rule, the refusal fields with no role list, scope or token, the AC-DENY and ROLE_CONFLICT entry addressed to the security administrator, and the session not answered when the entry cannot be written |
| TC-AD-005-06 | AC4 | Contract | Given the session section: GET /me/session (API-P4-012) is named and not restated, exactly one field conflictVersion is added and kept until the session ends, and no other session field is declared, removed or retyped |
| TC-AD-005-07 | AC5 | Contract | rwb.decision.DecisionRecorded.v1 on rwb.decision-record.v1 with AC-DENY and ROLE_CONFLICT; no access event for the refusal; no second name or topic; the conflict version load named as the load path of RWB-P4-E1037-CON; no payload carries a group membership, user reference, name or case fact |
| TC-AD-005-08 | AC6 | Contract | GET /api/recovery/case/v1/admin/parameters declared with owner rwb-case and RWB-P3-E1042-CON for the environment code only; v_ace_iam_group declared with DF-ACE-301 to DF-ACE-304 and data_as_of, with its test data written against the ACE group fake of section 12.8 (rwb-source-data contract fake); both one hop with 2 s budget and 503; no other service operation, table or list declared as provided |
| TC-AD-005-09 | AC7 | Contract | The error envelope carries code, message, messageId, traceId and field list with the problem media type; 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003 or MSG-GEN-004, 409 MSG-GEN-004, 422 MSG-GEN-001, 503 MSG-P7-003 or MSG-GEN-006; MSG-P4-006 declared with open text |
| TC-AD-005-10 | AC8 | Contract | The four fakes of section 12.8 match the document: separation-of-duty answers the three paths of 12.1; sign-in answers a role set and no session; parameters answers the environment code; ACE group answers each role code with data_as_of; decision-record answers the append and the 503 with MSG-P7-003; a contract test fails on drift; no fake carries a name or e-mail |
| TC-AD-005-11 | §12.7 tables (ASM-3438) | Not specified in the source documents (DOR-RWB-P4-AD005-CON-12) | Boundary test of the tables of §12.7 (ASM-3438); the boundary values are Not specified in the source documents (DOR-RWB-P4-AD005-CON-12) |
| TC-AD-005-12 | AC9 | Contract | Each rule BR1 to BR14 of section 8 is checked against the document or its guardrail; the fixture values are Not specified in the source documents (NEWAC-RWB-P4-AD005-CON-AC9) |
| TC-AD-005-13 | AC10 | Contract | The document states the answer to a replay of a write with the same idempotency key; the replay answer is Not specified in the source documents (NEWAC-RWB-P4-AD005-CON-AC10) |

The four legacy test cases are kept with their IDs and their legacy Covers values, and the legacy test name is written in the Data column. The Level column follows Template and Rules §R7.2: the check, the refusal and the version rule are tested against the artefact at Contract, the legacy Access row stays Component, and the legacy Resilience row of Principle 5 stays NFR. The behaviour of each case in the running service is RWB-P4-AD005-APP's at End to end, and the full test with its Given, When and Then is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The ITG copy of the set is RWB-ITG-AD005-ITG's and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in the contract: the pairs, the reasons and the version labels are data rows, the environment is a parameter, and the document fixes names and types only.
- No personal data in a schema, an example or a fake: a pair is two role codes, a refusal carries a subject reference and no name, and a name or an e-mail address in the document fails the review (BR12).
- The contract names only `rwb-access` tables, the read-only ACE view it consumes and operations owned by `rwb-access` or declared as consumed (DP-01, BR5).
- One REST base and one record topic, and no access event and no incident operation invented for a refusal (DP-13, BR3, BR4).
- The refusal is whole and it is recorded: a consumer that reads a partial refusal or a refusal with no entry fails the contract test (BR8, BR9).
- The session answer is touched once: one field, `conflictVersion`, and no operation of RWB-P4-E1037-CON restated (BR13).
- Every example and every fake is synthetic; no production group, person or entitlement is copied into a schema or a fake.
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

No requirement ID is recorded for legacy RWB-AD-005 in TSD P4 v3 T8, the legacy story's Feature row reads None, and the Work Package carries the requirement list of this key as empty. The control this key serves is the FSD P4 v3 exception row AC-EXC-P4-001-03, "A conflicting role pair is refused", which fixes the message MSG-P4-006, the two role codes of its example, the incident to the security administrator and the refusal reason `ROLE_CONFLICT`.

| Reference | Contract element | Test cases |
|---|---|---|
| FSD P4 v3 AC-EXC-P4-001-03, a conflicting role pair is refused | The check answer, the whole-session refusal and MSG-P4-006 of 12.1 and 14 | TC-AD-005-01 |
| The role conflict table as data with a version | `RoleConflict` and `RoleConflictVersion` of 12.7, and the version rule of BR7 | TC-AD-005-02 |
| The incident to the security administrator | The record type of 12.3 with reason `ROLE_CONFLICT` and its addressee, and the open channel carried as a gap | TC-AD-005-01 |
| The record-before-refusal rule | The 503 with MSG-P7-003 and the entry reference of a version load | TC-AD-005-04 |
| The permission check of the administration reads | The 403 of 12.1 and BR10 | TC-AD-005-03 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy AC1 and AC2 | The behaviour of RWB-P4-AD005-APP; this contract carries the elements they are tested against, and section 16 keeps their test cases |
| The role codes `RW-WRITEOFF` and `RW-WOCOMM` and the pair of the FSD example | Sections 3, 7, 11 |
| The Data table: `role` DF-REF-034 to DF-REF-038, and `role_conflict` DF-REF-205 to DF-REF-211 of TSD P4 v3 T3.1 | Sections 11, 12.7 |
| The permission checks Rules and parameters C and A | Not kept: the rule-version rights are other stories', and the pairs are Platform administration data (section 12.1) |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003, and MSG-P4-006 of the FSD | Section 14, exception paths |
| Screen SCR-43 Roles and access | Section 15 |
| Legacy test cases TC-AD-005-01 to TC-AD-005-04 | Section 16 |

### 19. Out of scope

- The implementation of the check, the migration, the refusal record, the two reads and the `conflictVersion` value: RWB-P4-AD005-APP.
- The sign-in, the token, the second factor, the group claim and the resolution of a person's roles: RWB-P4-E1022-CON and RWB-P4-E1022-APP. This contract is what that story calls, and it declares no session of its own.
- The session read itself: RWB-P4-E1037-CON declares `GET /me/session` (API-P4-012); this contract adds the one field `conflictVersion` and restates no operation.
- The permission matrix, the masking rows and the role catalogue: RWB-P4-E1037-CON, RWB-P4-E1037-APP and RWB-P4-E1019-APP.
- The group-to-role mapping and its maintenance: RWB-P4-AD001-APP and RWB-P4-AD001-CON.
- The load, the approval and the rollback of a new conflict version, and the matrix and masking loads: the load path of RWB-P4-E1037-CON with RWB-P4-AD002-CON, RWB-P4-AD004-CON and RWB-P4-AD010-CON.
- The two rule-version paths of the legacy Endpoints table, a load and an approval: the rule-version stories of this service and P7 rwb-decision under the ownership map. They are named as legacy rows and are not declared as paths of this document.
- The rule package registry and its tables (`rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`): P7 rwb-decision under the ownership map.
- The access review list and its Schedule (JOB-18): RWB-P4-AD008-CON and RWB-P4-AD008-APP; the access-log read is RWB-P4-AD007-CON's; the break-glass grant is RWB-P4-AD006-CON's.
- The central decision ledger and its query: P7 rwb-decision; the local entry is the library's.
- The reference data and the parameter values of the estate, including the environment codes: P3 rwb-case under DP-06 and its reference-data contract; this contract declares one consumed parameters read and no table of either.
- `partner_user`: S9 rwb-partner.
- The incident queue, the incident operation and the target service of the incident the criterion requires: named by no source, carried as a gap and an assumption, and not declared here (GAP-0796; ASM-1482).
- The bank IAM's own group administration: Entra ID and the bank IAM (INT-21).
- The deployment of the capability: the Helm values, the topic creation, the dashboards and the runbook.
- The integration harness and its evidence, and the `-ITG` copies of the test cases: RWB-ITG-AD005-ITG.
