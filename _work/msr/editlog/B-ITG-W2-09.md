# Edit log B-ITG-W2-09 — RWB-ITG-W2: legacy RWB-E3-017, RWB-E3-026, W2J01

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision: D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Run

- Agent: aisdlc-msr-worker, fanout 3 (one task subagent per legacy key: RWB-E3-017, RWB-E3-026, W2J01; WP allows 5). No merge — each subagent wrote its own story, fragment and jsonl rows.
- Source of the metadata values: the story line of each key in `_work/msr/wp/B-ITG-W2-09.md`, copied character for character.
- Legacy keys read: `04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md` headings RWB-E3-017 and RWB-E3-026. Only the owned AC of each key is copied verbatim (AC3 of each); AC1, AC2 and AC4 stay with RWB-S2-E3017-APP and RWB-S5-E3026-APP and are named as out of scope.
- AC3 of RWB-E3-017 and AC3 of RWB-E3-026 sit inside a gherkin block under a Background for the harness facts that the legacy story itself gives (account A-0001 with a zero balance, two active securities; the fixed run clock and the R-DIS-15 input values). The Scenario line and its Given/When/Then lines are the legacy text unchanged, with the origin tag appended.
- Release dates copied unchanged and marked "(tentative)": 31 January 2027 for both legacy keys. W2J01 is a new story with no release, so its row reads "None (new story)".
- Patterns applied, exactly the four the WP names for both legacy keys: DP03, DP05, DP13, DP19, each with its §R5.5 row in section 13. The platform H dependencies named by the DP table are not repeated in the metadata H row, which stays None. W2J01 has no pattern and its row reads None.
- Section 12 of every story follows §R7.2: tables 12.1 to 12.9, "None" where empty, every owner and every path taken from the Ownership Map (`POST /authorise` is the one operation the Architecture v5 slides 14 and 41 name for rwb-access). No `/api/recovery/v1/` base appears outside the DP-13 marker row, and no monolith base appears anywhere.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3017 ITG Release the collateral after settlement - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3026 ITG Re-appraise a held asset on cycle - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG W2J01 ITG Wave 2 journey end to end - integration v1.md
- _work/msr/fragments/RWB-ITG-E3017-ITG.json
- _work/msr/fragments/RWB-ITG-E3026-ITG.json
- _work/msr/fragments/RWB-ITG-W2J01-ITG.json
- _work/msr/gaps/B-ITG-W2-09.jsonl
- _work/msr/assumptions/B-ITG-W2-09.jsonl
- _work/msr/editlog/B-ITG-W2-09.md

| Story | File | ACs owned | TCs |
|---|---|---|---|
| RWB-ITG-E3017-ITG | RWB ITG E3017 ITG Release the collateral after settlement - integration v1.md | AC3 (legacy RWB-E3-017) | TC-E3-017-01-ITG to TC-E3-017-06-ITG |
| RWB-ITG-E3026-ITG | RWB ITG E3026 ITG Re-appraise a held asset on cycle - integration v1.md | AC3 (legacy RWB-E3-026) | TC-E3-026-01-ITG to TC-E3-026-06-ITG |
| RWB-ITG-W2J01-ITG | RWB ITG W2J01 ITG Wave 2 journey end to end - integration v1.md | AC1 to AC5 (new, D-RCV-60) | TC-W2J01-01-ITG to TC-W2J01-10-ITG |

## Gap and assumption rows

- Gap rows written to `_work/msr/gaps/B-ITG-W2-09.jsonl`: 3 (one combined row per story).
  - GAP-0426 — CCMS release interface, its confirmation fixture, the harness pack, the data product code for the account row, the screen ID of the case states, the feature flag key and the evidence format and retention (Missing, P2, wave 2).
  - GAP-0427 — fixed clock and JOB-19 window control, SVAF interface ID, file pattern and fixtures, the field ID of one_year_rule_applied, the harness environment and seeding, the evidence format and retention and the production switch (Missing, P2, wave 2).
  - GAP-0428 — wave 2 harness environment, repository, seeded identifiers, fixed business date outside the source examples, evidence format and retention, wave gate name and thresholds, gateway-bff composite route path and the S8 deviation read operation (Missing, P2, wave 2).
- Assumption rows written to `_work/msr/assumptions/B-ITG-W2-09.jsonl`: 3 (one per story, confidence Medium, confirming role named in the row).
  - ASM-0602, ASM-0603, ASM-0604.
- Counts: CG 3, ASM 3. No gap row numbers a GAP-nnnn and no assumption row numbers an ASM-nnnn; numbering is left to step D1.
- One correction after the fanout: the E3026 exception table now fails the run on AC3 when the SVAF order file reports FileFailed (was recorded as a separate observation), its reject path carries no message ID because the rule set gives none, the E3017 data table cites the outbound_item field IDs DF-OPS-169 to DF-OPS-175 instead of a placeholder, and the W2J01 gate test data names every wave 2 harness result instead of a count.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-09 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 metadata rows | PASS | 0 |
| C03 19 sections | PASS | 0 |
| C05 AC origin tags | PASS | 0 |
| C12 person names and emails | PASS | 0 |
| C13 issue tracker | PASS | 0 |
| C18 write-only and legacy hashes | PASS | 0 |

Also run on the same file set: C14 header lines PASS, C15 release and tentative PASS, C16 service names and API base PASS, C17 gap and assumption citations PASS, C19 as far as this WP's own planned output goes (all three story files, three fragments and this log exist), C20 tool line PASS. C11 (legacy test case coverage) and C19 in its whole-queue form report WARN and FAIL rows for other work packages whose stories are not written yet; no row of either names this WP and no legacy test case of RWB-E3-017 or RWB-E3-026 is reported missing.

No file outside the WP "Write only" list was written, and no existing file was edited.
