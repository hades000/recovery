# Edit log B-ITG-W4-02

WP B-ITG-W4-02 (RWB-ITG-W4: legacy RWB-DM-003, RWB-DM-004, RWB-DM-005, RWB-DM-006, RWB-DM-007). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM003 ITG Migrate case and ownership - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM004 ITG Migrate treatment and offers - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM005 ITG Migrate contact and promises - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM006 ITG Migrate collateral and assets - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM007 ITG Migrate legal events and cases - integration v1.md`
- `_work/msr/fragments/RWB-ITG-DM003-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM004-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM005-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM006-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM007-ITG.json`
- `_work/msr/gaps/B-ITG-W4-02.jsonl`
- `_work/msr/assumptions/B-ITG-W4-02.jsonl`
- `_work/msr/editlog/B-ITG-W4-02.md`

## Method

- Read the Template and Rules v1 fully first, then the WP, the Ownership Map, the Architecture v5 and Temporal and Drools text extracts, the five legacy data migration stories, the FSD P1 data product table and the Program BRD requirements REQ-RDF-007 and REQ-RDF-008.
- Fanout 5: one task subagent per legacy key (RWB-DM-003, RWB-DM-004, RWB-DM-005, RWB-DM-006, RWB-DM-007), each writing only its own story file and fragment. The parent reviewed the five files, corrected the P1-versus-owning-service cutover-load wording in the DM003, DM004 and DM006 stories, normalised the DM007 data table, removed the DP-10 citations that were outside the planned patterns in DM005, and assembled the two candidate registers and this edit log.
- AC policy: each story copies its owned legacy criteria verbatim with the origin tag (DM003, DM004 and DM006 own AC2; DM005 and DM007 own AC1 and AC2) and adds new criteria tagged (new, D-RCV-60) that test only the harness deliverable: the orphan break row with its reason and owners, the deterministic rerun, and the access refusal. No new criterion restates an app story's extraction or cutover behaviour.
- TCs: every legacy TC is carried as an ITG copy with the -ITG suffix and the Level column; the legacy AC each copy derives from is named in Covers, and the cutover copy names the app story that owns the cutover assertions.
- Patterns: every story applies DP05 (ACE data only through rwb-source-data), DP15 (per-service Flyway in the owner's schema) and DP19 (gateway-bff composite route where a screen exists; DM003 and DM005 record it for the wave's screen path only, because their legacy keys have no screen). The platform H dependencies of DP15 and DP19 are recorded in section 13 and not repeated in the metadata H field, which stays empty as the plan requires.
- Section 12 is complete in every story: 12.1 and 12.7 are "None"; 12.3 and 12.4 are "None" because JOB-04 is triggered through the owner's rerun operation; 12.5 exercises JOB-04 only; 12.8 holds the generated stubs and the two file fixtures.
- Registers: each story carries one combined gap row and one default assumption row, in the Template and Rules §R9 key formats, with the ids listed under Registers below. No other CG or ASM id is cited in the five stories or the five fragments.
- The plan leaves `reqs` empty for these slices, so each fragment records `reqs: []`. REQ-RDF-007 and REQ-RDF-008 appear only as the sources of the business rules they support in sections 2 and 8, and section 18 traces the legacy story, its ACs, its test cases, the data fields, the decisions and the DP patterns instead of inventing requirement ids.

## Registers

- Candidate gap rows: 5 (GAP-0443, GAP-0444, GAP-0445, GAP-0446, GAP-0447).
- Candidate assumption rows: 5 (ASM-0635, ASM-0636, ASM-0637, ASM-0638, ASM-0639).
- One combined gap row per story and one default assumption row per story. Step D1 numbers them.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-02 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Re-run after the content review fixes (the cutover-load wording in DM003, DM004 and DM006, the DM005 screen path, the DM006 pattern citations and the DM007 data table): same six PASS.
- Additional local validation: C15 PASS, C16 PASS and C17 PASS on the write-only files; metadata rows and values in order; 19 section headings in order; 12.1 to 12.9 present; every legacy AC body byte-equal to the legacy story after removing the origin tag; AC origin tags on every scenario line; one CG/ASM pair cited per story and present in the registers; fragment keys and lists; no tracker reference, no e-mail address, no person name, and no old monolith API base outside an as-built section.
