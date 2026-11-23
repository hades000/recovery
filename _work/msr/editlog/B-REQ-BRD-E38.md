# Edit log B-REQ-BRD-E38

Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60. Run date: 22 November 2026.
WP: `_work/msr/wp/B-REQ-BRD-E38.md` (new BRD, Epics 3 to 8, first version). Fanout: 0.

## Files written

- `03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.md`
- `03 Requirements and specifications/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx`
- `_work/msr/docs/B-REQ-BRD-E38/Recovery Workbench Business Requirements Epics 3 to 8 v1.md`
- `_work/msr/docs/B-REQ-BRD-E38/Recovery Workbench Business Requirements Epics 3 to 8 v1.docx.md`
- `_work/msr/gaps/B-REQ-BRD-E38.jsonl`
- `_work/msr/assumptions/B-REQ-BRD-E38.jsonl`
- `_work/msr/editlog/B-REQ-BRD-E38.md`

All seven paths are inside the WP's "Write only" block and nothing outside it was touched. The two output files are new: no `Business Requirements Epics 3 to 8` file existed before this run, so no source document was edited and no next version displaced anything. Four throwaway Python helpers (style inspection, front-matter strip, docx verification and table verification) sit in the scratch folder `_work/msr/docs/B-REQ-BRD-E38/` and are scratch only.

## What the document is

The new business requirements document for Epics 3 to 8, produced by the BRD Builder under D-RCV-60. It carries the 14 sections the BRD playbook fixes (document control, executive summary, business context and problem statement, objectives and outcomes, stakeholders, current state, scope, business requirements, business rules and policies, success measures, assumptions-constraints-dependencies-risks, open questions, governance and approval, traceability), with the two Template and Rules §R8.1 header lines at the top and a front-matter block stating title, description and `status: Draft`.

- **Requirements.** 84 business requirements (BR-001 to BR-084), grouped by epic: E3 15, E4 18, E5 11, E6 17, E7 10, E8 13. Each row states one testable need, a priority that follows the stories it covers (Must 74 of 84), a rationale, and a source line of program requirement IDs, feature IDs and story keys. Together the rows cover all 181 stories and all 181 features of the specification, and every row is traced again in section 14.1.
- **Rules.** 32 business rules and policies (RULE-001 to RULE-032), each naming the route-set rule family that implements it. The ten route sets of Business Rules v4 are cited in full: R-RES-01..37, R-SET-01..27, R-DIL-01..37, R-GUA-01..32, R-LIT-01..79, R-DIS-01..72, R-DS-01..41, R-WO-01..51, R-DEV-01..22 and R-UNI-01..50.
- **Measures.** 14 (KPI-001 to KPI-014): the eight program measures with their baseline and target exactly as the program requirements state them, and six measures whose target or baseline the sources do not give, each marked with its placeholder.
- **Assumptions, constraints, dependencies, risks.** 34 assumptions, 12 constraints, 10 dependencies and 10 risks.
- **Open questions.** 27 (Q-001 to Q-027), each with an owner role, what it blocks, its gap row and its assumption row.
- **Traceability.** Section 14 traces every BR, RULE and KPI to a source document and a section, maps each business epic to its service epics and wave under D-RCV-60, and closes with a coverage check table.

Business language throughout. The only technical statements are the confirmed business constraints of the target: 19 services inside ACE, contract-first, Kafka events, Temporal from Epic 3, embedded Drools, no data lake, one release per month end. No design beyond that, and no PRD content.

## How the realignment changed the source

- **Business gaps of the thin stories are filled.** The 181 stories carry a story line, acceptance criteria, data, endpoints and test cases, and no business rationale. This document supplies the rationale (section 8 rationale column), the policy frame (section 9), the outcome measure (section 10) and the ownership of every need. It adds no acceptance criterion to a story and changes no story wording.
- **Every missing value became a question and an assumption.** Where a limit, range, period, criterion, owner role or baseline is absent from the sources, a `Q-` item is raised, a gap row is written and an assumption row is written, and the document carries the placeholder `Not specified in the source documents (CG-B-REQ-BRD-E38-n; ASM-B-REQ-BRD-E38-n)`. No value is invented.
- **Owners come from the Ownership Map.** Every capability owner is the service code of the Microservice Ownership Map v1 (Services, Endpoints, Events, Jobs and Workflows sheets), and every decision owner is the business role of the source. No person is named anywhere.
- **Release dates are unchanged and marked (tentative)**: 31 January 2027, 28 February 2027, 31 March 2027, 30 April 2027, 31 May 2027 and 30 June 2027.
- **Five real conflicts are raised, not settled silently**: the deceased customer flow placed in E3 by REQ-DVH-008 and in E7 by FEAT-DVF-03 (CG-15); E3 features depending on E4 features that release a month later (CG-16); an E3 feature depending on an E8 feature (CG-17); the data lake still named by FEAT-RPT-07 against ADR-018 (CG-18); the partner instruction endpoints in E4 against the same features in E6 (CG-19). One delivery-model conflict is added for the S6 wave against the E6 epic wave (CG-21).
- **Status and approval.** No approval is recorded in the sources, so the document stays `Draft` and the approval table in section 13 is left empty for the Product Owner and the named roles. This is recorded as ASM-2590 rather than raised as a question, per the realignment overlay.

## Register counts

- Candidate gaps: 27 rows in `_work/msr/gaps/B-REQ-BRD-E38.jsonl` (GAP-1464 to -27). By type: Missing 19, Conflict 5, Outdated 1, Ambiguous 1, and the type is stated on every row. By severity: P1 9, P2 10, P3 8. Every row carries the 15 keys of Template and Rules §R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp).
- Candidate assumptions: 34 rows in `_work/msr/assumptions/B-REQ-BRD-E38.jsonl` (ASM-2569 to -34). Confidence: High 13, Medium 19, Low 5. Every row carries the ten keys of §R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp).
- **Count of CG rows: 27. Count of ASM rows: 34.** Twenty-one of the ASM rows answer a gap row one to one (ASM-1 to ASM-21 against CG-1 to CG-21), six answer a measure gap (ASM-29 to ASM-34 against CG-22 to CG-27), and seven are document-level readings with no gap (ASM-22 to ASM-28).
- Every CG row names the ASM id that answers it, every ASM row names its gap where it has one, every `CG-` and `ASM-` id cited in the document exists in a register row, and every register row is cited at least once in the document. Only step D1 numbers them as GAP-nnnn and ASM-nnnn.
- No ASM or CG id was allocated for an ID this run does not own: the D-RCV-60 decision ID and the ADR, DL and D-RCV numbers used in the text are the ones in `_work/msr/plan/ids.json`.

## Document formats

- **.md** written directly at the output path, with the front matter the playbook requires.
- **.docx** produced from the same text with `office_write.py md-docx`. Two things were needed and are recorded here:
  1. The source `.docx` named in the WP (`Recovery Workbench Epics 3 to 8 Specification v3.docx`) cannot be used as the style template: python-docx cannot resolve its `Heading 1` style (the file names the built-in style `Heading 1` where the library expects `heading 1`), so `md-docx --template` fails with `KeyError: no style with name 'Heading 1'`. The same failure occurs with the program BRD template, so the defect is in the document set, not in this WP. The docx was therefore generated on the library's default template, which supplies the same heading and table styles the source family uses. The result has 40 headings and 32 tables, the two header lines first in the body, and every table complete: 84 requirement rows, 32 rule rows, 14 measure rows, 34 assumption rows, 27 question rows, 84 traceability rows.
  2. `office_write.py` refuses to overwrite an existing file, so the docx was built into the scratch folder and moved into place, which also keeps the rule that no existing document is edited.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-BRD-E38 --quick` — C02, C03, C05, C12, C13 and C18 all PASS with zero findings. No step failed three times.

A wider manual pass on the same file set also ran C14, C15, C16, C17 and C20: all PASS. C19 reports 200 findings, and every one of them is a planned output of another, not yet written work package (for example `B-P1-04`, `B-P1-08`, `B-P3-02`); no finding names this WP, and both of its planned outputs exist with the D-RCV-60 change-log row present. C04, C09, C10 and C11 concern story files and other work packages and do not apply here.

## Assumptions carried

- The seven document-level readings (ASM-2590 to -28) carry this WP: Draft status without an approval, dates unchanged and tentative, roles only, a new BR id set mapped to the program ids, owners read as business role plus capability service, the service split changing delivery and not intent, and the Epics 1 and 2 baseline relied on as published.
- The twenty-one value gaps (ASM-1 to -21) are read the way the sources allow: limits, ranges, periods, criteria, owner roles and cap bases stay as versioned reference data with no value asserted here, and each is confirmed with the role named in section 12 before the requirement it blocks is accepted.
- The six measure gaps (ASM-29 to -34) keep the published targets and mark the missing baseline or tolerance with the placeholder, so a measure can be published from release and closed when the business supplies its base.
