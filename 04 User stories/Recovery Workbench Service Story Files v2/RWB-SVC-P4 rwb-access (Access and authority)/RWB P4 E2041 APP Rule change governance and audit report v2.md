# RWB-P4-E2041-APP Rule change governance and audit report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2041-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-041 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-AX |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2041-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CWC-013, REQ-DRI-011) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-041 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P4-E2041-APP-L320, X20 RWB-P4-E2041-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 15 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **compliance and audit reader (RW-AUDIT)**, I want **every attempt to prepare, approve or export a rule change decided in one place — the letters that role holds in Rules and parameters, the separation of duties between the person who prepared the version and the person who approves it, and the entitlement to read and export the change report — with one access-log entry for every attempt**, so that **a rule change is governed as strictly as a code change, no version is approved by the person who prepared it, the audit can prove who could have changed a rule and who did not, and every export of the rule change report is attributable**.

Inside `rwb-access` this is the authority half of the legacy story RWB-E2-041:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the read `GET /api/recovery/access/v1/rule-authority`, which answers for one person and one action whether the C letter (prepare), the A letter (approve) or the R letter (read) is held in `RULES_AND_PARAMETERS`, whether the caller is the person who prepared the version, and which matrix version decided it; and the record `POST /api/recovery/access/v1/rule-report-exports`, which decides the R letter of an export, reads the row count and the version labels of the report for that period, and appends one access-log entry for the export.
- The rule registry, the rule rows, the rule test cases and the change checklist (`rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, DF-REF-295) stay with `rwb-decision` (P7) under ASM-0069; so do the four-eyes approval of a version, the move to `APPROVED`, the promotion at 00:01 (JOB-20 with `RulePackageInForce` EV-30), the one-call rollback and the change report itself. They are reached through `RWB-P3-E2041-CON`, the contract story of this legacy key, and this service holds no rule table and no report row.
- This story is not the report producer: it does not compute the effect of a version, does not count the decisions per package version, does not run the checklist gate and does not produce the CSV. It decides who may do those things, and it records that the attempt happened.
- Separation of duties is decided on the person and not on the role: a person may hold RW-COE and RW-RISK at once, and then the registry's own four-eyes answer is not enough, because the letter check alone would let that person approve the version they prepared. The person who prepared the version, as the registry records the author, is therefore refused the A letter for that version in this service, with the text of MSG-P7-002.
- No delegation of authority level applies: a rule package version is not a credit decision (legacy RWB-E2-041 section 10). The DoA table and `GET /doa-limits` are not read or called by this story; the authority here is the permission matrix in `RULES_AND_PARAMETERS` and the author reference of the version.
- The access log of the target is a decision-record entry of the local library of DP-03, written in the same transaction as the answer and published on `rwb.decision-record.v1`; there is no separate access-log table in `rwb_access` (ASM-1698). The rule change, its checklist and the report entries themselves are never read into this service beyond the fields the two answers need.
- No screen of its own is served: the SCR-39 Rules and parameters panel arrives through the gateway-bff composite route of DP-19, one hop per operation, and this story answers the two operations behind it.
- The roles and letters of the rule-administration area differ between the work package line, the legacy authority table and TSD P4 v3 T6.1, and the legacy access test names a role that the matrix gives the right; this story reads the technical specification as the source and records the difference (GAP-0962; ASM-1694).
- The record code an authority answer and an export are written under, the field shape of those values inside an entry of the chain, and the request and answer shapes of the two operations are Not specified in the source documents (GAP-0963; ASM-1695) and (GAP-0964; ASM-1696).

### 2. Business rationale

Audit found the collection procedure was not followed because the rules lived in documents (CTL-08). Rules are data now: one wrong row in a rule package changes every case that reaches it, so a rule change needs the evidence of a code change — who asked, what it affects, the test result, who approved, when it took effect and how to undo it. The legacy key RWB-E2-041 carries that journey inside one module and one process: the same person could load the workbook, approve it and read the report, because the checklist, the approval and the report were three methods of one screen against one set of rule rows (RWB-E2-041; FEAT-CWC-16; FSD P4 v3 A2.18).

In the target the governance of a version is central in `rwb-decision` (Architecture v5 slide 27; Temporal and Drools design slide 15: governance central, evaluation local), and the authority over who may take each step is the one thing that cannot be central, because it must hold for every service on the same day and must answer for a person and not for a module. That is this story: the letters in Rules and parameters, the person-level separation of duties, and the entitlement that lets an export leave the bank's reporting surface. Everything the legacy story built to make a change *happen* is P7's; everything that makes a change *permissible and provable* is here.

The measure the business reads is the FSD's own: rule and limit changes made without a code release, 100 percent, measured from the decision log and the Workbench records every month (FSD P4 v3 A2.18.1). A count of changes is only trustworthy when the log also says who was allowed to make them and who was refused, and that is what the second half of this story adds: one access-log entry for every prepare, approve, read and export attempt, allowed or refused, so audit can compare the changes that happened with the entitlements that existed (R-UNI-39; CTL-08).

This story meets REQ-CWC-013 on its authority side (a rule change goes from a validated load to production with a version stamp and no code release, and rolls back by one call — and the person who prepared it cannot approve it) and REQ-DRI-011 on its entitlement side (the versioned table carries author and approver, and the decisions per version are reported — and only a role with the report right may read or export that report). It supports measure decisions within the delegation of authority at 100 percent by proving that a rule change never borrows the credit approval path: no DoA level, no limit, no route role.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E2041-CON | The published contract this story builds against: the version facts the four-eyes check reads (version id, package code, label, state, author reference, test result, verify date) and the rule-change audit report read (period, package filter, format, page, total, the entry columns of the legacy story, the decisions per package version and the version labels), with its fakes. It is a C dependency, so it never blocks the build |
| RWB-P4-E1037-CON (same service, its own contract story) | The existing `POST /api/recovery/access/v1/authorise`, `GET /api/recovery/access/v1/me/permissions` and the role and permission tables behind the A letter, with the ADR refusal shape and MSG-P4-002. This story adds two operations beside them and changes neither |
| RWB-PLT-E1037-CON | The guard library that carries the same letters to the other services (DP-08), refreshed on `rwb.access.AccessPolicyChanged.v1` |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the access-log entry of every authority answer and every export |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract of `rwb-case` (DP-07): LOV-CAPABILITY with `RULES_AND_PARAMETERS` among its 14 areas, and LOV-VERSION-STATUS, with the version in force |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-E1047-CON | The topic-naming library (DP-14); this story publishes no event of its own and resolves no topic name by hand |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the SCR-39 panel calls the two operations through it, one hop each |
| RWB-PLT-E1042-CON, RWB-PLT-E1072-CON | The parameters client library (DP-06) and the Drools kit (DP-04). Both are in the service baseline and behind the P4 contract story; this story reads no parameter and embeds no rule engine |

Business preconditions carried from RWB-E2-041 and from the rule design:

- The letters in force are those of TSD P4 v3 T6.1 and its refinement: RW-COE holds `CRUD` in Rules and parameters and uploads, lists, dry-runs and rolls back a version; RW-RISK holds `RA` and approves a version; RW-AUDIT holds `R` and reads the package list, the versions, the dry-run counts and the change report; RW-REFADM holds `R` and prepares the change checklist and the load file, with no upload, no approval and no rollback; RW-PLATADM and RW-SECADM hold `R`; RW-COMPLY holds `R`; RW-CASEOWN holds `R`; RW-PHONECOL holds `-`. A person holds the union of the letters of the roles held (FSD P4 v3 A2.1.4.2).
- The permission matrix version in force in SIT is `PM-2026.11` (FSD P4 v3 A2.4 and A2.5).
- The change checklist has seven items — request, impact, test result, approver, load, verify and rollback plan — and a version cannot be approved while an item is missing or its test result has failed (TSD P4 v3 T6.3; DF-REF-295; MSG-P3-022). The gate is the registry's and this story does not repeat it.
- The author of a version is RW-COE and the approver is RW-RISK, and the author cannot approve (Temporal and Drools design slide 15; TSD P4 v3 T6.3; MSG-P7-002). This story holds the person-level half of that rule.
- Package `ALLOCATION` version `ALLOC-2026.11` is in force with 24 rows, and `ALLOC-2026.12` is the version the legacy flow raises, tests, approves and reports (RWB-E2-041 background and AC1).
- A rule package version is not a credit decision, so no delegation of authority level and no limit applies to it (RWB-E2-041 section 10).
- The scope of a service identity that asks this service about a person other than the session user — which right it holds, and in which area — is Not specified in the source documents (GAP-0965; ASM-1697).

### 4. Flow

1. The user opens SCR-39 Rules and parameters, panel rule versions, through the gateway-bff composite route (DP-19). The route reads the versions of the package from the registry and calls `GET /api/recovery/access/v1/rule-authority` for the signed-in person with `action` `PREPARE`, so the screen knows whether the change form is offered before it draws it. States of the panel: loading, while the versions and the authority answer are awaited, the change form is not drawn; empty, when the package has no version, no version row and no change form are drawn, and the empty text is Not specified in the source documents (DOR-RWB-P4-E2041-APP-10); error, when the authority answer is 503 with MSG-P7-003 (step 8), the change form is withheld; no access, when the answer is authorised false with refusalReason NO_LETTER or the export answer is 403 with MSG-P4-002 (step 11), the change form and the export action are hidden and the refusal state is shown.
2. `RuleAuthorityController` validates the query: `personReference`, `action` and `onDate` are required, and an empty one is 422 with MSG-GEN-001 naming the field; an `action` outside the three of the contract is 422 with MSG-GEN-001 naming `action`; `versionId` is required for `APPROVE` and its absence is the same 422; the capability area `RULES_AND_PARAMETERS` is checked against LOV-CAPABILITY of DP-07 with the version in force, never against a constant.
3. `SessionAuthority` decides whether the caller may ask about that person at all. The caller's own reference comes from the session, and a person may always ask about themselves; any other person reference needs the R letter in `RULES_AND_PARAMETERS` and is refused with 403 and MSG-P4-002 without reading a row of that person's permissions, so a caller cannot use the operation to map the matrix (BR10).
4. `PermissionReader` reads the `role` and `permission` rows of the person in `rwb_access`: the roles of the person, and the row of each role in `RULES_AND_PARAMETERS` with its `letters` and its `matrix_version`. For a person other than the session user the roles are resolved from the service's own SELECT-only `v_ace_iam_group` view (DP-05), because the group-to-role mapping is ACE data and no Workbench column holds it. In tests this mapping is served by the rwb-source-data contract fake (§12.8).
5. The letters of the person are the union across the roles held (FSD P4 v3 A2.1.4.2), and the answer carries that union: `mayPrepare` for the C letter, `mayApprove` for the A letter and `mayReadReport` for the R letter. A role with no row in the area, or a row whose letter is `-`, gives a false and never a default allow (BR3).
6. For `APPROVE` only, `RuleChangeReader` reads the version through `RWB-P3-E2041-CON` — `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions`, filtered to the `versionId` — one hop with a 2 s timeout and a breaker (DP-11). The author reference the registry reports is the only one the check may use; the request carries no author of its own (BR5).
7. `SeparationOfDuties` compares the caller reference with the author reference of the version. Equal is `FAIL` with `refusalReason` `PREPARER_IS_APPROVER`, whether or not the person holds the A letter through another role; different is `PASS`; any action other than `APPROVE` is `NOT_APPLICABLE` (BR4).
8. Where the version cannot be read, the answer is 503 with MSG-P7-003 and no authority answer at all: an approval authority that cannot be decided against the recorded author is not granted and not refused, because a guessed answer would let a preparer through (BR9).
9. The answer is 200 with `personReference`, `capabilityArea` `RULES_AND_PARAMETERS`, `letters`, `matrixVersion`, `action`, `authorised`, `refusalReason` (`NONE`, `NO_LETTER`, `PREPARER_IS_APPROVER`), `separationOfDuties`, `preparerReference`, `approverRole` `RW-RISK` and, when refused, the `messageId` of the refusal.
10. `AccessLogWriter` appends exactly one decision-record entry of DP-03 before the answer leaves the service: decision code `AC-READ` when the action is authorised and `AC-DENY` when it is not, with the caller reference, the capability area, the right, the action, the version label and the author reference where an approval was asked, the matrix version, the outcome and the time (BR7).
11. For an export the gateway or the reader calls `POST /api/recovery/access/v1/rule-report-exports` with `from`, `to`, `packageCode`, `format` and the `Idempotency-Key` of the submission. The controller resolves the R letter of the caller in `RULES_AND_PARAMETERS` and refuses 403 with MSG-P4-002 before anything is read, then refuses a `to` before a `from` with 422 and MSG-GEN-003 naming both fields (BR6, BR8).
12. `RuleReportClient` reads the report once through `RWB-P3-E2041-CON` — `GET /api/recovery/decision/v1/admin/rule-packages/change-report` with the period, the package filter and the maximum page size of 200 — and takes three values only: `total`, the distinct `versionLabel` of the entries read and nothing else. It returns no entry and no CSV to the caller.
13. `ExportRecorder` appends one entry with decision code `AC-EXPT`, the user reference, the period, the package, the format, `total` as the row count and the version labels covered, in the same transaction as the idempotency row, and the answer is 202 with `exportId`, `status` `RECORDED`, `rowCount`, `versionLabels`, the period and the format (BR8).
14. The bytes stay with the report producer: the gateway fetches the same period and format from the report operation after this call answers 202, and `rwb_access` holds no report row, no rule row and no case row. A replay of the same `Idempotency-Key` answers the first answer and writes no second entry and no second export id (BR11).
15. Where the entry or its idempotency row cannot be written, nothing is recorded and the answer is 503 with MSG-P7-003, with no export id; an export that is not in the record is not an export audit can attribute, so it is not taken (BR7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `personReference`, `action` or `onDate` is empty, `versionId` is missing for `APPROVE`, or the action is outside the contract set | 422 naming the field, no permission row is read and no entry is written | MSG-GEN-001 | AC1, AC3 |
| X2 | The caller asks about a person other than themselves without the R letter | 403 before any row of that person is read, so the matrix cannot be mapped | MSG-P4-002 | AC2 |
| X3 | The person holds no row in `RULES_AND_PARAMETERS`, or the row's letter is `-` | 200 with `authorised` false and `refusalReason` `NO_LETTER`; the action is not offered; one `AC-DENY` entry | MSG-P4-002 on the action, not on the read | AC2, AC3 |
| X4 | The caller holds the A letter and is the author reference the registry reports for the version | 200 with `authorised` false, `refusalReason` `PREPARER_IS_APPROVER`, `separationOfDuties` `FAIL` and MSG-P7-002; one `AC-DENY` entry; no approve call is made | MSG-P7-002 | AC3 |
| X5 | The version cannot be read from the registry inside 2 s, or the connection fails | 503 and no authority answer; neither granted nor refused, and no entry that would claim a decision | MSG-P7-003 | AC9 |
| X6 | The caller of an export holds no R letter | 403, no report read and no entry that names a period, a package or an entry of the report | MSG-P4-002 | AC2 |
| X7 | The export period ends before it starts | 422 naming `to` and `from`, no report read and no entry | MSG-GEN-003 | AC7 |
| X8 | The report read answers an empty page with `total` 0 | 202 with `rowCount` 0 and one `AC-EXPT` entry; the empty list is the producer's answer and is not treated as an error | None | AC5 |
| X9 | The entry of the authority or of the export cannot be written | 503 and no answer; no export id is returned and the decision record is not written at all | MSG-P7-003 | AC9 |
| X10 | The same export arrives twice with the same `Idempotency-Key` | The first answer is replayed; no second export id and no second entry | None | AC1 |
| X11 | The same authority question arrives twice with the same parameters | Both are answered and each writes its own entry, because a read is an event and not a state change | None | AC9 |

No exception path of this story changes a version, a rule row, a case or a task: this service decides an entitlement and records it, and the lifecycle of a version is the registry's.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against `RWB-P3-E2041-CON` and its fakes; it reads `role` and `permission` in its own schema and holds no rule table, no version state and no report row |
| Negotiable | The letters, the roles and the matrix version are rows read at run time; the action set and the refusal reasons are the contract's; the field shapes are settled with the API owner at the contract review |
| Valuable | One place decides who may prepare, approve, read and export a rule change, prevents a preparer from approving, and puts every attempt in the append-only log |
| Estimable | Two controllers, one permission reader, one separation-of-duties check, one registry client, one export recorder, five fakes and nine criteria |
| Small | Fits one sprint with its tests; no table of its own, no workflow, no schedule, no event of its own and no screen of its own |
| Testable | Each owned criterion has a test case in section 16, and the registry and report sides are stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Rule change governance and audit report

  Background:
    Given the environment is SIT
    Given the run date is 15 December 2026
    Given the permission matrix version "PM-2026.11" is in force
    Given test user "U-7101" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS" and prepared rule package version "ALLOC-2026.12" of package "ALLOCATION"
    Given test user "U-7103" holds RW-RISK with "RA" in "RULES_AND_PARAMETERS"
    Given test user "U-7102" holds RW-REFADM with "R" in "RULES_AND_PARAMETERS"
    Given test user "U-AUD-01" holds RW-AUDIT with "R" in "RULES_AND_PARAMETERS"
    Given test user "U-7111" holds RW-PHONECOL whose "RULES_AND_PARAMETERS" letters are "-"
    Given rule package "ALLOCATION" version "ALLOC-2026.11" is in force with 24 rows

  Scenario: AC1 The audit reader is entitled by R and the export is recorded (new, D-RCV-60)
    Given the rwb-decision contract mock returns the change report for 2026-12-01 to 2026-12-31 with total 4 and the four entries, one of them package "ALLOCATION", version "ALLOC-2026.12", request "CR-2026-0042", test result "PASSED", author "U-7101", approver "U-7103", approved on 2026-12-02 and valid from 2026-12-10
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-AUD-01", action "READ_REPORT" and onDate 15 December 2026
    Then the response is 200 with letters "R", capabilityArea "RULES_AND_PARAMETERS", mayReadReport true, mayExportReport true, authorised true, refusalReason "NONE" and matrixVersion "PM-2026.11"
    When POST /api/recovery/access/v1/rule-report-exports is called with from 2026-12-01, to 2026-12-31, packageCode "ALLOCATION", format "csv" and Idempotency-Key "k-e2041-1"
    Then the response is 202 with an exportId, status "RECORDED", rowCount 4 and the same period
    Then one decision-record entry is appended with decision code "AC-EXPT", user reference "U-AUD-01", capability area "RULES_AND_PARAMETERS", the period, the package, the format "csv" and row count 4, and no party identifier and no case data
    Then the CSV and the columns of each report entry are the report producer's, and no rule row and no report row is held in rwb_access

  Scenario: AC2 A role without R is refused the report and learns nothing (new, D-RCV-60)
    Given test user "U-7111" holds RW-PHONECOL whose "RULES_AND_PARAMETERS" letters are "-"
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-7111", action "READ_REPORT" and onDate 15 December 2026
    Then the response is 200 with letters "-", mayReadReport false, mayExportReport false, authorised false and refusalReason "NO_LETTER"
    When POST /api/recovery/access/v1/rule-report-exports is called for "U-7111" with from 2026-12-01, to 2026-12-31, packageCode "ALLOCATION" and format "csv"
    Then the response is 403 with message MSG-P4-002 and no exportId
    Then the rwb-decision contract fake records no call, so no period, no package and no entry of the report is disclosed
    Then one decision-record entry is appended with decision code "AC-DENY", capability area "RULES_AND_PARAMETERS", right "R" and refusalReason "NO_LETTER"

  Scenario: AC3 The letters decide prepare and approve, and the person who prepared cannot approve (new, D-RCV-60)
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-7102", action "PREPARE" and onDate 1 December 2026
    Then the response is 200 with letters "R", mayPrepare false, authorised false and refusalReason "NO_LETTER", because RW-REFADM prepares the checklist and the load file and holds no C letter, no A letter and no rollback
    Given the rwb-decision contract mock returns version "ALLOC-2026.12" of package "ALLOCATION" in state "LOADED" with author reference "U-7101"
    Given test user "U-7101" holds RW-COE and RW-RISK as well, so the letters of "U-7101" are "CRUDA"
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-7101", action "APPROVE", the versionId of "ALLOC-2026.12" and onDate 2 December 2026
    Then the response is 200 with mayApprove false, authorised false, refusalReason "PREPARER_IS_APPROVER", separationOfDuties "FAIL" and messageId MSG-P7-002
    Then the message text is the separation-of-duties text of the legacy story, unchanged
    Then one decision-record entry is appended with decision code "AC-DENY", the action, the version label and the author reference the mock returned
    Then this service makes no approve call, and the registry refuses the same approval with MSG-P7-002 when it is asked

  Scenario: AC4 Another person with A is authorised and the registry takes the approval (new, D-RCV-60)
    Given the rwb-decision contract mock returns version "ALLOC-2026.12" of package "ALLOCATION" in state "LOADED" with author reference "U-7101", verify date 2026-12-08 and test result "PASSED"
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-7103", action "APPROVE", the versionId of "ALLOC-2026.12" and onDate 9 December 2026
    Then the response is 200 with letters "RA", mayApprove true, authorised true, refusalReason "NONE", separationOfDuties "PASS", preparerReference "U-7101", approverRole "RW-RISK" and matrixVersion "PM-2026.11"
    Then one decision-record entry is appended with decision code "AC-READ", version label "ALLOC-2026.12", author reference "U-7101", caller reference "U-7103" and matrix version "PM-2026.11"
    Then the approval of the version and its move to "APPROVED" on 2026-12-09 are the registry's, and this service answers only mayApprove true
    Then the rwb-decision contract mock records exactly one call, the version read, and no approve call

  Scenario: AC5 An export of a period with no changes is recorded with no rows (new, D-RCV-60)
    Given the rwb-decision contract mock returns the change report for 2026-11-01 to 2026-11-15 with total 0 and no entry
    When POST /api/recovery/access/v1/rule-report-exports is called for "U-AUD-01" with from 2026-11-01, to 2026-11-15, packageCode "ALLOCATION" and format "json"
    Then the response is 202 with an exportId, status "RECORDED", rowCount 0 and the same period
    Then one decision-record entry is appended with decision code "AC-EXPT" and row count 0
    Then the empty list is the report producer's answer and this service neither invents a row nor drops the attempt

  Scenario: AC6 The checklist gate and the version state are the registry's and are not decided here (new, D-RCV-60)
    Given the rwb-decision contract mock returns version "RES-2026.12" of package "RESTRUCTURE" in state "LOADED" with author reference "U-7101" and a checklist whose rollback plan is missing
    Given the rwb-decision contract mock returns version "PMT-2026.12" of package "PAYMENT_MATCH" in state "LOADED" with author reference "U-7101" and test result "FAILED"
    Given the rwb-decision contract mock returns version "ALLOC-2026.13" of package "ALLOCATION" in state "LOADED" with author reference "U-7101", approver empty and valid from 2026-12-15
    Given the rwb-decision contract mock returns version "ALLOC-2026.14" of package "ALLOCATION" in state "LOADED" with author reference "U-7101", verify date 2026-12-07 and load time 2026-12-08
    When GET /api/recovery/access/v1/rule-authority is called for "U-7103" and action "APPROVE" with each of the four versions in turn
    Then each response is 200 with authorised true and separationOfDuties "PASS"
    Then no response carries a checklist answer, a test result answer, a version state or an approve decision
    Then the refusals MSG-P3-022 naming "rollback plan" and "test result", the version that is never approved and stays "LOADED" with approver empty, and MSG-GEN-003 naming "verifiedAt" and "loadedAt" are produced by the registry and are not produced, repeated or pre-empted here
    Then one decision-record entry is appended for each of the four answers, so an attempt is in the log even where the registry refuses it

  Scenario: AC7 A period in the wrong order is refused before anything is read or recorded (new, D-RCV-60)
    When POST /api/recovery/access/v1/rule-report-exports is called for "U-AUD-01" with from 2026-12-31 and to 2026-12-01
    Then the response is 422 with message MSG-GEN-003 naming "to" and "from"
    Then the rwb-decision contract fake records no call and no exportId is returned
    Then no decision-record entry is appended

  Scenario: AC8 The export entry names the versions covered, so the counts reconcile (new, D-RCV-60)
    Given the rwb-decision contract mock returns the change report for 2026-12-01 to 2026-12-31 with total 4 and the two version labels "ALLOC-2026.11" and "ALLOC-2026.12", with 96 decisions counted against "ALLOC-2026.11" and 1,204 against "ALLOC-2026.12"
    When POST /api/recovery/access/v1/rule-report-exports is called for "U-AUD-01" with from 2026-12-01, to 2026-12-31, packageCode "ALLOCATION" and format "json"
    Then the response is 202 with rowCount 4 and versionLabels "ALLOC-2026.11" and "ALLOC-2026.12"
    Then the entry carries the same two labels and the same row count
    Then the counts 96 and 1,204 are the report producer's and are not counted, recomputed or stored here
    Then the entry carries no party identifier and no case data

  Scenario: AC9 Every attempt writes one entry, and an answer that cannot be recorded is withheld (new, D-RCV-60)
    Given the decision-record store is available and its hash chain verifies
    When one READ_REPORT authority for "U-AUD-01" and one refused export for "U-7111" complete
    Then two decision-record entries are appended, the first with decision code "AC-READ" and the second with "AC-DENY", each with the caller reference, the capability area, the right, the outcome and the time
    Then neither entry carries a name, an e-mail address or a personal field, and each is appended before the answer is returned
    Then when the record cannot be written the authority call returns 503 with MSG-P7-003 and neither granted nor refused is answered, and the export call returns 503 with no exportId and records nothing
    Then when the registry cannot be read for an approval the same 503 is answered, because an authority whose version cannot be confirmed is not given

  Scenario: AC10 The export entry carries both version labels and the row count, and the counts stay the producer's (restated from TC-E2-041-10) (new, D-RCV-60)
    Given 96 decisions against "ALLOC-2026.11" and 1,204 against "ALLOC-2026.12" in December 2026
    When an export of December 2026 is made through POST /api/recovery/access/v1/rule-report-exports
    Then the one decision-record entry carries both version labels and the row count, and the counts are the report producer's

  Scenario: AC11 The letters are the union of the roles held, a dash is refused and a replayed export key writes once (new, D-RCV-60)
    Given test user "U-7101" holds RW-COE with "CRUD" and RW-RISK with "RA" in "RULES_AND_PARAMETERS"
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-7101", action "PREPARE" and onDate 1 December 2026
    Then the response is 200 with letters "CRUDA", mayPrepare true and matrixVersion "PM-2026.11"
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-7111", action "PREPARE" and onDate 1 December 2026
    Then the response is 200 with letters "-", mayPrepare false, authorised false and refusalReason "NO_LETTER"
    When POST /api/recovery/access/v1/rule-report-exports is called for "U-AUD-01" with from 2026-12-01, to 2026-12-31, packageCode "ALLOCATION", format "csv" and Idempotency-Key "k-e2041-1" a second time
    Then the response is the first answer with the same exportId and no second decision-record entry is appended

  Scenario: AC12 A request without a session is 401 and a route the contract does not provide is 404 (new, D-RCV-60)
    Given the request carries no session
    When GET /api/recovery/access/v1/rule-authority is called for personReference "U-AUD-01", action "READ_REPORT" and onDate 15 December 2026
    Then the response is 401 and no decision-record entry is appended
    When GET /api/recovery/access/v1/rule-report-exports is called for any exportId
    Then the response is 404 and no decision-record entry is appended
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The authority of a rule change is the letters held in the capability area `RULES_AND_PARAMETERS`: C to prepare a change, A to approve a version, R to read and export the report | TSD P4 v3 T6.1 and T6.1 refinement; FSD P4 v3 A2.18.3.1; legacy RWB-E2-041 sections 10 and 12 |
| BR2 | The letters of a person are the union of the letters of the roles held, read from `role` and `permission` with the matrix version in force; no letter is held by name in code | FSD P4 v3 A2.1.4.2; TSD P4 v3 T3.1 and T3.2; BR-P4-018 |
| BR3 | No row in the area, or a `-` letter, is a refusal and never a default allow; the answer says which letter was asked and which letters were found | FSD P4 v3 AC-ALT-P4-001-01 and AC-EXC-P4-004-06; TSD P4 v3 T6.1 |
| BR4 | A version cannot be approved by the person who prepared it: the caller reference is compared with the author reference the registry records for the version, and equality is refused with `PREPARER_IS_APPROVER` and MSG-P7-002 whatever other role the person holds | Legacy RWB-E2-041 BR2 (roles.txt Separation of duty); TSD P4 v3 T6.3; Temporal and Drools design slide 15 |
| BR5 | The author reference is never taken from the request: an approval authority is decided against the author the registry reports, so a caller cannot declare another person as the preparer | TSD P4 v3 T6.3; ASM-1696 |
| BR6 | The report read and the export need the R letter; a caller without it is refused before the report is read, so the refusal discloses no period, no package and no entry | FSD P4 v3 A2.16.3.3 and AC-EXC-P4-016-06; TSD P4 v3 T6.1 |
| BR7 | Every authority answer and every export appends exactly one access-log entry in the transaction that produces the answer, with no personal data; an answer that cannot be recorded is not returned | Principle 5; R-UNI-39; FSD P4 v3 A2.7 and A2.8 |
| BR8 | An export is recorded before it is served, with the period, the package, the format, the row count the report answered and the version labels covered; a period whose end is before its start is refused and nothing is recorded | Legacy RWB-E2-041 AC8 and AC9; FSD P4 v3 AC-ALT-P4-016-02 |
| BR9 | An authority that cannot be decided against a readable version is not given: the answer is 503 and neither granted nor refused, so a preparer cannot be let through by an unavailable registry | Legacy RWB-E2-041 AC2 (decision cannot be recorded, nothing changes); R-UNI-39 |
| BR10 | A person may ask about themselves; asking about another person needs the R letter, and the refusal happens before that person's permission row is read | FSD P4 v3 A2.4 AC-ALT-P4-004-02 (a refusal before the handler runs); TSD P4 v3 T6.2 |
| BR11 | One `Idempotency-Key` answers one export: a replay answers the first answer and writes no second entry and no second export id, while an authority read writes one entry per call because a read is an event | Architecture v5 slide 11; DP-09 |
| BR12 | No business value in code: the roles, the letters, the matrix version, the action set and the capability area are rows and list values with a version; a new role or a new letter needs no build | BR-P4-018; FSD P4 v3 A2.18.3.1; REQ-DRI-011 |
| BR13 | The checklist gate, the test result, the verify date, the version state, the approval and the promotion are the registry's and are observed, never repeated here | TSD P4 v3 T6.3 and T4; ASM-0069 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are one query over `permission` joined to `role` for the person's roles, with `RULES_AND_PARAMETERS` as the area and the matrix version in force as the version; the union is computed in the service and never read from a Java map of roles.
- BR3 is the shape of the answer: `letters` is whatever the rows hold, including `-`, and the three may-flags are derived from it, so an empty row and a dash row answer the same and both are refusals.
- BR4 and BR5 are the same comparison: the caller reference from the session against the author reference of the registry answer for that `versionId`, with the A letter checked first so a person without A is refused with `NO_LETTER` and never learns who authored the version.
- BR6 is the order of the export handler: the letter is resolved before the report client is called, so a refused caller costs no hop and sees no row count.
- BR7 and BR11 are the appender and the idempotency row of DP-03 and DP-09 in one transaction; a failure rolls both back, so an authority or an export can never exist without its record.
- BR8 is the field set of the `AC-EXPT` entry: the period, the package, the format, `total` as the row count and the version labels read, with no case id because an export has no case.
- BR9 is the fail-closed branch of the controller: a registry timeout or a 5xx becomes 503 with MSG-P7-003 and the answer is withheld.
- BR10 is the check on the person reference before the permission query, so the operation cannot be used to enumerate another person's rights.
- BR12 is checked by test: a new role, a new letter or a new matrix version is a row and a list value, and the build changes nothing.
- BR13 is the absence of a rule repository and of a checklist validator: the service has no entity, no query and no constant for a rule row, a version state or a checklist item.

### 9. State transitions

This service holds no case, task, version or report state. The states it answers are the outcomes of an authority decision and of an export record, and the chain it writes is append-only.

| From | Event | Condition | To |
|---|---|---|---|
| No answer | A read authority is asked | The letter is held and, for `APPROVE`, the caller is not the author | `AUTHORISED`, one `AC-READ` entry |
| No answer | A read authority is asked | The letter is not held | `REFUSED` with `NO_LETTER`, one `AC-DENY` entry |
| No answer | An approval authority is asked | The A letter is held and the caller is the author the registry reports | `REFUSED` with `PREPARER_IS_APPROVER`, one `AC-DENY` entry |
| No answer | An approval authority is asked | The version cannot be read | No answer, 503 with MSG-P7-003, no entry |
| No answer | An export is submitted | The R letter is held and the period is in order | `RECORDED`, one `AC-EXPT` entry, 202 |
| No answer | An export is submitted | The R letter is not held, or the period is in the wrong order | `REFUSED` before any read, one `AC-DENY` entry only where the letter was the reason |
| No answer | An export is submitted with a used `Idempotency-Key` | The first answer exists | The first answer replayed, no second entry |

| Command | Condition | Outcome |
|---|---|---|
| Record an authority answer | The entry commits | The answer is returned with the matrix version that decided it |
| Record an authority answer | The entry cannot be written | 503 with MSG-P7-003, no answer at all |
| Record an export | The entry and the idempotency row commit | 202 with the export id and the row count |
| Record an export | The entry cannot be written | 503 with MSG-P7-003 and no export id |

The version moves `LOADED` to `APPROVED` to `IN_FORCE`, and to `SUPERSEDED` or `ROLLED_BACK`, in the registry; this story reads the state it needs and changes none of it.

The action `APPROVE` is a contract constant of the action set in section 13 and is not a value of LOV-CAPABILITY. This story adds no value to LOV-CAPABILITY, and the 11 transitions above are the complete set.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Center of excellence analyst (RW-COE), `CRUD` in Rules and parameters | Is answered `mayPrepare` true and may raise a change on a loaded version and roll a version back in the registry; is answered `mayApprove` false without the A letter, and is refused `PREPARER_IS_APPROVER` for a version they authored even when they also hold RW-RISK |
| Risk and model risk officer (RW-RISK), `RA` in Rules and parameters | Is answered `mayApprove` true for a version another person authored, and approves it in the registry, not here |
| Reference data administrator (RW-REFADM), `R` in Rules and parameters | Prepares the change checklist and the load file and is answered `mayPrepare` false and `mayApprove` false: preparing a checklist is not a C letter, an upload or an approval (TSD P4 v3 T6.1) |
| Internal audit (RW-AUDIT), `R` in Rules and parameters | Reads and exports the change report, and every export is recorded against the reference |
| Compliance and PDPA officer (RW-COMPLY), `R` in Rules and parameters | Reads the change report on the same R letter as audit, and exports it only where the letter is held |
| Platform administrator (RW-PLATADM) and security administrator (RW-SECADM), `R` | Read the change report; neither may prepare, approve or roll back a version here |
| Case roles, for example RW-CASEOWN with `R` and RW-PHONECOL with `-` | Are answered what their row holds; a case role has no route to a rule change |
| `rwb-decision` (P7) | Reads the authority of an approver before it accepts an approval, through the same two operations or through the guard library's cached answer, and owns the version, its state, the four-eyes answer on the version and the promotion |
| The gateway-bff route | Calls the two operations for the signed-in user, one hop each, and caches nothing across users |
| `rwb-access` itself | Reads `role` and `permission` in its own schema and the group-to-role mapping in its own SELECT-only `v_ace_iam_group` view, and writes only entries of its own chain, its outbox rows and its idempotency rows |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right, and the separation-of-duties refusal carries MSG-P7-002 with the text of the legacy story. The unauthenticated shape is 401 with MSG-P4-001. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON with the rest of the service's contract. Which right a service identity holds to ask about a person other than the session user is Not specified in the source documents (GAP-0965; ASM-1697).

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-038; entra_group Not specified in the source documents (DOR-RWB-P4-E2041-APP-7) | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the roles of the person and their class |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the C, A and R letters in `RULES_AND_PARAMETERS` and the matrix version that decided them |
| (ACE view) | `v_ace_iam_group` | entra_group of the person | Read only, through the service's own SELECT-only view, when the question is about a person other than the session user (DP-05); not a Workbench column |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the authority entry and the export entry: `decision_code` DF-DEC-003 (`AC-READ`, `AC-DENY` or `AC-EXPT`, ASM-1695), `case_id` DF-DEC-002 empty for a rule change, `inputs_ref` DF-DEC-008 with the action, the version label, the author reference, the period, the package, the format, the row count and the matrix version, `actions` DF-DEC-014, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the export entry's replay |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of an export | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` (platform library table in `rwb_access`) | the record row of an authority answer and of an export | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-274 to DF-REF-298 | `rule_package`, `rule_package_version`, `rule_row` of `rwb_decision` | the package code, the version label, the state, the author reference, the test result, the verify date, the checklist and the decisions per version | Returned through the contract of `RWB-P3-E2041-CON`; not read |
| DF-REF-185 to DF-REF-197, DF-REF-299 | `rule_test_case` of `rwb_decision` | none | Not read |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` of `rwb_decision` | none: the central ledger is P7's | Not read and not written; the decisions per version are summed by the report producer |

No rule table exists in `rwb_access` and none is created: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are `rwb-decision`'s under ASM-0069, and their fields arrive in the contract, not by a schema read (DP-01). No row of `case`, `task` or `assignment` is read, and no party identifier and no case data enters an export entry (legacy RWB-E2-041 AC9). Where the record code and the field shape of an entry sit inside DF-DEC-001 to DF-DEC-018 is Not specified in the source documents (GAP-0963; ASM-1695). Field IDs are those of the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/rule-authority` | P4 `rwb-access` | Query: `personReference`, `action` (`PREPARE`, `APPROVE`, `READ_REPORT`), `versionId` (required for `APPROVE`), `onDate` | `personReference`, `capabilityArea` `RULES_AND_PARAMETERS`, `letters`, `matrixVersion`, `action`, `authorised`, `mayPrepare`, `mayApprove`, `mayReadReport`, `mayExportReport`, `refusalReason` (`NONE`, `NO_LETTER`, `PREPARER_IS_APPROVER`), `separationOfDuties` (`PASS`, `FAIL`, `NOT_APPLICABLE`), `preparerReference`, `approverRole` `RW-RISK`, `messageId` | 401 (MSG-P4-001); 403 asking about another person without R (MSG-P4-002); 422 a required field empty or an unknown action (MSG-GEN-001); 503 the version cannot be read or the answer cannot be recorded (MSG-P7-003) | The person's own session for themselves; Rules and parameters R for any other person; a service identity per ASM-1697 | Not applicable, read only; no Idempotency-Key |
| POST | `/api/recovery/access/v1/rule-report-exports` | P4 `rwb-access` | Body: `from`, `to`, `packageCode`, `format` (`json` or `csv`); header `Idempotency-Key` | `exportId`, `status` `RECORDED`, `rowCount`, `versionLabels[]`, `from`, `to`, `format`, `recordedAt` | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 422 a required field empty (MSG-GEN-001) or `to` before `from` (MSG-GEN-003); 503 the report cannot be read or the export cannot be recorded (MSG-P7-003) | Rules and parameters R | `Idempotency-Key` header required; the stored answer is replayed |

Both operations sit under the base `/api/recovery/access/v1` of DP-13. Neither is named in Architecture v5 slide 14, which lists `POST /authorise`, `GET /me/permissions`, `GET /doa-limits` and `GET /masking-policies` for this service, and neither is in API Specification v5 or TSD P4 v3 appendix T-A: their request and answer shapes are Not specified in the source documents (GAP-0964; ASM-1696), and the contract review confirms or renames the field set before the two operations are frozen. The export is a record and not a file: the operation decides the entitlement and records the export, and the bytes are the report producer's.

The authority decision is a read and answers 200 even when the answer is no, because the question it answers is about a person and the screen renders the reason; the export is an action and is refused with 403 when the letter is absent, because there is nothing to record and nothing to disclose (BR6, BR10). The letter part of the same matrix is also carried by the existing `POST /api/recovery/access/v1/authorise` of RWB-P4-E1037-CON, whose cached answer the guard library of DP-08 hands to the other services, so a service decides with no extra hop and the answer is dropped on `rwb.access.AccessPolicyChanged.v1`.

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11). Contract version fixed at v1 (the `/v1` path) for every consumed operation; no other version is built against.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 `rwb-decision` | The version of the request, filtered to its `versionId`: its label, its state and the author reference the separation-of-duties check uses |
| GET | `/api/recovery/decision/v1/admin/rule-packages/change-report` | P7 `rwb-decision` | The report page for the export period and package: `total` as the row count and the distinct version labels covered; no entry is held or returned |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The R check of the export and of the cross-person read, one hop with the answer cached for the session; MSG-P4-002 on a refusal |

Both `rwb-decision` operations are published by the contract story of this legacy key, `RWB-P3-E2041-CON`, which is this story's C dependency, and served by the report producer. The ownership ruling of the API map gives `GET /admin/rule-packages/change-report` to P7 (ownership.json, ASM-0040), and this story consumes it as a contract and never as a table. Neither operation is repeated, extended or shadowed here: the approval, the rollback, the promotion and the report's own columns are out of scope.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | one hash-chained entry per authority answer and per export: the decision code, the caller reference, the capability area, the right, the action, the version label and author reference where an approval was asked, the period, the package, the format, the row count and the matrix version |

CloudEvents 1.0 envelope; the payload carries references, codes, versions, dates and times and no name, no e-mail address and no personal field. This story publishes no `rwb.access.<Event>.v1` message: the two events of `rwb-access` are `AccessPolicyChanged` and `DoaLimitChanged`, owned by other stories of this service, and the rule-version event `rwb.decision.RulePackageInForce.v1` (EV-30) is published by the registry's promotion at 00:01, not here.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this story adds no subscription: the letters are read on request and the cached answer of the guard is dropped by the caller when this service publishes `AccessPolicyChanged`.

#### 12.5 Workflows and activities

None. This story starts no workflow, signals none and registers no activity on the `rwb-access` queue. The promotion at 00:01 (JOB-20) is a Temporal Schedule of `rwb-decision`, and the six-monthly access review list (JOB-18) belongs to another story of this service.

#### 12.6 Schedules

None. An authority answer is request-driven and an export is submitted by a person.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the roles of the person and their class |
| `permission` | P4 (`rwb_access`) | Read only: the C, A and R letters in `RULES_AND_PARAMETERS` and the matrix version |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of an authority answer and of an export. Read: the entry of an export for its replay |
| `idempotency_key`, `outbox_event`, `processed_event` | PLT library, created in `rwb_access` | The idempotency row and the outbox row of each entry; no inbox row is written because no event is consumed (DP-09) |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written: the version and the report arrive through the contract (ASM-0069) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's |
| `reference_version`, `reference_row`, `lov_value` of `rwb-case` | P3 (`rwb_case`) | Read through the reference-data contract of DP-07: LOV-CAPABILITY and LOV-VERSION-STATUS with the version in force |

No table of another service is read and no foreign key crosses a schema (DP-01). The group-to-role mapping is ACE data and is read through this service's own SELECT-only view, not through a Workbench table.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-decision rule-change fake | `RWB-P3-E2041-CON` | `GET /admin/rule-packages/{packageCode}/versions` answering version "ALLOC-2026.12" `LOADED` with author reference "U-7101", verify date 2026-12-08 and test result `PASSED` for AC3 and AC4; versions "RES-2026.12", "PMT-2026.12", "ALLOC-2026.13" and "ALLOC-2026.14" of AC6 with their author, checklist state, test result, approver and dates; `GET /admin/rule-packages/change-report` answering total 4 with the four entries and the two version labels for AC1 and AC8, total 0 for AC5, and a record of every call, so a refused export can assert that no call was made |
| decision-record fake | RWB-PLT-E1027-CON | The append of an entry, the hash-chain check, the replay of an export by `Idempotency-Key` and the forced write failure of AC9 |
| authorise and guard fake | RWB-P4-E1037-CON, RWB-PLT-E1037-CON | A granted answer for RW-AUDIT with R, for RW-RISK with A and R, for RW-COE with CRUD and for RW-REFADM with R; a refused answer with MSG-P4-002 for RW-PHONECOL with `-` |
| reference-data fake | RWB-P3-E1043-CON | LOV-CAPABILITY with `RULES_AND_PARAMETERS` among the 14 areas and LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED), each with its version |
| gateway-bff fake | RWB-PLT-N001-CON | The SCR-39 rule-versions panel with the change form offered or hidden from the authority answer, the export action and the refusal state |
| permission fixture | RWB-P4-E1037-CON | Matrix version `PM-2026.11` with the letters of RW-COE, RW-RISK, RW-REFADM, RW-AUDIT, RW-COMPLY, RW-CASEOWN and RW-PHONECOL in `RULES_AND_PARAMETERS` |
| rwb-source-data contract fake | DP-05 group-to-role mapping of a person other than the session user | The entra_group of that person and the roles it maps to; no ACE view is set up directly by the tests |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2; consumed 3 | Base `/api/recovery/access/v1`; two `rwb-decision` reads and the own authorise path, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision.DecisionRecorded.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The promotion at 00:01 is a Schedule of `rwb-decision` |
| File | None | No file input and no file output; the CSV is produced and served by the report producer |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/ruleauthority`, Java package `th.co.scb.ace.workbench.recovery.access.ruleauthority`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module rule-version screen whose permission checks, approval and report sat in one process (DP-13 and DP-19: the service's own base and the two operations behind the composite route) and the monolith's own decision log write (DP-03: the local chain of the library). DP-04 is carried by the legacy key and its work sits with the P7 slice: the Drools kit, the compile, the KieBase and the evaluation of a package are `rwb-decision`'s and of the model-owning services, and this story embeds no rule engine and reads no package. DP-05 is one read of the group-to-role mapping through this service's own `v_ace_iam_group` view, which is ACE data and not a Workbench column. DP-06 is carried by the key and adds nothing here: no parameter is read by this story, and the parameters client is in the service baseline behind RWB-P4-E1037-CON. DP-14 is the naming library alone: this story publishes no event of its own, and the access-log entry travels on `rwb.decision-record.v1`.

This secondary slice adds no new build dependency of its own (metadata "Depends on (build)" is None): the libraries, the per-service Flyway baseline, the outbox, the guard and the gateway route are already build dependencies of the P4 service's own stories, in particular RWB-P4-E1037-CON, and this story builds against `RWB-P3-E2041-CON` and its fakes, which never block (ASM-1699). The eight platform contracts the DP table names are read as part of the build list (GAP-2414), and the registry operations are those published by RWB-P7-E2042-APP, built against the fake of section 12.8; re-checked at the wave 2 kick-off.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleAuthorityController | Controller | `GET /rule-authority`: query validation, the person check, the RFC 9457 mapping and the `messageId` of each refusal |
| RuleReportExportController | Controller | `POST /rule-report-exports`: the R check before any read, the period order, the 202 and the replay |
| PermissionReader | Service | The `role` and `permission` rows of the person in `RULES_AND_PARAMETERS`, the union of the letters, and the matrix version that decided them |
| SessionAuthority | Service | Self or another person: the session reference, the R letter for a third party, and the refusal before any permission row is read |
| RuleChangeReader | Client | The version read of `RWB-P3-E2041-CON`, one hop and 2 s, with a breaker; a timeout becomes 503 |
| RuleReportClient | Client | The report page read of `RWB-P3-E2041-CON` for `total` and the version labels only; it holds no entry and returns no CSV |
| SeparationOfDuties | Service | BR4 and BR5: the caller reference against the author reference the registry reports, with the three outcomes |
| ActionCatalog | Service | The three actions, the letter each asks, and the capability area checked against LOV-CAPABILITY of DP-07; no role name and no letter in code |
| AccessLogWriter | Service | The DP-03 entry of an authority answer, with its outbox row, in the transaction that produces the answer |
| ExportRecorder | Service | The `AC-EXPT` entry, its version labels and its idempotency row in one transaction, and the replay by key |
| ExportIdMinter | Service | The `exportId` of a recorded export, minted once per `Idempotency-Key` |

**Database and migrations**

- This story creates no table of its own. The local decision-record table of DP-03 and the platform library objects `outbox_event`, `processed_event` and `idempotency_key` are created in `rwb_access` by the service's own DB work in the per-service Flyway sequence of DP-15, and this story only writes and reads them.
- No rule table is created and no rule column is added: the registry holds `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` (ASM-0069), and a version and a report arrive as documents of the contract.
- The two read paths are `permission` by `role_id` and capability area, and `role` by the roles of the person. Where the SIT query plan needs an index that the creating story does not have, the index is added to that story's migration and not to a new one here.
- No statement updates or deletes an entry: the chain is append-only, and the writes of this story are one entry, one outbox row and, for an export, one idempotency row per attempt.
- The entry, the outbox row and the idempotency row commit in one transaction; a failure rolls all of them back, which is why AC9 answers 503 with nothing written.

**Configuration and reference data**

- The roles and the letters are rows of `role` and `permission` in `rwb_access`, loaded as a matrix version by the access-administration stories of this service; the version in force in SIT is `PM-2026.11`. No role code, no letter and no matrix version is a constant in code (BR12).
- `RULES_AND_PARAMETERS` among the 14 capability areas of LOV-CAPABILITY, and the version states of LOV-VERSION-STATUS, are read through the reference-data contract of DP-07 with the version in force (RWB-P3-E1043-CON).
- The action set ({`PREPARE`, `APPROVE`, `READ_REPORT`}) and the refusal reasons ({`NONE`, `NO_LETTER`, `PREPARER_IS_APPROVER`}) are contract constants, published by `RWB-P3-E2041-CON` and by the two operations of section 12.1; a new action is a contract change reviewed with the registry owner and with audit.
- The approver role `RW-RISK` is the role the technical specification names for the approval and is answered as data from the contract; this service resolves no role name of its own.

**Build steps**

1. `PermissionReader` and `ActionCatalog` over the `role` and `permission` rows and LOV-CAPABILITY; test the union of the letters of AC3 and the dash row of AC2, and that a new role or letter is data with no build (BR12).
2. `SessionAuthority`: self, another person with R, and the refusal before the permission query; the 403 of X2 with no row read.
3. `RuleChangeReader` against the contract fake: the version read of AC4, the four versions of AC6 and the timeout of X5.
4. `SeparationOfDuties`: the `PREPARER_IS_APPROVER` refusal of AC3 with MSG-P7-002, the `PASS` of AC4, and the proof that the author comes from the registry and never from the request (BR5).
5. `AccessLogWriter` with the outbox row in one transaction; AC9 for the allowed and the refused entry, and the 503 when the entry cannot be written.
6. `RuleReportClient` and `RuleReportExportController`: the R check before the read, the period order of AC7 and the total-4 read of AC1.
7. `ExportRecorder` and `ExportIdMinter`: the `AC-EXPT` entry with its row count and version labels for AC1 and AC8, row count 0 for AC5, and the replay by `Idempotency-Key`.
8. The composite-route run of the four SCR-39 states through the gateway-bff fake, so the panel can be demonstrated while the registry and the report are being built.

**Feature switch.** No switch of this slice's own: an authority that is switched off would either grant by default or refuse every rule change, and both are worse than the letter check. The service-level flag of the service baseline governs the administration surface, and this story adds no flag and removes nothing when a version is rolled back, because the letters are read on every call.

**Done when.** The tests in section 16 pass; audit reads and exports the change report of December 2026 with one `AC-EXPT` entry carrying row count 4 and the two version labels; a phone collector with `-` is refused with MSG-P4-002 and the report fake records no call; the reference data administrator is answered `mayPrepare` false; the analyst who prepared "ALLOC-2026.12" is refused `PREPARER_IS_APPROVER` with MSG-P7-002 while Risk is answered `PASS` and may approve; the four registry refusals of AC6 are produced by the registry and not here; and a forced record failure answers 503 with MSG-P7-003 and nothing written.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Rules and parameters R for an export or for a question about another person | You cannot {action} here. Your role does not include it. | This story, from the authorise answer |
| MSG-P7-002 | The caller holds the A letter and is the author of the version asked about | You prepared this decision, so you cannot approve it. | This story, on the approval authority; the registry answers the same text on its own approval path |
| MSG-GEN-001 | A required query or body field is empty, or `action` is outside the contract set | Enter {field}. | This story, on both operations |
| MSG-GEN-003 | The export period ends before it starts | {field} cannot be before {other}. | This story, on the export, naming `to` and `from` |
| MSG-P7-003 | The registry cannot be read, or the entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |
| MSG-P3-022 | A checklist item is missing or the test result has failed at approval | The change cannot be approved: {item} is missing or failed. | The registry, on its approval; this story produces neither the refusal nor its text, and asserts it through the fake (AC6) |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The 200 of a refused authority also carries `refusalReason` and `letters`, so the screen can say which letter was missing without a second call, and the 403 of an export carries no period, no package and no row count.

### 15. Screens and states

No screen is built in this story. The SCR-39 panel is served through the gateway-bff composite route of DP-19, which calls the two operations, one hop each, and merges their answers with the registry's versions.

| Screen | State | What it shows | Where it is |
|---|---|---|---|
| SCR-39 Rules and parameters | Versions, with the change action offered | The versions of the package with their state and label, and the change form offered because `mayPrepare` is true | Gateway-bff (RWB-PLT-N001-CON); the registry's versions and this story's authority |
| SCR-39 Rules and parameters | Change not offered | No change form, and the letter that is missing named from `letters` | Gateway-bff; this story's answer |
| SCR-39 Rules and parameters | Approval offered to another person | The approve action offered to RW-RISK, with `approverRole` `RW-RISK` and `separationOfDuties` `PASS` | Gateway-bff; the approval itself is the registry's |
| SCR-39 Rules and parameters | Prepared by the caller | The approve action hidden and MSG-P7-002 shown, because the caller authored the version | Gateway-bff; this story's answer |
| SCR-39 Rules and parameters | Export recorded | The export with its id, its row count and the version labels covered, and the note that the CSV is served by the report | Gateway-bff; this story's answer |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (CG-ALL-5413) | Gateway-bff (RWB-PLT-N001-CON) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-5413) | Gateway-bff (RWB-PLT-N001-CON) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (CG-ALL-5413) | Gateway-bff (RWB-PLT-N001-CON) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (CG-ALL-5413) | Gateway-bff (RWB-PLT-N001-CON) |
| Access audit query | The export and the refusal entries of a period | The `AC-EXPT` and `AC-DENY` entries of this capability, with the user reference, the right and the time | The access-log story of this service (legacy RWB-E1-039) |

Approval is not a state of this story: the approve action on a loaded version is the registry's, so the panel links to the decision center rather than approving here, and this story's answer only says whether the person in front of the screen may be the one to do it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-041-01 | AC1, AC4, BR4, BR5 | Contract | ALLOCATION "ALLOC-2026.11" to "ALLOC-2026.12", request "CR-2026-0042", author "U-7101", approver "U-7103" on 2026-12-02; the report fake answers total 4 and the version read answers author "U-7101" |
| TC-E2-041-02 | AC2, BR13 | Component | ALLOCATION "ALLOC-2026.13" loaded by "U-7101", valid from 2026-12-15, never approved: the authority answer is unchanged and the report shows "LOADED" with approver empty |
| TC-E2-041-03 | AC3, BR13 | Component | RESTRUCTURE "RES-2026.12" with no rollback plan: the registry refuses with MSG-P3-022 naming "rollback plan" and stays "LOADED" |
| TC-E2-041-04 | AC4, BR13 | Component | PAYMENT_MATCH "PMT-2026.12" with test result "FAILED" and 2 of 58 scenarios failing: the registry refuses with MSG-P3-022 naming "test result" |
| TC-E2-041-05 | AC5, BR4 | Component | Verify date 2026-12-08 and approval 2026-12-09 by a person other than the author: `separationOfDuties` "PASS" |
| TC-E2-041-06 | AC6, BR8 | Component | Period 2026-11-01 to 2026-11-15 with no versions: total 0, row count 0 and one `AC-EXPT` entry |
| TC-E2-041-07 | AC7, BR13 | Contract | Verify date 2026-12-07 before the load time 2026-12-08: the registry refuses with MSG-GEN-003 naming "verifiedAt" and "loadedAt", and the authority answer is unchanged |
| TC-E2-041-08 | AC8, BR8 | Component | Export period 2026-12-31 to 2026-12-01: 422 with MSG-GEN-003 naming "to" and "from", no report read and no entry |
| TC-E2-041-09 | AC9, BR8 | Contract | CSV export of the December versions: 202 with format "csv", one entry with no party identifier and no case data, and the CSV served by the report producer |
| TC-E2-041-10 | AC10, BR8 | Contract | 96 decisions against "ALLOC-2026.11" and 1,204 against "ALLOC-2026.12" in December 2026: the entry carries both labels and the row count, and the counts stay the producer's |
| TC-E2-041-11 | AC2, AC3, AC9 | Component | RW-PHONECOL with `-` reads and exports and is refused with MSG-P4-002; RW-REFADM with R only is refused the prepare; the record store is forced to fail on one authority and one export |
| TC-E2-041-12 | BR1, BR2, BR3, BR13 | Component | Table boundary of §12.7: a person with no `permission` row in `RULES_AND_PARAMETERS` and a person whose only row there is `-` are both answered with no letter; no `rule_*` table of `rwb_decision` is queried |
| TC-E2-041-13 | BR6, BR10 | Component | A caller without the R letter asks about another person and exports: 403 with MSG-P4-002 before any `permission` row of that person is read and before the report client is called |
| TC-E2-041-14 | BR7, BR9, BR11 | Component | The registry read times out on an `APPROVE` question: 503 with MSG-P7-003 and no authority answer; a replayed `Idempotency-Key` answers the first answer with no second entry; each authority read writes one `AC-READ` entry |
| TC-E2-041-15 | BR12 | Component | A new role code and a new letter added as rows of a new matrix version: the authority answer changes with no build |
| TC-E2-041-16 | AC11, BR1, BR2, BR3, BR11 | Component | U-7101 with RW-COE "CRUD" and RW-RISK "RA" answers "CRUDA"; U-7111 with "-" is refused with NO_LETTER; a replayed `Idempotency-Key` "k-e2041-1" writes no second entry |
| TC-E2-041-17 | AC12 | Contract | A request with no session answers 401 with no entry; a route the contract does not provide answers 404; the 404 condition for the provided operations is Not specified in the source documents (NEWAC-RWB-P4-E2041-APP-AC12) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The eleven legacy rows of the key are kept, six rows TC-E2-041-12 to TC-E2-041-17 are added for the rules, the table boundary and the new criteria, and each legacy row now proves the part of its criterion this slice owns; the level System maps to Contract or Component as the rows show, and Access to Component. The rows whose rule lives in the registry (the checklist gate, the failed test result, the never-approved version, the verify date) use this story's authority answer and the contract fake for the rest, so the slice proves that it decides the entitlement and does not repeat the gate. The ITG copy of the set is RWB-ITG-E2041-ITG and is not written here, so no `-ITG` id appears in this table. The SIT harness values (repository, environment, seeding, evidence format, retention, pass/fail gate and the composite route detail) are held as data in the harness pack and agreed with QA and the platform edge story at the wave 2 entry check; they are not written here. Scope: this story holds rule package versions only (ALLOCATION, RESTRUCTURE, PAYMENT_MATCH); the reference-data checklist and its report stay with RWB-E1-043. The retention of the audit read in AC1 and AC9 follows the retention of the decision-record entries it summarises.

### 17. Guardrails

- No business value in code: the roles, the letters, the matrix version, the action set and the capability area are rows and list values with a version; a test proves that a new role, a new letter or a new matrix version needs no build (BR12).
- No personal data anywhere: the two operations carry user references, codes, versions, dates, periods and counts, and no name, no e-mail address and no personal field appears in an answer, an entry, a payload or a test (NFR-040).
- No read of another service's tables (DP-01): `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` are `rwb-decision`'s, the case and its task are `rwb-case`'s, and no join crosses a schema. The group-to-role mapping is read through this service's own SELECT-only ACE view and is never copied into a Workbench table.
- One writer for a version: only `rwb-decision` approves, promotes and rolls back a version. This story exposes no approve path, holds no rule table and starts no workflow, so a change cannot approve itself.
- No record, no answer: the entry commits with the answer, and an authority or an export that cannot be recorded is withheld with MSG-P7-003, so nothing is granted that audit cannot read (BR7).
- A refused caller learns nothing: the 403 of an export names the missing right and no period, no package and no row count, and the person check refuses before another person's permission row is read (BR6, BR10).
- The separation of duties is on the person, not on the role, and the author is the registry's value: a caller cannot declare a different preparer to obtain the A letter (BR4, BR5).
- The evidence is copied and never recomputed: the row count and the version labels are the report's, the author and the state are the registry's, and this service counts no decision and computes no effect of a version (BR13).
- The export is a record and not a file: no report row, no CSV and no case data is stored in `rwb_access`, so a copy of the report cannot leak from this schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | A rule change goes from a validated load to production with a checklist, a version stamp and no code release, and rolls back by one call | Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | BR1, BR2, BR3, BR4, BR5, BR12, BR13 | TC-E2-041-01, TC-E2-041-02, TC-E2-041-03, TC-E2-041-04, TC-E2-041-05, TC-E2-041-07, TC-E2-041-11, TC-E2-041-12, TC-E2-041-15 |
| REQ-DRI-011 | The versioned table carries author and approver, and the decisions per version are counted and reported | Epic 1, section 4; Program, section 5.7 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | BR6, BR7, BR8, BR9, BR10, BR11 | TC-E2-041-06, TC-E2-041-08, TC-E2-041-09, TC-E2-041-10, TC-E2-041-11, TC-E2-041-13, TC-E2-041-14 |

The requirement IDs are the set the Work Package fixes for this story.

| Legacy reference | Where it is kept |
|---|---|
| The change checklist, the seven items and MSG-P3-022 at approval | Sections 3, 5, 8 BR13, 12.2, 16 — the registry's, asserted through the fake |
| The approver is not the author, and the author of the version is RW-COE while the approver is RW-RISK | Sections 1, 3, 4, 7 AC3 and AC4, 8 BR4, 10 |
| RW-COE loads, RW-RISK approves, RW-AUDIT reads and exports the report, RW-REFADM prepares the checklist only | Sections 3, 10, 13 configuration, 16 |
| The report carries the request reference, the impact, the verify note and date, the test result, the author, the approver, the load, the checksum, the rollback plan and the decisions per package version | Sections 1, 12.2, 16 — produced by the report, not held here |
| AC9 no party identifier and no case data in the CSV | Sections 7 AC1, 11, 17 |
| MSG-P4-002, MSG-P7-002, MSG-P7-003, MSG-GEN-001, MSG-GEN-003 | Section 14, exception paths |
| Rule IDs R-UNI-38, R-UNI-39 and control CTL-08 | Sections 2, 8, 17 |
| Legacy endpoints `POST /admin/rule-packages/{packageCode}/versions`, the approve path and `GET /admin/rule-packages/change-report` | Sections 1, 12.2, 19 — all the registry's and the report producer's |
| Field IDs DF-REF-034 to DF-REF-044, DF-REF-274 to DF-REF-298, DF-DEC-001 to DF-DEC-018 | Section 11 |
| Legacy key RWB-E2-041, story RWB-P4-E2041-APP, contract RWB-P3-E2041-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The report itself and the ten legacy criteria: RWB-P3-E2041-APP, the slice that owns AC1 to AC10 of the key, with the entry columns, the effect of a version, the decisions per package version, the empty period and the CSV. This story decides who may read and export it and records the export.
- The registry half under `rwb-decision`: RWB-P7-E2041-APP with the checklist gate, the compile and the checksum, the scenario run and the dry run, the four-eyes approval on the version with its MSG-P7-002, the version states, the promotion at 00:01 with `RulePackageInForce` and the one-call rollback. This story reads the version facts and makes no approve call.
- The `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables and their migrations; they are `rwb-decision`'s under ASM-0069.
- The change record of the administration screen: RWB-P4-E8007-APP (legacy RWB-E8-007), which raises and records a change request. This story decides the authority of the person who raises it and neither repeats nor extends that record.
- The role-to-permission matrix itself, its load and its approval: RWB-P4-E1037-CON and the access-administration stories of this service. This story reads the rows.
- The delegation of authority table: a rule package version is not a credit decision, and no level, limit or route role applies (legacy RWB-E2-041 section 10).
- The screen SCR-39 and its composite route: RWB-PLT-N001-CON and the Epic 8 screen work.
- The access audit query screen and its list: the access-log story of this service (legacy RWB-E1-039).
- The integration harness RWB-ITG-E2041-ITG and the `-ITG` copies of the test cases.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
