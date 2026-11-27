# RWB-P4-E8010-APP Add a letter template with Compliance approval

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | L-P4-BD |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P4-E8010-APP-16); set by the squad at refinement |
| Depends on (build) | RWB-P4-E8010-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON; API-P6-006; Not specified in the source documents (GAP-0871) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E8-010 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **compliance and PDPA officer**, I want **the approval of a letter template version taken through one gate that checks the right to approve, refuses an approval by the author of the version and by anyone outside Compliance, hands the approval to the service that owns the template, and records against the version who approved it and when**, so that **a letter or a notice is only ever produced from a version that Compliance approved, and the approval of that version can be shown afterwards without asking either team**.

Inside `rwb-access` this is the Compliance approval gate of the legacy story RWB-E8-010:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Two deliverables, and nothing else: the write `POST /api/recovery/access/v1/admin/template-approvals`, which authorises, checks, hands the approval to `rwb-comms` and answers it; and the read `GET /api/recovery/access/v1/admin/template-approvals/{templateId}`, which answers the approvals the gate has recorded for a template.
- The letter template itself lives in `rwb-comms` (P6). The ownership map puts `template`, `notice` and `merge_field` in P6, and the P6 appendix T-A declares the template operations `POST /admin/templates` (API-P6-004), `POST /admin/templates/{templateId}/approve` (API-P6-006), `POST /admin/templates/{templateId}/withdraw` (API-P6-007) and `GET /admin/templates` (API-P6-003). This story reads and writes **no** template row, holds no copy of a template body, a merge field or a notice, and renames or redefines no P6 operation.
- The gate is this service's: Rules and parameters A is authorised here, the four-eyes rule of TSD P4 v3 T6.3 is enforced here, the template version is read through the P6 contract, the approval is handed to the P6 approve operation, and the approval is appended to the local decision-record chain of the library of DP-03 with the template id, the version, the approving role and the time.
- The metadata of this story carries no `rwb-comms` contract dependency, so the two P6 operations the gate calls are built against the P6 contract and its fake and the missing C dependency is raised at D1 — Not specified in the source documents (GAP-0871; ASM-1580). The dependency is not added to the metadata here.
- The approval history is answered from this service's own append-only chain and not from a template row: one entry per approval, with the template id, the version, the state the version was approved into, the approving **role code**, the time and the approval reference, and no name, no e-mail address and no user reference (BR10, ASM-1582).
- The approval is reached from SCR-33 Template approval through the gateway-bff composite route of DP-19, which shows the template as `rwb-comms` answers it and calls the two operations of this story; this story renders no screen of its own and holds no template panel.
- This story starts no workflow, owns no Schedule and publishes no event of its own: the approval is synchronous, the four-eyes rule is a right and not a state, and the only message it produces is `rwb.decision.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1`.

The state a template version carries — `DRAFT`, `APPROVED`, `WITHDRAWN` — is `rwb-comms`'s, read through the P6 contract and never written here (API-P6-004 uploads a version in `DRAFT`, API-P6-006 approves it and API-P6-007 withdraws it). This story records one approval state of its own, `APPROVED`, at the moment the P6 approve operation confirms it (ASM-1580).

### 2. Business rationale

A letter to a borrower is a legal instrument: REQ-OCC-001 asks that notices be generated from templates approved by Legal and REQ-OCC-002 that letter templates be versioned and that the Legal approval be recorded against the version, both Must. The legacy story carried the capability as one administration journey inside the monolith (FEAT-ADM-05, RWB-E8-010), where the template, the approval and the decision log were rows of one schema and the approval was a screen in the same module. In the target the template is `rwb-comms`'s (Architecture v5 slide 41: P6 owns notices, templates and merge fields) and the record of who decided what is the decision record (ADR-022), so the approval of a version is no longer a column of the template: it is a decision that needs an authority, a four-eyes check and a record.

This story is that decision. It meets REQ-OCC-001 and REQ-OCC-002 on the approval side — the approval exists against a version and only a person who is not the author may give it — and it supports REQ-ACA-013, the administration surface with its rights. It carries the FSD target measure for the administration features: rule and limit changes made without a code release, 100 percent, measured monthly from the decision record (FSD P4 v3 A2.21.1). A template version is data, its approval is data, and neither needs a release.

The control that makes the approval worth anything is the separation of the two acts. TSD P4 v3 T6.3 states it in one row: the author who prepared the version and the approver who approved it, with both times, and the author cannot approve. The matrix of T6.1 then decides who may be that approver. Both are enforced here, in one place, before the P6 state is allowed to change — so no consumer of a template can be handed an approved version that passed a weaker gate, and the approval history is answerable by its owner without a call into `rwb-comms`.

Keeping the template in P6 is the point of the split. The gate authorises and records; `rwb-comms` owns the version, its body, its merge fields and the states it moves through, and the letter generation of FEAT-OCC-01 reads only approved versions from the owner. A single writer for the template is what makes REQ-OCC-002 provable: one approval per version, recorded once, and the version that generated a letter identifiable years later.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P4-E8010-CON (same service, its own contract story) | The OpenAPI 3.1 document of the two operations, the `TemplateApproval` and `TemplateApprovalHistory` schemas, the state set, the error envelope, the consumed-operation list and the five contract fakes. This story implements that document and adds no path |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of an approval, hash-linked, written in the transaction that stores the answer |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the shape of an approval reference and the page bounds of the history, as rows and not as code |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) that serves SCR-33 Template approval and calls the two operations, one hop each |
| The `rwb-comms` template contract | The two operations this story consumes and their fake: the read of one template version with its state and its author reference, and the approve operation that moves the version to `APPROVED` with its `valid_from`. It is not in this story's metadata contract-dependency list (GAP-0871; ASM-1580) |

Business preconditions carried from RWB-E8-010, from the feature specification and from the technical specification:

- The rights in force are those of TSD P4 v3 T6.1: RW-COE holds `CRUD` in Rules and parameters, RW-RISK holds `RA`, and the case roles hold `R` only or a dash. The gate authorises Rules and parameters A, and a caller without it is refused with 403 and MSG-P4-002 (BR3).
- The FSD P4 v3 A2.21.3.3 role table names the Compliance and PDPA officer and the Legal counsel as the roles that use the feature, and the center of excellence analyst as the primary author. The approving role this story records is RW-COMPLY; the difference between the FSD role table and the letters of the T6.1 matrix is carried as an assumption and changes no metadata value (ASM-1581).
- A template version is uploaded by `rwb-comms` in state `DRAFT` (API-P6-004) and becomes `APPROVED` only through the P6 approve operation (API-P6-006), which records the approval against the version with `approved_by` (DF-REF-063), `approved_at` (DF-REF-064) and `valid_from` (DF-REF-065). This story supplies the authority and the record of the gate; P6 supplies the state.
- The author of a version is the reference `rwb-comms` holds against the version it created (the standard record column `created_by` of TSD P6 v2 T3.0, because the `template` table of T3.1 carries no author column), and the same person may not approve that version (TSD P4 v3 T6.3; MSG-P7-002).
- The seven-item change checklist (TSD P4 v3 T6.3, DF-REF-295) and the checksum of a workbook (DF-REF-285) belong to a **rule package version** and to the rule-change story RWB-P4-E8007-APP; a template version carries `body_ref` (DF-REF-050) and no checksum, and this gate produces no checklist item and no MSG-P3-022 (BR13).
- The approval reference — the minute or instrument the Compliance approval rests on — is Not specified in the source documents (GAP-0871; ASM-1580): its shape is a parameter row read through DP-06, and the contract of RWB-P4-E8010-CON fixes the field.

### 4. Flow

1. The compliance and PDPA officer opens SCR-33 Template approval through the gateway-bff composite route (DP-19). The route shows the versions of a template as `rwb-comms` answers them and calls this service only for the approval and the history.
2. The officer selects a version in state `DRAFT` and submits the approval. The route calls `POST /api/recovery/access/v1/admin/template-approvals` on `rwb-access` with the body `templateId`, `templateVersion`, `productGroup`, `approvalReference`, `validFrom` and `reason`, and an `Idempotency-Key` header.
3. `TemplateApprovalController` validates the request: every field is required, `templateVersion` is a whole number, `validFrom` is a date, and `approvalReference` matches the shape in force read through DP-06. An empty field or a value of the wrong shape is refused with 422 and MSG-GEN-001 naming the field, and no read of the template and no call is made (BR11).
4. The controller looks the `Idempotency-Key` up in the idempotency table of the platform library in `rwb_access`. A key already answered replays that first answer and stores nothing and calls nothing (BR12, AC5).
5. The controller resolves the caller's session and calls `POST /api/recovery/access/v1/authorise` on its own service, one hop with a 2 s timeout and a cached answer, for Rules and parameters A. A caller without the A letter is refused with 403 and MSG-P4-002, and nothing is recorded and no template is read (BR3, AC3).
6. `CommsTemplateClient` reads the version through `GET /api/recovery/comms/v1/admin/templates/{templateId}` of `rwb-comms`, one hop with a 2 s timeout and a breaker, and takes from the answer only the version's `templateVersion`, its `state`, its `authorReference`, its `productGroup` and the `valid_from` it carries. No template body, no merge field and no notice is read (BR5).
7. `TemplateApprovalGate` refuses a version that is not in state `DRAFT` with 409 and MSG-GEN-004, the state being `rwb-comms`'s and the caller asked to reload it (BR4, AC4).
8. `TemplateApprovalGate` then compares the caller's reference with the version's author reference. The author of the version cannot approve it: the call is refused with 403 and MSG-P7-002 and nothing is recorded (BR4, AC4).
9. `CommsTemplateClient` hands the approval to `rwb-comms` through `POST /api/recovery/comms/v1/admin/templates/{templateId}/approve` with the `valid_from`, the `approvalReference` and the caller's `Idempotency-Key` forwarded. `rwb-comms` moves the version to `APPROVED`, sets `approved_by`, `approved_at` and `valid_from` and answers the template (API-P6-006).
10. In one local transaction the service appends one entry to the decision-record chain of DP-03 with the record code of a template approval, the template id, the version, the product group, the approving role code, the approval reference, the `approved_at` that `rwb-comms` answered and no case id; sets the idempotency row to the answer; and stages the outbox row of the entry (BR7, BR12).
11. The answer is 201 with `approvalId`, `templateId`, `templateVersion`, `productGroup`, `state` `APPROVED`, `approvedByRole`, `approvedAt`, `validFrom` and the `Location` of the history read (BR6).
12. Where `rwb-comms` refuses the approval, it answers 409 with its own reason; this story answers 409 with MSG-GEN-004 and records nothing, because the version state moved under the caller between the read and the handoff (BR4, X6).
13. Where `rwb-comms` cannot be reached, or answers beyond the 2 s budget, the call answers 503 with MSG-P7-003, nothing is recorded and no approval is answered; the officer retries with the same `Idempotency-Key` and the P6 approve operation answers the same approval, so no second approval is made (BR12, X8).
14. Where the local record cannot be written, the answer is withheld with 503 and MSG-P7-003 (BR7, AC2); the retry with the same `Idempotency-Key` completes exactly one entry against the approval `rwb-comms` already holds, and the on-call engineer raises the incident on the record failure. The order of the handoff and the record is Not specified in the source documents (GAP-0871; ASM-1580).
15. `GET /api/recovery/access/v1/admin/template-approvals/{templateId}` answers the approvals this service has recorded for the template: one item per approved version with its `templateVersion`, `state`, `approvedByRole`, `approvedAt` and `approvalReference`, ordered by `approvedAt` then by entry id so the paging is stable, with the page default and maximum read through DP-06 (BR9, BR10).
16. A template with no recorded approval answers 200 with an empty `items` and total 0; it is never a 404 and never a named author, so the read cannot be used to probe for a version that Compliance has not approved (BR14).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is empty, `templateVersion` is not a whole number, or `validFrom` is not a date | 422 naming the field; no template read, no handoff, no entry | MSG-GEN-001 | AC1 |
| X2 | `approvalReference` does not match the shape in force | 422 naming `approvalReference`; no template read, no handoff, no entry | MSG-GEN-001 | AC1 |
| X3 | The caller holds no Rules and parameters A | 403, no template read, no handoff, no entry | MSG-P4-002 | AC3 |
| X4 | The caller's session has ended | 401, no template read, no handoff and no entry | MSG-P4-001 | AC3 |
| X5 | The template version is not in state `DRAFT` | 409 and no entry; the screen reloads the template | MSG-GEN-004 | AC4 |
| X6 | `rwb-comms` refuses the handoff because the state moved after the read | 409 and no entry; the approval is not recorded and the version keeps the state P6 gave it | MSG-GEN-004 | AC4 |
| X7 | The caller is the author of the version | 403 and no entry; the P6 approve operation is not called | MSG-P7-002 | AC4 |
| X8 | `rwb-comms` does not answer inside 2 s, or the connection fails | 503 and no entry; a retry with the same `Idempotency-Key` makes no second approval | MSG-P7-003 | AC5 |
| X9 | The local decision-record entry, the idempotency row or the outbox row cannot be written | 503 and no approval answered; nothing is recorded and the retry completes one entry | MSG-P7-003 | AC2 |
| X10 | The same approval arrives twice with the same `Idempotency-Key` | The first answer is replayed; one entry, one handoff | None | AC5 |
| X11 | A break-glass grant is active for the caller | The approval proceeds and the answer carries the warning with the end time of the grant, and the entry carries the grant id | MSG-P4-004 | AC3 |

No exception path of this story changes a case, a task, a role, a permission or a template body: the template version belongs to `rwb-comms`, and the only row this story writes of its own is the entry of its own chain plus the platform library rows of the request.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P4-E8010-CON and its fakes; the template is read and approved through the P6 contract, so no template row, body or merge field is held here |
| Negotiable | The approval-reference shape and the page bounds are parameter rows; the approving role and the state set are reviewed with Compliance and with the P6 owner |
| Valuable | One gate decides who may approve a letter template version, refuses the author of the version, and leaves a record that answers which version Compliance approved and when |
| Estimable | One controller, one gate service, one history service, one P6 client, one record appender, one idempotency store, five fakes and six test cases |
| Small | Fits one sprint with its tests; no new table, no workflow, no schedule, no screen and no event of its own |
| Testable | Each owned criterion has a test case in section 16; the four-eyes rule is provable with two users, and the history is provable against a seeded chain |

### 7. Acceptance criteria

```gherkin
Feature: Add a letter template with Compliance approval

  Background:
    Given the environment is SIT
    Given the letter templates are held by rwb-comms and rwb-access holds no template row, no notice row and no merge-field row
    Given test user "U-6102" holds RW-COMPLY, the role the FSD A2.21.3.3 role table names as the approver of a letter template, with Rules and parameters A in the SIT matrix (ASM-1581)
    Given test user "U-6101" holds RW-COE with "CRUD" in "RULES_AND_PARAMETERS" and is the author reference rwb-comms holds for template version "3"
    Given test user "U-6110" holds RW-CASEOWN with "R" only in "RULES_AND_PARAMETERS"
    Given test user "U-6103" holds RW-AUDIT with "R" in "RULES_AND_PARAMETERS"

  Scenario: AC1 Add a letter template with Compliance approval (legacy RWB-E8-010 AC1)
    Given the rwb-comms contract mock returns template "TPL-SETTLE-EN" version "3" in state "DRAFT" for product group "MORTGAGE"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then adds a new template through the approval path and records who approved it
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-010 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A caller with the case owner right only is refused (new, D-RCV-60)
    Given "U-6110" holds RW-CASEOWN with "R" only and holds no A letter in "RULES_AND_PARAMETERS"
    When "U-6110" calls POST /api/recovery/access/v1/admin/template-approvals for templateId "TPL-SETTLE-EN", templateVersion 3 and approvalReference "APR-2027-000412" with Idempotency-Key "k-010-3"
    Then the response is 403 with message MSG-P4-002 and no approval is answered
    Then the rwb-comms contract fake records no template read and no approve call
    Then no approval entry is appended and GET /api/recovery/access/v1/admin/template-approvals/TPL-SETTLE-EN still answers an empty history

  Scenario: AC4 A version that is not a draft, and an approval by the author, are refused (new, D-RCV-60)
    Given the rwb-comms contract mock returns template "TPL-SETTLE-EN" version "2" in state "APPROVED" and its version "3" in state "DRAFT" with author reference "U-6101"
    When "U-6102" calls POST /api/recovery/access/v1/admin/template-approvals for version "2" with Idempotency-Key "k-010-4"
    Then the response is 409 with message MSG-GEN-004 and no approval is answered
    Then the rwb-comms contract fake records no approve call and no approval entry is appended
    When "U-6101", holding the A letter and being the author of version "3", calls the same operation for version "3" with Idempotency-Key "k-010-5"
    Then the response is 403 with message MSG-P7-002 and no approval is answered
    Then the rwb-comms contract fake records no approve call for version "3" and version "3" stays in state "DRAFT"

  Scenario: AC5 The history answers role codes only and a version is approved once (new, D-RCV-60)
    Given "U-6102" approved template "TPL-SETTLE-EN" version "3" with approvalReference "APR-2027-000412" and validFrom 2027-01-01 under Idempotency-Key "k-010-1"
    And template "TPL-SETTLE-EN" version "2" was approved earlier with approvalReference "APR-2026-000118" and validFrom 2026-12-01
    When "U-6103" calls GET /api/recovery/access/v1/admin/template-approvals/TPL-SETTLE-EN
    Then the answer carries one item for version "2" and one for version "3", each with its templateVersion, its state "APPROVED", approvedByRole "RW-COMPLY", its approvedAt and its approvalReference
    Then the answer carries no name, no e-mail address and no user reference
    When "U-6102" sends the approval of version "3" again with Idempotency-Key "k-010-1"
    Then the first answer is replayed with its approvalId, templateVersion "3", state "APPROVED" and approvedByRole "RW-COMPLY"
    Then exactly one approval entry exists for version "3" and the rwb-comms contract fake records one approve call for it

  Scenario: AC6 Rules with no criterion of their own hold: no template row, an approval reference from the parameter row in force, a checklist field refused, and an empty history never a 404 (new, D-RCV-60)
    When "U-6102" calls POST /api/recovery/access/v1/admin/template-approvals for templateId "TPL-SETTLE-EN", templateVersion 3 and approvalReference "APR-2027-000412" with a checklist field and Idempotency-Key "k-010-6"
    Then the request is refused by the schema with status Not specified in the source documents (NEWAC-RWB-P4-E8010-APP-AC6) and no approval is answered
    Then no row of template is read and no approval entry is appended
    When "U-6102" calls POST /api/recovery/access/v1/admin/template-approvals for templateId "TPL-SETTLE-EN", templateVersion 3 and an approvalReference that differs from the parameter row in force with Idempotency-Key "k-010-7"
    Then the answer carries MSG-GEN-001 and no approval is answered
    When "U-6103" calls GET /api/recovery/access/v1/admin/template-approvals/TPL-SETTLE-EN for a template this service has never approved
    Then the answer carries total 0 and no 404

  Scenario: AC7 A call without authentication is answered 401, and a version rwb-comms does not hold is answered 404 (new, D-RCV-60)
    When a caller without authentication calls POST /api/recovery/access/v1/admin/template-approvals for templateId "TPL-SETTLE-EN", templateVersion 3 and approvalReference "APR-2027-000412" with Idempotency-Key "k-010-8"
    Then the response is 401 and no approval is answered
    When "U-6102" calls POST /api/recovery/access/v1/admin/template-approvals for a templateVersion that the rwb-comms contract fake does not hold with Idempotency-Key "k-010-9"
    Then the response is 404 with message Not specified in the source documents (NEWAC-RWB-P4-E8010-APP-AC7) and no approval is answered
    Then the rwb-comms contract fake records no approve call

  Scenario: AC8 A consumed rwb-comms call that fails or does not answer records no approval (new, D-RCV-60)
    Given the rwb-comms contract fake fails or does not answer the approve call for template "TPL-SETTLE-EN" version "3"
    When "U-6102" calls POST /api/recovery/access/v1/admin/template-approvals for templateId "TPL-SETTLE-EN", templateVersion 3 and approvalReference "APR-2027-000412" with Idempotency-Key "k-010-10"
    Then the response status is Not specified in the source documents (NEWAC-RWB-P4-E8010-APP-AC8) and the approval is not answered
    Then no approval entry is appended and GET /api/recovery/access/v1/admin/template-approvals/TPL-SETTLE-EN still answers an empty history
```

AC1 and AC2 are the two criteria of RWB-E8-010, copied with their text unchanged and their values kept; AC1 carries one added line at the top of its scenario, the template mock, so the approval is provable while the `rwb-comms` contract is still a fake. AC3 to AC8 are new under D-RCV-60 and test only what this story adds: the right, the two refusals, the recorded history, the rules that had no criterion, the error answers and the failed consumed call.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A letter template version is approved through one gate that authorises the right, reads the version, checks the author and the state, hands the approval to `rwb-comms` and records the approval against the version | RWB-E8-010 AC1; FSD P4 v3 A2.21; REQ-OCC-002 |
| BR2 | A notice is generated only from a template version that Compliance approved, and the approval is recorded against the version it approved | REQ-OCC-001, REQ-OCC-002; FSD P4 v3 A2.21.1 |
| BR3 | The approval needs Rules and parameters A; a caller without it is refused with 403 and MSG-P4-002 and nothing is read and nothing is recorded | TSD P4 v3 T6.1; legacy RWB-E8-010 permission checks |
| BR4 | The author of a version cannot approve it (403, MSG-P7-002), and a version that is not in state `DRAFT` is refused (409, MSG-GEN-004); neither refusal records anything | TSD P4 v3 T6.3; MSG-P7-002; API-P6-004 |
| BR5 | The template is `rwb-comms`'s: this story reads it through the P6 contract and holds no template row, body, merge field or notice, and no copy of a template state | Ownership Map v1 (`template`, `notice`, `merge_field` = P6); Architecture v5 slide 41; DP-01 |
| BR6 | The approving role recorded is a role code, the state answered is `APPROVED`, and `approvedAt` and `validFrom` are the values `rwb-comms` answered, so the owner remains the single writer of the version's state and dates | API-P6-006; TSD P6 v2 T3.1 DF-REF-063 to DF-REF-065; ASM-1582 |
| BR7 | Every approval appends exactly one entry to the local decision-record chain of DP-03 in the transaction that stores the answer; an answer that cannot be recorded is withheld with 503 and MSG-P7-003 | R-UNI-39; RWB-E8-010 AC2; DP-03 |
| BR8 | The entry carries the template id, the version, the product group, the approving role code, the approval reference and the time, and no case id, no name and no user reference | NFR-040; Principle 5; ASM-1582 |
| BR9 | The history is answered from this service's own chain, one item per approved version, ordered by `approvedAt` then by entry id, and it never rewrites or deletes an entry | DP-03; DP-01; BR7 |
| BR10 | The history answers a role code and never a person: no name, no e-mail address and no user reference appears in the read, in the entry or in the tests | NFR-040; ASM-1582 |
| BR11 | The approval reference is validated against a parameter row read through DP-06 with the version in force; no shape is a constant in code | DP-06; BR-P4-021; FSD P4 v3 A2.21.3.1 |
| BR12 | One `Idempotency-Key` answers one approval: a replay answers the first answer, appends no second entry and makes no second handoff to `rwb-comms` | Architecture v5 slide 42; DP-09; API-P6-006 |
| BR13 | The seven-item change checklist (DF-REF-295) and the checksum (DF-REF-285) belong to a rule package version and to RWB-P4-E8007-APP; a template approval carries its approval reference and its reason and produces no checklist item and no MSG-P3-022 | TSD P4 v3 T6.3; FSD P4 v3 A2.21 |
| BR14 | A template with no recorded approval answers an empty history with total 0; the read is never a 404 and never names an author, so it cannot be used to probe for an unapproved version | TSD P4 v3 T6.2; FSD P4 v3 A2.21 |

Target-service statements that make the rules hold in `rwb-access`:

- BR1, BR3 and BR4 are one ordered gate in `TemplateApprovalGate`: authorise, read, state, author, handoff, record. Each step that refuses returns before the next one is reached, so a refused approval can never have called the P6 approve operation.
- BR2 is not a rule of this service but the reason for it: the letter generation of FEAT-OCC-01 reads approved versions from `rwb-comms`, and the only path that makes a version approved is the P6 approve operation, which this gate is the authority for.
- BR5 is the absence of a template repository: the module has no table, no view and no join for `template`, `notice` or `merge_field`, and every template field arrives in the P6 answer.
- BR6 is the field set of the answer: `approvedAt`, `validFrom` and the state are copied from the P6 answer, and the only field this service adds is the approving role code it resolved from its own `permission` and `role` rows.
- BR7 and BR9 are the record appender of DP-03 and its read: the entry commits with the idempotency row, and the history is a read over that chain with no write method.
- BR8 and BR10 are the absence of a person in the entry and in the answer: the actor reference lives inside `inputs_ref` as a reference and the answer carries the role code, so the history cannot show who the approver was by name.
- BR11 is the parameters reader at request time with the version in force; a changed reference shape is data and needs no build.
- BR12 is the `idempotency_key` row of the platform library in `rwb_access`, written with the answer and with the `Idempotency-Key` forwarded to P6.
- BR13 is a negative rule: the gate has no checklist field and no checksum field, and a call that carries one is refused with 422 by the schema of the contract.
- BR14 is the empty answer of the history read and the absence of a 404 branch.

### 9. State transitions

This story holds no template state. The states it reads are `rwb-comms`'s, and the one state it records is the approval state of its own entry.

| From | Event | Condition | To |
|---|---|---|---|
| No approval | An approval is submitted | A held, the version is `DRAFT`, the caller is not the author, `rwb-comms` answers `APPROVED` | One entry recorded, answer 201 with state `APPROVED` |
| No approval | An approval is submitted | No A letter | Refused 403 with MSG-P4-002; no read, no entry |
| No approval | An approval is submitted | The version is not `DRAFT` | Refused 409 with MSG-GEN-004; no entry |
| No approval | An approval is submitted | The caller is the author of the version | Refused 403 with MSG-P7-002; no handoff, no entry |
| No approval | An approval is submitted | `rwb-comms` cannot be reached | Refused 503 with MSG-P7-003; no entry |
| No approval | An approval is submitted | The entry cannot be written | Refused 503 with MSG-P7-003; nothing recorded |
| Recorded | The same `Idempotency-Key` is sent again | None | The first answer is replayed; no second entry, no second handoff |
| Recorded | A second approval of the same version is attempted with a new key | The version is `APPROVED` in `rwb-comms` | Refused 409 with MSG-GEN-004; one approval stays |

| Chain | Event | Outcome |
|---|---|---|
| Append-only local chain | An approval, or a refusal that is recorded at the service edge | One entry appended with its `prev_hash` and `entry_hash`; no entry is ever updated or deleted |
| `rwb-comms` | A version is approved | Its state, `approved_by`, `approved_at` and `valid_from` move to `APPROVED`, written by P6 |

A version that `rwb-comms` later withdraws keeps its recorded approval: the entry is append-only and the withdrawal is P6's, so the history states the approval and the account of a withdrawal is the P6 template and its own record (BR5, BR9).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Compliance and PDPA officer (RW-COMPLY) | Approve a template version: the approver the FSD P4 v3 A2.21.3.3 role table names, and the role code recorded on the approval (ASM-1581) |
| Legal counsel (RW-LEGAL) | Uses the feature as the FSD role table states; the gate records the role code the caller holds and no name |
| Center of excellence analyst (RW-COE) | Authors a version in `rwb-comms` with `CRUD` in Rules and parameters; approving the version authored is refused with MSG-P7-002 (TSD P4 v3 T6.3) |
| Risk and model risk officer (RW-RISK) | Holds `RA` in Rules and parameters; may act as an approver through the A letter, and the difference to the FSD role table is carried in ASM-1581 |
| Internal audit (RW-AUDIT) | Reads the history with Rules and parameters R; approves nothing |
| A case role without Rules and parameters A (RW-CASEOWN, RW-PHONECOL) | Refused with 403 and MSG-P4-002; nothing is read and nothing is recorded |
| The gateway-bff route | Calls the two operations on behalf of the signed-in user, one hop each, and passes the `Idempotency-Key` unchanged |
| `rwb-access` itself | Reads `role` and `permission` in its own schema and writes only its own chain and the platform library rows of the request |
| `rwb-comms` (P6) | Owns the template version, its body, its merge fields, its states and its approval columns; answers the read and the approve operation |
| `rwb-decision` (P7) | Owns the central ledger; this story calls it not at all |

The refusal shapes are 403 with an RFC 9457 problem response and `messageId` set to MSG-P4-002 for an absent right and to MSG-P7-002 for an approval by the author, 401 with MSG-P4-001 for no session, 409 with MSG-GEN-004 for a version that is not `DRAFT`, 422 with MSG-GEN-001 for a field, and 503 with MSG-P7-003 for a record or a handoff that cannot be completed. The database login is the per-service login of the service baseline (DP-02), which belongs to RWB-P4-E8010-CON.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 to DF-REF-039 | `role` | id, role_code, role_name, role_class, default_scope, entra_group | Read: the role code recorded as the approving role |
| DF-REF-040 to DF-REF-044 | `permission` | id, role_id, capability_area, letters, matrix_version | Read: the Rules and parameters A letter and the role it is held through |
| DF-DEC-001 to DF-DEC-018 | decision record (local library, DP-03) | the approval entry: `decision_code` DF-DEC-003, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the template id, the version, the product group, the approving role code, the approval reference and the grant id, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | Write; and read for the history |
| (idempotency) | `idempotency_key` (platform library table in `rwb_access`) | the request and the stored answer of an approval | Write and read (DP-09; ASM-0074) |
| (outbox) | `outbox_event` | the record row of the approval entry | Write |
| (inbox) | `processed_event` | none: this story consumes no event | None |
| DF-REF-045 to DF-REF-051, DF-REF-063 to DF-REF-065 | `template` of `rwb_comms` | template_code, template_version, language, product_group, body_ref, approved_by_legal, approved_by, approved_at, valid_from, and the standard record columns `state` and `created_by` of TSD P6 v2 T3.0 | Returned through the P6 contract; not read |
| DF-LEG-015 to DF-LEG-023 | `notice` of `rwb_comms` | none | Not read |
| DF-REF-252 and the merge codes | `merge_field` of `rwb_comms` | none | Not read |

No row of `template`, `notice` or `merge_field` is read or written: they are `rwb-comms`'s (P6) under the ownership map and their fields arrive in the contract, not by a schema read (DP-01). No row of `decision_log_entry` is read or written either: the central ledger is P7's and this story writes only its own local chain on `rwb.decision-record.v1`. No row of `case`, `task` or `rule_package_version` is read: a template approval addresses no case and carries no rule version of its own, and the "rule version" the legacy criterion names is read here as the version of the template that the approval is recorded against (BR8, GAP-0871). Field IDs are those of the Logical Data Model and Data Dictionary v9 and of TSD P6 v2 T3.1.

The name and the shape of the approval reference, the ordered field set of the approval answer, and the record code of a template approval are Not specified in the source documents (GAP-0871; ASM-1580); the schema of RWB-P4-E8010-CON fixes them and this story reads and writes them as that contract publishes them. The read of a single template by its id is Not specified either: the ownership map and the P6 appendix T-A declare `GET /admin/templates` with a code filter and not a read by id, so the path this story consumes is fixed by the contract and raised with the P6 owner (GAP-0871; ASM-1580).

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/template-approvals` | P4 `rwb-access` | Body: `templateId`, `templateVersion`, `productGroup`, `approvalReference`, `validFrom`, `reason` | `approvalId`, `templateId`, `templateVersion`, `productGroup`, `state` `APPROVED`, `approvedByRole`, `approvedAt`, `validFrom`, with `Location` of the history read | 401 (MSG-P4-001); 403 (MSG-P4-002, MSG-P7-002); 409 (MSG-GEN-004); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters A, and the caller is not the author of the version | `Idempotency-Key` required; a replay answers the first answer and makes no second handoff |
| GET | `/api/recovery/access/v1/admin/template-approvals/{templateId}` | P4 `rwb-access` | Path: `templateId`. Query: `page`, `size` | `TemplateApprovalHistory`: `templateId`, `items` of `templateVersion`, `state`, `approvedByRole`, `approvedAt`, `approvalReference`, `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001); 503 (MSG-P7-003) | Rules and parameters R, scope applied | Not applicable, read only |

Both operations sit on the base `/api/recovery/access/v1` of DP-13. The history answers only what this service recorded, so its `state` is `APPROVED` for a version this gate approved, and a later `WITHDRAWN` at `rwb-comms` is P6's answer and not this read's. `page` defaults to the value of its parameter row and `size` is capped by it, both read through DP-06 and never from code (BR11).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (own service) | The Rules and parameters A check behind the approval and the R check behind the history, cached for the session; MSG-P4-002 on a refusal |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The approval-reference shape and the page bounds, with the version in force (DP-06) |
| GET | `/api/recovery/comms/v1/admin/templates/{templateId}` | P6 `rwb-comms` | The version: its `templateVersion`, `state`, `authorReference` and `productGroup`, read before the gate decides. Declared as consumed, never as provided, and named as the missing C dependency of the key (GAP-0871; ASM-1580) |
| POST | `/api/recovery/comms/v1/admin/templates/{templateId}/approve` | P6 `rwb-comms` | The handoff: the approval of the version with its `valid_from` and the approval reference, forwarding the `Idempotency-Key`; P6 moves the version to `APPROVED` and answers the template |

One hop per call, 2 s timeout and a breaker per downstream (DP-11); the parameters read and the authorise answer are cached for the session or the request. The P6 approve operation is the operation of the P6 appendix T-A (API-P6-006), and this story declares it as consumed and never defines it. No other operation of `rwb-comms`, `rwb-decision`, `rwb-case` or `rwb-document` is called. The contract version built against is Not specified in the source documents (DOR-RWB-P4-E8010-APP-23); the paths above are the /v1 paths.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the hash-chained entry of an approval: the template id, the version, the product group, the approving role code, the approval reference and the time |

CloudEvents 1.0 envelope, from the outbox of the transaction that stores the answer. The payload carries references, codes and times and no name, no e-mail address and no personal field, and no template body and no merge field. This story publishes no `rwb.access.<Event>.v1` message: the two events of `rwb-access` are `AccessPolicyChanged` (RWB-P4-E1037-APP) and `DoaLimitChanged` (RWB-P4-E8008-APP), and a template approval adds neither (Architecture v5 slide 14).

#### 12.4 Events consumed

None. `rwb-access` is a reference-data owner in Architecture v5 slide 14 with no inbound event for this capability, and the gate answers from the P6 contract and its own chain. No `processed_event` row is written.

#### 12.5 Workflows and activities

None. The approval is synchronous and the four-eyes rule is a right, not a state: this story starts no workflow, signals no workflow and registers no activity on the `rwb-access` queue. The approval workflow of the kit belongs to `rwb-decision` (P7) and is not used for an administration change of this service.

#### 12.6 Schedules

None. The approval and the history are request-driven; the six-monthly access review list (JOB-18) is the only Schedule of `rwb-access` and belongs to RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role code recorded as the approving role |
| `permission` | P4 (`rwb_access`) | Read only: the Rules and parameters A and R letters and the role they are held through |
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | Write: the entry of an approval. Read: the history |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_access` | The outbox row of the entry and the idempotency row of the request; no inbox row, because no event is consumed (DP-09; ASM-0074) |
| `template`, `notice`, `merge_field` | P6 (`rwb_comms`) | Not read and not written: the template is `rwb-comms`'s and its fields arrive in the contract |
| `decision_log_entry` | P7 (`rwb_decision`) | Not read and not written: the central ledger is P7's and the local record goes on `rwb.decision-record.v1` |

No template, notice or merge-field table is named as this service's and none is created here. `lov_value`, `reference_version` and `reference_row` are reference data of P3 under the ownership ruling; this story's pattern list carries no DP-07 and its contract-dependency list no `RWB-P3-E1043-CON`, so the product group a version carries is taken from the P6 answer and validated against no list of this service (GAP-0871; ASM-1580). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| template fake | the `rwb-comms` contract (GAP-0871; ASM-1580) | `GET /admin/templates/{templateId}` answering "TPL-SETTLE-EN" version "3" in state `DRAFT` with product group `MORTGAGE` and author reference "U-6101", version "2" in state `APPROVED`, a version in state `WITHDRAWN`, and a 503 for X8; `POST /admin/templates/{templateId}/approve` answering the template `APPROVED` with `approved_at` and `valid_from`, a 409 for the state that moved, and the same answer for a repeated `Idempotency-Key` |
| authorise fake | RWB-P4-E8010-CON, RWB-P4-E1037-CON | A granted answer for RW-COMPLY with A, for RW-COE with A and for RW-AUDIT with R in Rules and parameters, and a refused answer with MSG-P4-002 for RW-CASEOWN with R only |
| parameters fake | RWB-P3-E1042-CON | The approval-reference shape and the page bounds, with the version in force |
| decision-record fake | RWB-PLT-E1027-CON | The append of an approval, the hash-link check, the seeded history of versions "2" and "3", and the forced failure AC2 needs |
| gateway-bff fake | RWB-PLT-N001-CON | The composite route of SCR-33 with the template as `rwb-comms` answers it, the approval form and the history panel |

No fake library version is recorded as published: Not specified in the source documents (DOR-RWB-P4-E8010-APP-22).

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2 (the approval and the history); consumed 4 | Base `/api/recovery/access/v1`; two `rwb-comms` operations, the own authorise operation and the `rwb-case` parameters read, one hop and 2 s each |
| Kafka | Published 1 event type; consumed 0 | `rwb.decision-record.v1` through the DP-03 library |
| Temporal | 0 workflows, 0 activities | The `rwb-access` queue carries the access review Schedule of RWB-P4-AD008-APP only |
| File | None | No file input and no file output: the template body is `rwb-comms`'s and its download is API-P6-005 |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access`, module `access/templateapproval`, Java package `th.co.scb.ace.workbench.recovery.access.templateapproval`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-module template row and the in-module approval write of the monolith (DP-01 and DP-13: the template owned by P6 and addressed on this service's own base through the P6 contract), and the ace-web screen that approved in process (DP-19: a gateway-bff composite route). DP-01, DP-02, DP-09 and DP-11 govern the service baseline and the one-hop budget of section 12.2; they add no dependency of their own, they are not in the pattern list the Work Package fixes for this story, and they are not claimed as patterns of it. The reference-data list check of a product group would need DP-07 and `RWB-P3-E1043-CON`, neither of which this story's metadata carries, so the value is taken from the P6 answer and the point is raised as the key's gap (GAP-0871; ASM-1580). The two `rwb-comms` operations are consumed through the P6 contract and its fake, and the missing C dependency is raised in the same gap row and not added to the metadata.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemplateApprovalController | Controller | The two operations: validation, the `Idempotency-Key` lookup, the RFC 9457 problem responses, `Location` on a created approval |
| TemplateApprovalGate | Service | The ordered gate of BR1, BR3 and BR4: right, template read, `DRAFT` state, author check, handoff; a refusal returns before the next step |
| TemplateApprovalService | Service | The answer of BR6: the approving role code from the caller's `permission` and `role` rows, the P6 `approved_at` and `valid_from`, and the entry payload |
| TemplateApprovalHistoryService | Service | The read of BR9 and BR14: the entries of a template, the stable order, the paging from DP-06 and the empty answer |
| TemplateApprovalRepository | Repository | Read-only queries over the local decision-record table of DP-03 in `rwb_access` filtered by the template id; no write method |
| CommsTemplateClient | Client | The two `rwb-comms` operations, one hop, 2 s timeout, a breaker and the `Idempotency-Key` forwarded; maps a 409 to the state refusal and a timeout to 503 |
| PermissionReader | Service | The `role` and `permission` rows of the caller, the A and R letters and the role code that carries the A letter |
| ParameterReader | Service | The approval-reference shape and the page bounds through the parameters contract of DP-06, with the version in force |
| DecisionRecordAppender | Service | The approval entry with its outbox row, in the transaction that stores the answer (DP-03, DP-09) |
| IdempotencyStore | Service | The `Idempotency-Key` lookup and store of the platform library, written with the answer |

**Database and migrations**

- This story creates no table of its own. `role` and `permission` are created by RWB-P4-E1037-APP, the local decision-record table by RWB-P4-E1039-APP and the platform library tables by the service's own DB story, in the per-service Flyway sequence of DP-15; this story reads and uses them.
- No template, notice or merge-field table is created in `rwb_access` and no column of one is copied: a copy would be a second writer of a template state and would drift from `rwb-comms` on the first withdrawal (BR5).
- No write statement touches `role` or `permission`: the reader is read-only, so an approval can never grant itself a right.
- The entry, the idempotency row and the outbox row commit in one transaction; a failure rolls all three back and the answer is withheld with MSG-P7-003 (BR7).

**Configuration and reference data**

- The approval-reference shape and the page default and maximum are parameter rows of `rwb-case` read through DP-06 with the version in force; no shape and no bound is a constant in code (BR11). Their names are fixed by RWB-P4-E8010-CON.
- The product group of a version is the value `rwb-comms` answers and is validated against no list of this service (section 12.7).
- The approving role code is read from `role` through the `permission` row that carries the A letter; no role code and no capability area is a constant in code (BR3, BR6).

**Build steps**

1. `TemplateApprovalController` and its validation; tests for X1 and X2 with no template read.
2. `PermissionReader` and the authorise call of step 5; test the AC3 refusal of a caller with R only, with no P6 call and an empty history afterwards.
3. `CommsTemplateClient` over the template fake: the `DRAFT` read of AC1, the `APPROVED` and `WITHDRAWN` answers of X5, the 409 of X6 and the 503 of X8.
4. `TemplateApprovalGate` with the state check and the four-eyes check; tests for AC4, including the proof that the P6 approve fake records no call for either refusal.
5. `TemplateApprovalService` and the answer of BR6; test that `approvedAt` and `validFrom` are the P6 values and that the approving role is a role code.
6. `DecisionRecordAppender` and `IdempotencyStore` in one transaction; test the replay of AC5 with one entry and one handoff, and the forced failure of AC2 with no record.
7. `TemplateApprovalHistoryService` over a seeded chain of versions "2" and "3"; test the order, the paging, the empty answer of BR14 and the absence of a name or a user reference (BR10).
8. `ParameterReader` over the parameters fake, so the story builds before `rwb-case` is in the environment; test that a changed reference shape is data and needs no build.
9. The contract-fake run of both operations through the gateway-bff fake, so SCR-33 can be demonstrated while the route and the P6 platform are being built.

**Feature switch.** The two operations are switched by the service baseline of RWB-P4-E1037-CON, not by a flag of their own. An approval that is switched off would leave a `DRAFT` version unapproved and visible as such, which is the state the gate is meant to resolve, so this story adds no flag and removes nothing.

**Done when.** The tests in section 16 pass; a `DRAFT` version "3" of "TPL-SETTLE-EN" is approved by RW-COMPLY and answered `APPROVED` with the approving role and the P6 dates; a caller with R only is refused with MSG-P4-002 and no template is read; a version that is not `DRAFT` is refused with MSG-GEN-004 and an approval by the author with MSG-P7-002, neither recording anything; the history answers each approved version with its role code and its time and no name; the same `Idempotency-Key` replays one answer with one entry and one handoff; and a forced record failure withholds the answer with MSG-P7-003.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on both operations |
| MSG-P4-002 | The caller holds no Rules and parameters A on the approval, or no R on the history | You cannot {action} here. Your role does not include it. | This story, on both operations |
| MSG-P4-003 | The legacy story lists it for an action outside the caller's scope | This case is not in your scope. | Not produced by this story: a letter template is not a case and the approval is scoped by role and not by case or product group, so the legacy text is carried unchanged for the key and the shared history read answers the same entries to every reader that holds R (BR14) |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. | This story, as a warning on the approval answer, with the grant id recorded in the entry |
| MSG-GEN-001 | A required field is empty, `templateVersion` is not a whole number, `validFrom` is not a date, or `approvalReference` is not of the shape in force | Enter {field}. | This story, on both operations |
| MSG-GEN-004 | The template version is not in state `DRAFT`, or `rwb-comms` answers that the state moved before the handoff | Someone else changed this record. Reload it to see their change. | This story, on the approval |
| MSG-P7-002 | The caller is the author of the version being approved | Not specified in the source documents (GAP-0871; ASM-1580) | This story, on the approval |
| MSG-P7-003 | `rwb-comms` cannot be reached, or the entry, the idempotency row or the outbox row cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on both operations |

Every error from this service is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request. The business texts are copied unchanged from the legacy story where the message already existed: MSG-P4-002, MSG-P4-003, MSG-P4-004, MSG-GEN-001 and MSG-P7-003 are the legacy texts, and MSG-GEN-004 is the platform text. MSG-P7-002 is the four-eyes rule of TSD P4 v3 T6.3 and its text is Not specified in the source documents (GAP-0871; ASM-1580); the message catalogue supplies it and the contract of RWB-P4-E8010-CON carries its `messageId` only. MSG-P3-022, the missing checklist item, is not produced here, because a template version carries no change checklist (BR13).

### 15. Screens and states

SCR-33 Template approval is the screen, served through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), which shows the versions of a template as `rwb-comms` answers them and calls the two operations of this story, one hop each. This story renders no screen surface of its own.

| Screen | State | What it shows |
|---|---|---|
| SCR-33 Template approval | Versions, list | The versions of a template with their state as `rwb-comms` answers it, and the approval of each version as this service has recorded it |
| SCR-33 Template approval | Approval, form | One `DRAFT` version opened for approval with `productGroup`, `approvalReference`, `validFrom` and `reason`; the reference is validated against the shape in force |
| SCR-33 Template approval | Approval, recorded | The 201 answer with `templateVersion`, state `APPROVED`, `approvedByRole`, `approvedAt` and `validFrom`, and the recorded entry named in the history |
| SCR-33 Template approval | Approval, not a draft | The 409 of X5 or X6 with MSG-GEN-004 and a reload action |
| SCR-33 Template approval | Approval, by the author | The 403 of X7 with MSG-P7-002, the version still `DRAFT` |
| SCR-33 Template approval | Approval, refused | The 403 of X3 with MSG-P4-002 for a role without the A letter |
| SCR-33 Template approval | History | One row per approved version with its version, state, approving role code, time and approval reference, paged |
| SCR-33 Template approval | History, empty | An empty history with total 0 and no error, also for a template no version of which this service has approved |
| SCR-33 Template approval | Not recorded | The 503 of X9 or X8 with MSG-P7-003 and a retry action that reuses the same `Idempotency-Key` |
| SCR-33 Template approval | Empty | Not specified in the source documents (CG-ALL-5507) |
| SCR-33 Template approval | Loading | Not specified in the source documents (CG-ALL-5507) |
| SCR-33 Template approval | Error | Not specified in the source documents (CG-ALL-5507) |
| SCR-33 Template approval | No access | Not specified in the source documents (CG-ALL-5507) |
| SCR-41 Delegation of authority | Empty | As named in Screen Specifications v1 for SCR-41 |
| SCR-41 Delegation of authority | Loading | Not specified in the source documents (CG-ALL-5509) |
| SCR-41 Delegation of authority | Error | Not specified in the source documents (CG-ALL-5509) |
| SCR-41 Delegation of authority | No access | Not specified in the source documents (CG-ALL-5509) |

The legacy story named SCR-39 Rules and parameters and SCR-41 Delegation of authority in its screen table although a letter template sits on neither; the target screen is SCR-33 Template approval (FSD P6 v3 screen list), and the composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the P6 screen work. This story serves the approval side of that screen only: the upload, the content download and the withdrawal of a version are `rwb-comms`'s, and the screen shows them as P6 answers them. SCR-39 is not a screen of this story, so it carries no state here. The SCR-41 Empty row restates the state that Screen Specifications v1 names for SCR-41; its other states are Not specified in the source documents (CG-ALL-5509); this story does not render that screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-010-01 | AC1, BR1, BR2, BR6 | Contract | The template fake answers "TPL-SETTLE-EN" version "3" `DRAFT` for `MORTGAGE`; the approval by RW-COMPLY answers `APPROVED` with `approvedByRole` "RW-COMPLY", the P6 `approved_at` and `validFrom` 2027-01-01 |
| TC-E8-010-02 | AC2, BR7 | Component | The record store forced to fail during the approval: 503 with MSG-P7-003, no approval answered and no entry; a retry with the same `Idempotency-Key` completes exactly one entry |
| TC-E8-010-03 | AC3, BR3 | Component | A caller holding RW-CASEOWN with Rules and parameters R only: 403 with MSG-P4-002, no P6 read, no P6 approve call, no entry and an empty history |
| TC-E8-010-04 | AC2, BR7 | NFR | The append and the outbox row forced to fail under load: every failure is a 503 with MSG-P7-003, no partial entry is ever readable, and the retry path yields one entry |
| TC-E8-010-05 | AC4, BR4 | Component | Version "2" in `APPROVED` refused 409 with MSG-GEN-004; version "3" authored by "U-6101" refused 403 with MSG-P7-002 when "U-6101" approves it; no P6 approve call and no entry for either |
| TC-E8-010-06 | AC5, BR9, BR10, BR12 | Component | The seeded history of versions "2" and "3" with their role codes, times and references and no name; the replay of `Idempotency-Key` "k-010-1" with one entry and one handoff |
| TC-E8-010-07 | §12.7 tables (ASM-3438) | Component | The approval and the history run against `role`, `permission` and the local chain only; no read or write statement on `template`, `notice`, `merge_field` or `decision_log_entry` is issued |
| TC-E8-010-08 | BR5, BR13 | Contract | An approval request carrying a checklist field or a checksum field is refused by the schema with status Not specified in the source documents (NEWAC-RWB-P4-E8010-APP-AC6); no row of `template` is read by this service |
| TC-E8-010-09 | BR8, BR11 | Component | An approval reference that differs from the parameter row in force is refused with MSG-GEN-001; the entry carries no case id, name or user reference |
| TC-E8-010-10 | BR14 | Component | A template with no recorded approval answers an empty history with total 0 and no 404 |
| TC-E8-010-11 | AC6, BR5, BR8, BR11, BR13, BR14 | Component | An approval with a checklist field refused with status Not specified in the source documents (NEWAC-RWB-P4-E8010-APP-AC6) and no template read; an approval reference that differs from the parameter row refused with MSG-GEN-001; an empty history for a template never approved answers total 0 with no 404 |
| TC-E8-010-12 | AC7 | Component | A call without authentication answered 401; a version rwb-comms does not hold answered 404 with no approve call and no entry |
| TC-E8-010-13 | AC8 | Component | The rwb-comms approve call forced to fail or left unanswered: the answer is withheld with status Not specified in the source documents (NEWAC-RWB-P4-E8010-APP-AC8) and no entry is appended |

The full test, with its Given, When and Then, is added to the next version of Recovery Workbench Test Cases, tab Story test cases, under the same test case ID. The four legacy rows are kept: TC-E8-010-01 for AC1, TC-E8-010-02 for AC2, TC-E8-010-03 for the access refusal and TC-E8-010-04 for the forced record failure; TC-E8-010-05 and TC-E8-010-06 are added for the new criteria of this story, and TC-E8-010-07 to TC-E8-010-13 are added for the §12.7 table boundary, the rules that no criterion covered, the error answers and the failed consumed call. The legacy test table carries a Covers column and no Level column: `Access` is read as Component and `Principle 5` as NFR, and the Level of each row is this template's assignment under §R7.2 s16. No ITG story is split from this legacy key, so no `-ITG` copy of these test cases is written here and no `-ITG` id appears in this table.

### 17. Guardrails

- No business value in code: the approval-reference shape and the page bounds are parameter rows (BR11), the approving role is read from `role` and `permission` (BR6), and a test proves that a changed shape needs no build.
- No personal data anywhere: the request, the answer, the history and the entry carry a template id, a version, a product group, a role code, an approval reference and times; no name, no e-mail address and no user reference appears in the answer, the entry or a test (BR8, BR10, NFR-040).
- No read of another service's tables (DP-01): `template`, `notice` and `merge_field` are `rwb-comms`'s and `decision_log_entry` is P7's, and no join crosses a schema. The template fields arrive in the P6 answer.
- One writer for a template: only `rwb-comms` moves a version's state, sets `approved_by`, `approved_at` and `valid_from`, and holds the body; this service holds no template row and no body, so a version cannot be approved, changed or withdrawn here.
- No approval without its record: the entry commits with the answer, and the answer is withheld with MSG-P7-003 when the entry cannot be written (BR7, R-UNI-39).
- Two acts, two people: the author of a version can never approve it, and the check happens before the P6 handoff, so a refused approval cannot move a template state.
- One key, one approval: the `Idempotency-Key` is stored with the answer and forwarded to P6, so a retry after a timeout cannot create a second approval or a second entry (BR12).
- The history cannot be gamed: it answers an empty page rather than a 404 and never names an author, so a caller cannot learn which version Compliance has not yet approved (BR14).
- Every example, fixture and test payload is synthetic; no template body, notice or production payload is copied into a schema, a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices are generated from templates approved by Legal, with merge fields from case data and no re-keying | Program, Communications | FEAT-OCC-01, FEAT-ADM-05 | All recovery processes | BR1, BR2 | TC-E8-010-01, TC-E8-010-05 |
| REQ-OCC-002 | Letter templates are versioned, and the Legal approval is recorded against the version | Program, Communications | FEAT-ADM-05 | All recovery processes | BR1, BR2, BR6, BR9 | TC-E8-010-01, TC-E8-010-06 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator | Epic 8 | FEAT-ADM-05 | All recovery processes | BR3, BR4, BR12 | TC-E8-010-03, TC-E8-010-04 |

The requirement IDs are those this key serves, and their text is taken from the Program BRD under the fill order of Template and Rules §R7.3; the Work Package carries no requirement list for this key.

| Legacy reference | Where it is kept |
|---|---|
| AC1 add a letter template with Compliance approval, the approval path and the record of who approved it | Sections 1, 4, 7, 8, 12.1, 12.2 |
| AC2 not recorded: nothing changes and the user sees MSG-P7-003 | Sections 4, 5, 7, 8, 12.1, 14 |
| The permission check: Rules and parameters C for RW-COE and A for RW-RISK | Sections 3, 7 (AC3), 8 (BR3, BR4), 10, 12.1 |
| MSG-P4-004, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | Section 14, exception paths |
| The legacy data rows `template` DF-REF-045 to DF-REF-051, `notice` DF-LEG-015 to DF-LEG-023 and `role` DF-REF-034 to DF-REF-038 | Sections 11, 12.7 |
| TC-E8-010-01 to TC-E8-010-04 | Section 16 |
| Legacy screens SCR-39 and SCR-41 as the story named them | Section 15, carried to SCR-33 Template approval |
| The author and approver rule of TSD P4 v3 T6.3 and the letters of T6.1 | Sections 3, 8, 10 |
| Legacy key RWB-E8-010, story RWB-P4-E8010-APP, contract RWB-P4-E8010-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The letter template itself: its upload, its versions, its body, its merge fields, its language, its channel, its content download and its withdrawal are `rwb-comms`'s (P6) under the ownership map and the P6 operations API-P6-003 to API-P6-007.
- The approval mechanics inside `rwb-comms`: the state change to `APPROVED`, the `approved_by`, `approved_at` and `valid_from` columns and the withdraw operation; this story supplies the authority and the record and calls the P6 operation.
- The generation of a letter or a notice from an approved template, its merge fields and its dispatch: FEAT-OCC-01 and the P6 stories RWB-E2-021 and RWB-E2-026.
- The central decision ledger, the query API over `rwb_decision` and the chain verification: `rwb-decision` (P7), and the end-to-end ledger view is the integration story's.
- The permission matrix, the role administration and the masking policy: RWB-P4-E1037-APP and the Epic 8 administration stories.
- The rule-change request, its seven-item checklist and its checksum: RWB-P4-E8007-APP and the registry of `rwb-decision`.
- The screen SCR-33 Template approval itself, its other panels and its composite route specification: RWB-PLT-N001-CON and the P6 screen work.
- The integration harness and the `-ITG` copies of the test cases: no ITG story is split from this legacy key.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability (an OPS story of this legacy key).
