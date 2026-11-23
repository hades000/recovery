# WP B-PLT-TPL-03 — RWB-PLT-TPL: legacy RWB-TE-008, RWB-TE-011, RWB-TE-012
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 5
Read only:
- 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (read fully first)
- _work/msr/plan/ownership.json
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB TE 008 Decision log hash chain check v1.md (heading RWB-TE-008)
- 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB TE 011 PDPA lint for code tests and logs v1.md (heading RWB-TE-011)
- 04 User stories\Recovery Workbench User Stories Epic 1 Story Files v7\RWB TE 012 Document storage containers v1.md (heading RWB-TE-012)
- Thin stories only: _work/msr/extract/Recovery Workbench Business Requirements Program v4.md, Epic 1 v4, Epic 2 v2, Epics 3 to 8 Specification v3, Business Rules and Routing Logic (fill order Template and Rules §R7.3)
Write only:
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE008 APP Decision log hash chain check v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE011 APP PDPA lint for code, tests and logs v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE012 APP Document storage containers v1.md
- _work/msr/fragments/RWB-PLT-TE008-APP.json
- _work/msr/fragments/RWB-PLT-TE011-APP.json
- _work/msr/fragments/RWB-PLT-TE012-APP.json
- _work/msr/gaps/B-PLT-TPL-03.jsonl
- _work/msr/assumptions/B-PLT-TPL-03.jsonl
- _work/msr/editlog/B-PLT-TPL-03.md
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
9. A missing value: "Not specified in the source documents (CG-B-PLT-TPL-03-<n>; ASM-B-PLT-TPL-03-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/B-PLT-TPL-03.jsonl and _work/msr/assumptions/B-PLT-TPL-03.jsonl.
Stories:
{"id": "RWB-PLT-TE008-APP", "title": "Decision log hash chain check", "wt": "APP", "epic": "RWB-PLT-TPL", "service": "platform", "lane": "L-PLT-TPL-P", "ready": "Day 1", "owner": "TechX", "wave": 0, "business_epic": "EP01-TE", "release": "30 November 2026", "legacy": "RWB-TE-008", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP01", "DP03", "DP06", "DP07", "DP10", "DP13", "DP17", "DP19"], "H": ["RWB-PLT-E1027-CON", "RWB-PLT-E1042-CON", "RWB-PLT-E1043-CON", "RWB-PLT-E1071-CON", "RWB-PLT-N001-CON"], "C": ["RWB-P3-E1042-CON", "RWB-P3-E1043-CON", "RWB-P7-E1008-CON"], "I": [], "X": [], "acs": ["AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7", "AC8"], "tcs_legacy": ["TC-TE-008-01", "TC-TE-008-02", "TC-TE-008-03", "TC-TE-008-04", "TC-TE-008-05", "TC-TE-008-06", "TC-TE-008-07", "TC-TE-008-08", "TC-TE-008-09"], "reqs": ["REQ-DRI-003"], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE008 APP Decision log hash chain check v1.md", "source": "04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB TE 008 Decision log hash chain check v1.md"}
{"id": "RWB-PLT-TE011-APP", "title": "PDPA lint for code, tests and logs", "wt": "APP", "epic": "RWB-PLT-TPL", "service": "platform", "lane": "L-PLT-TPL-Q", "ready": "Day 1", "owner": "TechX", "wave": 0, "business_epic": "EP01-TE", "release": "30 November 2026", "legacy": "RWB-TE-011", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP01", "DP05", "DP07", "DP08", "DP19"], "H": ["RWB-PLT-E1043-CON", "RWB-PLT-E1037-CON", "RWB-PLT-N001-CON"], "C": ["RWB-P3-E1043-CON", "RWB-P4-E1037-CON"], "I": [], "X": ["RWB-PLT-TE001-APP"], "acs": ["AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7", "AC8", "AC9", "AC10"], "tcs_legacy": ["TC-TE-011-11", "TC-TE-011-01", "TC-TE-011-02", "TC-TE-011-03", "TC-TE-011-04", "TC-TE-011-05", "TC-TE-011-06", "TC-TE-011-07", "TC-TE-011-08", "TC-TE-011-09", "TC-TE-011-10"], "reqs": ["REQ-RDF-010", "REQ-ACA-005"], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE011 APP PDPA lint for code, tests and logs v1.md", "source": "04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB TE 011 PDPA lint for code tests and logs v1.md"}
{"id": "RWB-PLT-TE012-APP", "title": "Document storage containers", "wt": "APP", "epic": "RWB-PLT-TPL", "service": "platform", "lane": "L-PLT-TPL-R", "ready": "Day 1", "owner": "TechX", "wave": 0, "business_epic": "EP01-TE", "release": "30 November 2026", "legacy": "RWB-TE-012", "disposition": "Moved (no impact)", "build_status": "Not started", "patterns": ["DP01", "DP06", "DP07", "DP10", "DP11", "DP13", "DP19"], "H": ["RWB-PLT-E1042-CON", "RWB-PLT-E1043-CON", "RWB-PLT-E1071-CON", "RWB-PLT-N001-CON"], "C": ["RWB-P3-E1042-CON", "RWB-P3-E1043-CON"], "I": [], "X": ["RWB-PLT-TE001-APP"], "acs": ["AC1", "AC2", "AC3", "AC4", "AC5", "AC6", "AC7", "AC8", "AC9", "AC10", "AC11", "AC12"], "tcs_legacy": ["TC-TE-012-13", "TC-TE-012-01", "TC-TE-012-02", "TC-TE-012-03", "TC-TE-012-04", "TC-TE-012-05", "TC-TE-012-06", "TC-TE-012-07", "TC-TE-012-08", "TC-TE-012-09", "TC-TE-012-10", "TC-TE-012-11", "TC-TE-012-12"], "reqs": ["REQ-DCM-003", "REQ-DCM-002", "REQ-DCM-016", "REQ-DCM-015", "REQ-DCM-014"], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT TE012 APP Document storage containers v1.md", "source": "04 User stories\\Recovery Workbench User Stories Epic 1 Story Files v7\\RWB TE 012 Document storage containers v1.md"}
Parallel: give each legacy key to its own task subagent (aisdlc-msr-worker) in ONE message, up to 5 at once; each subagent writes only that key's files and its own jsonl rows with ids CG-B-PLT-TPL-03-<key>-<n>.
Finish: run python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-TPL-03 --quick ; fix every failure ; write _work/msr/editlog/B-PLT-TPL-03.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; reply with the list of files written.
