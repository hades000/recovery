# Recovery Workbench P1 decisions, batch E (RD-P1-075 to RD-P1-100)

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Run | D-RCV-60 P1 developer readiness (RD-P1 register), third round of rulings |
| Input | `SET\_work\p1-ready\packets\rereview ruling items.csv` (37 items, fix_owner = ruling); the Blocker rows of `rereview story items.csv` (23) and `rereview document items.csv` (12) whose fix needs a decision; the open gaps of staged Gap Register v3 marked "blocks build: Yes" for RWB-P1 stories (30 rows) plus GAP-3412, GAP-3457 (NEW-GAP-S5-8) and GAP-0490; the cross-cutting questions of the orchestrator (XD-11, flag-off answer, DP04 STALE, child workflow start policy, RD-P1-025 seed version, DM cutover, personal-data flag source, access-log entries, recipient phone) |
| Builds on | Recovery Workbench P1 Decision Register v2 (binding). Amendments are stated per decision under "Amends" and collected at the end |
| Prepared by | Chief architect (design sub-agent), Claude Opus 5.5 (claude-opus-5-5) |
| Status of every decision | Proposed – Claude Opus 5.5 (applied); where a part stays Pending it names the owner and the interim build behaviour |
| Precedence | D-RCV-60 and Architecture v5 (SET\22) > RD-P1 decisions > 16 Temporal and Drools (D-RCV-36) > 15 ACE DB Alignment (D-RCV-35) > 14 Story Updates > all other documents |

Abbreviations used for sources: Arch v5 = `SET\22 Microservice Realignment\Recovery Workbench Architecture v5 Text Extract v1.md`; YAML = staged `05 Technical architecture\Recovery Workbench API Specification v7\rwb-source-data.yaml` 5.1.0; ASYNC = staged `asyncapi\rwb-source-data.asyncapi.yaml` 5.1.0; CASE-YAML = staged `rwb-case.yaml`; ACCESS-YAML = staged `rwb-access.yaml`; TWAC v3 = staged Temporal Workflow and Activity Catalog v3.xlsx; PS v9 = staged `06 Data\Recovery Workbench Physical Schema v9\`; DCPI v6 = staged Data Classification and Personal Data Inventory v6.xlsx; EMS v6 = staged Error and Message Standard v6.docx; GR v3 = staged Gap Register v3.md; REG v2 = Recovery Workbench P1 Decision Register v2.md; RR = re-review packets (`ruling items`, `story items`, `document items`) and the reviews under `RWB Story Review P1\rereview\<KEY>\`.

Temporary IDs: NEW-GAP-E1 to NEW-GAP-E5 are new pending items of this batch; the orchestrator assigns the next free GAP numbers after GAP-3580 (the last row of GR v3). Every other gap is cited by its register number (temporary IDs of earlier rounds resolved through `Temp ID to register ID v2.csv`).

## Index

| ID | Title | Re-review items and gaps |
|---|---|---|
| RD-P1-075 | Data dictionary baseline: values copied from Physical Schema v9 | E1001-APP#1 (ruling); amends RD-P1-025 |
| RD-P1-076 | Personal-data flag: Data Classification v6 governs; default masking by classification | E1001-APP#2 (document); E1068-APP#4; E2010-CON#13; GAP-3529; amends RD-P1-060 rule 2 |
| RD-P1-077 | Recipient phone number for SMS and LINE notices | Orchestrator question; narrows GAP-3283 |
| RD-P1-078 | Temporal start mechanisms: client starts, child starts and Schedule starts | Orchestrator question; amends RD-P1-040, RD-P1-002 |
| RD-P1-079 | Readiness after the run closes, the readiness recorder and restarts before wave 4 | XD-11; E1013-APP#1 (story), E1013-APP#8; GAP-3390 |
| RD-P1-080 | Flag-off answers: freshness never 404; 404 MSG-P4-003 for other flagged operations | E1015-OPS#1; GAP-3506; amends RD-P1-043, RD-P1-045 |
| RD-P1-081 | ON_CHANGE products and the DP04 stamp; active-count check; DP04 record selection | E2010-APP#3, #4, #6; E2010-CON#2, #7; E2010-OPS#2; E2010-APP#1 and E2010-CON#1 (story); GAP-3525, GAP-3524; amends RD-P1-041, RD-P1-068 |
| RD-P1-082 | DP04 build reads, rerun and the records read value formats | E2010-CON#3, #6; GAP-3523, GAP-3528, GAP-3571, GAP-0512 |
| RD-P1-083 | Freshness stamp edge cases: missing batch row, re-completion, restatement detection, weekly-only sources, gate value | E1015-APP#1, #2; E1015-CON#1; GAP-3430, GAP-3429, GAP-3288, GAP-3434 |
| RD-P1-084 | Proof-of-delivery: incomplete WIN date and the contract publisher | E1055-APP#1, #14 |
| RD-P1-085 | `GET /batch-status` with no batch row: 404 MSG-P1-001 (directive exception) | E2007-APP#2; amends RD-P1-004 |
| RD-P1-086 | Reconciliation results: REC-05 aggregate row, result page, alert values, rwb-case inputs | E1011-CON#3; AD019-APP#1 (document); E1011-OPS#5; GAP-3412, GAP-3418, GAP-3421, GAP-3422, GAP-3411 |
| RD-P1-087 | Ledger writer refusals and the actor check | E1066-APP#1; E1066-CON#1; GAP-3487, GAP-3489, GAP-3492 |
| RD-P1-088 | Ledger intake: refusals that are not transient | E1067-APP#1; E1067-CON#1; GAP-3496 |
| RD-P1-089 | Ledger series, integrity check, protection of append-only objects and the sandbox reload | E1066-OPS#1; E1065-APP#1; GAP-3494, GAP-3493 |
| RD-P1-090 | Migrated ledger entries: the cutover entry point of the writer | DM005-APP#1 (story) |
| RD-P1-091 | Access-log entries are written through the rwb-access access-log contract, never as decision records | RD-P1-072 vs RWB-P4-E1023-APP and RWB-P4-E1039; E1068-APP#2 (document); GAP-3395, GAP-3322 |
| RD-P1-092 | Retention run record, review list, age bases, record classes and the archive container | E1017-APP#1, #4, #5; E1017-OPS#1; GAP-3457, GAP-3454, GAP-0490 |
| RD-P1-093 | Migration cutover: provenance columns, pipeline authorisation, handover package and acceptance, clean days | DM003-APP#1, DM004-APP#1, DM007-APP#1 (document); DM006-APP#1, DM007-APP#2 (story); orchestrator questions |
| RD-P1-094 | Extension facts: first write, the read of the row and its ETag, access rule | E1018#3; GAP-3555, GAP-3409, GAP-3407 |
| RD-P1-095 | Data-product access: date of the access check, workload identities, field lists, catalog reconciliations | E1016-APP#11; E1016-CON#8; GAP-3443, GAP-3445, GAP-3446 |
| RD-P1-096 | Dictionary and contract rows: object rows, DC-ACE seed, smoke records, reference-load handler, applied version | E1064-APP#3; E1064-APP#1, E1064-OPS#1 (story); E1064-APP#2, E1064-CON#2 (document); GAP-3338, GAP-3403; amends RD-P1-020 |
| RD-P1-097 | Account-page read used by rwb-case for the case list | GAP-3274, GAP-3438 |
| RD-P1-098 | Sandbox contract files and bootstrap: interim build | E1065-CON#1 (story); GAP-3481 to GAP-3486 |
| RD-P1-099 | ACE additions: foreign-key delete rules, orphan rows and load order (interim) | ACE001-DB#4; GAP-3576 |
| RD-P1-100 | Smaller rulings: snapshot(page), SCR-44 route, holder pair, delivery status name, EFS filter, complaints, DM012 to DM014 | E1013-APP#2; AD018-OPS#1 (document); E2034-APP#1 (story); E1068-APP#1 (document); E2001-APP#1 (document); DM012-APP#1, DM013-APP#1, #2, DM014-APP#1, #2 (story); GAP-3375, GAP-3327, GAP-3425, GAP-3384 |

---

## RD-P1-075 · Data dictionary baseline: values copied from Physical Schema v9

**Question.** RD-P1-025 tells RWB-P1-E1001-APP to copy the 123 objects and 1,379 baseline fields from the Physical Schema v8 seed. The v8 seed has DF-REF-074 as `varchar(120)`; PS v9 (staged, line 1457) has `varchar(200)` and corrected DF-ACE types. Which seed is the baseline (RR ruling item RWB-P1-E1001-APP#1)?

**Options considered.** (1) Keep v8 and apply the v9 corrections by a later migration. (2) Copy the baseline from PS v9. Option 2: PS v9 is the staged next version that already carries the RD-P1-025 widening and the RD-P1-024 retirements; copying v8 would ship values the register already corrected.

**Sources.** REG v2 RD-P1-025 (baseline "Physical Schema v8 rwb_source_data.sql seed … DF-REF-074 widened to varchar(200)"); PS v9 `rwb_source_data.sql` line 1457 (DF-REF-074 `varchar(200)`), lines 2432-2434 (retired rows marked `RETIRED`), 2436 onwards (rows "added by later story migrations … not part of the RWB-P1-E1001-APP baseline"); PS v9 README line 235 (127 object rows and 1,409 field rows = the 123 / 1,379 baseline plus `data_product_source` and later story rows).

**Precedence applied.** RD-P1-025 is a register decision; this decision amends its source version only. Counts are unchanged.

**Ruling.**
1. The RWB-P1-E1001-APP baseline is the `rwb_source_data.sql` seed of **Physical Schema v9**: the 123 `sys_objects` and 1,379 `sys_fields` baseline rows with their v9 values (DF-REF-074 `varchar(200)`, the corrected DF-ACE physical types), the `data_product` seed (14 rows), `case_list_row` and `lake_copy_watermark` kept and marked `RETIRED`. Counts stay "at least 123 / 1,379".
2. The rows PS v9 lists after the comment "Dictionary rows added by later story migrations" (`job_run`, `job_run_check`, `business_day_readiness`, DF-OPS-233 to DF-OPS-257, DF-EXT-050, DF-INT-030) and the `data_product_source` rows (DF-REF-300 to DF-REF-302) are not baseline rows; they are written by the migration of the story that creates the table (RD-P1-096 rule 1).
3. RWB-P1-E1001-APP section 4 step 3, section 13 build step 8, AC1 and AC5 say "copied with their Physical Schema v9 values"; every "Physical Schema v8" citation in P1 stories that names the seed becomes v9.
4. The `is_personal` values of the seed follow RD-P1-076 (Data Classification v6), not the v9 seed as it stands.

**Rationale.** One baseline that already includes the corrections the register made, so no story ships a value that a later migration must undo.

**Affected services.** rwb-source-data.
**Affected stories.** RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1064-OPS, RWB-P1-E1016-DB, RWB-P1-ACE001-DB, RWB-P1-E1016-CON.
**Affected documents.** Register RD-P1-025 (amendment line); Test Cases v9 (TC-P1-E1001-APP rows citing v8); Logical Data Model and Data Dictionary v11 (no change; already v9 values).
**Findings settled.** RWB-P1-E1001-APP#1 (re-review).
**GAP/ASM.** None.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A dictionary baseline is always copied from the highest staged Physical Schema version.
**Values chosen without a source.** None.

---

## RD-P1-076 · Personal-data flag: Data Classification v6 governs; default masking by classification

**Question.** RWB-P1-E1001-APP AC13 (CTL-11) compares `sys_fields.is_personal` with the personal-data inventory, but the PS v9 seed and DCPI v6 disagree. Which source governs, what does AC13 compare, and what does "a field with no rule is masked" (RD-P1-060 rule 2) apply to? Related: RWB-P1-E1068-APP guardrail "A personal field with no unmasking rule is never returned" against BR4 returning promise fields (RR E1068-APP#4); DP04 personal data and an access-log write failure (GAP-3529; RR E2010-CON#13).

**Options considered.** (1) PS v9 seed governs. (2) DCPI v6 governs and `is_personal` mirrors its "Personal data" column; masking by default keyed on `is_personal`. (3) DCPI v6 governs; `is_personal` mirrors "Personal data"; the mask-by-default rule keys on the DCPI classification Restricted. Option 3.

**Sources.** DCPI v6 sheet Fields (1,395 fields; columns BR Field ID, Personal data category, Classification, Personal data, On screen); sheet Key ("Restricted: masked or never exposed in clear"; "Confidential: customer data shown within scope, encrypted"; "Internal: shown by permission"; "Masking policy: the P4 rwb-access masking_rule rows, enforced in each service and applied by rwb-source-data on every ACE field it serves"); sheet Handling; Read me v6 ("Personal-field flags remain keyed by field ID; P4 rwb-access owns masking_rule"). PS v9 `rwb_source_data.sql` sys_fields seed (1,409 rows). Comparison made for this ruling: 500 field IDs differ (seed false where DCPI says Yes: 361 Customer data, 76 Indirect identifier, 50 Staff identifier, 5 Sensitive, 4 Direct identifier; seed true where DCPI says No: DF-DOC-049, DF-DOC-052, DF-DOC-077, DF-DOC-089); 27 seed rows have no DCPI row (DF-INT-030, DF-REF-274 to DF-REF-299). DCPI v6 DF-TRT-050 `contract_no`: Not personal, Internal. REG v2 RD-P1-060 rule 2. RWB-P3-E1023-APP BR4 ("a read whose record cannot be written returns no data").

**Precedence applied.** No higher tier rules the flag. DCPI is the inventory owned by the data protection officer and the document the bank's PDPA controls cite; the dictionary column is a copy. **Amends RD-P1-060 rule 2** (scope of the mask-by-default rule).

**Ruling.**
1. **Source of truth.** DCPI v6 sheet Fields governs whether a field is personal, its category and its classification. `sys_fields.is_personal` = true exactly when the DCPI v6 row of the same field ID has Personal data = "Yes".
2. **Seed correction.** The data architect corrects the `is_personal` values of the PS v9 seed (staged, not yet released) to rule 1 before RWB-P1-E1001-APP is Done: 496 rows false → true and the four DF-DOC rows above true → false. LDM v11 sheet Fields follows the same flags.
3. **AC13.** RWB-P1-E1001-APP AC13 compares every baseline field ID present in DCPI v6: `is_personal` must equal (Personal data = "Yes"); any difference fails with the list of field IDs. A field ID absent from DCPI v6 is listed as "unclassified" and does not fail AC13; the 27 absent rows (DF-INT-030, DF-REF-274 to DF-REF-299) are **Pending, owner data protection officer**, NEW-GAP-E1; interim they are treated as not personal and the list is attached to the release evidence.
4. **Masking default (amends RD-P1-060 rule 2).** `FieldMasker.mask(dto, session)` (RWB-P4-E1037-CON) applies to every personal field. A field of classification **Restricted** (Direct identifier or Sensitive) with no unmasking rule for the caller is masked. A personal field of classification Confidential or Internal (Customer data, Indirect identifier, Staff identifier) is returned within the caller's case scope unless a masking rule masks it (DCPI v6 Handling and Key). Confirmation of this default by the data protection officer is **Pending**, NEW-GAP-E5; interim the FieldMasker fake applies rule 4 as written.
5. **RWB-P1-E1068-APP.** The guardrail reads "A Restricted field with no unmasking rule is never returned in clear". `personKey` and `contactKey` (Indirect identifier), `actorRef` (Staff identifier) and the promise fields `promiseAmount`, `promiseDate` (Customer data, Confidential; DF-INT-010) are returned within scope; `summary` keeps its own rule (masked unless the role may see it; RD-P1-072 rule 2).
6. **DP04 (GAP-3529).** No DP04 property is Restricted in DCPI v6; `contract_no` (DF-TRT-050) is Not personal, Internal, and is returned by permission. When the access-log entry of a records read cannot be written (RD-P1-091), the read answers **503 MSG-GEN-006** and returns no row (fail closed; RWB-P3-E1023-APP BR4 pattern). GAP-3529 is closed.

**Rationale.** One owner for classification; the dictionary flag becomes checkable; masking by default lands on the 17 Restricted fields instead of silently masking 500 customer-data fields that the screens must show within scope.

**Affected services.** rwb-source-data; rwb-access (masking rules, FieldMasker fake); every service that uses FieldMasker.
**Affected stories.** RWB-P1-E1001-APP, RWB-P1-E1068-APP, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1069-APP, RWB-P1-E2010-CON, RWB-P1-E2010-APP, RWB-P4-E1037-CON, RWB-P4-E1037-APP, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON.
**Affected documents.** Physical Schema v9 `rwb_source_data.sql` (is_personal values; owner data architect); Logical Data Model and Data Dictionary v11 (same); Data Classification and Personal Data Inventory v6 (27 rows Pending); register RD-P1-060 (amendment line); Gap Register v3 (GAP-3529 closed; NEW-GAP-E1, NEW-GAP-E5); Test Cases v9 (TC rows of E1001-APP AC13, E1068-APP guardrail).
**Findings settled.** RWB-P1-E1001-APP#2, RWB-P1-E1068-APP#4, RWB-P1-E2010-CON#13 (re-review).
**GAP/ASM.** Closes GAP-3529. Narrows GAP-3475 (NEW-GAP-S6-13) to the confirmation in NEW-GAP-E5. New NEW-GAP-E1, NEW-GAP-E5.
**Status.** Proposed – Claude Opus 5.5 (applied); NEW-GAP-E1 and NEW-GAP-E5 pending with the data protection officer.
**Reuse note.** Ask DCPI whether a field is personal; mask by default only what DCPI classes Restricted.
**Values chosen without a source.** Classification-keyed masking default; "unclassified" handling of fields absent from DCPI.

---

## RD-P1-077 · Recipient phone number for SMS and LINE notices

**Question.** RD-P1-060 rule 3 unmasks the clear name and the postal address for the rwb-comms notice and rwb-integration outbound-file identities (masking rows Pending GAP-3283, NEW-GAP-D1). SMS notices (RWB-P1-E2022-APP, RWB-P6-E2022-APP) need the clear phone number. Who may read it, and through which read?

**Sources.** REG v2 RD-P1-060 rules 2-4; DCPI v6 DF-ACE-078 `contact_value` (Direct identifier, Restricted, "Masked unless the role may see it", lawful basis "legal obligation for statutory notices"); DCPI v6 sheet Key ("ACE contact value: full value where a notice or a call needs it; masked for display"); YAML `ContactPointRow` and DP02 records rule (no contact value).

**Ruling.**
1. The clear phone number is the `contactValue` of a `contacts[]` row with `contactType` PHONE, read only through `GET /customers/{personKey}` (RD-P1-060), chosen by `contactKey`.
2. It is unmasked only for the **rwb-comms notice workload identity** (SMS and LINE dispatch through NSS and LINE OA; RWB-P1-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2021-APP). rwb-integration, gateway-bff and every user role get `contactValueMasked`. EMAIL rows follow the same rule.
3. The masking rule rows are part of GAP-3283 (NEW-GAP-D1), widened to "PHONE and EMAIL `contactValue` for the rwb-comms notice identity"; owner data protection officer with the rwb-access owner. Interim: the FieldMasker fake unmasks PHONE and EMAIL `contactValue` for the rwb-comms notice identity only; tests assert the masked branch for every other caller.
4. The phone number never enters an event, a workflow input, a ledger `summary`, a log or a metric (DCPI v6 PII controls); the ledger CONTACT entry carries `contactKey` only.

**Affected services.** rwb-source-data; rwb-comms; rwb-access.
**Affected stories.** RWB-P1-E2022-APP, RWB-P6-E2022-APP, RWB-P6-E2022-CON, RWB-P6-E2021-APP, RWB-P1-E1069-APP, RWB-P4-E1037-CON.
**Affected documents.** Gap Register v3 (GAP-3283 subject widened); Users Roles and Permissions v6 / Role to System Access Matrix v4 (masking rows Pending).
**GAP/ASM.** GAP-3283 widened.
**Status.** Proposed – Claude Opus 5.5 (applied); masking rows pending under GAP-3283.
**Reuse note.** Any channel that needs a clear contact point reads it from `GET /customers/{personKey}` under its own notice identity and stores only `contactKey`.
**Values chosen without a source.** EMAIL included with PHONE.

---

## RD-P1-078 · Temporal start mechanisms: client starts, child starts and Schedule starts

**Question.** RD-P1-040 and TWAC v3 rows R19 and R22 give the child starts of `ReconciliationWorkflow` and `Stage2ProductWorkflow` "conflict USE_EXISTING and reuse ALLOW_DUPLICATE". A Temporal child workflow start has no workflow-ID conflict policy: only client starts do. What is the correct mechanism, and does the 05:30 Schedule start the per-date run?

**Options considered.** (1) Keep the text. (2) Client starts keep USE_EXISTING; child starts use a deterministic workflow ID, a reuse policy and explicit handling of the already-started failure; Schedule starts go through a starter that issues a client start. Option 2.

**Sources.** TWAC v3 sheet Workflows R18 (AceIngestCheck: ID `ace-ingest-check-{businessDate}`, USE_EXISTING, ALLOW_DUPLICATE), R19 (`recon-{businessDate}`, "conflict USE_EXISTING and reuse ALLOW_DUPLICATE for the original child start"), R22 (`stage2-dp04-{businessDate}`, same), R23; sheet Schedules R12 (`rwb-source-data-ace-late-check`, 05:30, SKIP, catch-up 1 h, "Starts AceIngestCheck for the expected business date if no run is open"); sheet Platform rules R8 (ABANDON), R12 (Worker Versioning), R16 (SKIP), R18 (Temporal 1.30 or later), R22 (reruns FAIL + ALLOW_DUPLICATE_FAILED_ONLY). REG v2 RD-P1-040 item 1, item 5 as amended, XD-11. Temporal behaviour (platform facts, Temporal 1.30): `WorkflowIdConflictPolicy` is an option of a client start (and of signal-with-start) only; a child start takes a workflow ID and a `WorkflowIdReusePolicy`; when the ID is already running, or closed and the reuse policy refuses it, the child start fails (history event `StartChildWorkflowExecutionFailed` with cause `WORKFLOW_ALREADY_EXISTS`; the SDK raises its workflow-execution-already-started failure through the child's start promise); a Schedule action starts its workflow with the action's workflow ID suffixed by the scheduled time.

**Precedence applied.** RD-P1-040 (register) is amended; TWAC v3 rows follow. No higher-tier source sets a policy.

**Ruling.**
1. **Client starts of AceIngestCheck** (readiness handler, fallback poll, admin): workflow ID `ace-ingest-check-{businessDate}`, `WorkflowIdConflictPolicy` USE_EXISTING, `WorkflowIdReusePolicy` ALLOW_DUPLICATE, unchanged. The admin rerun of a FAILED run keeps FAIL + ALLOW_DUPLICATE_FAILED_ONLY (Platform rules R22).
2. **Child starts** (`ReconciliationWorkflow` `recon-{businessDate}`, `Stage2ProductWorkflow` `stage2-dp04-{businessDate}`), issued by AceIngestCheck in the workflow task that commits the ALS stamp:
   - `ChildWorkflowOptions`: the deterministic workflow ID, `ParentClosePolicy` ABANDON, `WorkflowIdReusePolicy` **ALLOW_DUPLICATE_FAILED_ONLY**, task queue `rwb-source-data`. No conflict policy is set (none exists for a child).
   - The parent waits for the child's start promise (`Workflow.getWorkflowExecution(child)` in the Java SDK) before it completes or continues, so an ABANDONed child is never lost when the parent closes.
   - When the start fails because the ID already exists (open run, or a closed COMPLETED run refused by the reuse policy), AceIngestCheck treats the child as started: it records nothing new, raises no failure and increments `rwb_source_data_duplicate_start_total` with label `workflow` = the child type. Any other start failure fails the workflow task and is retried by Temporal.
   - A closed FAILED child is never restarted by the parent; it is rerun only through `POST /admin/jobs/{jobId}/rerun` (a client start with FAIL + ALLOW_DUPLICATE_FAILED_ONLY), or before wave 4 as in RD-P1-079 rule 4.
3. **Schedule starts.** Because a Schedule suffixes its workflow ID with the scheduled time, the Schedule `rwb-source-data-ace-late-check` does not start AceIngestCheck itself. Its action starts the short workflow **`AceLateCheckStart`** (task queue `rwb-source-data`, ID `ace-late-check-start` plus the Schedule suffix), whose one activity `startIngestForExpectedDate` computes the expected business date (RD-P1-041 item 1) and issues the client start of rule 1 with `startedBy` SCHEDULE. The fallback poll, when built (GAP-3277), uses the same starter with `startedBy` POLL.
4. **Catalog rows.** TWAC v3 R19 and R22 read "child start: deterministic ID, reuse ALLOW_DUPLICATE_FAILED_ONLY, already-started treated as started; no conflict policy (child starts have none); admin rerun FAIL + ALLOW_DUPLICATE_FAILED_ONLY". R18 keeps its policies. A new Workflows row `AceLateCheckStart` (P1, kind "Schedule starter", activity `startIngestForExpectedDate`) and a new Activities row are added; Schedules R12 reads "starts AceLateCheckStart, which starts or attaches to AceIngestCheck for the expected business date".
5. **Reuse rule (amends the RD-P1-040 reuse note).** "Every system-started workflow uses USE_EXISTING + ALLOW_DUPLICATE" applies to client starts only. In-service child starts use a deterministic ID, ALLOW_DUPLICATE_FAILED_ONLY and the already-started handling of rule 2. Schedule-started per-date work goes through a starter activity.

**Rationale.** Uses only options Temporal offers for each start kind; keeps one run per date even when the Schedule fires; keeps XD-11's "never a second ReconciliationWorkflow" true by the reuse policy, not by convention.

**Affected services.** rwb-source-data; every service that starts child workflows or Schedule-started per-date work (reuse).
**Affected stories.** RWB-P1-E1015-APP, RWB-P1-E1015-OPS, RWB-P1-E1011-APP, RWB-P1-E2010-APP, RWB-P1-E2010-OPS, RWB-P1-AD019-APP, RWB-P1-E1013-APP, RWB-P1-AD018-APP, RWB-ITG-E1015-ITG.
**Affected documents.** Temporal Workflow and Activity Catalog v3 (R18 note, R19, R22, Schedules R12, two new rows); Batch and Scheduling Design v7 (JOB-04 and the 05:30 row); register RD-P1-040 and RD-P1-002 (amendment lines); Test Cases v9 (child start duplicate case).
**GAP/ASM.** None closed; GAP-3277 unchanged.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Client start: USE_EXISTING + ALLOW_DUPLICATE. Child start: deterministic ID + ALLOW_DUPLICATE_FAILED_ONLY + already-started = started. Schedule: start a starter, never the per-date workflow.
**Values chosen without a source.** Workflow type `AceLateCheckStart`, activity `startIngestForExpectedDate`, ID prefix `ace-late-check-start`, label `workflow` on the duplicate metric.

---

## RD-P1-079 · Readiness after the run closes, the readiness recorder and restarts before wave 4

**Question.** XD-11 (register v2) merged RD-P1-040 item 1 and RD-P1-065 rule 3 and asked for confirmation; TWAC v3 R18 still says "DONE or LATE starts nothing". Who writes `business_day_readiness` transitions for starts that are not HTTP (RR E1013-APP#1)? How is a date recovered when its ingest run failed or closed before the ALS batch arrived, before the AD018 rerun exists (RR E1013-APP#8; GAP-3390)?

**Sources.** REG v2 XD-11, RD-P1-040 item 1 (24 h close), RD-P1-065 rule 3, RD-P1-020 F (`business_day_readiness`, DF-OPS-252 to DF-OPS-257, state LOV-READINESS RUNNING/DONE/LATE, written by RWB-P1-E1013-APP), RD-P1-022 (readiness pair E1013-APP; AceIngestCheck E1015-APP), X-17 and NEW-ASM-X4 (restart before wave 4 by a repeated ready call or the poll); TWAC v3 R18; PS v9 `business_day_readiness` seed rows.

**Ruling.**
1. **XD-11 confirmed, with the mechanism.** On `POST /business-days/{date}/ready`:
   - (a) a run `ace-ingest-check-{date}` is open → the client start (USE_EXISTING) attaches; answer 202 with the stored state;
   - (b) no run is open and every due source of the date has its stamp row (`data_product_load` for the products it feeds) → nothing is started; answer 202 with the stored state;
   - (c) no run is open and a due source is not stamped (never started, the run FAILED, or the run closed at 24 h) → a new run opens (ALLOW_DUPLICATE) and stamps only the missing sources; `job_run.run_no` + 1 when AD018 is live.
   The check of (b) is the in-process `DailyCompletenessGate` source set of the date read by the handler. No second AceDataReady for a stamped source; no second ReconciliationWorkflow (RD-P1-078 rule 2).
2. **TWAC v3 R18** replaces "DONE or LATE starts nothing" with rule 1 (a)-(c). RD-P1-065 rule 3 reads with this rule.
3. **Readiness recorder (E1013-APP#1).** RWB-P1-E1013-APP builds the in-process component `ReadinessRecorder` with two methods, each idempotent and run inside the caller's transaction:
   - `recordReceived(businessDate, startedBy)` – upsert on `uk_business_day_readiness`; first insert state RUNNING, `received_at` now. Called by the ready handler (HTTP) and by the first activity of every AceIngestCheck run started otherwise (SCHEDULE, POLL, ADMIN).
   - `recordState(businessDate, DONE | LATE)` – called by RWB-P1-E1015-APP inside the `stampProducts` transaction that commits the ALS stamp (DONE) and inside the transaction that writes the ALS AceDataLate outbox row (LATE); sets `changed_at`. LATE may become DONE when ALS is stamped later; DONE never changes back.
   RWB-P1-E1015-APP adds both calls to section 4 and its workflow contract; the E1015-CON workflow note names them.
4. **Restart before wave 4 (GAP-3390).** Until RWB-P1-AD018 is released:
   - AceIngestCheck: rule 1 (c) is the restart: a repeated ready call (or the fallback poll where enabled) opens a new run for a date with an unstamped due source. The readiness row keeps its state until the new run writes DONE.
   - A FAILED `ReconciliationWorkflow` or `Stage2ProductWorkflow`: the platform administrator (RW-PLATADM) starts the same workflow ID with the Temporal CLI under runbook entry "P1 run failed before wave 4", reuse policy ALLOW_DUPLICATE_FAILED_ONLY, input `{businessDate, startedBy: ADMIN}`, and records the action in the release record. A COMPLETED run is never restarted. From wave 4 the admin rerun of RD-P1-012 replaces the runbook step.
   GAP-3390 is closed by this rule.

**Affected services.** rwb-source-data.
**Affected stories.** RWB-P1-E1013-APP, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1011-APP, RWB-P1-E2010-APP, RWB-P1-E2010-OPS, RWB-P1-AD018-APP, RWB-ITG-E1013-ITG, RWB-ITG-E1015-ITG.
**Affected documents.** Temporal Workflow and Activity Catalog v3 (R18 text); Observability and Monitoring Design v6 (runbook entry); register RD-P1-040, RD-P1-065 (amendment lines; XD-11 confirmed); Gap Register v3 (GAP-3390 closed); Assumptions Register v3 (ASM-5707 unchanged; NEW-ASM-X4 confirmed with rule 4).
**Findings settled.** RWB-P1-E1013-APP#1, RWB-P1-E1013-APP#8 (re-review).
**GAP/ASM.** Closes GAP-3390.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A repeated start opens a new run only for work not yet done; never re-run done work by a start call.
**Values chosen without a source.** Component and method names; runbook step for wave 3 and earlier.

---

## RD-P1-080 · Flag-off answers: freshness never 404; 404 MSG-P4-003 for other flagged operations

**Question.** RD-P1-043 (Section B flag `rwb.dataengine.freshness-stamp` off: ready 202, status LATE, freshness STALE with null date) and RD-P1-045 item 4 (first-release rollback: "the api answers 404 on the flagged operations") give two answers for the same flag; RWB-P1-E1015-OPS AC5 and AC21 disagree and the YAML freshness read has no 404 (RR E1015-OPS#1). Which message does a flagged-off 404 carry, and does the ledger-writer flag gate the in-process writer (GAP-3506)?

**Sources.** REG v2 RD-P1-043 item 3, RD-P1-045 item 4, RD-P1-062 (never-stamped answer); YAML `/data-products/freshness` (no 404), `/admin/jobs` ("While the flag rwb.p1.jobmonitor is off both job operations answer 404 MSG-P4-003 (RD-P1-045)"), `/admin/reconciliation/results` (same), `/proof-of-delivery` (flag off: 200 with no row and DP07 STALE); RWB-P1-E1015-OPS lines 85, 101, 150-155, 216-221; RWB-P1-E1015-APP AC40; EMS v6 MSG-P4-003.

**Ruling.**
1. **Freshness and readiness never answer 404 because of a flag.** For `rwb.dataengine.freshness-stamp` off – before the ACE dependency gate and after a first-release rollback alike – `GET /data-products/freshness` answers 200 with every product `businessDate` null, status STALE (RD-P1-043 item 3(c), RD-P1-062); `GET /business-days/{date}/status` answers LATE for a date with a readiness row (404 MSG-P4-003 only for a date with no row, RD-P1-020 F); `POST /business-days/{date}/ready` answers 202 and records the readiness row (RD-P1-079 rule 3) but **starts no AceIngestCheck** while the flag is off, so no run queues while the worker is at zero. AceIngestCheck keeps its own guard (RWB-P1-E1015-APP AC40: a run that starts with the flag off writes no stamp, event or child).
2. **Other flagged operations.** An operation behind a flag with no flag-off answer ruled in an RD-P1 decision answers **404 MSG-P4-003** while its flag is off (the YAML form already used for the job monitor and the reconciliation results). Reads whose flag-off answer is ruled keep it: `GET /proof-of-delivery` (200, no row, DP07 STALE).
3. **First-release rollback (amends RD-P1-045 item 4).** Flag off; worker scaled to zero; the release's Schedules paused; operations answer as in rules 1 and 2. RWB-P1-E1015-OPS AC21 reads "the readiness and freshness operations answer as in AC5 and every other flagged operation of the release answers 404 MSG-P4-003".
4. **Ledger-writer flag (GAP-3506).** `rwb.dataengine.ledger-writer` gates the REST append path only (404 MSG-P4-003). In-process callers are gated by their own flags: `rwb.dataengine.ledger-events` (intake consumers paused, RWB-P1-E1067-APP), the DM005 cutover switch (RWB-P1-DM005-APP), RWB-P1-E2034-APP's own flag. GAP-3506 is closed.

**Affected services.** rwb-source-data; consumers of freshness (no change).
**Affected stories.** RWB-P1-E1015-OPS, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1013-APP, RWB-P1-E1066-APP, RWB-P1-E1066-OPS, RWB-P1-E2001-APP, RWB-P1-E2007-APP, RWB-P1-E1011-OPS, RWB-P1-E1017-OPS, RWB-P1-E2010-OPS, RWB-P1-AD019-OPS.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (descriptions of the flagged operations: "404 MSG-P4-003 while <flag> is off"); register RD-P1-043 and RD-P1-045 (amendment lines); Gap Register v3 (GAP-3506 closed); Test Cases v9 (TC-P1-E1015-OPS-19 and the AC21 row).
**Findings settled.** RWB-P1-E1015-OPS#1 (re-review).
**GAP/ASM.** Closes GAP-3506.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A read that gates other services' work answers "no data" when flagged off, never 404; every other flagged-off operation answers 404 MSG-P4-003.
**Values chosen without a source.** Ready call starts no run while the flag is off.

---

## RD-P1-081 · ON_CHANGE products and the DP04 stamp; active-count check; DP04 record selection

**Question.** RD-P1-041 item 4 sets the stamp in use STALE at `expected_by` and its GAP lines close GAP-0511 as "DP04: STALE at expected_by 08:00"; RD-P1-068 rule 6 says DP04 is ON_CHANGE, stamped when its core-bank source completes, never STALE by time. `stampProducts` of AceIngestCheck and `stampDp04` of Stage2ProductWorkflow both claim the DP04 row (GAP-3525). The active-count check compares a window of changed rows with an unwindowed count (GAP-3524). Which row per treatment does the DP04 records read answer (RR E2010-APP#6, E2010-CON#7)?

**Sources.** REG v2 RD-P1-041 items 3, 4, 7 and GAP lines, RD-P1-068 rule 6, RD-P1-002 (Stage2ProductWorkflow activities); PS v9 `data_product` seed line 904 (DP04 ON_CHANGE, "As it changes"; DP03 line 903 ON_CHANGE), `data_product_source` seed lines 2429-2431 (no DP04 row; core-bank code Pending ASM-5695), `dp_treatment` (`uk_dp_treatment (business_date, treatment_id)`), `dp_guarantee_claim`; CASE-YAML / PS v9 `rwb_case.case_account.is_primary`, `linked_to`; TWAC v3 R22; RWB-P1-E2010-APP s4 steps 1-6; GR v3 GAP-2696 (Accepted (directive): active states held as a parameter row).

**Precedence applied.** RD-P1-068 (later, specific) prevails over RD-P1-041 for ON_CHANGE products. **Amends RD-P1-041** (item 4 scope; item 7 writer; GAP-0511 line) and **RD-P1-068 rule 6** (when the DP04 row is written).

**Ruling.**
1. **STALE by time applies to DAILY and WEEKLY products only.** RD-P1-041 item 4's `expected_by` trigger never runs for a product whose `refresh_cycle` is ON_CHANGE (DP03, DP04). The FAILED trigger still applies to an ON_CHANGE product that has a mapped source. The "Closes GAP-0511 (DP04: STALE at expected_by 08:00 …)" line of RD-P1-041 now reads "GAP-0511 closed by RD-P1-068: DP04 is ON_CHANGE and never STALE by time".
2. **One stamp component.** `data_product_load` is written only by the stamp component of RWB-P1-E1015-APP (`FreshnessStampWriter`, in process). `stampProducts` (AceIngestCheck) calls it for products whose `refresh_cycle` is DAILY or WEEKLY and that have at least one `data_product_source` row; it never stamps an ON_CHANGE product. `stampDp04` (Stage2ProductWorkflow, RWB-P1-E2010-APP) is the only caller that stamps DP04. GAP-3525 is closed.
3. **When DP04 is stamped (amends RD-P1-068 rule 6).** Stage2ProductWorkflow for D starts as a child in the workflow task that commits the ALS stamp (TWAC v3 R22). `stampDp04` writes the DP04 row for D (status LOADED, `source_system` `WORKBENCH`, `source_extracted_at` = the ALS `completed_at` of D, `loaded_at` = write instant) after every DP04 page of D is committed. When the core-bank code of ASM-5695 is confirmed and a DP04 `data_product_source` row is seeded, Stage2ProductWorkflow waits (durable timer, `ingest.poll.interval.minutes`) for that source to be COMPLETED for D before `stampDp04`; until then it does not wait.
4. **Active-count check (GAP-3524).** The comparable population is: for each `treatment_id`, the `dp_treatment` row with the greatest `business_date` ≤ D, counted when its state is active. Active states are the parameter row GAP-2696 names, **Pending, owner rwb-treatment owner with RW-COE** (GAP-3524 narrowed to the states). Interim: `checkActiveCount` runs in report mode – on a difference it lists the break with MSG-P1-002 and the count in the run result, but it does not hold `stampDp04`. The hold is switched on by the story change that closes GAP-3524.
5. **DP04 records read selection (E2010-APP#6, E2010-CON#7).** `GET /data-products/DP04/records?caseId=` answers, per `treatment_id` and per `guarantee_claim_id` of the case, the row with the greatest `business_date` ≤ the business date of the DP04 stamp in use. `recordId` = `treatment_id` or `guarantee_claim_id` (not the row `id`); `entity` = `dp_treatment` or `dp_guarantee_claim`. The contract number, contract date and plan terms are joined at request time from `v_ace_account` / `v_ace_plan` on the case's primary account: the `case_account` row with `is_primary` true and `linked_to` null, read through the rwb-case contract. Rows of a date later than the stamp in use (an unfinished or failed build) are never answered.
6. **Stories.** RWB-P1-E2010-APP, -CON and -OPS remove every "08:00 / expected_by / STALE from the expected-by time" statement for DP04 (s3, X3, s13, s19, AC4, AC5, BR4, s14; TC-P1-E2010-APP-08, TC-P1-E2010-CON-04, -12) and cite this decision; the E2010-OPS smoke asserts only that the DP04 row is written by `stampDp04` after the ALS stamp.

**Affected services.** rwb-source-data; rwb-treatment (parameter row).
**Affected stories.** RWB-P1-E2010-APP, RWB-P1-E2010-CON, RWB-P1-E2010-OPS, RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-DM004-APP, RWB-S2-E2010-APP, RWB-ITG-E2010-ITG.
**Affected documents.** Temporal Workflow and Activity Catalog v3 (R22 steps; Activities R22 `stampProducts` scope); register RD-P1-041, RD-P1-068, RD-P1-002 (amendment lines); API Specification v7 `rwb-source-data.yaml` (records read description for DP04); Gap Register v3 (GAP-3525 closed, GAP-3524 narrowed, GAP-0511 closure text); Test Cases v9.
**Findings settled.** RWB-P1-E2010-APP#1, #3, #4, #6; RWB-P1-E2010-CON#1, #2, #7; RWB-P1-E2010-OPS#2 (re-review).
**GAP/ASM.** Closes GAP-3525; narrows GAP-3524 (blocks build: No with the interim).
**Status.** Proposed – Claude Opus 5.5 (applied); active states pending under GAP-3524.
**Reuse note.** A derived product is stamped by its build, through the single stamp component, and only ACE-fed DAILY/WEEKLY products go STALE by time.
**Values chosen without a source.** `FreshnessStampWriter` name; `source_system` WORKBENCH and the time columns of the DP04 row; report-mode interim; latest-row-per-ID population.

---

## RD-P1-082 · DP04 build reads, rerun and the records read value formats

**Question.** RWB-P1-E2010-CON uses `page=0&size=1000` for the treatment and claim reads while RWB-S2-E2010-APP and RWB-S3-E2010-APP refuse "a page below one" (RR E2010-CON#3). What happens on a rerun to rows absent from the new answer and to pages committed before a failure (GAP-3523)? What are the string forms of `FieldValue.value`, the order and the `total` of the records read (RR E2010-CON#6; GAP-0512, GAP-3528, GAP-3571)?

**Sources.** YAML (every page parameter `minimum: 0, default: 0`; `JobPage`, `InteractionPage`, `DataProductRecordPage` {items, page, size, total}; `FieldValue.value` string, non-null); CASE-YAML (page `minimum: 0`); GR v3 GAP-2696 and GAP-2738 (Accepted (directive): window reads with page, size, total, maximum 1000, 400 on an empty or inverted window, order `updated_at` then `id`); PS v9 `dp_treatment` (numeric(18,2), timestamptz, date columns, `updated_at`).

**Ruling.**
1. **Page base.** Every page of the Recovery Workbench REST contracts is zero-based (`page` minimum 0, default 0), as every published page in API Specification v7. The rwb-treatment read `GET /treatments?changedFrom=&changedTo=&page=&size=` and the rwb-guarantee read `GET /guarantee-claims?changedFrom=&changedTo=&page=&size=` take `page` from 0, `size` 1 to 1000 (default 1000 for the DP04 build), answer {items, window, page, size, total}, order `updated_at` then `id`, and answer 400 MSG-GEN-003 on an inverted window and 400 MSG-GEN-001 on a missing bound; an empty window [D, D+1) with no row answers 200 with `items` empty. RWB-S2-E2010-APP and RWB-S3-E2010-APP change "a page below one" to "a page below zero".
2. **Rerun and visibility (GAP-3523).** A FAILED run's committed pages stay; they are invisible because the records read answers only rows dated ≤ the DP04 stamp in use (RD-P1-081 rule 5) and a failed run writes no stamp. The rerun upserts by (`business_date`, record ID), then, before `stampDp04`, deletes the rows of business date D (both tables) whose `updated_at` is earlier than the rerun's start instant – the rows its answer no longer contains. GAP-3523 is closed.
3. **Value formats of `FieldValue.value` (records read, every product).** Timestamp: ISO 8601 with offset `+07:00` (Asia/Bangkok), seconds precision. Date: `yyyy-MM-dd`. Numeric: plain decimal string with the scale of the physical type (`numeric(18,2)` → `300000.50`), no grouping, `.` as separator. Boolean: `true` / `false`. Integer: decimal digits. A null column: the `FieldValue` is omitted. A masked field: `value` = the masked form, `masked` true. GAP-0512 and GAP-3528 are closed; GAP-3571 (physical types of uncast view columns) stays open for the ACE data owner but no longer blocks: the format follows the type the view returns.
4. **Order and total (GAP-3528).** Items ordered by `entity`, then `recordId`, ascending; `total` = number of `DataProductRecord` items over all pages (not field values).

**Affected services.** rwb-source-data; rwb-treatment; rwb-guarantee.
**Affected stories.** RWB-P1-E2010-CON, RWB-P1-E2010-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP, RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-ITG-E2010-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`FieldValue.value` description; records read order and total), `rwb-treatment.yaml` and `rwb-guarantee.yaml` (when the two reads are published, CDC-03577 and GAP-2738); Gap Register v3 (GAP-3523, GAP-0512, GAP-3528 closed; GAP-3571 non-blocking).
**Findings settled.** RWB-P1-E2010-CON#3, RWB-P1-E2010-CON#6 (re-review).
**GAP/ASM.** Closes GAP-3523, GAP-0512, GAP-3528.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Zero-based pages everywhere; dated snapshot rows are made invisible by the stamp, not by transactions spanning pages.
**Values chosen without a source.** Claim-read maximum 1000; delete-by-`updated_at` rule; string formats; order key.

---

## RD-P1-083 · Freshness stamp edge cases: missing batch row, re-completion, restatement detection, weekly-only sources, gate value

**Question.** (a) AceDataLate `status` is required and "copied unchanged" from `v_ace_batch_status`, but a source may have no row (GAP-3430; RR E1015-APP#1, E1015-CON#1). (b) A date D whose row went STALE after a failure completes again, but `uk_data_product_load (product_code, business_date)` forbids a second row (RR E1015-APP#2). (c) How is a changed `completed_at` detected for a multi-source product (GAP-3429)? (d) Which run holds the timer and late event of a weekly-only source (GAP-3288)? (e) Where is the gate value COMPLETE/HOLD over REST (GAP-3434)?

**Sources.** ASYNC lines 186-222 (AceDataReady and AceDataLate payloads); PS v9 `recovery_views.sql` lines 498-510 (`v_ace_batch_status`), `data_product_load` (lines 185-203); PS v9 `data_product_source` seed (DP06: CCMS, SVAF, AMIS, RPS – weekly only); REG v2 RD-P1-040 item 1 ("a source is due on a date when it feeds a DAILY product, or a WEEKLY product whose cycle day that is") and item 3, RD-P1-041 items 1, 4-6; YAML `/data-products/freshness` (array of `DataProductFreshness`).

**Ruling.**
1. **No batch row (GAP-3430).** In ASYNC 5.1.0 AceDataLate `data.status` becomes `type: [string, "null"]`, still required: the `v_ace_batch_status` value copied unchanged, **null when the source has no batch row for the date**; `completedAt` stays null. AceDataReady is unchanged (always a row). RWB-P1-E1015-APP AC41 and RWB-P1-E1015-CON AC17 and the sample assert `status: null`. GAP-3430 is closed.
2. **Re-completion of a STALE date (E1015-APP#2).** When (P, D) already has a row that went STALE (failed after completed) and every mapped source is COMPLETED again for D, the existing row is **updated in place**: status LOADED, `stale_flagged_at` null, `source_extracted_at` = the new latest `completed_at`, `loaded_at` = update instant, `duplicate_count` + 1, `version` + 1. No second AceDataReady, no child start (RD-P1-079 rule 1); the operations duplicate alert fires (restated batch runbook entry). RWB-P1-E1015-APP s4 step 7 and a new state row and AC state this.
3. **Restatement detection (GAP-3429).** While the run of D is open, a restatement is detected when the latest `completed_at` among P's sources differs from `source_extracted_at` of P's row for D (RD-P1-041 item 6 then applies). A restatement of a source whose new time stays below the product's latest time, and any restatement after the run has closed, is not detected by P1 in version 1. AC35 asserts the open-run case on the latest source. GAP-3429 stays open for the per-source store, **blocks build: No**.
4. **Weekly-only sources (GAP-3288).** A source that feeds only a WEEKLY product is due in the AceIngestCheck run whose start day in Asia/Bangkok is the product's cycle weekday (DP06: Monday, from `expected_by` MON 08:00), i.e. the run of the latest bank business day before that day. That run raises AceDataLate for the source at 05:30 of the cycle day with that business date and holds DP06's `expected_by` timer (MON 08:00). Other runs neither poll nor raise anything for the source. GAP-3288 is closed; confirmation of the cycle-day rule by the ACE team lead is recommended.
5. **Gate value over REST (GAP-3434).** No gate member is added to `GET /data-products/freshness`. `DailyCompletenessGate` is in-process only (`listEligibleAccounts`, `/efs-history`, reconciliation, AD019); a REST caller uses the per-product `status` and `GET /business-days/{date}/status`. RWB-P1-E1015-CON removes the REST gate assertion. GAP-3434 is closed.

**Affected services.** rwb-source-data; AceDataLate consumers (alerts, gateway-bff banner).
**Affected stories.** RWB-P1-E1015-APP, RWB-P1-E1015-CON, RWB-P1-E1015-OPS, RWB-P1-E1013-APP, RWB-ITG-E1015-ITG.
**Affected documents.** `asyncapi/rwb-source-data.asyncapi.yaml` (AceDataLate status nullable); Event and Messaging Design v7 / Kafka Topic and Event Catalog v3 (EV-27 status note); Gap Register v3 (GAP-3430, GAP-3288, GAP-3434 closed; GAP-3429 non-blocking); Test Cases v9.
**Findings settled.** RWB-P1-E1015-APP#1, #2; RWB-P1-E1015-CON#1 (re-review).
**GAP/ASM.** Closes GAP-3430, GAP-3288, GAP-3434.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Null, never an invented code, for a value the source does not have; one row per key, updated in place on re-completion.
**Values chosen without a source.** Nullable status; in-place update; cycle-day run rule; version 1 detection limit.

---

## RD-P1-084 · Proof-of-delivery: incomplete WIN date and the contract publisher

**Question.** How does `GET /proof-of-delivery` show a date whose WIN batch is incomplete, with no answer member for it (RR E1055-APP#1)? Which story publishes `getProofOfDelivery` and its fake (RR E1055-APP#14)?

**Sources.** YAML `/proof-of-delivery` ("RWB-P1-E1055-APP … only when the WIN batch of the date is COMPLETED … the answer has no member for the reason (Pending: GAP-0579)"), `ProofOfDeliveryAnswer` {businessDate, productCode DP07, freshness, rows}; PS v9 `data_product_source` (DP07: LIT, WIN); RWB-P6-E1055-APP X2; REG v2 RD-P1-011 (fakes), RD-P1-022 (contract homes).

**Ruling.**
1. **Incomplete date.** No member is added. The answer carries `freshness` = DP07 stamp in use. rwb-comms treats the requested `businessDate` as incomplete when `freshness.businessDate` is null or earlier than the requested date, or `freshness.status` is STALE; it then appends no delivery entry and reads again on its next poll. `rows` is empty in that case. RWB-P1-E1055-APP adds the AC; RWB-P6-E1055-APP X2 reads the same rule.
2. **Publisher.** `getProofOfDelivery` is published in **RWB-P1-E1015-CON** (the freshness-and-read surface, as for the other P1 reads, X-27) and built by RWB-P1-E1055-APP; the fake (RD-P1-011) has three examples: complete date with rows, incomplete date (businessDate earlier, rows empty), flag off. RWB-P1-E1055-APP s20 "CON Done" points to RWB-P1-E1015-CON; RWB-P6-E1055-APP's contract dependency changes from RWB-P1-E1055-APP to RWB-P1-E1015-CON.

**Affected stories.** RWB-P1-E1055-APP, RWB-P1-E1015-CON, RWB-P6-E1055-APP, RWB-P6-E1055-CON, RWB-ITG-E1055-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (description: publisher and incomplete-date rule); Service Contract Catalog v3 (row of `getProofOfDelivery`); Story Build Order v5 / Dependency Map v7 (dependency edge).
**Findings settled.** RWB-P1-E1055-APP#1, #14 (re-review).
**GAP/ASM.** GAP-0579 closed by rule 1 (the reason member is not needed).
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A consumer decides completeness from the freshness stamp it is given; consumers depend on CON stories, never on APP stories.
**Values chosen without a source.** None beyond rule 2's choice of contract home.

---

## RD-P1-085 · `GET /batch-status` with no batch row: 404 MSG-P1-001 (directive exception)

**Question.** RD-P1-004's status table maps "record missing or outside scope" to 404 MSG-P4-003; the YAML and GAP-0597 answer 404 MSG-P1-001 for a source and date with no batch row; RWB-P2-E2007-APP and -CON say MSG-P4-003 (RR E2007-APP#2).

**Sources.** GR v3 GAP-0597 (Resolved (directive), D-RCV-60: "answer 404 with MSG-P1-001 when no batch row exists for the source and date"); YAML `/batch-status` 404; REG v2 RD-P1-004 status table; EMS v6 MSG-P1-001 ("Data product stale after a late or failed batch").

**Precedence applied.** D-RCV-60 directive resolution (top tier, as X-27) over RD-P1-004. **Amends RD-P1-004** (one recorded exception).

**Ruling.** `GET /batch-status` answers **404 MSG-P1-001** when `v_ace_batch_status` has no row for the source and date: the batch has not arrived, which is a freshness state, not a missing record. This is the one exception to the RD-P1-004 status table; 404 MSG-P4-003 keeps its meaning everywhere else. RWB-P2-E2007-APP and RWB-P2-E2007-CON (line 266) change to MSG-P1-001; RWB-P1-E2007-APP AC13 and X12 keep it.

**Affected stories.** RWB-P1-E2007-APP, RWB-P2-E2007-APP, RWB-P2-E2007-CON, RWB-ITG-E2007-ITG, RWB-P8-E4050-APP (caller of `getBatchStatus`).
**Affected documents.** Register RD-P1-004 (amendment line); API Specification v7 (no change).
**Findings settled.** RWB-P1-E2007-APP#2 (re-review).
**GAP/ASM.** GAP-0597 confirmed.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A source batch not yet arrived is MSG-P1-001 in every answer, whatever the status code.
**Values chosen without a source.** None.

---

## RD-P1-086 · Reconciliation results: REC-05 aggregate row, result page, alert values, rwb-case inputs

**Question.** Consumers read a "REC-05 aggregate for the date" (RWB-P8-E4050-APP s12, RWB-P3-AD019-APP, RWB-P1-DM009-APP s12.8), and the DM clean-day rule needs "no new REC-05 orphan", while RWB-P1-E1011-CON s11 says REC-05 is not inserted and the YAML `recCode` enum is REC-01, REC-02 (RR E1011-CON#3). The result page envelope is Pending (GAP-3412; RR AD019-APP#1). Alert selectors, ticket channel and thresholds are Pending (GAP-3418, GAP-3421, GAP-3422; RR E1011-OPS#5). The rwb-case allocation and exclusion paths are unpublished (GAP-3411).

**Sources.** PS v9 `reconciliation_result` (lines 326-347; `uk_reconciliation_result (rec_code, business_date, product_group)`); YAML `/admin/reconciliation/results` and `ReconciliationResultPage` (Pending), `/admin/jobs` (page 0-based, size default 50 max 200, from default today minus 7 days, `JobPage`); REG v2 RD-P1-022 (P1 computes REC-01, REC-02, REC-05), RD-P1-042 (tolerance 0.00, clean day), RD-P1-069 (aggregates only); BSD v7 JOB-04; data_product `expected_by` 08:00 (DL11).

**Ruling.**
1. **REC-05 is served as one aggregate row per business date** in `reconciliation_result`: `rec_code` REC-05, `product_group` `ALL`, `source_count` = keys checked, `workbench_count` = keys resolved, `variance_count` = orphan keys, `variance_pct` = orphans / keys checked × 100 (0 when none checked), `tolerance_pct` 0.0000, `result` PASS when `variance_count` = 0, else BREAK. The YAML `recCode` enum becomes [REC-01, REC-02, REC-05]; the LOV of `product_group` for results adds `ALL` (Reference Data and Lists of Values v6). RWB-P1-E1011-CON s11 drops "Do not … insert REC-05". Orphan key detail stays Pending (GAP-1508, GAP-3413). The DM clean day reads "every REC-01, REC-02 and REC-05 row of the date PASS" (RD-P1-093 rule 5).
2. **Result page (GAP-3412).** `ReconciliationResultPage` = {items: ReconciliationResult[], page, size, total}, required all four; `page` minimum 0 default 0, `size` 1 to 200 default 50; `from` default today minus 7 days, `to` default today (Asia/Bangkok, inclusive, on `business_date`); order `business_date` descending, then `rec_code`, then `product_group`; 422 MSG-GEN-002 for size out of range, 422 MSG-GEN-003 for `from` after `to`. The fake and AD019-APP AC1, AC9 use it. GAP-3412 is closed.
3. **Alerts (GAP-3418, GAP-3421, GAP-3422).** Interim values-file entries of rwb-source-data, armed only while the reconciliation flag is on: break alert on any REC-01, REC-02 or REC-05 BREAK row of the date (consistent with tolerance 0.00); JOB-04 not-completed alert when no ReconciliationWorkflow of D is COMPLETED by 08:00 Asia/Bangkok; route to the P1 squad channel of the values file; ticket channel blank (no ticket) until the owner fills it. The three gaps stay open for the operational owner, **blocks build: No**.
4. **rwb-case inputs (GAP-3411).** Until rwb-case publishes the allocation and exclusion paths and the dated REC-02 open-case input, the reconciliation is built and tested against the rwb-case contract fake with the shapes named in RWB-P1-E1011-CON; the reconciliation flag stays off outside DEV and SIT. GAP-3411 stays open, owner rwb-case service owner, **blocks build: No**.

**Affected services.** rwb-source-data; rwb-payment, rwb-case (readers).
**Affected stories.** RWB-P1-E1011-APP, RWB-P1-E1011-CON, RWB-P1-E1011-OPS, RWB-P1-AD019-APP, RWB-P1-AD019-OPS, RWB-P1-DM003-APP to RWB-P1-DM010-APP (clean day), RWB-P8-E4050-APP, RWB-P3-AD019-APP, RWB-ITG-E1011-ITG, RWB-ITG-AD019-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`recCode` enum, `ReconciliationResultPage`, parameters); Reference Data and Lists of Values v6 (`ALL`); Observability and Monitoring Design v6 (reconciliation break and JOB-04 rows); Gap Register v3 (GAP-3412 closed; GAP-3418, GAP-3421, GAP-3422, GAP-3411 non-blocking).
**Findings settled.** RWB-P1-E1011-CON#3, RWB-P1-AD019-APP#1, RWB-P1-E1011-OPS#5 (re-review).
**GAP/ASM.** Closes GAP-3412.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Every P1 page is {items, page, size, total}, 0-based, 50/200; a check without detail is still an aggregate row.
**Values chosen without a source.** `product_group` ALL; REC-05 column mapping; 08:00 not-completed boundary; sort order.

---

## RD-P1-087 · Ledger writer refusals and the actor check

**Question.** What status and messageCode does the writer answer for a DECISION_TAKEN append without `decisionLogId`, with an unknown entry, or when the decision-log read does not answer (GAP-3487)? For a future `occurredAt` and a `correctsEntryId` that names an unknown entry or one of another case (GAP-3489)? For a service identity other than rwb-case whose case read answers 404, and must a user token's `actorRef` equal its subject (GAP-3492)? (RR E1066-APP#1, E1066-CON#1.)

**Sources.** RWB-P1-E1066-APP v3 s4 steps 3, 5, 6, X4, X6, X9, AC16, AC17, s12.2; EMS v6 MSG-GEN-001, MSG-GEN-003, MSG-GEN-007, MSG-P4-002, MSG-P4-003, MSG-P1-022; REG v2 RD-P1-004 (status table), RD-P1-007 rule 5, RD-P1-009 (actor form `USER:` / `SERVICE:` / `PARTNER:`).

**Ruling.** Nothing is written in any refusal.
1. **DECISION_TAKEN (GAP-3487).** No `decisionLogId` → 422 MSG-GEN-001, `field` decisionLogId. The decision-log read answers 404, or the entry's `caseId` is not the path case → 422 MSG-GEN-007, `field` decisionLogId. The read does not answer in 2 s or answers 503 → 503 MSG-P1-022 (as X6). GAP-3487 is closed.
2. **CORRECTION (GAP-3489).** `correctsEntryId` unknown or of another case → 422 MSG-GEN-007, `field` correctsEntryId.
3. **Future occurredAt (GAP-3489).** `occurredAt` later than the server receipt instant plus `ledger.occurred-at.future-tolerance.seconds` (values file, 300) → 422 MSG-GEN-003, `field` occurredAt. GAP-3489 is closed.
4. **Other service identities (GAP-3492).** A service identity other than rwb-case whose case read answers 404 or 403 gets 404 MSG-P4-003, as a user caller (X4).
5. **Actor check (GAP-3492).** For a delegated user token (a token with a user subject), `actorType` must be USER and `actorRef` must equal the token's Workbench user identifier; otherwise 403 MSG-P4-002. For a workload token, `actorType` and `actorRef` are stored as sent (the calling service vouches; RD-P1-009). GAP-3492 is closed; confirmation by compliance is recommended.
6. The provider fake of RWB-P1-E1066-CON s12.8 maps each of these refusals.

**Affected stories.** RWB-P1-E1066-APP, RWB-P1-E1066-CON, RWB-P1-E1067-APP (in-process mapping, RD-P1-088), RWB-P3-E1066-APP, RWB-ITG-E1066-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`POST /cases/{caseId}/interactions` description and 422 rows); Gap Register v3 (GAP-3487, GAP-3489, GAP-3492 closed); Test Cases v9 (AC16, AC17 rows).
**Findings settled.** RWB-P1-E1066-APP#1, RWB-P1-E1066-CON#1 (re-review).
**GAP/ASM.** Closes GAP-3487, GAP-3489, GAP-3492.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A body reference that does not resolve is 422 MSG-GEN-007 naming the field; a downstream that does not answer is 503 with the owner's write-failed code.
**Values chosen without a source.** MSG-GEN-007 and MSG-GEN-003 for these cases; 300 s tolerance and its key; actor equality rule.

---

## RD-P1-088 · Ledger intake: refusals that are not transient

**Question.** The intake (RWB-P1-E1067-APP) retries transient failures and parks malformed events; what does it do when the in-process writer refuses for a reason a retry cannot cure – case not found, validation refusal, decision-log reference refused – and with which `rwb-dlt-reason` (GAP-3496; RR E1067-APP#1, E1067-CON#1)?

**Sources.** REG v2 RD-P1-009 (retry 1 min, 10 min, 1 h, then `<topic>.dlt`; headers `rwb-dlt-reason`, `rwb-dlt-consumer`, `rwb-dlt-owner`; LEDGER_WRITE_FAILED only on RETRIES_EXHAUSTED); RWB-P1-E1067-APP lines 92, 102, 145, 170, 198, 324 (reasons UNSUPPORTED_VERSION, RETRIES_EXHAUSTED, MISSING_ATTRIBUTE, SCHEMA_INVALID); RD-P1-087.

**Ruling.**
1. Such a refusal is parked **at once** on `<topic>.dlt` (no retry topic), with `rwb-dlt-consumer=rwb-source-data`, `rwb-dlt-owner=P1 squad` and `rwb-dlt-reason`:
   - `CASE_NOT_FOUND` – the case read answers 404 or 403;
   - `VALIDATION_REFUSED` – the writer answers 422 (any field), the field name in header `rwb-dlt-field`;
   - `DECISION_REF_REFUSED` – the DECISION_TAKEN reference is missing or refused (RD-P1-087 rule 1).
2. The offset is committed after the `.dlt` write; `processed_event` records the `ce_id` with no entry; no LEDGER_WRITE_FAILED is raised (it stays for RETRIES_EXHAUSTED). A decision-log or case read that does not answer stays transient (retry path).
3. Replay after correction uses the platform replay tool; the business key prevents a duplicate entry.
4. RWB-P1-E1067-APP X6 and AC8 read: "no entry; parked at once with `CASE_NOT_FOUND`; the consumer log shows the case ID and no payload value". RWB-P1-E1067-CON AC5, AC11 and the writer stub follow.

**Affected stories.** RWB-P1-E1067-APP, RWB-P1-E1067-CON, RWB-P1-E1066-OPS (dlt alert), RWB-ITG-E1067-ITG.
**Affected documents.** Event and Messaging Design v7 / Kafka Topic and Event Catalog v3 (reason values of the ledger-intake `.dlt`); Gap Register v3 (GAP-3496 closed).
**Findings settled.** RWB-P1-E1067-APP#1, RWB-P1-E1067-CON#1 (re-review).
**GAP/ASM.** Closes GAP-3496.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A consumer parks at once what a retry cannot fix and names why in `rwb-dlt-reason`.
**Values chosen without a source.** The three reason values; header `rwb-dlt-field`.

---

## RD-P1-089 · Ledger series, integrity check, protection of append-only objects and the sandbox reload

**Question.** RWB-P1-E1066-OPS names five ledger series and three alerts without metric names, types or the emitting component; the case_seq gap check, the periodic trigger check and an incident signal that survives a database outage are open (GAP-3494; RR E1066-OPS#1). How are TRUNCATE and trigger changes refused (E1066-OPS AC11), and how does the sandbox reload `interaction` while TRUNCATE is refused (GAP-3493; RR E1065-APP#1)?

**Sources.** RWB-P1-E1066-OPS v3 lines 58, 82, 95, 153-159, 198-202, 298 (series: append rate, failures by class, duplicate hits, p95 latency, case_seq gaps; dimensions environment, release, build ID; no case ID label); PS v9 `rwb_source_data.sql` lines 599-608 (`refuse_change()`, `tr_interaction_append_only BEFORE UPDATE OR DELETE`), README line 179 (logins by RWB-PLT-NF06-DB, privileges by RWB-PLT-N011-DB); existing metric form `rwb_source_data_duplicate_start_total`, `rwb_source_data_win_delivery_repeat_total`; TWAC v3 Platform rules R19 (no Quartz; a job is a Temporal Schedule); REG v2 RD-P1-073 rule 1, RD-P1-046.

**Ruling.**
1. **Series (GAP-3494)**, emitted by `InteractionLedgerWriter` (RWB-P1-E1066-APP) through the service's metrics registry, labels `environment`, `release`, `build_id` only (plus the label named):
   - `rwb_source_data_ledger_append_total` – counter, label `caller` (REST, INTAKE, E2034, CUTOVER);
   - `rwb_source_data_ledger_append_failure_total` – counter, label `error_class` (DB, SEQ_CLASH, CASE_READ, DECISION_READ, VALIDATION);
   - `rwb_source_data_ledger_duplicate_total` – counter, label `kind` (HEADER_REPLAY, BUSINESS_KEY);
   - `rwb_source_data_ledger_append_duration_seconds` – histogram; the dashboard shows p95;
   - `rwb_source_data_ledger_case_seq_gap_total` – counter, written by the integrity check of rule 2.
   The series live in process memory and are scraped from the metrics endpoint, so a database outage still raises the failure-rate alert on `error_class="DB"` (the incident signal). RWB-P1-E1066-APP adds the emitting code and an AC; RWB-P1-E1066-OPS AC4 and AC5 assert names and labels. Thresholds stay values-file entries of E1066-OPS.
2. **Integrity check.** Temporal Schedule `rwb-source-data-ledger-check`, hourly, overlap SKIP, starts workflow `LedgerIntegrityCheck` (activity `checkLedgerIntegrity`, RWB-P1-E1066-APP). It counts case_seq gaps on cases not closed (gaps of closed cases are accepted, RD-P1-048) into `rwb_source_data_ledger_case_seq_gap_total`, and sets gauge `rwb_source_data_ledger_guard_present` to 1 when `tr_interaction_append_only` and `tr_interaction_no_truncate` exist and are enabled, else 0 (alert on 0). TWAC v3 gains the Schedule and workflow rows.
3. **Protection of append-only objects (GAP-3493).** Both mechanisms apply:
   - the tables of `rwb_source_data` are owned by the migration owner role that runs Flyway for the schema (created by RWB-PLT-NF06-DB, privileges by RWB-PLT-N011-DB); the runtime login `rwb_source_data` holds SELECT and INSERT on `interaction` only (no UPDATE, DELETE, TRUNCATE or TRIGGER), so it cannot TRUNCATE or `ALTER TABLE … DISABLE TRIGGER`;
   - a forward migration of RWB-P1-E1066-APP adds `CREATE TRIGGER tr_interaction_no_truncate BEFORE TRUNCATE ON interaction FOR EACH STATEMENT EXECUTE FUNCTION refuse_change();`, so even the owner role cannot truncate.
4. **Sandbox reload (E1065-APP#1).** The in-place reload of RWB-P1-E1065-APP truncates and reloads the ACE-shaped tables of `public` and the generator-seeded P1 tables **except `interaction`**; generator `interaction` rows are inserted only when the table is empty. The "rebuild from DDL between suites" of RD-P1-073 is `DROP SCHEMA rwb_source_data CASCADE` in `rwb_sandbox` by the migration owner role under the sandbox build identity (RD-P1-098 rule 4), then the Flyway sequence and the seed; the database is never dropped (RD-P1-046). Never done outside `rwb_sandbox`. AC5 of RWB-P1-E1065-APP is aligned; GAP-3493 is closed.

**Affected stories.** RWB-P1-E1066-APP, RWB-P1-E1066-OPS, RWB-P1-E1067-APP, RWB-P1-E2034-APP, RWB-P1-E1065-APP, RWB-P1-E1065-DB, RWB-PLT-NF06-DB, RWB-PLT-N011-DB, RWB-ITG-E1066-ITG.
**Affected documents.** Physical Schema v9 `rwb_source_data.sql` (TRUNCATE trigger as the next forward version; ownership note in the README); Temporal Workflow and Activity Catalog v3 (Schedule and workflow rows); Observability and Monitoring Design v6 (ledger series and alerts); register RD-P1-073 (clarification line); Gap Register v3 (GAP-3494, GAP-3493 closed).
**Findings settled.** RWB-P1-E1066-OPS#1, RWB-P1-E1065-APP#1 (re-review).
**GAP/ASM.** Closes GAP-3494, GAP-3493.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Append-only tables: runtime login INSERT/SELECT only, BEFORE UPDATE/DELETE and BEFORE TRUNCATE triggers, an hourly integrity check; reset only by a schema rebuild in the sandbox.
**Values chosen without a source.** Metric and label names; hourly Schedule, workflow and activity names; the gauge.

---

## RD-P1-090 · Migrated ledger entries: the cutover entry point of the writer

**Question.** RWB-P1-DM005-APP writes migrated notes and promises through `InteractionLedgerWriter` in process (XD-08), but the writer sets `id`, `caseSeq` and `sourceSystem` itself, and `migration_source` and `migrated_at` are not in `InteractionRequest` (RR DM005-APP#1).

**Sources.** REG v2 XD-08, RD-P1-007 (server-set fields), RD-P1-027 (standard columns `migration_source varchar(20)`, `migrated_at timestamptz`), RD-P1-064 rule 1; PS v9 `interaction`; GR v3 GAP-3275 (LOV-MIGRATION-SOURCE values).

**Ruling.**
1. RWB-P1-E1066-APP builds the in-process method `InteractionLedgerWriter.appendMigrated(MigratedInteraction)`, callable only by RWB-P1-DM005-APP and only while the DM005 cutover switch is on; no REST path.
2. It takes the legacy `occurredAt`, `eventCode`, `actorType`, `actorRef`, `channel`, `direction`, `contactResult`, `summary`, `promiseAmount`, `promiseDate`, `contactKey`, `idempotencyKey` (the legacy business key) and `migrationSource`. It sets `id`, `caseSeq` (per case, in legacy `occurredAt` order, under the same advisory lock as `append`), `sourceSystem` WORKBENCH, `migration_source`, and `migrated_at` = commit instant (UTC), and keeps the append-only rules. An existing business key adds nothing.
3. `migration_source` takes the LOV-MIGRATION-SOURCE value (Pending, owner data owner, GAP-3275); interim the fixture value is a test constant, never a LOV row.
4. The legacy-to-writer field mapping is RWB-P1-DM005-APP's (section 11, from Source to Target Mapping v7 sheet Migration packages). RWB-P1-E1066-APP becomes a build dependency of RWB-P1-DM005-APP.

**Affected stories.** RWB-P1-DM005-APP, RWB-P1-E1066-APP, RWB-ITG-DM005-ITG.
**Affected documents.** Story Build Order v5 / Dependency Map v7 (edge E1066-APP → DM005-APP); register RD-P1-007 (clarification line).
**Findings settled.** RWB-P1-DM005-APP#1 (re-review).
**GAP/ASM.** GAP-3275 unchanged.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A migration writes through the owner's own component, never by a raw insert, and that component sets the provenance columns.
**Values chosen without a source.** Method and type names.

---

## RD-P1-091 · Access-log entries are written through the rwb-access access-log contract, never as decision records

**Question.** RD-P1-072 says reads go to the access log only and publish no DecisionRecorded, but RWB-P4-E1023-APP (BR6, BR7, BR12, AC24) writes AC-READ and AC-DENY through the decision-record library (GAP-3395, NEW-GAP-G6-1). How are access-log entries written? ACCESS-YAML publishes only `GET /admin/access-log`; the write is unpublished (GAP-3322; RR E1068-APP#2).

**Sources.** REG v2 RD-P1-072; RWB-P3-E1023-APP v3 lines 53, 67, 169, 227 (BR4), 341, 346, 410; RWB-PLT-E1037-CON v3 lines 235, 279, 287, 396, 406 (the access-log operation belongs to P4 through RWB-P4-E1039-CON; the audit fake records the case id, field id and flag and refuses a record that carries a value); DCPI v6 sheet Key ("Read audit … through PII Kafka"; "PII logging: the ACE Common audit and personal-data access log path (INT-34) to the SOC, separate from the rwb.<service>.events.v1 topics"); ACCESS-YAML `/admin/access-log`.

**Ruling.**
1. **One path.** Every read of personal data, and every refused access check, writes one access record through the **rwb-access access-log contract of RWB-P4-E1039-CON**, called by the reading service's `AccessClient` (platform library, RWB-PLT-E1037). Record: event `AC-READ` or `AC-DENY`, the caller's user or workload identity, `caseId` where there is one, the operation, the field IDs read and their `masked` flags, the instant; never a value. rwb-access stores it in its access log (read by `GET /admin/access-log`) and forwards the PII access record to the ACE Common PII path (INT-34) to the SOC.
2. **Not a decision record.** No access record is written through the decision-record library, published as `rwb.decision.DecisionRecorded.v1`, sent on any `rwb.<service>.events.v1` topic or appended to the interaction ledger. RWB-P4-E1023-APP BR6, BR7, BR12 and AC24, and RWB-P4-E1039-APP, -CON and -DB, are restated accordingly. AC-DENY is an access check, not a DP-03 decision.
3. **Failure.** A read whose access record cannot be written returns no data: 503 MSG-GEN-006 (RWB-P3-E1023-APP BR4; RD-P1-076 rule 6).
4. **Pending transport (GAP-3322).** The write operation, its payload and its transport are **Pending, owner rwb-access contract owner with the solution architect**. Interim: `AccessClient.record(accessRecord)` is an in-process port of the platform library; in tests and DEV it is backed by the audit fake of RWB-PLT-E1037-CON s12.8, which records the fields and refuses a record with a value; P1 and P3 stories assert the record through the fake. GAP-3395 is closed; GAP-3322 stays open, **blocks build: No** with this interim.

**Affected services.** rwb-access; rwb-source-data; rwb-case; gateway-bff; every service that reads personal data.
**Affected stories.** RWB-P4-E1023-APP, RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P3-E1023-APP, RWB-ITG-E1023-ITG, RWB-P4-E1037-CON, RWB-PLT-E1037-APP, RWB-PLT-E1037-CON, RWB-P1-E1068-APP, RWB-P1-E1016-APP, RWB-P1-E1069-APP, RWB-P1-E2010-CON.
**Affected documents.** API Specification v7 `rwb-access.yaml` (description of the access-log write as Pending GAP-3322); register RD-P1-072 (clarification line); Gap Register v3 (GAP-3395 closed; GAP-3322 non-blocking).
**Findings settled.** RWB-P1-E1068-APP#2 (document); RWB-P4-E1023-APP#3 residual.
**GAP/ASM.** Closes GAP-3395.
**Status.** Proposed – Claude Opus 5.5 (applied); transport pending under GAP-3322.
**Reuse note.** Access is logged through rwb-access; decisions are recorded through the decision-record library; never both for one read.
**Values chosen without a source.** Record field list (taken from the audit fake and the E1023 AC wording).

---

## RD-P1-092 · Retention run record, review list, age bases, record classes and the archive container

**Question.** No table stores the retention run record (GAP-3457, NEW-GAP-S5-8; RR E1017-APP#1). Where are the listed REVIEW keys held, and how does Compliance read them (RR E1017-APP#4)? Which `ageBasis` and `recordClass` values are accepted per REVIEW table (GAP-3454; RR E1017-APP#5)? Which archive container, identity and prefix (GAP-0490; RR E1017-OPS#1)?

**Sources.** YAML `RetentionRun` {status RUNNING/COMPLETED/FAILED, countsPerTable, archiveLocation, holdReport (GAP-3450)}, `RetentionTableCount`, `RetentionRule` (`ageBasis` "for interaction the only allowed value is case.closedAt"), `/retention-runs/{runId}` (Platform administration R); CASE-YAML `ClosureDate` {caseId, closedAt, accountKeys, personKeys}, `RetentionExclusion` {caseId, reason LEGAL_HOLD/OPEN, accountKeys, personKeys}; PS v9 `interaction.retention_class`; DCPI v6 Read me v6 (DF-EXT-050 `contact_point_ext.person_key`); REG v2 RD-P1-047, RD-P1-048; GR v3 GAP-0490 (Resolved (directive): path `retention/YYYY-MM-DD/<table>/`, manifest of row count and SHA-256 per file, the service's own credential, read back before any delete; container contract with RWB-PLT-TE012-APP), GAP-3279.

**Ruling.**
1. **Run record (GAP-3457).** RWB-P1-E1017-APP creates, in its own forward migration, table `retention_run` in `rwb_source_data`: `id uuid` (= runId), `run_date date`, `run_no integer`, `rule_version varchar(20)`, `status varchar(10)` (RUNNING, COMPLETED, FAILED), `started_at timestamptz`, `completed_at timestamptz` null, `archive_location varchar(400)` null, `counts_per_table jsonb` (array of `RetentionTableCount`), `hold_report jsonb`, and the standard columns; `uk_retention_run (run_date, run_no)`. The stored HTTP answer stays in the platform idempotency store (RD-P1-001). Dictionary rows come with the migration (next free DF-OPS IDs; RD-P1-071, RD-P1-096 rule 1). `recordRun` writes it; `GET /retention-runs/{runId}` reads it. From wave 4 `job_run` also carries the run for the job monitor; `retention_run` stays.
2. **Listed keys (E1017-APP#4).** Table `retention_review_item`: `id uuid`, `retention_run_id uuid` (FK to `retention_run`), `table_name varchar(30)`, `record_key varchar(255)`, `age_basis_at timestamptz`, and the standard columns; `uk_retention_review_item (retention_run_id, table_name, record_key)`. Compliance reads it through the new `GET /retention-runs/{runId}/review-items` (operationId `getRetentionRunReviewItems`; Platform administration R; `page` 0-based; `size` 1 to 200, default 50; answer {items[{tableName, recordKey, ageBasisAt}], page, size, total}; 404 MSG-P4-003 for an unknown run). Platform administration R is the read-only right that Compliance (RW-COMPLY) and audit hold.
3. **Age bases (GAP-3454).** Accepted `ageBasis` per table, each measured with the boundary-kept rule of RD-P1-048:
   - `interaction`, `dp_treatment`, `dp_guarantee_claim`: `case.closedAt` (join by `case_id` to `ClosureDate`);
   - `account_ext`: `account.lastClosedAt` – the latest `closedAt` of the `ClosureDate` items whose `accountKeys` hold the key, when no `RetentionExclusion` holds it;
   - `party_ext`, `contact_point_ext`: `person.lastClosedAt` – the same by `personKeys` (`contact_point_ext.person_key`, DF-EXT-050);
   - `valuation_ext`: no join key yet (GAP-3279, owner data architect); interim its rule is accepted, nothing is selected (`selected` 0, `listed` 0) and the run log names the reason.
   Any other value answers 422 MSG-GEN-007. GAP-3454 is closed except for valuation_ext (GAP-3279).
4. **Record classes.** For `interaction`, `recordClass` filters `retention_class`. The six REVIEW tables have no class column: their only accepted `recordClass` is `ALL`; any other value answers 422 MSG-GEN-007.
5. **Archive container (GAP-0490; E1017-OPS#1).** Path and manifest as GAP-0490: `retention/{runDate}/{tableName}/`, a manifest with the row count and SHA-256 per file, read back before any delete, written under the rwb-source-data workload identity. The container name per environment and a prefix-scoped write-once role for that identity are **Pending, owner solution architect with platform security**, NEW-GAP-E2 (container contract with RWB-PLT-TE012-APP). Interim: DEV and the pipeline test write to a local blob emulator container `rwb-source-data-retention` behind the `ArchiveStore` port; in SIT and later the ARCHIVE delete step stays behind the retention flag off (the REVIEW listing may run) until NEW-GAP-E2 is closed. No row is deleted without a write-once container.

**Affected services.** rwb-source-data; rwb-document (JOB-17 caller); rwb-case (closure and exclusion reads).
**Affected stories.** RWB-P1-E1017-APP, RWB-P1-E1017-CON, RWB-P1-E1017-OPS, RWB-P5-E1017-APP, RWB-PLT-TE012-APP, RWB-ITG-E1017-ITG.
**Affected documents.** Physical Schema v9 (two tables as the next forward versions); API Specification v7 `rwb-source-data.yaml` (`/retention-runs/{runId}/review-items`; `ageBasis` and `recordClass` descriptions; operation count, see RD-P1-094 and RD-P1-097); Service Contract Catalog v3; Temporal Workflow and Activity Catalog v3 (R23 `recordRun` target); Logical Data Model and Data Dictionary v11; Gap Register v3 (GAP-3457, GAP-3454 closed; NEW-GAP-E2).
**Findings settled.** RWB-P1-E1017-APP#1, #4, #5; RWB-P1-E1017-OPS#1 (re-review).
**GAP/ASM.** Closes GAP-3457 and GAP-3454 (valuation_ext stays with GAP-3279). New NEW-GAP-E2. GAP-0490 confirmed.
**Status.** Proposed – Claude Opus 5.5 (applied); container pending under NEW-GAP-E2.
**Reuse note.** A run with per-table counts has its own run table; REVIEW lists are rows, read through a paged read under the read-only admin right.
**Values chosen without a source.** Table and column names; operation path and id; `ageBasis` literals other than `case.closedAt`; `ALL`; emulator container name.

---

## RD-P1-093 · Migration cutover: provenance columns, pipeline authorisation, handover package and acceptance, clean days

**Question.** (a) DM stories read back `migration_source` and `migrated_at` through owner contracts that do not expose them (RR DM003-APP#1, DM004-APP#1, DM007-APP#1). (b) How is a cutover run started, with which rights, and who signs off? DM006 and DM007 check "Platform administration R", which is a read-only right. (c) The handover package layout and the owner's acceptance signal (RR DM006-APP#1, DM007-APP#2; GAP-2170, GAP-0529, GAP-3541). (d) How are ten clean days counted when a date has no reconciliation row?

**Sources.** REG v2 RD-P1-027 (standard columns on every migrated table), RD-P1-042 (clean day; MSG-P1-023), RD-P1-068 rule 7 (each package loaded by its target service identity), RD-P1-086 rule 1; RWB-P1-DM003-APP v3 lines 55, 58, 85, 93, 98, 103-108 (release-pipeline command; the handover is a file; sign-off in the cutover record; ASM-0717); RWB-P1-DM007-APP v3 lines 54, 77, 80, 83, 98-99 (ASM-3485); RWB-P1-DM006-APP v3 lines 77, 85, 102-105; EMS v6 MSG-P1-023.

**Ruling.**
1. **Provenance (one rule).** Owner contracts do not expose `migration_source` or `migrated_at`, and no DM story asserts them through an owner read. A DM story asserts them (i) on the rows it writes itself (`valuation_ext` for DM006; `contact_point_ext` and `interaction` for DM005) and (ii) on every row of its handover package files. The owner load and the RWB-ITG-DM0nn-ITG story assert them in the owner schema. DM003-APP AC3, BR6 and TC-DM-003-03, DM004-APP AC3 and BR4, DM007-APP AC1 and the owner-mock lines change accordingly.
2. **Entry mechanism and rights.** A cutover step is a **release-pipeline stage**, never a REST call or a Workbench screen action, so no Workbench capability is checked to start it. The stage runs under the workload identity of the service that reads or writes (P1 extract: `rwb_source_data`; owner load: the target service, RD-P1-068 rule 7), with one Idempotency-Key (UUID) per run recorded in the cutover record. Starting the stage needs the pipeline's protected-environment approval by the **release owner**; squad members (RW-TRIBE) build it and trigger it in DEV and the pipeline test only. The exception rows "a caller without Platform administration R … 403 MSG-P4-002 / 401 MSG-P4-001" (DM006 exception 6, DM007 X8, and AC3 and AC8 where they test it) become "a stage without the environment approval does not start; nothing is read".
3. **Sign-off.** The data steward (RW-DATASTEW) signs off through the pipeline's manual-approval step on the cutover record. The step first recomputes the clean-day count and, when it is below ten, fails with the MSG-P1-023 text and records no sign-off. Platform administration R (RW-AUDIT, RW-COMPLY and the other holders) only reads the cutover record and its evidence; it never starts a stage or signs off.
4. **Handover package and acceptance.** Each package is a folder of the cutover record, `<packageStory>/<cutoverBusinessDate>/<targetService>/`, holding one UTF-8 CSV per entity (header row; one column per section 11 field by `field_name`, plus `migration_source` and `migrated_at`) and `manifest.json` {packageStory, cutoverBusinessDate, targetService, idempotencyKey, files[{entity, rowCount, sha256}]}. The owner's load stage writes `acceptance.json` beside it: {packageStory, cutoverBusinessDate, targetService, status ACCEPTED | REFUSED, acceptedRowCount, refusedKeys[], loadedAt, loaderIdentity}. A package counts as handed over only with an ACCEPTED acceptance whose `acceptedRowCount` equals the manifest. There is no timeout: the cutover record stays open, and sign-off is impossible, until every owner of the story has ACCEPTED. DM003, DM004, DM006 (AC9, AC10, exception 8) and DM007 (AC10, AC12, X7) use this layout; the CSV column order is the section 11 order.
5. **Ten clean days.** Counting starts on the first bank business date after the last owner's ACCEPTED acceptance. A date is clean when it has REC-01 and REC-02 rows for every product group and the REC-05 row (RD-P1-086 rule 1), all PASS. A bank business date with any BREAK row, or with no row at all (run not finished, gate HOLD or allocation unreadable – RD-P1-042 writes no row then), is not clean and resets the count to zero; the date is listed with reason `BREAK` or `NO_RESULT`. Non-business days (DP14 holiday calendar) are skipped. The count is derived from the rows each time it is read, so a FAILED run that is rerun later and writes PASS rows makes that date clean on the next read.

**Affected services.** rwb-source-data; rwb-case, rwb-treatment, rwb-asset, rwb-litigation, rwb-comms, rwb-partner, rwb-decision, rwb-payment (owner loads).
**Affected stories.** RWB-P1-DM001-APP, RWB-P1-DM002-APP, RWB-P1-DM003-APP, RWB-P1-DM004-APP, RWB-P1-DM005-APP, RWB-P1-DM006-APP, RWB-P1-DM007-APP, RWB-P1-DM008-APP, RWB-P1-DM009-APP, RWB-P1-DM010-APP, RWB-P1-DM011-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P1-DM014-APP (rules 2 and 3 for every cutover story; rule 4 for the packaged ones DM003, DM004, DM006, DM007, DM008, DM009, DM010, DM013), RWB-ITG-DM003-ITG to RWB-ITG-DM013-ITG, RWB-P8-DM013-APP.
**Affected documents.** Data Migration Approach v5 (cutover stage, rights, package layout, clean-day rule); Users Roles and Permissions v6 (Platform administration R read-only note); Gap Register v3 (GAP-2170, GAP-0529, GAP-3541 closed; GAP-3275 unchanged).
**Findings settled.** RWB-P1-DM003-APP#1, RWB-P1-DM004-APP#1, RWB-P1-DM007-APP#1 (document); RWB-P1-DM006-APP#1, RWB-P1-DM007-APP#2 (story).
**GAP/ASM.** Closes GAP-2170, GAP-0529, GAP-3541. ASM-0717 and ASM-3485 confirmed.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A cutover runs in the pipeline under service identities, signs off in the pipeline, hands over by manifest and acceptance files, and counts clean days from result rows only.
**Values chosen without a source.** Folder and file names; manifest and acceptance members; reset on a missing row; reason codes.

---

## RD-P1-094 · Extension facts: first write, the read of the row and its ETag, access rule

**Question.** `PUT /extension-facts/parties/{personKey}` and `/accounts/{accountKey}` require If-Match (RD-P1-006), but the first write has no version (GAP-3555; RR E1018#3) and no GET returns a row or its ETag (GAP-3409). The roles and masking of the writes are open (GAP-3407).

**Sources.** REG v2 RD-P1-006 (`ETag: "<version>"`; 428 and 409 MSG-GEN-004); YAML lines 1318-1411 (the two PUT operations, `PartyExtFactsRecord`, `AccountExtFactsRecord`); DCPI v6 (DF-EXT-002 to DF-EXT-004 Sensitive, Restricted).

**Ruling.**
1. **First write (GAP-3555).** A write for a key with no row sends `If-None-Match: *` and no If-Match; the row is created and the answer is **201** with `ETag: "1"`. `If-None-Match: *` when a row exists → 409 MSG-GEN-004. Neither header → 428 MSG-GEN-004. An If-Match for a key with no row → 409 MSG-GEN-004. GAP-3555 is closed.
2. **Read (GAP-3409).** `GET /extension-facts/parties/{personKey}` (operationId `getExtensionFactsPartiesPersonkey`) and `GET /extension-facts/accounts/{accountKey}` (`getExtensionFactsAccountsAccountkey`) answer the record with its `ETag`; 404 MSG-P4-003 when no row exists; x-capability Case record R; built by RWB-P1-E1018-APP. A test obtains the ETag from this read or from the write answer. GAP-3409 is closed.
3. **Access rule (GAP-3407), interim.** The PUTs carry x-capability **Case record C**, checked from the token (no authorise call). The change is written to the access log (RD-P1-091) with the field IDs. Answers pass through FieldMasker (RD-P1-076: the three Sensitive booleans are masked unless a rule unmasks them). The permission letter, the owning screen story and the unmasking rule for the exclusion screen stay **Pending, owner product owner with compliance** (GAP-3407, **blocks build: No**); the FieldMasker fake carries an unmasking rule for the test role so that both branches are tested.

**Affected stories.** RWB-P1-E1018-APP, RWB-P1-E1069-APP, RWB-P4-E1037-CON.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (If-None-Match parameter, 201, two GET operations); Service Contract Catalog v3; Gap Register v3 (GAP-3555, GAP-3409 closed; GAP-3407 non-blocking); register RD-P1-006 (clarification line).
**Findings settled.** RWB-P1-E1018#3 (re-review).
**GAP/ASM.** Closes GAP-3555, GAP-3409.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Create with `If-None-Match: *`, update with `If-Match`; every updatable resource has a GET that returns its ETag.
**Values chosen without a source.** operationIds; 201 for the first write; the Case record C interim.

---

## RD-P1-095 · Data-product access: date of the access check, workload identities, field lists, catalog reconciliations

**Question.** RWB-P1-E1016-APP resolves `data_product_access` rows on "the business date in Asia/Bangkok", while RWB-P4-E1016-APP tests valid-from against "the case's business date" (GAP-3443; RR E1016-APP#11). How is a workload identity (the rwb-comms dispatch loop of RWB-P1-E2021-APP) authorised for the records read, which has role rows only (RR E1016-CON#8)? Which fields does each product serve, and how is an object without `account_key` or `person_key` restricted to the case (GAP-3445)? Where are the REC codes per product of the catalog stored (GAP-3446)?

**Sources.** PS v9 `data_product_access` (`uk_data_product_access (product_code, role_code, access_version)`, `valid_from`, `valid_to`), `sys_objects.data_product`, `sys_fields`; RWB-P1-E1016-APP line 106; RWB-P4-E1016-APP lines 84, 102, 116; YAML records read description; REG v2 RD-P1-064 (service rows "Case record C on rwb-source-data" for workload identities).

**Ruling.**
1. **One date (GAP-3443).** Access rows are in force on the **calendar date of the request instant in Asia/Bangkok** (`valid_from` ≤ that date, and `valid_to` null or ≥ that date): access is about now, not about the data date. P1 puts the date in the access resolution it presents with the authorise request (`resolvedOn`; the rest of the field set stays Pending under GAP-0983), and RWB-P4-E1016-APP step 9 and X5 test valid-from against `resolvedOn`. GAP-3443 is closed.
2. **Workload identities (E1016-CON#8).** A workload identity is authorised by its **service row**, the same row form RD-P1-064 uses for the ledger: Case record R on rwb-source-data for the service, plus one `data_product_access` row per product with `role_code` = the service row code. The service row codes are **Pending, owner rwb-access owner with the data steward**, NEW-GAP-E3; interim fixture codes sit in the rwb-access fake and the P1 seed of DEV only. The section 12.1 access column of RWB-P1-E1016-CON names the consumers: gateway-bff (users), rwb-comms (RWB-P1-E2021-APP dispatch loop, DP02), rwb-integration (RWB-P2-E1007-APP), and the readers of RWB-P1-E2010-APP through gateway-bff.
3. **Field list per product (GAP-3445).** The records read of product P serves the active `sys_fields` of the objects whose `sys_objects.data_product` = P and that the read path holds (the v_ace_* view or the P1 table). An object is restricted to the case by `account_key` or `person_key` (ACE views) or by `case_id` (Workbench tables); an object with none of them is not served by the records read. GAP-3445 is closed.
4. **Catalog reconciliations (GAP-3446).** No table holds REC codes per product. Interim: the catalog entry answers `reconciliations` as an empty list and AC15 asserts the empty list. Pending, owner data steward (GAP-3446, **blocks build: No**).

**Affected stories.** RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P4-E1016-APP, RWB-P1-E2021-APP, RWB-P2-E1007-APP, RWB-ITG-E1016-ITG.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (records read access note); Gap Register v3 (GAP-3443, GAP-3445 closed; GAP-3446 non-blocking; NEW-GAP-E3).
**Findings settled.** RWB-P1-E1016-APP#11, RWB-P1-E1016-CON#8 (re-review).
**GAP/ASM.** Closes GAP-3443, GAP-3445. New NEW-GAP-E3.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Validity dates of access rows are calendar dates of the request; services are authorised by service rows, never by borrowing a user role.
**Values chosen without a source.** Calendar-date rule; `resolvedOn`; the empty-list interim.

---

## RD-P1-096 · Dictionary and contract rows: object rows, DC-ACE seed, smoke records, reference-load handler, applied version

**Question.** Who writes new `sys_objects` rows when the E1064 governed load refuses a field of an unknown object (RD-P1-071; RR E1064-APP#3)? Who writes the DC-ACE version 1 DRAFT row (RR E1064-APP#1)? Which synthetic records does the E1064 smoke run use (RR E1064-OPS#1; GAP-3471)? How is the P3 reference-load handler built while its contract is unpublished (GAP-3338; RR E1064-APP#2, E1064-CON#2)? Which column holds the applied reference version (GAP-3403)?

**Sources.** PS v9 `rwb_source_data.sql` (lines 2436 onwards, "Dictionary rows added by later story migrations", for example `job_run`), `data_contract` (lines 205-218: `contract_code`, `source_system`, `interface_id` NOT NULL varchar(40), `contract_version`, `status` default DRAFT); RWB-P1-E1064-APP lines 58, 96-101, 139-140; RWB-P1-E1064-OPS lines 70, 310; REG v2 RD-P1-020 D and G, RD-P1-071, RD-P1-045 (a seed fails on an existing key); EMS v6 MSG-P1-021.

**Ruling.**
1. **Object rows (amends RD-P1-020 D).** The `sys_objects` and `sys_fields` rows of a new table are written by the same forward migration that creates the table (the PS v9 pattern), not by the E1064 governed load. The governed load changes field rows and adds fields of existing objects only; a field of an object absent from `sys_objects` is refused with MSG-P1-005 (RD-P1-071). RWB-P1-E1064-APP adds that AC; RWB-P1-AD018-APP's "through the governed load of RWB-P1-E1064-APP" reads "in its own migration".
2. **DC-ACE seed.** A forward data migration of RWB-P1-E1064-APP inserts the `data_contract` row (`contract_code` DC-ACE, `source_system` ACE, `interface_id` per GAP-3469 – interim `ACE-VIEW-CONTRACT`, `contract_version` 1, `status` DRAFT, no confirmation) in every environment; it fails on an existing key. Its AC asserts the row.
3. **Smoke records (GAP-3471).** In SIT and UAT the smoke run writes nothing: it reads the dictionary and the contracts, sends a PATCH with a stale If-Match (expects 409 MSG-GEN-004, nothing written) and publishes the unconfirmed DC-ACE (expects the MSG-P1-021 refusal, nothing written). The write smoke with a synthetic field and contract runs in DEV only. The smoke identity with Reference data U stays Pending, owner QA lead (GAP-3471, **blocks build: No**).
4. **Reference-load handler (GAP-3338).** Interim: P1 builds `ReferenceLoadApplyHandler` in process (RWB-P1-E1001-APP for `data_product`, `data_product_access` and `data_product_source`; RWB-P1-E1064-APP for dictionary rows), with table code = the table name, idempotent on (table code, version). Its tests drive it with the payload of the RWB-P3-E1043-CON fake; it is not integrated with rwb-case until the transport is published. The 12.8 handler stubs of E1064-APP and E1064-CON are taken from that fake. GAP-3338 stays open, owner solution architect with the rwb-case service owner, **blocks build: No**.
5. **Applied version (GAP-3403).** A forward migration of RWB-P1-E1001-APP adds the nullable column `applied_reference_version integer` to `data_product`, `data_product_access` and `data_product_source` (next free DF-REF IDs after DF-REF-302); the handler skips a load whose version is not greater. GAP-3403 is closed.

**Affected stories.** RWB-P1-E1064-APP, RWB-P1-E1064-CON, RWB-P1-E1064-OPS, RWB-P1-E1001-APP, RWB-P1-AD018-APP, RWB-P3-E1043-CON, RWB-ITG-E1064-ITG.
**Affected documents.** Physical Schema v9 (the new column as a forward version); register RD-P1-020 (amendment line); Gap Register v3 (GAP-3403 closed; GAP-3338, GAP-3471 and GAP-3469 non-blocking).
**Findings settled.** RWB-P1-E1064-APP#1, #2, #3; RWB-P1-E1064-CON#2; RWB-P1-E1064-OPS#1 (re-review).
**GAP/ASM.** Closes GAP-3403.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A table and its dictionary rows ship in one migration; smoke runs in shared environments prove refusals, not writes.
**Values chosen without a source.** Interim `interface_id`; column name; handler name.

---

## RD-P1-097 · Account-page read used by rwb-case for the case list

**Question.** X-27 put the account-page read of rwb-case in RWB-P1-E1015-CON, built by RWB-P1-E1002-APP; its path, page limit, wire names, right and errors are open (GAP-3274, GAP-3438).

**Sources.** REG v2 X-27, RD-P1-024 item 3, RD-P1-060 (single-account `GET /accounts/{accountKey}`, `Account` schema); YAML (`size` maximum 200 on P1 pages); DCPI v6 Read me v6 ("Redact query-string keys").

**Ruling.** `GET /accounts` with the repeated query parameter `accountKey` (1 to 200 values; more → 422 MSG-GEN-002; none → 400 MSG-GEN-001); operationId `getAccounts`; x-capability Case record R; caller the rwb-case workload identity only. Answer `AccountPage` {items: `Account`[] in the order of the request, missingKeys: string[], freshness: the DP01 `DataProductFreshness`}; a key with no row is listed in `missingKeys`, never answered 404. Errors 400 MSG-GEN-001, 401 MSG-P4-001, 403 MSG-P4-002, 422 MSG-GEN-002, 503 MSG-GEN-006. Query-string keys are redacted in logs. Published in RWB-P1-E1015-CON, built by RWB-P1-E1002-APP, deployed by RWB-P1-E1002-OPS; the YAML line "Pending: account-page read path …" is removed. GAP-3274 and GAP-3438 are closed.

**Affected stories.** RWB-P1-E1002-APP, RWB-P1-E1002-OPS, RWB-P1-E1015-CON, RWB-P3-E1002-APP.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (path and schema); Service Contract Catalog v3; Gap Register v3.
**GAP/ASM.** Closes GAP-3274, GAP-3438.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A multi-key read is a GET with repeated keys, the page maximum as the key limit, and the missing keys listed.
**Values chosen without a source.** Path form, operationId, `missingKeys`, the 200-key limit.

**Operation count after batch E.** `rwb-source-data.yaml` `x-service.operations` goes from 32 to 36: `GET /retention-runs/{runId}/review-items` (RD-P1-092), the two extension-facts GETs (RD-P1-094) and `GET /accounts` (RD-P1-097).

---

## RD-P1-098 · Sandbox contract files and bootstrap: interim build

**Question.** The sandbox contract files and build identities are open (GAP-3481 to GAP-3486; RR E1065-CON#1).

**Sources.** REG v2 RD-P1-046, RD-P1-073; RWB-P1-E1065-APP s7-s8 (shape table); RWB-P1-E1065-CON s11, s12.8.

**Ruling (interims; each gap stays open with its owner, blocks build: No).**
1. **GAP-3481 (files).** RWB-P1-E1065-CON s11 publishes, for `seed-profile.json`, `case-seed-list.csv` and `shape-table.csv`, a column and key table generated from the files the build produces now: every key present is required; its type is the generated JSON or CSV type; the `shape_id` values are the 11 rows of RWB-P1-E1065-APP s7-s8 and the `product_group` codes are those used there. Build report: JSON. Checksum: SHA-256 over the file bytes as written (UTF-8, LF), every column included. The contract test of AC2 compares a build with this table.
2. **GAP-3482 (list read).** The build reads `GET /admin/lists/{listCode}` from the rwb-case contract fake (RD-P1-011) in DEV and the pipeline test; the real read waits for the build identity.
3. **GAP-3483 (target gate).** Pipeline parameter `sandboxTarget`; the allow-list of hosts is the pipeline variable group of DEV and the pipeline test; any other host fails the build before a connection is opened.
4. **GAP-3484 (bootstrap).** In DEV and the pipeline test one bootstrap principal of the environment (the pipeline's DEV database administrator login) runs CREATE DATABASE `rwb_sandbox`, the `recovery` views, the grants on `public` and `recovery`, the role creation and ALTER VIEW OWNER as a step before Flyway, and acts as the sandbox build identity of RD-P1-089 rule 4. Outside those two environments the principal is the ACE DBA's (Pending).
5. **GAP-3485.** Unchanged (already blocks build: No).
6. **GAP-3486.** `rwb_sandbox_read` is a NOLOGIN group role with SELECT on the sandbox schemas; individual DEV logins are granted membership; the Entra group mapping waits, and the human extraction test is out of Done until it is mapped.

**Affected stories.** RWB-P1-E1065-CON, RWB-P1-E1065-APP, RWB-P1-E1065-DB, RWB-P1-E1069-DB, RWB-ITG-E1065-ITG.
**Affected documents.** Gap Register v3 (GAP-3481, GAP-3482, GAP-3483, GAP-3484 and GAP-3486 set to blocks build: No with these interims).
**Findings settled.** RWB-P1-E1065-CON#1 (re-review).
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** A sandbox interim never reaches beyond DEV and the pipeline test.
**Values chosen without a source.** Parameter name; the bootstrap step; the NOLOGIN role.

---

## RD-P1-099 · ACE additions: foreign-key delete rules, orphan rows and load order (interim)

**Question.** RWB-P1-ACE001-DB AC15 states the D-RCV-35 account cascade; the ON DELETE of the other foreign keys (hearing to lawsuit, npa_sale to npa_asset, three tables to asset, party_product to customer), the orphan rejection and the load order are Pending (GAP-3576; RR ACE001-DB#4).

**Sources.** RWB-P1-ACE001-DB v3 lines 220-229, 452; ACE Field Gap List v2 sheet ACE additions (Key column); D-RCV-35 (account cascade); PS v9 (own foreign keys use ON DELETE RESTRICT).

**Ruling (interim; GAP-3576 stays open for confirmation by the ACE team lead, blocks build: No).**
1. `hearing` → `lawsuit`: ON DELETE CASCADE, so that the D-RCV-35 account delete that cascades to `lawsuit` completes; the Given of AC15 adds hearing rows and its Then asserts that they are deleted.
2. Every other new foreign key (`npa_sale` → `npa_asset`, the three tables → `asset`, `party_product` → `customer`): ON DELETE RESTRICT.
3. An ingested row whose parent key is absent is rejected alone (not the whole file) and written to the ingestion job's reject log with its key; AC14 asserts that the row is not stored and the rest of the file is.
4. Load order of the ingestion jobs: parents before children – `customer`, `account`, `asset`, `npa_asset`, `lawsuit`, then their children.

**Affected stories.** RWB-P1-ACE001-DB, RWB-P1-E1069-DB.
**Affected documents.** ACE Field Gap List v2 (note); Gap Register v3 (GAP-3576 interim).
**Findings settled.** RWB-P1-ACE001-DB#4 (re-review).
**Status.** Proposed – Claude Opus 5.5 (applied); confirmation by the ACE team lead pending.
**Reuse note.** New ACE keys restrict deletes, except where an existing cascade must keep working.
**Values chosen without a source.** All four rules (interim).

---

## RD-P1-100 · Smaller rulings: snapshot(page), SCR-44 route, holder pair, delivery status name, EFS rows, complaints, DM012 to DM014

**Ruling.**
1. **`snapshot(page)` (RR E1013-APP#2; GAP-3425, GAP-3384).** P9 has not published the activity, its dated fields, sort, cursor or page size. RWB-P1-E1013-APP takes `snapshot(page)` and AC6 out of its Done; the activity is added by a later change of the story once RWB-P9-E1013-CON publishes it. Pending, owner P1 contract owner with the rwb-reporting owner (GAP-3425, blocks build: No).
2. **SCR-44 route (RR AD018-OPS#1; GAP-0516, ASM-0708).** The gateway-bff composite route is not published; route registration and AC13 leave the RWB-P1-AD018-OPS release and are not a release stop. Pending, owner gateway-bff contract owner (RWB-PLT-N001-CON), GAP-0516.
3. **Holder pair (RR E2034-APP#1).** `toHolderRef` is required on CASE_ALLOCATED (`fromHolderRef` optional); both are required on CASE_TRANSFERRED; both are optional on HANDOVER; on any other event code a holder field answers 422 MSG-GEN-007 naming the field (RD-P1-009 rows 02 and 03). RWB-P1-E2034-APP X4, BR2, step 4 and the ACs, the YAML description and the append of RWB-P3-E2034-APP align.
4. **Delivery status name (RR E1068-APP#1, document; GAP-3477).** The property is `latestDeliveryStatus` (RD-P1-064). Derivation per `externalRef`: the `deliveryStatus` of the entry with the latest `occurredAt`, ties broken by the highest `caseSeq`. `barcodeStatus` is removed from the YAML; RWB-P1-E1068-APP adds the AC.
5. **EfsHistoryRow (RR E2001-APP#1, document).** Every `EfsHistoryRow` property except `efsRecordKey`, `idempotencyKey` and `contactAt` is nullable in the YAML, and the fake is re-published (follows the story; no new rule).
6. **EFS ledger filter (GAP-3375).** P1 owns `efs_ledger_outcome` (DL29), so `GET /efs-history` applies the filter and answers only the rows that are to be appended; the P2 hand-over run appends every row it is given (RD-P1-067). The filter content stays with DL29, owner data architect with the solution architect (GAP-3375, blocks build: No).
7. **Complaints (GAP-3327).** RD-P1-064 keeps complaints Pending; X1 and AC5 of RWB-P10-E1062-APP leave its Done until GAP-3327 is closed.
8. **DM012 (RR DM012-APP#1).** The legacy hash, rule and version fields travel only in the extract file and the cutover evidence until GAP-3547 (NEW-GAP-S13-4) is closed (RD-P1-068 rule 1); AC1, BR2 and s11 say so.
9. **DM013 (RR DM013-APP#1, #2).** No source names the column that matches a Workbench write-off decision to a GL write-off: **Pending, owner rwb-writeoff owner with the data owner**, NEW-GAP-E4. Interim: RWB-P1-DM013-APP migrates the decisions without the write-off resolution and stamp, and its fixture drops them. The selection per part is the story's: the open matches of proceeds, the cases closed in the migration window and the write-off decisions of those cases.
10. **DM014 (RR DM014-APP#1, #2).** The comparison uses only what `GET /admin/lists/{listCode}` answers (version number, valid-from, rows), with the count and hash computed by P1. The scope is the seven rows of section 9.4 of RWB-DM-014; the rows rwb-case does not answer stay Pending under GAP-0238.

**Affected stories.** RWB-P1-E1013-APP, RWB-P9-E1013-CON, RWB-P1-AD018-OPS, RWB-PLT-N001-CON, RWB-P1-E2034-APP, RWB-P3-E2034-APP, RWB-P1-E1068-APP, RWB-P1-E2001-APP, RWB-P2-E2001-APP, RWB-P10-E1062-APP, RWB-P1-DM012-APP, RWB-P1-DM013-APP, RWB-P8-DM013-APP, RWB-P1-DM014-APP.
**Affected documents.** API Specification v7 `rwb-source-data.yaml` (`latestDeliveryStatus`, `EfsHistoryRow` nullability, holder description); Gap Register v3 (NEW-GAP-E4).
**GAP/ASM.** New NEW-GAP-E4. GAP-3425, GAP-0516, GAP-3375, GAP-3327 and GAP-0238 stay open, non-blocking with these interims.
**Status.** Proposed – Claude Opus 5.5 (applied).
**Reuse note.** Out of Done with a pending item is better than a guessed contract.
**Values chosen without a source.** The derivation tie-break; the DM013 interim.

---

## Verdicts on the re-review Blocker rows owned by a story or document (no ruling needed)

| Row | Verdict |
|---|---|
| RWB-P1-ACE001-DB#1 | Story: take the extra-column rule, type and length from sheet ACE additions. |
| RWB-P1-DM001-APP#1, #2 | Story: rewrite on the published `Account` schema (RD-P1-060); no gate; 200 with DP01 freshness STALE (RD-P1-062). |
| RWB-P1-DM009-APP#1 | Story: add `case_account` to the dump read (read, not carried); the account's case is its `case_account` row with `linked_to` null, the primary row first. |
| RWB-P1-E1016-CON#1 | Story: regenerate section 11 from the Physical Schema v9 seed (RD-P1-075) and add an automated comparison. |
| RWB-P1-E1018#1 | Story: `totalBalance` BigDecimal scale 2, nullable; the currency unit stays with GAP-3405. |
| RWB-P1-E2010-APP#2, RWB-P1-E2010-OPS#1 | Story: the DP04 tables are created by RWB-P1-E1001-APP (PS v9); E2010 only writes them; add the dependency. |
| RWB-P1-E1064-CON#1 (document) | Document owner (API contract): add enums, maxLength, required flags, ETag headers and the 422 to the YAML. |

## Register amendments to add (applied in register v3)

- RD-P1-002: child start policies of `ReconciliationWorkflow` and `Stage2ProductWorkflow`; `AceLateCheckStart` – RD-P1-078.
- RD-P1-004: one exception, `GET /batch-status` with no row → 404 MSG-P1-001 – RD-P1-085.
- RD-P1-006: first write with `If-None-Match: *`; GET of the extension facts – RD-P1-094 (clarification).
- RD-P1-007: `appendMigrated` cutover entry point – RD-P1-090 (clarification).
- RD-P1-020 D: dictionary rows of a new table come with its migration – RD-P1-096 rule 1.
- RD-P1-025: baseline copied from Physical Schema v9; `is_personal` per RD-P1-076 – RD-P1-075.
- RD-P1-040: child starts and Schedule starts (RD-P1-078); XD-11 confirmed with its mechanism and the TWAC R18 text (RD-P1-079).
- RD-P1-041: item 4 time trigger for DAILY and WEEKLY only; item 7 single stamp component with `stampDp04` for DP04; GAP-0511 line (RD-P1-081); AceDataLate status null and in-place re-completion (RD-P1-083).
- RD-P1-043: the ready call starts no run while the flag is off – RD-P1-080.
- RD-P1-045: item 4 first-release rollback answers – RD-P1-080.
- RD-P1-060: rule 2 masking default by classification – RD-P1-076; rule 3 phone and email for rwb-comms – RD-P1-077.
- RD-P1-065: rule 3 read with RD-P1-079.
- RD-P1-068: rule 6 DP04 stamped by `stampDp04` after the build – RD-P1-081.
- RD-P1-072: access-log path – RD-P1-091 (clarification).
- RD-P1-073: protection and rebuild mechanism – RD-P1-089 (clarification).

## New gap rows (temporary IDs, next free GAP numbers after GAP-3580)

| Temp ID | Subject | Owner | Decision |
|---|---|---|---|
| NEW-GAP-E1 | Data Classification rows for the 27 dictionary fields absent from DCPI v6 (DF-INT-030, DF-REF-274 to DF-REF-299) | Data protection officer | RD-P1-076 |
| NEW-GAP-E2 | Retention archive container per environment and the prefix-scoped write-once role of the rwb-source-data workload identity | Solution architect with platform security | RD-P1-092 |
| NEW-GAP-E3 | Service row codes of workload identities used as `role_code` in `data_product_access` | rwb-access owner with the data steward | RD-P1-095 |
| NEW-GAP-E4 | Column that matches a Workbench write-off decision to a GL write-off in the DM013 migration | rwb-writeoff owner with the data owner | RD-P1-100 |
| NEW-GAP-E5 | Confirmation of the classification-keyed masking default (Restricted masked without a rule; Confidential and Internal returned within scope) | Data protection officer | RD-P1-076 |

## Gap register dispositions

- **Closed:** GAP-0512, GAP-0529, GAP-0579, GAP-2170, GAP-3274, GAP-3288, GAP-3390, GAP-3395, GAP-3403, GAP-3409, GAP-3412, GAP-3430, GAP-3434, GAP-3438, GAP-3443, GAP-3445, GAP-3454 (valuation_ext stays with GAP-3279), GAP-3457, GAP-3487, GAP-3489, GAP-3492, GAP-3493, GAP-3494, GAP-3496, GAP-3506, GAP-3523, GAP-3525, GAP-3528, GAP-3529, GAP-3541, GAP-3555.
- **Kept open, blocks build changed to No with the stated interim:** GAP-3322, GAP-3327, GAP-3338, GAP-3375, GAP-3407, GAP-3411, GAP-3418, GAP-3421, GAP-3422, GAP-3429, GAP-3446, GAP-3471, GAP-3481, GAP-3482, GAP-3483, GAP-3484, GAP-3486, GAP-3524 (narrowed to the active states), GAP-3571, GAP-3576.
- **Widened:** GAP-3283 (PHONE and EMAIL for rwb-comms). **Confirmed:** GAP-0490, GAP-0597.
