# RWB-P4-E2008-APP Payment matching with the missed payment event

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E2008-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P4-AH |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-P4-E2008-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2008-CON; RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-CHO-007, REQ-CHO-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-008 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 50 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer (RW-CREDITAD), a case owner (RW-CASEOWN), the reconciliation agent (SY-AGENT) and internal audit (RW-AUDIT)**, I want **rwb-access to decide, from the permission rows and the policy pack it owns, who may read the matched and unmatched receipts behind SCR-28 and the plan position behind SCR-14, and to write one access-log entry for every allowed read and every refusal**, so that **the payment-matching capability of legacy RWB-E2-008 opens only to the roles the bank has authorised, the reconciliation agent reads the exception list under its own service identity, and every receipt looked at or refused is on the record in the same append-only log as the matching decisions**.

### 2. Business rationale

Payment matching is only as safe as the door in front of it. A matched receipt names a customer's plan and amount, and the exception list is a queue of cash that has not been placed; both are read by a Credit Administration officer, by a case owner and by an automated reconciliation agent, and the bank has to be able to say who looked at which receipt, when, and who was turned away. rwb-access owns Recovery roles as data, the scope, the masking policy, the delegation of authority table and the access log (Arch v5 slide 41; schema `rwb_access`), so the answer to "may this caller read this receipt or this plan position" and the record of that answer are this service's work.

This story is the rwb-access part of legacy RWB-E2-008. The match itself, JOB-07 and the missed payment event are rwb-payment (RWB-P8-E2008-APP and RWB-P8-E2008-CON); the case and treatment movement on the events is rwb-case (RWB-P3-E2008-APP); the cross-service run is RWB-ITG-E2008-ITG. What is left here is the authorise decision and its access-log entry for the two reads the capability needs: the matched and unmatched receipts on `GET /proceeds` (SCR-28) and the plan position on SCR-14.

The policy pack is versioned data in `rwb_access`: a permission row per role and capability area with the letters C, R, U, D and A (or a dash), a role row with its class and default scope, and, where a personal field is involved, a masking row (TSD P4 T3.1; FSD A2.4 and A2.5). For this capability the rows are WRITE_OFF_AND_POSTING R to RW-CREDITAD and to SY-AGENT as a NON_HUMAN_ACTOR, TREATMENT_AND_OFFER R to RW-CASEOWN, no WRITE_OFF_AND_POSTING row for RW-CASEOWN, and R with scope ALL for RW-AUDIT. No masking row is added: a proceeds row carries `payment_code`, `account_key`, `amount` and `matched_to` only, and `account_key` is a token, never the account number, so there is no personal field to mask on this path.

It serves REQ-CHO-007 (a missed payment raises an event) and REQ-CHO-009 (payments matched to the plan, the unmatched on an exception list), the control that receipts are matched the same day (CTL-41) and the rule that unmatched cash is held for the reconciliation agent (R-UNI-03).

### 3. Preconditions

- RWB-P4-E1037-CON is published: the `POST /api/recovery/access/v1/authorise` envelope, its error contract, the Idempotency-Key rule and the cached-call behaviour (DP-08 in the service, DP-11 in the call). This story serves its answer for two capability areas and adds no path.
- The `rwb_access` baseline is applied: `role`, `permission`, `masking_rule`, `role_conflict` and `delegation_limit` exist before this story runs its own migration, with the outbox, inbox and idempotency objects of the library.
- The policy pack is loaded as versioned rows by RWB-P4-AD002-APP (out of scope): matrix version "PM-2026.11" in force, with the rows named in section 2. The exact load path, its approval and its rollback are that story's.
- RWB-P8-E2008-CON is published: the `GET /api/recovery/payment/v1/proceeds` response shape and the fixtures this story's component tests stand on — the matched receipt "PAY-90001" of 12,500.00 for case "RC-2026-000555" and treatment "T-0701", and the unmatched receipt "PAY-90002" of 3,000.00.
- The requested role, area, right, scope, resource, filter and row count of the read, and the matrix version to apply, are named on the authorise call. The request shape is Not specified in the source documents (GAP-0925; ASM-1648).
- The permission letters of the two capability areas, and the scope value of the Credit Administration role, are read from the policy pack. They are Not specified in the source documents (GAP-0926; ASM-1649).
- The position of the filter and the row count inside the decision-record entry is Not specified in the source documents (GAP-0927; ASM-1650).
- The seven operations this story consumes are each a one-hop REST contract of their owner (DP-11). Their names, paths and payloads are Not specified in the source documents (GAP-1346). This story builds against the owners' fakes from Day 1, and the placeholder stands until each owner publishes its operation.
- The case payment list is answered through `GET /proceeds` with the case scope applied. The payment matching workflow name and its four step activity names are Not specified in the source documents (GAP-1349; GAP-1639). The SCR-28 and SCR-29 field lists and the run view are Not specified in the source documents (GAP-1349).
- The twelve patterns add their platform and contract rows, which are Not specified in the source documents (GAP-2496). The metadata row Depends on (build) stays None.
- The login is the rwb-access login (DP-02).

### 4. Flow

1. The caller service posts a read on its own endpoint: `GET /api/recovery/payment/v1/proceeds?matched=false` for the exception list behind SCR-28, the proceeds list filtered by matched or unmatched, or the plan-position read behind SCR-14. Before it answers, it calls `POST /api/recovery/access/v1/authorise` on rwb-access: one hop, 2 s timeout, cached permission data (Arch v5 slide 14; DP-11).
2. rwb-access: resolves the caller's roles for the session and reads the permission rows of those roles for the requested capability area on the matrix version in force. Where a caller holds two roles, the letters are the union of the rows of the roles held, and no permission comes from a role the caller does not hold (FSD A2.1 AC-ALT-P4-001-02).
3. rwb-access: a caller with no permission row in the area — or a dash for the right asked — is refused by default; the answer names the area and the right, and the caller answers 403 with MSG-P4-002.
4. rwb-access: a caller who holds the right is checked against the scope it resolves for the resource. A case or a treatment outside that scope is refused as out of scope, and the caller answers 404 with MSG-P4-003 rather than a row (FSD A2.4 AC-EXC-P4-004-01).
5. rwb-access: writes the access-log entry as a decision record in the same transaction as the decision — decision code "AC-READ" for an allowed read, "AC-DENY" for a refusal — with the actor, the capability area, the right, the matrix version and, for a list or export read, the filter and the row count and no case ID (FSD A2.7 AC-P4-007-01 and AC-ALT-P4-007-02).
6. rwb-access: the record is written first. If it cannot be written, the decision is not returned, the caller answers 503 with MSG-P7-003 and no data reaches the reader (FSD A2.7 AC-EXC-P4-007-03; R-UNI-39).
7. rwb-access: the outbox relay publishes DecisionRecorded on `rwb.decision-record.v1`, and the central ledger in rwb-decision collects the record within 5 minutes (DP-03).
8. RW-CREDITAD reads the matched and the unmatched receipts on SCR-28: 200 with the page of proceeds rows, and one AC-READ entry with the filter and the row count.
9. RW-CASEOWN reads the plan position of the treatment on SCR-14 under TREATMENT_AND_OFFER R and is refused on the proceeds list under WRITE_OFF_AND_POSTING R; the two answers are two decisions and two entries.
10. SY-AGENT reads the exception list under its own service identity, class NON_HUMAN_ACTOR, with WRITE_OFF_AND_POSTING R; the entry names the service identity and never a person (R-UNI-03; TSD P4 T6.1).
11. A new matrix version comes into force and rwb-access publishes AccessPolicyChanged on `rwb.access.events.v1`; the cached permission data behind the authorise call is dropped and the next call answers on the version in force, with no deployment (Arch v5 slide 43).
12. RW-AUDIT reads the access-log entries and the matrix with scope ALL; the entries are the same append-only decision records the matching decisions sit in, so access and decisions are queried together (FSD A2.8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role holds the right but the case or treatment is outside the caller's scope | The read is refused as out of scope; the caller answers 404 and no row is returned | MSG-P4-003 | AC5 |
| X2 | The role holds no permission row in the area, or a dash for the right | Deny by default; the caller answers 403 and nothing is read | MSG-P4-002 | AC2, AC7 |
| X3 | No matrix version is in force on the business date | The call is refused and never defaulted to allowed; one AC-DENY entry is written | MSG-P4-002 | AC7 |
| X4 | The decision record cannot be written | The decision is not returned; the caller answers 503 and no data is returned; an incident is raised | MSG-P7-003 | AC8 |
| X5 | A list or export read carries a filter and a row count | The entry holds the filter and the count and no case ID | None | AC1, AC3 |
| X6 | A non-human actor calls the same path | The same permission rows decide; the entry names the service identity and the role class | MSG-P4-002 when the right is absent | AC3 |
| X7 | A revoked right is read after the new matrix version is published | The cached data is dropped on AccessPolicyChanged and the next call answers on the version in force | None | AC6 |
| X8 | The token carries no Workbench role | No role resolves, so no permission row applies; the call is refused with 401 before any read | MSG-P4-001 | AC7 |
| X9 | The payment service does not answer inside the REST budget on the caller's side | One hop, 2 s timeout (DP-11); the authorise answer stands and the caller retries; no partial page is logged as a read | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E1037-CON for the authorise envelope and RWB-P8-E2008-CON for the receipt fixtures; the policy pack is rows in its own schema, and no other service is called at build time |
| Negotiable | Every role, area, letter, scope and version is a row of the policy pack or a request value; the story fixes the decision and the entry, not the matrix content |
| Valuable | The two reads of the payment-matching capability are decided and logged, and a refused reader is on the record with the area and the right |
| Estimable | One authorise branch, one scope check, one access-record writer, one endpoint of its own schema and one migration |
| Small | Fits one sprint with its tests |
| Testable | Every owned criterion is a test case in section 16, and every cross-service answer is stubbed by RWB-P8-E2008-CON |

### 7. Acceptance criteria

```gherkin
Feature: Authorise decisions and access-log entries for payment matching

  Background:
    Given matrix version "PM-2026.11" is in force with WRITE_OFF_AND_POSTING R for roles "RW-CREDITAD" and "SY-AGENT", TREATMENT_AND_OFFER R for role "RW-CASEOWN", no WRITE_OFF_AND_POSTING row for role "RW-CASEOWN", and R with scope "ALL" for role "RW-AUDIT"
    Given the rwb-payment contract mock returns proceeds "PAY-90001" of 12,500.00 matched to "INSTALLMENT" for case "RC-2026-000555" and treatment "T-0701" with due date 2026-12-15
    Given the rwb-payment contract mock returns proceeds "PAY-90002" of 3,000.00 unmatched with no treatment

  Scenario: AC1 Credit Administration reads the exception list and the read is logged (new, D-RCV-60)
    Given role "RW-CREDITAD" holds WRITE_OFF_AND_POSTING R in matrix version "PM-2026.11"
    When rwb-access is asked to authorise GET /api/recovery/payment/v1/proceeds?matched=false for role "RW-CREDITAD"
    Then the authorise answer allows the read
    Then the rwb-payment contract mock returns status 200 with 1 row, proceeds "PAY-90002" of 3,000.00 unmatched
    Then one decision-record entry with decision code "AC-READ" exists with the actor, area "WRITE_OFF_AND_POSTING", right "R", matrix version "PM-2026.11", the filter "matched=false" and row count 1
    Then the entry holds no case ID

  Scenario: AC2 Case owner is refused the proceeds list (new, D-RCV-60)
    Given role "RW-CASEOWN" holds TREATMENT_AND_OFFER R and no WRITE_OFF_AND_POSTING row in matrix version "PM-2026.11"
    When rwb-access is asked to authorise GET /api/recovery/payment/v1/proceeds?matched=false for role "RW-CASEOWN"
    Then the authorise answer refuses with area "WRITE_OFF_AND_POSTING" and right "R"
    Then the rwb-payment contract mock returns status 403 with message MSG-P4-002
    Then one decision-record entry with decision code "AC-DENY" exists with area "WRITE_OFF_AND_POSTING", right "R" and no case ID
    Then no proceeds row is returned

  Scenario: AC3 Reconciliation agent reads the exception list under its service identity (new, D-RCV-60)
    Given role "SY-AGENT" has role class "NON_HUMAN_ACTOR" and holds WRITE_OFF_AND_POSTING R in matrix version "PM-2026.11"
    When rwb-access is asked to authorise the exception list read for role "SY-AGENT"
    Then the authorise answer allows the read
    Then one decision-record entry with decision code "AC-READ" exists and names role "SY-AGENT", the role class "NON_HUMAN_ACTOR" and no person
    Then the entry holds the filter "matched=false" and the row count of the answer

  Scenario: AC4 Two capability areas in one session (new, D-RCV-60)
    Given role "RW-CASEOWN" holds TREATMENT_AND_OFFER R and no WRITE_OFF_AND_POSTING row in matrix version "PM-2026.11"
    When rwb-access is asked to authorise the plan-position read of treatment "T-0701" on case "RC-2026-000555" for role "RW-CASEOWN"
    Then the authorise answer allows that read with area "TREATMENT_AND_OFFER"
    Then one decision-record entry with decision code "AC-READ" exists with the case "RC-2026-000555"
    When the same session is asked to authorise the proceeds list read
    Then the authorise answer refuses that read with area "WRITE_OFF_AND_POSTING"
    Then one decision-record entry with decision code "AC-DENY" exists, and the answer to the plan-position read is unchanged

  Scenario: AC5 Case outside the caller's scope (new, D-RCV-60)
    Given role "RW-CASEOWN" holds default scope "OWN" and owns 12 cases
    Given case "RW-2026-000456" belongs to team "MTG-NE" and another owner
    When rwb-access is asked to authorise the plan-position read of case "RW-2026-000456" for role "RW-CASEOWN"
    Then the authorise answer refuses the case as out of scope
    Then the rwb-payment contract mock returns status 404 with message MSG-P4-003
    Then one decision-record entry with decision code "AC-DENY" exists with area "TREATMENT_AND_OFFER", right "R" and no case ID
    Then the 12 cases the caller owns are still returned on the case list read

  Scenario: AC6 Cached decision refreshed on AccessPolicyChanged (new, D-RCV-60)
    Given role "RW-LEGAL" holds no WRITE_OFF_AND_POSTING row in matrix version "PM-2026.11"
    And matrix version "PM-2026.12" gives role "RW-LEGAL" WRITE_OFF_AND_POSTING R with 756 rows and valid from 2026-12-01
    When rwb-access is asked to authorise the exception list read for role "RW-LEGAL" on 2026-11-30
    Then the authorise answer refuses the read and the entry names matrix version "PM-2026.11"
    When matrix version "PM-2026.12" comes into force and AccessPolicyChanged is published on rwb.access.events.v1
    And the same call is made for role "RW-LEGAL" on 2026-12-01
    Then the authorise answer allows the read with no deployment
    Then the second entry names matrix version "PM-2026.12"

  Scenario: AC7 Deny by default for a role with no row and for no version in force (new, D-RCV-60)
    Given role "RW-PHONECOL" holds no permission row for area "WRITE_OFF_AND_POSTING" in matrix version "PM-2026.11"
    When rwb-access is asked to authorise the exception list read for role "RW-PHONECOL"
    Then the answer refuses and never defaults to allowed
    Then one decision-record entry with decision code "AC-DENY" exists with area "WRITE_OFF_AND_POSTING", right "R" and no case ID
    When no matrix version is IN_FORCE on 2026-12-15
    Then the same call is refused in the same way and the rwb-payment contract mock returns status 403 with message MSG-P4-002

  Scenario: AC8 The access entry is a decision record and not a new event (new, D-RCV-60)
    Given the exception list read of AC1 is allowed
    When the access-log entry is written
    Then exactly one decision-record entry with decision code "AC-READ" exists
    Then the outbox holds one DecisionRecorded message for topic rwb.decision-record.v1
    Then no AC-READ and no AC-DENY message is published on rwb.access.events.v1
    Then the only events rwb-access publishes on that topic are AccessPolicyChanged and DoaLimitChanged

  Scenario: AC9 A non-human actor, a refused out-of-scope request and a changed matrix follow the business rules (new, D-RCV-60)
    Given a non-human actor calls the authorise call under its service identity and role class
    Then the access entry names the service identity and the class and never a person
    Given a case or treatment outside the caller's resolved scope is requested
    Then the call is refused and no data is returned; status and message are Not specified in the source documents (NEWAC-RWB-P4-E2008-APP-AC9)
    Given AccessPolicyChanged is published on rwb.access.events.v1
    Then cached permission data is dropped and the next authorise call uses the changed matrix with no deployment and no restart
    Then only AccessPolicyChanged and DoaLimitChanged go to rwb.access.events.v1 and DecisionRecorded to rwb.decision-record.v1
```

These nine criteria are new for this slice. The legacy criteria of RWB-E2-008 describe the match, the missed payment and the run summary and are carried by RWB-P8-E2008-APP; the access criterion TC-E2-008-10 is proved here as AC2 and AC4.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The authorise answer comes from the permission rows of the caller's roles on the matrix version in force; no role code, capability area, letter, scope value or version sits in code | FSD A2.4 BR-P4-004; TSD P4 T3.1; DP-01 |
| BR2 | A read of the proceeds list or of one proceeds row needs WRITE_OFF_AND_POSTING R for the caller's role; a plan-position read needs TREATMENT_AND_OFFER R; the two areas are decided separately and one answer never grants the other | Legacy RWB-E2-008 section 10; TSD P4 T3.2 LOV-CAPABILITY |
| BR3 | A non-human actor is authorised the same way a person is, under its service identity and its role class, and its entry names the service identity and the class, never a person | TSD P4 T6.1; NFR-051; req R-UNI-03 |
| BR4 | Every allowed read writes one decision-record entry with decision code "AC-READ" and every refusal one with "AC-DENY", in the same transaction as the decision; if the record cannot be written the decision is not returned and no data reaches the reader | FSD A2.7 AC-EXC-P4-007-03; R-UNI-39; DP-03 |
| BR5 | A list, page or export read records the filter and the row count and no case ID; a single-record read records the case ID | FSD A2.7 AC-ALT-P4-007-02 and AC-P4-007-01 |
| BR6 | A caller with no permission row in the area, a dash for the right, or no matrix version in force is refused by default and never defaulted to allowed | TSD P4 T4; R-UNI-41; ASM-1651 |
| BR7 | A case or treatment outside the caller's resolved scope is not returned: the answer is a refusal and the caller answers 404 with MSG-P4-003 | FSD A2.4 AC-EXC-P4-004-01; FSD A2.11 VR-P4-011-1 |
| BR8 | The cached permission data is dropped when AccessPolicyChanged is published; a changed matrix takes effect on the next authorise call, with no deployment and no restart | Arch v5 slide 43; FSD A2.4 AC-P4-004-01; ASM-1651 |
| BR9 | No masking row is needed on this path: a proceeds row carries `payment_code`, `account_key`, `amount` and `matched_to` only, `account_key` is a token and never the account number, and a personal field with no masking row is masked by default | FSD A2.5 AC-EXC-P4-005-05; TSD P4 T3.1 masking_rule; NFR-039 |
| BR10 | The access log is a decision-record entry and never a new Kafka event: rwb-access publishes only AccessPolicyChanged and DoaLimitChanged on `rwb.access.events.v1`, plus DecisionRecorded on `rwb.decision-record.v1` | Arch v5 slide 43; DP-03; FSD A2.8; ASM-1651 |

### 9. State transitions

None. This story changes no case state and no treatment state: it answers a permission question and writes an access entry. The plan route state moves in rwb-case on the events rwb-payment publishes (RWB-P3-E2008-APP), and the proceeds match state belongs to rwb-payment (RWB-P8-E2008-APP).

The only lifecycle this slice touches is the record's: the entry is written with the state change and is not amended, and rwb-decision collects it into the central ledger within 5 minutes (DP-03). A matrix version has the LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED lifecycle of TSD P4 T4, which RWB-P4-AD002-APP owns.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-access service identity (the rwb-access login, DP-02) | Decides the authorise answer for the two areas and writes the access-log entry |
| Decision-record library identity | Writes the local decision record and its outbox row before the answer is returned (Decision log C) |
| RW-CREDITAD, Credit Administration officer | Reads the matched and unmatched receipts on SCR-28 (Write-off and posting R) |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14 (Treatment and offer R); holds no Write-off and posting right, so the proceeds list is refused |
| SY-AGENT, agent platform (role class NON_HUMAN_ACTOR) | Reads the exception list under its service identity (Write-off and posting R) |
| RW-AUDIT, internal audit | Reads the access-log entries and the matrix with scope ALL (Platform administration R; TSD P4 T6.1) |
| RW-SECADM, security administrator | Owns the matrix and loads a new version through RWB-P4-AD002-APP; this story only reads the rows |
| gateway-bff | Serves SCR-28 and SCR-14 and calls the owning services one hop each (DP-19); it holds no permission logic |

The per-role letters of the two areas and the scope value of the Credit Administration role are Not specified in the source documents (GAP-0926; ASM-1649); the story reads them from the policy pack and fixes none in code.

### 11. Data

| BR Field ID | Entity in rwb_access | Field | Read or write |
|---|---|---|---|
| Not specified in the source documents (CG-ALL-5188) | role | id, role_code, role_name, role_class, default_scope, entra_group | Read |
| DF-REF-038 | role | default_scope (OWN, TEAM, REGION or ALL) | Read |
| DF-REF-040 to DF-REF-044 | permission | id, role_id, capability_area, letters, matrix_version | Read |
| DF-REF-043 | permission | letters (C, R, U, D and A, or a dash) | Read |
| DF-REF-198 to DF-REF-204 | masking_rule | id, role_code, field_id, unmasked, masking_version, valid_from, valid_to | Read; no row applies to a proceeds field in this slice |
| DF-REF-205 to DF-REF-211 | role_conflict | role_code, conflicts_with, reason, conflict_version, valid_from, valid_to | Read at session resolution only |
| DF-REF-016 to DF-REF-026 and DF-REF-055 to DF-REF-062 | delegation_limit | decision code, level, product and limits | Not read by this slice: no approval is decided here |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields, including the decision code, actor, area, right and version | Write |
| DF-FIN-001 to DF-FIN-009 | proceeds (through the rwb-payment contract) | the row the caller is about to return, named by payment_code, account_key token, amount and matched_to | Read as request values only; never copied |

No proceeds row, no case row and no treatment row is copied into `rwb_access`: the service sees the identifiers and facts the caller names on the authorise call, writes them into the entry where the rule allows, and stores nothing else (DP-01). Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None new. The decision is served through `POST /api/recovery/access/v1/authorise`, whose path, request and response envelope, error contract and Idempotency-Key rule belong to RWB-P4-E1037-CON; this story adds no path, no query parameter and no response field. Base of the service `/api/recovery/access/v1`, owner rwb-access (P4).

The three answers this slice serves on that envelope are: allow, refuse by right, refuse by scope. Their field names in the envelope are Not specified in the source documents (GAP-0925; ASM-1648).

#### 12.2 REST operations consumed

None. rwb-access is the called side of this capability: the payment and case endpoints call the authorise contract, and this story makes no outbound call. The receipt fixtures it tests against are a contract fake (12.8), not a consumed operation.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.access.AccessPolicyChanged.v1` | `rwb.access.events.v1` | P4 | roleCode | roleCode, capabilityArea, matrixVersion, validFrom |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId or roleCode | decision code "AC-READ" or "AC-DENY", area, right, matrix version, business date, record reference |

Both are written to the outbox in the same transaction as the decision and relayed with the CloudEvents envelope; neither carries personal data (DP-09). The access log itself is not an event: every read and every refusal is a decision-record entry (DP-03), so `rwb.access.events.v1` carries policy changes only.

#### 12.4 Events consumed

None. The cache behind the authorise call is dropped by this service when it publishes AccessPolicyChanged, so no consumer handler is needed; the other services drop their own cached copy on the same event (Arch v5 slide 43).

#### 12.5 Workflows and activities

None. This slice has no Temporal workflow, activity or state machine: the decision is one synchronous call inside the 2 s budget (DP-11). The task queue `rwb-access` serves the service's other work.

#### 12.6 Schedules

None. JOB-18 Access review list is rwb-access's six-monthly Schedule (Arch v5 slide 44) and sits with the access-administration work, not with this slice.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| role | P4 (rwb_access) | The caller's roles, class and default scope |
| permission | P4 (rwb_access) | The letters per role and capability area, with `matrix_version` |
| masking_rule | P4 (rwb_access) | Read at resolution; no row applies to a proceeds field |
| role_conflict | P4 (rwb_access) | Read at session resolution only |
| delegation_limit | P4 (rwb_access) | Not read by this slice |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_access | Outbox, inbox and idempotency objects (DP-09) |

`lov_value` stays with rwb-case as reference data (DP-07) and `partner_user` with rwb-partner; rwb-access reads no table of another service and holds no foreign key across services (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-payment WireMock | The P8 contract of RWB-P8-E2008-CON | `GET /api/recovery/payment/v1/proceeds?matched=false` returning "PAY-90002" of 3,000.00 unmatched, the matched page with "PAY-90001" of 12,500.00 for case "RC-2026-000555" and treatment "T-0701", and the 403 and 404 answers that carry MSG-P4-002 and MSG-P4-003 |
| rwb-access policy-pack fixture | The `role`, `permission`, `masking_rule` and `role_conflict` rows of matrix versions "PM-2026.11" and "PM-2026.12" | The rows named in section 2, the dash and no-row cases, and the 756-row version of AC6 |
| decision-record library fake | The local record writer and the outbox relay | A written entry per decision, a forced write failure for AC8 and the 503 path, and the DecisionRecorded message |
| rwb-access authorise envelope fixture | The RWB-P4-E1037-CON contract | The allow, refuse-by-right and refuse-by-scope answers, and the request carrying area, right, scope, filter and row count |

The request shape the fixture carries is Not specified in the source documents (GAP-0925; ASM-1648).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The authorise decision is served on the RWB-P4-E1037-CON contract; no new path, no outbound call, and one hop within 2 s on the inbound call |
| Kafka | 2 published, 0 consumed | `rwb.access.events.v1` (AccessPolicyChanged) and `rwb.decision-record.v1` (DecisionRecorded) published; nothing consumed |
| Temporal | None | No workflow, activity or Schedule in this slice; the task queue `rwb-access` serves other work |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `authorise`, Java package `th.co.scb.ace.workbench.recovery.access.authorise`.

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
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 applies as the rule that the policy rows are read only from `rwb_access`; DP-05 as a prohibition, because this slice reads no ACE view and needs no `v_ace_*` grant; DP-04 as the service's kit for the administrative change paths, since the authorise answer itself is a table read on the version in force and this slice carries no package; DP-10 as the mechanism that will carry JOB-18 in the access-administration work; DP-11 as the one-hop, 2 s form of the authorise call; DP-19 as the composite route that serves SCR-28 and SCR-14. The rows above name the platform and service contracts of the pattern family; this secondary slice adds no new build dependency of its own (metadata H = None), because it is delivered inside the `rwb-access` baseline and serves an endpoint whose envelope RWB-P4-E1037-CON already publishes. The contract version it builds against is the `/v1` path of that envelope; no finer version is specified in the source documents (DOR-RWB-P4-E2008-APP-23).

Contract published. The REST surface this story serves is the RWB-P4-E1037-CON envelope, already published, so this story adds no contract story of its own (DOR-RWB-P4-E2008-APP-21). Contract fake library version: Not specified in the source documents (DOR-RWB-P4-E2008-APP-22).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AuthoriseHandler | Controller | Serves the authorise answer for the WRITE_OFF_AND_POSTING and TREATMENT_AND_OFFER areas on the RWB-P4-E1037-CON envelope; maps a refusal to the right error |
| PolicyPackReader | Repository | Reads `permission` and `role` for the caller's roles on the matrix version in force; one query per call |
| PermissionResolver | Service | Unions the letters of the roles the caller holds, applies the dash rule and denies by default when no row exists (BR1, BR6) |
| ScopeResolver | Service | Resolves OWN, TEAM, REGION or ALL for the resource from `role.default_scope` and answers the out-of-scope refusal (BR7) |
| CachedPermissionStore | Cache | Holds the resolved permission data for the call and drops it when AccessPolicyChanged is published (BR8) |
| AccessRecordWriter | Service | Writes the AC-READ or AC-DENY decision record with the actor, area, right, version, filter and row count, first in the transaction (BR4, BR5) |
| DecisionRecordClient | Client | Calls the decision-record library and its outbox relay (DP-03) |
| NonHumanActorResolver | Service | Reads the role class of a service identity so an agent is decided like a person and logged as a service (BR3) |
| AccessPolicyPublisher | Service | Writes AccessPolicyChanged to the outbox when a matrix version comes into force (BR8, BR10) |
| MaskingReader | Repository | Reads `masking_rule` at resolution; returns no row for the proceeds fields (BR9) |

**Database and migrations**

- Reads and writes `role`, `permission`, `masking_rule` and `role_conflict` in schema `rwb_access`, and writes the decision record through the library. The outbox, inbox and idempotency objects arrive with the baseline.
- Constraint: unique index `ux_permission_role_area_version ON permission (role_id, capability_area, matrix_version)`, so one letter set exists per role and area per version (BR1).
- Constraint: check `ck_permission_letters_known` on `permission.letters`, for C, R, U, D, A and the dash (TSD P4 T3.1; FSD A2.4 field catalog).
- Constraint: index `ix_permission_area_version ON permission (capability_area, matrix_version)` for the authorise read.
- Migration in this story: `V2008_1__access_payment_matching.sql` adds the three constraints above. No table and no column is added: the policy pack is rows, and the load path is RWB-P4-AD002-APP, out of scope.

**Configuration and reference data**

- Matrix version "PM-2026.11" in force at the start of wave 2, with the rows named in section 2; the version in force per environment is recorded in `config/access-matrix.lock`. A new version is loaded and approved by RWB-P4-AD002-APP, not by this story.
- LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS are read through the reference-data contract, owner rwb-case (DP-07), so no area, scope or class value is written in Java.
- The login is the rwb-access login (DP-02).

**Build steps**

1. Write the migration and the three constraints; test the unique index and the letters check.
2. Build PolicyPackReader and PermissionResolver against the fixture of "PM-2026.11"; test AC1, AC2 and AC7.
3. Build NonHumanActorResolver; test AC3.
4. Build ScopeResolver with the OWN case and the out-of-scope answer; test AC5 and AC4.
5. Build AccessRecordWriter and DecisionRecordClient, with the record written first and the forced failure path; test AC8 and the 503 path.
6. Build CachedPermissionStore and AccessPolicyPublisher; test AC6 with the "PM-2026.12" fixture.
7. Run the contract-fake suite of every cross-service answer in isolation, so the story builds before rwb-payment is live, and prove on SIT that no AC-READ or AC-DENY message appears on `rwb.access.events.v1`.

**Feature switch.** None of its own. The switch of the capability is the legacy flag `rwb.payments.matching`, owned by the rwb-payment slice; rwb-access answers the authorise call whether or not the capability is on, so this story adds no switch and no parameter.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P8-E2008-CON stay green, and a SIT week shows every read of the exception list and of the plan position with exactly one access entry, every refusal with exactly one AC-DENY entry, and no proceeds row returned to a role without WRITE_OFF_AND_POSTING R.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | The token carries no Workbench role | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | The role lacks the right in the capability area | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case or treatment is outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

For MSG-P4-002 in this story, {action} is "read the receipts" on the proceeds list and "read the plan position" on SCR-14, and the message never names a payment, an account or an amount. A refusal writes one AC-DENY entry with the area and the right and no case ID; a scope refusal writes the same entry and the answer carries MSG-P4-003 instead.

### 15. Screens and states

SCR-28 Proceeds matching (skeleton in E2; states Loading; matched; unmatched; empty, error and no access are Not specified in the source documents (CG-ALL-5201)) lists the receipts from `GET /proceeds` for the Credit Administration officer, filtered by matched or unmatched; SCR-14 Treatment record shows the plan position and the missed payment to the case owner; its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-5200); SCR-04 Case timeline shows the missed payment for the same case; its loading, empty, error and no access states are Not specified in the source documents (CG-ALL-5199). Both screens are served by the gateway-bff composite route, which calls each owning service one hop and merges the answer (DP-19); this story supplies the authorise answer and the access entry behind them and draws no screen of its own.

The screen states that this slice decides are the three answers of section 12.1: allowed (the screen renders the page), refused by right (the screen shows MSG-P4-002 in place of the list) and refused by scope (the screen shows MSG-P4-003 in place of the record).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-01 | AC1, AC4, BR1, BR4 | Component | RW-CREDITAD reads the matched receipt "PAY-90001" of 12,500.00 for RC-2026-000555/T-0701; one AC-READ entry with the matrix version |
| TC-E2-008-02 | AC2, BR2, BR5 | Component | RW-CASEOWN reads the plan position of "T-0701" on "RC-2026-000555"; no payment between 2026-12-05 and 2026-12-15 |
| TC-E2-008-03 | AC1, AC3, BR5 | Component | "PAY-90002" of 3,000.00 unmatched; filter "matched=false", row count 1, no case ID |
| TC-E2-008-04 | AC4, BR5 | Component | A receipt whose account "A-0999" has no open case; the page is empty and the entry holds row count 0 |
| TC-E2-008-05 | AC5, BR5, BR6 | Component | The ALS batch of 2026-12-15 failed, so the page holds the rows of 2026-12-14; the entry holds the filter and the count |
| TC-E2-008-06 | AC6, BR4 | Contract | The same authorise call replayed with the same Idempotency-Key; one entry, not two |
| TC-E2-008-07 | AC7, BR2, BR6 | Component | RW-CASEOWN reads the plan position and then calls the proceeds list; second call refused with MSG-P4-002 |
| TC-E2-008-08 | AC8, BR6 | Component | No matrix version IN_FORCE on 2026-12-15; the call is refused, never allowed |
| TC-E2-008-09 | AC1, AC6, AC8, BR1, BR4, BR9 | Component | "PAY-90001" matched under matrix version "PM-2026.11"; a later version published on AccessPolicyChanged is used on the next call with no restart; the entry names the version and carries no masked field |
| TC-E2-008-10 | AC2, AC4, BR2, BR6 | Component | RW-CASEOWN calls `GET /proceeds`; refused with status 403 and MSG-P4-002, area WRITE_OFF_AND_POSTING, right R |
| TC-E2-008-11 | Not specified in the source documents (DOR-RWB-P4-E2008-APP-12) | Component | Boundary rows of each table in section 12.7 that this slice reads, at the edges of their validity and version fields |
| TC-E2-008-12 | BR3 | Component | A non-human actor calls the authorise call under its service identity and role class; the entry names the service identity and the class, never a person |
| TC-E2-008-13 | BR7 | Component | A case or treatment outside the caller's resolved scope is requested; the call is refused; status and message are Not specified in the source documents (NEWAC-RWB-P4-E2008-APP-AC9) |
| TC-E2-008-14 | BR8 | Component | AccessPolicyChanged is published; cached permission data is dropped and the next authorise call uses the changed matrix with no deployment and no restart |
| TC-E2-008-15 | BR10 | Component | Only AccessPolicyChanged and DoaLimitChanged go to rwb.access.events.v1 and DecisionRecorded to rwb.decision-record.v1; no other Kafka event carries the access log |
| TC-E2-008-16 | AC9, BR3, BR7, BR8, BR10 | Component | Not specified in the source documents (NEWAC-RWB-P4-E2008-APP-AC9) |

Levels map the legacy System level to End to end where the test spans services and to Component where it runs inside this slice, and the legacy Access level to Component. An integration copy of a case ends in `-ITG` and belongs to RWB-ITG-E2008-ITG, so no `-ITG` id is listed here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the roles, capability areas, letters, scopes, matrix versions and masking rows are versioned rows of `rwb_access`, read on the version in force. No role code and no area appears in Java (BR1).
- No personal data in logs, events or workflow inputs. The path carries `payment_code`, `account_key`, `amount`, `matched_to` and case and treatment identifiers only; there is no name, address, identity number or account number, and a test fixture uses synthetic keys.
- `account_key` is a token, never the account number, and is never logged as an account number; amounts are BigDecimal with scale 2 and are compared exactly.
- ACE data only through the owner's contract or the service's own `v_ace_*` views, and no cross-schema read: this slice reads no ACE view at all, and the receipt facts reach it only as values on the authorise call (DP-01, DP-05).
- The access entry is written first and in the same transaction as the decision, so a read that cannot be recorded returns no data (R-UNI-39).
- The access log is a decision-record entry and never a new Kafka event: `rwb.access.events.v1` carries AccessPolicyChanged and DoaLimitChanged only (BR10).
- A list or export entry holds the filter and the row count and no case ID, so the log itself does not become a way of enumerating a case list (BR5; FSD A2.7).
- Every outbound event is written to the outbox in the same transaction as the change and carries IDs and facts only (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-004-01, TC-E2-004-02, TC-E2-004-12, TC-E2-008-01, TC-E2-008-02, TC-E2-008-03 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-04, TC-E2-008-06, TC-E2-008-07, TC-E2-008-08, TC-E2-008-09, TC-E2-008-10 |

The two requirements are met by the capability as a whole; this slice carries the access side of both, because the exception list of REQ-CHO-009 and the plan position of REQ-CHO-007 are the two reads it decides and logs. The FSD P8 requirement ID for each is Not specified in the source documents (GAP-1624); the FEAT-PAY IDs above are the FSD feature traces.

### 19. Out of scope

- The matching run, JOB-07, the missed payment event and the exception list content: rwb-payment (RWB-P8-E2008-APP), with its contract in RWB-P8-E2008-CON.
- The case and treatment movement on the events: rwb-case (RWB-P3-E2008-APP).
- The end-to-end run across rwb-payment, rwb-case and rwb-access: RWB-ITG-E2008-ITG.
- Manual matching of an unmatched receipt in Epic 4, including its own authorise questions.
- The policy pack load, approval and rollback, and the access review Schedule JOB-18: RWB-P4-AD002-APP.
- Authoring, approval and rollback of package PAYMENT_MATCH (legacy RWB-E2-042).
- The authorise envelope itself, its error contract and its caching contract: RWB-P4-E1037-CON.
- The `rwb_access` schema baseline, the topic and queue provisioning, the dashboards and the runbook of this capability.
