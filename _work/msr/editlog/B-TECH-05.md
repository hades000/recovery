# Edit log - WP B-TECH-05 (Environment and Deployment Design next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Status: Draft, no approval recorded (ASM-3238).

## Files written

- `05 Technical architecture/Recovery Workbench Environment and Deployment Design v5.docx`

- `_work/msr/docs/B-TECH-05/Recovery Workbench Environment and Deployment Design v5.md`

- `_work/msr/docs/B-TECH-05/template-fixed.docx`

- `_work/msr/docs/B-TECH-05/fix_template.py`

- `_work/msr/docs/B-TECH-05/set_props.py`

- `_work/msr/docs/B-TECH-05/write_jsonl.py`

- `_work/msr/docs/B-TECH-05/verify.py`

- `_work/msr/docs/B-TECH-05/verify/Recovery Workbench Environment and Deployment Design v5.md`

- `_work/msr/gaps/B-TECH-05.jsonl`

- `_work/msr/assumptions/B-TECH-05.jsonl`

- `_work/msr/editlog/B-TECH-05.md`

Scratch only (under `_work/msr/docs/B-TECH-05/`): the full rendered text of the new version, the repaired
template copy, the small property script, the row writer and the verification script, and the round-trip
extract used to check the docx. The converted source text sits in `_work/msr/extract/B-TECH-05/` and is not an
output of the run.

The docx family carries an author and a last-modified-by property from its template, and this family inherited
a person name. Both properties of the new version are set to the organisation and the tool, and the repaired
template copy in scratch is cleaned the same way, so no person name is left in any file this work package
wrote (AGENTS.md rule 4).

## What was done

The source `05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx` was never
edited. It was converted to text for reading with `compat/convert_sources.py`, and the new version was written
in full as Markdown, then rendered with `compat/office_write.py md-docx` onto a repaired copy of the v4
template. The copy is repaired only so the renderer can find the `heading 1` style names and a `List Bullet`
style; the family itself is unchanged, and the footer of version 4 is preserved.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules §R8.1. The metadata table
   keeps every v4 row (Document, Version, Date, Change, Prepared by, Structure) and adds Supersedes (version 4,
   16 November 2026), Decision (D-RCV-60) and Status (Draft). The Change row is the change-log row
   `5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
2. **Every section, ID, number and date kept.** Sections 1 to 8 keep their titles and order, with 3.1 and the
   new 3.2, and the new section 9 records the changes. Every ID of v4 is still present (RWB-ACE-001,
   RWB-E1-069, RWB-E1-070, RWB-E1-073, RWB-E2-039, TE-001, V0001, JOB-05, D-RCV-28, D-RCV-35, D-RCV-36,
   ADR-011, DL03, DL04, DL05, DL11, DL27, DL33, DL34, DL35, DL37, DL43, temporal_svc, recovery_svc,
   ace_view_owner, rwb.p3.temporal, rwb.p3.drools, rwb-platform), every number (16 Tier 1 and 14 Tier 2 views,
   30 recovery.v_ace_* views, 30 days of retention, cache 20, 50 rule test cases, port 7233, 99.9%, 2 November,
   21 November 2026, 16 November 2026) and every version (server 1.28.1, Java SDK 1.31.0). `verify.py` checks
   the token list against the v4 text: 0 missing. No release date appears in the source, so none is written;
   the text states that any date added later is tentative (U7; ASM-3246).
3. **Per-service deployments.** Section 1 restates the deployment unit as 19 services inside ACE (ADR-013);
   section 3 restates each shared row and adds the Kafka row and the per-service worker, queue and Drools rows;
   the new section 3.2 gives one row per service with code, service, wave, schema, topic, task queue, API pods
   and worker scaling, all values taken from the Ownership Map v1 (sheet Services). The estate is about 38
   small deployments at rest (Arch v5 slide 33).
4. **Environment names.** The four environment rows are kept as they are. The per-service names inside an
   environment (Helm release, Kubernetes deployment, DNS name) and the value of the `{env}` token are not fixed
   by any source, so the token is kept exactly as version 4 writes it and the missing names are written as the
   §R9 placeholder and carried by GAP-2009 and ASM-3239.
5. **Owners.** Section 3.2 and the paragraph after the section 3 table take every service owner from the
   Ownership Map v1 (sheet Services) and every shared owner from the role the source or Architecture v5
   slide 39 names: the ACE platform team and Enterprise Architecture for Kafka, the Platform team and the ACE
   team for Temporal, the ACE team and the DBA for the schemas and logins, P5 rwb-document for the document
   containers. No person is named anywhere.
6. **New decisions.** The version cites ADR-013 to ADR-017, ADR-019 to ADR-021 and ADR-023 from
   `_work/msr/plan/ids.json`, and D-RCV-60 in the metadata table and the header note. No new ADR or DL ID
   was allocated by this work package, and no decision-log row is written here; DL44 to DL49 belong to the
   decision log work package.
7. **Conflicts that the realignment exposes.** Four points where v4 and Architecture v5 disagree are stated in
   the text and raised as gaps instead of being silently changed: the Kubernetes namespace of the services
   against the namespace of the Temporal release (GAP-2010), the pinned server 1.28.1 against the 1.30
   floor for Nexus and Worker Versioning (GAP-2011), the 19 logins and connection budget (GAP-2012)
   and the shared Quartz and Spring Batch tables (GAP-2015). The Kafka row has no owner decision in any
   source (GAP-2014) and the per-service sizing has no figures (GAP-2013).

**Never invented.** No source file was changed and no value was invented: where the sources are silent the text
says so and the gap and assumption rows carry the point. No per-service Helm release, deployment or DNS name,
no login name beyond the three the sources fix, no CPU or memory figure, no replica maximum and no release date
is written.

## Counts

| Item | Value |
|---|---|
| Candidate gap rows | 7 (GAP-2009 to GAP-2015) |
| Candidate assumption rows | 10 (ASM-3238 to ASM-3247) |
| Services in section 3.2 | 19 |
| Component rows in section 3 | 20 (v4 had 19) |
| Changes recorded in section 9 | 14 |
| Source tokens checked by `verify.py` | 54, none missing |

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-05 --quick`: PASS (C02, C03, C05, C12,
C13, C18). C17 (gap and assumption keys and citations) and C20 (tool line) were also run against the same file
set and PASS. `verify.py` reports PASS: header lines present, change-log row present, every v4 section heading
kept, no source token missing, 19 service rows.
