# Technical Specification — RWB-E1-038 Delegation of authority table as reference data

| Field | Value |
|---|---|
| Story | RWB-E1-038 — Delegation of authority table as reference data |
| Epic / module | E1 / P4 Access and administration |
| RUN_ID | `INC-027-epic-1-RWB-E1-038` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-012); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 038 Delegation of authority table as reference data v1.md` |
| Upstream IDs | BRD-RWB-004; FR-RWB-012; REQ-ACA-004, REQ-APD-010; US-RWB-E1-038; FEAT-ACA-06, FEAT-APD-10; CTL-04, CTL-08; R-UNI-38, R-UNI-39; DF-REF-016..026, DF-REF-055..062; DL18 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Delegation versions arrive by file load until SCR-41 in Epic 8; the load response and difference report are read from the API. |
| Logic In Scope | `YES` — whole-file validation, approval, effective dating, lookup by level, related-party rule, delay-count rule, NOT_COVERED incident. |
| API In Scope | `NO` — no new or changed endpoint. Reuses `POST /api/recovery/v1/admin/reference-loads` and `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve` (delivered by RWB-E1-043). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | Reference-load and approval service (RWB-E1-043); `delegation_limit` table (RWB-E1-001); approval router consumer (RWB-E2-013); decision log writer (RWB-E1-027). |
| New Nodes Required | `YES` — `DelegationLimitLoader`, `DelegationLookupService`, `DelegationLimitRepository`, `DelegationLimit`, `DelegationOfAuthority`, `delegation_limit` columns and `ix_delegation_lookup`. |
| Inherited Existing Behavior | Reference load/approve/rollback (RWB-E1-043); rule load template and rollback (RWB-E1-029); decision log writer (RWB-E1-027); parameter catalogue (RWB-E1-042); LOV-DECISION, LOV-APPROVAL-LEVEL, LOV-PRODUCT. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Limits are held as the regulation states: principal in baht, loss percentage, maximum loss in baht, price against fair market value and against principal outstanding; empty means no limit. | SPEC-RWB-E1-038-001, SPEC-RWB-E1-038-010, SPEC-RWB-E1-038-011 | DIRECT | Amounts stored as numeric(18,2); no conversion at lookup. | COVERED |
| BR2 | Where a level has two rows, the approval is within limit if either row is met. | SPEC-RWB-E1-038-005 | DIRECT | Any matching row at the level accepts. | COVERED |
| BR3 | The lowest level from L6 up to L1 with a row for the decision and regulation item valid on the date that covers the request is returned. | SPEC-RWB-E1-038-004, SPEC-RWB-E1-038-009 | DIRECT | Walk L6 → L1; date-valid rows only. | COVERED |
| BR4 | A decision no limit covers goes to the next level up; no row at any level returns NOT_COVERED and raises an incident. | SPEC-RWB-E1-038-004, SPEC-RWB-E1-038-008 | DIRECT | Walk continues; final NOT_COVERED. | COVERED |
| BR5 | A write-off for a director, senior executive, major shareholder or related party goes to the Board (L1). | SPEC-RWB-E1-038-006 | DIRECT | `relatedParty` + write-off rows; reason `RELATED_PARTY`. | COVERED |
| BR6 | A delay of legal action, seizure or auction is within limit only while the delay count, including this one, is not above the level's delay count. | SPEC-RWB-E1-038-007 | DIRECT | `delayCount <= max_delay_count`. | COVERED |
| BR7 | A decision keeps the version it was approved under; a new version applies from its valid from date. | SPEC-RWB-E1-038-003, SPEC-RWB-E1-038-009 | DIRECT | `limit_version` on the result; approval stores it. | COVERED |
| BR8 | A limit change is a data load approved by Risk, never by its loader. | SPEC-RWB-E1-038-002, SPEC-RWB-E1-038-013 | DIRECT | `rwb.refload.approver.delegation_limit=RW-RISK`; maker-checker. | COVERED |
| BR9 | Hire purchase and unsecured limits follow chapter 8 and load when supplied. | SPEC-RWB-E1-038-008, SPEC-RWB-E1-038-012 | DIRECT | No rows means NOT_COVERED; no invented limits. | COVERED |
| BR10 | An approval that cannot be written to the decision log does not take effect. | SPEC-RWB-E1-038-014 | DIRECT | Log write last; rollback on failure. | COVERED |
| AC1 | DOA-2026.11 stores 218 rows: 109 MORTGAGE and 109 SSME; every row has decision, level and product; item 2.1.1 L4 has two rows. | SPEC-RWB-E1-038-001, SPEC-RWB-E1-038-011 | DIRECT | 95 matrix limits expand to two products. | COVERED |
| AC2 | D6.4 item 2.1.1 MORTGAGE 2.4M, loss 20%, loss amount 480k returns L6, row ID and DOA-2026.11. | SPEC-RWB-E1-038-004 | DIRECT | Walk from L6. | COVERED |
| AC3 | DOA-2027.01 adds item 2.1.5 L5 10M from 2027-01-01; DOA-2026.11 stays readable to 2026-12-31; lookup on 2 Jan 2027 returns L5; one log entry. | SPEC-RWB-E1-038-003, SPEC-RWB-E1-038-009 | DIRECT | Previous version closed on approval. | COVERED |
| AC4 | A file with L5 400M above L4 300M and decision D6.9 is refused whole; DOA-2026.11 stays. | SPEC-RWB-E1-038-001 | DIRECT | Monotonic limit check; unknown code. | COVERED |
| AC5 | The loader cannot approve; RW-PRODHEAD is refused 403. | SPEC-RWB-E1-038-002 | DIRECT | MSG-P7-002 then MSG-P4-002. | COVERED |
| AC6 | Decision log unavailable: approve returns 503 MSG-P7-003; load stays Loaded. | SPEC-RWB-E1-038-014 | DIRECT | Rollback. | COVERED |
| AC7 | No HIRE_PURCHASE rows: lookup returns NOT_COVERED and raises MSG-P7-010 to RW-RISK. | SPEC-RWB-E1-038-008 | DIRECT | Incident names decision and product. | COVERED |
| AC8 | DOA-2026.11 to 31 Dec 2026 and DOA-2027.01 from 1 Jan 2027: 31 Dec returns L4, 1 Jan returns L5. | SPEC-RWB-E1-038-009 | DIRECT | Decision date selects the version. | COVERED |
| AC9 | D9.2 item 2.1.10 SSME 300k with related party true returns L1 reason RELATED_PARTY. | SPEC-RWB-E1-038-006 | DIRECT | Board override. | COVERED |
| X1 | A file repeats a row or a level's highest principal limit falls below a lower level's. | SPEC-RWB-E1-038-001 | DIRECT | Whole-file refusal. | COVERED |
| X2 | Unknown decision, level or product, or an empty required field. | SPEC-RWB-E1-038-001 | DIRECT | Whole-file refusal. | COVERED |
| X3 | The loader approves their own version. | SPEC-RWB-E1-038-002 | DIRECT | MSG-P7-002. | COVERED |
| X4 | A role other than RW-RISK approves. | SPEC-RWB-E1-038-002, SPEC-RWB-E1-038-013 | DIRECT | 403 MSG-P4-002. | COVERED |
| X5 | The decision log write fails during approval. | SPEC-RWB-E1-038-014 | DIRECT | Stays Loaded. | COVERED |
| X6 | No row covers the decision and product. | SPEC-RWB-E1-038-008 | DIRECT | NOT_COVERED; incident. | COVERED |
| X7 | Lookup on the last day of the old version or the first day of the new one. | SPEC-RWB-E1-038-009 | DIRECT | Date-valid version. | COVERED |
| X8 | A write-off for a related party. | SPEC-RWB-E1-038-006 | DIRECT | L1. | COVERED |

## User story intent interpretation

As a **risk and model risk officer (RW-RISK)**, I want **the delegation of authority held as a versioned table that the approval router reads**, so that **approval limits change by an approved data load and every approval can be checked against the limit that applied on its date**.

The story is the data behind the Epic 2 approval router. It adds no screen: it loads the 95 regulation limits as 218 product rows, lets Risk approve a version, and gives the router one lookup that returns the lowest level whose limit covers the decision, with the version used. When no limit covers the request, the decision is held and Risk is told.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `POST /admin/reference-loads` for table `delegation_limit`; `POST /admin/reference-loads/{loadId}/approve`; `DelegationOfAuthority.lowestLevel` from the approval router. |
| Preconditions | RWB-E1-043 done; RWB-E1-029 done; RWB-E1-027 done; `delegation_limit` exists (RWB-E1-001); LOV-DECISION, LOV-APPROVAL-LEVEL and LOV-PRODUCT loaded; `rwb.refload.approver.delegation_limit=RW-RISK` in the catalogue; holders and substitutes empty in PROD (DL18). |
| Input | Delegation matrix load file, version name, valid from, caller identity; lookup request with decision, regulation item, product, amounts, conditions, related-party flag and decision date. |
| Output | `delegation_limit` rows; approved version; `DelegationResult` (`COVERED`/`NOT_COVERED`, level, row IDs, version, reason, holder, substitute); incident when not covered. |
| Feature flag | `rwb.access.delegation-table`. Off: the lookup is not published to the router and E2 approval routing stays disabled; load and approve remain available for data preparation. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `delegation_limit` | `decision_code`, `regulation_item`, `product_group`, `approval_level` | Load file | Data load only | Known LOV values; required. |
| `delegation_limit` | `principal_limit`, `loss_pct_limit`, `max_loss_amount`, `min_price_pct_fmv`, `min_price_pct_principal`, `min_received_pct`, `max_delay_count`, `max_term_years` | Load file | Data load only | Numeric; empty means no limit; amounts in baht, 2 decimals. |
| `delegation_limit` | `applies_when` | Load file | Data load only | `WO_CRITERIA_MET`, `WO_CRITERIA_NOT_MET` or null; null applies to any request. |
| `delegation_limit` | `limit_version`, `valid_from`, `valid_to` | Load / approval | Data load only | New version from its valid from; previous `valid_to` set to the day before. |
| `delegation_limit` | `holder_user_id`, `substitute_user_id` | Load / DL18 | Data load only | Empty in PROD; named test users in SIT and UAT. |
| `decision_log_entry` | `decision_code`, `final_call`, `actions` | Approval | System | One `AC-VERS` entry per approved version. |
| `DelegationResult` | `status`, `approvalLevel`, `rowIds`, `limitVersion`, `reason` | Lookup | System | `NOT_COVERED` when no row covers. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load | Every check passes | Loaded | Rows written; not in force. |
| None | Load | Any check fails | Refused | No row written; version in force stays. |
| Loaded | Approve | RW-RISK, not the loader, log written | Approved | Valid from recorded; previous version's `valid_to` set. |
| Loaded | Approve | Loader, wrong role, or log failure | Loaded | 409/403/503; nothing changes. |
| Approved | New version approved | Later valid from | Superseded | Previous rows readable with `valid_to`. |

No case status changes in this story.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Duplicate row or falling principal limit | Load refused whole; version in force stays | MSG-P1-002 |
| X2 | Unknown code or empty required field | Load refused whole | MSG-P1-002 |
| X3 | Loader approves own load | Refused; stays Loaded | MSG-P7-002 |
| X4 | Role other than RW-RISK approves | 403; stays Loaded | MSG-P4-002 |
| X5 | Decision log write fails | Approval rolled back; stays Loaded | MSG-P7-003 |
| X6 | No row covers the decision and product | `NOT_COVERED`; incident to RW-RISK | MSG-P7-010 |
| X7 | Lookup on a version boundary date | The version valid on that date is used | None |
| X8 | Write-off with related party true | L1 with reason `RELATED_PARTY` | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/reference-loads`; `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`. |
| Contract delta | None. `DelegationOfAuthority` is a published Java interface, not a REST contract. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load; the `delegation_limit` approver role parameter (RW-RISK) to approve. |
| Error behaviour | 401; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P7-002 / MSG-GEN-004; 422 MSG-P1-002; 503 MSG-P7-003 / MSG-GEN-006. |
| Versioning | No API version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state change; SCR-41 is Epic 8. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-012; SPEC-RWB-E1-038-001..014 | New loader, lookup service, repository, entity and migration. | Positive, negative, boundary and error paths: whole-file checks, falling limit, maker-checker, log failure, level walk, either-row, related party, delay count, date boundary, NOT_COVERED. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AccessAndAdministrationController` | Controller | Load and approve for `delegation_limit`. |
| `DelegationLimitLoader` | Service | Whole-file validation; stores the new version with `limit_version`. |
| `ReferenceLoadApprovalService` | Service | Approver role, maker-checker, decision log and status change; shared with RWB-E1-037. |
| `DelegationLookupService` | Published interface | Implements `DelegationOfAuthority.lowestLevel`. |
| `DelegationLimitRepository` | Repository | Reads rows valid on a date for decision, item, product and `applies_when`. |
| `DelegationLimit` | Entity | Maps `delegation_limit` with the new columns. |

### Package and boundaries

`recovery.access.delegation` holds the implementation; the published interface is `recovery.access.delegation.api`. The approval router calls only `DelegationOfAuthority`; no module reads `delegation_limit` directly.

### Data and migration

- Reads and writes `delegation_limit`: `decision_code`, `approval_level`, `product_group`, `principal_limit`, `loss_pct_limit`, `min_price_pct_fmv`, `holder_user_id`, `substitute_user_id`, `valid_from`, `valid_to`, `limit_version`, `regulation_item`, `applies_when`, `max_loss_amount`, `max_delay_count`, `min_price_pct_principal`, `min_received_pct`, `max_term_years`.
- Migration `V_E1_038__delegation_limit_columns.sql` adds `limit_version varchar(20) not null`, `regulation_item varchar(10) not null`, `applies_when varchar(40)`, `max_loss_amount numeric(18,2)`, `max_delay_count integer`, `min_price_pct_principal numeric(5,2)`, `min_received_pct numeric(5,2)`, `max_term_years numeric(4,1)`, and `ix_delegation_lookup` on `(decision_code, regulation_item, product_group, approval_level, valid_from) WHERE is_active`.
- No hard-coded limit, level, product or approver role.

### Load checks

1. Table code `delegation_limit`; `validFrom` is not before the business date and is after the current version's `valid_from`.
2. Every row has a known decision code, approval level L1–L6, product and regulation item; required fields are present.
3. No two rows repeat decision, regulation item, product, level, `applies_when` and limits.
4. For each decision, item, product and `applies_when`, the highest principal limit per level does not fall from L6 to L1.
5. Amounts are baht with two decimals; "No limit" loads empty; "Up to X%" loads `loss_pct_limit`; "At least X%" loads `min_price_pct_fmv`; "Once"/"Twice" loads `max_delay_count` 1/2.
6. Any failure refuses the load whole; no row is written and the version in force stays.

### Approval and effective dating

- The approver must hold `rwb.refload.approver.delegation_limit` (RW-RISK) and must not be the loader.
- Approval writes one `AC-VERS` decision log entry with the load ID, version, row count, approver and the new valid from date, sets the new version Approved and the previous version's `valid_to` to the day before the new `valid_from`, in one transaction.
- A failed log write rolls back the approval; the load stays Loaded (MSG-P7-003).
- An approved version is never edited; a change is a new version.

### Lookup algorithm

1. Select rows where `decision_code`, `regulation_item`, `product_group` match, `valid_from <= decisionDate` and (`valid_to` is null or `valid_to >= decisionDate`), and `applies_when` is null or equals the request value.
2. If `relatedParty = true` and the decision has write-off rows (`applies_when` starts `WO_`), return L1 with reason `RELATED_PARTY`, the matching L1 row IDs and the version.
3. Otherwise walk levels L6, L5, L4, L3, L2, L1. At each level, a row covers when every non-empty limit is met: principal ≤ `principal_limit`; loss % ≤ `loss_pct_limit`; loss amount ≤ `max_loss_amount`; price % FMV ≥ `min_price_pct_fmv`; price % principal ≥ `min_price_pct_principal`; received % ≥ `min_received_pct`; delay count ≤ `max_delay_count`; term years ≤ `max_term_years`.
4. The first level with at least one covering row wins; return all covering row IDs at that level, `limit_version`, holder and substitute.
5. If no level covers, return `NOT_COVERED` and raise an incident to the RW-RISK queue with MSG-P7-010 naming the decision and product.

### Related party and delay rules

- The related-party flag is supplied by the case/party data; the lookup does not infer it. A true flag on a write-off decision returns L1 regardless of amount.
- The delay count includes the delay being requested; a row with `max_delay_count = 2` covers the first and second delay, not the third.

### Transaction and events

The load and the approval are each one transaction; the approval log entry is written last. The lookup is read-only. The NOT_COVERED incident goes through the ACE incident path; no domain event is published.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data C (load); approves none | All |
| RW-RISK | Approver for `delegation_limit`; Rules and parameters RA | All |
| RW-PRODHEAD | Agrees limits with Risk; may not approve the load | All |
| RW-AUDIT | Reads every version and approval entry | All |
| SY-RULES | Calls the lookup for the approval router | All |

The approval role is a parameter, not a hard-coded role code. The loader and approver are separate people (CTL-08).

### Observability and performance

- Load response: row count, failed check and row, difference report.
- Reconciliation: 218 rows of DOA-2026.11 reconcile to the 95 matrix limits in SIT.
- Metrics: loads, refusals by check, approvals, lookups by level, NOT_COVERED incidents, lookup latency.
- Alerts: approval log failure; a NOT_COVERED incident; a version with no rows for an in-force product.
- Lookup is one indexed query plus an in-memory level walk over a small table.

### Feature flag and rollback

- `rwb.access.delegation-table`. Off: the lookup is not published to the router; load and approve remain available for data preparation.
- Rollback: turn the flag off and redeploy the previous tag; the added columns are nullable and harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-038-01 | AC1, BR1, BR2 | System | DOA-2026.11 from the 95 limits | 218 rows: 109 MORTGAGE, 109 SSME; item 2.1.1 L4 two rows |
| TC-E1-038-02 | AC2, BR3 | System | D6.4 MORTGAGE 2.4M, loss 20%, 480k | L6, row ID, DOA-2026.11 |
| TC-E1-038-03 | AC3, BR7 | System | DOA-2026.11 and DOA-2027.01 | Old rows valid to 2026-12-31; 2 Jan 2027 returns L5; one log entry |
| TC-E1-038-04 | AC4, BR1 | System | L5 400M above L4 300M; D6.9 | Refused; MSG-P1-002; no row; old version stays |
| TC-E1-038-05 | AC5, BR8 | System | Loader approves; RW-PRODHEAD approves | MSG-P7-002; then 403 MSG-P4-002 |
| TC-E1-038-06 | AC6, BR10 | System | Decision log store off | 503 MSG-P7-003; stays Loaded |
| TC-E1-038-07 | AC7, BR4, BR9 | System | HIRE_PURCHASE request | NOT_COVERED; MSG-P7-010 names D6.4 and HIRE_PURCHASE |
| TC-E1-038-08 | AC8, BR7 | System | Lookups on 31 Dec 2026 and 1 Jan 2027 | L4 then L5; version changes |
| TC-E1-038-09 | AC9, BR5 | System | D9.2 SSME 300k related party true | L1, reason RELATED_PARTY |
| TC-E1-038-10 | X1, X2 | Unit | Duplicate row; falling limit; unknown code | Refused; no row |
| TC-E1-038-11 | BR2, BR6 | Unit | Two rows at one level; delay counts 1, 2, 3 | Either row accepts; count boundary correct |

## Guardrails

- No business value in code: levels, limits, conditions, products and the approver role are data.
- No personal data in logs, tests or prompts; holders are test user references in SIT and UAT.
- No read of another module's tables; the router calls the published interface.
- No limit is converted or rounded at lookup time; amounts are stored in baht with two decimals.
- A version already approved is never edited; a change is a new version.

## Out of scope

- Routing an approval to the holder of the level, the queue and escalation (RWB-E2-013).
- Names of holders and substitutes, and the chapter 8 limits for hire purchase and unsecured loans (Risk with the product heads, DL18).
- The rule that new credit to a problem loan takes the higher of the restructuring and credit authorities (Epic 3).
- The Delegation of authority screen SCR-41 and moving a limit through screens (Epic 8, FEAT-ADM-03).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC1; SPEC-001 | Why 218 rows when the matrix has 95 limits? | Row count and reconciliation. | The 95 limits expand to two products: 109 MORTGAGE and 109 SSME. | RESOLVED | SPEC-001 |
| CLAR-002 | BR8; SPEC-002 | Who approves the delegation table? | Approval cannot proceed without an approver role. | `rwb.refload.approver.delegation_limit=RW-RISK`; the loader is never the approver. | RESOLVED | SPEC-002 |
| CLAR-003 | Preconditions; SPEC-011 | Are holders and substitutes loaded? | A missing holder would block routing. | Empty in PROD (DL18); named test users in SIT and UAT. | RESOLVED | SPEC-011 |
| CLAR-004 | BR9, AC7; SPEC-008 | What if a product has no rows? | HIRE_PURCHASE and UNSECURED arrive later. | Return NOT_COVERED and raise MSG-P7-010; do not invent a limit. | RESOLVED | SPEC-008 |
| CLAR-005 | BR5, AC9; SPEC-006 | How is a related party identified? | The lookup needs a flag, not a name. | The request carries `relatedParty`; a true flag on a decision with `WO_*` rows returns L1 `RELATED_PARTY`. No decision code is hard-coded. | RESOLVED | SPEC-006 |
| CLAR-006 | BR6; SPEC-007 | Does the delay count include the delay being requested? | Boundary at the maximum count. | Yes; `delayCount <= max_delay_count`. | RESOLVED | SPEC-007 |
| CLAR-007 | BR2; SPEC-005 | What if two rows at one level cover? | Which row ID to return. | Return all covering row IDs at the level; either row accepts. | RESOLVED | SPEC-005 |
| CLAR-008 | BR7, AC3; SPEC-003 | Can a new version start before the current one? | Overlapping versions would make the lookup ambiguous. | Refuse a `validFrom` not after the current version's `valid_from` with 422 MSG-P1-002. | RESOLVED | SPEC-003 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the delegation matrix, the reference-data process or the decision log. CLAR-005 and CLAR-008 are design resolutions with a named owner in the compliance review.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend reference-data story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New delegation-of-authority reference table, approval and lookup; no screen or contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new table columns, loader and published lookup on existing load/approve endpoints]
REQUIREMENT_COVERAGE_SUMMARY: All 10 business rules, 9 acceptance criteria, 8 exception paths and 5 version states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 10] [COVERED_RULES: 10] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
