# Technical Specification — RWB-E1-014 Decision log copy to the data lake

| Field | Value |
|---|---|
| Story | RWB-E1-014 — Decision log copy to the data lake |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-024-epic-1-RWB-E1-014` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-DRI-009, REQ-RDF-013); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 014 Decision log copy to the data lake v1.md` |
| Upstream IDs | REQ-DRI-009, REQ-RDF-013; FEAT-RDF-20, FEAT-DRI-06; US-RWB-E1-014; REC-08; DL25, DL26; ADR-009 |
| Status | `SUCCESS` — CLAR-002 resolved by the story AC2 correction (2026-11-06) |
| Prepared | 2026-11-04 |
| Regated | 2026-11-06 — Technical Specifier re-run after the AC2 correction and the DL26 recording |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The job monitor and the lake copy are the surfaces; story §15. |
| Logic In Scope | `YES` — watermark, cut-off, paging, Parquet/manifest, REC-08 reconciliation, watermark advance, retention step. |
| API In Scope | `NO` — no new or changed contract. Reuses `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `lake_copy_watermark` (new); decision log read through P7 `DecisionLogExport`; `retention_rule` (RWB-E1-017); INT-19 lake intake container. |
| New Nodes Required | `YES` — `DecisionLogLakeCopyJob`, `DecisionLogLakeCopyService`, `LakeFileWriter`, `LakeCopyReconciler`, `LakeRetentionService`, `LakeCopyWatermarkRepository`, `LakeCopyWatermark`. |
| Inherited Existing Behavior | Decision log store and writer (RWB-E1-008, RWB-E1-027); retention rule table (RWB-E1-017); job monitor and run book (RWB-E1-056); outbox/retry pattern. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The copy matches the live log on count and last hash with zero tolerance, or it is not published. | SPEC-RWB-E1-014-006, 007 | DIRECT | REC-08; watermark moves only on a match. | COVERED |
| BR2 | The copy reads the decision log only through the P7 published interface. | SPEC-RWB-E1-014-003, 004 | DIRECT | `DecisionLogExport.head()` and `entriesAfter()`; no table read. | COVERED |
| BR3 | Analysis reads the lake copy, not the live log. | SPEC-RWB-E1-014-005 | DIRECT | Parquet partitions in the INT-19 container. | COVERED |
| BR4 | A lake partition older than the DP12 LAKE_COPY rule moves to the archive tier. | SPEC-RWB-E1-014-008, 014 | DIRECT | Retention step; exact-age kept. | COVERED |
| BR5 | The retention period is a data row with a version. | SPEC-RWB-E1-014-008 | DIRECT | `retention_rule`; no literal. | COVERED |
| BR6 | A failed copy is rerun the next night; the previous copy stays in use. | SPEC-RWB-E1-014-009, 011 | DIRECT | Watermark unchanged; rerun from the watermark. | COVERED |
| AC1 | 380 entries on 2026-11-30 produce a 380-row partition; manifest 12,480/`a3f1...09c2`; watermark moves. | SPEC-RWB-E1-014-001, 002, 003, 004, 005, 006, 007 | DIRECT | Page size 5,000; manifest cumulative count and last hash. | COVERED |
| AC2 | Partitions 2024-11-29 and 2024-11-30: both archive on the strict rule (2 archived). | SPEC-RWB-E1-014-008, 014 | DIRECT | The rule archives every partition strictly older than 2024-12-01, so both archive; the story AC2 was corrected on 2026-11-06 to expect 2. | COVERED |
| AC3 | A 379-of-380 copy is not marked complete; watermark stays; REC-08 fails with MSG-P1-019. | SPEC-RWB-E1-014-006, 007, 011 | DIRECT | Manifest read-back; no advance. | COVERED |
| AC4 | A rerun for the same date leaves 380 rows and cumulative 12,480. | SPEC-RWB-E1-014-009 | DIRECT | Same partition, same chain range; no duplicates. | COVERED |
| AC5 | DecisionLogExport error ends FAILED; watermark and partitions unchanged. | SPEC-RWB-E1-014-011 | DIRECT | MSG-GEN-006. | COVERED |
| AC6 | No new decisions: empty partition, cumulative 12,100, REC-08 passes. | SPEC-RWB-E1-014-010 | DIRECT | Manifest zero rows; unchanged hash. | COVERED |
| AC7 | A rerun while JOB-13 runs returns 409. | SPEC-RWB-E1-014-012 | DIRECT | MSG-P2-006; `@DisallowConcurrentExecution`. | COVERED |
| AC8 | A partition exactly at retention age stays. | SPEC-RWB-E1-014-014 | DIRECT | Strictly older only. | COVERED |
| X1 | Count or last hash differs. | SPEC-RWB-E1-014-006, 011 | DIRECT | Not complete; no watermark move; MSG-P1-019. | COVERED |
| X2 | Rerun for a copied date. | SPEC-RWB-E1-014-009 | DIRECT | Same partition; no duplicates. | COVERED |
| X3 | DecisionLogExport or lake write fails. | SPEC-RWB-E1-014-011 | DIRECT | FAILED; previous copy and watermark kept. | COVERED |
| X4 | No decision since the last copy. | SPEC-RWB-E1-014-010 | DIRECT | Empty partition; checks pass. | COVERED |
| X5 | Second start while running. | SPEC-RWB-E1-014-012 | DIRECT | 409 MSG-P2-006. | COVERED |
| X6 | Partition exactly at retention age. | SPEC-RWB-E1-014-014 | DIRECT | Kept. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **the decision log copied to the data lake each night, with a retention rule applied to the copy**, so that **reporting reads the log without touching the live log and nothing in the copy is kept longer than its rule**.

The job reads the live log only through P7's `DecisionLogExport`. It writes Parquet partitions and a manifest, reconciles count and last hash with zero tolerance, and advances the watermark only on a match. A separate retention step archives lake partitions older than the DP12 LAKE_COPY rule.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-13 Decision log copy` at 01:00 Asia/Bangkok for business date D (previous calendar day). |
| Preconditions | RWB-E1-008 and RWB-E1-027 done; RWB-E1-056 done (run book and monitor); RWB-E1-017 done (DP12 LAKE_COPY rule); INT-19 container writable by SY-DATALOAD; Quartz trigger. |
| Input | Watermark; `DecisionLogExport.head()`; `entriesAfter(watermarkHash, 5000)`. |
| Output | Parquet files and `_manifest.json` under `decision-log/business_date=YYYY-MM-DD/`; watermark row; job run checks. |
| Feature flag | `rwb.dataengine.lake-copy`. Off: JOB-13 does not run. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `lake_copy_watermark` | `copy_name` | Seed `DECISION_LOG` | System | Primary key. |
| `lake_copy_watermark` | `last_entry_hash` | Seed 64 zeros | System | Advanced only on REC-08 match. |
| `lake_copy_watermark` | `last_decided_at` | Seed null | System | Last entry time at the cut-off. |
| `lake_copy_watermark` | `rows_copied_total` | Seed 0 | System | Cumulative count; monotonic. |
| `lake_copy_watermark` | `business_date` | Seed null | System | Last copied business date. |
| Lake partition | `business_date=YYYY-MM-DD` | Job | Write once | One partition per date; no duplicates. |
| Lake manifest | `rowCount`, `firstHash`, `lastHash`, `cumulativeCount` | Job | Write once | Read back and compared. |
| `retention_rule` | DP12 `LAKE_COPY` months/version | Compliance | Reference data | Used by the retention step; no literal. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | JOB-13 start | 01:00 | Running | Watermark read; cut-off fixed. |
| Running | Copy and REC-08 match | Count and last hash equal | Complete | Partition complete; watermark advanced; checks recorded. |
| Running | REC-08 mismatch | Count or hash differs | Failed | Partition not complete; watermark unchanged; MSG-P1-019. |
| Running | Interface or lake error | Export or write fails | Failed | Previous copy and watermark kept; MSG-GEN-006. |
| Complete | Rerun for the same date | Same chain range | Complete | Same partition; no duplicates. |
| Partition | Retention step | Older than the rule | Archived | Archive tier; count and version recorded. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Count or last hash differs | Partition not complete; watermark stays; alert. | MSG-P1-019 |
| X2 | Rerun for a copied date | Same partition; no duplicates. | None |
| X3 | Export or lake unavailable | FAILED; previous copy and watermark kept. | MSG-GEN-006 |
| X4 | No new decisions | Empty partition; manifest cumulative unchanged; REC-08 passes. | None |
| X5 | Second start while running | Refuse; 409 on manual rerun. | MSG-P2-006 |
| X6 | Partition exactly at retention age | Keep. | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs`; `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`. |
| Contract delta | None. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for the job list; Platform administration U for rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P2-006; 503 MSG-GEN-006. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; the job monitor and lake copy are the surfaces. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DRI-009, REQ-RDF-013; SPEC-RWB-E1-014-001..016 | New job, copy service, file writer, reconciler, retention service and watermark repository. | Positive, negative, boundary and error-path tests: paging; manifest; REC-08 match/mismatch; watermark; empty day; rerun; export failure; exact age; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DecisionLogLakeCopyJob` | Quartz job | JOB-13; one run per business date; no concurrent run. |
| `DecisionLogLakeCopyService` | Service | Reads the watermark, fixes the cut-off, pages entries. |
| `LakeFileWriter` | Service | Writes Parquet files and the manifest. |
| `LakeCopyReconciler` | Service | Reads the manifest back and checks REC-08. |
| `LakeRetentionService` | Service | Applies the DP12 LAKE_COPY rule to lake partitions. |
| `LakeCopyWatermarkRepository` | Repository | Reads and writes `lake_copy_watermark`. |
| `LakeCopyWatermark` | Entity | One row per copy name. |
| `DecisionLogExport` | Published interface (P7) | `head()` and `entriesAfter()`; no table read. |

### Data and migration

- Creates `lake_copy_watermark` (`copy_name` primary key, `last_entry_hash char(64)`, `last_decided_at`, `rows_copied_total bigint`, `business_date date`, standard columns).
- Seeds `DECISION_LOG` with 64 zeros and 0 rows.
- Reads `retention_rule` for DP12 `LAKE_COPY`; no literal period.
- No read of `decision_log_entry` in P1 code.

### Rules

1. At start, `head()` fixes the live count and last hash (the cut-off).
2. Page `entriesAfter(watermarkHash, 5000)` in chain order until the cut-off hash.
3. Write Parquet files and `_manifest.json` with row count, first hash, last hash and cumulative count.
4. Read the manifest back; REC-08 compares cumulative count and last hash with the cut-off, tolerance zero.
5. On a match, mark the partition complete and advance the watermark; on a mismatch, leave both unchanged.
6. Retention step: partitions strictly older than the rule move to the archive tier; a partition exactly at age stays.
7. A rerun for the same date rewrites the same partition from the same chain range; no duplicates.
8. The job never writes, updates or deletes a live decision log entry.

### Transaction and events

- The watermark update and the partition-complete marker are one transaction after REC-08 passes.
- No event is published; the job run and manifest are the record.
- A failed run leaves the watermark unchanged; the next run starts from it.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Run JOB-13; read via P7; write lake and watermark | All |
| SY-DECLOG | Own the live log; no write in this story | All |
| RW-PLATADM | Platform administration U — rerun | All |
| RW-DATASTEW | Platform administration R — read the result | All |
| RW-COE, RW-AUDIT, RW-COMPLY | Platform administration R; read the lake copy | All |
| RW-BIANAL | Read the lake copy for reporting | All |
| Any other role | None | 403 MSG-P4-002 |

The copy carries decision metadata and references, not personal values; test entries use synthetic case IDs and hashes.

### Observability and operations

- Job run: rows, REC-08 result, partitions archived, rule version, status.
- Alert on a mismatch or a failed run; data steward and platform administrator.
- Metrics: rows copied, lag, REC-08 pass rate, archive count.
- Run book from RWB-E1-056 covers the rerun.

### Performance

- Page size 5,000; rows per file 50,000; Parquet columnar output.
- Nightly at 01:00, before JOB-15 at 01:30 and JOB-14 at 02:00.
- The retention step lists partitions and moves only those older than the rule.

### Feature flag and rollback

- `rwb.dataengine.lake-copy`. Off: JOB-13 does not run; the watermark stays.
- Rollback: turn the flag off; the previous partition and watermark remain; the job is idempotent on rerun.

### No UI change

No screen. The platform administrator and data steward read `GET /admin/jobs`; SCR-44 arrives in Epic 2.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-014-01 | AC1, BR1, BR2 | System | 12,480 entries; watermark 12,100 | 380-row partition; manifest 12,480/`a3f1...09c2`; watermark moves |
| TC-E1-014-02 | AC2, BR4, BR5 | System | Partitions 2024-11-29 and 2024-11-30; 24 months | Both are older than 2024-12-01; the job records 2 partitions archived under rule version RET-2026.11 |
| TC-E1-014-03 | AC3, BR1 | System | Lake write stops after 379/380 | Not complete; watermark stays; REC-08 fails; MSG-P1-019 |
| TC-E1-014-04 | AC4 | System | Rerun for 2026-11-30 | 380 rows; cumulative 12,480 |
| TC-E1-014-05 | AC5, BR6 | System | Export stub errors | FAILED; watermark and partitions unchanged; MSG-GEN-006 |
| TC-E1-014-06 | AC6 | System | No entry after watermark | 0-row partition; cumulative 12,100; REC-08 passes |
| TC-E1-014-07 | AC7 | System | Rerun during JOB-13 | 409 MSG-P2-006 |
| TC-E1-014-08 | AC8, BR4 | System | Partition 2024-12-01 on 2026-12-01 | Kept |
| TC-E1-014-09 | X5 | Security | RW-CASEOWN calls `GET /admin/jobs` | 403 MSG-P4-002 |
| TC-E1-014-10 | BR1, BR2 | Unit | Manifest match/mismatch; paging order | Watermark only on match; chain order |

## Guardrails

- The retention period, page size, file size and lake path are data rows or properties.
- No personal data in logs, tests or prompts; test entries use synthetic case IDs and hashes.
- No read of another module's tables; `decision_log_entry` is read only through `DecisionLogExport`.
- The job never writes, updates or deletes a live decision log entry.

## Out of scope

- Retention of the live decision log (NFR-030, DL26) and the hash-chain check (JOB-14, RWB-TE-008).
- Operations reports on the copy (FEAT-RPT-04, Epic 2); access logging of lake reads (RWB-E1-039).
- The retention rule table and data-store job (RWB-E1-017).

## Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| REQ-DRI-009 | Decision log copied to the lake daily with row counts matched | FEAT-RDF-20, FEAT-DRI-06 | REC-08 | TC-E1-014-01, 03, 04, 05, 06, 07 |
| REQ-RDF-013 | Retention and archive rule by record class | FEAT-RDF-20 | DL26 | TC-E1-014-02, 08 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4, AC2; SPEC-008 | §3 gives the DP12 LAKE_COPY rule as 120 months; §7 gives 24 months. | Which partitions archive in the AC. | AC2 and the Background use 24 months; the production period is a data row set by Compliance under DL26. The code reads the rule. | `RESOLVED` | SPEC-008 |
| CLAR-002 | AC2; SPEC-008, 014 | AC2 had partitions 2024-11-29 and 2024-11-30 but recorded only one archived. | The expected archive count and the boundary test. | **Resolved 2026-11-06:** the business analyst corrected the story AC2 to the strict boundary from the build notes ("a partition exactly at its retention age is kept"): on a 2026-12-01 run under a 24-month rule the cut-off is 2024-12-01, so both 2024-11-29 and 2024-11-30 are older and record 2 partitions archived; AC8's kept boundary (2024-12-01) is unchanged. The production period stays a data row owned by Compliance under DL26 (needed by 2026-11-13). | `RESOLVED` | SPEC-008, 014 |
| CLAR-003 | AC4; SPEC-009 | Does a rerun duplicate rows? | Idempotency. | AC4: the same partition is rewritten from the same chain range; no duplicates. | `RESOLVED` | SPEC-009 |
| CLAR-004 | AC6; SPEC-010 | Does an empty day write a partition? | Reporting completeness. | AC6: a 0-row partition and a manifest with the unchanged cumulative count; REC-08 passes. | `RESOLVED` | SPEC-010 |
| CLAR-005 | BR2; SPEC-003 | Can P1 read `decision_log_entry` directly? | Module boundary. | No; only through P7 `DecisionLogExport`. | `RESOLVED` | SPEC-003 |

`CLARIFICATION_STATUS: RESOLVED` — no open items. The AC2 count follows the corrected story of
6 November 2026; the production retention period stays a data row under DL26 and does not enter the specification.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New nightly decision-log copy and lake retention job; no UI or API contract change; existing job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new lake copy job with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria and 6 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Start the Implementation Planner on this specification.
```
