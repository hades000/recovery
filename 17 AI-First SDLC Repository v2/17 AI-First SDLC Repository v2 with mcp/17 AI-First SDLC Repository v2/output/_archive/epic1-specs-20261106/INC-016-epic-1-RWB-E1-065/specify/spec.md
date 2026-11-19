# Technical Specification — RWB-E1-065 Sandbox database with synthetic recovery data

| Field | Value |
|---|---|
| Story | RWB-E1-065 — Sandbox database with synthetic recovery data |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-016-epic-1-RWB-E1-065` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-001, REQ-RDF-010); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 065 Sandbox database with synthetic recovery data v1.md` |
| Upstream IDs | REQ-RDF-001, REQ-RDF-010; US-RWB-E1-065; NFR-045; CTL-11; R-UNI-05, R-UNI-07, R-UNI-10, R-UNI-17, R-UNI-20; DL15, DL16, DL39 |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The build result is a pipeline report; story §15. |
| Logic In Scope | `YES` — metadata-driven generator, exception shapes, access seed, verifier, staging swap, lock. |
| API In Scope | `NO` — no new or changed contract. The DEV service uses the existing `GET /api/recovery/v1/cases`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `rwb_sandbox` database; recovery Flyway migrations (RWB-E1-001, RWB-E1-044); `sys_objects`, `sys_fields`, `lov_value`; `role`, `permission`. |
| New Nodes Required | `YES` — `SandboxGenerator`, `ValueFactory`, `ExceptionShapeBuilder`, `SandboxVerifier`, `AccessSeedLoader`, `SandboxExport`, sandbox build stage. |
| Inherited Existing Behavior | Flyway migrations and schema parameter (RWB-E1-044); metadata tables (RWB-E1-001); role and permission seed (RWB-E1-037). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | No production data in DEV; the sandbox is synthetic only. | SPEC-RWB-E1-065-008, 013 | DIRECT | Verifier rejects national ID, mobile and email patterns; no production extract path. | COVERED |
| BR2 | The sandbox schema comes from the same Flyway migrations as every environment. | SPEC-RWB-E1-065-001, 002, 011 | DIRECT | Staging schema `recovery_next`; apply all migrations; swap to `recovery`. | COVERED |
| BR3 | Generated values come from the dictionary and the lists, not from code. | SPEC-RWB-E1-065-003, 011 | DIRECT | Metadata reader; `ValueFactory` per type and LOV; no column literal. | COVERED |
| BR4 | Ten exception shapes are generated, 10 cases each. | SPEC-RWB-E1-065-005 | DIRECT | Duplicate customer/product, deceased, bankruptcy, deviation, legal hold, unmapped product, collateral without account, three-account case, 89/90 DPD, withdrawn consent. | COVERED |
| BR5 | Volumes follow the 30 June 2026 inventory at 10%. | SPEC-RWB-E1-065-004 | DIRECT | 1,226 Mortgage + 1,296 HP + 290 SSME = 2,812. | COVERED |
| BR6 | Every role has a named test user before real users. | SPEC-RWB-E1-065-006 | DIRECT | 54 roles; one test user per role. | COVERED |
| X1 | A migration adds a column with no dictionary row. | SPEC-RWB-E1-065-003 | DIRECT | Build fails; previous sandbox kept. | COVERED |
| X2 | The build runs twice for the same commit. | SPEC-RWB-E1-065-010 | DIRECT | Same seed, same rows and counts. | COVERED |
| X3 | A generated value breaks a constraint. | SPEC-RWB-E1-065-007 | DIRECT | Build fails naming table and constraint. | COVERED |
| X4 | A generated value matches a personal pattern. | SPEC-RWB-E1-065-008 | DIRECT | Build fails naming column. | COVERED |
| X5 | Accounts at the 90 DPD boundary. | SPEC-RWB-E1-065-012 | DIRECT | 89 and 90 generated. | COVERED |
| X6 | A second build starts while one runs. | SPEC-RWB-E1-065-001 | DIRECT | Waits on the lock; runs after. | COVERED |

> **AC cleanup (4 November 2026):** all previous acceptance criteria in this story were development-process criteria and were removed from story §7. This engineering enabler has no business acceptance criteria; the coverage table above maps the business rules and exception paths only.

## User story intent interpretation

As a **Tribe lead and squad member (RW-TRIBE)**, I want **a sandbox database holding synthetic recovery data**, so that **I can build and test before the real interfaces are available**.

The sandbox is a DEV-only build tool outside the ACE service. It reads the data dictionary so a schema change reaches the sandbox without generator code changes. It never runs in SIT, UAT or production and never holds a production value.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Merge to main that changes a recovery Flyway migration, or a manual start by RW-TRIBE/RW-PLATADM. |
| Preconditions | RWB-E1-001 done; `rwb_sandbox` exists in DEV with schema `recovery`; Entra group RWB-DEV-RW-TRIBE maps to `rwb_sandbox_read`; role/permission seed available; ACE service can run in DEV against the sandbox. |
| Input | Flyway migrations; `sys_objects`, `sys_fields`, `lov_value`; role and permission seed; properties `rwb.sandbox.seed`, `rwb.sandbox.cases.*`, `rwb.sandbox.shape-count`. |
| Output | Schema `recovery` in `rwb_sandbox` with synthetic rows; build report with row count per table and verifier result. |
| Feature flag | `rwb.dataengine.sandbox` enables the DEV profile that points the service at `rwb_sandbox`. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery_case` | `case_no` | Generator | Build only | `RW-YYYY-NNNNNN`; unique. |
| `recovery_case` | `product_group` | LOV-PRODUCT | Build only | MORTGAGE, HIRE_PURCHASE, SSME; empty list fails the build. |
| `recovery_case` | `total_outstanding_at_entry` | Generator | Build only | Same value for the same seed and commit. |
| `loan_account` | `days_past_due` | Generator | Build only | Boundary shape 89 and 90. |
| `party` | `id_no_token`, `first_name`, `last_name` | `ValueFactory` | Build only | Synthetic; must not match a personal pattern. |
| `contact_point` | `value_token` | `ValueFactory` | Build only | Random 64-hex token; no real mobile or email. |
| `role`, `permission` | All | Seed file | Build only | 54 roles; one test user per role. |
| Any generated table | Every column | `sys_fields` | Build only | A column with no dictionary row fails the build. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Build start | Trigger and lock acquired | Building | `recovery_next` created; migrations applied. |
| Building | Generator and verifier pass | All checks pass | Published | `recovery_next` renamed to `recovery`; SELECT granted. |
| Building | Any check fails | Migration, dictionary, constraint or PII failure | Failed | Previous `recovery` kept; build report names the failure. |
| Published | New build | New commit or manual start | Building | Previous sandbox stays until the swap. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Column with no dictionary row | Build fails naming table and column; previous sandbox kept. | Pipeline result |
| X2 | Same commit built twice | Same rows and counts. | Pipeline result |
| X3 | Generated value breaks a constraint | Build fails naming table and constraint; previous sandbox kept. | Pipeline result |
| X4 | Generated value matches a personal pattern | Build fails naming column; no sandbox published. | Pipeline result |
| X5 | DPD boundary | 10 accounts at 89 with no case; 10 at 90 with one open case. | None |
| X6 | Two builds at once | Second waits on the lock; runs after the first. | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/cases` in DEV only, for a test user to list sandbox cases. |
| Contract delta | None. |
| Backward compatibility | Unchanged. |
| Authorization | Case record R; scope applied; 403 MSG-P4-002; 404 MSG-P4-003 for an out-of-scope case. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; the pipeline report and SQL are the surfaces. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-001, REQ-RDF-010; SPEC-RWB-E1-065-001..015 | New generator, value factory, shape builder, verifier, access loader, export and stage. | Positive, negative, boundary and error-path tests: metadata read; every shape; empty LOV; missing dictionary; PII pattern; determinism; lock; read-only role. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `SandboxGenerator` | Service | Reads metadata; writes synthetic rows table by table in FK order. |
| `ValueFactory` | Service | Produces a value per type and LOV from the seed; synthetic names `SYN-FIRST-000123`; tokens 64-hex. |
| `ExceptionShapeBuilder` | Service | Adds the ten shapes in BR4, 10 cases each. |
| `SandboxVerifier` | Service | Row, list, FK and personal-pattern checks. |
| `AccessSeedLoader` | Service | Loads 54 roles, the permission matrix and one test user per role. |
| `SandboxExport` | Service | Writes a table to CSV for the read-only role. |
| Sandbox build stage | Job | Migrate `recovery_next`, generate, verify, swap, grant. |

### Data and migration

- No new recovery table. The stage creates `recovery_next`, applies every Flyway migration, fills it, verifies it, then renames it to `recovery`.
- A PostgreSQL advisory lock covers the whole build. A failed build leaves the previous `recovery` schema in place.
- The generator reads `sys_objects`, `sys_fields` and `lov_value`; `decision_log_entry` is not generated (story §11) and is exempt from the row check.
- `recovery_case` volumes: 1,226 Mortgage, 1,296 Hire Purchase, 290 SSME (2,812) plus 10 cases per shape (100).

### Rules

1. Every generated column must have a `sys_fields` row; otherwise the build fails.
2. Values come from the dictionary type and the LOV; no column value is hard-coded.
3. Exception shapes are the ten in BR4, 10 cases each.
4. The verifier checks rows, LOV values, FK resolution and personal patterns (Thai national ID with check digit, Thai mobile, email).
5. The same commit and seed produce the same rows, counts and `total_outstanding_at_entry`.
6. The sandbox is read-only to `rwb_sandbox_read`; UPDATE is refused.
7. No production data path exists.

### Transaction and events

- The build is a pipeline stage, not a database transaction; the swap is atomic at the schema level.
- No event is published.
- The build report is the record: commit, seed, row count per table, verifier result.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-TRIBE | Read and export via `rwb_sandbox_read`; start a manual build | DEV sandbox |
| RW-PLATADM | Own the sandbox database and stage | DEV |
| Test users per role | Call the DEV service with their role's rights | DEV |
| Any other role | No sandbox access | 403 MSG-P4-002 |

No production data; all names, identifiers and contact values are synthetic. The verifier blocks values that look real.

### Observability and operations

- Pipeline result: commit, seed, table row counts, verifier result, failure table/column/constraint.
- No runtime metric or alert; the sandbox is a DEV tool.
- The export script is the supported read path for analysts.

### Performance

- 2,812 cases plus 100 shape cases, with linked accounts, parties, contacts, collateral, valuations, payments and interactions.
- Generation is set-based per table in FK order; the build is bounded by the pipeline timeout.
- The advisory lock serialises builds; a second build waits.

### Feature flag and rollback

- `rwb.dataengine.sandbox` enables the DEV profile. Off: the service does not point at `rwb_sandbox`.
- Rollback: keep the previous `recovery` schema; a failed build never swaps. The tool is never deployed to SIT, UAT or production.

### No UI change

No screen. Developers and analysts use SQL, the export script and the pipeline report; DEV screens show sandbox cases through the normal endpoints.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-065-01 | BR4, BR5 | System | Seed 20261128; 2,812 cases plus shapes | 2,812 + 100 cases; generated tables hold rows; RW-2026-000001 linked |
| TC-E1-065-02 | Engineering verification | System | Read-only role; SELECT, export, UPDATE | SELECT works; CSV written; UPDATE refused |
| TC-E1-065-03 | BR3 | System | Test migration adds `risk_tier` with dictionary row and LOV | Every case filled; no generator change |
| TC-E1-065-04 | BR3 | System | Test migration adds `note_x` with no dictionary row | Build fails naming `loan_account.note_x`; previous sandbox kept |
| TC-E1-065-05 | Engineering verification | System | Two builds for commit a1b2c3d | Same counts; same total 1,845,200.00 |
| TC-E1-065-06 | Engineering verification | System | Empty LOV-PRODUCT | Build fails naming `recovery_case.product_group`; previous sandbox kept |
| TC-E1-065-07 | BR1 | System | Injected 13-digit valid ID in `party.id_no_token` | Build fails naming the column; no sandbox published |
| TC-E1-065-08 | BR4 | System | Boundary shape | 10 accounts DPD 89 no case; 10 DPD 90 one open case |
| TC-E1-065-09 | Engineering verification | System | Two builds started together | Second waits; final data for e4f5a6b |
| TC-E1-065-10 | X6 | Security | RW-REFADM test user calls `GET /cases` | 403 MSG-P4-002 |
| TC-E1-065-11 | BR3 | Unit | Each data type and LOV | ValueFactory returns a valid value; no literal |

## Guardrails

- Volumes, seed and shape counts are properties; values come from the dictionary and lists.
- No personal data in logs, tests or prompts; every name, identifier and contact value is synthetic; the verifier blocks real-looking values.
- The generator is a build tool outside the ACE service and is never deployed to SIT, UAT or production.
- The sandbox is DEV only; no copy goes to another environment.

## Out of scope

- Masked copies in SIT/UAT (RWB-TE-004); rule and performance harnesses (RWB-TE-005, RWB-TE-009); PDPA lint (RWB-TE-011).
- Real COLLINS and file loads (RWB-E1-003, RWB-E1-004, RWB-E1-007).

## Traceability

| Requirement ID | Requirement (short) | Rules | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, one system of record and one owner | R-UNI-05, R-UNI-07, R-UNI-10, R-UNI-17, R-UNI-20; DL15, DL16 | TC-E1-065-01..06, 08, 09 |
| REQ-RDF-010 | Access per product; personal data masked under PDPA | CTL-11 | TC-E1-065-07 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2, X1/X3; SPEC-002 | Flow step 2 drops and recreates `recovery`; §12/§13 fill `recovery_next` and swap only after the verifier. | Whether a failed build destroys the previous sandbox. | Section 12/13 and X1/X3 require the previous sandbox to survive; use the staging schema and swap. | `RESOLVED` | SPEC-002 |
| CLAR-002 | SPEC-007, 015 | The story says every one of the 41 entity tables holds a row; §11 says `decision_log_entry` is not generated. | The verifier's row check. | Exempt `decision_log_entry`; the other generated tables must hold rows. | `RESOLVED` | SPEC-007, 015 |
| CLAR-003 | BR5; SPEC-004 | The case count is 2,812 plus 10 per shape; the shape count is 10. | Build volume. | 2,812 = 1,226 + 1,296 + 290; 100 shape cases; total 2,912. | `RESOLVED` | SPEC-004 |
| CLAR-004 | BR6; SPEC-006 | Which roles get test users? | Access seed size. | 54 roles from the role seed; one test user per role (DL39). | `RESOLVED` | SPEC-006 |
| CLAR-005 | SPEC-004 | Does `RW-2026-000001` have a fixed total? | Determinism check. | The deterministic seed fixes `total_outstanding_at_entry` at 1,845,200.00 for the seed; use it as the fixture. | `RESOLVED` | SPEC-010 |

`CLARIFICATION_STATUS: RESOLVED` — all 5 items are answered from the story, its ACs or the defect
register. No open item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this build-tool story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New DEV-only synthetic data generator and sandbox build stage; no UI or API contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build tool and pipeline stage with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: No business acceptance criteria (story §7); all 6 business rules, and 6 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
