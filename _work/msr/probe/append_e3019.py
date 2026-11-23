import json, os
W = r"_work/msr"

def gap(i, title, desc, evidence, gtype="Missing", sev="P2", section="", area="", legacy="", owner="Solution architect", asm="", proposed="", wave="2"):
    return {"id": f"CG-B-S5-01-E3019-{i}", "title": title, "source": "Template and Rules v1 R5.4, R5.5, R7.3 and R9; split_plan.json slice RWB-S5-E3019-APP and -CON (H, C, I, X); Architecture v5 Text Extract v1 slides 13, 19, 29, 37, 41, 43 and 45; TSD S5 v2 T2, T3.1, T3.2, T4, T6.1 and T-A; FSD S5 v3 A1.4 and A2.1; Business Rules and Routing Logic v4 rows R-DIS-01, R-DIS-03 and R-DIS-06; legacy RWB-E3-019", "section": section, "description": desc, "evidence": evidence, "type": gtype, "area": area, "severity": sev, "needed_by_wave": wave, "legacy_ref": legacy, "owner_role": owner, "asm": asm, "proposed": proposed, "wp": "B-S5-01"}

def asm(i, text, why, read, g, applied, conf="Medium", confirm="", impact=""):
    return {"id": f"ASM-B-S5-01-E3019-{i}", "text": text, "why": why, "read": read, "gap": g, "applied_in": applied, "confidence": conf, "confirm": confirm, "impact": impact, "wp": "B-S5-01"}

gaps = [
 gap(1, "RWB-S5-E3019: the take-on slice has no source for its dependency rows, its event, its case move, its requirement id and the duplicated R-DIS-06 criterion",
     "(1) The plan gives H = RWB-S5-E3019-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON and C, I, X = None, while the step also needs the rwb-source-data data-product read, the rwb-case state and move answer and the DP-09 outbox and inbox library. (2) Architecture v5 slide 19 OUT gives the topic rwb.asset.events.v1 with AssetTakenOn and slide 43 row 22 gives the event two consumers, yet the plan's pattern set (DP03, DP05, DP13, DP19) omits DP-09, so the library dependency and the event have no plan row. (3) No source publishes an operation that moves a case state on behalf of a stage, and the S5 row of slide 13 names no call to P1 while the legacy data table names v_ace_npa_asset. (4) The split plan carries no requirement id and the legacy story master carries none; REQ-S5-001 is read from the program and FSD tables. (5) The legacy masters carry the same R-DIS-06 criterion in RWB-E3-019 AC2 and RWB-E3-023 AC2, so two APP stories own the same words and the build must not run two clocks. (6) The legacy Data table lists v_ace_npa_asset, timer, decision_log_entry and rule_row, none of which this service may read or write.",
     "split_plan.json slices RWB-S5-E3019-APP and -CON with H of three CRs and empty C, I, X; Template and Rules v1 R5.5 rows DP-03, DP-05, DP-09, DP-13 and DP-19; Architecture v5 slide 19 OUT and slide 43 rows 21 and 22; Architecture v5 slides 13, 29, 37 and 45; legacy RWB-E3-019 Data and Test cases tables; legacy RWB-E3-023 AC2 identical to RWB-E3-019 AC2",
     section="Metadata (Depends on (build), Contract dependencies, External dependencies); Sections 2, 3, 4, 7, 11, 12.2, 12.3, 12.4 and 18",
     area="Dependency, event delivery, case boundary and requirement traceability",
     legacy="RWB-E3-019 (sections 4, 7 and 11)",
     asm="ASM-B-S5-01-E3019-1",
     proposed="Keep the plan's H, C, I and X rows as they stand, record the rwb-source-data, rwb-case and DP-09 rows as the dependencies the build actually needs, declare AssetTakenOn from the outbox, read the case move as the workflow stage outcome, and read REQ-S5-001 with the note that the plan carries no requirement id"),
 gap(2, "RWB-S5-E3019: the asset table has no Ownership Map row and rwb-asset holds no ACE view grant while the legacy story reads v_ace_npa_asset",
     "The Ownership Map table list carries listing and asset_sale for S5 and no asset row, although Architecture v5 slides 19 and 41 and TSD S5 T3.1 give the asset record to S5. Separately, the legacy Data table names recovery.v_ace_npa_asset, while Architecture v5 slides 29, 37 and 45 give the 30 recovery.v_ace_* views to rwb-source-data alone and give the S5 row no call to P1, so under R-PREC the ACE fact must arrive on the owner's data-product contract whose operation names are not published.",
     "ownership.json tables: asset_sale S5, listing S5, no asset key; Architecture v5 slide 41 S5 row and slide 19 OUT; TSD S5 T3.1 asset; Architecture v5 slide 29 'only rwb_source_data has SELECT on the views', slide 37 'Views read only by rwb-source-data', slide 45; legacy RWB-E3-019 Data table row v_ace_npa_asset DF-ACE-208 to DF-ACE-219",
     section="Sections 11, 12.2 and 12.7",
     area="Data ownership and ACE read boundary",
     legacy="RWB-E3-019 (section 11)",
     asm="ASM-B-S5-01-E3019-2",
     proposed="Record the asset table as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 and ask the Ownership Map owner to add the row; read the ACE asset fact on the rwb-source-data DP06 Collateral and assets contract with the placeholder on its operation names"),
 gap(3, "RWB-S5-E3019: the published asset event has no DP-09 row in the plan",
     "Architecture v5 slide 19 OUT names the topic rwb.asset.events.v1 with AssetTakenOn and AssetSold and slide 43 row 22 gives AssetTakenOn the consumers rwb-case and rwb-payment, so the take-on must publish. The plan's pattern set for the key is DP03, DP05, DP13 and DP19, so DP-09 and its library RWB-PLT-TE006-CON are absent from the H row, and the story both declares the event and records the missing dependency.",
     "Architecture v5 slide 19 OUT; slide 43 rows 22 and 25; Template and Rules v1 R5.5 DP-09 row ('Outbox and inbox library; Kafka topic of the owner; CloudEvents', H RWB-PLT-TE006-CON); split_plan.json slice H list",
     section="Metadata (Depends on (build)); Sections 4, 12.3, 12.7 and 13",
     area="Event delivery and dependency",
     legacy="RWB-E3-019 (section 7 AC1)",
     asm="ASM-B-S5-01-E3019-3",
     proposed="Declare AssetTakenOn on rwb.asset.events.v1 from the outbox; keep the H row as the plan states it and record RWB-PLT-TE006-CON as the wave 0 library the relay needs"),
 gap(4, "RWB-S5-E3019: the case state read and the case-move answer have no published operation",
     "The step reads the case state and answers ASSET_ON_BOOKS or ASSET_HELD to rwb-case. The Ownership Map carries no case-move operation: the P3 rows are GET /cases, GET /cases/{caseId}, the timeline, accounts, parties, transfer, legal hold, the task and queue operations and the timers, and none of them is a stage outcome. The state and the move are therefore declared as contract shapes with the operation name placeholder.",
     "ownership.json api: P3 rows listed above; Architecture v5 slide 14 rwb-case IN; TSD S5 T5.2 'Calls go through the published Java interfaces: P3 for the case'; legacy RWB-E3-019 AC2 and AC3",
     section="Sections 3, 4, 9, 12.2 and 12.8",
     area="Case boundary and interface",
     legacy="RWB-E3-019 (AC2, AC3)",
     asm="ASM-B-S5-01-E3019-4",
     proposed="Declare the case state read and the move answer as consumed and faked, with the operation name placeholder, and confirm the name with rwb-case before the contract is tagged"),
 gap(5, "RWB-S5-E3019: the module declares no external dependency although the legacy step names RPS, the Field App and AMIS",
     "The legacy Data and rule rows name RPS, the Field App and AMIS as the sources of the repossession result, the condition, the photographs and the location, and TSD S5 T5.1 carries INT-11 SVAF, INT-12 AMIS, INT-13 RPS and INT-27 HOME.SCB. The plan's X row is None because in the target those systems feed ACE and are reached through rwb-source-data, so no external dependency is declared and the trace is kept in the text instead.",
     "legacy RWB-E3-019 Data table and R-DIS-01 Systems column; TSD S5 T5.1; FSD S5 A2.1.2 'Integration points: ACE (v_ace_npa_asset; RPS and AMIS ingested by ACE)'; D-RCV-35",
     section="Metadata (External dependencies); Sections 2, 3 and 19",
     area="External interface and source systems",
     legacy="RWB-E3-019 (sections 4 and 11)",
     asm="ASM-B-S5-01-E3019-5",
     proposed="Keep the X row at None, name RPS, AMIS and the Field App as systems behind the rwb-source-data data product, and record that no direct adapter exists in rwb-asset"),
]

asms = [
 asm(1, "The take-on slice builds against the plan's H row and records the three rows the build also needs as facts rather than adding them to the metadata.",
     "The plan fixes the H, C, I and X rows of every slice; a worker may not rewrite them, yet the step cannot run without the P1, P3 and DP-09 rows.",
     "The rwb-source-data data-product read, the rwb-case state read and move answer and the outbox library RWB-PLT-TE006-CON are named in the text, faked for the build and recorded as missing rows.",
     "CG-B-S5-01-E3019-1", "Sections 3, 4, 12.2, 12.3 and 13",
     confirm="Solution architect and the owners of rwb-source-data, rwb-case and the platform library",
     impact="The story can start on Day 1; the dependency map under-reports three rows until the map is corrected"),
 asm(2, "The asset table is read as S5's in rwb_asset and the ACE asset fact is read only on the rwb-source-data contract.",
     "The Ownership Map has no asset row and rwb-asset holds no v_ace_* grant, while three sources give S5 the asset record and R-PREC puts Architecture v5 above the legacy story.",
     "asset is S5's own table per Architecture v5 slides 19 and 41 and TSD S5 T3.1; DF-ACE-208 to DF-ACE-219 are P1's and arrive through DP06 Collateral and assets.",
     "CG-B-S5-01-E3019-2", "Sections 3, 11, 12.2 and 12.7",
     confirm="Ownership Map owner and the solution architect",
     impact="No ACE grant is requested for rwb-asset and the asset row is created from the data product"),
 asm(3, "AssetTakenOn is published from the outbox on rwb.asset.events.v1 with rwb-case and rwb-payment as its only consumers.",
     "Architecture v5 gives the service the topic and the event with two consumers, while the plan's pattern set omits DP-09.",
     "The event is the catalogue's event 22; the relay is the platform outbox library of DP-09, recorded as an absent H row.",
     "CG-B-S5-01-E3019-3", "Sections 4, 8, 12.3 and 13",
     confirm="Platform library owner and the owners of rwb-case and rwb-payment",
     impact="The event is declared and built; a second event or a direct publish is refused by the absence test"),
 asm(4, "The case move is the stage outcome answered to rwb-case, with no published REST operation name.",
     "No source publishes a case-move operation and the parent CaseWorkflow applies the stage outcome to the case of record.",
     "The state read is the GET /cases family; the move answer carries ASSET_ON_BOOKS or ASSET_HELD with the rule ID and version and is faked.",
     "CG-B-S5-01-E3019-4", "Sections 3, 4, 9 and 12.2",
     confirm="rwb-case owner",
     impact="The step is buildable and testable on Day 1; the name is confirmed before the contract is tagged"),
 asm(5, "RPS, AMIS and the Field App are named as the systems behind the rwb-source-data data product and no direct adapter is built.",
     "The legacy step names them directly while the target gives the ACE ingestion to ACE and the views to rwb-source-data.",
     "The X row stays None; the systems are named in the text as upstream of DP06 Collateral and assets.",
     "CG-B-S5-01-E3019-5", "Sections 2, 3 and 19",
     confirm="Solution architect",
     impact="No external interface is built in this service and the trace to the source systems is kept in prose"),
]

for kind, rows in (("gaps", gaps), ("assumptions", asms)):
    p = os.path.join(W, kind, "B-S5-01.jsonl")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("appended", len(gaps), "gaps and", len(asms), "assumptions")
