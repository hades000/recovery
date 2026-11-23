# Edit log - WP B-TECH-07 (Recovery Workbench Rules Engine Design next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Fanout: 0 (one worker, no subagents). Status: Draft, no approval recorded
(ASM-3271).

Sources read: `05 Technical architecture/Recovery Workbench Rules Engine Design v3.docx`, converted with
`compat/convert_sources.py` to `_work/msr/extract/B-TECH-07/Recovery Workbench Rules Engine Design v3.md`
(read-only); `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md`
(R1, R3, R5, R8, R9); `_work/msr/plan/ownership.json`; `22 Microservice Realignment/Recovery Workbench
Microservice Ownership Map v1.xlsx` (Services, Tables, Endpoints, Events, Workflows and activities, Jobs,
Parameters, Rulings); `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md`;
`22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`;
`_work/msr/plan/split_plan.json` (stats and legacy only); `_work/msr/plan/ids.json`.

## Files written

- 05 Technical architecture/Recovery Workbench Rules Engine Design v4.docx
- _work/msr/gaps/B-TECH-07.jsonl
- _work/msr/assumptions/B-TECH-07.jsonl
- _work/msr/editlog/B-TECH-07.md

Scratch files under `_work/msr/docs/B-TECH-07/` (build and verification only, not outputs of the run):

- _work/msr/docs/B-TECH-07/Recovery Workbench Rules Engine Design v4.md
- _work/msr/docs/B-TECH-07/fix_template.py
- _work/msr/docs/B-TECH-07/polish.py
- _work/msr/docs/B-TECH-07/set_props.py
- _work/msr/docs/B-TECH-07/verify.py
- _work/msr/docs/B-TECH-07/verify_docx.py

`template-fixed.docx` (the scratch template copy) also sits there and is not an output.

## What was done

Version 3 was never edited. The full text of the next version was written to the scratch `.md` above and
rendered with `compat/office_write.py md-docx` against a scratch copy of the source document, so the family
styles, page setup and section properties carry over. Three scratch scripts then restore the look of version 3
(title block 26 pt / 17 pt in the family colours, body 10 pt, bullets as bullets, tables 9 pt with the
9 pt brand-coloured header row) and set the document properties to the organisation and the tool, because
the version 3 properties carry a person's name, which rule 4 forbids in an output.

1. **Header and change log.** Lines 1 and 2 of the new document are the header of Template and Rules R8.1.
   The document control table adds Version 4, the date, `Supersedes | Version 3, 16 November 2026`, the
   change-log row `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek
   v4.1 Flash`, the version 3 change row kept word for word, the decision (D-RCV-60 with ADR-017) and the
   Status `Draft`.
2. **Every section, ID, number and date kept.** All eleven sections and their tables are present in the same
   order. `verify.py` compares the source text with the new text and reports PASS: every token that carries a
   digit (`ADR-012`, `DF-REF-274` to `DF-REF-299`, `DF-REF-261` to `DF-REF-273`, `MSG-P3-027`, `MSG-P7-002`,
   `ALLOC-031`, `ALLOC-2026.12`, `R-RES-25` to `R-RES-31`, `R-LIT-02`, `R-UNI-xx`, `E1-072`, `E1-073`,
   `E2-041`, `E2-042`, `E1-048`, `DL24`, `448`, `37`, `27`, `32`, `79`, `72`, `41`, `51`, `22`, `50`, `93`,
   `92`, `20`, `50` scenarios, `1000`, `988`, `00:01`, `02:00`, `3d`) appears in the new version, and so does
   every source heading, every table row and the dates 16 November 2026, 30 November 2026 and
   31 December 2026.
3. **Embedded Drools per service.** Section 1 now says Drools is embedded in each of the 19 services, in the
   service that owns the decision, and that the registry, versions and governance sit in rwb-decision (P7);
   the new row `Where it runs` states the split. Section 6 states where each of the six runtime parts runs:
   KieBaseRegistry, RuleEvaluator, DecisionLogAgendaListener and NoPackageInForce in every service on its own
   queue, RuleCatalog and RulePackageRepository in rwb-decision. Section 10.1 gives the same split as a table.
4. **Registry in rwb-decision.** Section 2 adds an owning-service column to both tables. Section 4 turns
   RulePackageEffectiveDateJob into the JOB-20 Temporal Schedule at 00:01 in rwb-decision, which publishes
   RulePackageInForce (EV-30); the state table itself is unchanged. Section 5 states that the load checks run
   in the registry and that each service repeats the checksum check at cache build. Section 8 adds the owner
   column and keeps the 93-table count of Physical Schema v6.
5. **Ownership Map for every owner.** Every owner is a code and service of the Microservice Ownership Map v1
   and `ownership.json`: the four rule tables and every `/admin/rule-package` path with P7 rwb-decision,
   `delegation_limit` with P4 rwb-access, JOB-14 and JOB-20 with P7, and the package owners S2, S3, S4, S5,
   S6, S7, S8 and P3 for the route sets. No owner is taken from a story master and no name of a person
   appears (ASM-3270).
6. **New decision IDs from `ids.json`.** ADR-017 (embedded Drools per service, registry in rwb-decision,
   amends ADR-012 and D-RCV-36 T1 and T2), ADR-014, ADR-016 and ADR-022 are cited in the document control row,
   the new section 1.1 table and the references. DL44, DL45, DL46 and DL49 appear in the references row for
   D-RCV-60. No ADR, DL or D-RCV number was invented (ASM-3273).
7. **Section 1.1, new.** Eight rows, one per change, each naming the version 3 statement it replaces, the
   version 4 statement and the decision. Nothing in section 1.1 removes a rule, a package, a check or a
   control.
8. **Section 7, one activity.** The version 3 order of WriteDecisionLogActivity and then ApplyStateActivity
   is replaced by one RecordAndApply activity, because ADR-022 writes the record, the change and the outbox
   row in one transaction. The version 3 order is named as the superseded statement and the conflict is
   recorded (GAP-2032; ASM-3266).
9. **Release dates.** 30 November 2026 and 31 December 2026 are copied unchanged and marked `(tentative)`;
   `Phase 2` stays as the source gives it. No date was raised as a gap (ASM-3272).
10. **Verification.** `verify_docx.py` reads the built `.docx` back and finds every heading, paragraph, bullet
    and table cell of the scratch `.md` in it: PASS, 447 fragments. `verify.py` reports PASS on tokens, dates,
    headings, table rows, header lines, change-log row, tentative dates and register citations.

## Registers

| Item | Value |
|---|---|
| Candidate gap rows | 10 (GAP-2025 to GAP-2034) |
| Candidate assumption rows | 15 (ASM-3260 to ASM-3274) |
| Gap types | Conflict 4, Ambiguous 3, Missing 1, Outdated 2 |
| Gap severity | P2 2, P3 8 |
| Assumption confidence | High 10, Medium 5 |

Every gap row names its assumption, and every gap and assumption citation in the document resolves to a row
of this WP. Numbering to GAP-nnnn and ASM-nnnn is left to step D1 (rule 7; Template and Rules R9).

The open points are: where Drools lives (CG-1), the owner of PAYMENT_MATCH (CG-2), who serves RuleCatalog
(CG-3), the fact class of each package (CG-4), the `/rule-models` operation (CG-5), delivery ownership of
E1-072 and E1-073 (CG-6), the effective-date job (CG-7), the decision-record write path (CG-8), the 93 tables
across 19 schemas (CG-9) and the owner of UNIVERSAL (CG-10).

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-07 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

C02, C03 and C05 are the story-file checks and this WP writes no story file. C12 finds no person name and no
email address: the version 3 document properties carried a person's name and were reset to the organisation
and the tool. C13 finds no issue-tracker reference. C18 finds no write outside the `Write only` list and no
change to a story master.

## Not done, by rule

- No approval was sought and none is recorded; the document is Draft.
- The source `.docx` was opened read-only and never written; no other document, master file or register was
  edited, and no register was numbered.
- No issue tracker, wiki, repository, Figma or web call was made and no commit was created.
- No later lifecycle stage was started.
