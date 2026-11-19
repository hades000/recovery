# Technical Specification — RWB-E1-055 Proof of delivery capture design with WIN

| Field | Value |
|---|---|
| Story | RWB-E1-055 — Proof of delivery capture design with WIN |
| Epic / module | E1 / P6 Communications |
| RUN_ID | `INC-078-epic-1-RWB-E1-055` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-OCC-003, REQ-ILG-004); story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 055 Proof of delivery capture design with WIN v1.md`; FSD P6 A2.2; TSD P6 T3.1, T5.1 |
| Upstream IDs | REQ-OCC-003, REQ-ILG-004; FEAT-DRI-17; US-RWB-E1-055; R-LIT-07, R-UNI-33, R-UNI-34, R-UNI-40; CTL-15; INT-14, INT-15; DQ-085..091; DF-LEG-015..034 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |
## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The litigation officer reads notice state, dates and barcode on SCR-03 and SCR-30; the platform administrator uses the E1 job endpoints; SCR-44 and SCR-45 are E2. |
| Logic In Scope | `YES` — JOB-10 selection and file build, WIN acknowledgment, JOB-09 INT-15 checks and matching, ledger writes, events, retry, REC-05 reconciliation, stale marker and idempotency. |
| API In Scope | `NO` — no new or changed contract. Reuses `GET /admin/jobs`, `POST /admin/jobs/{jobId}/rerun` and `GET /admin/data-quality/exceptions` (P1, E1). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `notice` table (RWB-E1-052); `outbound_item` and `interface_run` (P2); `dq_exception` (P1); interaction ledger (RWB-E1-066); P3 NOTICE_PERIOD consumer (RWB-E1-028); ACE PII service; job monitor. |
| New Nodes Required | `YES` — `WinNoticeFileJob`, `WinNoticeFileWriter`, `WinAcknowledgmentHandler`, `WinProofOfDeliveryStep`, `DeliveryMatcher`, `NoticeEventPublisher`, `BarcodeReconciliation`, `V1_055__notice_dispatch.sql`. |
| Inherited Existing Behavior | Generated notices (RWB-E1-052); P3 timer on `NoticeDelivered` (RWB-E1-028); interaction ledger (RWB-E1-066); P2 adapters and retry (RWB-E1-007); JOB-09 (RWB-E1-051); configuration (RWB-E1-042); run books (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Only notices in a dispatch-eligible state are written to the WIN file; Generated in E1, Approved from E2. | SPEC-RWB-E1-055-001 | DIRECT | `rwb.comms.dispatch.eligible-states` = GENERATED. | COVERED |
| BR2 | A notice period starts only from the delivery date on the proof of delivery. | SPEC-RWB-E1-055-009, -010 | DIRECT | `NoticeDelivered` carries the callback date; P3 starts the timer. | COVERED |
| BR3 | An unacknowledged file is sent again; after the third failure a task goes to the owning team. | SPEC-RWB-E1-055-006 | DIRECT | Attempt count per notice; task to the litigation officer team. | COVERED |
| BR4 | An INT-15 file that fails a check is refused in full; a record with an unknown reference is held. | SPEC-RWB-E1-055-007, -008 | DIRECT | DQ-085..091 refuse the file; the notice match holds the record. | COVERED |
| BR5 | A notice sent with no barcode after three days is a reconciliation break. | SPEC-RWB-E1-055-013 | DIRECT | REC-05 daily; `barcode-break-days` = 3. | COVERED |
| BR6 | The same event twice produces one effect and the repeat is counted. | SPEC-RWB-E1-055-012 | DIRECT | Barcode + callback date; R-UNI-40 hit count. | COVERED |
| BR7 | The notice data product is stale one business day after the INT-15 file was due. | SPEC-RWB-E1-055-014 | DIRECT | P1 freshness stamp; MSG-P1-001. | COVERED |
| AC1 | JOB-10 runs; WIN acknowledges; notice Sent; ledger entry; `NoticeDispatched`; MSG-P6-004. | SPEC-RWB-E1-055-002..005 | DIRECT | End-to-end dispatch. | COVERED |
| AC2 | INT-15 returns the barcode with a callback date; notice Delivered; ledger entry; `NoticeDelivered`; P3 timer. | SPEC-RWB-E1-055-008..010 | DIRECT | Match by barcode; delivered date. | COVERED |
| AC3 | The WIN sample INT-15 file passes DQ-085..091 with 0 refused; the job monitor records the layout version. | SPEC-RWB-E1-055-007, -018 | DIRECT | Contract test in SIT; `interface_run.checks.layoutVersion`. | COVERED |
| AC4 | Three unacknowledged runs keep the notice Generated and resend it; after the third, a task with MSG-GEN-006. | SPEC-RWB-E1-055-006 | DIRECT | Attempt count 3; task idempotent. | COVERED |
| AC5 | An INT-15 file with trailer 40 and body 39 is refused in full; no notice changes state. | SPEC-RWB-E1-055-007 | DIRECT | DQ-087 control total; MSG-P1-002. | COVERED |
| AC6 | 30 records, 1 unknown: 29 update; 1 held with check References. | SPEC-RWB-E1-055-008 | DIRECT | Per-record hold; no tolerance for notice references (CLAR-007). | COVERED |
| AC7 | The same INT-15 business date loaded twice is refused with MSG-P1-002. | SPEC-RWB-E1-055-011 | DIRECT | DQ-085; no state change. | COVERED |
| AC8 | JOB-10 rerun on the same day writes no second record for the notice. | SPEC-RWB-E1-055-015 | DIRECT | Notice ID + file date idempotency. | COVERED |
| AC9 | A notice with no barcode three days after sending is listed for the platform administrator. | SPEC-RWB-E1-055-013 | DIRECT | REC-05 break on SCR-45. | COVERED |
| AC10 | A repeated delivery record leaves the notice unchanged, publishes no second event and counts the repeat. | SPEC-RWB-E1-055-012 | DIRECT | Barcode + callback date; R-UNI-40. | COVERED |
| AC11 | A late INT-15 file makes the notice data product stale; MSG-P1-001 names DP07 Legal and the last date. | SPEC-RWB-E1-055-014 | DIRECT | P1 freshness; case notice section. | COVERED |
## User story intent interpretation

As a **litigation officer (RW-LITOFF)**, I want **generated notices sent to WIN for print and registered mail, with the dispatch and the proof of delivery written back on the notice**, so that **the case shows what was sent and when it arrived**.

The story owns the WIN boundary. It writes one daily INT-14 file from the notices in a dispatch-eligible state, takes back the WIN barcode and the weekly INT-15 proof of delivery file, and publishes the delivery so P3 starts the notice period from the arrival date, not the print date. Refused, returned and undeliverable letters remain in RWB-E2-021.
## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-10 daily 16:00 Asia/Bangkok; WIN acknowledgment on arrival; JOB-09 weekly Monday 04:00 or on file arrival; REC-05 daily after JOB-01. |
| Preconditions | RWB-E1-052, RWB-E1-028 and RWB-E1-066 done; P2 adapters and the WIN SFTP path agreed; `rwb.comms.dispatch.eligible-states` = GENERATED; JOB-10 and JOB-09 in the job monitor with run books (RWB-E1-056); DQ-085..091 in force. |
| Input | Notices in Generated with no sent date; INT-14 layout; WIN acknowledgment; INT-15 file; `outbound_item`; `interface_run`. |
| Output | INT-14 file; notice `Sent` with sent date, barcode and sent type; notice `Delivered` with callback date and delivery status; ledger entries; `NoticeDispatched` / `NoticeDelivered`; REC-05 breaks; stale marker. |
| Feature flag | `rwb.comms.win-dispatch-v1`. Off: JOB-10, the INT-15 step and REC-05 do not run; notices stay Generated. |
## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `notice` | `state` | Generated | System writes Sent or Delivered | Only the two transitions in this story |
| `notice` | `sent_date` | WIN acknowledgment, DDMMYYYY | System writes | Parsed to a date; not before the file date |
| `notice` | `barcode` | WIN acknowledgment | System writes | Unique where not null |
| `notice` | `sent_type` | WIN acknowledgment, s2t mapping | System writes | BEFORE_NPL or NPL |
| `notice` | `callback_date`, `delivery_status` | INT-15, DDMMYYYY_callBack | System writes | Delivery date; DELIVERED in this story |
| `notice` | `dispatch_file_id`, `dispatch_attempts` | P2 outbound item; increment per file | System writes | UUID; integer default 0; third failure raises a task |
| `outbound_item` | id, interface_id, idempotency_key, payload_ref | P2 enqueue | System writes through P2 | Key `INT-14:<businessDate>` |
| `interface_run` | interface_id, business_date, status, record_count, checks | P2 | System writes through P2 | INT-15 run; `checks` holds layout version and DQ results |
| `dq_exception` | product_code, check_code, record_key, reason_code, status | P1 | System writes through P1 | Held INT-15 records and REC-05 breaks |
| `interaction` | case_id, occurred_at, channel, direction, summary | Ledger writer | System writes | Outbound LETTER and delivery entries |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `GENERATED` | WIN acknowledgment | Barcode returned for the ContractNO in the file | `SENT` | Sent date, barcode, sent type; ledger LETTER; `NoticeDispatched`; MSG-P6-004 |
| `GENERATED` | JOB-10 run, no acknowledgment | No barcode; attempts below 3 | `GENERATED` | New file next run; attempt count +1 |
| `GENERATED` | Third failed attempt | Attempts reach 3 | `GENERATED` | Task to the litigation officer team; MSG-GEN-006 |
| `SENT` | `PROOF_OF_DELIVERY_RECEIVED` | Callback date present | `DELIVERED` | Callback date; delivery status DELIVERED; ledger; `NoticeDelivered`; P3 timer |
| No case status change | — | — | — | P3 starts the NOTICE_PERIOD timer on the event; `recovery_case.status` is unchanged |
## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event | SPEC |
|---|---|---|---|---|
| X1 | WIN does not acknowledge | Notices stay Generated; next JOB-10 sends again; after three, a task | MSG-GEN-006 | SPEC-006 |
| X2 | INT-15 fails a check | File refused in full; earlier delivery data stays | MSG-P1-002 | SPEC-007 |
| X3 | Unknown barcode and ContractNO | Record held on the exception list; the rest load | None | SPEC-008 |
| X4 | INT-15 business date loaded twice | Refused; no state change | MSG-P1-002 | SPEC-011 |
| X5 | JOB-10 runs twice in one day | No second record for the notice | None | SPEC-015 |
| X6 | No barcode three days after sending | REC-05 break listed for the platform administrator | None | SPEC-013 |
| X7 | Later file repeats a delivery | Ignored; counted under R-UNI-40 | None | SPEC-012 |
| X8 | INT-15 one business day late | Notice data product stale | MSG-P1-001 | SPEC-014 |
## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` (Platform administration R); `POST /admin/jobs/{jobId}/rerun` (Platform administration U); `GET /admin/data-quality/exceptions` (Platform administration R). All P1, first in E1. |
| Contract delta | None. `GET /notices/{noticeId}` is first in E2 and is not required in E1; notice fields are read through the SCR-03 and SCR-30 read models. |
| Backward compatibility | Unchanged; no version change. |
| Authorization | Platform administration R/U for jobs and breaks; Litigation R for notice fields; SY-DATALOAD runs the jobs. 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004; 503 MSG-GEN-006. |
## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; notice fields are read on existing screens. | Existing frontend tests stay green; no new test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR7; SPEC-RWB-E1-055-001..019 | New jobs, file writer, acknowledgment handler, INT-15 step, matcher, publisher and reconciliation. | Eligible states; file layout and trailer; DDMMYYYY parse; ack match; no ack at attempts 1/2/3; each DQ check; barcode and contract match; unknown record; duplicate file; duplicate delivery; REC-05 at 2/3 days; stale at 1 business day; rerun. |
## Detailed design
### Components

| Component | Type | Responsibility |
|---|---|---|
| `WinNoticeFileJob` | Job | JOB-10: selects eligible notices, builds and enqueues the INT-14 file, records the outbound item and attempts. |
| `WinNoticeFileWriter` | Service | Builds records and trailer to the INT-14 layout; detokenizes the address into the file stream only. |
| `WinAcknowledgmentHandler` | Published interface | Applies the WIN acknowledgment: Sent, sent date, barcode, sent type; ledger; event. |
| `WinProofOfDeliveryStep` | Job step | JOB-09 INT-15 step: DQ-085..091, matching, Delivered, ledger, event. |
| `DeliveryMatcher` | Service | Matches by barcode, then ContractNO and sent date; holds unknown or ambiguous records. |
| `NoticeEventPublisher` | Service | Writes `NoticeDispatched` and `NoticeDelivered` to the outbox. |
| `BarcodeReconciliation` | Job | Daily REC-05: compares sent notices with returned barcodes; lists 3-day breaks; marks stale. |
### Package, data and migration

Package `recovery.comms.dispatch`. The job calls P2 to enqueue the outbound file; no direct SFTP or WIN call. The contract number comes through P1/P3; the timer is started by P3; the ledger is written through RWB-E1-066.

- `V1_055__notice_dispatch.sql`: adds `dispatch_file_id uuid` and `dispatch_attempts integer not null default 0`.
- `ux_notice_barcode` unique on `barcode` where `barcode` is not null; `ix_notice_state_sent` on `(state, sent_date)`.
- Reads `case_account.is_primary`, `loan_account.contract_no` and `contact_point.value_token` through P1/P3; writes `notice`, `outbound_item` and `interface_run` through P2, `dq_exception` through P1, `interaction` through the ledger writer and the outbox.
- Configuration: `rwb.comms.dispatch.eligible-states` = GENERATED; `max-attempts` = 3; `barcode-break-days` = 3; `pod.stale-after-business-days` = 1.
### Dispatch rules

1. JOB-10 selects notices in an eligible state with no `sent_date` and not already in an unacknowledged file of the same business date. It builds one INT-14 file: ContractNO of the primary account, addressee, detokenized address, notice type, template version and document reference; the trailer carries the record count.
2. It enqueues the file through the P2 outbound interface, writes `dispatch_file_id` and increments `dispatch_attempts` for each notice in the file. The notice stays `GENERATED`.
3. On acknowledgment, parse DDMMYYYY to a date; for each ContractNO, apply the barcode, sent date and sent type to the matching notice in that file. If more than one notice in the file matches the ContractNO, hold the record and raise an incident (CLAR-008).
4. Set `SENT`; write an outbound LETTER ledger entry with the barcode; publish `NoticeDispatched` (EV-14) in the same transaction; the case shows MSG-P6-004.
5. No acknowledgment: the notice stays `GENERATED`; the next JOB-10 includes it again. At `dispatch_attempts = 3`, raise one task to the litigation officer team naming WIN (MSG-GEN-006); a fourth attempt does not raise a second task.
### Proof-of-delivery rules

1. JOB-09 runs weekly Monday 04:00 or on file arrival; the INT-15 step runs DQ-085..091. Any failed check refuses the whole file, changes no notice and writes MSG-P1-002 naming the check.
2. A business date already loaded is refused under DQ-085 with MSG-P1-002.
3. For each record, match by barcode; if none, match by ContractNO and sent date. Apply only when exactly one notice matches; an unknown or ambiguous record is held on the exception list with check References and the rest of the file loads.
4. On a match, set `callback_date`, `delivery_status = DELIVERED` and state `DELIVERED`; write the delivery to the ledger and publish `NoticeDelivered` (EV-15) with the delivery date in the same transaction. P3 starts the NOTICE_PERIOD timer from that date.
5. A later record with the same barcode and callback date changes nothing, publishes no event and increments the R-UNI-40 hit count.
### Reconciliation, events and security

REC-05 runs daily after JOB-01 at a configured time (06:00 assumed; DL11). It compares notices sent to WIN with barcodes returned and lists any notice with no barcode `barcode-break-days` after sending for the platform administrator on SCR-45. The same job marks the DP07 Legal data product stale one business day after the INT-15 file was due, with the last data date; the case notice section shows MSG-P1-001.

| Event | Payload | When |
|---|---|---|
| `NoticeDispatched` (EV-14) | `noticeId`, `barcode`, `sentDate` | Per acknowledged notice. |
| `NoticeDelivered` (EV-15) | `noticeId`, `deliveredDate` | Per newly delivered notice. |

Both are written to the outbox in the same transaction as the notice change; the publisher retries with idempotency.

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Litigation U; runs JOB-10 and JOB-09; writes the outbound file | All |
| SY-CASEWF | Consumes `NoticeDelivered` and starts the timer | All |
| RW-LITOFF | Litigation R; reads notice state, dates and barcode; receives the failure task | Team |
| RW-CASEOWN | Litigation R; reads notice state | Own |
| RW-PLATADM | Platform administration R/U; reruns JOB-10; reads REC-05 breaks | All |
| RW-DATASTEW | Platform administration R; reads refused files and held records | All |

The jobs run under service identities with the same method checks as a person. Addresses are detokenized only into the outbound file stream and never logged; job logs hold notice IDs and counts.

- Metrics and alerts: notices written, acknowledged, delivered, refused; attempts; REC-05 breaks; stale products. Alerts on JOB-10 failure, no acknowledgment after three attempts, INT-15 refused or late, and barcode breaks above baseline.
- Run books and performance: JOB-10 and JOB-09 with purpose, schedule, owner, failure signs, restart steps and escalation (RWB-E1-056). One INT-14 file per day; the INT-15 step matches on the unique barcode index, then on contract and date; no numeric target, record the SIT volume (DL11).
### Feature flag and rollback

`rwb.comms.win-dispatch-v1`. Off: JOB-10, the INT-15 step and REC-05 do not run; notices stay Generated and no file is written. Rollback: turn the flag off and redeploy the previous tag; the migration adds nullable columns and indexes, which the previous tag ignores.
## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-055-01 | AC1, BR1 | System | N-0001 Generated; ack RR123456789TH | Sent; sent date; barcode; ledger LETTER; `NoticeDispatched`; MSG-P6-004 |
| TC-E1-055-02 | AC2, BR2 | System | INT-15 of 2026-11-30 with callback 28112026 | Delivered; callback date; ledger; `NoticeDelivered`; timer starts |
| TC-E1-055-03 | AC3 | System | WIN sample WIN-POD-SAMPLE-v1, 25 records | DQ-085..091 pass; 0 refused; layout version recorded |
| TC-E1-055-04 | AC4, BR3 | System | No ack on 26, 27 and 28 November | Resent each day; stays Generated; task after third; MSG-GEN-006 |
| TC-E1-055-05 | AC5, AC6, BR4 | System | Trailer 40/body 39; then 30 records, 1 unknown | First refused in full; second updates 29 and holds 1 with check References |
| TC-E1-055-06 | AC7, AC8, AC9, AC10, BR5, BR6 | System | INT-15 loaded twice; JOB-10 rerun; N-0002 no barcode; repeat delivery | Second file refused; rerun writes no second record; REC-05 break; repeat unchanged, no second event, R-UNI-40 count |
| TC-E1-055-07 | AC11, BR7 | System | No INT-15 file on 2026-11-30 | DP07 Legal stale; MSG-P1-001 with 2026-11-23 |
| TC-E1-055-08 | Access | Security | RW-PHONECOL reads dispatch detail | 403; MSG-P4-002 |
| TC-E1-055-09 | BR1, BR3, BR4, BR5 | Unit | Eligible states; attempts 2/3; each DQ check; break 2/3 days | Only Generated selected; task at 3; file refused with check named; break at 3 days |
## Guardrails

- No business value in code: schedule, eligible states, attempt limit, break days and stale period are configuration; file layouts follow the interface specification.
- No personal data in logs, tests or prompts; the address is detokenized only into the outbound file stream and is never logged; job logs hold notice IDs and counts.
- No read of another module's tables; contract number through P1/P3; timer started by P3 on the event; held records through P1; files only through the integration adapters (REQ-DRI-006).
## Out of scope

- Refused, returned and undeliverable letters, the proof window and the transfer to the owner's queue (RWB-E2-021, R-LIT-08, R-LIT-09).
- The conduct check before dispatch (RWB-E2-021).
- Notice approval before dispatch (RWB-E2-014).
- Statutory sale notices for repossessed assets (FEAT-AST-04, Epic 3).
## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns to the case | Epic 2 §4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-LIT-07, R-UNI-33, R-UNI-34, R-UNI-40 | TC-E1-055-01..07 |
| REQ-ILG-004 | What happens in an interaction is recorded against that interaction | Epic 1 §3.6, §4 | FEAT-DRI-17 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-055-01, 02, 08 |
## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §4 step 3, §12; SPEC-003 | `WinFileGateway.send` is void, but `dispatch_file_id` needs the file ID; E1-007 publishes `OutboundFiles.enqueue` returning the outbound item. | The job cannot record the file ID with a void send. | Use the P2 `OutboundFiles.enqueue` published interface; write the returned `outbound_item.id` to `dispatch_file_id`. `WinFileGateway` is not a second path. | RESOLVED | SPEC-003 |
| CLAR-002 | AC3; §12; SPEC-002, -018 | The INT-14 layout version and field positions are not supplied; AC3 covers only the INT-15 sample. | The writer cannot be built without a layout. | The WIN owner supplies the INT-14 layout; build to `contracts/win/INT-14`, record the layout version in `interface_run.checks`, and run a contract test with the WIN sample. | RESOLVED | SPEC-002, SPEC-018 |
| CLAR-003 | Header; SPEC-008 | The header depends on RWB-E1-054 (document review queue), which does not provide the INT-15 held-record list. | A wrong dependency would block the story unnecessarily. | Drop the behavioural dependency: held INT-15 records go to the P1 `dq_exception` list and SCR-45. E1-054 remains a separate document-review feature. | RESOLVED | SPEC-008 |
| CLAR-004 | AC8, AC9; §15; SPEC-013, -015 | AC8 reruns JOB-10 "from the job monitor" and AC9 lists breaks on SCR-44/SCR-45, but the story has no screen and those screens are E2. | Determines how the ACs are exercised in E1. | Use the E1 endpoints `POST /admin/jobs/{jobId}/rerun` and `GET /admin/data-quality/exceptions`; SCR-44 and SCR-45 are the E2 surface. | RESOLVED | SPEC-013, SPEC-015 |
| CLAR-005 | AC4, BR3; SPEC-006 | Is the third-failure task raised once per notice or once per file/team? | Determines task volume and repeat behaviour. | One task per notice at `dispatch_attempts = 3`, idempotent by notice so a fourth attempt raises no second task. | RESOLVED | SPEC-006 |
| CLAR-006 | §4 step 9; SPEC-013 | REC-05 runs "each day ... after JOB-01" but no time is given. | Determines the schedule row. | Daily at a configured time after JOB-01; 06:00 is the assumed value (DL11), owned by the platform administrator. | RESOLVED | SPEC-013 |
| CLAR-007 | AC6, BR4; DQ-089; SPEC-008 | AC6 holds 1 of 30 records, but DQ-089 refuses a file above a 0.5 percent reference tolerance. | The AC and the data quality row would give different outcomes. | The notice-reference match is a per-record hold with no tolerance; DQ-089's 0.5 percent applies to account, customer and asset references. One unknown notice does not refuse the weekly file. | RESOLVED | SPEC-008 |
| CLAR-008 | AC1; §4 step 4; SPEC-004 | The acknowledgment carries one entry per ContractNO; a file may hold more than one notice for a contract. | The wrong notice could be marked Sent and start the wrong period. | Apply an acknowledgment only when exactly one notice in that file matches the ContractNO; otherwise hold the record and raise an incident. If WIN can echo the document reference, use it as the first key. | RESOLVED | SPEC-004 |
| CLAR-009 | BR7, AC11; SPEC-014 | Where is the "notice data product stale" state held? | Determines whether a new field is needed. | The P1 data product freshness stamp; the job marks DP07 Legal stale through the P1 interface. No new P6 field. | RESOLVED | SPEC-014 |
| CLAR-010 | §12; SPEC-007 | JOB-09 runs weekly and "or on file arrival"; does an arrival run outside Monday? | Determines duplicate loads and scheduling. | The INT-15 step runs on the Monday schedule and on arrival; the business-date idempotency check prevents a second load. | RESOLVED | SPEC-007, SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all ten items are answered from the story, the P2/P3 interfaces, the data quality rules or the decision log. No item changes the business outcome; CLAR-007 and CLAR-008 remove wrong-state risks.
## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend WIN dispatch story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New JOB-10 WIN outbound file, WIN acknowledgment handling, JOB-09 INT-15 proof of delivery, events and REC-05 reconciliation; existing job and data-quality endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: jobs, file interfaces and events, no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 11 acceptance criteria and 8 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
