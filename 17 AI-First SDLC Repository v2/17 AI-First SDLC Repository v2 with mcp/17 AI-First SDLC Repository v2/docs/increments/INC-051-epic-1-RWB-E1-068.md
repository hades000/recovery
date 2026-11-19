# Increment Card — INC-051-epic-1-RWB-E1-068

**RWB-E1-068 — Interaction ledger read interface**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-051` |
| Title | Interaction ledger read interface |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-068` |
| RUN_ID | `INC-051-epic-1-RWB-E1-068` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 51 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-066 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **case owner (RW-CASEOWN)**, I want **to read a case's ledger in one ordered sequence, filtered by channel, actor or date range**, so that **I can see what has happened to it before I decide anything**.

**Business outcome:** A case owner who decides a route, a settlement or a legal step must first know what was said, promised, sent and done on the case. One read interface returns the ledger in order with the source of each entry, filters it by channel, actor and date range, and masks personal content by role on the same rules as the case record. The case record view and every other consumer read through this interface, so there is one ordering and one masking rule for the history. Serves REQ-ILG-006, REQ-ILG-003 and REQ-ILG-014; NFR-070 (one case history read in under 2 seconds at its 2031 size; DL11).

**Main flow:**
1. Case owner: opens SCR-03 Case record; the history panel calls GET /cases/{caseId}/interactions?page=0&size=50.
2. P3 interactions handler (API-P3-014): checks Case record R and calls InteractionLedgerReader.read() with the caller's context.
3. InteractionLedgerReader: checks the case is in the caller's scope through CaseScopeQuery.
4. InteractionLedgerReader: validates the filter (channel in LOV-CHANNEL, from not after to, size 1 to 200).
5. InteractionLedgerReader: reads the case's entries matching the filter, ordered by occurred_at, then case_seq.
6. InteractionLedgerReader: masks the summary field (is_personal) through the P4 masking interface for the caller's roles.

**Acceptance criteria:**
- AC1: The ledger reads in order
- AC2: It can be filtered
- AC3: It is available to the case record
- AC4: A date range in the wrong order
- AC5: A case outside the caller's scope
- AC6: Summary masked when no masking rule allows it
- AC7: Page size at and above the limit
- AC8: A case with no entries

**Out of scope:**
- The full case timeline screen SCR-04 and the ledger as a timeline on the case (FEAT-ILG-09, RWB-E2-034).
- Recording entries (RWB-E1-066, RWB-E1-067).
- Masking rule values (DL26, Compliance) and the masking mechanism (RWB-E1-037).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-068-interaction-ledger-read-interface-v1.md` |
| Requirement IDs | REQ-ILG-006, REQ-ILG-003, REQ-ILG-014 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-ILG-003, REQ-ILG-006, REQ-ILG-014) |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the ledger of own cases (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads the ledger of team cases (Case record R, scope Team) |
| RW-CONDUCT, RW-AUDIT and other roles with Case record R | Read the ledger of cases in their scope |
| RW-REFADM, reference data administrator | May not read (no Case record right) |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules that decide who sees the summary (DL26) |

## Contract extract

**Endpoint (P3, API-P3-014, extended; see additions)** | Item | Value | |---|---| | Method and path | GET /cases/{caseId}/interactions | | Request | Path: caseId; query: channel, from, to, page, size as in api.yaml, plus actor (new) | | Response | InteractionPage: items of Interaction, page, size, total. Interaction gains eventCode, caseSeq, actorType, actorRef, sourceRef and decisionLogEntryId (new); summary is masked by role | | Errors | 401 no session (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 case missing or out of scope (MSG-P4-003); 422 filter invalid (MSG-GEN-001, MSG-GEN-002, MSG-GEN-003); 503 store down (MSG-GEN-006) | | Authorization | Case record, R, scope applied | | Idempotency | Not applicable | **Published interface (P1)** ```java package recovery.dataengine.ledger.api; public interface InteractionLedgerReader { LedgerPage read(UUID caseId, LedgerFilter filter,…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: page sizes are properties; channels and masking come from lists and rules. - No personal data in logs, tests or prompts: summaries are never logged; test summaries are synthetic text. - No read of another module's tables: scope comes from CaseScopeQuery and masking from MaskingPolicy; P3 reads the ledger only through InteractionLedgerReader. - The read changes nothing in the ledger.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-068-interaction-ledger-read-interface-v1.md` |
| Specification | `output/INC-051-epic-1-RWB-E1-068/specify/spec.md` |
| Compliance validation | `output/INC-051-epic-1-RWB-E1-068/specify/compliance-validation.md` |
| Agent run log | `output/INC-051-epic-1-RWB-E1-068/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-051-epic-1-RWB-E1-068/plan/` |
| Implementation evidence | `output/INC-051-epic-1-RWB-E1-068/implement/` |
| API / functional test reports | `output/INC-051-epic-1-RWB-E1-068/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-051-epic-1-RWB-E1-068/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-068-interaction-ledger-read-interface-v1.md` |
| Output run | `output/INC-051-epic-1-RWB-E1-068/` |

