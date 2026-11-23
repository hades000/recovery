# RWB-P6-E1034-APP Letter template management

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1034-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-034 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP13, DP19 |
| Parallel lane | L-P6-A |
| Ready to start | After RWB-P6-E1046-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P6-E1046-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P1-E1015-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-001, FR-P6-002, FR-P6-003, FR-P6-004, FR-P6-005, FR-P6-012, FR-P6-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: moved from RWB-E1-034 to rwb-comms, with the five template administration operations on base `/api/recovery/comms/v1` and the screen behind gateway-bff. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **a screen to upload a template version, have Legal counsel record the approval and set it current**, so that **templates are managed without a developer**.

### 2. Business rationale

A template change today needs a person outside Legal to edit a file and send it round, and nothing records which wording was approved. This story gives the litigation officer an upload and Legal counsel an approve and withdraw action on SCR-33 Template approval, with the approver and date held on the version. It serves REQ-OCC-002 and control CTL-14 (every notice from the current Legal-approved version), and removes the developer from template changes.

### 3. Preconditions

- RWB-E1-046 is done: the template and merge_field tables, the load checks and the TemplateCatalog interface exist.
- RWB-E1-015 is done: the freshness stamp shows on screens that read data products.
- The merge field catalog is loaded, with codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE" in the synthetic set.
- The uploader holds RW-LITOFF or RW-LEGAL (Documents C); the approver holds RW-LEGAL (Documents A).
- The ACE storage pattern with a write-once container is available for template bodies (DL27).

### 4. Flow

1. Litigation officer: opens SCR-33 Template approval and chooses the template code and language, or a new code.
2. Litigation officer: uploads the DOCX body and enters product group, channel, notice type, signature basis and the merge codes used.
3. System: checks the role (Documents C), the required fields, the file type and size, and every merge code against the catalog (MergeCodeScanner from RWB-E1-046).
4. System: stores the body write-once, creates the next version number in state Draft and shows it in the list.
5. Legal counsel: opens the Draft version, reads the body and the merge codes, enters the valid from date and approves.
6. System: checks the role (Documents A), that the approver is not the uploader (CTL-05), that the version is Draft and that valid from is not before today; sets state Approved with approver and approval time.
7. System: from valid from, TemplateCatalog returns this version as current; earlier Approved versions stay readable on SCR-33.
8. Legal counsel: may withdraw an Approved version with a reason; the system sets state Withdrawn and generation for that code and language holds (R-LIT-04).
9. System: writes every upload, approval and withdrawal to the ACE audit log with the user, the version and the time.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Set current is chosen on a version with no approver | Refused; the version stays Draft | MSG-P6-005 | AC2 |
| X2 | The uploader of a version tries to approve it | Refused; the version stays Draft | MSG-P7-002 | AC3 |
| X3 | The body uses a merge code not in the catalog | Upload refused; nothing stored | MSG-P6-006 | AC4 |
| X4 | Template code or language is empty | Upload refused | MSG-GEN-001 | AC5 |
| X5 | The file is not a DOCX file | Upload refused | MSG-P6-010 | AC6 |
| X6 | Valid from is before today | Approval refused | MSG-GEN-003 | AC7 |
| X7 | Legal withdraws the current version | Version Withdrawn; generation holds | MSG-P6-003 | AC8 |
| X8 | Two approvers act on the same version at once | The first wins; the second is refused | MSG-GEN-004 | AC9 |
| X9 | Approve is sent twice with the same Idempotency-Key | The second returns the first result; nothing changes | None | AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the catalog (RWB-E1-046) only; generation (RWB-E1-052) is separate |
| Negotiable | Layout of SCR-33 follows the ACE components (DL08, DL31); the behavior is fixed here |
| Valuable | Legal approves wording in the Workbench, and the approval is on the version |
| Estimable | Five endpoints, one screen with three states |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion is an API or screen test with synthetic templates |

### 7. Acceptance criteria

```gherkin
Feature: Letter template management

  Background:
    Given user "LIT-0101" holds RW-LITOFF
    Given user "LEG-0001" holds RW-LEGAL
    Given template "DEMAND-MTG" in language "TH" has version 2 Approved by "LEG-0001" with valid from 2026-11-01
    Given today is 2026-11-20

  Scenario: AC1 New version (legacy RWB-E1-034 AC1)
    Given "LIT-0101" uploads "demand-mtg-th-v3.docx" for "DEMAND-MTG" "TH" using merge codes "CASE_NO" and "TOTAL_OUTSTANDING"
    Given version 3 is created in state "Draft"
    When "LEG-0001" approves version 3 with valid from 2026-11-20
    Then version 3 has state "Approved", approver "LEG-0001" and an approval time on 2026-11-20
    Then TemplateCatalog returns version 3 as current for "DEMAND-MTG" "TH" on 2026-11-20
    Then version 2 stays readable on SCR-33 with approver "LEG-0001"

  Scenario: AC2 Approval required (legacy RWB-E1-034 AC2)
    Given version 3 of "DEMAND-MTG" "TH" is in state "Draft" with no approver
    When "LIT-0101" chooses set current on version 3
    Then the system refuses it with MSG-P6-005 naming "DEMAND-MTG" version 3
    Then version 2 stays current

  Scenario: AC3 The uploader cannot approve the version (legacy RWB-E1-034 AC3)
    Given "LEG-0001" uploaded version 4 of "RECALL-SSME" "TH"
    When "LEG-0001" approves version 4
    Then the system refuses it with status 409 and MSG-P7-002
    Then version 4 stays "Draft"

  Scenario: AC4 Unknown merge code refused at upload (legacy RWB-E1-034 AC4)
    Given "LIT-0101" uploads a body for "DEMAND-HP" "TH" that uses the merge code "LINE_ID"
    Given "LINE_ID" is not in the merge field catalog
    When the upload is sent
    Then the system refuses it with status 422 and MSG-P6-006 naming "LINE_ID"
    Then the system creates no version of "DEMAND-HP" and no file is stored

  Scenario: AC5 Required field empty (legacy RWB-E1-034 AC5)
    Given "LIT-0101" uploads a body with no template code
    When the upload is sent
    Then the system refuses it with status 422 and MSG-GEN-001 naming "template code"

  Scenario: AC6 File type not allowed (legacy RWB-E1-034 AC6)
    Given "LIT-0101" uploads "demand.pdf" for "DEMAND-MTG" "TH"
    When the upload is sent
    Then the system refuses it with status 415 and MSG-P6-010 naming "DOCX"

  Scenario: AC7 Valid from before today (legacy RWB-E1-034 AC7)
    Given version 3 of "DEMAND-MTG" "TH" is "Draft"
    When "LEG-0001" approves it with valid from 2026-11-19
    Then the system refuses it with status 422 and MSG-GEN-003 naming "valid from" and "today"

  Scenario: AC8 Withdraw the current version (legacy RWB-E1-034 AC8)
    Given version 3 of "DEMAND-MTG" "TH" is Approved and current
    When "LEG-0001" withdraws version 3 with reason "Wording under review"
    Then version 3 has state "Withdrawn"
    Then TemplateCatalog throws TemplateWithdrawnException for "DEMAND-MTG" "TH" with MSG-P6-003
    Then the system does not mak version 2 current again

  Scenario: AC9 Two approvals at the same time (legacy RWB-E1-034 AC9)
    Given version 3 of "DEMAND-MTG" "TH" is "Draft" at record version 1
    Given "LEG-0001" and "LEG-0002" both open it
    When both approve within the same second
    Then one approval succeeds
    Then the system refuses the other with status 409 and MSG-GEN-004

  Scenario: AC10 Repeated approval request (legacy RWB-E1-034 AC10)
    Given "LEG-0001" approved version 3 with Idempotency-Key "7f1c0d2e-0001"
    When the same request is sent again with Idempotency-Key "7f1c0d2e-0001"
    Then the response is the first response with status 200
    Then the audit log holds one approval for version 3
```

The ten criteria are the legacy scenarios AC1 to AC10 of RWB-E1-034, copied word for word with their values, IDs, statuses and messages, and each carries its origin tag. No Given line is added and no legacy line is changed. `TemplateCatalog` is the legacy name of the current-version read that this story serves behind the five operations of section 12.1, and the exception name `TemplateWithdrawnException` is carried on MSG-P6-003.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only an Approved version with an approver and approval time can become current | REQ-OCC-002; CTL-14 |
| BR2 | The person who uploaded a version cannot approve it | CTL-05; roles.txt separation of duty |
| BR3 | Approval needs Documents A, held by Legal counsel | roles.txt permission matrix; DL28 |
| BR4 | Every merge code in the body is in the merge field catalog in force | RWB-E1-046 BR4; Principle 1 |
| BR5 | Valid from is today or later | MSG-GEN-003 rule; refdata.txt change process, step 5 |
| BR6 | A withdrawn version holds generation until a new version is approved; no fallback to an earlier version | R-LIT-04, R-LIT-06 |
| BR7 | Template bodies are stored write-once; a change is a new version | CTL-12; DL27 |
| BR8 | Allowed body file types are a configuration list, DOCX in Epic 1 | Principle 1 |

### 9. State transitions

None. This story does not change a case status. It changes the template version state (standard column state):

| From | Event | Condition | To |
|---|---|---|---|
| None | Upload | Checks pass | Draft |
| Draft | Approve | Approver is Legal counsel and not the uploader; valid from today or later | Approved |
| Approved | Withdraw | Reason entered | Withdrawn |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Uploads a version (Documents C), reads templates (Documents R) |
| RW-LEGAL, Legal counsel | Uploads, approves and withdraws a version (Documents CRUA); cannot approve own upload |
| RW-CASEOWN, RW-TEAMMGR and other roles with Documents R | Read templates on SCR-33 |
| RW-COMPLY, Compliance and PDPA officer | Reads templates (Documents R) |

No approval level from the delegation of authority applies; Legal approval of wording is a Documents A right.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-045 | template | id | Write |
| DF-REF-046 | template | template_code | Write |
| DF-REF-047 | template | template_version | Write |
| DF-REF-048 | template | language | Write |
| DF-REF-049 | template | product_group | Write |
| DF-REF-050 | template | body_ref | Write |
| DF-REF-051 | template | approved_by_legal | Write |
| DF-REF-063 | template | approved_by | Write |
| DF-REF-064 | template | approved_at | Write |
| DF-REF-065 | template | valid_from | Write |
| DF-REF-066 | template | channel | Write |
| DF-REF-067 | template | notice_type | Write |
| DF-REF-068 | template | signature_basis | Write |
| DF-REF-069 | template | merge_codes | Write |
| Standard column | template | state | Write |
| Standard column | template | created_by | Write |
| DF-REF-253 | merge_field | merge_code | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). The five operations are the TSD P6 appendix T-A.1 rows API-P6-003 to API-P6-007 re-based on the per-service base, with the purpose, request and answer, errors, authorization and idempotency of the T-A.2 rows.

| Method | Path | API ID | Purpose | Request and answer | Access | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/admin/templates` | API-P6-003 | List template versions by code, language and state | Query: code, language, state, page, size; answer 200 `TemplatePage` of `Template` | Documents, right R, scope applied | Not applicable |
| POST | `/admin/templates` | API-P6-004 | Upload a new template version in state Draft | Multipart: file, templateCode, language, productGroup, channel, noticeType, signatureBasis, mergeCodes; answer 201 `Template` in state DRAFT | Documents, right C, scope applied | `Idempotency-Key` header |
| GET | `/admin/templates/{templateId}/content` | API-P6-005 | Download a template body | None; answer 200 `application/octet-stream` | Documents, right R, scope applied | Not applicable |
| POST | `/admin/templates/{templateId}/approve` | API-P6-006 | Record the Legal approval of a Draft version with its valid-from date | `TemplateApproval`: validFrom; answer 200 `Template` in state APPROVED | Documents, right A, scope applied | `Idempotency-Key` header |
| POST | `/admin/templates/{templateId}/withdraw` | API-P6-007 | Withdraw an Approved version with a reason | `TemplateWithdrawal`: reason; answer 200 `Template` in state WITHDRAWN | Documents, right A, scope applied | `Idempotency-Key` header |

The error statuses per operation are the legacy ones and agree with T-A.2: 401, 403, 503 on the list; 401, 403 (MSG-P4-002), 413, 415 (MSG-P6-010), 422 (MSG-GEN-001, MSG-P6-006), 503 (MSG-GEN-006) on the upload; 401, 403, 404, 503 on the content read; 401, 403 (MSG-P4-002), 404, 409 not Draft (MSG-P3-005), changed (MSG-GEN-004), own upload (MSG-P7-002), 422 (MSG-GEN-003), 503 on the approve; 401, 403, 404, 409 not Approved (MSG-P3-005), 422 reason empty (MSG-GEN-001), 503 on the withdraw. Every error uses the platform error envelope with the `Problem` schema and one message ID of section 14.

`Template` schema: id, templateCode, templateVersion, language, productGroup, channel, noticeType, signatureBasis, mergeCodes, state, approvedBy, approvedAt, validFrom, createdBy, createdAt, version. 409 MSG-GEN-004 is raised from the optimistic lock on the standard column `version`.

**Legacy names.** The legacy story declares the same five operations on the legacy base path (DP-13) as `GET /templates`, `POST /templates`, `GET /templates/{templateId}/content`, `POST /templates/{templateId}/approve` and `POST /templates/{templateId}/withdraw`. The target names them `/admin/templates`, `/admin/templates/{templateId}/content`, `/admin/templates/{templateId}/approve` and `/admin/templates/{templateId}/withdraw` on `/api/recovery/comms/v1`, as TSD P6 T-A.1 gives them. The disagreement between the legacy story and the TSD is carried as a gap and an assumption; the TSD name wins on source precedence and the legacy names are kept only as a record `Not specified in the source documents (GAP-1137; ASM-2084)`.

**Set current.** Legacy AC2 names an action "set current", and the target has no such operation: none of the five operations sets a version current. The current version of a template code and language on a date is the Approved version with the latest valid from on or before that date, and the rule that makes it current is `Not specified in the source documents (GAP-1138; ASM-2085)`. AC2 is kept word for word and its refusal is served by the approve operation on a Draft version with no Legal approval, which answers 422 with MSG-P6-005 and leaves the version Draft.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | Read LOV-LANG, LOV-PRODUCT, LOV-NOTICE, LOV-CHANNEL and LOV-SIGNATURE-BASIS of TSD P6 T3.2 at the version in force (DP-07, RWB-P3-E1043-CON) |
| GET | the freshness read of RWB-P1-E1015-CON | P1 rwb-source-data | The freshness stamp SCR-33 shows beside the template rows; its path and its answer are fixed by that contract and are not restated here |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (DP-07). A read that does not answer refuses the upload or the approval with MSG-GEN-006 naming the system that failed; no version is created or approved on a partial answer. No list value and no stamp is written in code.

#### 12.3 Events published

None. The event catalogue names no template event on `rwb.comms.events.v1`, so this story publishes none and invents none: `rwb.comms.NoticeGenerated.v1`, `rwb.comms.NoticeDispatched.v1` and `rwb.comms.NoticeDelivered.v1` belong to the generation and dispatch stories of this service. An upload, an approval and a withdrawal are synchronous answers, written to the service log and the ACE audit entry.

#### 12.4 Events consumed

None. No topic is subscribed by this story; the reference-data read and the freshness read of section 12.2 are synchronous answers. A change to a list reaches the screen on its next read.

#### 12.5 Workflows and activities

None. The five operations are synchronous REST calls in the caller's thread; this story starts no workflow, registers no activity and holds nothing on task queue `rwb-comms` in namespace `rwb-recovery`.

#### 12.6 Schedules

None. No Schedule and no cron entry is registered by this story; JOB-10 WIN notices belongs to the dispatch stories and JOB-11 is the platform outbox relay.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (`rwb_comms`) | The template versions, their state and their Legal approval record; written by the upload, approve and withdraw operations and read by the list and content operations |
| merge_field | P6 (`rwb_comms`) | The merge codes of the catalog version in force; read only by the upload check (BR4) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The `idempotency_key` row of each POST and the envelope objects of the service; this story writes the idempotency row only and no outbox event |

`lov_value`, `reference_row` and `reference_version` are P3 rwb-case's and are read only through the reference-data contract of 12.2 (DP-07). `document`, `document_custody`, `document_text`, `document_type` and `document_checklist_item` are P5 rwb-document's, `recovery_case`, `task` and `timer` are P3's, `decision_log_entry` is P7's and `interaction` is P1's; they are named as consumed answers only and never read or written here (DP-01).

The template body is the claim-check file named by `body_ref` (DF-REF-050). Whether the object behind that reference is held by P5 rwb-document or by this service's own Blob container is `Not specified in the source documents (GAP-1140; ASM-2087)`; either way only the reference is a row of this service and the body is never a row and never a log line.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case reference-data fake (RWB-P3-E1043-CON) | `GET /admin/lists/{listCode}` answers LOV-LANG "TH" and "EN"; LOV-PRODUCT "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"; LOV-NOTICE "DEMAND", "RECALL", "STATUTORY_SALE_NOTICE" and "GUARANTOR_NOTICE"; LOV-CHANNEL "MOBILE", "HOME_PHONE", "WORK_PHONE", "LINE", "EMAIL", "POSTAL_ADDRESS", "CALL", "VISIT", "SMS", "LETTER", "PORTAL" and "BRANCH"; LOV-SIGNATURE-BASIS "E_SIGNATURE_ALLOWED" and "WET_INK_REQUIRED" | App story, contract tests |
| rwb-source-data freshness fake (RWB-P1-E1015-CON) | A fresh stamp for the business date and a stale stamp beyond it | App story, contract tests |
| template fixture pack | DEMAND-MTG "TH" version 2 Approved by "LEG-0001" with valid from 2026-11-01; the DEMAND-MTG "TH" version 3 body `demand-mtg-th-v3.docx`; RECALL-SSME "TH" version 4 uploaded by "LEG-0001"; a DEMAND-HP "TH" body using "LINE_ID"; `demand.pdf`; an upload with no template code | App story, contract tests |
| merge-field catalog fixture, version "MF-2026.11" | Rows for merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE", with catalog version "MF-2026.11" and its valid-from date | App story, contract tests |

The two consumed fakes answer the paths of section 12.2 with the values above, so the story builds and its tests run before rwb-case and rwb-source-data are live. The template fixture pack is the synthetic material of section 7 and of section 16; it carries synthetic wording only.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 2 consumed | The five template administration operations of 12.1 provided; the reference-data read and the freshness read of 12.2 consumed; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No template event exists in the catalogue; no topic is subscribed |
| Temporal | None | No workflow, no activity, no Schedule and nothing on task queue `rwb-comms` |
| File | 1 | The template body as a claim-check file named by `body_ref`, stored write-once and streamed on the content operation |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `template`, Java package `th.co.scb.ace.workbench.recovery.comms.template`; the front end module sits in the ACE front end behind the gateway-bff composite route (DP-19). The legacy folders `recovery/comms/templates` of the monolith are replaced by this package.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemplateAdminController | Controller | The five operations of 12.1; maps every error to the `Problem` answer and the message ID of section 14 |
| TemplateAdminService | Service | Upload, approve and withdraw; applies BR1 to BR8; writes the ACE audit entry |
| TemplateRepository | Repository | From RWB-P6-E1046-APP; reads and writes `template` in `rwb_comms`; carries the optimistic lock on `version` |
| TemplateBodyStore | Service | Stores the body write-once and returns `body_ref`; the container is the open point of 12.7 (GAP-1140) |
| MergeCodeScanner | Service | From RWB-P6-E1046-APP; reads every `{{CODE}}` of the body and checks it against the catalog version in force (BR4) |
| ReferenceCatalog | Service | Reads the five LOV lists of 12.2 through the reference-data client (DP-07) |
| TemplateApprovalScreen | React component | SCR-33: list by code and language, version detail, upload form, approve and withdraw dialogs, the Loading and Error states |

**Database and migrations.** `template` and `merge_field` live in schema `rwb_comms` with the rwb-comms login (DP-01). This story adds no table and no migration: it reads and writes `template` with the columns of section 11 and reads `merge_field`, both created by RWB-P6-E1046-APP in the per-service Flyway sequence of `rwb_comms`. The unique constraint `uk_template_version` on `template_code`, `language` and `template_version` stops a duplicate version number; version numbers are assigned inside a transaction with `SELECT ... FOR UPDATE` on the highest version of the code and language.

**Configuration and reference data.** The property `rwb.comms.template.allowed-types` = DOCX and the property `rwb.comms.template.max-size-mb` = 10 are marked assumed in the legacy text, and no source fixes the list or the limit: the two values are `Not specified in the source documents (GAP-1139; ASM-2086)`. Both are read as configuration, never written in Java (BR8); the allowed list drives MSG-P6-010. The merge field catalog is loaded by the reference data administrator through RWB-P6-E1046-APP (DL11). The five lists of 12.2 arrive on the reference-data contract at the version in force (DP-07). The feature switch is `rwb.comms.template-admin` (legacy name kept): off means the five operations answer 503 with MSG-GEN-006 and nothing is stored.

**Platform rows**

| Platform element | What this story uses it for |
|---|---|
| Error envelope and `Problem` schema | Every error answer of 12.1, one message ID per condition |
| `idempotency_key` store in `rwb_comms` | The `Idempotency-Key` of the three POSTs and the stored first answer (AC10) |
| gateway-bff composite route (RWB-PLT-N001-CON) | SCR-33 and its Draft, Approved and Withdrawn states, read and acted on through one route (DP-19) |
| Reference-data client (RWB-PLT-E1043-CON) | The five LOV lists of 12.2, with one hop and a 2 s budget (DP-07) |
| Freshness read of RWB-P1-E1015-CON | The freshness stamp SCR-33 shows beside the rows that read data products |
| ACE audit entry | The upload, approval and withdrawal entry with the user, the version and the time; never a body and never a merge value |

**Build steps**

1. Add the `Template`, `TemplatePage`, `TemplateApproval` and `TemplateWithdrawal` schemas to the OpenAPI file of `/api/recovery/comms/v1` and generate the controller interface.
2. Build the upload path with the type, size, required field and merge code checks; test AC1 (upload part), AC4, AC5, AC6.
3. Build TemplateBodyStore with write-once storage; test that a second write to the same ref is refused.
4. Build approve with the role, self-approval, state and valid from checks; test AC1, AC2, AC3, AC7.
5. Add the optimistic lock and the Idempotency-Key store; test AC9 and AC10.
6. Build withdraw; test AC8.
7. Build SCR-33 with states Draft, Approved and Withdrawn, the common Loading and Error states, and the MSG texts in English and Thai; browser test of the upload and approve path through the gateway-bff route.
8. Run the contract test of section 16 over the five operations and their error answers.

**Feature flag.** `rwb.comms.template-admin`.

**Done when.** The tests in section 16 pass, SCR-33 shows only the actions the signed-in role holds, and no template body and no merge value appears in a log of the run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | Set current on a version with no Legal approval | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P7-002 | The uploader approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P6-006 | A merge code is not in the catalog | {template} uses the merge field {field}, which is not in the merge field catalog. The load was refused. |
| MSG-GEN-001 | A required field is empty | Enter {field}. |
| MSG-P6-010 | The body file type is not allowed | This template file type cannot be loaded. Use {types}. |
| MSG-GEN-003 | Valid from is before today | {field} cannot be before {other}. |
| MSG-P6-003 | A withdrawn template is asked for | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-GEN-004 | Another person changed the version first | Someone else changed this record. Reload it to see their change. |
| MSG-P3-005 | Approve on a version that is not Draft, or withdraw on one that is not Approved | This case cannot move to {state} from {current}. |
| MSG-P4-002 | The role lacks the right | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

SCR-33 Template approval (module P6, capability area Documents). screens.txt lists it as first in E2; this story builds it in Epic 1 behind its flag.

| State | What the user sees and does |
|---|---|
| Draft | The litigation officer sees the uploaded version, its merge codes and the body preview. Legal counsel sees Approve with a valid from date |
| Approved | Everyone with Documents R sees the version, approver, approval time and valid from. Legal counsel sees Withdraw |
| Withdrawn | The version shows its withdrawal reason; no action is offered |

The common states Loading and Error apply (screens.txt, common states).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-034-01 | AC1, BR1, BR7 | End to end | DEMAND-MTG TH version 2 Approved; upload of version 3 by LIT-0101; approval by LEG-0001 |
| TC-E1-034-02 | AC2, BR1 | End to end | DEMAND-MTG TH version 3 Draft |
| TC-E1-034-03 | AC3, BR2 | End to end | RECALL-SSME TH version 4 uploaded by LEG-0001 |
| TC-E1-034-04 | AC4, BR4 | End to end | Body using LINE_ID |
| TC-E1-034-05 | AC5 | End to end | Upload with no template code |
| TC-E1-034-06 | AC6, BR8 | End to end | demand.pdf |
| TC-E1-034-07 | AC7, BR5 | End to end | Valid from 2026-11-19 on 2026-11-20 |
| TC-E1-034-08 | AC8, BR6 | End to end | DEMAND-MTG TH version 3 current, withdrawn |
| TC-E1-034-09 | AC9 | End to end | Two approvals on record version 1 |
| TC-E1-034-10 | AC10 | End to end | Approve repeated with one Idempotency-Key |
| TC-E1-034-11 | Access | Component | RW-LITOFF calls POST /templates/{templateId}/approve; refused with MSG-P4-002 |
| TC-P6-E1034-APP-01 | Section 12.1 to 12.9 | Contract | The OpenAPI document validates; the five operations, the `Template` schema, the Idempotency-Key rule on the three POSTs and the error statuses per operation are present; the legacy `/templates` names are recorded as legacy names only |

The eleven legacy cases keep their legacy order, their legacy data and their legacy level mapping: legacy System maps to End to end and legacy Access maps to Component. TC-E1-034-11 keeps its legacy path in its Data column, and the path it exercises in this story is the approve operation under `/admin/templates`, recorded as GAP-1137. TC-P6-E1034-APP-01 is new and tests the contract tables of section 12; the story carries those tables, so it carries their contract test. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: file types, size limit, merge codes and the template list are data or configuration.
- No personal data in logs, tests or prompts. Template bodies in tests carry synthetic wording; the audit entry holds user IDs, template code and version only.
- No read of another module's tables. Roles come from the ACE access check; storage through the ACE storage pattern.
- A stored body is never overwritten; a correction is a new version.
- The screen hides actions the role does not hold, and the server checks the right on every call.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-15 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06 | TC-E1-034-01 to TC-E1-034-11 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | `template` and `merge_field` in `rwb_comms`; no other service's table read |
| DP-07 | The five LOV lists on the rwb-case reference-data contract (12.2, section 13) |
| DP-13 | Base `/api/recovery/comms/v1` on all five operations (12.1) |
| DP-19 | SCR-33 read and acted on through the gateway-bff composite route (section 13) |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_comms` schema and the rwb-comms login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout on the two consumed reads |
| CTL-14 | Only an Approved version with its approver and approval time becomes current (BR1) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E1-034, disposition Moved (no impact) |
| Legacy criteria | AC1 to AC10 of the legacy story, all owned by this story and copied word for word with their origin tags |
| Legacy dependencies | RWB-E1-046 is RWB-P6-E1046-APP in the target; RWB-E1-015 is the freshness read of RWB-P1-E1015-CON |
| Build dependencies | RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P6-E1046-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P1-E1015-CON |
| Test cases | TC-E1-034-01 to TC-E1-034-11 as the legacy evidence, and TC-P6-E1034-APP-01 as the new contract case |
| Decoupling patterns | DP01, DP07, DP13, DP19 |
| Gap and assumption rows | GAP-1137 to GAP-1140, and their paired ASM-2084 to ASM-2087 |

### 19. Out of scope

- The catalog tables, load checks and TemplateCatalog interface (RWB-E1-046). Target: RWB-P6-E1046-APP.
- Generating notices from a template (RWB-E1-052) and resuming held notices when a new version is approved (R-LIT-06, RWB-E2-021). Target: RWB-P6-E1052-APP and RWB-P6-E2021-APP.
- Adding a template through the Compliance approval path (FEAT-ADM-05, Epic 8). Target: RWB-P6-AD017-APP carries the Epic 8 administration surface on top of this story; the Compliance approval path itself is not part of that surface.
- Thai labels on SCR-33 beyond the standard messages (DL10). Target: RWB-PLT-N001-CON for the screen field list and the Thai message texts.
