# Shared brief — WP B-S5-01, S5 rwb-asset, legacy RWB-E3-019 to RWB-E3-023

Scratch note for the five parallel workers of WP B-S5-01. It fixes the facts that must be
identical across the ten story files so the set reads as one service. It is not a story file.

## A. Service facts (identical in every file)

| Item | Value | Source |
|---|---|---|
| Service | rwb-asset, code S5, "Assets and auction" | Template and Rules §R4; Architecture v5 slide 19 |
| Service epic / wave | RWB-SVC-S5 / wave 2 (Arch v5 wave 2 for S5; W-MAP EP03 is also 2, no conflict) | §R4, §R5.6 |
| Schema / login | `rwb_asset` / `rwb_asset` | §R4; Arch v5 slide 19 OUT |
| REST base | `/api/recovery/asset/v1` (DP-13) | §R4, DP-13 |
| Topic | `rwb.asset.events.v1`, with `rwb.asset.events.v1.retry` and `rwb.asset.events.v1.dlt` (DP-14) | §R4; Arch v5 slide 19 |
| Event names | `rwb.asset.<Event>.v1` | §R4 |
| Task queue / namespace | `rwb-asset` in `rwb-recovery` | §R4 |
| Java package | `th.co.scb.ace.workbench.recovery.asset` | §R4 |
| Stage workflow | `AssetDisposalWorkflow`, the stage child of `CaseWorkflow` (P3), continues-as-new | Arch v5 slide 19 IN; Temporal and Drools extract slide 13 |
| Schedule | Only JOB-19 re-appraisal monthly belongs to rwb-asset and it belongs to the re-appraisal story (RWB-S5-E3026); none of the five keys owns a Schedule | Arch v5 slide 44; Ownership Map jobs JOB-19 |
| Tables (Ownership Map) | `listing` S5, `asset_sale` S5; `asset` is S5 by Arch v5 slides 19 and 41 and TSD S5 T3.1 although the Ownership Map table list has no `asset` row — say so and cite it in the gap row | ownership.json tables |
| Tables of others (never written here) | `recovery_case` P3, `task` P3, `timer` P3, `notice` P6, `document` P5, `proceeds` P8, `decision_log_entry` P7, `rule_row` P7, every `v_ace_*` P1 | ownership.json tables |
| API provided (Ownership Map) | `GET /assets` API-S5-001 (owner S5); `GET /assets/{assetId}` API-S5-002 (owner S5, ASM-A6-api-15 notes `/assets/{assetKey}` supersedes it in v3) | ownership.json api; TSD S5 T-A.1 |
| API not ours | `POST /assets/{assetId}/valuations` API-S5-003 is rwb-valuation (S1) under ASM-A6-api-6; `POST /assets/{assetId}/listings` API-S5-004 and `POST /listings/{listingId}/rounds` API-S5-005 belong to the pricing and auction stories of this service | ownership.json api |
| Events published by S5 | `AssetTakenOn` (catalogue event 22, consumers rwb-case and rwb-payment) and `AssetSold` (catalogue; consumers rwb-payment, rwb-case) | Arch v5 slide 43 rows 22, 25 and "+" |
| Events consumed by S5 | `JudgmentRecorded`, `AuctionResult` (rwb-litigation), `ProceedsMatched` (rwb-payment), `PartnerResultSubmitted` (rwb-partner) | Arch v5 slide 19 IN; slide 43 rows 21, 25, "+" |
| Screens | SCR-21 Asset list (Loading; list) and SCR-22 Asset record (Take-on; held; listed; sold), read through the gateway-bff composite route (DP-19) | legacy story §Screen and states; DP-19 |
| Capability area | "Asset and disposal". RW-SALEOFF CRUA, RW-NPAMGR CRU, RW-ENFORCE CRU, SY-DATALOAD CU, PT-AUCTION RU, PT-RAMC RU, RW-PRODHEAD/RW-HEADNPA/RW-HEADASL RA, every other role of the matrix R | TSD S5 T6.1 |
| LOVs | LOV-ASSET-TYPE, LOV-TRANSFER-IN, LOV-SEGMENT, LOV-HOLDING, LOV-LISTING, LOV-SALE-CHANNEL — read as reference data, never constants | TSD S5 T3.2 |
| Messages | MSG-S5-001, MSG-S5-002, MSG-GEN-001, MSG-P4-002, MSG-P7-003 (all five from the legacy message set); MSG-P1-001 only where a stale data product is raised (VR-S5-00n-1) | legacy story; FSD S5 A2.n.3.1 |
| ACE side | `v_ace_npa_asset` (and `v_ace_collateral` for the deed in lieu) are read only by rwb-source-data (Arch v5 slides 13, 29, 37 and 45). rwb-asset holds no `v_ace_*` grant, so DP-05 applies as a **prohibition** and the ACE asset fact arrives on the rwb-source-data data-product contract, whose operation names are not published | Arch v5 slides 29, 37, 45; DP-05; sibling gap CG-B-S5-06-1 |
| Case side | the case of record, its route states (ASSET_PENDING_TAKE_ON, ASSET_ON_BOOKS, ASSET_HELD, FAILED_NOTICE_QUEUE) and the `CaseWorkflow` parent are rwb-case's (P3). This service **answers** the case move; it never writes `recovery_case`. No published case-move operation exists in the Ownership Map, so the operation name is the placeholder | ownership.json; Arch v5 slide 14 |
| Money side | any posting, charge or balance change is rwb-payment's (P8) | ownership.json (`proceeds` P8); Arch v5 slide 17 |

## B. Per-key specifics

| Key | Legacy story lines | FSD | Rules to table in §8 | Trigger in the target | Consumed contract of this step | Tables written |
|---|---|---|---|---|---|---|
| RWB-E3-019 | v3 md 5614–5709 | A2.1 (99–170) | R-DIS-01, R-DIS-06, R-DIS-03 | the repossession result of the case, read on the rwb-source-data ACE asset fact; no Kafka event | rwb-source-data data-product contract (name placeholder); rwb-case case-move answer | `asset` (DF-COL-028…042), decision_record, idempotency_key |
| RWB-E3-020 | 5712–5808 | A2.2 (173–244) | R-DIS-02, R-DIS-01, R-DIS-03 | the completed deed in lieu transfer, read on `RWB-S2-E3012-CON` ("Run a deed in lieu to ownership transfer") | RWB-S2-E3012-CON; rwb-source-data data-product contract; rwb-case case-move answer | `asset` |
| RWB-E3-021 | 5811–5907 | A2.3 (247–318) | R-DIS-01, R-DIS-02, R-DIS-03 | the `AuctionResult` event of rwb-litigation (`rwb.litigation.events.v1`), plus the ladder facts on `RWB-S4-E5019-CON` | `AuctionResult` (Kafka), RWB-S4-E5019-CON, rwb-source-data contract, rwb-case answer | `asset` |
| RWB-E3-022 | 5910–6007 | A2.4 (321–391) | R-DIS-04, R-DIS-05 | the take-on step of `AssetDisposalWorkflow` for a case in ASSET_PENDING_TAKE_ON | `RWB-P6-E1052-CON` ("Notice generation v1") and the proof of delivery of P6; rwb-case answer for the failed notice task and the case move | decision_record, idempotency_key (no `asset` row before the take-on completes) |
| RWB-E3-023 | 6010–6097 | A2.5 (394–463) | R-DIS-06, R-DIS-09 | the confirmed asset record and the durable holding/provision clocks of `AssetDisposalWorkflow` | the rwb-payment cost-of-carry posting (operation name placeholder; `RWB-P8-E4049-CON` is proceeds application, not a cost-of-carry charge); rwb-case answer | `asset` columns DF-COL-041, DF-COL-042 and the provision facts; decision_record |

Every take-on key (E3019, E3020, E3021) publishes `AssetTakenOn` from the outbox. E3022 and E3023
publish nothing. No key of this WP consumes `ProceedsMatched`.

**One tension to state openly in each file.** The plan's pattern set for these keys is DP03, DP05,
DP13, DP19 and does not carry DP-09, yet Arch v5 slide 19 OUT gives the topic and event 22 gives
`AssetTakenOn`. The file declares the event, keeps the H row exactly as the plan states it, and
records in its gap and assumption rows that the outbox and inbox library (`RWB-PLT-TE006-CON`,
DP-09) and the rwb-case move answer are real dependencies the plan's rows do not carry.

## C. Document requirements (Template and Rules §R7)

1. First line `# <Story key> <Title>`; then the two header lines of §R8.1; then the metadata table
   of §R7.1 with the twenty rows in order and no row removed; then a **Change log** paragraph that
   names D-RCV-60, the date 22 November 2026, what was split, and ends with
   `Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.`
2. The nineteen `### n. Name` headings in the §R7.2 order, spelled exactly.
3. Metadata values, copied from the WP story line: Release `31 January 2027 (tentative)`; owner
   `TechX (suggested; any team may pick up this story)`; Work type `APP (App development)` or
   `CON (Contract)`; Depends on (build) / Contract dependencies / Integration dependencies /
   External dependencies = the H, C, I, X lists comma-separated, `None` when empty; PRD reference
   `Pending (C1)`; Status `Draft (realignment v1)`; Patterns applied `DP03, DP05, DP13, DP19`.
4. APP files: §7 holds **only** the legacy criteria of that key, verbatim, in legacy order, each
   `Scenario: ACn <legacy scenario text> (legacy RWB-E3-0nn ACn)`; the only permitted addition is
   one or two `Given the <service> contract mock returns <x>` lines at the top of a scenario whose
   cross-service part is mocked, keeping every legacy value character for character (the legacy
   dates, MSG ids, state names, `Then` repetitions and awkward wording all stay). A paragraph after
   the block explains the additions and what happens where in the target.
5. CON files: §7 holds only new criteria, each tagged `(new, D-RCV-60)`, testing the artefact
   (schema validity, additive rule, vocabulary, shapes, consumed rows, fakes, naming, boundary) —
   never a business outcome of the APP file and never a copy of a legacy criterion.
6. §16 test cases: table `TC ID | Covers | Level | Data`; the legacy TC ids of that key kept with
   the legacy order and intent, `Level` = Unit / Component / Contract / Integration / End to end /
   NFR; `-ITG` copies named where an integration copy exists. Add new `TC-S5-E30nn-CON-0n` cases in
   the CON files only.
7. §12 Contract: 12.1 to 12.9, `None` where empty, correct per-service names only. 12.7 lists the
   tables of §B and the PLT library objects (`decision_record`, `idempotency_key`, `outbox_event`,
   `processed_event`) created in `rwb_asset`.
8. §17 guardrails must repeat the §R7.2 s17 rule: no business values in code, no PII in events,
   workflow inputs or logs, ACE data only through the owner's contract or `v_ace_*` views.
9. §18 traceability: the requirement of §A/§B with `REQ-S5-001` (take-on) or `REQ-S5-003` (holding
   age), noting the split plan carries no requirement id for the slice; ADR-013, ADR-014, ADR-015,
   ADR-020, ADR-022; the legacy key; the test cases; the patterns.
10. British spelling, no bullet-free walls of text, no person names, no email addresses, no mention
    of the issue tracker, no external call, no invented business value.

## D. Gaps and assumptions (per key)

- Ids: `CG-B-S5-01-<Ekey>-<n>` and `ASM-B-S5-01-<Ekey>-<n>` with `<Ekey>` = `E3019` … `E3023`.
  Each worker writes only its own ids into `_work/msr/gaps/B-S5-01.jsonl` and
  `_work/msr/assumptions/B-S5-01.jsonl`, **appending** one JSON object per line and never
  rewriting the file.
- One combined gap row per story file (the placeholder of §9 of the WP), plus at most four targeted
  rows (for example the missing `asset` row in the Ownership Map, the missing DP-09 outbox
  dependency, the unpublished rwb-source-data operation names, the missing external dependency of
  WIN or the LED portal). Every gap id cited in a file must exist in the jsonl, and every assumption
  id likewise. Rows carry the §R9 keys; `wp` is `B-S5-01`.
- A default read (a value no source gives) gets an assumption row with confidence Medium and the
  placeholder text in the file. A missing business value is never invented.

## E. Fragment

`_work/msr/fragments/<id>.json`, the exact key order of WP B-S5-01 §8. `acs` entries are
`{"id","origin","text_first_line"}` where `text_first_line` is the whole `Scenario:` line including
its tag. `gaps` and `assumptions` list the ids that file cites. `ops_provided`,
`ops_consumed`, `events_published`, `events_consumed`, `workflows` use the target names of §A.

## F. Self-check before returning

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-S5-01 --quick` and fix every
finding that names a file of your own key (`C02`, `C03`, `C05`, `C12`, `C13`, `C18`). Findings that
name a sibling key are the sibling's. Do not write `_work/msr/editlog/B-S5-01.md`; the lead does.
