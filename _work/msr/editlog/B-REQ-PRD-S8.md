# Edit log B-REQ-PRD-S8 — PRD S8 rwb-deviation v1

Decision D-RCV-60. Agent aisdlc-prd-builder. fanout 0.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md`
- `_work/msr/gaps/B-REQ-PRD-S8.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-S8.jsonl`
- `_work/msr/editlog/B-REQ-PRD-S8.md`

Scratch (working scripts for this work package):

- `_work/msr/docs/B-REQ-PRD-S8/append_rows.py` — appended the two rows for the missing FSD v1 and v2 history
- `_work/msr/docs/B-REQ-PRD-S8/audit.py` — identifier audit: every citation resolves, every FR is covered by a criterion, no gap in a numbered family
- `_work/msr/docs/B-REQ-PRD-S8/tablecheck.py` — markdown table column-count check
- `_work/msr/docs/B-REQ-PRD-S8/checks_extra.py` — ran C14, C17, C19, C20 and C01 against this work package's files

No source file was edited. No master file was written. No file outside the "Write only" list of this work package was touched. No issue tracker, wiki, repository or web service was called. No git commit was made.

## What the document is

The first PRD of the S8 family: `Recovery Workbench PRD S8 rwb-deviation v1.md`, in `03 Requirements and specifications/PRD/`. It replaces nothing and sits next to the other service PRDs printed by this run.

Its first two lines are the header of Template and Rules §R8.1. The change log carries the row `1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash`. Status is Draft and the approval table of section 13 is deliberately empty; the missing approval is carried as an assumption (ASM-3012).

The document keeps every section the PRD contract asks for: document control and change log, product overview and the relationship to ACE, personas and roles, user journeys (current and target), capabilities, functional requirements, non-functional requirements, data requirements, integration points, release slicing by wave, acceptance criteria and validation evidence, open questions, an empty approval table and an appendix of sources.

## Counts

| Item | Count |
|---|---|
| Capabilities CAP-S8 | 19 (CAP-S8-001 to CAP-S8-019) |
| Functional requirements FR-S8 | 56 (FR-S8-001 to FR-S8-056) |
| Non-functional requirements NFR-S8 | 29 (NFR-S8-001 to NFR-S8-029) |
| Acceptance criteria AC-S8 | 23 (AC-S8-001 to AC-S8-023) |
| User journeys JRN-S8 | 7 (JRN-S8-01 to JRN-S8-07) |
| Personas ROL-S8 | 13 (ROL-S8-01 to ROL-S8-13) |
| Open questions OQ-S8 | 16 (OQ-S8-01 to OQ-S8-16) |
| Gap rows CG | 19 (GAP-1816 to GAP-1834) |
| Assumption rows ASM | 22 (ASM-2994 to ASM-3015) |

Every one of the 56 functional requirements is covered by at least one acceptance criterion, and every criterion cites a source acceptance criterion, a source rule or the gap and assumption it rests on. The identifier audit found no gap in any numbered family and no unresolved CG or ASM citation.

## BR coverage

The FSD serves 18 requirements: REQ-DVH-001 to REQ-DVH-011 (program, 11) and REQ-S8-001 to REQ-S8-007 (E7 set, 7). All 18 are covered by at least one functional requirement, and every functional requirement traces to one of them.

The BRD requirements that name this service are BR-062, BR-063, BR-064, BR-065, BR-066, BR-067, BR-068, BR-069 and BR-079: 9 of 9 are covered. BR-062 covers both REQ-S8-001 and REQ-S8-003, and BR-069 covers both REQ-DVH-007 and REQ-S8-006, which is why the row count in section 11.2 is higher than the requirement count.

Coverage gaps, recorded rather than papered over:

1. Epic 2 has no BR numbering of its own. The E2 screening requirements (REQ-DVH-001 to REQ-DVH-007, REQ-DVH-009, REQ-DVH-010) are carried with their program requirement ID in the BR column of sections 5 and 6, and the BRD row that would name them does not exist.
2. REQ-DVH-008 (death) is one requirement with two epics: E3 in the program and the FSD, E7 in BR-064. It is covered by FR-S8-034 and FR-S8-035 and split across two release slices, with the question carried as OQ-S8-05 and gap 10.
3. REQ-DVH-011 (the full flows end to end) has no BR row of its own; it is carried under BR-062 to BR-068 through the X1 to X7 capabilities.
4. RULE-012, RULE-013 and RULE-014 are carried as BR IDs next to the program requirements they restate, because the E2 slice has no BR row to point at.

## Gap rows raised (CG)

| ID | Type | Severity | Subject |
|---|---|---|---|
| GAP-1816 | Conflict | P1 | The FSD reads the ACE views and v_ace_batch_status directly; Arch v5 gives that read to rwb-source-data and the slide 13 matrix gives the S8 row one R and one E to P1 |
| GAP-1817 | Outdated | P2 | Three FSD integration points name the Quartz scheduler; Arch v5 and the Temporal design replace it with durable timers in DeviationWorkflow |
| GAP-1818 | Conflict | P1 | The raise, the clear and the read are each named three different ways, and no read operation is recorded for the deviation query the FSD times at two seconds |
| GAP-1819 | Missing | P2 | The Ownership Map gives S8 one table; the FSD requires a screening run, a score, a contact stop and a breach record as well |
| GAP-1820 | Conflict | P1 | The FSD records an approver on a deviation while the S8 row has no rwb-decision cell and no approval workflow is named for the service |
| GAP-1821 | Missing | P2 | The FSD calls the fraud system, the bureau, the external flow system, the litigation system, the appraisal system and the partner portal directly; the S8 row has no rwb-integration and no outside cell |
| GAP-1822 | Missing | P1 | The screening reads call notes and documents; the S8 row has no rwb-document cell and no call-note data product is named |
| GAP-1823 | Ambiguous | P2 | Seven E2 features carry the same case-record "Timers shown" criterion on another story, and every alternate and exception row repeats three scenarios |
| GAP-1824 | Missing | P2 | All ten E7 features carry the placeholder criterion "Written one epic ahead" and no alternate flow |
| GAP-1825 | Conflict | P1 | REQ-DVH-008 is E3 in the program and the FSD and E7 in the BRD, and BRD Q-015 is open |
| GAP-1826 | Missing | P2 | The FSD names 12 of the 22 R-DEV rules and the deviation route-set package is Phase 2 with no owner |
| GAP-1827 | Missing | P2 | The deviation service level is "set with DL22" and has no number; the ten working day escalation comes only from the design |
| GAP-1828 | Missing | P2 | The confidence threshold and the evidence required to run the agent at level 1 are not stated |
| GAP-1829 | Missing | P3 | The retention period and the classification scheme of the deviation record are not set (DL26, Q-012) |
| GAP-1830 | Missing | P3 | The two deviation screens have no owner cell in the service catalogue and no recorded edge route |
| GAP-1831 | Missing | P3 | The wording, the Thai version and the approver of the eight messages are not in the FSD (DL10) |
| GAP-1832 | Missing | P2 | The two events have a catalogue row and a topic but no field list, while the criteria expect an agent verdict and a decision record entry to travel |
| GAP-1833 | Missing | P3 | No deviation, screening or queue volume is stated for this module |
| GAP-1834 | Missing | P3 | The change notes and dates of FSD S8 versions 1 and 2 are not in the sources read |

## Assumption rows raised (ASM)

| ID | Confidence | Subject |
|---|---|---|
| ASM-2994 | High | Read path through the rwb-source-data contract only; boundary test fails the build on a view or ACE table read |
| ASM-2995 | High | The pause, the prescription clock and the resume are durable timers in DeviationWorkflow; no Quartz dependency |
| ASM-2996 | Medium | The raise and the clear are the two recorded commands and the deviation read is one GET through gateway-bff; no other path is fixed |
| ASM-2997 | Medium | Five entity groups in rwb_deviation, one named by the Ownership Map and four named as product entities |
| ASM-2998 | Medium | The approval a deviation carries is a step in DeviationWorkflow recorded through the decision-record library |
| ASM-2999 | Medium | Every outside effect is a contract dependency on rwb-integration or on the owning service's contract |
| ASM-3000 | Medium | Documents through P5 and call notes through P1; no copy of either in the deviation schema |
| ASM-3001 | Medium | Each FSD criterion row is one criterion; the step criteria the source row does not assert are this PRD's |
| ASM-3002 | Medium | The E7 placeholders are carried unchanged and their tests are written at story grooming |
| ASM-3003 | Medium | The deceased slice lands twice on purpose: the E3 conduct control in wave 2 and the full X3 flow in wave 4 |
| ASM-3004 | Medium | The 12 named R-DEV rules plus R-DEV-19 to R-DEV-21 are the requirement set; the rest is package authoring |
| ASM-3005 | Medium | The service level, the escalation period and the skip trace window are reference data; no number asserted |
| ASM-3006 | Medium | The confidence threshold and the autonomy policy are held by rwb-agent and rwb-decision; no value asserted |
| ASM-3007 | Medium | The deviation record is confidential, the handler identifier is a staff identifier, and no retention period is stated |
| ASM-3008 | Medium | The two screens are gateway-bff composite routes; this service owns neither |
| ASM-3009 | Medium | Message IDs and English wording preserved; Thai wording and approver left to DL10 |
| ASM-3010 | Medium | Two events by name and topic, keyed by case, CloudEvents through the outbox, no personal and no financial value |
| ASM-3011 | Medium | No module volume asserted; the platform population figures and the 200 and 500 case samples are used |
| ASM-3012 | High | Status Draft and no approval recorded in this run; the BRD is read as approved and the missing approval is this assumption |
| ASM-3013 | High | Service wave 2, EP02 and EP03 wave 2, EP07 wave 4; no wave conflict is raised |
| ASM-3014 | High | The PRD's identifier families are new; every FSD and BRD identifier is preserved character for character |
| ASM-3015 | High | The FSD v1 and v2 change notes are carried as "not specified" rather than reconstructed |

## Decisions taken

1. Status Draft and an empty approval table, per the D-RCV-60 overlay: a missing approval is an assumption, never an answer.
2. Release slicing by wave and by business epic: the service is wave 2 with EP02 (release 31 December 2026 (tentative)), the E3 conduct slice lands at the E3 release (31 January 2027 (tentative)) and the X1 to X7 flows land in wave 4 with EP07 (31 May 2027 (tentative)). Every date is copied unchanged from the program and the split plan and marked "(tentative)".
3. The E2 slice is sliced six ways in wave 2 so that each slice is independently demonstrable: the record and the read path, the two clocks, the code-to-owner route, the contact stop, the clear and the second deviation, and the screening agent.
4. No design beyond the confirmed v5 constraints: no class name, no DDL, no endpoint beyond the three operations the sources already record (and the read carried as open), and no physical table name beyond `deviation`.
5. Every owner is taken from the Ownership Map. Where the map has no owner for an edge or a table, the row says so and a gap row and an assumption row are raised instead of a name being invented.
6. `_work/msr/plan/ids.json` was read and is not needed: this document introduces no new decision, ADR or decision-log row, and cites D-RCV-60, ADR-013 to ADR-023 and DL44 to DL49 as inherited.
7. The 19 CG rows and the 22 ASM rows are candidate rows only. Their final numbering as GAP-nnnn and ASM-nnnn and the rewriting of every citation is left to step D1.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S8 --quick` — C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, no findings.

Additional audit run from the scratch folder: 42 CG and ASM citations in the document, all resolved against the two registers (the one non-PRD citation, ASM-0074, resolves against the table rulings register); 19 CAP, 56 FR, 29 NFR, 23 AC, 7 JRN, 13 ROL and 16 OQ identifiers with no gap in any family; 56 of 56 functional requirements covered by an acceptance criterion; every markdown table with a consistent column count; header lines present; no issue-tracker reference, no email address and no person name.

C14, C17, C19, C20 and C01 were also run against this work package's files: C14 PASS, C17 PASS, C20 PASS, C01 PASS. C19 reports only the planned outputs of other work packages that have not been written yet in this run (for example B-P1-04, B-P3-02 and B-P4-06) and carries no finding for B-REQ-PRD-S8.

No failure to record. No retry was needed.
