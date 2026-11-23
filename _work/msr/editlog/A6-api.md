# A6-api - Ownership Map part: api

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Agent: aisdlc-msr-worker
Date: 22 November 2026
WP: A6-api (fanout 0; run in parallel with A6-tables and A6-flows)
Status: Draft

## Files written

| # | Path |
|---|---|
| 1 | `_work/msr/plan/ownership_part_api.json` |
| 2 | `_work/msr/gaps/A6-api.jsonl` |
| 3 | `_work/msr/assumptions/A6-api.jsonl` |
| 4 | `_work/msr/editlog/A6-api.md` |

No other file in the workspace was created or changed by this WP; the check script writes its own report under the checks reports folder.

## What was done

1. Read the WP, the root run rules, the `api` section of `_work/msr/plan/ownership_skeleton.json`, the Arch v5 text extract (catalogue slides 14 to 20 and 41 to 44 first, as the WP orders), the Temporal and Drools text extract, the TSD v5 module set inside `05 Technical architecture\Recovery Workbench Technical Specifications by Module v5.zip` (read in memory, nothing extracted to disk), the Batch and Scheduling Design v4, the Event and Messaging Design v4, the Business Requirements Epic 1 v4 for E1-042 and E1-043, and Appendix R §R3 of `2026-11-22-recovery-microservice-realignment-implementation-plan.md`.

2. Turned 422 skeleton api rows into 156 unique items, because the skeleton repeats the same method and path once per API Specification version (v2, v3, v4). The id is the method and path as the WP defines it, each id appears once, and the version history is stated in the `basis` column. The v2, v3 and v4 x-module values are identical for every repeated path, so de-duplication loses no attribution.

3. Assigned exactly one owner from P1 to P10, S1 to S9, PLT to every item, in R-PREC order: the Arch v5 catalogue (slides 41 to 44, then the REST contracts on slides 14 to 20) first, the Temporal and Drools design second, then the TSD v5 module set, then the plan default rulings in Appendix R §R3. The `basis` column names the document, the slide or sheet, and the x-module of the API Specification.

4. Covered the rest of the non-table skeleton sections in the same file, under the keys `events` (30), `jobs` (22) and `workflows` (15), because the WP output schema names EV-nn, JOB-nn and Workflow ids and asks for a job `replacement`. The merge in `compat/ownership.py` routes those keys to the events, jobs and workflows buckets, so an A6-flows result for the same id simply replaces this one.

5. Recorded 33 rulings where two sources disagree on the owner, and gave every ruling one conflict gap row (type Conflict, severity P2) and one assumption row: 14 conflicts, 17 assumptions. The extra three assumptions (15 to 17) record the method used and cite no gap.

6. Kept the reference-data boundary narrow: the plan default ruling moves the generic list and reference-load paths to rwb-case, but the role, DoA and template endpoints stay with the services that Arch v5 slide 41 names, so the access service keeps its role and DoA tables and the communications service keeps its templates. The reasoning is in ASM-A6-api-4.

7. Used the plan default rulings where they bite: interaction ledger to rwb-source-data (P1), rule package registry to rwb-decision (P7), feature flags to the platform library (PLT), parameters and reference data to rwb-case (P3). The case list API is x-module P3 in every version, so it agrees with its ruling and needs no conflict row.

8. Marked the 15 paths that no longer exist in API Specification v4 in the `basis` column: the tracker paths, the data quality exception list, the manual interface retirement, the v2 asset paths that v3 re-keyed to `{assetKey}`, the POST credit-result form and the four rule-version paths. They keep the last module that owned them so that every skeleton item has one owner; the retirement is stated, not hidden. ASM-A6-api-15 covers this treatment.

9. For jobs, gave the `replacement` value from Arch v5 slide 44: a named Temporal Schedule in the owning service where the slide says Schedule, `event-started workflow` where an event starts it, and a retired successor where the slide retires the job (JOB-01, JOB-05, JOB-09). The WP rule that Quartz is retired is respected: no replacement text names Quartz or a qrtz_* table, and every job the old scheduler used to run is given a Temporal Schedule, an event-started workflow or a named retired successor (v5 slide 44 notes).

## Conflicts found and resolved

| # | Item | Winner | Loser | Ruling |
|---|---|---|---|---|
| 1 | GET and POST /cases/{caseId}/interactions | P1 | P3 (API Specification v4, TSD P3) | plan default ruling, interaction ledger |
| 2 | Four feature-flag paths | PLT | P2 (API Specification v4, TSD P2) | plan default ruling, platform library |
| 3 | Seven rule-package paths and four rule-version paths | P7 | P3 and P4 (API Specification v4 and v2/v3, TSD P3 and P4) | plan default ruling plus Arch v5 slide 14 |
| 4 | GET /admin/lists/{listCode} and four reference-load paths | P3 | P4 (API Specification v4, TSD P4) | plan default ruling, E1-042 and E1-043 |
| 5 | POST /admin/workflows/smoke | PLT | P3 and P4 (API Specification v4, TSD P3 and P4) | Arch v5 slide 44 JOB-22, task queue rwb-platform |
| 6 | Two asset valuation paths | S1 | S5 (API Specification v4, TSD S5) | Arch v5 slides 18 and 41, TSD S1 T3.1 |
| 7 | EV-18 TimerDue | P3 | durable timer (Arch v5 slide 42) | event retired, case timers stay in P3 |
| 8 | JOB-01 COLLINS load check | P1 | ACE team (Batch v4), no row in v5 | job retired, P1 read path is the successor |
| 9 | JOB-05 timer check | PLT | all (Arch v5 slide 44), platform administrator (Batch v4) | job retired, shared timer capability |
| 10 | JOB-09 file loads | P1 | ACE team (Batch v4), no row in v5 | job retired, P1 read path is the successor |
| 11 | JOB-10 WIN notices | P6 | rwb-comms plus integration (Arch v5 slide 44), platform administrator (Batch v4) | one owner, comms writes, integration delivers |
| 12 | JOB-11 outbox sender | PLT | every service (Arch v5 slide 44), platform administrator (Batch v4) | service template library |
| 13 | JOB-13 decision log copy | P7 | data lake copy (Batch v4) | Arch v5 slide 44 has no data lake, daily ledger seal |
| 14 | JOB-15 reporting extract | P9 | data lake copy (Batch v4) | Arch v5 slide 44 has no data lake, Airflow trigger |

No ruling was raised where the sources agree on the owner but name a different path: the Arch v5 contract path is stated in the `basis` column and the API Specification v4 path is kept as the item id (for example `/cases/{caseId}/route` against `/cases/{id}/route-proposals`, and `/debt-sale-lots` against `/lots`). Those do not move an owner, and ASM-A6-api-16 records the convention. No date was raised as a gap.

## Counts

| Section | Items | Items with a ruling |
|---|---|---|
| api | 156 | 25 |
| events | 30 | 1 |
| jobs | 22 | 7 |
| workflows | 15 | 0 |
| total | 223 | 33 |

Owner spread for the 156 api items: P3 22, P7 19, P1 18, P5 17, P6 11, P10 11, P2 11, S5 6, S9 6, S4 5, S6 5, PLT 5, S2 4, P4 4, S1 3, S8 2, S3 2, S7 2, P8 2, P9 1.

Gap register: 14 rows, all type Conflict and severity P2. Assumption register: 17 rows. Every cited ASM id exists in the register, and every gap row points at its ASM row and back.

## Verification

1. Id check in the generator: the 156 output ids equal the 156 unique skeleton api ids, with no missing item and no extra item; the 30 events, 22 jobs and 15 workflows equal the skeleton lists item for item; no id appears twice.
2. Owner check in the generator: every owner is one of the 20 allowed codes; no owner was left empty.
3. Citation check in the generator: every `asm` value in the output resolves to a row in the assumption register.
4. `python -I "22 Microservice Realignment/checks/run_all.py" --wp A6-api --quick` was run after the last edit to this log; the result is recorded in the check report for this WP. The quick set is C02, C03, C05, C12, C13 and C18. C02, C03 and C05 have no files to inspect because this WP writes no story; C12 and C13 inspect the four files for person names, email addresses and issue-tracker references; C18 checks that this log names no file outside the WP "Write only" list and that no legacy master changed.
5. No person name, email address, customer datum or issue-tracker reference is written in any of the four files. Role names only.

## Not done, on purpose

Sections one to nineteen of a story were not written: this WP produces an ownership map part only. No table owner was decided (that is A6-tables) and no event, job or workflow owner outside the three lists above was decided (that is A6-flows). No master file was written: `_work/msr/plan/ownership.json` and the ownership workbook belong to the Stage C assembler. No gap or assumption was numbered GAP-nnnn or ASM-nnnn; the candidate ids CG-A6-api-n and ASM-A6-api-n stand until step D1. No approval was sought; the part stands at Draft.
