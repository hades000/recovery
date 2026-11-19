# Technical Specification — RWB-E1-017 Retention and archive rule for the data store

| Field | Value |
|---|---|
| Story | RWB-E1-017 — Retention and archive rule for the data store |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-022-epic-1-RWB-E1-017` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-013); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 017 Retention and archive rule for the data store v1.md` |
| Upstream IDs | REQ-RDF-013; FEAT-RDF-17; US-RWB-E1-017; R-UNI-20, R-UNI-38; CTL-08; DL26; NFR-031, NFR-072, NFR-074 |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Compliance reads the run and the summary alert; story §15. |
| Logic In Scope | `YES` — rule validation, selection, legal-hold exclusion, archive/manifest, delete after check, job run and hold report. |
| API In Scope | `NO` — no new or changed contract. Reuses the reference-load endpoints and `GET`/`POST /admin/jobs`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `retention_rule` (new); `interaction` (delete under purge setting); `recovery_case.legal_hold` (read via P3); `sys_objects`; `data_product`; archive container (RWB-TE-012). |
| New Nodes Required | `YES` — `RetentionJob`, `RetentionService`, `ArchiveWriter`, `RetentionRuleLoader`, `RetentionRuleRepository`, `RetentionRule`, `CaseHoldQuery` consumer. |
| Inherited Existing Behavior | Recovery tables (RWB-E1-001); reference data service (RWB-E1-043); data product catalog (RWB-E1-064); archive container (RWB-TE-012); job monitor and rerun (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Each data product and table has one retention rule in force, held as a versioned row. | SPEC-RWB-E1-017-001, 002, 015 | DIRECT | `retention_rule`; version and valid-from. | COVERED |
| BR2 | A row older than its retention period on its age-basis field is archived and removed. | SPEC-RWB-E1-017-004, 007, 011 | DIRECT | Strictly older than run date minus months; exact age kept. | COVERED |
| BR3 | A legal hold keeps every row of the case, overriding retention. | SPEC-RWB-E1-017-005, 009 | DIRECT | `CaseHoldQuery.casesOnLegalHold()`; hold report. | COVERED |
| BR4 | A row is removed only after its archive copy is written and checked. | SPEC-RWB-E1-017-006, 007, 014 | DIRECT | Manifest row count and SHA-256; read back before delete. | COVERED |
| BR5 | The decision log is not archived by this job. | SPEC-RWB-E1-017-008 | DIRECT | Rule validation refuses `decision_log_entry`; trigger keeps unconditional refusal. | COVERED |
| BR6 | A retention load with an exception is refused whole. | SPEC-RWB-E1-017-002 | DIRECT | `validate` writes nothing; `apply` one transaction. | COVERED |
| BR7 | A new version applies from its valid-from date; earlier runs keep their version. | SPEC-RWB-E1-017-015 | DIRECT | Rule in force on the run date; version recorded on the run. | COVERED |
| AC1 | 1,250 old rows and 4,800 recent rows: old rows archive and leave the live table. | SPEC-RWB-E1-017-004, 006, 007, 009 | DIRECT | Archive path `retention/2026-12-06/interaction/`. | COVERED |
| AC2 | A 36-month rule keeps 2024-01-15 and archives 2023-12-20; run records RET-2027.01. | SPEC-RWB-E1-017-004, 015 | DIRECT | Rule version in force on 2027-01-03. | COVERED |
| AC3 | A legal-hold case keeps its 40 old rows; hold report names it; summary MSG-P1-020. | SPEC-RWB-E1-017-005, 009 | DIRECT | Case number and row count only. | COVERED |
| AC4 | A 0-month rule is refused; previous version stays. | SPEC-RWB-E1-017-002 | DIRECT | MSG-GEN-002; range 1..600. | COVERED |
| AC5 | Archive write failure deletes no row; run FAILED with MSG-GEN-006. | SPEC-RWB-E1-017-006, 014 | DIRECT | No delete before the manifest check. | COVERED |
| AC6 | A repeat run in the same month archives 0; one archive set remains. | SPEC-RWB-E1-017-010 | DIRECT | Selection reads live rows; idempotent by run date and rule. | COVERED |
| AC7 | A row exactly at its retention age stays. | SPEC-RWB-E1-017-011 | DIRECT | Strict `older than` comparison. | COVERED |
| AC8 | A rule for `decision_log_entry` is refused whole. | SPEC-RWB-E1-017-008 | DIRECT | MSG-P1-002 with the check text. | COVERED |
| AC9 | A rerun while JOB-17 runs returns 409. | SPEC-RWB-E1-017-010 | DIRECT | MSG-P2-006; `@DisallowConcurrentExecution`. | COVERED |
| X1 | A case is on legal hold. | SPEC-RWB-E1-017-005 | DIRECT | Rows kept; hold report. | COVERED |
| X2 | Months outside 1..600. | SPEC-RWB-E1-017-002 | DIRECT | MSG-GEN-002. | COVERED |
| X3 | Archive write or manifest check fails. | SPEC-RWB-E1-017-006, 014 | DIRECT | No delete; FAILED; alert. | COVERED |
| X4 | Repeat run in the same month. | SPEC-RWB-E1-017-010 | DIRECT | 0 archived. | COVERED |
| X5 | Row exactly at retention age. | SPEC-RWB-E1-017-011 | DIRECT | Kept. | COVERED |
| X6 | Rule names `decision_log_entry`. | SPEC-RWB-E1-017-008 | DIRECT | Refused whole. | COVERED |
| X7 | Rerun while JOB-17 runs. | SPEC-RWB-E1-017-010 | DIRECT | 409 MSG-P2-006. | COVERED |

## User story intent interpretation

As a **Compliance and PDPA officer (RW-COMPLY)**, I want **a retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action**, so that **the store holds what the policy allows and nothing older**.

The job archives to a write-once container and removes the live row only after the archive manifest matches. A legal hold overrides the rule. The decision log is never touched by this job.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-17 Retention job`, first Sunday of each month at 02:30 Asia/Bangkok. |
| Preconditions | RWB-E1-001 done; RWB-E1-043 done; RWB-E1-064 done (`data_product`); RWB-TE-012 done (archive container writable by SY-DATALOAD); retention version RET-2026.11 approved; P3 publishes `CaseHoldQuery`; job monitor (RWB-E1-056). |
| Input | Rules in force on the run date; live rows of each named table; legal-hold case IDs. |
| Output | Archive files and manifest under `retention/YYYY-MM-DD/<table>/`; deleted live rows; job run counts, rule version, archive location and hold report; MSG-P1-020. |
| Feature flag | `rwb.dataengine.retention`. Off: JOB-17 does not run. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `retention_rule` | `product_code` | Compliance load | Reference data C | Must exist in `data_product`. |
| `retention_rule` | `table_name` | Compliance load | Reference data C | Must exist in `sys_objects`; not `decision_log_entry`. |
| `retention_rule` | `record_class` | Compliance load | Reference data C | Free text up to 20; part of the key. |
| `retention_rule` | `retention_months` | Compliance load | Reference data C | 1..600. |
| `retention_rule` | `age_basis_field` | Compliance load | Reference data C | Must exist in `sys_fields` for the table. |
| `retention_rule` | `end_action` | Compliance load | Reference data C | ARCHIVE or REVIEW. |
| `retention_rule` | `rule_version`, `valid_from`, `valid_to` | Compliance load | Reference data C | One rule in force per product/table/class on a date. |
| `interaction` | `occurred_at` | Live row | Read | Age basis; strictly older than run date minus months. |
| `interaction` | `case_id` | Live row | Read | Used for the legal-hold exclusion. |
| Archive | `_manifest.json` | Job | Write once | Row count and SHA-256 per file. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | JOB-17 start | First Sunday 02:30 | Running | Rules read; hold set read. |
| Running | Archive and delete complete | Manifest matches for each table/rule | Complete | Counts, version, location and hold report recorded. |
| Running | Archive or delete fails | Container or database error | Failed | No delete for the failed unit; alert. |
| Complete | Repeat run in the same month | Rows already archived | Complete | 0 archived; one archive set. |
| Rule version N | New version approved | Valid-from reached | Rule version N+1 | Next run uses N+1; earlier runs keep N. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Legal hold | Keep every row of the case; list it in the hold report. | MSG-P1-020 |
| X2 | Months outside 1..600 | Refuse the load whole; previous version stays. | MSG-GEN-002 |
| X3 | Archive write or manifest check fails | No delete; run FAILED; alert; rerun from the monitor. | MSG-GEN-006 |
| X4 | Repeat run in the same month | Archive 0; one archive set. | None |
| X5 | Row exactly at retention age | Keep. | None |
| X6 | Rule names `decision_log_entry` | Refuse the load whole. | MSG-P1-002 |
| X7 | Rerun while JOB-17 runs | 409; one run continues. | MSG-P2-006 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve`, `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun`. |
| Contract delta | None. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load; Reference data A to approve; Platform administration R to read; Platform administration U to rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004 / MSG-P2-006; 422 MSG-GEN-001/002; 503 MSG-GEN-006. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; the job monitor and alert are the surfaces. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-013; SPEC-RWB-E1-017-001..015 | New rule table, loader, job, archive writer and retention service. | Positive, negative, boundary and error-path tests: rule validation; selection; exact age; legal hold; archive failure; repeat run; decision-log refusal; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `RetentionJob` | Quartz job | JOB-17; no concurrent run. |
| `RetentionService` | Service | Reads rules, selects rows, excludes legal holds, deletes after the archive check. |
| `ArchiveWriter` | Service | Writes JSON lines and the manifest; verifies count and SHA-256. |
| `RetentionRuleLoader` | Published interface | Validates and stores an approved version. |
| `RetentionRuleRepository` | Repository | Reads and writes `retention_rule`. |
| `RetentionRule` | Entity | One row per product, table, class and version. |

### Data and migration

- Creates `retention_rule` (id, product_code, table_name, record_class, retention_months, age_basis_field, end_action, rule_version, valid_from, valid_to, approved_by, standard columns; unique `(product_code, table_name, record_class, rule_version)`).
- `retention_months` check 1..600; `table_name` references `sys_objects(object_name)`.
- Replaces `refuse_change()` so DELETE on `interaction` is allowed only when `recovery.retention_purge = 'on'`, set inside the delete transaction; UPDATE stays refused; `decision_log_entry` keeps the unconditional refusal.
- Uses `ix_interaction_case_time (case_id, occurred_at)`.
- The archive container and `rwb.dataengine.retention.batch-size=5000` are properties.

### Rules

1. Rule validation: product exists; table exists in `sys_objects`; table is not `decision_log_entry`; months 1..600; age-basis field exists in `sys_fields` for the table.
2. Rule in force on the run date = approved version with the latest valid-from on or before the run date.
3. Selection: rows whose age-basis field is strictly older than the run date minus the retention months.
4. Legal hold: every row of a case returned by `CaseHoldQuery.casesOnLegalHold()` is kept.
5. Archive: write JSON lines and a manifest with row count and SHA-256; read the manifest back; only then delete.
6. Delete one table/rule unit in one transaction under the purge setting.
7. The decision log is never archived or deleted by this job.
8. Record counts per product/table, rule version, archive location and hold report on the job run.

### Transaction and events

- Each table/rule is one unit: archive, check, delete. A failure before the delete leaves the live rows; a rerun repeats the unit.
- No event is published; the job run and the summary alert are the record.
- The archive is write-once; a repeat run does not overwrite an existing set.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COMPLY | Own the periods; Platform administration R | All |
| RW-REFADM | Reference data C — submit the load | All |
| Holder of Reference data A | Approve the load | All |
| RW-DATASTEW | Platform administration R — read the run | All |
| RW-PLATADM | Platform administration U — rerun | All |
| SY-DATALOAD | Run JOB-17; write archive; delete rows | All |
| SY-CASEWF | Answer `CaseHoldQuery` | All |
| Any other role | None | 403 MSG-P4-002 |

The job run and hold report carry counts and case numbers only; no personal values.

### Observability and operations

- Job run: counts per product/table, rule version, archive location, hold report, status.
- Alert: MSG-P1-020 summary to Compliance.
- Metrics: rows archived, rows held, archive failures, run duration.
- Run book from RWB-E1-056 covers a failed run.

### Performance

- Monthly run; batch size 5,000; index `ix_interaction_case_time` supports selection.
- One transaction per table/rule; no long transaction across all tables.
- Archive write is streamed; the manifest check reads back only the manifest.

### Feature flag and rollback

- `rwb.dataengine.retention`. Off: JOB-17 does not run; no row is deleted.
- Rollback: turn the flag off; the migration is forward-only. A failed run leaves the live rows and the archive as it is.

### No UI change

No screen. Compliance reads `GET /admin/jobs` and MSG-P1-020; SCR-47 arrives in Epic 8.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-017-01 | AC1, BR1, BR2, BR4 | System | 1,250 old + 4,800 recent interaction rows | 1,250 archived; removed from live; count and version on the run |
| TC-E1-017-02 | AC2, BR7 | System | RET-2027.01 at 36 months; rows 2024-01-15 and 2023-12-20 | 2024-01-15 stays; 2023-12-20 archives; version RET-2027.01 |
| TC-E1-017-03 | AC3, BR3 | System | Case RW-2024-000311 on hold with 40 old rows | 40 kept; hold report; MSG-P1-020 |
| TC-E1-017-04 | AC4, BR6 | System | 0 months | Refused; MSG-GEN-002; previous version stays |
| TC-E1-017-05 | AC5, BR4 | System | Archive container refuses writes | No delete; FAILED; MSG-GEN-006 |
| TC-E1-017-06 | AC6 | System | JOB-17 twice on 2026-12-06 | 0 archived; one archive set |
| TC-E1-017-07 | AC7 | System | Row at 2024-12-06T00:00+07:00 | Kept |
| TC-E1-017-08 | AC8, BR5 | System | Rule for decision_log_entry | Refused; MSG-P1-002 |
| TC-E1-017-09 | AC9 | System | Rerun during JOB-17 | 409 MSG-P2-006 |
| TC-E1-017-10 | X2 | Security | RW-COMPLY rerun | 403 MSG-P4-002 |
| TC-E1-017-11 | BR2, BR4 | Unit | Exact-age boundary; manifest mismatch | Keep at exact age; no delete on mismatch |

## Guardrails

- Periods, tables, age-basis fields and the archive location are data rows or properties.
- No personal data in logs, tests or prompts; the run and hold report carry counts and case numbers.
- No read of another module's tables; legal hold comes from `CaseHoldQuery`.
- The decision log is never archived or deleted by this job, and no row is deleted before its archive copy is checked.

## Out of scope

- Document retention and legal hold (RWB-E1-041); ledger retention (RWB-E2-034); decision log retention (NFR-030, DL26) and the lake copy (RWB-E1-014).
- Closing a case after retention (Epic 6); SCR-47 (Epic 8).

## Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | FEAT-RDF-17 | R-UNI-20, R-UNI-38; CTL-08; DL26 | TC-E1-017-01..11 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC1; SPEC-004, 011 | Is a row exactly at the retention age archived or kept? | The boundary selection. | AC7: exactly at age is kept; only strictly older rows archive. | `RESOLVED` | SPEC-004, 011 |
| CLAR-002 | BR1; SPEC-001, 015 | Are the DP05 24-month and DP12 120-month periods approved? | The rule values; the code reads data. | They are assumed until Compliance supplies the bank schedule (DL26); load as data. | `RESOLVED` | SPEC-001, 015 |
| CLAR-003 | AC1; SPEC-009 | Does the hold report carry case numbers or case IDs? | Privacy of the report. | AC3 names the case number; no personal value. | `RESOLVED` | SPEC-009 |
| CLAR-004 | AC6; SPEC-010 | Does a repeat run overwrite the archive? | Archive integrity. | AC6: 0 archived and one set remains; the archive is write-once. | `RESOLVED` | SPEC-010 |
| CLAR-005 | Traceability; SPEC-010 | The story lists 10 test cases but traceability names TC-E1-017-01..09. | Test coverage record. | TC-E1-017-10 is the access test; include it in the traceability row. | `RESOLVED` | SPEC-010 |

`CLARIFICATION_STATUS: RESOLVED` — all 5 items are answered from the story or its ACs. The retention
periods remain data under DL26; the job logic is not blocked.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New monthly retention and archive job; no UI or API contract change; existing reference-load and job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new retention rule table and job with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 9 acceptance criteria and 7 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
