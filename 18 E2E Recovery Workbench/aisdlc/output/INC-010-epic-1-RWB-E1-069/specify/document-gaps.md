# Document gaps — INC-010-epic-1-RWB-E1-069 (Technical Specifier, remediation run 3, spec revision run 4, 2026-11-18)

Run 1 is kept as `document-gaps.run1.md`, run 2 as `document-gaps.run2.md` and run 3 as `document-gaps.run3.md`. Run 4 updates DG-L19 (RWB-TE-001 re-baselined on v4, REVIEW-123) and DG-L29 (OI-069-A scope, REVIEW-124), and adds no gap (spec gate round 3, `../review/spec-gate-review-3.md`).

Source tags (S1–S19, C1–C3, E1, E2, R1, T1–T3) are defined in `spec.md` § Sources.

Precedence is the RUN-BRIEF order: D-RCV-35/36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts.

The README items "Decisions taken while setting this up" 1–7 are cited where they apply and are not re-reported.

There are no blockers. All 30 gaps are Blocker = No.

## External dependency

**DG-L16. RWB-ACE-001 (ACE team), external dependency, Section B.**
- **Document:** [S1] Story RWB-E1-069 v1, header "Depends on", §3, BR9.
- **Gap or conflict:** Section B (AC3) depends on the ACE team's RWB-ACE-001 being deployed in DEV and SIT. The work is outside the recovery squad's control. RWB-ACE-001 provides:
  - 14 Tier 2 tables;
  - 12 columns on `account`, `customer` and `efs_action`;
  - SELECT on the Tier 2 tables for `ace_view_owner`;
  - REVOKE from PUBLIC.
- **Second source:**
  - [S4] RWB-ACE-001: `V027__rwb_ace_001_recovery_source_additions.sql` at ACE head V026; flow step 5 is the grant.
  - [S8] Decision Log v10, DL43: answered "Yes - scope and dates as in RWB-ACE-001"; owner is the ACE team lead; needed by 2026-11-21.
  - `aisdlc/docs/open-items.md` OPEN-032.
- **Blocker?** No.
- **Why:** Section A (AC1, AC2, AC4–AC8) does not depend on it. BR9 and §13 step 7 define the default: Section B waits and its features stay behind their flags. The local Tier 2 probe (`02-ace-tier2-probe.sql`) with its grant stand-in is the recorded stand-in, not a replacement of the dependency.
- **How this stage proceeded:** Section B is specified in full (SPEC-005/006), with its merge gated on RWB-ACE-001. Locally, `infra/postgres/schema/02-ace-tier2-probe.sql` (`RWB_ACE_TIER2_PROBE=true`) stands in, as [R1] "Local vs target" records. This gap is re-confirmed in run 3: the dependency is recorded, Blocker = No, and the probe stand-in is the local evidence only.

## Other gaps

**DG-L01. Extension tables: which file creates them.**
- **Document:** [S1] Story RWB-E1-069 v1, AC1, AC7 Given, §12, §13 build step 1.
- **Gap or conflict:** These sections place the four extension tables in the second file (the story calls it V0002).
- **Second source:**
  - [S1] §4 step 1 says they ship "in V0001 ... this story verifies them rather than creating them". The increment card says the same.
  - [S5] RWB-E1-001 v1: the RWB-E1-001 migration creates 92 tables, the extension tables among them.
  - [S3] header: "V0001 tables and dictionary".
  - [S9] D-RCV-35 §8.2 says E1-069 "carries" them, but names no file.
- **Blocker?** No.
- **Why:** The tables cannot be created twice. Both story files and the physical schema agree on the RWB-E1-001 file, and D-RCV-35 names no file, so it does not decide the question.
- **How this stage proceeded:** E1-069 verifies the tables and does not create them (SPEC-007, SPEC-011).

**DG-L02. Helper functions: the RWB-E1-001 migration or the Section A file.**
- **Document:** [S1] §3 and the AC Background: the RWB-E1-001 migration created the three helper functions.
- **Gap or conflict:** [S1] §4 step 1 and §13 put "the three helper functions" in the Section A file (the story calls it V0002).
- **Second source:**
  - [T2] RWB-E1-001 spec Revision 4, table T6: the `v_ace_*` views and the three helpers are "Not carried. RWB-E1-069 owns them".
  - [S5] RWB-E1-001 v1 does not mention the functions.
  - [S3] places them at lines 6141–6198, inside the views part ("V0002 Tier 1 views" in the file's own comment).
  - [S2] lines 31–86.
- **Blocker?** No.
- **Why:** `CREATE OR REPLACE` is idempotent, so both readings are satisfied.
- **How this stage proceeded:** The Section A file creates them with `CREATE OR REPLACE` (SPEC-002). Since [T2] Revision 4 T6, the Section A file is the only creator; `ace_to_date` follows BR6, not the [S2] body (DG-L23).

**DG-L03. The Section A and B files break the D-RCV-28 lint rules.**
- **Document:** [S10] D-RCV-28 requires at most one non-fix file per story key and only the `${recoverySchema}` qualifier. C2 BS-2.2, BS-2.5 ("Recovery migrations contain no GRANT/REVOKE") and BS-2.6 say the same. `RecoveryMigrationLintTest` enforces all of it.
- **Gap or conflict:** E1-069 must ship two files, with `public.` qualifiers and grants.
- **Second source:**
  - [S9] D-RCV-35 §3.2 and §8.2 (two migrations; the grant and the revoke).
  - [S7] ADR-010 (30 views in two migrations).
  - [S1] §12.
  - BS-2.5 itself says the view grants "live in the view story".
  - Source D-RCV-28 (Decision Log v10) lacks the one-file-per-key clause.
- **Blocker?** No.
- **Why:** D-RCV-35 ranks above D-RCV-28 and the standards.
- **How this stage proceeded:** Through the two seams RWB-E1-044 hands to E1-069 ([T3] v14-7 SPEC-016). SEAM-E044-01 admits `public` only inside `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*` (orchestrator triage). SEAM-E044-02 admits two named files and recovery-side GRANT/REVOKE for key `rwb_e1_069` only (SPEC-014). `recovery.` literals still fail.

**DG-L04. Migration sequence numbers.**
- **Document:** [S1] names the files `V0002` and `V0003`.
- **Gap or conflict:** [S10] D-RCV-28 takes `<seq>` in merge order. The D-RCV-34 map (which calls E1-042's files V0001/V0002 and E1-001's V0003) follows Build Sequence v4 and is stale against [S14] v6 (E1-001 is order 9, E1-069 order 10).
- **Second source:** [S10] D-RCV-34; [S14] rows 9–10.
- **Blocker?** No.
- **Why:** D-RCV-28's merge-order rule is a documented default.
- **How this stage proceeded:** The files are named by role, with `<seq>` = next free at merge (SPEC-001/005).

**DG-L05. Dictionary totals.**
- **Document:** [S1] Story RWB-E1-069 v1 AC5 and §16 TC-05: 122 objects, 1,366 fields, 1,062 table fields. [S16] Data Classification Inventory v4 header: "1366 fields in 122 entities".
- **Gap or conflict:** [S3] Physical Schema v6 seeds 123 `sys_objects` rows and 1,379 `sys_fields` rows (1,075 on tables, 49 of them on extension tables; 304 on views). The RWB-E1-001 spec Revision 4 counting table reproduces both sets and adds three provisional field rows DF-REF-300..302 for the columns RWB-E1-042 adds to `parameter_value` (ASM-E1001-17), so the file seeds **1,382** fields and **1,078** table fields. [R1] decision 7 notes the difference.
- **Second source:** [S17] D-RCV-36 change register row 18 (Physical Schema v6 replaces v5) and A.7 (v6 holds 93 tables); [T2] Revision 4 SPEC-006, ASM-E1001-01, ASM-E1001-17 (the RWB-E1-001 file seeds v6 plus the three rows); [S6] §10 step 2; [S9] (122/1,366).
- **Blocker?** No.
- **Why:** D-RCV-36 is tier 1 under the RUN-BRIEF precedence, above story files v7, and the RWB-E1-001 migration seeds [S3] plus the three provisional rows.
- **How this stage proceeded:** Run 3 (REVIEW-118(5), -109): the test asserts 123 / 1,382 / 1,078 / 49 (and the view counts 30 / 304 / 177 / 127), citing both value sets and naming the three provisional rows (SPEC-010). If the RWB-E1-001 file ships other totals after its gate, the test asserts what that file seeds. Proposed open item OI-069-K asks the story owner to align AC5 and TC-05.

**DG-L06. Extension-table names.**
- **Document:** C1 backend-context §4.2 names `party_ext, collateral_ext, case_account_ext, asset_ext`.
- **Gap or conflict:** [S1] §13 and [S3] lines 2087–2154 name `party_ext, contact_point_ext, account_ext, valuation_ext`.
- **Second source:** [S1] AC7; OPEN-033.
- **Blocker?** No.
- **Why:** The story file v7 and the physical schema outrank a context file.
- **How this stage proceeded:** The spec uses the story names.

**DG-L07. RWB-ACE-001 Appendix A mapping.**
- **Document:** [S4] RWB-ACE-001 Appendix A maps the 12 new columns into Section A view columns, for example `v_ace_account.business_unit`, `v_ace_account.bucket` and `v_ace_customer.segment`.
- **Gap or conflict:** These columns are not in [S2] Section A or in the 177-field list.
- **Second source:** [S2] A1, A3, A9; [S1] §11; [S1] §19 (the 30-view list is frozen).
- **Blocker?** No.
- **Why:** Story §19 sends any change to the data architect and the recovery tech lead.
- **How this stage proceeded:** The [S2] bodies are kept verbatim. A proposed open item is raised.

**DG-L08. RWB-ACE-001 AC4 scope of the SELECT grant.**
- **Document:** [S4] RWB-ACE-001 AC4: SELECT on the 14 new tables "and no other table".
- **Gap or conflict:** [S4] §10 and §12 step 4 grant SELECT on the "21 listed tables" and REVOKE from PUBLIC.
- **Second source:** [S4] §10, §12.
- **Blocker?** No.
- **Why:** It is the ACE team's story.
- **How this stage proceeded:** Recorded. A proposed open item is raised. Run 2: E1-069 no longer grants the Tier 1 tables itself; the ACE DBA does (DG-L22).

**DG-L09. Who creates the roles.**
- **Document:** [S12] Environment and Deployment Design v4, line 124: the Section A migration "creates or confirms" the roles.
- **Gap or conflict:** [S1] §3 says the roles already exist and the Section A migration does not create them.
- **Second source:** [S1] §3, AC Background.
- **Blocker?** No.
- **Why:** The story file v7 outranks the Environment and Deployment Design.
- **How this stage proceeded:** The migration creates no role. Locally, `00-roles-and-databases.sh` creates them.

**DG-L10. Write rules for `recovery_svc`.**
- **Document:**
  - [S12] line 124: `recovery_svc` has SELECT on the views "and nothing else".
  - [S12] line 126 and [S13] line 219 (Security and Access Design v4): it cannot write "any public or recovery table".
  - [S2] line 737 says the same.
- **Gap or conflict:** [S1] BR3 limits the rule to "no write on a view". The DML on Workbench tables is granted by the RWB-E1-001 migration.
- **Second source:** [S1] BR3; [S11] Build Notes Epic 1 v6, grants table.
- **Blocker?** No.
- **Why:** The story and the build notes outrank the older design wording. ADR-010's "nothing else" is about ACE data.
- **How this stage proceeded:** Conformance check 4 follows BR3 (SPEC-008).

**DG-L11. Grant on all tables in the recovery schema.**
- **Document:** [S2] lines 718–732 and [S3] lines 6828–6840 (both commented out) grant SELECT `ON ALL TABLES IN SCHEMA recovery`.
- **Gap or conflict:** [S1] §12 says "never GRANT SELECT ON ALL TABLES".
- **Second source:** [S1] §12.
- **Blocker?** No.
- **Why:** The story governs.
- **How this stage proceeded:** One grant per view (SPEC-004).

**DG-L12. BR2 against the PostgreSQL ownership rule.**
- **Document:** [S1] BR2: `ace_view_owner` holds "no right in schema recovery".
- **Gap or conflict:** PostgreSQL requires the new owner to hold CREATE on the schema for `ALTER VIEW ... OWNER`, and the migration account needs USAGE and CREATE transiently on `recovery` to make that grant and revoke it. This is an implementation constraint. The local `20-grants.sql.inc` comment says "CREATE is needed to own the views".
- **Second source:** `infra/postgres/init/20-grants.sql.inc`.
- **Blocker?** No.
- **Why:** A transient grant satisfies both.
- **How this stage proceeded:** Run 3: `USAGE, CREATE` is granted, the views are created, the SELECT grant is made while the migration account owns each view, the owner is changed, and `USAGE, CREATE` are revoked in the same file, in **both** files (SPEC-004 steps 6, 8–11; SPEC-006). PostgreSQL refuses the owner change without CREATE (`permission denied for schema recovery`) and refuses the SELECT grant after the owner change to a non-inheriting member (`permission denied for table <view>`) ([E2] run 3); the reordered steps were run end to end. SPEC-017 asserts the end state after Section B.

**DG-L13. Revoking USAGE on schema `public` from PUBLIC.**
- **Document:** [S1] AC2 expects "permission denied for schema public".
- **Gap or conflict:** That message needs USAGE on `public` revoked from PUBLIC. The [S1] §12 grant block does not revoke it, and ACE owns `public`.
- **Second source:** [S4] §12 step 4 ("REVOKE from PUBLIC"); [S12] line 64 ("PUBLIC is revoked").
- **Blocker?** No.
- **Why:** The ACE DBA owns this. SQLSTATE 42501 is asserted in every case.
- **How this stage proceeded:** Treated as ACE DBA precondition P4(d). Locally, `20-grants.sql.inc` provides it in both modes; [E2] confirmed the exact text `permission denied for schema public`. OI-069-A.

**DG-L14. PostgreSQL version.**
- **Document:** [S1] §16 TC-E1-069-01 uses a "PostgreSQL 17 container".
- **Gap or conflict:** C2 BS-2.9, C3 and `docker-compose.yml` (`postgres:16.16-alpine`) use PostgreSQL 16.
- **Second source:** C2 BS-2.9; C3.
- **Blocker?** No.
- **Why:** The local standard applies, and the views use no feature specific to PostgreSQL 17.
- **How this stage proceeded:** The tests use PostgreSQL 16.

**DG-L15. Migration folder.**
- **Document:** [S1] §13 gives `ace-service/src/main/resources/db/migration/recovery`.
- **Gap or conflict:** The local folder is `backend/src/main/resources/db/modulemigration/recovery/`.
- **Second source:** C2 BS-2.3; `RecoveryFlywayConfig`; RUN-BRIEF "Local stack facts".
- **Blocker?** No.
- **Why:** RUN-BRIEF maps the ACE paths to this repository.
- **How this stage proceeded:** The local path is used.

**DG-L17. Preconditions missing locally.**
- **Document:** [S1] §3 requires the RWB-E1-001 migration and the RWB-TE-001 module map. Run 3: both are earlier stories in [S14] (orders 9 and 2), so they are dependencies, not things E1-069 creates (ASM-006; D-RUN-08).
- **Gap or conflict:** INC-009 (E1-001) is "Ready for specify" and not built. `recovery-modules.yaml` is absent: `backend/src/test/resources/architecture/` is empty (E1 A-02).
- **Second source:** `aisdlc/docs/increments/INDEX.md` rows 002 and 009; E1 A-02.
- **Blocker?** No.
- **Why:** Build order ([S14]) puts E1-001 first. ASM-006 sets the default for the map.
- **How this stage proceeded:** Build-order dependency. The plan must not start the build before the RWB-E1-001 migration exists.

**DG-L18. Who delivers the three migration files.**
- **Document:** [R1] "Local vs target" says "Flyway V0001-V0003 from RWB-E1-001" (quoted: the README's own naming).
- **Gap or conflict:** [S1] and [S5] say E1-001 delivers its own file only, and the two view files (called V0002 and V0003 in the story) belong to E1-069.
- **Second source:** [S5]; [S1] §12.
- **Blocker?** No.
- **Why:** The story file v7 governs.
- **How this stage proceeded:** Run 3: the README correction is part of SPEC-015(a), because E1-069 takes the S2 hand-over (DG-L27).

**DG-L19. Overlap with the RWB-TE-001 spec.**
- **Document:** RWB-TE-001 v2 spec, SPEC-RWB-TE-001-021, specified BND-6 with the 30-view list. Run 4: [T1] **v4** withdraws SPEC-021 to E1-069 and keeps `sourceViews` as an opaque key (SPEC-003); the overlap is resolved (run 2 recorded the same withdrawal at v3, then the live revision; REVIEW-123).
- **Gap or conflict:** [S1] §4 step 5 and §19 give BND-6 and `sourceViews` to E1-069. E1 A-02 gives "BND-6 hardening" to E1-069.
- **Second source:** E1 A-02, A-04.
- **Blocker?** No.
- **Why:** Story v7 and the audit's owner column agree.
- **How this stage proceeded:** E1-069 extends the existing rule (SPEC-012) and does not duplicate it. TE-001 keeps the rest of the map.

**DG-L20. Skipping the Section B stage.**
- **Document:** [S1] §13 step 7: the V0003 stage "is skipped" until RWB-ACE-001 is deployed.
- **Gap or conflict:** Flyway is set with `outOfOrder(false)` and one history table (`flyway_schema_history_recovery`). Under that setting a version present in the folder cannot be skipped while later versions apply, and it cannot be applied after them.
- **Second source:** C2 BS-2.3; `RecoveryFlywayConfig` (`outOfOrder(false)`); [S10] D-RCV-28 (contiguous sequence).
- **Blocker?** No.
- **Why:** BR9 ("V0003 is a later Flyway sequence") and §12 Restart ("V0003 waits") allow the merge to be gated.
- **How this stage proceeded:** The Section B file merges only after RWB-ACE-001 is deployed, and takes the next free sequence (SPEC-005). A proposed open item is raised.

**DG-L21. Name of screen SCR-44.**
- **Document:** [S1] §10 names SCR-44 "Migration runs".
- **Gap or conflict:** [S1] §15 names SCR-44 "Interface and job monitor".
- **Second source:** [S1] §15.
- **Blocker?** No.
- **Why:** No screen is in scope.
- **How this stage proceeded:** Recorded only.

## Gaps added in run 2

**DG-L22. Who grants ACE-side SELECT and USAGE to `ace_view_owner`.**
- **Document:** [S1] Story RWB-E1-069 v1 §12 grant block: `GRANT USAGE ON SCHEMA public TO ace_view_owner` and `GRANT SELECT ON public.<21 tables> TO ace_view_owner`, "run as the ACE schema owner".
- **Gap or conflict:** [S9] D-RCV-35 §8.2 puts "The SELECT grant for the recovery role on the listed tables" in RWB-ACE-001 and gives E1-069 "The grant to the recovery service identity and the revoke from PUBLIC". [S4] ACE Team Stories v1 RWB-ACE-001 flow step 5, §10 ("Selects the 21 listed tables") and §12 step 4 have the ACE DBA grant the view-owner role. [S1] §10 Authority itself gives the grant to the ACE DBA. The [T3] lint admits `public.` only inside the view statement (orchestrator triage).
- **Second source:** [S9] §8.2; [S4]; [S1] §10; [T3] SEAM-E044-01.
- **Blocker?** No.
- **Why:** D-RCV-35 is tier 1; [S1] §10 and [S4] agree with it.
- **How this stage proceeded:** The recovery migrations contain no statement on `public` (SPEC-004). The grants are ACE DBA precondition P4(d), checked by SPEC-009 and check 1, supplied locally by SPEC-015(b). OI-069-A; ASM-015.

**DG-L23. The `ace_to_date` body does not meet its own contract.**
- **Document:** [S2] ACE Source Views v1 lines 29–30 (return NULL on anything else, so a dirty source row can never break a read) and lines 31–43 (the body casts with `::date` and `to_date` without validation). [S3] Physical Schema v6 lines 6141–6157 hold the same body.
- **Gap or conflict:** On PostgreSQL 16.16 the body raises `date/time field value out of range` for `2026-02-30`, `20261345`, `31/02/2026` and `0000-01-01`, and returns `0001-01-01 BC` for `00000000` ([E2]; round-1 reviewer run). One dirty `pay_date` row would fail every read of `v_ace_payment`.
- **Second source:** [S1] BR6 ("return NULL rather than fail a read").
- **Blocker?** No.
- **Why:** BR6 and the [S2] comment state the required behaviour; only the body is defective.
- **How this stage proceeded:** SPEC-002 specifies the behaviour, not the source text; SPEC-020 tests it. ASM-012; OI-069-G to the data architect to correct [S2] and [S3].

**DG-L24. Personal-data flags in the dictionary against the classification inventory.**
- **Document:** [S3] Physical Schema v6 `sys_fields.is_personal` is true for 9 DF-ACE fields only (057, 058, 059, 066, 072, 073, 074, 078, 079).
- **Gap or conflict:** [S16] Data Classification and Personal Data Inventory v4, Fields tab, classes 250 of the 304 DF-ACE fields as personal, 12 of them Restricted. The RWB-E1-001 spec Revision 4 does not seed [S3]'s 9 flags as written: it seeds the protective union of [S3] and [S16], 526 `true` in the whole dictionary (ASM-E1001-14), which makes all 250 personal DF-ACE fields true and leaves the 54 non-personal false. The residual mismatch is therefore between the two **source documents** (9 vs 250), not between the source and the seed.
- **Second source:** [S16]; [S9] §3.3; [T2] Revision 4 SPEC-006 (the 526 union), ASM-E1001-14, GAP-E1001-18 (Blocker = Yes there for the 26 PS-v6-only fields).
- **Blocker?** No, for this story.
- **Why:** [S16] is the classification document; the dictionary flag is seeded by RWB-E1-001, not by this story, and its settled seed value (the union) already marks all 250 DF-ACE personal fields true. The ruling on the 26 PS-v6-only fields and the two staff identifiers belongs to RWB-E1-001's Blocker = Yes gap.
- **How this stage proceeded:** SPEC-019 takes [S16] as the classification of record, names the 12 Restricted fields, and asserts what that file seeds: 304 non-null, 250 true (including the 9 and all 12 Restricted), 54 false; the whole-dictionary 526 is E1-001's test. OI-069-J now asks the data architect to correct [S3]'s 9 flags to the inventory, not to change the seed.

**DG-L25. DML grants for `recovery_svc` on Workbench tables in SIT and above.**
- **Document:** [S1] BR3: its DML on the Workbench's own tables "is granted by V0001" (quoted from the story).
- **Gap or conflict:** [T2] RWB-E1-001 spec T7: the RWB-E1-001 file carries no GRANT; grants are local default privileges, and in SIT and above they are left to "the view story".
- **Second source:** [T2]; [S11] Build Notes Epic 1 v6 grants table; C2 BS-2.5.
- **Blocker?** No.
- **Why:** [S1] BR3 places the grant outside this story, and no source gives it to E1-069.
- **How this stage proceeded:** Not taken (Out of scope). OI-069-I to the recovery tech lead and RWB-E1-001.

**DG-L26. Text of the X2 message.**
- **Document:** [S1] AC3 and §5 X2: "relation public.valuation does not exist".
- **Gap or conflict:** PostgreSQL 16 writes `relation "public.valuation" does not exist`, with quotes ([E2]).
- **Second source:** [E2].
- **Blocker?** No.
- **Why:** The database text is fixed.
- **How this stage proceeded:** SPEC-018 asserts SQLSTATE 42P01 and that the message contains `public.valuation` and `does not exist`.

**DG-L27. The local switch to Flyway mode is handed over by a sibling spec.**
- **Document:** [T2] RWB-E1-001 spec **Revision 4** SPEC-010: at its merge RWB-E1-001 flips S1 `RWB_LOAD_REFERENCE_SCHEMA` to `false`, adds S2 `RWB_LOAD_REFERENCE_VIEWS` (default `true`, views-only stand-in) and S3 `RWB_FLYWAY_ENABLED`, and hands E1-069 the S2 flip (default `false`, branch deleted) when its view migrations merge. Its ASM-E1001-18 also states that on S2 `false` the schema is empty and no version-`0` baseline row is written.
- **Gap or conflict:** The run-2 spec claimed S1 as E1-069's hand-over and did not mention S2 or S3, so the two specs owned S1 twice and disagreed on `RecoveryDatabaseIT` (REVIEW-118(1)–(4)). [S1] itself has no item for the local default or for `RecoveryDatabaseIT`.
- **Second source:** [R1] "Local versus target"; `.env.example` line 14 ("set false once V0001-V0003 exist as migrations"); the code in `10-load-ace-database.sh` (S1 branch today; no S2 branch yet).
- **Blocker?** No.
- **Why:** [T2] Revision 4 is the later, gated definition of the hand-over, and the repository's own comment ties the switch to the view migrations; leaving S2 unowned would break the default start path.
- **How this stage proceeded:** Run 3 takes the hand-over as [T2] states it: S1 and S3 stay RWB-E1-001's; E1-069 flips S2 to `false`, deletes the branch, removes the baseline-row assertion from `RecoveryDatabaseIT` with the S2 stage and replaces it with SPEC-017's per-file history assertion (stronger, no coverage lost). The one wording difference from [T2] ("no assertion removed") is DG-L30. Add-on debt: the open item OI-069-D and the shared update carry the README change.

**DG-L28. `sourceViews` lists 30 names before the Section B file exists.**
- **Document:** [S1] §4 step 5 adds the 30 names at once, before the Section B file (steps 6–7).
- **Gap or conflict:** [S1] BR9 and [S9] §3.2 (Section B ships the week RWB-ACE-001 lands) put the Section B file later, so a set-equality test between the list and the migrated views fails in the window between merges (REVIEW-106).
- **Second source:** [S1] BR9; [S9] §3.2.
- **Blocker?** No.
- **Why:** [S1] §4 step 5 governs the list content; the test rule is design.
- **How this stage proceeded:** SPEC-013 keeps 30 names, split by section, with rules that hold in both states.

## Gaps added in run 3

**DG-L29. The migration account's rights for the ACE views: two specs disagree.**
- **Document:** [T3] RWB-E1-044 spec **v14-3** SPEC-017 and T-044-17: the recovery migration account is declined the ACE DBA role, "any privilege in `public` or membership of `ace_view_owner`", and T-044-17 asserts `has_schema_privilege('rwb_migrator','public','USAGE')` is false. Its OI-E044-I says the question must be resolved before RWB-E1-069 is specified and that E1-069 must not treat the role as delivered by E1-044 (D-RUN-08).
- **Gap or conflict:** The run-2 E1-069 spec (P4(a)–(b), SPEC-015(b)) required the same account to hold USAGE on `public` and membership of `ace_view_owner`, which would turn T-044-17 red. Story RWB-E1-069 §3 ("the ACE DBA role ... (RWB-E1-044)") is the lower-precedence source on this point.
- **Second source:** [T3] v14-3 (as above); [S9] D-RCV-35 U3/U4 and §8.2 ("Recovery squad: Reads the views only; has no grant on a public table" in [S4]); [S7] ADR-010; story [S1] §10 (the ACE DBA makes the table grants).
- **Blocker?** No.
- **Why:** Orchestrator decision D-RUN-14 ([S19], 2026-11-18T00:31) settles it: `rwb_migrator` gets exactly `USAGE ON SCHEMA public` with no table privilege and `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE`, never the ACE DBA role, SELECT on a `public` table or an inheriting membership; the SELECT grants to `ace_view_owner` stay with the ACE DBA. [T3] **v14-7** (review-7 PASS) has since applied D-RUN-14 in its SPEC-017 and T-044-17, so the two specs now agree. D-RUN-14 is an AI orchestrator decision whose ratification is open (OI-069-M, proposed OPEN-051); no human approval is claimed.
- **How this stage proceeded:** E1-069 applies D-RUN-14 as P4(a)–(b) and SPEC-004/SPEC-008 check 5; it does not restate the two rights (T3 v14-7 delivers them in the local init) and does not weaken T-044-17. [E2] run 3 proves the rights are sufficient: with USAGE on `public` and no table privilege, `CREATE VIEW ... FROM public.<table>` succeeds, `ALTER VIEW ... OWNER TO ace_view_owner` succeeds under `INHERIT FALSE, SET TRUE`, and `recovery_svc` reads the view; the per-view SELECT grant must be made before the owner change. The run-2 sequence's last statement (`REVOKE ALL ON ALL TABLES ... FROM PUBLIC`) was also found to fail once a view is owned by `ace_view_owner`, so it moves to the top of the Section A file and is omitted from Section B (SPEC-004 step 1, SPEC-006). **Open-item split (REVIEW-124):** OI-069-A carries only P4(c)–(d); who applies P4(a)–(b) in SIT, UAT and PROD remains [T3] v14-7 OI-E044-I, which this story neither answers nor claims. OI-069-M, OPEN-035.

**DG-L30. The E1-001 hand-over on the baseline row and the seed counts.**
- **Document:** [T2] RWB-E1-001 spec **Revision 4** SPEC-010 hand-off and ASM-E1001-18: E1-069 flips S2 to `false`, deletes the branch and runs the `RecoveryDatabaseIT` view and grant assertions on Flyway-created views, while this story "keeps it in the S2 stage (`ASM-E1001-18`)" and "E1-069 keeps it in the same stage". ASM-E1001-18 also says "On an empty schema (S2 `false`) no baseline row is written" and "no assertion removed".
- **Gap or conflict:** With S2 `false` the stage in which the version-`0` baseline row exists is gone, so the assertion cannot be kept as it stands; the run-2 E1-069 spec said it was "replaced" without naming S2 (REVIEW-118(4)). The same revision seeds 1,382 `sys_fields` and 1,078 table fields (ASM-E1001-17) and 526 `is_personal` (ASM-E1001-14), against the run-2 spec's 1,379 / 1,075 / 9 DF-ACE premise (REVIEW-118(5)–(6)).
- **Second source:** [T2] Revision 4 SPEC-006, ASM-E1001-14, -17, -18, GAP-E1001-18; [S3] Physical Schema v6 (1,379 / 1,075 / 9); [S16] (250 personal DF-ACE fields).
- **Blocker?** No.
- **Why:** The later, gated sibling spec defines the seed values and the S2 mechanism; the consequence of S2 `false` (empty schema, no baseline row) follows from `RecoveryFlywayConfig` (`baselineOnMigrate(true)`, `baselineVersion("0")`) and Flyway's rule that a baseline is written only to a non-empty schema. E1-069 asserts what the RWB-E1-001 file seeds, which is the rule both specs already state.
- **How this stage proceeded:** SPEC-017 asserts no `version = '0'` row and one success row per applied file, which is stronger than the baseline row; SPEC-010 asserts 123 / 1,382 / 1,078 / 49; SPEC-019 asserts 250 true / 54 false among the 304 view fields and leaves the 526 union to [T2]. The wording difference ("no assertion removed") is carried in OI-069-L and the shared update so the RWB-E1-001 owner can accept it at plan time.

## Spec gate

Round 1 (`../review/spec-gate-review.md`): FAIL, with 0 Critical, 3 High, 6 Medium and 7 Low findings. Each finding is answered in `gate-response.md` (Round 1). Round 2 (`../review/spec-gate-review-2.md`): FAIL, with 0 Critical, 1 High, 1 Medium and 3 Low (REVIEW-117..121); each is answered in `gate-response.md` (Round 2). Round 3 (`../review/spec-gate-review-3.md`): FAIL, Low-only, 0 Critical, 0 High, 0 Medium and 3 Low (REVIEW-122..124); each is answered in `gate-response.md` (Round 3), with no new gap and no change to any Blocker value. The orchestrator runs round 4 as `../review/spec-gate-review-4.md`.
