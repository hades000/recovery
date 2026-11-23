# Edit log - WP B-TECH-09 (Observability and Monitoring Design next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Status: Draft, no approval recorded (ASM-3283). Fanout: 0.

## Files written

- `05 Technical architecture/Recovery Workbench Observability and Monitoring Design v4.docx`

- `_work/msr/docs/B-TECH-09/Recovery Workbench Observability and Monitoring Design v4.md`

- `_work/msr/docs/B-TECH-09/build_md.py`

- `_work/msr/docs/B-TECH-09/build.py`

- `_work/msr/docs/B-TECH-09/template-fixed.docx`

- `_work/msr/docs/B-TECH-09/verify.py`

- `_work/msr/docs/B-TECH-09/write_jsonl.py`

- `_work/msr/docs/B-TECH-09/verify/Recovery Workbench Observability and Monitoring Design v4.md`

- `_work/msr/gaps/B-TECH-09.jsonl`

- `_work/msr/assumptions/B-TECH-09.jsonl`

- `_work/msr/editlog/B-TECH-09.md`

Scratch only (under `_work/msr/docs/B-TECH-09/`): the full rendered text of version 4, the generator
that writes it from the Ownership Map, the repaired template copy, the row writer and the verification
script, and the round-trip extract used to check the docx. The converted source text sits in
`_work/msr/extract/B-TECH-09/` and is not an output of the run.

## What was done

The source `05 Technical architecture/Recovery Workbench Observability and Monitoring Design v3.docx`
was never edited. It was converted to text for reading with `compat/convert_sources.py`, and the new
version was written in full as Markdown, then rendered with `compat/office_write.py md-docx` onto a
repaired copy of the v3 template. The copy is repaired only so the renderer finds the `heading 1` style
names and a `List Bullet` style; the family itself is unchanged and the footer of version 3 is kept.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules §R8.1. The metadata
   table keeps every v3 row (Document, Version, Date, Change, Prepared by, Structure) and adds
   Supersedes (3, 16 November 2026), Source version, Decision (D-RCV-60; ADR-023), Tool and Status
   (Draft). The Change row is the change-log row `4, 22 November 2026, D-RCV-60 microservice
   realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`; the change-log table also keeps the v3 row
   word for word.
2. **Every section, ID, number and date kept.** Sections 1 to 4 keep their titles, their order, their
   tables and their paragraphs; 1.1, 1.2, 2.1, 2.2, 3.1, 4.1 and an open-points section are added.
   Every ID of v3 is still present (MSG-P3-037, MSG-P3-027, temporal.stuck.hours, RWB-E1-056,
   RWB-E1-070, RWB-E1-073, RWB-E2-037, RWB-E2-038, RW-PLATADM, RW-COE, NoPackageInForce, KieBase),
   every number (50th and 95th percentile, 5xx above 1 percent for 5 minutes, 2 seconds for 15
   minutes, 10 percent of calls in an hour, 50 items or one day, 24 hours, 07:00, 15 minutes, 1 hour,
   next morning, every 5 minutes) and every date (16 November 2026) is copied. `verify.py` checks the
   token list against the v3 text: 0 missing. The source holds no release date, so none is written;
   any date added later is tentative under U7.
3. **Per-service dashboards and alerts.** Section 1.1 gives the 19 measured units, copied from the
   Ownership Map v1 Services sheet (code, service, wave, schema, topic, task queue, owner). Section 1.2
   says what each v3 area covers after the split. Section 2.1 reads the 13 alerts with the service as
   the unit and keeps every threshold and window; section 2.2 gives the ownership and routing of each
   alert scope. Section 3.1 turns the one Service health dashboard into one per service and fixes the
   panel groups each one carries; the four other dashboards stay and name the owning service on each
   panel. Section 4.1 maps each run book to the service and to the story that writes it.
4. **Owners.** Every owner named as a service is the code and service name of the Ownership Map v1
   Services sheet (ASM-3297); the platform parts stay with the platform team; the six recipient
   role names of version 3 are kept as they are and are not mapped to a role code that no source gives
   (GAP-2048; ASM-3293). No person is named anywhere.
5. **New decisions.** The version cites ADR-023 for observability per service, with ADR-013, ADR-015,
   ADR-016, ADR-017 and ADR-022 where the text changes, and D-RCV-60 in the metadata, the change log
   and the realignment table; all of them come from `_work/msr/plan/ids.json` and Rules v1 §R8.4. No
   new ADR or DL ID was allocated by this work package.
6. **What the realignment exposes.** Nine points are stated in the text and raised as gaps instead of
   being silently changed: the one-to-19 read of the measures, dashboards and alerts (GAP-2043);
   the owner of a per-service artefact (GAP-2044); the metric, label, retention, sampling and
   delivery conventions (GAP-2045); the Quartz job table (GAP-2046); the local record plus
   central ledger (GAP-2047); the recipient role names (GAP-2048); the rule package compile
   alert named P3 while the registry is P7 (GAP-2049); the Data health and Work health panels
   (GAP-2050); and the hash chain check across 19 local chains and one ledger (GAP-2051).

**Never invented.** No source file was changed and no value was invented: where the sources are silent
the text says so and the gap and assumption rows carry the point. No dashboard name beyond the five of
version 3, no per-service SLO, no threshold beyond the ones version 3 fixes, no metric or span name, no
retention or sampling value, no alert delivery channel, no role code beyond RW-PLATADM and RW-COE and
no release date is written.

## Counts

| Item | Value |
|---|---|
| Candidate gap rows | 9 (GAP-2043 to GAP-2051) |
| Candidate assumption rows | 13 (ASM-3288 to ASM-3299) |
| Services in section 1.1 | 19 |
| Services in section 3.1 | 19 |
| Alerts in section 2 and section 2.1 | 13 in each, with the same thresholds and windows |
| Changes recorded in the realignment table | 10 |
| Source tokens checked by `verify.py` | 25, none missing |

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-09 --quick`: PASS (C02, C03,
C05, C12, C13, C18; the story checks C02, C03 and C05 have no story file in this work package).
`verify.py` reports PASS: header lines present, change-log row present, every v3 section heading kept
and in order, no source token missing, two per-service rows for each of the 19 codes, every named
single-owner alert instance present, no person name, no email address and no issue-tracker reference.

## Second pass (work package re-issued)

The work package was issued again after the run above had already delivered version 4. Version 4 was
re-verified instead of rewritten: rule 1 forbids editing a file that already exists, the "Write only"
list of the work package names version 4 and nothing later, and a further version would fall outside
that list (check C18 rejects any file written outside it). No deliverable was created, changed or
deleted in this pass.

What was re-read, and the result:

| Item | Result |
|---|---|
| Header lines 1 and 2 (Template and Rules §R8.1) | Present in the rendered docx |
| Change-log row `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash` | Present, in the metadata Change row and in the change-log table |
| Sections 1 to 4 and their headings, in order | All four kept, none renamed |
| Source IDs and numbers (MSG-P3-037, MSG-P3-027, temporal.stuck.hours, RWB-E1-056, RWB-E1-070, RWB-E1-073, RWB-E2-037, RWB-E2-038, RW-PLATADM, RW-COE, NoPackageInForce, KieBase, 50th and 95th percentile, 1 percent, 2 seconds, 50 items, one day, 24 hours, 07:00, 90 days) | 0 missing against the converted source text |
| Source dates | 16 November 2026 kept; no release date exists in the source, so none is written |
| 19 measured units (1.1) against the Ownership Map v1 Services sheet | Code, service, wave, schema, topic and queue match for all 19 rows |
| 19 per-service dashboards (3.1) | One row per service, owner is the service code of the map |
| 13 alerts, thresholds and windows | Unchanged in section 2 and in section 2.1 |
| Story IDs cited (RWB-PLT-N005-OPS, RWB-PLT-E2037-APP, RWB-PLT-E2038-APP, RWB-PLT-E1056-OPS, RWB-P7-E1073-APP, RWB-P3-E1073-APP, RWB-P6-E1073-APP, RWB-P2-E1073-APP) | All present in `split_plan.json`; no identifier invented |
| Decision IDs | D-RCV-60 with ADR-023 and ADR-013, ADR-015, ADR-016, ADR-017, ADR-022, all from `ids.json` |
| Candidate rows | 9 gap rows and 13 assumption rows, key sets of §R9 complete |
| Person names, email addresses, issue-tracker references | None |
| `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-09 --quick` | PASS (C02, C03, C05, C12, C13, C18) |

One point was re-read and left as it stands. JOB-10 (WIN notices) is owned by P6 rwb-comms in the
Ownership Map v1, and the replacement text of that row calls it a Temporal Schedule, while
Architecture v5 slide 44 gives its mechanism as "Airflow file window + workers". Under R-PREC the
catalogue slide outranks the derived map, so P6 carries no Schedule-to-start latency instance and the
set stays P3 rwb-case (JOB-06), P4 rwb-access (JOB-18), P5 rwb-document (JOB-17), P7 rwb-decision
(JOB-14 and JOB-20), S5 rwb-asset (JOB-19) and S7 rwb-writeoff (JOB-16). The point is documentation
only and is carried by GAP-2046, which records that the Jobs row now reads the job map rather
than one shared table; no new row was raised for it because this pass changed nothing.

Scratch added in this pass: `_work/msr/docs/B-TECH-09/recheck/`, the converted text of the delivered
docx used for the comparison above.

| Item | Value |
|---|---|
| Deliverables written in this pass | 0 (version 4 already in place) |
| Candidate gap rows | 9, unchanged |
| Candidate assumption rows | 13, unchanged |
| Checks | PASS (C02, C03, C05, C12, C13, C18) |
