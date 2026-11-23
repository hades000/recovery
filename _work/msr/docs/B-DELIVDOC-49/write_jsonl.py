"""Writes the gap and assumption candidate rows for B-DELIVDOC-49 (D1 numbers them)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
G = ROOT / "_work/msr/gaps/B-DELIVDOC-49.jsonl"
A = ROOT / "_work/msr/assumptions/B-DELIVDOC-49.jsonl"
WP = "B-DELIVDOC-49"
SRC = "11 Delivery and operations/Recovery Workbench Resource Plan and Team Structure v2.xlsx"
OM = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"

gaps = [
    dict(id="CG-B-DELIVDOC-49-1",
         title="The source workbook records no version, version date, change log or tool line",
         source=SRC, section="Document control (Read me)",
         description="Version 2 has four sheets (Team, People by month, Structure, Accountability) and no change-log sheet. "
                     "It states no version number, no version date and no tool line, so the change-log row of version 3 has "
                     "nothing to copy for version 2. No release date is involved.",
         evidence="Sheets of the v2 workbook: Team, People by month, Structure, Accountability; no cell of the four sheets holds "
                  "a version, a version date, a change log or a tool line.",
         type="Missing", area="documentation", severity="P3", needed_by_wave="0", legacy_ref="",
         owner_role="Program manager",
         asm="ASM-B-DELIVDOC-49-1",
         proposed="Record the version 2 row as 'not stated in the source workbook' and add the R8.1 header, the change-log row and "
                  "the tool line in the new Read me sheet of version 3.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-2",
         title="Two recovery squads and fourteen source module names do not map one to one onto nineteen services",
         source=SRC, section="Structure; Team; People by month",
         description="The Structure sheet gives two recovery squads and fourteen module names (data engine, case and workflow, "
                     "rules component, access, valuation and route, assets and auction, deviations, document hub, communications, "
                     "decision center and log, settlement, litigation, debt sale, write-off). Architecture v5 has nineteen services, "
                     "and no source states which squad carries which service, how many people each service needs, or how the "
                     "9.5 program and 7 data and business full-time equivalents split across the five waves.",
         evidence="Structure sheet rows 'Recovery squad 1' and 'Recovery squad 2'; Team and People by month sheets hold no service "
                  "dimension; Ownership Map v1 Services sheet lists 19 services.",
         type="Missing", area="delivery", severity="P2", needed_by_wave="1", legacy_ref="",
         owner_role="Product owner with the two tech leads and the program manager",
         asm="ASM-B-DELIVDOC-49-2",
         proposed="Keep the squad and module words of version 2, and put the service, the source module and the squad side by side on "
                  "the Services and squads sheet. Record the story slices and legacy stories per service from the plan. The "
                  "per-service headcount stays open.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-3",
         title="Six services have no source module and no squad in the resource plan",
         source=SRC, section="Structure; Services and squads",
         description="rwb-integration (P2), rwb-payment (P8), rwb-reporting (P9), rwb-agent (P10), rwb-guarantee (S3) and "
                     "rwb-partner (S9) exist in Architecture v5 and in the Ownership Map v1, but no module of the Structure sheet "
                     "names them and the Team sheet has no row for them. The source says the split between the squads is agreed at "
                     "the first daily review, which has not happened in this run.",
         evidence="Structure sheet module lists hold no integration, payment, reporting, agent, guarantee or partner module; "
                  "Services sheet of the Ownership Map v1 lists P2, P8, P9, P10, S3 and S9.",
         type="Missing", area="delivery", severity="P2", needed_by_wave="1", legacy_ref="",
         owner_role="Product owner with the two tech leads",
         asm="ASM-B-DELIVDOC-49-3",
         proposed="Carry the R9 placeholder for the squad of the six services on the Services and squads sheet, and let the first "
                  "daily review assign them as the Structure sheet says.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-4",
         title="The wave 0 platform epics have no team, no full-time equivalent and no accountable role",
         source=SRC, section="Team; Structure; Team types and resources",
         description="Template and Rules R5.1 puts seven platform epics in wave 0 (service template, shared libraries, Temporal "
                     "platform, ACE DB schemas, Kafka event platform, edge, observability) and R5.7 rule 6 requires Day-1 work for "
                     "every team type. The resource plan records no platform team, no platform full-time equivalent and no "
                     "accountable role, so wave 0 has no staffing basis in the source.",
         evidence="Team sheet has no platform row; Structure sheet lists supporting teams only as shared; Ownership Map v1 has no "
                  "team column; Temporal and Drools Design slide 23 gives the four reusable layers to the platform team.",
         type="Missing", area="delivery", severity="P1", needed_by_wave="0", legacy_ref="RWB-PLT-TPL",
         owner_role="IT lead with the platform team",
         asm="ASM-B-DELIVDOC-49-4",
         proposed="Name the platform team owner for RWB-PLT-TPL, LIB, WF, DB, EVT, EDGE and OBS, and record its full-time "
                  "equivalents before wave 0 starts. Until then the sheet carries the R9 placeholder.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-5",
         title="The DevOps team type has no full-time equivalent in the resource plan",
         source=SRC, section="Team; People by month; Team types and resources",
         description="Template and Rules R5.3 makes the DevOps team the suggested owner of every OPS story, and the plan has OPS "
                     "stories in every wave (the pipeline, Helm chart, KEDA scaling, outbox relay, worker deployments and "
                     "observability). The Team and People by month sheets have no DevOps row and the Total row counts none.",
         evidence="Team sheet: 24 rows, no DevOps role; People by month sheet: 20 role rows, none DevOps; the Total row of that "
                  "sheet sums the 20 rows to 29.5.",
         type="Missing", area="delivery", severity="P2", needed_by_wave="0", legacy_ref="",
         owner_role="IT lead",
         asm="ASM-B-DELIVDOC-49-5",
         proposed="Add the DevOps full-time equivalents to the plan of the next version, or state that the pipeline work is carried "
                  "by the TechX squads. The sheet records 0 and the placeholder instead of inventing a number.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-6",
         title="SCB IT infrastructure has no full-time equivalent and appears only as a shared supporting team",
         source=SRC, section="Team; Structure; Team types and resources",
         description="Template and Rules R5.3 makes SCB IT infrastructure the suggested owner of every INF story (AKS namespace, "
                     "Kafka topic ACLs and quotas, Temporal namespace quotas, keys and certificates, the network path to ACE). The "
                     "Structure sheet names 'SCB IT security, architecture team' under supporting teams and the People by month "
                     "sheet does not count them.",
         evidence="Structure sheet row 'Supporting teams: Data engineering, Enterprise AI, Autonomous Ops, SCB IT security, "
                  "architecture team'; People by month note 'Shared teams are not counted'.",
         type="Missing", area="delivery", severity="P2", needed_by_wave="0", legacy_ref="",
         owner_role="IT lead",
         asm="ASM-B-DELIVDOC-49-6",
         proposed="Confirm the infrastructure capacity as a shared service with named working agreements per wave; the plan records "
                  "the placeholder, not a number.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-7",
         title="The QA team type is staffed inside the TechX squads and has no separate capacity line",
         source=SRC, section="Team; People by month; Team types and resources",
         description="Template and Rules R5.3 gives the QA team the harness and the NFR stories, and R5.7 rule 6 requires Day-1 "
                     "work for that team type. The source staffs one QA engineer per recovery squad under Organization TechX, so the "
                     "QA capacity is two full-time equivalents inside the twelve TechX and is not visible as a team of its own.",
         evidence="Team sheet: 'Recovery squad 1 | QA engineer | TechX | 1' and 'Recovery squad 2 | QA engineer | TechX | 1'; "
                  "Template and Rules R5.3 ITG row.",
         type="Ambiguous", area="delivery", severity="P3", needed_by_wave="1", legacy_ref="",
         owner_role="QA lead with the program manager",
         asm="ASM-B-DELIVDOC-49-7",
         proposed="State that the QA team type is served by the QA engineers of the two squads, and record the integration harness "
                  "and NFR stories against it.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-8",
         title="The phrase 'TechX' and the source rows 'Recovery squad 1 and 2 (Organization TechX)' use two vocabularies",
         source=SRC, section="Team; Team types and resources",
         description="Template and Rules R5.3 names the team type TechX; the resource plan names the squads Recovery squad 1 and "
                     "Recovery squad 2 and puts TechX in the Organization column. The two vocabularies are not reconciled in any "
                     "source, and the counts are described as following 'the assumed squad shape until the named team is "
                     "confirmed (DL36)', which predates the nineteen-service shape.",
         evidence="Team sheet Organization column value 'TechX' on the eight squad rows; Team sheet note line 2; Template and Rules "
                  "R5.3 work-type table.",
         type="Ambiguous", area="documentation", severity="P3", needed_by_wave="0", legacy_ref="",
         owner_role="Program manager",
         asm="ASM-B-DELIVDOC-49-8",
         proposed="Read TechX as the organisation of Recovery squad 1 and Recovery squad 2 and keep both names, as version 3 does "
                  "on the Team types and resources sheet.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-9",
         title="The accountability text is module based and names the recovery module that no longer exists as one unit",
         source=SRC, section="Team; Accountability; Structure",
         description="Rows such as 'Design within the module, code review, merges into the recovery module' and 'Screens in the ACE "
                     "front end' describe the monolith, while ADR-013 and Architecture v5 give one repository, one schema and one "
                     "pipeline per service. The rows are kept word for word, so the service-level reading is not stated in the "
                     "source at all.",
         evidence="Team sheet 'Accountable for' column, 24 rows; Architecture v5 slide 20 and the ADR-013 position on 19 services.",
         type="Outdated", area="documentation", severity="P3", needed_by_wave="1", legacy_ref="",
         owner_role="Solution architect",
         asm="ASM-B-DELIVDOC-49-9",
         proposed="Keep the twenty-four rows word for word and state the service-level reading next to them, as the Ownership by "
                  "team type sheet does with the contract, schema, topic and queue owner of every service.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-10",
         title="The shared Epic 2 items of DL30 are not identified per service",
         source=SRC, section="Team; Structure",
         description="The Structure sheet gives the Collection squad 'the collection module and shared Epic 2 items (DL30)' and the "
                     "Team sheet repeats it. Which Epic 2 items are shared, and which service owns them after the split, is not "
                     "stated in any source read in this work package.",
         evidence="Structure sheet row 'Collection squad'; Team sheet row 'Collection squad'; no list of the shared items in the "
                  "resource plan.",
         type="Missing", area="delivery", severity="P3", needed_by_wave="2", legacy_ref="RWB-E2",
         owner_role="Product owner with the Collection squad and P3 rwb-case",
         asm="ASM-B-DELIVDOC-49-10",
         proposed="Keep the shared items with the Collection squad as the source says and list them per service when the Epic 2 "
                  "BRD names them.",
         wp=WP),
    dict(id="CG-B-DELIVDOC-49-11",
         title="No approval of the resource plan is recorded",
         source=SRC, section="Read me; Document status",
         description="The source workbook carries no approval, no sign-off table and no status field, and this run has no approval "
                     "step. The new version therefore has no approved baseline to point at.",
         evidence="The four sheets of version 2 hold no status or approval cell; the run overlay records no approval for D-RCV-60.",
         type="Missing", area="governance", severity="P3", needed_by_wave="1", legacy_ref="",
         owner_role="Program manager with the business lead",
         asm="ASM-B-DELIVDOC-49-11",
         proposed="Issue version 3 as Draft and record the missing approval as an assumption, as AGENTS.md rule 9 requires.",
         wp=WP),
]

assumptions = [
    dict(id="ASM-B-DELIVDOC-49-1",
         text="Version 2 is the source version; its change-log row reads 'not stated in the source workbook' and version 3 is issued "
              "as Draft on 22 November 2026.",
         why="The workbook records no version, version date, change log or tool line, so none can be copied.",
         read="The v2 workbook, its four sheets and its core properties.",
         gap="CG-B-DELIVDOC-49-1",
         applied_in="Read me, change-log row v2 and the status row",
         confidence="High",
         confirm="Program manager",
         impact="Document control only; no number, date or role of the source changes.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-2",
         text="The fourteen source module names are read as the service mapping of thirteen services: squad 1 carries P1 rwb-source-data (data engine), "
              "P3 rwb-case (case and workflow), the rules component of every service (the embedded Drools kit, DP-04), P4 "
              "rwb-access, S1 rwb-valuation, S5 rwb-asset and S8 rwb-deviation; squad 2 carries P5 rwb-document, P6 rwb-comms, "
              "P7 rwb-decision, S2 rwb-treatment, S4 rwb-litigation, S6 rwb-debtsale and S7 rwb-writeoff. Per-service headcount "
              "is not derived and is left open.",
         why="The Structure sheet names modules, not services, and gives no per-service staffing.",
         read="Structure sheet rows for the two squads; Ownership Map v1 Services sheet; Architecture v5 slide 41.",
         gap="CG-B-DELIVDOC-49-2",
         applied_in="Services and squads, columns Source module and Squad; Read me, what changed",
         confidence="Medium",
         confirm="Product owner with the two tech leads",
         impact="Shows which squad carries which service without moving any person or changing any count of the source.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-3",
         text="The six services with no source module (P2, P8, P9, P10, S3, S9) are left at the R9 placeholder for the squad and are "
              "assigned at the first daily review, as the Structure sheet says the split is agreed there.",
         why="No module of the Structure sheet names them and no squad is recorded for them.",
         read="Structure sheet module lists; Ownership Map v1 Services sheet; Template and Rules R5.7 rule 6.",
         gap="CG-B-DELIVDOC-49-3",
         applied_in="Services and squads, column Squad and the note under the table; Team types and resources, what the plan does "
                    "not staff",
         confidence="Medium",
         confirm="Product owner with the two tech leads",
         impact="Six of nineteen services have no squad in the plan; the story slices of those services are still counted.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-4",
         text="Wave 0 platform work is owned by the platform team of the Temporal design (the cluster, the namespace and the "
              "workflow kit), with the DevOps team for the pipeline and SCB IT infrastructure for topics and ACLs; no full-time "
              "equivalent is recorded because the source records none.",
         why="Template and Rules R5.1 puts seven platform epics in wave 0 and R5.7 rule 6 requires Day-1 work for every team type, "
              "but the resource plan has no platform row.",
         read="Template and Rules R5.1 and R5.7; Temporal and Drools Design slide 23; Architecture v5 slides 20 to 23.",
         gap="CG-B-DELIVDOC-49-4",
         applied_in="Ownership by team type, artefact ownership and the OPS and INF rows; Team types and resources, what the plan "
                    "does not staff",
         confidence="Medium",
         confirm="IT lead with the platform team",
         impact="Wave 0 has an owner role but no headcount until the platform team confirms its full-time equivalents.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-5",
         text="The DevOps team type has no recorded full-time equivalent; the plan reads 0 and does not attribute the pipeline work "
              "to the TechX squads in this version.",
         why="The Team and People by month sheets have no DevOps row.",
         read="Team and People by month sheets; Template and Rules R5.3 OPS row.",
         gap="CG-B-DELIVDOC-49-5",
         applied_in="Team types and resources, row DevOps team; Ownership by team type, OPS row",
         confidence="High",
         confirm="IT lead",
         impact="OPS stories in waves 0 to 4 have a suggested owner and no capacity behind it.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-6",
         text="SCB IT infrastructure is treated as a shared supporting team that is not counted, as the People by month note says of "
              "shared teams; the full-time equivalent cell carries the R9 placeholder.",
         why="The Structure sheet names SCB IT security and the architecture team as supporting teams only and the People by month "
              "sheet counts no infrastructure role.",
         read="Structure sheet 'Supporting teams'; People by month sheet note; Template and Rules R5.3 INF row.",
         gap="CG-B-DELIVDOC-49-6",
         applied_in="Team types and resources, row SCB IT infrastructure; Ownership by team type, INF row",
         confidence="Medium",
         confirm="IT lead",
         impact="INF stories have a suggested owner and no counted capacity.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-7",
         text="The QA team type is served by the two QA engineers inside the TechX squads (2 of the 12 full-time equivalents, not "
              "counted twice), and it owns the integration harness and NFR stories.",
         why="The source staffs QA inside the squads under Organization TechX and has no separate QA row.",
         read="Team and People by month sheets; Template and Rules R5.3 ITG row; Architecture v5 slide 46.",
         gap="CG-B-DELIVDOC-49-7",
         applied_in="Team types and resources, row QA team; Ownership by team type, ITG row",
         confidence="High",
         confirm="QA lead",
         impact="The harness work of wave 1 has two named full-time equivalents drawn from the squads.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-8",
         text="TechX is read as the organisation of Recovery squad 1 and Recovery squad 2, so the team type of Template and Rules "
              "R5.3 and the squad names of the source both stay in use.",
         why="The source puts TechX in the Organization column of the eight squad rows and never uses it as a team name.",
         read="Team sheet Organization column and note line 2; Template and Rules R5.3.",
         gap="CG-B-DELIVDOC-49-8",
         applied_in="Team types and resources, row TechX; Services and squads, columns CON and APP",
         confidence="High",
         confirm="Program manager",
         impact="None on the counts; the two vocabularies are reconciled in one line instead of renaming the source rows.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-9",
         text="The module-based accountability rows of version 2 are kept word for word, and the service-level reading of them is "
              "stated on the Ownership by team type and Services and squads sheets instead of editing the rows.",
         why="Template and Rules U2 and R6 keep built or in-build content word for word, and AGENTS.md rule 1 forbids editing an "
              "existing row of the source.",
         read="Team and Accountability sheets; Architecture v5 slide 20; ADR-013.",
         gap="CG-B-DELIVDOC-49-9",
         applied_in="Read me, what changed; Ownership by team type, artefact ownership; Services and squads",
         confidence="High",
         confirm="Solution architect",
         impact="The source words and the service-level reading both stay visible; no row is rewritten.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-10",
         text="The shared Epic 2 items stay with the Collection squad as version 2 says, and are not split across the nineteen "
              "services in this version.",
         why="No source read in this work package identifies the shared items or their target service.",
         read="Team and Structure sheets; Epic 2 BRD and the Ownership Map v1 Services sheet.",
         gap="CG-B-DELIVDOC-49-10",
         applied_in="Team types and resources, what the plan does not staff",
         confidence="Medium",
         confirm="Product owner with the Collection squad",
         impact="Epic 2 shared scope has no per-service owner yet; the squad that carries it does not change.",
         wp=WP),
    dict(id="ASM-B-DELIVDOC-49-11",
         text="Version 3 is issued as Draft because no approval is recorded for the source or for this realignment, and the run "
              "overlay of D-RCV-60 asks for a record instead of a stop.",
         why="The source carries no status or approval and the run has no approval step.",
         read="The four sheets of version 2; the D-RCV-60 run overlay.",
         gap="CG-B-DELIVDOC-49-11",
         applied_in="Read me, status row; Team types and resources, what the plan does not staff",
         confidence="High",
         confirm="Program manager with the business lead",
         impact="The plan is usable for planning and is not an approved baseline.",
         wp=WP),
]

G.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in gaps) + "\n", encoding="utf-8")
A.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in assumptions) + "\n", encoding="utf-8")
print("gaps", len(gaps), "assumptions", len(assumptions))
