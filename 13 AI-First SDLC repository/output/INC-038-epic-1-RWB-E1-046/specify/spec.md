# Technical Specification — RWB-E1-046 Template and merge field catalog as data

| Field | Value |
|---|---|
| Story | RWB-E1-046 — Template and merge field catalog as data |
| Epic / module | E1 / P6 Communications |
| RUN_ID | `INC-038-epic-1-RWB-E1-046` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-OCC-001, REQ-OCC-002); story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 046 Template and merge field catalog as data v1.md`; FSD P6 A2.1–A2.2; TSD P6 T3.1 |
| Upstream IDs | REQ-OCC-001, REQ-OCC-002; FEAT-DRI-16; US-RWB-E1-046; R-LIT-03, R-LIT-04, R-LIT-06; CTL-14; DL28; DF-REF-045..069, DF-REF-252..260 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |
## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The reference data administrator loads files through the existing P4 path and reads the reference load record. SCR-40 is E8; SCR-33 is RWB-E1-034. |
| Logic In Scope | `YES` — two load handlers, merge code scanning, version numbering, state derivation, catalog selection, refusals and audit. |
| API In Scope | `NO` — no new or changed contract. Reuses `POST /api/recovery/v1/admin/reference-loads` (P4, E1) and registers two table handlers through its published interface. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `POST /admin/reference-loads` handler registry (P4); `sys_fields` (P4 interface); `template` table (existing in Physical Schema v4); `lov_value`; ACE audit log. |
| New Nodes Required | `YES` — `TemplateEntity`, `MergeFieldEntity`, `TemplateRepository`, `MergeFieldRepository`, `TemplateLoadHandler`, `MergeFieldLoadHandler`, `MergeCodeScanner`, `TemplateCatalogService`, `TemplateNotApprovedException`, `TemplateWithdrawnException`. |
| Inherited Existing Behavior | Recovery tables only (RWB-E1-012); P4 reference load path and `sys_fields` (RWB-E1-042/043); ACE audit log; one migration per story (RWB-E1-044); `TemplateCatalog` consumed by RWB-E1-052. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A template version is used only when Approved and it carries the Legal approver and approval date. | SPEC-RWB-E1-046-007, -008 | DIRECT | State derived from `approved_by` + `approved_at`; catalog selects Approved only. | COVERED |
| BR2 | The current version is the Approved version with the highest version number whose valid from is on or before the date. | SPEC-RWB-E1-046-008, -013 | DIRECT | Ordered query on code, language, state, `valid_from`, `template_version`. | COVERED |
| BR3 | A withdrawn template has no current version; generation holds until Legal approves a new one. | SPEC-RWB-E1-046-010 | DIRECT | `TemplateWithdrawnException` with MSG-P6-003. | COVERED |
| BR4 | Every merge code a template uses is in the catalog; every catalog row names a BR Field ID in the data dictionary. | SPEC-RWB-E1-046-002, -005 | DIRECT | `sys_fields` check; `{{CODE}}` scan; union check against the catalog in force. | COVERED |
| BR5 | A load with any refused row is refused in full; the previous version stays in force. | SPEC-RWB-E1-046-003, -004, -005, -012 | DIRECT | Validate whole file, then apply in one transaction. | COVERED |
| BR6 | Earlier versions are never changed or deleted; open cases keep the version they were generated under. | SPEC-RWB-E1-046-011 | DIRECT | Append-only version rows; no update path. | COVERED |
| BR7 | Templates are owned by Legal counsel as reference data. | SPEC-RWB-E1-046-007, -015 | DIRECT | `approved_by` is the Legal user ID; DL28 ownership; RW-REFADM loads, RW-LEGAL approves. | COVERED |
| AC1 | A load creates version 2 Approved with approver and date; the catalog returns version 2; version 1 stays readable. | SPEC-RWB-E1-046-006, -007, -008, -011 | DIRECT | Next version per code and language. | COVERED |
| AC2 | A template with only a Draft version is refused with `TemplateNotApprovedException` and MSG-P6-005. | SPEC-RWB-E1-046-009 | DIRECT | No Approved row; refusal names the code and the highest Draft version. | COVERED |
| AC3 | A body using an unknown merge code is refused in full with MSG-P6-006; no version is created. | SPEC-RWB-E1-046-005 | DIRECT | Scanner and catalog check before any insert. | COVERED |
| AC4 | A catalog row with an unknown BR Field ID refuses the load with MSG-P1-002; the catalog in force stays. | SPEC-RWB-E1-046-002, -003 | DIRECT | `sys_fields` lookup; all-or-nothing apply. | COVERED |
| AC5 | A template row with no body reference refuses the load with MSG-GEN-001 naming `body_ref`. | SPEC-RWB-E1-046-004 | DIRECT | Required-field check before scanning. | COVERED |
| AC6 | The same file loaded twice creates no new version and is refused with MSG-P1-002 `repeat of load`. | SPEC-RWB-E1-046-012 | DIRECT | SHA-256 per table; 409 at the P4 endpoint. | COVERED |
| AC7 | A withdrawn current version leaves no current version and raises `TemplateWithdrawnException` with MSG-P6-003. | SPEC-RWB-E1-046-010 | DIRECT | No fallback to an earlier Approved version. | COVERED |
| AC8 | A future valid from keeps the earlier version current until that date. | SPEC-RWB-E1-046-013 | DIRECT | `valid_from <= onDate` filter. | COVERED |
## User story intent interpretation

As a **litigation officer (RW-LITOFF)**, I want **letter and document templates and their merge fields held as versioned data with the Legal approval record on each version**, so that **a template change is a data release approved by Legal and never a code release**.

The story builds the catalog, not the letter engine. It gives RWB-E1-052 a read-only `TemplateCatalog` that returns only a Legal-approved version and only fields the catalog knows. The reference data administrator loads two file types through the P4 path; Legal approval is carried on the template row in Epic 1 and moves to SCR-33 in RWB-E1-034.
## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `POST /api/recovery/v1/admin/reference-loads` with `table` = `merge_field` or `template`, a file and `validFrom`. |
| Preconditions | RWB-E1-012 done; `template` table present; P4 load path live; LOV-LANG, LOV-PRODUCT and LOV-NOTICE loaded; merge field file prepared; loader holds Reference data C; Legal approval on the file where the version is Approved. |
| Input | Merge field catalog file; template version file; `sys_fields`; lists of values. |
| Output | `merge_field` rows by catalog version; `template` rows by code, language and version; reference load result; ACE audit entry; `TemplateCatalog` reads. |
| Feature flag | `rwb.comms.template-catalog`. Off: handlers not registered and the catalog not published; RWB-E1-052 is off in the same release. |
## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `template` | `template_code`, `template_version`, `language` | Load file; next number | Loader writes | varchar(30), integer, TH/EN; unique together |
| `template` | `product_group`, `channel`, `notice_type`, `signature_basis` | Load file | Loader writes | Must belong to LOV-PRODUCT, LOV-CHANNEL, LOV-NOTICE, LOV-SIGNATURE-BASIS |
| `template` | `body_ref` | Load file; write-once object key | Loader writes | Required; the DOCX must exist and parse |
| `template` | `merge_codes` | Load file and body scan | Loader writes | jsonb array; must equal the `{{CODE}}` set in the body |
| `template` | `approved_by`, `approved_at`, `approved_by_legal` | Load file; derived | Loader writes | Both required when APPROVED; boolean follows |
| `template` | `valid_from` | Load file | Loader writes | Date; future date allowed |
| `template` | `state` | Derived | Loader writes | DRAFT, APPROVED or WITHDRAWN only |
| `merge_field` | `merge_code`, `catalog_version`, `valid_from` | Load file | Loader writes | Unique within the catalog version; version in force by date |
| `merge_field` | `source_entity`, `source_field`, `field_id` | Load file | Loader writes | Entity and field present; `field_id` in `sys_fields` |
| `merge_field` | `is_required`, `personal_data` | Load file | Loader writes | Booleans; required flag must be set |
| `lov_value` | `lov_code`, `value_code` | Reference data | Read-only | Values must belong to the named list |
## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| — | Template row loaded | `approved_by` and `approved_at` absent | `DRAFT` | Row inserted; earlier versions unchanged |
| — | Template row loaded | Both approval columns present | `APPROVED` | Row inserted with approver and time |
| `DRAFT` | Approval recorded | RWB-E1-034 approve; this story only reads the result | `APPROVED` | RWB-E1-034 owns this transition; the catalog then returns the version from its valid-from date |
| `APPROVED` | Withdrawal | RWB-E1-034 withdraw with reason | `WITHDRAWN` | No current version; MSG-P6-003 |
| — | Merge field load | All rows valid | In force | Catalog version available from `valid_from` |
| — | Any load | One row refused | Refused | No row written; previous data stays; MSG-P1-002 |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event | SPEC |
|---|---|---|---|---|
| X1 | All versions Draft | `TemplateNotApprovedException`; nothing generated | MSG-P6-005 | SPEC-009 |
| X2 | Unknown merge code in body or list | Whole load refused; code named; no version | MSG-P6-006 | SPEC-005 |
| X3 | BR Field ID not in `sys_fields` | Whole catalog load refused; catalog in force stays | MSG-P1-002 | SPEC-002 |
| X4 | Missing code, language or body reference | Whole load refused; field named | MSG-GEN-001 | SPEC-004 |
| X5 | Same file hash loaded twice | 409; no new version | MSG-P1-002 | SPEC-012 |
| X6 | Only Approved version withdrawn | `TemplateWithdrawnException`; generation holds | MSG-P6-003 | SPEC-010 |
| X7 | `valid_from` in the future | Earlier Approved version stays current until the date | None | SPEC-013 |
## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoint used | `POST /api/recovery/v1/admin/reference-loads` (P4, E1): multipart `file`, `table`, `validFrom`; response `ReferenceLoad`. |
| Contract delta | None to the schema. The endpoint accepts two further table codes, `template` and `merge_field`, through the registered `ReferenceLoadHandler`. |
| Backward compatibility | Unchanged; other table handlers are unaffected. |
| Authorization | Reference data C. 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P1-002; 422 MSG-GEN-001, MSG-P6-006, MSG-P1-002; 503 MSG-GEN-006. |
| Versioning | No version change. |
## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change. | Existing frontend tests stay green; no new test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR7; SPEC-RWB-E1-046-001..018 | Two handlers, a scanner, version assignment and catalog selection are new units. | Each required field; unknown field ID; unknown merge code; body/list mismatch; repeat hash; version 1→2; Draft/Approved/Withdrawn; valid-from boundary; future version; audit result. |
## Detailed design
### Components

| Component | Type | Responsibility |
|---|---|---|
| `TemplateEntity` / `MergeFieldEntity` | Entity | Map `template` and `merge_field`. |
| `TemplateRepository` | Repository | Current version by code, language and date; next number under a row lock. |
| `MergeFieldRepository` | Repository | Catalog version in force; writes rows by `catalog_version`. |
| `TemplateLoadHandler` | Service | `ReferenceLoadHandler` for `template`: parse, validate, scan, version, derive state. |
| `MergeFieldLoadHandler` | Service | `ReferenceLoadHandler` for `merge_field`: uniqueness, `sys_fields`, source entity/field, required flag. |
| `MergeCodeScanner` | Service | Reads `{{CODE}}` tokens from a DOCX body. |
| `TemplateCatalogService` | Published interface | Implements `current`, `version`, `mergeFields`; raises the two exceptions. |
### Package and boundaries

Package `recovery.comms.templates`, folder `recovery/comms/templates`. The catalog is a published P6 interface; other modules call it only through the interface. `sys_fields` is read through P4, never by querying P4 tables. The body is read from the ACE write-once container through the storage interface (DL27).
### Data and migration

- `V1_046__template_catalog.sql`: creates `merge_field`; alters `template` to add `approved_by`, `approved_at`, `valid_from`, `channel`, `notice_type`, `signature_basis` and `merge_codes`.
- Replaces `uk_template (template_code)` with `uk_template_version (template_code, language, template_version)`.
- Adds `ck_template_state` (`DRAFT`, `APPROVED`, `WITHDRAWN`) and `ck_template_approval` (both approval columns set when APPROVED).
- `merge_field` has `uk_merge_code_version (merge_code, catalog_version)`.
- Reads `lov_value` and `sys_fields`; no hard-coded code, language, merge code, field ID or date.
### Load validation and versioning

1. Resolve the handler by `table`; reject an unregistered table through P4.
2. Parse the whole file and validate every row before writing anything.
3. `merge_field`: `merge_code` unique in `catalog_version`; `field_id` in `sys_fields`; `source_entity` and `source_field` present; `is_required` set.
4. `template`: code, language and `body_ref` present; the body resolves and parses; list values valid.
5. Scan the body; require the body set and the declared `merge_codes` set to be equal; check every code against the catalog in force.
6. Assign `template_version` = highest existing for the code and language + 1, under a row lock; derive `state` and `approved_by_legal`; apply all rows in one transaction.
7. Write rows loaded, rows refused and versions assigned to the P4 load record and the ACE audit log.
### Catalog selection

`current(templateCode, language, onDate)` returns the Approved version with the highest `template_version` whose `valid_from` is on or before `onDate`. A future-dated version is ignored until its date. No Approved version → `TemplateNotApprovedException` (MSG-P6-005); the only Approved version Withdrawn → `TemplateWithdrawnException` (MSG-P6-003). `version(...)` reads an earlier version; `mergeFields(...)` returns its catalog rows. `TemplateVersion` carries no personal data.
### Transaction, security and operations

One load is one transaction for the rows. A refused load writes no row and leaves the load record at `REFUSED` with the failed check. No domain event is published; the load record and audit entry are the outcome.

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data C; loads both files | All |
| RW-LEGAL | Documents A; approves wording | All |
| RW-LITOFF | Documents R; reads templates | All |
| RW-COE | Reference data R; reads the catalog | All |
| SY-CASEWF | Calls `TemplateCatalog` | All |

Every load is checked for Reference data C; the audit entry records the loader, table, file hash and versions. The Legal approver is stored from the file; CTL-05 is enforced on the E1-034 approval action.

- Metrics: loads by table and status; rows refused; catalog lookups; refusals by exception type.
- Alerts: refused catalog load; repeated no-Approved requests; audit write failure.
- Run book: load order (merge fields before templates), repeat-hash behaviour, escalation to RW-REFADM (RWB-E1-056).
- Performance: one indexed catalog query per generation; no numeric target, record the SIT load time (DL11).
### Feature flag and rollback

`rwb.comms.template-catalog`. Off: handlers not registered, a load for these tables is refused as unsupported, and the catalog is not published; RWB-E1-052 is off in the same release. Rollback: turn both flags off and redeploy the previous tag; the migration is additive and forward-only.
## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-046-01 | AC1, BR1, BR2, BR6 | System | MF-2026.11; DEMAND-MTG TH v1 Approved; load v2 | v2 Approved; catalog returns v2; v1 readable |
| TC-E1-046-02 | AC2, BR1 | System | RECALL-HP TH with one Draft | `TemplateNotApprovedException`; MSG-P6-005 |
| TC-E1-046-03 | AC3, BR4 | System | GUARANTOR-SSME body using GUARANTOR_EMAIL | Whole load refused; MSG-P6-006; no version |
| TC-E1-046-04 | AC4, BR4, BR5 | System | Catalog file of 12 rows, row 7 field ID XX-CAS-999 | Whole load refused; MSG-P1-002; MF-2026.11 stays |
| TC-E1-046-05 | AC5, BR5 | System | Template row with empty `body_ref` | Whole load refused; MSG-GEN-001 naming `body_ref` |
| TC-E1-046-06 | AC6 | System | The AC1 file loaded twice | 409; MSG-P1-002 `repeat of load`; still 2 versions |
| TC-E1-046-07 | AC7, BR3 | System | DEMAND-MTG TH v2 Withdrawn | `TemplateWithdrawnException`; MSG-P6-003 |
| TC-E1-046-08 | AC8, BR2 | System | v3 valid from 2026-12-01 | v2 on 2026-11-30; v3 on 2026-12-01 |
| TC-E1-046-09 | Access | Security | RW-LITOFF calls the load endpoint | 403; MSG-P4-002 |
| TC-E1-046-10 | BR4, BR5 | Unit | Body/list mismatch; unknown field; duplicate code | Refusal naming the code or field; no partial write |
## Guardrails

- No business value in code: template codes, languages, merge codes, field mappings, lists and dates are rows.
- No personal data in logs, tests or prompts; template bodies use synthetic wording; merge values never appear in logs.
- No read of another module's tables; `sys_fields` through P4; body through the storage interface; earlier versions never updated or deleted.
## Out of scope

- The SCR-33 upload, approve and withdraw screen (RWB-E1-034).
- Generating notices from the templates (RWB-E1-052).
- Contract, credit approval and mortgage document generation (RWB-E2-026).
- The Compliance approval path for a template (FEAT-ADM-05, Epic 8).
## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | Epic 1 §3.6, §4 | FEAT-DRI-16 | 13 Manage documents and correspondence | R-LIT-03 | TC-E1-046-02, 03, 04 |
| REQ-OCC-002 | Templates versioned, Legal approval recorded against the version | Epic 1 §3.6, §4 | FEAT-DRI-16 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06 | TC-E1-046-01, 05–09 |
## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC2; SPEC-009 | What if the code and language have no template row at all? | The refusal path must still name a template and version. | Treat it as no Approved version: `TemplateNotApprovedException` with MSG-P6-005 naming the code and version 0. | RESOLVED | SPEC-009 |
| CLAR-002 | §4 step 2; SPEC-002 | The story lists the merge field checks but not the load file format or column order. | The handler cannot parse a file without a format. | Use the P4 delimited format with a header row naming the fields in §11; confirm the delimiter with P4 before build. | RESOLVED | SPEC-002 |
| CLAR-003 | BR7, §10; SPEC-007 | Legal approves through the load file, but the loader holds Reference data C and Legal does not. | The audit trail could show the loader rather than Legal as approver. | The file carries the Legal approver ID and date; the version stores them; the audit entry records the loader and the approval reference. CTL-05 is enforced on SCR-33. | RESOLVED | SPEC-007, SPEC-015 |
| CLAR-004 | §4 step 4; SPEC-005 | Must the declared `merge_codes` list equal the `{{CODE}}` set in the body? | An undeclared body code would render unfilled; a declared code absent from the body is dead data. | Yes. The sets must be equal; the union is checked against the catalog. A body code missing from the list refuses with MSG-P6-006; a listed code absent from the body refuses with MSG-GEN-001 naming `merge_codes`. | RESOLVED | SPEC-005 |
| CLAR-005 | AC1; SPEC-006 | Is the version number per template code or per code and language? | Determines the next number and the unique key. | Per code and language, as §4 step 5 and `uk_template_version` state. A new language starts at version 1. | RESOLVED | SPEC-006 |
| CLAR-006 | AC6; SPEC-012 | Does a repeat load return 409 or 422? | Determines the API response the administrator sees. | 409, as §12 and the P4 contract state; MSG-P1-002 names `repeat of load`. | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, the P4 contract, DL27/DL28 or the data dictionary. No item changes the business outcome.
## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend reference data story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New template and merge field catalog with two P4 load handlers and a published TemplateCatalog; existing reference load endpoint reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: catalog data and load handlers, no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria and 7 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
