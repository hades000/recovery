# RWB-P3-E1019-CON Roles, teams and queues as data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1019-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E1019-CON-16) |
| Depends on (build) | RWB-PLT-E1037-CON (guard library, DP-08) |
| Contract dependencies | RWB-P4-E1037-CON (rwb-access authorise contract, DP-08) |
| Contract version | v1 (path /api/recovery/case/v1; version frozen when consuming stories pass their contract tests) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-008, FR-P3-026) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-019 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 21 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the rwb-case case and workflow service**, I want **the contract baseline for queues, queue membership, queue measures, lists of values and reference loads, published on Day 1 with a working fake**, so that **the rwb-case app stories, the case list, allocation, transfer, the gateway and the other services can build and test against stable request and response schemas before the service exists**.

This is the contract story of legacy RWB-E1-019. It publishes, under `/api/recovery/case/v1` (DP-13):

- OpenAPI 3.1 documents for the queue resources, the list-of-values resource and the two reference-load operations, with the error envelope, the `Idempotency-Key` rule on every POST and the versioning rule.
- AsyncAPI 3.0 schemas for the `rwb.case.events.v1` events that carry a queue code and an owner reference, on topic naming `rwb.case.<Event>.v1` (DP-14).
- The table-and-index baseline for the nine contract tables of section 12, so the DB story and the fake agree with the service.
- A contract fake that answers every published operation with the examples in this document.

The role, permission and scope resources are **not** published here: they belong to rwb-access (P4) and are consumed through the rwb-access contract (DP-08; contract dependency of RWB-P3-E1019-APP is RWB-P4-E1037-CON). The parameter and reference-data contracts are published by their own stories (DP-06, DP-07). This story builds nothing that writes a business table; it has no build dependency and starts on Day 1.

### 2. Business rationale

The legacy story exposed its behaviour only through published Java interfaces inside one application. In the target, the other services, the gateway and the case list reach the queue data over HTTPS, and they cannot wait for the rwb-case build. A published contract on Day 1 with a fake removes that wait (DP-11): allocation, transfer and the case list code against the queue and reference-load schemas from the first sprint, contract tests fail the build when a field drifts, and the AsyncAPI schema is the single place where the queue code and the owner reference inside `rwb.case.events.v1` are agreed.

It also fixes the two boundaries the realignment depends on: the queue and reference resources are served by rwb-case, the role and permission resources are consumed from rwb-access, and nothing in the contract invites a caller to ask rwb-case for a role list. That is what keeps REQ-CWC-006 and REQ-ACA-002 true after the split, and it is the artefact the DB story and the app story are verified against.

### 3. Preconditions

- The service naming rules of Template and Rules §R4 are fixed and used unchanged: schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1`, event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` (namespace `rwb-recovery`); the Java package is `Not specified in the source documents (CG-ALL-3501)`.
- The nine contract tables of section 12 are agreed: `queue`, `queue_member`, `queue_measure`, `lov_value`, `reference_row`, `reference_version`, `assignment`, `task` and, for the read-only counts, `recovery_case`. Ownership comes from the ownership map only: all nine are P3.
- The field identifiers DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038, DF-WRK-045 to DF-WRK-052, DF-RPT-020 to DF-RPT-030, DF-REF-028, DF-REF-029 and DF-REF-181 to DF-REF-184 are taken from the technical specification, character for character.
- The legacy message IDs MSG-P1-002, MSG-GEN-001, MSG-GEN-002, MSG-P7-002, MSG-P3-015 and MSG-P4-002 are used unchanged in the error examples.
- The column definitions of each reference table code and the element types of the reference resources are not specified in the source documents (GAP-0697); the load row check reads the per-code column definitions as data held beside LOV-REF-TABLE, and the placeholder stays in sections 11 and 13 until the data steward agrees them.
- The legacy rule-version endpoints (GET admin rule-versions and POST admin rule-versions/{versionId}/approve) are not operations of this contract; the RWB-E1-019 dependency is read as the queue and allocation work now owned by RWB-P3-E1019-APP and this contract (GAP-0857).
- No reader of this contract keeps a cache of queue or role data beyond one call (GAP-1177).
- The per-service login of rwb-case is not named here; where a credential or a grantee must appear in an example, the text reads the rwb-case login (DP-02), whose name is Not specified in the source documents (GAP-0678; ASM-1225).
- No approval is required to publish a Draft contract: the baseline is published at status Draft (realignment v1) and the version is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. The contract author writes the OpenAPI 3.1 document for the six published operations, one tag per resource: Queues, Queue membership, Queue measures, Lists, Reference loads. The author also publishes the Queues template as an xlsx workbook with one header row per sheet, a column per queue and queue_member field, and one check per required column (GAP-0681).
2. The author writes the AsyncAPI 3.0 document for `rwb.case.events.v1`, with the channels and message schemas of the events that carry a queue code or an owner reference.
3. The author writes the nine §12 tables into this story and generates the schema files from them, so the document, the tables and the fake cannot drift.
4. The lint and schema steps run: OpenAPI 3.1 validation, sibling-file rule, operation-id rule, error-envelope rule, `Idempotency-Key` on every POST, and an AsyncAPI validation with CloudEvents 1.0 headers.
5. The contract fake is generated from the documents; it answers every operation and every example in this story, including the error examples of section 14.
6. The documents and the fake are published to the contract registry; the consuming stories (RWB-P3-E1019-APP, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1023-APP, the gateway-bff stories and RWB-P2-E2036-CON, which forwards the placement operation) pin the version.
7. A contract test in this story runs the fake against the documents on every change; a breaking change raises a new version and marks the old one deprecated.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An operation is published without a 4xx error envelope | The lint step fails the build and the document is not published | Lint finding, no message id | AC4 |
| X2 | A POST operation declares no `Idempotency-Key` header | The lint step fails the build | Lint finding, no message id | AC3 |
| X3 | A path is published outside `/api/recovery/case/v1` | The lint step fails the build; the monolith base is never republished | Lint finding, no message id | AC6 |
| X4 | An example carries a personal name, an email address or an account number | The review step rejects the example; only user IDs and case numbers appear | Review finding | AC5 |
| X5 | The AsyncAPI schema adds a field holding a personal name | The schema review rejects the change; the queue and owner fields stay codes and references | Review finding | AC5 |
| X6 | A consumer needs a field that no source defines | The field is not invented: the example carries the placeholder and a gap is raised | GAP-0680 | AC2, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and a fake; builds nothing and depends on nothing |
| Negotiable | Field order, example values and error detail layout are open until the version is frozen |
| Valuable | Allocation, transfer, the case list and the gateway start on Day 1 against the fake |
| Estimable | Six operations, two event schemas, nine tables, one fake |
| Small | One sprint for the documents and the fake, with the lint and contract tests |
| Testable | Each criterion is a schema or lint assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: rwb-case contract baseline for queues, membership, measures, lists and reference loads

  Background:
    Given the rwb-case base path is /api/recovery/case/v1 and the schema is rwb_case
    Given the contract version is v1

  Scenario: AC1 The queue document is published and complete (new, D-RCV-60)
    Given the OpenAPI 3.1 document for the Queues tag
    When it is validated and linted
    Then it declares GET /queues and GET /queues/{queueId}/cases and POST /queues/{queueId}/placements
    Then the Queue schema carries the queue code, queue name, team code, role code, assignment method, capacity cap, overflow queue and table version, matching DF-WRK-001 to DF-WRK-008 and DF-WRK-038
    Then every response carries the schema `rwb_case` table name and the field names of the technical specification, character for character

  Scenario: AC2 The membership and measure documents are published (new, D-RCV-60)
    Given the schemas QueueMember and QueueMeasure in the same document
    When the document is validated
    Then QueueMember carries the member id, queue id, user id, capacity, skill codes, table version, valid from and valid to, matching DF-WRK-045 to DF-WRK-052
    Then QueueMeasure carries the measure id, queue id, as-of, depth, unassigned, average age, maximum age, owner minimum, owner maximum, breached and status, matching DF-RPT-020 to DF-RPT-030
    Then no field is added that no source defines, and a needed field with no source carries the placeholder

  Scenario: AC3 The lists and reference-load document is published (new, D-RCV-60)
    Given the OpenAPI 3.1 document for the Lists and Reference loads tags
    When it is validated and linted
    Then GET /admin/lists/{listCode} returns the values of one list in force
    Then POST /admin/reference-loads takes multipart/form-data with file, table and validFrom, requires the Idempotency-Key header and answers 201 with the load id, table, valid from, status and row count
    Then POST /admin/reference-loads/{loadId}/approve answers 200 with the approved load and requires no Idempotency-Key on approve
    Then both operations answer 401, 403, 404, 409, 422 and 503

  Scenario: AC4 The error envelope and the legacy messages are published (new, D-RCV-60)
    Given the error envelope is one problem schema used by every operation
    When the error examples are validated
    Then the envelope carries the type, title, status, detail, instance and an errors list with row and field
    Then the examples carry MSG-P1-002, MSG-GEN-001, MSG-GEN-002, MSG-P7-002, MSG-P3-015 and MSG-P4-002 unchanged
    Then the 409 example for an author who approves their own load names MSG-P7-002 and the 422 example names the failing row and check for MSG-P1-002

  Scenario: AC5 The queue-carrying events are published in AsyncAPI (new, D-RCV-60)
    Given the AsyncAPI 3.0 document for the topic rwb.case.events.v1
    When it is validated
    Then the document declares rwb.case.CaseAllocated.v1 and rwb.case.CaseAllocationFailed.v1 as CloudEvents 1.0 messages keyed by the case id
    Then both payload schemas name the queue code field that GET /queues returns and the owner reference field that GET /queues/{queueId}/cases returns
    Then no payload schema carries a personal name, an email address or an account number
    Then a field required by a consumer and defined by no source carries the placeholder rather than an invented name

  Scenario: AC6 The tables, versioning and the fake agree (new, D-RCV-60)
    Given the nine contract tables of section 12 and the published documents
    When the contract test runs
    Then every table, key and index named in section 12 appears in the schema baseline file with its P3 owner
    Then every path sits under /api/recovery/case/v1 and no path of rwb-access is published here
    Then the fake answers every operation and every example, and a breaking change raises a new version and marks v1 deprecated

  Scenario: AC7 The assignment method, the cap parameter and the version status are published (new, D-RCV-60)
    Given the business rules BR2, BR3 and BR6 of section 8
    When the contract documents are validated
    Then the assignment method of the Queue schema is one of ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL
    Then the capacity cap range is 1 to 500 and is published as the parameter `queue.cap.max`, never as a constant in the schema
    Then the version status vocabulary is LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED
```

These criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here, and every business value in the examples comes from the legacy story or the technical specification, character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every queue in the contract belongs to one team code and one role code | Legacy BR1; DF-WRK-004, DF-WRK-005 | AC1; TC-P3-E1019-CON-01 |
| BR2 | The assignment method is one of ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL | LOV-ASSIGN | AC1, AC7; TC-P3-E1019-CON-01, TC-P3-E1019-CON-07 |
| BR3 | The capacity cap range is 1 to 500, published as the parameter `queue.cap.max` and never as a constant in the schema | Legacy BR8; DL23 (ASM-1232, ASM-1237, ASM-1259, ASM-1560) | AC7; TC-P3-E1019-CON-07 |
| BR4 | A load is refused whole when any row fails, and the refusal names rows and checks | Legacy BR2; MSG-P1-002 | AC3, AC4; TC-P3-E1019-CON-03, TC-P3-E1019-CON-04 |
| BR5 | The author of a load cannot approve it, and the contract publishes the refusal as 409 | Legacy BR4; MSG-P7-002 | AC4; TC-P3-E1019-CON-04 |
| BR6 | The version status vocabulary is LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED | LOV-VERSION-STATUS (TSD P3 v3 T3.2) | AC7; TC-P3-E1019-CON-07 |
| BR7 | Every POST requires an `Idempotency-Key`; a repeat returns the first result | Legacy contract, idempotency row | AC3; TC-P3-E1019-CON-03 |
| BR8 | The contract publishes rwb-case resources only; role, permission and scope resources are rwb-access | DP-08; ownership map | AC6; TC-P3-E1019-CON-06 |

### 9. State transitions

None in this story: a document has no runtime state. The states the documents describe are the queue version states of the rwb-case reference registry, published as LOV-VERSION-STATUS in the `status` field of the load schema (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED), and the state machine itself is the one specified in RWB-P3-E1019-APP section 9. This story fixes only the vocabulary and the HTTP status that accompanies each transition: 201 on load, 200 on approve, 409 when the author approves, 409 when no earlier version exists, 422 when a row fails.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the documents and the fake |
| The service owner of rwb-case | Approves a breaking change and a version freeze |
| The consumer teams (allocation, transfer, case list, gateway) | Read the documents, pin a version, raise a change request |
| rwb-access (P4) | Owns the role, permission and scope contract this document only references |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

Role names appear in the examples only as role codes, resolved by rwb-access at run time (DP-08). The grant of RW-TEAMMGR for the TEAM, QUEUE and QUEUE_MEMBER tables is recorded as rwb-access data by the access owner (GAP-0683); a refused approval returns 403 MSG-P4-002. No personal name, no email address and no credential appears in a document or an example; where a grantee must be named, the example says the rwb-case login (DP-02), whose name is Not specified in the source documents (GAP-0678; ASM-1225).

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Field identifiers published | DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038 (queue); DF-WRK-045 to DF-WRK-052 (queue member); DF-RPT-020 to DF-RPT-030 (queue measure); DF-REF-028, DF-REF-029 (list of values); DF-REF-181 to DF-REF-184 (reference row); DF-REF-159 to DF-REF-180 (reference version, referenced only) | DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038, DF-WRK-045 to DF-WRK-052, DF-RPT-020 to DF-RPT-030, DF-REF-028, DF-REF-029, DF-REF-181 to DF-REF-184, DF-REF-159 to DF-REF-180 |
| Field identifiers not published, consumed instead | DF-REF-035 (`role.role_code`) and the permission, scope and delegation fields of rwb-access: reached over the rwb-access contract, never in this document (DP-01, DP-08) | DF-REF-035 |
| Field identifiers with no source | Queue-measure columns are DF-RPT-020 to DF-RPT-030 (TSD P3 v3 T3.1); list-of-values columns are DF-REF-028 and DF-REF-029 at minimum; any further `lov_value` column is added by a later migration, not by a guess (GAP-0680; ASM-1227) | Not specified in the source documents (DOR-RWB-P3-E1019-CON-7) |
| File format | The Queues template is an xlsx workbook with the two sheets QUEUE and QUEUE_MEMBER, sent as multipart on the load operation; it has one header row per sheet, a column per queue and queue_member field and one check per required column; v1 does not fix the column order (GAP-0681; ASM-1228) | Not specified in the source documents (DOR-RWB-P3-E1019-CON-7) |
| Personal data in examples | None. Members and approvers appear as user IDs only (U-11, U-12, U-90) | None |

The documents carry no value that no source holds. Where a consumer needs a field that neither the legacy story nor the technical specification defines, the schema carries the placeholder text and the change waits for the gap to close; this is a draft baseline, so a new version can add the field without breaking a consumer.

### 12. Contract

**12.1 REST operations provided**

| Operation | Document | Request | Responses | Owner |
|---|---|---|---|---|
| GET /api/recovery/case/v1/queues | queues.yaml | Optional team code, role code, assignment method filter | 200 QueueList; 401; 403 MSG-P4-002; 503 | P3 |
| GET /api/recovery/case/v1/queues/{queueId}/cases | queues.yaml | Path queueId; paging | 200 CaseListRowPage; 401; 403; 404; 503 | P3 |
| POST /api/recovery/case/v1/queues/{queueId}/placements | queues.yaml | Path queueId; body caseId, reason; `Idempotency-Key` | 202 Placement; 401; 403; 404; 409; 422; 503 | P3 |
| GET /api/recovery/case/v1/admin/lists/{listCode} | lists.yaml | Path listCode, for example LOV-ASSIGN | 200 ListValues; 401; 403; 404; 503 | P3 |
| POST /api/recovery/case/v1/admin/reference-loads | reference-loads.yaml | `multipart/form-data`: file (Queues template, GAP-0681), table, validFrom; `Idempotency-Key` | 201 ReferenceLoad; 401; 403 MSG-P4-002; 409; 413; 422 MSG-GEN-001, MSG-GEN-002, MSG-P1-002; 503 | P3 |
| POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve | reference-loads.yaml | Path loadId; optional note | 200 ReferenceLoad; 401; 403; 404; 409 MSG-P7-002 or the version changed; 503 | P3 |

The rollback and verify operations of reference loads (POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback and .../verify) are owned by P3 and are published in a later rwb-case contract story; this document does not claim them (GAP-0682).

No queue membership operation is published by this document; the QueueMember schema is carried in queues.yaml as a schema only (GAP-1176).

The placement operation above is owned by P3 and keeps its behaviour; the rwb-integration admission and forwarding operation on its own base is contracted in RWB-P2-E2036-CON and is not published here (GAP-0670).

**12.2 REST operations consumed**

| Operation | Provider | Why this document needs it | Pattern |
|---|---|---|---|
| POST /api/recovery/access/v1/authorise | rwb-access (P4) | The examples show the 403 and the approval refusal raised by the guard, with MSG-P4-002 and MSG-P7-002 | DP-08, DP-11 |
| GET /api/recovery/access/v1/admin/roles | rwb-access (P4) | The queue and member examples carry role codes that exist in that list; this document references it and never republishes it | DP-08, DP-11 |

**12.3 Events published**

| Event | Topic | Message schema | Payload carries |
|---|---|---|---|
| rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | CaseAllocated | Case id, queue code, owner reference, table version of the queue version applied, occurred at |
| rwb.case.CaseAllocationFailed.v1 | rwb.case.events.v1 | CaseAllocationFailed | Case id, tried queue code, failure reason, occurred at |

Both are CloudEvents 1.0, keyed by case id, with no personal name, no email address and no account number. This story publishes the schemas only; the behaviour that emits them belongs to RWB-P3-E1020-APP, and the topic naming library to RWB-PLT-E1047-CON (DP-14). `rwb.case.CaseCreated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.case.TimerBreached.v1` are contracted in the stories that own their behaviour.

**12.4 Events consumed**

None. The contract baseline of this story is requested synchronously and consumes no event.

**12.5 Workflows and activities**

None. The contract declares no Temporal workflow, activity or signal; the `rwb-case` task queue and `CaseWorkflow`, `DailyCaseRun` and the `allocate`, `transfer`, `rebalance` activities are declared in the contracts of the stories that own them.

**12.6 Schedules**

None. No Temporal Schedule is declared here; the legacy daily 00:05 queue job is not carried by this story (DP-10 is not applied to this legacy key).

**12.7 Tables owned**

| Table | Schema | Key and indexes to publish in the baseline file | Owner | Rows exposed |
|---|---|---|---|---|
| queue | rwb_case | PK id; unique queue_code; team_code and role_code codes; overflow_queue_id to queue | P3 | GET /queues |
| queue_member | rwb_case | PK id; queue_id to queue; partial index on queue_id where active; partial index on user_id where active | P3 | QueueMember schema |
| queue_measure | rwb_case | PK id; queue_id to queue; index on queue_id and as-of | P3 | QueueMeasure schema |
| lov_value | rwb_case | PK id; unique on list code and value code | P3 | GET /admin/lists/{listCode} |
| reference_row | rwb_case | PK id; version_id to reference_version | P3 | ReferenceLoad row count |
| reference_version | rwb_case | PK id; unique on table code and version number | P3 | ReferenceLoad status |
| assignment | rwb_case | PK id; case_id, task_id, queue_id | P3 | Queue membership view |
| task | rwb_case | PK id; case_id; queue_id | P3 | GET /queues/{queueId}/cases |
| recovery_case | rwb_case | PK id; index ix_case_owner_status | P3 | GET /queues/{queueId}/cases, read only |

The tables and indexes arrive with RWB-P3-E1019-DB on the per-service Flyway sequence after the V0001 baseline (DP-15; RWB-PLT-E1044-CON). This document adds no table outside `rwb_case` and no reference to a table in `rwb_access`. Roles, permissions, scope, masking and delegation stay with rwb-access; `team_code` stays reference data here and only `role_code` is carried, as a code validated at load time over the rwb-access authorise contract (DP-08); the column list of the split is confirmed with P4 in RWB-P4-E1037-CON (GAP-0679; ASM-1226), so the documents never publish a role resource. Roles are loaded in rwb-access (P4) and read here by contract over GET /admin/roles on the rwb-access contract, while teams, queues and the reference rows stay in rwb_case (GAP-3159); the queue names its team code, role code and version as P3 values, and the role, its rights and its scope are read from P4 (GAP-1176).

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| rwb-case queue and reference fake (this story) | The six published operations | RWB-P3-E1019-APP, RWB-P3-E1020-APP, RWB-P3-E1021-APP, RWB-P3-E1023-APP, gateway-bff stories |
| rwb-access contract fake (P4) | POST /authorise, GET /admin/roles | The error and approval examples of this document, and every role check of the app story |
| rwb-case reference and parameter fakes (P3) | The reference-data and parameter contracts | The list-of-values and `queue.cap.max` examples |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 6 operations under `/api/recovery/case/v1` | 2 operations (both to rwb-access) | OpenAPI 3.1, one hop, 2 s timeout, `Idempotency-Key` on every POST |
| Kafka | 2 message schemas on `rwb.case.events.v1` | 0 | AsyncAPI 3.0, CloudEvents 1.0, keyed by case id |
| Temporal | 0 | 0 | Declared by the stories that own the workflows |
| File | 1 (xlsx upload on the load operation) | 0 | `multipart/form-data`, read in the request, no claim-check store |

### 13. Solution plan

**Deliverables.** `queues.yaml`, `lists.yaml`, `reference-loads.yaml` (OpenAPI 3.1); `rwb.case.events.yaml` (AsyncAPI 3.0); `schema-baseline.sql` (the nine tables of section 12, for reference only — the executable migration is RWB-P3-E1019-DB); the contract fake; the contract test.

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The DP rows above are the Template and Rules §R5.5 rows; this story documents the patterns; its dependency rows name RWB-P4-E1037-CON and RWB-PLT-E1037-CON for DP-08 (GAP-1175), and it starts on Day 1 as a CON story. Any grant or runbook step that names the rwb-case login reads the rwb-case login (DP-02); its name is Not specified in the source documents (GAP-0678).

**Build steps**

1. Write `queues.yaml` with the three operations and the Queue, QueueMember, QueueMeasure and CaseListRow schemas.
2. Write `lists.yaml` and `reference-loads.yaml` with the multipart request, the ReferenceLoad response and the problem envelope.
3. Write `rwb.case.events.yaml` with the two channels and the CloudEvents headers; add the message examples.
4. Add the lint rules: OpenAPI 3.1 validation, one envelope, `Idempotency-Key` on POST, base path, operation ids, no personal data in examples.
5. Write `schema-baseline.sql` from section 12 and cross-check every column against the field identifiers.
6. Generate the fake and the contract test; wire both into the build of this story and into a nightly run against RWB-P3-E1019-APP.
7. Publish v1 to the contract registry and notify the consumers.

**Done when.** Every document validates, the lint rules pass, the fake answers every operation and every example, and the contract test runs green on the build of this story.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P1-002 | A queue check fails on a row (team code, member role, overflow loop) | The {source} load for {date} was refused: {check}. The previous load is still in use. | 422, errors list with row and check |
| MSG-GEN-001 | Required column empty, or no rollback reason | Enter {field}. | 422, errors list with field |
| MSG-GEN-002 | Cap outside 1 to 500 | {field} must be between {min} and {max}. | 422, errors list with field, min and max |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. | 409 |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. | 409 |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. | 403 |

The message IDs and texts are the legacy ones; the HTTP status beside each one is fixed by this contract and is the same in every service that raises it. Validation rules for the request body are published as schema constraints where the value is defined (cap minimum 1 and maximum 500, valid from as a date, table in QUEUE or QUEUE_MEMBER, file content type xlsx) and as the placeholder where it is not (the remaining template columns — GAP-0681; ASM-1228).

### 15. Screens and states

No screen in this story. The documents are read through the gateway-bff composite route when a screen needs the schema (DP-19), and the reference-load response is what SCR-42 Queues and service levels will show in Epic 8. The states the response exposes are the version states of the reference registry: LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED, each with the HTTP status that produces it (201, 200, 200, 200, 200, 200, 422). The SCR-42 empty, loading, error and no access states are Not specified in the source documents (CG-ALL-3502).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P3-E1019-CON-01 | AC1 | Contract | queues.yaml validated and linted; Queue schema compared field by field with DF-WRK-001 to DF-WRK-008 and DF-WRK-038 |
| TC-P3-E1019-CON-02 | AC2 | Contract | QueueMember and QueueMeasure schemas compared with DF-WRK-045 to DF-WRK-052 and DF-RPT-020 to DF-RPT-030 |
| TC-P3-E1019-CON-03 | AC3 | Contract | lists.yaml and reference-loads.yaml; multipart request; Idempotency-Key present on both POST operations |
| TC-P3-E1019-CON-04 | AC4 | Contract | One problem envelope; the six legacy message ids present in the examples; 409 and 422 examples checked |
| TC-P3-E1019-CON-05 | AC5 | Contract | rwb.case.events.yaml validated; the two channels; CloudEvents headers; a personal-data scan of the examples |
| TC-P3-E1019-CON-06 | AC6 | Component | schema-baseline.sql with the nine P3 tables; the fake run against every operation and example; a breaking change raises v2 and deprecates v1 |
| TC-P3-E1019-CON-07 | AC7 | Contract | Queue assignment method compared with LOV-ASSIGN; queue.cap.max referenced as a parameter, not a constant; version status enumeration compared with LOV-VERSION-STATUS (TSD P3 v3 T3.2) |

### 17. Guardrails

- No business value is embedded in a schema as a constant: the cap range is published as the parameter `queue.cap.max` reference, not as an enumeration (DP-06).
- No personal data in examples, events or logs: members and approvers appear as user IDs only, and no event schema carries a name, an email address or an account number.
- No cross-schema reference: the documents name `rwb_case` tables only, and the role, permission and scope resources are referenced through rwb-access, never republished (DP-01, DP-08).
- One hop and 2 s timeout for every consumed operation; the examples show 503 on a timeout, never a stale answer.
- The base path is `/api/recovery/case/v1` and no document repeats the monolith base (DP-13).
- Every POST carries `Idempotency-Key`, and the examples show the repeat behaviour: the first result is returned.
- The document is Draft until the consumers pass, and it is versioned: a breaking change raises v2 and deprecates v1 rather than editing v1 in place.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-CWC-006 | Roles, teams, queues, membership and capacity as versioned data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-06 | R-UNI-38 | TC-P3-E1019-CON-01 to TC-P3-E1019-CON-07 |
| REQ-ACA-002 | Roles held as data; a change without a release | Epic 1, 3.4; Program, 5.4 | FEAT-ACA-03 | None | TC-P3-E1019-CON-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1019-APP | App development | H consumer: builds against this contract and its fake |
| RWB-P3-E1019-DB | ACE DB | Sibling: executes the schema in section 12 |
| RWB-P3-E1043-CON, RWB-P3-E1042-CON | Contract | Contracts this document references for lists, versions and the cap parameter |
| RWB-P4-E1037-CON | Contract | C: the rwb-access role and authorise contract this document references |
| RWB-PLT-E1044-CON, RWB-PLT-E1047-CON, RWB-PLT-N001-CON | Contract | H: Flyway sequence, topic naming, gateway-bff composite route |

### 19. Out of scope

- Any implementation, repository, migration or deployment: this story publishes documents and a fake only.
- The role, permission, scope, masking and delegation-of-authority resources: rwb-access (P4).
- The parameter and reference-data contracts themselves: RWB-P3-E1042-CON and RWB-P3-E1043-CON.
- The behaviour that emits the events: RWB-P3-E1020-APP and RWB-P3-E1021-APP.
- The rollback and verify operations of reference loads: outside the rwb-case operation set given for this legacy key (GAP-0682; ASM-1229), so they are not published in v1.
- Screens, the gateway route definition and the Epic 8 administration UI.
