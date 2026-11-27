# RWB-P4-AD014-CON Configure queues - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD014-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-AD014-CON-16) |
| Contract version | v1 (base /api/recovery/access/v1) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| Open decision | DL23 (assumptions ASM-1232, ASM-1237, ASM-1259, ASM-1560): still open; the assumptions apply |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: written for rwb-access from legacy RWB-AD-014, replacing the earlier pass at the same path. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 8 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-access**, I want **the published OpenAPI 3.1 document of the two queue-file check operations, with its schemas, its finding codes, its error envelope, the list of owner operations it consumes and a fake for each, available on Day 1**, so that **the app story of this key, gateway-bff and every other caller can build against the contract without waiting for the service, and so that no finding code, field name or error code reaches a caller by accident**.

- **Naming.** Base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, task queue `rwb-access` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.access`. The document carries no path outside that base.
- **The two operations.** `POST /api/recovery/access/v1/admin/queue-file-checks` (multipart `file` and `validFrom`, required `Idempotency-Key`) and `GET /api/recovery/access/v1/admin/queue-file-checks/{checkId}`. Their paths are this run's own surface: Not specified in the source documents (GAP-2274; ASM-3749).
- **The four schemas.** `QueueFileRow` (the eight queue fields), `QueueFinding` (row, field, code, message), `QueueFileCheck` (the record) and `QueueFileCheckAnswer` (the record with its findings and its hand-off reference). The ninth check code and the last two field names are this run's: Not specified in the source documents (GAP-2274; ASM-3755; ASM-3752).
- **The split boundary, stated in the document itself.** The document declares that the queue row and its version are the owner's (RWB-P3-E1019-CON), that the check writes no queue field, and that the approval is the owner's operation; the document therefore has no approve path, no rollback path and no queue write (GAP-2274; ASM-3748).
- **What it consumes and must name.** The owner's reference load, the owner's approve, the owner's queue read, the owner's list read (DP-07) and the owner's parameters read (DP-06), each with its contract id, so the app story builds against a fake and never against a build (GAP-2274; ASM-3749).
- **The record.** The document declares that an accepted check is written through the decision-record library before the hand-off (DP-03), and what the caller sees when that write fails (GAP-2274; ASM-3756).
- **The ACE read.** The document names `v_ace_iam_group` as the only ACE data the check reads, read-only, and states that no ACE table and no other schema is named (DP-05).
- **No dependency.** This is a CON story: it has no build dependency, it is Day 1, and it blocks only the app story of the same key. It does not wait for RWB-P3-E1019-CON; it names the owner's operations and ships the fake that answers them.

### 2. Business rationale

A contract story exists so that the two sides of a boundary can be built at the same time. Here the boundary is unusual: the queue is the owner's data, the role it names is this service's data, and the file that carries both is written by a reference data administrator who expects one answer, at once, in words. Left to the build, that answer would be invented twice, once in the gate and once in the screen, and the finding codes would drift within a release. Writing them down first makes the codes the contract, and it lets gateway-bff mock SCR-42 and the app story mock the owner from Day 1.

It is also the cheapest place to hold the whole-file rule. Legacy AC2 is a refusal, and a refusal is only useful if the caller can read which row and which field caused it. The document therefore fixes the finding shape (row, field, code, message), makes one Error finding refuse the entire file, and forbids any partial acceptance in the answer schema. A reviewer can check that rule in one page instead of in a validator. DP-03 then fixes what "accepted" means: an answer with a state of VALIDATED exists only after the acceptance entry is written, so the contract and the record cannot disagree.

### 3. Preconditions

None of these is a build dependency; the story is Day 1 and depends on no other story being done.

| Precondition | What it gives this story |
|---|---|
| The service naming and the contract template of the platform (DP-13, §R4) | The base path, the schema name and the document skeleton |
| The RFC 9457 error envelope and the message standard of the programme | The shape of 4xx and 5xx answers, and the message key convention |
| The published shape of RWB-P3-E1019-CON, RWB-P3-E1043-CON and RWB-P3-E1042-CON, read not awaited | The five consumed operations the document names, and the fake each one needs |
| The template and rules of this run (§R7.2 s12, §R5.5) | The nine contract tables and the DP mapping |
| The legacy story RWB-AD-014 | AC1 and AC2, the queue fields, the messages MSG-P4-002, MSG-P7-003 and MSG-GEN-001 |

### 4. Flow

| Step | Actor | Action | Result |
|---|---|---|---|
| 1 | Contract owner | Writes the document on base `/api/recovery/access/v1` with the two operations and the four schemas | A draft the app story can read |
| 2 | Contract owner | Declares the seven finding codes with their field names and their message keys | The refusal vocabulary is fixed before any code |
| 3 | Contract owner | Declares the five consumed operations with their contract ids and their fake behaviour | The app story builds against fakes from Day 1 |
| 4 | Contract owner | Publishes the fakes and the contract test suite | A suite that runs with no service built |
| 5 | Reviewer (solution architect) | Checks the naming, the error envelope, the finding shape and the additive rule | The document is published as v1 |
| 6 | Any later change | Adds a field or a code, or raises a major version for a breaking change | v1 stays readable for its callers |

### 5. Exception paths

| Path | What the document declares | Covered by |
|---|---|---|
| A body that is not multipart, or a missing `validFrom` | 400 with the error envelope and MSG-GEN-001 naming the field | AC9 |
| A missing `Idempotency-Key` | 400, the same envelope, the header named as the field | AC10 |
| The same key with a different file or a different `validFrom` | 409, the envelope naming the key, no state change | AC5 |
| A caller without Reference data C or R | 403 with MSG-P4-002 and the area and right named in the document | AC6 |
| A check that is not the caller's or not present | 404 with the envelope; a check of another author is 404, never 403 | AC11 |
| Any Error finding | 422 with MSG-P1-002 and the findings list | AC2 |
| The acceptance entry cannot be written | 503 with MSG-P7-003, no state transition and no owner load reference | AC7 |
| The owner answers an error during the hand-off | The owner's code mapped into the envelope, the check left in VALIDATED with the hand-off pending | AC12 |

### 6. INVEST check

| Letter | Finding | Result |
|---|---|---|
| Independent | No build dependency; it names the owner's contract and ships a fake, so it is not blocked by rwb-case | Met |
| Negotiable | The finding codes and the two paths are this run's; the shape and the messages come from the sources | Met |
| Valuable | It is what makes the app story, the screen and the owner's client agree on one vocabulary | Met |
| Estimable | One document, four schemas, seven codes, five fakes and one contract test suite | Met |
| Small | One service boundary and nothing else; no table, no workflow, no event | Met |
| Testable | Every criterion is checked by reading the document or running the suite against the fakes | Met |

### 7. Acceptance criteria

```gherkin
Feature: Configure queues - contract

  Scenario: AC1 The document and its two operations (new, D-RCV-60)
    Given the published contract document of this story
    When the two operations are read on base /api/recovery/access/v1
    Then POST /admin/queue-file-checks declares a multipart body of file and validFrom, a required Idempotency-Key header, a 200 answer of QueueFileCheckAnswer and the errors 401, 403, 409, 422 and 503
    And GET /admin/queue-file-checks/{checkId} declares a 200 answer of the same schema and the errors 401, 403, 404 and 503
    And QueueFileCheckAnswer holds checkId, state, validFrom, author, fileHash, rowCount, ownerLoad and findings

  Scenario: AC2 One error finding refuses the whole file (new, D-RCV-60)
    Given a QueueFileCheckAnswer with one finding of code OVERFLOW_QUEUE_UNKNOWN at row 7 and field overflow_queue_code
    When its state is read
    Then the state is REFUSED
    And the finding carries the row, the field, the code and the message key
    And the document states that one Error finding refuses the whole file and offers no partial acceptance

  Scenario: AC3 Role, team and method findings read the owner's lists (new, D-RCV-60)
    Given the document and the reference-data contract of RWB-P3-E1043-CON
    When the finding catalogue is read
    Then it declares ROLE_UNKNOWN on role_code, TEAM_UNKNOWN on team_code and ASSIGNMENT_METHOD_UNKNOWN on assignment_method
    And it names the list read of RWB-P3-E1043-CON as the source of LOV-ASSIGN and LOV-TEAM
    And the document embeds no list value

  Scenario: AC4 The caseload cap is a parameter, not a number in the document (new, D-RCV-60)
    Given the parameters contract of RWB-P3-E1042-CON
    When the finding catalogue is read
    Then it declares CAP_ABOVE_PARAMETER on capacity_cap
    And it states that the limit is read with the version in force
    And the document carries no numeric cap of its own

  Scenario: AC5 The check is idempotent (new, D-RCV-60)
    Given a POST with Idempotency-Key "K-1" for one file and one validFrom
    When the same call is repeated with the same key, file and validFrom
    Then the document declares 200 with the first checkId and the same findings
    And a call with the same key and a different file answers 409

  Scenario: AC6 A caller without the right is refused in the envelope (new, D-RCV-60)
    Given a caller whose Reference data letter is "-"
    When it calls either operation
    Then the document declares 403 with the error envelope carrying MSG-P4-002, the area Reference data and the right C or R
    And no state changes

  Scenario: AC7 A check that cannot be recorded is not accepted (new, D-RCV-60)
    Given the decision-record write of DP-03 fails
    When the POST is answered
    Then the document declares 503 with MSG-P7-003
    And the state is not VALIDATED
    And the answer carries no ownerLoad

  Scenario: AC8 The suite runs with no service built, and v1 stays additive (new, D-RCV-60)
    Given the five fakes of section 12.8
    When the contract test suite runs against them
    Then every operation, schema, finding code and error code of the document is exercised
    And the document carries an additive-change rule within v1 and requires a new major version for a breaking change

  Scenario: AC9 A body that is not multipart or has no validFrom is refused (new, D-RCV-60)
    Given a POST whose body is not multipart or carries no validFrom
    When the POST is answered
    Then the document declares 400 with the error envelope and MSG-GEN-001 naming the field

  Scenario: AC10 A missing Idempotency-Key is refused (new, D-RCV-60)
    Given a POST without an Idempotency-Key header
    When the POST is answered
    Then the document declares 400 with the same envelope and the header named as the field

  Scenario: AC11 A check that is absent or of another author is 404 (new, D-RCV-60)
    Given a GET for a checkId that is not present or belongs to another author
    When the GET is answered
    Then the document declares 404 with the envelope
    And a check of another author is answered 404, never 403

  Scenario: AC12 An owner error in the hand-off is mapped into the envelope (new, D-RCV-60)
    Given the owner answers an error during the hand-off
    When the check is read
    Then the document declares the owner's code mapped into the envelope
    And the check stays VALIDATED with the hand-off pending
```

### 8. Business rules

| BR ID | Rule | What the document must state |
|---|---|---|
| BR1 | One check, one answer | A POST returns the whole answer, findings included; there is no paged check and no partial result |
| BR2 | No partial acceptance | `rowCount` is the number of rows read from the file, not the number accepted; the schema has no accepted-row count |
| BR3 | Row numbering is the file's | A finding's `row` is the 1-based row of the data as the administrator sees it in the file, header excluded |
| BR4 | Field names are the owner's | The finding's `field` carries the queue field name as the owner names it, so the message names a column the administrator can find |
| BR5 | No value in the document | No list value, no cap, no method name and no role code appears in the document as a fixed value; all come from the contracts named |
| BR6 | Author and approver are two people | The document states that the approval is the owner's operation and that the author cannot approve; it declares MSG-P7-002 for that refusal |
| BR7 | Additive within v1 | A new optional field or a new finding code is a minor change; a removed field, a renamed field or a changed meaning needs a new major version |
| BR8 | Only the queue sheet is checked | The check reads the queue sheet only; a member sheet is passed to the owner untouched |

### 9. State transitions

| Object | States | Who sets them |
|---|---|---|
| The document | Draft, Published v1, Superseded by a major version | The contract owner |
| The check | RECEIVED, REFUSED, VALIDATED, HANDED_OFF | The app story, within the enum the document fixes |
| The owner's version | LOADED, APPROVED, IN_FORCE, ROLLED_BACK | rwb-case through its own contract; the document only reads the label it reports |

The document fixes the check enum and no other: it declares the owner's states as an opaque label the answer reports, so a change in the owner's lifecycle does not break this contract.

### 10. Authority

| Area | Right | Declared on |
|---|---|---|
| Reference data | C | POST /admin/queue-file-checks |
| Reference data | R | GET /admin/queue-file-checks/{checkId}, and the list read it consumes |
| Rules and parameters | A | Not declared here: the approval is the owner's operation (GAP-2274; ASM-3751) |

The document names the area and the right on each operation (TSD P4 T6.2) and states that the right is read from `permission` at the version in force, never from a role name in code (REQ-ACA-003). The legacy permission row of RWB-AD-014 gives the load and the approval the letters of Rules and parameters; the C letter is carried as Reference data C, and the difference is recorded with one gap and two assumptions (GAP-2274; ASM-3750).

### 11. Data

| Schema | Field | Type | Note | BR Field ID |
|---|---|---|---|---|
| QueueFileRow | queue_code | string | DF-WRK-002, unique in the file | DF-WRK-002 |
| QueueFileRow | queue_name | string | DF-WRK-003 | DF-WRK-003 |
| QueueFileRow | team_code | string | DF-WRK-004, a value of LOV-TEAM | DF-WRK-004 |
| QueueFileRow | role_code | string | DF-WRK-005, a role of rwb-access at the version in force | DF-WRK-005 |
| QueueFileRow | assignment_method | string | DF-WRK-006, a value of LOV-ASSIGN | DF-WRK-006 |
| QueueFileRow | capacity_cap | integer | DF-WRK-007, optional; the name is this run's (GAP-2274; ASM-3752) | DF-WRK-007 |
| QueueFileRow | overflow_queue_code | string | DF-WRK-008; the name is this run's (GAP-2274; ASM-3752) | DF-WRK-008 |
| QueueFinding | row, field, code, message | integer, string, enum, string | `row` is 1-based in the file, `field` is the queue field name | Not specified in the source documents (DOR-RWB-P4-AD014-CON-7) |
| QueueFileCheck | checkId, state, validFrom, author, fileHash, rowCount, ownerLoad | string, enum, date, string, string, integer, string | `ownerLoad` is absent until the hand-off answers | Not specified in the source documents (DOR-RWB-P4-AD014-CON-7) |
| QueueFileCheckAnswer | the check and its findings | object, array | No accepted-row count and no per-row success flag | Not specified in the source documents (DOR-RWB-P4-AD014-CON-7) |

The finding codes are `OVERFLOW_QUEUE_UNKNOWN`, `ROLE_UNKNOWN`, `TEAM_UNKNOWN`, `ASSIGNMENT_METHOD_UNKNOWN`, `CAP_ABOVE_PARAMETER`, `DUPLICATE_QUEUE_CODE` and `VALID_FROM_IN_PAST`, each with a severity of Error. The code set is this run's own naming and not a source value (GAP-2274; ASM-3755).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Right | Request | Answer |
|---|---|---|---|---|
| POST | /api/recovery/access/v1/admin/queue-file-checks | Reference data C | multipart: `file`, `validFrom`; header `Idempotency-Key` (required; a repeat with the same key and file answers the first checkId, AC5) | 200 QueueFileCheckAnswer; 400, 401, 403, 409, 422, 503 |
| GET | /api/recovery/access/v1/admin/queue-file-checks/{checkId} | Reference data R | none | 200 QueueFileCheckAnswer; 401, 403, 404, 503 |

#### 12.2 REST operations consumed

| Contract | Operation the document names | Declared use | Owner service |
|---|---|---|---|
| RWB-P3-E1019-CON | Reference load of rwb-case | Store the accepted queue version under its owner | rwb-case |
| RWB-P3-E1019-CON | Approve of rwb-case | The second pair of eyes and MSG-P7-002 | rwb-case |
| RWB-P3-E1019-CON | Queue read of rwb-case | The queues in force, for the overflow check | rwb-case |
| RWB-P3-E1043-CON | List read of rwb-case | LOV-ASSIGN and LOV-TEAM with their version | rwb-case |
| RWB-P3-E1042-CON | Parameters read of rwb-case | The cap maximum and the file and row limits | rwb-case |

The exact path and shape of each consumed operation are the owner's contract's, not this document's: Not specified in the source documents (GAP-2274; ASM-3749).

The queue-load gate of rwb-access is declared here: POST /api/recovery/access/v1/admin/queue-loads with two request shapes, a multipart queue load and a JSON approval, and GET /api/recovery/access/v1/admin/queue-loads/{loadId}. The owner's reference-load family stays consumed as listed above.

#### 12.3 Events published

None. The document names no event of `rwb.access.events.v1`; the acceptance entry of DP-03 is written through the platform library and reaches `rwb.decision-record.v1` from there.

#### 12.4 Events consumed

None. The check is asked and does not listen; the queues in force are read with the owner's operation and are never mirrored.

#### 12.5 Workflows and activities

None. The document declares no workflow start, no activity and no signal.

#### 12.6 Schedules

None. Nothing in this contract is time driven; `validFrom` is a date on the file and the effect of it is the owner's.

#### 12.7 Tables owned

None. A contract story owns no table: the queue rows are rwb-case's, the role and permission rows are RWB-P4-E1019-APP's, and the check record is RWB-P4-AD014-APP's.

#### 12.8 Contract fakes

| Fake | Behaviour declared |
|---|---|
| rwb-case queue fake | Answers a reference load with a load reference, an approve with the owner's state, and the queues in force; a variant omits the overflow queue |
| rwb-case list fake | Answers LOV-ASSIGN and LOV-TEAM with a version label; a variant returns a list without the value under test |
| rwb-case parameters fake | Answers the cap maximum, the row limit and the file size limit |
| Decision-record fake | Answers an accepted entry; a variant fails, to prove the 503 and the absence of VALIDATED |
| ACE view stub | Answers `v_ace_iam_group` rows for the test roles; a variant omits the group of one role |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST, provided | 2 | One POST and one GET on base `/api/recovery/access/v1` |
| REST, consumed | 5 | Three owner operations of the queue contract, one list read, one parameters read |
| Kafka | 0 | No topic and no event is declared |
| Temporal | 0 | No workflow, no activity, no schedule |
| File | 1 | The multipart queue file, and the file hash the answer carries |

### 13. Solution plan

| Artefact | Content | Size |
|---|---|---|
| `queue-file-check.openapi.yaml` | The two operations, the four schemas, the seven finding codes, the error envelope, the security scheme | 1 file |
| The consumed-operation appendix | The five owner operations with their contract ids, marked as external references and not copied | 1 section |
| The fakes | Five, as in section 12.8, runnable with no service | 5 files |
| The contract test suite | One test per criterion AC1 to AC8, plus one per finding code | 15 tests |
| The change note | The additive rule and the major-version rule | 1 note |

### 14. Validation and messages

| Condition | Status | Message key |
|---|---|---|
| A required field or the idempotency header is missing | 400 | MSG-GEN-001 |
| No Reference data right | 403 | MSG-P4-002 |
| The idempotency key is reused for another file or date | 409 | The envelope's conflict code, no business message |
| A check is absent or not the caller's | 404 | The envelope's not-found code |
| Any Error finding | 422 | MSG-P1-002, with the findings list |
| The acceptance entry cannot be written | 503 | MSG-P7-003 |
| The author is presented as the approver, on the owner's operation | 409 | MSG-P7-002 |

The messages this document uses are listed here:

| Message key | Text |
|---|---|
| MSG-GEN-001 | Not specified in the source documents (DOR-RWB-P4-AD014-CON-9) |
| MSG-P1-002 | Not specified in the source documents (DOR-RWB-P4-AD014-CON-9) |
| MSG-P4-002 | Not specified in the source documents (DOR-RWB-P4-AD014-CON-9) |
| MSG-P7-002 | Not specified in the source documents (DOR-RWB-P4-AD014-CON-9) |
| MSG-P7-003 | Not specified in the source documents (DOR-RWB-P4-AD014-CON-9) |

### 15. Screens and states

| Screen | What the document gives it |
|---|---|
| SCR-42 Queues and service levels | The two calls the screen makes, one hop each through gateway-bff (DP-19); the finding shape it renders by row and field; the refusal text it shows from the message keys; states empty, loading, error and no access: Not specified in the source documents (CG-ALL-4792) |
| SCR-43 Roles and access | Nothing of its own; the role and group check is inside the POST and never a second call from the screen; states empty, loading, error and no access: Not specified in the source documents (CG-ALL-4793) |

The document states that the screen never chains calls and that a refused check leaves the version in force untouched, so the screen has one state to show and not two.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-014-01 | AC1, AC2 | Contract | The document, its four schemas and the overflow finding at row 7 |
| TC-AD-014-02 | AC2 | Contract | The queue fake without the overflow queue; the answer asserted as REFUSED with no partial acceptance |
| TC-AD-014-03 | AC6 | Contract | A caller with the letter "-" and one with R only; the envelope, the area and the right |
| TC-AD-014-04 | AC7 | Contract | The decision-record fake forced to fail; 503, no VALIDATED and no ownerLoad |
| TC-AD-014-05 | AC3 | Contract | The reference-data list fake of RWB-P3-E1043-CON; ROLE_UNKNOWN, TEAM_UNKNOWN and ASSIGNMENT_METHOD_UNKNOWN asserted; no list value in the document |
| TC-AD-014-06 | AC4 | Contract | The parameters fake of RWB-P3-E1042-CON; CAP_ABOVE_PARAMETER asserted on capacity_cap with the version in force |
| TC-AD-014-07 | AC5 | Contract | POST with an Idempotency-Key repeated with the same file and validFrom (200, same checkId and findings); a different file on the same key (409) |
| TC-AD-014-08 | AC8 | Contract | The five fakes of section 12.8; every operation, schema, finding code and error code exercised; additive-change rule checked |
| TC-AD-014-09 | AC9 | Contract | POST with a body that is not multipart, and POST with no validFrom; 400 with the envelope and MSG-GEN-001 naming the field |
| TC-AD-014-10 | AC10 | Contract | POST without Idempotency-Key; 400 with the envelope and the header named as the field |
| TC-AD-014-11 | AC11 | Contract | GET for an absent checkId and for a check of another author; both 404 with the envelope, never 403 |
| TC-AD-014-12 | AC12 | Contract | The owner error forced during the hand-off; the owner's code mapped into the envelope and the check left in VALIDATED with the hand-off pending |

The four legacy test case ids of RWB-AD-014 are kept here with the Level of Contract; the app story keeps the same ids at their own levels.

### 17. Guardrails

- No business value in the document: no cap, no list value, no method name and no role code is written as a fixed value; each is named as coming from a contract.
- No personal data in the schemas, the fakes or the tests; a row is named by its number, its `queue_code` and its field.
- ACE data only through `v_ace_iam_group`, named in the document as a read-only view; no ACE table and no other service's table is named.

### 18. Traceability

| Source | Reference |
|---|---|
| Legacy story | RWB-AD-014 Configure queues, module P4, epic E8, decision DL23; AC1 and AC2 are the app story's; TC-AD-014-01 to TC-AD-014-04 are kept here at Contract level |
| FSD P4 | A2.3 (the load and its approval), A2.17 (the administration screens), AC-P4-003-01, AC-ALT-P4-003-01, AC-ALT-P4-003-02, AC-EXC-P4-003-01, AC-EXC-P4-003-02, AC-EXC-P4-003-07, AC-EXC-P4-003-08 |
| TSD P4 | T6.1 (the RBAC matrix), T6.2 (area and right on each endpoint), T-A.1 (the reference-load family and its idempotency key) |
| Requirements | REQ-ACA-002, REQ-ACA-003, REQ-ACA-013 |
| Patterns | DP-03, DP-05, DP-06, DP-07, DP-13, DP-19 of §R5.5 |

### 19. Out of scope

- The implementation of the check: RWB-P4-AD014-APP, which implements this document and adds no path.
- The queue reference load, its approve, its verify and its rollback: RWB-P3-E1019-CON and its app and DB stories.
- The queue write interface for models and agents: RWB-P4-E2036-APP.
- Service levels, timers and the rule-version operations of the legacy endpoints row: RWB-AD-015, RWB-AD-011 and RWB-AD-012.
- The screen build of SCR-42, the gateway-bff route itself (RWB-PLT-N001-CON) and any event of this service's own topic.
