# Edit log B-ARCH-CON — Service Contract Catalog v1

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026.

## Sources read

| Source | Used for |
|---|---|
| `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` | Slides 13 to 20 (the call-type matrix and the 19 service contracts), slides 41 to 44 (service, event and job catalogues), slide 11 (the call-type standards) |
| `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` | Slides 11 to 14 (runtime, the five Temporal layers, the workflow model, the rule evaluation step) |
| `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` | Services, Endpoints, Events, Workflows and activities, Jobs, Tables, Rulings — the owner of every element |
| `_work/msr/plan/ownership.json` | The same owners in machine form: 156 endpoints, 30 events, 15 workflows, 22 jobs, 93 tables |
| `_work/msr/plan/ids.json` | The allocated decision, ADR and DL IDs (D-RCV-60 confirmed) |
| `_work/msr/plan/split_plan.json` | `stats` and `legacy` only, for the wave and story context |
| `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` | §R1, §R3, §R5, §R8, §R9 |

No source file was edited. No issue tracker, wiki, repository or web call was made.

## Files written

- `05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md`
- `05 Technical architecture/Recovery Workbench Service Contract Catalog v1.xlsx`
- `_work/msr/gaps/B-ARCH-CON.jsonl`
- `_work/msr/assumptions/B-ARCH-CON.jsonl`
- `_work/msr/editlog/B-ARCH-CON.md`
- `_work/msr/docs/B-ARCH-CON/build.py`
- `_work/msr/docs/B-ARCH-CON/catalog_xlsx.md`
- `_work/msr/docs/B-ARCH-CON/patch1.py`
- `_work/msr/docs/B-ARCH-CON/patch2.py`
- `_work/msr/docs/B-ARCH-CON/patch3.py`
- `_work/msr/docs/B-ARCH-CON/patch4.py`
- `_work/msr/docs/B-ARCH-CON/patch5.py`
- `_work/msr/docs/B-ARCH-CON/patch6.py`
- `_work/msr/docs/B-ARCH-CON/patch7.py`
- `_work/msr/docs/B-ARCH-CON/patch8.py`

## What the document contains

- Header per Template and Rules §R8.1 (two lines, character for character), document control, and the change-log row `1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
- Section 4 reproduces the Architecture v5 slide 13 call-type matrix in full: 19 rows, 22 columns, the combined cells kept as printed, the legend, and the four rules that come with it.
- Section 5 is the contract inventory: 141 provider and consumer pairs derived from the matrix and the service contracts, each with its interface, its contract artefact, its dependency class (C, X, and H once) and its source.
- Section 6 is the contract by service, 19 sections in Ownership Map order, each with the identity table, the contracts provided, the contracts consumed, the REST operations the map assigns to the service under its own base path, and the schema boundary.
- Section 7 registers the artefacts each service publishes (OpenAPI 3.1, AsyncAPI 3.0, activity contract jar), the artefact rules and the shared platform contracts. Section 8 states the dependency classes, the decoupling patterns as contract rules, the one-hop rule and the edge contracts. Section 9 is the 12 contract conformance rules with the test that proves each one. Section 10 is the contract change control. Section 11 is the open points.
- The workbook has 12 sheets: Read me, Services, Call type matrix, Contract pairs, REST operations, Events, Temporal contracts, Jobs, Resources owned, Conformance, Open points, Change log.

## Ownership

Every owner comes from the Ownership Map v1 (Services, Endpoints, Events, Workflows and activities, Jobs, Tables, Rulings sheets) and from `_work/msr/plan/ownership.json`. The 19 service identities (code, name, wave, schema, REST base, topic, task queue) are read from the map's Services sheet at build time. The 18 tables the map assigns to P1, the single proceeds table of P8 and the 6 platform tables follow the map and its rulings without change.

## Counts

- Gap rows: 8 candidate rows in `_work/msr/gaps/B-ARCH-CON.jsonl` (GAP-0099 to 8). Numbered GAP-nnnn in step D1.
- Assumption rows: 10 candidate rows in `_work/msr/assumptions/B-ARCH-CON.jsonl` (ASM-0168 to 10). Numbered ASM-nnnn in step D1.
- Placeholders in the document: 5 values, each paired with a gap and an assumption row — the two unnamed event consumers (CG-4/ASM-4), the contract jar coordinates (CG-3/ASM-3), the registry product (CG-5/ASM-5) and the S5 to P6 interface (CG-8/ASM-8).
- Contracts: 141 pairs — REST 16, Kafka 82, Temporal 38, Nexus 1, File 3, SQL view 1. 131 pairs are provided by a service and 124 are consumed by a service; the rest have the platform, an edge or All 19 services on one side.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ARCH-CON --quick` — C02, C03, C05, C12, C13 and C18 all PASS. The report is under `22 Microservice Realignment/checks/reports/wp-B-ARCH-CON-*.md`.

## Notes

- Release dates are not held in this document; the Release Plan keeps them unchanged and every one is tentative (U7, DL48). The only date written here is the document date, 22 November 2026, and the change-log date.
- No person name appears in any file written by this work package; every owner is a role.
- The `.xlsx` is a new file, not a copy of an earlier workbook: no Service Contract Catalog family exists before v1.
- The five call types are named as Architecture v5 names them; Nexus is carried as its own call type because slide 18 uses it once, for the restructure calculator.
