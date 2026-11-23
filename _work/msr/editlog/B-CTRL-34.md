# Edit log - WP B-CTRL-34 (Recovery Workbench Personal Data Protection Design next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Work pack: B-CTRL-34. Fanout: 0.

## Files written

- `10 Policy, controls and compliance/Recovery Workbench Personal Data Protection Design v3.docx`
- `_work/msr/docs/B-CTRL-34/Recovery Workbench Personal Data Protection Design v3.md`
- `_work/msr/docs/B-CTRL-34/fix_template.py`
- `_work/msr/docs/B-CTRL-34/template-fixed.docx`
- `_work/msr/docs/B-CTRL-34/set_props.py`
- `_work/msr/docs/B-CTRL-34/verify_fidelity.py`
- `_work/msr/gaps/B-CTRL-34.jsonl`
- `_work/msr/assumptions/B-CTRL-34.jsonl`
- `_work/msr/editlog/B-CTRL-34.md`

The source text for reading came from the sanctioned conversion command, written to `_work/msr/extract/B-CTRL-34/`. The source workbook was never edited: the v3 file was built new from the full text by `compat/office_write.py md-docx` against the v2 document as the style template, so no existing file is opened for writing.

## What was done

1. **Header and metadata.** The first two lines are the Template and Rules §R8.1 header. The title block keeps "Recovery Workbench" and "Personal data protection design" and adds the version line. The metadata table keeps the v2 rows and adds the source version, the decision D-RCV-60, the status Draft, the tool, the tentative-dates row and the change-log row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
2. **Sections 1 to 10 kept.** Every heading, category, classification, lawful-basis section, consent rule, minimization rule, access rule, retention statement, right, recipient, safeguard, breach rule and open decision (DL26, DL33) is kept word for word. `verify_fidelity.py` compares all 117 non-empty paragraphs and table cells of v2 against v3: the only string that differs is the v2 title date line `SCB Collections and Recovery. Henka Group, 28 October 2026`, replaced by the §R8.1 header; the date itself is kept in the metadata row "Source version 2, dated 28 October 2026" and in the version line.
3. **Closing paragraphs added, not substituted.** Sections 3, 4, 5, 6, 7, 8 and 9 each keep their v2 text and gain one paragraph that names the target service owner of the statement. This is the only edit inside sections 1 to 10; no v2 sentence is reworded.
4. **Section 11 (new).** Personal data boundaries per service: Table 11.1 with one row per service, 19 rows, each owner taken from Ownership Map v1 and Architecture v5 slide 41 (P1 to P10, S1 to S9), the personal data it may hold, the owned tables, and what it must not hold; Table 11.2 with the enforcement point and rule owner of each control in sections 4, 5, 6 and 12.
5. **Section 12 (new).** Personal data in events, workflow payloads and logs: Table 12.1 the event envelope (CloudEvents 1.0 binary, key caseId, IDs and facts only, schema registry BACKWARD, outbox/inbox, ACLs separate from the ACE PII logging topics), Table 12.2 the 16 event groups with what travels and where the personal data stays, then the workflow payload rules (PdpaPayloadCodec AES-GCM, Key Vault, search attributes CaseId/Stage/ProductGroup/QueueCode, 30-day retention, break-glass decode), the log and PII Kafka path, and the file and third-party paths.
6. **Section 13 (new).** Change log with the D-RCV-60 row and the list of what changed, and nothing else.
7. **Decisions.** New decisions use only the IDs of `_work/msr/plan/ids.json`: D-RCV-60, ADR-010 (existing, cited), ADR-014, ADR-015, ADR-020, ADR-021, ADR-022, DP-01, DP-02, DP-03, DP-05, DP-08, DP-09, DP-11, DP-12, DP-17. No new ADR, DL or decision number is created.
8. **Document properties.** The v2 file carries a person name in Creator and Last modified by. Both are set to "Henka Group" in v3; title, subject and comments carry version 3, D-RCV-60 and the tool line. No person name appears in the document text or its properties.
9. **Dates.** No date is added or changed. The document date of v3 is 22 November 2026 (the run date); the v2 date of 28 October 2026 is kept. The metadata states that programme dates are tentative (D-RCV-60, U7). No release date exists in the source and none is invented.

## Gaps and assumptions

- Gap rows written: 8 (`GAP-0186` to `GAP-0193`).
- Assumption rows written: 8 (`ASM-0276` to `ASM-0283`), one twin per gap.
- Every placeholder in the document carries its pair: sections 3, 4, 5, 7, 11 and the metadata table.
- Subjects: v2 stamps itself Version 1 (CG-1); no service owner anywhere in v2 (CG-2); consent column name in the target schema (CG-3); no approval recorded (CG-4); debt-sale masking check owner and field list (CG-5); PII read log has no event contract (CG-6); data-subject retrieval across 19 services (CG-7); tokenization point and token format (CG-8).
- Severity: 3 rows P2 (CG-3, CG-5, CG-8) and 5 rows P3 (CG-1, CG-2, CG-4, CG-6, CG-7). No row is P1.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-CTRL-34 --quick` was run after the files were written: C02, C03, C05, C12, C13 and C18 all PASS with zero findings. The fidelity check (`verify_fidelity.py`) reports 117 source strings checked and 1 difference, the replaced title date line noted above. No failure needed a fix in the document.

## Notes

- Every owner in sections 11 and 12 is the table owner of Ownership Map v1; no owner is invented and none is taken from a person's name.
- P2 rwb-integration holds file content only in transit, and P9 rwb-reporting is read-only from events; neither is given a PII store it does not own in the Architecture v5 extract.
- `template-fixed.docx` is a scratch copy only, made because this document family has no python-docx `Heading 1` lookup and no `List Bullet` style; the v2 source is untouched.
