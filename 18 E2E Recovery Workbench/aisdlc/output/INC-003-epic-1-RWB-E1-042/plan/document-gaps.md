# Document gaps: RWB-E1-042 plan, revision 2

RUN_ID `INC-003-epic-1-RWB-E1-042`, stage `plan`, 2026-11-18, run 2. Revision 2 narrows `PG-E1042-01` to the six D-RCV-36 rows after re-reading the 10 Nov pack CSV/SQL; no other row changed. Candidate rows for `aisdlc/DOCUMENT-GAPS.md`; the orchestrator numbers them. The spec stage's rows `E1042-SP-DG-01` to `-18` are carried, not repeated: the "How this stage proceeded" column states what the plan does with each. The `review/` stage's `E1042-RV-DG-01` to `-15` are carried the same way.

- Precedence: client decisions D-RCV-35 and D-RCV-36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts.
- `legacy/` = `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/`. `aisdlc/`, `api/` and `backend/` are under `<repo>`.
- A row is recorded only with two citations that disagree, or one citation plus the place the answer should be and is not.

**Blockers: none.**

## New gaps raised by this stage

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| PG-E1042-01 | Technical specification RWB-E1-042 revision 13, §7.1: `description` is a **required** catalog column, at most 400 characters | The six D-RCV-36 rows of §12.4 have no `description` text in any source. The 13 rows inherited from the 10 Nov pack are **not** a gap: `_v2-baseline/implement/config/parameter-catalog.csv` has a `description` column with text for all 13 (lines 2-14), and `_v2-baseline/implement/sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` seeds the same text (lines 353-430). Story v7 §4 carries no per-key description | Spec §12.4 (the 19 rows; its "Source" column names owners, ranges and defaults, never description text); the pack text covers only the first 13 keys, and the six D-RCV-36 rows are added by the spec, not the pack | No | The field is documentation: it appears in the catalog, the generated key and the response (`Parameter` has no description field, so nothing is served) and no rule reads it. A wrong description cannot change a value, a threshold or a decision | The plan uses the 13 pack descriptions verbatim in `data-model.md` §2.1 and writes one short line for each of the six D-RCV-36 rows from the key name and spec §12.4, adding no business rule, with the owner free to reword it (`PA-E1-042-06`); TASK-03 writes it, TASK-05 checks only presence and length |
| PG-E1042-02 | Technical specification RWB-E1-042 revision 13, §7.5 and §11.3: `ParameterLoadResult` carries `repeat`, and an identical repeat load answers 201 with the same body | API Specification v4 `components/schemas/ReferenceLoad` (`api/recovery-api-v4.yaml` lines 8832-8846) has five fields — `id`, `table`, `validFrom`, `status`, `rows` — and no field for a repeat; the same file's `postAdminReferenceLoads` (line 3167) does not say which status a repeat returns | Spec §11.3 ("Identical repeat load answers 201 with the existing body; 409 only for conflicting content — behaviour the OpenAPI leaves open", `OI-E1-042-011`); `CLAR-011` | No | The flag is internal to the interface this story publishes; RWB-E1-043's endpoint has to decide whether and how to expose it, and `OI-E1-042-011` already asks the API owner to record it. Nothing in this story's code, schema or test depends on the API field | The flag stays on `ParameterLoadResult` and is asserted through the interface (`TC-16`, `TC-33`); no JSON field is invented and `api/recovery-api-v4.yaml` is not edited; the row is carried for the API owner |

## Carried gaps and how this stage proceeded

| Carried ID | Blocker? | How the plan proceeds |
|---|---|---|
| E1042-SP-DG-01 (ENVIRONMENT-kind key with table values) | No | `value_source` drives the generated key (TABLE/ENV/SECRET); AC8's table values for `refdata.cache.ttl-seconds` are seeded (§2 rows 2 and 8); TASK-03, TASK-05 |
| E1042-SP-DG-02 (X3 "does not start" vs AC4) | No | Readiness DOWN with the process up; TASK-17, TC-04, TC-32 |
| E1042-SP-DG-03 (no role holds Reference data A) | No | Only author <> approver is enforced here; C/A/U are RWB-E1-043's check; TASK-19, `CLAR-013` |
| E1042-SP-DG-04 (one `versionNo` cannot describe a multi-key load) | No | The event carries `versions[{paramKey, environment, versionNo}]`; `data-model.md` §6; TASK-09, TASK-19 |
| E1042-SP-DG-05 (business date source arrives later) | No | `BusinessDateProvider` seam with the Asia/Bangkok interim; TASK-09, TASK-17 |
| E1042-SP-DG-06 (pack's Thai differs from the Standard) | No | Standard v4 text is used; TASK-11, `PA-E1-042-09` |
| E1042-SP-DG-07 (story v7 expects a table-code list) | No | Not served here; only `ParameterLoadHandler.TABLE = "PARAMETER"`; TASK-09 |
| E1042-SP-DG-08 (who owns the shared endpoint) | No | RWB-E1-043 (D-RUN-10); this story builds no controller for it; TASK-09, TASK-19 |
| E1042-SP-DG-09 (no message for an unknown load, no 503 ID) | No | 404 `MSG-P4-003`; the GET 503 is status-only; TASK-11, TASK-17 |
| E1042-SP-DG-10 (no message for the flag-off refusal) | No | RWB-E1-043 refuses with 404 `MSG-P4-003`; this story only states the contract; TASK-09, TASK-20 (TC-22) |
| E1042-SP-DG-11 (`MSG-GEN-006` promises a retry) | No | Approve uses `MSG-P7-003`; the GET 503 carries no message ID; TASK-11, TASK-17, TC-30, TC-34 |
| E1042-SP-DG-12 (column definitions per table code) | No | This catalog holds none; RWB-E1-043 owns the keys and the check; TASK-05 does not scan for them |
| E1042-SP-DG-13 (`README.md` coverage note vs D-RCV-40) | No | Both coverage tasks stay outside `check`; TASK-21, TASK-22 |
| E1042-SP-DG-14 (story package vs baseline module) | No | `casewf.config` and `casewf.config.api` on RWB-TE-001's homes; TASK-09 |
| E1042-SP-DG-15 (`is_personal` false for author and approver) | No | Protective reading: personal, never logged or served; TASK-11, TASK-17, TASK-19, TASK-25 |
| E1042-SP-DG-16 (AGENTS §7 "more than one module") | No | D-RUN-21 reads "one module" as the ACE module (recovery); the plan passes the one-module check and claims no ratification; `plan.md` "One-module check" |
| E1042-SP-DG-17 (audit columns absent from the Inventory) | No | Protective reading: personal; `data-model.md` §10; TASK-25 |
| E1042-SP-DG-18 (P1/P4 readers cannot call a P3 service) | No | `access.api.CatalogParameterReader`, implemented in `casewf.config` (D-RUN-19); TASK-09, TASK-17, TC-46 |
| E1042-RV-DG-01 to -15 | No | Each is settled in the spec's "Carried gaps" table; the plan implements the settlement named there and adds no new decision |

## Where an answer should be and is not (recorded, not guessed)

| Item | Place the answer should be | What the plan does |
|---|---|---|
| A message ID for a failed synchronous read (`GET /admin/parameters` 503) | Error and Message Standard v4 (no row fits; `MSG-GEN-006` promises a retry) | status-only Problem, no message ID (`CLAR-019`, `E1042-SP-DG-11`) |
| Wording for an unknown `loadId` and for the flag-off refusal | Story v7 RWB-E1-042 §14 (lists neither) | existing `MSG-P4-003` (`CLAR-021`) |
| The full Epic 1 catalog file | `config/parameter-catalog.csv` does not exist in the document set | 19-row bootstrap; later stories add rows by PR and migration (`CLAR-003`) |
| Whether a P1/P4 reader may hold a computed key | `AGENTS.md` §3.2 and SPEC-003 allow only a literal | the literal-only rule stands; `CLAR-028` is RWB-E1-037's to answer and is not decided here |
