# Edit log — WP B-TECH-08 (Recovery Workbench Security and Access Design next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Security and Access Design v4.docx` (converted text, all 11
sections), `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, §R3, §R5,
§R8, §R9), `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map
v1.xlsx` (Read me, Services, Tables, Endpoints, Workflows and activities, Rulings), `22 Microservice Realignment/Recovery
Workbench Architecture v5 Text Extract v1.md` (slides 5, 10, 11, 14, 29, 30, 35, 39, 41, 44),
`22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (L2 and L4, decision
record, PDPA notes), `_work/msr/plan/split_plan.json` (stats and legacy only) and `_work/msr/plan/ids.json`.
Nothing read was edited; the v4 document was opened read-only and used as a template, never written.

## Files written

- 05 Technical architecture/Recovery Workbench Security and Access Design v5.docx
- _work/msr/gaps/B-TECH-08.jsonl
- _work/msr/assumptions/B-TECH-08.jsonl
- _work/msr/editlog/B-TECH-08.md

Scratch files under `_work/msr/docs/B-TECH-08/` (build and verification only, not outputs of the run): the full text
`Recovery Workbench Security and Access Design v5.md`, `template-fixed.docx`, `build.py`, `verify.py` and the round-trip
extract under `roundtrip/`. The converted source text sits in the run extract folder, `_work/msr/extract/B-TECH-08`.

## 1. How the next version was produced

The source was never edited. The full text of version 5 was written to
`_work/msr/docs/B-TECH-08/Recovery Workbench Security and Access Design v5.md` and rendered onto a scratch copy of the v4
document with `compat/office_write.py md-docx --template`, so the new version keeps the v4 styles, section properties,
page setup and footer.

**Template repair, in the scratch copy only.** This document family stores the heading style names as `Heading 1`, which
`python-docx` looks up as `heading 1`, and it has no `List Bullet` style; `md-docx` therefore failed on the family, and the
bullet fallback appended a second, prefixed copy of every bullet. `build.py` repairs the copy (conventional style names, a
`List Bullet` style on `List Paragraph` with the numbering the v4 document uses) and then renders. The v4 file is byte-for-
byte unchanged; `roundtrip/` is the extract of the new file used for verification.

**Document properties.** The v4 file carries a person name in `author` and `last_modified_by`. `build.py` sets the new
file to `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Security and Access
Design v5`, revision 5, modified 22 November 2026 (rule 4).

**Header, change log and status.** Lines 1 and 2 of the new file are the header of Template and Rules §R8.1. The metadata
table carries the change row `5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
Flash`, the source version row `4, 16 November 2026` and the status row `Draft. No approval is recorded for this version
(ASM-3283)`. The change log repeats the v4 change row of 16 November 2026 and D-RCV-36 character for character.

## 2. Fidelity to version 4

`verify.py` compares every non-empty line of the v4 text with the round-trip extract of the v5 file:

| Item | Result |
|---|---|
| Lines of version 4 present verbatim in version 5 | All, except the lines listed as intended changes below |
| Lines of version 4 not found and not listed as changed | 0 |
| Sections | 1 to 11, in order |
| Subsections | 3.1, 3.2, 4.1, 4.2, 7.1, 7.2 |
| Tables | 18 (14 of the source, 4 new) |
| Header lines 1 and 2 | Present, as the first two lines |
| Change-log row with D-RCV-60 and the tool line | Present |

Every heading, table, ID, number, message code (MSG-P4-001 to MSG-P7-002), role code (RW-PLATADM, RW-AUDIT, RW-SECADM,
RW-COE, RW-RISK, SY-RULES, SY-CASEWF), decision reference (DL01 to DL43, D-RCV-35, D-RCV-36, ADR-010 to ADR-012, E1-037,
E1-039, E1-069, E1-070, E2-038) and date (16 November 2026, the DL43 date of 21 November 2026) of the source is kept. No
date is moved and no release date is added; the one forward date stays as written and is read as tentative under U7
(ASM-3284). Section 4.1 of the source, "Rights on the new objects", becomes 4.2 and its nine rows are unchanged,
because the authorise contract takes the 4.1 place; the order of the sections is unchanged.

## 3. What version 5 changes, and why

The change set is the realignment only: login per service, workload identity, and the authorise contract. The closing
table of the document, `Realignment changes in version 5 (D-RCV-60)`, lists the twelve changes with the section, the v4
value, the v5 value and the decision. In summary:

1. **Login per service.** The single `recovery` schema and the single `recovery_svc` login of sections 1, 2, 7, 9 and 10
   become 19 schemas and 19 logins `rwb_<short with _>`, one per service, each with grants on its own schema only, a
   PgBouncer pool and a connection cap, and its own Flyway sequence (ADR-014, ADR-021; DP-02, DP-15). Schema `recovery`
   keeps the 30 read-only `v_ace_*` views and nothing else. The `recovery_svc isolation` row is replaced by a service
   login isolation row that says so in words, so the change is visible in the document.
2. **ACE data access.** Only `rwb_source_data` (P1) holds USAGE on schema recovery and SELECT on the views. The other 18
   logins hold no grant on schema recovery and no grant on any ACE schema, and they read ACE data through the
   rwb-source-data REST contract (DP-05, DP-11).
3. **Workload identity.** One workload identity per service, 19 in all, plus one per non-human actor. The new §7 rows
   (`Workload identity`, `Kafka`, `Service login isolation`) carry mesh mTLS, per-service Kafka ACLs with OAUTHBEARER
   (Entra) or mTLS, and one worker identity per Temporal task queue (Architecture v5 slides 11 and 35; ADR-013, ADR-014).
4. **Authorise contract.** Every service authorises its own object against cached permission data from rwb-access. The
   new §4.1 table names the four operations of Architecture v5 slide 14 and their owner P4, the cache refresh on
   `rwb.access.events.v1`, and the guard library as a platform contract story (`H RWB-PLT-E1037-CON`; `C
   RWB-P4-E1037-CON`; DP-08). The new §4.2 second table gives the owning service of every object that the rights table
   touches, from the Ownership Map: CaseWorkflow P3, the stage workflows S1 to S8, ApprovalWorkflow P7, the rule registry
   P7, the break-glass grant and the access log P4, the Temporal Web UI and codec server the platform.
5. **Masking, DoA and retention owners.** `masking_rule`, `delegation_limit`, `role`, `permission` and `role_conflict` are
   rows of rwb-access (P4); `retention_rule` is P5; `partner_user` is S9. The partner paragraph records the split, and the
   partner gateway in the DMZ replaces the external gateway wording (ADR-019).
6. **Drools.** The registry, the versions and the four-eyes approval stay central in rwb-decision (P7); each owning
   service loads the version in force, verifies the checksum and evaluates locally (ADR-017; DP-04).
7. **Decision log.** The local record in the owning service's schema plus the central ledger in rwb-decision (ADR-022).
8. **Temporal.** Certificates and codec keys are held per namespace, and the authorizer plugin maps the workload identity
   as well as the OIDC claim and the client certificate (E2-038).
9. **Logging and tests.** The access log is placed in rwb_access; the §10 table gains `Login per service`, `Authorise
   contract` and `Workload identity` and restates `Read-only ACE grant` for `rwb_source_data` and the other 18 logins.
10. **Open decisions.** §11 keeps DL01, DL03, DL26, DL38, DL40 and DL43 verbatim and adds DL44 to DL49 as decided on
    22 November 2026 under D-RCV-60 (ids.json; Rules v1 §R8.4).

## 4. Owners

Every owner in the document is a service code of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`
(ASM-3285). No owner is taken from the story masters, and no owner is a team type or a person. Where the source
names a component that the map does not own (the codec server, the guard library), the document names the platform epic
`RWB-PLT-WF` or the platform contract story, and the gap row carries the open point.

## 5. Registers

- Gap rows written: **8** candidate rows, `GAP-2035` to `GAP-2042`, in `_work/msr/gaps/B-TECH-08.jsonl`
  (1 Outdated, 1 Conflict, 3 Ambiguous, 3 Missing; 2 of severity P2 and 6 of P3).
- Assumption rows written: **13** candidate rows, `ASM-3275` to `ASM-3287`, in
  `_work/msr/assumptions/B-TECH-08.jsonl` (11 High, 2 Medium).
- Every gap row names its assumption, every assumption names its gap where it has one, and every citation in the document
  resolves to a row: the document cites CG-1 to CG-8 and ASM-1 to ASM-9.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-08 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

`verify.py` reports PASS: header lines 1 and 2 present, the D-RCV-60 change-log row present, 0 unexplained missing lines of
version 4, sections 1 to 11 in order, 6 subsections, 18 tables, and 0 unresolved CG/ASM citations. C12 finds no person
name and no email address in the files of this WP; C13 finds no issue-tracker reference; C18 finds no write outside the
"Write only" list and no change to a story master. The v4 document is unchanged on disk.

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded for this run (ASM-3283). No later lifecycle stage was
started. No issue tracker, wiki, repository, Figma or web call was made, and no commit was created. No other document of
the family was touched.
