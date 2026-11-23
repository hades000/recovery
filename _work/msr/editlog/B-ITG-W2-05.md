# Edit log B-ITG-W2-05

WP B-ITG-W2-05 (RWB-ITG-W2: legacy RWB-E2-024, RWB-E2-025, RWB-E2-026, RWB-E2-027, RWB-E2-028). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2024 ITG Field app photos and bills into the document hub - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2025 ITG Extraction for the stage 2 and 3 document types - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2026 ITG Document generation engine for contract, CA and mortgage templates - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2027 ITG Payment matching rules with the data team - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2028 ITG Case intake agent live at L1 [E3a] - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2024-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2025-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2026-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2027-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2028-ITG.json`
- `_work/msr/gaps/B-ITG-W2-05.jsonl`
- `_work/msr/assumptions/B-ITG-W2-05.jsonl`
- `_work/msr/editlog/B-ITG-W2-05.md`

## Method

- Read the Template and Rules v1 in full, the WP, the Ownership Map, the Architecture v5 text extract (slides 13-20 and 41-44 in particular), the Temporal and Drools text extract (slides 11-16), the five legacy Epic 2 stories and the thin-story extracts used for fill order (Program BRD v4, Epic 2 BRD v2, Epics 3 to 8 Specification v3, Business Rules and Routing Logic v4).
- Fanout 5: one task subagent per legacy key (RWB-E2-024, RWB-E2-025, RWB-E2-026, RWB-E2-027, RWB-E2-028) in one message, each writing only its own story file and fragment. The parent wrote the two candidate registers and this edit log, then ran the check.
- Story shape: each of the five is the wave 2 integration harness for its legacy key. It builds no production endpoint, screen, table or migration. Sections 1 and 13 say so plainly; the harness runs the real cross-service journey against the published contracts of its I dependencies, replaces each contract fake as the real service lands, keeps a seed pack and an evidence pack, and applies a pass or fail gate.
- AC policy: RWB-E2-027 owns AC1, AC2, AC3, AC4, AC5, AC8 and AC9; those seven scenarios and the Background are copied word for word from the legacy section 7 with only the origin tag added, and a diff after stripping the tag is byte-identical. The other four stories own no legacy AC in the plan, so each writes new criteria tagged (new, D-RCV-60) that test only the integration deliverable, using values that already exist in the legacy story (case IDs, amounts, dates, message codes, thresholds) and inventing none.
- TCs: every id of `tcs_legacy` is carried as an ITG copy with the `-ITG` suffix, in the WP order, with the Level column of section R7.2 s16. Journey cases are Integration; the access case is Component; the Principle 5 case is NFR.
- Sections 12.1-12.9 are present in every story. 12.1, 12.3, 12.6 and 12.7 are "None" because an ITG story provides no production operation, publishes no event, adds no schedule and owns no table. 12.2 names owners from the Ownership Map only, on each owner's `/api/recovery/<short>/v1` base with one hop and the 2 s timeout of DP-11.
- Patterns: every DP in the story line gets a row in the section 13 table with the exact "Microservice pattern" and "Dependency added" text of section R5.5. The platform H dependencies in that table are delivered by the platform waves and are not repeated in the metadata, which carries no build dependency for any of the five stories.
- Naming: topics `rwb.<short>.events.v1` and the shared `rwb.decision-record.v1`, event names `rwb.<short>.<Event>.v1`, queues `rwb-<short>`, schema names only in prose and never read by the harness (DP-01).

## Registers

- Candidate gap rows: 5 (GAP-0406, GAP-0407, GAP-0408, GAP-0409, GAP-0410). One combined row per story, all type Missing, severity P2, each carrying the harness pack, fixtures and evidence format, plus the story-specific open point (the rule-version load route and its routed path for E2027).
- Candidate assumption rows: 5 (ASM-0581, ASM-0582, ASM-0583, ASM-0584, ASM-0585), one default per story: SIT harness against the published contracts, each fake replaced as its I story lands, evidence a per-run report keyed by story and business date.
- Every missing value in the five stories and five fragments cites only its own pair. No other CG or ASM id is cited.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-05 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Additional local validation, all clean: the 20 metadata rows in order with the values of the story line; the 19 section headings in order; 12.1-12.9 present in order; 8 new scenarios per story except E2027 (7 legacy copies) and E2028 (9); every `tcs_legacy` id present with `-ITG` and equal to the fragment `tcs`; the five fragment JSON files carry exactly the 28 required keys and their I, reqs, ops, events and ids match the story lines; every cited CG and ASM id resolves to a row; no tracker reference, no e-mail address, no person name, no monolith API base outside the DP-13 legacy-marker cell; every API base, topic and queue uses one of the 19 service shorts; each story carries the two header lines, the D-RCV-60 change-log row and the tool line.
