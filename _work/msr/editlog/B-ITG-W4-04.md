# Edit log B-ITG-W4-04

WP B-ITG-W4-04 (RWB-ITG-W4: legacy RWB-DM-013, RWB-E6-008, RWB-E6-017, RWB-E6-021, RWB-E6-025). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM013 ITG Migrate money and closure - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6008 ITG Derecognize and post to the general ledger - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6017 ITG Route the population to the committee and schedule it - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6021 ITG Post an approved write-off - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6025 ITG Close the case after the retention period - integration v1.md`
- `_work/msr/fragments/RWB-ITG-DM013-ITG.json`
- `_work/msr/fragments/RWB-ITG-E6008-ITG.json`
- `_work/msr/fragments/RWB-ITG-E6017-ITG.json`
- `_work/msr/fragments/RWB-ITG-E6021-ITG.json`
- `_work/msr/fragments/RWB-ITG-E6025-ITG.json`
- `_work/msr/gaps/B-ITG-W4-04.jsonl`
- `_work/msr/assumptions/B-ITG-W4-04.jsonl`
- `_work/msr/editlog/B-ITG-W4-04.md`

## Method

- Read the Template and Rules v1 fully first, then the WP, the Ownership Map, the Architecture v5 and Temporal and Drools extracts, the five legacy sections and the thin-story extracts. The finished sibling `RWB ITG DM003 ... - integration v1.md` set the shape, the depth and the voice.
- Fanout 5: one task subagent (aisdlc-msr-worker) per legacy key, five at once in one message. Each wrote its own story file and its own fragment only. The WP owner then wrote the two jsonl registers (one combined gap row and one assumption row per story, cited by every story) and this log, so that five parallel writers never appended to one register file.
- Every story carries the 20 metadata rows of §R7.1 in order and the 19 sections of §R7.2 in order; `preserved` and `delta` are false for all five, so no legacy section is copied word for word and no as-built section is carried.
- Acceptance criteria: the legacy ACs the slice owns are copied verbatim with their origin tag (DM013 AC2; E6-008 AC1, AC2, AC3; E6-021 AC1, AC3). All other criteria are new, tagged `(new, D-RCV-60)`, and test only the integration deliverable in the title. E6-017 and E6-025 own no legacy AC; their four legacy ACs stay with RWB-S7-E6017-APP and RWB-P3-E6017-APP, and RWB-S7-E6025-APP and RWB-P3-E6025-APP.
- Test cases: the legacy TC IDs of each key are kept as `-ITG` copies, with the Level column added and the Covers column naming both the legacy AC the copy derives from and the ITG AC it asserts.
- Patterns: the DP table of §R5.5 is applied for every pattern in the slice (DP03, DP05, DP13, DP15, DP19) and listed in "Patterns applied". The platform H dependencies the DP table adds (RWB-PLT-E1027-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) belong to the platform waves and are not repeated in the metadata H field, which stays empty on every story; the metadata I field carries exactly the I dependencies of the slice.
- Contract: no operation, event, job, table or workflow is invented. Every consumed operation is one the Ownership Map publishes for its owner, on `/api/recovery/<short>/v1`; no story writes the monolith base `/api/recovery/v1/`. Where the map publishes no read operation for a write-off record and no meeting-booking or retention operation, the story says so and asserts the fact through rwb-case, rwb-document, DP13 and the decision log instead of inventing an endpoint.
- Dates: copied unchanged and marked "(tentative)".
- No issue-tracker, Confluence, GitLab, Figma or web call; no git commit; no person named; roles only.

## Gaps and assumptions

- Gap rows: 5, one combined row per story — `GAP-0453`, `GAP-0454`, `GAP-0455`, `GAP-0456`, `GAP-0457`. All type Missing, severity P2, needed by wave 4.
- Assumption rows: 5, one per default — `ASM-0645`, `ASM-0646`, `ASM-0647`, `ASM-0648`, `ASM-0649`. All confidence Medium, each linked to its gap.
- The missing values behind them: the harness environment, fixture layout, break-list fields, evidence format and retention and the pass or fail gate for each key; the ALS and general ledger answer shape, the posting reference format, the rejection codes and the retry settings (E6-008, E6-021); the write-off committee queue code, the committee meeting calendar and the shape of the scan answer (E6-017); the retention period, which NFR-031 leaves Not set under DL26, the synthetic clock mechanism, the closure evidence shape and the document retention evidence (E6-025). The Ownership Map's lack of a write-off read operation and of a booking or retention operation is recorded in E6-017, E6-021 and E6-025.
- No date is raised as a gap. No approval is asked for: everything missing is recorded as an assumption and every story stays in Draft status, per the D-RCV-60 overlay.

## Check

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-04 --quick` on 22 November 2026:

| Check | Result | Findings |
|---|---|---|
| C02 metadata rows | PASS | 0 |
| C03 the 19 sections | PASS | 0 |
| C05 AC origin tags | PASS | 0 |
| C12 no person name or email | PASS | 0 |
| C13 no issue-tracker reference | PASS | 0 |
| C18 write scope and untouched legacy files | PASS | 0 |

One failure was found and fixed: the first version of this log named the issue tracker in its method list, which C13 refuses outside the one permitted impact file. The sentence now reads "No issue-tracker, Confluence, GitLab, Figma or web call". The rerun is clean.

C16 (service names and no monolith base), C17 (every CG and ASM citation resolves to a register row), C15 (release unchanged and marked tentative), C14, C20, C06 and C07 (dependencies and lane depth) were also run over the same files and pass with no findings.
