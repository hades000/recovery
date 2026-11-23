# Edit log B-ITG-W3-02 — RWB-ITG-W3: legacy RWB-E4-050, RWB-E5-002, RWB-E5-009, W3J01

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision: D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Run

- Agent: aisdlc-msr-worker, fanout 5 (the WP allows 5; 4 keys were fanned out, one task subagent per legacy key: RWB-E4-050, RWB-E5-002, RWB-E5-009 and the new key W3J01). No merge — each subagent wrote its own story, its own fragment and its own keyed jsonl rows, appending to the two shared registers.
- Source of the metadata values: the story line of each key in `_work/msr/wp/B-ITG-W3-02.md`, copied character for character. Every story is an ITG story of the integration service, lane `L-ITG-W3`, wave 3, ready Day 1, with an empty build list and an empty contract list; the integration dependencies are the ones the WP names and the external ones are empty.
- Legacy keys read: `04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md`, headings RWB-E4-050, RWB-E5-002 and RWB-E5-009. W3J01 has no legacy story; it was built from the wave 3 legacy keys, the wave 2 journey harness it mirrors, and the architecture and design extracts.
- Acceptance criteria ownership per key:
  - RWB-E4-050: AC1 is copied verbatim with the tag "(legacy RWB-E4-050 AC1)" and owns the key. AC2 ("Not recorded") is owned by RWB-P8-E4050-APP and is exercised only as the negative path of the same loop. AC3 and AC4 are harness-only criteria tagged "(new, D-RCV-60)".
  - RWB-E5-002: the WP lists no legacy criterion for this story, so the four legacy criteria stay with RWB-S4-E5002-APP and are not restated. Seven harness criteria are new under D-RCV-60 and test only the cross-service serving chain.
  - RWB-E5-009: AC1 is copied verbatim with the tag "(legacy RWB-E5-009 AC1)". AC2, AC3 and AC4 are owned by RWB-S4-E5009-APP and are not restated; AC2 to AC6 of this story are harness criteria new under D-RCV-60.
  - W3J01: new story, no legacy counterpart; every criterion is new under D-RCV-60.
- Release dates copied unchanged and marked "(tentative)": 28 February 2027 for RWB-E4-050, 31 March 2027 for RWB-E5-002 and RWB-E5-009. W3J01 carries "None (new story)".
- Patterns applied are exactly those the WP names: DP03, DP05, DP19 for RWB-E4-050; DP03, DP05, DP13, DP19 for RWB-E5-002; DP03, DP13, DP19 for RWB-E5-009; none for W3J01. Each applied pattern has its section 13 row from the §R5.5 table. The platform H dependencies named by the DP table (RWB-PLT-E1027-CON, RWB-PLT-N001-CON) are not repeated in the metadata H row, which stays None, and the only blocking dependencies are the I stories.
- Section 12 of every story follows §R7.2: tables 12.1 to 12.9, "None" where empty, every owner and path taken from the Ownership Map or from the Architecture v5 contract slides. No `/api/recovery/v1/` base appears outside a DP-13 marker sentence, and no monolith base is served.
- Post-fanout correction: the row shape was aligned with WP step 9 before the stories were finalised, so each story carries one combined gap row (not one row per open item) plus one assumption row per default it applied. The registers were not rewritten by any subagent; every row is an append.
- The split of each legacy key is stated in its story: the notice fact and its serving are P6's, the pack is P5's, the instruction and result are S9's, the rule evaluation and the case move are S4's, the timer and the case of record are P3's, the reconciliation result is P1's and the proceeds, the write-off and the decision record are their owners'. No harness computes a business rule, starts a clock, or reads another service's table; every read and every seed goes through a published contract.
- The harness stories are the QA team's Day-1 work of §R5.7 rule 6 where the owner is QA (W3J01); the other three carry the TechX phrase the WP fixes for an ITG story.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E4050 ITG Reconcile money movements daily - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E5002 ITG Record proof of delivery on a notice - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG E5009 ITG Instruct the firm through the portal - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W3 Wave 3 integration/RWB ITG W3J01 ITG Wave 3 journey end to end - integration v1.md
- _work/msr/fragments/RWB-ITG-E4050-ITG.json
- _work/msr/fragments/RWB-ITG-E5002-ITG.json
- _work/msr/fragments/RWB-ITG-E5009-ITG.json
- _work/msr/fragments/RWB-ITG-W3J01-ITG.json
- _work/msr/gaps/B-ITG-W3-02.jsonl
- _work/msr/assumptions/B-ITG-W3-02.jsonl
- _work/msr/editlog/B-ITG-W3-02.md

| Story | File | ACs owned | TCs | I dependencies |
|---|---|---|---|---|
| RWB-ITG-E4050-ITG | RWB ITG E4050 ITG Reconcile money movements daily - integration v1.md | AC1 (legacy RWB-E4-050); AC3 and AC4 new | TC-E4-050-01-ITG to TC-E4-050-04-ITG | RWB-P8-E4050-APP |
| RWB-ITG-E5002-ITG | RWB ITG E5002 ITG Record proof of delivery on a notice - integration v1.md | None from the legacy key (S4 owns AC1 to AC4); AC1 to AC7 new | TC-E5-002-01-ITG to TC-E5-002-06-ITG | RWB-S4-E5002-APP, RWB-P6-E5002-APP, RWB-P3-E5002-APP |
| RWB-ITG-E5009-ITG | RWB ITG E5009 ITG Instruct the firm through the portal - integration v1.md | AC1 (legacy RWB-E5-009); AC2 to AC6 new | TC-E5-009-01-ITG to TC-E5-009-06-ITG | RWB-S4-E5009-APP |
| RWB-ITG-W3J01-ITG | RWB ITG W3J01 ITG Wave 3 journey end to end - integration v1.md | AC1 to AC6, all new | TC-W3J01-01-ITG to TC-W3J01-10-ITG | None (stub set from Day 1) |

## Gap and assumption rows

- Gap rows written to `_work/msr/gaps/B-ITG-W3-02.jsonl`: 4, one combined row per story as WP step 9 requires, each enumerating every open item of its story in one description with its evidence and a proposed resolution.
  - GAP-0434 — the `reconciliation_result` ownership conflict and its read operation, the ACE product codes and the reconciliation operation, the REC-04 and REC-06 rule package, the rwb-writeoff read, the result codes and tolerance, and the wave 3 harness pack (Conflict, P2, wave 3, legacy RWB-E4-050).
  - GAP-0437 — the four-way split of the legacy step, the unnamed proof-record operation and notice proof write, the delivery-status to notice-state mapping, the notice lifecycle state and the three unnamed case notice facts, the notice-period and proof-window reference data, the S4 to P3 hand-off, the FEAT-LIT-02 conflict between the specification and the story master, and the harness pack (Missing, P2, wave 3, legacy RWB-E5-002).
  - GAP-0435 — the four-way split of the legacy step, the instruction and result field names and pack reference, which timer is the partner clock, the idempotency key, the pack-serving surface, the message at instruction against filing, and the harness pack (Missing, P2, wave 3, legacy RWB-E5-009).
  - GAP-0436 — the harness environment, the seeded case and every identifier, the fixed business date, the evidence format and its retention, the gate name and thresholds, the three operation names no source gives, the six data product codes, and the wave 3 harness pack (Missing, P2, wave 3, new story).
- Assumption rows written to `_work/msr/assumptions/B-ITG-W3-02.jsonl`: 20, one per default applied, confidence Medium or High, each naming its gap, the default it applies and the role that confirms it.
  - RWB-E4-050: ASM-0610 to -3.
  - RWB-E5-002: ASM-0623 to -7.
  - RWB-E5-009: ASM-0613 to -5.
  - W3J01: ASM-0618 to -5.
- Counts: CG 4, ASM 20. No gap row numbers a GAP-nnnn and no assumption row numbers an ASM-nnnn; numbering is left to step D1.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W3-02 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 metadata rows | PASS | 0 |
| C03 19 sections | PASS | 0 |
| C05 AC origin tags | PASS | 0 |
| C12 person names and emails | PASS | 0 |
| C13 issue tracker | PASS | 0 |
| C18 write-only and legacy hashes | PASS | 0 |

Also run on the same file set: C14 header lines PASS, C15 release and tentative PASS, C16 service names and API base PASS, C17 gap and assumption citations PASS, C20 tool line PASS. Every story was checked before it was accepted with a structural self-check (title and story ID, the 20 metadata rows in order, the 19 section headings, the AC origin tags, the header lines, the change-log and tool line, the tentative marker, the service shorts in topics, bases and queues, and the absence of the monolith base); the helper is scratch tooling in the run area, not a deliverable.

No file outside the WP "Write only" list was written, no existing file was edited, and no register row was rewritten: the two registers hold only appended rows and each is valid JSON per line.

## Carried forward, not decided here

- RWB-S4-E5002-APP, which owns the four legacy criteria of RWB-E5-002, has no story file in the folder yet, so that ownership is a forward reference until the WP of that key writes it. This affects the legacy-AC coverage check at stage C (C10) and not the criteria of this story.
- The instruction fact of RWB-E5-009 is carried on `rwb.partner.events.v1` (EV-20), because `rwb.litigation.events.v1` carries only LawsuitFiled, JudgmentRecorded and AuctionResult. Recorded in ASM-0615.
- The wave 3 journey asserts the S7 write-off and S9 partner hops on stubs, because both are wave 4 owners; a stub pass is never reported as a real-service pass. Recorded in ASM-0622.
