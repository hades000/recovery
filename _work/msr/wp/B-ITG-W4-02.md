# WP B-ITG-W4-02 — RWB-ITG-W4: legacy RWB-DM-003, RWB-DM-004, RWB-DM-005, RWB-DM-006, RWB-DM-007
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 5
Read only:
- 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (read fully first)
- _work/msr/plan/ownership.json
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- 04 User stories/Recovery Workbench Data Migration Stories v3.md (heading RWB-DM-003)
- 04 User stories/Recovery Workbench Data Migration Stories v3.md (heading RWB-DM-004)
- 04 User stories/Recovery Workbench Data Migration Stories v3.md (heading RWB-DM-005)
- 04 User stories/Recovery Workbench Data Migration Stories v3.md (heading RWB-DM-006)
- 04 User stories/Recovery Workbench Data Migration Stories v3.md (heading RWB-DM-007)
- Thin stories only: _work/msr/extract/Recovery Workbench Business Requirements Program v4.md, Epic 1 v4, Epic 2 v2, Epics 3 to 8 Specification v3, Business Rules and Routing Logic (fill order Template and Rules §R7.3)
Write only:
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM003 ITG Migrate case and ownership - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM004 ITG Migrate treatment and offers - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM005 ITG Migrate contact and promises - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM006 ITG Migrate collateral and assets - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM007 ITG Migrate legal events and cases - integration v1.md
- _work/msr/fragments/RWB-ITG-DM003-ITG.json
- _work/msr/fragments/RWB-ITG-DM004-ITG.json
- _work/msr/fragments/RWB-ITG-DM005-ITG.json
- _work/msr/fragments/RWB-ITG-DM006-ITG.json
- _work/msr/fragments/RWB-ITG-DM007-ITG.json
- _work/msr/gaps/B-ITG-W4-02.jsonl
- _work/msr/assumptions/B-ITG-W4-02.jsonl
- _work/msr/editlog/B-ITG-W4-02.md
Do, for each story line below (one JSON object per line), write exactly one file at its "file" path:
1. Use the template in Template and Rules v1 §R7: the 19 headings in order, the metadata table rows of §R7.1 in order (never remove a row).
   Copy these values exactly from the JSON: Story key=id, Work type, Suggested owner (fixed phrase for "owner"), Service, Service epic=epic,
   Wave, Business epic, Release (+ " (tentative)"; "None (new story)" when empty), Legacy key, Legacy disposition, Build status,
   Patterns applied, Parallel lane, Ready to start, Depends on (build)=H, Contract dependencies=C, Integration dependencies=I,
   External dependencies=X, PRD reference "Pending (C1)", Status "Draft (realignment v1)".
2. preserved=true: copy legacy §1-11, §14-16, §18 and §19 word for word; keep §12 and §13 under the heading "As built (monolith)".
3. delta=true: describe only the microservice change for that legacy key in Template and Rules §R6.
4. ACs: "acs" lists the legacy AC IDs this story owns. Copy each verbatim with the origin tag "(legacy <legacy> <AC>)".
   An APP AC whose cross-service part can be mocked gets the Given "Given the <service> contract mock returns <x>" (keep every value).
   CON, DB, INF, OPS and new stories: write ACs tagged "(new, D-RCV-60)" that test only the deliverable in the title. Never invent business values.
5. TCs: keep the legacy TC IDs of the ACs this story owns; an ITG copy of a TC gets the suffix -ITG. Add the Level column (§R7.2 s16).
6. Apply the DP table (§R5.5) for every pattern in "patterns"; list them in "Patterns applied".
7. Section 12 Contract: tables 12.1-12.9 (or None). Names: topic rwb.<short>.events.v1, event rwb.<short>.<Event>.v1, queue rwb-<short>,
   REST base /api/recovery/<short>/v1, schema rwb_<name>. Owners come from the Ownership Map only.
8. Write _work/msr/fragments/<id>.json with keys: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy,
   disposition, H, C, I, X, acs [{"id","origin","text_first_line"}], tcs, reqs, ops_provided, ops_consumed, events_published,
   events_consumed, workflows, prd_ref "Pending (C1)", gaps [CG ids], assumptions [ASM ids], file.
9. A missing value: "Not specified in the source documents (CG-B-ITG-W4-02-<n>; ASM-B-ITG-W4-02-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/B-ITG-W4-02.jsonl and _work/msr/assumptions/B-ITG-W4-02.jsonl.
Stories:
{"id": "RWB-ITG-DM003-ITG", "title": "Migrate case and ownership", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP08", "release": "30 November 2026", "legacy": "RWB-DM-003", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP05", "DP15", "DP19"], "H": [], "C": [], "I": ["RWB-P1-DM003-APP"], "X": [], "acs": ["AC2"], "tcs_legacy": ["TC-DM-003-01", "TC-DM-003-02", "TC-DM-003-03", "TC-DM-003-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM003 ITG Migrate case and ownership - integration v1.md", "source": "04 User stories/Recovery Workbench Data Migration Stories v3.md"}
{"id": "RWB-ITG-DM004-ITG", "title": "Migrate treatment and offers", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP08", "release": "31 December 2026", "legacy": "RWB-DM-004", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP05", "DP15", "DP19"], "H": [], "C": [], "I": ["RWB-P1-DM004-APP"], "X": [], "acs": ["AC2"], "tcs_legacy": ["TC-DM-004-01", "TC-DM-004-02", "TC-DM-004-03", "TC-DM-004-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM004 ITG Migrate treatment and offers - integration v1.md", "source": "04 User stories/Recovery Workbench Data Migration Stories v3.md"}
{"id": "RWB-ITG-DM005-ITG", "title": "Migrate contact and promises", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP08", "release": "30 November 2026", "legacy": "RWB-DM-005", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP05", "DP15", "DP19"], "H": [], "C": [], "I": ["RWB-P1-DM005-APP"], "X": [], "acs": ["AC1", "AC2"], "tcs_legacy": ["TC-DM-005-01", "TC-DM-005-02", "TC-DM-005-03", "TC-DM-005-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM005 ITG Migrate contact and promises - integration v1.md", "source": "04 User stories/Recovery Workbench Data Migration Stories v3.md"}
{"id": "RWB-ITG-DM006-ITG", "title": "Migrate collateral and assets", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP08", "release": "31 December 2026", "legacy": "RWB-DM-006", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP05", "DP15", "DP19"], "H": [], "C": [], "I": ["RWB-P1-DM006-APP"], "X": [], "acs": ["AC2"], "tcs_legacy": ["TC-DM-006-01", "TC-DM-006-02", "TC-DM-006-03", "TC-DM-006-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM006 ITG Migrate collateral and assets - integration v1.md", "source": "04 User stories/Recovery Workbench Data Migration Stories v3.md"}
{"id": "RWB-ITG-DM007-ITG", "title": "Migrate legal events and cases", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP08", "release": "31 December 2026", "legacy": "RWB-DM-007", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP05", "DP15", "DP19"], "H": [], "C": [], "I": ["RWB-P1-DM007-APP"], "X": [], "acs": ["AC1", "AC2"], "tcs_legacy": ["TC-DM-007-01", "TC-DM-007-02", "TC-DM-007-03", "TC-DM-007-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG DM007 ITG Migrate legal events and cases - integration v1.md", "source": "04 User stories/Recovery Workbench Data Migration Stories v3.md"}
Parallel: give each legacy key to its own task subagent (aisdlc-msr-worker) in ONE message, up to 5 at once; each subagent writes only that key's files and its own jsonl rows with ids CG-B-ITG-W4-02-<key>-<n>.
Finish: run python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-02 --quick ; fix every failure ; write _work/msr/editlog/B-ITG-W4-02.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; reply with the list of files written.
