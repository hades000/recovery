# Edit log — WP B-TECH-10 (Recovery Workbench Error Handling and Resilience Standard next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v3.docx` (all seven
sections, the metadata table and all five tables), `22 Microservice Realignment/Recovery Workbench Microservice Story
Template and Rules v1.md` (§R1, §R3, §R5, §R8, §R9), `_work/msr/plan/ownership.json` and `22 Microservice Realignment/
Recovery Workbench Microservice Ownership Map v1.xlsx` (Read me, Services, Tables, Endpoints, Events, Workflows and
activities, Jobs), `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 10, 11, 20,
22, 44, the call-type table and the resilience appendix), `22 Microservice Realignment/Recovery Workbench Temporal and
Drools Design Text Extract v1.md` (activity retry policy, idempotency, Kafka failure), `_work/msr/plan/split_plan.json`
(stats and legacy only) and `_work/msr/plan/ids.json`. Nothing read was edited; the v3 document was opened read-only and
used as a template, never written.

## Files written

- 05 Technical architecture/Recovery Workbench Error Handling and Resilience Standard v4.docx
- _work/msr/gaps/B-TECH-10.jsonl
- _work/msr/assumptions/B-TECH-10.jsonl
- _work/msr/editlog/B-TECH-10.md

Scratch files under `_work/msr/docs/B-TECH-10/` (build and verification only, not outputs of the run): the full text
`Recovery Workbench Error Handling and Resilience Standard v4.md`, `template-fixed.docx`, `build.py`, `verify.py`,
`verify_docx.py`, the probe scripts and `roundtrip.txt`. The converted source text sits in the run extract folder,
`_work/msr/extract/B-TECH-10`, with the extract of the ownership map next to it in the same folder.

## 1. How the next version was produced

The source was never edited. The full text of version 4 was written to
`_work/msr/docs/B-TECH-10/Recovery Workbench Error Handling and Resilience Standard v4.md` and rendered onto a scratch copy
of the v3 document with `compat/office_write.py md-docx --template`, so the new version keeps the v3 section properties,
page setup, footer and core styles.

**Template repair, in the scratch copy only.** This document family stores its heading style names as `Heading 1` to
`Heading 6` (python-docx looks them up as `heading 1`) and has no `List Bullet` style, so `md-docx` would fail on the
headings and would prefix every bullet with a replacement character. `build.py` repairs the copy: it lower-cases the six
heading style names and adds a `List Bullet` style based on `List Paragraph` with the bullet numbering the v3 document
already uses (numId 2, the bullet list its own sections are set in). After the render it applies the v3 table look to
every table (the v3 borders, the DCD3EB header band, the cell margins, Aptos 8 pt, bold header row and bold first column
except in the two-column metadata table). The v3 file is byte-for-byte unchanged.

**Document properties.** The v3 file carries a person name in `author` and `last_modified_by`. The new file is set to
`Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Error Handling and Resilience
Standard v4`, revision 4, modified 22 November 2026 (rule 4). The package XML of the new file was scanned: the name is
gone.

**Header, change log and status.** Lines 1 and 2 of the new file are the header of Template and Rules §R8.1. The metadata
table carries the change row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
Flash`, the source version row `3, 16 November 2026` and the status row `Draft. No approval is recorded for this version
(ASM-3300)`. The change log repeats the v3 row `v3, 16 November 2026, D-RCV-36: …` character for character.

## 2. Fidelity to version 3

`verify_docx.py` compares every non-empty paragraph and table cell of the v3 document with the text of the v4 file:

| Item | Result |
|---|---|
| v3 text lines present verbatim in v4 | All 187, except the 4 listed as intended changes below |
| v3 lines missing and not listed as changed | 0 |
| Sections | 1 to 7 of v3, in order, then the new sections 8 and 9 |
| Tables | 9 (5 of the source, 4 new) |
| Header lines 1 and 2 | Present, as the first two paragraphs |
| Change-log row with D-RCV-60 and the tool line | Present |
| Bullets | 39 real bulleted paragraphs; no replacement-character prefix |

The four intended changes are the header date line (`16 November 2026` becomes the v4 date) and the three metadata rows
`Version`, `Date` and `Change`. Every other line of v3 is kept word for word: the seven opening rules, all thirteen
failure categories, all eight retry rows, the six user-facing statements, all nine recovery paths, all nine Temporal and
Drools bullets, all eight message rows and the closing sentence of section 7.

Every ID, number and date of v3 is kept unchanged: MSG-GEN-001, MSG-GEN-004, MSG-P1-001, MSG-P3-005, MSG-P3-027,
MSG-P3-036, MSG-P3-037, MSG-P3-038, MSG-P4-002, MSG-P4-003, MSG-P7-003, REQ-DRI-005, E2-043, NFR-026, RW-PLATADM, checks
compile, package in force and checksum, the 1, 5 and 15 minute ladder, the 60 second agent limit, the 1 second, back-off
2 and 10 attempt activity policy, ADR-011 and ADR-012, and the dates 16 November 2026. No date is moved, and the document
holds no release date to mark (tentative).

## 3. What version 4 changes, and why

The change set is the realignment only: the 2 s timeout, one REST hop, and the retry and `.dlt` rules. The closing table
of the document, `Realignment changes in version 4 (D-RCV-60)`, lists the eight changes with the section, the v3 value,
the v4 value and the decision. In summary:

1. **2 s timeout.** Every REST hop now has a 2 s ceiling, a circuit breaker and a bulkhead per downstream, and a GET
   retried once with jitter inside the budget; a POST is never retried automatically and carries its Idempotency-Key
   (Architecture v5 slides 10 and 11; ADR-020). Added to §1 (two rules), §2 (REST timeout), §3 (REST calls and REST calls
   inside an activity), §4 (one bullet), §5 (one recovery row), §6 (one bullet), §7 (one row) and §8.2.
2. **One REST hop.** gateway-bff calls each owner directly and in parallel, a service never chains a call to answer a
   screen, and anything longer becomes a workflow; trace analysis flags call depth above one (Architecture v5 slide 11;
   ADR-020). Added to §1, §2 (call chain), §3 (REST call depth), §5 (call chain found in a trace) and the new §8.1.
3. **Retry.** The event retry ladder is 1 minute, 10 minutes and 1 hour on the retry topics of the owner's topic, with
   one consumer group per service and an inbox row per `ce_id`, so a retry or a redelivery acts once (Architecture v5
   slides 11 and 22; ADR-015; DP-09). Added to §1, §2 (event retry, duplicate event), §3 (event consumers, Kafka broker
   unavailable), §4, §5 and §8.3.
4. **`.dlt` rule.** An event that exhausts the three retries is parked on the `.dlt` topic of the owner's topic with an
   alert and the replay tool (Architecture v5 slide 22). Added to §2 (dead letter), §3, §4, §5, §7 and §8.3, with the
   alert and replay role recorded as the platform administrator (GAP-2055; ASM-3304).
5. **Owner of every topic.** The new §8.3 table gives all 19 services, their topic `rwb.<short>.events.v1`, the retry
   ladder, the `.dlt` topic and the owning service, from the Microservice Ownership Map v1 Services and Events sheets. The
   shared topic `rwb.decision-record.v1` is recorded as owned by rwb-decision (P7).
6. **Outbox scope.** The v3 sentence is kept word for word and version 4 records the Arch v5 reading next to it: the
   transactional outbox and the inbox are library objects in all 19 schemas, and the Epic 1 and Epic 2 wording is the
   as-built position (GAP-2053; ASM-3301).

## 4. Owners

Every service owner in the document is a service code and name of the Microservice Ownership Map v1 and
`_work/msr/plan/ownership.json`: rwb-source-data (P1) to rwb-agent (P10) and rwb-valuation (S1) to rwb-partner (S9) for
the topics, rwb-integration (P2) for the file transfer, rwb-decision (P7) for the shared decision-record topic, and
gateway-bff for the screen calls. The operational owners stay the roles of v3 (platform administrator, data steward, SCB
IT, centre of excellence analyst, risk and model risk officer, developer); no team type is turned into a service owner
and no person is named.

## 5. Registers

- Gap rows written: **5** candidate rows, `GAP-2052` to `GAP-2056`, in `_work/msr/gaps/B-TECH-10.jsonl`
  (3 Missing, 1 Conflict, 1 Ambiguous; 1 of severity P2 and 4 of P3).
- Assumption rows written: **6** candidate rows, `ASM-3300` to `ASM-3305`, in
  `_work/msr/assumptions/B-TECH-10.jsonl` (4 High, 2 Medium).
- Every gap row names its assumption and every assumption names its gap where it has one; every citation in the document
  resolves to a row: the document cites GAP-2052 to GAP-2056 and ASM-3300 to ASM-3305.
- The rows are open points only: the retry-topic and `.dlt` names (CG-1), the outbox scope conflict between v3 and Arch
  v5 (CG-2), the missing message ID for a REST timeout or a dead-lettered event (CG-3), the role that replays (CG-4) and
  the 2 s ceiling against the 2 s screen target (CG-5).
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-10 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

`verify_docx.py` reports PASS: header lines 1 and 2 present, the D-RCV-60 change-log row and the v3 change row present, 0
unexplained missing lines of v3, sections 1 to 7 in order, 9 tables matching the full text, 39 real bullets, all 11
CG/ASM citations resolved, no person name in the package, no email address, no issue-tracker reference and no wrong tool
attribution. `verify.py` reports 83 of 87 source lines verbatim with 0 missing and the 4 intended changes accounted for.

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded for this run (ASM-3300). No later lifecycle stage was
started. No issue tracker, wiki, repository, Figma or web call was made, and no commit was created. No other document of
the family was touched, and the v3 file is unchanged on disk.
