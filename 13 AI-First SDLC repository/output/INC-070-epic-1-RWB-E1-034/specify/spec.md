# Technical Specification — RWB-E1-034 Letter template management

| Field | Value |
|---|---|
| Story | RWB-E1-034 — Letter template management |
| Epic / module | E1 / P6 Communications |
| RUN_ID | `INC-070-epic-1-RWB-E1-034` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-OCC-002); story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 034 Letter template management v1.md`; FSD P6 A2.1; TSD P6 T3.1, T-A |
| Upstream IDs | REQ-OCC-002; FEAT-DRI-15; US-RWB-E1-034; R-LIT-03, R-LIT-04, R-LIT-06; CTL-05, CTL-12, CTL-14; DL10, DL27, DL28; DF-REF-045..069 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |
## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-33 Template approval: version list by code and language, detail with body preview and merge codes, upload form, approve and withdraw dialogs, Draft/Approved/Withdrawn states, Loading and Error. |
| Logic In Scope | `YES` — upload validation, write-once body storage, version numbering, approval, self-approval block, valid-from check, withdrawal, optimistic lock, idempotency and audit. |
| API In Scope | `YES` — five endpoints first delivered in E1: `GET/POST /admin/templates`, `GET /admin/templates/{templateId}/content`, `POST /admin/templates/{templateId}/approve`, `POST /admin/templates/{templateId}/withdraw` (API-P6-003..007). |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `template` table and `TemplateRepository` (RWB-E1-046); `MergeCodeScanner` (RWB-E1-046); ACE write-once storage (DL27); ACE audit log; SCR-33. |
| New Nodes Required | `YES` — `TemplateController`, `TemplateAdminService`, `TemplateBodyStore`, `TemplateApprovalScreen`, `TemplateSchemaMapper`, `V1_034__template_admin.sql`. |
| Inherited Existing Behavior | Catalog, version key and merge field checks (RWB-E1-046); freshness stamp (RWB-E1-015); migration pattern (RWB-E1-044); configuration and lists (RWB-E1-042); ACE access check and audit. |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Only an Approved version with an approver and approval time can become current. | SPEC-RWB-E1-034-006, -007 | DIRECT | Approve sets state, approver and time; current is derived from valid from. | COVERED |
| BR2 | The uploader of a version cannot approve it. | SPEC-RWB-E1-034-006 | DIRECT | Compare `created_by` with the caller; 409 MSG-P7-002. | COVERED |
| BR3 | Approval needs Documents A, held by Legal counsel. | SPEC-RWB-E1-034-006, -015 | DIRECT | Method security on approve and withdraw. | COVERED |
| BR4 | Every merge code in the body is in the merge field catalog in force. | SPEC-RWB-E1-034-003 | DIRECT | `MergeCodeScanner` + catalog lookup before storage. | COVERED |
| BR5 | Valid from is today or later. | SPEC-RWB-E1-034-006 | DIRECT | Server check against the business date; 422 MSG-GEN-003. | COVERED |
| BR6 | A withdrawn version holds generation; no fallback to an earlier version. | SPEC-RWB-E1-034-008, -007 | DIRECT | State Withdrawn; catalog returns no current version. | COVERED |
| BR7 | Template bodies are stored write-once; a change is a new version. | SPEC-RWB-E1-034-004 | DIRECT | Storage key generated; no overwrite path. | COVERED |
| BR8 | Allowed body file types are configuration, DOCX in Epic 1. | SPEC-RWB-E1-034-002 | DIRECT | `rwb.comms.template.allowed-types`; 415 MSG-P6-010. | COVERED |
| AC1 | Upload creates version 3 Draft; Legal approves; version 3 current; version 2 readable. | SPEC-RWB-E1-034-002, -004, -005, -006, -007 | DIRECT | Next version; Draft then Approved; earlier rows unchanged. | COVERED |
| AC2 | Set current on a Draft with no approver is refused; version 2 stays current. | SPEC-RWB-E1-034-006, -007, -013 | DIRECT | No set-current endpoint (known defect 7); current is derived. MSG-P6-005 is raised by the catalog when no Approved version exists; the screen offers no Set current action on a Draft. | COVERED |
| AC3 | The uploader cannot approve their own version; 409 MSG-P7-002. | SPEC-RWB-E1-034-006 | DIRECT | Separation of duty. | COVERED |
| AC4 | Unknown merge code refused at upload; 422 MSG-P6-006; no version, no file. | SPEC-RWB-E1-034-003 | DIRECT | Validation before storage. | COVERED |
| AC5 | Missing template code refused; 422 MSG-GEN-001 naming template code. | SPEC-RWB-E1-034-002 | DIRECT | Required-field check. | COVERED |
| AC6 | A PDF upload is refused; 415 MSG-P6-010 naming DOCX. | SPEC-RWB-E1-034-002 | DIRECT | Allowed-type property. | COVERED |
| AC7 | Valid from before today refused; 422 MSG-GEN-003 naming valid from and today. | SPEC-RWB-E1-034-006 | DIRECT | Server-side date check. | COVERED |
| AC8 | Withdraw the current version; state Withdrawn; catalog throws; no fallback. | SPEC-RWB-E1-034-008, -007 | DIRECT | Reason required; no earlier version made current. | COVERED |
| AC9 | Two approvals at once: one succeeds, the other 409 MSG-GEN-004. | SPEC-RWB-E1-034-009 | DIRECT | Optimistic lock on `version`. | COVERED |
| AC10 | Repeated approval with one Idempotency-Key returns the first response; one audit entry. | SPEC-RWB-E1-034-010, -011 | DIRECT | P2 idempotency store, 24 hours. | COVERED |
## User story intent interpretation

As a **litigation officer (RW-LITOFF)**, I want **a screen to upload a template version, have Legal counsel record the approval and set it current**, so that **templates are managed without a developer**.

The story puts the upload in the litigation officer's hands and the approval in Legal's. The current version is not switched by a button: it is derived from the approval and the valid-from date, so the screen shows which version is current and which earlier versions remain readable. SCR-33 is built in Epic 1 behind its flag; the inventory's E2 first release is the general release.
## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A litigation officer opens SCR-33 from the Documents menu and uploads a DOCX; Legal counsel opens a Draft and approves or withdraws. |
| Preconditions | RWB-E1-046 done; RWB-E1-015 done; merge field catalog loaded; uploader holds Documents C; approver holds Documents A; ACE write-once container available (DL27). |
| Input | DOCX body; template code, language, product group, channel, notice type, signature basis and merge codes; valid from and approval decision; withdrawal reason. |
| Output | `template` row in Draft, Approved or Withdrawn; write-once body; audit entry; catalog current version. |
| Feature flag | `rwb.comms.template-admin`. Off: SCR-33 hidden and the five routes not registered; the catalog and generation are unaffected. |
## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `template` | `template_code` | Upload form | Editable before upload | varchar(30); required; existing code continues its sequence |
| `template` | `template_version` | System | Read-only | Next number per code and language; unique |
| `template` | `language`, `product_group`, `channel`, `notice_type`, `signature_basis` | Upload form | Editable before upload | Values from LOV-LANG, LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE, LOV-SIGNATURE-BASIS |
| `template` | `merge_codes` | Body scan and upload list | Read-only after upload | Must equal the `{{CODE}}` set in the body |
| `template` | `body_ref` | ACE storage | Read-only | Write-once object key |
| `template` | `state` | System | Read-only | DRAFT, APPROVED or WITHDRAWN |
| `template` | `approved_by`, `approved_at` | Approving Legal user; approval time | System writes | Set on approve; never the uploader |
| `template` | `valid_from` | Approval dialog | Editable before approve | Today or later |
| `template` | `withdrawal_reason` | Withdraw dialog | Editable before withdraw | Required; varchar(400); shown in the Withdrawn state |
| `template` | `version` | Optimistic lock | System writes | Increment on each change; mismatch is 409 |
| `merge_field` | `merge_code` | Catalog | Read-only | Every code must exist in the catalog in force |
## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| — | Upload | Checks pass | `DRAFT` | Body stored write-once; next version; audit entry |
| `DRAFT` | Approve | Documents A, caller is not uploader, valid from today or later | `APPROVED` | Approver and time set; current from valid from; audit entry |
| `APPROVED` | Withdraw | Documents A; reason entered | `WITHDRAWN` | Reason stored; no fallback; generation holds; audit entry |
| `DRAFT` | Approve | Caller is the uploader | `DRAFT` | 409 MSG-P7-002; no change |
| `DRAFT` | Approve | Valid from before today | `DRAFT` | 422 MSG-GEN-003; no change |
| `APPROVED` | Approve | Not Draft | `APPROVED` | 409 MSG-P3-005; no change |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event | SPEC |
|---|---|---|---|---|
| X1 | Set current on a version with no approver | Refused; stays Draft; current unchanged | MSG-P6-005 | SPEC-006, -013 |
| X2 | Uploader approves own version | 409; stays Draft | MSG-P7-002 | SPEC-006 |
| X3 | Unknown merge code | Upload refused; no version and no stored file | MSG-P6-006 | SPEC-003 |
| X4 | Template code or language empty | 422; nothing stored | MSG-GEN-001 | SPEC-002 |
| X5 | File is not DOCX | 415; nothing stored | MSG-P6-010 | SPEC-002 |
| X6 | Valid from before today | 422; stays Draft | MSG-GEN-003 | SPEC-006 |
| X7 | Current version withdrawn | State Withdrawn; generation holds | MSG-P6-003 | SPEC-008 |
| X8 | Two approvers at once | First wins; second 409 | MSG-GEN-004 | SPEC-009 |
| X9 | Repeated approve with the same key | First response returned; one audit entry | None | SPEC-010 |
## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/admin/templates` (Documents R); `POST /admin/templates` (Documents C, multipart); `GET /admin/templates/{templateId}/content` (Documents R, binary); `POST /admin/templates/{templateId}/approve` (Documents A); `POST /admin/templates/{templateId}/withdraw` (Documents A). |
| Contract delta | The five operations and the `Template`, `TemplatePage`, `TemplateApproval` and `TemplateWithdrawal` schemas are in API Specification v2 (API-P6-003..007, first in E1). One additive field is required: `withdrawalReason` on `Template` for AC8/§15; record it in the additions file. `mergeCodes` is a comma-separated multipart string on upload and an array in the response. |
| Backward compatibility | Additive; no existing operation changes. |
| Authorization | Documents R for list/content; Documents C for upload; Documents A for approve/withdraw. 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P3-005, MSG-GEN-004, MSG-P7-002; 413 platform limit; 415 MSG-P6-010; 422 MSG-GEN-001/003, MSG-P6-006; 503 MSG-GEN-006. |
| Versioning | No version change; additive field only. |
## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR8; SPEC-RWB-E1-034-001..018 | New SCR-33 component, upload form, approve/withdraw dialogs, role-based actions and message rendering. | Each state; role-based action visibility; required-field and file-type errors; dialogs; message text in English and Thai; Loading and Error; keyboard access. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR8; SPEC-RWB-E1-034-001..018 | New controller, service, body store and migration; repository extended with the optimistic lock. | Each required field; DOCX/PDF; size boundary; unknown code; self-approval; valid-from today/yesterday; state conflicts; concurrent approval; idempotent repeat; withdraw; audit. |
## Detailed design
### Components

| Component | Type | Responsibility |
|---|---|---|
| `TemplateController` | Controller | Five endpoints; maps errors to Problem responses and message IDs. |
| `TemplateAdminService` | Service | Upload, approve and withdraw; applies BR1–BR8; writes the audit entry. |
| `TemplateRepository` | Repository | From RWB-E1-046; adds the optimistic lock and next-version query. |
| `TemplateBodyStore` | Service | Stores the DOCX write-once through the ACE pattern and returns `body_ref`. |
| `MergeCodeScanner` | Service | From RWB-E1-046; reused for the upload check. |
| `TemplateApprovalScreen` | React component | SCR-33: list, detail, upload form, approve/withdraw dialogs, state-specific actions. |
| `TemplateSchemaMapper` | Mapper | Maps entity to `Template`, including `withdrawalReason`. |
### Package and boundaries

Backend package `recovery.comms.templates`; front end folder `recovery/comms/templates` in the ACE front end (DL07). The service calls the catalog repository, the storage interface and the ACE audit log; it does not read P4 or P7 tables. The screen calls only the five P6 endpoints.
### Data and migration

- `V1_034__template_admin.sql`: adds `withdrawal_reason varchar(400)` to `template`; no new table.
- Version numbers are assigned inside a transaction with `SELECT ... FOR UPDATE` on the highest version of the code and language; `uk_template_version` is the backstop.
- `version` is the optimistic lock; a mismatch returns 409 MSG-GEN-004.
- `withdrawal_reason` is a new column not yet in the data dictionary (GAP); the data steward allocates the field ID at merge.
- Configuration: `rwb.comms.template.allowed-types` = DOCX; `rwb.comms.template.max-size-mb` = 10 (assumed; DL11).
### Rules

1. Upload requires Documents C; code and language required; list values valid; file type allowed; size within the limit; every `{{CODE}}` in the body and every declared code in the catalog in force.
2. On success, store the body write-once, assign the next version, insert the row in `DRAFT` with `created_by`, and write the audit entry. A refused upload stores no body and creates no row.
3. Approve requires Documents A; the version must be `DRAFT`; the caller must not be `created_by`; `valid_from` must be today or later. Set `APPROVED`, `approved_by`, `approved_at` and `approved_by_legal = true`; write the audit entry.
4. Withdraw requires Documents A; the version must be `APPROVED`; a reason is required. Set `WITHDRAWN` and `withdrawal_reason`; write the audit entry. No earlier version is made current.
5. Current is derived: RWB-E1-046 `TemplateCatalog.current` returns the Approved version with the highest version number whose `valid_from` is on or before the date. A Draft or Withdrawn version is never current.
6. Approve and withdraw use the `Idempotency-Key` through the P2 store (24 hours); a repeat returns the stored response and writes no second audit entry.
7. Error mapping: 415 MSG-P6-010; 422 MSG-GEN-001/003/006; 409 MSG-P3-005/GEN-004/P7-002; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006.
### Transaction, security and operations

Upload: validate, store the body, insert the row and write the audit entry. If the insert fails after the body write, the object is unreferenced and reported by the storage inventory; it is not a template version. Approve and withdraw: one transaction for the row and the audit entry. No domain event is published; the catalog read is derived.

| Actor | Right | Scope |
|---|---|---|
| RW-LITOFF | Documents C for upload; Documents R | All templates |
| RW-LEGAL | Documents CRUA; approves and withdraws; cannot approve own upload | All templates |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLY and other Documents R roles | Documents R; read SCR-33 | All templates |
| RW-REFADM | Reference data C; loads the catalog (RWB-E1-046) | All |

Every endpoint has a Spring Security method check naming Documents and the operation. The screen hides actions the role does not hold; the server rechecks every call. The audit entry holds user IDs, template code and version only.

- Metrics: uploads, approvals, withdrawals, refusals by reason; approval latency.
- Alerts: repeated 403/409 on approve; storage write failure; audit write failure.
- Run book: template release steps, approval evidence, rollback to the previous version (RWB-E1-056).
- Performance: list is paginated; body streams from write-once storage; screen response under 2 seconds at P95 (NFR-008).
### Feature flag and rollback

`rwb.comms.template-admin`. Off: the five routes are not registered, SCR-33 is hidden, and templates continue to load through the RWB-E1-046 file path. Rollback: turn the flag off; the migration adds one nullable column, so the previous tag runs unchanged.
## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-034-01 | AC1, BR1, BR7 | System | DEMAND-MTG TH v2 Approved; upload v3 by LIT-0101; approve by LEG-0001 | v3 Approved and current; v2 readable with its approver |
| TC-E1-034-02 | AC2, BR1 | System | DEMAND-MTG TH v3 Draft | No Set current action; v2 stays current; MSG-P6-005 at the catalog boundary |
| TC-E1-034-03 | AC3, BR2 | System | RECALL-SSME TH v4 uploaded by LEG-0001 | 409; MSG-P7-002; stays Draft |
| TC-E1-034-04 | AC4, BR4 | System | Body using LINE_ID | 422; MSG-P6-006; no version, no file |
| TC-E1-034-05 | AC5, AC6, BR8 | System | Upload with no template code; then demand.pdf | 422 MSG-GEN-001; 415 MSG-P6-010 |
| TC-E1-034-06 | AC7, BR5 | System | Valid from 2026-11-19 on 2026-11-20 | 422; MSG-GEN-003 naming valid from and today |
| TC-E1-034-07 | AC8, BR6 | System | v3 current; withdraw with reason | Withdrawn; catalog throws; no fallback |
| TC-E1-034-08 | AC9, AC10 | System | Two approvals on version 1; repeated key | One succeeds, one 409; repeat returns first, one audit entry |
| TC-E1-034-09 | Access, UI states | Security/System | RW-LITOFF calls approve; each role on SCR-33 | 403 MSG-P4-002; actions match the role; messages in English and Thai; keyboard access passes WCAG 2.2 AA |
| TC-E1-034-10 | BR1–BR8 | Unit | Required fields, file type/size, dates, concurrency | Each branch returns the specified message and state |
## Guardrails

- No business value in code: file types, size limit, merge codes, lists and template codes are data or configuration.
- No personal data in logs, tests or prompts; template bodies use synthetic wording; audit entries hold user IDs, code and version only.
- No read of another module's tables; roles from the ACE access check and storage through the ACE pattern; a stored body is never overwritten.
## Out of scope

- The catalog tables, load checks and `TemplateCatalog` interface (RWB-E1-046).
- Generating notices from a template (RWB-E1-052) and resuming held notices (R-LIT-06, RWB-E2-021).
- The Compliance approval path (FEAT-ADM-05, Epic 8).
- Thai labels beyond the standard messages (DL10).
## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | Epic 1 §3.6, §4 | FEAT-DRI-15 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06 | TC-E1-034-01..10 |
## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §12; SPEC-001..008 | §12 gives the base path as `/api/recovery/v1` with `/templates`; the TSD and API specification use `/api/recovery/v1/admin/templates`. | Determines the routes the screen calls. | Use the API specification and TSD paths (`/admin/templates`); §12 is shorthand. | RESOLVED | SPEC-001..008 |
| CLAR-002 | AC2, X1; SPEC-006, -013 | AC2 and X1 use a "set current" action, but §12 has no such endpoint and flow step 7 derives current from valid from. This is known defect 7 in the story defect register. | Determines how AC2 is exercised and which message is asserted. | There is no set-current endpoint and no set-current action. Current is derived from approval and valid from. The screen offers no Set current action on a Draft; MSG-P6-005 is raised by the catalog when generation asks for a template with no Approved version. | RESOLVED | SPEC-006, -007, -013 |
| CLAR-003 | §15; SPEC-012 | The screen inventory and screen specification list SCR-33 as first in E2 and do not name RWB-E1-034; the story says build it in E1 behind its flag. The screen specification also lists only six fields. | Determines whether the screen is in this story and which fields it shows. | Build SCR-33 in E1 behind `rwb.comms.template-admin`; E2 is the general release. Use the story's field set; the screen specification is stale and is updated at merge. | RESOLVED | SPEC-012 |
| CLAR-004 | AC8, §15; SPEC-008, -014 | The `template` table and the `Template` response have no withdrawal reason, but the Withdrawn state must show it. | The reason cannot be shown without a column and a response field. | Add `withdrawal_reason varchar(400)` in `V1_034__template_admin.sql` and `withdrawalReason` to the `Template` response as an additive field. The data steward allocates the field ID. | RESOLVED | SPEC-008, -014 |
| CLAR-005 | §12; SPEC-002 | The upload returns 413 for a file over the limit, but no message row is defined for size. | The screen needs text for the refusal. | The platform returns 413 with the standard Problem body before the handler; the screen shows the configured maximum from `rwb.comms.template.max-size-mb` (10, assumed; DL11). No new message ID. | RESOLVED | SPEC-002 |
| CLAR-006 | §10; SPEC-015 | The roles document gives RW-LEGAL first release E3, while this story needs Legal approval in E1. | Determines whether Legal can approve in E1. | The story gives RW-LEGAL Documents A in E1; E3 is the full Legal workspace. The approval right is loaded for E1. | RESOLVED | SPEC-015 |
| CLAR-007 | §12; SPEC-013 | 409 on a template state conflict uses MSG-P3-005, whose wording is case-centric. | The screen text is awkward for a template. | Reuse MSG-P3-005 as §12 requires; a P6-specific state-conflict message is a later content change. | RESOLVED | SPEC-013 |
| CLAR-008 | §12; SPEC-002 | The API multipart schema types `mergeCodes` as a string, while the response returns an array. | Determines how the upload sends the codes. | Send a comma-separated list in the multipart field; parse to a list server-side; return an array. No schema change. | RESOLVED | SPEC-002 |

`CLARIFICATION_STATUS: RESOLVED` — all eight items are answered from the story, the API specification, the screen specification, DL10/DL11/DL27 or the defect register. No item changes the business outcome.
## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; the SCR-33 screen specification is the local design evidence and the HTML prototype has no SCR-33 panel.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New SCR-33 template approval screen with upload, approve and withdraw, and five E1 template endpoints already recorded in API Specification v2.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new screen and five first-release endpoints]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 10 acceptance criteria and 9 exception paths are mapped; AC2 is read with known defect 7 resolved in CLAR-002.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
