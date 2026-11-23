# WP B-ITG-W1-11 — RWB-ITG-W1: legacy W1J01, W1J02
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 5
Read only:
- 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (read fully first)
- _work/msr/plan/ownership.json
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- Thin stories only: _work/msr/extract/Recovery Workbench Business Requirements Program v4.md, Epic 1 v4, Epic 2 v2, Epics 3 to 8 Specification v3, Business Rules and Routing Logic (fill order Template and Rules §R7.3)
Write only:
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J01 ITG Contract-test harness and synthetic test data - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J02 ITG Wave 1 v5 journey end to end - integration v1.md
- _work/msr/fragments/RWB-ITG-W1J01-ITG.json
- _work/msr/fragments/RWB-ITG-W1J02-ITG.json
- _work/msr/gaps/B-ITG-W1-11.jsonl
- _work/msr/assumptions/B-ITG-W1-11.jsonl
- _work/msr/editlog/B-ITG-W1-11.md
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
9. A missing value: "Not specified in the source documents (CG-B-ITG-W1-11-<n>; ASM-B-ITG-W1-11-<n>)" plus one combined gap row per story and one
   assumption row per default (formats in Template and Rules §R9) in _work/msr/gaps/B-ITG-W1-11.jsonl and _work/msr/assumptions/B-ITG-W1-11.jsonl.
Stories:
{"id": "RWB-ITG-W1J01-ITG", "title": "Contract-test harness and synthetic test data", "wt": "ITG", "epic": "RWB-ITG-W1", "service": "integration", "lane": "L-ITG-W1", "ready": "Day 1", "owner": "QA", "wave": 1, "business_epic": "NEW", "release": "", "legacy": "W1J01", "disposition": "New", "build_status": "Not started", "patterns": [], "H": [], "C": [], "I": [], "X": [], "acs": [], "tcs_legacy": [], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": true, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J01 ITG Contract-test harness and synthetic test data - integration v1.md", "source": null}
{"id": "RWB-ITG-W1J02-ITG", "title": "Wave 1 v5 journey end to end", "wt": "ITG", "epic": "RWB-ITG-W1", "service": "integration", "lane": "L-ITG-W1", "ready": "Day 1", "owner": "QA", "wave": 1, "business_epic": "NEW", "release": "", "legacy": "W1J02", "disposition": "New", "build_status": "Not started", "patterns": [], "H": [], "C": [], "I": [], "X": [], "acs": [], "tcs_legacy": [], "reqs": [], "preserved": false, "delta": false, "secondary": false, "new": true, "file": "04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J02 ITG Wave 1 v5 journey end to end - integration v1.md", "source": null}
Parallel: give each legacy key to its own task subagent (aisdlc-msr-worker) in ONE message, up to 5 at once; each subagent writes only that key's files and its own jsonl rows with ids CG-B-ITG-W1-11-<key>-<n>.
Finish: run python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-11 --quick ; fix every failure ; write _work/msr/editlog/B-ITG-W1-11.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; reply with the list of files written.
