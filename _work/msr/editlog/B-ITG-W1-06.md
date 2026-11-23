# Edit log B-ITG-W1-06 — RWB-ITG-W1 (legacy RWB-E1-039, RWB-E1-046, RWB-E1-047, RWB-E1-049, RWB-E1-050)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-W1-06 (RWB-ITG-W1 Wave 1 integration)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, dispatched in one message; each wrote only its own story and fragment and cited the register rows written once by the parent.

## Story files written (5)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1039 ITG Access log into the decision log and break-glass admin - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1046 ITG Template and merge field catalog as data - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1047 ITG Feature flags for module release with a removal date - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1049 ITG OCR pipeline on the Workbench document hub - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1050 ITG Document classification - integration v1.md`

Each story carries the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in order with the values of its WP story line, the 19 section headings of §R7.2 in order, the nine sub-tables 12.1–12.9, the §R7.2 s16 Level column, an origin tag on every Scenario line, the release marked `(tentative)` and a D-RCV-60 change-log row with the tool line. Service facts follow §R4 for P2 rwb-integration: schema `rwb_integration`, REST base `/api/recovery/integration/v1`, topic `rwb.integration.events.v1`, event names `rwb.integration.<Event>.v1`, task queue `rwb-integration`, Java package `th.co.scb.ace.workbench.recovery.integration`. No REST operation is provided by any of the five suites, so 12.1, 12.3 and 12.7 are `None` in every story.

## Fragments written (5)

- `_work/msr/fragments/RWB-ITG-E1039-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1046-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1047-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1049-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1050-ITG.json`

Each fragment has the 28 keys of the WP in order: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file. Every `acs` entry carries the Scenario line exactly as written in the story, and every `tcs` id appears in the story §16 table.

## Candidate registers

- `_work/msr/gaps/B-ITG-W1-06.jsonl` — 5 rows, one combined gap row per story (GAP-0359, GAP-0360, GAP-0361, GAP-0362, GAP-0363). Four are conflicts between the legacy module wording and the Ownership Map (P4 to P3 for the reference-load path, P2 to PLT for the flags, the JOB-12 trigger and worker count, the P10 agent route for the classifier); E1039 is a missing value (grant operation, ledger fault point and SIT evidence). Count: CG = 5.
- `_work/msr/assumptions/B-ITG-W1-06.jsonl` — 16 rows, one per default per story (E1039 three, E1046 four, E1047 three, E1049 three, E1050 three). Count: ASM = 16.

The register rows were written once by the parent before the fanout with a per-key id, so the five parallel subagents could cite them without a concurrent write to the same jsonl file.

## Coverage

| Story | Legacy | ACs | TCs | I dependencies |
|---|---|---|---|---|
| RWB-ITG-E1039-ITG | RWB-E1-039 | 8, all `(new, D-RCV-60)` | 8 | RWB-P7-E1008-APP, RWB-P4-E1039-APP, RWB-P5-E1039-APP, RWB-P7-E1039-APP |
| RWB-ITG-E1046-ITG | RWB-E1-046 | 10, all `(new, D-RCV-60)` | 11 | RWB-P1-E1001-APP, RWB-P1-E1069-APP, RWB-P6-E1046-APP, RWB-P7-E1046-APP, RWB-P5-E1046-APP |
| RWB-ITG-E1047-ITG | RWB-E1-047 | 11, all `(new, D-RCV-60)` | 11 | RWB-P1-E1001-APP, RWB-PLT-E1047-APP |
| RWB-ITG-E1049-ITG | RWB-E1-049 | 11, all `(new, D-RCV-60)` | 12 | RWB-P3-E1045-APP, RWB-P5-E1049-APP, RWB-P6-E1049-APP |
| RWB-ITG-E1050-ITG | RWB-E1-050 | 11, all `(new, D-RCV-60)` | 11 | RWB-P5-E1050-APP, RWB-P3-E1050-APP |

- The plan gives every one of the five ITG stories `"acs": []`, so the legacy ACs stay with the sibling APP stories (P4/P5/P7 for E1039, P6/P5/P7 for E1046, PLT for E1047, P5/P6/P3 for E1049, P5/P3 for E1050). Each ITG story therefore writes only new acceptance criteria that test the deliverable in its own title, and each §18 names the APP stories that own the component-level ACs.
- Test cases keep the legacy ids of the scenarios the suite covers, with the `-ITG` suffix (for example TC-E1-039-01-ITG, TC-E1-047-10-ITG, TC-E1-050-11-ITG). Where a new integration criterion has no legacy counterpart (data lake absence, the naming library, the ledger approval, the parameters as data, the inbox dedupe) one new id of the form TC-ITG-<compact>-ITG-<nn> is added. Levels use the §R7.2 s16 vocabulary: Integration for the SIT cross-service scenarios, Component for refusals, Contract for stub-based checks, NFR for the throughput, resilience and ledger cases.
- Every business value is copied from its legacy story and none is invented: U-4101 to U-4106, RW-2026-000123, DOC-2026-0009981, INC0004521, IAM-778812, 14:20 and 14:31 against the 4-hour window; MF-2026.11, DEMAND-MTG, RECALL-HP, GUARANTOR-SSME, LEG-0001, XX-CAS-999, body_ref; the five flag keys and their removal dates 2027-01-31 and 2026-11-30, today 2026-12-07 and 2026-11-16; OCR_MIN_QUALITY 0.70, OCR_WORKERS 4, OCR_TIMEOUT_SECONDS 120, OCR_MAX_ATTEMPTS 3, the 180 samples and the 500-page set in 60 minutes, TEST-CO-01; CLASSIFY_THRESHOLD 0.80, the 60-second timeout, 162 of 180, COURT_NOTICE 0.62, DEMAND_LETTER 0.21, APPRAISAL_REPORT 0.80, LOAN_CONTRACT 0.91, TITLE_DEED, 0000000000000 and TEST-ACC-0001.
- Patterns: DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19 (E1039); DP01, DP07, DP11, DP13, DP15, DP19 (E1046); DP01, DP07, DP10, DP11, DP14, DP15, DP19 (E1047); DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 (E1049); DP01, DP06, DP07, DP10, DP11, DP15, DP19 (E1050). Every pattern has its §R5.5 row in §13 with the dependency added and where it sits; the H, C, I and X lists stay exactly as the plan sets them (no H, no C, no X, and the I list on the metadata row).
- Owners come from the Ownership Map only: P4 rwb-access for the grant, the access log and the session; P7 rwb-decision for the ledger and the decision-log query; P3 rwb-case for the case, the task action and the reference-load path; P5 rwb-document for the body, the intake item, the text and the generated document; P6 rwb-comms for the templates, the merge fields and the notices; P1 rwb-source-data for the data dictionary; P10 rwb-agent for the agent run; PLT for the four flag operations and the flag tables.
- The monolith base never appears outside a legacy marker: the DP-13 row writes `/api/recovery/v1` with no trailing slash, and every consumed path uses the owner's per-service base through gateway-bff. The four flag operations are written as bare paths because the Ownership Map names them as platform operations owned by PLT, not as one of the 19 service bases.
- No person name, no email address and no issue-tracker reference appears in any file; no legacy master file was changed; no web, git or external system call was made.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-06 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- Additional checks run directly on the 12 WP artefacts: C01 (baseline hashes unchanged), C15 (release 30 November 2026 marked tentative), C16 (service names in topics, bases and queues), C17 (every cited CG/ASM id has a register row) and C20 (tool line) all PASS.
- C19 still reports planned outputs of WPs not yet run (B-ITG-W1-03 and later); no B-ITG-W1-06 output is missing.
- C11 warns on legacy test cases of legacy keys whose APP stories are not yet written (for example TC-E1-039-03, -06, -07, -09, -11 and the app-owned tests of other keys); the ITG ids keep their legacy prefix so the warn clears when those stories land.
- This edit log itself:

- `_work/msr/editlog/B-ITG-W1-06.md`
