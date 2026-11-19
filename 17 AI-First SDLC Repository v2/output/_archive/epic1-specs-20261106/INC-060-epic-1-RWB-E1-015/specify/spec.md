# Technical Specification — RWB-E1-015 Freshness stamp per data product

| Field | Value |
|---|---|
| Story | RWB-E1-015 — Freshness stamp per data product |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-060-epic-1-RWB-E1-015` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001; REQ-RDF-009); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 015 Freshness stamp per data product v1.md`; FSD P1 A2.14; TSD P1 T3.1 (`data_product_load`) |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1 and 4; REQ-RDF-009; FEAT-RDF-14, FEAT-DRI-12; US-RWB-E1-015; R-UNI-40; CTL-02; DL11; NFR-013 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — a new data panel (`DataFreshnessPanel`) is added to SCR-03 Case record, with the business date, load time, LOADED/STALE status and the stale warning. |
| Logic In Scope | `YES` — stamp on load commit, duplicate handling, expected-by stale check, LoadRefused handling, late-load clear and decision input snapshot. |
| API In Scope | `YES` — `GET /api/recovery/v1/data-products/freshness` is first delivered in this story (API-P1-009). |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `data_product_load` (new); `data_product` (read); `loan_account`, `account_payment` (`data_as_of`); `dq_exception` (FRESHNESS); `decision_log_entry.inputs_ref` (read by P7); SCR-03 data panel (new). |
| New Nodes Required | `YES` — `FreshnessStampService`, `FreshnessCheckStep`, `StaleMarkerListener`, `DataProductLoadRepository`, `DataProductLoad`, `FreshnessQuery`, `FreshnessController`, `DataFreshnessPanel`. |
| Inherited Existing Behavior | Tables and `data_as_of` (RWB-E1-001); ALS load and LoadCompleted/LoadRefused (RWB-E1-003); data products and expected-by (RWB-E1-064); exception list (RWB-E1-006); P7 inputs snapshot (RWB-E1-027). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every committed load writes one freshness stamp per product and business date, in the same transaction as the load. | SPEC-RWB-E1-015-002 | DIRECT | `recordLoad` called in the load commit transaction. | COVERED |
| BR2 | A product with no load for its expected business date by its expected-by time is stale. | SPEC-RWB-E1-015-004, 005 | DIRECT | Quartz trigger per product from `data_product.expected_by`. | COVERED |
| BR3 | A refused load leaves the previous load in use and marks the product stale. | SPEC-RWB-E1-015-006 | DIRECT | `StaleMarkerListener` on LoadRefused. | COVERED |
| BR4 | Every decision records the freshness of each data product it read. | SPEC-RWB-E1-015-011 | DIRECT | P7 calls `stampsFor()` and writes the snapshot. | COVERED |
| BR5 | A repeat stamp for the same product and business date is ignored and counted. | SPEC-RWB-E1-015-003 | DIRECT | Unique (`product_code`, `business_date`); `duplicate_count`. | COVERED |
| BR6 | Expected-by times and refresh cycles are data rows, not code. | SPEC-RWB-E1-015-004 | DIRECT | `data_product.expected_by` and `refresh_cycle`. | COVERED |
| AC1 | DP01 for 2026-11-30 loaded 06:50 on 2026-12-01 from an extract at 23:30 carries source time, load time and LOADED. | SPEC-RWB-E1-015-001, 002, 009, 010 | DIRECT | Row stamp and endpoint. | COVERED |
| AC2 | No DP01 load at 08:00: STALE; FRESHNESS exception; operations alert; case record shows the warning. | SPEC-RWB-E1-015-004, 005, 012 | DIRECT | Stale check, exception and panel. | COVERED |
| AC3 | A decision reading DP01 and DP06 records each stamp in the inputs snapshot. | SPEC-RWB-E1-015-011 | DIRECT | `stampsFor`. | COVERED |
| AC4 | A refused DP01 load is STALE from 05:20; the 2026-11-30 stamp stays in use. | SPEC-RWB-E1-015-006 | DIRECT | Listener marks stale without deleting. | COVERED |
| AC5 | A repeat stamp for DP01 and 2026-11-30 leaves one row and duplicate count 1. | SPEC-RWB-E1-015-003 | DIRECT | Unique key and counter. | COVERED |
| AC6 | A late DP01 load at 08:40 sets LOADED and closes the FRESHNESS exception. | SPEC-RWB-E1-015-007 | DIRECT | Late load clears stale and closes exception. | COVERED |
| AC7 | A load at 07:59 is not flagged stale at 08:00. | SPEC-RWB-E1-015-004 | DIRECT | Expected-by comparison with the load time. | COVERED |
| AC8 | A weekly DP06 load on Monday is not stale on Thursday. | SPEC-RWB-E1-015-008 | DIRECT | Refresh cycle and expected business date. | COVERED |
| X1 | No load by the expected-by time. | SPEC-RWB-E1-015-004, 005 | DIRECT | STALE; exception; alert. | COVERED |
| X2 | The load is refused at a check. | SPEC-RWB-E1-015-006 | DIRECT | STALE at once; previous stamp stays. | COVERED |
| X3 | The same load is stamped twice. | SPEC-RWB-E1-015-003 | DIRECT | One row; duplicate count. | COVERED |
| X4 | A late load arrives after the stale flag. | SPEC-RWB-E1-015-007 | DIRECT | LOADED; exception closed. | COVERED |
| X5 | A load commits one minute before expected-by. | SPEC-RWB-E1-015-004 | DIRECT | Not stale. | COVERED |
| X6 | A weekly product between loads. | SPEC-RWB-E1-015-008 | DIRECT | Not stale inside the cycle. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **every data product to carry the source extract time and the load time, exposed to every consumer and shown on the case record view**, so that **every decision input states how old it is and stale facts are visible**.

The story gives each product a stamp per business date and makes staleness visible. It does not change
the loads themselves except to call `recordLoad` in their transaction. It supplies a published query to
P3 and P7, a read endpoint, and the SCR-03 data panel. The decision log carries the stamp of every input.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A load commits (JOB-01/JOB-09); the freshness step runs at each product's expected-by time; LoadRefused is consumed; a consumer calls `FreshnessQuery` or the endpoint. |
| Preconditions | RWB-E1-001 tables with `data_as_of`; RWB-E1-003 ALS load and events; RWB-E1-064 `data_product` with refresh cycle and expected-by; RWB-E1-006 exception list; RWB-E1-027 inputs snapshot. |
| Input | `productCode`, `businessDate`, `sourceExtractedAt`, `loadedAt`; `data_product` rows; `data_product_load` rows; LoadRefused. |
| Output | `data_product_load` row; STALE status; FRESHNESS exception; operations alert; `FreshnessStamp`; SCR-03 panel. |
| Feature flag | `rwb.dataengine.freshness-stamp`. Off: no stamp is written and the panel shows the prior state. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `data_product_load` | `product_code` | Load | System writes | DP01–DP14; unique with business date |
| `data_product_load` | `business_date` | Load | System writes | Required; unique with product |
| `data_product_load` | `source_system` | Load | System writes | ALS, EFS, CCMS, SVAF, etc. |
| `data_product_load` | `source_extracted_at` | COLLINS control record | System writes | Required; timestamptz |
| `data_product_load` | `loaded_at` | Load commit | System writes | Required; timestamptz |
| `data_product_load` | `status` | Load | System writes | `LOADED` or `STALE` |
| `data_product_load` | `stale_flagged_at` | Freshness check | System writes | Set when STALE |
| `data_product_load` | `duplicate_count` | Repeat stamp | System writes | Starts at 0; increments |
| `data_product` | `expected_by`, `refresh_cycle` | Reference data | Read only | Drives the stale check |
| `dq_exception` | `check_code` | Freshness check | System writes | `FRESHNESS` |
| `decision_log_entry` | `inputs_ref` | P7 snapshot | Read only | Contains each product stamp |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| `data_product_load` | Does not exist | Load commits | `LOADED` | Stamp written in the load transaction |
| `data_product_load` | `LOADED` | Expected load missing at expected-by | `STALE` | `stale_flagged_at`; FRESHNESS exception; alert |
| `data_product_load` | `LOADED` | LoadRefused | `STALE` | Marked at once; previous stamp stays in use |
| `data_product_load` | `STALE` | Late load commits | `LOADED` | `loaded_at` updated; FRESHNESS exception closed |
| `data_product_load` | `LOADED` | Repeat stamp | `LOADED` | `duplicate_count` incremented; no second row |

No case status changes.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No load by expected-by | STALE; FRESHNESS exception; operations alert; panel warning | MSG-P1-001 |
| X2 | Load refused at a check | STALE at once; previous stamp stays | MSG-P1-002, MSG-P1-001 |
| X3 | Same load stamped twice | One row; duplicate count 1 | None |
| X4 | Late load after the stale flag | LOADED; exception closed | None |
| X5 | Load one minute before expected-by | Not stale | None |
| X6 | Weekly product between loads | Not stale inside the cycle | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoint | `GET /api/recovery/v1/data-products/freshness` (API-P1-009). |
| Contract delta | `DataProductFreshness[]`: productCode, productName, businessDate, sourceExtractedAt, loadedAt, status, staleSince. |
| Backward compatibility | New endpoint; no existing contract changes. |
| Authorization | Case record R; no case scope applies because the stamp holds no case data. |
| Error behaviour | 400 malformed product or date MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002; 503 MSG-GEN-006. |
| Versioning | First release E1; no version bump. Contract tests from the API specification (RWB-TE-003). |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-009; SPEC-RWB-E1-015-012 | New `DataFreshnessPanel` on SCR-03 with LOADED, STALE, Loading and Error states. | Renders each product's date and load time; stale warning; skeleton; error; no personal data in fixtures. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-009; SPEC-RWB-E1-015-001..011 | New service, step, listener, repository, entity, query and controller. | Stamp on commit; duplicate; expected-by boundary; refused; late clear; weekly cycle; snapshot; endpoint; security. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `FreshnessStampService` | Service | Writes stamps in the load transaction; marks and clears stale. |
| `FreshnessCheckStep` | Job | Freshness step of JOB-01 and JOB-09 at each expected-by time. |
| `StaleMarkerListener` | Listener | Consumes LoadRefused and marks the product stale. |
| `DataProductLoadRepository` | Repository | Reads and writes `data_product_load`. |
| `DataProductLoad` | Entity | One row per product and business date. |
| `FreshnessQuery` | Published interface | Stamps for P3 and P7. |
| `FreshnessController` | Controller | `GET /data-products/freshness`. |
| `DataFreshnessPanel` | React component | Data panel on SCR-03. |

Package `recovery.dataengine.freshness`.

### Data and migration

Table `data_product_load`: `id` uuid, `product_code` varchar(25), `source_system` varchar(40),
`business_date` date, `source_extracted_at` timestamptz, `loaded_at` timestamptz, `status` varchar(10),
`stale_flagged_at` timestamptz, `duplicate_count` integer default 0, standard columns; unique
(`product_code`, `business_date`); index (`product_code`, `loaded_at desc`). Reads `data_product` and
`data_as_of` on `loan_account` and `account_payment`.

### Freshness algorithm

1. On a load commit, call `recordLoad(productCode, businessDate, sourceExtractedAt, loadedAt)` in the
   same transaction. A repeat increments `duplicate_count` and leaves one row.
2. At each product's `expected_by`, check that a load exists for the expected business date. If not,
   set the latest row to `STALE`, write a `FRESHNESS` exception and send the operations alert.
3. On LoadRefused, mark the product `STALE` at once, idempotent on the event ID; do not delete loaded
   rows.
4. On a later load for the same business date, set `LOADED`, update `loaded_at` and close the FRESHNESS
   exception.
5. A weekly product is checked against its weekly cycle, not every day.
6. `FreshnessQuery.stampsFor` returns the stamps P7 writes into `inputs_ref`.

**Transaction.** `recordLoad` runs in the load transaction; the stale check and the late-load clear each
run in their own transaction. Consumes EV-27 `LoadRefused`; publishes no event.

### UI behaviour

SCR-03 Case record, read only: the data panel shows each product's business date and load time. When a
product is stale, the panel shows MSG-P1-001 next to it. States: Loading (skeleton rows), Stale input,
Error. The panel is read only.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Writes stamps, marks stale, writes FRESHNESS exception | All |
| SY-DECLOG | Reads stamps through `FreshnessQuery` | All |
| RW-DATASTEW | Platform administration R | All |
| RW-PLATADM | Platform administration R; receives the alert | All |
| RW-CASEOWN, RW-TEAMMGR and other case roles | Case record R; see the panel | Own / team |

### Observability and operations

- Metrics: stamps written; duplicates; stale products per day; time to clear; snapshot calls.
- Alerts: stale product; operations channel; FRESHNESS exception.
- Audit: every decision snapshot holds the stamps it used.
- Run book entry under RWB-E1-056.

### Performance

- One stamp write per load; a single indexed read per query.
- Stale check is one query per product at its expected-by time.
- Snapshot call is a set query for the products a decision read.

### Feature flag and rollback

`rwb.dataengine.freshness-stamp`. Off: no stamp is written and the panel shows the prior state.
Rollback: turn the flag off; `data_product_load` remains and is harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-015-01 | AC1, BR1 | System | DP01 for 2026-11-30; extract 23:30; load 06:50 | Source and load times; LOADED |
| TC-E1-015-02 | AC2, BR2 | System | No DP01 load at 08:00; test clock | STALE; FRESHNESS exception; alert; panel shows "Account and arrears is from 2026-11-30. Today's load has not arrived." |
| TC-E1-015-03 | AC3, BR4 | System | Decision reading DP01 and DP06 | Both stamps in the inputs snapshot |
| TC-E1-015-04 | AC4, BR3 | System | LoadRefused at Control totals 05:20 | STALE from 05:20; 2026-11-30 stamp stays |
| TC-E1-015-05 | AC5, BR5 | System | Same stamp written twice | One row; duplicate count 1 |
| TC-E1-015-06 | AC6, X4 | System | Late DP01 load at 08:40 | LOADED; exception closed |
| TC-E1-015-07 | AC7, X5 | System | DP01 load at 07:59 | Not stale at 08:00 |
| TC-E1-015-08 | AC8, BR6 | System | Weekly DP06 Monday; check Thursday | Not stale |
| TC-E1-015-09 | X1 | System | Missing load for two products | Two stale flags; two exceptions |
| TC-E1-015-10 | Access | Security | RW-REFADM calls the freshness endpoint | 403 MSG-P4-002 |
| TC-E1-015-11 | UI states | Unit | LOADED, STALE, Loading, Error | Correct state and message; no personal data |
| TC-E1-015-12 | BR1, BR5 | Unit | First stamp, repeat stamp, different date | Insert, increment, new row |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2; SPEC-004 | What is the expected-by time? | Determines the stale trigger. | `data_product.expected_by`; 08:00 daily and Monday 08:00 weekly are the assumed values under DL11. | RESOLVED | SPEC-004 |
| CLAR-002 | BR5; SPEC-003 | What happens on a repeat stamp? | Determines duplicate handling. | One row; `duplicate_count` increments (story AC5, R-UNI-40). | RESOLVED | SPEC-003 |
| CLAR-003 | BR3; SPEC-006 | Does a refused load delete prior rows? | Determines data safety. | No; the previous load stays in use and the product is marked STALE. | RESOLVED | SPEC-006 |
| CLAR-004 | BR4; SPEC-011 | Who writes the decision snapshot? | Determines ownership. | P7 calls `stampsFor()` and writes the snapshot; P1 supplies the stamps. | RESOLVED | SPEC-011 |
| CLAR-005 | API; SPEC-010 | Is the freshness endpoint new? | Determines API impact. | Yes; API-P1-009, first release E1. | RESOLVED | SPEC-010 |
| CLAR-006 | AC8; SPEC-008 | How is a weekly product treated between loads? | Determines false stale flags. | Checked against its weekly cycle; not stale between loads (AC8). | RESOLVED | SPEC-008 |
| CLAR-007 | UI; SPEC-012 | Which screen shows the stamp? | Determines UI scope. | SCR-03 data panel; SCR-45 is Epic 2. | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or DL11. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] — SCR-03 Case record and its data panel are specified in the screen inventory and FSD Appendix B; no Figma source is claimed.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New freshness store, query, endpoint and SCR-03 data panel; no change to the loads beyond the stamp call.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new freshness endpoint and SCR-03 data panel]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria, 6 exception paths and 4 stamp transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
