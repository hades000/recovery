# Edit log B-ARCH-SVC — Service Catalog v1 and Service Template Specification v1

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026.
Sources read: `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 9 to 33, 38, 41 to 45), `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (slides 13 to 15), `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` (Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Parameters, Rulings), `_work/msr/plan/ownership.json`, `_work/msr/plan/split_plan.json` (stats and legacy counts), `_work/msr/plan/ids.json`, `Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, §R3, §R5, §R8, §R9), and the converted text under `_work/msr/extract/` (TSD S1 v2, TSD P8 v2, Non Functional Specification v3, Physical Schema v6).
Nothing read was edited.

## Files written

- `05 Technical architecture/Recovery Workbench Service Catalog v1.md`
- `05 Technical architecture/Recovery Workbench Service Catalog v1.xlsx`
- `05 Technical architecture/Recovery Workbench Service Template Specification v1.md`
- `_work/msr/gaps/B-ARCH-SVC.jsonl`
- `_work/msr/assumptions/B-ARCH-SVC.jsonl`
- `_work/msr/editlog/B-ARCH-SVC.md`
- Scratch: `_work/msr/docs/B-ARCH-SVC/data.py`, `build_catalog.py`, `build_template.py`, `write_registers.py`, `catalog_xlsx.md`, `ownership_rollup.json`, and the small verification scripts in the same folder.

## What was produced

Both documents are new at version 1; no earlier Service Catalog or Service Template Specification exists in the set (GAP-0140; ASM-0218). Both start with the §R8.1 header lines and both carry the change-log row `1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Both are status Draft, because no approval is available in this run.

### Service Catalog v1 (`.md` and `.xlsx`)

- 11 sections: purpose, how the catalogue is built, the 19 services at a glance, waves and service epics, naming, one section per service, resource ownership, call summary, conformance rules, open points, change log.
- 19 services, in Ownership Map order, each with code, name, wave, service epic, schema, login, REST base, Kafka topic, retry and dead-letter topics, task queue, Java package, the Architecture v5 "owns" text, the first API path, and a contract table by call type (REST, Kafka, Temporal, File, SQL view) for provided and consumed.
- 87 business tables assigned to the 19 services from the Ownership Map v1 Tables sheet, plus 6 PLT library tables created in every schema (93 rows in total, the whole map). Each row names the map ruling where one exists.
- Waves 0 to 4 and the 19 service epics, with no release date invented; the catalogue states that release dates live in the Release Plan and are tentative.
- The workbook has 10 sheets: Read me, Services, Resources, REST operations, Events published, Events consumed, Workflows and schedules, Naming, Waves, Call types.

### Service Template Specification v1 (`.md`)

- 22 sections: purpose, the twelve template parts, repository and module layout, naming, configuration and secrets, data layer, REST layer, event layer, Temporal layer, rules layer, decision record layer, access and authority, observability, error handling and resilience, security and supply chain, testing, delivery and runtime shape, Definition of Done, instantiation checklist with the 19 parameter sets, conformance register for the 19 services, open points, change log.
- Every standard that a source pins is copied unchanged: 2 s REST timeout, one GET retry with jitter, RFC 9457, Idempotency-Key, OpenAPI 3.1 and /v1, AsyncAPI 3.0 and CloudEvents 1.0 binary mode, 12 partitions with replication factor 3 and 7-day retention keyed on caseId, retry 1 min, 10 min and 1 h then `.dlt`, outbox every minute (JOB-11), Temporal 1.30 or later, namespace rwb-recovery, Continue-As-New at each stage end and at least every 28 days, parent close policy ABANDON, codec AES-GCM, KEDA 2.17 or later, rules under 300 ms, the 60 s agent fallback, the 5-minute ledger target, strict mode at the four points of no return, NFR-008, NFR-011, NFR-020, NFR-026, NFR-027, NFR-067 and NFR-068.

## Counts

- Gap rows: 10 candidate rows in `_work/msr/gaps/B-ARCH-SVC.jsonl` (GAP-0132 to 10). Numbered GAP-nnnn in step D1.
- Assumption rows: 10 candidate rows in `_work/msr/assumptions/B-ARCH-SVC.jsonl` (ASM-0210 to 10). Numbered ASM-nnnn in step D1.
- Placeholders in the documents: 17 occurrences of the §R9 placeholder string, covering 8 distinct pairs: CG-1/ASM-1 (S1 resources), CG-2/ASM-2 (P8 resources), CG-3/ASM-3 (stack versions), CG-4/ASM-4 (repository name and location), CG-5/ASM-5 (chart, release, registry), CG-6/ASM-6 (consumers of ApprovalDecided and ReportPublished), CG-7/ASM-7 (decision_record in every schema), CG-8/ASM-8 (pipeline tool). Each of the 10 gap rows has its assumption row.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ARCH-SVC --quick` — see the report under `22 Microservice Realignment/checks/reports/wp-B-ARCH-SVC-*.md`.

## Notes

- Owners are taken from the Ownership Map v1 for every resource: P1 rwb-source-data, P2 rwb-integration, P3 rwb-case, P4 rwb-access, P5 rwb-document, P6 rwb-comms, P7 rwb-decision, P8 rwb-payment, P9 rwb-reporting, P10 rwb-agent, S1 rwb-valuation, S2 rwb-treatment, S3 rwb-guarantee, S4 rwb-litigation, S5 rwb-asset, S6 rwb-debtsale, S7 rwb-writeoff, S8 rwb-deviation, S9 rwb-partner, and PLT for the shared library tables and the platform jobs.
- The workbook was created with `compat/office_write.py md-xlsx` from a markdown source in the scratch folder, because no earlier Service Catalog workbook exists to copy. No existing file was copied over or edited.
- The service-to-service call types follow Architecture v5 slide 13: route services reach the shared capabilities through Temporal and never REST, only rwb-source-data reads the ACE views, and the case router turns events into signals.
- No person name, email address or issue-tracker reference appears in any file written by this work package. The word used for the tracker is avoided entirely; no tracker call was made.
- The two events whose consumers the catalogue does not name are carried as placeholders rather than guessed (GAP-0137).
