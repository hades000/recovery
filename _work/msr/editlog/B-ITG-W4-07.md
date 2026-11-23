# Edit log B-ITG-W4-07

WP B-ITG-W4-07 (RWB-ITG-W4: legacy RWB-E7-005, RWB-E7-006, RWB-E7-007, RWB-E7-012, RWB-E7-013). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7005 ITG Run X5 bankruptcy and seizure end to end - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7006 ITG Run X6 lost contact and skip trace end to end - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7007 ITG Run X7 collateral event end to end - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7012 ITG Approve partner fees - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7013 ITG Hold a partner review - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E7005-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7006-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7007-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7012-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7013-ITG.json`
- `_work/msr/gaps/B-ITG-W4-07.jsonl`
- `_work/msr/assumptions/B-ITG-W4-07.jsonl`
- `_work/msr/editlog/B-ITG-W4-07.md`

## Method

- Read the Template and Rules v1 fully first, then the WP, the Ownership Map, the Architecture v5 and Temporal and Drools extracts, the five legacy sections and the thin-story extracts in the §R7.3 fill order.
- Fanout 5: one task subagent (aisdlc-msr-worker) per legacy key, five at once in one message. Each wrote its own story file and its own fragment only. One fan dropped with a connection reset before writing anything; it was rerun once for RWB-E7-012 and completed. The WP owner then wrote the two jsonl registers (one combined gap row and one assumption row per story, cited by every story) and this log, so that five parallel writers never appended to one register file.
- Every story carries the 20 metadata rows of §R7.1 in order and the 19 sections of §R7.2 in order; `preserved` and `delta` are false for all five, so no legacy section is copied word for word and no as-built section is carried.
- Acceptance criteria: AC1 of each legacy key is copied verbatim with its origin tag (RWB-E7-005 AC1, RWB-E7-006 AC1, RWB-E7-007 AC1, RWB-E7-012 AC1, RWB-E7-013 AC1). All other criteria are new, tagged `(new, D-RCV-60)`, and test only the integration deliverable in the title. The legacy AC2, AC3 and AC4 of each key stay with its APP story, and the forced decision-record failure is asserted at the harness boundary in the new criteria.
- Test cases: the legacy TC IDs of each key are kept as `-ITG` copies, with the Level column added and the Covers column naming the legacy AC the copy derives from and the ITG AC it asserts. The older `-ITG` copy of a failure that the APP story owns is labelled as such, not as a legacy AC of this story.
- Patterns: the DP table of §R5.5 is applied for every pattern in the slice (DP03, DP13, DP19, plus DP05 on RWB-E7-007) and listed in "Patterns applied". The platform H dependencies the DP table adds (RWB-PLT-E1027-CON, RWB-PLT-N001-CON) belong to the platform waves and are not repeated in the metadata H field, which stays None on every story; the metadata I field carries exactly the I dependency of the slice.
- Contract: no operation, event, job, table or workflow is invented. Every consumed operation is one the Ownership Map publishes for its owner, on `/api/recovery/<short>/v1`; no story writes the monolith base. Where the map publishes no deviation read or clear, no fee-approval or invoice read, and no partner-review or scorecard read, the story says so and asserts the fact through the case, the timers, the decision log and the invoice submission outcome instead of inventing an endpoint.
- Dates: copied unchanged and marked "(tentative)".
- No issue-tracker, Confluence, GitLab, Figma or web call; no git commit; no person named; roles only.

## Gaps and assumptions

- Gap rows: 5, one combined row per story — `GAP-0470`, `GAP-0471`, `GAP-0472`, `GAP-0473`, `GAP-0474`. All type Missing, severity P2, needed by wave 4.
- Assumption rows: 5, one per default — `ASM-0662`, `ASM-0663`, `ASM-0664`, `ASM-0665`, `ASM-0666`. All confidence Medium, each linked to its gap.
- The missing values behind them: the SIT environment and base hosts, the fixture layout and synthetic keys, the stub answer shapes, the evidence format and retention, and the pass or fail gate for each harness; for E7-005 the receiver and LED fixture; for E7-006 the NCB, EFS and agency skip-trace answers; for E7-007 the insurance-claim answer shape and the re-appraisal read-back; for E7-012 the fee claim and schedule answer shape; for E7-013 the shape of the review evidence.
- No date is raised as a gap. No approval is asked for: everything missing is recorded as an assumption and every story stays in Draft status, per the D-RCV-60 overlay.

## Check

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-07 --quick` on 22 November 2026:

| Check | Result | Findings |
|---|---|---|
| C02 metadata rows | PASS | 0 |
| C03 the 19 sections | PASS | 0 |
| C05 AC origin tags | PASS | 0 |
| C12 no person name or email | PASS | 0 |
| C13 no issue-tracker reference | PASS | 0 |
| C18 write scope and untouched legacy files | PASS | 0 |

A targeted audit over the same files was also run for C06 and C07 (H and I dependencies), C14 and C20 (headers, tool line), C15 (release date and tentative mark), C16 (service names and no monolith base) and C17 (every CG and ASM citation resolves to a register row): all pass, and the exact operation and event lists in the five fragments match §12.2 and §12.4 of their stories one for one.

Four wording defects were found in review and fixed before the final run: the E7012 state table used state labels that are not in the instruction status LOV (replaced by SENT and DONE of DF-PRT-014 and the decision record for the approval), the E7013 state table used event codes that the rules do not define (replaced by `PartnerResultSubmitted` and the R-UNI event codes), the E7013 duplicate-submission test case was mislabelled as a legacy AC (relabelled to the APP story), and the E7005, E7006 and E7007 notes said "both topics" where the run subscribes to three or four (corrected). The rerun is clean.
