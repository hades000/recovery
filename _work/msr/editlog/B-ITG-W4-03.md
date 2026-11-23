# Edit log B-ITG-W4-03

WP B-ITG-W4-03 (RWB-ITG-W4: legacy RWB-DM-008, RWB-DM-009, RWB-DM-010, RWB-DM-011, RWB-DM-012). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM008 ITG Migrate partner performance - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM009 ITG Migrate debt sale - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM010 ITG Migrate documents and extracted fields - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM011 ITG Migrate scores and route economics - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM012 ITG Migrate decision log - integration v1.md`
- `_work/msr/fragments/RWB-ITG-DM008-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM009-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM010-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM011-ITG.json`
- `_work/msr/fragments/RWB-ITG-DM012-ITG.json`
- `_work/msr/gaps/B-ITG-W4-03.jsonl`
- `_work/msr/assumptions/B-ITG-W4-03.jsonl`
- `_work/msr/editlog/B-ITG-W4-03.md`

## Method

- Read the Template and Rules v1 fully first, then the WP, the Ownership Map (tables and api sections), the Architecture v5 text extract, the Temporal and Drools text extract, the five legacy data migration headings RWB-DM-008 to RWB-DM-012, and the accepted sibling RWB-ITG-DM003-ITG as the house-style exemplar.
- Fanout 5: one task subagent per legacy key, each writing only its own story file and fragment. DM008 and DM010 failed once on a socket reset before writing and were re-dispatched clean; DM009, DM011 and DM012 completed on the first pass.
- The parent reviewed all five stories against the legacy text and the Ownership Map, corrected the screen wording in DM008, DM009 and DM011 (the legacy stories name the SCR-45 Data quality console, which the harness does not build or read), removed the invented field-id range `DF-ACE-001 onward` from DM009 and DM010 in favour of an explicit no-BR-Field-ID row, and replaced the invented chain status label in DM012 section 9 with the condition the harness actually asserts.
- Registers: the parent assembled the two jsonl files from the workers' returned rows so that five concurrent appends could not corrupt them. DM009's worker reply was truncated before its rows, so its gap and assumption were written by the parent from that story's own missing-value citation, in the same §R9 shape as the other four.
- AC policy: DM008 owns legacy AC1 and AC2 verbatim; DM009, DM010, DM011 and DM012 own legacy AC2 verbatim, each tagged with its legacy origin. Every story adds 3 new criteria tagged (new, D-RCV-60) that test only the harness deliverable: the orphan break row with its reason and two owners, the no-copy or no-re-extraction assertion, the deterministic rerun, and the access refusal with MSG-P4-002. Legacy AC1 and AC3 stay with the P1 app stories and are named in section 19.
- TCs: every legacy TC is carried as an ITG copy with the -ITG suffix and the Level column; the Covers column names the legacy AC or test the copy derives from, and the cutover copy names the P1 app story that owns the cutover assertions.
- Patterns: DP05 (ACE data only through rwb-source-data), DP15 (per-service Flyway in the owner's schema) and DP19 (gateway-bff composite route where a screen exists) in every story, plus DP03 in DM012 (local decision-record library and the shared topic `rwb.decision-record.v1`). The platform H dependencies of DP15, DP19 and DP03 are recorded in section 13 and not repeated in the metadata H field, which stays empty as the plan requires.
- Section 12 is complete in every story: 12.1 and 12.7 are "None"; 12.3 and 12.4 are "None" because JOB-04 is triggered through the owner's rerun operation (DM012 states that `rwb.decision-record.v1` is the owner's DP-03 transport and that the harness reads no event); 12.5 exercises JOB-04 and, in DM012, reads JOB-14 without starting it; 12.8 holds the generated stubs and the two file fixtures. Every consumed operation is the owner's published operation, and every owner comes from the Ownership Map.
- The plan leaves `reqs` empty for these slices, so each fragment records `reqs: []`. Section 18 traces the legacy story, its ACs, its TCs, the data fields, the decisions, the DP patterns and the job map instead of inventing requirement ids.

## Registers

- Candidate gap rows: 5 (GAP-0448, GAP-0449, GAP-0450, GAP-0451, GAP-0452).
- Candidate assumption rows: 5 (ASM-0640, ASM-0641, ASM-0642, ASM-0643, ASM-0644).
- One combined gap row and one default assumption row per story, all type Missing, severity P2, needed_by_wave 4, owner_role Integration lead. Step D1 numbers them.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-03 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Additional local validation on the write-only files: C15 PASS (release dates unchanged and marked tentative), C16 PASS (every service short in a topic, path or queue is a known service), C17 PASS (every cited CG/ASM id has a jsonl row and every row has the required keys).
- C10 and C11 report no finding for RWB-DM-008 to RWB-DM-012; their remaining findings are other legacy keys whose WPs have not run yet and are outside this WP.
- Content self-check: 20 metadata rows in §R7.1 order and the exact values of the WP slice; 19 section headings in order; 12.1 to 12.9 present in every story; every Scenario line carries an origin tag; the owned legacy AC bodies are byte-equal to the legacy file after the tag; one CG/ASM pair cited per story and present in the registers; fragments parse as JSON with the 28 keys of the DM003 exemplar; no person name, no e-mail address, no tracker or wiki product name, and no old monolith API base outside an as-built section.
