"""Write the candidate gap and assumption rows of WP B-TECH-16 (Template and Rules v1 R9).

Keys and order follow R9; numbering stays CG-B-TECH-16-n and ASM-B-TECH-16-n and step D1
renumbers them to GAP-nnnn and ASM-nnnn later.
"""
import json
from pathlib import Path

WP = "B-TECH-16"
S_SRC = "Recovery Workbench System Disposition and Integration Inventory v3.xlsx"
S_RULES = "Recovery Workbench Microservice Story Template and Rules v1"
S_ARCH = "Recovery Workbench Architecture v5 Text Extract v1"
S_MAP = "Recovery Workbench Microservice Ownership Map v1"
S_TD = "Recovery Workbench Temporal and Drools Design Text Extract v1"

GAPS = [
    dict(
        id="CG-B-TECH-16-1",
        title="The By route counts are blank in v2 and v3 although the sheet says they are calculated",
        source=f"{S_SRC}; Recovery Workbench System Disposition and Integration Inventory v2.xlsx",
        section="v3 sheet By route, cells A5 to E10; v2 sheet By route, cells A5 to E10",
        description=(
            "The By route sheet carries the line 'Calculated from the Interfaces tab.' and six rows (COLLINS, File, "
            "Direct through ACE, Through partners, Not at all today and Total) with four count columns (In, Out, Both, "
            "Total), but every count cell is empty in v2 and in v3. The 36 rows of the Interfaces sheet carry the route "
            "and the direction of each interface, so the counts can be calculated without adding a value that no source "
            "gives. Without them a reader cannot check how many interfaces run in, out or both ways per route, and the "
            "statement in the Interfaces description that ACE ingests every inbound source cannot be checked either."),
        evidence=(
            "v3 sheet By route, row 2: 'Calculated from the Interfaces tab.'; rows 5 to 10: 'COLLINS' with every count "
            "cell empty, then 'File', 'Direct through ACE', 'Through partners', 'Not at all today' and 'Total', each "
            "with the same four empty cells. v2 sheet By route: the same six rows and the same empty cells."),
        type="Outdated", area="interfaces", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Solution architect", asm="ASM-B-TECH-16-2",
        proposed=(
            "Calculate the counts from the Interfaces sheet and keep the calculation rule on the sheet (done in v4: "
            "20 In, 12 Out, 4 Both, 36 Total); the owner confirms the route vocabulary, which the Key sheet already "
            "defines, at the next review."),
        wp=WP),
    dict(
        id="CG-B-TECH-16-2",
        title="The data lake row and INT-19 and INT-20 are kept while Architecture v5 removes them",
        source=f"{S_SRC}; {S_ARCH}; {S_RULES}",
        section=(
            "v3 sheet Disposition, row 'Data lake and Power BI'; v3 sheet Interfaces, rows INT-19 and INT-20; "
            "Architecture v5 slides 2, 7, 9 and 37; Template and Rules v1 R5.5 DP-17"),
        description=(
            "Version 3 keeps the system 'Data lake and Power BI' with disposition 'Keep and feed' and the interfaces "
            "INT-19 (case, queue, decision and outcome data for reporting, out, file, daily) and INT-20 (decisions and "
            "outcomes to COLLINS for model learning, out, daily batch to the data lake), both owned by the Workbench. "
            "Architecture v5 removes the data lake: slide 2 notes 'Recovery has no connection to the data lake; "
            "INT-19/INT-20 are removed', slide 7 says 'No data lake or Power BI connection (INT-19/20 removed)', slide 9 "
            "says the data lake and Power BI are not connected, and slide 37 lists the data lake and Power BI feed among "
            "the parts that go. DP-17 and ADR-018 replace the feed with a read model in rwb-reporting built from events "
            "and call for a gap where a story needs lake data. This work package keeps every section, ID and row of the "
            "source, so the three rows stay with their v3 wording and carry P9 rwb-reporting as the owning service; the "
            "build story for them is not raised."),
        evidence=(
            "v3 sheet Disposition: 'Data lake and Power BI | Bank reporting | Keep and feed | Not applicable | Workbench | "
            "Receives case, queue, decision and outcome data daily | E1 | INT-19 | None'. v3 sheet Interfaces: 'INT-19 | "
            "Data lake and Power BI | ... | Out | File | Daily batch | Daily | DP03, DP12 | Not applicable | Workbench | "
            "E1 | File specification | None' and 'INT-20 | COLLINS | ... | Out | File | Daily batch to the data lake | "
            "Daily | DP12 | Not applicable | Workbench | E2 | File specification | None'. Architecture v5 slide 2 note, "
            "slide 7, slide 9 and slide 37. Template and Rules v1 R5.5 DP-17: 'Removed (no data lake); reporting from "
            "events into rwb-reporting; none; gap if the story needs lake data'."),
        type="Conflict", area="interfaces", severity="P2", needed_by_wave=1, legacy_ref="",
        owner_role="Solution architect", asm="ASM-B-TECH-16-4",
        proposed=(
            "Keep the three rows in this inventory and record them as removed from build. If the business needs a "
            "reporting output, raise it as a new interface with a free ID against rwb-reporting when the reporting read "
            "model is specified; serve model learning from the decision records on rwb.decision-record.v1 (P7) if it is "
            "still needed, as the Temporal and Drools design describes."),
        wp=WP),
    dict(
        id="CG-B-TECH-16-3",
        title="Four services own no row of the disposition or the interface inventory",
        source=f"{S_SRC}; {S_ARCH}",
        section="v3 sheets Disposition and Interfaces, all rows; Architecture v5 slides 14 to 20 and 45",
        description=(
            "With the Service column filled, P3 rwb-case, S1 rwb-valuation, S2 rwb-treatment and S7 rwb-writeoff own no "
            "row of either sheet, although each has a contract of its own in Architecture v5. The reason is the shape of "
            "the source: it inventories the systems and the interfaces around recovery, and these four services consume "
            "those paths through P1 rwb-source-data and P2 rwb-integration instead of owning one. The inventory therefore "
            "reads as complete for the paths but not for the consumers, and a reader cannot see from it which service "
            "uses the write-off postings of INT-16 or the credit decision of INT-35."),
        evidence=(
            "v3 sheet Interfaces row INT-16: 'GL | Write-off postings | In | File | ACE ingests the file | Monthly | DP13', "
            "owner ACE team; Architecture v5 slide 20 gives rwb-writeoff 'REST Source data: GL outcome'. v3 row INT-35 "
            "reads the NLEADS credit decision through v_ace_credit_decision; Architecture v5 slide 18 gives rwb-treatment "
            "the credit pack and the restructure calculator through rwb-integration. Slide 45: 'Only rwb-source-data reads "
            "the 30 recovery.v_ace_* views ... Everyone else asks it through REST or a Temporal activity'."),
        type="Ambiguous", area="interfaces", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Solution architect", asm="ASM-B-TECH-16-13",
        proposed=(
            "Record the consumer of each path on the Service rules sheet when the Service Contract Catalog is next "
            "revised; no row is added here, because the inventory counts systems and interfaces and not consumers."),
        wp=WP),
    dict(
        id="CG-B-TECH-16-4",
        title="No source names an owning service for any system or interface",
        source=f"{S_SRC}; {S_MAP}; {S_ARCH}; {S_RULES}",
        section="v3 sheets Disposition and Interfaces, column Owner; Ownership Map v1, all sheets; Architecture v5 slides 13 to 20 and 41; Template and Rules v1 R5.5",
        description=(
            "The Service column that the realignment asks for has no source value. Version 3 gives an Owner of 'ACE "
            "team', 'Workbench' or 'Bank platform' on every row and names no service anywhere in the workbook; the "
            "Ownership Map v1 owns tables, endpoints, events and jobs and has no system or interface sheet. The owning "
            "service of each row is therefore derived from the scope of the 19 services in Architecture v5 and from "
            "ADR-010, and the derivation is written on the new Service rules sheet, one rule per path group (SR-01 to "
            "SR-19), so each filled cell can be traced to a slide, an ADR or an Ownership Map ruling."),
        evidence=(
            "v3 sheet Disposition column E reads 'ACE team', 'Workbench' or 'Bank platform' on all 25 rows; v3 sheet "
            "Interfaces column J reads the same three values on all 36 rows. Ownership Map v1 sheets: Read me, Services, "
            "Tables, FK cuts, Endpoints (and the event, job and workflow sheets) - no system and no interface. "
            "Architecture v5 slide 41 gives the data ownership per service."),
        type="Missing", area="ownership", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Solution architect", asm="ASM-B-TECH-16-3",
        proposed=(
            "Confirm the 19 rules on the Service rules sheet with the architecture owner; where a rule changes, the "
            "Service cells of the rows it covers change with it."),
        wp=WP),
    dict(
        id="CG-B-TECH-16-5",
        title="The data product of INT-06 (AAL) reads To confirm",
        source=f"{S_SRC}",
        section="v3 sheet Interfaces, row INT-06, column Data product",
        description=(
            "INT-06 carries the data product 'To confirm' where every other interface names a DP number or 'None'. The "
            "row is the AAL feed, 'Data ACE already receives through COLLINS', and the disposition row for AAL says ACE "
            "ingests the data through COLLINS and the Workbench reads it through the account and customer views. The "
            "value is the marker of a missing answer and not a data product, so it is kept character for character and "
            "no DP number is assigned in this version."),
        evidence=(
            "v3 sheet Interfaces: 'INT-06 | AAL | Data ACE already receives through COLLINS | In | COLLINS | ACE ingests "
            "the COLLINS batch | Daily, end of day | To confirm | Yes | ACE team | E1 | File specification | DL12'. v3 "
            "sheet Disposition row AAL: 'Data ACE already receives | Keep | Yes | ACE team | ACE ingests the data through "
            "COLLINS and the Workbench reads it through the account and customer views'."),
        type="Missing", area="data", severity="P2", needed_by_wave=1, legacy_ref="",
        owner_role="Data architect", asm="ASM-B-TECH-16-5",
        proposed=(
            "Name the data product of INT-06 from the Logical Data Model and Data Dictionary and the data product "
            "catalogue at the next revision of the interface specifications."),
        wp=WP),
    dict(
        id="CG-B-TECH-16-6",
        title="INT-33 (Legal Execution Department and courts) has no standard and two candidate services",
        source=f"{S_SRC}; {S_ARCH}",
        section="v3 sheet Interfaces, row INT-33, columns Standard and Decision; Architecture v5 slides 17 and 19",
        description=(
            "INT-33 arrives 'Through partners', entered by the law firms in the partner portal, and its Standard and "
            "Decision cells read 'None'. The path spans two services: S4 rwb-litigation owns enforcement and court "
            "records, and S9 rwb-partner owns the partner instruction and the result the partner reports. The inventory "
            "records S4 as the owning service and keeps the partner entry on the Service rules sheet (SR-14). The "
            "standard stays 'None', because the contract of the partner gateway is specified in the partner portal "
            "design and not here."),
        evidence=(
            "v3 sheet Interfaces: 'INT-33 | Legal Execution Department and courts | Enforcement and court records | In | "
            "Through partners | Through the law firms in the partner portal | As entered | DP07 | Not applicable | "
            "Workbench | E5 | None | None'. Architecture v5 slide 8: 'Partners use the partner gateway (FAPI 2.0) that "
            "fronts rwb-partner'; slide 19 gives rwb-litigation legal actions, hearings, judgments and enforcement and "
            "rwb-partner the instruction and the result."),
        type="Ambiguous", area="interfaces", severity="P3", needed_by_wave=5, legacy_ref="",
        owner_role="Solution architect", asm="ASM-B-TECH-16-9",
        proposed=(
            "Decide whether INT-33 is a partner-result interface under S9 or an enforcement record under S4, and give it "
            "the standard of the partner gateway contract when the partner portal is built."),
        wp=WP),
    dict(
        id="CG-B-TECH-16-7",
        title="Three statements of v3 read as outdated and are kept word for word",
        source=f"{S_SRC}; {S_ARCH}",
        section="v3 sheet Interfaces, description row 2; v3 sheet Disposition, description row 2; Architecture v5 slides 8 and 37",
        description=(
            "The Interfaces description says 'The Workbench owns its outbound files, the reporting feeds and the partner "
            "portal'; Architecture v5 has no reporting feed, and the partner portal sits behind the partner gateway in "
            "front of rwb-partner. The Disposition description says 'Supersedes v2', which was true of v3 and is not "
            "true of this version. The rest of the same sentences stays right: ACE ingests every inbound source, the "
            "Workbench owns the outbound files, and SMS, LINE and the audit logs leave through ACE paths. The rule of "
            "the run is to keep every value of the source and to change only what the realignment needs, so the three "
            "statements are unchanged and recorded here."),
        evidence=(
            "v3 sheet Interfaces row 2: '36 numbered interfaces with 32 systems. ACE ingests every inbound source ... The "
            "Workbench owns its outbound files, the reporting feeds and the partner portal ...'. v3 sheet Disposition "
            "row 2: '25 systems and tools that recovery uses today, what happens to each, who owns the data path and "
            "when. Supersedes v2.' Architecture v5 slide 37 removes the data lake and Power BI feed; slide 8 replaces "
            "the external gateway with the partner gateway."),
        type="Outdated", area="documentation", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Solution architect", asm="ASM-B-TECH-16-10",
        proposed=(
            "Reword the two description rows at the next full revision of the inventory; the individual rows of the "
            "sheets give the owning service in the Service column meanwhile."),
        wp=WP),
    dict(
        id="CG-B-TECH-16-8",
        title="The partner portal row keeps the wording of the external gateway",
        source=f"{S_SRC}; {S_ARCH}",
        section="v3 sheet Disposition, row 'Partner portal'; v3 sheet Interfaces, row INT-24, column Path; Architecture v5 slide 8; ADR-019",
        description=(
            "The disposition row for the partner portal says the screens run 'through the external gateway', and INT-24 "
            "gives the path 'Workbench screens through the external gateway' with OpenAPI 3.1. Architecture v5 slide 8 "
            "replaces the external gateway with the partner gateway (FAPI 2.0) in the DMZ that fronts rwb-partner, and "
            "ADR-019 records the edge decision. The two cells are kept as written; the Service column names S9 "
            "rwb-partner, and the Service rules sheet records the gateway behind that choice."),
        evidence=(
            "v3 sheet Disposition 'Partner portal': 'Does not exist | New | No | Workbench | Workbench screens for law "
            "firms, auction houses and buyers through the external gateway; needs the architecture change with one to "
            "three months of lead time | E5 | INT-24, INT-25 | DL03'. v3 sheet Interfaces INT-24: 'Both | Direct through "
            "ACE | Workbench screens through the external gateway | As entered | DP06, DP07, DP08'. Architecture v5 "
            "slide 8: 'Partners use the partner gateway (FAPI 2.0) that fronts rwb-partner'."),
        type="Conflict", area="interfaces", severity="P3", needed_by_wave=2, legacy_ref="",
        owner_role="Solution architect", asm="ASM-B-TECH-16-11",
        proposed=(
            "Reword both cells to the partner gateway (FAPI 2.0) at the next full revision, and confirm the direction "
            "and the standard of INT-24 against the partner gateway contract."),
        wp=WP),
]

ASM = [
    dict(
        id="ASM-B-TECH-16-1",
        text="The System Disposition and Integration Inventory v4 is issued in Draft status with no approval recorded.",
        why=("This run is the D-RCV-60 realignment: no human approval step is available, the run must not stop for one, "
             "and the overlay records the missing status as an assumption."),
        read=("Every row of v4 may be cited by the architecture, requirements and story documents of this run as the "
              "disposition and integration inventory, in Draft, and the approval is recorded afterwards by the owner of "
              "the architecture set."),
        gap="", applied_in="Read me sheet, status line", confidence="High", confirm="Architecture owner",
        impact=("If the architecture owner rejects a Service cell, the affected rows and the three sheets that count "
                "them (By service, Service rules, Realignment changes) change together."), wp=WP),
    dict(
        id="ASM-B-TECH-16-2",
        text=("The In, Out, Both and Total counts of the By route sheet are calculated from the 36 interfaces: 20 In, "
              "12 Out, 4 Both and 36 in all."),
        why=("The sheet states that it is calculated from the Interfaces tab but every count cell is empty in v2 and "
             "v3; the route and the direction of each interface are source values, so the count adds no value that no "
             "source gives."),
        read=("COLLINS 8 In and no Out; File 8 In and 4 Out; Direct through ACE 1 In, 3 Out and 3 Both; Through partners "
              "1 In; Not at all today 2 In, 5 Out and 1 Both; Total 20, 12, 4 and 36."),
        gap="CG-B-TECH-16-1", applied_in="By route sheet, rows 5 to 10; Realignment changes R-09",
        confidence="High", confirm="Solution architect",
        impact="If an interface changes route or direction the counts change with it; the verify script recounts them from the Interfaces sheet.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-3",
        text=("Every Service cell is derived from the Microservice Ownership Map v1 and the scope of the 19 services in "
              "Architecture v5: the inbound ACE path goes to P1 rwb-source-data (ADR-010), the outbound file path to P2 "
              "rwb-integration unless a route service owns the content, and the route or platform service for the rest. "
              "The rule behind each group is on the Service rules sheet, SR-01 to SR-19."),
        why=("No source names an owning service for a system or an interface, and the realignment requires the column on "
             "every row."),
        read=("The 36 interfaces: P1 rwb-source-data 17, P6 rwb-comms 3, S5 rwb-asset 3, P2 rwb-integration 2, P9 "
              "rwb-reporting 2, and P4 rwb-access, P8 rwb-payment, P10 rwb-agent, PLT (RWB-PLT-OBS), S3 rwb-guarantee, "
              "S4 rwb-litigation, S6 rwb-debtsale, S8 rwb-deviation and S9 rwb-partner 1 each. The 25 systems: 15 rows "
              "lead with P1 rwb-source-data and 9 name one service per interface."),
        gap="CG-B-TECH-16-4",
        applied_in=("Disposition and Interfaces sheets, Service column; By service sheet; Service rules sheet; "
                    "Realignment changes R-02, R-03, R-04, R-08"),
        confidence="High", confirm="Solution architect",
        impact=("A rule that changes moves every row it covers; the By service counts and the Read me counts are "
                "recalculated from the Service column."), wp=WP),
    dict(
        id="ASM-B-TECH-16-4",
        text=("INT-19 and INT-20 and the disposition row 'Data lake and Power BI' are kept with the wording and the IDs "
              "of v3 and carry P9 rwb-reporting as the owning service; no build story is raised for them under DP-17 "
              "and ADR-018."),
        why=("The work package keeps every ID of the source and changes only what the realignment needs; Architecture v5 "
             "removes the data lake, so the rows cannot be built, and dropping them would lose two IDs the document set "
             "may still cite."),
        read=("A reader sees the three rows as v3 wrote them, with P9 as the service, and the Read me open point, the Key "
              "row and the Realignment changes row record that they are not built. The reporting story uses the "
              "rwb-reporting read model instead."),
        gap="CG-B-TECH-16-2",
        applied_in=("Disposition row 'Data lake and Power BI'; Interfaces rows INT-19 and INT-20; Key sheet; Read me "
                    "open points; Realignment changes R-06"),
        confidence="High", confirm="Solution architect",
        impact=("If the business later needs the reporting or model-learning output, a new interface with a free ID is "
                "raised against P9 or P7; the three rows stay as the record of what v3 said."), wp=WP),
    dict(
        id="ASM-B-TECH-16-5",
        text="The data product of INT-06 stays 'To confirm' and no DP number is assigned.",
        why=("The value is the source's own marker of a missing answer; assigning a DP number would invent a data product "
             "that the interface specifications and the data product catalogue do not give."),
        read=("The row keeps the marker, and the open point of the Read me and the gap row carry the question. Every "
              "other interface row keeps its DP number or 'None' character for character."),
        gap="CG-B-TECH-16-5", applied_in="Interfaces sheet, row INT-06; Read me open points",
        confidence="High", confirm="Data architect",
        impact="The data product catalogue of P1 and the interface specifications must agree before the AAL feed is built.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-6",
        text=("An inbound interface that ACE ingests stays owned by the ACE team and carries P1 rwb-source-data as its "
              "owning service, because only rwb-source-data reads the 30 recovery.v_ace_* views."),
        why=("ADR-010 and Architecture v5 slides 7, 9 and 29 keep the views in the hands of rwb-source-data alone, and "
             "v3 gives the inbound rows the ACE team as owner and no Recovery-side service."),
        read=("The Owner cells keep the source values; the Service cell of every inbound ACE row reads P1 rwb-source-data "
              "and the Service rules sheet gives the rule (SR-01)."),
        gap="", applied_in="Interfaces sheet, 17 inbound rows; Disposition sheet, the inbound systems",
        confidence="High", confirm="Solution architect",
        impact="If a later change lets a service read a view directly, ADR-010 is revisited first and the affected Service cells change with it.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-7",
        text=("An outbound interface is owned by P2 rwb-integration when no route service owns the content, and by the "
              "route service when one does: P6 rwb-comms for INT-14, S6 rwb-debtsale for INT-25 and P9 rwb-reporting "
              "for INT-19 and INT-20."),
        why=("Architecture v5 slide 16 gives rwb-integration the interface config, the file runs, the outbound items and "
             "the ACE integration paths, while slides 15, 17 and 19 give rwb-comms the notice, rwb-debtsale the lot and "
             "rwb-reporting the extract; the Ownership Map ruling for JOB-10 splits the WIN path the same way."),
        read=("The Service cell names one service, the content owner, and the Service rules sheet names rwb-integration "
              "for the file build and transfer (SR-03, SR-09, SR-10)."),
        gap="", applied_in="Interfaces rows INT-14, INT-19, INT-20, INT-25; Service rules SR-03, SR-09, SR-10",
        confidence="Medium", confirm="Solution architect",
        impact="If rwb-integration is given the file contract of a route service, the Service cells of the file rows move to P2.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-8",
        text="INT-03 (restructure, settlement and write-off bookings) carries P8 rwb-payment as its owning service.",
        why=("The route is 'Not at all today' and the officer books in the core bank, but the target gives rwb-payment the "
             "bookings and the posting files (Architecture v5 slide 17), which is the only service whose scope covers a "
             "booking path."),
        read=("The row keeps Direction Out, Route 'Not at all today' and Path 'Booked by the officer; confirmed on the "
              "next day's load'; only the Service cell is new."),
        gap="", applied_in="Interfaces row INT-03; Service rules SR-02", confidence="Medium",
        confirm="Solution architect",
        impact="If booking confirmation stays entirely inside the core bank, the row needs no service and the cell is cleared in the next version.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-9",
        text=("INT-33 carries S4 rwb-litigation as its owning service, with S9 rwb-partner for the partner entry, and "
              "keeps Standard 'None'."),
        why=("Architecture v5 slide 19 gives rwb-litigation enforcement and court records and slide 17 gives rwb-partner "
             "the partner instruction and result; the source names neither and gives no standard."),
        read=("The Service cell reads S4 rwb-litigation, the Service rules sheet records the partner entry (SR-14), and "
              "the Standard and Decision cells stay 'None'."),
        gap="CG-B-TECH-16-6", applied_in="Interfaces row INT-33; Service rules SR-14; Read me open points",
        confidence="Medium", confirm="Solution architect",
        impact="The partner portal design decides whether the path moves to S9 and whether a standard is added.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-10",
        text=("The three statements of v3 that read as outdated are kept word for word: the Interfaces description on the "
              "reporting feeds, the Disposition description 'Supersedes v2', and the partner portal wording."),
        why=("The rule of the run is to keep every value of the source and to change only what the realignment needs; "
             "rewording a description row is a documentation edit for the owner of the inventory."),
        read=("The rows stay as written and the gap row records them; the Service column gives the owning service of "
              "every path meanwhile."),
        gap="CG-B-TECH-16-7", applied_in="Disposition row 2; Interfaces row 2; Read me open points",
        confidence="High", confirm="Solution architect",
        impact="The next full revision of the inventory rewords the two descriptions; nothing else depends on them.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-11",
        text=("The partner portal row and INT-24 keep the external gateway wording and carry S9 rwb-partner as the "
              "owning service."),
        why=("Architecture v5 slide 8 puts the partner gateway (FAPI 2.0) in front of rwb-partner and ADR-019 records the "
             "edge decision, while the source still says external gateway; the value is kept and the owner is derived."),
        read=("The Path cell stays as written, the Service cell reads S9 rwb-partner, and the Service rules sheet names "
              "the partner gateway (SR-08)."),
        gap="CG-B-TECH-16-8", applied_in="Disposition row 'Partner portal'; Interfaces row INT-24; Service rules SR-08",
        confidence="Medium", confirm="Solution architect",
        impact="When the partner gateway contract is written, the two cells are reworded and the standard of INT-24 is confirmed.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-12",
        text=("INT-21 carries P4 rwb-access, INT-22 PLT (RWB-PLT-OBS), INT-23 P10 rwb-agent, INT-24 S9 rwb-partner and "
              "INT-34 P2 rwb-integration."),
        why=("Architecture v5 slide 30 gives the capability each service consumes: sign-in and access checks to "
             "rwb-access, audit and PII logging to every service through the platform sender, the model endpoint to "
             "rwb-agent, the partner results to rwb-partner; slide 7 and slide 16 give rwb-integration the ACE Common "
             "contract and the ACE integration paths."),
        read=("Each row carries one service; the Service rules sheet gives the slide behind each one (SR-05 to SR-08 and "
              "SR-19); the Owner cells keep ACE team and Bank platform."),
        gap="", applied_in="Interfaces rows INT-21, INT-22, INT-23, INT-24, INT-34; Service rules SR-05 to SR-08, SR-19",
        confidence="High", confirm="Solution architect",
        impact="ACE Common has five consumers and no single owner in the source; the contract owner P2 is the reading of the source that keeps one Service cell per row.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-13",
        text=("P3 rwb-case, S1 rwb-valuation, S2 rwb-treatment and S7 rwb-writeoff own no row of the inventory, because "
              "they consume the paths through P1 and P2 rather than owning one."),
        why=("The inventory counts systems and interfaces, not consumers, and the source gives no consuming service "
             "anywhere; adding a consumer column would change rows the realignment does not ask to change."),
        read=("The Read me counts state 16 of the 20 owner entries and name the four services that own no row; the "
              "Service rules sheet gives the paths they use."),
        gap="CG-B-TECH-16-3", applied_in="Read me counts; Service rules SR-02, SR-10, SR-11",
        confidence="Medium", confirm="Solution architect",
        impact="A later revision may add the consumer of each path to the Service rules; the rows themselves stay as they are.",
        wp=WP),
    dict(
        id="ASM-B-TECH-16-14",
        text=("Every other cell of the workbook is unchanged: the 25 disposition rows and the 36 interface rows keep "
              "every source value, the Key sheet keeps its 27 rows and gains six, and the four source sheets keep their "
              "titles and description rows."),
        why=("The rule of the run is to keep every section, ID, number and date of the source and to change only what the "
             "realignment needs, which is the Service column, the calculated counts and the document control."),
        read=("A reader can diff v4 against v3 and find one new cell per data row and nothing else; the verify script "
              "does exactly that cell by cell."),
        gap="", applied_in="All sheets; Realignment changes R-14", confidence="High", confirm="Reviewer",
        impact="Any further change to a source cell is a new gap row.", wp=WP),
    dict(
        id="ASM-B-TECH-16-15",
        text=("The workbook properties are set to the organisation and the tool: creator Henka Group, last modified by "
              "T3 Code / OpenCode / DeepSeek v4.1 Flash, title v4, revision 4, dated 22 November 2026."),
        why=("The source workbook carries a person name in the author and last-modified-by properties, and root rule 4 "
             "forbids the name of a person anywhere in the output."),
        read=("The properties name no person and no email address; the build and the verify scripts check both."),
        gap="", applied_in="Workbook core properties; Realignment changes R-13", confidence="High",
        confirm="Reviewer",
        impact="None on the content; a reader of the file properties sees the organisation and the tool.", wp=WP),
    dict(
        id="ASM-B-TECH-16-16",
        text=("No release date is added and no date is raised: the source carries none, and any release date written "
              "into the workbook later is tentative."),
        why=("Dates stay unchanged and tentative (U7, DL48) and a date is never raised as a gap; the release line of the "
             "Read me says so in words."),
        read=("The From column keeps the epic codes E1 to E8 of the source, the change-log row carries 22 November 2026, "
              "and no other date appears in the workbook."),
        gap="", applied_in="Read me sheet, release line and change log", confidence="High", confirm="Programme office",
        impact="A release date added later is marked tentative in the same cell.", wp=WP),
]

for path, rows in ((Path("_work/msr/gaps") / f"{WP}.jsonl", GAPS),
                   (Path("_work/msr/assumptions") / f"{WP}.jsonl", ASM)):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print("WROTE", path, len(rows), "rows")
