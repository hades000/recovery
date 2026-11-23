# WP B-ITG-W2-08 — RWB-ITG-W2: legacy RWB-E2-042, RWB-E2-043, RWB-E3-006, RWB-E3-010, RWB-E3-013
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 5
Read only:
- 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (read fully first)
- _work/msr/plan/ownership.json
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- 04 User stories\Recovery Workbench User Stories Epic 2 Story Files v5\RWB E2 042 Epic 2 rule packages in Drools v1.md (heading RWB-E2-042)
- 04 User stories\Recovery Workbench User Stories Epic 2 Story Files v5\RWB E2 043 Temporal and Drools integration pattern and reference case workflow v1.md (heading RWB-E2-043)
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E3-006)
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E3-010)
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E3-013)
- Thin stories only: _work/msr/extract/Recovery Workbench Business Requirements Program v4.md, Epic 1 v4, Epic 2 v2, Epics 3 to 8 Specification v3, Business Rules and Routing Logic (fill order Template and Rules §R7.3)
Write only:
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2042 ITG Epic 2 rule packages in Drools - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2043 ITG Temporal and Drools integration pattern and reference case workflow - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3006 ITG Calculate the plan installment - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3010 ITG Book the plan and set the schedule - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3013 ITG Check encumbrance and eligibility before negotiation - integration v1.md
- _work/msr/fragments/RWB-ITG-E2042-ITG.json
- _work/msr/fragments/RWB-ITG-E2043-ITG.json
- _work/msr/fragments/RWB-ITG-E3006-ITG.json
- _work/msr/fragments/RWB-ITG-E3010-ITG.json
- _work/msr/fragments/RWB-ITG-E3013-ITG.json
- _work/msr/gaps/B-ITG-W2-08.jsonl
- _work/msr/assumptions/B-ITG-W2-08.jsonl
- _work/msr/editlog/B-ITG-W2-08.md
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
9. A missing value: "Not specified in the source documents (CG-B-ITG-W2-08-<n>; ASM-B-ITG-W2-08-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/B-ITG-W2-08.jsonl and _work/msr/assumptions/B-ITG-W2-08.jsonl.
Stories:
{"id": "RWB-ITG-E2042-ITG", "title": "Epic 2 rule packages in Drools", "wt": "ITG", "epic": "RWB-ITG-W2", "service": "integration", "lane": "L-ITG-W2", "ready": "Day 1", "owner": "TechX", "wave": 2, "business_epic": "EP02", "release": "31 December 2026", "legacy": "RWB-E2-042", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP01", "DP03", "DP04", "DP05", "DP06", "DP07", "DP10", "DP13", "DP14", "DP15", "DP19"], "H": [], "C": [], "I": ["RWB-P3-E2042-APP", "RWB-P6-E2042-APP", "RWB-P4-E2042-APP", "RWB-P7-E2042-APP"], "X": [], "acs": [], "tcs_legacy": ["TC-E2-042-01", "TC-E2-042-02", "TC-E2-042-03", "TC-E2-042-04", "TC-E2-042-05", "TC-E2-042-06"], "reqs": ["REQ-CWC-013", "REQ-CWC-014"], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2042 ITG Epic 2 rule packages in Drools - integration v1.md", "source": "04 User stories\\Recovery Workbench User Stories Epic 2 Story Files v5\\RWB E2 042 Epic 2 rule packages in Drools v1.md"}
{"id": "RWB-ITG-E2043-ITG", "title": "Temporal and Drools integration pattern and reference case workflow", "wt": "ITG", "epic": "RWB-ITG-W2", "service": "integration", "lane": "L-ITG-W2", "ready": "Day 1", "owner": "TechX", "wave": 2, "business_epic": "EP02", "release": "31 December 2026", "legacy": "RWB-E2-043", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP01", "DP03", "DP04", "DP05", "DP07", "DP09", "DP10", "DP11", "DP14", "DP15", "DP19"], "H": [], "C": [], "I": ["RWB-P3-E2043-APP", "RWB-P7-E2043-APP"], "X": [], "acs": [], "tcs_legacy": ["TC-E2-043-01", "TC-E2-043-02", "TC-E2-043-03", "TC-E2-043-04", "TC-E2-043-05", "TC-E2-043-06", "TC-E2-043-07"], "reqs": ["REQ-DRI-001", "REQ-DRI-005", "REQ-CWC-016", "REQ-DRI-007"], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2043 ITG Temporal and Drools integration pattern and reference case workflow - integration v1.md", "source": "04 User stories\\Recovery Workbench User Stories Epic 2 Story Files v5\\RWB E2 043 Temporal and Drools integration pattern and reference case workflow v1.md"}
{"id": "RWB-ITG-E3006-ITG", "title": "Calculate the plan installment", "wt": "ITG", "epic": "RWB-ITG-W2", "service": "integration", "lane": "L-ITG-W2", "ready": "Day 1", "owner": "TechX", "wave": 2, "business_epic": "EP03", "release": "31 January 2027", "legacy": "RWB-E3-006", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP05", "DP07", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S2-E3006-APP"], "X": [], "acs": ["AC2"], "tcs_legacy": ["TC-E3-006-01", "TC-E3-006-02", "TC-E3-006-03", "TC-E3-006-04", "TC-E3-006-05"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3006 ITG Calculate the plan installment - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
{"id": "RWB-ITG-E3010-ITG", "title": "Book the plan and set the schedule", "wt": "ITG", "epic": "RWB-ITG-W2", "service": "integration", "lane": "L-ITG-W2", "ready": "Day 1", "owner": "TechX", "wave": 2, "business_epic": "EP03", "release": "31 January 2027", "legacy": "RWB-E3-010", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP05", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S2-E3010-APP"], "X": [], "acs": ["AC1"], "tcs_legacy": ["TC-E3-010-01", "TC-E3-010-02", "TC-E3-010-03", "TC-E3-010-04", "TC-E3-010-05", "TC-E3-010-06"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3010 ITG Book the plan and set the schedule - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
{"id": "RWB-ITG-E3013-ITG", "title": "Check encumbrance and eligibility before negotiation", "wt": "ITG", "epic": "RWB-ITG-W2", "service": "integration", "lane": "L-ITG-W2", "ready": "Day 1", "owner": "TechX", "wave": 2, "business_epic": "EP03", "release": "31 January 2027", "legacy": "RWB-E3-013", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP05", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S2-E3013-APP", "RWB-P3-E3013-APP"], "X": [], "acs": [], "tcs_legacy": ["TC-E3-013-01", "TC-E3-013-02", "TC-E3-013-03", "TC-E3-013-04", "TC-E3-013-05", "TC-E3-013-06"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3013 ITG Check encumbrance and eligibility before negotiation - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
Parallel: give each legacy key to its own task subagent (aisdlc-msr-worker) in ONE message, up to 5 at once; each subagent writes only that key's files and its own jsonl rows with ids CG-B-ITG-W2-08-<key>-<n>.
Finish: run python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-08 --quick ; fix every failure ; write _work/msr/editlog/B-ITG-W2-08.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; reply with the list of files written.
