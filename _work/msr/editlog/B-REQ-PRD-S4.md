# Edit log B-REQ-PRD-S4 — PRD S4 rwb-litigation v1

Decision D-RCV-60. Agent aisdlc-prd-builder. fanout 0.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md`
- `_work/msr/gaps/B-REQ-PRD-S4.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-S4.jsonl`
- `_work/msr/editlog/B-REQ-PRD-S4.md`

Scratch (working scripts and query notes for this work package):

- `_work/msr/docs/B-REQ-PRD-S4/emit.py`
- `_work/msr/docs/B-REQ-PRD-S4/audit.py`
- `_work/msr/docs/B-REQ-PRD-S4/q1.py`
- `_work/msr/docs/B-REQ-PRD-S4/q2.py`
- `_work/msr/docs/B-REQ-PRD-S4/q3.py`
- `_work/msr/docs/B-REQ-PRD-S4/q4.py`
- `_work/msr/docs/B-REQ-PRD-S4/q5.py`

No source file was edited. No master file was written. No file outside the "Write only" list of this work package was touched. No issue tracker, wiki, repository or web service was called.

## What the document is

The first PRD of the S4 family: `Recovery Workbench PRD S4 rwb-litigation v1.md`, in `03 Requirements and specifications/PRD/`. It replaces nothing and sits next to the other service PRDs printed by this run.

Its first two lines are the header of Template and Rules §R8.1. The change log carries the row `1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash`. Status is Draft and the approval table of section 13 is deliberately empty; the missing approval is carried as an assumption.

## Counts

| Item | Count |
|---|---|
| Capabilities CAP-S4 | 25 (CAP-S4-001 to CAP-S4-025) |
| Functional requirements FR-S4 | 57 (FR-S4-001 to FR-S4-057) |
| Non-functional requirements NFR-S4 | 34 (NFR-S4-001 to NFR-S4-034) |
| Acceptance criteria AC-S4 | 40 (AC-S4-001 to AC-S4-040) |
| User journeys JRN-S4 | 7 (JRN-S4-01 to JRN-S4-07) |
| Personas ROL-S4 | 13 (ROL-S4-01 to ROL-S4-13) |
| Open questions OQ-S4 | 17 (OQ-S4-01 to OQ-S4-17) |
| Gap rows CG | 14 (GAP-1736 to GAP-1749) |
| Assumption rows ASM | 20 (ASM-2898 to ASM-2917) |

## BR coverage

BR-034 to BR-043, the ten requirements of the E5 requirement set that name rwb-litigation, are each covered by at least one functional requirement, and every functional requirement traces to one of them. Two programs requirements have no BRD row of their own: REQ-S4-009 is carried under BR-034 through FR-S4-051 and FR-S4-052 and recorded as gap 11; BR-038 and BR-042 carry no program requirement ID and are traced from FEAT-LIT-10 and FEAT-LIT-17 to FEAT-LIT-21 and the RWB-E5 story keys. No requirement of this module is left without a functional requirement.

## Gap rows raised (CG)

| ID | Type | Severity | Subject |
|---|---|---|---|
| GAP-1736 | Conflict | P1 | FSD reads the ACE views and v_ace_batch_status directly; Arch v5 gives that read to rwb-source-data and the slide 13 matrix gives the S4 row no cell to P1 |
| GAP-1737 | Conflict | P1 | The matrix gives S4 no cell to rwb-document, rwb-payment or rwb-agent while the FSD names the document hub, ALS and GL and the model gateway |
| GAP-1738 | Missing | P2 | The Ownership Map gives S4 two tables; Arch v5 gives the schema judgments, enforcement and the LED ladder, and the FSD holds notice, pack and deferral state |
| GAP-1739 | Conflict | P2 | legal_action.case_id is a uuid in the FSD; ADR-014 and DP-01 require a varchar(255) business key with no foreign key |
| GAP-1740 | Ambiguous | P1 | The notice, its state and its proof of delivery sit in S4 in the FSD and in rwb-comms in Arch v5 and the Ownership Map; three notice paths split across two services |
| GAP-1741 | Conflict | P1 | The notice is first needed in E2 (wave 2) while the service is created in wave 3 |
| GAP-1742 | Missing | P1 | 32 of the 79 R-LIT rules are named in the FSD; the litigation package is Phase 2 |
| GAP-1743 | Ambiguous | P2 | Every FSD acceptance criterion is the same generic sentence; no alternate flow and no background event for any of the 22 features |
| GAP-1744 | Missing | P2 | LawsuitFiled, JudgmentRecorded and AuctionResult have no EV number and no catalogue row |
| GAP-1745 | Conflict | P2 | R-LIT-01 starts litigation on route R4 while the case journeys call R4 the guarantee claim and R5 litigation |
| GAP-1746 | Missing | P2 | REQ-S4-009 has no BRD requirement row; BR-038 and BR-042 carry no program requirement ID |
| GAP-1747 | Missing | P3 | The three S4 screens have no owner cell in the v5 screen matrix |
| GAP-1748 | Missing | P2 | The message wording and the Thai and English versions are not in the FSD (DL10) |
| GAP-1749 | Missing | P3 | No litigation, hearing or enforcement volume is stated for the module |

## Assumption rows raised (ASM)

| ID | Confidence | Subject |
|---|---|---|
| ASM-2898 | High | Read path through the rwb-source-data contract only; boundary test fails the build on a view or ACE table read |
| ASM-2899 | Medium | The pack, the fee and the agent reach this service as contract dependencies on the P5, P8 and P10 contract stories |
| ASM-2900 | Medium | Eight entity groups in rwb_litigation, two named by the Ownership Map and six named as Arch v5 names them |
| ASM-2901 | High | A case link is a varchar(255) business key with no foreign key |
| ASM-2902 | Medium | S4 decides, approves and times the notice; P6 owns the template, the merge fields, the delivery and the proof |
| ASM-2903 | Medium | The notice slice keeps the EP02 wave 2 and lands as a contract with its fake before wave 3 |
| ASM-2904 | Medium | The 32 named rules are the requirement set; the other 47 are package authoring for rwb-decision |
| ASM-2905 | Medium | Each FSD criterion row is read as one per feature and the step-specific criteria are this PRD's |
| ASM-2906 | Medium | Three events carried by name and topic, keyed by the case, with no EV number asserted |
| ASM-2907 | Low | No route number asserted; the trigger is the rule IDs R-LIT-01 and R-LIT-02 |
| ASM-2908 | Medium | REQ-S4-009 carried under BR-034; BR-038 and BR-042 traced from their FSD features and story keys |
| ASM-2909 | Medium | The three screens are served from gateway-bff composite routes |
| ASM-2910 | Medium | Message IDs and English wording preserved; Thai wording, field text and approver left to DL10 |
| ASM-2911 | Medium | No module volume asserted; the population figures of the non-functional specification are used |
| ASM-2912 | High | Status Draft and no approval recorded in this run; the approval table is empty on purpose |
| ASM-2913 | Medium | The BRD is read as approved for this run; the missing governance decision is this assumption |
| ASM-2914 | High | The service wave 3 and the EP05 business epic wave 3 are the same, so no E5 wave conflict is raised |
| ASM-2915 | High | Every release date copied unchanged and marked (tentative): E2 31 December 2026, E5 31 March 2027 |
| ASM-2916 | High | Roles only: no person is named anywhere, including the approval table |
| ASM-2917 | High | The PRD's identifier families are new; every FSD identifier is preserved character for character |

## Decisions taken

1. Status Draft and an empty approval table, per the D-RCV-60 overlay: a missing approval is an assumption, never an answer.
2. Release slicing by wave: one contract slice before wave 3 for the notice that Epic 2 needs (release 31 December 2026 (tentative)), then ten wave-3 slices that follow the order in which the product can be demonstrated (release 31 March 2027 (tentative)). Both dates are copied unchanged and marked (tentative).
3. No design beyond the confirmed v5 constraints: no class name, no DDL, no endpoint beyond the five S4 paths and the two P6 paths the Ownership Map already records, and no physical table name beyond the two the map already holds.
4. Every owner is taken from the Ownership Map. Where the map has no owner for an edge or a table, the row says so and a gap row and an assumption row are raised instead of a name being invented.
5. New identifiers come from `_work/msr/plan/ids.json` where a decision, ADR or decision-log row is needed; this document needs none of them because it introduces no new decision, and it cites D-RCV-60, ADR-013 to ADR-023 and DL44 to DL49 as inherited.
6. The 14 CG rows and the 20 ASM rows are candidate rows only. Their final numbering as GAP-nnnn and ASM-nnnn and the rewriting of every citation is left to step D1.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S4 --quick` — C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, no findings.

No failure to record. No retry was needed.
