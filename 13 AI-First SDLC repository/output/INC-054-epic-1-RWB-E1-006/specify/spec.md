# Technical Specification — RWB-E1-006 Data quality rules v1

| Field | Value |
|---|---|
| Story | RWB-E1-006 — Data quality rules v1 |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-054-epic-1-RWB-E1-006` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001; REQ-RDF-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 006 Data quality rules v1 v1.md`; FSD P1 A2.10; TSD P1 T3.1 (`dq_rule`, `dq_exception`) |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1; Program 5.1; REQ-RDF-008; FEAT-RDF-10; US-RWB-E1-006; R-UNI-17, R-UNI-38; CTL-08; DL16 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no Workbench screen. The data steward reads exceptions through the existing endpoint and the Power BI data quality report; SCR-45 is Epic 2. |
| Logic In Scope | `YES` — rule versioning, in-force selection, seven rule-type templates, rule validation, execution, exception write/clear and extract. |
| API In Scope | `NO` — no new or changed endpoint. The story uses the existing `GET /api/recovery/v1/admin/data-quality/exceptions` (API-P1-003) and the P4 reference-load endpoints. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `dq_rule` (new); `dq_exception` (extended); `load_run` (check results); `loan_account`, `account_payment`, `party`, `contact_point`, `account_collateral`, `case_list_row` (read); JOB-01, JOB-04, JOB-09. |
| New Nodes Required | `YES` — `DqRule`, `DqRuleRepository`, `DqRuleHandler`, `RuleTypeTemplates`, `DataQualityRuleRunner`, `DataQualityExtractWriter`. |
| Inherited Existing Behavior | Load framework, `load_run` and `dq_exception` (RWB-E1-003); `case_list_row` (RWB-E1-002); reference data handler (RWB-E1-043); parameter catalog (RWB-E1-042). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Data quality rules run on every load and every failed row carries a reason code. | SPEC-RWB-E1-006-005, 006 | DIRECT | Runner called from JOB-01/JOB-09 completion and the JOB-04 case list step. | COVERED |
| BR2 | Each rule is a versioned data row with valid from, valid to, approver and test case; a change needs no code release. | SPEC-RWB-E1-006-001, 004, 012 | DIRECT | `dq_rule` columns; reference handler. | COVERED |
| BR3 | A rule version takes effect on its valid-from date. | SPEC-RWB-E1-006-002 | DIRECT | `valid_from <= businessDate` and `valid_to` null or >=. | COVERED |
| BR4 | A rule version with an exception is refused in full. | SPEC-RWB-E1-006-004 | DIRECT | Whole-load validation before insert. | COVERED |
| BR5 | Rules read only P1-owned tables and columns the data dictionary holds. | SPEC-RWB-E1-006-003, 004 | DIRECT | Identifiers from `sys_fields`; allowed entity set. | COVERED |
| BR6 | Row rule codes DQ01–DQ10 are separate from load checks DQ-001–DQ-098. | SPEC-RWB-E1-006-006 | DIRECT | `check_code` holds the rule code; load checks unchanged. | COVERED |
| BR7 | DQ03 uses the entry threshold of 90 days past due. | SPEC-RWB-E1-006-011 | DIRECT | `case.entry.dpd` parameter. | COVERED |
| BR8 | A duplicate case found by DQ02 is merged by P3 under its own rule. | SPEC-RWB-E1-006-006 | DIRECT | The runner raises the exception only; merge is P3. | COVERED |
| AC1 | Three accounts each on two open cases produce three DQ02 rows; the endpoint returns them; the load_run shows DQ02 = 3. | SPEC-RWB-E1-006-005, 006, 008, 010 | DIRECT | Rule run and count. | COVERED |
| AC2 | The extract holds 19 rows with rule code, name, product, business date and record key; Power BI shows failures by rule, product and day. | SPEC-RWB-E1-006-009 | DIRECT | Extract writer in the JOB-04 publish step. | COVERED |
| AC3 | Rule version DQR-2026.12 adds DQ11 RANGE on `interest_rate` max 30.0000; it runs with no deployment and writes 2 exceptions. | SPEC-RWB-E1-006-002, 012 | DIRECT | New version loaded and approved; in-force query. | COVERED |
| AC4 | A rule naming `loan_account.balance_total` is refused with MSG-P1-005; DQR-2026.11 stays in force. | SPEC-RWB-E1-006-004 | DIRECT | `sys_fields` lookup. | COVERED |
| AC5 | A rule on `recovery_case.owner_user_id` is refused with MSG-P1-007 naming the allowed entities. | SPEC-RWB-E1-006-004 | DIRECT | Allowed-entity set. | COVERED |
| AC6 | A DQ05 statement timeout: DQ05 ERROR on the load_run; other rules run; MSG-P1-015. | SPEC-RWB-E1-006-005, 008 | DIRECT | 60-second per-rule limit; isolate failures. | COVERED |
| AC7 | Rules run twice for one load: no second exception row. | SPEC-RWB-E1-006-006 | DIRECT | Unique (`load_run_id`, `check_code`, `record_key`); ON CONFLICT DO NOTHING. | COVERED |
| AC8 | DQ07 valid to 2026-11-30 does not run on 2026-11-30; the check results do not list it. | SPEC-RWB-E1-006-002 | DIRECT | `valid_to` boundary. | COVERED |
| AC9 | An OPEN DQ01 exception whose account now has an owner is set CLEARED with the date. | SPEC-RWB-E1-006-007 | DIRECT | Clear by rule and record on a passing run. | COVERED |
| X1 | A rule names a field not in the dictionary. | SPEC-RWB-E1-006-004 | DIRECT | MSG-P1-005; whole load refused. | COVERED |
| X2 | A rule type or table is outside the allowed set. | SPEC-RWB-E1-006-004 | DIRECT | MSG-P1-007; whole load refused. | COVERED |
| X3 | One rule fails at run time. | SPEC-RWB-E1-006-005 | DIRECT | ERROR on the load_run; others continue. | COVERED |
| X4 | Rules run again for the same load. | SPEC-RWB-E1-006-006 | DIRECT | No duplicate. | COVERED |
| X5 | A rule is outside its valid dates. | SPEC-RWB-E1-006-002 | DIRECT | Rule does not run. | COVERED |
| X6 | A record that failed before now passes. | SPEC-RWB-E1-006-007 | DIRECT | Exception CLEARED. | COVERED |
| X7 | A role without Platform administration R lists exceptions. | SPEC-RWB-E1-006-010, 013 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **ten data quality rules (missing owner, duplicate account, days past due mismatch, stale balance, missing collateral link and five more) run on every load, with a reason code on every failed row**, so that **the case list can be trusted**.

The story makes data quality a versioned data product: the ten rules are rows, the seven rule types are
the only code, and the exception list is the shared output. It does not build a Workbench screen and
does not work a break to closure. It runs on load completion and after the case list build.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Completion of each load step in JOB-01 and JOB-09 (`DataQualityRuleRunner.runFor(productCode, loadRunId)`); the case list step of JOB-04 for DP03. |
| Preconditions | RWB-E1-003 load framework and exception table; RWB-E1-002 `case_list_row`; RWB-E1-043 reference handler; rule version `DQR-2026.11` loaded and approved; `case.entry.dpd` 90 (DL16). |
| Input | `dq_rule` rows in force; P1 tables named by the rules; `load_run_id`; business date. |
| Output | `dq_exception` rows; `load_run.check_results` counts; data quality extract for Power BI. |
| Feature flag | `rwb.p1.dq-rules`. Off: no rule runs; loads complete as before. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `dq_rule` | `rule_code` | Reference load | System writes | DQ01–DQ10 in v1; unique with version |
| `dq_rule` | `rule_version` | Reference load | System writes | Version string; in force by date |
| `dq_rule` | `product_code` | Reference load | System writes | DP01–DP14 |
| `dq_rule` | `target_entity` | Reference load | System writes | Must be a P1-owned entity |
| `dq_rule` | `rule_type` | Reference load | System writes | One of the seven types |
| `dq_rule` | `rule_params` | Reference load | System writes | JSON; bound parameters only |
| `dq_rule` | `valid_from`, `valid_to` | Reference load | System writes | `valid_from` required; `valid_to` optional |
| `dq_rule` | `approved_by`, `test_case_id` | Reference load | System writes | Required; separation of duty |
| `dq_exception` | `check_code`, `reason_code` | Rule code | System writes | Rule code, not a load check |
| `dq_exception` | `record_key` | Rule output | System writes | Account key or record ID; never a name |
| `dq_exception` | `status` | Open | System writes | `OPEN` → `CLEARED` only |
| `dq_exception` | `cleared_on` | Passing run | System writes | Set with CLEARED |
| `load_run` | `check_results` | Runner | System writes | Count per rule, or ERROR |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| `dq_exception` | Does not exist | Rule fails | `OPEN` | Row written with rule code, version, record key and business date |
| `dq_exception` | `OPEN` | Rule passes on a later run | `CLEARED` | `cleared_on` set; no delete |
| `dq_exception` | `OPEN` | Rule still fails | `OPEN` | No duplicate row |
| `dq_rule` version | Prior version | Approved version reaches `valid_from` | New version in force | Prior rows retained; no update |
| `load_run` | `RUNNING` | Rule run completes | `COMPLETED`/`FAILED` | Check results written |

No case status changes. DQ02 raises the duplicate; P3 merges under R-UNI-17.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Rule names an unknown field | Whole load refused; prior version stays | MSG-P1-005 |
| X2 | Rule type or table outside the allowed set | Whole load refused | MSG-P1-007 |
| X3 | One rule fails at run time | Rule ERROR; other rules run; alert | MSG-P1-015 |
| X4 | Rules run again for the same load | No second exception row | None |
| X5 | Rule outside its valid dates | Rule does not run | None |
| X6 | A record that failed now passes | Exception CLEARED with date | None |
| X7 | Role without Platform administration R | 403 | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/data-quality/exceptions` (API-P1-003); `POST /api/recovery/v1/admin/reference-loads` and approve (P4). |
| Contract delta | None. The existing response already carries id, product, check, record and raisedOn. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for exceptions; Reference data C/A for the rule load. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 422 MSG-P1-005/007; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; the Power BI report is built by RW-BIANAL. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-008; SPEC-RWB-E1-006-001..015 | New entity, repository, handler, seven templates, runner and extract writer. | Each template pass/fail; in-force boundaries; invalid field/table; duplicate run; clear; timeout isolation; counts; extract; security. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DqRule` | Entity | Maps `dq_rule`. |
| `DqRuleRepository` | Repository | Reads rules in force by product and date. |
| `DqRuleHandler` | Published interface implementation | `ReferenceTableHandler` for `dq_rule`; validates entity, field, type and params. |
| `RuleTypeTemplates` | Service | One SQL template per type: NOT_NULL, UNIQUE_ACROSS, RANGE, SUM_EQUALS, EXISTS_LINK, MAX_AGE_DAYS, FIELD_BEFORE. |
| `DataQualityRuleRunner` | Service | Runs one product's rules for one load with a 60-second limit per rule; writes and clears exceptions. |
| `DqExceptionRepository` | Repository (RWB-E1-003) | Insert with ON CONFLICT DO NOTHING; clear by rule and record. |
| `DataQualityExtractWriter` | Service | Writes the day's exceptions to the lake extract in the JOB-04 publish step. |

Package `recovery.dataengine.quality`.

### Data and migration

Migration `V1_006__dq_rule.sql` creates `dq_rule` (`rule_code` varchar(8), `rule_version` varchar(20),
`rule_name` varchar(120), `product_code` varchar(25), `target_entity` varchar(60), `rule_type`
varchar(15), `rule_params` jsonb, `valid_from` date, `valid_to` date, `approved_by` uuid,
`test_case_id` varchar(20), standard columns, unique (`rule_code`, `rule_version`)); adds `rule_version`
and `cleared_on` to `dq_exception` and `uk_dq_exception UNIQUE (load_run_id, check_code, record_key)`.

### Rule definitions in v1

| Rule | Name | Product | Table | Type and parameters |
|---|---|---|---|---|
| DQ01 | Missing owner | DP03 | `case_list_row` | NOT_NULL `owner_user_id` where status is not NEW |
| DQ02 | Duplicate account | DP03 | `case_list_row` | UNIQUE_ACROSS `account_id` over `case_id` |
| DQ03 | Days past due mismatch | DP03 | `case_list_row` | RANGE `days_past_due` minimum `case.entry.dpd` |
| DQ04 | Stale balance | DP01 | `loan_account` | MAX_AGE_DAYS `data_as_of` 0 days behind the load business date, for accounts on the case list |
| DQ05 | Missing collateral link | DP03 | `case_list_row` | EXISTS_LINK `account_collateral.account_id` where product group in MORTGAGE, HIRE_PURCHASE |
| DQ06 | Balance parts do not add up | DP01 | `loan_account` | SUM_EQUALS `total_balance = principal_outstanding + interest_outstanding + fees_outstanding`, tolerance 0.00 |
| DQ07 | Negative principal | DP01 | `loan_account` | RANGE `principal_outstanding` minimum 0.00 |
| DQ08 | Missing classification | DP01 | `loan_account` | NOT_NULL `classification` where `days_past_due` at or above `case.entry.dpd` |
| DQ09 | Party without a contact point | DP02 | `party` | EXISTS_LINK `contact_point.party_id` |
| DQ10 | Payment after the last payment date | DP01 | `account_payment` | FIELD_BEFORE `payment_date` not after `loan_account.last_payment_date` |

The rule rows are reference data; only the seven templates are code.

### Execution

1. Read rules in force for the product on the business date.
2. Build SQL from the type template and bound parameters; identifiers only from `sys_fields`.
3. Run each rule with a 60-second limit; collect failing record keys.
4. Insert one `dq_exception` per failing record with the rule code as check and reason code, rule
   version, record key and business date; ON CONFLICT DO NOTHING.
5. Clear OPEN exceptions of the same rule and record that no longer fail.
6. Write the count per rule, or ERROR, to `load_run.check_results`.
7. The JOB-04 publish step writes the day's exceptions to the lake extract.

**Transaction.** The rule run reads committed load data; exception writes and check results are written
after the run. A rule failure is recorded as ERROR and does not stop the other rules. No event is
published by this story.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Runs the rules; writes exceptions and check results | All |
| RW-REFADM | Reference data C for a rule load | All |
| RW-DATASTEW | Approves the version as owner; Platform administration R | All |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Platform administration R | All |
| RW-BIANAL | Reporting CRUD for the Power BI report | All |

Separation of duty: the administrator who loads a version cannot approve it.

### Observability and operations

- Metrics: exceptions per rule; rules in ERROR; run duration; cleared count.
- Alerts: MSG-P1-015 to the data steward; rule load refused.
- Audit: rule version and approver recorded on each exception.
- Run book entry under RWB-E1-056.

### Performance

- One query per rule; 60-second limit isolates a slow rule.
- Indexes on `dq_exception (load_run_id, check_code, record_key)` and `(product_code, raised_on)`.
- Rules run after the load step completes; a rule failure is recorded as ERROR without stopping the
  other rules.

### Feature flag and rollback

`rwb.p1.dq-rules`. Off: no rule runs; loads complete as before. Rollback: turn the flag off; `dq_rule`
and the exception rows remain.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-006-01 | AC1, BR1, BR8 | System | Three accounts each on two open cases | Three DQ02 rows; endpoint returns them; count 3 |
| TC-E1-006-02 | AC2 | System | 3 DQ02, 14 DQ05, 2 DQ06 | 19 extract rows; Power BI by rule, product and day |
| TC-E1-006-03 | AC3, BR2, BR3 | System | DQR-2026.12 with DQ11; two accounts at 32.5000 | Two exceptions; DQ01–DQ10 unchanged |
| TC-E1-006-04 | AC4, BR4, BR5 | System | DQ12 on `loan_account.balance_total` | MSG-P1-005; DQR-2026.11 stays |
| TC-E1-006-05 | AC5, BR5 | System | DQ12 on `recovery_case.owner_user_id` | MSG-P1-007 naming the allowed entities |
| TC-E1-006-06 | AC6, X3 | System | DQ05 forced past 60 seconds | DQ05 ERROR; other rules write; MSG-P1-015 |
| TC-E1-006-07 | AC7, X4 | System | Rules run twice on one load | Two DQ06 rows only |
| TC-E1-006-08 | AC8, BR3 | System | DQ07 valid to 2026-11-30 | DQ07 does not run; not in check results |
| TC-E1-006-09 | AC9, X6 | System | OPEN DQ01 for ACC0000777; owner now set | CLEARED with 2026-11-30 |
| TC-E1-006-10 | X7 | Security | RW-CASEOWN lists exceptions | 403 MSG-P4-002 |
| TC-E1-006-11 | BR5 | Unit | Each template pass/fail; identifier from `sys_fields` | Bound parameters; no rule text executed as SQL |
| TC-E1-006-12 | BR7 | Unit | DQ03 at 89, 90 and 91 days | Only below 90 fails |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1; SPEC-005 | When do the rules run? | Determines integration points. | On JOB-01/JOB-09 load completion and the JOB-04 case list step; story §12. | RESOLVED | SPEC-005 |
| CLAR-002 | BR4; SPEC-004 | Is the rule load whole-file or row-by-row? | Determines partial writes. | Whole-load refusal; prior version stays (story BR4, AC4, AC5). | RESOLVED | SPEC-004 |
| CLAR-003 | BR6; SPEC-006 | Are DQ01–DQ10 the same as load checks DQ-001–DQ-098? | Determines the code space. | No; separate spaces. Rule codes go in `check_code` and `reason_code`. | RESOLVED | SPEC-006 |
| CLAR-004 | AC6; SPEC-005 | What is the per-rule time limit? | Determines isolation. | 60 seconds; story AC6. | RESOLVED | SPEC-005 |
| CLAR-005 | BR2; SPEC-001 | Which rule version is in force at go-live? | Determines the seed data. | `DQR-2026.11`, loaded and approved (story §3). | RESOLVED | SPEC-001, 012 |
| CLAR-006 | AC5; SPEC-004 | Which entities may a rule target? | Determines the allowed set. | The eight P1 entities listed in AC5. | RESOLVED | SPEC-004 |
| CLAR-007 | UI; SPEC-009 | Is a Workbench screen built? | Determines UI scope. | No; SCR-45 is Epic 2. The report is Power BI. | RESOLVED | SPEC-009 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or DL16. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend/reporting story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New versioned data-quality rule engine and exception output; existing exception endpoint and reference-load path reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new rule runner and table with no contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 9 acceptance criteria, 7 exception paths and 5 record transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
