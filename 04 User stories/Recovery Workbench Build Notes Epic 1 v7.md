SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench build notes, Epic 1

### Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| v7 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

The change-log row is v7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Version 6 of these notes is dated 16 November 2026. Version 7 keeps its 72 story notes word for word and adds a service-and-lane note, a table-and-owner note and a dependency note to each one.

> **D-RCV-60.** This version applies decision D-RCV-60. The Workbench runs as 19 services inside ACE, each with its own schema `rwb_<name>`, one login of its own, REST base `/api/recovery/<name>/v1`, Kafka topic `rwb.<name>.events.v1`, Temporal task queue `rwb-<name>` in namespace `rwb-recovery`, and the service epic `RWB-SVC-<code>`. Only rwb-source-data reads the 30 `recovery.v_ace_*` views; every other service asks it through its contract. The rule registry moves to rwb-decision and each owning service evaluates locally with the embedded Drools kit. Temporal Schedules replace Quartz in the owning service, and the data lake is removed. Epic 1 work already built or in build is not changed until its delta story is picked up (Template and Rules §R6).

> **D-RCV-36.** This version applies decision D-RCV-36. Temporal runs the case lifecycle from Epic 3, with case data in the ACE database, and Drools evaluates rules from versioned rule packages. RWB-E1-029, RWB-TE-005 and RWB-E1-048 are retired; their work moved to RWB-E1-073 and RWB-E2-041. The new configuration notes RWB-E1-070 to RWB-E1-073 sit before RWB-E1-018 in the build order.

These notes follow the 72 stories of Recovery Workbench User Stories Epic 1 v9. Version 4 walked every flow step, and most of those steps were load or job steps. The ACE re-base of 15 November 2026 (D-RCV-35, ADR-010) removed that estate: the Workbench takes no inbound source data, ACE ingests every source, and the recovery module reads ACE only through the 30 SELECT-only `recovery.v_ace_*` views. In this version each story carries four notes in place of the old steps, and a new configuration story adds its build order and main risk.

| Note | What it answers |
|---|---|
| View | Which views or Workbench tables the story reads, and what it takes from each |
| Grant | Which role holds which privilege, and what the story may not do |
| Freshness | Which data product the read belongs to, how its business date and stamp are set, and what a stale product does |
| Boundary | Where the module boundary falls and which rule fails the build when a class crosses it |
| Service and lane | Which services own the story, which new story IDs carry it, which lane each one sits in, and when it is ready to start (D-RCV-60) |
| Tables and owner | Which service owns each table the note names, and in which schema (Ownership Map v1) |
| Dependencies | The decoupling patterns applied and the H, C, I and X dependencies of each new story (D-RCV-60) |

The story remains the specification. Where these notes and the story differ, the story governs. Section 13 of each story is its solution plan and section 16 its tests; where version 4 described a Workbench step that the re-base did not change, that section still carries it, and where it described a load or a job, the four notes replace it. RWB-E1-069 owns the view list, the grants and the view conformance test. RWB-ACE-001 owns the 14 Tier 2 tables and the 12 columns that Section B needs, and nothing in the Workbench creates or alters them.

## Epic 1 and the 19 services

Thirteen of the 19 services take Epic 1 stories; S1 rwb-valuation, S2 rwb-treatment, S3 rwb-guarantee, S4 rwb-litigation, S6 rwb-debtsale and S7 rwb-writeoff have none. The 298 Epic 1 stories are 212 service stories, 52 integration stories and 34 platform stories. Nine of the thirteen are wave 1 services; P8 rwb-payment, S5 rwb-asset, S8 rwb-deviation and S9 rwb-partner take their Epic 1 stories in wave 1 by the W-MAP rule, ahead of their own Arch v5 wave (GAP-3171 to GAP-3174).

| Code | Service | Schema | Arch v5 wave | Epic 1 stories | Epic 1 lanes | Day-1 stories |
|---|---|---|---|---|---|---|
| P1 | `rwb-source-data` | `rwb_source_data` | 1 | 34 | 15 lanes: 1 (`CG-W1`), 14 (`L-P1-*`) | 24 |
| P2 | `rwb-integration` | `rwb_integration` | 1 | 5 | 5 lanes: 1 (`CG-W1`), 4 (`L-P2-*`) | 5 |
| P3 | `rwb-case` | `rwb_case` | 1 | 44 | 23 lanes: 1 (`CG-W1`), 22 (`L-P3-*`) | 36 |
| P4 | `rwb-access` | `rwb_access` | 1 | 26 | 22 lanes: 1 (`CG-W1`), 21 (`L-P4-*`) | 24 |
| P5 | `rwb-document` | `rwb_document` | 1 | 38 | 21 lanes: 1 (`CG-W1`), 20 (`L-P5-*`) | 27 |
| P6 | `rwb-comms` | `rwb_comms` | 1 | 16 | 11 lanes: 1 (`CG-W1`), 10 (`L-P6-*`) | 13 |
| P7 | `rwb-decision` | `rwb_decision` | 1 | 20 | 18 lanes: 1 (`CG-W1`), 17 (`L-P7-*`) | 19 |
| P8 | `rwb-payment` | `rwb_payment` | 2 | 1 | 1 lane: 1 (`L-P8-*`) | 1 |
| P9 | `rwb-reporting` | `rwb_reporting` | 1 | 3 | 3 lanes: 1 (`CG-W1`), 2 (`L-P9-*`) | 3 |
| P10 | `rwb-agent` | `rwb_agent` | 1 | 17 | 6 lanes: 1 (`CG-W1`), 5 (`L-P10-*`) | 11 |
| S1 | `rwb-valuation` | `rwb_valuation` | 3 | 0 | none | none |
| S2 | `rwb-treatment` | `rwb_treatment` | 2 | 0 | none | none |
| S3 | `rwb-guarantee` | `rwb_guarantee` | 3 | 0 | none | none |
| S4 | `rwb-litigation` | `rwb_litigation` | 3 | 0 | none | none |
| S5 | `rwb-asset` | `rwb_asset` | 2 | 1 | 1 lane: 1 (`L-S5-*`) | 1 |
| S6 | `rwb-debtsale` | `rwb_debtsale` | 3 | 0 | none | none |
| S7 | `rwb-writeoff` | `rwb_writeoff` | 4 | 0 | none | none |
| S8 | `rwb-deviation` | `rwb_deviation` | 2 | 5 | 5 lanes: 5 (`L-S8-*`) | 5 |
| S9 | `rwb-partner` | `rwb_partner` | 4 | 2 | 2 lanes: 2 (`L-S9-*`) | 2 |

The platform stories of Epic 1 sit in wave 0 lanes (`CG-W0` and `L-PLT-*`) with the business epic EP01 as their tag, which is how a wave 1 business story gets platform work on Day 1 (Template and Rules §R5.7).

Every team type has Day-1 work in Epic 1, as §R5.7 rule 6 requires. The counts below are the Epic 1 stories whose ready-to-start value is Day 1, by suggested owner.

| Team type | Day-1 Epic 1 stories | Example stories |
|---|---|---|
| TechX | 213 | `RWB-ITG-E1001-ITG`, `RWB-ITG-E1002-ITG`, `RWB-ITG-E1007-ITG` |
| ACE team | 8 | `RWB-P1-ACE001-DB`, `RWB-P1-E1016-DB`, `RWB-P1-E1065-DB` |
| SCB IT infrastructure | 7 | `RWB-P10-E1058-INF`, `RWB-P2-E1007-INF`, `RWB-P3-E1073-INF` |
| DevOps team | 27 | `RWB-P1-E1002-OPS`, `RWB-P1-E1011-OPS`, `RWB-P1-E1015-OPS` |
| QA team | 2 | `RWB-ITG-TE009-ITG`, `RWB-ITG-TE010-ITG` |

## The 30 views and their sources

The 16 Section A views ship in V0002 and read the 21 ACE tables that exist today. The 14 Section B views ship in V0003 and read the tables that RWB-ACE-001 adds. Together they hold 304 columns, each with a dictionary row in the 122-object, 1,366-field dictionary of V0001.

Under D-RCV-60 the views stay with P1 rwb-source-data and no other service names them (DP-05; Arch v5 slide 45: only rwb-source-data reads the 30 `recovery.v_ace_*` views). Every other service reaches ACE data through P1's REST contract (`GET /customers/{id}`, `/accounts/{id}`, `/collateral/{id}`, `/payments?accountId=`, `/freshness`) or a P1 Temporal activity (`listEligibleAccounts`, `snapshot(page)`), and listens to `AceDataReady` and `AceDataLate`.

| View | ACE source | Fields | Section | Read by (D-RCV-60) |
|---|---|---:|---|---|
| `v_ace_account` | account | 42 | A | P1 `rwb_source_data` only |
| `v_ace_payment` | payment | 12 | A | P1 `rwb_source_data` only |
| `v_ace_customer` | customer | 20 | A | P1 `rwb_source_data` only |
| `v_ace_contact` | phone, email, address | 9 | A | P1 `rwb_source_data` only |
| `v_ace_ca_relation` | ca_relation | 5 | A | P1 `rwb_source_data` only |
| `v_ace_aa_relation` | aa_relation | 2 | A | P1 `rwb_source_data` only |
| `v_ace_collateral` | collateral | 8 | A | P1 `rwb_source_data` only |
| `v_ace_asset` | asset | 9 | A | P1 `rwb_source_data` only |
| `v_ace_efs_action` | efs_action | 20 | A | P1 `rwb_source_data` only |
| `v_ace_efs_action_code` | efs_action_code | 3 | A | P1 `rwb_source_data` only |
| `v_ace_efs_assignment` | efs_assignment | 9 | A | P1 `rwb_source_data` only |
| `v_ace_bucket_log` | bucket_log_snapshot | 6 | A | P1 `rwb_source_data` only |
| `v_ace_product` | product | 5 | A | P1 `rwb_source_data` only |
| `v_ace_branch` | branch | 4 | A | P1 `rwb_source_data` only |
| `v_ace_holiday` | bot_holiday | 5 | A | P1 `rwb_source_data` only |
| `v_ace_plan` | ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation, ai_recommended_plan | 18 | A | P1 `rwb_source_data` only |
| `v_ace_batch_status` | ace_batch_run | 9 | B | P1 `rwb_source_data` only |
| `v_ace_valuation` | valuation | 9 | B | P1 `rwb_source_data` only |
| `v_ace_collateral_detail` | collateral_detail | 12 | B | P1 `rwb_source_data` only |
| `v_ace_npa_asset` | npa_asset | 12 | B | P1 `rwb_source_data` only |
| `v_ace_npa_sale` | npa_sale | 11 | B | P1 `rwb_source_data` only |
| `v_ace_lawsuit` | lawsuit | 13 | B | P1 `rwb_source_data` only |
| `v_ace_hearing` | hearing | 7 | B | P1 `rwb_source_data` only |
| `v_ace_pod` | pod_receipt | 10 | B | P1 `rwb_source_data` only |
| `v_ace_write_off` | gl_write_off | 9 | B | P1 `rwb_source_data` only |
| `v_ace_score` | collins_score | 10 | B | P1 `rwb_source_data` only |
| `v_ace_party_product` | party_product | 6 | B | P1 `rwb_source_data` only |
| `v_ace_credit_decision` | credit_decision | 8 | B | P1 `rwb_source_data` only |
| `v_ace_esign` | esign_request | 7 | B | P1 `rwb_source_data` only |
| `v_ace_iam_group` | iam_group | 4 | B | P1 `rwb_source_data` only |

## The grants

Two database roles carry the read path. Their names are fixed in the Environment and Deployment Design, and no story invents a third.

| Role | Holds | On what | Set by |
|---|---|---|---|
| `ace_view_owner` | USAGE and SELECT | The 21 Section A tables and the 14 Section B tables in `public`; owner of the 30 views | V0002 and V0003 (RWB-E1-069), with the SELECT on the Tier 2 tables granted to it by RWB-ACE-001 |
| `recovery_svc` | USAGE on `recovery` and SELECT on each view | The 30 views only; no privilege of any kind in `public` | V0002 for Section A, V0003 for Section B |
| `recovery_svc` | DML on the Workbench tables | The 92 tables of schema `recovery` | V0001 (RWB-E1-001) |
| `PUBLIC` | Nothing | Nothing | `REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC` in V0002 |

No view takes an INSERT, UPDATE, DELETE or TRUNCATE. A story that changes a Workbench decision writes its own table; a story that appears to change an ACE record writes an extension table keyed by the ACE business key.

**D-RCV-60.** `recovery_svc` is the login of the as-built monolith and it ends at cutover (ADR-014). DP-02 gives every service one login of its own with DML in its own schema only and no privilege of any kind in another schema; the login names are set by the ACE DB stories of RWB-PLT-DB and are not fixed in the source documents (GAP-3155; ASM-5545). `ace_view_owner` and the 30 views stay with P1 (GAP-3156).

| Code | Service | Its own schema | Holds there | Holds elsewhere |
|---|---|---|---|---|
| P1 | `rwb-source-data` | `rwb_source_data` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | SELECT on the 30 `recovery.v_ace_*` views |
| P2 | `rwb-integration` | `rwb_integration` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P3 | `rwb-case` | `rwb_case` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P4 | `rwb-access` | `rwb_access` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P5 | `rwb-document` | `rwb_document` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P6 | `rwb-comms` | `rwb_comms` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P7 | `rwb-decision` | `rwb_decision` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P8 | `rwb-payment` | `rwb_payment` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P9 | `rwb-reporting` | `rwb_reporting` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| P10 | `rwb-agent` | `rwb_agent` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S1 | `rwb-valuation` | `rwb_valuation` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S2 | `rwb-treatment` | `rwb_treatment` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S3 | `rwb-guarantee` | `rwb_guarantee` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S4 | `rwb-litigation` | `rwb_litigation` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S5 | `rwb-asset` | `rwb_asset` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S6 | `rwb-debtsale` | `rwb_debtsale` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S7 | `rwb-writeoff` | `rwb_writeoff` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S8 | `rwb-deviation` | `rwb_deviation` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |
| S9 | `rwb-partner` | `rwb_partner` | DML on its own tables, plus the library outbox, inbox and decision-record tables (DP-09) | Nothing |

## Freshness

A product is fresh when ACE reports its batch for the business date COMPLETE. RWB-E1-015 writes one `data_product_load` row per product per business date from `v_ace_batch_status`, and the `ace_batch_run` record that RWB-ACE-001 adds carries the business date, the status and the record count. A read that finds no COMPLETE batch keeps the last good business date, marks the product stale and raises MSG-P1-001. The Workbench products (DP03, DP04, DP08, DP09, DP10, DP12 and DP14) are stamped from their own last committed write, because no ACE batch produces them.

| Product | Data | Cycle | Expected by | Owning service (D-RCV-60) |
|---|---|---|---|---|
| DP01 | Account and arrears | DAILY | 08:00 | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP02 | Customer and party | DAILY | 08:00 | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP03 | Case and ownership | ON_CHANGE | As it changes | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP04 | Treatment and offers | ON_CHANGE | As it changes | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP05 | Contact and promises | DAILY | 08:00 | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP06 | Collateral and assets | WEEKLY | MON 08:00 | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP07 | Legal events and cases | DAILY | 08:00 | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP08 | Partner performance | ON_CHANGE | As it changes | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP09 | Debt sale | ON_CHANGE | As it changes | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP10 | Documents and extracted fields | ON_CHANGE | As it changes | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP11 | Scores and route economics | DAILY | 08:00 | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP12 | Decision log | ON_CHANGE | As it changes | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP13 | Money and closure | DAILY | 08:00 | Not specified in the source documents (GAP-3154; ASM-5544) |
| DP14 | Reference data | ON_CHANGE | As it changes | Not specified in the source documents (GAP-3154; ASM-5544) |

**D-RCV-60.** The freshness stamp stays with P1 rwb-source-data, which publishes it through `GET /freshness` and the `AceDataReady` and `AceDataLate` events (Arch v5 slide 15). A service reads the business date from that contract and raises its own stale flag; no service writes `data_product_load`, and no service reads `v_ace_batch_status` itself. Which service owns each of the 14 products is not fixed in the source documents (GAP-3154; ASM-5544).

## The boundary

The boundary has four parts, and each one fails loudly.

- **No copy.** The recovery schema holds no ACE source table. The 88 Workbench tables hold Workbench records; the four extension tables hold a Workbench decision about an ACE record; the 30 views are the only read of ACE data.
- **No constraint into `public`.** No foreign key, check or unique constraint in `recovery` names a table or type outside it, because ACE cascades deletes on `account`. A link is a varchar(255) business key with no foreign key.
- **No direct read.** Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table. The allowed objects are the 30 view names in `recovery-modules.yaml`, not a literal list in the test.
- **No write to a view.** `recovery_svc` holds SELECT only; the view conformance test of RWB-E1-069 fails if it finds a write privilege or a privilege in `public`.

**D-RCV-60.** The boundary is applied per service. No service schema holds an ACE source table and no constraint names another schema or a `public` type; a cross-service link is an ID in a varchar(255) column, and a cross-service read is a contract call (ADR-014, ADR-020). BND-6 runs in each service's build against the same `recovery-modules.yaml`, and only P1 may name a `recovery.v_ace_*` view. The four extension tables and the 30 views stay with P1.

## What this version removes from version 4

| Removed | Why | Where it went |
|---|---|---|
| RWB-E1-003 ALS daily extract load | ACE ingests ALS | ACE ingestion; the Workbench reads `v_ace_account` and `v_ace_payment` |
| RWB-E1-004 EFS extract load | ACE ingests EFS | ACE ingestion; the Workbench reads `v_ace_efs_action` |
| RWB-E1-005 Excel and SharePoint inventory | No tracker estate to inventory | Cutover plan |
| RWB-E1-006 Data quality rules v1 | ACE runs the ingestion checks | ACE ingestion; the daily gate is in RWB-E1-015 |
| RWB-E1-009 CCMS and SVAF loads | ACE ingests CCMS and SVAF | ACE ingestion; `v_ace_collateral`, `v_ace_valuation` and Section B |
| RWB-E1-010 Excel and SharePoint loads | No tracker estate to load | Cutover plan |
| RWB-E1-012 Retire local copies | No local copy to retire | Cutover plan |
| RWB-E1-051 Legacy feed jobs on ADF and Control-M | No ADF job remains | ACE ingestion |

D-RCV-36 also retires RWB-E1-029, RWB-TE-005 and RWB-E1-048. Their notes are removed and the work is carried by RWB-E1-073 and RWB-E2-041. The job steps that remain are Workbench jobs: allocation, rebalancing, the letter and notice runs, OCR and the agent runs. Every one of them reads its source through a view and writes only a Workbench table. The pipeline steps that remain are migrations, the dictionary conformance test, the view conformance test, the boundary test and the PDPA lint.

## What D-RCV-60 retires, preserves and keeps in Epic 1

| Group | Stories | Rule in this version |
|---|---|---|
| Built or in build, preserved | RWB-TE-001, TE-002, TE-003, E1-042, E1-043, E1-044 | The as-built story keeps its base ID with `preserved=true`; the microservice change is a separate delta story (`-2` copy, or a CON or OPS story). No change to built code until a delta story is picked up. |
| Must change | RWB-E1-001 | The single recovery schema is kept as built; the split into `rwb_*` schemas is new work (RWB-PLT-NF06-DB and the per-service DB stories). |
| Retired | RWB-E1-014 (no data lake, DP-17); RWB-TE-007 (Quartz replaced by Temporal Schedules, DP-10) | No new story. Dependencies on E1-014 are dropped; dependencies on TE-007 point to RWB-PLT-E1071-CON. |
| Already cancelled | E1-003, 004, 005, 006, 009, 010, 012, 029, 048, 051; TE-005 | No new story. |
| No impact | E1-024, 025, 026, 033, 034, 038, 040, 041, 045, 053, 060, 061, 068; TE-010, TE-012 | Moved to their epic with content unchanged. |

## The 72 story notes, by legacy key

One row per source note. The new stories, the lane and the ready-to-start position come from the Service Story Catalog v1 and the split plan. The release of every story of these 72 notes is 30 November 2026 (tentative); the two non-functional integration stories RWB-ITG-TE009-ITG and RWB-ITG-TE010-ITG are dated 31 December 2026 (tentative) and are not sections of these notes. The platform stories sit in wave 0.

| Legacy key | Story note | Disposition | Primary | New stories | Lane(s) | Ready to start |
|---|---|---|---|---|---|---|
| `RWB-E1-001` | Recovery tables for the 14 data products | Must change | P1 | integration `RWB-ITG-E1001-ITG`; rwb-source-data `RWB-P1-E1001-APP`; rwb-access `RWB-P4-E1001-APP`; rwb-decision `RWB-P7-E1001-APP`; rwb-payment `RWB-P8-E1001-APP` | L-ITG-W1, L-P1-A, L-P4-K, L-P7-A, L-P8-B | Day 1 for 5 of 5 |
| `RWB-E1-002` | Case list v1 with case ID, owner and queue | Split (rework) | P1 | integration `RWB-ITG-E1002-ITG`; rwb-source-data `RWB-P1-E1002-APP`, `RWB-P1-E1002-CON`, `RWB-P1-E1002-OPS`; rwb-case `RWB-P3-E1002-APP` | CG-W1, L-ITG-W1, L-P1-A, L-P1-F, L-P3-B | Day 1 for 4 of 5; `RWB-P1-E1002-APP` after RWB-P1-E1069-APP, RWB-P1-E1015-APP |
| `RWB-E1-007` | Integration adapters for outbound files | Split (rework) | P2 | integration `RWB-ITG-E1007-ITG`; rwb-integration `RWB-P2-E1007-APP`, `RWB-P2-E1007-CON`, `RWB-P2-E1007-INF`, `RWB-P2-E1007-OPS`; rwb-case `RWB-P3-E1007-APP`; rwb-access `RWB-P4-E1007-APP`; rwb-document `RWB-P5-E1007-APP`; rwb-comms `RWB-P6-E1007-APP` | CG-W1, L-ITG-W1, L-P2-A, L-P2-B, L-P2-C, L-P3-C, L-P4-L, L-P5-B, L-P6-B | Day 1 for 9 of 9 |
| `RWB-E1-008` | Decision log store v1, append only and hash chained | Split (rework) | P7 | integration `RWB-ITG-E1008-ITG`; rwb-access `RWB-P4-E1008-APP`; rwb-decision `RWB-P7-E1008-APP`, `RWB-P7-E1008-CON`, `RWB-P7-E1008-DB`, `RWB-P7-E1008-OPS` | CG-W1, L-ITG-W1, L-P4-M, L-P7-B, L-P7-C, L-P7-D | Day 1 for 6 of 6 |
| `RWB-E1-011` | Reconciliation and data quality report | Split (rework) | P1 | integration `RWB-ITG-E1011-ITG`; rwb-source-data `RWB-P1-E1011-APP`, `RWB-P1-E1011-CON`, `RWB-P1-E1011-OPS`; rwb-case `RWB-P3-E1011-APP`; rwb-comms `RWB-P6-E1011-APP`; rwb-asset `RWB-S5-E1011-APP` | CG-W1, L-ITG-W1, L-P1-A, L-P1-G, L-P3-D, L-P6-C, L-S5-A | Day 1 for 6 of 7; `RWB-P1-E1011-APP` after RWB-P1-E1015-APP, RWB-P1-E1069-APP |
| `RWB-E1-013` | Baseline measures | Split (rework) | P9 | integration `RWB-ITG-E1013-ITG`; rwb-source-data `RWB-P1-E1013-APP`; rwb-case `RWB-P3-E1013-APP`; rwb-reporting `RWB-P9-E1013-APP`, `RWB-P9-E1013-CON`, `RWB-P9-E1013-OPS` | CG-W1, L-ITG-W1, L-P1-H, L-P3-E, L-P9-A, L-P9-B | Day 1 for 6 of 6 |
| `RWB-E1-014` | Decision log copy to the data lake | Retired (D-RCV-60) | none | none | none | none |
| `RWB-E1-015` | Freshness stamp per data product | Split (rework) | P1 | integration `RWB-ITG-E1015-ITG`; rwb-source-data `RWB-P1-E1015-APP`, `RWB-P1-E1015-CON`, `RWB-P1-E1015-OPS` | CG-W1, L-ITG-W1, L-P1-A, L-P1-I | Day 1 for 3 of 4; `RWB-P1-E1015-APP` after RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| `RWB-E1-016` | Access control per data product and catalog entries | Split (rework) | P1 | integration `RWB-ITG-E1016-ITG`; rwb-source-data `RWB-P1-E1016-APP`, `RWB-P1-E1016-CON`, `RWB-P1-E1016-DB`; rwb-access `RWB-P4-E1016-APP`; rwb-document `RWB-P5-E1016-APP` | CG-W1, L-ITG-W1, L-P1-A, L-P1-J, L-P4-N, L-P5-C | Day 1 for 5 of 6; `RWB-P1-E1016-APP` after RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP |
| `RWB-E1-017` | Retention and archive rule for the data store | Split (rework) | P1 | integration `RWB-ITG-E1017-ITG`; rwb-source-data `RWB-P1-E1017-APP`, `RWB-P1-E1017-CON`, `RWB-P1-E1017-OPS`; rwb-document `RWB-P5-E1017-APP`; rwb-decision `RWB-P7-E1017-APP` | CG-W1, L-ITG-W1, L-P1-A, L-P1-K, L-P5-D, L-P7-E | Day 1 for 5 of 6; `RWB-P1-E1017-APP` after RWB-P1-E1001-APP, RWB-P1-E1064-APP |
| `RWB-E1-070` | Temporal platform on the ACE AKS clusters | Split (rework) | PLT | integration `RWB-ITG-E1070-ITG`; platform `RWB-PLT-E1070-APP`, `RWB-PLT-E1070-CON` | CG-W0, L-ITG-W1, L-PLT-WF-D | Day 1 for 3 of 3 |
| `RWB-E1-071` | Temporal worker and SDK in the recovery module | Split (rework) | PLT | platform `RWB-PLT-E1071-APP`, `RWB-PLT-E1071-CON` | CG-W0, L-PLT-WF-E | Day 1 for 2 of 2 |
| `RWB-E1-072` | Drools runtime and rule package store | Split (rework) | PLT | platform `RWB-PLT-E1072-APP`, `RWB-PLT-E1072-CON` | CG-W0, L-PLT-LIB-I | Day 1 for 2 of 2 |
| `RWB-E1-073` | Rule authoring, validation, test scenarios, approval and rollback in Drools | Split (rework) | P3 | integration `RWB-ITG-E1073-ITG`; rwb-integration `RWB-P2-E1073-APP`; rwb-case `RWB-P3-E1073-APP`, `RWB-P3-E1073-CON`, `RWB-P3-E1073-INF`; rwb-comms `RWB-P6-E1073-APP`; rwb-decision `RWB-P7-E1073-APP` | CG-W1, L-ITG-W1, L-P2-D, L-P3-F, L-P3-W, L-P6-J, L-P7-P | Day 1 for 7 of 7 |
| `RWB-E1-018` | Case ID issuance and case record v1 | Split (rework) | P3 | integration `RWB-ITG-E1018-ITG`; rwb-source-data `RWB-P1-E1018-APP`; rwb-case `RWB-P3-E1018-APP`, `RWB-P3-E1018-CON`, `RWB-P3-E1018-OPS`; rwb-access `RWB-P4-E1018-APP`; rwb-document `RWB-P5-E1018-APP`; rwb-decision `RWB-P7-E1018-APP` | CG-W1, L-ITG-W1, L-P1-L, L-P3-F, L-P3-G, L-P4-O, L-P5-E, L-P7-F | Day 1 for 7 of 8; `RWB-P3-E1018-APP` after RWB-P3-E1073-APP |
| `RWB-E1-019` | Roles, teams and queues as data | Split (rework) | P3 | integration `RWB-ITG-E1019-ITG`; rwb-case `RWB-P3-E1019-APP`, `RWB-P3-E1019-CON`, `RWB-P3-E1019-DB`; rwb-access `RWB-P4-E1019-APP`; rwb-comms `RWB-P6-E1019-APP` | CG-W1, L-ITG-W1, L-P3-F, L-P3-H, L-P4-P, L-P6-D | Day 1 for 6 of 6 |
| `RWB-E1-020` | Allocation and assignment engine v1 | Split (rework) | P3 | integration `RWB-ITG-E1020-ITG`; rwb-case `RWB-P3-E1020-APP`, `RWB-P3-E1020-CON`, `RWB-P3-E1020-OPS`; rwb-access `RWB-P4-E1020-APP`; rwb-decision `RWB-P7-E1020-APP`; rwb-deviation `RWB-S8-E1020-APP` | CG-W1, L-ITG-W1, L-P3-F, L-P3-I, L-P4-Q, L-P7-G, L-S8-A | Day 1 for 6 of 7; `RWB-P3-E1020-APP` after RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP |
| `RWB-E1-021` | Transfer rules and engine v1 | Split (rework) | P3 | integration `RWB-ITG-E1021-ITG`; rwb-case `RWB-P3-E1021-APP`, `RWB-P3-E1021-CON`, `RWB-P3-E1021-OPS`; rwb-access `RWB-P4-E1021-APP`; rwb-document `RWB-P5-E1021-APP`; rwb-decision `RWB-P7-E1021-APP`; rwb-deviation `RWB-S8-E1021-APP` | CG-W1, L-ITG-W1, L-P3-F, L-P3-J, L-P4-R, L-P5-F, L-P7-H, L-S8-B | Day 1 for 7 of 8; `RWB-P3-E1021-APP` after RWB-P3-E1020-APP, RWB-P3-E1073-APP |
| `RWB-E1-022` | Sign-on with SSO, MFA and the first roles | Split (rework) | P4 | integration `RWB-ITG-E1022-ITG`; rwb-access `RWB-P4-E1022-APP`, `RWB-P4-E1022-CON`, `RWB-P4-E1022-DB` | CG-W1, L-ITG-W1, L-P4-A, L-P4-S | Day 1 for 4 of 4 |
| `RWB-E1-023` | Case record view v1, read only | Split (rework) | P3 | integration `RWB-ITG-E1023-ITG`; rwb-case `RWB-P3-E1023-APP`, `RWB-P3-E1023-CON`; rwb-access `RWB-P4-E1023-APP`; rwb-deviation `RWB-S8-E1023-APP` | CG-W1, L-ITG-W1, L-P3-F, L-P4-T, L-S8-C | Day 1 for 4 of 5; `RWB-P3-E1023-APP` after RWB-P3-E1018-APP |
| `RWB-E1-024` | Document store and index | Moved (no impact) | P5 | integration `RWB-ITG-E1024-ITG`; rwb-document `RWB-P5-E1024-APP` | L-ITG-W1, L-P5-G | Day 1 for 1 of 2; `RWB-P5-E1024-APP` after RWB-P5-E1025-APP |
| `RWB-E1-025` | Document types and fields agreed | Moved (no impact) | P5 | integration `RWB-ITG-E1025-ITG`; rwb-document `RWB-P5-E1025-APP` | L-ITG-W1, L-P5-G | Day 1 for 2 of 2 |
| `RWB-E1-026` | Attach and search screen | Moved (no impact) | P5 | integration `RWB-ITG-E1026-ITG`; rwb-document `RWB-P5-E1026-APP` | L-ITG-W1, L-P5-G | Day 1 for 1 of 2; `RWB-P5-E1026-APP` after RWB-P5-E1025-APP, RWB-P5-E1024-APP |
| `RWB-E1-027` | Decision log writer v1 | Split (rework) | P7 | integration `RWB-ITG-E1027-ITG`; rwb-decision `RWB-P7-E1027-APP`, `RWB-P7-E1027-CON`; platform `RWB-PLT-E1027-APP`, `RWB-PLT-E1027-CON` | CG-W0, CG-W1, L-ITG-W1, L-P7-B, L-PLT-LIB-C | Day 1 for 4 of 5; `RWB-P7-E1027-APP` after RWB-P7-E1008-APP |
| `RWB-E1-028` | Service levels, timers, escalation and prescription dates | Split (rework) | P3 | integration `RWB-ITG-E1028-ITG`; rwb-case `RWB-P3-E1028-APP`, `RWB-P3-E1028-CON`, `RWB-P3-E1028-OPS`; rwb-access `RWB-P4-E1028-APP`; rwb-decision `RWB-P7-E1028-APP` | CG-W1, L-ITG-W1, L-P3-F, L-P3-K, L-P4-U, L-P7-I | Day 1 for 5 of 6; `RWB-P3-E1028-APP` after RWB-P3-E1045-APP, RWB-P3-E1020-APP |
| `RWB-E1-030` | Daily rebalancing and queue measures | Split (rework) | P3 | integration `RWB-ITG-E1030-ITG`; rwb-case `RWB-P3-E1030-APP`, `RWB-P3-E1030-CON`, `RWB-P3-E1030-OPS`; rwb-decision `RWB-P7-E1030-APP` | CG-W1, L-ITG-W1, L-P3-F, L-P3-L, L-P7-J | Day 1 for 4 of 5; `RWB-P3-E1030-APP` after RWB-P3-E1020-APP |
| `RWB-E1-031` | Queue and owner on the case list with filters | Split (rework) | P3 | integration `RWB-ITG-E1031-ITG`; rwb-case `RWB-P3-E1031-APP`, `RWB-P3-E1031-CON` | CG-W1, L-ITG-W1, L-P3-F | Day 1 for 2 of 3; `RWB-P3-E1031-APP` after RWB-P3-E1020-APP |
| `RWB-E1-032` | Automatic attach from the OCR intake | Split (rework) | P5 | integration `RWB-ITG-E1032-ITG`; rwb-case `RWB-P3-E1032-APP`; rwb-document `RWB-P5-E1032-APP`, `RWB-P5-E1032-CON`, `RWB-P5-E1032-INF`, `RWB-P5-E1032-OPS`; rwb-comms `RWB-P6-E1032-APP`; rwb-decision `RWB-P7-E1032-APP`; rwb-partner `RWB-S9-E1032-APP` | CG-W1, L-ITG-W1, L-P3-M, L-P5-G, L-P5-H, L-P5-I, L-P6-E, L-P7-K, L-S9-B | Day 1 for 8 of 9; `RWB-P5-E1032-APP` after RWB-P5-E1024-APP |
| `RWB-E1-033` | Search across cases | Moved (no impact) | P5 | rwb-document `RWB-P5-E1033-APP` | L-P5-G | Day 1 for 0 of 1; `RWB-P5-E1033-APP` after RWB-P5-E1024-APP, RWB-P5-E1049-APP |
| `RWB-E1-034` | Letter template management | Moved (no impact) | P6 | integration `RWB-ITG-E1034-ITG`; rwb-comms `RWB-P6-E1034-APP` | L-ITG-W1, L-P6-A | Day 1 for 1 of 2; `RWB-P6-E1034-APP` after RWB-P6-E1046-APP |
| `RWB-E1-035` | Case record view v1.1 with documents and history timeline | Split (rework) | P3 | rwb-case `RWB-P3-E1035-APP`, `RWB-P3-E1035-CON` | CG-W1, L-P3-F | Day 1 for 1 of 2; `RWB-P3-E1035-APP` after RWB-P3-E1023-APP |
| `RWB-E1-037` | Role to permission matrix as data and PDPA field masking by role | Split (rework) | P4 | integration `RWB-ITG-E1037-ITG`; rwb-access `RWB-P4-E1037-APP`, `RWB-P4-E1037-CON`; platform `RWB-PLT-E1037-APP`, `RWB-PLT-E1037-CON` | CG-W0, CG-W1, L-ITG-W1, L-P4-A, L-PLT-LIB-D | Day 1 for 4 of 5; `RWB-P4-E1037-APP` after RWB-P4-E1022-APP |
| `RWB-E1-038` | Delegation of authority table as reference data | Moved (no impact) | P4 | rwb-access `RWB-P4-E1038-APP` | L-P4-J | Day 1 for 1 of 1 |
| `RWB-E1-039` | Access log into the decision log and break-glass admin | Split (rework) | P4 | integration `RWB-ITG-E1039-ITG`; rwb-access `RWB-P4-E1039-APP`, `RWB-P4-E1039-CON`, `RWB-P4-E1039-DB`, `RWB-P4-E1039-OPS`; rwb-document `RWB-P5-E1039-APP`; rwb-decision `RWB-P7-E1039-APP` | CG-W1, L-ITG-W1, L-P4-A, L-P4-V, L-P4-W, L-P5-J, L-P7-L | Day 1 for 6 of 7; `RWB-P4-E1039-APP` after RWB-P4-E1022-APP |
| `RWB-E1-040` | Document checklist per case type as reference data | Moved (no impact) | P5 | rwb-document `RWB-P5-E1040-APP` | L-P5-G | Day 1 for 0 of 1; `RWB-P5-E1040-APP` after RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP |
| `RWB-E1-041` | Retention classes and virus scan on intake | Moved (no impact) | P5 | rwb-document `RWB-P5-E1041-APP`, `RWB-P5-E1041-CON` | CG-W1, L-P5-G | Day 1 for 1 of 2; `RWB-P5-E1041-APP` after RWB-P5-E1024-APP, RWB-P5-E1049-APP |
| `RWB-E1-042` | Central configuration service and parameter catalog | Preserved + delta | P3 | rwb-case `RWB-P3-E1042-APP`, `RWB-P3-E1042-CON`; platform `RWB-PLT-E1042-APP`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1042-OPS` | CG-W0, CG-W1, L-P3-N, L-PLT-LIB-E, L-PLT-LIB-F | Day 1 for 5 of 5 |
| `RWB-E1-043` | Reference data service with versioned tables | Preserved + delta | P3 | rwb-case `RWB-P3-E1043-APP`, `RWB-P3-E1043-CON`; platform `RWB-PLT-E1043-APP`, `RWB-PLT-E1043-CON` | CG-W0, CG-W1, L-P3-O, L-PLT-LIB-G | Day 1 for 4 of 4 |
| `RWB-E1-044` | Database migrations versioned with parameterized schema names | Preserved + delta | PLT | platform `RWB-PLT-E1044-APP`, `RWB-PLT-E1044-APP-2`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1044-OPS` | CG-W0, L-PLT-TPL-F, L-PLT-TPL-G, L-PLT-TPL-H | Day 1 for 4 of 4 |
| `RWB-E1-045` | Multi-product parameters for Mortgage, HP and SSME | Moved (no impact) | P3 | rwb-case `RWB-P3-E1045-APP` | L-P3-F | Day 1 for 1 of 1 |
| `RWB-E1-046` | Template and merge field catalog as data | Split (rework) | P6 | integration `RWB-ITG-E1046-ITG`; rwb-document `RWB-P5-E1046-APP`; rwb-comms `RWB-P6-E1046-APP`, `RWB-P6-E1046-CON`; rwb-decision `RWB-P7-E1046-APP` | CG-W1, L-ITG-W1, L-P5-K, L-P6-A, L-P7-M | Day 1 for 5 of 5 |
| `RWB-E1-047` | Feature flags for module release with a removal date | Split (rework) | PLT | integration `RWB-ITG-E1047-ITG`; platform `RWB-PLT-E1047-APP`, `RWB-PLT-E1047-CON` | CG-W0, L-ITG-W1, L-PLT-LIB-H | Day 1 for 3 of 3 |
| `RWB-E1-049` | OCR pipeline on the Workbench document hub | Split (rework) | P5 | integration `RWB-ITG-E1049-ITG`; rwb-document `RWB-P5-E1049-APP`, `RWB-P5-E1049-CON`, `RWB-P5-E1049-INF`, `RWB-P5-E1049-OPS`; rwb-comms `RWB-P6-E1049-APP` | CG-W1, L-ITG-W1, L-P5-G, L-P5-L, L-P5-M, L-P6-F | Day 1 for 5 of 6; `RWB-P5-E1049-APP` after RWB-P5-E1024-APP |
| `RWB-E1-050` | Document classification | Split (rework) | P5 | integration `RWB-ITG-E1050-ITG`; rwb-case `RWB-P3-E1050-APP`; rwb-document `RWB-P5-E1050-APP`, `RWB-P5-E1050-CON`, `RWB-P5-E1050-OPS` | CG-W1, L-ITG-W1, L-P3-P, L-P5-G, L-P5-N | Day 1 for 4 of 5; `RWB-P5-E1050-APP` after RWB-P5-E1049-APP, RWB-P5-E1025-APP |
| `RWB-E1-052` | Notice generation v1 | Split (rework) | P6 | integration `RWB-ITG-E1052-ITG`; rwb-case `RWB-P3-E1052-APP`; rwb-document `RWB-P5-E1052-APP`; rwb-comms `RWB-P6-E1052-APP`, `RWB-P6-E1052-CON`; rwb-decision `RWB-P7-E1052-APP` | CG-W1, L-ITG-W1, L-P3-Q, L-P5-O, L-P6-A, L-P7-N | Day 1 for 5 of 6; `RWB-P6-E1052-APP` after RWB-P6-E1046-APP |
| `RWB-E1-053` | Field extraction for the six types into the index | Moved (no impact) | P5 | rwb-document `RWB-P5-E1053-APP`, `RWB-P5-E1053-CON` | CG-W1, L-P5-G | Day 1 for 1 of 2; `RWB-P5-E1053-APP` after RWB-P5-E1049-APP, RWB-P5-E1025-APP |
| `RWB-E1-054` | Review queue for low-confidence documents | Split (rework) | P5 | integration `RWB-ITG-E1054-ITG`; rwb-case `RWB-P3-E1054-APP`; rwb-access `RWB-P4-E1054-APP`; rwb-document `RWB-P5-E1054-APP`, `RWB-P5-E1054-CON`; rwb-decision `RWB-P7-E1054-APP` | CG-W1, L-ITG-W1, L-P3-R, L-P4-X, L-P5-G, L-P7-O | Day 1 for 5 of 6; `RWB-P5-E1054-APP` after RWB-P5-E1049-APP, RWB-P5-E1032-APP |
| `RWB-E1-055` | Proof of delivery capture design with WIN | Split (rework) | P6 | integration `RWB-ITG-E1055-ITG`; rwb-source-data `RWB-P1-E1055-APP`; rwb-case `RWB-P3-E1055-APP`; rwb-document `RWB-P5-E1055-APP`; rwb-comms `RWB-P6-E1055-APP`, `RWB-P6-E1055-CON`, `RWB-P6-E1055-INF`, `RWB-P6-E1055-OPS` | CG-W1, L-ITG-W1, L-P1-M, L-P3-S, L-P5-P, L-P6-A, L-P6-G, L-P6-H | Day 1 for 7 of 8; `RWB-P6-E1055-APP` after RWB-P6-E1052-APP |
| `RWB-E1-056` | Run books and monitoring for every Epic 1 Workbench job | Split (rework) | PLT | platform `RWB-PLT-E1056-OPS` | L-PLT-OBS-B | Day 1 for 1 of 1 |
| `RWB-E1-057` | Intake from branches, mailroom, partner SFTP and email | Split (rework) | P5 | integration `RWB-ITG-E1057-ITG`; rwb-document `RWB-P5-E1057-APP`, `RWB-P5-E1057-CON`, `RWB-P5-E1057-INF`, `RWB-P5-E1057-OPS`; rwb-partner `RWB-S9-E1057-APP` | CG-W1, L-ITG-W1, L-P5-G, L-P5-Q, L-P5-R, L-S9-C | Day 1 for 5 of 6; `RWB-P5-E1057-APP` after RWB-P5-E1049-APP |
| `RWB-E1-058` | Agent platform set-up [E1a] | Split (rework) | P10 | integration `RWB-ITG-E1058-ITG`; rwb-agent `RWB-P10-E1058-APP`, `RWB-P10-E1058-CON`, `RWB-P10-E1058-INF`, `RWB-P10-E1058-OPS` | CG-W1, L-ITG-W1, L-P10-A, L-P10-B, L-P10-C | Day 1 for 5 of 5 |
| `RWB-E1-059` | Case intake agent in shadow [E1b] | Split (rework) | P10 | integration `RWB-ITG-E1059-ITG`; rwb-agent `RWB-P10-E1059-APP`, `RWB-P10-E1059-CON` | CG-W1, L-ITG-W1, L-P10-A | Day 1 for 2 of 3; `RWB-P10-E1059-APP` after RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| `RWB-E1-060` | Extraction evaluation [E1c] | Moved (no impact) | P10 | integration `RWB-ITG-E1060-ITG`; rwb-agent `RWB-P10-E1060-APP` | L-ITG-W1, L-P10-A | Day 1 for 1 of 2; `RWB-P10-E1060-APP` after RWB-P10-E1058-APP |
| `RWB-E1-061` | Intake agent evaluation and L1 proposal [E2a] | Moved (no impact) | P10 | rwb-agent `RWB-P10-E1061-APP`, `RWB-P10-E1061-CON` | CG-W1, L-P10-A | Day 1 for 1 of 2; `RWB-P10-E1061-APP` after RWB-P10-E1059-APP |
| `RWB-E1-062` | Deviation screening agent in shadow [E2b] | Split (rework) | P10 | integration `RWB-ITG-E1062-ITG`; rwb-agent `RWB-P10-E1062-APP`, `RWB-P10-E1062-CON`; rwb-access `RWB-P4-E1062-APP`; rwb-document `RWB-P5-E1062-APP`; rwb-deviation `RWB-S8-E1062-APP` | CG-W1, L-ITG-W1, L-P10-A, L-P4-Y, L-P5-S, L-S8-D | Day 1 for 5 of 6; `RWB-P10-E1062-APP` after RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| `RWB-E1-063` | Agent monitoring dashboard v1 [E2c] | Split (rework) | P10 | integration `RWB-ITG-E1063-ITG`; rwb-agent `RWB-P10-E1063-APP`, `RWB-P10-E1063-CON`, `RWB-P10-E1063-OPS`; rwb-access `RWB-P4-E1063-APP`; rwb-comms `RWB-P6-E1063-APP` | CG-W1, L-ITG-W1, L-P10-A, L-P10-D, L-P4-Z, L-P6-I | Day 1 for 5 of 6; `RWB-P10-E1063-APP` after RWB-P10-E1058-APP |
| `RWB-E1-064` | Data dictionary for the 14 data products | Split (rework) | P1 | integration `RWB-ITG-E1064-ITG`; rwb-source-data `RWB-P1-E1064-APP`, `RWB-P1-E1064-CON`, `RWB-P1-E1064-OPS`; rwb-access `RWB-P4-E1064-APP` | CG-W1, L-ITG-W1, L-P1-A, L-P1-N, L-P4-AA | Day 1 for 4 of 5; `RWB-P1-E1064-APP` after RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| `RWB-E1-065` | Sandbox database with synthetic recovery data | Split (rework) | P1 | integration `RWB-ITG-E1065-ITG`; rwb-source-data `RWB-P1-E1065-APP`, `RWB-P1-E1065-CON`, `RWB-P1-E1065-DB`; rwb-case `RWB-P3-E1065-APP`; rwb-access `RWB-P4-E1065-APP`; rwb-document `RWB-P5-E1065-APP`; rwb-deviation `RWB-S8-E1065-APP` | CG-W1, L-ITG-W1, L-P1-A, L-P1-O, L-P3-T, L-P4-AB, L-P5-T, L-S8-E | Day 1 for 7 of 8; `RWB-P1-E1065-APP` after RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| `RWB-E1-066` | Interaction ledger store and writer | Split (rework) | P1 | integration `RWB-ITG-E1066-ITG`; rwb-source-data `RWB-P1-E1066-APP`, `RWB-P1-E1066-CON`, `RWB-P1-E1066-OPS`; rwb-case `RWB-P3-E1066-APP` | CG-W1, L-ITG-W1, L-P1-P, L-P1-Q, L-P3-U | Day 1 for 5 of 5 |
| `RWB-E1-067` | Every Workbench action into the interaction ledger | Split (rework) | P1 | integration `RWB-ITG-E1067-ITG`; rwb-source-data `RWB-P1-E1067-APP`, `RWB-P1-E1067-CON`; rwb-case `RWB-P3-E1067-APP`; rwb-document `RWB-P5-E1067-APP` | CG-W1, L-ITG-W1, L-P1-P, L-P3-V, L-P5-U | Day 1 for 4 of 5; `RWB-P1-E1067-APP` after RWB-P1-E1066-APP |
| `RWB-E1-068` | Interaction ledger read interface | Moved (no impact) | P1 | rwb-source-data `RWB-P1-E1068-APP` | L-P1-P | Day 1 for 0 of 1; `RWB-P1-E1068-APP` after RWB-P1-E1066-APP |
| `RWB-E1-069` | Read-only ACE source views, grants and boundary rule | Split (rework) | P1 | integration `RWB-ITG-E1069-ITG`; rwb-source-data `RWB-P1-E1069-APP`, `RWB-P1-E1069-DB`; rwb-access `RWB-P4-E1069-APP` | L-ITG-W1, L-P1-A, L-P1-R, L-P4-AC | Day 1 for 3 of 4; `RWB-P1-E1069-APP` after RWB-P1-E1001-APP, RWB-P1-ACE001-DB |
| `RWB-TE-001` | Recovery module folder and boundary test | Preserved + delta | PLT | platform `RWB-PLT-TE001-APP`, `RWB-PLT-TE001-APP-2` | L-PLT-TPL-I, L-PLT-TPL-J | Day 1 for 2 of 2 |
| `RWB-TE-002` | Code owners for the recovery module | Preserved + delta | PLT | platform `RWB-PLT-TE002-APP`, `RWB-PLT-TE002-OPS` | L-PLT-TPL-K, L-PLT-TPL-L | Day 1 for 2 of 2 |
| `RWB-TE-003` | Types and contract tests from the API specification | Preserved + delta | PLT | platform `RWB-PLT-TE003-APP`, `RWB-PLT-TE003-APP-2` | L-PLT-TPL-M, L-PLT-TPL-N | Day 1 for 2 of 2 |
| `RWB-TE-004` | Masked data in SIT and UAT | Split (rework) | PLT | integration `RWB-ITG-TE004-ITG`; platform `RWB-PLT-TE004-APP` | L-ITG-W1, L-PLT-TPL-O | Day 1 for 2 of 2 |
| `RWB-TE-006` | Outbox and retry for outbound work | Split (rework) | PLT | integration `RWB-ITG-TE006-ITG`; platform `RWB-PLT-TE006-APP`, `RWB-PLT-TE006-CON` | CG-W0, L-ITG-W1, L-PLT-LIB-J | Day 1 for 3 of 3 |
| `RWB-TE-007` | Scheduled jobs on Quartz | Retired (D-RCV-60) | none | none | none | none |
| `RWB-TE-008` | Decision log hash chain check | Split (rework) | PLT | integration `RWB-ITG-TE008-ITG`; platform `RWB-PLT-TE008-APP` | L-ITG-W1, L-PLT-TPL-P | Day 1 for 2 of 2 |
| `RWB-TE-011` | PDPA lint for code, tests and logs | Split (rework) | PLT | platform `RWB-PLT-TE011-APP` | L-PLT-TPL-Q | Day 1 for 1 of 1 |
| `RWB-TE-012` | Document storage containers | Moved (no impact) | PLT | platform `RWB-PLT-TE012-APP` | L-PLT-TPL-R | Day 1 for 1 of 1 |
| `RWB-TE-013` | Agent runtime client with fallback | Split (rework) | P10 | integration `RWB-ITG-TE013-ITG`; rwb-agent `RWB-P10-TE013-APP`, `RWB-P10-TE013-CON`, `RWB-P10-TE013-OPS`; rwb-decision `RWB-P7-TE013-APP` | CG-W1, L-ITG-W1, L-P10-A, L-P10-M, L-P7-AR | Day 1 for 4 of 5; `RWB-P10-TE013-APP` after RWB-P10-E1058-APP |

## The 72 story notes, with their service-and-lane note

Each section below reproduces the version 6 note word for word and then states what the realignment changes.

## RWB-E1-001 Recovery tables for the 14 data products

Module: P1 Recovery data engine

**View.** No view. The story creates the 92 tables of Physical Schema v5, `data_product`, `sys_objects` and `sys_fields`; the 30 views arrive next in V0002 and V0003 (RWB-E1-069).

**Grant.** V0001 gives the recovery service role DML on the Workbench tables and nothing on a view; no `GRANT` on `public` and no `GRANT SELECT ON ALL TABLES`.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 created a 43-table copy schema and seeded 108 objects and 1,256 fields. v5 creates the 92 tables, the four extension tables and the 122-object, 1,366-field dictionary, and leaves every source read to RWB-E1-069. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P7 `rwb-decision`; P8 `rwb-payment`.

- P1 `rwb-source-data`: `RWB-P1-E1001-APP` (App development, `L-P1-A`, Day 1).
- integration: `RWB-ITG-E1001-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1001-APP` (App development, `L-P4-K`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1001-APP` (App development, `L-P7-A`, Day 1).
- P8 `rwb-payment`: `RWB-P8-E1001-APP` (App development, `L-P8-B`, Day 1).

Ready to start: Day 1 for 5 of the 5 stories.

**Tables and owner.** `data_product` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `sys_fields` P1 `rwb_source_data`; `sys_objects` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP05, DP06, DP07, DP11, DP14, DP15, DP19. Build (H): `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P4-E1001-APP`, `RWB-P7-E1001-APP`, `RWB-P8-E1001-APP`. External (X): none.

**What moves.** The one `recovery` schema becomes 19 schemas (ADR-014). This story keeps the dictionary, the data products and the four extension tables in `rwb_source_data`; every other table moves to the schema of the service that owns it, and the split is new work carried by RWB-PLT-NF06-DB and the per-service DB stories (Template and Rules §R6). The built migration is unchanged until the split stories are picked up.

## RWB-E1-002 Case list v1 with case ID, owner and queue

Module: P1 Recovery data engine

**View.** `v_ace_account` for balance and days past due, `v_ace_efs_action` for the last contact, `v_ace_batch_status` for the business date of the ACE batch; `case_account`, `case_list_row` and `recovery_case` come through `CaseQueryApi`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 steps 2, 3 and 5 built a `load_run` row, called `LoadRunQuery.completedLoad` and joined `loan_account`. The table is gone: the completeness check is a read of `v_ace_batch_status`, and the join is to `v_ace_account`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`.

- P1 `rwb-source-data`: `RWB-P1-E1002-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1002-APP` (App development, `L-P1-A`, after RWB-P1-E1069-APP, RWB-P1-E1015-APP); `RWB-P1-E1002-OPS` (DevOps, `L-P1-F`, Day 1).
- integration: `RWB-ITG-E1002-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1002-APP` (App development, `L-P3-B`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P1-E1002-APP` after RWB-P1-E1069-APP, RWB-P1-E1015-APP.

**Tables and owner.** `case_account` P3 `rwb_case`; `case_list_row` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19. Build (H): `RWB-P1-E1015-APP`, `RWB-P1-E1069-APP`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P2-E1007-CON`, `RWB-P3-E1018-CON`, `RWB-P3-E1020-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1002-APP`, `RWB-P2-E1007-APP`, `RWB-P3-E1002-APP`, `RWB-P3-E1018-APP`, `RWB-P3-E1020-APP`. External (X): `RWB-P1-E1002-OPS`.

**What moves.** The case list row stays with P1 in `rwb_source_data` and the case itself comes from P3 `rwb_case` through the case API (R-PREC default ruling: case list API to rwb-case). The ACE read moves to P1 only, so this story no longer names `v_ace_account`, `v_ace_efs_action` or `v_ace_batch_status`; the P3 slice reads the freshness of DP01 from P1's contract.

## RWB-E1-007 Integration adapters for outbound files

Module: P2 Integration

**View.** `v_ace_account` for the account key, `v_ace_contact` for the contact key and channel, `v_ace_batch_status` for the date; writes `interface_config`, `outbound_item`, `outbox_event`, `outbox_delivery`, `processed_event`, `debt_sale_account` and `recovery_case`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 built the inbound file loads INT-10, INT-11 and INT-15 and the outbound interface INT-14. v5 keeps the outbound adapter, the outbox and the contract tests; the inbound loads are gone, and the adapter writes Workbench outbound files only. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P2 `rwb-integration` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P3 `rwb-case`; P6 `rwb-comms`; P5 `rwb-document`.

- P2 `rwb-integration`: `RWB-P2-E1007-CON` (Contract, `CG-W1`, Day 1); `RWB-P2-E1007-APP` (App development, `L-P2-A`, Day 1); `RWB-P2-E1007-INF` (Infrastructure, `L-P2-C`, Day 1); `RWB-P2-E1007-OPS` (DevOps, `L-P2-B`, Day 1).
- integration: `RWB-ITG-E1007-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1007-APP` (App development, `L-P4-L`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1007-APP` (App development, `L-P3-C`, Day 1).
- P6 `rwb-comms`: `RWB-P6-E1007-APP` (App development, `L-P6-B`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1007-APP` (App development, `L-P5-B`, Day 1).

Ready to start: Day 1 for 9 of the 9 stories.

**Tables and owner.** `data_product_load` P1 `rwb_source_data`; `debt_sale_account` S6 `rwb_debtsale`; `interface_config` P2 `rwb_integration`; `outbound_item` P2 `rwb_integration`; `outbox_delivery` platform library (no service schema); `outbox_event` platform library (no service schema); `processed_event` platform library (no service schema); `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP16, DP17, DP19. Build (H): `RWB-P2-E1007-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P1-E1015-CON`, `RWB-P2-E1007-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P1-E1015-APP`, `RWB-P1-E1069-APP`, `RWB-P2-E1007-APP`, `RWB-P3-E1007-APP`, `RWB-P4-E1007-APP`, `RWB-P5-E1007-APP`, `RWB-P6-E1007-APP`. External (X): `RWB-P2-E1007-INF`, `RWB-P2-E1007-OPS`.

**What moves.** The outbound adapter stays with P2 `rwb_integration`, and the outbox, inbox and idempotency tables become the platform library objects created in P2's own schema (DP-09). `debt_sale_account` is owned by S6 `rwb_debtsale`, so the write named in the View note goes through S6's contract (GAP-3160). The P3, P4, P5 and P6 slices consume the file contract and name no ACE view.

## RWB-E1-008 Decision log store v1, append only and hash chained

Module: P7 Decision center and log

**View.** No view. The story owns `decision_log_entry` and reads no ACE source.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The entry carries the business keys of the ACE records it names, never a copy of an ACE column. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P7 `rwb-decision` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`.

- P7 `rwb-decision`: `RWB-P7-E1008-CON` (Contract, `CG-W1`, Day 1); `RWB-P7-E1008-APP` (App development, `L-P7-B`, Day 1); `RWB-P7-E1008-DB` (ACE DB, `L-P7-D`, Day 1); `RWB-P7-E1008-OPS` (DevOps, `L-P7-C`, Day 1).
- integration: `RWB-ITG-E1008-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1008-APP` (App development, `L-P4-M`, Day 1).

Ready to start: Day 1 for 6 of the 6 stories.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP07, DP10, DP13, DP15, DP17, DP19. Build (H): `RWB-P7-E1008-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`, `RWB-P7-E1008-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P4-E1008-APP`, `RWB-P7-E1008-APP`. External (X): `RWB-P7-E1008-DB`, `RWB-P7-E1008-OPS`.

**What moves.** The decision log store becomes P7 `rwb_decision`, and the writer that other services call is the platform library RWB-PLT-E1027 (DP-03). The P4 slice records an access decision through that library and keeps no ledger table of its own.

## RWB-E1-011 Reconciliation and data quality report

Module: P1 Recovery data engine

**View.** `v_ace_account`, `v_ace_payment`, `v_ace_plan`, `v_ace_customer`, `v_ace_contact`, `v_ace_asset` and `v_ace_batch_status` for the reconciliation; writes `reconciliation_result`, `case_list_row` and the case exceptions.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00; DP13 Money and closure, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 reconciled the load runs and the copy tables after JOB-04. v5 reconciles the Workbench case data against the ACE views and the ACE batch record; there is no load run to reconcile. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; S5 `rwb-asset`; P3 `rwb-case`; P6 `rwb-comms`.

- P1 `rwb-source-data`: `RWB-P1-E1011-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1011-APP` (App development, `L-P1-A`, after RWB-P1-E1015-APP, RWB-P1-E1069-APP); `RWB-P1-E1011-OPS` (DevOps, `L-P1-G`, Day 1).
- integration: `RWB-ITG-E1011-ITG` (Integration, `L-ITG-W1`, Day 1).
- S5 `rwb-asset`: `RWB-S5-E1011-APP` (App development, `L-S5-A`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1011-APP` (App development, `L-P3-D`, Day 1).
- P6 `rwb-comms`: `RWB-P6-E1011-APP` (App development, `L-P6-C`, Day 1).

Ready to start: Day 1 for 6 of the 7 stories; `RWB-P1-E1011-APP` after RWB-P1-E1015-APP, RWB-P1-E1069-APP.

**Tables and owner.** `case_list_row` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `reconciliation_result` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19. Build (H): `RWB-P1-E1002-CON`, `RWB-P1-E1015-APP`, `RWB-P1-E1069-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1011-APP`, `RWB-P3-E1011-APP`, `RWB-P6-E1011-APP`, `RWB-S5-E1011-APP`. External (X): `RWB-P1-E1011-OPS`.

**What moves.** Reconciliation stays with P1 `rwb_source_data` and reads the ACE views there. The case rows it reconciles come from P3 `rwb_case` through the case API, and the P6 and S5 slices consume the reconciliation result as a report rather than reading a P1 table (GAP-3169).

## RWB-E1-013 Baseline measures

Module: P9 Reporting

**View.** `v_ace_payment` for money collected and `case_account` for the case stock; writes `measure_definition` and `measure_snapshot`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP13 Money and closure, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 read the money measures from the copy tables. v5 reads `v_ace_payment`; the case stock comes from `case_account`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P9 `rwb-reporting` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`; P1 `rwb-source-data`.

- P9 `rwb-reporting`: `RWB-P9-E1013-CON` (Contract, `CG-W1`, Day 1); `RWB-P9-E1013-APP` (App development, `L-P9-A`, Day 1); `RWB-P9-E1013-OPS` (DevOps, `L-P9-B`, Day 1).
- integration: `RWB-ITG-E1013-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1013-APP` (App development, `L-P3-E`, Day 1).
- P1 `rwb-source-data`: `RWB-P1-E1013-APP` (App development, `L-P1-H`, Day 1).

Ready to start: Day 1 for 6 of the 6 stories.

**Tables and owner.** `case_account` P3 `rwb_case`; `data_product_load` P1 `rwb_source_data`; `measure_definition` P9 `rwb_reporting`; `measure_snapshot` P9 `rwb_reporting` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP05, DP07, DP10, DP11, DP13, DP15, DP17, DP19. Build (H): `RWB-P9-E1013-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1018-CON`, `RWB-P3-E1043-CON`, `RWB-P9-E1013-CON`. Integration (I): `RWB-P1-E1013-APP`, `RWB-P3-E1013-APP`, `RWB-P3-E1018-APP`, `RWB-P9-E1013-APP`. External (X): `RWB-P9-E1013-OPS`.

**What moves.** The measures and snapshots stay with P9 `rwb_reporting`. Money collected comes from P1's payment read and the case stock from P3 `rwb_case`, both by contract; P9 names no ACE view and holds only `measure_definition` and `measure_snapshot`.

## RWB-E1-014 Decision log copy to the data lake

Module: P1 Recovery data engine

**View.** No view. The story copies `decision_log_entry` to the lake and owns `lake_copy_watermark`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** The copy is unchanged; it now stamps the ACE business date it copies alongside the Workbench sequence. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** Retired (D-RCV-60): no new story, no lane and no Day-1 work. The source note above is kept word for word for traceability.

**What moves.** The decision log copy has no target: Arch v5 has no data lake, so there is no lake copy to make (DP-17). `lake_copy_watermark` has no target and P1's DB story drops it, and the change is recorded in the Change Register (GAP-3165).

## RWB-E1-015 Freshness stamp per data product

Module: P1 Recovery data engine

**View.** `v_ace_batch_status` is the freshness source: one row per ACE batch with its business date, status and record count; reads `data_product` and writes `data_product_load`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 stamped each product from its `load_run`. v5 stamps it from `v_ace_batch_status` and the `ace_batch_run` record that RWB-ACE-001 populates; a Workbench product is stamped from its own last committed write. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`.

- P1 `rwb-source-data`: `RWB-P1-E1015-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1015-APP` (App development, `L-P1-A`, after RWB-P1-E1001-APP, RWB-P1-E1069-APP); `RWB-P1-E1015-OPS` (DevOps, `L-P1-I`, Day 1).
- integration: `RWB-ITG-E1015-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 3 of the 4 stories; `RWB-P1-E1015-APP` after RWB-P1-E1001-APP, RWB-P1-E1069-APP.

**Tables and owner.** `data_product` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19. Build (H): `RWB-P1-E1001-APP`, `RWB-P1-E1015-CON`, `RWB-P1-E1069-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P1-E1015-APP`. External (X): `RWB-P1-E1015-OPS`.

**What moves.** The freshness stamp stays with P1 `rwb_source_data`, which publishes it through `GET /freshness` and the `AceDataReady` and `AceDataLate` events. Every other service reads the business date from that contract instead of stamping a copy of `data_product_load` (GAP-3154).

## RWB-E1-016 Access control per data product and catalog entries

Module: P1 Recovery data engine

**View.** `v_ace_account`, `v_ace_customer` and `v_ace_contact` for the field level checks; writes `data_product_access` and `masking_rule` and reads the four extension tables.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including the extension table it writes; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00; DP14 Reference data, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 answered a data product record request from the copy tables. v5 answers it from the views named for each product, so access is decided on the view and the product, and the customer view still returns only the masked identity. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P5 `rwb-document`.

- P1 `rwb-source-data`: `RWB-P1-E1016-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1016-APP` (App development, `L-P1-A`, after RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP); `RWB-P1-E1016-DB` (ACE DB, `L-P1-J`, Day 1).
- integration: `RWB-ITG-E1016-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1016-APP` (App development, `L-P4-N`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1016-APP` (App development, `L-P5-C`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P1-E1016-APP` after RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP.

**Tables and owner.** `data_product_access` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `masking_rule` P4 `rwb_access` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP05, DP07, DP08, DP11, DP19. Build (H): `RWB-P1-E1001-APP`, `RWB-P1-E1064-APP`, `RWB-P1-E1069-APP`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): `RWB-P1-E1016-APP`, `RWB-P4-E1016-APP`, `RWB-P5-E1016-APP`. External (X): `RWB-P1-E1016-DB`.

**What moves.** The data product access rows stay with P1 `rwb_source_data`; `masking_rule` is owned by P4 `rwb_access` (Ownership Map), so the masking rows this story relies on come from P4's contract. The access decisions are made per product and per view, not per table copy.

## RWB-E1-017 Retention and archive rule for the data store

Module: P1 Recovery data engine

**View.** No view. The story owns `retention_rule` and `retention_action` over `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP10 Documents and extracted fields, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The retention classes cover the 92 Workbench tables; the ACE source is retained by ACE under its own schedule. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P7 `rwb-decision`; P5 `rwb-document`.

- P1 `rwb-source-data`: `RWB-P1-E1017-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1017-APP` (App development, `L-P1-A`, after RWB-P1-E1001-APP, RWB-P1-E1064-APP); `RWB-P1-E1017-OPS` (DevOps, `L-P1-K`, Day 1).
- integration: `RWB-ITG-E1017-ITG` (Integration, `L-ITG-W1`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1017-APP` (App development, `L-P7-E`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1017-APP` (App development, `L-P5-D`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P1-E1017-APP` after RWB-P1-E1001-APP, RWB-P1-E1064-APP.

**Tables and owner.** `recovery_case` P3 `rwb_case`; `retention_action` P5 `rwb_document`; `retention_rule` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP19. Build (H): `RWB-P1-E1001-APP`, `RWB-P1-E1017-CON`, `RWB-P1-E1064-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P1-E1017-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1017-APP`, `RWB-P5-E1017-APP`, `RWB-P7-E1017-APP`. External (X): `RWB-P1-E1017-OPS`, `RWB-PLT-TE012-APP`.

**What moves.** `retention_rule` and `retention_action` are owned by P5 `rwb_document` (Ownership Map ruling, ASM-0076), so P1's retention classes end and P5 applies them to Workbench documents (GAP-3158). P7 keeps the decision log retention by contract.

## RWB-E1-070 Temporal platform on the ACE AKS clusters

Module: P3 Case and workflow

**Build order.** First of the four configuration stories, and before RWB-E1-018, RWB-E1-020 and RWB-E1-021: RWB-E1-070, RWB-E1-071, RWB-E1-072, RWB-E1-073.

**View.** No view. The Temporal persistence databases `temporal` and `temporal_visibility` sit outside the recovery schema and are read by no Workbench query.

**Grant.** No grant in the recovery schema. `temporal_svc` owns the Temporal databases and has no grant on the ACE database; `recovery_svc` has no grant on either Temporal database. The Web UI maps Entra claims to RW-PLATADM (operate) and RW-AUDIT (read).

**Freshness.** Not a data product. The `rwb-recovery` namespace keeps a 30-day retention, and no search attribute carries personal data.

**Boundary.** No recovery constraint references `public`. The platform adds no table to the recovery schema; the Workbench objects are the Temporal client configuration and the run book catalog row. Boundary rule BND-6 is unchanged.

**Risk.** The main risk is operational: SCB IT must run the cluster, its upgrades, backup and certificates from the first day. The run book is an acceptance criterion, not a later task, and the DEP-36 version approval gates the build.

**Service and lane.** integration `RWB-ITG-W1`; platform (wave 0, `CG-W0` and `L-PLT-*`).

- integration: `RWB-ITG-E1070-ITG` (Integration, `L-ITG-W1`, Day 1).
- platform: `RWB-PLT-E1070-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1070-APP` (App development, `L-PLT-WF-D`, Day 1).

Ready to start: Day 1 for 3 of the 3 stories.

**Tables and owner.** No table in the service schemas; the objects are platform, template or deployment artefacts.

**Dependencies.** Patterns: DP01, DP02, DP04, DP05, DP06, DP07, DP13, DP14, DP15, DP19. Build (H): `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1070-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1022-CON`. Integration (I): `RWB-P4-E1022-APP`, `RWB-PLT-E1070-APP`. External (X): `RWB-PLT-E1056-OPS`.

**What moves.** The Temporal platform is platform work: RWB-PLT-E1070 owns the cluster, its namespace `rwb-recovery`, its upgrades and its run book, and lives in a platform lane (GAP-3163). P3 consumes the platform through the SDK and contributes no platform story.

## RWB-E1-071 Temporal worker and SDK in the recovery module

Module: P3 Case and workflow

**Build order.** Second, after RWB-E1-070, and before RWB-E1-072 and RWB-E1-073.

**View.** No view. The worker polls `rwb-platform` and writes `decision_log_entry` from the smoke workflow.

**Grant.** No new recovery grant. The worker runs as SY-CASEWF and `POST /admin/workflows/smoke` needs RW-PLATADM; another role is refused with MSG-P4-002.

**Freshness.** DP12 Decision log, ON_CHANGE. The smoke entry is stamped from its committed write.

**Boundary.** Workflow classes stay in `recovery.casewf.workflow`, activities in `recovery.casewf.activity`, and the gateway is the only published entry. The boundary test fails a workflow class that calls a repository, an HTTP client or Drools.

**Risk.** The main risk is a workflow class that reads the clock or performs I/O, or a clear payload in history. The `recovery.casewf.workflow` boundary test and PdpaPayloadCodec are in the first build, not added later.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-E1071-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1071-APP` (App development, `L-PLT-WF-E`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1070-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): none. External (X): `RWB-PLT-TE001-APP`.

**What moves.** The worker kit and the smoke workflow are platform work (RWB-PLT-E1071), and the platform story also replaces the Quartz scheduler of RWB-TE-007 (DP-10). P3 registers its own workflow and activity classes and its own task queue `rwb-case`.

## RWB-E1-072 Drools runtime and rule package store

Module: P3 Case and workflow

**Build order.** Third, after RWB-E1-044, RWB-E1-043 and RWB-E1-027, and before RWB-E1-073.

**View.** No view. The story creates `rule_package` and `rule_package_version`, adds DF-REF-296 to 298 to `rule_row` and DF-REF-299 to `rule_test_case`, and seeds the five Epic 1 package codes.

**Grant.** RW-COE reads the package list and SY-RULES evaluates. No grant on an ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE. The package version is chosen at evaluation time and recorded on the decision.

**Boundary.** The rule tables are in the recovery schema, and no engine reads the package source. `RuleEvaluator` and `RuleCatalog` are published in `recovery.casewf.rules`; a caller outside that package uses the interface only.

**Risk.** Two versions in force on one date would break first match and the decision log. The valid-from constraint, the checksum check and the refusal to load a mismatched DRL into the cache are the controls.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-E1072-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1072-APP` (App development, `L-PLT-LIB-I`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** `rule_package` P7 `rwb_decision`; `rule_package_version` P7 `rwb_decision`; `rule_row` P7 `rwb_decision`; `rule_test_case` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP05, DP06, DP07, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): none. External (X): none.

**What moves.** The rule registry is P7 `rwb_decision` (Ownership Map ruling, ASM-0069) and the runtime is the embedded Drools kit RWB-PLT-E1072 (DP-04). The table location in the source note is superseded: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 tables, and a service holds only its evaluated copy (GAP-3157). The five Epic 1 package codes are not reconciled with the eight phase 1 packages of the design (GAP-3167).

## RWB-E1-073 Rule authoring, validation, test scenarios, approval and rollback in Drools

Module: P3 Case and workflow

**Build order.** Fourth, after RWB-E1-072 and RWB-E1-042, and before RWB-E1-018, RWB-E1-020 and RWB-E1-021.

**View.** No view. The story reads `rule_package_version`, `rule_row` and `rule_test_case`, and stores the workbook, the generated DRL and the checksum.

**Grant.** RW-COE uploads and runs a dry run, RW-RISK approves, and the author cannot approve. RW-AUDIT reads. A role without the right gets MSG-P4-002.

**Freshness.** DP14 Reference data, ON_CHANGE. A version is in force from its valid-from date, and a rollback is one call.

**Boundary.** The controller and the load service stay in `recovery.casewf.rules`; the workbook is stored in Blob and no ACE table is read or written. Boundary rule BND-6 is unchanged.

**Risk.** The main risk is authoring skill: the first packages need the Drools XLS template and at least `rules.testcases.min` scenarios before approval. RuleScenarioBuildGate runs every in-force package on every build, so a broken package stops the pipeline, not a case.

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P6 `rwb-comms`; P7 `rwb-decision`; P2 `rwb-integration`.

- P3 `rwb-case`: `RWB-P3-E1073-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1073-APP` (App development, `L-P3-F`, Day 1); `RWB-P3-E1073-INF` (Infrastructure, `L-P3-W`, Day 1).
- integration: `RWB-ITG-E1073-ITG` (Integration, `L-ITG-W1`, Day 1).
- P6 `rwb-comms`: `RWB-P6-E1073-APP` (App development, `L-P6-J`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1073-APP` (App development, `L-P7-P`, Day 1).
- P2 `rwb-integration`: `RWB-P2-E1073-APP` (App development, `L-P2-D`, Day 1).

Ready to start: Day 1 for 7 of the 7 stories.

**Tables and owner.** `rule_package_version` P7 `rwb_decision`; `rule_row` P7 `rwb_decision`; `rule_test_case` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P3-E1073-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1073-CON`. Integration (I): `RWB-P2-E1073-APP`, `RWB-P3-E1073-APP`, `RWB-P6-E1073-APP`, `RWB-P7-E1073-APP`. External (X): `RWB-P3-E1073-INF`.

**What moves.** Authoring, test, four-eyes approval, valid-from dating and rollback are central in P7 `rwb_decision`; evaluation is local in the owning service (Temporal and Drools design slide 15). The P3, P6 and P2 slices are the package owners of their own rules, and each fetches a version with `GET /rule-models/{n}/{v}` and verifies the checksum (GAP-3157).

## RWB-E1-018 Case ID issuance and case record v1

Module: P3 Case and workflow

**View.** `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status` for the entry gate; writes `recovery_case`, `case_account`, `case_party`, `case_entry_exclusion`, `party_ext` and `account_ext`.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including `party_ext` and `account_ext`; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP03 Case and ownership, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 created cases when JOB-01 published LoadCompleted for COLLINS. v5 creates them when the ACE batch for the business date is COMPLETE; the entry gate reads `v_ace_batch_status`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P7 `rwb-decision`; P5 `rwb-document`; P1 `rwb-source-data`.

- P3 `rwb-case`: `RWB-P3-E1018-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1018-APP` (App development, `L-P3-F`, after RWB-P3-E1073-APP); `RWB-P3-E1018-OPS` (DevOps, `L-P3-G`, Day 1).
- integration: `RWB-ITG-E1018-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1018-APP` (App development, `L-P4-O`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1018-APP` (App development, `L-P7-F`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1018-APP` (App development, `L-P5-E`, Day 1).
- P1 `rwb-source-data`: `RWB-P1-E1018-APP` (App development, `L-P1-L`, Day 1).

Ready to start: Day 1 for 7 of the 8 stories; `RWB-P3-E1018-APP` after RWB-P3-E1073-APP.

**Tables and owner.** `account_ext` P1 `rwb_source_data`; `case_account` P3 `rwb_case`; `case_entry_exclusion` P3 `rwb_case`; `case_party` P3 `rwb_case`; `data_product_load` P1 `rwb_source_data`; `party_ext` P1 `rwb_source_data`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1018-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P3-E1073-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1018-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P1-E1016-APP`, `RWB-P1-E1018-APP`, `RWB-P1-E1069-APP`, `RWB-P3-E1018-APP`, `RWB-P4-E1018-APP`, `RWB-P5-E1018-APP`, `RWB-P7-E1018-APP`. External (X): `RWB-P3-E1018-OPS`.

**What moves.** The case, the case accounts and parties and the entry exclusion stay with P3 `rwb_case`. `party_ext` and `account_ext` are P1 extension tables (Ownership Map), so the write named in the View note becomes a P1 story and P3 calls it by contract (GAP-3162). The entry gate reads the ACE batch state from P1's freshness contract.

## RWB-E1-019 Roles, teams and queues as data

Module: P3 Case and workflow

**View.** No view. The story loads `role`, `queue`, `queue_member`, `reference_row` and `reference_version` as reference data.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 loaded the queue files through the reference data service; v5 does the same, so only the table names and the version rules moved. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P6 `rwb-comms`.

- P3 `rwb-case`: `RWB-P3-E1019-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1019-APP` (App development, `L-P3-F`, Day 1); `RWB-P3-E1019-DB` (ACE DB, `L-P3-H`, Day 1).
- integration: `RWB-ITG-E1019-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1019-APP` (App development, `L-P4-P`, Day 1).
- P6 `rwb-comms`: `RWB-P6-E1019-APP` (App development, `L-P6-D`, Day 1).

Ready to start: Day 1 for 6 of the 6 stories.

**Tables and owner.** `queue` P3 `rwb_case`; `queue_member` P3 `rwb_case`; `reference_row` P3 `rwb_case`; `reference_version` P3 `rwb_case`; `role` P4 `rwb_access` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1019-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1019-CON`, `RWB-P4-E1037-CON`. Integration (I): `RWB-P3-E1019-APP`, `RWB-P4-E1019-APP`, `RWB-P4-E1038-APP`, `RWB-P6-E1019-APP`. External (X): `RWB-P3-E1019-DB`.

**What moves.** Teams and queues stay with P3 `rwb_case`; `role` is owned by P4 `rwb_access`, so the role load in this story becomes a P4 story and P3 reads roles by contract (GAP-3159). The reference rows and their versions stay with P3 (R-PREC default ruling, DP-07).

## RWB-E1-020 Allocation and assignment engine v1

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `queue_member` and `rule_row` and writes `assignment` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Allocation no longer waits on a load: it waits on the entry gate of RWB-E1-018, which reads the ACE batch record. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P7 `rwb-decision`; S8 `rwb-deviation`.

- P3 `rwb-case`: `RWB-P3-E1020-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1020-APP` (App development, `L-P3-F`, after RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP); `RWB-P3-E1020-OPS` (DevOps, `L-P3-I`, Day 1).
- integration: `RWB-ITG-E1020-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1020-APP` (App development, `L-P4-Q`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1020-APP` (App development, `L-P7-G`, Day 1).
- S8 `rwb-deviation`: `RWB-S8-E1020-APP` (App development, `L-S8-A`, Day 1).

Ready to start: Day 1 for 6 of the 7 stories; `RWB-P3-E1020-APP` after RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP.

**Tables and owner.** `assignment` P3 `rwb_case`; `decision_log_entry` P7 `rwb_decision`; `queue_member` P3 `rwb_case`; `recovery_case` P3 `rwb_case`; `rule_row` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1018-APP`, `RWB-P3-E1019-APP`, `RWB-P3-E1020-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P3-E1073-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1020-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P3-E1020-APP`, `RWB-P4-E1020-APP`, `RWB-P7-E1020-APP`, `RWB-S8-E1020-APP`. External (X): `RWB-P3-E1020-OPS`, `RWB-PLT-E1056-OPS`.

**What moves.** Allocation stays with P3 `rwb_case`; the queue membership it reads is its own and the rule rows are P7's, reached by contract (DP-04). The P4 slice authorises the assignment, the P7 slice records it and the S8 slice reacts to the case state; none of them writes a case table.

## RWB-E1-021 Transfer rules and engine v1

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `queue` and `rule_row` and writes `assignment` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A transfer names an ACE business key where it names an account; it never copies one. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P7 `rwb-decision`; S8 `rwb-deviation`; P5 `rwb-document`.

- P3 `rwb-case`: `RWB-P3-E1021-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1021-APP` (App development, `L-P3-F`, after RWB-P3-E1020-APP, RWB-P3-E1073-APP); `RWB-P3-E1021-OPS` (DevOps, `L-P3-J`, Day 1).
- integration: `RWB-ITG-E1021-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1021-APP` (App development, `L-P4-R`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1021-APP` (App development, `L-P7-H`, Day 1).
- S8 `rwb-deviation`: `RWB-S8-E1021-APP` (App development, `L-S8-B`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1021-APP` (App development, `L-P5-F`, Day 1).

Ready to start: Day 1 for 7 of the 8 stories; `RWB-P3-E1021-APP` after RWB-P3-E1020-APP, RWB-P3-E1073-APP.

**Tables and owner.** `assignment` P3 `rwb_case`; `decision_log_entry` P7 `rwb_decision`; `queue` P3 `rwb_case`; `recovery_case` P3 `rwb_case`; `rule_row` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1020-APP`, `RWB-P3-E1021-CON`, `RWB-P3-E1028-CON`, `RWB-P3-E1043-CON`, `RWB-P3-E1073-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1021-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P3-E1021-APP`, `RWB-P4-E1021-APP`, `RWB-P5-E1021-APP`, `RWB-P7-E1021-APP`, `RWB-S8-E1021-APP`. External (X): `RWB-P3-E1021-OPS`.

**What moves.** Transfers stay with P3 `rwb_case`; the rule rows are P7's and the decision entries are P7's, both by contract. The S8 slice clears a deviation on transfer, and P4 authorises it, so the transfer holds no cross-service constraint.

## RWB-E1-022 Sign-on with SSO, MFA and the first roles

Module: P4 Access and administration

**View.** No view. The story owns `role`, `permission` and `role_conflict`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The first roles are seeded as reference data, not as a copy of an ACE identity table. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P4 `rwb-access` (primary); integration `RWB-ITG-W1`.

- P4 `rwb-access`: `RWB-P4-E1022-CON` (Contract, `CG-W1`, Day 1); `RWB-P4-E1022-APP` (App development, `L-P4-A`, Day 1); `RWB-P4-E1022-DB` (ACE DB, `L-P4-S`, Day 1).
- integration: `RWB-ITG-E1022-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 4 of the 4 stories.

**Tables and owner.** `permission` P4 `rwb_access`; `role` P4 `rwb_access`; `role_conflict` P4 `rwb_access` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP07, DP08, DP11, DP13, DP15, DP19. Build (H): `RWB-P4-E1022-CON`, `RWB-P4-E1037-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1019-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P3-E1019-APP`, `RWB-P4-E1022-APP`. External (X): `RWB-P4-E1022-DB`.

**What moves.** Sign-on and the first roles are P4 `rwb_access`, which owns `role`, `permission` and `role_conflict`. Identity comes from ACE Common (Entra) through the sign-in contract, and no ACE identity table is copied.

## RWB-E1-023 Case record view v1, read only

Module: P3 Case and workflow

**View.** `v_ace_account`, `v_ace_customer`, `v_ace_contact`, `v_ace_efs_action` and `v_ace_batch_status` for the read-only case record; reads `recovery_case`, `case_account`, `case_party`, `document` and `interaction`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 read the case, party and contact data from the copy tables. v5 reads the five views for the account and customer side and shows the freshness line from the batch record; that line stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; S8 `rwb-deviation`.

- P3 `rwb-case`: `RWB-P3-E1023-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1023-APP` (App development, `L-P3-F`, after RWB-P3-E1018-APP).
- integration: `RWB-ITG-E1023-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1023-APP` (App development, `L-P4-T`, Day 1).
- S8 `rwb-deviation`: `RWB-S8-E1023-APP` (App development, `L-S8-C`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P3-E1023-APP` after RWB-P3-E1018-APP.

**Tables and owner.** `case_account` P3 `rwb_case`; `case_party` P3 `rwb_case`; `data_product_load` P1 `rwb_source_data`; `document` P5 `rwb_document`; `interaction` P1 `rwb_source_data`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP18, DP19. Build (H): `RWB-P3-E1018-APP`, `RWB-P3-E1023-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1023-CON`, `RWB-P4-E1037-CON`, `RWB-P4-E1039-CON`. Integration (I): `RWB-P1-E1068-APP`, `RWB-P1-E1069-APP`, `RWB-P3-E1023-APP`, `RWB-P4-E1023-APP`, `RWB-P4-E1039-APP`, `RWB-P5-E1024-APP`, `RWB-S8-E1023-APP`. External (X): none.

**What moves.** The case record is P3 `rwb_case`; the documents are P5's and the interactions are P1's, so both are read by contract. The five ACE views are read by P1 only, and the freshness line the note describes arrives from P1's contract (GAP-3154).

## RWB-E1-024 Document store and index

Module: P5 Document hub

**View.** No view. The story owns `document`, `document_field`, `document_type` and `document_hub_parameter`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A document carries the case and ACE business keys; the document itself is a Workbench record. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`.

- P5 `rwb-document`: `RWB-P5-E1024-APP` (App development, `L-P5-G`, after RWB-P5-E1025-APP).
- integration: `RWB-ITG-E1024-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P5-E1024-APP` after RWB-P5-E1025-APP.

**Tables and owner.** `document` P5 `rwb_document`; `document_field` P5 `rwb_document`; `document_hub_parameter` P5 `rwb_document`; `document_type` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19. Build (H): `RWB-P5-E1025-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1018-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P3-E1018-APP`, `RWB-P5-E1024-APP`. External (X): `RWB-PLT-TE012-APP`.

**What moves.** The document store and index are P5 `rwb_document`, which owns `document`, `document_field`, `document_type` and `document_hub_parameter`. Files go to the P5 Blob container, and no ACE table is read.

## RWB-E1-025 Document types and fields agreed

Module: P5 Document hub

**View.** No view. The story loads `document_type` as reference data.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 took the type list from the trackers of RWB-E1-012. v5 takes it from the fields the ACE views can supply and the types legal counsel signs off. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`.

- P5 `rwb-document`: `RWB-P5-E1025-APP` (App development, `L-P5-G`, Day 1).
- integration: `RWB-ITG-E1025-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** `document_type` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP07, DP11, DP13, DP15, DP19. Build (H): `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1069-APP`, `RWB-P5-E1025-APP`. External (X): none.

**What moves.** The document types and fields are P5 `rwb_document` reference data. The type list comes from the fields the P1 view contract can supply plus the types legal counsel signs off, so the story names no view itself.

## RWB-E1-026 Attach and search screen

Module: P5 Document hub

**View.** No view. The attach screen reads `recovery_case`, `document`, `document_type` and `document_hub_parameter`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 listed the document types and fields from the copy tables. v5 lists the same types and the view fields the caller may see; no copy table is read. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`.

- P5 `rwb-document`: `RWB-P5-E1026-APP` (App development, `L-P5-G`, after RWB-P5-E1025-APP, RWB-P5-E1024-APP).
- integration: `RWB-ITG-E1026-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P5-E1026-APP` after RWB-P5-E1025-APP, RWB-P5-E1024-APP.

**Tables and owner.** `document` P5 `rwb_document`; `document_hub_parameter` P5 `rwb_document`; `document_type` P5 `rwb_document`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP19. Build (H): `RWB-P5-E1024-APP`, `RWB-P5-E1025-APP`, `RWB-P5-E1041-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1030-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P3-E1030-APP`, `RWB-P3-E1045-APP`, `RWB-P5-E1026-APP`. External (X): none.

**What moves.** The attach and search screen is served by P5 `rwb_document`, composed at gateway-bff from P5 and P3 calls (DP-19). The case key comes from P3's contract and the type list from P5's own reference data.

## RWB-E1-027 Decision log writer v1

Module: P7 Decision center and log

**View.** No view. The story writes `decision_log_entry` and reads `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The writer takes the ACE business keys and the rule, model and agent versions it is given. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P7 `rwb-decision` (primary); integration `RWB-ITG-W1`; platform (wave 0, `CG-W0` and `L-PLT-*`).

- P7 `rwb-decision`: `RWB-P7-E1027-CON` (Contract, `CG-W1`, Day 1); `RWB-P7-E1027-APP` (App development, `L-P7-B`, after RWB-P7-E1008-APP).
- integration: `RWB-ITG-E1027-ITG` (Integration, `L-ITG-W1`, Day 1).
- platform: `RWB-PLT-E1027-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1027-APP` (App development, `L-PLT-LIB-C`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P7-E1027-APP` after RWB-P7-E1008-APP.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision`; `lov_value` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19. Build (H): `RWB-P7-E1008-APP`, `RWB-P7-E1027-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P7-E1027-APP`, `RWB-PLT-E1027-APP`. External (X): `RWB-PLT-E1056-OPS`.

**What moves.** The writer stays with P7 `rwb_decision`; the library that other services embed is RWB-PLT-E1027 and the shared topic is `rwb.decision-record.v1` (DP-03). P7 also serves `GET /api/recovery/decision/v1/decision-log`.

## RWB-E1-028 Service levels, timers, escalation and prescription dates

Module: P3 Case and workflow

**View.** `v_ace_account` for days past due and the prescription basis; reads `recovery_case`, `case_account`, `reference_row` and writes `timer` and `decision_log_entry`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP03 Case and ownership, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 read `loan_account.days_past_due` and `last_payment_date`. v5 reads the same two values from `v_ace_account`; the calendar comes from `v_ace_holiday`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P7 `rwb-decision`.

- P3 `rwb-case`: `RWB-P3-E1028-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1028-APP` (App development, `L-P3-F`, after RWB-P3-E1045-APP, RWB-P3-E1020-APP); `RWB-P3-E1028-OPS` (DevOps, `L-P3-K`, Day 1).
- integration: `RWB-ITG-E1028-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1028-APP` (App development, `L-P4-U`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1028-APP` (App development, `L-P7-I`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P3-E1028-APP` after RWB-P3-E1045-APP, RWB-P3-E1020-APP.

**Tables and owner.** `case_account` P3 `rwb_case`; `data_product_load` P1 `rwb_source_data`; `decision_log_entry` P7 `rwb_decision`; `recovery_case` P3 `rwb_case`; `reference_row` P3 `rwb_case`; `timer` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1020-APP`, `RWB-P3-E1028-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P3-E1045-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1028-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P3-E1028-APP`, `RWB-P4-E1028-APP`, `RWB-P7-E1028-APP`. External (X): `RWB-P3-E1028-OPS`.

**What moves.** Service levels and timers are P3 `rwb_case`: the clock is a durable timer inside `CaseWorkflow` and `timer` remains the screen projection (Ownership Map ruling, ASM-0078). Days past due and the prescription basis come from P1's account read, and the decision entries are P7's.

## RWB-E1-030 Daily rebalancing and queue measures

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `queue`, `queue_member` and `timer` and writes `queue_measure` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 started JOB-06 at 06:30 or when JOB-03 completed. v5 keeps that chain; the one load shaped wait behind it, the case list, now reads `v_ace_batch_status` through RWB-E1-002. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`; P7 `rwb-decision`.

- P3 `rwb-case`: `RWB-P3-E1030-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1030-APP` (App development, `L-P3-F`, after RWB-P3-E1020-APP); `RWB-P3-E1030-OPS` (DevOps, `L-P3-L`, Day 1).
- integration: `RWB-ITG-E1030-ITG` (Integration, `L-ITG-W1`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1030-APP` (App development, `L-P7-J`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P3-E1030-APP` after RWB-P3-E1020-APP.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision`; `queue` P3 `rwb_case`; `queue_measure` P3 `rwb_case`; `queue_member` P3 `rwb_case`; `recovery_case` P3 `rwb_case`; `timer` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP17, DP19. Build (H): `RWB-P3-E1020-APP`, `RWB-P3-E1028-CON`, `RWB-P3-E1030-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1030-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P3-E1030-APP`, `RWB-P7-E1030-APP`. External (X): `RWB-P3-E1030-OPS`.

**What moves.** Rebalancing stays with P3 `rwb_case` and runs as a Temporal Schedule in `rwb-case` (JOB-06, Arch v5 slide 44), not as a Quartz job. The case list it waits on comes from P1's contract, and the decision entries are P7's.

## RWB-E1-031 Queue and owner on the case list with filters

Module: P3 Case and workflow

**View.** No view. The case list filters read `recovery_case` and `queue` through the P3 interface.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 showed the product from the case record. v5 keeps that column and takes the product category from `v_ace_account` when the caller may see it. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); integration `RWB-ITG-W1`.

- P3 `rwb-case`: `RWB-P3-E1031-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1031-APP` (App development, `L-P3-F`, after RWB-P3-E1020-APP).
- integration: `RWB-ITG-E1031-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 2 of the 3 stories; `RWB-P3-E1031-APP` after RWB-P3-E1020-APP.

**Tables and owner.** `queue` P3 `rwb_case`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1020-APP`, `RWB-P3-E1031-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P4-E1037-CON`, `RWB-P4-E1039-CON`. Integration (I): `RWB-P3-E1031-APP`, `RWB-P4-E1039-APP`. External (X): none.

**What moves.** The queue and owner filter is P3 `rwb_case`, served by `GET /api/recovery/case/v1/cases` and `/queues/{queueId}/cases`. The product category shown when the caller may see it comes from P1's account read.

## RWB-E1-032 Automatic attach from the OCR intake

Module: P5 Document hub

**View.** `v_ace_account` for the account key that the intake matches; reads `document_intake`, `document_text` and `document` and writes `decision_log_entry`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 ran the match step in JOB-12 against the case and account rows. v5 matches to the account key and product on `v_ace_account`; the job step stays, the copy read does not. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`; P6 `rwb-comms`; P7 `rwb-decision`; S9 `rwb-partner`.

- P5 `rwb-document`: `RWB-P5-E1032-CON` (Contract, `CG-W1`, Day 1); `RWB-P5-E1032-APP` (App development, `L-P5-G`, after RWB-P5-E1024-APP); `RWB-P5-E1032-INF` (Infrastructure, `L-P5-I`, Day 1); `RWB-P5-E1032-OPS` (DevOps, `L-P5-H`, Day 1).
- integration: `RWB-ITG-E1032-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1032-APP` (App development, `L-P3-M`, Day 1).
- P6 `rwb-comms`: `RWB-P6-E1032-APP` (App development, `L-P6-E`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1032-APP` (App development, `L-P7-K`, Day 1).
- S9 `rwb-partner`: `RWB-S9-E1032-APP` (App development, `L-S9-B`, Day 1).

Ready to start: Day 1 for 8 of the 9 stories; `RWB-P5-E1032-APP` after RWB-P5-E1024-APP.

**Tables and owner.** `data_product_load` P1 `rwb_source_data`; `decision_log_entry` P7 `rwb_decision`; `document` P5 `rwb_document`; `document_intake` P5 `rwb_document`; `document_text` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19. Build (H): `RWB-P5-E1024-APP`, `RWB-P5-E1032-CON`, `RWB-P5-E1050-CON`, `RWB-P5-E1053-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P5-E1032-CON`. Integration (I): `RWB-P3-E1032-APP`, `RWB-P5-E1032-APP`, `RWB-P6-E1032-APP`, `RWB-P7-E1032-APP`, `RWB-S9-E1032-APP`. External (X): `RWB-P5-E1032-INF`, `RWB-P5-E1032-OPS`.

**What moves.** The OCR intake attach is P5 `rwb_document`. The account key it matches comes from P1's account read, the intake can also arrive from a partner SFTP (S9 slice), and the decision entry is P7's.

## RWB-E1-033 Search across cases

Module: P5 Document hub

**View.** No view. Search reads `document_text`, `document_field` and `document`; an ACE field is shown by its dictionary entry.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 searched the stored document text and fields. v5 searches the same Workbench index; an ACE field is reached through the views only when a document links to one. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary).

- P5 `rwb-document`: `RWB-P5-E1033-APP` (App development, `L-P5-G`, after RWB-P5-E1024-APP, RWB-P5-E1049-APP).

Ready to start: Day 1 for 0 of the 1 stories; `RWB-P5-E1033-APP` after RWB-P5-E1024-APP, RWB-P5-E1049-APP.

**Tables and owner.** `document` P5 `rwb_document`; `document_field` P5 `rwb_document`; `document_text` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP11, DP15, DP19. Build (H): `RWB-P5-E1024-APP`, `RWB-P5-E1049-APP`, `RWB-P5-E1053-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): none. External (X): none.

**What moves.** Search stays with P5 `rwb_document` over `document_text`, `document_field` and `document`. An ACE field is reached through the P1 view contract and only when a document links to one.

## RWB-E1-034 Letter template management

Module: P6 Communications

**View.** No view. The story owns `template` and reads `merge_field` and `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A merge field names a BR Field ID; the value is read from the owning interface at generation. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P6 `rwb-comms` (primary); integration `RWB-ITG-W1`.

- P6 `rwb-comms`: `RWB-P6-E1034-APP` (App development, `L-P6-A`, after RWB-P6-E1046-APP).
- integration: `RWB-ITG-E1034-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P6-E1034-APP` after RWB-P6-E1046-APP.

**Tables and owner.** `lov_value` P3 `rwb_case`; `merge_field` P6 `rwb_comms`; `template` P6 `rwb_comms` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP07, DP13, DP19. Build (H): `RWB-P6-E1046-APP`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P1-E1015-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1015-APP`, `RWB-P6-E1034-APP`. External (X): none.

**What moves.** Letter template management is P6 `rwb_comms`, which owns `template`, `merge_field` and the notice catalogue. The LOV rows are P3's reference data, read by contract (DP-07).

## RWB-E1-035 Case record view v1.1 with documents and history timeline

Module: P3 Case and workflow

**View.** No view. The timeline reads `interaction`, `document`, `assignment` and `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP05 Contact and promises, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 built each timeline entry from the ledger and the document store. v5 keeps that and adds the source reference the ledger already carries for an ACE-sourced event. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary).

- P3 `rwb-case`: `RWB-P3-E1035-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1035-APP` (App development, `L-P3-F`, after RWB-P3-E1023-APP).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P3-E1035-APP` after RWB-P3-E1023-APP.

**Tables and owner.** `assignment` P3 `rwb_case`; `data_product_load` P1 `rwb_source_data`; `decision_log_entry` P7 `rwb_decision`; `document` P5 `rwb_document`; `interaction` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP11, DP13, DP14, DP15, DP18, DP19. Build (H): `RWB-P3-E1021-CON`, `RWB-P3-E1023-APP`, `RWB-P3-E1035-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P7-E1027-CON`. Integration (I): none. External (X): none.

**What moves.** The timeline is P3 `rwb_case`; `interaction` is owned by P1 `rwb_source_data` (DP-18 ruling), so the timeline reads the ledger by contract. Documents come from P5 and decision entries from P7.

## RWB-E1-037 Role to permission matrix as data and PDPA field masking by role

Module: P4 Access and administration

**View.** `v_ace_customer` and `v_ace_contact` for the masking rules and the two masked identity fields; owns `role`, `permission`, `masking_rule` and writes `decision_log_entry`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP02 Customer and party, DAILY, expected 08:00; DP14 Reference data, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 masked the personal fields of the copy tables through FieldMasker. v5 masks the view columns and never sees a clear identity number, because `v_ace_customer` exposes only `id_no_masked` and `id_no_last4`. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P4 `rwb-access` (primary); integration `RWB-ITG-W1`; platform (wave 0, `CG-W0` and `L-PLT-*`).

- P4 `rwb-access`: `RWB-P4-E1037-CON` (Contract, `CG-W1`, Day 1); `RWB-P4-E1037-APP` (App development, `L-P4-A`, after RWB-P4-E1022-APP).
- integration: `RWB-ITG-E1037-ITG` (Integration, `L-ITG-W1`, Day 1).
- platform: `RWB-PLT-E1037-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1037-APP` (App development, `L-PLT-LIB-D`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P4-E1037-APP` after RWB-P4-E1022-APP.

**Tables and owner.** `data_product_load` P1 `rwb_source_data`; `decision_log_entry` P7 `rwb_decision`; `masking_rule` P4 `rwb_access`; `permission` P4 `rwb_access`; `role` P4 `rwb_access` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP10, DP11, DP13, DP15, DP17, DP19. Build (H): `RWB-P4-E1022-APP`, `RWB-P4-E1037-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P1-E1069-APP`, `RWB-P4-E1037-APP`, `RWB-PLT-E1037-APP`. External (X): none.

**What moves.** The role to permission matrix and masking policy are P4 `rwb_access`, and the guard library other services embed is RWB-PLT-E1037 (DP-08). The two masked identity fields come from P1's customer read, which never exposes a clear identity number.

## RWB-E1-038 Delegation of authority table as reference data

Module: P4 Access and administration

**View.** No view. The story loads `delegation_limit` and reads `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Limit 0 to 95 are loaded as reference data; no approval level reads an ACE table. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P4 `rwb-access` (primary).

- P4 `rwb-access`: `RWB-P4-E1038-APP` (App development, `L-P4-J`, Day 1).

Ready to start: Day 1 for 1 of the 1 stories.

**Tables and owner.** `delegation_limit` P4 `rwb_access`; `lov_value` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP06, DP07, DP08, DP11, DP13, DP15, DP19. Build (H): `RWB-P4-E1037-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): none. External (X): none.

**What moves.** The delegation of authority table is P4 `rwb_access` (Ownership Map ruling, ASM-0070) and is read by `GET /api/recovery/access/v1/doa-limits`. The LOV rows are P3's reference data, read by contract.

## RWB-E1-039 Access log into the decision log and break-glass admin

Module: P4 Access and administration, with P7 Decision center and log

**View.** No view. The story writes `decision_log_entry` and reads `role` and `permission`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A break-glass action is a decision log entry with its reason and its expiry. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P4 `rwb-access` (primary); integration `RWB-ITG-W1`; P7 `rwb-decision`; P5 `rwb-document`.

- P4 `rwb-access`: `RWB-P4-E1039-CON` (Contract, `CG-W1`, Day 1); `RWB-P4-E1039-APP` (App development, `L-P4-A`, after RWB-P4-E1022-APP); `RWB-P4-E1039-DB` (ACE DB, `L-P4-W`, Day 1); `RWB-P4-E1039-OPS` (DevOps, `L-P4-V`, Day 1).
- integration: `RWB-ITG-E1039-ITG` (Integration, `L-ITG-W1`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1039-APP` (App development, `L-P7-L`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1039-APP` (App development, `L-P5-J`, Day 1).

Ready to start: Day 1 for 6 of the 7 stories; `RWB-P4-E1039-APP` after RWB-P4-E1022-APP.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision`; `permission` P4 `rwb_access`; `role` P4 `rwb_access` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP11, DP13, DP17, DP19. Build (H): `RWB-P4-E1022-APP`, `RWB-P4-E1039-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1039-CON`, `RWB-P7-E1008-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P4-E1039-APP`, `RWB-P5-E1039-APP`, `RWB-P7-E1008-APP`, `RWB-P7-E1039-APP`. External (X): `RWB-P4-E1039-DB`, `RWB-P4-E1039-OPS`.

**What moves.** Access logging is P4 `rwb_access`: a break-glass action is a decision record written through the RWB-PLT-E1027 library and stored in P7's ledger (DP-03). The P5 and P7 slices consume the event.

## RWB-E1-040 Document checklist per case type as reference data

Module: P5 Document hub

**View.** No view. The story loads `document_checklist_item` and reads `document_type`, `document`, `case_document_check` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The checklist names document types, not source tables. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary).

- P5 `rwb-document`: `RWB-P5-E1040-APP` (App development, `L-P5-G`, after RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP).

Ready to start: Day 1 for 0 of the 1 stories; `RWB-P5-E1040-APP` after RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP.

**Tables and owner.** `case_document_check` P5 `rwb_document`; `document` P5 `rwb_document`; `document_checklist_item` P5 `rwb_document`; `document_type` P5 `rwb_document`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP07, DP09, DP10, DP11, DP13, DP15, DP19. Build (H): `RWB-P5-E1024-APP`, `RWB-P5-E1025-APP`, `RWB-P5-E1026-APP`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1043-CON`. Integration (I): none. External (X): none.

**What moves.** The document checklist is P5 `rwb_document` reference data over its own `document_type`, `document` and `case_document_check`. The case key comes from P3's contract.

## RWB-E1-041 Retention classes and virus scan on intake

Module: P5 Document hub

**View.** No view. The story owns `retention_rule`, `retention_action` and the scan state on `document_intake`; reads `document`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Retention classes apply to Workbench documents; ACE source documents stay in ACE. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary).

- P5 `rwb-document`: `RWB-P5-E1041-CON` (Contract, `CG-W1`, Day 1); `RWB-P5-E1041-APP` (App development, `L-P5-G`, after RWB-P5-E1024-APP, RWB-P5-E1049-APP).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P5-E1041-APP` after RWB-P5-E1024-APP, RWB-P5-E1049-APP.

**Tables and owner.** `document` P5 `rwb_document`; `document_intake` P5 `rwb_document`; `retention_action` P5 `rwb_document`; `retention_rule` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP18, DP19. Build (H): `RWB-P5-E1024-APP`, `RWB-P5-E1049-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`. Integration (I): none. External (X): none.

**What moves.** Retention classes and the virus scan are P5 `rwb_document`, which owns `retention_rule`, `retention_action` and the scan state. ACE source documents stay in ACE, and the scan runs on the P5 intake only.

## RWB-E1-042 Central configuration service and parameter catalog

Module: P3 Case and workflow

**View.** No view. The story owns `parameter_catalog` and `parameter_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Parameters are data; no environment name or source table is written in code. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); platform (wave 0, `CG-W0` and `L-PLT-*`).

- P3 `rwb-case`: `RWB-P3-E1042-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1042-APP` (App development, `L-P3-N`, Day 1).
- platform: `RWB-PLT-E1042-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1042-APP` (App development, `L-PLT-LIB-F`, Day 1); `RWB-PLT-E1042-OPS` (DevOps, `L-PLT-LIB-E`, Day 1).

Ready to start: Day 1 for 5 of the 5 stories.

**Tables and owner.** `parameter_catalog` P3 `rwb_case`; `parameter_value` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP09, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): none. Integration (I): none. External (X): none.

**What moves.** The parameter catalogue stays with P3 `rwb_case` (R-PREC default ruling, DP-06) and is served by `GET /api/recovery/case/v1/admin/parameters`. The client library other services embed is RWB-PLT-E1042; the story is preserved, and the microservice change ships as the platform CON and APP stories and the P3 CON and APP stories.

## RWB-E1-043 Reference data service with versioned tables

Module: P3 Case and workflow

**View.** No view. The story owns `reference_version`, `reference_row` and `lov_value`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The reference load service is the only path that changes a versioned table. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary); platform (wave 0, `CG-W0` and `L-PLT-*`).

- P3 `rwb-case`: `RWB-P3-E1043-CON` (Contract, `CG-W1`, Day 1); `RWB-P3-E1043-APP` (App development, `L-P3-O`, Day 1).
- platform: `RWB-PLT-E1043-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1043-APP` (App development, `L-PLT-LIB-G`, Day 1).

Ready to start: Day 1 for 4 of the 4 stories.

**Tables and owner.** `lov_value` P3 `rwb_case`; `reference_row` P3 `rwb_case`; `reference_version` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP04, DP05, DP06, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19. Build (H): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P4-E1037-CON`. Integration (I): none. External (X): none.

**What moves.** Versioned reference data stays with P3 `rwb_case` (R-PREC default ruling, DP-07) and is served by the reference-load endpoints. The client library other services embed is RWB-PLT-E1043; the story is preserved, and the microservice change ships as the platform CON and APP stories and the P3 CON and APP stories.

## RWB-E1-044 Database migrations versioned with parameterized schema names

Module: P3 Case and workflow

**View.** No view. The story owns the migration path and the schema name parameter; it creates no table of its own.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** v4 shipped a baseline migration file. v5 rules that RWB-E1-044 ships no production migration file; RWB-E1-001 owns V0001 and RWB-E1-069 owns V0002 and V0003. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-E1044-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1044-APP` (App development, `L-PLT-TPL-G`, Day 1); `RWB-PLT-E1044-APP-2` (App development, `L-PLT-TPL-F`, Day 1); `RWB-PLT-E1044-OPS` (DevOps, `L-PLT-TPL-H`, Day 1).

Ready to start: Day 1 for 4 of the 4 stories.

**Tables and owner.** No table in the service schemas; the objects are platform, template or deployment artefacts.

**Dependencies.** Patterns: DP01, DP05, DP06, DP07, DP13, DP14, DP15, DP19. Build (H): `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): none. External (X): `RWB-PLT-E1044-OPS`.

**What moves.** Database migrations become the platform template rule RWB-PLT-E1044 (DP-15): one Flyway sequence per service in that service's own schema. The preserved story keeps its base ID and the microservice change ships as `RWB-PLT-E1044-APP-2`.

## RWB-E1-045 Multi-product parameters for Mortgage, HP and SSME

Module: P3 Case and workflow

**View.** No view. The story reads `recovery_case`, `reference_row` and `timer` and writes `parameter_value` rows for the three products.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 already held the three products as reference data. v5 keeps that and adds the product category from `v_ace_account` as the key the parameters are read by. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P3 `rwb-case` (primary).

- P3 `rwb-case`: `RWB-P3-E1045-APP` (App development, `L-P3-F`, Day 1).

Ready to start: Day 1 for 1 of the 1 stories.

**Tables and owner.** `parameter_value` P3 `rwb_case`; `recovery_case` P3 `rwb_case`; `reference_row` P3 `rwb_case`; `timer` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP05, DP06, DP07, DP11, DP13, DP14, DP19. Build (H): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`. Contract (C): none. Integration (I): none. External (X): none.

**What moves.** Multi-product parameters stay with P3 `rwb_case`; the product category they are keyed by comes from P1's account read. The three products stay reference data, and no ACE table is read.

## RWB-E1-046 Template and merge field catalog as data

Module: P6 Communications

**View.** No view. The story loads `merge_field` and reads `lov_value` and `template`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 checked each merge field against the copy tables. v5 checks it against the dictionary, where the 30 views and the Workbench tables both have rows. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P6 `rwb-comms` (primary); integration `RWB-ITG-W1`; P7 `rwb-decision`; P5 `rwb-document`.

- P6 `rwb-comms`: `RWB-P6-E1046-CON` (Contract, `CG-W1`, Day 1); `RWB-P6-E1046-APP` (App development, `L-P6-A`, Day 1).
- integration: `RWB-ITG-E1046-ITG` (Integration, `L-ITG-W1`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1046-APP` (App development, `L-P7-M`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1046-APP` (App development, `L-P5-K`, Day 1).

Ready to start: Day 1 for 5 of the 5 stories.

**Tables and owner.** `lov_value` P3 `rwb_case`; `merge_field` P6 `rwb_comms`; `template` P6 `rwb_comms` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP07, DP11, DP13, DP15, DP19. Build (H): `RWB-P6-E1046-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`, `RWB-P6-E1046-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P1-E1069-APP`, `RWB-P5-E1046-APP`, `RWB-P6-E1046-APP`, `RWB-P7-E1046-APP`. External (X): none.

**What moves.** The template and merge field catalogue is P6 `rwb_comms` reference data. The fields are checked against P1's dictionary contract, so a merge field names a BR Field ID and never a source column.

## RWB-E1-047 Feature flags for module release with a removal date

Module: P2 Integration

**View.** No view. The story owns `feature_flag` and `feature_flag_change`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Section B features keep a flag until RWB-ACE-001 is deployed and V0003 applies. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** integration `RWB-ITG-W1`; platform (wave 0, `CG-W0` and `L-PLT-*`).

- integration: `RWB-ITG-E1047-ITG` (Integration, `L-ITG-W1`, Day 1).
- platform: `RWB-PLT-E1047-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-E1047-APP` (App development, `L-PLT-LIB-H`, Day 1).

Ready to start: Day 1 for 3 of the 3 stories.

**Tables and owner.** `feature_flag` platform library (no service schema); `feature_flag_change` platform library (no service schema) (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP07, DP10, DP11, DP14, DP15, DP19. Build (H): `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1047-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-PLT-E1047-APP`. External (X): none.

**What moves.** Feature flags move to the platform library (R-PREC default ruling, ASM-0073), which owns `feature_flag` and `feature_flag_change`; P2's admin API serves them (GAP-3161). Section B features keep a flag until RWB-ACE-001 is deployed and V0003 applies.

## RWB-E1-049 OCR pipeline on the Workbench document hub

Module: P5 Document hub

**View.** No view. The OCR pipeline reads `document_intake` and writes `document_text` and `document_hub_parameter`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. OCR reads the Workbench document copy; no ACE table is read. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`; P6 `rwb-comms`.

- P5 `rwb-document`: `RWB-P5-E1049-CON` (Contract, `CG-W1`, Day 1); `RWB-P5-E1049-APP` (App development, `L-P5-G`, after RWB-P5-E1024-APP); `RWB-P5-E1049-INF` (Infrastructure, `L-P5-M`, Day 1); `RWB-P5-E1049-OPS` (DevOps, `L-P5-L`, Day 1).
- integration: `RWB-ITG-E1049-ITG` (Integration, `L-ITG-W1`, Day 1).
- P6 `rwb-comms`: `RWB-P6-E1049-APP` (App development, `L-P6-F`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P5-E1049-APP` after RWB-P5-E1024-APP.

**Tables and owner.** `document_hub_parameter` P5 `rwb_document`; `document_intake` P5 `rwb_document`; `document_text` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19. Build (H): `RWB-P5-E1024-APP`, `RWB-P5-E1049-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P5-E1049-CON`. Integration (I): `RWB-P3-E1045-APP`, `RWB-P5-E1049-APP`, `RWB-P6-E1049-APP`. External (X): `RWB-P5-E1049-INF`, `RWB-P5-E1049-OPS`, `RWB-PLT-TE012-APP`.

**What moves.** The OCR pipeline stays with P5 `rwb_document`, which owns `document_intake`, `document_text` and `document_hub_parameter`. The worker pool runs in the P5 namespace, and the P6 slice consumes `DocumentFieldsExtracted`.

## RWB-E1-050 Document classification

Module: P5 Document hub

**View.** No view. Classification reads `document_text` and `document_type` and writes the type on `document_intake`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The classifier reads the document text only. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`.

- P5 `rwb-document`: `RWB-P5-E1050-CON` (Contract, `CG-W1`, Day 1); `RWB-P5-E1050-APP` (App development, `L-P5-G`, after RWB-P5-E1049-APP, RWB-P5-E1025-APP); `RWB-P5-E1050-OPS` (DevOps, `L-P5-N`, Day 1).
- integration: `RWB-ITG-E1050-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1050-APP` (App development, `L-P3-P`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P5-E1050-APP` after RWB-P5-E1049-APP, RWB-P5-E1025-APP.

**Tables and owner.** `document_intake` P5 `rwb_document`; `document_text` P5 `rwb_document`; `document_type` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP10, DP11, DP15, DP19. Build (H): `RWB-P5-E1025-APP`, `RWB-P5-E1049-APP`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P3-E1050-APP`, `RWB-P5-E1050-APP`. External (X): `RWB-P5-E1050-OPS`.

**What moves.** Classification stays with P5 `rwb_document`; the P3 slice links the classified document to the case by contract. The classifier reads the document text only.

## RWB-E1-052 Notice generation v1

Module: P6 Communications

**View.** `v_ace_account`, `v_ace_customer`, `v_ace_contact` and `v_ace_pod` for the merge values and the proof of delivery; reads `template`, `merge_field`, `case_party` and `recovery_case`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP02 Customer and party, DAILY, expected 08:00; DP07 Legal events and cases, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 merged values from the party, account and contact copy tables. v5 reads them from the views; the proof of delivery comes from `v_ace_pod` and stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P6 `rwb-comms` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`; P7 `rwb-decision`; P5 `rwb-document`.

- P6 `rwb-comms`: `RWB-P6-E1052-CON` (Contract, `CG-W1`, Day 1); `RWB-P6-E1052-APP` (App development, `L-P6-A`, after RWB-P6-E1046-APP).
- integration: `RWB-ITG-E1052-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1052-APP` (App development, `L-P3-Q`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1052-APP` (App development, `L-P7-N`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1052-APP` (App development, `L-P5-O`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P6-E1052-APP` after RWB-P6-E1046-APP.

**Tables and owner.** `case_party` P3 `rwb_case`; `data_product_load` P1 `rwb_source_data`; `merge_field` P6 `rwb_comms`; `recovery_case` P3 `rwb_case`; `template` P6 `rwb_comms` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19. Build (H): `RWB-P6-E1046-APP`, `RWB-P6-E1052-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P1-E1015-CON`, `RWB-P3-E1018-CON`, `RWB-P3-E1043-CON`, `RWB-P6-E1052-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P1-E1015-APP`, `RWB-P1-E1069-APP`, `RWB-P3-E1018-APP`, `RWB-P3-E1052-APP`, `RWB-P5-E1052-APP`, `RWB-P6-E1052-APP`, `RWB-P7-E1052-APP`. External (X): none.

**What moves.** Notice generation is P6 `rwb_comms`: the merge values come from P1's account, customer and contact reads, the proof of delivery from P1's `v_ace_pod` read, the documents from P5 and the approval from P7. P6 names no ACE view.

## RWB-E1-053 Field extraction for the six types into the index

Module: P5 Document hub

**View.** No view. Extraction reads `document_text` and `document_type` and writes `document_field`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. Extracted values stay Workbench records; an ACE field is compared through its dictionary entry, never written back. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary).

- P5 `rwb-document`: `RWB-P5-E1053-CON` (Contract, `CG-W1`, Day 1); `RWB-P5-E1053-APP` (App development, `L-P5-G`, after RWB-P5-E1049-APP, RWB-P5-E1025-APP).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P5-E1053-APP` after RWB-P5-E1049-APP, RWB-P5-E1025-APP.

**Tables and owner.** `document_field` P5 `rwb_document`; `document_text` P5 `rwb_document`; `document_type` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20. Build (H): `RWB-P5-E1025-APP`, `RWB-P5-E1049-APP`, `RWB-P5-E1050-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P10-TE013-CON`, `RWB-P3-E1043-CON`. Integration (I): none. External (X): none.

**What moves.** Field extraction stays with P5 `rwb_document`. An ACE field is compared through the P1 dictionary entry and never written back.

## RWB-E1-054 Review queue for low-confidence documents

Module: P5 Document hub

**View.** No view. The review queue reads `document_intake`, `document_text`, `document_field` and `recovery_case` and writes `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. A reviewer confirms a Workbench field; no ACE object is updated. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P3 `rwb-case`; P7 `rwb-decision`.

- P5 `rwb-document`: `RWB-P5-E1054-CON` (Contract, `CG-W1`, Day 1); `RWB-P5-E1054-APP` (App development, `L-P5-G`, after RWB-P5-E1049-APP, RWB-P5-E1032-APP).
- integration: `RWB-ITG-E1054-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1054-APP` (App development, `L-P4-X`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1054-APP` (App development, `L-P3-R`, Day 1).
- P7 `rwb-decision`: `RWB-P7-E1054-APP` (App development, `L-P7-O`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P5-E1054-APP` after RWB-P5-E1049-APP, RWB-P5-E1032-APP.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision`; `document_field` P5 `rwb_document`; `document_intake` P5 `rwb_document`; `document_text` P5 `rwb_document`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19. Build (H): `RWB-P5-E1032-APP`, `RWB-P5-E1049-APP`, `RWB-P5-E1050-CON`, `RWB-P5-E1053-CON`, `RWB-P5-E1054-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1035-CON`, `RWB-P3-E1043-CON`, `RWB-P5-E1054-CON`. Integration (I): `RWB-P3-E1035-APP`, `RWB-P3-E1054-APP`, `RWB-P4-E1054-APP`, `RWB-P5-E1054-APP`, `RWB-P7-E1054-APP`. External (X): none.

**What moves.** The review queue is P5 `rwb_document`; masking follows P4's policy, the case key comes from P3's contract and the decision entry from P7. A reviewer confirms a Workbench field, and no ACE object is updated.

## RWB-E1-055 Proof of delivery capture design with WIN

Module: P6 Communications

**View.** `v_ace_account`, `v_ace_contact` and `v_ace_pod` for the delivery evidence; reads `case_account`, `notice` and `template`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP07 Legal events and cases, DAILY, expected 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 waited on the INT-15 load. v5 reads `v_ace_pod` after ACE ingests the WIN result; the proof path stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P6 `rwb-comms` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`; P5 `rwb-document`; P1 `rwb-source-data`.

- P6 `rwb-comms`: `RWB-P6-E1055-CON` (Contract, `CG-W1`, Day 1); `RWB-P6-E1055-APP` (App development, `L-P6-A`, after RWB-P6-E1052-APP); `RWB-P6-E1055-INF` (Infrastructure, `L-P6-H`, Day 1); `RWB-P6-E1055-OPS` (DevOps, `L-P6-G`, Day 1).
- integration: `RWB-ITG-E1055-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1055-APP` (App development, `L-P3-S`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1055-APP` (App development, `L-P5-P`, Day 1).
- P1 `rwb-source-data`: `RWB-P1-E1055-APP` (App development, `L-P1-M`, Day 1).

Ready to start: Day 1 for 7 of the 8 stories; `RWB-P6-E1055-APP` after RWB-P6-E1052-APP.

**Tables and owner.** `case_account` P3 `rwb_case`; `data_product_load` P1 `rwb_source_data`; `notice` P6 `rwb_comms`; `template` P6 `rwb_comms` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP05, DP07, DP09, DP10, DP11, DP15, DP18, DP19. Build (H): `RWB-P6-E1052-APP`, `RWB-P6-E1055-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P1-E1066-CON`, `RWB-P3-E1028-CON`, `RWB-P3-E1043-CON`, `RWB-P5-E1054-CON`, `RWB-P6-E1055-CON`. Integration (I): `RWB-P1-E1055-APP`, `RWB-P1-E1066-APP`, `RWB-P3-E1028-APP`, `RWB-P3-E1055-APP`, `RWB-P5-E1054-APP`, `RWB-P5-E1055-APP`, `RWB-P6-E1055-APP`. External (X): `RWB-P6-E1055-INF`, `RWB-P6-E1055-OPS`.

**What moves.** Proof of delivery is P6 `rwb_comms`; the delivery evidence comes from P1's `v_ace_pod` read, the case from P3, the notice from P6 and the document from P5. P1's read stays behind its flag until RWB-ACE-001 lands.

## RWB-E1-056 Run books and monitoring for every Epic 1 Workbench job

Module: P2 Integration

**View.** `v_ace_batch_status` for the ACE batch state; reads `job_catalog`, `data_product_load`, `case_list_row` and `reconciliation_result`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 gave every Epic 1 job a run book, most of them load jobs. v5 gives a run book to every Workbench job and to the ACE batch record the Workbench depends on; the load jobs no longer exist. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-E1056-OPS` (DevOps, `L-PLT-OBS-B`, Day 1).

Ready to start: Day 1 for 1 of the 1 stories.

**Tables and owner.** `case_list_row` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `job_catalog` P2 `rwb_integration`; `reconciliation_result` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP15, DP19. Build (H): none. Contract (C): none. Integration (I): none. External (X): none.

**What moves.** The run books and monitoring are platform work: RWB-PLT-E1056-OPS gives every Workbench job and the ACE batch record a run book, and each service's own run book rows move to its ops lane (GAP-3164). The `job_catalog` view stays with P2 (Ownership Map ruling).

## RWB-E1-057 Intake from branches, mailroom, partner SFTP and email

Module: P5 Document hub

**View.** No view. Intake reads `document_intake` and `document_hub_parameter` and writes the received file record.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 ran intake as JOB-12 and stored each file in the document hub. v5 keeps that path and the source reference; ACE ingests no document from it. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P5 `rwb-document` (primary); integration `RWB-ITG-W1`; S9 `rwb-partner`.

- P5 `rwb-document`: `RWB-P5-E1057-CON` (Contract, `CG-W1`, Day 1); `RWB-P5-E1057-APP` (App development, `L-P5-G`, after RWB-P5-E1049-APP); `RWB-P5-E1057-INF` (Infrastructure, `L-P5-R`, Day 1); `RWB-P5-E1057-OPS` (DevOps, `L-P5-Q`, Day 1).
- integration: `RWB-ITG-E1057-ITG` (Integration, `L-ITG-W1`, Day 1).
- S9 `rwb-partner`: `RWB-S9-E1057-APP` (App development, `L-S9-C`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P5-E1057-APP` after RWB-P5-E1049-APP.

**Tables and owner.** `document_hub_parameter` P5 `rwb_document`; `document_intake` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19. Build (H): `RWB-P5-E1041-CON`, `RWB-P5-E1049-APP`, `RWB-P5-E1057-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P5-E1057-CON`. Integration (I): `RWB-P5-E1057-APP`, `RWB-S9-E1057-APP`. External (X): `RWB-P5-E1057-INF`, `RWB-P5-E1057-OPS`, `RWB-PLT-TE012-APP`.

**What moves.** Intake is P5 `rwb_document`, with a partner SFTP source from S9 and the worker pool in the P5 namespace. ACE ingests no document from this path, and the file record stays in `document_intake`.

## RWB-E1-058 Agent platform set-up [E1a]

Module: P10 Agent runtime

**View.** No view. The agent platform reads `recovery_case`, `rule_row` and `agent_policy` and writes the agent tables.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP14 Reference data, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** v4 depended on the ALS load before an agent test could see cases. v5 seeds cases in the sandbox and reads ACE data through the views, so no load gate remains. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P10 `rwb-agent` (primary); integration `RWB-ITG-W1`.

- P10 `rwb-agent`: `RWB-P10-E1058-CON` (Contract, `CG-W1`, Day 1); `RWB-P10-E1058-APP` (App development, `L-P10-A`, Day 1); `RWB-P10-E1058-INF` (Infrastructure, `L-P10-B`, Day 1); `RWB-P10-E1058-OPS` (DevOps, `L-P10-C`, Day 1).
- integration: `RWB-ITG-E1058-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 5 of the 5 stories.

**Tables and owner.** `agent_policy` P10 `rwb_agent`; `recovery_case` P3 `rwb_case`; `rule_row` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP08, DP09, DP11, DP13, DP15, DP19, DP20. Build (H): `RWB-P10-E1058-CON`, `RWB-P10-TE013-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): `RWB-P1-E1001-APP`, `RWB-P1-E1069-APP`, `RWB-P10-E1058-APP`. External (X): `RWB-P10-E1058-INF`, `RWB-P10-E1058-OPS`.

**What moves.** The agent platform is P10 `rwb_agent`, which owns `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation`, `agent_evaluation_run`, `agent_feedback` and `agent_alert`. The case facts come from P3 and the rule rows from P7, both by contract.

## RWB-E1-059 Case intake agent in shadow [E1b]

Module: P10 Agent runtime

**View.** `v_ace_valuation` and `v_ace_contact` for the shadow comparison; writes `agent_run`, `agent_sample` and `agent_evaluation_run`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP02 Customer and party, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 compared the agent against the contact and appraisal rows it held. v5 compares it against `v_ace_contact` and `v_ace_valuation`; the story stays behind its flag until RWB-ACE-001 lands. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P10 `rwb-agent` (primary); integration `RWB-ITG-W1`.

- P10 `rwb-agent`: `RWB-P10-E1059-CON` (Contract, `CG-W1`, Day 1); `RWB-P10-E1059-APP` (App development, `L-P10-A`, after RWB-P10-E1058-APP, RWB-P10-TE013-APP).
- integration: `RWB-ITG-E1059-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 2 of the 3 stories; `RWB-P10-E1059-APP` after RWB-P10-E1058-APP, RWB-P10-TE013-APP.

**Tables and owner.** `agent_evaluation_run` P10 `rwb_agent`; `agent_run` P10 `rwb_agent`; `agent_sample` P10 `rwb_agent`; `data_product_load` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP15, DP19, DP20. Build (H): `RWB-P10-E1058-APP`, `RWB-P10-E1059-CON`, `RWB-P10-TE013-APP`, `RWB-P10-TE013-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P3-E1030-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P10-E1059-APP`, `RWB-P3-E1030-APP`. External (X): none.

**What moves.** The shadow case intake agent is P10 `rwb_agent`; the values it compares come from P1's collateral and contact reads, and its results stay in the P10 tables. The ACE read stays behind P1's flag until RWB-ACE-001 lands.

## RWB-E1-060 Extraction evaluation [E1c]

Module: P10 Agent runtime

**View.** No view. The evaluation reads `document_field` and the agent tables.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The evaluation compares extracted fields with the reviewed Workbench field. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P10 `rwb-agent` (primary); integration `RWB-ITG-W1`.

- P10 `rwb-agent`: `RWB-P10-E1060-APP` (App development, `L-P10-A`, after RWB-P10-E1058-APP).
- integration: `RWB-ITG-E1060-ITG` (Integration, `L-ITG-W1`, Day 1).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P10-E1060-APP` after RWB-P10-E1058-APP.

**Tables and owner.** `document_field` P5 `rwb_document` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP13, DP15, DP19. Build (H): `RWB-P10-E1058-APP`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P10-E1060-APP`, `RWB-P5-E1053-APP`. External (X): none.

**What moves.** The extraction evaluation is P10 `rwb_agent` over P5's extracted fields, read by contract. The reviewed Workbench field is P5's record, and the agent never writes it.

## RWB-E1-061 Intake agent evaluation and L1 proposal [E2a]

Module: P10 Agent runtime

**View.** No view. The proposal reads `agent_evaluation_run`, `agent_evaluation`, `agent_run` and `agent_policy`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The L1 proposal is a decision log entry, not an automatic change. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P10 `rwb-agent` (primary).

- P10 `rwb-agent`: `RWB-P10-E1061-CON` (Contract, `CG-W1`, Day 1); `RWB-P10-E1061-APP` (App development, `L-P10-A`, after RWB-P10-E1059-APP).

Ready to start: Day 1 for 1 of the 2 stories; `RWB-P10-E1061-APP` after RWB-P10-E1059-APP.

**Tables and owner.** `agent_evaluation` P10 `rwb_agent`; `agent_evaluation_run` P10 `rwb_agent`; `agent_policy` P10 `rwb_agent`; `agent_run` P10 `rwb_agent` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP13, DP15, DP19. Build (H): `RWB-P10-E1059-APP`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): none. External (X): none.

**What moves.** The intake agent evaluation and the L1 proposal are P10 `rwb_agent`; the proposal is a decision record in P7's ledger, not an automatic case change. The case state comes from P3 by contract.

## RWB-E1-062 Deviation screening agent in shadow [E2b]

Module: P10 Agent runtime

**View.** No view. The screening reads `recovery_case`, `rule_row`, `document_field` and the agent tables; writes `deviation`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The screening agent reads Workbench records and proposes; a person decides. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P10 `rwb-agent` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; S8 `rwb-deviation`; P5 `rwb-document`.

- P10 `rwb-agent`: `RWB-P10-E1062-CON` (Contract, `CG-W1`, Day 1); `RWB-P10-E1062-APP` (App development, `L-P10-A`, after RWB-P10-E1058-APP, RWB-P10-TE013-APP).
- integration: `RWB-ITG-E1062-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1062-APP` (App development, `L-P4-Y`, Day 1).
- S8 `rwb-deviation`: `RWB-S8-E1062-APP` (App development, `L-S8-D`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1062-APP` (App development, `L-P5-S`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P10-E1062-APP` after RWB-P10-E1058-APP, RWB-P10-TE013-APP.

**Tables and owner.** `deviation` S8 `rwb_deviation`; `document_field` P5 `rwb_document`; `recovery_case` P3 `rwb_case`; `rule_row` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20. Build (H): `RWB-P10-E1058-APP`, `RWB-P10-E1062-CON`, `RWB-P10-TE013-APP`, `RWB-P10-TE013-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P10-E1062-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P10-E1062-APP`, `RWB-P4-E1062-APP`, `RWB-P5-E1062-APP`, `RWB-S8-E1062-APP`. External (X): none.

**What moves.** Screening stays with P10 `rwb_agent`, while `deviation` is owned by S8 `rwb_deviation`: the agent proposes and S8 records the deviation (Ownership Map). The P5, P7 and P4 slices supply fields, rule rows and masking.

## RWB-E1-063 Agent monitoring dashboard v1 [E2c]

Module: P10 Agent runtime

**View.** No view. The dashboard reads `agent_run`, `agent_policy`, `agent_evaluation` and `agent_alert`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The dashboard reports the agent tables and the freshness line of the products the agents read. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P10 `rwb-agent` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P6 `rwb-comms`.

- P10 `rwb-agent`: `RWB-P10-E1063-CON` (Contract, `CG-W1`, Day 1); `RWB-P10-E1063-APP` (App development, `L-P10-A`, after RWB-P10-E1058-APP); `RWB-P10-E1063-OPS` (DevOps, `L-P10-D`, Day 1).
- integration: `RWB-ITG-E1063-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1063-APP` (App development, `L-P4-Z`, Day 1).
- P6 `rwb-comms`: `RWB-P6-E1063-APP` (App development, `L-P6-I`, Day 1).

Ready to start: Day 1 for 5 of the 6 stories; `RWB-P10-E1063-APP` after RWB-P10-E1058-APP.

**Tables and owner.** `agent_alert` P10 `rwb_agent`; `agent_evaluation` P10 `rwb_agent`; `agent_policy` P10 `rwb_agent`; `agent_run` P10 `rwb_agent` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19. Build (H): `RWB-P10-E1058-APP`, `RWB-P10-E1061-CON`, `RWB-P10-E1063-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P10-E1063-CON`, `RWB-P2-E1007-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P10-E1063-APP`, `RWB-P2-E1007-APP`, `RWB-P4-E1063-APP`, `RWB-P6-E1063-APP`. External (X): `RWB-P10-E1063-OPS`.

**What moves.** The agent monitoring dashboard is P10 `rwb_agent` over its own runs, policies, evaluations and alerts, with the freshness line of the products the agents read supplied by P1. The P4, P6 and OPS slices add masking, contacts and alerting.

## RWB-E1-064 Data dictionary for the 14 data products

Module: P1 Recovery data engine

**View.** No view. The dictionary reads `sys_objects`, `sys_fields`, `sys_field_version`, `data_contract` and `data_product`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP01 Account and arrears, DAILY, expected 08:00; DP06 Collateral and assets, WEEKLY, expected MON 08:00; DP14 Reference data, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 described the copy tables. v5 describes the 92 tables and the 30 views, so the dictionary is the one place a view column and its ACE source field are defined. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`.

- P1 `rwb-source-data`: `RWB-P1-E1064-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1064-APP` (App development, `L-P1-A`, after RWB-P1-E1001-APP, RWB-P1-E1069-APP); `RWB-P1-E1064-OPS` (DevOps, `L-P1-N`, Day 1).
- integration: `RWB-ITG-E1064-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1064-APP` (App development, `L-P4-AA`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P1-E1064-APP` after RWB-P1-E1001-APP, RWB-P1-E1069-APP.

**Tables and owner.** `data_contract` P1 `rwb_source_data`; `data_product` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `sys_field_version` P1 `rwb_source_data`; `sys_fields` P1 `rwb_source_data`; `sys_objects` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP05, DP07, DP11, DP13, DP15, DP19. Build (H): `RWB-P1-E1001-APP`, `RWB-P1-E1064-CON`, `RWB-P1-E1069-APP`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P1-E1064-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1064-APP`, `RWB-P4-E1064-APP`. External (X): `RWB-P1-E1064-OPS`.

**What moves.** The dictionary stays with P1 `rwb_source_data`, which owns `sys_objects`, `sys_fields`, `sys_field_version`, `data_contract` and `data_product`. It is the one place where a P1 view column and its ACE source field are defined, and P4 consumes it for access decisions.

## RWB-E1-065 Sandbox database with synthetic recovery data

Module: P1 Recovery data engine

**View.** All 30 views: the sandbox seeds the ACE schema, applies V0001 to V0003 so the 30 views exist, and fills the 88 Workbench tables and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` from their dictionary rows.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** v4 built a sandbox from the copy schema. v5 builds it from the ACE schema, the RWB-ACE-001 Tier 2 DDL and the 30 views, so DEV and SIT test the same read path as PROD. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`; P3 `rwb-case`; S8 `rwb-deviation`; P5 `rwb-document`.

- P1 `rwb-source-data`: `RWB-P1-E1065-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1065-APP` (App development, `L-P1-A`, after RWB-P1-E1001-APP, RWB-P1-E1069-APP); `RWB-P1-E1065-DB` (ACE DB, `L-P1-O`, Day 1).
- integration: `RWB-ITG-E1065-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1065-APP` (App development, `L-P4-AB`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1065-APP` (App development, `L-P3-T`, Day 1).
- S8 `rwb-deviation`: `RWB-S8-E1065-APP` (App development, `L-S8-E`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1065-APP` (App development, `L-P5-T`, Day 1).

Ready to start: Day 1 for 7 of the 8 stories; `RWB-P1-E1065-APP` after RWB-P1-E1001-APP, RWB-P1-E1069-APP.

**Tables and owner.** `account_ext` P1 `rwb_source_data`; `contact_point_ext` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `party_ext` P1 `rwb_source_data`; `valuation_ext` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19. Build (H): `RWB-P1-E1001-APP`, `RWB-P1-E1065-CON`, `RWB-P1-E1069-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P1-E1065-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1065-APP`, `RWB-P3-E1065-APP`, `RWB-P4-E1065-APP`, `RWB-P5-E1065-APP`, `RWB-S8-E1065-APP`. External (X): `RWB-P1-E1065-DB`.

**What moves.** The sandbox stays with P1 `rwb_source_data`, but it now applies 19 Flyway sequences into 19 schemas and fills the tables each service owns (GAP-3168). The P4, P3, S8 and P5 slices seed their own schemas, and the 30 views remain P1 artefacts.

## RWB-E1-066 Interaction ledger store and writer

Module: P1 Recovery data engine

**View.** No view. The story owns `interaction` and reads `recovery_case` through `CaseQueryApi`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP05 Contact and promises, DAILY, expected 08:00; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** No change of substance. An ACE-sourced contact is a ledger entry with its source reference, not a copy of the contact. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`.

- P1 `rwb-source-data`: `RWB-P1-E1066-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1066-APP` (App development, `L-P1-P`, Day 1); `RWB-P1-E1066-OPS` (DevOps, `L-P1-Q`, Day 1).
- integration: `RWB-ITG-E1066-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1066-APP` (App development, `L-P3-U`, Day 1).

Ready to start: Day 1 for 5 of the 5 stories.

**Tables and owner.** `data_product_load` P1 `rwb_source_data`; `interaction` P1 `rwb_source_data`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP18, DP19. Build (H): `RWB-P1-E1066-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P1-E1066-CON`, `RWB-P3-E1018-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P1-E1066-APP`, `RWB-P3-E1018-APP`, `RWB-P3-E1066-APP`. External (X): `RWB-P1-E1066-OPS`.

**What moves.** The interaction ledger is P1 `rwb_source_data` (R-PREC default ruling, DP-18), which owns `interaction`. The case key comes from P3's contract, and the case timeline in P3 reads the ledger by contract.

## RWB-E1-067 Every Workbench action into the interaction ledger

Module: P1 Recovery data engine

**View.** No view. The story intercepts Workbench actions and writes `interaction` and `processed_event`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP05 Contact and promises, DAILY, expected 08:00; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** No change of substance. The interception covers Workbench actions; an ACE change reaches the ledger as an event reference. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P3 `rwb-case`; P5 `rwb-document`.

- P1 `rwb-source-data`: `RWB-P1-E1067-CON` (Contract, `CG-W1`, Day 1); `RWB-P1-E1067-APP` (App development, `L-P1-P`, after RWB-P1-E1066-APP).
- integration: `RWB-ITG-E1067-ITG` (Integration, `L-ITG-W1`, Day 1).
- P3 `rwb-case`: `RWB-P3-E1067-APP` (App development, `L-P3-V`, Day 1).
- P5 `rwb-document`: `RWB-P5-E1067-APP` (App development, `L-P5-U`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P1-E1067-APP` after RWB-P1-E1066-APP.

**Tables and owner.** `data_product_load` P1 `rwb_source_data`; `interaction` P1 `rwb_source_data`; `processed_event` platform library (no service schema) (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19. Build (H): `RWB-P1-E1066-APP`, `RWB-P1-E1067-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P1-E1067-CON`, `RWB-P3-E1043-CON`. Integration (I): `RWB-P1-E1067-APP`, `RWB-P3-E1067-APP`, `RWB-P5-E1067-APP`. External (X): none.

**What moves.** Every Workbench action into the ledger is P1 `rwb_source_data`; the interception library is the platform inbox and outbox (DP-09), and an ACE change reaches the ledger as an event reference. The P3 and P5 slices publish their actions.

## RWB-E1-068 Interaction ledger read interface

Module: P1 Recovery data engine

**View.** No view. The read interface reads `interaction` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; this story grants nothing and writes no ACE object.

**Freshness.** DP05 Contact and promises, DAILY, expected 08:00; DP12 Decision log, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** No change of substance. The ledger read is a Workbench read; masking of `summary` follows RWB-E1-037. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P1 `rwb-source-data` (primary).

- P1 `rwb-source-data`: `RWB-P1-E1068-APP` (App development, `L-P1-P`, after RWB-P1-E1066-APP).

Ready to start: Day 1 for 0 of the 1 stories; `RWB-P1-E1068-APP` after RWB-P1-E1066-APP.

**Tables and owner.** `data_product_load` P1 `rwb_source_data`; `interaction` P1 `rwb_source_data`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP06, DP07, DP08, DP11, DP15, DP18, DP19. Build (H): `RWB-P1-E1066-APP`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): none. External (X): none.

**What moves.** The ledger read interface is P1 `rwb_source_data`, served under `/api/recovery/source-data/v1`; P3's case timeline reads the ledger through it (DP-18), and masking of `summary` follows P4's policy.

## RWB-E1-069 Read-only ACE source views, grants and boundary rule

Module: P1 Recovery data engine

**View.** All 30 views: 16 Section A views over the 21 ACE tables that exist today and 14 Section B views over the 14 tables and 12 columns RWB-ACE-001 adds; writes the four extension tables.

**Grant.** V0002 grants `USAGE` on `public` and `SELECT` on the 21 Tier 1 tables to `ace_view_owner`, sets that role as owner of each view, grants `USAGE` on `recovery` and `SELECT` on each view to `recovery_svc`, and revokes all from `PUBLIC`. V0003 repeats the SELECT grant for the 14 Section B views. No `GRANT SELECT ON ALL TABLES` and no write on a view.

**Freshness.** All 14 products: DP01, DP02, DP05, DP07, DP11 and DP13 DAILY by 08:00, DP06 WEEKLY by Monday 08:00, and the Workbench products DP03, DP04, DP08, DP09, DP10, DP12 and DP14 ON_CHANGE as they change. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** This is the story that replaces the load estate: V0002 ships the 16 Section A views, the four extension tables and the grant block; V0003 ships the 14 Section B views and waits for RWB-ACE-001. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 enforces the view-only read, and the Section B read stays behind its flag until RWB-ACE-001 is deployed and V0003 applies (DL43).

**Service and lane.** P1 `rwb-source-data` (primary); integration `RWB-ITG-W1`; P4 `rwb-access`.

- P1 `rwb-source-data`: `RWB-P1-E1069-APP` (App development, `L-P1-A`, after RWB-P1-E1001-APP, RWB-P1-ACE001-DB); `RWB-P1-E1069-DB` (ACE DB, `L-P1-R`, Day 1).
- integration: `RWB-ITG-E1069-ITG` (Integration, `L-ITG-W1`, Day 1).
- P4 `rwb-access`: `RWB-P4-E1069-APP` (App development, `L-P4-AC`, Day 1).

Ready to start: Day 1 for 3 of the 4 stories; `RWB-P1-E1069-APP` after RWB-P1-E1001-APP, RWB-P1-ACE001-DB.

**Tables and owner.** `data_product_load` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP02, DP03, DP05, DP06, DP07, DP08, DP11, DP15, DP19. Build (H): `RWB-P1-ACE001-DB`, `RWB-P1-E1001-APP`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): `RWB-P1-E1069-APP`, `RWB-P4-E1069-APP`. External (X): `RWB-P1-E1069-DB`.

**What moves.** The views, the grants and the view conformance test stay with P1 `rwb_source_data`, but the single `recovery_svc` login is replaced by one login per service (DP-02; GAP-3156), and the grants are split so that each service holds DML only in its own schema. V0002 ships the Section A views and V0003 the Section B views, and only P1 names them.

## RWB-TE-001 Recovery module folder and boundary test

Module: P2 Integration

**View.** No view. The story owns the module map `recovery-modules.yaml` and the boundary test that reads it.

**Grant.** No database grant. The module map is the contract; the build fails when a class names an object outside it.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** Rule BND-6 lives in this story: no recovery class names a `public` table, and the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`. No constraint in `recovery` references `public`; a link to an ACE record is a varchar(255) business key with no foreign key.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-TE001-APP` (App development, `L-PLT-TPL-J`, Day 1); `RWB-PLT-TE001-APP-2` (App development, `L-PLT-TPL-I`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** No table in the service schemas; the objects are platform, template or deployment artefacts.

**Dependencies.** Patterns: DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP16, DP19, DP20. Build (H): `RWB-PLT-E1027-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P10-TE013-CON`, `RWB-P2-E1007-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): none. External (X): none.

**What moves.** The folder layout and the boundary test become the platform template rule RWB-PLT-TE001 (DP-13, DP-19), and the microservice change ships as the delta copy `RWB-PLT-TE001-APP-2`. Rule BND-6 is applied per service against the 30 view names in `recovery-modules.yaml`, which is a P1 artefact.

## RWB-TE-002 Code owners for the recovery module

Module: P2 Integration

**View.** No view. The story owns `CODEOWNERS` and the review rules.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** No change of substance. The owners cover the view migrations as well as the module folders. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-TE002-APP` (App development, `L-PLT-TPL-L`, Day 1); `RWB-PLT-TE002-OPS` (DevOps, `L-PLT-TPL-K`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** No table in the service schemas; the objects are platform, template or deployment artefacts.

**Dependencies.** Patterns: DP07, DP15, DP19. Build (H): `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`. Integration (I): none. External (X): `RWB-PLT-TE001-APP`, `RWB-PLT-TE002-OPS`.

**What moves.** Code owners become the platform template rule RWB-PLT-TE002 and cover the 19 service folders as well as the view migrations. The OPS slice publishes the ownership map that the Ownership Map v1 records by team type only.

## RWB-TE-003 Types and contract tests from the API specification

Module: P2 Integration

**View.** No view. The story owns the generated types and the contract tests.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** No change of substance. An ACE-sourced field keeps its dictionary type; the view type and the API type are compared. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-TE003-APP` (App development, `L-PLT-TPL-N`, Day 1); `RWB-PLT-TE003-APP-2` (App development, `L-PLT-TPL-M`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** No table in the service schemas; the objects are platform, template or deployment artefacts.

**Dependencies.** Patterns: DP01, DP07, DP08, DP13, DP19. Build (H): `RWB-PLT-E1037-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): none. External (X): `RWB-PLT-TE001-APP`.

**What moves.** The generated types and contract tests become the platform template rule RWB-PLT-TE003, with the microservice change in `RWB-PLT-TE003-APP-2`. Every service's contract test is generated from its own OpenAPI and AsyncAPI documents under `/api/recovery/<short>/v1`.

## RWB-TE-004 Masked data in SIT and UAT

Module: P1 Recovery data engine

**View.** No view. The masked copy loads the Workbench tables `recovery_case`, `case_account`, `case_party`, `interaction`, `document_field`, `party_ext` and `contact_point_ext` in SIT and UAT.

**Grant.** No change beyond the DML V0001 already gives `recovery_svc` on the Workbench tables, including `party_ext` and `contact_point_ext`; SELECT on the views comes from V0002 (RWB-E1-069). The story grants no privilege in `public` and no write on a view.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP05 Contact and promises, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** The earlier story loaded a masked copy of the ACE source tables. v5 loads a masked copy of the Workbench tables only; ACE supplies its own SIT and UAT data through ACE, so no ACE source is copied. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** integration `RWB-ITG-W1`; platform (wave 0, `CG-W0` and `L-PLT-*`).

- integration: `RWB-ITG-TE004-ITG` (Integration, `L-ITG-W1`, Day 1).
- platform: `RWB-PLT-TE004-APP` (App development, `L-PLT-TPL-O`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** `case_account` P3 `rwb_case`; `case_party` P3 `rwb_case`; `contact_point_ext` P1 `rwb_source_data`; `data_product_load` P1 `rwb_source_data`; `document_field` P5 `rwb_document`; `interaction` P1 `rwb_source_data`; `party_ext` P1 `rwb_source_data`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP05, DP07, DP08, DP13, DP19. Build (H): `RWB-PLT-E1037-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P1-E1065-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): `RWB-P1-E1065-APP`, `RWB-P1-E1069-APP`, `RWB-PLT-TE004-APP`. External (X): none.

**What moves.** The masked copy becomes platform work (RWB-PLT-TE004), but the tables it fills belong to P3, P5 and P1, so the copy can only run in the owning service's own schema and no such service story exists yet (GAP-3170). ACE supplies its own SIT and UAT data.

## RWB-TE-006 Outbox and retry for outbound work

Module: P2 Integration

**View.** No view. The story owns `outbox_event`, `outbox_delivery` and `task` and reads `decision_log_entry` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** The outbox is unchanged. v5 retries Workbench outbound work only; a failed ACE ingest is the ACE team's retry and shows as a stale product. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** integration `RWB-ITG-W1`; platform (wave 0, `CG-W0` and `L-PLT-*`).

- integration: `RWB-ITG-TE006-ITG` (Integration, `L-ITG-W1`, Day 1).
- platform: `RWB-PLT-TE006-CON` (Contract, `CG-W0`, Day 1); `RWB-PLT-TE006-APP` (App development, `L-PLT-LIB-J`, Day 1).

Ready to start: Day 1 for 3 of the 3 stories.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision`; `outbox_delivery` platform library (no service schema); `outbox_event` platform library (no service schema); `recovery_case` P3 `rwb_case`; `task` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19. Build (H): `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P2-E1007-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P2-E1007-APP`, `RWB-PLT-TE006-APP`. External (X): none.

**What moves.** The outbox and retry library is the platform rule RWB-PLT-TE006 (DP-09), embedded in every service with its own `outbox_event`, `outbox_delivery` and `processed_event` tables. A failed ACE ingest is ACE's retry and shows as a stale product.

## RWB-TE-007 Scheduled jobs on Quartz

Module: P3 Case and workflow

**View.** No view. The story owns the Quartz schedule and `job_catalog`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** No ACE freshness. The only clock is the Workbench `created_at` and `updated_at`; nothing in this story waits on an ACE batch.

**Boundary.** The Quartz schedule is unchanged. v5 schedules Workbench jobs only; the ACE batch schedule belongs to ACE. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** Retired (D-RCV-60): no new story, no lane and no Day-1 work. The source note above is kept word for word for traceability.

**What moves.** The Quartz scheduler is replaced by Temporal Schedules in the owning service (RWB-PLT-E1071, DP-10; Arch v5 slide 44), and every dependency on TE-007 points to RWB-PLT-E1071-CON (GAP-3166).

## RWB-TE-008 Decision log hash chain check

Module: P7 Decision center and log

**View.** No view. The check reads `decision_log_entry`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The hash chain covers the ledger, including entries that name ACE business keys. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** integration `RWB-ITG-W1`; platform (wave 0, `CG-W0` and `L-PLT-*`).

- integration: `RWB-ITG-TE008-ITG` (Integration, `L-ITG-W1`, Day 1).
- platform: `RWB-PLT-TE008-APP` (App development, `L-PLT-TPL-P`, Day 1).

Ready to start: Day 1 for 2 of the 2 stories.

**Tables and owner.** `decision_log_entry` P7 `rwb_decision` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP06, DP07, DP10, DP13, DP17, DP19. Build (H): `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1008-CON`. Integration (I): `RWB-P7-E1008-APP`, `RWB-PLT-TE008-APP`. External (X): none.

**What moves.** The decision log hash-chain check becomes the platform rule RWB-PLT-TE008 and runs over P7's ledger. The chain covers entries that name ACE business keys, and P7 exposes the check as a Schedule.

## RWB-TE-011 PDPA lint for code, tests and logs

Module: P2 Integration

**View.** The dictionary entries of `v_ace_customer` and `v_ace_contact` and the Workbench fields `interaction.summary` and `document_field.field_value`.

**Grant.** No change. `recovery_svc` holds SELECT on the views named above from V0002 (RWB-E1-069) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP02 Customer and party, DAILY, expected 08:00; DP05 Contact and promises, DAILY, expected 08:00; DP10 Documents and extracted fields, ON_CHANGE as it changes. RWB-E1-015 stamps `data_product_load` from `v_ace_batch_status`; a product with no COMPLETE batch keeps its last good business date, is marked stale and raises MSG-P1-001.

**Boundary.** The earlier lint read the copy table columns. v5 reads the field list from the dictionary, so the view columns and the Workbench fields are covered by one rule set. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-TE011-APP` (App development, `L-PLT-TPL-Q`, Day 1).

Ready to start: Day 1 for 1 of the 1 stories.

**Tables and owner.** `data_product_load` P1 `rwb_source_data` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP05, DP07, DP08, DP19. Build (H): `RWB-PLT-E1037-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON`. Integration (I): none. External (X): `RWB-PLT-TE001-APP`.

**What moves.** The PDPA lint becomes the platform rule RWB-PLT-TE011 and reads the field list from P1's dictionary, so the view columns and the Workbench fields are covered by one rule set. The lint runs per service in its own pipeline.

## RWB-TE-012 Document storage containers

Module: P5 Document hub

**View.** No view. The story owns the document storage containers.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP10 Documents and extracted fields, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. An ACE source document stays in ACE; the container holds Workbench documents only. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** platform (wave 0, `CG-W0` and `L-PLT-*`).

- platform: `RWB-PLT-TE012-APP` (App development, `L-PLT-TPL-R`, Day 1).

Ready to start: Day 1 for 1 of the 1 stories.

**Tables and owner.** No table in the service schemas; the objects are platform, template or deployment artefacts.

**Dependencies.** Patterns: DP01, DP06, DP07, DP10, DP11, DP13, DP19. Build (H): `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`. Contract (C): `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`. Integration (I): none. External (X): `RWB-PLT-TE001-APP`.

**What moves.** The document storage containers become the platform rule RWB-PLT-TE012 and hold P5 documents only; an ACE source document stays in ACE. The container carries the WORM policy of Arch v5 slide 16.

## RWB-TE-013 Agent runtime client with fallback

Module: P10 Agent runtime

**View.** No view. The client reads `agent_policy` and `agent_run` and writes `decision_log_entry` and `recovery_case`.

**Grant.** No view in this story. `recovery_svc` holds DML on the Workbench tables it uses (V0001) and no privilege in `public`; the check grants nothing and writes no ACE object.

**Freshness.** DP03 Case and ownership, ON_CHANGE as it changes; DP12 Decision log, ON_CHANGE as it changes. A Workbench product is stamped from its last committed write, not from an ACE batch, so no ACE clock makes it stale.

**Boundary.** No change of substance. The fallback keeps a person in the path when the agent runtime is unavailable. No recovery constraint references `public`; a link to an ACE record is a varchar(255) business key with no foreign key. Boundary rule BND-6 in RWB-TE-001 fails the build when a recovery class names a `public` table; the only source objects it may name are the 30 `recovery.v_ace_*` views listed in `recovery-modules.yaml`.

**Service and lane.** P10 `rwb-agent` (primary); integration `RWB-ITG-W1`; P7 `rwb-decision`.

- P10 `rwb-agent`: `RWB-P10-TE013-CON` (Contract, `CG-W1`, Day 1); `RWB-P10-TE013-APP` (App development, `L-P10-A`, after RWB-P10-E1058-APP); `RWB-P10-TE013-OPS` (DevOps, `L-P10-M`, Day 1).
- integration: `RWB-ITG-TE013-ITG` (Integration, `L-ITG-W1`, Day 1).
- P7 `rwb-decision`: `RWB-P7-TE013-APP` (App development, `L-P7-AR`, Day 1).

Ready to start: Day 1 for 4 of the 5 stories; `RWB-P10-TE013-APP` after RWB-P10-E1058-APP.

**Tables and owner.** `agent_policy` P10 `rwb_agent`; `agent_run` P10 `rwb_agent`; `decision_log_entry` P7 `rwb_decision`; `recovery_case` P3 `rwb_case` (Ownership Map v1).

**Dependencies.** Patterns: DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20. Build (H): `RWB-P10-E1058-APP`, `RWB-P10-TE013-CON`, `RWB-PLT-E1027-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-E1072-CON`, `RWB-PLT-N001-CON`, `RWB-PLT-TE006-CON`. Contract (C): `RWB-P10-TE013-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`. Integration (I): `RWB-P10-TE013-APP`, `RWB-P7-TE013-APP`. External (X): `RWB-P10-TE013-OPS`.

**What moves.** The agent runtime client and its fallback become the P10 contract RWB-P10-TE013 (DP-20), which P7's decision centre also calls. The fallback keeps a person in the path when the agent runtime is unavailable.
