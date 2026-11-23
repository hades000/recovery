# RWB-P4-AD014-APP Configure queues

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD014-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-P4-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P4-AD014-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1019-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: written for rwb-access from legacy RWB-AD-014, replacing the earlier pass at the same path. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator (RW-REFADM)**, I want **a queue file, with its team, role, assignment method, caseload cap and overflow queue, checked whole against the role catalogue, the lists and the parameters in force, and its acceptance recorded, before the file reaches the service that owns the queue**, so that **allocation follows the team set-up without a code change, a file that names an overflow queue that does not exist is refused before a single queue row is in force, and no queue version is accepted without its author, its approver and its record**.

- **Service.** `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1` (DP-13), topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery` (not used here), Java package `th.co.scb.ace.workbench.recovery.access`.
- **The ownership split, stated plainly.** `queue`, `queue_member`, `queue_measure`, `capacity` and the assignment are P3 `rwb-case`'s tables, and the reference-load path with its approve and rollback operations is rwb-case's as well (RWB-P3-E1019-APP, -CON, -DB; default ruling of §R3 gives parameters and reference data to P3). `rwb_access` holds no queue row, creates no queue table and writes no queue field (DP-01). This story is the **gate in front of the owner**: the ingest, the whole-file validation, the refusal, the hand-off through the owner's contract and the record of the acceptance.
- **Two operations provided, and no others.** `POST /api/recovery/access/v1/admin/queue-file-checks` takes the multipart queue file with its `validFrom` and answers a check; `GET /api/recovery/access/v1/admin/queue-file-checks/{checkId}` answers the same check with its findings. The paths are this story's own surface and are not named in the sources: Not specified in the source documents (GAP-2273; ASM-3749).
- **Consumed.** The owner's reference-load operation and its approve operation, the owner's queue read for the queues in force, the owner's list read for LOV-ASSIGN and LOV-TEAM (DP-07), and the owner's parameters read for the cap limit (DP-06). Exact paths and shapes are the owner's contract's: Not specified in the source documents (GAP-2273; ASM-3749).
- **The record.** Each accepted check appends one entry of the local decision-record library and its outbox row in the same local transaction as the stored answer, and the entry reaches the shared topic `rwb.decision-record.v1` (DP-03). Where the entry cannot be written the check stops with 503 and MSG-P7-003 and the owner is never asked to take the file, so no queue version changes unrecorded (legacy TC-AD-014-04). The decision code of that entry is Not specified in the source documents (GAP-2273; ASM-3756).
- **Whole file or nothing.** Any finding of severity Error refuses the whole file and names the row and the field, with MSG-P1-002 "The {source} load for {date} was refused: {check}. The previous load is still in use." No row reaches the owner on a refused check. The finding codes below are this story's own names: Not specified in the source documents (GAP-2273; ASM-3755).
- **The two columns the legacy text does not name.** The legacy Data table gives the queue as "id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more"; the last two are read here as `capacity_cap` and `overflow_queue_code` from the capacity criterion of FSD P4 AC-ALT-P4-003-02 and legacy AC2: Not specified in the source documents (GAP-2273; ASM-3752).
- **The ACE read (DP-05).** The Entra ID group that maps to a role named in the file is read from the read-only view `v_ace_iam_group` of the ACE database, never from an ACE table, and never copied into `rwb_access`.
- **The legacy endpoints row does not belong to this story.** It lists the rule-version read and the rule-version approve, which are RWB-AD-011 and RWB-AD-012, and it names the monolith base; it is carried as one gap and not implemented here (GAP-2273; ASM-3749).

### 2. Business rationale

A queue is the one place where a team, the role that works it, the way an officer is chosen, the workload cap and the queue a case overflows into are set. The legacy story says it in one sentence: queues with their team, role, assignment method, caseload cap and overflow queue loaded as data, so that allocation follows the team set-up without a code change. The target is measured: rule and limit changes made without a code release, 100 percent, from the decision log and the Workbench records, every month (FSD P4 A2.17.1). In the monolith the queue row, the member row and the cap were rows of one recovery schema and the load was one administration screen; in the target the queue row is rwb-case's and the role it names is rwb-access's, so the two services meet on a contract and the gate between them has to be explicit about what it accepts, what it refuses and what it records.

The whole-file refusal is why this story is a build and not a form. A queue file is a set of rows that only makes sense together: queue A overflows into queue B, and if B is neither in the file nor in force then A has a hole, and the hole shows only when every officer of A is at the cap and a case has nowhere to go, which is already too late. Legacy AC2 says the system refuses the load. This story refuses the whole file at the check, naming the row and the field, before a single row reaches the owner, so the administrator repairs one file rather than reconciles two half-loaded versions. That is the same discipline the owner puts on its own reference loads (FSD P4 AC-EXC-P4-003-01) and it is why the validator is the largest component here.

Two controls sit beside it. The cap is a workload decision and the overflow is a routing decision, so the file is not accepted by the person who wrote it: the legacy story keeps the loader and the approver apart, and the owner's approve operation enforces it with MSG-P7-002. And every acceptance is recorded before it is acted on, which is R-UNI-39 and legacy TC-AD-014-04. The story meets REQ-ACA-002 (a change of roles and reference data takes effect without a code release), REQ-ACA-003 (the role to permission matrix is the only source of what a role may do) and REQ-ACA-013 (administration screens with their rights), and it keeps R-UNI-38 at its edge by passing the file's `valid_from` to the owner and never answering a version as in force before that date.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD014-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two operations, the `QueueFileCheck`, `QueueFileRow`, `QueueFinding` and `QueueFileCheckAnswer` schemas, the finding codes, the error envelope, the consumed-operation list and the contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the hash chain and the outbox row |
| RWB-PLT-E1042-CON | The parameters client (DP-06): the cap limit and the row and file limits of a queue file, read with the version in force |
| RWB-PLT-E1043-CON | The reference-data client (DP-07): LOV-ASSIGN and LOV-TEAM with their versions |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): SCR-42 Queues and service levels reaches the two operations through it, one hop each |
| RWB-P3-E1019-CON (contract dependency, C) | The rwb-case queue contract and its fake: the reference load, the approve, the queue read for the queues in force, the list read and the parameters read. A C dependency, so it never blocks the build |
| The `rwb_access` baseline of RWB-P4-E1019-APP and RWB-P4-E1069-APP | `role` and `permission` rows with the version in force, so a `role_code` in the file can be checked, and the read-only grant on `v_ace_iam_group` |

### 4. Flow

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reference data administrator | Opens SCR-42 through gateway-bff and loads the queue file with its valid from date | Authorises Reference data C; refuses at once if the right is missing, with 403 and MSG-P4-002 |
| 2 | System | Reads the file | Rejects a malformed or oversized file against the limits read with DP-06, before any row is parsed |
| 3 | System | Parses the queue sheet into `QueueFileRow` items | Numbers every row as it appeared in the file, so a finding can name it |
| 4 | System | Runs the checks of section 8 against the role catalogue, LOV-ASSIGN, LOV-TEAM, `v_ace_iam_group`, the parameters limit and the owner's queues in force | Collects findings; no finding is repaired silently and no value is defaulted |
| 5 | System | Decides the check | Any Error finding: state REFUSED, 422, MSG-P1-002 naming the checks. No Error finding: state VALIDATED |
| 6 | System | Writes the acceptance entry and its outbox row with DP-03 | A failed write stops the check with 503 and MSG-P7-003; the state never becomes VALIDATED |
| 7 | System | Hands the accepted file to the owner's reference-load operation with `validFrom`, once, with an idempotency key | The owner stores the version; its answer is kept as the check's `ownerLoad` reference. A timeout is not retried blindly |
| 8 | Security administrator or Risk | Approves the load through the owner's approve operation | The owner enforces author different from approver with 409 and MSG-P7-002; the gate never approves |

### 5. Exception paths

| Path | What happens | Message |
|---|---|---|
| No right in the capability area | Refused before the handler runs; nothing stored and no file read | 403, MSG-P4-002 "You cannot {action} here. Your role does not include it." |
| Unknown overflow queue | The file is refused whole, naming the row and `overflow_queue_code` | 422, MSG-P1-002 |
| Unknown role code, unknown team code, assignment method not in LOV-ASSIGN, cap above the parameter | Each is a finding on its own row; the file is refused whole | 422, MSG-P1-002 |
| Decision record cannot be written | The check stops; the owner is never called; no acceptance exists | 503, MSG-P7-003 "The action was not taken because the decision could not be recorded. Try again in a few minutes." |
| Owner unreachable, slow or answering an error | The check stays VALIDATED with its hand-off pending, and the screen says so; a repeated POST with the same Idempotency-Key returns the same check | 503 or the owner's code, mapped to the envelope; no queue version is claimed |
| Duplicate upload of the same file and date | The idempotency key returns the first check; a different file for the same date is a conflict | 200 with the same `checkId`; 409 |

### 6. INVEST check

| Letter | Finding |
|---|---|
| Independent | Builds against five published contract faces and needs no other story to be finished; C dependencies are mocked from Day 1 |
| Negotiable | The finding codes and the two paths are this run's; the checks themselves are fixed by the legacy criteria and the FSD rules |
| Valuable | It is the difference between one repaired file and two half-loaded queue versions |
| Estimable | Six checks, one parser, one owner client and one record writer; no workflow and no event of its own |
| Small | One service, two operations, no table of its own beyond a check record in `rwb_access` |
| Testable | Both legacy criteria are expressed as a check answer, a finding list and a state, all observable through the two operations |

### 7. Acceptance criteria

```gherkin
Feature: Configure queues

  Scenario: AC1 Queue loaded (legacy RWB-AD-014 AC1)
    Given the rwb-case contract mock returns the queue version in force from its valid from date
    And a queue file
    When it is loaded and approved
    Then allocation uses the new method and cap from the valid from date

  Scenario: AC2 Overflow must exist (legacy RWB-AD-014 AC2)
    Given the rwb-case contract mock returns the queues in force
    And a queue that names an overflow queue that does not exist
    When it is loaded
    Then the system refuses the load
```

### 8. Business rules

The six checks below are this story's own names for the rules the sources state in words; they are not source rule identifiers (GAP-2273; ASM-3755).

| Check | Rule | Outcome on failure |
|---|---|---|
| QFC-1 Overflow | Every `overflow_queue_code` is either a `queue_code` of the same file or a queue of the version in force, read from the owner's queue read. A queue may not overflow into itself | Error `OVERFLOW_QUEUE_UNKNOWN`, field `overflow_queue_code`, row n |
| QFC-2 Role | Every `role_code` exists in `rwb_access.role` at the version in force and its class is a bank or partner user role. The Entra group of that role exists in `v_ace_iam_group` (DP-05) | Error `ROLE_UNKNOWN`; field `role_code` |
| QFC-3 Team | Every `team_code` is a value of LOV-TEAM read with DP-07 at the version in force | Error `TEAM_UNKNOWN`; field `team_code` |
| QFC-4 Method | Every `assignment_method` is a value of LOV-ASSIGN read with DP-07. No method is written in code | Error `ASSIGNMENT_METHOD_UNKNOWN`; field `assignment_method` |
| QFC-5 Cap | `capacity_cap`, where the file carries it, is a whole number above zero and not above the maximum read from the parameters contract with DP-06. No default cap is applied. The key name and the value are the owner's: Not specified in the source documents (GAP-2273; ASM-3754) | Error `CAP_ABOVE_PARAMETER`; field `capacity_cap` |
| QFC-6 Uniqueness and dates | `queue_code` is unique in the file, `validFrom` is one date for the whole file and is not earlier than the date the check is run | Error `DUPLICATE_QUEUE_CODE` or `VALID_FROM_IN_PAST` |
| QFC-7 Record | The acceptance entry is written before the hand-off, and its absence stops the check | Stop with 503 and MSG-P7-003 |

BR-P4-003 of FSD P4 A2.3.3.1 holds throughout: no value a business person may change is written in code; it is read from reference data or parameters with its version.

### 9. State transitions

| State | Entered when | Leaves when |
|---|---|---|
| RECEIVED | The file is accepted for parsing | A parse error (422) or the checks begin |
| REFUSED | Any Error finding | Never; a corrected file is a new check |
| VALIDATED | No Error finding and the acceptance entry is written | The owner answers the hand-off, or the check is abandoned |
| HANDED_OFF | The owner's reference-load operation answers with a load reference | The owner's version moves to APPROVED and IN_FORCE on its own dates; the gate does not follow it |

The owner's version states LOADED, APPROVED, IN_FORCE and ROLLED_BACK are rwb-case's (its contract and FSD P4 AC-ALT-P4-003-01); this story reads them and never sets them. The old shapes and the old load path of the monolith are outside this story (GAP-2273; ASM-3748).

### 10. Authority

| Capability area | Right | Roles that hold it (TSD P4 T6.1) |
|---|---|---|
| Reference data | C, for the check | RW-COE, RW-REFADM |
| Reference data | R, for the check read and the lists | Every role in the matrix's Reference data column with R |
| Rules and parameters | A, for the approval | RW-RISK; the approval is the owner's operation, not this story's |
| Rules and parameters | R | The roles of TSD P4 T6.1, for the queue and cap view on SCR-42 |

The right is read from `permission` at the version in force, never from a role name in code (REQ-ACA-003). The legacy permission row gives the load the C letter of Reference data to RW-COE and RW-REFADM and the approval the A letter of Rules and parameters to RW-RISK, which the RBAC matrix carries only in part: the C letter is carried, the A letter is left with the owner and one gap records the difference (GAP-2273; ASM-3750; ASM-3751).

### 11. Data

| Field in the file | Meaning | Field ID | Owner of the column |
|---|---|---|---|
| (row) | The queue row itself | DF-WRK-001 | rwb-case |
| queue_code | Queue code, for example LIT-BKK-OFF | DF-WRK-002 | rwb-case |
| queue_name | Queue name | DF-WRK-003 | rwb-case |
| team_code | Team that works the queue, for example LIT-BKK | DF-WRK-004 | rwb-case |
| role_code | Role that works the queue, for example RW-LITOFF | DF-WRK-005 | rwb-access holds the role; the queue row points at it |
| assignment_method | How an officer is chosen, a value of LOV-ASSIGN | DF-WRK-006 | rwb-case |
| capacity_cap | The workload cap of a member of the queue | DF-WRK-007 | rwb-case |
| overflow_queue_code | The queue a case goes to when the cap is met, for example TDR-BKK-OVF | DF-WRK-008 | rwb-case |

The check record is this story's own: `checkId`, `state`, `validFrom`, `author`, `fileHash`, `rowCount`, `ownerLoad` and the finding list of row, field and code. It carries no personal data, no ACE column and no copy of a queue row. The two column names of the last two rows are Not specified in the source documents (GAP-2273; ASM-3752), and a member sheet in the same file is passed to the owner without inspection (GAP-2273; ASM-3753).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Right | Purpose |
|---|---|---|---|
| POST | /api/recovery/access/v1/admin/queue-file-checks | Reference data C | Load a queue file with `validFrom`, run the six checks, answer the check with its findings and its state |
| GET | /api/recovery/access/v1/admin/queue-file-checks/{checkId} | Reference data R | Read a check, its findings and its hand-off reference |

#### 12.2 REST operations consumed

| Contract | Operation | Used for |
|---|---|---|
| RWB-P3-E1019-CON | The reference-load operation of rwb-case (`POST /api/recovery/case/v1/admin/reference-loads`) | Storing the accepted queue version under the owner |
| RWB-P3-E1019-CON | The approve operation of rwb-case (`POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve`) | The second pair of eyes; the gate only reports its answer |
| RWB-P3-E1019-CON | The queue read of rwb-case (`GET /api/recovery/case/v1/queues`) | The queues in force, for QFC-1 |
| RWB-P3-E1043-CON | The list read of rwb-case (`GET /api/recovery/case/v1/admin/lists/{listCode}`) | LOV-ASSIGN and LOV-TEAM, for QFC-3 and QFC-4 |
| RWB-P3-E1042-CON | The parameters read of rwb-case (`GET /api/recovery/case/v1/admin/parameters`) | The cap maximum and the file and row limits, for QFC-5 |

#### 12.3 Events published

None. DP-09 is not in this story's pattern set: the acceptance entry of DP-03 is written locally with its outbox row and reaches `rwb.decision-record.v1` through the platform library, so `rwb.access.events.v1` carries nothing from this story.

#### 12.4 Events consumed

None. The gate is asked, it does not listen; the queues in force are read with the owner's contract and never mirrored as an event.

#### 12.5 Workflows and activities

None. No DP-10 and no DP-12: a check is one synchronous request with a bounded set of checks and no human wait.

#### 12.6 Schedules

None. Nothing in this story runs on a timer; a queue version takes effect from its own `validFrom` inside the owner.

#### 12.7 Tables owned

| Table | Access | Note |
|---|---|---|
| rwb_access.role | Read | The role catalogue at the version in force; written by RWB-P4-E1019-APP |
| rwb_access.permission | Read | The right of the caller in Reference data; written by RWB-P4-E1019-APP |
| No queue table | — | `queue` and `queue_member` are rwb-case's; the check record is held in `rwb_access` under this key's migration (GAP-2273; ASM-3748) |

#### 12.8 Contract fakes

| Fake | Answers |
|---|---|
| rwb-case queue fake (RWB-P3-E1019-CON) | The reference-load answer with a load reference, the approve answer, and the queues in force, with a case where the overflow queue is absent |
| rwb-case list fake (RWB-P3-E1043-CON) | LOV-ASSIGN and LOV-TEAM with a version label |
| rwb-case parameters fake (RWB-P3-E1042-CON) | The cap maximum, the row limit and the file size limit |
| Decision-record fake (RWB-PLT-E1027-CON) | An accepted entry, and a forced failure to prove the 503 path |
| ACE view stub | `v_ace_iam_group` rows for the roles of the test files, and an absent group for the refusal |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST, provided | 2 | The check and the check read, one hop from gateway-bff |
| REST, consumed | 5 | Three owner operations of the queue contract, the list read and the parameters read, 2 s timeout each |
| Kafka | 0 | The record travels through the platform library, not through this service's topic |
| Temporal | 0 | No workflow, no activity, no schedule |
| File | 1 | The multipart queue file, with its row and size limits read from the parameters contract |

### 13. Solution plan

| Component | What it does | Size |
|---|---|---|
| `QueueFileCheckController` | The two operations, authorisation, the idempotency key, the error envelope | 1 class, 2 handlers |
| `QueueFileParser` | Reads the queue sheet, numbers the rows, applies the file limits, refuses a malformed file | 1 class |
| `QueueFileValidator` | The six checks of section 8, each a separate rule with its own finding code | 6 rules |
| `QueueContractClient` | The five consumed operations against the contract faces, with the 2 s timeout and one retry on a GET | 1 class |
| `QueueCheckStore` | The check, its findings and its state in `rwb_access`, with the acceptance entry in the same transaction | 1 repository, 1 table |
| `AcceptanceRecorder` | The DP-03 entry and its outbox row | 1 class |
| Configuration | The finding codes, the message keys and the parameters keys as configuration, not constants | 1 file |

### 14. Validation and messages

| Condition | Message | Retryable |
|---|---|---|
| Required field empty in the file header or a row | MSG-GEN-001 "Enter {field}." | Yes, with a corrected file |
| No right in Reference data | MSG-P4-002 "You cannot {action} here. Your role does not include it." | No |
| Any Error finding | MSG-P1-002 "The {source} load for {date} was refused: {check}. The previous load is still in use." with the row and the field named | Yes, with a corrected file |
| Author presented as approver | MSG-P7-002, answered by the owner's approve operation with 409 | No |
| Record cannot be written | MSG-P7-003 "The action was not taken because the decision could not be recorded. Try again in a few minutes." | Yes |
| Rollback of a version with no earlier version | MSG-P3-015, answered by the owner; the gate does not roll back | No |
| A case or queue outside the caller's scope | MSG-P4-003 "This case is not in your scope." on the queue view | No |

### 15. Screens and states

| Screen | States shown |
|---|---|
| SCR-42 Queues and service levels | Versions; load. The queue list with team, role, assignment method and cap; the file picker with its valid from date; the check answer with its findings by row and field; the hand-off reference; the approval state as the owner reports it |
| SCR-43 Roles and access | Read only here: the role and its Entra group, through the role catalogue |

The screen is composed by gateway-bff (DP-19) in one hop per call; it never chains a call. A refused check keeps the previous version in force on the screen, with the refused file still downloadable for repair. No screen state is stored, and no state survives a reload except the check itself.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-014-01 | AC1 | End to end | The queue file of FSD P4 AC-P4-003-01 shape, 12 queues for the TDR, DIL, litigation, NPA, debt sale and write-off teams; the owner fake in force; the screen through gateway-bff |
| TC-AD-014-02 | AC2 | End to end | A queue whose `overflow_queue_code` is neither in the file nor in force, for example TDR-BKK-OVF when TDR-BKK-OVF is absent; the owner fake without it |
| TC-AD-014-03 | Access | Component | A caller whose Reference data letter is "-" and a caller whose letter is R only |
| TC-AD-014-04 | Principle 5 | NFR | The decision-record fake forced to fail; the owner fake asserted as never called |

### 17. Guardrails

- No value a business person may change is written in code: the finding codes, the message keys, the cap maximum and the lists are configuration or reference data with a version.
- No personal data in the check, in the events, in the workflow inputs or in the logs; the file carries queue and role codes only, and a row is named by its number and its `queue_code`.
- ACE data only through the read-only `v_ace_iam_group` view or through the owner's contract; no ACE table is read, no queue table is written, and no statement names a table of another schema.

### 18. Traceability

| Source | Reference |
|---|---|
| Legacy story | RWB-AD-014 Configure queues, module P4, epic E8, priority Must, decision DL23, depends on RWB-E1-019; AC1 and AC2 carried with their origin tags; TC-AD-014-01 to TC-AD-014-04 carried |
| FSD P4 | A2.3 (hold roles as data, its load and approval), A2.17 (the administration screens), AC-P4-003-01, AC-ALT-P4-003-01, AC-ALT-P4-003-02, AC-EXC-P4-003-01, AC-EXC-P4-003-02, AC-EXC-P4-003-07, AC-EXC-P4-003-08; SCR-42 |
| TSD P4 | T6.1 (the RBAC matrix), T6.2 (each endpoint declares its area and right), T-A.1 (API-P4-005, API-P4-006, API-P4-009, API-P4-010) |
| Requirements | REQ-ACA-002, REQ-ACA-003, REQ-ACA-013 |
| Rules | R-UNI-38 (a version applies from its date), R-UNI-39 (no change without its record) |
| Patterns | DP-03, DP-05, DP-06, DP-07, DP-13, DP-19 of §R5.5 |

### 19. Out of scope

- The queue table, the member table, the capacity and the assignment: RWB-P3-E1019-APP and -DB.
- The reference-load operation, its approve, its verify and its rollback: RWB-P3-E1019-CON and the stories that implement it.
- The queue write interface for models and agents: RWB-P4-E2036-APP.
- Service levels and timers per state: RWB-AD-015 and the timer stories.
- The rule-version operations of the legacy endpoints row: RWB-AD-011 and RWB-AD-012.
- The screen build of SCR-42 beyond its composition route, and any event of this service's own topic.
