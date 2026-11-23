# Edit log — WP B-ARCH-API

WP: `_work/msr/wp/B-ARCH-API.md`. Agent: aisdlc-msr-worker. Fanout: 0 (no subagents).
Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What was done

The API source is one OpenAPI 3.1 file, `05 Technical architecture/Recovery Workbench API Specification v4.yaml`
(4.0.0, 16 November 2026; 131 paths, 141 operations, 172 schemas, 9 responses, 1 security scheme). It was split
into the next version of the family, `05 Technical architecture/Recovery Workbench API Specification v5`: one
document per service (19), `gateway-bff.yaml`, `index.yaml`, and AsyncAPI 3.0 documents under `asyncapi/`.

Each operation was assigned with the `api` section of `_work/msr/plan/ownership.json`, which is the Endpoints
sheet of `Recovery Workbench Microservice Ownership Map v1.xlsx`. Every operation sits in exactly one document.
Twenty operations changed owner against the v4 `x-module`; each keeps `x-module` character for character and
carries `x-owner` and `x-owner-note`, and all twenty are listed in `index.yaml` under `x-owner-changes`:

- 2 interaction paths, P3 to P1 (ASM-0038)
- 4 feature-flag paths and POST /admin/workflows/smoke, P2/P3 to PLT (ASM-0039, ASM-0042)
- 7 rule-package paths, P3 to P7 (ASM-0040)
- 5 list and reference-load paths, P4 to P3 (ASM-0041)
- 1 asset valuation path, S5 to S1 (ASM-0043)

Nothing was edited in place: the v4 source, its `.html` rendering and every other existing file are unchanged.
The v5 folder did not exist before this WP.

The two header lines of Template and Rules §R8.1 are the first two lines of every file, as YAML comments, each
followed by the change-log row `5.0.0, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode /
DeepSeek v4.1 Flash`. Four YAML anchors/aliases of the source (`&id001`, `*id001`, `&id002`, `*id002`) were
expanded in place so that every split document parses on its own; the data is identical.

Verification: every one of the 141 operations, all 172 component schemas and all 9 responses of v4 were compared
field by field against v5 (only `x-owner` and `x-owner-note` added); no difference was found. All 21 OpenAPI and
20 AsyncAPI documents parse, and every `$ref` inside them resolves.

## Files written

- `05 Technical architecture/Recovery Workbench API Specification v5/index.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/gateway-bff.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-source-data.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-integration.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-case.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-document.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-comms.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-payment.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-reporting.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-agent.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-valuation.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-treatment.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-guarantee.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-litigation.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-debtsale.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-writeoff.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-deviation.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/rwb-partner.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-source-data.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-integration.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-case.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-access.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-document.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-comms.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-decision.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-payment.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-reporting.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-agent.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-valuation.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-treatment.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-guarantee.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-litigation.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-asset.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-debtsale.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-writeoff.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-deviation.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-partner.asyncapi.yaml`
- `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb.decision-record.v1.asyncapi.yaml`
- `_work/msr/gaps/B-ARCH-API.jsonl`
- `_work/msr/assumptions/B-ARCH-API.jsonl`
- `_work/msr/editlog/B-ARCH-API.md`

Scratch (not part of the deliverable), under `_work/msr/docs/B-ARCH-API/`: `inspect_api.py`, `inspect_own.py`,
`compare_owners.py`, `analyse_split.py`, `check_layout.py`, `gen_api_v5.py`, `verify_api_v5.py`, `ops.json`.

## Counts

- Operations: 141 in v4, 141 in v5, none duplicated, none missing. Per document: rwb-case 22, rwb-document 17,
  rwb-decision 15, rwb-source-data 12, rwb-comms 11, rwb-agent 11, rwb-integration 9, rwb-partner 6, rwb-litigation 5,
  rwb-debtsale 5, rwb-access 4, rwb-treatment 4, rwb-asset 4, gateway-bff 5 (PLT), rwb-payment 2, rwb-guarantee 2,
  rwb-deviation 2, rwb-writeoff 2, rwb-valuation 2, rwb-reporting 1.
- Component schemas: 172 (7 of them referenced by no operation, kept in the owning service document).
- Responses: 9. Security schemes: 1. Tags: 16.
- AsyncAPI 3.0 documents: 20 (one per service plus the shared `rwb.decision-record.v1`).
- Gap rows (`CG-B-ARCH-API-*`): 5. Assumption rows (`ASM-B-ARCH-API-*`): 10.

## Gaps and assumptions

Gaps: GAP-0094 (no BFF composite route in the source, P2), GAP-0095 (PLT has no service document
and no base path, P3), GAP-0096 (no event payload types, P2), GAP-0097 (no event for rwb-reporting,
dash topic and wildcard name in the guarantee row, P3), GAP-0098 (seven unreferenced schemas, P3).
Assumptions: ASM-0158 to ASM-0167, including Draft status with no approval recorded
(ASM-0167).

## Notes for the assembler

- Only the assembler writes master files; this WP wrote no master file.
- Only step D1 numbers gap and assumption rows; the local ids `CG-B-ARCH-API-n` and `ASM-B-ARCH-API-n` are the
  candidate ids and are cited as such in the documents.
- Contract citations used from the ownership work: ASM-0038 to ASM-0043, which already exist in
  `_work/msr/assumptions/A6-api.jsonl`.
