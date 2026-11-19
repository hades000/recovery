# Wave 3 story brief (read fully before editing)

ROOT = C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14 (Git Bash: /c/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14). PYTHONIOENCODING=utf-8.

## What changed (frozen; do not re-decide)
Read first: `15 ACE DB Alignment/Recovery Workbench ACE DB Alignment Change Register v1.md` (U1–U5 = D-RCV-35, ADR-010, DL43, Appendix A removals, Appendix B re-keyed FKs) and `15 ACE DB Alignment/Recovery Workbench ACE Data Tier Map v1.md` (copy entity → ACE table and `recovery.v_ace_*` view). View names and columns: `15 ACE DB Alignment/Recovery Workbench ACE Source Views v1.sql`. Coordinator decisions: `_work/verify/defects.md` sections "COORDINATOR DECISION" and "COORDINATOR DECISIONS — data model".

- U1: the Workbench loads no source data. ALS, EFS, SCBPDM, COLLINS, CCMS, SVAF, AMIS, RPS, LIT, WIN POD, GL, NLEADS, EasyApp and Entra groups land in ACE through ACE ingestion (ACE team, RWB-ACE-001).
- U4: the recovery module reads ACE ONLY through `recovery.v_ace_*` read-only views. There are no FKs into ACE; links use business keys: `account_key`, `person_key`, `asset_key`, `payment_code`, `contact_key` (composite `contact_type:key`), `primary_person_key`.
- U3: Workbench-only attributes live in extension tables `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` (check the Tier Map for the final list).
- U5: Excel and SharePoint trackers are out of system scope (Cutover plan).
- Freshness and "data ready" come from `ace_batch_run`, read through `v_ace_batch_status`. Events: `AceDataReady` replaces LoadCompleted, `AceDataLate` replaces LoadRefused. JOB-01 and JOB-09 are retired; other jobs trigger on the ACE batch-complete record.
- Migrations: V0001 baseline (E1-001), V0002 Section A views (E1-069), V0003 Section B views after RWB-ACE-001 (features behind flags until then).
- Roles: `ace_view_owner` owns the views; `recovery_svc` has SELECT on `recovery.v_ace_*` only for ACE data and no privilege on `public`.
- Removed tables (never reference as live): loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation (now ACE Tier 2 `valuation` via `v_ace_valuation`), score (`collins_score` via `v_ace_score`), asset (NPA asset now ACE `npa_asset` via `v_ace_npa_asset`), load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory, tracker_row.
- Removed stories (Appendix A): E1-003, 004, 005, 006, 009, 010, 012, 051, E2-023, DM-001, DM-002. A live story that depends on one of them must drop that dependency, or point to RWB-ACE-001 / RWB-E1-069.
- API v3: tracker, DQ-exception and manual-retirement endpoints are removed. Asset paths are `/assets/{assetKey}`. Schemas use accountKey, personKey, paymentCode, assetKey, contactKey.

## Fragment protocol (one writer per fragment)
- Source: the story's `## RWB-XX-NNN …` section in its consolidated md (Epic 1 v7.md, Epic 2 v5.md, Epics 3 to 8 v2.md, Technical Enabler Stories v5.md, Data Migration Stories v2.md, Administration Stories v2.md), plus its rows in the matching xlsx (sheets Stories, Acceptance criteria, Test cases, Traceability, Dependencies, or as present).
- Write `_work/fragments/<KEY>.md`: the COMPLETE revised section, from the `## <KEY> <Title>` line up to (not including) the next story heading. Keep the template, the section numbering and the style. Plain short sentences.
- Write `_work/fragments/<KEY>.json`, the xlsx patch: `{"key": "...", "file": "<xlsx name>", "Stories": {<column header>: <new value>, ...only changed columns}, "Acceptance criteria": {"Gherkin": "<full new gherkin>"} or omitted, "Test cases": {"replace": [{"Test case": ..., "Covers": ..., "Test": ..., "Level": ..., "Data": ...}], "remove": ["TC-..."]} or omitted, "Traceability": ..., "Dependencies": ...}`. Use the exact column headers of that workbook.
- Also write `_work/fragments/<KEY>.log.md` with: disposition, sections changed, IDs added or removed (ACs, TCs, BRs, messages), dependencies changed, open questions.
- Do NOT edit any project document. Only write fragment files.

## Edit rules
- Rewrite: re-base flow, exception paths, ACs (Gherkin), business rules, data table (§11), contract (§12), solution plan (§13), tests (§16), guardrails and traceability around the views and business keys. Keep the story's purpose, its key and its AC numbering where possible. A removed AC keeps its number with "Removed by D-RCV-35" only if other docs cite it; otherwise renumber cleanly and log the mapping.
- Minor: change only the references (entity and field names, JOB-01/09, INT load wording, LoadCompleted, tracker mentions, removed-story dependencies, `/assets/{assetId}`). Do not touch anything else.
- The guardrail "No read of another module's tables" stays, with the addition: "ACE data only through recovery.v_ace_* views."
- Data table field IDs: take field IDs for view columns from `06 Data/Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx` (DF-ACE-xxx); do not invent IDs. If a field ID can't be resolved, keep the name and log it.
- Do not invent new message IDs, rule IDs, or story keys. New TC IDs are allowed only within the story's own TC-<story>-NN series.
- Dates in new text: 15 November 2026.
