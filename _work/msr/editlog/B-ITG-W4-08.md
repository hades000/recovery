SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Edit log — WP B-ITG-W4-08 (realignment D-RCV-60)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent: aisdlc-msr-worker. Decision: D-RCV-60. Date: 22 November 2026.

## What the work package did

WP B-ITG-W4-08 is the RWB-ITG-W4 wave 4 integration set for five legacy keys: RWB-E7-014, RWB-E7-015, RWB-E7-016, RWB-E7-017 and RWB-E8-012. Fanout 5: one task subagent per legacy key, each writing only its own story file, its own fragment and its own two register rows; nothing was merged, and the parent wrote only this log and ran the checks.

Each story is the wave 4 integration harness for its feature and nothing else. The feature, the screen and the data stay with the owning service's CON and APP stories (RWB-S9-E7014-APP, RWB-S9-E7015-APP, RWB-S9-E7016-APP, RWB-S9-E7017-APP and RWB-P4-E8012-APP). Each file carries the 19 template headings in §R7.2 order, the 20 metadata rows of §R7.1 in order, the two §R8.1 header lines, a D-RCV-60 change-log row inside the file, the legacy AC1 copied word for word with its origin tag, four new criteria tagged (new, D-RCV-60), the legacy test cases copied with the -ITG suffix and the Level column, the DP rows of §R5.5 for every pattern in the slice, and §12.1 to §12.9 with the owner of every operation taken from the Ownership Map.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7014 ITG Issue a notice on a missed target - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7015 ITG End a partner contract and recall the work - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7016 ITG Check partner conduct - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7017 ITG Manage extra costs and services on an asset - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E8012 ITG Publish a panel change - integration v1.md
- _work/msr/fragments/RWB-ITG-E7014-ITG.json
- _work/msr/fragments/RWB-ITG-E7015-ITG.json
- _work/msr/fragments/RWB-ITG-E7016-ITG.json
- _work/msr/fragments/RWB-ITG-E7017-ITG.json
- _work/msr/fragments/RWB-ITG-E8012-ITG.json
- _work/msr/gaps/B-ITG-W4-08.jsonl
- _work/msr/assumptions/B-ITG-W4-08.jsonl
- _work/msr/editlog/B-ITG-W4-08.md

## Register rows

Gap rows: 5 in _work/msr/gaps/B-ITG-W4-08.jsonl, one per story, all type Missing and severity P2, needed by wave 4, owner role Integration lead: GAP-0475, GAP-0479, GAP-0476, GAP-0477, GAP-0478.

Assumption rows: 5 in _work/msr/assumptions/B-ITG-W4-08.jsonl, one per story, all confidence Medium, confirm at the wave 4 entry check with the integration lead and the QA lead: ASM-0667, ASM-0671, ASM-0668, ASM-0669, ASM-0670.

No row is numbered GAP-nnnn or ASM-nnnn here; numbering stays with step D1. Each placeholder in a story cites the candidate id it belongs to.

## What each gap and assumption covers

The five gaps are the same class of value: the harness environment and base hosts, the fixture layout and the synthetic keys, the stub answer shapes of the consumed contracts, the one hop that has no published operation (the conduct trigger, the contract-end action, the cost approval and the panel change), the evidence format and retention, and the pass or fail gate. No source in the §R7.3 fill order states any of them, and none of them is a business value, so each story carries one placeholder in §3, §12.8, §13 and §15 and one assumption that lets the work start on Day 1 against generated stubs, with a stub pass never reported as a real pass.

## Decisions taken while writing

- The legacy AC1 of every story is copied word for word, including its own Given, When and Then, because the WP asks for a verbatim copy; the harness assertions sit in the four new criteria beside it, and each story says in one sentence after the gherkin block that legacy AC2 stays with the owning APP story and is asserted here at the harness's own action.
- Patterns applied are copied from the slice: DP03, DP13 and DP19 for E7014, E7015 and E7016; DP03, DP05, DP13 and DP19 for E7017; DP03, DP06, DP13 and DP19 for E8012. The platform H dependencies the DP rows add (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON) are recorded in §13 and are not repeated in the metadata H field, which stays None, as the accepted wave 4 stories do; the only blocking dependency is the I story, so every story is Day 1.
- E8012 keeps the integration dependency RWB-P4-E8012-APP of the slice. Its feature sits in the P4 module, and the panel and fee schedule are versioned reference data under the default ruling that puts reference data with P3 rwb-case, so the harness publishes the change through the reference-load operation of P3 and the rule-version operations of P7, then proves the effect through the S9 partner read.
- E7017 reads the asset fields the legacy data section names through S5's asset contract and no ACE view (DP-05), and keeps valuation_ext with P1 out of the run.
- E7016 consumes rwb.decision.RulePackageInForce.v1 to pin the rule version in force, cited from Architecture v5 slide 43 row 30. E7017 leaves rwb.asset.AssetTakenOn.v1 out of the events consumed because the run starts with the asset already held.

## Fixes made in this work package

- C16 flagged one old monolith API base in the E7017 story, outside any as-built section. The §12.2 note was reworded to name the two legacy partner paths and the old base once, without the monolith path form, and the story now passes C16 with the rest.
- The two register files were rewritten once, byte for byte in content, to drop the UTF-8 byte-order mark the first append left at byte 0 and to restore the section sign in six citations of §R3, §R5.5, §R7, §R7.3 and §R9. Row ids and row content are otherwise unchanged, and all ten rows parse as UTF-8.

## Checks

python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-08 --quick: C02, C03, C05, C12, C13 and C18 all PASS with 0 findings.

The wider set run over the same 13 files also passes: C01, C06, C07, C11 (warn only, for legacy test cases of other work packages), C15, C16, C17 and C20 with 0 findings. C19 reports planned outputs of other work packages that have not run yet; every planned output of this work package exists.

## Open items for the assembler

- Twelve candidate ids in the two registers wait for step D1 to number and re-cite them.
- Every story is Draft (realignment v1) and Day 1; none needs a human approval to proceed, and no later lifecycle stage was started.
- No issue-tracker, Confluence, GitLab, Figma or web call was made, and no git commit was made.
