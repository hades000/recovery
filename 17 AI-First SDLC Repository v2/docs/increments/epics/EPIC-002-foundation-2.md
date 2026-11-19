# Epic Increment Card — EPIC-002 Foundation 2

## Identification

| Field | Value |
|---|---|
| Epic ID | `EPIC-002` |
| Title | Foundation 2: treatments, plans, integration completion and live agent operation |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E2` / `RWB-E2-*`, `RWB-TE-*` |
| Story increments | 43 Epic 2 items in `../epic-2-stories.md`; opened one month before the release |
| Release | 31 December 2026 |
| Status | Mobilised |
| Baseline | Document set v14, 16 November 2026; User Stories Epic 2 v5 |

## Scope

- P3 Case and workflow: ACE plan status, treatment entity and plan timers, transfer, full case record,
  approval routing, timers and deviation flag, next action, queue write interface.
- P6 Communications: contract/CA/mortgage document generation, e-signature, letter dispatch with WIN
  proof of delivery, SMS and LINE dispatch.
- P5 Document hub: stage 2/3 document extraction, field-app photos and bills.
- P8 Payments and posting: payment matching in Drools package `PAYMENT_MATCH`, booking match via
  `BOOKING_MATCH`.
- P10 Agent runtime: case intake agent live at L1, deviation screening agent evaluation, legal
  document agent in shadow, monitoring dashboard v2, TDR offer model through the model gateway.
- **Temporal and Drools (new):** `RWB-E2-037`–`RWB-E2-043` — observability, security codec server,
  resilience, workflow versioning and replay gate, rule change governance, Epic 2 rule packages and
  the integration pattern for Epic 3.
- Technical enablers: `RWB-TE-009` performance harness and `RWB-TE-010` browser/accessibility tests.

**Out of scope:** Epic 3–8 journeys; case workflow execution on Temporal before Epic 3 (D-RCV-36 T1).

## Dependencies

| Dependency | Owner | Needed by |
|---|---|---|
| `RWB-E1-073` rule authoring path | Recovery squad | `RWB-E2-041`, `RWB-E2-042` |
| `RWB-E1-070`/`071` Temporal platform and worker | Recovery squad | `RWB-E2-037`–`040`, `RWB-E2-043` |
| NLEADS, EasyApp, Entra ID data through ACE | ACE team | `RWB-E2-006`, `RWB-E2-018`, `RWB-E2-019` |
| Payment matching package approval | RW-COE / RW-RISK | `RWB-E2-008`, `RWB-E2-027` |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | Chitchaya Muanchonchana | Epic 2 v5, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | `output/CONTEXT-20261116/` |
| Requirements approval | Product Owner, FDA | Chitchaya Muanchonchana, Jesniphat Pukkham | Epic 2 v5 |
| Design and architecture approval | Forward Deployed Architect | Jesniphat Pukkham | ADR-001–012 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per story |

## Risk, rollback and stop signals

| Risk | Control |
|---|---|
| Temporal workflow replay incompatibility | Workflow versioning and replay test gate (`RWB-E2-040`). |
| Rule package regression | Minimum 50 scenarios per package; rollback one call. |
| Agent quality below L1 threshold | Agent stays in shadow; promotion grammar in D-RCV-33. |
| Payment matching tolerance error | Package columns and scenario tests owned by the data team. |
| Epic 2 starts before Epic 1 exits | Pull rule: the next item whose dependencies are done. |

## Evidence links

| Evidence | Location |
|---|---|
| Epic 2 story list | `docs/increments/epic-2-stories.md` |
| Build sequence | `docs/increments/build-sequence.md` |
| Context package | `.github/contexts/` |
| Traceability | `requirement/Traceability_Matrix.md` |
