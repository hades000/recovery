# RWB-P6-AD017-APP Manage letter and notice templates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-AD017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E1034-APP |
| Depends on (build) | RWB-P6-AD017-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON, RWB-P6-E1034-APP |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-017 for rwb-comms; the Epic 8 administration surface of the template and notice wording on top of the Epic 1 upload-and-approve core. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-AD017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **legal counsel (RW-LEGAL)**, I want **every template version of rwb-comms listed by template code, language and state with paging, its body downloadable, a Draft version approved with a valid from date and an Approved version withdrawn with a reason that holds generation and raises a task to the litigation officer**, so that **every notice and letter uses wording Legal has approved, a withdrawn template can never generate a new notice, and the officer who has to decide what happens to the held notices is told on the day the wording is withdrawn**.

### 2. Business rationale

The legacy story RWB-AD-017 is the Epic 8 administration entry for letter and notice wording, and it is thin: two criteria (approve, withdraw), a screen SCR-33 Template approval with three states, a data table that mixes four entities of four owners, and an endpoint table that names the notice request and the notice read of the communications module and not one template operation. The work it describes already exists in part in the Epic 1 story RWB-E1-034, which builds the upload, the approve and the withdraw of a template version behind its own flag. The two legacy stories therefore overlap, and no source states which of them owns which part of the surface (GAP-1146; ASM-2093).

In the target the ownership is fixed by the architecture and not by the legacy tables: `template` and `merge_field` are P6 rwb-comms in the Ownership Map and on slide 41 of Architecture v5, the notice and its hold reason are P6's own rows, the task of the litigation officer is rwb-case's, the reference lists are rwb-case's under the DP-07 default ruling, the decision record is written through the local decision-record library, and the physical document of any kind stays with rwb-document. The Decision Log row DL28 that the legacy story cites reads "the document module owns templates and fields; Legal approves wording", which is a lower precedence source than the catalogue and is recorded as the loser of that disagreement, not followed quietly (GAP-1146; ASM-2093). This story is the Epic 8 administration surface on top of the Epic 1 core: it lists versions by code, language and state with paging, downloads a body, approves with a valid from date, withdraws with a reason, and raises the litigation officer task that R-LIT-04 requires. The Epic 1 upload-and-approve core of RWB-P6-E1034-APP is kept word for word and is not re-planned here (rule U2, Template and Rules §R6).

The two rules that give the story its value are R-LIT-04 and R-LIT-06. R-LIT-04 holds generation when the template of a notice is withdrawn and raises a task to the litigation officer, and R-LIT-06 resumes generation on the current version once Legal approves a new one. This story writes the state those rules act on and raises the task from its own held notices; it does not generate a notice, and the generation story RWB-P6-E1052-APP only reads the template state that this story sets.

The decoupling is the one the target fixes: the template version, its merge codes and its body reference are `rwb_comms` rows (DP-01); every approval and withdrawal writes one decision record through the local library on the shared topic before the change (DP-03); no `v_ace_*` view and no ACE row is read by this service, and the account and party facts a notice needs reach it through their owner's contract (DP-05, applied here as a prohibition); the base is `/api/recovery/comms/v1` (DP-13); and SCR-33 reaches the answers through the gateway-bff composite route (DP-19). The value sets of TSD P6 T3.2 for product group, channel and notice type are read with the version in force and are never written in code.

### 3. Preconditions

- RWB-P6-E1034-APP is done: the Epic 1 upload-and-approve core exists unchanged — the five template operations of the TSD appendix T-A.1 on the base of the service, the `template` and `merge_field` tables from RWB-P6-E1046-APP, the version state column with Draft, Approved and Withdrawn, the write-once body container and the `rwb.comms.template-admin` switch behind which the screen runs (rule U2, Template and Rules §R6).
- RWB-P6-AD017-CON is published: the five operations on `/api/recovery/comms/v1`, the template resource with its state vocabulary, the current-version rule, the approval and withdrawal rules, the reference-data and body-reference rows and the fakes, so this story builds against a fixed contract on Day 1.
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with the RWB-PLT-E1027-CON contract (DP-03); an approval and a withdrawal write one decision record each, and a failure of that write stops the change (R-UNI-39).
- The gateway-bff composite route of RWB-PLT-N001-CON is live for SCR-33 (DP-19), with the screen field list and the masking of the template list fixed by that contract and not here.
- The role set of TSD P6 T6.1 is enforced: Documents C for the upload, Documents R for the list and the body, Documents A for the approve and the withdraw. The rights come from the matrix and are not restated as code.
- The three value lists the upload and the list need — LOV-PRODUCT, LOV-CHANNEL and LOV-NOTICE of TSD P6 T3.2 — are available with the version in force. Their owner is rwb-case under the DP-07 default ruling, and this key carries no DP-07 and no C row for that read: the lists are Not specified in the source documents as a consumed contract of this story (GAP-1147; ASM-2094).
- The split of the surface between RWB-P6-E1034-APP and this story is Not specified in the source documents (GAP-1146; ASM-2093). This story assumes the Epic 1 core stays as built and delivers the Epic 8 administration surface: the paged list, the body download, the approve with a valid from date, the withdraw with a reason and the litigation officer task.
- The `rwb_comms` baseline is in place from RWB-P6-E1046-APP and RWB-P6-E1034-APP: `template`, `merge_field`, `notice` and the library objects `outbox_event`, `processed_event` and `idempotency_key` exist, and the per-service Flyway sequence runs in the service's own schema (ADR-021).
- The withdrawn-template task is a task of rwb-case raised on the rwb-case contract. Its task code, its target queue and the fields it carries are Not specified in the source documents (GAP-1149; ASM-2096).
- The decision code and the rule id that an approval or a withdrawal records, the content of the withdrawal reason and the field that holds it are Not specified in the source documents (GAP-1148; ASM-2095); no code and no new column is invented here.
- No build dependency outside rwb-comms and the platform contracts: the H rows are the contract baseline of this key, the two platform contracts and the Epic 1 story; the C rows are empty and therefore never block the build (Template and Rules §R5.7).

### 4. Flow

1. Legal counsel opens SCR-33 Template approval through the composite route and lists the template versions with `GET /api/recovery/comms/v1/admin/templates`, filtered by template code, language and state, one page at a time with the page size of the request.
2. The list answers with the version, its language, its product group, its channel, its notice type, its signature basis, its state, its approver and approval time, its valid from date and the record version, and no body and no personal data.
3. Legal counsel downloads the body of one version with `GET /api/recovery/comms/v1/admin/templates/{templateId}/content`; the answer is the binary body of the write-once container at `body_ref`, streamed as it is stored and never rendered here.
4. The litigation officer uploads a new version with `POST /api/recovery/comms/v1/admin/templates` and an Idempotency-Key; the upload runs the Epic 1 checks of RWB-P6-E1034-APP unchanged (required fields, file type and size, every merge code against the `merge_field` catalogue in force) and the new version is created in state Draft with the next version number of its code and language.
5. Legal counsel approves a Draft version with `POST /api/recovery/comms/v1/admin/templates/{templateId}/approve` and a valid from date; the service checks Documents A, that the approver is not the uploader, that the version is still Draft at the record version read, and that the valid from date is today or later.
6. The service writes the decision record of the approval through the local library in the same transaction, then sets state Approved with the approver, the approval time and the valid from date, and answers the Template of the updated version.
7. From the valid from date the approved version is the current version of its code and language: the current version is the Approved version with the latest valid from date on or before today. There is no set-current operation; earlier Approved versions stay readable on SCR-33.
8. Legal counsel withdraws an Approved version with `POST /api/recovery/comms/v1/admin/templates/{templateId}/withdraw` and a reason; the service checks Documents A, that the version is Approved at the record version read, and that the reason is not empty, writes the decision record of the withdrawal with the reason through the library, and sets state Withdrawn.
9. The service then reads its own held notices of that template version in `rwb_comms` — the `notice` rows whose `template_id` is the withdrawn version and whose `hold_reason` is `TEMPLATE_WITHDRAWN` — and raises one task per case to the litigation officer team through the rwb-case contract, with the template code, the version, the language, the case and the message MSG-P6-003. Generation for that code and language holds under R-LIT-04 until a new version is approved; no earlier version is made current again.
10. When Legal approves a new version of the same code and language, the current version moves to it on its valid from date and generation resumes on the current version under R-LIT-06. That move is this story's state; the resumption itself is the generation story's.
11. A withdrawn version offers no action on SCR-33 beyond reading it and its reason, and the reason is read from the decision record of the withdrawal because no column of `template` holds it.
12. A repeat of the approve or the withdraw POST with the same Idempotency-Key returns the first answer; an approve or a withdraw of a version in the wrong state answers 409 with MSG-P3-005 or MSG-GEN-004; a decision record that cannot be written leaves the state unchanged, answers 503 with MSG-P7-003 and raises an incident under R-UNI-39.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The approver uploads the version they approve | Refused; the version stays Draft | MSG-P7-002 | AC1 |
| X2 | Approve on a version that is not Draft, or withdraw on one that is not Approved | Refused; the state is unchanged | MSG-P3-005 | AC1, AC2 |
| X3 | The valid from date is before today | Approval refused; the version stays Draft | MSG-GEN-003 | AC1 |
| X4 | The withdrawal reason is empty | Withdrawal refused; the version stays Approved | MSG-GEN-001 | AC2 |
| X5 | A merge code of the uploaded body is not in the catalogue in force | Upload refused; nothing is stored | MSG-P6-006 | AC1 |
| X6 | The body file type or size is not allowed | Upload refused | MSG-P6-010 | AC1 |
| X7 | Two approvers act on the same version at once | The first wins; the second is refused with the record version | MSG-GEN-004 | AC1 |
| X8 | The decision record cannot be written for an approve or a withdraw | The state is unchanged; incident raised | MSG-P7-003 | AC1, AC2 |
| X9 | The role lacks the Documents right of the operation | Refused at the composite route and at the service | MSG-P4-002 | AC1, AC2 |
| X10 | The rwb-case task raise fails after a withdrawal | The withdrawal stands, the task is retried from the outbox-style retry of the call, and the failure is visible on the run record | MSG-GEN-006 | AC2 |
| X11 | A version or a code and language pair does not exist | 404 on the version and the body; an empty page for the list | None | AC1 |

X2 and X3 are the guards of the Epic 1 core and are restated here because the Epic 8 surface calls the same operations. The legacy story raises no path of its own beyond its two criteria; the other rows are the paths the five operations need and each one is named in the contract of RWB-P6-AD017-CON.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-AD017-CON, the two platform contracts and the Epic 1 story RWB-P6-E1034-APP; the rwb-case task raise and the reference lists are contract fakes from the first run |
| Negotiable | The value sets, the withdrawal reason rule, the task code and queue and the field that holds the reason are data or gaps; the state vocabulary, the operations and the current-version rule are fixed |
| Valuable | Legal approves wording once, on the version; a withdrawal holds generation and tells the litigation officer on the same day; no notice is generated from withdrawn wording |
| Estimable | Five operations, one screen with three states and a paged list, one task client and one decision-record path |
| Small | Fits one sprint with its tests, as the administration slice of the legacy key on top of the Epic 1 core |
| Testable | Each criterion runs against the contract fakes, and the four legacy test cases of the key keep their level and their data |

### 7. Acceptance criteria

```gherkin
Feature: Manage letter and notice templates — the rwb-comms administration surface

  Background:
    Given user "LIT-0101" holds RW-LITOFF
    Given user "LEG-0001" holds RW-LEGAL
    Given template "DEMAND-MTG" in language "TH" has version 2 Approved by "LEG-0001" with valid from 2026-11-01
    Given today is 2026-11-20

  Scenario: AC1 Approve (legacy RWB-AD-017 AC1)
    Given a new template version in Thai and English
    When Legal approves it
    Then notices generated from its date use it

  Scenario: AC2 Withdraw (legacy RWB-AD-017 AC2)
    Given a template withdrawn
    Given the rwb-case contract mock returns the task raised to the litigation officer team with MSG-P6-003 for template "DEMAND-MTG" "TH" version 3
    When a notice of that type is due
    Then generation holds and a task goes to the litigation officer (R-LIT-04)
```

The two criteria above are the two criteria of the legacy story RWB-AD-017, copied line for line with the origin tag on each scenario line; every legacy line and every legacy value is kept. One mock Given is added, in AC2, because that criterion names a fact of another owner: the task to the litigation officer is a task of rwb-case and is not a row this service writes (GAP-1149; ASM-2096). AC1 names no fact of another owner — the approval and the generation that reads the approved version are both of rwb-comms — so no mock line is added there, and the reading of the approved version by the generation of RWB-P6-E1052-APP is fixed in section 12.3 and section 19.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only an Approved version with an approver, an approval time and a valid from date is the current version of its code and language, and the current version is the Approved version with the latest valid from date on or before today | REQ-OCC-002; RWB-E1-034 BR1; RWB-P6-E1034-APP |
| BR2 | The person who uploaded a version cannot approve it | CTL-05; RWB-E1-034 BR2 |
| BR3 | Approval and withdrawal need Documents A, which only RW-LEGAL holds in the matrix | TSD P6 T6.1; RWB-E1-034 BR3 |
| BR4 | The valid from date of an approval is today or later | RWB-E1-034 BR5; MSG-GEN-003 |
| BR5 | Every merge code in the body of an uploaded version is in the `merge_field` catalogue in force, and the catalogue is this service's own table | RWB-E1-034 BR4; TSD P6 T3.1 |
| BR6 | A body is stored write-once and a change is a new version; the container of the body is the one RWB-P6-E1034-APP fixed and this story adds none | CTL-12; DL27; TSD P6 T3.1 (DF-REF-050) |
| BR7 | A withdrawn version holds generation for its code and language, no earlier version is made current again, and the litigation officer receives a task | R-LIT-04; MSG-P6-003 |
| BR8 | Generation resumes on the current version when a new version of the code and language is approved by Legal | R-LIT-06 |
| BR9 | A withdrawn version is terminal; a correction is a new version in Draft and not a return of the withdrawn one to Approved | RWB-E1-034 section 9; TSD P6 T3.1 |
| BR10 | The approval and the withdrawal write one decision record through the local decision-record library before the change, and a failed write stops the change | Principle 5; DP-03; R-UNI-39; MSG-P7-003 |
| BR11 | The template version, its merge codes and its body reference are `rwb_comms` rows; this service reads no other service's table and no `v_ace_*` view (DP-01, DP-05 applied as a prohibition) | Architecture v5 slide 41; DP-01; DP-05 |
| BR12 | The product group, channel, notice type, language and signature basis values are read with the version in force and never written in code (DP-07 default ruling, carried by the gap of this key) | TSD P6 T3.2; BR-P6-001; GAP-1147 |
| BR13 | The rights of the five operations are the Documents rights of the TSD (C, R, R, A, A) and not the Litigation right that the legacy permission table of the thin story names | TSD P6 T-A.1; TSD P6 T6.1; GAP-1148 |
| BR14 | The litigation officer task is rwb-case's row, raised through its contract with the template code, the version, the language, the case and MSG-P6-003; its task code and queue are not stated by a source | R-LIT-04; FSD P6 A2.1 AC-EXC-P6-001-02; GAP-1149 |
| BR15 | No template event exists in the event catalogue of the service, so approval and withdrawal are not published as events and the consumers of the state read it | Architecture v5 slide 42; GAP-1150 |
| BR16 | A list, a body download and every answer of this story carry IDs, codes, dates and state only; no name, address, identity number or account number is a column of `template` | Template and Rules §R7.2 s17; TSD P6 T3.1 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | Upload of a new version | The Epic 1 checks of RWB-P6-E1034-APP pass and the next version number of the code and language is free | Draft |
| Draft | Approve | Documents A; the approver is not the uploader; the valid from date is today or later; the record version is unchanged | Approved |
| Draft | Nothing else | A Draft version is not current and generates nothing | Draft |
| Approved | Withdraw | Documents A; the version is Approved at the record version read; the reason is not empty | Withdrawn |
| Approved | The valid from date arrives | The version is the Approved version with the latest valid from date on or before today | Approved, and current for its code and language |
| Withdrawn | Nothing | A withdrawn version is terminal and offers no action; a change is a new version in Draft | Withdrawn |
| Withdrawn | A new version of the code and language is approved and its valid from date arrives | The new version is Approved with a valid from date on or before today | The new version is current and generation resumes under R-LIT-06 |

This state machine is the version state of `template` and nothing else. The notice state, the hold reason of a held notice and the resumption of a held generation are the rows and the behaviour of RWB-P6-E1052-APP; this story writes the template state those rows read, and the task it raises on a withdrawal is the fact R-LIT-04 names. The current version is a derived fact and not a state: "set current" is not an operation, as the Epic 1 contract of RWB-P6-E1034-APP resolves it, and this story adds no operation that would set it.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LEGAL, Legal counsel | Documents CRUA in the matrix of TSD P6 T6.1: approves with a valid from date (right A), withdraws with a reason (right A), uploads (right C), lists and downloads (right R); cannot approve their own upload |
| RW-LITOFF, litigation officer | Documents CRU: uploads a version (right C), lists and downloads (right R), and receives the task raised on a withdrawn template |
| RW-ENFORCE, enforcement owner | Documents CRU: uploads (right C), lists and downloads (right R) |
| RW-CASEOWN, case owner | Documents CRU: uploads (right C), lists and downloads (right R) |
| RW-COMPLY, Compliance and PDPA officer | Documents RU: reads the list and the body, and maintains the fields the matrix gives it |
| RW-TEAMMGR, team manager | Documents R: reads the list and the body |
| RW-AUDIT, internal audit | Documents R: reads the list, the versions and their approval and withdrawal records |
| RW-CONDUCT, conduct and QA officer | Documents R: reads the list and the body |
| RW-PLATADM, platform administrator | Documents R: reads the list and the versions for support; operates the switch behind the platform controls |
| rwb-comms service identity | Reads and writes its own `rwb_comms` rows, streams the body of the container at `body_ref` and writes the outbox row (DP-02) |
| Decision-record library identity | Writes the local decision record of an approval and of a withdrawal and relays it on `rwb.decision-record.v1` (DP-03) |

Only RW-LEGAL holds Documents A in the matrix of TSD P6 T6.1, so the approve and the withdraw refuse every other role with MSG-P4-002; the legacy permission table of the thin story names the Litigation right and a list of roles that includes roles without Documents A, and that table is the loser of the gap of this key (GAP-1148; ASM-2095). The authorise contract of rwb-access is not in the pattern set of this story: the capability area and the right of each operation are declared in RWB-P6-AD017-CON and enforced at gateway-bff, which asks rwb-access, so no P4 dependency is declared here.

### 11. Data

| BR Field ID | Entity in `rwb_comms` | Field | Read or write |
|---|---|---|---|
| DF-REF-045 | template | id | Write on upload, read on every operation |
| DF-REF-046 | template | template_code | Write on upload, read on the list and the filters |
| DF-REF-047 | template | template_version | Write on upload, read |
| DF-REF-048 | template | language | Write on upload, read on the list and the filters |
| DF-REF-049 | template | product_group | Write on upload, read |
| DF-REF-050 | template | body_ref | Write on upload, read on the body download |
| DF-REF-051 | template | approved_by_legal | Write on approval, read |
| DF-REF-063 | template | approved_by | Write on approval, read |
| DF-REF-064 | template | approved_at | Write on approval, read |
| DF-REF-065 | template | valid_from | Write on approval, read on the current-version rule |
| DF-REF-066 | template | channel | Write on upload, read |
| DF-REF-067 | template | notice_type | Write on upload, read |
| DF-REF-068 | template | signature_basis | Write on upload, read |
| DF-REF-069 | template | merge_codes | Write on upload, read |
| Standard column | template | state, version, created_by, created_at, updated_by, updated_at | Write on every state move, read for the optimistic lock |
| DF-REF-253 | merge_field | merge_code | Read, against the catalogue in force |
| DF-REF-259 | merge_field | catalog_version | Read, the version in force of the catalogue |
| DF-LEG-031 | notice | template_id | Read, to find the notices of a withdrawn version |
| DF-LEG-032 | notice | hold_reason | Read, to find the notices held with `TEMPLATE_WITHDRAWN` |
| DF-LEG-018 | notice | notice_type | Read, to name the notice type of a held notice in the task |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, template version, reason, decided at, hash chain | Write on approval and on withdrawal |
| DF-WRK-017 to DF-WRK-026 | task, owned by rwb-case | task code, case, element, status | Not read and not written; the task is raised through the rwb-case contract and never as a table |

The withdrawal reason has no column: no source gives one on `template` (GAP-1148; ASM-2095). It is recorded in the decision record of the withdrawal through the library and read back from there by SCR-33, so the template row stays the shape TSD P6 T3.1 gives it. The list needs one index, `ix_template_code_lang_state` on `template (template_code, language, state)`, added by one per-service Flyway step in `rwb_comms` (ADR-021); the unique constraint on the code and the version number is the one RWB-P6-E1046-APP created and this story adds none. No column of `template` holds a name, an address, an identity number or an account number, and the body at `body_ref` is a reference into the write-once container and never a joined row of another schema. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The paths are the five template operations of the TSD appendix T-A.1, API-P6-003 to API-P6-007, as the Ownership Map holds them for P6; the legacy endpoint table of the thin story names the notice request and the notice read instead and names no template operation (GAP-1146; ASM-2093). The shapes are those fixed in RWB-P6-AD017-CON; this story implements them and adds no path.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/templates` | API-P6-003: list template versions by code, language and state with `page` and `size`, 200 with the TemplatePage; scope applied | Documents, right R | Not applicable |
| POST | `/admin/templates` | API-P6-004: upload a new template version in state Draft, 201 with the Template; multipart file with `templateCode`, `language`, `productGroup`, `channel`, `noticeType`, `signatureBasis` and `mergeCodes` | Documents, right C | Idempotency-Key header, answer kept 24 hours |
| GET | `/admin/templates/{templateId}/content` | API-P6-005: download the body of a template version, 200 as a binary stream from the write-once container at `body_ref` | Documents, right R | Not applicable |
| POST | `/admin/templates/{templateId}/approve` | API-P6-006: record the Legal approval of a Draft version with its valid from date, 200 with the Template in state Approved | Documents, right A | Idempotency-Key header, answer kept 24 hours |
| POST | `/admin/templates/{templateId}/withdraw` | API-P6-007: withdraw an Approved version with a reason, 200 with the Template in state Withdrawn, and the task of R-LIT-04 | Documents, right A | Idempotency-Key header, answer kept 24 hours |

Errors on the five operations: 401 no session; 403 the role lacks the Documents right (MSG-P4-002); 404 the version or the body is absent, with no message; 409 the version is in the wrong state (MSG-P3-005) or was changed by another person (MSG-GEN-004) or is being approved by its uploader (MSG-P7-002); 413 the body is larger than the allowed size; 415 the body type is not allowed (MSG-P6-010); 422 a required field is empty (MSG-GEN-001), a merge code is not in the catalogue (MSG-P6-006) or the valid from date is before today (MSG-GEN-003); 503 the decision was not recorded (MSG-P7-003) or a consumed answer did not come back in time (MSG-GEN-006).

Request and answer shapes. TemplatePage carries `items` of Template and the paging facts; Template carries `id`, `templateCode`, `templateVersion`, `language`, `productGroup`, `channel`, `noticeType`, `signatureBasis`, `mergeCodes`, `state`, `approvedBy`, `approvedAt`, `validFrom`, `createdBy`, `createdAt` and `version` as the Epic 1 contract of RWB-P6-E1034-APP names them, and the exact field list, types and required flags of the list and the page are Not specified in the source documents beyond the query of API-P6-003 and the fields of TSD P6 T3.1 (GAP-1148; ASM-2095). TemplateApproval carries `validFrom`; TemplateWithdrawal carries `reason`, and no field of `template` holds it (GAP-1148; ASM-2095).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | the list read of RWB-P3-E1043-CON, `GET /api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS with the version in force, for the upload checks and the list filters; faked. This key carries no DP-07 and no C row for the read, and the row is Not specified in the source documents as a dependency of this story (GAP-1147; ASM-2094) |
| POST | the task raise of RWB-P6-AD017-CON for the held notices of a withdrawn version | P3 rwb-case | One task per case to the litigation officer team under R-LIT-04 with the template code, the version, the language, the case, the notice type and MSG-P6-003; faked. The operation, the task code, the target queue and the task fields are Not specified in the source documents (GAP-1149; ASM-2096) |

Two rows and no third: the notice rows a withdrawal looks at are this service's own `rwb_comms` rows, the body is streamed from the container that RWB-P6-E1034-APP fixed and is not a cross-service read, and the authorise answer is asked by gateway-bff and not by this service (section 10). Every row is one hop with the platform's 2 s budget and a breaker per downstream, and a missing answer never approves, never withdraws and never marks a notice as served (ADR-020). No row reads a table and no row reads a `v_ace_*` view (DP-05, DP-01).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and codes only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | template version | decision record reference, decision code, rule id, template code, template version, language, state after the change, decided at; the local decision-record library publishes it (DP-03) |

This is the only event element of the story, and it is written by the library and not by a new event of this service. No template event exists in the catalogue of Architecture v5 slide 42 — the three events on `rwb.comms.events.v1` are NoticeGenerated, NoticeDispatched and NoticeDelivered — so this story publishes no `rwb.comms.*` event and invents none (GAP-1150; ASM-2097). A consumer that needs to know that wording changed reads the template state through the read operations of this service.

#### 12.4 Events consumed

None. This story consumes no event: an approval and a withdrawal are user actions, and the state they set is read by its own consumers when they run.

#### 12.5 Workflows and activities

None. The five operations are synchronous request and answer calls; no workflow, no activity and no durable timer is registered by this story. The task raise and the decision record are calls made inside the transaction of the state change, and a failure of either is answered as section 5 states.

#### 12.6 Schedules

None. Nothing in this key runs on a clock: the version state moves when Legal acts, and no Schedule, no Quartz row and no shared job table is declared (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| template | P6 (rwb_comms) | The version, its language, product group, channel, notice type, signature basis, merge codes, body reference, approver, approval time, valid from date and state; written here and by RWB-P6-E1034-APP |
| merge_field | P6 (rwb_comms) | The merge catalogue; read only here, against the version in force |
| notice | P6 (rwb_comms) | Read only here, to find the held notices of a withdrawn version; written by RWB-P6-E1052-APP |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The record of an approval and of a withdrawal, with the withdrawal reason (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The envelope of the decision record and the idempotency of the three POST operations |

Not owned and never read: `recovery_case`, `task`, `timer`, `queue`, `assignment`, `reference_row`, `reference_version` and `lov_value` (P3), `document`, `document_custody`, `document_text` and `signature_request` (P5), `decision_log_entry`, `approval` and `rule_row` (P7), `role` and `permission` (P4), `interaction` (P1), `outbound_item` and `interface_config` (P2), `deviation` (S8), `legal_action` (S4). The task and the reference lists are reached through the contracts of their owners, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-case list fake (RWB-P3-E1043-CON) | The reference lists of the upload checks and the list filters | LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE and LOV-SIGNATURE-BASIS with the version in force; a list that does not contain a value the body uses; a delayed answer beyond 2 s |
| rwb-case task fake | The task raise on a withdrawal | A task accepted for case `RC-2026-000321` with template `DEMAND-MTG` TH version 3 and MSG-P6-003; a refused raise; a delayed answer beyond 2 s |
| decision-record library stub | The approval and the withdrawal record | A healthy chain and outbox, and a stopped chain for X8 and TC-AD-017-04 |
| Body container stub | The write-once container at `body_ref` | A stored DOCX body for `DEMAND-MTG` TH version 3; a missing body for a version whose reference is stale |

The fakes are derived from the published contracts of RWB-P6-AD017-CON, and the drift test of that story fails a build in which a fake and the document disagree. The two rows whose operation no source names carry the placeholder of their gap (GAP-1147; GAP-1149).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 2 consumed | List, upload, body download, approve and withdraw provided; the reference lists and the task raise consumed; one hop, 2 s |
| Kafka | 1 declared, none consumed | `rwb.decision-record.DecisionRecorded.v1` through the local library; no template event exists to publish |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | The body is streamed from the write-once container through its reference and no file is produced by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `templateadmin`, Java package `th.co.scb.ace.workbench.recovery.comms.templateadmin`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition with no exception here: this service reads no `v_ace_*` view and no ACE row, and the account, party and contact facts that a generated notice needs reach it through the owner's contract at generation time and never through this story. That is why no P1 dependency is declared in this key.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemplateAdminController | Controller | The five operations of 12.1, the query and the multipart parsing, the Idempotency-Key and the problem mapping for 401, 403, 404, 409, 413, 415, 422 and 503 |
| TemplateCatalogQueryService | Service | The paged list by code, language and state, the current-version rule and the read of one version |
| TemplateApprovalService | Service | Approve and withdraw: the Documents right, the self-approval refusal, the state guard, the valid from date, the optimistic lock and the reason check; reuses the Epic 1 checks of RWB-P6-E1034-APP unchanged |
| TemplateBodyReader | Service | Streams the body of the write-once container at `body_ref` with the type the container holds, and refuses a stale or missing reference |
| HeldNoticeFinder | Service | Reads the `notice` rows of `rwb_comms` held with `TEMPLATE_WITHDRAWN` under the withdrawn `template_id` and groups them by case |
| LitigationTaskClient | Adapter | The task raise on the rwb-case contract for each case of a withdrawn version |
| TemplateDecisionRecorder | Service | Writes the local decision record of an approval and of a withdrawal, with the reason, before the state change |
| MergeCatalogReader | Service | Reads `merge_field` with the catalogue version in force for the upload check |
| TemplateAdminScreen | React component | SCR-33 for the Epic 8 surface: the paged list, the filters, the version detail, the body download, the upload form, the approve and withdraw dialogs with the reason, and the three states |

**Database and migrations**

- Reads and writes `template` and `merge_field`, reads `notice`, and writes the local decision record and the library objects, all in schema `rwb_comms`; reads no other schema.
- Migration in this story: `AD017_1__template_admin_index.sql` adds `ix_template_code_lang_state` on `template (template_code, language, state)` for the paged list. No new table and no new column: the withdrawal reason is in the decision record (section 11).
- The version number of a new version is assigned inside a transaction with `SELECT ... FOR UPDATE` on the highest version of the code and language, as RWB-P6-E1034-APP does; the unique constraint of RWB-P6-E1046-APP stops a duplicate.

**Configuration and reference data**

- `rwb.comms.template-admin-surface` = on, read as a parameter: off leaves only the Epic 1 actions of the switch `rwb.comms.template-admin` and offers no paged administration list.
- `rwb.comms.template.page-size` = the default page size of the list, read as data.
- `rwb.comms.template.allowed-types` and `rwb.comms.template.max-size-mb` are the Epic 1 values of RWB-P6-E1034-APP and are not restated here.
- The three value lists LOV-PRODUCT, LOV-CHANNEL and LOV-NOTICE are read with the version in force and never written in code (GAP-1147; ASM-2094).
- The task code and the target queue of the litigation officer task are read as configuration and stay unset until the rwb-case owner publishes them (GAP-1149; ASM-2096).

**Build steps**

1. TemplateAdminController and TemplateCatalogQueryService over the list and the read, with the paging, the filters and the 404; test the list against the fakes.
2. TemplateBodyReader over the body download with a stale reference and a missing container entry.
3. TemplateApprovalService over the approve path, reusing the Epic 1 checks: the right, the self-approval, the state, the valid from date and the lock; tests for X1, X2, X3, X7.
4. TemplateApprovalService over the withdraw path: the right, the state, the reason and the record, with the decision record written before the state change; tests for X4, X8.
5. HeldNoticeFinder and LitigationTaskClient: the held notices of the withdrawn version, one task per case, and the retry of a refused raise; tests for X10 and AC2.
6. TemplateDecisionRecorder and the fail-closed path: a failed record leaves the state unchanged, answers 503 with MSG-P7-003 and raises the incident of R-UNI-39; test for TC-AD-017-04.
7. MergeCatalogReader and the upload path behind the Epic 1 operation, with the catalogue version in force; tests for X5 and X6.
8. TemplateAdminScreen on SCR-33 with the three states, the common Loading and Error states, the message texts of section 14 in English and Thai, and the hidden actions of a role that lacks the right; a browser test of the list, the download and the withdraw path.

**Feature switch.** `rwb.comms.template-admin-surface`, read as a parameter; off refuses the paged administration list and leaves the Epic 1 actions as they were built.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-AD017-CON stay green, a SIT week shows every approved version current from its valid from date and no earlier version made current after a withdrawal, every withdrawal with one decision record naming the reason and one task per held case, and no notice generated from a withdrawn version.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-003 | A withdrawn version is asked for by the generation of a notice, and on the task of a withdrawal | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-005 | A version with no Legal approval is asked to become current | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-006 | A merge code of the uploaded body is not in the catalogue in force | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-P6-010 | The body file type is not allowed | This template file type cannot be loaded. Use {types}. |
| MSG-GEN-001 | A required field is empty, including the withdrawal reason | Enter {field}. |
| MSG-GEN-003 | The valid from date is before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Another person changed the version first | Someone else changed this record. Reload it to see their change. |
| MSG-P7-002 | The uploader approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | The decision record of an approval or a withdrawal cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-005 | Approve on a version that is not Draft, or withdraw on one that is not Approved | This case cannot move to {state} from {current}. |
| MSG-P4-002 | The role lacks the Documents right of the operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A consumed call, the reference lists or the task raise, does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P6-004 | A notice was acknowledged by WIN for registered mail; named by the legacy validation table and owned by the notice dispatch | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | A contact stop blocks a notice; named by the legacy validation table and owned by the notice dispatch | Contact with this customer is stopped for {reason}. |

Every text above is copied unchanged from the Epic 1 story RWB-E1-034 and its contract RWB-P6-E1034-APP where the message already exists there, including MSG-P6-003, MSG-P6-005, MSG-P6-006, MSG-P6-010, MSG-GEN-001, MSG-GEN-003, MSG-GEN-004, MSG-P7-002, MSG-P7-003, MSG-P3-005 and MSG-P4-002. MSG-P6-004 and MSG-P6-001 are named by the legacy validation table of RWB-AD-017, belong to the notice operations of RWB-P6-E1052-APP, and are listed here unchanged so that no value of the legacy table is lost. MSG-GEN-006 is the platform message of a call that does not answer in time.

### 15. Screens and states

SCR-33 Template approval, served through the gateway-bff composite route (DP-19), with the Epic 8 administration surface of this story:

| State | What the user sees and does |
|---|---|
| Draft | The litigation officer sees the uploaded version, its merge codes and the body download. Legal counsel sees Approve with a valid from date |
| Approved | Everyone with Documents R sees the version, its approver, its approval time and its valid from date, and whether it is current. Legal counsel sees Withdraw with a reason |
| Withdrawn | The version shows its withdrawal reason and its record; no action is offered, and the litigation officer sees the task raised for the cases whose notices are held |

The list offers the filters on template code, language and state and moves one page at a time. The common states Loading and Error apply to the list, the detail, the download, the approve and the withdraw. The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and are not restated here; the screen is the one the Epic 1 story builds in RWB-P6-E1034-APP behind its flag, and this story adds the paged administration surface to it.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-017-01 | AC1, BR1, BR4, BR7 | End to end | DEMAND-MTG TH version 2 Approved; the list of the versions of DEMAND-MTG TH; the body download of version 2; version 3 Draft; approval by LEG-0001 with valid from 2026-11-20 |
| TC-AD-017-02 | AC2, BR7, BR8, BR14 | End to end | DEMAND-MTG TH version 3 Approved and current, withdrawn by LEG-0001 with a reason; a notice of DEMAND-MTG TH held with TEMPLATE_WITHDRAWN for case RC-2026-000321; the rwb-case task fake returns the task with MSG-P6-003 |
| TC-AD-017-03 | Access, BR3, BR13 | Component | RW-LITOFF holds Documents CRU and sends POST /admin/templates/{templateId}/approve; refused with 403 and MSG-P4-002 |
| TC-AD-017-04 | Principle 5, BR10 | NFR | The decision-record library stopped on 10 approvals and 10 withdrawals in a row; no version changes state and every answer is 503 with MSG-P7-003 |

The four cases keep their legacy IDs, their legacy order and their legacy coverage of the legacy story, with the level of each mapped to the target vocabulary: Approve and Withdraw are end-to-end journeys of the service, Access is a component test and Principle 5 is a non-functional test. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The Epic 1 cases TC-E1-034-01 to TC-E1-034-11 stay with RWB-P6-E1034-APP and are not copied here; the contract cases TC-P6-AD017-CON-01 to TC-P6-AD017-CON-07 stay with RWB-P6-AD017-CON.

### 17. Guardrails

- No business value in code: the value sets of the product group, the channel, the notice type and the signature basis, the page size, the allowed body types, the size limit and the task code are data or configuration read with the version in force.
- No personal data in events, logs, tests or prompts: template codes, versions, languages, states, dates and synthetic user IDs only. The body is a template wording and the body reference is never exchanged for a name or an address.
- No read of another service's tables and no `v_ace_*` read of this service: the task and the reference lists arrive on the owner's contract, and the account and party facts of a notice never reach this story (DP-01, DP-05).
- The record comes before the change: an approval and a withdrawal write the decision record through the library in the same transaction, and a failed write leaves the state unchanged with an incident under R-UNI-39.
- A withdrawn version is terminal: no operation makes it current again and no earlier version becomes current by fallback (R-LIT-04, R-LIT-06).
- The body is written once and read unchanged: a correction is a new version, and this story adds no second container and no overwrite.
- The screen hides the actions a role does not hold and the service checks the Documents right on every call; no right is decided on the screen.
- One base and one topic: `/api/recovery/comms/v1` and `rwb.comms.events.v1`; this story adds no path outside the base and publishes no event of its own (DP-13).
- Every consumed call is one hop with the platform's 2 s budget, and a timeout never approves a version, never withdraws one and never marks a task as raised.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-AD-017, disposition Split (rework) |
| Legacy criteria owned here | AC1 (Approve) and AC2 (Withdraw), each tagged (legacy RWB-AD-017 AC1) and (legacy RWB-AD-017 AC2) in section 7 |
| Test cases | TC-AD-017-01 to TC-AD-017-04, the four cases of the legacy story in its order, with the Level column added |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership) |
| Rules | R-LIT-04, R-LIT-06, R-UNI-39 |
| Operations | API-P6-003 to API-P6-007 of TSD P6 appendix T-A.1, on the base `/api/recovery/comms/v1` |
| Gaps and assumptions of this key | GAP-1146 to -5 with ASM-2093 to -5 |

The legacy story carries no requirement ID of its own: its metadata row names the decision DL28 and no feature. The requirement that the wording be versioned with the Legal approval recorded against the version is REQ-OCC-002, it is held by RWB-P6-E1034-APP, and this story restates none of it. The data of the legacy table names `task`, `legal_action` and `notice` beside `template`; `task` is P3's, `legal_action` is S4's and `notice` is this service's own, and section 11 keeps the template fields of that table and reads the notice fields it needs.

### 19. Out of scope

- RWB-P6-E1034-APP keeps the Epic 1 upload-and-approve core unchanged: the five operations as they are built there, the upload checks, the self-approval refusal, the valid from guard, the body container, the state column and the `rwb.comms.template-admin` switch. This story adds the Epic 8 administration surface on top of that core and re-plans none of it (rule U2, Template and Rules §R6).
- Notice generation: RWB-P6-E1052-APP and RWB-P6-E1052-CON. Notice generation only reads the template state this story sets; it decides the hold of a notice under R-LIT-04, it resumes generation under R-LIT-06, and it never writes a template version.
- The notice request and the notice read: RWB-P6-E1052-APP. The legacy endpoint table of the thin story names them and not a template operation (GAP-1146; ASM-2093).
- The template and merge field catalogue, its load checks and its data: RWB-P6-E1046-APP and RWB-P6-E1046-CON. This story reads the catalogue and adds no row to it.
- The task row, the queue, the assignment and the timer of the litigation officer: rwb-case (P3). This story calls the task contract and reads no task table (GAP-1149; ASM-2096).
- The reference lists and their versions: rwb-case (P3) under the DP-07 default ruling. This key carries no DP-07 and no C row for that read (GAP-1147; ASM-2094).
- The physical document of a template body, its custody, its retention and its signature: rwb-document (P5). This story streams a body through the reference the Epic 1 container holds and reads no P5 table.
- The central decision ledger, the approvals and the rule packages: rwb-decision (P7). This story writes the local record through the library and reads no ledger row.
- A template event and the event catalogue change it would need: no source names one (GAP-1150; ASM-2097).
- The gateway-bff composite route, the screen field list and the masking: RWB-PLT-N001-CON and the stories that own each screen.
- The deployment, the dashboards, the alerts and the runbook of this capability, which this key carries as no story of its own.
