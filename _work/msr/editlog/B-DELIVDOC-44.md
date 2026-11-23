# Edit log - WP B-DELIVDOC-44 (Recovery Workbench Engineering Practices next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `11 Delivery and operations/Recovery Workbench Engineering Practices v6.docx`
- `_work/msr/docs/B-DELIVDOC-44/Recovery Workbench Engineering Practices v6.md`
- `_work/msr/docs/B-DELIVDOC-44/template-fixed.docx`
- `_work/msr/docs/B-DELIVDOC-44/verify/Recovery Workbench Engineering Practices v6.md`
- `_work/msr/docs/B-DELIVDOC-44/inspect.py`
- `_work/msr/docs/B-DELIVDOC-44/styles.py`
- `_work/msr/docs/B-DELIVDOC-44/scan.py`
- `_work/msr/docs/B-DELIVDOC-44/own_keys.py`
- `_work/msr/docs/B-DELIVDOC-44/own_peek.py`
- `_work/msr/docs/B-DELIVDOC-44/svc_peek.py`
- `_work/msr/docs/B-DELIVDOC-44/plt_peek.py`
- `_work/msr/docs/B-DELIVDOC-44/plan_peek.py`
- `_work/msr/docs/B-DELIVDOC-44/fix_template.py`
- `_work/msr/docs/B-DELIVDOC-44/set_props.py`
- `_work/msr/docs/B-DELIVDOC-44/verify_docx.py`
- `_work/msr/docs/B-DELIVDOC-44/scan_names.py`
- `_work/msr/docs/B-DELIVDOC-44/write_jsonl.py`
- `_work/msr/docs/B-DELIVDOC-44/check_extra.py`
- `_work/msr/gaps/B-DELIVDOC-44.jsonl`
- `_work/msr/assumptions/B-DELIVDOC-44.jsonl`
- `_work/msr/editlog/B-DELIVDOC-44.md`

Scratch only (`_work/msr/docs/B-DELIVDOC-44/`): the full text of the new version, the template
copy that `md-docx` can render, the property writer, the verification script and the small readers
used to count the Ownership Map and the plan. The converted source text was written by the
conversion tool to the extract folder the WP names, `_work/msr/extract/B-DELIVDOC-44/`.

## What was done

The source `11 Delivery and operations/Recovery Workbench Engineering Practices v5.docx` was never
edited. It was converted to text for reading, copied to the scratch folder as the render template,
and the new version was written in full as Markdown and rendered with
`compat/office_write.py md-docx` onto the repaired copy of the v5 template.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules §R8.1. The metadata
   table keeps every v5 row (Document, Version, Date, Prepared by, Applies to) and adds Supersedes
   (Version 5, 16 November 2026), Decision (D-RCV-60), Status (Draft) and the change-log row
   `6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
   Section 12 is a change-log table that carries that row again with what changed.
2. **Every section, ID, number and date of the source kept.** Sections 1 to 11 keep their titles and
   order, with the eleven pipeline gates (1 to 11), the four DEV and two SIT deployment slots, the one
   week of SIT and one week of UAT, the monthly release, the 2 s timeout, the 30 read-only views, the
   rule package checksum and four-eyes review, the decision log IDs DL04, DL05, DL07, DL32, DL34,
   DL35 and DL37, the dates 2 November, 29 Oct, 31 Oct, 30 Oct and 6 Nov, and the 16 November 2026
   date of the source. No date was raised as a gap. No release date is stated in the source, so
   section 9 records that the release dates are unchanged and tentative (U7; DL48) instead of marking
   a date that does not exist.
3. **Repository per service.** Section 2.1 replaces "one service, three modules" with one repository
   per service and gives the 19 services with their schema, REST base, topic, task queue and wave,
   read from the Services sheet of the Ownership Map v1 and matched to Template and Rules §R4. A
   second table maps the three v5 modules (common, collection, recovery) onto the new shape, and the
   edge (gateway-bff, partner gateway) and the one ACE front end are stated with DL07 and ADR-019.
   Section 2.2 turns the module boundary into the service and schema boundary: contract or event
   only, no cross-schema join, view or foreign key, only rwb-source-data reads the v_ace_* views.
4. **Contract first.** Section 2.4 gives the contract of every call type from Architecture v5
   slide 11: OpenAPI 3.1 with RFC 9457 problems and Idempotency-Key, AsyncAPI 3.0 with the JSON
   Schema registry in BACKWARD compatibility, the CloudEvents 1.0 envelope, the activity and workflow
   contract jar, the file manifest, the one hop and 2 s timeout rule. The CON story lands the
   contract and its fake before the application story, so a C dependency never blocks (R5.4, R5.7).
   Sections 4.1, 5, 6 and 7 carry the contract branch order, the contract review row, the contract
   test row and gate 7.
5. **Per-service Flyway.** Section 2.5 gives the per-service Flyway sequence, its own schema and
   history table, its own pipeline, the V0001 baseline, the no cross-schema DDL rule, expand and
   contract migrations, the Testcontainers migration test in every pull request, and the kept
   Epic 1 migration with the schema split as new work (R6; ADR-021). Section 6 adds the Migration
   test level and section 7 folds the migration check into gate 7, so the count of eleven gates of
   the source stays true.
6. **Ownership Map for every owner.** Section 10 keeps the eight practice rows of version 5 with
   their owners brought to the service shape and adds Contracts and Flyway, then adds the shared
   artefact table: parameters and reference data P3 rwb-case, case list API P3, rule registry
   P7 rwb-decision, interaction ledger P1 rwb-source-data, feature flags the platform library with
   the admin paths served by P2 rwb-integration, ACE data and views P1. Section 8 states the flags as
   library objects (`feature_flag`, `feature_flag_change`) from the Rulings and Tables sheets.
7. **Decision log kept and extended.** Section 11 keeps the seven v5 rows and adds DL44 to DL49 with
   the positions of Template and Rules §R8.4. The owner column of the seven v5 rows held a person
   name; it now names the role, because AGENTS.md rule 4 forbids a person name in a run document
   (ASM-0374). The same repair was applied to the core properties of the new docx.
8. **Template repair and document properties.** The family stores `w:name/@w:val` as `Heading 1`,
   which `python-docx` looks up as `heading 1`, so `md-docx --template` fails with
   `KeyError: no style with name 'Heading 1'`; the family also has no `List Bullet` style. The
   scratch `fix_template.py` repairs the copy only. `set_props.py` replaces the person name in the
   author and last-modified-by properties with the organisation and the tool line, sets the v6
   title, subject, category, comment and revision 6, and dates the document 22 November 2026.
   A byte scan of all 16 parts of the new docx finds no person name and no e-mail address.
9. **Verification.** The docx was extracted again with `compat/convert_sources.py`; the rendered
   Markdown and the extracted text match line for line (267 normalised lines each, 0 missing,
   0 extra), with 15 tables and 19 headings: the two title lines, sections 1 to 12 and the five
   subsections of section 2 and 4. No line contains a person name, an e-mail address, the issue
   tracker or its product name.
10. **Checks.** `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DELIVDOC-44 --quick`
    was run and passed: C02, C03, C05 (story-file checks, no story file in this WP), C12 (no person
    name, no e-mail), C13 (no issue-tracker reference) and C18 (no write outside the WP list, no
    legacy file changed). C14 (header lines), C17 (every CG and ASM citation has a row) and C20
    (tool line) were run against the same file set and also pass.

## Registers

- Gap rows: 8 (`GAP-0284` to `GAP-0291`): Conflict 1 (documentation, the one
  service position against the 19 services), Outdated 1 (infrastructure, the deployment slots),
  Missing 6 (data 3, governance 2, documentation 1). Severity: P2 5, P3 3. No gap row raises a date.
- Assumption rows: 8 (`ASM-0374` to `ASM-0381`), confidence High 2,
  Medium 6, Low 0.
- Every missing value in the document is the R9 placeholder with its CG and ASM pair; no repository
  name, table cut, contract approver, slot count, owner or date is invented.

## Not done, by rule

- No approval was sought and none is recorded; the document is issued as Draft.
- No master file was written, no register was numbered, and no other document was edited.
- No issue tracker, Confluence, repository or web call was made, and no commit was created.
