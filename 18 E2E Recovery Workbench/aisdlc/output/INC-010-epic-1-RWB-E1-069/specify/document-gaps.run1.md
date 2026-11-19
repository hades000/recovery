# Document gaps — INC-010-epic-1-RWB-E1-069 (Technical Specifier, 2026-11-17)

Source tags (S1–S15, C1–C3, E1, R1, T1) are defined in `spec.md` § Sources.

Precedence is the RUN-BRIEF order: D-RCV-35/36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts.

The README items "Decisions taken while setting this up" 1–7 are cited where they apply and are not re-reported.

There are no blockers. All 21 gaps are Blocker = No.

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
- **Why:** Section A (AC1, AC2, AC4–AC8) does not depend on it. BR9 and §13 step 7 define the default: Section B waits and its features stay behind their flags.
- **How this stage proceeded:** Section B is specified in full (SPEC-005/006), with its merge gated on RWB-ACE-001. Locally, `infra/postgres/schema/02-ace-tier2-probe.sql` (`RWB_ACE_TIER2_PROBE=true`) stands in, as [R1] "Local vs target" records.

## Other gaps

**DG-L01. Extension tables: which file creates them.**
- **Document:** [S1] Story RWB-E1-069 v1, AC1, AC7 Given, §12, §13 build step 1.
- **Gap or conflict:** These sections place the four extension tables in V0002.
- **Second source:**
  - [S1] §4 step 1 says they ship "in V0001 ... this story verifies them rather than creating them". The increment card says the same.
  - [S5] RWB-E1-001 v1: V0001 creates 92 tables, the extension tables among them.
  - [S3] header: "V0001 tables and dictionary".
  - [S9] D-RCV-35 §8.2 says E1-069 "carries" them, but names no file.
- **Blocker?** No.
- **Why:** The tables cannot be created twice. Both story files and the physical schema agree on V0001, and D-RCV-35 names no file, so it does not decide the question.
- **How this stage proceeded:** E1-069 verifies the tables and does not create them (SPEC-007, SPEC-011).

**DG-L02. Helper functions: V0001 or the Section A file.**
- **Document:** [S1] §3 and the AC Background: V0001 created the three helper functions.
- **Gap or conflict:** [S1] §4 step 1 and §13 put "the three helper functions" in V0002.
- **Second source:**
  - [S5] RWB-E1-001 v1 does not mention the functions.
  - [S3] places them at lines 6141–6198, inside the views part ("V0002 Tier 1 views").
  - [S2] lines 31–86.
- **Blocker?** No.
- **Why:** `CREATE OR REPLACE` is idempotent, so both readings are satisfied.
- **How this stage proceeded:** The Section A file carries them with `CREATE OR REPLACE` (SPEC-002).

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
- **How this stage proceeded:** A lint exception scoped to `rwb_e1_069` only (SPEC-014). `recovery.` literals still fail.

**DG-L04. Migration sequence numbers.**
- **Document:** [S1] names the files `V0002` and `V0003`.
- **Gap or conflict:** [S10] D-RCV-28 takes `<seq>` in merge order. The D-RCV-34 map (E1-042 V0001/V0002, E1-001 V0003) follows Build Sequence v4 and is stale against [S14] v6 (E1-001 is order 9, E1-069 order 10).
- **Second source:** [S10] D-RCV-34; [S14] rows 9–10.
- **Blocker?** No.
- **Why:** D-RCV-28's merge-order rule is a documented default.
- **How this stage proceeded:** The files are named by role, with `<seq>` = next free at merge (SPEC-001/005).

**DG-L05. Dictionary totals.**
- **Document:** [S1] AC5 gives 122 objects and 1,366 fields.
- **Gap or conflict:** [S3] seeds 123 and 1,379. This is [R1] decision 7, cited and not re-reported.
- **Second source:** [S6] RWB-E1-001 Specification Rulings v2, §10 step 2; [S9] (122/1,366).
- **Blocker?** No.
- **Why:** The totals belong to V0001, which is RWB-E1-001.
- **How this stage proceeded:** The totals are marked INHERITED. E1-069 asserts 30/304/177/127 and 49 DF-EXT fields (SPEC-010).

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
- **Why:** It is the ACE team's story. E1-069 grants the 21 Tier 1 tables itself ([S1] §12).
- **How this stage proceeded:** Recorded. A proposed open item is raised.

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
- **Gap or conflict:** [S1] BR3 limits the rule to "no write on a view". The DML on Workbench tables is granted by V0001.
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
- **Gap or conflict:** PostgreSQL requires the new owner to hold CREATE on the schema for `ALTER VIEW ... OWNER`. This is an implementation constraint. The local `20-grants.sql.inc` comment says "CREATE is needed to own the views".
- **Second source:** `infra/postgres/init/20-grants.sql.inc`.
- **Blocker?** No.
- **Why:** A transient grant satisfies both.
- **How this stage proceeded:** CREATE is granted, the owner is changed, and CREATE is revoked in the same file (SPEC-004 steps 3 and 7). A test asserts the end state.

**DG-L13. Revoking USAGE on schema `public` from PUBLIC.**
- **Document:** [S1] AC2 expects "permission denied for schema public".
- **Gap or conflict:** That message needs USAGE on `public` revoked from PUBLIC. The [S1] §12 grant block does not revoke it, and ACE owns `public`.
- **Second source:** [S4] §12 step 4 ("REVOKE from PUBLIC"); [S12] line 64 ("PUBLIC is revoked").
- **Blocker?** No.
- **Why:** The ACE DBA owns this. SQLSTATE 42501 is asserted in every case.
- **How this stage proceeded:** Treated as an ACE DBA precondition. Locally, `20-grants.sql.inc` provides it. A proposed open item is raised.

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
- **Document:** [S1] §3 requires V0001 (RWB-E1-001) and the RWB-TE-001 module map.
- **Gap or conflict:** INC-009 (E1-001) is "Ready for specify" and not built. `recovery-modules.yaml` is absent: `backend/src/test/resources/architecture/` is empty (E1 A-02).
- **Second source:** `aisdlc/docs/increments/INDEX.md` rows 002 and 009; E1 A-02.
- **Blocker?** No.
- **Why:** Build order ([S14]) puts E1-001 first. ASM-006 sets the default for the map.
- **How this stage proceeded:** Build-order dependency. The plan must not start the build before V0001 exists.

**DG-L18. Who delivers V0001–V0003.**
- **Document:** [R1] "Local vs target" says "Flyway V0001-V0003 from RWB-E1-001".
- **Gap or conflict:** [S1] and [S5] say E1-001 delivers V0001 only, and V0002 and V0003 belong to E1-069.
- **Second source:** [S5]; [S1] §12.
- **Blocker?** No.
- **Why:** The story file v7 governs.
- **How this stage proceeded:** Recorded for the README owner. A proposed DOCUMENT-GAPS row is raised.

**DG-L19. Overlap with the RWB-TE-001 spec.**
- **Document:** T1 RWB-TE-001 v2 spec, SPEC-RWB-TE-001-021, specifies BND-6 with the 30-view list.
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
