# WP B-ITG-W4-05 — RWB-ITG-W4: legacy RWB-E6-028, RWB-E6-029, RWB-E6-030, RWB-E6-031, RWB-E6-032
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 5
Read only:
- 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (read fully first)
- _work/msr/plan/ownership.json
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E6-028)
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E6-029)
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E6-030)
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E6-031)
- 04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md (heading RWB-E6-032)
- Thin stories only: _work/msr/extract/Recovery Workbench Business Requirements Program v4.md, Epic 1 v4, Epic 2 v2, Epics 3 to 8 Specification v3, Business Rules and Routing Logic (fill order Template and Rules §R7.3)
Write only:
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6028 ITG Sell a post charge-off population - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6029 ITG Onboard a partner and set terms - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6030 ITG Hold the partner panel and fee schedule as data - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6031 ITG Allocate work by measured return - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6032 ITG Override an allocation with a reason - integration v1.md
- _work/msr/fragments/RWB-ITG-E6028-ITG.json
- _work/msr/fragments/RWB-ITG-E6029-ITG.json
- _work/msr/fragments/RWB-ITG-E6030-ITG.json
- _work/msr/fragments/RWB-ITG-E6031-ITG.json
- _work/msr/fragments/RWB-ITG-E6032-ITG.json
- _work/msr/gaps/B-ITG-W4-05.jsonl
- _work/msr/assumptions/B-ITG-W4-05.jsonl
- _work/msr/editlog/B-ITG-W4-05.md
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
9. A missing value: "Not specified in the source documents (CG-B-ITG-W4-05-<n>; ASM-B-ITG-W4-05-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/B-ITG-W4-05.jsonl and _work/msr/assumptions/B-ITG-W4-05.jsonl.
Stories:
{"id": "RWB-ITG-E6028-ITG", "title": "Sell a post charge-off population", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP06", "release": "30 April 2027", "legacy": "RWB-E6-028", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S7-E6028-APP", "RWB-P7-E6028-APP"], "X": [], "acs": [], "tcs_legacy": ["TC-E6-028-01", "TC-E6-028-02", "TC-E6-028-03", "TC-E6-028-04", "TC-E6-028-05", "TC-E6-028-06"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6028 ITG Sell a post charge-off population - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
{"id": "RWB-ITG-E6029-ITG", "title": "Onboard a partner and set terms", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP06", "release": "30 April 2027", "legacy": "RWB-E6-029", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S9-E6029-APP"], "X": [], "acs": ["AC1"], "tcs_legacy": ["TC-E6-029-01", "TC-E6-029-02", "TC-E6-029-03", "TC-E6-029-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6029 ITG Onboard a partner and set terms - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
{"id": "RWB-ITG-E6030-ITG", "title": "Hold the partner panel and fee schedule as data", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP06", "release": "30 April 2027", "legacy": "RWB-E6-030", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP07", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S9-E6030-APP"], "X": [], "acs": ["AC1"], "tcs_legacy": ["TC-E6-030-01", "TC-E6-030-02", "TC-E6-030-03", "TC-E6-030-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6030 ITG Hold the partner panel and fee schedule as data - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
{"id": "RWB-ITG-E6031-ITG", "title": "Allocate work by measured return", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP06", "release": "30 April 2027", "legacy": "RWB-E6-031", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP05", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S9-E6031-APP"], "X": [], "acs": ["AC1"], "tcs_legacy": ["TC-E6-031-01", "TC-E6-031-02", "TC-E6-031-03", "TC-E6-031-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6031 ITG Allocate work by measured return - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
{"id": "RWB-ITG-E6032-ITG", "title": "Override an allocation with a reason", "wt": "ITG", "epic": "RWB-ITG-W4", "service": "integration", "lane": "L-ITG-W4", "ready": "Day 1", "owner": "TechX", "wave": 4, "business_epic": "EP06", "release": "30 April 2027", "legacy": "RWB-E6-032", "disposition": "Split (rework)", "build_status": "Not started", "patterns": ["DP03", "DP13", "DP19"], "H": [], "C": [], "I": ["RWB-S9-E6032-APP"], "X": [], "acs": ["AC1"], "tcs_legacy": ["TC-E6-032-01", "TC-E6-032-02", "TC-E6-032-03", "TC-E6-032-04"], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": false, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6032 ITG Override an allocation with a reason - integration v1.md", "source": "04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md"}
Parallel: give each legacy key to its own task subagent (aisdlc-msr-worker) in ONE message, up to 5 at once; each subagent writes only that key's files and its own jsonl rows with ids CG-B-ITG-W4-05-<key>-<n>.
Finish: run python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-05 --quick ; fix every failure ; write _work/msr/editlog/B-ITG-W4-05.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; reply with the list of files written.
