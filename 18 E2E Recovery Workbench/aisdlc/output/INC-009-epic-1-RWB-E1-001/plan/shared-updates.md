# Shared updates proposed: RWB-E1-001 plan

RUN_ID `INC-009-epic-1-RWB-E1-001`, stage `plan`, 18 November 2026, run 1. RUN-BRIEF rule 3: this stage
**edited no shared file**. The orchestrator applies these rows in order and assigns the next free IDs.
The spec stage's `../specify/shared-updates.md` (revision 4) stands and is not repeated; this file adds
only what the plan stage needs. No row is a human approval, and no row ratifies D-RUN-12/-18/-21.
`GAP-E1001-17` and `GAP-E1001-18` remain **Blocker = Yes**.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

| Change | Row |
|---|---|
| §3 Story trace, row 009 (`RWB-E1-001`) status | Replace the spec-stage text with: "Planned — plan v1 (18 Nov 2026; `output/INC-009-epic-1-RWB-E1-001/plan/plan.md`, `tasks.md`, `data-model.md`, `contracts/*`, `tests/scenarios.md`); plan gate pending. Spec revision 4 passed its gate round 4 (PASS 0/0/0/0) on 18 Nov 2026. Build not started. **Two Blocker = Yes gaps remain open** (`GAP-E1001-17`, `GAP-E1001-18`; human ruling required before the merge of the migration)" |
| Plan trace for `BR-RWB-013` / `FR-RWB-013` | `BR-RWB-013` / `FR-RWB-013` → SPEC-RWB-E1-001-001..010, 012..019 (011 retired) → TASK-00..TASK-19 (`plan/tasks.md`) → tests TC-E1-001-01..-20 plus T-E1001-01..-33 (`plan/tests/scenarios.md`) → code pending, branch cut after RWB-TE-001, RWB-E1-044, RWB-E1-042 and RWB-E1-043 merge |
| Migration trace | `FR-RWB-013` → `V<seq>__rwb_e1_001_recovery_schema.sql` (`backend/src/main/resources/db/modulemigration/recovery/`); `<seq>` assigned at merge (D-RUN-07); **record the assigned number here once the orchestrator sets it** |
| Dictionary and catalog trace | `REQ-RDF-001` → the migration's 123 `sys_objects` / 1,382 `sys_fields` / 14 `data_product` / `v_data_dictionary` → `backend/src/main/resources/config/parameter-catalog.csv` (two rows) → tests T-E1001-01..-33 |
| NFR trace | NFR-RWB-005, -006, -008, -009 → SPEC-007, -008, -016, -017, -018 → TASK-05, TASK-09, TASK-13, TASK-14, TASK-18 |
| Blockers | The two spec contradictions stay recorded; no trace row is claimed as resolved by an AI decision |

## 2. `aisdlc/docs/increments/INC-009-epic-1-RWB-E1-001.md` and `INDEX.md`

| File | Change |
|---|---|
| The increment card, Status | "Planned — plan v1 (18 Nov 2026; `plan/plan.md`, `plan/tasks.md`, `plan/data-model.md`, `plan/contracts/*`, `plan/tests/scenarios.md`); plan gate pending; spec revision 4 passed round 4 (0/0/0/0). Two Blocker = Yes gaps (GAP-E1001-17, GAP-E1001-18) still need a human ruling before the merge of the migration" |
| The increment card, files table (if it carries one) | Add `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_001_recovery_schema.sql`; `backend/src/main/resources/config/parameter-catalog.csv` (two rows); the P1 `dataengine/internal/catalog/**` files; the additive `access/internal/FixedMessageCatalog.java`; `application.yaml` and `application-local.yaml`; `infra/postgres/init/10-load-ace-database.sh`; `docker-compose.yml`; `.env.example`; `README.md`; the migration-folder `README.md` |
| `aisdlc/docs/increments/INDEX.md`, row 009 | "Planned" instead of "Specified (rev 4)"; keep the note that the two Blocker = Yes gaps are open and the merge needs a human ruling |

## 3. `aisdlc/DOCUMENT-GAPS.md` (candidate rows)

The plan stage's full evidence is in `plan/document-gaps.md`. The two blockers are carried unchanged.

| Local ID | Document (name, version, section) | Gap or conflict | Second source | Blocker? | Why | How the plan proceeded |
|---|---|---|---|---|---|---|
| GAP-E1001-17 (existing) | Story v7 §13 | DP07 is 139 characters for `varchar(120)` | PS v6 line 820; LDM v8 line 561 | **Yes** | No precedence rule yields a text that fits and passes BR3 | `ASM-E1001-13`; TASK-03; TASK-19 gates the merge |
| GAP-E1001-18 (existing) | PS v6 `sys_fields.is_personal` | 18 vs 523 personal; 9 Restricted unmarked; 26 fields with no Inventory row | PDPA v4; Design v2 line 31 | **Yes** | Classification is a human decision; the pointer would remove 4 marks and has no row for 26 | `ASM-E1001-14`; TASK-03; TASK-19 gates the merge |
| `PG-E1001-01` | Spec revision 4 SPEC-015 | The prose names `RowCheckFailure(messageCode, placeholders, column)`; the live E1-043 record is `(row, column, messageCode, placeholders)` | E1-043 spec revision 10 "Reference load handler" | No | The live SPI is the compile contract; no behaviour change | `plan.md` § "Handler design"; the live signatures are in `contracts/backend-apis.json` |
| `PG-E1001-02` | Spec revision 4 field matrix | `data_product.updated_by` cannot be written: `apply` carries no actor | E1-043 rev 10 SPI; `reference_version.approver_user_id` | No | The approval audit is intact in E1-043; the column is nullable and carries no decision | `updated_at` written, `updated_by` NULL; record in TASK-18 |
| `PG-E1001-03` | E1-042 plan v2; spec SPEC-019 item 5 | The two rows have defaults but no `parameter_value` row; if E1-042's rule requires one, the build fails | E1-042 plan v2; `ParameterService` default; E1-043 SPEC-027 | No | A test-scope gate owned by E1-042; a default-only key is a normal shape | TASK-00 confirms; if it differs, stop and report |
| `PG-E1001-04` | `10-load-ace-database.sh`; spec SPEC-010 S2 | The view section has no stable line number and the PS v6 file is read-only | PS v6 line 6132 marker; RUN-BRIEF rule 1 | No | A marker is a documented, testable start point; a line number would break silently | TASK-13 extracts from the marker; a missing marker fails loudly |
| `PG-E1001-05` | E1-043 plan A-08; spec SPEC-016 | The approve path needs Reference data A, held by no PS v6 role | PS v6 permission seed; API v4 approve line 3214 | No | E1-043 merges earlier and states the interim A row and a synthetic approver fixture | TASK-00 confirms; TASK-14 uses it; no bypass |
| `PG-E1001-06` | Spec SPEC-010; E1-042/E1-043 ITs | Their S1=`true` containers meet this migration after the merge; no Flyway `target` property exists | E1-044 `RecoveryMigrationProperties.Flyway` (no target); OPEN-NEW-9 | No | A coordination edit with no assertion change | TASK-16 moves them to S1=`false` (S2 per their needs) and records each change |

## 4. `aisdlc/docs/open-items.md`

| Change | Row |
|---|---|
| Keep OPEN-NEW-6 open and blocking | "**Blocker (human ruling).** Rule on DP07: widen `data_product.system_of_record` and DF-REF-074 (and LDM v8 line 561) or shorten the Story v7 §13 text to ≤ 120. RWB-E1-001 plan v1 (18 Nov 2026) implements `varchar(200)` with the text verbatim and **TASK-19 forbids the merge without this ruling**. Owner: data architect. Needed by: before the merge of the RWB-E1-001 migration." |
| Keep OPEN-NEW-7 open and blocking | "**Blocker (human ruling).** Rule on `sys_fields.is_personal`: PS v6 (18) vs PDPA Inventory v4 (523), the 26 PS-v6-only fields (DF-REF-274..299, incl. DF-REF-288/-289), and the governed path. RWB-E1-001 plan v1 seeds the 526 union as INSERT literals; **TASK-19 forbids the merge without this ruling**. Owner: data architect with the DPO (Compliance). Needed by: before the merge." |
| Update OPEN-NEW-9 (local switch coordination) | Add: "RWB-E1-001 plan v1 supplies S1 `false`, S2 `true` (the PS v6 view section from the marker `-- ACE source views. Section A ships as V0002; Section B ships after RWB-ACE-001.`, preceded by `SET search_path TO recovery;`) and S3 `${RWB_FLYWAY_ENABLED:true}`. E1-042's TC-E1-042-14 and E1-043's PS v6 baseline IT are moved to S1 `false` with S2 set to what their assertions require, no assertion removed (plan TASK-16). E1-069 still owns flipping S2 and deleting the branch." |
| Update OPEN-NEW-10 (access log) | Add: "RWB-E1-001 plan v1 asserts one REFUSED `event=REFERENCE_LOAD_AUDIT` line in its `DataProductCatalogLoadIT`; the persistent AC-DENY entry stays E1-039's." |
| Update OPEN-NEW-11 (TE-011 lint) | Add: "RWB-E1-001 plan v1 writes 526 `is_personal` literals, one per `sys_fields` INSERT, and no `UPDATE`; TASK-18 runs the lint if merged and records zero findings or the exact findings; it is never waivered." |
| Add a note against OPEN-NEW-5 | "The plan's two `parameter_catalog` rows have `value_source=TABLE` and a default but seed no `parameter_value` row; the merged `ParameterService` returns the catalog default. TASK-00 confirms the E1-042 rule. If a value row is required, the builder stops and reports (`PG-E1001-03`)." |
| Add OPEN-NEW-17 (new, non-blocking) | "`data_product.updated_by` is not writable through the published `apply(loadId, file, validFrom)` (no actor). RWB-E1-001 plan v1 writes `updated_at` and leaves `updated_by` NULL; the approver is audited in `reference_version.approver_user_id`. A later story that adds an actor-bearing apply can fill it without a data migration. Owner: recovery tech lead with the E1-043 owner. Raised by `PG-E1001-02`." |
| Keep OPEN-050 open | "Ratify or reject D-RUN-12, D-RUN-18 and D-RUN-21. RWB-E1-001 plan v1 applies them as orchestrator decisions and claims no ratification. Owner: recovery tech lead." |

## 5. Orchestrator actions at merge

| Action | Detail |
|---|---|
| Assign `<seq>` | The next four-digit number in merge order (D-RUN-07, D-RCV-28); rename `V<seq>__rwb_e1_001_recovery_schema.sql`; line 1 stays `-- Story: RWB-E1-001`; run the E1-044 lint |
| Record the human ruling | Before the merge, attach the ruling on `GAP-E1001-17` and `GAP-E1001-18` to the story and compare it with `ASM-E1001-13`/`-14`; if it differs, send the branch back through TASK-03 and the affected tests |
| Apply the shared rows above | Traceability row 009, the increment card and INDEX, the DOCUMENT-GAPS candidates, the open-item updates |
| Do not merge | While any of the two rulings is absent, or while a `checklist` item in `implement/merge-readiness.md` is open (TASK-19) |

No row in this file is a human decision, an approval, or a ratification.
