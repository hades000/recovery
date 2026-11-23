# Edit log B-ITG-W2-01

WP B-ITG-W2-01 (RWB-ITG-W2: legacy RWB-E2-001, RWB-E2-002, RWB-E2-003, RWB-E2-004, RWB-E2-005). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2001 ITG EFS hand-over with full history - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2002 ITG ACE plan status on the case - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2003 ITG Customer's other products on the case - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2004 ITG Treatment entity and plan timers data model - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2005 ITG Decision log query API for audit - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2001-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2002-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2003-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2004-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2005-ITG.json`
- `_work/msr/gaps/B-ITG-W2-01.jsonl`
- `_work/msr/assumptions/B-ITG-W2-01.jsonl`
- `_work/msr/editlog/B-ITG-W2-01.md`

## Method

- Read first: the WP, Template and Rules v1 in full (R4 naming, R5.4 dependency classes, R5.5 DP table, R5.7 Day-1, R7 template and section rules, R8.1 header, R9 formats), the Ownership Map, the Architecture v5 and Temporal and Drools text extracts, the five legacy Epic 2 stories, and the thin-story extracts (Program and Epic 1/Epic 2 BRDs, Epics 3 to 8 Specification, Business Rules and Routing Logic) for values the legacy stories do not carry.
- Fanout 5: one task subagent per legacy key (RWB-E2-001, RWB-E2-002, RWB-E2-003, RWB-E2-004, RWB-E2-005), all five dispatched in one message. Each wrote only its own story file, its own fragment and its own candidate rows in the two shared registers under its own CG/ASM id. E2003 was re-dispatched once after a provider rate limit and completed its own three paths; no file was overwritten and no register row was written twice.
- Register appends were serialised through a lock file by a small helper, so the five-parallel fanout wrote five gap rows and five assumption rows with no interleaved or lost line; both registers parse line by line.
- AC policy: E2001 owns legacy AC1, AC3, AC5 and AC6 in the plan, so its story copies those four scenarios word for word, keeps the legacy Feature and Background lines, and tags the origin on each Scenario line; its AC9 to AC12 are new criteria for the harness seams only. E2002, E2003, E2004 and E2005 own no legacy AC in the plan, so each writes only new criteria tagged (new, D-RCV-60) that test the cross-service deliverable in its title, using the legacy values and never a new business value. The legacy criteria stay with the owning app stories and are named as such in each story.
- TCs: every legacy test case in the WP line is carried as an ITG copy with the -ITG suffix in the WP order, with the Level column added and the legacy Covers and Data kept (the seam added as an ITG AC reference); E2001 adds TC-ITG-E2001-01 to -04 for its four new criteria.
- Sections 12.1 to 12.9 are present in every story; 12.1, 12.3 and 12.7 are "None" in all five (the harness serves no operation, publishes no event and owns no table) and 12.5 and 12.6 are "None" or a watched workflow or schedule where the owner has one. Every table, operation, event, job, workflow, topic, queue and schema in section 12 comes from the WP naming rule or the Ownership Map.
- Section 13 carries one DP row per pattern in the WP line (10, 12, 7, 13 and 10 rows) with the R5.5 text and dependency, and states per story that the platform H and C dependencies those patterns add are held by the service and platform stories and are not repeated in the metadata H and C columns, which stay None.
- Realignment facts carried into the five stories: DP-18 puts the interaction ledger, the EFS ledger outcome list and the reconciliation results on rwb-source-data (the legacy E2-001 put the append on P7); DP-10 replaces the Quartz jobs and the TimerScheduler with the Temporal workflow kit and retires the EV-18 TimerDue Kafka event per the Ownership Map ruling; DP-17 retires the data-lake copy of the decision log (RWB-E1-014) so the E2005 export streams from rwb-decision; DP-13 gives the rwb-integration and rwb-decision bases; DP-19 makes each screen read a gateway-bff composite route.
- No issue-tracker reference, no person name, no e-mail address, no monolith API base outside an as-built section, and no service short outside the 19.

## Counts

| Item | Count | Detail |
|---|---|---|
| Stories | 5 | one per legacy key; 19 sections, 20 metadata rows and the R8.1 header each |
| Fragments | 5 | the WP step-8 key set; `prd_ref` Pending (C1); H, C and X empty as the WP line gives them |
| Acceptance criteria | 42 | 4 legacy ACs copied verbatim with the origin tag; 38 new integration ACs tagged (new, D-RCV-60) |
| Test cases | 60 | 56 legacy TC copies with the -ITG suffix and the Level column; 4 new TCs for the new criteria of E2001 |
| Candidate gap rows | 5 | GAP-0388, -E2002-1, -E2003-1, -E2004-1, -E2005-1 |
| Candidate assumption rows | 5 | ASM-0563 to -E2005-1 |

## Registers

- Candidate gap rows: 5. One combined row per story in the Template and Rules R9 gap key set: the harness repository and environments, its seeding, its per-run evidence format and retention, its pass/fail gate, and the gateway-bff composite route detail the story reads through. Type Missing, severity P2, needed by wave 2, owner role Integration lead.
- Candidate assumption rows: 5. One default row per story in the Template and Rules R9 assumption key set: SIT as the run of record, UAT for acceptance, seeding through the owning contracts, a per-run report keyed by story and business date, an all-green gate, and the composite route owned by RWB-PLT-N001-CON. Confidence Medium.
- Every missing value in the five story files cites its own pair in the `Not specified in the source documents (…; …)` form: GAP-0388 with ASM-0563, and the same pairing for E2002, E2003, E2004 and E2005. No other gap or assumption id is cited in the five story files or the five fragments. Step D1 numbers the rows.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-01 --quick`: C02, C03, C05, C12, C13 and C18 all PASS with zero findings.
- Additional local runs over the same twelve files: C06 (H and I classes), C07 (lane depth), C14, C15 (release unchange and tentative), C16 (service shorts and no monolith base), C17 (every cited CG and ASM id exists in a register row) and C20 (tool attribution) all PASS. The C10 and C11 findings of the run at this point name other legacy keys whose app stories are not written yet (Epic 1 and the other Epic 2 waves), and no finding names RWB-E2-001 to RWB-E2-005 outside the ACs the WP gives to the app stories.
- Structural review of the five story files: 19 headings in order, the 20 metadata rows in order, every Scenario line tagged, the four E2001 copies byte-identical to the legacy bodies, all nine 12.x tables present, the Pattern application table equal to the WP pattern list, every fragment carrying the 28 WP keys with values equal to the story metadata, and every legacy TC id of the WP line present as an -ITG copy.
