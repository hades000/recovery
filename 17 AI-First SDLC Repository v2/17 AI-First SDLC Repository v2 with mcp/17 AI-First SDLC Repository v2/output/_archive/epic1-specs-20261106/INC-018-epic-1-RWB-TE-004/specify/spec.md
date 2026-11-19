# Technical Specification — RWB-TE-004 Masked data in SIT and UAT

| Field | Value |
|---|---|
| Story | RWB-TE-004 — Masked data in SIT and UAT |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-018-epic-1-RWB-TE-004` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-010, REQ-ACA-005); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 004 Masked data in SIT and UAT v1.md` |
| Upstream IDs | REQ-RDF-010, REQ-ACA-005; US-RWB-TE-004; NFR-045; CTL-02; CTL-11; DL26 |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The pipeline report is the surface; story §15. |
| Logic In Scope | `YES` — environment guard, manifest validation, CTL-02 checks, masking verification, staging swap, load report. |
| API In Scope | `NO` — no new or changed contract. The SIT service uses the existing `GET /api/recovery/v1/cases/{caseId}`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | SIT/UAT recovery schema; PII service intake container; `sys_fields.is_personal`; RWB-E1-065 verifier patterns. |
| New Nodes Required | `YES` — `MaskedCopyLoader`, `ManifestValidator`, `MaskingVerifier`, `LoadReportWriter`, masked-copy stage, `tools.masked_copy_load`. |
| Inherited Existing Behavior | PII service extract and manifest (bank); `sys_fields` personal tags (RWB-E1-001); personal-pattern verifier (RWB-E1-065); reference-data masking rules (DL26). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | No production data in DEV; SIT and UAT use masked copies only. | SPEC-RWB-TE-004-001, 012 | DIRECT | Environment guard refuses DEV and PROD before reading a file. | COVERED |
| BR2 | Every personal field is masked or tokenized under the masking rules in force. | SPEC-RWB-TE-004-004, 006, 013 | DIRECT | `sys_fields.is_personal`; masking rule version; token per customer. | COVERED |
| BR3 | A copy with any personal value left is refused whole. | SPEC-RWB-TE-004-004, 005 | DIRECT | `MaskingVerifier`; previous copy stays. | COVERED |
| BR4 | Balances, dates and keys are not masked; counts and totals equal the manifest. | SPEC-RWB-TE-004-003, 007 | DIRECT | CTL-02 row count and balance sum per file. | COVERED |
| BR5 | The same customer gets the same token in every table, so joins hold. | SPEC-RWB-TE-004-006 | DIRECT | Token map by customer key; no per-table random token. | COVERED |
| BR6 | With no masking rule loaded, every personal field is replaced by a token. | SPEC-RWB-TE-004-013 | DIRECT | Default-deny masking. | COVERED |
| X1 | A personal value is left in a column. | SPEC-RWB-TE-004-004 | DIRECT | Refuse whole; previous copy stays. | COVERED |
| X2 | Row count or balance differs from the manifest. | SPEC-RWB-TE-004-003 | DIRECT | Refuse whole. | COVERED |
| X3 | Target environment is DEV or PROD. | SPEC-RWB-TE-004-001 | DIRECT | Refuse before reading. | COVERED |
| X4 | Same extract ID again. | SPEC-RWB-TE-004-008 | DIRECT | Skip; report names the earlier load. | COVERED |
| X5 | Masking rule version not in force. | SPEC-RWB-TE-004-002 | DIRECT | Refuse whole. | COVERED |
| X6 | Second load starts while one runs. | SPEC-RWB-TE-004-009 | DIRECT | 409 MSG-P2-006. | COVERED |

> **AC cleanup (4 November 2026):** all previous acceptance criteria in this story were development-process criteria and were removed from story §7. This engineering enabler has no business acceptance criteria; the coverage table above maps the business rules and exception paths only.

## User story intent interpretation

As a **Tribe lead and squad member (RW-TRIBE)**, I want **masked copies of recovery data loaded into SIT and UAT from the PII service**, so that **tests run on realistic volumes without exposing customers**.

The bank's PII service produces the masked extract. This story loads it into SIT or UAT only, refuses any copy that still holds a personal value, and keeps balances, dates and keys unchanged so counts and reconciliations behave as in production.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Manual start by RW-PLATADM for SIT or UAT after the PII service delivers an extract. |
| Preconditions | RWB-E1-065 done (pattern checks and `is_personal` tags); PII service extract and manifest in the intake container; masking rule version in force (DL26); SIT/UAT schema at the extract's Flyway version; RW-PLATADM starts the load. |
| Input | Masked extract files and manifest: extract ID, business date, masking rule version, row count and balance totals per table. |
| Output | Recovery schema in SIT/UAT replaced by the masked copy; load report with extract ID, date, rule version, rows and totals per table and checks. |
| Feature flag | `rwb.dataengine.masked-copy`. Off: the stage is unavailable. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `party` | `id_no_token`, `first_name`, `last_name`, `date_of_birth` | PII masked extract | Load only | Must be a token or masked value; no valid national ID, name or date pattern. |
| `contact_point` | `value_token` | PII masked extract | Load only | Token or masked; no real mobile or email. |
| `loan_account` | `account_no`, `total_balance`, `days_past_due` | PII extract | Load only | Not masked; counts and sums match the manifest. |
| `recovery_case` | `case_no`, `status`, `owner_user_id` | PII extract | Load only | Not masked; keys preserved. |
| `case_party` | `party_id`, `case_id` | PII extract | Load only | Same token joins to the same party. |
| `tools.masked_copy_load` | `extract_id`, `environment`, `business_date`, `masking_rule_version`, `result` | Stage | Tool only | Unique extract per environment; no personal values. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Stage start | Target SIT/UAT; lock acquired | Running | Manifest read; staging schema prepared. |
| Running | All checks pass | Manifest, CTL-02, masking, FK | Loaded | `recovery_next` swapped to `recovery`; report written. |
| Running | Any check fails | Guard, manifest, total or personal value | Refused | Previous copy stays; report names the check. |
| Running | Extract ID already loaded | Same environment | Skipped | Report names the earlier load; no file read. |
| Running | Second start | Lock held | Refused | 409 MSG-P2-006. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Personal value left in a column | Refuse whole; previous copy stays. | MSG-P1-002; check names table.column |
| X2 | Row count or balance differs from the manifest | Refuse whole; previous copy stays. | MSG-P1-002; control-total check |
| X3 | Target is DEV or PROD | Refuse before reading any file. | MSG-P1-002; environment check |
| X4 | Same extract ID again | Skip; report names the earlier load. | None |
| X5 | Masking rule version not in force | Refuse whole. | MSG-P1-002; version check |
| X6 | Second load while one runs | Refuse the second. | MSG-P2-006 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/cases/{caseId}` in SIT/UAT for a test user to read a masked case. |
| Contract delta | None. |
| Backward compatibility | Unchanged. |
| Authorization | Case record R; scope applied; 403 MSG-P4-002; 404 MSG-P4-003. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; test users see the masked copy through existing screens. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-010, REQ-ACA-005; SPEC-RWB-TE-004-001..014 | New loader, manifest validator, masking verifier, report writer and stage. | Positive, negative, boundary and error-path tests: environment guard; manifest; CTL-02; national ID, mobile and email patterns; token consistency; duplicate extract; lock. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `MaskedCopyLoader` | Job | Spring Batch: environment guard, manifest checks, staging load, swap. |
| `ManifestValidator` | Service | Extract ID, masking rule version, schema version, control totals. |
| `MaskingVerifier` | Service | Personal-pattern scan on every `is_personal` column; reuses RWB-E1-065 patterns. |
| `LoadReportWriter` | Service | Writes the load report for the pipeline. |
| Masked copy stage | Job | SIT/UAT pipeline stage with a per-environment lock. |

### Data and migration

- No new recovery table. The stage loads into `recovery_next` in SIT or UAT and renames it to `recovery` after every check.
- `tools.masked_copy_load` records extract ID, environment, business date, masking rule version and result; unique `(extract_id, environment)`.
- The target schema must be at the same Flyway version as the extract; otherwise the manifest check refuses.
- No copy is made from SIT or UAT to another environment.

### Rules

1. Environment guard: only SIT and UAT; DEV and PROD are refused before any file read.
2. Manifest: extract ID not loaded before; masking rule version equals the version in force; schema version equals the target.
3. CTL-02 per file: business date, structure, control totals (row count and balance sum) and keys.
4. `MaskingVerifier` scans every `is_personal` column for a 13-digit Thai national ID with a valid check digit, a Thai mobile number or an email address.
5. Token consistency: one token per customer across `party`, `contact_point`, `case_party` and `loan_account`.
6. Balances, dates and keys are not masked.
7. With no masking rule loaded, every personal field is tokenized (default deny).

### Transaction and events

- Files load into `recovery_next`; the swap is one step after every check.
- A failure leaves the previous `recovery` schema in place.
- No event is published; the load report is the record.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM | Start the load; own the intake containers | SIT, UAT |
| RW-COMPLY | Own the masking rules and version | All |
| RW-TRIBE | Run tests on the loaded copy | SIT, UAT |
| SY-DATALOAD | Identity the loader runs under | SIT, UAT |
| Any other role | No load or read | 403 MSG-P4-002 |

The load report holds counts, totals and check names, never a value. Test extracts are built from synthetic data.

### Observability and operations

- Pipeline report: extract ID, environment, business date, masking rule version, rows and totals per table, check results.
- `tools.masked_copy_load` is the audit record of each load.
- No runtime metric or alert; a failed load is visible in the pipeline.

### Performance

- 28,119 accounts plus parties, contacts, cases and interactions; the load is set-based per file.
- The per-environment advisory lock serialises loads; a second start is refused.
- The masking scan is a single pass per personal column.

### Feature flag and rollback

- `rwb.dataengine.masked-copy`. Off: the stage is unavailable.
- Rollback: the previous `recovery` schema stays until the swap; a failed load never replaces it. No copy leaves SIT/UAT.

### No UI change

No screen. The platform administrator and squads read the pipeline report; test users see the masked copy through existing screens.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-004-01 | BR2, BR4, BR5 | System | PII-SIT-20261120; 28,119 accounts | Personal fields tokenized; counts and sums match; joins hold |
| TC-TE-004-02 | BR3 | System | Valid national ID in party row 4,512 | Refused whole; MSG-P1-002; previous copy stays |
| TC-TE-004-03 | BR4 | System | 28,118-row loan_account file | Refused; control-total check |
| TC-TE-004-04 | BR1 | System | Target DEV | Refused; no file read |
| TC-TE-004-05 | Engineering verification | System | Extract loaded twice | Skipped; report names 2026-11-20 |
| TC-TE-004-06 | BR6 | System | Manifest MASK-2026.10 | Refused; version check |
| TC-TE-004-07 | Engineering verification | System | Two SIT loads at once | 409 MSG-P2-006 |
| TC-TE-004-08 | X1 | Security | RW-REFADM reads a SIT case | 403 MSG-P4-002 |
| TC-TE-004-09 | BR5 | Unit | Same customer in party and contact_point | Same token in both |
| TC-TE-004-10 | BR6 | Unit | No masking rule loaded | Every personal field tokenized |

## Guardrails

- Masking rules and their version belong to Compliance; allowed environments are properties.
- No personal data in logs, tests or prompts; the load report holds counts, totals and check names only.
- The loader is a tool outside the ACE service and runs only in SIT and UAT.
- No masked copy reaches DEV, and no copy is made from SIT or UAT to another environment.

## Out of scope

- Synthetic data in DEV (RWB-E1-065); masking rule values per field and role (DL26, Compliance); screen masking (RWB-E1-037).
- The PII service itself; the masked debt sale data tape (Epic 5).

## Traceability

| Requirement ID | Requirement (short) | Rules | Test cases |
|---|---|---|---|
| REQ-RDF-010 | Access per product; personal data masked under PDPA | CTL-02, CTL-11; DL26 | TC-TE-004-01..07 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | CTL-11 | TC-TE-004-01, 08 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4; SPEC-003 | Flow step 5 runs CTL-02 before the staging load; §13 step 3 runs it during the load into `recovery_next`. | When a bad file is detected. | Run the checks while reading each file into `recovery_next`, before the swap. No live copy is exposed either way. | `RESOLVED` | SPEC-003 |
| CLAR-002 | BR2, BR3; SPEC-004 | Flow step 6 verifies masking before the staging load; §13 step 4 verifies after the load into `recovery_next`. | When an unmasked value is detected. | Verify in `recovery_next` before the swap; no live copy is exposed. | `RESOLVED` | SPEC-004 |
| CLAR-003 | BR4, SPEC-007 | Are balances, dates and keys copied unchanged? | Reconciliation behaviour. | BR4: not masked; counts and totals equal the manifest. | `RESOLVED` | SPEC-007 |
| CLAR-004 | BR6, SPEC-013 | What if no masking rule is loaded? | Default masking. | DL26: every personal field is replaced by a token. | `RESOLVED` | SPEC-013 |
| CLAR-005 | SPEC-009 | Is the second load refused or queued? | Concurrency behaviour. | X6: refused with 409 MSG-P2-006; one load continues. | `RESOLVED` | SPEC-009 |

`CLARIFICATION_STATUS: RESOLVED` — all 5 items are answered from the story, its ACs or DL26. No open
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this pipeline story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New SIT/UAT masked-copy loader and verifier; no UI or API contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: pipeline tool with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: No business acceptance criteria (story §7); all 6 business rules, and 6 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
