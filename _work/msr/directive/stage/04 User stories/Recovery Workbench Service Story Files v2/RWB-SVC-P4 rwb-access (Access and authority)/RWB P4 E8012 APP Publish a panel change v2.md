# RWB-P4-E8012-APP Publish a panel change

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BF |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E8012-APP-16) |
| Depends on (build) | RWB-P4-E8012-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P4-E8012-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-012 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer**, I want **an access-panel configuration version put in force from an effective date by one publication that checks my right, checks that the version is approved, checks the date against the bounds in force, closes the version it replaces on the day before, records the act once and announces it so every authorise cache refreshes**, so that **roles, permission letters, default scope, masking rows and limits change on a date and not at a release, exactly one version decides on any day, and the publication can be shown afterwards without asking either team**.

Inside `rwb-access` this is the publication gate of the legacy story RWB-E8-012:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the write `POST /api/recovery/access/v1/admin/config-versions/{versionId}/publish`, which puts a configuration version in force from a date and answers it; and the read `GET /api/recovery/access/v1/admin/config-versions`, which answers the configuration versions this service holds with the state each of them is in today.
- A **configuration version** is a set of access-panel rows that share one version label: `permission.matrix_version` (DF-REF-044), `masking_rule.masking_version` (DF-REF-202) and `delegation_limit.limit_version` (DF-REF-055), with the `valid_from` and `valid_to` those rows carry. **No new table is created for it**: the version is a label over rows of three tables this service already owns, and `versionId` is the identity the contract gives that triple.
- The state set of a configuration version is LOV-VERSION-STATUS of TSD P4 v3 T3.2: `LOADED`, `VALIDATED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK`, `REFUSED`. `IN_FORCE` and `SUPERSEDED` are derived from the `valid_from` and `valid_to` of the rows; `VALIDATED`, `APPROVED`, `ROLLED_BACK` and `REFUSED` are carried on the decision-record entry of the version, because the three tables carry no state column — the version labels and the date windows are their only version columns in TSD P4 v3 T3.1, and T3.0's standard columns are not declared for them. The point is carried once, with the rest of the key's open points, in Not specified in the source documents (GAP-0872; ASM-1583).
- Publishing puts a version in force from an effective date and does four things in one transaction: the rows of the version that carry a date window take `valid_from` = the effective date; the rows of the version in force take `valid_to` = the day before the effective date; the act is appended to the local decision-record chain of DP-03 with both labels, the effective date, the reason, the actor reference and the time; and `rwb.access.AccessPolicyChanged.v1` is staged in the outbox so the authorise caches of every consumer refresh.
- **No Schedule and no Temporal job is added.** The version in force is resolved at read time by `POST /authorise` as the version whose `valid_from` ≤ today < `valid_to`, so an effective date needs no clock of its own and no promotion job: the date is data, the resolution is a read, and the six-monthly access review list (JOB-18) stays the only Schedule of this service.
- The "panel" this story publishes is the **access panel**: roles, permission letters, default scope, masking rows and limits. The **partner panel, the partner firm, the partner users, the fee schedule and the partner service levels are S9's** — the ownership map gives `partner`, `partner_user` and `partner_instruction` to `rwb-partner` — and they are neither read nor written here. That is the resolution of the conflict between this legacy key and FEAT-PRM-02, and it is carried in the key's gap row (GAP-0872; ASM-1583).
- Every publication appends one entry to the local decision-record chain of the library of DP-03, in the same transaction as the dates it writes, hash-linked to the entry before it, and publishes it as `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1`. The central ledger `decision_log_entry` stays in `rwb-decision` (P7) and is never read or written here.
- `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` is the one business event of the capability, and Architecture v5 slide 43 gives it the consumers "all (cache refresh)". Its payload carries the version labels, the effective date, the id of the version it supersedes and the publishing role, and no person and no personal data. `rwb.access.DoaLimitChanged.v1` belongs to RWB-P4-E8008-APP and is not published here.
- The publication is reached from SCR-43 Roles and access, with the delegation-of-authority panel and the masking panel, through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON); this story renders no screen of its own. The composite route specification belongs to RWB-PLT-N001-CON.
- This story starts no workflow, signals no workflow, registers no activity and owns no Schedule: the publication is synchronous and the maker-checker separation is a pair of letters, not a state.

The three tables are not symmetric, and the asymmetry is carried rather than hidden: `masking_rule` carries `valid_from` (DF-REF-203) and `valid_to` (DF-REF-204) and `delegation_limit` carries `valid_from` (DF-REF-025) and `valid_to` (DF-REF-026), while `permission` carries the `matrix_version` label and no date column at all. The publication therefore writes the window on the rows of the version that carry one, and the matrix label of the same version is in force for the window the version takes; the date columns of the matrix label are Not specified in the source documents (GAP-0872; ASM-1583), and the contract of RWB-P4-E8012-CON fixes the shape the read answers for it.

### 2. Business rationale

The access panel is the control that decides what every role may see and do, and it is also the control that goes stale first: a permission letter, a default scope, a masking row or an approval limit changes because Risk or Compliance changed its mind, not because a release is due. The legacy story carried the change as one administration journey inside the monolith (FEAT-ADM-07, RWB-E8-012), where the panel, its approval and the decision log were rows of one schema, the change was a screen in the same module and the only way to date it was to release. The FSD target measure for the whole administration group is blunt: rule and limit changes made without a code release, 100 percent, measured monthly from the decision record (FSD P4 v3 A2.23.1).

The target makes that possible only if a change of the panel is a versioned, dated, recorded act of data. REQ-DRI-011 asks that a reference data service hold every versioned table with its valid from and valid to dates, author and approver, and REQ-ACA-003 that the role to permission matrix be held as data and be the only source of what a role may see and do. Both are Must. A version label with a window is what turns those two requirements from a table into a control: the matrix of a date can be named, the masking of a date can be named, the limits of a date can be named, and the three labels of one publication name the panel that decided on that date.

The one rule that makes a publication safe is the separation of preparing from publishing, and it is achieved with the letters rather than with a new state. TSD P4 v3 T6.1 gives RW-COE `CRUD` in Rules and parameters and RW-RISK `RA`: the analyst prepares and loads a version with C and U, the officer publishes it with A, and no one can do both with one role. Nothing in this story needs a named-person four-eyes message, because the separation is already in the matrix and a caller without A is simply refused.

The effective date is why the story exists at all. A change that takes effect on a date needs no release and no window of downtime, and it needs no scheduler either: because `POST /authorise` resolves the version in force from the rows' own dates, the clock that makes the change happen is the calendar, not a job. That is what lets the publication be a single recorded act — the dates are written once, the record says who published what from when, and every reader afterwards sees the same answer without any process having to run.

This story meets REQ-DRI-011, REQ-ACA-003 and REQ-ACA-013, and it carries FEAT-ADM-07. It is the publication side of the panel whose load and approval belong to the administration stories of the same service, and it is the writer of the dates that the authorise operation of RWB-P4-E1037-APP reads.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8012-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two operations, the `ConfigVersion` and `ConfigVersionPage` schemas, the state set, the `rwb.access.AccessPolicyChanged.v1` declaration and the contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of a publication, hash-linked, written in the transaction that writes the dates |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the effective-date bounds and the page bounds, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-43 Roles and access with its panels and calls the two operations, one hop each |
| The panel rows themselves | The three tables and their migrations belong to the administration stories of this service: `permission` to RWB-P4-E1037-APP, `masking_rule` to RWB-P4-AD004-APP and `delegation_limit` to RWB-P4-E1038-APP. This story adds no table and no column |

Business preconditions carried from RWB-E8-012, from the feature specification and from the technical specification:

- The rights in force are those of TSD P4 v3 T6.1: RW-COE holds `CRUD` in Rules and parameters, RW-RISK holds `RA`, and the case roles hold `R` only or a dash. Publication authorises Rules and parameters A, and a caller without it is refused with 403 and MSG-P4-002 (BR3).
- The FSD P4 v3 A2.23.3.3 role table names the partner and agency manager as the primary user and the reference data administrator as the second. Neither letter set includes A in Rules and parameters, and the publishing role of the target is RW-RISK; the difference between the FSD role table and the letters of the T6.1 matrix is carried in ASM-1583 and changes no metadata value.
- A version is prepared and loaded by the administration stories with C and U, and it is `APPROVED` before this gate will publish it. The approval itself is not this story's: the state is read from the entry the preparing story recorded, and a version that is not `APPROVED` is refused with 409 and MSG-GEN-004 (BR4).
- The state of a version is `LOADED`, `VALIDATED`, `APPROVED`, `IN_FORCE`, `SUPERSEDED`, `ROLLED_BACK` or `REFUSED` of LOV-VERSION-STATUS (TSD P4 v3 T3.2). The two derived states come from the rows' dates; the other five come from the record, because the tables carry no state column (section 1; GAP-0872).
- The effective-date bounds — the earliest date a publication may name and the latest — are Not specified in the source documents (GAP-0872; ASM-1583): they are parameter rows read through DP-06 with the version in force, their names are fixed by RWB-P4-E8012-CON, and this story holds no bound and no default.
- The panel the story publishes is the access panel only. The partner panel, the partner firm, the partner users and the fee schedule are S9's under the ownership map, and FEAT-PRM-02 is S9's feature and not a prerequisite of this story (GAP-0872; ASM-1583).

### 4. Flow

1. The risk and model risk officer opens SCR-43 Roles and access through the gateway-bff composite route (DP-19), on the panel that lists configuration versions. The route calls `GET /api/recovery/access/v1/admin/config-versions` and shows each version with its three labels, its state and its window.
2. The officer selects a version in state `APPROVED` and submits the publication. The route calls `POST /api/recovery/access/v1/admin/config-versions/{versionId}/publish` on `rwb-access` with the body `effectiveFrom`, `reason` and an optional `note`, and an `Idempotency-Key` header.
3. `ConfigVersionPublicationController` validates the request: `effectiveFrom` and `reason` are required, `effectiveFrom` is a date and `note` is optional. An empty field or a value of the wrong shape is refused with 422 and MSG-GEN-001 naming the field, and no row is read for a decision and nothing is written (BR11).
4. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer and writes nothing, appends nothing and publishes nothing (BR12, AC5).
5. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters A. A caller without the A letter is refused with 403 and MSG-P4-002, and nothing is read for a decision, nothing is written and no event is staged (BR3, AC3).
6. `ConfigVersionRepository` resolves the configuration version from its `versionId` and reads the three labels and the rows of each of them in this service's own schema, with their `valid_from` and `valid_to` and their standard record columns. A `versionId` that names no complete triple is refused with 422 and MSG-GEN-001 naming `versionId` (BR5).
7. `PublicationGate` reads the recorded state of the version from the local decision-record chain and refuses a version that is not `APPROVED` with 409 and MSG-GEN-004, the caller being asked to reload the version; nothing is written (BR4, AC4).
8. `ParameterReader` reads the effective-date bounds through DP-06 with the version in force, and `PublicationGate` refuses an `effectiveFrom` outside them with 422 and MSG-GEN-001 naming `effectiveFrom`; nothing is written and no event is staged (BR6, AC4).
9. In one local transaction `ConfigVersionPublisher` writes the window: the `masking_rule` rows and the `delegation_limit` rows of the version take `valid_from` = `effectiveFrom` and a null `valid_to`; the rows of the version in force take `valid_to` = the day before `effectiveFrom`; the `permission` rows of the version carry the matrix label and take no date, and the matrix label is in force for the window the version takes (BR1, BR2).
10. In the same transaction `DecisionRecordAppender` appends one entry to the chain of DP-03 with the record code of a configuration publication, the three labels, the `versionId`, the effective date, the reason, the note, the publishing role code, the id of the version superseded and the time, and stages the outbox row of the entry (BR7, BR8).
11. In the same transaction `AccessPolicyEventPublisher` stages `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` with the payload of section 12.3, keyed by `versionId`, so the authorise caches of every consumer refresh after the commit (BR9, AC5).
12. The answer is the version with its `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state` `IN_FORCE` from `effectiveFrom`, `validFrom`, `validTo` null, `publishedAt`, `publishedByRole` and the `supersedesVersionId` it supersedes (BR10).
13. `GET /api/recovery/access/v1/admin/config-versions` answers the versions this service holds, newest window first, with a filter on `status` and the page default and maximum read through DP-06. Each item carries `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state`, `validFrom`, `validTo`, `publishedAt` and `publishedByRole`, and the page carries `page`, `size` and `total` (BR13).
14. The state an item carries is derived on the day of the read: `IN_FORCE` while `valid_from` ≤ today < `valid_to`, `SUPERSEDED` once `valid_to` has passed, and the recorded state of the version — `LOADED`, `VALIDATED`, `APPROVED`, `ROLLED_BACK` or `REFUSED` — while the window has not opened (BR14).
15. Where the dates, the entry, the outbox row or the idempotency row cannot be written, the answer is withheld with 503 and MSG-P7-003 and the transaction rolls back, so nothing changes and no event is published; the officer retries with the same `Idempotency-Key` and exactly one publication is completed (BR7, AC2).
16. Where a version is published with an effective date in the future, the version it supersedes keeps deciding until that date, because `POST /authorise` resolves the version in force from the dates and not from the act of publication (BR2).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `effectiveFrom` or `reason` is empty, or `effectiveFrom` is not a date | 422 naming the field; no row read for a decision, no write, no event | MSG-GEN-001 | AC4 |
| X2 | `versionId` names no complete triple of labels | 422 naming `versionId`; no write, no event | MSG-GEN-001 | AC4 |
| X3 | The caller holds no Rules and parameters A | 403, no write, no entry, no event | MSG-P4-002 | AC3 |
| X4 | The caller's session has ended | 401, no write, no entry and no event | MSG-P4-001 | AC3 |
| X5 | The version is not in state `APPROVED` | 409 and no write; the screen reloads the version | MSG-GEN-004 | AC4 |
| X6 | `effectiveFrom` is before the earliest bound or after the latest bound in force | 422 naming `effectiveFrom`; no write, no event | MSG-GEN-001 | AC4 |
| X7 | The same publication arrives twice with the same `Idempotency-Key` | The first answer is replayed; one entry, one event, no second write | None | AC5 |
| X8 | The dates, the entry, the outbox row or the idempotency row cannot be written | 503 and no answer; the transaction rolls back and nothing changes | MSG-P7-003 | AC2 |
| X9 | A break-glass grant is active for the caller | The publication proceeds and the answer carries the warning with the end time of the grant, and the entry carries the grant id | MSG-P4-004 | AC3 |
| X10 | A second publication of the same `versionId` arrives with a new key after the first | 409 and no write: the version is already in force or superseded, and its window cannot be moved twice | MSG-GEN-004 | AC5 |
| X11 | The version in force has no rows with a date window of its own | The publication still writes the labels it can and the entry, and the answer carries a null `validTo` on the version it supersedes only where a row carried one | MSG-GEN-001 | AC4 |

No exception path of this story changes a case, a task, a partner row or a rule package: the panel is this service's own three tables, and the only rows this story writes of its own are the dates of those rows, the entry of its own chain and the platform library rows of the request.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8012-CON and its fakes; the panel tables belong to the administration stories of the same service, the bounds come from the parameters contract and no partner row is touched |
| Negotiable | The effective-date bounds and the page bounds are parameter rows; the state names and the event payload are fixed by the contract and reviewed with Risk and with Compliance |
| Valuable | One recorded act puts a whole access-panel version in force on a date, closes the version it replaces on the day before, and refreshes every cache without a release and without a job |
| Estimable | Two controllers, one gate, one publisher, one repository, one record appender, one event publisher, one parameters reader, five fakes and five test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule and no screen of its own |
| Testable | Each owned criterion has a test case in section 16; the window is provable on a fixed clock, and the single publication is provable by counting entries and events |

### 7. Acceptance criteria

```gherkin
Feature: Publish a panel change

  Background:
    Given the environment is SIT
    Given the access panel is held by rwb-access as permission, masking_rule and delegation_limit rows with their version labels and date windows, and the partner panel is held by rwb-partner and is not touched here
    Given configuration version "CFG-2026.11" is in force from 30 November 2026 with matrixVersion "MAT-2026.11", maskingVersion "MSK-2026.11" and limitVersion "DOA-2026.11"
    Given configuration version "CFG-2027.01" is prepared with matrixVersion "MAT-2027.01", maskingVersion "MSK-2027.01" and limitVersion "DOA-2027.01" and is in state "APPROVED"
    Given test user "U-8101" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS"
    Given test user "U-8102" holds RW-RISK with "RA" in "RULES_AND_PARAMETERS"
    Given test user "U-8103" holds RW-CASEOWN with "R" only in "RULES_AND_PARAMETERS"
    Given test user "U-8104" holds RW-AUDIT with "R" in "RULES_AND_PARAMETERS"

  Scenario: AC2 Not recorded (legacy RWB-E8-012 AC2)
    Given the rwb-case contract mock returns the effective-date bounds and the page bounds at the version in force
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller with the case owner right only is refused (new, D-RCV-60)
    Given "U-8103" holds RW-CASEOWN with "R" only and holds no A letter in "RULES_AND_PARAMETERS"
    When "U-8103" calls POST /api/recovery/access/v1/admin/config-versions/CFG-2027.01/publish for effectiveFrom 2027-01-01 and reason "Annual panel refresh" with Idempotency-Key "k-012-3"
    Then the response is 403 with message MSG-P4-002 and no version is answered
    Then no row of permission, masking_rule or delegation_limit changes its valid_from or valid_to
    Then no decision-record entry is appended and no message is published on rwb.access.events.v1
    Then GET /api/recovery/access/v1/admin/config-versions still answers "CFG-2027.01" in state "APPROVED"

  Scenario: AC4 A version that is not approved, and a date outside the bounds, are refused (new, D-RCV-60)
    Given configuration version "CFG-2027.02" is in state "VALIDATED"
    Given the rwb-case contract mock returns an earliest effective date of 2026-12-01 and a latest of 2028-12-31 at the version in force
    When "U-8102" calls POST /api/recovery/access/v1/admin/config-versions/CFG-2027.02/publish for effectiveFrom 2027-01-01 with Idempotency-Key "k-012-4"
    Then the response is 409 with message MSG-GEN-004 and no version is answered
    When "U-8102" calls the same operation for "CFG-2027.01" with effectiveFrom 2026-11-01 with Idempotency-Key "k-012-5"
    Then the response is 422 with message MSG-GEN-001 naming effectiveFrom
    Then neither version changes a valid_from or a valid_to, no entry is appended and no message is published

  Scenario: AC5 A publication is dated, recorded once and announced once (new, D-RCV-60)
    Given "U-8102" publishes "CFG-2027.01" with effectiveFrom 2027-01-01 and reason "Annual panel refresh" under Idempotency-Key "k-012-1" on 15 December 2026
    Then the response is 201 with versionId "CFG-2027.01", state "IN_FORCE", validFrom 2027-01-01, validTo null, publishedByRole "RW-RISK" and supersedesVersionId "CFG-2026.11"
    Then exactly one decision-record entry is appended with both labels, the effective date, the reason, the publishing role code and the time
    Then exactly one message is published on rwb.access.events.v1 as rwb.access.AccessPolicyChanged.v1 with versionId, matrixVersion, maskingVersion, limitVersion, effectiveFrom 2027-01-01 and supersedesVersionId
    When "U-8104" calls GET /api/recovery/access/v1/admin/config-versions on 2 January 2027
    Then the answer carries "CFG-2027.01" in state "IN_FORCE" with validFrom 2027-01-01 and validTo null
    Then the answer carries "CFG-2026.11" in state "SUPERSEDED" with validTo 2026-12-31
    When "U-8102" sends the same publication again with Idempotency-Key "k-012-1"
    Then the first answer is replayed with versionId "CFG-2027.01" and state "IN_FORCE"
    Then exactly one entry exists for "CFG-2027.01" and exactly one AccessPolicyChanged message was published for it

  Scenario: AC6 The rules without a criterion are asserted in the list, the validation, the record and the module (new, D-RCV-60)
    When "U-8104" calls GET /api/recovery/access/v1/admin/config-versions
    Then the answer names the versions ordered by window, filtered by status and paged
    Then an empty or malformed effectiveFrom is refused with the status Not specified in the source documents (NEWAC-RWB-P4-E8012-APP-AC6) and MSG-GEN-001 naming the field, and nothing is read for a decision or written
    Then the decision-record entry holds no name, no e-mail address and no personal field
    Then no configuration-version table is read or written and no partner fake is called

  Scenario: AC7 An unauthenticated call is answered 401 and an unknown version is answered 404 (new, D-RCV-60)
    When an unauthenticated caller calls GET /api/recovery/access/v1/admin/config-versions
    Then the response is 401 and no version is answered
    When "U-8102" calls POST /api/recovery/access/v1/admin/config-versions/{versionId}/publish for a version identifier the service does not hold
    Then the response is 404 and no version is answered

  Scenario: AC8 A consumed call that fails or does not answer refuses the publication (new, D-RCV-60)
    Given the rwb-case contract mock does not answer the effective-date bounds at the version in force
    When "U-8102" calls POST /api/recovery/access/v1/admin/config-versions/CFG-2027.01/publish for effectiveFrom 2027-01-01 with Idempotency-Key "k-012-7"
    Then the response is Not specified in the source documents (NEWAC-RWB-P4-E8012-APP-AC8) and no version is answered
    Then no date changes, no entry is appended and no message is published
```

AC2 is the one criterion of RWB-E8-012 this story owns, copied with its text unchanged and its values kept; it carries one added line at the top of its scenario, the parameters mock, so the bounds are provable while the parameters contract is still a fake. AC1 of RWB-E8-012 — publish a panel change, put the change in force with an effective date and write the result to the decision log with the rule version — is owned by the integration story RWB-ITG-E8012-ITG and is not restated here. AC3 to AC5 are new under D-RCV-60 and test only what this story adds: the right, the two refusals and the dated single act.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A publication puts a configuration version in force from an effective date: the rows of the version take `valid_from` = that date, the rows of the version in force take `valid_to` = the day before, and the two windows never overlap | RWB-E8-012 AC1; FSD P4 v3 A2.23; REQ-DRI-011 |
| BR2 | Exactly one configuration version is in force on any date, and it is resolved from the rows' dates and not from the act of publication | FSD P4 v3 A2.23.1; TSD P4 v3 T3.1; ASM-1584 |
| BR3 | A publication needs Reference data C, read under the R-PREC order; a caller without it is refused with 403 and MSG-P4-002 and nothing is read for a decision, written or published | TSD P4 v3 T6.1; GAP-2283; legacy RWB-E8-012 permission checks |
| BR4 | Only a version in state `APPROVED` is published; any other state is refused with 409 and MSG-GEN-004 and nothing is written | FSD P4 v3 A2.23.4.3; TSD P4 v3 T3.2; ASM-1583 |
| BR5 | A configuration version is the triple of `matrix_version`, `masking_version` and `limit_version` over rows this service owns; no table, column or copy is created for it | TSD P4 v3 T3.1 DF-REF-044, DF-REF-202, DF-REF-055; ownership map; GAP-0872 |
| BR6 | `effectiveFrom` is checked against the earliest and the latest date the parameters contract answers, and a date outside them is refused with 422 and MSG-GEN-001; no bound is a constant in code | DP-06; FSD P4 v3 A2.23.3.1 VR-P4-023-1; GAP-0872 |
| BR7 | Every publication appends exactly one entry to the local decision-record chain of DP-03 in the transaction that writes the dates; an act that cannot be recorded is not taken and is withheld with 503 and MSG-P7-003 | R-UNI-39; RWB-E8-012 AC2; DP-03 |
| BR8 | The entry carries the three labels, the `versionId`, the effective date, the reason, the note, the publishing role code and the time, and no name, no e-mail address and no personal field | NFR-040; Principle 5; ASM-1585 |
| BR9 | The publication publishes exactly one `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1`, keyed by `versionId`, so the authorise caches refresh; the payload carries no person and no personal data | Architecture v5 slide 14, slide 41 and slide 43; ASM-1585 |
| BR10 | The answer names the version, its three labels, the state it takes from `effectiveFrom`, its window, the time and role of the publication and the version it supersedes | TSD P4 v3 T3.2; section 12.1 |
| BR11 | Every field is validated before any row is read for a decision: an empty or malformed value is 422 with MSG-GEN-001 naming the field, and nothing is written | FSD P4 v3 A2.23.3.1 VR-P4-023-1 |
| BR12 | One `Idempotency-Key` answers one publication: a replay answers the first answer, writes no second window, appends no second entry and publishes no second event | Architecture v5 slide 42; DP-09 |
| BR13 | The list read answers the versions this service holds with the state each is in on the day of the read, ordered by window, filtered by `status` and paged from the parameters contract | FSD P4 v3 A2.23.2; TSD P4 v3 T3.2 |
| BR14 | The state of a version is `IN_FORCE` inside its window and `SUPERSEDED` after it, both derived from the rows' dates; the five states that are not derived are read from the record because the tables carry no state column | TSD P4 v3 T3.2; GAP-0872; ASM-1583 |
| BR15 | The partner panel, the partner firm, the partner users, the fee schedule and the partner service levels are S9's and are neither read nor written; FEAT-PRM-02 is not a prerequisite of this story | Ownership map (`partner`, `partner_user`, `partner_instruction` = S9); Architecture v5 slide 41; GAP-0872 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 and BR2 are one update statement per table inside one transaction: `valid_from` on the rows of the version and `valid_to` on the rows of the version it replaces, so no reader ever sees two windows open on the same date or none.
- BR3 is one call to the own authorise operation with C on Reference data, made before the version is read for a decision; the refusal returns before the repository is reached, which is why AC3 can assert that no row changed.
- BR4 is the recorded state read from the chain, not a column read: the gate compares the version's last recorded state with `APPROVED` and refuses anything else, including a version that was rolled back.
- BR5 is the absence of a table: the module has no configuration-version table, no view and no join for one, and the version is the label triple the contract names.
- BR6 is the parameters reader at request time with the version in force; a changed bound is data and needs no build.
- BR7, BR8 and BR9 are one transaction: the two date updates, the entry, the outbox row and the idempotency row commit together, and the relay sends the event after the commit.
- BR10 is the answer shape of the contract: the version item plus the id of the version superseded, and no field of another service.
- BR11 is the validation of the controller before any read, so a malformed request cannot even be counted as an attempt on a version.
- BR12 is the `idempotency_key` row of the platform library in `rwb_access`, written with the answer.
- BR13 and BR14 are the read: a projection over the three tables and the chain, with the derived state computed for the day of the read and the paging from DP-06.
- BR15 is a negative rule: the module has no repository, no client and no join for `partner`, `partner_user` or `partner_instruction`, and the tests assert that no partner fake is called.

### 9. State transitions

This story holds no state of its own. The state it reads and moves is the state of a configuration version, and the two states it writes are written as dates on the rows.

| From | Event | Condition | To |
|---|---|---|---|
| `APPROVED` | A publication is submitted | A held, the version is `APPROVED`, the date is inside the bounds | `IN_FORCE` from `effectiveFrom`; the version in force `SUPERSEDED` from the day before |
| `APPROVED` | A publication is submitted | No A letter | Refused 403 with MSG-P4-002; no write, no entry, no event |
| `APPROVED` | A publication is submitted | The date is outside the bounds | Refused 422 with MSG-GEN-001; no write, no entry, no event |
| `APPROVED` | A publication is submitted | The entry or a date cannot be written | Refused 503 with MSG-P7-003; nothing changed |
| `LOADED`, `VALIDATED`, `ROLLED_BACK`, `REFUSED` | A publication is submitted | The recorded state is not `APPROVED` | Refused 409 with MSG-GEN-004; no write |
| `IN_FORCE` | A publication of the same version with a new key | The window is already open | Refused 409 with MSG-GEN-004; the window is never moved twice |
| `IN_FORCE` | The same `Idempotency-Key` is sent again | None | The first answer is replayed; no second write, entry or event |
| `IN_FORCE` | The window closes | `valid_to` has passed | `SUPERSEDED`, derived from the dates and written by no process |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | A publication, or a refusal that is recorded at the service edge | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| `rwb.access.events.v1` | A publication | Exactly one `rwb.access.AccessPolicyChanged.v1`, from the outbox of the publishing transaction |
| `rwb.decision-record.v1` | A publication | Exactly one `DecisionRecorded` for the entry, from the same outbox |

The two shapes of the state must not be confused, and the contract says so once: the answer of the publication names the state the version takes on its effective date, `IN_FORCE`, while the list read derives the state of each version from its window and the day of the read, so the same version is `APPROVED` in the list on the day before its date, `IN_FORCE` inside its window and `SUPERSEDED` after it. No process moves a version from one state to the other: the calendar does, which is why no Schedule and no Temporal job is added for it (ASM-1584).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Risk and model risk officer (RW-RISK) | Publish a configuration version with Rules and parameters A; the publisher of the target, and the role code recorded on the entry (TSD P4 v3 T6.1) |
| Center of excellence analyst (RW-COE) | Prepares and loads a version with `CRUD` in Rules and parameters and cannot publish it, because `CRUD` carries no A; the maker half of the separation |
| Security administrator (RW-SECADM) | Holds `CRUDA` in Platform administration and `R` in Rules and parameters; this story gives no write path to that right, and the role administration is RWB-P4-E1037-APP's |
| Reference data administrator (RW-REFADM) | Prepares a load with `CRUD` in Reference data as the FSD A2.23.3.3 role table states; holds `R` in Rules and parameters and cannot publish |
| Internal audit (RW-AUDIT) | Reads the list with Rules and parameters R and reads the entries; publishes nothing |
| A case role without Rules and parameters A (RW-CASEOWN, RW-PHONECOL) | Refused with 403 and MSG-P4-002; nothing is read for a decision, written or published |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` unchanged |
| `rwb-access` itself | Reads and writes `permission`, `masking_rule` and `delegation_limit` in its own schema, reads `role` and `permission`, and writes only its own chain and outbox |
| `rwb-partner` (S9) | Owns the partner panel, the partner firm, the partner users, the fee schedule and the partner service levels; this story calls it not at all |
| `rwb-decision` (P7) | Owns the central ledger and the rule package registry; this story calls it not at all |

The maker-checker separation is achieved through the letters and needs no named-person four-eyes message: RW-COE prepares with C and U, RW-RISK publishes with A, and no single role holds both in Rules and parameters. A caller without A is refused with 403 and MSG-P4-002, which is the same refusal the legacy story carried for an action outside the role's permission. The other refusal shapes are 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a version that is not `APPROVED` or is already in force, 422 with MSG-GEN-001 for a field or a date, and 503 with MSG-P7-003 for a record that cannot be written. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the rows of the version and the matrix label. Write: none — the table carries no date column, and the matrix label is in force for the window the version takes |
| DF-REF-198 to DF-REF-204 | `masking_rule` | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read: the rows of the version and of the version in force. Write: `valid_from` on the rows of the version, `valid_to` on the rows of the version it supersedes |
| DF-REF-016 to DF-REF-026, DF-REF-055 to DF-REF-062 | `delegation_limit` | id, decision_code, approval_level, product_group, the four amounts, valid_from, valid_to, limit_version and the other conditions | Read: the rows of the version and of the version in force. Write: `valid_from` on the rows of the version, `valid_to` on the rows of the version it supersedes. No amount, level or product group is changed |
| DF-REF-034 to DF-REF-038 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the caller's role and its class, and the role code recorded as the publisher |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the publication entry: `decision_code` DF-DEC-003, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the three labels, the `versionId`, the effective date, the reason, the note, the publishing role code, the version superseded and the grant id, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the state of a version and for the list |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of a publication | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` | the `AccessPolicyChanged` row and the record row of the publication entry | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-PRT-001 to DF-PRT-007 | `partner` of `rwb_partner` | none | Not read and not written: the partner panel is S9's |
| DF-REF-212 to DF-REF-217 | `partner_user` of `rwb_partner` | none | Not read and not written: the partner users are S9's |

No row of `partner`, `partner_user` or `partner_instruction` is read or written: they are `rwb-partner`'s (S9) under the ownership map, the legacy story's `partner` rows travel with the partner capability and not with the access panel, and no foreign key crosses a schema (DP-01, BR15). No row of `decision_log_entry` is read or written either: the central ledger is P7's and this story writes only its own local chain on `rwb.decision-record.v1`. No row of `rule_row`, `rule_package_version` or `lov_value` is read: the rule registry is P7's, the list values are P3 reference data, and the version labels are read from the rows themselves. Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P4 v3 T3.1.

The configuration version and its `versionId`, the exact field set of the two operations, the scheme that builds `versionId` from the three labels, and the date columns of the matrix label are Not specified in the source documents (GAP-0872; ASM-1583): no source defines a configuration-version object, the two paths appear in no endpoint inventory, and `permission` carries no date column. The schema of RWB-P4-E8012-CON fixes them and this story reads and writes them as that contract publishes them.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/config-versions/{versionId}/publish` | P4 `rwb-access` | Path: `versionId`. Body: `effectiveFrom` (a date), `reason`, `note` (optional) | `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state` `IN_FORCE` from `effectiveFrom`, `validFrom`, `validTo`, `publishedAt`, `publishedByRole`, `supersedesVersionId` | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters A, scope applied | `Idempotency-Key` required; a replay answers the first answer and publishes no second event |
| GET | `/api/recovery/access/v1/admin/config-versions` | P4 `rwb-access` | Query: `status`, `page`, `size` | `items[]` of `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `state`, `validFrom`, `validTo`, `publishedAt`, `publishedByRole`, plus `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters R, scope applied | Not applicable, read only |

Both operations sit on the base `/api/recovery/access/v1` of DP-13. The publication answer names the state the version takes from its effective date, and the list derives the state of each version from its window and the day of the read (section 9). `status` filters on the state set of BR14, `page` defaults to the value of its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR6, BR13). Neither operation appears in the endpoint inventory of TSD P4 v3 appendix T-A, which declares no configuration-version operation at all, so both paths are fixed by RWB-P4-E8012-CON and raised in the key's gap (GAP-0872; ASM-1583).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Rules and parameters A check behind the publication and the R check behind the list, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The earliest and the latest effective date and the page bounds, with the version in force (DP-06) |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the parameters read and the authorise answer are cached for the request or the session. The own authorise operation is the one Architecture v5 slide 14 names as the first path of `rwb-access`, and this story declares it as consumed and never defines it. No other operation of `rwb-case`, `rwb-decision`, `rwb-partner` or `rwb-document` is called.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | `versionId` | `versionId`, `matrixVersion`, `maskingVersion`, `limitVersion`, `effectiveFrom`, `supersedesVersionId`, `publishedByRole`, `reason` |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of a publication: the three labels, the effective date, the reason, the note, the publishing role code and the time |

CloudEvents 1.0 envelope, from the outbox of the transaction that writes the dates. `AccessPolicyChanged` is one of the two events of `rwb-access` in Architecture v5 slide 14 and slide 41, and slide 43 gives it every service as a consumer with the note "cache refresh". Its payload carries labels, a date, a role code and a reason and no name, no e-mail address, no user reference and no personal field (BR9). `rwb.access.DoaLimitChanged.v1` belongs to RWB-P4-E8008-APP and is not published here, even though a limit label travels in the payload.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, and a publication of its own tables needs no subscription. No `processed_event` row is written and the contract declares no consumer group.

#### 12.5 Workflows and activities

None. The publication is synchronous and the maker-checker separation is a pair of letters, not a state: this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. `ApprovalWorkflow` of the workflow kit belongs to `rwb-decision` (P7) and is not used for an administration change of this service.

#### 12.6 Schedules

None, and the absence is deliberate. The effective date of a version is resolved at read time by `POST /authorise` as the version whose `valid_from` ≤ today < `valid_to`, so no promotion job has to run at 00:01 and no Temporal Schedule or workflow is added for it (ASM-1584). The six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP. The rule-promotion Schedule of `rwb-decision` is P7's and promotes rule packages, not an access panel.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `permission` | P4 (`rwb_access`) | Read only: the rows of the version, the matrix label and the letters of the caller. Created by RWB-P4-E1037-APP |
| `masking_rule` | P4 (`rwb_access`) | Read and write: `valid_from` on the rows of the version, `valid_to` on the rows it supersedes. Created by RWB-P4-AD004-APP |
| `delegation_limit` | P4 (`rwb_access`) | Read and write: `valid_from` on the rows of the version, `valid_to` on the rows it supersedes; no amount is changed. Created by RWB-P4-E1038-APP |
| `role` | P4 (`rwb_access`) | Read only: the role code recorded as the publisher |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of a publication. Read: the recorded state of a version and the list |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The two outbox rows of a publication and its idempotency row; no inbox row, because no event is consumed (DP-09; ASM-0074) |
| `partner`, `partner_user`, `partner_instruction` | S9 (`rwb_partner`) | Not read and not written: the partner panel is S9's (BR15) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's and the local record goes on `rwb.decision-record.v1` |
| `rule_package_version`, `rule_row` | P7 (`rwb_decision`) | Not read and not written: the rule registry is P7's and the "rule version" of the legacy criterion is read here as the version of the panel (section 11) |
| `lov_value`, `reference_version`, `reference_row` | P3 (`rwb_case`) | Not read: reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON` |

No table is created by this story: the configuration version is a label over three tables that already exist, and a configuration-version table would be a second writer of a window that the rows themselves carry (BR5). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| authorise fake | RWB-P4-E8012-CON, RWB-P4-E1037-CON | A granted answer for RW-RISK with A in Rules and parameters, for RW-COE with C, U and R in Reference data, and for RW-AUDIT with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-CASEOWN with R only in Reference data |
| parameters fake | RWB-P3-E1042-CON (serves rwb-case) | The earliest and the latest effective date and the page bounds at the version in force, including a window that makes 2026-11-01 out of bounds and 2027-01-01 inside them |
| decision-record fake | RWB-PLT-E1027-CON | The append of a publication, the hash-link check, the recorded state of "CFG-2026.11", "CFG-2027.01" and "CFG-2027.02", the seeded entries of the two earlier versions, and the forced failure AC2 needs |
| access-panel fixture | RWB-P4-E8012-CON, seeded by RWB-P4-E1037-APP, RWB-P4-AD004-APP and RWB-P4-E1038-APP | The three tables with the rows of "CFG-2026.11" in force from 30 November 2026 and the rows of "CFG-2027.01" without a window, so a publication has both a version to put in force and a version to supersede |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-43 with the version list panel, the publication form and the states of section 15 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (the publication and the list); consumed 2 | Base `/api/recovery/access/v1`; the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 2 event types; consumed 0 | `rwb.access.events.v1` for `AccessPolicyChanged`, and `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only; no promotion job is added |
| File | None | No file input and no file output; the load of a version's rows is the administration stories' |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/configversion`, Java package `th.co.scb.ace.workbench.recovery.access.configversion`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module rule-version load and approve of the monolith, addressed on the monolith's own base (DP-13: the service's own base and its own tables), and the ace-web screens that published in process (DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. The reference-data list check of the version labels would need DP-07 and `RWB-P3-E1043-CON`, neither of which this story's metadata carries, so the labels are read from the rows and the point is raised in the key's gap (GAP-0872; ASM-1583).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ConfigVersionPublicationController | Controller | `POST /admin/config-versions/{versionId}/publish`: validation, the `Idempotency-Key` lookup, the RFC 9457 problem responses |
| ConfigVersionQueryController | Controller | `GET /admin/config-versions`: the `status` filter, the paging from DP-06 and the state of each version on the day of the read |
| PublicationGate | Service | The ordered gate of BR3, BR4 and BR6: right, recorded state, bounds; a refusal returns before the next step |
| ConfigVersionPublisher | Service | BR1 and BR2: the two date updates in one transaction, the version superseded, the answer of BR10 |
| ConfigVersionRepository | Repository | The triple and its rows in `permission`, `masking_rule` and `delegation_limit`, the version in force for a date, the two updates; no delete method and no write to `permission` |
| ConfigVersionStateService | Service | BR14: the derived state of a version and the recorded state read from the chain, and the list projection |
| PermissionReader | Service | The `role` and `permission` rows of the caller, the A and R letters and the role code that carries A |
| ParameterReader | Service | The effective-date bounds and the page bounds through the parameters contract of DP-06, with the version in force |
| AccessPolicyEventPublisher | Service | The `rwb.access.AccessPolicyChanged.v1` row in the outbox of the publishing transaction, with the payload of section 12.3 |
| DecisionRecordAppender | Service | The publication entry with its outbox row, in the transaction that writes the dates (DP-03, DP-09) |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations**

- This story creates no table and adds no column. `permission`, `masking_rule` and `delegation_limit` are created by RWB-P4-E1037-APP, RWB-P4-AD004-APP and RWB-P4-E1038-APP in the per-service Flyway sequence of DP-15, the local decision-record table by RWB-P4-E1039-APP and the platform library tables by the service's own DB story; this story reads and writes rows of them.
- The two date updates are guarded so that two windows cannot overlap: the update of the version in force is conditional on its rows having no `valid_to` after the new `valid_from`, and the update of the new version is conditional on its rows having no window of their own. If SIT needs an index for the version-in-force window, it is added to the owning story's migration with the agreement of its owner.
- No write statement touches an amount, a level, a product group, a letter or a role: the publisher writes two dates per row, which is what makes a publication unable to change a business value by accident.
- The two date updates, the entry, the two outbox rows and the idempotency row commit in one transaction; a failure rolls all of them back and the answer is withheld with MSG-P7-003 (BR7).

**Configuration and reference data**

- The earliest and the latest effective date and the page default and maximum are parameter rows of `rwb-case` read through DP-06 with the version in force; no bound is a constant in code (BR6). Their names are fixed by RWB-P4-E8012-CON.
- The version labels are values of the rows the administration stories loaded; this story copies and compares them and validates nothing against a list of its own (section 12.7).
- The publishing role code is read from `role` through the `permission` row that carries the A letter; no role code and no capability area is a constant in code (BR3, BR8).
- The state names are those of LOV-VERSION-STATUS of TSD P4 v3 T3.2 and are the contract's enumeration, not a local list.

**Build steps**

1. `ConfigVersionRepository` and the triple resolution; test that a `versionId` with an incomplete triple is refused with 422 and that the repository has no delete and no write to `permission`.
2. `ConfigVersionPublicationController` and its validation; tests for X1 and X2 with no read for a decision and no write.
3. `PermissionReader` and the authorise call; test the AC3 refusal of a caller with R only, with no date changed, no entry and no event, and the list still answering `APPROVED`.
4. `ConfigVersionStateService` over the chain and the fixture; test that "CFG-2026.11" is `IN_FORCE`, "CFG-2027.02" is `VALIDATED` and an old version is `SUPERSEDED`, all from the same read.
5. `PublicationGate` with the state and the bounds; test AC4, including the proof that neither refusal writes a date and that the parameters fake is the only source of the bounds.
6. `ConfigVersionPublisher` with the two guarded updates; test the window of AC5 on a fixed clock, including the day before, the effective day and the day after.
7. `DecisionRecordAppender`, `AccessPolicyEventPublisher` and `IdempotencyStore` in one transaction; test the replay of AC5 with one entry and one event, and the forced failure of AC2 with nothing changed.
8. `ParameterReader` over the parameters fake, so the story builds before `rwb-case` is in the environment; test that a changed bound is data and needs no build.
9. The contract-fake run of both operations through the gateway-bff fake, so SCR-43 can be demonstrated while the route and the panel stories are being built.

**Feature switch.** The two operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of their own. A publication that is switched off would leave an approved version undated and visible as such in the list, which is the state the gate is meant to resolve, so this story adds no flag and removes nothing.

**Done when.** The tests in section 16 pass; "CFG-2027.01" is published for 2027-01-01 by RW-RISK and answered with its labels, its window and the version it supersedes; the rows of "CFG-2026.11" carry `valid_to` 2026-12-31 and the list answers it `SUPERSEDED` on 2 January 2027; a caller with R only is refused with MSG-P4-002 with no row changed; a version in `VALIDATED` is refused with MSG-GEN-004 and a date outside the bounds with MSG-GEN-001, neither writing anything; one entry is appended and one `AccessPolicyChanged` is published per publication; the same `Idempotency-Key` replays one answer; and a forced failure of the record leaves every date as it was with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Rules and parameters A on the publication, or no R on the list | You cannot {action} here. Your role does not include it. | This story, on both operations |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the publication answer, with the grant id recorded in the entry |
| MSG-GEN-001 | A required field is empty, `effectiveFrom` is not a date, `versionId` names no complete triple, or `effectiveFrom` is outside the bounds in force | Enter {field}. | This story, on both operations |
| MSG-GEN-004 | The version is not in state `APPROVED`, or it is already in force and its window cannot be moved again | Someone else changed this record. Reload it to see their change. | This story, on the publication |
| MSG-P7-003 | The dates, the entry, the outbox row or the idempotency row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-001, MSG-P4-002, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the legacy texts, and MSG-GEN-004 is the platform text of the record that someone else changed, carried unchanged and added here as a platform value and not as a new business text. No named-person four-eyes message is produced, because the separation of the preparer and the publisher is held by the C and A letters of TSD P4 v3 T6.1 and not by a comparison of two people on one act.

### 15. Screens and states

The publication is reached from SCR-43 Roles and access through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), on the panel that lists configuration versions and the form that publishes one. The delegation-of-authority panel of the screen shows the limit label of a version, and the masking panel shows its masking label, both read through the operations of the stories that own those panels; this story renders no screen surface of its own.

| Screen | State | What it shows |
|---|---|---|
| SCR-43 Roles and access | Versions, list | The configuration versions with their three labels, their state and their window, paged, filtered by `status` |
| SCR-43 Roles and access | Versions, in force | The version whose window contains today, marked `IN_FORCE`, and the versions before it marked `SUPERSEDED` with their `valid_to` |
| SCR-43 Roles and access | Publication, form | One `APPROVED` version opened for publication with `effectiveFrom`, `reason` and `note`; the bounds come from the parameters read |
| SCR-43 Roles and access | Publication, recorded | The 201 answer with the three labels, state `IN_FORCE`, `validFrom`, `publishedAt`, `publishedByRole` and the version superseded |
| SCR-43 Roles and access | Publication, not approved | The 409 of X5 with MSG-GEN-004 and a reload action |
| SCR-43 Roles and access | Publication, date outside the bounds | The 422 of X6 with MSG-GEN-001 naming `effectiveFrom`, and the bounds shown beside the field |
| SCR-43 Roles and access | Publication, refused | The 403 of X3 with MSG-P4-002 for a role without the A letter |
| SCR-43 Roles and access | Publication, not recorded | The 503 of X8 with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (CG-ALL-5543) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-5543) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (CG-ALL-5543) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (CG-ALL-5543) |
| SCR-41 Delegation of authority | Empty | Not specified in the source documents (CG-ALL-5544) |
| SCR-41 Delegation of authority | Loading | Not specified in the source documents (CG-ALL-5544) |
| SCR-41 Delegation of authority | Error | Not specified in the source documents (CG-ALL-5544) |
| SCR-41 Delegation of authority | No access | Not specified in the source documents (CG-ALL-5544) |
| SCR-43 Roles and access | Empty | Not specified in the source documents (CG-ALL-5545) |
| SCR-43 Roles and access | Loading | Not specified in the source documents (CG-ALL-5545) |
| SCR-43 Roles and access | Error | Not specified in the source documents (CG-ALL-5545) |
| SCR-43 Roles and access | No access | Not specified in the source documents (CG-ALL-5545) |

The legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority in its screen table, and neither name fits the access panel of the target: the panel a publication puts in force is the role, permission, scope, masking and limit panel, which the target screen SCR-43 Roles and access carries with the delegation-of-authority and masking panels. The composite route specification, the panel field lists and the screen states belong to RWB-PLT-N001-CON and to the screen work of the administration stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-012-02 | AC2, BR7 | Component | The decision-record store forced to fail during the publication of "CFG-2027.01": 503 with MSG-P7-003, no date changed, no entry and no event; a retry with the same `Idempotency-Key` completes exactly one publication |
| TC-E8-012-03 | AC3, BR3 | Component | A caller holding RW-CASEOWN with Reference data R only: 403 with MSG-P4-002, no date changed on any of the three tables, no entry, no event, and the list still answering "CFG-2027.01" `APPROVED` |
| TC-E8-012-04 | AC2, BR7 | NFR | The date updates and the outbox rows forced to fail under load: every failure is a 503 with MSG-P7-003, no partial window is ever readable, and the retry path yields one publication |
| TC-E8-012-05 | AC4, BR4, BR6 | Component | "CFG-2027.02" in `VALIDATED` refused 409 with MSG-GEN-004; "CFG-2027.01" with `effectiveFrom` 2026-11-01 against a mock bound of 2026-12-01 refused 422 with MSG-GEN-001; no date, entry or event for either |
| TC-E8-012-06 | AC5, BR1, BR2, BR9, BR12, BR14 | Component | The publication on 15 December 2026 for 2027-01-01: the list on 2 January 2027 answers "CFG-2027.01" `IN_FORCE` and "CFG-2026.11" `SUPERSEDED` with `validTo` 2026-12-31; one entry and one `AccessPolicyChanged`; the replay of "k-012-1" with one entry and one event |
| TC-E8-012-07 | §12 operations and events; BR9, BR10 | Contract | The two operations of §12 and the `AccessPolicyChanged.v1` payload as RWB-P4-E8012-CON publishes them: the answer names the version, its three labels, state, window, time, role and superseded version; the payload carries no person and no personal data |
| TC-E8-012-08 | BR5, BR15 | Component | The module has no configuration-version table and no repository, client or join for `partner`, `partner_user` or `partner_instruction`: no partner fake is called and no table of the version is read or written |
| TC-E8-012-09 | BR8, BR10 | Component | A publication: the entry holds the three labels, `versionId`, effective date, reason, note, publishing role code and time, with no name, e-mail address or personal field; the answer names the version, its three labels, state, window, time, role and superseded version |
| TC-E8-012-10 | BR11, BR13 | Component | An empty or malformed `effectiveFrom` is refused with the status Not specified in the source documents (NEWAC-RWB-P4-E8012-APP-AC6) and MSG-GEN-001 naming the field and nothing is written; the list answers the versions ordered by window, filtered by `status` and paged |
| TC-E8-012-11 | §12.7 tables; ASM-3438; BR1, BR2 | Component | The rows at the window edges of `permission`, `masking_rule` and `delegation_limit`: `valid_from` on the first day of the new window and `valid_to` the day before on the superseded rows, with no overlap and no gap on the date of the change |
| TC-E8-012-12 | AC6, BR5, BR8, BR10, BR11, BR13, BR15 | Component | Not specified in the source documents (NEWAC-RWB-P4-E8012-APP-AC6); the Scenario of AC6 in section 7 states the assertions |
| TC-E8-012-13 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-P4-E8012-APP-AC7); the Scenario of AC7 in section 7 states the assertions |
| TC-E8-012-14 | AC8, BR7 | Component | Not specified in the source documents (NEWAC-RWB-P4-E8012-APP-AC8); the Scenario of AC8 in section 7 states the assertions |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The legacy rows of this key that cover the criteria this story owns are kept: TC-E8-012-02 for AC2, TC-E8-012-03 for the access refusal and TC-E8-012-04 for the forced record failure; two rows are added for the new criteria. TC-E8-012-01 covers legacy AC1 and stays with RWB-ITG-E8012-ITG, so it is named here and not carried as a row of this story. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16. No `-ITG` copy of a test case is written here.

### 17. Guardrails

- No business value in code: the effective-date bounds and the page bounds are parameter rows (BR6), the publishing role is read from `role` and `permission` (BR8), and the state names are the contract's enumeration of LOV-VERSION-STATUS.
- No personal data anywhere: the request, the answer, the list and the entry carry version labels, a date, a role code, a reason and a time; no name, no e-mail address and no user reference appears in the answer, the entry, the event or a test (BR8, BR9, NFR-040).
- No read of another service's tables (DP-01): `partner`, `partner_user` and `partner_instruction` are S9's, `decision_log_entry` and the rule registry are P7's, and no join crosses a schema.
- One writer for the panel window: only this operation writes `valid_from` and `valid_to` of a configuration version, and it writes nothing else of a row; the rows themselves are loaded by the administration stories.
- No publication without its record: the two date updates, the entry and the outbox rows commit together, and the answer is withheld with MSG-P7-003 when the entry cannot be written (BR7, R-UNI-39).
- Maker and publisher are different letters: `CRUD` prepares and `A` publishes, so no single role can load a version and put it in force, and the refusal is the ordinary MSG-P4-002.
- No clock of its own: the effective date is resolved at read time from the rows' dates, so the story adds no Schedule, no workflow and no promotion job (ASM-1584).
- One key, one publication: the `Idempotency-Key` is stored with the answer, so a retry after a timeout cannot write a second window, a second entry or a second event (BR12).
- The partner panel is out of reach: the module has no repository and no client for it, and a test asserts that no partner fake is called (BR15).
- Every example, fixture and test payload is synthetic; no production panel row is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-011 | A reference data service holds every versioned table with its valid from and valid to dates, author and approver | Program, P7 Decision center and log | FEAT-ADM-07 | All recovery processes | BR1, BR2, BR5, BR14 | TC-E8-012-06 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do | Program, P4 Access and administration | FEAT-ADM-07 | All recovery processes | BR1, BR5, BR13 | TC-E8-012-05, TC-E8-012-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Program, P4 Access and administration | FEAT-ADM-07 | All recovery processes | BR3, BR11, BR12 | TC-E8-012-03, TC-E8-012-04 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key. The versioned reference-data requirement is the P7 one in the Program BRD and is served here by the panel version rather than by the rule registry, which is P7's.

| Legacy reference | Where it is kept |
|---|---|
| AC1 publish a panel change, the change put in force with an effective date and the result written to the decision log with the rule version | Owned by RWB-ITG-E8012-ITG and kept there; named in sections 7 and 16, and carried in this story as sections 4, 8 and 12.1 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7, 8, 12.1, 14 |
| The permission check: Reference data C for the publish; the A letter stays with the load and rule-version approvals (GAP-2283) | Sections 3, 7 (AC3), 8 (BR3), 10, 12.1 |
| MSG-P4-004, MSG-P4-002, MSG-P4-001, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The legacy data rows `partner` DF-PRT-001 to DF-PRT-007 | Moved with the partner capability to S9 `rwb-partner`; section 11 records that no row is read or written here |
| The legacy data rows `decision_log_entry` DF-DEC-001 to DF-DEC-018 and `rule_row` DF-REF-001 to DF-REF-015 | The local record of DP-03 in section 11 and the rule registry of P7; the "rule version" of AC1 is read here as the version of the panel |
| The legacy data rows `role` DF-REF-034 to DF-REF-038 and `permission` DF-REF-040 to DF-REF-044 | Sections 11, 12.7 |
| TC-E8-012-02 to TC-E8-012-04, and TC-E8-012-01 with the ITG story | Section 16 |
| Legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority as the story named them | Section 15, carried to SCR-43 Roles and access with its delegation and masking panels |
| The effective-dating of a version and the state set of LOV-VERSION-STATUS | Sections 1, 3, 8, 9, 12.6 |
| Legacy key RWB-E8-012, story RWB-P4-E8012-APP, contract RWB-P4-E8012-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The partner panel, the partner firm, the partner users, the fee schedule and the partner service levels: S9 `rwb-partner` under the ownership map, and FEAT-PRM-02 is that service's feature and not a prerequisite of this story.
- The preparation, load and approval of a configuration version: the version is loaded and approved by the administration stories that own the tables — RWB-P4-E1037-APP for the matrix, RWB-P4-AD004-APP for masking and RWB-P4-E1038-APP for the limits — and this story publishes a version they have approved.
- The rollback of a version in force and the change report of a version: the rollback of a rule or reference version is RWB-P4-AD013-APP's, and this story has no rollback path.
- The rule package version, its registry and its promotion at 00:01: P7 `rwb-decision` (ASM-0069, ASM-0040), and no rule package is loaded, approved or promoted here.
- Reference-data loads and the list of values: P3 `rwb-case` (ASM-0071), and this story's pattern list carries no DP-07.
- The central decision ledger, the query API over `rwb_decision` and the chain verification: P7 `rwb-decision`.
- The permission matrix, the role administration, the masking policy and the DoA table themselves: RWB-P4-E1037-APP, RWB-P4-AD004-APP and RWB-P4-E1038-APP, and the authorise operation that reads the version in force is RWB-P4-E1037-APP's.
- The screen SCR-43 Roles and access, its panels and its composite route specification: RWB-PLT-N001-CON and the screen work of the administration stories.
- The integration harness and the `-ITG` copies of the test cases: the journey of this key is RWB-ITG-E8012-ITG and it owns AC1.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
