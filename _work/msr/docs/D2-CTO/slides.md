## Cover
@cover
h1|SCB Collections and Recovery. Henka Group, 22 November 2026.
h2|(C) Siam Commercial Bank and Henka Pte Ltd
title|Recovery Workbench: 19 services inside ACE
sub|Version 4, microservice realignment (D-RCV-60)
meta|Executive presentation for the CTO
change|v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash

## Change log and what this version adds
| Version | Date | Change | Tool |
|---|---|---|---|
| v3 | 28 October 2026 | Executive presentation for the CTO: architecture and build, as issued | — |
| v4 | 22 November 2026 | Services, waves, Day-1 work and gaps added; decisions ADR-013 to ADR-023 and DL44 to DL49 applied; version 3 content kept on slides 13 to 19 | T3 Code / OpenCode / DeepSeek v4.1 Flash |
> v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash
- Version 4 is diagram-led on four questions: which services, in which wave, what can start on Day 1, and which gaps remain.
- Every source section, ID, count and date of version 3 is kept; release dates stay as issued and are tentative (R1 U7, DL48).
- Sources: Architecture v5 (slides 13 to 20 and 41 to 44), the Temporal and Drools design v1, Ownership Map v1, Template and Rules v1 and the split plan.

## What this version changes in the deck
> Statements on the version 3 slides are kept word for word. Where the realignment changes an answer, the decision that changes it is named here (R3 precedence: Architecture v5 first).
@widths 0.85,3.9,5.6,1.75
| Version 3 slide | Statement in version 3 | After D-RCV-60 | Decision |
|---|---|---|---|
| 2 | Build on ACE: one service, one repository, one front end | 19 services inside ACE, one repository and one epic per service; ACE sign-in, IAM, audit, PII and SOC logs reused | ADR-013, DL44 |
| 2 | Programmatic workflow: no Temporal | CaseWorkflow with a child workflow per stage on one shared, reusable Temporal layer; Schedules replace Quartz | ADR-016, DL44 |
| 3 | PostgreSQL with the recovery schema: 108 entities, 1,256 fields, 14 data products | One rwb_<name> schema and login per service in the ACE database; never read another service's tables | ADR-014, ADR-021 |
| 2 | Data through COLLINS: daily batch into the ACE database | Kept: ACE data arrives as before and is read through rwb-source-data's contract or the service's own v_ace_* views | ADR-014 |
| 5 | Out: reporting to the data lake | No data lake: rwb-reporting builds its read model from events | ADR-018 |
| 6 | Two TechX recovery squads, one repository | Kept as a suggestion only: ownership is soft by team type and any team may pick up a story | DL45, DL46 |
| 7 | DL03, DL05, DL06, DL07, DL11, DL12, DL21 and DL27 are open | IDs and dates kept; DL05 is restated for 19 services: one repository per service from the service template | ADR-013, DL44 |

## Realignment at a glance: the wave bands
- 19 services, one epic each (RWB-SVC-P1 to RWB-SVC-S9), plus 7 platform epics (RWB-PLT-TPL, -LIB, -WF, -DB, -EVT, -EDGE, -OBS) and 5 integration epics (RWB-ITG-W1 to W4 and -NFR).
- Legacy stories by wave: 73 in Wave 1, 72 in Wave 2, 76 in Wave 3, 110 in Wave 4, 8 in the platform and NF band, 19 new and integration keys.
- Diagram of record: Recovery Workbench Microservice Architecture by Epic and Story v1, and Wave 1 to Wave 4 Architecture v1 (folder 22).
@diagram waves

## The ten platform services: 9 in Wave 1, 1 in Wave 2
@widths 0.62,1.85,0.62,1.55,7.46
| Code | Service | Wave | Service epic | Owns (Architecture v5 slide 41) |
|---|---|---|---|---|
| P1 | rwb-source-data | 1 | RWB-SVC-P1 | ACE view contract, extension tables, freshness, reconciliation |
| P2 | rwb-integration | 1 | RWB-SVC-P2 | interface config, file runs, outbound items, ACE integration paths |
| P3 | rwb-case | 1 | RWB-SVC-P3 | case, CMMN state, queues, tasks, allocation, timers |
| P4 | rwb-access | 1 | RWB-SVC-P4 | roles as data, scope, masking policy, DoA table, access log |
| P5 | rwb-document | 1 | RWB-SVC-P5 | metadata, custody, OCR text and fields, signatures, retention |
| P6 | rwb-comms | 1 | RWB-SVC-P6 | notices, templates, merge fields, proof of delivery |
| P7 | rwb-decision | 1 | RWB-SVC-P7 | approvals, central decision ledger, DMN model registry |
| P8 | rwb-payment | 2 | RWB-SVC-P8 | payment and proceeds matching, fees, bookings, posting files |
| P9 | rwb-reporting | 1 | RWB-SVC-P9 | measures, snapshots, steering dashboard, regulatory reports |
| P10 | rwb-agent | 1 | RWB-SVC-P10 | agent policies, prompts, runs, guardrails, evaluations |
> Every service: schema rwb_<short> with its own login, REST base /api/recovery/<short>/v1 behind gateway-bff, topic rwb.<short>.events.v1 with retry and .dlt, task queue rwb-<short> in namespace rwb-recovery (R4).

## The nine stage services: Waves 2 to 4
@widths 0.62,1.85,0.62,1.55,7.46
| Code | Service | Wave | Service epic | Owns (Architecture v5 slide 41) |
|---|---|---|---|---|
| S1 | rwb-valuation | 3 | RWB-SVC-S1 | valuations, D6 route decision, route agent output |
| S2 | rwb-treatment | 2 | RWB-SVC-S2 | treatments, contracts, settlement and deed-in-lieu agreements, plan timers |
| S3 | rwb-guarantee | 3 | RWB-SVC-S3 | TCG and insurance claims, guarantor notices and pursuit |
| S4 | rwb-litigation | 3 | RWB-SVC-S4 | legal actions, hearings, judgments, enforcement, LED auction ladder |
| S5 | rwb-asset | 2 | RWB-SVC-S5 | assets taken on, holding, floor price, listings, auction rounds |
| S6 | rwb-debtsale | 3 | RWB-SVC-S6 | lots, data room, buyer terms, bids, award, transfer |
| S7 | rwb-writeoff | 4 | RWB-SVC-S7 | eligibility, committee, posting, recovery after charge-off |
| S8 | rwb-deviation | 2 | RWB-SVC-S8 | X1-X7 screening, pause, handling, return |
| S9 | rwb-partner | 4 | RWB-SVC-S9 | panel, partner users, instructions, results, fees, scorecards |
> Rules run inside the owning service (embedded Drools) with the rule package registry in rwb-decision; decision records are written locally and sealed centrally (DP-03, DP-04).

## Wave plan: 5 bands, 19 services, one programme
@widths 0.6,3.0,0.8,2.0,5.7
| Wave | Services in the wave | Count | Business epic (R5.6) | Platform or integration epic |
|---|---|---|---|---|
| 0 | none: the platform, the shared libraries and the edge | 0 | platform and non-functional | RWB-PLT-TPL, -LIB, -WF, -DB, -EVT, -EDGE, -OBS and RWB-ITG-NFR |
| 1 | P1, P2, P3, P4, P5, P6, P7, P9, P10 | 9 | EP01 | RWB-ITG-W1 |
| 2 | P8, S2, S5, S8 | 4 | EP02, EP03 | RWB-ITG-W2 |
| 3 | S1, S3, S4, S6 | 4 | EP04, EP05 | RWB-ITG-W3 |
| 4 | S7, S9 | 2 | EP06, EP07, EP08 | RWB-ITG-W4 |
> Release dates by wave: Not specified in the source documents (CG-D2-CTO-1; ASM-D2-CTO-3). Every release date is kept as issued and is tentative (R1 U7, DL48).
- A story whose business-epic wave is earlier than its service wave keeps the business-epic wave (R5.6).
- Wave 0 does not wait for Wave 1: the service template, the workflow kit, the event platform and the edge contract are Day 1 work for every team type (R5.7).

## Day-1 work: 939 of 1,034 story slices can start on Day 1
@widths 1.5,2.4,8.2
| Team type (suggested owner) | Work types (R5.3) | Day-1 position |
|---|---|---|
| TechX | CON, APP, ITG | At least one CON story per service, and every CON story is Day 1 (R5.7.1, R5.7.7); the new platform stories N001 to N012 are Day 1 |
| ACE team | DB | Day 1 by rule R5.7.6: every team type has Day-1 work; only H dependencies, and a platform CON story is Day 1 itself |
| SCB IT infrastructure | INF | Day 1 by rule R5.7.6 |
| DevOps team | OPS | Day 1 by rule R5.7.6; the new platform stories N001 to N012 carry it |
| QA team | ITG harness and NFR | The integration harness W1J01 is Day 1 (R5.7.6) |
@diagram day1
> C dependencies never block a build: a story builds against the published contract and its fake (R5.7.2). A lane is a connected group of non-CON stories linked by H, at most 4 deep (R5.7.5).

## Ownership: soft, by team type (Ownership Map v1)
@widths 2.5,0.9,8.7
| Ownership Map v1 sheet | Rows | What it fixes for the CTO |
|---|---|---|
| Services | 19 | code, service, wave, schema, REST base, topic and task queue for each service |
| Tables | 93 | the one service that owns each table; no table is read by another service |
| Endpoints | 156 | the owner of every REST operation |
| Events | 30 | the producer of every event; consumers read only through their own inbox |
| Workflows and activities | 15 | the service that owns each workflow or activity |
| Jobs | 22 | the owner and the replacement mechanism: a Temporal Schedule or an event-started workflow, no shared Quartz tables |
| Rulings | 71 | the default ruling where the sources are silent |
- Default rulings (R3): parameters and reference data, and the case list API, to P3 rwb-case; the rule package registry to P7 rwb-decision; the interaction ledger to P1 rwb-source-data; feature flags to the platform library.
- Owners are suggestions only: any team may pick up a story (R1 U3, DL46). No person is named anywhere.

## Gaps and assumptions that matter to the CTO
@widths 1.15,4.2,1.1,0.85,5.0
| Candidate gap | What is missing or in conflict | Type | Severity | Handling |
|---|---|---|---|---|
| CG-D2-CTO-1 | Release dates are not stated per wave in the sources; story releases are per story only | Missing | P2 | Left as a placeholder on the wave slide; dates stay tentative (R1 U7, DL48) |
| CG-D2-CTO-2 | The version 3 slides describe the monolith (one service, no Temporal, a data lake); Architecture v5 says 19 services, Temporal and no data lake | Conflict | P3 | Version 3 slides kept; the "what this version changes" slide maps each statement to its decision |
| CG-D2-CTO-3 | No accountable team per service: ownership is soft, by work type (R1 U3) | Missing | P3 | Service owners shown as the service code of the Ownership Map plus the suggested work-type owner |
| CG-D2-CTO-4 | 19 legacy keys in the split plan carry no wave value (new and integration keys) | Ambiguous | P3 | Wave taken from the service or the integration epic (R4, R5.1) |
> Candidate rows are numbered GAP-nnnn and ASM-nnnn at step D1 and land in the Gap Register and the Assumptions Register (folder 23, Template and Rules R9). Severity: P1 blocks a wave start, P2 blocks a story's Done, P3 is documentation only.

## Where to read more
- Architecture: Recovery Workbench Architecture v5 Text Extract v1 and the Temporal and Drools Design Text Extract v1 (folder 22).
- Ownership: Recovery Workbench Microservice Ownership Map v1, 19 services, 93 tables, 156 endpoints, 30 events, 15 workflows and activities, 22 jobs.
- Delivery: the service story set (358 legacy stories into 1,034 slices), the Service Story Catalog v1, the Day-1 Work Allocation v1 and the Service Epics v1.
- Decisions and registers: ADR-013 to ADR-023, Decision Log rows DL44 to DL49, the Change Register v1, and the Gap Register and Assumptions Register (folder 23).
- Diagrams: Recovery Workbench Microservice Architecture by Epic and Story v1, and Wave 1 to Wave 4 Architecture v1.

## Version 3 content, kept unchanged
- Slides 13 to 19 are the version 3 slides of 28 October 2026, kept word for word (R8.2 versioning; CG-D2-CTO-2).
- They describe the monolith that was current in October 2026: one service, one repository, programmatic workflow and a data lake.
- Where a statement there differs from the section above, this section and its decision win (R3 precedence, Architecture v5 first).
