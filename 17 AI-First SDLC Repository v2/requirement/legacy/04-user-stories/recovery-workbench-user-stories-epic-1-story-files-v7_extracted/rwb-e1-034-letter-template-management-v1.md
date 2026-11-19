<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 034 Letter template management v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 034 Letter template management v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-034 Letter template management

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-034 |
| Epic | E1, release 30 November 2026 |
| Module | P6 Communications |
| Feature | FEAT-DRI-15 Manage letter templates with Legal approval |
| Requirement IDs | REQ-OCC-002 |
| BRD section | Business Requirements Epic 1, sections 3.6 and 4 |
| L3 process | 13 Manage documents and correspondence |
| Decision | D7.1 |
| Priority | Should |
| Depends on | RWB-E1-046, RWB-E1-015 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **a screen to upload a template version, have Legal counsel record the approval and set it current**, so that **templates are managed without a developer**.

## 2. Business rationale

A template change today needs a person outside Legal to edit a file and send it round, and nothing records which wording was approved. This story gives the litigation officer an upload and Legal counsel an approve and withdraw action on SCR-33 Template approval, with the approver and date held on the version. It serves REQ-OCC-002 and control CTL-14 (every notice from the current Legal-approved version), and removes the developer from template changes.

## 3. Preconditions

- RWB-E1-046 is done: the template and merge_field tables, the load checks and the TemplateCatalog interface exist.
- RWB-E1-015 is done: the freshness stamp shows on screens that read data products.
- The merge field catalog is loaded, with codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE" in the synthetic set.
- The uploader holds RW-LITOFF or RW-LEGAL (Documents C); the approver holds RW-LEGAL (Documents A).
- The ACE storage pattern with a write-once container is available for template bodies (DL27).

## 4. Flow

1. Litigation officer: opens SCR-33 Template approval and chooses the template code and language, or a new code.
2. Litigation officer: uploads the DOCX body and enters product group, channel, notice type, signature basis and the merge codes used.
3. System: checks the role (Documents C), the required fields, the file type and size, and every merge code against the catalog (MergeCodeScanner from RWB-E1-046).
4. System: stores the body write-once, creates the next version number in state Draft and shows it in the list.
5. Legal counsel: opens the Draft version, reads the body and the merge codes, enters the valid from date and approves.
6. System: checks the role (Documents A), that the approver is not the uploader (CTL-05), that the version is Draft and that valid from is not before today; sets state Approved with approver and approval time.
7. System: from valid from, TemplateCatalog returns this version as current; earlier Approved versions stay readable on SCR-33.
8. Legal counsel: may withdraw an Approved version with a reason; the system sets state Withdrawn and generation for that code and language holds (R-LIT-04).
9. System: writes every upload, approval and withdrawal to the ACE audit log with the user, the version and the time.

## 5. Exception paths

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

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the catalog (RWB-E1-046) only; generation (RWB-E1-052) is separate |
| Negotiable | Layout of SCR-33 follows the ACE components (DL08, DL31); the behavior is fixed here |
| Valuable | Legal approves wording in the Workbench, and the approval is on the version |
| Estimable | Five endpoints, one screen with three states |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion is an API or screen test with synthetic templates |

## 7. Acceptance criteria

```gherkin
Feature: Letter template management

  Background:
    Given user "LIT-0101" holds RW-LITOFF
    Given user "LEG-0001" holds RW-LEGAL
    Given template "DEMAND-MTG" in language "TH" has version 2 Approved by "LEG-0001" with valid from 2026-11-01
    Given today is 2026-11-20

  Scenario: AC1 New version
    Given "LIT-0101" uploads "demand-mtg-th-v3.docx" for "DEMAND-MTG" "TH" using merge codes "CASE_NO" and "TOTAL_OUTSTANDING"
    Given version 3 is created in state "Draft"
    When "LEG-0001" approves version 3 with valid from 2026-11-20
    Then version 3 has state "Approved", approver "LEG-0001" and an approval time on 2026-11-20
    Then TemplateCatalog returns version 3 as current for "DEMAND-MTG" "TH" on 2026-11-20
    Then version 2 stays readable on SCR-33 with approver "LEG-0001"

  Scenario: AC2 Approval required
    Given version 3 of "DEMAND-MTG" "TH" is in state "Draft" with no approver
    When "LIT-0101" chooses set current on version 3
    Then the system refuses it with MSG-P6-005 naming "DEMAND-MTG" version 3
    Then version 2 stays current

  Scenario: AC3 The uploader cannot approve the version
    Given "LEG-0001" uploaded version 4 of "RECALL-SSME" "TH"
    When "LEG-0001" approves version 4
    Then the system refuses it with status 409 and MSG-P7-002
    Then version 4 stays "Draft"

  Scenario: AC4 Unknown merge code refused at upload
    Given "LIT-0101" uploads a body for "DEMAND-HP" "TH" that uses the merge code "LINE_ID"
    Given "LINE_ID" is not in the merge field catalog
    When the upload is sent
    Then the system refuses it with status 422 and MSG-P6-006 naming "LINE_ID"
    Then the system creates no version of "DEMAND-HP" and no file is stored

  Scenario: AC5 Required field empty
    Given "LIT-0101" uploads a body with no template code
    When the upload is sent
    Then the system refuses it with status 422 and MSG-GEN-001 naming "template code"

  Scenario: AC6 File type not allowed
    Given "LIT-0101" uploads "demand.pdf" for "DEMAND-MTG" "TH"
    When the upload is sent
    Then the system refuses it with status 415 and MSG-P6-010 naming "DOCX"

  Scenario: AC7 Valid from before today
    Given version 3 of "DEMAND-MTG" "TH" is "Draft"
    When "LEG-0001" approves it with valid from 2026-11-19
    Then the system refuses it with status 422 and MSG-GEN-003 naming "valid from" and "today"

  Scenario: AC8 Withdraw the current version
    Given version 3 of "DEMAND-MTG" "TH" is Approved and current
    When "LEG-0001" withdraws version 3 with reason "Wording under review"
    Then version 3 has state "Withdrawn"
    Then TemplateCatalog throws TemplateWithdrawnException for "DEMAND-MTG" "TH" with MSG-P6-003
    Then the system does not mak version 2 current again

  Scenario: AC9 Two approvals at the same time
    Given version 3 of "DEMAND-MTG" "TH" is "Draft" at record version 1
    Given "LEG-0001" and "LEG-0002" both open it
    When both approve within the same second
    Then one approval succeeds
    Then the system refuses the other with status 409 and MSG-GEN-004

  Scenario: AC10 Repeated approval request
    Given "LEG-0001" approved version 3 with Idempotency-Key "7f1c0d2e-0001"
    When the same request is sent again with Idempotency-Key "7f1c0d2e-0001"
    Then the response is the first response with status 200
    Then the audit log holds one approval for version 3
```

## 8. Business rules

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

## 9. State transitions

None. This story does not change a case status. It changes the template version state (standard column state):

| From | Event | Condition | To |
|---|---|---|---|
| None | Upload | Checks pass | Draft |
| Draft | Approve | Approver is Legal counsel and not the uploader; valid from today or later | Approved |
| Approved | Withdraw | Reason entered | Withdrawn |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Uploads a version (Documents C), reads templates (Documents R) |
| RW-LEGAL, Legal counsel | Uploads, approves and withdraws a version (Documents CRUA); cannot approve own upload |
| RW-CASEOWN, RW-TEAMMGR and other roles with Documents R | Read templates on SCR-33 |
| RW-COMPLY, Compliance and PDPA officer | Reads templates (Documents R) |

No approval level from the delegation of authority applies; Legal approval of wording is a Documents A right.

## 11. Data

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

## 12. Contract

All five endpoints are new and recorded in the additions file. Base path /api/recovery/v1. Errors use the Problem schema.

| Method and path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|
| GET /templates | Query: code, language, state, page, size | 200 TemplatePage (items of Template) | 401, 403, 503 | Documents R, scope applied | Not applicable |
| POST /templates | multipart: file, templateCode, language, productGroup, channel, noticeType, signatureBasis, mergeCodes | 201 Template, state DRAFT | 401; 403 (MSG-P4-002); 413; 415 (MSG-P6-010); 422 (MSG-GEN-001, MSG-P6-006); 503 (MSG-GEN-006) | Documents C | Idempotency-Key header |
| GET /templates/{templateId}/content | None | 200 application/octet-stream | 401, 403, 404, 503 | Documents R | Not applicable |
| POST /templates/{templateId}/approve | TemplateApproval: validFrom | 200 Template, state APPROVED | 401; 403 (MSG-P4-002); 404; 409 not Draft (MSG-P3-005), changed (MSG-GEN-004), own upload (MSG-P7-002); 422 (MSG-GEN-003); 503 | Documents A | Idempotency-Key header |
| POST /templates/{templateId}/withdraw | TemplateWithdrawal: reason | 200 Template, state WITHDRAWN | 401; 403; 404; 409 not Approved (MSG-P3-005); 422 reason empty (MSG-GEN-001); 503 | Documents A | Idempotency-Key header |

Template schema: id, templateCode, templateVersion, language, productGroup, channel, noticeType, signatureBasis, mergeCodes, state, approvedBy, approvedAt, validFrom, createdBy, createdAt, version. 409 MSG-GEN-004 is raised from the optimistic lock on the standard column version.

## 13. Solution plan

- Package: folder `recovery/comms/templates`, Java package `recovery.comms.templates`; front end folder `recovery/comms/templates` in the ACE front end (DL07).

| Component | Type | Responsibility |
|---|---|---|
| TemplateController | Controller | The five endpoints; maps errors to Problem responses |
| TemplateAdminService | Service | Upload, approve, withdraw; applies BR1 to BR8; writes the ACE audit entry |
| TemplateRepository | Repository | From RWB-E1-046; adds the optimistic lock on version |
| TemplateBodyStore | Service | Stores the body write-once through the ACE storage pattern and returns body_ref |
| MergeCodeScanner | Service | From RWB-E1-046; reused for the upload check |
| TemplateApprovalScreen | React component | SCR-33: list by code and language, version detail, upload form, approve and withdraw dialogs |

- Database: reads and writes table template (columns from RWB-E1-046). No new table. The unique constraint uk_template_version from RWB-E1-046 stops a duplicate version number; version numbers are assigned inside a transaction with SELECT ... FOR UPDATE on the highest version of the code and language.
- Configuration and reference data: property `rwb.comms.template.allowed-types` = DOCX; property `rwb.comms.template.max-size-mb` = 10, assumed; DL11. Merge field catalog loaded by RW-REFADM.
- Build steps:
  1. Add the Template, TemplatePage, TemplateApproval and TemplateWithdrawal schemas to the OpenAPI file and generate the controller interface.
  2. Build the upload path with the type, size, required field and merge code checks; test AC1 (upload part), AC4, AC5, AC6.
  3. Build TemplateBodyStore with write-once storage; test that a second write to the same ref is refused.
  4. Build approve with the role, self-approval, state and valid from checks; test AC1, AC2, AC3, AC7.
  5. Add the optimistic lock and the Idempotency-Key store; test AC9 and AC10.
  6. Build withdraw; test AC8.
  7. Build SCR-33 with states Draft, Approved and Withdrawn, the common Loading and Error states, and the MSG texts in English and Thai; browser test of the upload and approve path.
- Feature flag: `rwb.comms.template-admin`.
- Done when: the tests in section 16 pass, and SCR-33 shows only the actions the signed-in role holds.

## 14. Validation and messages

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

## 15. Screens and states

SCR-33 Template approval (module P6, capability area Documents). screens.txt lists it as first in E2; this story builds it in Epic 1 behind its flag.

| State | What the user sees and does |
|---|---|
| Draft | The litigation officer sees the uploaded version, its merge codes and the body preview. Legal counsel sees Approve with a valid from date |
| Approved | Everyone with Documents R sees the version, approver, approval time and valid from. Legal counsel sees Withdraw |
| Withdrawn | The version shows its withdrawal reason; no action is offered |

The common states Loading and Error apply (screens.txt, common states).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-034-01 | AC1, BR1, BR7 | System | DEMAND-MTG TH version 2 Approved; upload of version 3 by LIT-0101; approval by LEG-0001 |
| TC-E1-034-02 | AC2, BR1 | System | DEMAND-MTG TH version 3 Draft |
| TC-E1-034-03 | AC3, BR2 | System | RECALL-SSME TH version 4 uploaded by LEG-0001 |
| TC-E1-034-04 | AC4, BR4 | System | Body using LINE_ID |
| TC-E1-034-05 | AC5 | System | Upload with no template code |
| TC-E1-034-06 | AC6, BR8 | System | demand.pdf |
| TC-E1-034-07 | AC7, BR5 | System | Valid from 2026-11-19 on 2026-11-20 |
| TC-E1-034-08 | AC8, BR6 | System | DEMAND-MTG TH version 3 current, withdrawn |
| TC-E1-034-09 | AC9 | System | Two approvals on record version 1 |
| TC-E1-034-10 | AC10 | System | Approve repeated with one Idempotency-Key |
| TC-E1-034-11 | Access | Access | RW-LITOFF calls POST /templates/{templateId}/approve; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: file types, size limit, merge codes and the template list are data or configuration.
- No personal data in logs, tests or prompts. Template bodies in tests carry synthetic wording; the audit entry holds user IDs, template code and version only.
- No read of another module's tables. Roles come from the ACE access check; storage through the ACE storage pattern.
- A stored body is never overwritten; a correction is a new version.
- The screen hides actions the role does not hold, and the server checks the right on every call.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | Business Requirements Epic 1, sections 3.6 and 4 | FEAT-DRI-15 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06 | TC-E1-034-01 to TC-E1-034-11 |

## 19. Out of scope

- The catalog tables, load checks and TemplateCatalog interface (RWB-E1-046).
- Generating notices from a template (RWB-E1-052) and resuming held notices when a new version is approved (R-LIT-06, RWB-E2-021).
- Adding a template through the Compliance approval path (FEAT-ADM-05, Epic 8).
- Thai labels on SCR-33 beyond the standard messages (DL10).
