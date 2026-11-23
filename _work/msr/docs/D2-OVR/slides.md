## SCB Collections and Recovery. Henka Group, 22 November 2026.

- (C) Siam Commercial Bank and Henka Pte Ltd
- Recovery Workbench Project Overview, version 5. Decision D-RCV-60 microservice realignment.
- Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Status: Draft.
- Supersedes version 4 of 28 October 2026, which stays unchanged next to this file.
- Change log: v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
- Bank approval of D-RCV-60 and of DL44 to DL49: Not specified in the source documents (CG-D2-OVR-4; ASM-D2-OVR-4).

## Realignment summary: 19 services inside ACE

- D-RCV-60 adopts Architecture v5. Recovery stays part of ACE: same AKS cluster and App Gateway, ACE Common shared services, ACE PostgreSQL database.
- recovery-core is split into 19 services, one per business module: P1 to P10 for the shared capability, S1 to S9 for the case and route services.
- Each service owns schema rwb_<name>, REST base /api/recovery/<name>/v1, topic rwb.<name>.events.v1, task queue rwb-<name> in namespace rwb-recovery, and epic RWB-SVC-<code>.
- One schema and login per service in the ACE database; Kafka with outbox and inbox; one reusable Temporal layer; embedded Drools with the rule registry in rwb-decision.
- Why: one service per module gives each capability its own release, owner and contract, so it can be reused or replaced alone.
- What does not change: the six-stage journey, the eight routes, the five decision steps, the CMMN 1.1 case model, rules as versioned data, one decision log entry per decision.

## The 19 services, their owners and waves

- Wave 1: P1 rwb-source-data (Source data), P2 rwb-integration (Integration), P3 rwb-case (Case and workflow), P4 rwb-access (Access and authority).
- Wave 1 continued: P5 rwb-document (Document), P6 rwb-comms (Communications), P7 rwb-decision (Decision and rules), P9 rwb-reporting (Reporting), P10 rwb-agent (Agent).
- Wave 2: P8 rwb-payment (Payment), S2 rwb-treatment (Treatment and offer), S5 rwb-asset (Asset), S8 rwb-deviation (Deviation).
- Wave 3: S1 rwb-valuation (Valuation and route), S3 rwb-guarantee (Guarantee), S4 rwb-litigation (Litigation), S6 rwb-debtsale (Debt sale).
- Wave 4: S7 rwb-writeoff (Write-off), S9 rwb-partner (Partner).
- Every owner above is the row of that service in the Ownership Map v1 Services sheet; the service epic is RWB-SVC-<code>.
- Service wave to the eight releases on slide 9: Not specified in the source documents (CG-D2-OVR-2; ASM-D2-OVR-2).

## How the realignment touches this overview

- Slides 3 and 8 keep their text. "One service, one repository and one front end" is read as 19 services with one repository and schema each, and one ACE front end behind gateway-bff (CG-D2-OVR-1).
- Slide 5 holds, service by service: case list P3 rwb-case, document hub P5 rwb-document, partner portal S9 rwb-partner, decision log P7 rwb-decision, parameters and reference data P3 rwb-case, DoA table P4 rwb-access.
- Slide 6: receive P1 and P3, choose the route S1 with the rules in P7, resolve S2 and S3, enforce S4, realize S5 and S6, close S7, deviate S8.
- Slide 7: decide and log in P7 rwb-decision, AI prepares in P10 rwb-agent, act in the owning service.
- Slide 10 measures and slide 11 decisions are unchanged; DL01 to DL33 stay open and D-RCV-60 adds DL44 to DL49.
- Which service serves each screen route behind gateway-bff: Not specified in the source documents (CG-D2-OVR-3; ASM-D2-OVR-3).

## Where the realignment is written down

- Architecture v5, slides 13 to 20 and 41 to 44: services, contracts, service catalogue and job map.
- Decision Log: D-RCV-60 and DL44 to DL49. Architecture Decision Records: ADR-013 to ADR-023.
- Delivery: one epic per service, RWB-SVC-P1 to RWB-SVC-S9, 7 platform epics (RWB-PLT-TPL, LIB, WF, DB, EVT, EDGE, OBS) and 5 integration epics (RWB-ITG-W1 to W4 and NFR).
- Every story also carries its business epic EP01 to EP08 as a tag; the owner is a suggestion only and any team may pick up the story.
- Run material: Template and Rules v1, Ownership Map v1, Change Register v1; gaps and assumptions in the registers in folder 23.
- All release dates on slide 9 are marked tentative and are unchanged (U7, DL48).
- Slide numbers follow version 5, where this document-control slide is slide 1.
