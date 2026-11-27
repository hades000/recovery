# RWB-P4-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P4-Q |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1020-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CWC-007, REQ-CWC-008, REQ-CWC-009, REQ-CWC-016) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-020 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1020-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager, a capacity planner, a platform administrator or an auditor who works the morning allocation**, I want **the access service to answer, for the allocation run and for what it produced, who may run or rerun it, whose team summary I may read, and whose case I may look at after the run**, so that **the morning run and its summary reach the people entitled to them, the run itself is not stopped by a person's session, and nothing about a case is told to anybody else**.

Inside `rwb-access` this is the authority slice of legacy RWB-E1-020. The story is secondary (`secondary = true`): it carries no legacy acceptance criterion of its own, it preserves nothing word for word, and it describes only the access change of the key.

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- The capability answers three questions behind the three operations the service already publishes, `POST /authorise`, `GET /me/permissions` and `GET /masking-policies`: does the caller hold the Queue and allocation letter the action needs, does the scope in force admit this team or this case, and — for the run itself — does the service identity hold the letters the run writes with. No operation is added.
- Who the answers are about: a person may run or rerun the morning allocation run JOB-03 only with Platform administration right U; the run itself executes as the service identity SY-CASEWF, which carries Queue and allocation CRU; a person reads the allocation summary of a team with Queue and allocation right R and the default scope TEAM; and a person reads the queue, the team and the owner of a case after the run with Queue and allocation R, together with Case record R through the case-record slice RWB-P4-E1023-APP (legacy RWB-E1-020 section 10; FSD P4 A2.14, A2.30).
- The case, queue, team and allocation facts the decision needs — the case, its team, its queue, its owner, the team of a summary and the business date of the run — arrive in the authorise request from `rwb-case`, one hop, inside the 2 s timeout. The attribute set of an authorise request for an allocation or a queue read is Not specified in the source documents (GAP-0987; ASM-1734).
- The policy the answers come from is data in `rwb_access`: the role list, the role-to-permission matrix version in force, the letters per capability area and the scope rule. The lists LOV-SCOPE and LOV-CAPABILITY are read through the reference-data contract of `rwb-case` (DP-07). Loading and approving a policy pack is the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP and is out of scope here.
- The access log is a decision-record entry on `rwb.decision-record.v1` written through the local library of DP-03: `AC-READ` for a granted summary read, with the filter, the row count and the team and no personal value, and `AC-DENY` for a refused rerun, with the area, the right and the result and no case fact (FEAT-ACA-07, FEAT-ACA-08).
- Default deny holds: no Workbench role gives 401 MSG-P4-001, no letter in the area gives 403 MSG-P4-002 naming the action, and a team or a case outside the caller's scope gives 404 MSG-P4-003 with no case fact, so the answer never confirms that a team or a case exists.

The allocation itself — package ALLOCATION and package ASSIGNMENT, JOB-03, the round-robin cursor, the caseload caps, the overflow queue, the exception queue, the decision-log entry of the allocation and the `CaseAllocated` event — is the P3 slice of this key (RWB-P3-E1020-APP and its contract RWB-P3-E1020-CON) and is out of scope here. This service reads no rule row, evaluates no Drools rule of its own, runs no job and writes no case row (DP-01, DP-04, DP-10).

### 2. Business rationale

Legacy RWB-E1-020 gives every new case an owner by rule before 07:00 on the morning after case creation, and it names the people who may touch the run: the team manager reads the queue and the allocation summary of their team, the case owner reads the cases given to them, the platform administrator reruns JOB-03, and the run itself writes as the service identity SY-CASEWF (RWB-E1-020 sections 4 and 10). Those rights are the controls on the engine, and the legacy path that carries them is a screen call and a job-monitor call against one monolith; in the target the run is a step of the daily case workflow of `rwb-case` and each service authorises its own object against the cached permission answer of `rwb-access` (Architecture v5 slides 14 and 43; slide 44 JOB-03).

This story supplies that answer for the allocation key on the access side: the letters in the area QUEUE_AND_ALLOCATION, the Platform administration right on a rerun, the TEAM default scope on a summary, and the record of both answers. It meets REQ-CWC-007, REQ-CWC-008, REQ-CWC-009 and REQ-CWC-016 on the authority side — the requirement that every new case is placed by rule, that the rule applies first match, that the owner method and the caps decide, and that every allocation is logged — by making sure that only the people and the identity the policy names can start, read or explain a run. It supports the measure "rule and limit changes made without a code release" at 100 percent, because the letters, the scope values, the areas and their versions are rows in `rwb_access` and list values read through DP-07 (FSD P4 A2.4, A2.14).

The measure of success is that a rerun without Platform administration U is refused before anything runs and leaves a refusal entry, that a summary read is answered only for the caller's own team and leaves one entry naming the filter, the row count and the team, that a case's queue, team and owner are answered only where both the Queue and allocation right and the case-record right hold, and that an approved matrix version changes every answer with no deployment.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E1037-CON | The service contract of `rwb-access` already in force from wave 1: `POST /authorise`, `GET /me/permissions` and `GET /masking-policies` on base `/api/recovery/access/v1`, with the roles, the role-to-permission matrix and the scope rule as data (legacy RWB-E1-037). This story implements the decision behind those operations for the allocation key; it adds no operation |
| RWB-P3-E1020-CON | The case, queue and allocation facts the authorise request is built from — the case, its team, its queue, its owner, the team of an allocation summary and the business date of the run — as the P3 slice of this legacy key publishes them. Which of those attributes an authorise request carries is Not specified in the source documents (GAP-0987; ASM-1734) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), written in the same transaction as the answer |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the reference-data contract that carries LOV-SCOPE (OWN, TEAM, REGION, ALL) and LOV-CAPABILITY (the 14 capability areas, QUEUE_AND_ALLOCATION among them) with the version in force (DP-07); `lov_value` stays P3's, and no scope or area string is written in code |
| RWB-PLT-E1047-CON | The naming library behind the topic and event names of DP-14 |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_access` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves the case list and the allocation summary (DP-19); the route itself is P3's story |

Business preconditions carried from RWB-E1-020, owned by other services where they say so:

- Permission matrix version `PM-2026.11` is in force at the release date of this story, and `PM-2026.12` is loaded by RW-REFADM and approved by RW-SECADM with valid from 2026-12-01 (FSD P4 A2.4 AC-P4-004-01). That `PM-2026.11` is the label in force on 30 November 2026, and which other labels sit between it and the release date, is Not specified in the source documents (GAP-0987; ASM-1744).
- The roster of role codes that hold Queue and allocation letters in the matrix is the acting default of this story — RW-TEAMMGR, RW-CAPACITY, RW-CASEOWN and RW-AUDIT hold R, SY-CASEWF holds CRU and SY-RULES holds R, and RW-REFADM holds none — because the source names the letters of RW-CASEOWN and RW-LEGAL only, and no source fixes the full roster (GAP-0987; ASM-1745).
- The run executes as service identity SY-CASEWF with Queue and allocation CRU and writes as SY-RULES for the rule evaluation (RWB-E1-020 sections 3, 4 and 10).
- The allocation summary exists as an answer of the case service for a team and a business date, carrying the cases read, the cases assigned and the cases in overflow (RWB-P3-E1020-APP; RWB-E1-020 sections 4 and 5).
- The caller signed in through Entra ID with multi-factor authentication and holds at least one Recovery role; with no role the answer is 401 MSG-P4-001 (FSD P4 A2.1).
- The database login is the rwb-access login (DP-02). Its name is Not specified in the source documents (GAP-0987; ASM-1734); the story says "the rwb-access login (DP-02)" and never the shared monolith login.
- The platform contracts the DP rows name are already in place behind RWB-P4-E1037-CON in wave 1. This secondary slice adds no new build dependency of its own (metadata H = None; ASM-1745).

### 4. Flow

1. Caller: the daily case run of `rwb-case` reaches its allocation step, or a platform administrator opens the job monitor and asks for a rerun of JOB-03 for a business date. The run itself needs no person: it presents the service identity SY-CASEWF.
2. Caller: the request names the area, the right and the object attributes the policy reads — for a rerun the area `PLATFORM_ADMINISTRATION`, the right `U` and the job and business date; for a summary the area `QUEUE_AND_ALLOCATION`, the right `R`, the team and the business date; for a case after the run the area `QUEUE_AND_ALLOCATION`, the right `R`, the case and its team and owner. The full attribute set is Not specified in the source documents (GAP-0987; ASM-1734).
3. `rwb-access`: resolves the caller's roles from the session the ACE common module resolved at sign-in, and the letters from `permission` for the matrix version in force. `role`, `permission` and the version are read from `rwb_access` only.
4. `rwb-access`, run and rerun: Platform administration right U on the job and the business date grants the rerun; a caller with only Queue and allocation letters is refused 403 with MSG-P4-002 naming the action, and the refusal is written as an `AC-DENY` entry before the answer (BR2, BR6).
5. `rwb-access`, service identity: SY-CASEWF asks for Queue and allocation C, R and U for the run and is granted by the matrix like a person; a service identity with no role is refused 401 (BR1, BR8). The letters are data, so a run identity granted fewer letters is refused by the same path.
6. `rwb-access`, summary: the team of the summary is compared with the caller's `default_scope` in force, read from LOV-SCOPE through the reference-data contract of DP-07: TEAM admits the caller's own team, OWN admits a team the caller is a member of for their own cases, REGION admits a team in the caller's region, and ALL admits any team (BR3). A team outside the scope is answered 404 with MSG-P4-003 and no team, no count and no case fact, so the answer never confirms that a team exists (BR3).
7. `rwb-access`, case after the run: the queue, the team and the owner of a case are answered only where the caller holds Queue and allocation R and the Case record R answer of RWB-P4-E1023-APP is granted for the same case; where either is refused, the answer is the refusal and carries no queue, no team and no owner (BR4).
8. `rwb-access`: writes one `AC-READ` decision record for a granted summary read, with the filter (business date and team), the row count and the team and no personal value; writes one `AC-READ` for a granted rerun with the job and the business date and no case fact; writes one `AC-DENY` for a refusal with the area, the right and the result. The record is written before the answer (BR5, BR6).
9. `rwb-access`: caches the answer for the matrix version in force. A caller that asks again under the same version is answered from the cache and reads no matrix row twice; the record is still written for that call (BR8).
10. Policy change: a new matrix version (`PM-2026.12`) is approved through the load path, `rwb-access` writes the rows, and publishes `rwb.access.AccessPolicyChanged.v1` on `rwb.access.events.v1` in the same transaction. The cached answer is dropped and the next call is answered under `PM-2026.12`, with no deployment (BR8).
11. Case service: runs the allocation, renders the summary and the case list with the queue, the team and the owner it may show; the run itself, its counts and its queues are RWB-P3-E1020-APP's.

Every answer, granted or refused, is written before it is returned; when the record cannot be written nothing is returned, the call answers 503 with MSG-P7-003 and an incident is raised, so no read of an allocation summary is ever unlogged (BR5, BR6, BR7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The token carries no Recovery role, or no second factor | No answer is given: 401 before the policy is read; one refusal entry with the reason | MSG-P4-001 | AC2 |
| X2 | The caller holds no letter the action needs in the area | Refused before any case fact is read: 403, no case data, and the message names the action | MSG-P4-002 | AC2, AC7 |
| X3 | The team of the summary, or the case, is outside the caller's scope | Not found: 404 with no team, no count and no case fact; one `AC-DENY` entry | MSG-P4-003 | AC4 |
| X4 | The caller holds Queue and allocation R but the Case record R answer of RWB-P4-E1023-APP is refused for the case | The answer is that refusal and carries no queue, no team and no owner | The case-record slice's own message; 403 MSG-P4-002 or 404 MSG-P4-003 as it decides | AC6 |
| X5 | The decision record cannot be written | Nothing is returned: 503 with no case fact and no count, and an incident is raised to the platform administrator queue | MSG-P7-003 | AC8 |
| X6 | Two roles of the caller conflict (for example RW-SECADM with a business role) | The sign-in access check refuses the session from the `role_conflict` rows this service holds; no authorise request is made | MSG-P4-006 | BR9 |
| X7 | A service identity with no role asks for the run | Refused 401 like a person; the run does not start, and the job monitor shows it waiting | MSG-P4-001 | AC1, BR1 |
| X8 | The reference list of scope or capability is not available | No answer is given rather than a guessed one: 503; the refusal is recorded | MSG-GEN-006 | BR9 |
| X9 | Two matrix versions are valid on the same business date | The version whose `valid_from` is the latest on or before the business date is used, and the answer names the version it used | None | AC9, ASM-1744 |

A caller that holds a Queue and allocation letter but no Case record letter is not a path of this story: the case-record answer is RWB-P4-E1023-APP's, and this story only declines to add queue, team and owner to a refusal (DP-11, one hop). Which of the two answers a caller sees first when both refuse is Not specified in the source documents (GAP-0987; ASM-1734); until it is, the Queue and allocation refusal is answered first and the case-record answer is not called.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds and tests against RWB-P3-E1020-CON and its contract fake; reads its own schema only and calls no other service at run time |
| Negotiable | The policy pack — role codes, the letters per area, the scope values and their versions — is data; the story fixes the shape of the answer and the default-deny behaviour only |
| Valuable | The morning run starts under an identity that is checked, a team manager sees its own team's summary, a case's queue, team and owner are answered only to the entitled, and every answer leaves a record |
| Estimable | Three answers behind existing operations, one cache, one decision-record path and one migration with two indexes |
| Small | Fits one sprint with its tests; no screen, no job and no rule package |
| Testable | Every criterion in section 7 has a component or NFR test in section 16; the case side is a published fake |

### 7. Acceptance criteria

```gherkin
Feature: Allocation and assignment engine v1 — the authority slice

  Background:
    Given the rwb-access base path is /api/recovery/access/v1 and the schema is rwb_access
    Given permission matrix version "PM-2026.11" is in force and "PM-2026.12" is approved with valid from 2026-12-01
    Given the matrix gives QUEUE_AND_ALLOCATION right "R" to RW-TEAMMGR, RW-CAPACITY, RW-CASEOWN and RW-AUDIT, right "CRU" to SY-CASEWF, right "R" to SY-RULES and no QUEUE_AND_ALLOCATION letter to RW-REFADM
    Given the matrix gives PLATFORM_ADMINISTRATION right "U" to RW-PLATADM and no PLATFORM_ADMINISTRATION letter to RW-CASEOWN
    Given the default scope in force is "TEAM" for RW-TEAMMGR and RW-CAPACITY, "OWN" for RW-CASEOWN and "ALL" for RW-AUDIT
    Given the rwb-case contract mock returns the allocation summary of team "MTG-BKK" for business date 2026-12-01 with 12 cases read, 11 assigned and 1 in overflow
    Given the rwb-case contract mock returns the allocation summary of team "SME-NTH" for business date 2026-12-01
    Given the rwb-case contract mock returns case "RW-2026-000201" in team "MTG-BKK", queue "MTG-BKK-CO", owner "U-03" and status "ASSIGNED"

  Scenario: AC1 The morning run and its rerun are authorised (new, D-RCV-60)
    Given the run itself executes as service identity "SY-CASEWF" holding QUEUE_AND_ALLOCATION "CRU"
    When "SY-CASEWF" asks POST /api/recovery/access/v1/authorise for area "QUEUE_AND_ALLOCATION", right "C" and the run of job "JOB-03" for business date 2026-12-01
    Then the answer is granted with scope "ALL" under matrix version "PM-2026.11"
    Then one AC-READ decision record is written with area "QUEUE_AND_ALLOCATION", right "C" and the job reference and no case fact
    Given test user "U-7401" holds RW-PLATADM with PLATFORM_ADMINISTRATION right "U"
    When "U-7401" asks for area "PLATFORM_ADMINISTRATION", right "U" and the rerun of job "JOB-03" for business date 2026-12-01
    Then the answer is granted with scope "ALL" under matrix version "PM-2026.11"

  Scenario: AC2 Default deny before any case fact (new, D-RCV-60)
    Given test user "U-7402" holds no Recovery Workbench role
    When "U-7402" asks for area "QUEUE_AND_ALLOCATION", right "R" and the summary of team "MTG-BKK"
    Then the answer is refused with status 401 and message MSG-P4-001
    Then no policy row and no summary row is read and no count is returned
    Given test user "U-7301" holds RW-CASEOWN with QUEUE_AND_ALLOCATION right "R" and no PLATFORM_ADMINISTRATION letter
    When "U-7301" asks for area "PLATFORM_ADMINISTRATION", right "U" and the rerun of job "JOB-03"
    Then the answer is refused with status 403 and message MSG-P4-002 naming the action "rerun the morning allocation run"
    Then no case fact and no job count is returned

  Scenario: AC3 A team manager reads the summary of their own team (new, D-RCV-60)
    Given test user "U-7302" holds RW-TEAMMGR with QUEUE_AND_ALLOCATION right "R" and default scope "TEAM" in team "MTG-BKK"
    When "U-7302" asks for area "QUEUE_AND_ALLOCATION", right "R" and the summary of team "MTG-BKK" for business date 2026-12-01
    Then the answer is granted with scope "TEAM" under matrix version "PM-2026.11"
    Then the answer carries 12 cases read, 11 assigned and 1 in overflow for team "MTG-BKK"
    Then the answer carries no borrower, no account and no personal value

  Scenario: AC4 The summary of another team is not found (new, D-RCV-60)
    Given test user "U-7302" holds RW-TEAMMGR with default scope "TEAM" in team "MTG-BKK"
    When "U-7302" asks for the summary of team "SME-NTH" for business date 2026-12-01
    Then the answer is refused with status 404 and message MSG-P4-003
    Then the answer carries no team name, no row count and no case fact

  Scenario: AC5 A granted summary read leaves one AC-READ entry (new, D-RCV-60)
    Given test user "U-7302" holds RW-TEAMMGR with QUEUE_AND_ALLOCATION right "R" and default scope "TEAM" in team "MTG-BKK"
    When "U-7302" asks for the summary of team "MTG-BKK" for business date 2026-12-01 and the answer is granted
    Then one AC-READ decision record is written before the answer is returned
    Then the record carries the filter (business date 2026-12-01, team "MTG-BKK"), row count 12 and team "MTG-BKK"
    Then the record carries no case ID, no owner, no borrower and no personal value

  Scenario: AC6 The queue, team and owner of a case after the run (new, D-RCV-60)
    Given test user "U-7302" holds RW-TEAMMGR with QUEUE_AND_ALLOCATION right "R" in team "MTG-BKK" and the case-record slice RWB-P4-E1023-APP grants Case record right "R" for case "RW-2026-000201"
    When "U-7302" asks for area "QUEUE_AND_ALLOCATION", right "R" and case "RW-2026-000201"
    Then the answer is granted with scope "TEAM"
    Then the answer carries queue "MTG-BKK-CO", team "MTG-BKK" and owner "U-03"
    Then when the same ask is made for a caller whose Case record right "R" is refused by RWB-P4-E1023-APP
    Then the answer is refused with status 404 and message MSG-P4-003 and carries no queue, no team and no owner

  Scenario: AC7 A refused rerun is recorded with no case fact (new, D-RCV-60)
    Given test user "U-7303" holds RW-CAPACITY with QUEUE_AND_ALLOCATION right "R" and no PLATFORM_ADMINISTRATION letter
    When "U-7303" asks for area "PLATFORM_ADMINISTRATION", right "U" and the rerun of job "JOB-03" for business date 2026-12-01 and the answer is refused
    Then the answer is refused with status 403 and message MSG-P4-002
    Then one AC-DENY decision record is written with area "PLATFORM_ADMINISTRATION", right "U" and result "REFUSED"
    Then the record carries no case ID, no team, no owner and no job count, and nothing runs

  Scenario: AC8 A read that cannot be recorded returns nothing (new, D-RCV-60)
    Given test user "U-7302" holds RW-TEAMMGR with QUEUE_AND_ALLOCATION right "R" in team "MTG-BKK"
    Given the decision-record write is forced to fail
    When "U-7302" asks for the summary of team "MTG-BKK" for business date 2026-12-01
    Then the call answers status 503 with message MSG-P7-003
    Then no count, no team and no case fact is returned
    Then an incident is raised to the platform administrator queue and no policy row changes

  Scenario: AC9 An approved matrix version changes the answer with no deployment (new, D-RCV-60)
    Given test user "U-7304" holds RW-LEGAL, which has no QUEUE_AND_ALLOCATION letter in "PM-2026.11"
    When "U-7304" asks for the summary of team "MTG-BKK" twice inside matrix version "PM-2026.11"
    Then the second answer is served from the cached decision without a second read of the permission matrix
    Then each answer is returned inside the 2 s timeout and each refusal writes its own AC-DENY entry
    Then when matrix version "PM-2026.12" is approved and rwb.access.AccessPolicyChanged.v1 is published for it
    Then the next ask is answered under matrix version "PM-2026.12" with no deployment
    Then the same ask is granted, because "PM-2026.12" gives RW-LEGAL right "R" in QUEUE_AND_ALLOCATION, and one AC-READ entry is written for the granted summary read
```

AC1 to AC9 are the criteria this story owns, and every one of them is new under D-RCV-60 because this slice owns no legacy acceptance criterion. In AC1 the two callers prove that the run identity and the person who reruns are checked by the same matrix — SY-CASEWF through Queue and allocation CRU, RW-PLATADM through Platform administration U — and that neither is a hard-coded exception. In AC2 the two refusals are proved before any case fact is read: 401 when there is no role, 403 when there is no letter, with the action named so the reader knows what they are missing. In AC3 and AC4 the same caller proves that the summary is scoped per team, that the scope value is read from the list, and that a team outside the scope is answered as not found rather than as forbidden. In AC5 the entry of a granted summary read is proved to carry the filter, the row count and the team and no personal value, which is the shape the access log needs for an export or a screen read (FSD P4 A2.7 AC-ALT-P4-007-02). In AC6 the case read is proved to need both answers, so a Queue and allocation letter alone never discloses the queue, the team or the owner of a case. In AC7 the refusal is proved twice: as the answer the caller gets and as the entry the audit reads. In AC8 the record-before-answer rule is proved to leave nothing behind. In AC9 the cached answer is proved to change on the policy event and to need no deployment.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A caller with no Recovery Workbench role is refused 401 with MSG-P4-001 before the policy is read; a service identity is checked exactly as a person is | FSD P4 A2.1 VR-P4-001-1; TSD P4 T6.2; NFR-051 |
| BR2 | A rerun of the morning allocation run JOB-03 needs Platform administration right U; a caller whose roles hold no such letter is refused 403 with MSG-P4-002 naming the action, and nothing runs | Legacy RWB-E1-020 section 10; section 5 X10; FSD P4 A2.4 VR-P4-004-1; TSD P4 T6.1 |
| BR3 | The allocation summary of a team is answered only where the team satisfies the caller's `default_scope` in force: TEAM for the caller's own team, OWN, REGION or ALL; a team outside it is answered 404 with MSG-P4-003 and no team, no count and no case fact | FSD P4 A2.14 VR-P4-014-1; LOV-SCOPE; legacy AC9 of RWB-E1-020 |
| BR4 | The queue, the team and the owner of a case are answered only where the caller holds Queue and allocation right R and the Case record right R answer of RWB-P4-E1023-APP is granted for the same case; where either is refused, the answer carries none of the three | Legacy RWB-E1-020 section 10; Architecture v5 slide 14 (every service authorises its own object); DP-11 |
| BR5 | Every granted answer writes one `AC-READ` decision record before the answer is returned: a summary read with the filter, the row count and the team, a rerun with the job and the business date, and no personal value in either | FSD P4 A2.7 AC-P4-007-01, AC-ALT-P4-007-02; FEAT-ACA-07; FEAT-ACA-08 |
| BR6 | Every refusal writes one `AC-DENY` decision record with the area, the right and the result, and carries no case fact | FSD P4 A2.7 AC-EXC-P4-007-04; FEAT-ACA-07 |
| BR7 | A decision that cannot be written is not taken: the call answers 503 with MSG-P7-003, nothing is returned and an incident is raised | FSD P4 AC-EXC-P4-007-03; principle 5; R-UNI-39; CTL-06 |
| BR8 | An answer is cached for the matrix version in force and dropped when `AccessPolicyChanged` arrives, so an approved matrix version takes effect with no deployment | Architecture v5 slide 43; FSD P4 A2.4 AC-P4-004-01; DP-14 |
| BR9 | Role codes, capability areas, letters, scope values and every version are data read from `rwb_access` and the reference lists; no business value is written in code | FSD P4 BR-P4-004, BR-P4-005, BR-P4-014; TSD P4 T3.2; principle 1 |
| BR10 | The case, queue, team and allocation facts a decision uses arrive in the request; no table of `rwb_case`, `rwb_decision` or `rwb_source_data` is read, and no rule row is read | DP-01, DP-04; ownership map (case, queue, queue_member, assignment, timer to P3; rule_row, rule_package to P7) |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is a check on the session the ACE common module resolved, before any row of `permission` is read; the refusal is written with the reason and no area, because there is no area to name yet.
- BR2 is a read of `permission` for the caller's roles, the area `PLATFORM_ADMINISTRATION` and the `matrix_version` in force; the letters C, R, U, D and A are held as the five-character field of TSD P4 T3.1, and the answer names the version it used. The rerun grant is not a job of this service: JOB-03 runs as a step of the daily case run in `rwb-case` (DP-10).
- BR3 is the scope rule of `ScopeRule`, comparing the team of the summary and the team of the caller with the `default_scope` value read through DP-07; the scope names OWN, TEAM, REGION and ALL are list values, never Java constants. The attribute names of a request are Not specified in the source documents (GAP-0987; ASM-1734).
- BR4 is the one place where two answers meet: this service answers Queue and allocation R and reads the case-record answer of RWB-P4-E1023-APP, which is a local call inside the same service and the same schema, so no cross-service call is added and the 2 s budget of DP-11 is unchanged. Whether the case-record answer or this one is asked first is a caller choice; both are needed.
- BR5 and BR6 are the same `RecordAndApply` transaction as the answer: the record is written first, the answer is returned after it commits, and a failure answers 503 with MSG-P7-003 and changes nothing (X5).
- BR7 is visible in the code review as one writer: no answer path returns before the record call returns.
- BR8 is a cache keyed by the matrix version in force; the `AccessPolicyChanged` entry that drops it is published by the same transaction that writes the new policy rows, and the version label is data.
- BR9 is visible in the code review: no role code, area name, letter, scope name or version string appears in a constant, and the roster the tests use is the acting default of ASM-1745 rather than a source fact.
- BR10 is the reason there is no repository for a case, a queue or a rule: the service holds `role`, `permission`, `role_conflict`, the decision record and the outbox, and nothing else.

### 9. State transitions

None for a case. This story changes no case status, no queue, no assignment, no round-robin cursor and no timer: the case and its queue, owner and allocation are P3's, the run is a step of the daily case run in `rwb-case`, and the rule packages are P7's registry (DP-01, DP-04, DP-10; Architecture v5 slides 41 and 44). This story runs no workflow of its own and owns no Schedule.

The only states this story has are the states of its answer and of its record, which it does not persist beyond the record:

| Answer state | When | What the caller gets | Record written |
|---|---|---|---|
| Granted | The caller holds the letter the area needs and the team or the case is in scope | The granted answer with the scope it used, the letters and the matrix version in force; for a summary the counts, for a case the queue, team and owner | `AC-READ` |
| Refused, no right | No role of the caller holds the letter in the area, or no Recovery role at all | 403 MSG-P4-002 naming the action, or 401 MSG-P4-001 for no role; no case fact | `AC-DENY` |
| Not found | The caller holds the letter and the team or the case is outside the scope | 404 MSG-P4-003, no team, no count and no case fact | `AC-DENY` |
| Not answered | The record cannot be written, or the reference list cannot be read | 503 with MSG-P7-003 or MSG-GEN-006, no case fact | None; the failure is raised as an incident |

A granted answer has no stored state of its own beyond the cache entry for the matrix version in force and the decision record: the objects it is about are P3's and their state is P3's, so nothing here is reconciled back.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Queue and allocation R with default scope TEAM: reads the allocation summary of the team, and the queue, team and owner of a case of the team (legacy RWB-E1-020 section 10) |
| RW-CAPACITY, capacity and workforce planner | Queue and allocation R with default scope TEAM: reads the summary of the team to plan the load; the default scope of the role is the acting default of ASM-1745 |
| RW-CASEOWN, case owner | Queue and allocation R with default scope OWN: reads the queue and the owner of a case it owns, and nothing of another owner's case |
| RW-PLATADM, platform administrator | Platform administration U: reruns JOB-03 from the job monitor; the rerun itself is P3's step and this service answers only the grant |
| RW-COE, centre of excellence analyst | Reads the versions in force through `GET /me/permissions` and the matrix rows behind the load path; the story asserts no Queue and allocation letter for the role and adds nothing beyond what the matrix says |
| RW-AUDIT, internal audit | Queue and allocation R with default scope ALL: reads any team's summary and any case's queue and owner, and reads the entries this story writes |
| RW-REFADM, reference data administrator | No Queue and allocation letter: refused MSG-P4-002 on a summary. Prepares the matrix workbook; the load and the approval are the load path's stories |
| SY-CASEWF, case workflow module | Queue and allocation CRU: the run allocates and writes with these letters, so the run does not depend on a person's session |
| SY-RULES, Drools evaluator | Queue and allocation R: reads the allocation and assignment answers the run needs; the rule packages themselves are RWB-P3-E1020-APP's and RWB-P7-E1020-APP's, and this service evaluates no rule |

Reading is the whole of this story: it grants or refuses a read, a summary and a rerun, and writes the record of each. It changes no case, no queue, no assignment and no policy row. A policy row changes only through the load path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and a break-glass grant, its incident reference and its four-hour ceiling stay with the wave-1 stories of the access service.

No delegation of authority level applies to an allocation: an allocation is made by a rule package and a cap, not by an approved limit, so the delegation table, its approval levels and its lookup are RWB-P4-E2013-APP's and are not read here.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-0987; ASM-1734); the story refers to "the rwb-access login (DP-02)".

### 11. Data

| BR Field ID | Table in rwb_access | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read (the sign-in check, X6) |
| DF-REF-027 to DF-REF-033 | `lov_value` | LOV-SCOPE and LOV-CAPABILITY values, read through the reference-data contract of DP-07 | Read through the contract; the table is P3's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the `AC-READ` and `AC-DENY` entries: code, actor, area, right, case ID where there is one, actions, decided at | Write |
| (outbox) | outbox library table in `rwb_access` | the `AccessPolicyChanged` row and the decision-record row | Write |
| (inbox) | `processed_event` | event_id, consumer, processed_at; used by the policy listener | Write |

`permission.capability_area` carries `QUEUE_AND_ALLOCATION` and `PLATFORM_ADMINISTRATION` as list values of LOV-CAPABILITY, and `permission.letters` carries the five-character string of TSD P4 T3.1; `role.default_scope` carries a LOV-SCOPE value. The answer echoes the area, the letters and the version it used and never a person's name: the actor appears as a user reference (U-xxxx) and the run as SY-CASEWF. No personal value enters `rwb_access`, the answer, the record or the event, because the objects of this key are cases, teams and queues and the summary carries counts only (NFR-039, NFR-040).

The case, queue, team and allocation facts of a request — the case ID, its team, its queue, its owner, the team of a summary and the business date — are read from the request and never from a table: `recovery_case`, `queue`, `queue_member`, `assignment`, `timer` and `rule_row` are P3's and P7's, and no foreign key and no query crosses a schema (DP-01, DP-04). No statement of this story names any of those six tables. Which attributes a request must carry is Not specified in the source documents (GAP-0987; ASM-1734).

### 12. Contract

#### 12.1 REST operations provided

None new in this story. The operations are those of the service contract already in force from wave 1 (RWB-P4-E1037-CON), on base `/api/recovery/access/v1`, owner rwb-access (P4), unchanged in path, request, response and error shape:

| Operation | Path | What this story decides behind it |
|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | The letters in `QUEUE_AND_ALLOCATION` and `PLATFORM_ADMINISTRATION`, the scope of a team or a case, and the record of the answer. Errors 401 (MSG-P4-001), 403 (MSG-P4-002), 404 (MSG-P4-003), 503 (MSG-P7-003, MSG-GEN-006) |
| GET | `/api/recovery/access/v1/me/permissions` | The roles, the letters per area, the scope and the matrix version of the caller, as the session resolved them |
| GET | `/api/recovery/access/v1/masking-policies` | The masking version in force and the fields it covers for the caller's roles; unchanged by this story and not read by it |

`GET /doa-limits` is the same service's operation and is not used here: the delegation of authority table and its routing lookup are RWB-P4-E2013-APP's.

#### 12.2 REST operations consumed

None. The case, queue and allocation facts arrive in the authorise request, built by the caller from its own rows; this story calls no service at run time. The shape it expects is the one RWB-P3-E1020-CON publishes, and that contract is used as a fake in the tests (12.8) and as the alignment reference in the build. The Case record answer of BR4 is a local call inside this service, so it adds no hop (DP-11).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | policy kind and version | the policy kind (permission matrix, roles, scope), the version label, the valid-from date and the change reference |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | caseId where there is one, else the actor reference | the hash-chained `AC-READ` or `AC-DENY` record |

CloudEvents 1.0 envelope. Neither payload carries a personal value and the allocation event of the key is not published here: `CaseAllocated` (EV-02) is rwb-case's, on `rwb.case.events.v1` (Architecture v5 slide 42 row 02; ownership map EV-02 = P3). This story publishes no allocation event of its own.

#### 12.4 Events consumed

None. A policy change is written and published by the same service, so the cache is dropped on the commit that publishes `AccessPolicyChanged` rather than on a consumed event; the topic exists for the other services' caches (Architecture v5 slide 43: all consume it for cache refresh). The run's own events are P3's and this service subscribes to none of them.

#### 12.5 Workflows and activities

None. This story runs no Temporal workflow and registers no activity on `rwb-access`. JOB-03 is a step of the daily case run in `rwb-case` (Architecture v5 slide 44), and this service answers a question about it; it starts nothing.

#### 12.6 Schedules

None. The six-monthly access review list (JOB-18) is the Temporal Schedule of this service, and its story is RWB-P4-AD008-APP. This story starts no Schedule, reads no `timer` row and replaces no Quartz job of the key (DP-10).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | The caller's roles, their `role_class` and their `default_scope` |
| `permission` | P4 (`rwb_access`) | The letters in `QUEUE_AND_ALLOCATION` and `PLATFORM_ADMINISTRATION` and the `matrix_version` in force |
| `role_conflict` | P4 (`rwb_access`) | The conflicting role pairs the sign-in check reads |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | Outbox, inbox and idempotency objects (DP-09) |
| `lov_value`, `reference_row`, `reference_version` | P3 (`rwb_case`) | LOV-SCOPE and LOV-CAPABILITY, read through the contract; not owned here |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read in this story: the rule registry and the package evaluation are the P7 slice's (DP-04) |
| `masking_rule`, `delegation_limit` | P4 (`rwb_access`) | Not read in this story: masking is the case-record slice's, the delegation table is RWB-P4-E2013-APP's |

No table of `rwb_case`, `rwb_decision` or `rwb_source_data` is read: the case, the queue, the assignment, the timer and the rule row stay with their owners, and the only fields of them that enter this service are identifiers and counts carried by a request (DP-01, DP-04).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case allocation and queue WireMock | RWB-P3-E1020-CON | The summary of team MTG-BKK for 2026-12-01 with 12 read, 11 assigned and 1 in overflow; the summary of team SME-NTH; case "RW-2026-000201" in team MTG-BKK, queue MTG-BKK-CO, owner "U-03", status ASSIGNED; the same case with no queue for a case not yet allocated |
| decision-record fake | RWB-PLT-E1027-CON | The `AC-READ` and `AC-DENY` write and the publish on `rwb.decision-record.v1`, including the forced failure of X5 |
| policy pack fixture | RWB-P4-E1037-CON | Matrix version PM-2026.11 in force and the later PM-2026.12 for AC9; the roles, the letters and the scopes of the background |
| reference-data fake | RWB-P3-E1043-CON | LOV-SCOPE (OWN, TEAM, REGION, ALL) and LOV-CAPABILITY with QUEUE_AND_ALLOCATION and PLATFORM_ADMINISTRATION, with the version in force, and the unavailable list of X8 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 0 new (3 existing operations of RWB-P4-E1037-CON implemented), consumed 0 | Base `/api/recovery/access/v1`; the case, queue and allocation facts arrive in the request |
| Kafka | Published 1 service event and 1 decision record; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-access`; JOB-03 is a step of P3's daily case run |
| File | None | No file input or output, and no export |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/allocation-authority`, Java package `th.co.scb.ace.workbench.recovery.access.allocation`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

What each DP means for this authority slice:

- DP-01 is the reason the service answers from the attributes it is given: `recovery_case`, `queue`, `queue_member`, `assignment`, `timer` and `rule_row` are P3's and P7's, so the queue, the team, the owner and the counts arrive as identifiers and figures in the request and never from a joined query.
- DP-03 is the access log: an `AC-READ` and an `AC-DENY` are decision records on `rwb.decision-record.v1`, so an access question and a decision question are answered from one log, and the allocation's own decision-log entry stays P3's.
- DP-04 is recorded because the legacy key evaluates package ALLOCATION and package ASSIGNMENT through `RuleEvaluator`: in the target the rule packages and the Drools evaluation stay with `rwb-decision` (the registry) and `rwb-case` (the evaluation), and this story reads no rule row and runs no Drools rule of its own.
- DP-05 is recorded because the legacy key reads ACE data for the case snapshot: this story reads no ACE view at all, and the customer data of a case is P1's through P3's contract.
- DP-06 is recorded because the legacy key reads two parameters for the exception and deviation queues: this story reads no parameter, and both remain P3's data.
- DP-09 is recorded because the key writes application events: here the only outbox row this story writes is the decision-record row of an access entry, and the allocation event `CaseAllocated` is P3's on `rwb.case.events.v1`.
- DP-10 is recorded because the key owns JOB-03: no job of this key runs in this service, JOB-03 is a step of P3's daily case run, and the access review Schedule (JOB-18) belongs to RWB-P4-AD008-APP.
- DP-11 is the caller-facing boundary: one hop, 2 s timeout, cached, and the answer must hold inside it; the case-record answer of BR4 is a local call and adds no hop.
- DP-13, DP-14 and DP-15 are the naming and migration conventions of the service: the base is `/api/recovery/access/v1`, the topic is `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, and the one migration below sits in the `rwb_access` Flyway sequence.
- DP-19 is the route that renders the answer: the case list SCR-02 and the allocation summary are P3's through the gateway-bff composite route, and this story supplies only the grant, the counts and the refusal.

The platform contracts behind these rows are wave-1 preconditions of RWB-P4-E1037-CON, already in place; this secondary slice adds no new build dependency of its own (metadata H = None; ASM-1745).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseController | Controller | The three operations of the existing contract on `/api/recovery/access/v1`; validation and problem responses |
| AllocationAuthorityService | Service | The letters, the rerun grant, the scope of a team or a case and the two-answer rule of BR4, in that order; one answer, one record |
| PermissionResolver | Service | Reads `permission` for the caller's roles and the `matrix_version` in force; resolves the five letters and the areas |
| ScopeRule | Service | Compares the team of the summary, or the team and owner of a case, with the `default_scope` value in force |
| RunAuthorityService | Service | The Platform administration U answer for a rerun and the Queue and allocation CRU answer for the run identity; no job is started here |
| CaseAllocationViewService | Service | Joins this service's Queue and allocation answer with the case-record answer of RWB-P4-E1023-APP; returns the queue, team and owner or nothing |
| AccessRecordWriter | Service | The `AC-READ` and `AC-DENY` entries through the library of DP-03, and the `AccessPolicyChanged` outbox row |
| PolicyCache | Service | The cached answer per matrix version, dropped on the policy change |
| PolicyChangeListener | Service | Applies a new matrix version and publishes `rwb.access.AccessPolicyChanged.v1` in the same transaction |
| AccessRepository | Repository | `role`, `permission`, `role_conflict`, inbox and outbox in `rwb_access`; no foreign table |

**Database and migrations**

- No new table: `role`, `permission` and `role_conflict` exist from the wave-1 stories of this service behind RWB-P4-E1037-CON, and the matrix rows are loaded by the load path stories.
- One migration in the per-service Flyway sequence of DP-15: `V1020_1__allocation_authority_read_path.sql` adds `ix_permission_role_area` on `permission (role_id, capability_area, matrix_version)` and `ix_role_scope` on `role (role_code, default_scope)`, so the two reads of an answer are index reads inside the 2 s budget of DP-11.
- The matrix rows are versioned by `matrix_version` and the roles' `valid_from` and `valid_to`; this story writes none of them, and a version is never edited in place (a new version is loaded, approved and published).
- No column of this migration carries a business value: the area names, the letters and the scope names are row values, and the index names are neutral.

**Configuration and reference data**

- The matrix version in force is data: the latest `valid_from` on or before the business date, read from `permission.matrix_version`. The label in force at the release date is the acting default `PM-2026.11`, with `PM-2026.12` approved from 2026-12-01 (GAP-0987; ASM-1744).
- LOV-SCOPE (OWN, TEAM, REGION, ALL) and LOV-CAPABILITY (the 14 capability areas, QUEUE_AND_ALLOCATION and PLATFORM_ADMINISTRATION among them) through the reference-data contract of DP-07 (RWB-P3-E1043-CON).
- The roster the tests use is the acting default of ASM-1745 and is a row set in `permission`, not a table in code; a change of roster is a new matrix version.
- No parameter row, no timeout constant and no role code in code: the 2 s is the platform standard of RWB-PLT-E1037-CON's client, and the cache lives for the matrix version in force (BR8).
- The database login is the rwb-access login (DP-02): Not specified in the source documents (GAP-0987; ASM-1734).

**Build steps**

1. `PermissionResolver` over `permission` and `role`, with the matrix version named in the answer; tests for AC2 and AC9, and a test that a new area name and a new letter set are accepted as data.
2. `RunAuthorityService`: the Platform administration U grant for a rerun and the Queue and allocation CRU grant for SY-CASEWF, with no job started; tests for AC1 and AC7.
3. `ScopeRule`: the TEAM default scope on a summary, the other three scope values, and the not-found answer with no team and no count; tests for AC3 and AC4.
4. `CaseAllocationViewService`: the two-answer rule of BR4 with the case-record answer stubbed, and the answer with no queue, no team and no owner when either refuses; test for AC6.
5. `AccessRecordWriter`: the `AC-READ` entry of a summary read with the filter, the row count and the team, the `AC-DENY` entry of a refused rerun, and the forced failure of X5; tests for AC5, AC7 and AC8.
6. `PolicyCache` and `PolicyChangeListener` with the publish and the drop; test for AC9 against the PM-2026.12 fixture.
7. The migration with the two indexes, and a timing test that one answer stays inside the 2 s budget on a matrix pack of the loaded size, against the contract fake of RWB-P3-E1020-CON and the decision-record fake.

**Feature switch.** `rwb.p4.allocation-summary`, read from the platform feature-flag library under the R-PREC default ruling. Off: the summary read of BR3 is not answered — every caller other than RW-PLATADM and RW-AUDIT is answered 403 MSG-P4-002 and the `AC-DENY` entry is written as usual, while the rerun grant, the record and the caching are unchanged — so the switch narrows the answer and never widens a scope. It needs no schema rollback and blocks no case read that the policy allows.

**Done when.** The tests in section 16 pass; a rerun with Platform administration U is granted and a rerun without it is refused with one `AC-DENY` entry; the run identity SY-CASEWF is granted Queue and allocation CRU by the matrix; a team manager reads the summary of their own team with the counts and no personal value; another team is answered 404 with no team and no count; a granted summary read leaves one `AC-READ` entry with the filter, the row count and the team; a case's queue, team and owner are answered only with both rights; a record failure leaves nothing returned; and an approved matrix version changes every answer with no deployment.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token carries no Recovery role, or no second factor | You have no Recovery Workbench role. Ask your team manager to request one. | The access check before this story's answer (X1, X7) |
| MSG-P4-002 | No role of the caller holds the letter the area needs | You cannot {action} here. Your role does not include it. | This story, on the refusal of BR2 and BR4 |
| MSG-P4-003 | The team or the case is outside the caller's scope | This case is not in your scope. | This story, on the refusal of BR3 and BR4 |
| MSG-P4-006 | Two roles of the caller conflict | {role} may not be held together with {role}. | The access check, from this service's `role_conflict` rows (X6) |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on every answer (X5) |
| MSG-GEN-006 | A list the answer needs is not available | {system} is not available. Your request is queued and will be retried. | This story, on a reference-list failure (X8) |

For MSG-P4-002 the {action} value is the action the caller attempted, for example "rerun the morning allocation run" or "read the allocation summary"; for MSG-P4-003 no team name and no case fact is echoed, because the message must not confirm that a team or a case exists. Every error is an RFC 9457 problem response with `messageId`, the text with its placeholders filled and the instance of the request; the Thai text follows DL10.

### 15. Screens and states

This story builds no screen. SCR-02 Case list, the allocation summary panel, its route and its paging are RWB-P3-E1020-APP's through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the job monitor that offers the rerun is the platform's console, and the case record view SCR-03 is RWB-P3-E1023-APP's.

What this story decides for the case list and for the summary is what each state may show:

| Screen | State | What the answer decides |
|---|---|---|
| SCR-02 Case list | Post-run list, granted | The queue, the team and the owner of each case are rendered because both the Queue and allocation right and the case-record right hold; the list holds no rule of its own |
| SCR-02 Case list | Allocation summary, granted | The counts of the caller's own team are rendered; the summary carries no case and no personal value |
| SCR-02 Case list | Summary of another team | The panel shows MSG-P4-003 and no team name, no count and no case fact, and one `AC-DENY` entry exists |
| SCR-02 Case list | Refused | The panel shows MSG-P4-002 with the action and no case fact, and one `AC-DENY` entry exists |
| SCR-02 Case list | Not available | The panel shows MSG-P7-003 where the record could not be written, and no case fact |
| Job monitor | Rerun offered | The button is shown only where the caller holds Platform administration U; the rerun itself is P3's and the job monitor is the platform's |
| Job monitor | Rerun refused | The monitor shows MSG-P4-002 and nothing runs, and one `AC-DENY` entry exists |

A screen that shows a summary of a team the caller is not scoped for, or a queue the caller may not read, is a defect of the screen, not of the answer: the answer always names the scope and the matrix version it used.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-020-14 | AC7, BR2, BR6 — the refused rerun and its `AC-DENY` entry | Component | RW-CASEOWN "U-7301" (Queue and allocation R, no Platform administration U) asks for the rerun of JOB-03; refused 403 MSG-P4-002 with action "rerun the morning allocation run", one `AC-DENY` entry, nothing runs |
| TC-E1-020-01 | owned by RWB-P3-E1020-APP (the queue a new case is placed in) | Component | One case per product group and region; package ALLOCATION "ALLOC-2026.11"; the case side's data |
| TC-E1-020-15 | AC8, BR7 — the decision-record failure | NFR | The record write forced to fail for a granted summary read and for a granted rerun; 503 MSG-P7-003, nothing returned, nothing changed |
| TC-E1-020-08 | owned by RWB-P3-E1020-APP (a repeated run for the same business date) | Component | The same run repeated for 2026-12-01; the case side's data |
| TC-E1-020-02 | owned by RWB-P3-E1020-APP (the owner chosen by the assignment rule) | Component | Three owners with 120, 95 and 140 open cases; the case side's data |
| TC-E1-020-03 | owned by RWB-P3-E1020-APP (an owner at the cap is skipped) | Component | The next owner at 150 open cases; the case side's data |
| TC-E1-020-04 | owned by RWB-P3-E1020-APP (every owner at the cap, overflow) | Component | Every owner at 150 open cases; the case side's data |
| TC-E1-020-05 | owned by RWB-P3-E1020-APP (no allocation rule matched) | Component | Product group SSME and region NE3 with no rule; the case side's data |
| TC-E1-020-06 | AC5, BR5 — the `AC-READ` entry of a granted summary read | Component | Summary of team MTG-BKK for 2026-12-01 with 12 read, 11 assigned and 1 in overflow; one entry with the filter, row count 12 and team MTG-BKK and no personal value |
| TC-E1-020-07 | owned by RWB-P3-E1020-APP (a case with an open deviation) | Component | A case with an open deviation; the case side's data |
| TC-E1-020-09 | owned by RWB-P3-E1020-APP (a run with no new cases) | Component | No case with status NEW on 2026-12-01; the case side's data |
| TC-E1-020-10 | owned by RWB-P3-E1020-APP (the run waits for case creation) | Component | JOB-02 not complete for the business date; the case side's data |
| TC-E1-020-11 | owned by RWB-P3-E1020-APP (two runs at once allocate each case once) | Component | Two workers on the same case; the case side's data |
| TC-E1-020-12 | owned by RWB-P3-E1020-APP (an owner one case below the cap) | Component | The next owner at 149 open cases; the case side's data |
| TC-E1-020-13 | owned by RWB-P3-E1020-APP (a queue with no overflow queue) | Component | Queue HP-CEN-CO with no overflow queue and every owner at 150; the case side's data |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Every legacy test case of the key is listed above: the three that this slice answers are rewritten to the criteria it owns — TC-E1-020-14 to the refused rerun of AC7, TC-E1-020-06 to the `AC-READ` entry of a granted summary read of AC5, and TC-E1-020-15 to the decision-record failure of AC8 — and the twelve that test the allocation itself stay with RWB-P3-E1020-APP and are named here only so that the key's test set is not lost. The legacy levels map as the Template and Rules require: Access maps to Component, System maps to Component because the case-side assertion is stubbed by RWB-P3-E1020-CON, and Resilience maps to NFR. No `-ITG` copy sits in this story: the integration copy of this key is RWB-ITG-E1020-ITG.

### 17. Guardrails

- No business value in code: role codes, capability areas, the letters, the scope values and the matrix version are data rows in `rwb_access` and list values read through DP-07; the switch is a platform flag (BR9).
- No personal data in logs, events, the record or the tests: the summary carries counts, the `AC-READ` entry carries the filter, the row count and the team, the `AC-DENY` entry carries the area, the right and the result, and the event carries version labels; the actor appears as a user reference (U-xxxx) or as SY-CASEWF, and test data is synthetic (NFR-039, NFR-040).
- No cross-schema read (DP-01): `recovery_case`, `queue`, `queue_member`, `assignment`, `timer` and `rule_row` are never queried; the case, queue and allocation facts arrive in the request and the policy is the service's own.
- One writer for the policy: only the load path stories of this service write a role or a permission row; this story reads them and publishes the change, so an answer and the matrix it names cannot disagree.
- The record is written before the answer: a failure answers 503 with no case fact and raises an incident, so no summary read and no rerun grant is unlogged (BR5, BR6, BR7).
- Default deny everywhere: no role gives 401, no letter gives 403 with the action named, and a team or a case outside the scope gives 404 with no fact; an answer that fails open is a defect of the answer.
- The answer is idempotent for a matrix version: the same question under the same version returns the same answer, and the cache is dropped on the policy event rather than on a timer.
- The feature switch changes one rule and no schema, and it never widens a scope: off narrows the summary read to nothing for the roles it names and leaves every other decision as it was.
- No allocation logic here: the story adds no package row, no cap, no cursor and no overflow rule, and it reads no rule row (DP-04).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-07 | 18.3.2 Allocate work to teams, people and partners by rule | BR1, BR2 | TC-E1-020-14, and the allocation side in RWB-P3-E1020-APP |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | BR1, BR9 | TC-E1-020-06, and the allocation side in RWB-P3-E1020-APP |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-08 | 18.3.2 | BR3, BR4 | TC-E1-020-06, TC-E1-020-15, and the allocation side in RWB-P3-E1020-APP |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-07 | 6.1 Take over the case at 90 days past due | BR5, BR6, BR7 | TC-E1-020-15, TC-E1-020-06, TC-E1-020-14 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P3-E1020-CON | CON | The contract this story builds against: the case, queue, team, owner and summary attributes an authorise request carries, used as a fake in the tests and as the build reference. C dependency; it never blocks |
| RWB-P3-E1020-APP | APP | The allocation slice of the same legacy key: packages ALLOCATION and ASSIGNMENT, JOB-03, the cursor, the caps, the overflow queue, the allocation's decision-log entry and the `CaseAllocated` event. It calls the answer of this story; this story does none of it |
| RWB-P4-E1037-CON | CON | The service contract whose three operations this story implements, and the wave-1 place where the platform contracts behind the DP rows are already in place |
| RWB-PLT-E1037-CON | CON | The platform guard and client library behind the service contract: the 2 s timeout, the cache client and the error shape of the answer |
| RWB-P4-E1023-APP | APP | The case-record slice: it answers Case record R for a case, which BR4 needs before the queue, team and owner are returned |
| RWB-P7-E1020-APP | APP | The rule package registry and the evaluation of packages ALLOCATION and ASSIGNMENT: this story reads no rule row and runs no Drools rule of its own |
| RWB-S8-E1020-APP | APP | The deviation slice: it places a case with an open deviation in the deviation handler queue. This story answers the letters for that placement and knows nothing of the queue choice |
| RWB-ITG-E1020-ITG | ITG | The wave-1 integration harness copy of the key's tests, which proves the real cross-service behaviour end to end against this answer |

| Legacy reference | Where it is kept |
|---|---|
| The authority table of section 10 (SY-RULES, SY-CASEWF, RW-TEAMMGR, RW-CASEOWN, RW-PLATADM, RW-REFADM, the process owner's approval) | Sections 1, 3, 10 |
| The refusal of a rerun by a user without the right (X10, MSG-P4-002) | Sections 4, 5, 7, 14 |
| The allocation summary per team and the counts of overflow and exception (MSG-P3-011, MSG-P3-012) | Sections 3, 7, 12.8 |
| The rule ID and package version on every allocation decision-log entry (BR9 of the legacy key) | Sections 2, 13, 18, as the access record of the same answer |
| MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-P4-006, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| The five letters C, R, U, D and A, the areas QUEUE_AND_ALLOCATION and PLATFORM_ADMINISTRATION, and LOV-SCOPE | Sections 3, 8, 10, 11 |
| Legacy key RWB-E1-020, story RWB-P4-E1020-APP, contract RWB-P3-E1020-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The rwb-case slice of this legacy key, RWB-P3-E1020-APP and its contract RWB-P3-E1020-CON: package ALLOCATION and package ASSIGNMENT, JOB-03 and its run, the round-robin cursor, the caseload caps, the overflow queue, the exception queue, the allocation summary itself, the allocation's decision-log entry and the `CaseAllocated` and `CaseAllocationFailed` events.
- RWB-P7-E1020-APP, the rule package registry, the version lifecycle, the dry run, the approval and the Drools evaluation of the packages: this story reads no rule row and runs no rule.
- RWB-S8-E1020-APP and the deviation-queue placement of a case with an open deviation.
- RWB-ITG-E1020-ITG, the wave-1 integration harness copy of the tests of this key, which proves the real cross-service behaviour end to end.
- Loading, approving and rolling back the policy pack: the reference-load and approval path of RWB-P4-AD002-APP and RWB-P4-AD004-APP, and the administration screens of Epic 8. This story reads the versions in force and publishes the change.
- The six-monthly access review list (JOB-18, RWB-P4-AD008-APP) and every other job, workflow and Schedule of this service.
- The delegation of authority table, its approval levels and its lookup (RWB-P4-E2013-APP and RWB-P4-E2014-APP); no delegation level applies to an allocation.
- Break-glass access, its incident reference, its ceiling and its review (the wave-1 stories of this service).
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
