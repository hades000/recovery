# RWB-P4-AD008-APP Access review list

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P4-A |
| Ready to start | After RWB-P4-E1022-APP |
| Depends on (build) | RWB-P4-AD008-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON, RWB-P4-E1022-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-008 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-AD008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **role owner**, I want **a list of every holder of my roles each review cycle, to confirm or remove**, so that **access is recertified on schedule**.

Inside `rwb-access` this is the recertification capability of the legacy story RWB-AD-008:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two provided operations, and nothing else: the review read `GET /api/recovery/access/v1/admin/access-reviews/{reviewId}`, which answers the cycle, its dates, the roles the caller owns and the holders of those roles with their confirmation state; and the decision write `POST /api/recovery/access/v1/admin/access-reviews/{reviewId}/decisions`, which confirms or removes one holder of one role with a reason, under `Idempotency-Key` and four eyes (the holder cannot confirm their own access).
- Consumed: `POST /api/recovery/access/v1/authorise` of RWB-P4-E1037-CON, with Platform administration R, answering the ADR refusal shape with MSG-P4-002; and, once per unconfirmed holder at the close, the ACE Common group membership removal path (INT-21). The `rwb-case` parameters contract and the `rwb-case` reference-data contract are not used: this story has no parameter row and no list to read (metadata "Contract dependencies" is None).
- The cycle is opened by one Temporal Schedule on queue `rwb-access` in namespace `rwb-recovery`, the legacy JOB-18 (six-monthly), and the same workflow closes it. Architecture v5 slide 14 gives `rwb-access` exactly this one Schedule. The Schedule is not in this story's metadata build list: it needs the workflow kit RWB-PLT-E1071-CON and that absence is carried (GAP-0807; ASM-1508).
- The role holders are the members of the role's Entra group, mapped by the `entra_group` column of `role` and read through this service's own SELECT-only ACE view `v_ace_iam_group` (DP-05). No person's name is stored or returned, only the staff user reference, and no e-mail address either.
- Data: `role`, `permission` and `role_conflict` are read in `rwb_access`, and the review cycle is kept in two tables of the same schema, `access_review` and `access_review_item`, created by this story's migration (GAP-0806; ASM-1507). `assignment` is P3's and `decision_log_entry` is P7's: neither is read and neither is written. The access entry of DP-03 is the local decision record of this service, so the access log and the decision log are one chain.
- Screens: SCR-43 Roles and access (list; access log) is the screen this capability feeds, served through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON). The review states open, decided and closed are answered by the two operations above.
- The legacy endpoints `GET /admin/roles` and `GET /admin/access-log` are not new work here: the roles read is the service's role administration (legacy RWB-AD-001) and the access-log read is RWB-P4-AD007-APP (legacy RWB-AD-007). This story adds the review read and the decision write and changes neither of them.

### 2. Business rationale

Access recertification is an audit finding and a bank IAM standard obligation: every six months each role owner has to see who holds their roles, confirm the ones that are still right and remove the ones that are not. Legacy RWB-AD-008 produced the holder lists with a Quartz job (JOB-18) over a joined read of `assignment`, `decision_log_entry` and `role`, and the confirmation lived in a screen. In the target the holders come from the Entra group the role is mapped to, the cycle is a Temporal Schedule in the owning service, and the confirmation is an access decision with a record — so the list, the decision and the removal request are one service's answer, and no operator re-runs a Quartz job to produce them.

This story meets REQ-ACA-002, REQ-ACA-011 and REQ-ACA-013 on the recertification side: roles are held as data and the holders are resolved from the group mapping with no code release (REQ-ACA-002, FEAT-ACA-13); a leaver who drops out of the group is dropped from the list and requested out at the close, within the same working day as the bank IAM standard requires (REQ-ACA-011, DL38); and the security administrator has the administration screen that shows roles, their holders and the access log behind one composite route (REQ-ACA-013, FEAT-ADM-14). It puts the control that CTL-10 expects within reach, and it makes the six-monthly review a fact of the service instead of a job nobody owns.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-AD008-CON (same service, its own contract story) | The published review contract: the review read and the decision write, the `AccessReview`, `AccessReviewHolder` and `AccessReviewDecision` schemas, the holder page, the role-owner scoping rule, the error envelope and the fakes this story builds against |
| RWB-P4-E1022-APP (same service, its own story) | Sign-on with Entra ID single sign-on and multi-factor authentication and the first roles (legacy RWB-E1-022): the signed-in staff user reference, the session and the resolved roles, which is what makes a caller a role owner. Without it the review read has no caller |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of every read, every decision, every refusal and every removal request |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19), which serves SCR-43 and merges the review read with the access-log read |
| RWB-PLT-E1071-CON, the workflow kit in namespace `rwb-recovery` | The Schedule, `AccessReviewWorkflow` and its two activities on queue `rwb-access`. This dependency is not in the metadata build list of the story and is carried as a gap (GAP-0807; ASM-1508) |
| The `v_ace_iam_group` view and its SELECT grant | The member list of the Entra group behind each role (DP-05; TSD P1 v3 T-A.1 view 30 with `entra_group`, `role_code`, `source_system` and `data_as_of`). The view is read only and is granted to this service's login; no ACE table is read |
| The `role`, `permission` and `role_conflict` tables in `rwb_access` | The role, its `entra_group`, its scope and its letters, from the service's role-to-permission baseline (legacy RWB-E1-037, RWB-P4-E1037-CON). This story reads them and creates none of them |

Business preconditions carried from RWB-AD-008:

- The review runs every six months. The interval is a bank IAM standard value and the Decision Log DL38 rules that placeholder values are loaded until it is supplied: "review every six months, leaver within the same working day, break-glass reviewed within one working day" (DL38).
- Legacy JOB-18 "Access review list — Produces role holder lists for recertification — Every six months — Depends on: None — If it fails or runs late: Rerun — Owner: Security administrator" (Batch and Scheduling Design v5, Jobs sheet).
- The role owners are RW-SECADM Security administrator and RW-PLATADM Platform administrator, which hold the A letter in Platform administration in TSD P4 v3 T6.1, and RW-COE for the reference-data roles (GAP-0809; ASM-1510). The security administrator is the operational owner of the job and is not the runtime identity of the Schedule: the activity runs as the service identity.
- A break-glass grant that is active puts MSG-P4-004 on every answer of the screen and writes its grant id on every entry (VR-P4-013-1, VR-P4-030-1). The grant itself is the service's break-glass story (legacy RWB-AD-006) and is not created here.

### 4. Flow

1. The Schedule `access-review` fires on the business date, six-monthly, on task queue `rwb-access` in namespace `rwb-recovery`, with overlap policy SKIP and the kit's catch-up window. It starts `AccessReviewWorkflow` with the business date as its input and the review id derived from the cycle (legacy JOB-18; DP-10).
2. `AccessReviewWorkflow` opens the cycle: one `access_review` row with the review id, the cycle code, `opened_on` (the business date), `closes_on` and state `OPEN`. A second firing for a cycle that already exists is a no-op, so a re-run of a failed Schedule never opens a duplicate (legacy "If it fails or runs late: Rerun").
3. The activity `BuildReviewList` reads the roles in `rwb_access`, joins each role to its `entra_group`, reads the members of that group through the SELECT-only view `v_ace_iam_group`, and writes one `access_review_item` row per holder per role with state `PENDING`. The row holds the staff user reference only: no name, no e-mail address and no identity number is copied, and `v_ace_iam_group` is read with `data_as_of` so the list states the freshness of the group read (DP-05).
4. A holder in the group with no role row, or a role with no `entra_group`, produces no item and is reported in the workflow's result as a count, not as a person. A role whose group cannot be read leaves its items unbuilt, the activity retries, and after the last retry the cycle stays `OPEN` with the role listed as unread and an incident is recorded.
5. The role owner opens SCR-43 through the gateway-bff composite route and the page calls `GET /api/recovery/access/v1/admin/access-reviews/{reviewId}`.
6. `AccessReviewController` validates the path and the query: `reviewId` must exist, and `page` and `size` must be numbers with `size` at most 200; an empty or malformed one is 422 with MSG-GEN-001 naming the field.
7. The handler asks `POST /api/recovery/access/v1/authorise` for Platform administration R. A caller without the right, and a caller with no Workbench role at all, is refused with 403 and MSG-P4-002 (or MSG-P4-001 for the absent role) and one entry with decision code `AC-DENY` is written before the refusal leaves the service.
8. The handler resolves the roles the caller owns: the roles in which the caller holds the A letter in Platform administration — RW-SECADM and RW-PLATADM, and RW-COE for the reference-data roles (GAP-0809; ASM-1510). Only those roles and only their holders are answered. A caller who owns no role in that review receives 403 with MSG-P4-002 and one `AC-DENY` entry, because a review the caller does not own is not readable.
9. The answer is the review header (review id, cycle code, `opened_on`, `closes_on`, state), the roles the caller owns, and for each role a page of holders with `holderUserReference`, the decision state, `decidedAt`, the reason code and the removal request reference. The holder list is paged with a default of 50 and a maximum of 200.
10. The role owner decides: the page posts `roleCode`, `holderUserReference`, `decision` (`CONFIRM` or `REMOVE`), `reasonCode` and `reason` to `POST /api/recovery/access/v1/admin/access-reviews/{reviewId}/decisions` with an `Idempotency-Key`.
11. `AccessReviewDecisionService` validates the request: the review must be `OPEN`, the role must be one the caller owns, the holder reference must be an item of that role in that review, and the decision, the reason code and the reason must be present; an absent field is 422 with MSG-GEN-001, an unknown review, role or holder is 404, and a decided item posted under a new key is 409 with MSG-GEN-004.
12. Four eyes: the caller's own staff user reference is compared with the holder reference. A holder who tries to confirm their own access is refused with 403 and MSG-P4-002, the item stays `PENDING` and one `AC-DENY` entry names the review, the role and the holder reference. A removal of the holder's own access is accepted, because a removal never grants access.
13. The decision is written in one transaction: the `access_review_item` row moves to `CONFIRMED` or `REMOVED` with `decidedAt`, the deciding user reference, the reason code and the reason; one decision-record entry is appended with decision code `AC-READ`, the review, the role, the holder reference, the decision and the reason code; and the outbox row is written by the same library (DP-03). Where the entry cannot be written the decision is not stored and the call fails with 503 and MSG-P7-003.
14. Idempotency: the same `Idempotency-Key` posted again returns the first answer unchanged and writes no second entry; a different key on an item that is no longer `PENDING` is 409 with MSG-GEN-004, so a double click never overwrites a decision (R-UNI-40).
15. An active break-glass grant puts MSG-P4-004 on the answer as a warning and its grant id on the entry, so the review record shows that a decision was taken while emergency access was on.
16. The close: on the close date, or when the operator closes the cycle through the kit's Schedule operations, `AccessReviewWorkflow` reads every item still `PENDING`. A holder with no decision by the close is not confirmed (GAP-0810; ASM-1511), the activity `RequestRemoval` posts one removal request per holder through the ACE Common group membership path (INT-21: sign-in and group-to-role), and one decision-record entry is written per removal request with the review, the role, the holder reference and the request reference.
17. A removal request that is accepted moves the item to `REMOVAL_REQUESTED` with the request reference; a request that fails leaves the item open, keeps it on the review, raises a follow-up task to the role owner and the security administrator on the review's own open-item list, and records an incident; the review is not closed while one item is open (GAP-0808; ASM-1509).
18. When every item is decided and every removal request is answered, the review moves to `CLOSED` and one `rwb.access.AccessPolicyChanged.v1` is published with the review id, the role codes, the counts of confirmed and removed holders and the change kind, and with no holder reference.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `reviewId`, `page` or `size` is empty or malformed | 422, no read is made and no entry is written | MSG-GEN-001 | AC3 |
| X2 | The caller holds no Platform administration R | 403 before the review is read, one `AC-DENY` entry | MSG-P4-002 | AC4 |
| X3 | The caller holds no Workbench role at all | 403, one `AC-DENY` entry | MSG-P4-001 | AC4 |
| X4 | The caller holds R but owns no role in the review | 403, no role and no holder is answered, one `AC-DENY` entry | MSG-P4-002 | AC3, AC4 |
| X5 | The review id is unknown | 404 with the envelope; no role is named | MSG-P4-002 (envelope `messageId`), no business text | AC3 |
| X6 | The role, or the holder reference, is not an item of that review | 404 with the envelope; no decision is stored | MSG-P4-002 (envelope `messageId`), no business text | AC4 |
| X7 | The holder confirms their own access | 403, the item stays `PENDING`, one `AC-DENY` entry | MSG-P4-002 | AC4 |
| X8 | The item is already decided and a new key posts another decision | 409 with the envelope; the first decision stands | MSG-GEN-004 | AC4 |
| X9 | The review is closed and a decision arrives | 409 with the envelope; nothing is stored | MSG-GEN-004 | AC4 |
| X10 | The decision-record entry cannot be written | 503 and no decision is stored; the item stays as it was | MSG-P7-003 | AC5, TC-AD-008-04 |
| X11 | A removal request fails at the close | The item stays open, a follow-up task is raised and an incident is recorded; the review stays `OPEN` | MSG-GEN-004 (envelope), the incident carries the failure | AC5 |
| X12 | The Entra group of a role cannot be read | `BuildReviewList` retries; after the last retry the cycle stays `OPEN` with the role listed as unread and an incident is recorded; no item is invented | None | AC1, AC5 |
| X13 | A break-glass grant is active | The answer carries the warning and every entry carries the grant id | MSG-P4-004 | AC3 |

No exception path of this story changes a case, a task or an approval: this service opens a review, records decisions and requests removals, and the case state machine stays `rwb-case`'s and the approval `rwb-decision`'s.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the review contract of RWB-P4-AD008-CON and its fakes, the decision-record library and the gateway-bff route; it reads `role`, `permission` and `role_conflict` in its own schema and the `v_ace_iam_group` view only |
| Negotiable | The interval is a bank IAM standard value (DL38 placeholder until supplied), the reason codes are the contract's enumerated values, and the role-owner rule is a stated target-service rule — none of them is fixed in this story's code |
| Valuable | One read and one decision replace a Quartz job, a per-screen join and a manual removal e-mail; the recertification becomes a recorded act of the service |
| Estimable | Two operations, one workflow with two activities, one migration of two tables, one group reader, one record writer, one contract-fake run |
| Small | Fits two weeks with its tests; the three reference tables and the screens are other stories' |
| Testable | Each owned criterion has a test case in section 16, and the Schedule, the group read and the removal request are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Access review list

  Background:
    Given the environment is SIT
    Given the service is rwb-access on queue rwb-access in namespace rwb-recovery
    Given test user "U-4101" holds RW-SECADM with the A letter in Platform administration and owns role "RW-CASEOWN"
    Given test user "U-4102" holds RW-PLATADM with the A letter in Platform administration, owns role "RW-TEAMMGR" and is also a holder of "RW-TEAMMGR"
    Given test user "U-4103" holds RW-AUDIT with the R letter only in Platform administration
    Given the review interval is the DL38 placeholder value of six months until SCB IT security supplies the bank IAM standard value

  Scenario: AC1 List produced (legacy RWB-AD-008 AC1)
    Given the review date
    Given the rwb-access contract mock returns review "AR-2027-H1" opened on 4 January 2027 with 12 role owners and their holders
    When the review opens
    Then each role owner receives the holders of their roles

  Scenario: AC2 Not confirmed (legacy RWB-AD-008 AC2)
    Given a holder not confirmed by the end of the review
    Given the bank IAM contract mock returns removal request "IAM-REM-0007" accepted for holder "U-4105"
    When the review closes
    Then the system requests removal through the bank IAM and logged

  Scenario: AC3 A role owner sees only the roles they own, and no holder name (new, D-RCV-60)
    Given review "AR-2027-H1" is open with role "RW-CASEOWN" owned by "U-4101" and role "RW-TEAMMGR" owned by "U-4102", each with its holders
    When "U-4101" calls GET /api/recovery/access/v1/admin/access-reviews/AR-2027-H1
    Then the response is 200 with the cycle code, openedOn 4 January 2027, closesOn and state "OPEN"
    Then the answer names role "RW-CASEOWN" only, and no holder of "RW-TEAMMGR" is returned
    Then each holder is a staff user reference such as "U-4105" with its decision state, its decidedAt and its reason code, and no holder name, no e-mail address and no identity number is returned
    Then the holder page carries page, size and total with size at most 200
    Then one decision-record entry is written with decision code "AC-READ", the review, the role count and the time

  Scenario: AC4 A holder cannot confirm their own access, and a caller without the right is refused (new, D-RCV-60)
    Given review "AR-2027-H1" is open and "U-4102" is a holder of role "RW-TEAMMGR" which "U-4102" owns
    When "U-4102" posts decision "CONFIRM" for holder "U-4102" on role "RW-TEAMMGR" with a reason code and a reason
    Then the response is 403 with message MSG-P4-002 and the item stays "PENDING"
    Then one decision-record entry is written with decision code "AC-DENY", the review, the role and the holder reference, and no decision is stored
    When "U-4103" holds only the R letter and owns no role, and calls GET /api/recovery/access/v1/admin/access-reviews/AR-2027-H1
    Then the response is 403 with message MSG-P4-002 and no role and no holder is answered
    Then one decision-record entry is written with decision code "AC-DENY" naming the reader and the review
    When "U-4102" posts the same decision again with the same Idempotency-Key
    Then the first answer returns unchanged and no second entry is written
    When "U-4102" posts a different decision for that holder with a new Idempotency-Key
    Then the response is 409 with message MSG-GEN-004 and the first decision stands

  Scenario: AC5 The six-monthly Schedule opens the review, and a failed removal leaves the item open (new, D-RCV-60)
    Given the Schedule "access-review" is in force on queue rwb-access in namespace rwb-recovery with overlap policy SKIP and the DL38 interval of six months
    When the Schedule fires on business date 7 July 2027
    Then AccessReviewWorkflow opens review "AR-2027-H2" with state "OPEN" and openedOn 7 July 2027, and one access_review_item is written per holder per role with state "PENDING"
    Then a second firing for the same cycle opens no second review
    When the review is closed with three holders still "PENDING"
    Then one removal request is posted per holder through the ACE Common group membership path and one decision-record entry is written per removal request
    Then the three items move to "REMOVAL_REQUESTED" and one "rwb.access.AccessPolicyChanged.v1" is published with the review, the role codes and the counts, and with no holder reference
    When one of the three removal requests fails
    Then that item stays open with the failure reason, a follow-up task is raised to the role owner and the security administrator, and an incident is recorded
    Then the review stays "OPEN" while an item is open and the two accepted requests keep their reference
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The review cycle runs every six months on the business date, as a Temporal Schedule on queue `rwb-access` in namespace `rwb-recovery`; a second firing of the same cycle opens no second review | JOB-18; Arch v5 slides 14 and 44; DL38; DP-10 |
| BR2 | One `access_review_item` exists per holder per role per cycle; a holder is a member of the role's Entra group, mapped by `role.entra_group` and read through `v_ace_iam_group`; only the staff user reference is stored | FEAT-ACA-13; FSD P4 v3 A2.13; TSD P4 v3 T3.1 DF-REF-039; DP-05 |
| BR3 | The review read and the decision write need Platform administration R | Legacy RWB-AD-008 permission checks; TSD P4 v3 T6.1 |
| BR4 | A role owner sees only the roles they own: the A letter in Platform administration for the role (RW-SECADM, RW-PLATADM) and RW-COE for the reference-data roles. A caller who owns no role in the review is refused | GAP-0809; ASM-1510; TSD P4 v3 T6.1 |
| BR5 | Four eyes: the holder cannot confirm their own access; a refusal is MSG-P4-002 with one `AC-DENY` entry. A removal of one's own access is accepted, because removal never grants access | FSD P4 v3 A2.13 and A2.30; TSD P4 v3 T4 (a second person approves) |
| BR6 | Every decision and every removal request appends one decision-record entry in the same transaction; an answer that cannot be recorded is not returned | R-UNI-39; Principle 5; FSD P4 v3 A2.13 AC-EXC-P4-013-07 |
| BR7 | The same `Idempotency-Key` returns the first answer and writes no second entry; a different key on a decided item is 409 MSG-GEN-004 | R-UNI-40; Arch v5 slide 11 |
| BR8 | A holder with no decision by the close is not confirmed, and its removal is requested through the bank IAM, within the same working day as the bank IAM standard requires | Legacy RWB-AD-008 AC2; DL38; GAP-0810; ASM-1511 |
| BR9 | A removal request that fails leaves the item open with a task and an incident, and the review does not close over an open item | GAP-0808; ASM-1509; R-UNI-39 |
| BR10 | No personal data: no holder name, e-mail address or identity number is stored, returned, logged or published; the answer carries the staff user reference and the decision state only | Guardrails; FSD P4 v3 A2.13 field catalog; REQ-ACA-005 |
| BR11 | No business value in code: the interval is the Schedule's configuration under DL38 and the reason codes are the contract's enumerated values, so neither is a Java constant | BR-P4-013; BR-P4-030; DL38 |
| BR12 | While a break-glass grant is active the answer carries MSG-P4-004 and every entry carries the grant id | VR-P4-013-1; VR-P4-030-1; REQ-ACA-008 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1 is the kit's Schedule, not a shared Quartz row: one Schedule ID, the six-monthly cron of the deployment, overlap policy SKIP and the catch-up window, and the workflow-id is the review id, so a re-run of a failed firing cannot open a second cycle (legacy "If it fails or runs late: Rerun").
- BR2 is one query over `role`, `permission` and `role_conflict` in `rwb_access` plus one read of `v_ace_iam_group` per role; the group read is a SELECT on a granted view and never a join to an ACE table, and `data_as_of` is carried so the list states the freshness of the group mapping.
- BR3 and BR4 are two answers from one authorise call and one local read: the right is the authorise answer of RWB-P4-E1037-CON and the ownership is the A letter of the caller in Platform administration, so a caller with R only cannot see a list of holders even though the legacy permission row carries R.
- BR5 is a comparison of two references — the caller's and the holder's — before the handler runs, so the refusal costs no write.
- BR6 is the record appender of DP-03 inside the transaction that writes the item, with the outbox row; the decision is committed with its entry or not at all.
- BR7 is the idempotency table of the library: the stored answer is returned for the same key, and the item's own state is the guard for a second key.
- BR8 and BR9 are the close step: the item states are the ledger of the close, and a review closes only when no item is `PENDING` or open.
- BR10 is a property of the schema as much as of the code: `access_review_item` has no column for a name, so no code path can store one.
- BR11 is checked by test: a new reason code is a contract enumeration value and a new interval is the Schedule's configuration, and the build changes nothing.
- BR12 is the grant reader of the service's break-glass story, read at the start of the transaction and written on every entry.

### 9. State transitions

The review and its items are the only states this service holds.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The Schedule fires on the business date | No review exists for the cycle | `OPEN`, items built |
| `OPEN` | The same cycle fires again | A review already exists | `OPEN`, unchanged, no second review and no second item |
| `OPEN` | The role owner confirms a holder | The caller owns the role and is not the holder | `OPEN`, the item `CONFIRMED` |
| `OPEN` | The role owner removes a holder | The caller owns the role, with a reason | `OPEN`, the item `REMOVED` |
| `OPEN` | The close runs | Items are `PENDING` | `OPEN`, each item `REMOVAL_REQUESTED` after its request is accepted |
| `OPEN` | A removal request fails | None | `OPEN`, the item open with its failure reason, a task and an incident |
| `OPEN` | The close runs | No item is `PENDING` or open | `CLOSED`, one `AccessPolicyChanged` |

| Command | Condition | Outcome |
|---|---|---|
| Confirm a holder | The caller owns the role and is not the holder | 200, item `CONFIRMED`, one `AC-READ` entry |
| Confirm own access | The caller is the holder | 403, MSG-P4-002, item unchanged, one `AC-DENY` entry |
| Remove a holder | The caller owns the role, with a reason | 200, item `REMOVED`, one `AC-READ` entry |
| Decide again with the same key | The first answer exists | 200, the stored answer, no new entry |
| Decide again with a new key | The item is not `PENDING` | 409, MSG-GEN-004, item unchanged |
| Decide on a closed review | The review is `CLOSED` | 409, MSG-GEN-004, nothing stored |

No case, task or approval state is held or changed here: the follow-up task of a failed removal sits on the review's own open-item list and is not a `rwb-case` task, because this story carries no `rwb-case` dependency.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SECADM Security administrator | Owns the roles in which it holds the A letter in Platform administration; reads the review and confirms or removes a holder of those roles. It is also the operational owner of the job (Batch and Scheduling Design v5) |
| RW-PLATADM Platform administrator | The same, for the roles in which it holds the A letter (CRUD in Platform administration in TSD P4 v3 T6.1) |
| RW-COE Center of excellence analyst | The same, for the reference-data roles, as the owner of the policy data (GAP-0809; ASM-1510) |
| RW-AUDIT Internal audit, RW-COMPLY, RW-DATASTEW | Hold Platform administration R and read the review only if they own a role in it; they hold no A letter in Platform administration and are refused with MSG-P4-002 when they own none |
| The `rwb-access` service identity of the Schedule | Opens the cycle, builds the list, posts the removal requests and closes the review, on queue `rwb-access` in namespace `rwb-recovery`. It holds no user right and acts as the service, not as the security administrator |
| ACE Common (INT-21) | Receives one group membership removal request per holder at the close. It owns the sign-in and the group-to-role mapping and answers whether the request was accepted |
| `rwb-access` itself | Reads `role`, `permission`, `role_conflict` and `v_ace_iam_group` and writes `access_review` and `access_review_item` in its own schema |

The refusal shape is 403 with an RFC 9457 problem response and `messageId` set: MSG-P4-001 for a caller with no Workbench role, MSG-P4-002 for an absent right or a review the caller does not own, and MSG-P4-002 again for the self-confirmation. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E1037-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, `entra_group` | Read |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | id, role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read |
| DF-ACE-301 to DF-ACE-304 | `v_ace_iam_group` (this service's granted ACE view) | entra_group, role_code, source_system, data_as_of | Read |
| Not specified in the source documents (GAP-0806; ASM-1507) | `access_review` (new, this story's migration) | review_id, cycle_code, opened_on, closes_on, state, created_at, created_by | Write, read |
| Not specified in the source documents (GAP-0806; ASM-1507) | `access_review_item` (new, this story's migration) | review_id, role_code, holder_user_reference, decision_state, decision, reason_code, reason, decided_at, decided_by_user_reference, removal_request_ref, removal_requested_at, failure_reason | Write, read |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the access entry of a read, a decision, a refusal and a removal request, with the break-glass grant id where a grant is active | Write |
| (outbox) | outbox library table in `rwb_access` | the record row and the `AccessPolicyChanged` row | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |

`access_review` and `access_review_item` are new tables of this story's own schema, so their field IDs are Not specified in the source documents (GAP-0806; ASM-1507); the columns above are the ones the two operations need and the contract review confirms or renames them before the endpoint is frozen. No row of `assignment` is read: the holders are the group members, not the case assignments, and `assignment` is P3's. No row of `decision_log_entry` is read or written: it is P7's, and the entry of this story is the local decision record of DP-03 (DP-01). `partner_user` is S9's and is not read. No foreign key crosses a schema.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/admin/access-reviews/{reviewId}` | P4 `rwb-access` | Path: `reviewId`. Query: `roleCode`, `state`, `page`, `size` (default 50, max 200) | `reviewId`, `cycleCode`, `openedOn`, `closesOn`, `state` (OPEN, CLOSED); `roles[]` with `roleCode`, `roleName`, and a holder page of `holderUserReference`, `decisionState`, `decidedAt`, `reasonCode`, `removalRequestRef`; `page`, `size`, `total` | 401; 403 Platform administration R and role ownership (MSG-P4-002, MSG-P4-001 for an absent role); 404 unknown review (envelope); 422 malformed query (MSG-GEN-001); 503 record not written (MSG-P7-003) | Platform administration R, then the A letter in Platform administration for each role returned | Not applicable, read only; no `Idempotency-Key` |
| POST | `/api/recovery/access/v1/admin/access-reviews/{reviewId}/decisions` | P4 `rwb-access` | Path: `reviewId`. Body: `roleCode`, `holderUserReference`, `decision` (CONFIRM, REMOVE), `reasonCode`, `reason`. Header: `Idempotency-Key` | `reviewId`, `roleCode`, `holderUserReference`, `decision`, `decidedAt`, `decisionRecordEntryRef`, `removalRequestRef` where the decision is REMOVE | 401; 403 not the role owner, or the holder confirming their own access (MSG-P4-002); 404 unknown review, role or holder (envelope); 409 item already decided or review closed (MSG-GEN-004); 422 missing or invalid field (MSG-GEN-001); 503 record not written (MSG-P7-003) | Platform administration R, and the A letter in Platform administration for that role | `Idempotency-Key` required; the stored answer is returned for the same key |

The two operations sit under the base `/api/recovery/access/v1` of DP-13 and are the contract of RWB-P4-AD008-CON; they are absent from Recovery Workbench API Specification v4, which carries `GET /admin/roles` and `GET /admin/access-log` for this service and no review path, so the contract story publishes them. The legacy endpoints `GET /admin/roles` (API-P4-007, Platform administration R) and `GET /admin/access-log` (API-P4-008) keep their owners and their rights and are not changed by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access`, published by RWB-P4-E1037-CON | Platform administration R, and the A letter of the caller in Platform administration, behind both operations. One hop and a 2 s client budget; the answer is cached for the request |
| POST | ACE Common group membership removal (INT-21) | ACE Common, the bank IAM entry point | One removal request per holder at the close, on the sign-in and group-to-role path; the answer says whether the request was accepted. The request and answer shapes are Not specified in the source documents (GAP-0808; ASM-1509) |

The `rwb-case` parameters contract (DP-06) and reference-data contract (DP-07) are not consumed: this story has no parameter row, no list of values and no reason code held as reference data — the reason codes are the contract's enumerated values. `assignment` of `rwb-case` is not read, and `decision_log_entry` of `rwb-decision` is not read.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | `reviewId` | The review, the role codes whose access changed, the counts of confirmed and removed holders and the change kind, with no holder reference and no personal field |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | `entryId` | The hash-chained access entry of a read, a decision, a refusal or a removal request |

CloudEvents 1.0 envelope; neither payload carries a name, an e-mail address, an identity number or a staff user reference. `rwb.access.DoaLimitChanged.v1` is not published here: the DoA table is RWB-P4-E1038-APP's.

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 (events: none), and this story adds no subscription. The joiner and leaver changes of REQ-ACA-011 reach the list through the Entra group membership read on the ACE view, not through an event of this service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Element |
|---|---|---|---|
| `AccessReviewWorkflow` | Workflow, workflow ID = review id | `rwb-access` | Input business date and cycle; opens the review, runs the build, runs the close, holds the review state; search attributes ReviewId and CycleCode |
| `BuildReviewList` | Activity (workflow kit) | `rwb-access` | The roles of `rwb_access`, the group read through `v_ace_iam_group` and the one `access_review_item` per holder per role; retried, and reported as a count when a group cannot be read |
| `RequestRemoval` | Activity (workflow kit) | `rwb-access` | One removal request per unconfirmed holder through the ACE Common path, and one decision-record entry per request; a failed request leaves the item open with its reason |

#### 12.6 Schedules

| Schedule | Cadence | Overlap policy | Owner | Starts |
|---|---|---|---|---|
| `access-review` | Six-monthly, Asia/Bangkok, on the business date (DL38 placeholder value until SCB IT security supplies the bank IAM standard value) | SKIP, with the kit's catch-up window | P4 `rwb-access`, on queue `rwb-access` in namespace `rwb-recovery` | `AccessReviewWorkflow` with the business date, which opens the cycle (legacy JOB-18) |

This is the only Schedule of `rwb-access` (Architecture v5 slide 14). It runs on the workflow kit RWB-PLT-E1071-CON, and that dependency is not in this story's metadata build list (GAP-0807; ASM-1508): the kit is a precondition of the Schedule and the metadata is corrected at the contract review. The exact month, day and hour of the cron are the deployment's configuration and are Not specified in the source documents (GAP-0807; ASM-1508); the interval itself is DL38.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read: the role, its `entra_group` and its class. Created by the service's role baseline |
| `permission` | P4 (`rwb_access`) | Read: the letters of the caller's roles, so the ownership test is made on rows |
| `role_conflict` | P4 (`rwb_access`) | Read: a pair of roles one person may not hold together, listed to the role owner of both roles |
| `access_review` | P4 (`rwb_access`) | Read and write: one row per cycle, created by this story's migration |
| `access_review_item` | P4 (`rwb_access`) | Read and write: one row per holder per role per cycle, created by this story's migration |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the record and of `AccessPolicyChanged`, and the stored decision answer of the idempotency key; no inbox row is written because no event is consumed |
| `assignment` | P3 (`rwb_case`) | Not read and not written: the holders are group members, not case assignments (DP-01) |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the local decision record of DP-03 is the entry |

No table of another service is read and no foreign key crosses a schema (DP-01). `v_ace_iam_group` is a granted, SELECT-only view of this service and not a table of another service.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access access-review WireMock | RWB-P4-AD008-CON | Review "AR-2027-H1" opened on 4 January 2027 with 12 role owners and their holders (AC1); review "AR-2027-H2" for the Schedule run of 7 July 2027 (AC5); the holder page of role "RW-CASEOWN"; the 409 for a decided item and the 422 for a missing reason |
| bank IAM removal fake | RWB-P4-AD008-CON, ACE Common path | Removal request "IAM-REM-0007" accepted for holder "U-4105" (AC2); one request refused for the failed-removal case of AC5 |
| decision-record fake | RWB-PLT-E1027-CON | The record append, the hash-chain check and the forced failure of TC-AD-008-04 |
| authorise and guard fake | RWB-P4-E1037-CON | The Platform administration R answer for RW-SECADM, RW-PLATADM and RW-COE, and the refusal with MSG-P4-002 for RW-AUDIT when it owns no role, and MSG-P4-001 for a caller with no role |
| gateway-bff composite fake | RWB-PLT-N001-CON | The SCR-43 composite answer that merges the review read with the access-log read of RWB-P4-AD007-APP |
| group directory fixture | RWB-P4-E1022-APP and the SIT sandbox | Entra group "ACE-RWB-CASEOWN" with the holder references of role "RW-CASEOWN", and a role whose group cannot be read for X12. No name and no e-mail address in the fixture |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (`GET /admin/access-reviews/{reviewId}`, `POST /admin/access-reviews/{reviewId}/decisions`); consumed 2 | Base `/api/recovery/access/v1`; the authorise operation of the same service and the ACE Common removal path, one hop and 2 s |
| Kafka | Published 2 event types; consumed 0 | `rwb.access.events.v1` and `rwb.decision-record.v1` |
| Temporal | 1 workflow, 2 activities, 1 Schedule | `AccessReviewWorkflow`, `BuildReviewList`, `RequestRemoval`, the `access-review` Schedule on queue `rwb-access` |
| File | None | No file input or output; the removal request is a REST call and not a file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/review`, Java package `th.co.scb.ace.workbench.recovery.access.review`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the local `DecisionLogWriter` of the monolith (DP-03: the entry of every read, decision, refusal and removal request is a record on `rwb.decision-record.v1`), the `AceSourceQuery` read of `iam_group` (DP-05: the service reads its own SELECT-only `v_ace_iam_group` view), the monolith base `/api/recovery/v1` (DP-13), and the `ace-web` screen SCR-43 (DP-19: the gateway-bff composite route).

One pattern of the table is carried by the legacy key and is **not** in this story's pattern row: DP-10 (`Quartz, JOB-nn` → a Temporal Schedule through the workflow kit). JOB-18 is the service's one Schedule and it needs the kit RWB-PLT-E1071-CON, which the metadata build list does not carry; the absence is a gap and an assumption, and the metadata is corrected at the contract review (GAP-0807; ASM-1508). The Schedule is deployed by the operations story of this legacy key.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AccessReviewController | Controller | The two operations: path and query validation, RFC 9457 problem responses, `messageId` mapping, `requiredLevel`-free refusals with MSG-P4-002 |
| AccessReviewQueryService | Service | BR3 and BR4: the authorise answer, the roles the caller owns, the holder page, and the refusal of a review the caller does not own |
| AccessReviewDecisionService | Service | BR5, BR6 and BR7: the four-eyes test, the reason, the idempotent answer and the item state |
| AccessReviewRepository | Repository | `access_review` and `access_review_item`, with the unique key on review, role and holder reference and the item state machine |
| HolderDirectoryReader | Service | BR2: the `entra_group` of each role and the members of that group through `v_ace_iam_group`, with `data_as_of`; no name is selected |
| RoleOwnershipReader | Service | BR4: the A letter in Platform administration of the caller, per role, read from `permission` |
| AccessRecordWriter | Service | BR6 and BR12: one decision-record entry per read, decision, refusal and removal request, with the break-glass grant id, in the transaction with the outbox row |
| AuthoriseClient | Client | `POST /api/recovery/access/v1/authorise` of RWB-P4-E1037-CON: one hop, 2 s, cached per request |
| AceGroupMembershipClient | Client | The removal request through the ACE Common path (INT-21), one per holder at the close |
| AccessReviewWorkflow, BuildReviewListActivity, RequestRemovalActivity | Temporal | BR1, BR8 and BR9: the open, the list build, the close and the per-holder removal request |

**Database and migrations**

- This story owns one Flyway version in the per-service sequence of the service baseline. It creates `access_review` and `access_review_item` in `rwb_access` (GAP-0806; ASM-1507).
- `access_review` carries the review id, the cycle code, `opened_on`, `closes_on`, the state and the audit columns; a unique key on the cycle code stops a second review for one cycle.
- `access_review_item` carries the review, the role, the holder reference, the decision state, the decision, the reason code, the reason, the deciding reference, the decision time, the removal request reference and the failure reason; a unique key on review, role and holder reference stops a duplicate item, and there is no column for a name, an e-mail address or an identity number (BR10).
- The item state is `PENDING`, `CONFIRMED`, `REMOVED` or `REMOVAL_REQUESTED`; the check constraint admits no other value, so a partially decided item cannot be stored.
- No row of `role`, `permission` or `role_conflict` is written: those tables belong to the service's role baseline and this story's repository has no write method for them.

**Configuration and reference data**

- The interval is the Schedule's configuration: six-monthly, Asia/Bangkok, overlap policy SKIP and the kit's catch-up window, under the DL38 placeholder value until SCB IT security supplies the bank IAM standard value. The cron is a deployment value and not a Java constant (BR11).
- The reason codes are the contract's enumerated values of RWB-P4-AD008-CON; there is no reference list to read for them, which is why DP-07 is not applied.
- The role-owner rule is a property of the `permission` rows: the A letter in Platform administration, plus the RW-COE exception for the reference-data roles (GAP-0809; ASM-1510). No role code is a constant in the ownership test.
- The ACE view and its grant are the service's own: `v_ace_iam_group` is created and granted by the service's ACE view story and read here with `data_as_of` (DP-05).

**Build steps**

1. The migration of `access_review` and `access_review_item` with their unique keys and the state check; a test that a duplicate item and an unknown state are refused.
2. `HolderDirectoryReader` over `role.entra_group` and `v_ace_iam_group`, with `data_as_of`; a test that the reader selects no name and no e-mail column.
3. `AccessReviewWorkflow` with the open, the idempotent re-fire and the `BuildReviewList` activity; tests for AC1 and for the double firing of AC5.
4. `AccessReviewQueryService` with the authorise call and the ownership filter; tests for AC3 and for the R-only refusal of AC4.
5. `AccessReviewDecisionService` with the four-eyes test, the reason, the item state and the idempotent answer; tests for AC4 and for the 409 of a second key.
6. `AccessRecordWriter` with the entry and the outbox row in one transaction, and the break-glass grant id; tests for TC-AD-008-04 and for BR12.
7. `RequestRemovalActivity` with one request per unconfirmed holder and the failure path that leaves the item open with its task and its incident; tests for AC2 and AC5.
8. The contract-fake run of both operations against RWB-P4-AD008-CON, the composite-route run of SCR-43 against RWB-PLT-N001-CON, and the Schedule test on a fixed clock.

**Feature switch.** The two operations carry no switch of their own. The operational control is the kit's Schedule operation: the `access-review` Schedule can be paused, resumed and back-filled, and a paused Schedule leaves an open review open rather than closing it, so no review is ever closed by a pause. The service-level feature flag of RWB-P4-E1037-CON governs the service baseline and is not changed here.

**Done when.** The tests in section 16 pass; the review of AC1 is read by its role owner with its holders and no name; a self-confirmation is refused with MSG-P4-002 and one `AC-DENY` entry; the Schedule of AC5 opens a review on the business date and a close writes one removal request and one entry per unconfirmed holder; a failed removal leaves the item open with its task; and every read, decision, refusal and removal request leaves one entry in the decision record chain.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-004 | A break-glass grant is active | Emergency access is on until {time}. Every action is recorded. | This story, on both operations, as a warning with the grant id on the entry |
| MSG-P4-001 | The caller holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Platform administration R, owns no role in the review, or confirms their own access | You cannot {action} here. Your role does not include it. | This story, on both operations |
| MSG-GEN-001 | A required field is empty or a query value is malformed | Enter {field}. | This story, on both operations |
| MSG-GEN-004 | The item is already decided under another key, or the review is closed | Someone else changed this record. Reload it to see their change. | This story, on the decision write and on a failed removal request |
| MSG-P7-003 | The decision-record entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are the legacy texts of RWB-AD-008, copied unchanged.

### 15. Screens and states

SCR-43 Roles and access is built by this capability and served through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), which calls the review read and the access-log read of RWB-P4-AD007-APP in parallel, one hop each, and merges the answers.

| Screen | State | What the answer decides |
|---|---|---|
| SCR-43 Roles and access | List, open review | The cycle, its dates and the roles the caller owns, each with its holders and their decision state; the role owner confirms or removes |
| SCR-43 Roles and access | Decided | Every item of the review is decided and a removal request may still be outstanding; the item shows its decision, its reason code and its request reference |
| SCR-43 Roles and access | Closed | Every item is decided and every request is answered; the review is read only and a decision is refused with MSG-GEN-004 |
| SCR-43 Roles and access | Access log | The decision-record entries of the review, read through the access-log operation of RWB-P4-AD007-APP; the review read supplies no log row of its own |
| SCR-43 Roles and access | Refused | The page shows MSG-P4-002 with no role and no holder, and one `AC-DENY` entry exists |
| SCR-43 Roles and access | Failed to record | The page shows MSG-P7-003 and no decision stands |
| SCR-43 Roles and access | Break-glass warning | MSG-P4-004 is shown above the list while a grant is active, and each entry carries the grant id |
| SCR-41 Delegation of authority | Versions; load; approval | Not this story: the DoA table is RWB-P4-E1038-APP's and this page reads none of it |

The screen field list, the column order and the masking of customer fields on the composite page are Not specified in the source documents (GAP-0806; ASM-1507); this story fixes the review side of the merge only, and no holder name reaches the page because the answer carries no name.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-008-01 | AC1, BR1, BR2 | Component | Review "AR-2027-H1" opened on 4 January 2027 with 12 role owners and their holders; one role with two holders; a role whose group cannot be read |
| TC-AD-008-02 | AC2, BR8 | Component | A close with two holders still `PENDING`; removal request "IAM-REM-0007" accepted for holder "U-4105" and one request refused |
| TC-AD-008-03 | AC4, BR3, BR5, BR7 | Component | Self-confirmation by "U-4102"; RW-AUDIT "U-4103" with R only; the same key replayed and a second key on a decided item |
| TC-AD-008-04 | BR6, BR9 | NFR | The decision-record write forced to fail on a decision and at the close |
| TC-AD-008-05 | AC3, BR4, BR10 | Component | The review read by its owner and by a caller who owns another role; the answer checked for a name, an e-mail address and an identity number |
| TC-AD-008-06 | AC5, BR1, BR8, BR9 | Component | The Schedule on 7 July 2027, a second firing of the same cycle, and a removal request that fails |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. TC-AD-008-01 to TC-AD-008-04 are the legacy test cases of RWB-AD-008, kept with their IDs; their legacy "System" level maps to Component and "Resilience" to NFR. TC-AD-008-05 and TC-AD-008-06 are new for the new criteria. The ITG copy of the whole set is RWB-ITG-AD008-ITG and is not written here, so no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the interval is the Schedule's configuration under DL38 and the reason codes are the contract's enumerated values; a test proves that a new reason code or a new interval needs no build (BR11).
- No personal data anywhere: `access_review_item` has no column for a name, an e-mail address or an identity number, and neither the answer, nor the entry, nor the `AccessPolicyChanged` payload carries one (BR10).
- No read of another service's tables (DP-01): `assignment` is P3's and `decision_log_entry` is P7's, and no foreign key crosses a schema. The holders come from the group mapping, not from the case assignment.
- ACE data only through the owner's contract or the service's own `v_ace_*` views: the group membership is read through the granted, SELECT-only `v_ace_iam_group`, with `data_as_of` stated (DP-05).
- One writer per table: this story writes `access_review`, `access_review_item` and the library tables of its own schema and nothing else; `role`, `permission` and `role_conflict` are read through a repository with no write method.
- No answer without its record: the entry commits with the decision, and the decision is withheld with MSG-P7-003 when it cannot be written (BR6).
- Four eyes is enforced in the service, not in the screen: the client cannot talk its way past the comparison of the two staff user references (BR5).
- The Schedule has one ID and one cycle: a second Schedule or a second review for the same cycle fails the review, because a double cycle would request removals twice (BR1).
- A refused caller learns nothing of the holders: the refusal carries the message and the decision code and no role, no holder and no count.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-002 | Roles are held as data and a role change takes effect without a code release | Program BRD, Epic 1 | FEAT-ACA-13 | 16 Manage risk, control and compliance | BR2, BR11 | TC-AD-008-01, TC-AD-008-05 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench so access matches the organization | Program BRD, Epic 2 | FEAT-ACA-13 | 16 Manage risk, control and compliance | BR1, BR2, BR8 | TC-AD-008-01, TC-AD-008-02, TC-AD-008-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Program BRD, Epic 8 | FEAT-ADM-14 | 16 Manage risk, control and compliance | BR3, BR4, BR10 | TC-AD-008-03, TC-AD-008-05 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy AC1 "List produced" and AC2 "Not confirmed" | Section 7, tests TC-AD-008-01 and TC-AD-008-02 |
| JOB-18, six-monthly, owner security administrator, "If it fails or runs late: Rerun" | Sections 1, 3, 4, 12.5, 12.6, 13 |
| DL38 placeholder values: review every six months, leaver within the same working day, break-glass review within one working day | Sections 3, 8, 13, 14 |
| MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-004, MSG-P7-003 | Section 14, exception paths |
| Screens SCR-43 and SCR-41 | Section 15 |
| Legacy endpoints `GET /admin/roles` and `GET /admin/access-log` | Sections 1, 12.1 |
| Permission check Platform administration R, roles RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Sections 8, 10 |
| Rules R-UNI-39, R-UNI-40, CTL-10, and the INT-21 ACE path | Sections 2, 8, 12.2, 17 |
| Field IDs DF-REF-034 to DF-REF-039, DF-REF-040 to DF-REF-044, DF-REF-205 to DF-REF-211, DF-ACE-301 to DF-ACE-304 | Section 11 |
| Legacy key RWB-AD-008, story RWB-P4-AD008-APP, contract RWB-P4-AD008-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The contract itself — the OpenAPI 3.1 document, the schemas, the role-owner scoping rule, the error envelope and the fakes — which is RWB-P4-AD008-CON.
- The roles read `GET /admin/roles` and the role and group mapping (legacy RWB-AD-001), and the access-log search and export (RWB-P4-AD007-APP, legacy RWB-AD-007). This story adds two operations and changes neither.
- The break-glass grant itself and its review (legacy RWB-AD-006): this story reads the active grant and writes its id on every entry.
- The role-to-permission matrix load and approval, the scope per role and the masking profiles (the service's role baseline and the reference-load stories of this legacy set).
- The case task and the case state: a failed removal raises a follow-up task on the review's own open-item list, and no `rwb-case` task and no `rwb-case` dependency is claimed.
- The delegation of authority table and the SCR-41 page (RWB-P4-E1038-APP).
- The `rwb-decision` slice that reads the entries: the central ledger, its hash-chain check and the audit query are P7's.
- The `partner_user` of S9 and the partner portal: no partner user is reviewed here.
- The deployment of the Schedule, its cron, its catch-up window, the Helm values, the alerts and the runbook (the operations story of this legacy key and the platform kit story RWB-PLT-E1071-CON).
- The integration harness RWB-ITG-AD008-ITG and the `-ITG` copies of the test cases.
