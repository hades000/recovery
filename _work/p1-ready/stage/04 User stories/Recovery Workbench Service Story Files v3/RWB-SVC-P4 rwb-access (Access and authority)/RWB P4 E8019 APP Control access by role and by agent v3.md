# RWB-P4-E8019-APP Control access by role and by agent

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8019-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P4-E8019-APP-14); confirm with the epic design record |
| Size | Not set; the squad sizes it at refinement |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP13, DP19 |
| Parallel lane | L-P4-BM |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-E8019-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E8019-APP-23); the paths carry `/v1` |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-019 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 13 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator**, I want **the access matrix of the recovery workbench as one data surface over people, partner users and agents, the setting of one role's or one agent's letters in one capability area as a recorded matrix change, the second approval an agent's change needs, and a report of the matrix that Compliance, Risk and Internal audit read**, so that **what a role or an agent may see and do is data that changes without a release, an agent holds letters in the same matrix as a person, and every change can be shown afterwards with the version it was made under and the reason it was made**.

Inside `rwb-access` this is the role-and-agent slice of the legacy story RWB-E8-019 (FEAT-ADM-14):

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Four deliverables, and nothing else: the read `GET /api/recovery/access/v1/admin/access-matrix`, which answers the matrix of every role and every service identity with its letters per capability area and can be filtered by role class; the write `PATCH /api/recovery/access/v1/admin/access-matrix/{roleCode}`, which sets the letters of one role or one agent in one capability area as a new matrix version under an `If-Match` guard, a reason and, for a non-human actor, a second approver; the write `POST /api/recovery/access/v1/admin/access-matrix/{roleCode}/approve`, which is that second approval; and the read `GET /api/recovery/access/v1/admin/access-matrix/report`, which is the report Compliance, Risk and Internal audit read.
- The capability is **one matrix over three role classes and no separate agent table**. An agent is a role whose `role_class` (DF-REF-037) is `NON_HUMAN_ACTOR`, one of the three values of LOV-ROLE-CLASS (TSD P4 v3 T3.2), and it holds letters in `permission` (DF-REF-043) exactly as a person's role does. The five system roles of the T6.1 matrix (`SY-CASEWF`, `SY-RULES`, `SY-DATALOAD`, `SY-OCR`, `SY-AGENT`) are rows of that class, and `SY-AGENT` holds `R` in Rules and parameters and in Reference data in that matrix (TSD P4 v3 T6.1). An agent's service identity, its allowed-action list and its run records stay with `rwb-agent` (P10) and are not read, stored or copied here (ASM-1610).
- The same service writes only its own `role` and `permission` rows. The group mapping is **not** this service's data: `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) is an ACE view and the `iam_group` rows behind it belong to `rwb-source-data` (P1) under the ownership map, so the mapping reaches this story only as an answer of the `rwb-source-data` contract, one hop under DP-05, and no statement of this story names the view or a `public` table (BR10).
- A change is data and needs no release. The letters are rows of `permission` stamped with a `matrix_version` (DF-REF-044); the change mints the next matrix version label, supersedes the row in force and writes one entry of the local decision-record chain of DP-03 in the same transaction as its idempotency and outbox rows. The central ledger `decision_log_entry` stays in `rwb-decision` and is neither read nor written here (BR7, BR8).
- Every applied change is announced as `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, the event of Arch v5 slide 14 and slide 43 that every consumer of the cached permission data subscribes to for its cache refresh (BR6).
- The boundary: the whole-file load of a matrix pack and the masking profiles are RWB-P4-AD002-APP and RWB-P4-E1037-APP's; the scope per role is RWB-P4-AD003-APP's; the separation of duty rows are RWB-P4-AD005-APP's; the delegation table and the access log with break-glass are RWB-P4-E1038-APP and RWB-P4-E1039-APP's; the guard that enforces the matrix in the other services is RWB-PLT-E1037-CON. This story sets one grant, reads the matrix and reports it.
- This story starts no workflow, owns no Schedule and holds no Temporal activity: a set, an approval and a report are synchronous, the effective time of a change is the time of its record, and the only Schedule of `rwb-access` remains the six-monthly access review list (JOB-18) of RWB-P4-AD008-APP.
- Where a value is missing, the placeholder of Template and Rules R9 is used with the rows of this story: Not specified in the source documents (GAP-0885; ASM-1604).

The set of a matrix change and the set of an agent's letters differ in one step and in nothing else: a change to a `BANK_USER` or `PARTNER_USER` role is applied by the requester in one call, and a change to a `NON_HUMAN_ACTOR` role is held as `PENDING_APPROVAL` until a second person who does not hold the requester's identity approves it (BR5, ASM-1605). The state set a change carries - `PENDING_APPROVAL`, `APPLIED`, `REFUSED`, `SUPERSEDED` - is Not specified in the source documents (GAP-0886; ASM-1605) and is fixed by the contract of RWB-P4-E8019-CON.

### 2. Business rationale

The FSD fixes one measure for this module: rule and limit changes made without a code release, 100 percent, measured monthly from the decision record and the Workbench records (FSD P4 v3 A2.30.1). The problem the feature names is that access, limits and rules live in documents and people's heads, so a change needs code or a manual check. This story is where the artefact that answers "who may do what, under which version, since when" is produced: the matrix, read in one place, changed by a person with the right, approved where the actor is not a person, and reported with its versions.

The legacy story asked for three things in one sentence and the target keeps all three: review the matrix, set what each role and each agent may read and do, and report the matrix. What the target adds is the answer an auditor asks for after a change - which version was in force before, which one after, which reason the change carries and which parameters version was read on the day. In the monolith the letters, the rules and the cases sat in one schema and a change was a table update by whoever could reach it; here a letter is a row of `permission` stamped with a version, and a change is a hash-chained record of `rwb-access` written in the same transaction as its outbox row.

The agent half is the reason the story is not a screen over a lookup table. Architecture v5 gives this service the authorisation decisions of the whole estate (slide 14: `POST /authorise`, role, scope and DoA), and five of the roles of the T6.1 matrix are system roles. A matrix that covers people and forgets the services and the agents is exactly the gap that lets a non-human actor read what no role grants it, and REQ-ACA-010 and NFR-051 put it plainly: agents run under service identities and are subject to the same role checks as people. This story makes an agent a row of the same matrix with the same letters, no second table and no second enforcement path, so one change is seen by the guard, by the screens and by the agent runtime at the same moment.

The change is also deliberately narrow. It sets one role in one capability area under an optimistic lock, so two administrators cannot silently overwrite each other, and it names a reason, so the record explains itself years later. The second approval for a non-human actor is the four-eyes control of the estate applied where the actor cannot be the person who is affected: an agent's grant is reviewed by a second human before it can be used.

The story serves REQ-ACA-002, REQ-ACA-003, REQ-ACA-010, REQ-ACA-013 and REQ-CWC-018 and carries the guardrails of the legacy key: no value a business person may change is written in code (FSD P4 v3 BR-P4-030), no personal data in the answer, the record, the event or the report, and no read of another service's tables.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8019-CON (same service, its own contract story) | The OpenAPI 3.1 document of the four operations, the `AccessMatrix`, `AccessMatrixRow`, `AccessMatrixChange`, `AccessMatrixReport` and `ChangeRequest` schemas, the closed sets of the capability areas and the letters, the three role classes, the change state set, the error envelope, the consumed-operation list and the five contract fakes. This story implements that document and adds no path and no field |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a change, hash-linked, written in the transaction that stores the change |
| RWB-PLT-E1042-CON and RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the report page bounds, the second-approval switch of a non-human actor change and the parameter version recorded on the entry |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-43 Roles and access and calls the four operations, one hop each |
| The `rwb-source-data` contract | The read of the ACE group mapping per role: the groups mapped to a role, the role code, the source system and the date of the data (DF-ACE-301 to DF-ACE-304). Declared as consumed and faked, because the `iam_group` rows are P1's (DP-05; GAP-0889; ASM-1608) |
| The `rwb_access` baseline | `role` and `permission` with their dictionary rows, created by the service baseline migration of RWB-PLT-E1044-CON and by RWB-P4-E1037-APP; this story adds one index and no table (ASM-1606) |

Business preconditions carried from the legacy story, the feature specification and the technical specification:

- A matrix version is in force. Tests use `PM-2026.11`, the version the module's own matrix work already names; a change mints the next label, and the tests use `PM-2027.01` for the label a change mints (BR2, GAP-0885). A change is a new versioned set that supersedes the version in force and is never an edit in place (GAP-2304).
- The rights in force are those of TSD P4 v3 T6.1: `RW-SECADM` holds `CRUDA` in Platform administration, `RW-AUDIT` and `RW-COMPLY` hold `R` in it, and a case role such as `RW-CASEOWN` holds a dash. The legacy story names Rules and parameters `C` for `RW-COE` and `A` for `RW-RISK` for the same journey; the target right of this story is Platform administration `R` to read and report, `U` to set and `A` to approve, and the difference is the key's conflict row; the legacy `Rules and parameters` letters belong to the rule-change stories (GAP-0888; ASM-1607).
- The three role classes are `BANK_USER`, `PARTNER_USER` and `NON_HUMAN_ACTOR` (TSD P4 v3 T3.2 LOV-ROLE-CLASS), and `role.role_class` (DF-REF-037) carries one of them.
- The letters are `C`, `R`, `U`, `D` and `A` in that order, or a dash for none (FSD P4 v3 A2.30.3.2 `permission.letters`; TSD P4 v3 T3.1 DF-REF-043).
- The capability areas are the fourteen of TSD P4 v3 T3.2 LOV-CAPABILITY. The list itself is P3 reference data under the ownership ruling and this story carries neither DP-07 nor `RWB-P3-E1043-CON`, so the set a change may name is the closed set the contract publishes and the set present in the matrix at the version in force, and the point is raised as the key's gap (GAP-0885; ASM-1604).
- The ACE group mapping is read, never written: the legacy data row `v_ace_iam_group` names `entra_group`, `role_code`, `source_system` and `data_as_of` (DF-ACE-301 to DF-ACE-304), it is an ACE view, and `role.entra_group` (DF-REF-039) is the only group column of this service and is read as a stored answer (BR10).
- Partner users stay with S9: the role class `PARTNER_USER` is a value of this service's `role` table, but the partner user identity, the partner firm, the partner case and the partner session are `rwb-partner`'s under the ownership map, and this story holds none of them (BR11; ASM-1609).
- Every user, role, group, version and reason in the tests is synthetic. No production entitlement and no personal value is read, and no name is stored in a row, a log, an event or a prompt.
- A change to the matrix carries one of four states: `PENDING_APPROVAL`, `APPLIED`, `REFUSED` or `SUPERSEDED`. A change to a `NON_HUMAN_ACTOR` role waits in `PENDING_APPROVAL` for a second person, and the approver is taken from the matrix and not from code (GAP-0886).

### 4. Flow

1. The security administrator opens SCR-43 Roles and access through the gateway-bff composite route (DP-19). The route calls `GET /api/recovery/access/v1/admin/access-matrix` with an optional `roleClass` filter and renders the rows it is given.
2. `AccessMatrixController` validates the filter against the three role class values the matrix holds at the version in force and against no constant list; a value outside them is refused with 422 and MSG-GEN-001 (BR15).
3. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Platform administration `R`. A caller without the `R` letter is refused with 403 and MSG-P4-002 and no row is answered (BR3, AC6).
4. `AccessMatrixService` reads the version in force from `permission` (DF-REF-044) and `role` (DF-REF-034 to DF-REF-038) and builds one row per role: role code, role name, role class, default scope, and per capability area the letters and the matrix version that carries them (BR1, BR4).
5. `GroupMappingClient` reads the group mapping of the roles in the page from `GET /api/recovery/source-data/v1/iam-groups` of `rwb-source-data`, one hop with a 2 s timeout and a breaker, and takes from the answer only the role code, the mapped group codes, the source system and the date of the data (DP-05, BR10).
6. The answer is 200 with `matrixVersion`, `items` of role rows, `page`, `size`, `total`, and a `groupMapping` block per row that carries the group codes and `dataAsOf` and nothing else. Where `rwb-source-data` does not answer inside its budget, the matrix is still answered, the `groupMapping` block is absent and `groupMappingAvailable` is false for the page, because the matrix is this service's data and the mapping is enrichment (X12, ASM-1608).
7. The administrator opens one role, one capability area and the letters, and submits the change. The route calls `PATCH /api/recovery/access/v1/admin/access-matrix/{roleCode}` with the header `If-Match` carrying the `matrixVersion` it read and the body `capabilityArea`, `letters`, `reason` and, for a non-human actor, `secondApproverRole`; an `Idempotency-Key` is required.
8. `AccessMatrixController` validates the request: `roleCode` is a role of the matrix at the version in force, `capabilityArea` is a capability area of the closed set in force, `letters` are `C`, `R`, `U`, `D` and `A` in that order or a dash, and `reason` is present. An empty field, an unknown code or an invalid letter is refused with 422 and MSG-GEN-001 naming the field, and nothing is read further and nothing is written (BR2, X1, X2).
9. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer, records nothing and publishes nothing (BR13, AC8).
10. The controller calls the authorise operation for Platform administration `U`. A caller without it is refused with 403 and MSG-P4-002, and nothing is written (BR3, AC6).
11. `AccessMatrixService` compares the `If-Match` value with the matrix version in force. A different value is refused with 409 and MSG-GEN-004 and the caller is asked to reload, because another administrator changed the matrix under the read (BR12, X5).
12. `AccessMatrixService` reads the role class of the role. For a `BANK_USER` or `PARTNER_USER` role the change is applied in this call. For a `NON_HUMAN_ACTOR` role the change is stored as one pending change of that role and area with state `PENDING_APPROVAL`, the answer is 202 with the `changeId` and that state, and the permission row in force is not touched (BR5, AC4).
13. `PermissionWriter` mints the next matrix version label, writes the letters of the role and area under that label, and sets the end of validity of the row it replaces, so the version before stays readable with its dates and is never edited (BR1, BR9).
14. In one local transaction the service appends one entry to the decision-record chain of DP-03 with the record code of a matrix change, the role code, the capability area, the letters before and after, the matrix version before and after, the reason, the parameter version read and, where a break-glass grant is active, the grant id; sets the idempotency row to the answer; and stages the outbox rows of the entry and of the policy event (BR7, BR13).
15. The answer is 200 for an applied change with `changeId`, `roleCode`, `capabilityArea`, `lettersBefore`, `lettersAfter`, `matrixVersionBefore`, `matrixVersion`, `state` `APPLIED`, `changedAt`, `changedByRole`, `reason`, and the `Location` of the report read filtered to the role; where a break-glass grant is active the answer carries the warning with the end time of the grant (BR6, X11).
16. A second person holding Platform administration `A` calls `POST /api/recovery/access/v1/admin/access-matrix/{roleCode}/approve` with the `changeId`, the `If-Match` of the version in force, the `secondApproverRole` and an `Idempotency-Key`. `AgentChangeApprovalService` refuses the requester's own identity with 403 and MSG-P7-002, refuses an approver without `A` with 403 and MSG-P4-002, and otherwise applies the change exactly as steps 13 to 15 apply it, with the approver's role code and the requester's reference recorded on the entry (BR5, AC4).
17. Every applied change publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` through the outbox of the transaction, with the role code, the capability area, the letters before and after, the matrix version before and after, the change kind and the effective time, and no personal value. A consumer of the cached permission data refreshes its answer when it receives it (BR6, AC8).
18. `AccessMatrixReportService` answers `GET /api/recovery/access/v1/admin/access-matrix/report` for Platform administration `R`: one row per role and capability area at the version in force, or at a version named in the query, with the role code, the role class, the capability area, the letters, the matrix version, the time of the change that produced it and the reason; paged, with the page default and maximum read through DP-06, in JSON or in `text/csv` where the caller asks for the CSV media type (BR14, AC5).
19. A role, an area or a version with no row answers 200 with an empty `items` and total 0; the report is never a 404 and never names a person, so it cannot be used to probe for a role that holds nothing (BR14, AC9).
20. Where the local record cannot be written, the answer is withheld with 503 and MSG-P7-003 and nothing changes: the permission row, the idempotency row and the outbox row roll back together (BR8, AC2).
21. Responses behind SCR-39, SCR-41 and SCR-43 (their screen states are in section 15): an empty read answers 200 with an empty `items` and total 0 (step 19, AC5); a caller without the letter is refused with MSG-P4-002 and no row (step 3, AC6); a change that cannot be recorded shows 503 with MSG-P7-003 and nothing changes (step 20, AC2); a group answer outside its budget leaves `groupMappingAvailable` false (step 6); the loading state is Not specified in the source documents (DOR-RWB-P4-E8019-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, `roleCode` is not a role of the matrix, or `letters` are not `C`, `R`, `U`, `D`, `A` in order or a dash | 422 naming the field; no change stored, nothing published | MSG-GEN-001 | AC4, AC6 |
| X2 | `capabilityArea` is not a capability area of the set in force | 422 naming `capabilityArea`; no change stored | MSG-GEN-001 | AC4 |
| X3 | The caller holds no Platform administration `R` on a read, `U` on a set, or `A` on an approval | 403; no row answered and no change stored | MSG-P4-002 | AC6 |
| X4 | The caller's session has ended | 401; no row answered and no change stored | MSG-P4-001 | AC6 |
| X5 | `If-Match` names a matrix version that is not the version in force | 409; the change is not stored and the caller reloads | MSG-GEN-004 | AC4 |
| X6 | A second change to the same role and area arrives while one change of that role and area is `PENDING_APPROVAL` | 409; the pending change stays and is the one the approver sees | MSG-GEN-004 | AC4 |
| X7 | The requester of a non-human actor change calls approve on the change | 403; the change stays `PENDING_APPROVAL` and nothing is applied | MSG-P7-002 | AC4 |
| X8 | A non-human actor change is approved by a caller without Platform administration `A` | 403; the change stays `PENDING_APPROVAL` | MSG-P4-002 | AC4, AC6 |
| X9 | The decision-record entry, the idempotency row or an outbox row cannot be written | 503; the letters, the version and the event are all unchanged | MSG-P7-003 | AC2 |
| X10 | The same change arrives twice with the same `Idempotency-Key` | The first answer is replayed; one entry, one version, one event | None | AC8 |
| X11 | A break-glass grant is active for the caller | The change proceeds and the answer carries the warning with the end time of the grant, and the entry carries the grant id | MSG-P4-004 | AC7 |
| X12 | `rwb-source-data` does not answer inside 2 s, or the connection fails | The matrix is still answered with `groupMappingAvailable` false and no group block; no change is made and nothing is recorded | None | AC3 |

No exception path of this story changes a case, a task, a partner user or a masking rule: it writes the letters of one role and its record, or it writes nothing at all.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8019-CON and its fakes; the group mapping arrives through the `rwb-source-data` contract, so no ACE view and no `iam_group` row is held here |
| Negotiable | The report page bounds and the second-approval switch are parameter rows; the state set and the report field set are reviewed with Compliance, Risk and Internal audit and fixed by the contract |
| Valuable | One matrix covers people, partner users and agents, a change is data with a reason and a version, and an agent's grant needs a second person |
| Estimable | One controller, one matrix service, one approval service, one report service, one writer, one group client, one record appender, one publisher, five fakes and nine test cases |
| Small | Fits one sprint with its tests; one index, no new table, no workflow, no schedule and no screen of its own |
| Testable | Each owned criterion has a test case in section 16; the four-eyes rule is provable with two administrators, the version is provable from the rows, and the event is provable from the fake topic |

### 7. Acceptance criteria

```gherkin
Feature: Control access by role and by agent

  Background:
    Given the environment is SIT
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given permission matrix version "PM-2026.11" is in force
    Given SY-AGENT is a role of class NON_HUMAN_ACTOR with "R" in "RULES_AND_PARAMETERS" and in "REFERENCE_DATA" at "PM-2026.11"
    Given test user "U-8101" holds RW-SECADM with "CRUDA" in "PLATFORM_ADMINISTRATION"
    Given test user "U-8103" holds RW-SECADM with "CRUDA" in "PLATFORM_ADMINISTRATION"
    Given test user "U-8104" holds RW-AUDIT with "R" in "PLATFORM_ADMINISTRATION"
    Given test user "U-8105" holds RW-CASEOWN with "-" in "PLATFORM_ADMINISTRATION"

  Scenario: AC1 Control access by role and by agent (legacy RWB-E8-019 AC1)
    Given the rwb-source-data contract mock returns the group "RWB-SIT-SY-AGENT01" mapped to role "SY-AGENT" and parameter version in force
    Given the matrix in force is "PM-2026.11"
    When the user acts on the screen
    Then the response is 200 with state "APPLIED" and matrixVersion "PM-2027.01" and the letters set for each role and each agent
    Then one decision-record entry is appended with the role, the capability area, the letters before and after, both matrix versions and the parameter version

  Scenario: AC2 Not recorded (legacy RWB-E8-019 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The matrix read covers the three role classes and an agent is a row (new, D-RCV-60)
    Given the rwb-source-data contract mock answers GET /api/recovery/source-data/v1/iam-groups for role "SY-AGENT" with group "RWB-SIT-SY-AGENT01", source system "ENTRA_ID" and data_as_of "2026-11-20"
    When "U-8101" calls GET /api/recovery/access/v1/admin/access-matrix
    Then the response is 200 with matrixVersion "PM-2026.11" and one row per role at that version, each with roleCode, roleName, roleClass, defaultScope and the letters of each capability area
    Then the rows carry roleClass "BANK_USER" for role "RW-CASEOWN" and roleClass "NON_HUMAN_ACTOR" for role "SY-AGENT", and "SY-AGENT" holds "R" in "RULES_AND_PARAMETERS"
    Then the "SY-AGENT" row carries the group "RWB-SIT-SY-AGENT01" and dataAsOf "2026-11-20" from the rwb-source-data contract answer
    When "U-8101" calls the same operation with roleClass "NON_HUMAN_ACTOR"
    Then the response is 200 and carries only rows of that class
    When "U-8101" calls the same operation with roleClass "PARTNER_USER"
    Then the response is 200 and carries only rows of class "PARTNER_USER", and no partner user identity, partner firm or partner case is read or answered by rwb-access
    When "U-8101" calls the same operation with roleClass "SERVICE_ACCOUNT"
    Then the response is 422 with message MSG-GEN-001 naming roleClass

  Scenario: AC4 A change to an agent's letters needs a second approver (new, D-RCV-60)
    Given "U-8101" calls PATCH /api/recovery/access/v1/admin/access-matrix/SY-AGENT with If-Match "PM-2026.11" and the body capabilityArea "TREATMENT_AND_OFFER", letters "RU", reason "Agent reads the offer stage", secondApproverRole "RW-SECADM" and Idempotency-Key "k-019-1"
    Then the response is 202 with a changeId, roleCode "SY-AGENT", state "PENDING_APPROVAL" and no matrixVersion
    Then SY-AGENT still holds no letter in "TREATMENT_AND_OFFER" at "PM-2026.11" and the matrix in force is still "PM-2026.11"
    When "U-8101" calls POST /api/recovery/access/v1/admin/access-matrix/SY-AGENT/approve with that changeId, If-Match "PM-2026.11" and Idempotency-Key "k-019-2"
    Then the response is 403 with message MSG-P7-002 and the change stays "PENDING_APPROVAL"
    When "U-8103" calls the same approve operation with that changeId and If-Match "PM-2026.11"
    Then the response is 200 with state "APPLIED", matrixVersion "PM-2027.01" and lettersAfter "RU"
    Then SY-AGENT holds "RU" in "TREATMENT_AND_OFFER" at "PM-2027.01" and the row at "PM-2026.11" is still readable with its end date
    Then one decision-record entry and one rwb.access.AccessPolicyChanged.v1 exist for the change
    When "U-8101" calls the same PATCH again with Idempotency-Key "k-019-1"
    Then the first answer is replayed with its changeId and state "PENDING_APPROVAL" and no second change is stored

  Scenario: AC5 The report of the matrix is readable by Compliance, Risk and Internal audit (new, D-RCV-60)
    Given "U-8101" applied a change to "RW-CASEOWN" in "QUEUE_AND_ALLOCATION" with reason "Queue read for the case owner" and matrix version "PM-2027.01"
    When "U-8104" holding RW-AUDIT with "R" calls GET /api/recovery/access/v1/admin/access-matrix/report?version=PM-2027.01
    Then the response is 200 with one row per role and capability area at that version, each with roleCode, roleClass, capabilityArea, letters, matrixVersion, changedAt and reason
    Then the report carries the matrix versions "PM-2026.11" and "PM-2027.01" and the reason of the change
    Then the report carries no name, no e-mail address and no user reference
    When "U-8104" calls the same operation with the CSV media type
    Then the response is 200 with content type text/csv, one header row and one line per report row, with the same fields
    When "U-8104" calls the same operation for a capability area with no row
    Then the response is 200 with an empty items and total 0, and never a 404

  Scenario: AC6 A role without Platform administration R is refused (new, D-RCV-60)
    Given "U-8105" holds RW-CASEOWN with "-" in "PLATFORM_ADMINISTRATION"
    When "U-8105" calls GET /api/recovery/access/v1/admin/access-matrix
    Then the response is 403 with message MSG-P4-002 and no row is answered
    When "U-8105" calls PATCH /api/recovery/access/v1/admin/access-matrix/RW-CASEOWN with If-Match "PM-2026.11" and the body capabilityArea "CASE_RECORD", letters "RU", reason "Own case edit" and Idempotency-Key "k-019-6"
    Then the response is 403 with message MSG-P4-002
    Then no change is stored, no decision-record entry is appended and no rwb.access.AccessPolicyChanged.v1 is published
    Then RW-CASEOWN keeps its letters at "PM-2026.11"

  Scenario: AC7 A break-glass grant carries a warning on the change (new, D-RCV-60)
    Given a break-glass grant for "U-8101" is active until "2027-01-15T18:00:00Z"
    When "U-8101" applies a change to "RW-CASEOWN" in "DECISION_LOG" with letters "R", reason "Audit read of the decision log" and Idempotency-Key "k-019-7"
    Then the response is 200 with state "APPLIED" and the warning MSG-P4-004 carrying the end time "2027-01-15T18:00:00Z"
    Then the decision-record entry of the change carries the grant id

  Scenario: AC8 A change is announced and the cached permission data is refreshed (new, D-RCV-60)
    Given the matrix in force is "PM-2026.11"
    When "U-8101" applies a change to "RW-CASEOWN" in "QUEUE_AND_ALLOCATION" with letters "RU" and reason "Queue read and update for the case owner" under Idempotency-Key "k-019-8"
    Then the response is 200 with state "APPLIED", matrixVersionBefore "PM-2026.11" and matrixVersion "PM-2027.01"
    Then one rwb.access.AccessPolicyChanged.v1 is published on rwb.access.events.v1 with roleCode "RW-CASEOWN", capabilityArea "QUEUE_AND_ALLOCATION", lettersBefore "R", lettersAfter "RU", matrixVersionBefore "PM-2026.11", matrixVersion "PM-2027.01", changeKind "matrix" and the time of the change
    Then a consumer of the cached permission data refreshes its answer for "RW-CASEOWN" and its next authorise call answers "RU" in "QUEUE_AND_ALLOCATION"
    When "U-8101" sends the same change again with Idempotency-Key "k-019-8"
    Then the first answer is replayed and no second event is published and no second entry is appended

  Scenario: AC9 No personal data in the matrix or the report, and partner users stay with S9 (new, D-RCV-60)
    Given the matrix read at "PM-2027.01" and the report at the same version
    When both are answered to "U-8104" holding RW-AUDIT with "R"
    Then neither carries a name, an e-mail address, a user reference or a personal field value
    Then the group enrichment carries the mapped group codes, the source system and dataAsOf only
    Then the PARTNER_USER class appears as a role class value and no partner user identity, partner firm or partner case is held in rwb_access
    Then no row of v_ace_iam_group and no row of the iam_group table behind it is read by rwb-access

  Scenario: AC10 A change never edits the version it replaces (new, D-RCV-60)
    Given the matrix in force is "PM-2026.11" and "RW-CASEOWN" holds "R" in "QUEUE_AND_ALLOCATION" at "PM-2026.11"
    When "U-8101" applies a change to "RW-CASEOWN" in "QUEUE_AND_ALLOCATION" with letters "RU" and reason "Queue read and update for the case owner" under Idempotency-Key "k-019-9"
    Then the row at "PM-2026.11" still holds "R" and keeps its end date, and no row is updated in place
    Then the matrix in force is "PM-2027.01" and "RW-CASEOWN" holds "RU" in "QUEUE_AND_ALLOCATION" at "PM-2027.01"

  Scenario: AC11 A page bound and the second-approval switch are read from parameters (new, D-RCV-60)
    Given the parameters fake holds the page bound and the second-approval switch as parameter rows at the version in force
    Given the page bound parameter is changed in the parameters fake without a code release
    When "U-8104" calls GET /api/recovery/access/v1/admin/access-matrix/report
    Then the page bound in force applies to the answer and no build is needed

  Scenario: AC12 A call without an authenticated session is answered 401 on each operation (new, D-RCV-60)
    When an unauthenticated caller calls GET /api/recovery/access/v1/admin/access-matrix
    Then the response is 401 and no row is answered
    When an unauthenticated caller calls PATCH /api/recovery/access/v1/admin/access-matrix/RW-CASEOWN with If-Match "PM-2026.11" and the body capabilityArea "CASE_RECORD", letters "RU" and reason "Own case edit"
    Then the response is 401 and no change is stored and no rwb.access.AccessPolicyChanged.v1 is published
    When an unauthenticated caller calls POST /api/recovery/access/v1/admin/access-matrix/SY-AGENT/approve with the changeId of the pending change
    Then the response is 401 and the change stays "PENDING_APPROVAL"
    When an unauthenticated caller calls GET /api/recovery/access/v1/admin/access-matrix/report?version=PM-2027.01
    Then the response is 401 and no row is answered

  Scenario: AC13 A failed group mapping call leaves the matrix answered without its group block (new, D-RCV-60)
    Given the rwb-source-data contract mock answers 503 for GET /api/recovery/source-data/v1/iam-groups
    When "U-8101" calls GET /api/recovery/access/v1/admin/access-matrix
    Then the response is 200 with matrixVersion "PM-2026.11" and groupMappingAvailable false, and no error
```

AC1 and AC2 are the two criteria of RWB-E8-019, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the group mapping mock, so the ACE group of an agent is provable while the `rwb-source-data` contract is still a fake. AC3 to AC9 are new under D-RCV-60 and test only what this story adds: the three role classes in one matrix, the second approval of an agent's change, the report, the refusals, the break-glass warning, the announced change with its cache refresh, and the absence of personal data and of partner user identity.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The matrix in force is the only source of what a role or an agent may see and do: one row per role and capability area, with letters from `C`, `R`, `U`, `D` and `A` in that order or a dash | REQ-ACA-003; `permission.letters` DF-REF-043 and `matrix_version` DF-REF-044; TSD P4 v3 T6.1 |
| BR2 | Roles are held as data and a change takes effect without a code release; a change mints the next matrix version label and supersedes the row it replaces | REQ-ACA-002; FSD P4 v3 A2.30.1, BR-P4-030 |
| BR3 | A read and the report need Platform administration `R`, a set needs `U` and an approval needs `A`; a caller without the letter is refused with 403 and MSG-P4-002 and nothing is read or written | TSD P4 v3 T6.1 (RW-SECADM `CRUDA`, RW-AUDIT `R`); TSD P4 v3 T-A API-P4-007; GAP-0888 |
| BR4 | One matrix covers three role classes - `BANK_USER`, `PARTNER_USER` and `NON_HUMAN_ACTOR` - and an agent is a role of the non-human actor class that holds letters like a person; there is no separate agent grant table | TSD P4 v3 T3.2 LOV-ROLE-CLASS; TSD P4 v3 T6.1 (SY-AGENT and the four other system roles); REQ-ACA-010; NFR-051; ASM-1610 |
| BR5 | A change to a `NON_HUMAN_ACTOR` role is applied only when a second person, who is not the requester, approves it; the requester's own approval is refused with 403 and MSG-P7-002 and the change stays pending | TSD P4 v3 T6.3 (the author cannot approve); GAP-0886; ASM-1605 |
| BR6 | Every applied change publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, in the transaction that stores the change, with codes, letters, versions and a time and with no personal value; a consumer refreshes its cached permission data on it | Architecture v5 slide 14 and slide 43 (all consumers, cache refresh); NFR-040; ASM-1609 |
| BR7 | Every applied change appends exactly one entry to the local decision-record chain of DP-03 in the transaction that stores it, with the role, the area, the letters before and after, both versions, the reason and the parameter version | DP-03; R-UNI-39; RWB-E8-019 AC1 |
| BR8 | A change that cannot be recorded changes nothing: the answer is withheld with 503 and MSG-P7-003 and the letters, the version and the event are unchanged | RWB-E8-019 AC2; Principle 5; R-UNI-39 |
| BR9 | A version is never edited in place: a change writes a new version label and an end of validity on the row it replaces, so the version before stays readable for audit | TSD P4 v3 T4 version lifecycle; DP-15; ASM-1606 |
| BR10 | The group mapping is ACE data read through the `rwb-source-data` contract and never from `rwb_access`: this story reads no `v_ace_iam_group` row, holds no `iam_group` row, and writes no `role.entra_group` value | Ownership Map v1 (`iam_group`, `party_ext` = P1); DP-05; DF-ACE-301 to DF-ACE-304; GAP-0889 |
| BR11 | Partner users stay with S9 `rwb-partner`: the class `PARTNER_USER` is a value of this service's `role` table, and no partner user identity, partner firm, partner case or partner session is held, read or answered here | Ownership Map v1 (`partner_user` = S9); Architecture v5 slide 41; ASM-1609 |
| BR12 | A change carries `If-Match` with the matrix version the caller read; a stale value is refused with 409 and MSG-GEN-004, so two administrators cannot silently overwrite each other | Architecture v5 slide 42 (optimistic lock); DP-15 |
| BR13 | One `Idempotency-Key` answers one change: a replay answers the first answer, writes no second version, appends no second entry and publishes no second event | Architecture v5 slide 42; DP-09; DP-03 |
| BR14 | The report answers the rows at the version in force or at a version named in the query, with the version label, the time and the reason of each change, paged by parameter, in JSON or CSV; it is never a 404 and never names a person | REQ-ACA-013; FSD P4 v3 A2.30.3.3; GAP-0887 |
| BR15 | No value a business person may change is written in code: the role classes, the capability areas, the letters, the versions, the page bounds and the second-approval switch are rows, parameters or the contract's closed sets | FSD P4 v3 BR-P4-030; DP-06 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR4 are one read: `AccessMatrixService` answers from `role` and `permission` only, one row per role, and the class comes from `role.role_class`, so an agent has no separate path through the code.
- BR2, BR9 and BR12 are the write of `PermissionWriter`: a new version label, an end of validity on the replaced row, and an `If-Match` comparison before any row is touched.
- BR3 is the authorise call before the handler, with the letter named by the operation and never by the caller.
- BR5 is `AgentChangeApprovalService`: the class of the role decides whether the change is applied at once or held, and the requester's identity is compared with the approver's before anything is applied.
- BR6 is the outbox row of `AccessPolicyEventPublisher`, written with the entry and the letters, so a published event always describes a change that is stored.
- BR7 and BR8 are `DecisionRecordAppender` and the one transaction: the entry commits with the idempotency row and the outbox rows, and a failure rolls all of them back.
- BR10 is the absence of an ACE read: the module has no view, no synonym and no statement naming `v_ace_iam_group` or `iam_group`, and every group field arrives in the `rwb-source-data` answer.
- BR11 is the absence of a partner table: the module has no `partner_user` row and no partner field, and the class is a value it reads and reports.
- BR13 is the `idempotency_key` row of the platform library in `rwb_access`, written with the answer.
- BR14 and BR15 are `AccessMatrixReportService` and the parameters reader: the page bounds and the second-approval switch are read at request time with the version in force, and a changed value needs no build.

### 9. State transitions

This story changes no case state (TSD P4 v3 T4). It moves one matrix change and the matrix version of one role and area.

| From | Event | Condition | To |
|---|---|---|---|
| No change | A set is submitted for a `BANK_USER` or `PARTNER_USER` role | `R` and `U` held, `If-Match` current, the record written | `APPLIED`; the new matrix version is in force for that row |
| No change | A set is submitted for a `NON_HUMAN_ACTOR` role | `U` held, `If-Match` current | `PENDING_APPROVAL`; the row in force is untouched |
| `PENDING_APPROVAL` | A second person holding `A` approves | The approver is not the requester, `If-Match` current, the record written | `APPLIED`; the new matrix version is in force for that row |
| `PENDING_APPROVAL` | The requester calls approve | The approver holds the requester's identity | `PENDING_APPROVAL`; 403 with MSG-P7-002 |
| `PENDING_APPROVAL` | A later change of the same role and area is applied | The matrix version moved | `SUPERSEDED`; the later change is the one in force |
| No change | A set is submitted | No `U` letter, or `If-Match` stale, or a field invalid | No change; 403, 409 or 422 as the case is |
| No change | A set is submitted | The entry cannot be written | No change; 503 with MSG-P7-003 |

| Object | From | Event | To | Result |
|---|---|---|---|---|
| Matrix version of one role and area | Version N in force | A change is applied | Version N+1 in force | Version N keeps its end date and stays readable; the report answers both |
| Matrix version of one role and area | Version N+1 in force | A later change is applied | Version N+2 in force | Version N+1 is superseded on its end date |
| Matrix change | `PENDING_APPROVAL` | The change is refused by its approver or by a check | `REFUSED` | No row of the pending change is written and the version in force is untouched |
| Local chain | A change, or a refusal recorded at the service edge | Any | One entry appended with its `prev_hash` and `entry_hash` | No entry is ever updated or deleted |

The state set of a change and the labels of the transitions are Not specified in the source documents (GAP-0886; ASM-1605); the contract of RWB-P4-E8019-CON publishes the four values and this story writes them as that contract declares them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Security administrator (RW-SECADM) | Reads the matrix and the report, sets the letters of a role or an agent, and gives the second approval of an agent's change: `CRUDA` in Platform administration (TSD P4 v3 T6.1) |
| Risk and model risk officer (RW-RISK) | Reads the matrix and the report with `R` in Platform administration; the legacy story named this role as the approver of the journey, and the difference is carried in GAP-0888 |
| Compliance and PDPA officer (RW-COMPLY) | Reads the matrix and the report with `R`; no set and no approval |
| Internal audit (RW-AUDIT) | Reads the matrix and the report with `R`; changes nothing and reads every version |
| Platform administrator (RW-PLATADM) | Holds `CRUD` in Platform administration and may set a grant; the agent's identity and its runs are P10's |
| Case owner (RW-CASEOWN) and every case role | Holds a dash in Platform administration: refused with 403 and MSG-P4-002 on every operation of this story |
| Center of excellence analyst (RW-COE) | Holds `R` in Platform administration; the whole-file load of a matrix pack is RWB-P4-E1037-APP's and not this story's |
| A role of class `NON_HUMAN_ACTOR` (SY-AGENT and the other system roles) | No caller of this story: an agent holds letters and calls no operation of this service; its authorise calls are the guard's and its runs are P10's |
| The gateway-bff route | Calls the four operations on behalf of the signed-in administrator, one hop each, and passes `If-Match` and `Idempotency-Key` unchanged |
| `rwb-access` itself | Reads `role` and `permission` in its own schema, writes the letters, its chain and the platform library rows of the request; reads no ACE view and no P1 table |
| `rwb-source-data` (P1) | Owns the ACE group mapping and answers the read; this story never writes it and never holds a copy of it |
| `rwb-agent` (P10) | Owns the agent service identity, the allowed-action list and the run records; not read here |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right and to MSG-P7-002 for an approval by the requester, 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a stale version, 422 with MSG-GEN-001 for a field, and 503 with MSG-P7-003 for a change that cannot be recorded. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8019-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the row of the matrix, the class that decides the approval path, the scope, and the stored group answer |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the matrix in force; Write: the letters of one role and area under a new matrix version |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read only: named in the matrix answer as a conflict flag; the rows and the refusal are RWB-P4-AD005-APP's |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Named only: the masking profiles are RWB-P4-AD004-APP's and are not read or written here |
| DF-ACE-301 to DF-ACE-304 | `v_ace_iam_group` (P1) | entra_group, role_code, source_system, data_as_of | Returned through the `rwb-source-data` contract; not read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the change entry: `decision_code` DF-DEC-003, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the role code, the area, the letters before and after, both versions, the reason, the parameter version and the grant id, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the report's change time and reason |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a change or an approval | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` | the rows of the change entry, of `rwb.access.AccessPolicyChanged.v1` and of the record event | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

No row of `v_ace_iam_group`, of `iam_group`, of `public.customer` or of any other ACE table is read or written: they are ACE's and `rwb-source-data`'s under the ownership map, and the group fields arrive in the contract answer, not in a schema read (DP-05, BR10). No row of `partner_user` is read or written: partner users are S9's (BR11). No row of `decision_log_entry` is read or written: the central ledger is P7's and this story writes only its own local chain on `rwb.decision-record.v1`. No row of `masking_rule` is read: the masking profiles are RWB-P4-AD004-APP's and this story only names the table in the contract. Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P4 v3 T3.1.

Three values the sources do not fix are carried as placeholders. The paths, the request and answer field sets of the four operations, and the shape of the matrix version label a change mints, are Not specified in the source documents (GAP-0885; ASM-1604); FSD P4 v3 A2.30 names the journey and two rules and no operation, and TSD P4 v3 appendix T-A declares `GET /admin/roles` (API-P4-007) and no matrix operation. The four-eyes step of a non-human actor change, its approver and its state set are Not specified in the source documents (GAP-0886; ASM-1605); the four-eyes rule of TSD P4 v3 T6.3 belongs to a rule package version and is applied here by analogy. The field set and the columns of the report are Not specified in the source documents (GAP-0887; ASM-1606); the contract publishes them and this story answers them as it publishes them. The contract of RWB-P4-E8019-CON fixes all three and this story adds no field of its own.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/access-matrix` | P4 `rwb-access` | Query: `roleClass`, `capabilityArea`, `version`, `page`, `size` | `AccessMatrix`: `matrixVersion`, `items` of `roleCode`, `roleName`, `roleClass`, `defaultScope`, `letters` per capability area, `groupMapping` of group codes, source system and `dataAsOf`, `groupMappingAvailable`, `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Platform administration R, scope applied | Not applicable, read only |
| PATCH | `/api/recovery/access/v1/admin/access-matrix/{roleCode}` | P4 `rwb-access` | Path: `roleCode`. Header: `If-Match` (matrix version), `Idempotency-Key`. Body: `capabilityArea`, `letters`, `reason`, `secondApproverRole` | `AccessMatrixChange`: `changeId`, `roleCode`, `capabilityArea`, `lettersBefore`, `lettersAfter`, `matrixVersionBefore`, `matrixVersion`, `state`, `changedAt`, `changedByRole`, `reason`, with `Location` of the report read filtered to the role | 401 (MSG-P4-001); 403 (MSG-P4-002, MSG-P4-004 as a warning); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Platform administration U; 202 and state `PENDING_APPROVAL` where the role class is `NON_HUMAN_ACTOR` | `Idempotency-Key` required; a replay answers the first answer, writes no second version and publishes no second event |
| POST | `/api/recovery/access/v1/admin/access-matrix/{roleCode}/approve` | P4 `rwb-access` | Path: `roleCode`. Header: `If-Match`, `Idempotency-Key`. Body: `changeId`, `secondApproverRole`, `reason` | `AccessMatrixChange` with `state` `APPLIED` and the applied `matrixVersion` | 401 (MSG-P4-001); 403 (MSG-P4-002 on an absent A, MSG-P7-002 on the requester's own approval); 404 (MSG-GEN-001 naming the change); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Platform administration A, and the approver is not the requester of the change | `Idempotency-Key` required; a repeat approve of an applied change answers 409 and writes nothing |
| GET | `/api/recovery/access/v1/admin/access-matrix/report` | P4 `rwb-access` | Query: `roleClass`, `capabilityArea`, `version`, `page`, `size`; media type `text/csv` for the CSV form | `AccessMatrixReport`: `version`, `items` of `roleCode`, `roleClass`, `capabilityArea`, `letters`, `matrixVersion`, `changedAt`, `changedByRole`, `reason`, `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Platform administration R, scope applied | Not applicable, read only |

All four paths sit on the base `/api/recovery/access/v1` of DP-13. The write paths are fixed by this story and by its contract (GAP-0885; ASM-1604) and confirmed by the contract review before they are frozen. `page` defaults to the value of its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR15). The matrix version a change mints is the label the contract publishes; its shape is fixed there and no label is a constant in code.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Platform administration `R`, `U` and `A` checks behind the four operations, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The report page bounds, the second-approval switch of a non-human actor change and the parameter version recorded on the entry, with the version in force (DP-06) |
| GET | `/api/recovery/source-data/v1/iam-groups` | P1 `rwb-source-data` | The ACE group mapping per role: the mapped group codes, the role code, the source system and the date of the data (DF-ACE-301 to DF-ACE-304). The path and the shape are fixed by this story and its contract and raised with the P1 owner (GAP-0889; ASM-1608) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the authorise answer and the parameters row are cached for the session or the request, and the group mapping is cached for a short window whose length is Not specified in the source documents (GAP-0889; ASM-1608). The `rwb-source-data` read is enrichment of the matrix and never the source of a letter: a failure degrades the `groupMapping` block and never blocks a set, an approval or a report. No other operation of `rwb-case`, `rwb-source-data`, `rwb-agent`, `rwb-decision` or `rwb-partner` is called.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 `rwb-access`; consumed by every service that caches the permission data | roleCode | the change kind, the role code, the role class, the capability area, the letters before and after, the matrix version before and after, the approving role code and the effective time |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of the change: the role code, the area, the letters before and after, both versions, the reason and the time |

Both are CloudEvents 1.0 envelopes written from the outbox of the transaction that stores the change, so a published event always describes a change that is committed. The payload carries codes, letters, versions and times and no name, no e-mail address, no user reference and no personal field value (BR6, NFR-040). The name and the exact field set of `rwb.access.AccessPolicyChanged.v1` are Not specified in the source documents (GAP-0889; ASM-1609): Arch v5 slide 14 and slide 43 fix the topic and the event name and state that every consumer refreshes its cache on it, and the contract of RWB-P4-E8019-CON publishes the schema. `rwb.access.DoALimitChanged.v1` belongs to RWB-P4-E8008-APP and is not published here.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, the matrix in force is read from `rwb_access` on each call, and this story subscribes to no topic and writes no inbox row. The cache refresh of BR6 is the work of the consumers of the policy event and not of this service.

#### 12.5 Workflows and activities

None. The read, the set, the approval, the record and the report are synchronous work in the caller's thread. This story registers no workflow, no activity and no signal on the `rwb-access` queue, and the approval workflow of the kit belongs to `rwb-decision` (P7) and is not used for an administration change of this service.

#### 12.6 Schedules

None. Every operation is request-driven and the effective time of a change is the time of its record, which is data and not a Schedule. The six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role code, name, class, default scope and stored group answer of a matrix row |
| `permission` | P4 (`rwb_access`) | Read: the matrix in force. Write: the letters of one role and area under a new matrix version, and the end of validity of the row it replaces |
| `role_conflict` | P4 (`rwb_access`) | Read only: the conflict flag of a row; the rows are RWB-P4-AD005-APP's |
| `masking_rule` | P4 (`rwb_access`) | Named only in the contract; the profiles are RWB-P4-AD004-APP's and are not read here |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of a change. Read: the change time and the reason of a report row |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox rows of the entry and the policy event and the idempotency row of the request; no inbox row, because no event is consumed (DP-09; ASM-0074) |
| `v_ace_iam_group` and `iam_group` | ACE / P1 (`rwb_source_data`) | Not read and not written: the mapping arrives through the `rwb-source-data` contract |
| `partner_user` | S9 (`rwb_partner`) | Not read and not written: partner users are S9's |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's and the local record goes on `rwb.decision-record.v1` |

No ACE view and no `public` table is named as this service's and none is created here. `lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so the capability areas and the role classes (LOV-ROLE-CLASS) it accepts are the closed sets the contract publishes and the values the matrix carries, and the point is raised as the key's gap (GAP-0885; ASM-1604). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| source-data group-mapping fake | the `rwb-source-data` contract (GAP-0889; ASM-1608) | `GET /iam-groups` answering group "RWB-SIT-SY-AGENT01" mapped to role "SY-AGENT" with source system `ENTRA_ID` and `dataAsOf` "2026-11-20", a role with two groups, a role with no group, and a 503 for X12 |
| authorise fake | RWB-P4-E8019-CON, RWB-P4-E1037-CON | A granted answer for RW-SECADM with `CRUDA`, for RW-AUDIT, RW-COMPLY and RW-RISK with `R` in Platform administration, and a refused answer with MSG-P4-002 for RW-CASEOWN with a dash |
| parameters fake | the `rwb-case` contract RWB-P3-E1042-CON | The page bounds, the second-approval switch and the parameter version, with the version in force |
| decision-record fake | RWB-PLT-E1027-CON | The append of a change, the hash-link check, a seeded chain of the last changes and the forced failure AC2 needs |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-43 with the matrix grid, the change form, the approval panel and the report view |

Fake library version: Not specified in the source documents (DOR-RWB-P4-E8019-APP-22); no contract fake library version is recorded as published.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4 (the matrix read, the set, the approve and the report); consumed 3 | Base `/api/recovery/access/v1`; the own authorise operation, the `rwb-case` parameters read and the `rwb-source-data` group-mapping read, one hop and 2 s each |
| Kafka | Published 2 event types; consumed 0 | `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` and `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, through the outbox and the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None at run time | No file input and no file output: the CSV form of the report is a media type of the read and no upload is accepted, the matrix pack load being RWB-P4-AD002-APP's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `accessmatrix`, Java package `th.co.scb.ace.workbench.recovery.access.accessmatrix`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. Here the ACE group mapping is read through the `rwb-source-data` contract and no view is read | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module write of the letters against the monolith path (DP-13: the four paths of this service's own base), the direct read of `v_ace_iam_group` in the monolith (DP-05: the mapping through the `rwb-source-data` contract and no ACE read here), the decision log written in process (DP-03: the local record library and the shared topic) and the ace-web screen that set the letters (DP-19: a gateway-bff composite route over four operations). DP-01, DP-02, DP-09 and DP-11 govern the service baseline, the outbox and the one-hop budget of section 12.2; they are not in the pattern list the Work Package fixes for this story and are not claimed as patterns of it. The capability-area and role-class lists of DP-07 and `RWB-P3-E1043-CON` are not in that list either, so the accepted sets are the contract's closed sets and the values the matrix carries, and the point is raised as the key's gap (GAP-0885; ASM-1604).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccessMatrixController | Controller | The four operations: validation, the `If-Match` and `Idempotency-Key` handling, the RFC 9457 problem responses and the `Location` of the report read |
| AccessMatrixService | Service | The read of BR1 and BR4: the version in force, one row per role of the three classes, the letters per area and the class filter |
| PermissionWriter | Service | The write of BR2, BR9 and BR12: the version comparison, the minted version label, the letters of one role and area and the end of validity of the replaced row |
| AgentChangeApprovalService | Service | The four-eyes step of BR5: the class decision, the pending change, the requester comparison and the apply on approval |
| AccessMatrixReportService | Service | The report of BR14: the rows at the version asked for, the stable order, the paging from DP-06, the JSON and CSV forms and the empty answer |
| RoleReader | Repository | Read-only queries over `role`, `permission` and `role_conflict` in `rwb_access`, filtered by version, class and area |
| GroupMappingClient | Client | The `rwb-source-data` read of the group mapping, one hop, 2 s timeout, a breaker and a short cache; a failure degrades the block and never blocks the matrix |
| ParameterReader | Service | The page bounds, the second-approval switch and the parameter version through the parameters contract of DP-06, with the version in force |
| DecisionRecordAppender | Service | The entry of a change with its outbox rows, in the transaction that stores the change (DP-03) |
| AccessPolicyEventPublisher | Service | The outbox row of `rwb.access.AccessPolicyChanged.v1`, written with the change and with no personal value (BR6) |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations**

- This story creates no table. `role`, `permission` and `role_conflict` are created by RWB-P4-E1037-APP and the platform library tables by the service's own DB story, in the per-service Flyway sequence of DP-15; this story reads them and writes the letters of one row per change.
- Migration `V8019_1__permission_change_index.sql` adds one index on `permission (role_id, capability_area, matrix_version)` so the version in force and the report of one role and one area are read in one range scan. It adds no other object.
- No write statement touches `role`: the class, the scope and the stored group answer are read, so a change can never move a role between classes and never rewrite a group answer (BR4, BR10).
- No statement names `v_ace_iam_group`, `iam_group`, `partner_user`, `masking_rule` or `decision_log_entry`; the group fields arrive in the `rwb-source-data` answer and the record goes through RWB-PLT-E1027-CON (BR10, DP-03).
- The entry, the idempotency row and the two outbox rows commit in one transaction and the change row carries the standard `version` column, so a failure rolls everything back and two concurrent changes of one row cannot both commit (BR8, BR12).

**Configuration and reference data**

- The report page default and maximum, the second-approval switch of a non-human actor change and the window of the group-mapping cache are parameter rows of `rwb-case` read through DP-06 with the version in force; no bound and no switch is a constant in code (BR15). Their names are fixed by RWB-P4-E8019-CON.
- The capability areas and the role classes a request may name are the closed sets the contract publishes; the roles a request may name are the rows of `role` at the version in force (BR1).
- The rights are read from `permission` through the authorise operation of this service, with `R` for a read and the report, `U` for a set and `A` for an approval; no role code and no capability area is a constant in code (BR3).
- A matrix version label is minted by the write; the label of the version in force is a row and never a build value (BR2).

**Build steps**

1. `AccessMatrixController` and its validation over the four operations; tests for X1 and X2 with no write and no read of the matrix.
2. `RoleReader` and `AccessMatrixService` over a seeded version `PM-2026.11`; test AC3 with the three classes, the class filter and the unknown class refused.
3. `GroupMappingClient` over the group-mapping fake; tests for the enrichment of AC3, the absent block of X12 and the 2 s budget.
4. `PermissionWriter` with the `If-Match` comparison, the minted label and the end of validity of the replaced row; tests for AC8 and the 409 of X5.
5. `AgentChangeApprovalService` with the class decision, the pending change and the requester comparison; tests for AC4, including the proof that the permission row is untouched while the change is pending and that the requester's own approval is refused with MSG-P7-002.
6. `DecisionRecordAppender`, `AccessPolicyEventPublisher` and `IdempotencyStore` in one transaction; tests for AC2 with the forced failure, AC8 with one entry and one event, and the replay with no second event.
7. `AccessMatrixReportService` over a seeded chain of two versions; tests for AC5 with the JSON and CSV forms, the paging, the empty answer of BR14 and the absence of a name or a user reference of AC9.
8. `ParameterReader` over the parameters fake, so the story builds before `rwb-case` is in the environment; test that a changed bound or a changed switch is data and needs no build.
9. The contract-fake run of the four operations through the gateway-bff fake, so SCR-43 can be demonstrated while the route and the `rwb-source-data` service are being built.

**Feature switch.** `rwb.access.access-matrix`, read through the platform feature-flag library. Off answers the matrix of the baseline file, refuses a set with MSG-P4-002 and leaves a report readable, so a switched-off capability never hides the version in force. The switch changes no letter, no version and no approver.

**Done when.** The tests in section 16 pass; the matrix answers one row per role of the three classes with `SY-AGENT` among them and its group mapping from the `rwb-source-data` fake; a change to a person role is applied and answered with its new version; a change to an agent is held pending, refused to its requester with MSG-P7-002 and applied by a second administrator; the report answers both versions, the reason and the times and no person; one `rwb.access.AccessPolicyChanged.v1` is published per applied change and a consumer refreshes on it; a role without Platform administration `R` is refused with MSG-P4-002; a break-glass grant carries MSG-P4-004 with its end time; a forced record failure withholds the answer with MSG-P7-003 and changes nothing; and no statement in the package names an ACE view, a P1 table, a P7 table or a partner table.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. | This story, on all four operations |
| MSG-P4-002 | The caller holds no Platform administration `R` on a read or the report, no `U` on a set, or no `A` on an approval | You cannot {action} here. Your role does not include it. | This story, on all four operations |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the answer of a set or an approval, with the grant id recorded in the entry |
| MSG-GEN-001 | A required field is empty, `roleCode` is not a role of the matrix, `capabilityArea` is not of the set in force, `letters` are not `C`, `R`, `U`, `D`, `A` in order or a dash, or `changeId` names no change | Enter {field}. | This story, on the set and the approval, and on the read for the class filter |
| MSG-GEN-004 | `If-Match` names a matrix version that is not the version in force, a change of the same role and area is pending, or an approve names a change that is not `PENDING_APPROVAL` | Someone else changed this record. Reload it to see their change. | This story, on the set and the approval |
| MSG-P7-002 | The requester of a non-human actor change calls approve on that change | Not specified in the source documents (GAP-0886; ASM-1605) | This story, on the approval |
| MSG-P7-003 | The entry, the idempotency row or an outbox row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on all four operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the legacy texts of RWB-E8-019, and MSG-GEN-004 is the platform text. MSG-P7-002 is the four-eyes rule applied to a non-human actor change and its text is Not specified in the source documents (GAP-0886; ASM-1605); the message catalogue supplies it and the contract of RWB-P4-E8019-CON carries its `messageId` only. The legacy scope message MSG-P4-003 is not produced here, because a role grant is not a case and this story scopes no case; it is carried unchanged for the key and RWB-P4-E1039-APP answers it where a case is out of scope.

### 15. Screens and states

SCR-43 Roles and access is the screen, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), which renders the matrix grid and the report and calls the four operations of this story, one hop each. This story renders no screen surface of its own.

| Screen | State | What it shows |
|---|---|---|
| SCR-43 Roles and access | Matrix, grid | One row per role and agent with its class, its scope and its letters per capability area, filterable by class and area, with the group mapping of the `rwb-source-data` answer |
| SCR-43 Roles and access | Matrix, group mapping absent | The grid answered with the group block absent and a note that the mapping is not available, without an error and without a blocked screen |
| SCR-43 Roles and access | Change, form | One role, one capability area and the letters, with the reason and, for a non-human actor, the second approver role; the version the caller read is carried in `If-Match` |
| SCR-43 Roles and access | Change, applied | The 200 answer with the letters before and after, both versions, the state `APPLIED` and the time, and the change named in the report |
| SCR-43 Roles and access | Change, pending | The 202 answer of a non-human actor change with its state `PENDING_APPROVAL` and the approval action for a second administrator |
| SCR-43 Roles and access | Change, stale | The 409 of X5 or X6 with MSG-GEN-004 and a reload action |
| SCR-43 Roles and access | Change, refused | The 403 of X3 with MSG-P4-002 for a role without the letter, and the 403 of X7 with MSG-P7-002 for the requester's own approval |
| SCR-43 Roles and access | Change, break-glass | The warning of X11 with the end time of the grant, the change applied and recorded |
| SCR-43 Roles and access | Report | One row per role and area with the version, the time and the reason, paged, with a CSV action |
| SCR-43 Roles and access | Report, empty | An empty report with total 0 and no error, also for a class or an area with no row |
| SCR-43 Roles and access | Not recorded | The 503 of X9 with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-43 Roles and access | Empty | Not specified in the source documents (CG-ALL-5694) |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-5694) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-5694) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-5694) |

The legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority in its screen table although a role grant sits on neither; the target screen is SCR-43 Roles and access (FSD P4 v3 screen list, FEAT-ADM-14), and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. This story serves the matrix, the change and the report panels of that screen only; the masking profile panel is RWB-P4-AD004-APP's, the scope panel is RWB-P4-AD003-APP's and the separation of duty panel is RWB-P4-AD005-APP's. SCR-39 carries no state in this story; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-5692). SCR-41 carries no state in this story; its empty state is in Screen Specifications v1 and its loading, error and no access states are Not specified in the source documents (CG-ALL-5692; CG-ALL-5693).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-019-01 | AC1, BR1, BR2, BR7 | Component | Matrix version `PM-2026.11` in force; a change to one role and area applied as `PM-2027.01`; the letters, the reason and the version recorded; the group-mapping fake answers the agent's group |
| TC-E8-019-02 | AC2, BR8 | Component | The record store forced to fail during a change: 503 with MSG-P7-003, no letters changed, no version minted and no event; a retry completes exactly one entry |
| TC-E8-019-03 | Access | Component | A role with a dash in Platform administration refused with MSG-P4-002 on the read, the set and the approve; the legacy level Access maps to Component |
| TC-E8-019-04 | Principle 5 | NFR | The entry and the outbox row forced to fail under load: every failure is a 503 with MSG-P7-003, no partial change is ever readable and no event is published; the legacy level Principle 5 maps to NFR |
| TC-E8-019-05 | AC3, BR4, BR10 | Component | The seeded matrix of `PM-2026.11` with RW-CASEOWN as `BANK_USER` and SY-AGENT as `NON_HUMAN_ACTOR`; the class filter for the three values; an unknown class refused with MSG-GEN-001; the group mapping from the `rwb-source-data` fake and its 503 case |
| TC-E8-019-06 | AC4, BR5, BR12 | Component | A pending change of SY-AGENT in `TREATMENT_AND_OFFER` with letters `RU`; the requester's own approval refused with MSG-P7-002; the second administrator's approval applied as `PM-2027.01`; a stale `If-Match` refused with MSG-GEN-004 |
| TC-E8-019-07 | AC5, BR14 | Component | The report of `PM-2026.11` and `PM-2027.01` with the reasons and the times; the JSON and CSV forms; the paging; an area with no row answering total 0 |
| TC-E8-019-08 | AC7, AC8, BR6, BR13 | Contract | An applied change with a break-glass grant carrying MSG-P4-004 and the grant id; one `rwb.access.AccessPolicyChanged.v1` with the codes and versions; the replay of the same `Idempotency-Key` with no second event |
| TC-E8-019-09 | AC9, BR11 | NFR | The matrix and the report of `PM-2027.01` scanned for a name, an e-mail address, a user reference and a personal value; the PARTNER_USER class present and no partner identity, firm or case in `rwb_access` |
| TC-E8-019-10 | AC6, BR3 | Component | U-8105 holding RW-CASEOWN with `-` in PLATFORM_ADMINISTRATION: the read and the set refused with MSG-P4-002, no row answered, no change stored, no decision-record entry and no event published; the authorise fake as in GAP-0888 |
| TC-E8-019-11 | AC10, BR9 | Component | The matrix in force `PM-2026.11` with `R` for RW-CASEOWN in `QUEUE_AND_ALLOCATION`; a change applied as `PM-2027.01`; the row of `PM-2026.11` read unchanged with its end date |
| TC-E8-019-12 | AC11, BR15 | Component | The parameters fake with the page bound and the second-approval switch changed without a build; the report answered with the page bound in force |
| TC-E8-019-13 | AC12 | Component | A caller with no authenticated session calls each of the four operations: 401 on each, no row answered, no change stored, no decision-record entry and no event published |
| TC-E8-019-14 | AC13 | Component | The rwb-source-data fake answering 503 for the group mapping: the matrix of PM-2026.11 answered 200 with groupMappingAvailable false and no error |

The four legacy rows are kept: TC-E8-019-01 for AC1, TC-E8-019-02 for AC2, TC-E8-019-03 for the access refusal and TC-E8-019-04 for the forced record failure; five rows are added for the new criteria of this story. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under R7.2 s16. The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the role classes, the capability areas, the letters, the versions, the page bounds and the second-approval switch are rows, parameters or the contract's closed sets, and a test proves that a changed bound or a changed switch needs no build (BR15).
- No personal data anywhere: the request, the matrix, the report, the entry and the event carry role codes, classes, scopes, letters, versions, times and a reason; no name, no e-mail address, no user reference and no personal field value appears in an answer, a row, a fake or a test (BR9, NFR-040).
- ACE data only through the owner's contract or the service's own `v_ace_*` views: this service has no ACE view, so the group mapping arrives through the `rwb-source-data` contract and no `v_ace_iam_group` or `iam_group` row is read (DP-05, BR10).
- No read of another service's tables (DP-01): `partner_user` is S9's, `masking_rule` is named only and owned by RWB-P4-AD004-APP, `decision_log_entry` is P7's, and no join crosses a schema.
- One matrix, three classes: an agent holds letters in the same `role` and `permission` rows as a person, so no second grant table can drift from the first (BR4).
- Two people for an agent: a non-human actor change cannot be applied by the administrator who requested it, and the check happens before any row is written (BR5).
- No change without its record: the entry commits with the change, and the answer is withheld with MSG-P7-003 when it cannot be written (BR8, R-UNI-39).
- One writer for a version: the version in force is superseded and never edited, and two administrators cannot overwrite each other because the write carries `If-Match` (BR9, BR12).
- One key, one change: the `Idempotency-Key` is stored with the answer, so a retry after a timeout cannot mint a second version, a second entry or a second event (BR13).
- The report cannot be gamed: it answers an empty page rather than a 404 and never names a person, so a caller cannot learn which role holds nothing (BR14).
- Every example, fixture and test payload is synthetic; no production entitlement, group or personal value is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release | Program, Access and administration | FEAT-ADM-14, FEAT-ACA-04 | All recovery processes | BR2, BR9, BR15 | TC-E8-019-01, TC-E8-019-06 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do | Program, Access and administration | FEAT-ADM-14, FEAT-ACA-04 | All recovery processes | BR1, BR4, BR12 | TC-E8-019-01, TC-E8-019-05, TC-E8-019-06 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | Program, Access and administration | FEAT-ADM-14 | All recovery processes | BR4, BR5 | TC-E8-019-05, TC-E8-019-06 |
| REQ-CWC-018 | A model or agent writing to a queue passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version | Program, Workflow and case work | FEAT-ADM-14 | All recovery processes | BR4, BR6 | TC-E8-019-05, TC-E8-019-08 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 | FEAT-ADM-14 | All recovery processes | BR3, BR14 | TC-E8-019-03, TC-E8-019-07, TC-E8-019-09, TC-E8-019-10 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 control access by role and by agent: reviews and sets what each role and each agent may read and do, reports the matrix, records the result with the rule version | Sections 1, 4, 7 (AC1), 8, 12.1, 12.3 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7 (AC2), 8 (BR8), 12.1, 14 |
| The permission checks: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 7 (AC6), 8 (BR3), 10, 12.1, with the target right of Platform administration carried in GAP-0888 |
| The data rows `role` DF-REF-034 to DF-REF-038, `rule_row` DF-REF-001 to DF-REF-015, `decision_log_entry` DF-DEC-001 to DF-DEC-018 and `v_ace_iam_group` DF-ACE-301 to DF-ACE-304 | Sections 11, 12.7; the rule rows are RWB-P4-E8007-APP's, the ledger is P7's and the view is read through the P1 contract |
| The endpoints `/admin/rule-versions` and `/admin/rule-versions/{versionId}/approve` as the story listed them | Section 12.1, replaced by the four matrix operations; the rule-version operations are RWB-P4-E8007-APP's |
| The legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority as the story named them | Section 15, carried to SCR-43 Roles and access |
| MSG-P4-004, MSG-P4-002, MSG-P4-001, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| TC-E8-019-01 to TC-E8-019-04 | Section 16 |
| Legacy key RWB-E8-019, story RWB-P4-E8019-APP, contract RWB-P4-E8019-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The matrix pack load and the whole-file validation of a matrix version, its difference report and its approve path: RWB-P4-AD002-APP and RWB-P4-E1037-APP, whose `POST /admin/reference-loads` and approve operations this story neither calls nor redefines.
- The matrix read over a role and its letters as the administration view already publishes it: RWB-P4-E1037-APP's `GET /admin/roles` (API-P4-007) and RWB-P4-E1019-APP's role, class and conflict rows. This story answers the matrix as it applies to non-human actors and the report, and adds no field to that answer.
- The masking profiles per role and field: RWB-P4-AD004-APP; the `masking_rule` rows are named here and not read.
- The separation of duty pairs and their refusal at sign-in: RWB-P4-AD005-APP.
- The scope per role and the scope descriptor: RWB-P4-AD003-APP; the default scope is read here and not set.
- Partner users: their identity, firm, cases, session and portal are S9 `rwb-partner`'s; only the `PARTNER_USER` role class is in scope here.
- The ACE group mapping itself, the `iam_group` rows and the ACE views behind them: P1 `rwb-source-data` and the ACE team; this story reads the mapping through the contract and writes no group value.
- The agent runtime, the agent service identity, the prompt and policy store, the allowed-action list and the run records: P10 `rwb-agent`.
- The central decision ledger, the query API over `rwb_decision` and the chain verification: P7 `rwb-decision`; the `-ITG` copy of the end-to-end proof: no ITG story is split from this legacy key.
- The delegation of authority table and its limits: RWB-P4-E1038-APP and RWB-P4-E2013-APP.
- The access log, its search and export, and break-glass grants: RWB-P4-E1039-APP; only the warning MSG-P4-004 and the grant id on the entry are this story's.
- The screen SCR-43 Roles and access itself, its other panels and its composite route specification: RWB-PLT-N001-CON.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: an OPS story of this legacy key.
