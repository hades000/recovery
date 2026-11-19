# Assumptions: RWB-E1-001 plan

RUN_ID `INC-009-epic-1-RWB-E1-001`, stage `plan`, 18 November 2026, run 1. No question was asked
(RUN-BRIEF rule 4; L-RCV-03; `AGENTS.md` §10.6). Each plan assumption is labelled, gives its basis,
says where it is used and names who confirms it. **No assumption here is a human approval**, and none
resolves `GAP-E1001-17` or `GAP-E1001-18`. The spec's assumptions `ASM-E1001-01` .. `-20` are carried
unchanged and are not re-litigated.

## Carried blocker assumptions (not plan assumptions)

| ID | Assumption | Status | Basis and effect |
|---|---|---|---|
| `ASM-E1001-13` | The Story v7 §13 DP07 system-of-record text is kept verbatim; `data_product.system_of_record` and DF-REF-074 `physical_type` are `varchar(200)` | **Blocker = Yes gap `GAP-E1001-17`; open** | Story v7 §13 DDL vs its own seed (139 characters); PS v6 line 820; LDM v8 `06-data/recovery-workbench-logical-data-model-and-data-dictionary-v8-xlsx.md` line 561. A human ruling by the data architect is required **before the merge of the migration** (OPEN-NEW-6). The plan uses the assumption in TASK-03 and tests it in TASK-01/02; nothing here ratifies it |
| `ASM-E1001-14` | `sys_fields.is_personal` is the protective union of PS v6 `true` and PDPA v4 "Personal data = Yes": 526 rows, literals in each `INSERT`, never an `UPDATE`; the 26 PS-v6-only fields stay `false` | **Blocker = Yes gap `GAP-E1001-18`; open** | PS v6 18 vs PDPA v4 523; Design v2 line 31; no precedence ranks them. A human ruling by the data architect with the DPO is required **before the merge** (OPEN-NEW-7). The plan uses it in TASK-03 and tests it in TASK-01/02; the 526 marks may only narrow by that ruling |

Their `document-gaps.md` rows are Blocker = Yes and are repeated in the plan-stage gaps file with the
merge gate (TASK-19).

## Plan-stage assumptions

| ID | Assumption | Basis | Used in | Confirms |
|---|---|---|---|---|
| `PA-E1001-01` | The migration body is a **mechanical transcription** of PS v6 lines 16–6130 with T1–T11; the plan does not restate 1,075 columns as a second source. `MigrationDerivationTest` compares the file with `infra/postgres/schema/03-recovery-physical-schema-v6.sql` (the byte-identical repo copy) table by table, column by column | Spec SPEC-002; the plan-time count of PS v6 (93 tables, 92 FKs, 112 indexes); `RecoveryDatabaseIT` already reads `../infra/postgres` | TASK-01, TASK-03 | Tech lead |
| `PA-E1001-02` | K4 reads the active `role.role_code` values through a package-private read-only JPA entity/repository in `dataengine.internal.catalog`. The table is created and seeded by this migration; no other module publishes a role-list reader and `LOV-ROLE` does not exist | `ASM-E1001-10`; PS v6 `role` and `lov_value`; AGENTS §3.11 (no other module's code is called) | TASK-07 | Tech lead; data owner |
| `PA-E1001-03` | K1 names the missing codes ascending in `{products}`. When nothing is missing, it names the duplicated or unexpected codes instead, so an unknown code is refused by the same check without inventing a new message ID; the text and ID are unchanged | Spec SPEC-013 K1 ("an unknown code is refused by the same check"); MSG-P1-004 text; AC8 | TASK-06, TASK-07 | BA |
| `PA-E1001-04` | K0-R requires five columns and width-checks every column, but does not require `system_of_record` or `owner_user_id`; their absence is K2/K3 with MSG-P1-003. K0 never suppresses K2/K3 for the same row | `ASM-E1001-19`; Story v7 X4; AC7; MSG v4 lines 68, 151 | TASK-06, TASK-07 | BA |
| `PA-E1001-05` | `data_product.version` is mapped as the JPA `@Version` column; `apply` does not set it, and Hibernate increments it once on flush. The System test asserts `version + 1` per row | PS v6 `version integer NOT NULL DEFAULT 1`; spec SPEC-014 ("increments `version`"); the standard-column pattern | TASK-07, TASK-14 | Tech lead |
| `PA-E1001-06` | `data_product.updated_by` is **not writable** through the published `apply(loadId, file, validFrom)`: the SPI carries no actor. `apply` writes `updated_at`; the approver is audited by E1-043 in `reference_version.approver_user_id`; the column stays at its seeded NULL | E1-043 spec revision 10 "Reference load handler" signature; PS v6 `updated_by uuid` nullable; spec field matrix | TASK-07, TASK-18 | Tech lead; E1-043 owner (awareness) — recorded as `PG-E1001-02`, Blocker = No |
| `PA-E1001-07` | The handler's K4 lookup runs `activeRoleCodes()` once per `validate` call, not once per row; there is no cache and no reload during a call | Spec SPEC-013; 54 seeded roles; a validate is one file | TASK-07 | Tech lead |
| `PA-E1001-08` | K0-H compares `ReferenceLoadFile.columns()` exactly (case-sensitive, no trim) with the 8-name list; E1-043's reader supplies the header strings as read from the file | Spec SPEC-013 K0-H ("exactly", "in this order"); E1-043's `ReferenceLoadFileReader` | TASK-06, TASK-07 | Tech lead |
| `PA-E1001-09` | `{row}` renders as a plain decimal integer; `{date}` renders as ISO-8601 `yyyy-MM-dd` (`LocalDate.toString()`); no locale-specific format is introduced | MSG v4 lines 81, 85; AC9's "Row 4"; E1-043 `RowCheckFailure.row` | TASK-06, TASK-07, TASK-14 | BA |
| `PA-E1001-10` | The AC4 failing copy is built at test runtime by applying the merged E1-042 and E1-043 migrations to a throwaway schema first, then the modified E1-001 copy with a broken `valuation_ext` statement. The failure is therefore at `valuation_ext`, not earlier at an FK to `reference_version` | AC4; the file's T8 FKs; E1-042/E1-043 files on the classpath | TASK-02 | Tech lead |
| `PA-E1001-11` | `DataDictionaryConformanceTest` asserts the 93-table baseline before C1/C2/C3, so an empty schema cannot pass C1 vacuously | Spec SPEC-009; the red-first order of TASK-02 | TASK-02 | Tech lead |
| `PA-E1001-12` | The 526-ID fixture is copied as field IDs plus object/field metadata (the `../specify/evidence/is_personal_union_v4.tsv` columns). It is schema metadata, not personal data; no value, name or account number is copied | `ASM-E1001-14`; AGENTS §4.7 | TASK-01 | DPO (awareness) |
| `PA-E1001-13` | The S2 branch in `10-load-ace-database.sh` extracts the PS v6 view section by the marker comment `-- ACE source views. Section A ships as V0002; Section B ships after RWB-ACE-001.`, not by a line number, so the read-only PS v6 file can be replaced by a corrected copy without silently changing the start point. A missing marker fails the init loudly | Spec SPEC-010 S2; PS v6 line 6132; RUN-BRIEF (the document set is read only) | TASK-13 | Tech lead; RWB-E1-069 owner (awareness) |
| `PA-E1001-14` | Earlier-story ITs that build an S1=`true` container move to S1=`false` (S2 set to what their assertions require) rather than being skipped or weakened; every assertion stays. If one cannot be moved without an assertion change, the builder stops and reports | Spec SPEC-010 ("no assertion is removed"); OPEN-NEW-9 | TASK-16 | Tech lead; E1-042 and E1-043 owners (awareness) |
| `PA-E1001-15` | `DataProductCatalogLoadIT` uses E1-043's real security chain with `jwt()` authorities naming RW-REFADM or RW-DATASTEW and a synthetic `oid` UUID. It does not bypass `@PreAuthorize` and does not mock `ApiExceptionHandler` | SPEC-016; E1-043's controller and `ActorIdResolver`; AC11/TC-11 | TASK-14 | Tech lead; access owner (awareness) |
| `PA-E1001-16` | The DB presence of the two `parameter_catalog` rows is proven by the load IT (E1-043's `ReferenceLoadAuthority` refuses when a key is missing) plus `ParameterCatalogRowsTest` over both artefacts. No extra assertion is added to `RecoverySchemaMigrationIT`, so TASK-03 stays the single green step for TASK-02 | SPEC-019 item 5; E1-043 SPEC-027; TC-E1-001-20 | TASK-10, TASK-11, TASK-14 | Tech lead |
| `PA-E1001-17` | The `DataProductCatalogHandler` bean is **package-private** with public interface methods; the SPI type is the interface. E1-043 collects it by type, so no visibility change is needed | TE-001's package-private module records; E1-043 `ReferenceTableHandlers` injects `List<ReferenceTableHandler>`; D-RUN-18 | TASK-07, TASK-09 | Tech lead |

No assumption changes a business rule, a value, a message text, a permission or a data classification.
The two that touch a business value (`PA-E1001-03`, `PA-E1001-09`) are message-rendering details whose
IDs and texts stay exactly as the story and MSG v4 give them.
