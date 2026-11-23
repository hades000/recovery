"""Writes the gap rows and the assumption rows of WP C4-SBO."""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
WORK = os.path.join(ROOT, "_work", "msr")
SRC = "Recovery Workbench Story Build Order v3"
TR = "Recovery Workbench Microservice Story Template and Rules v1"
WP = "C4-SBO"

gaps = [
    dict(
        title="Version 3 carries no approval record and no status, so version 4 has no approved baseline",
        source=SRC, section="Title block; the source has no status or approval section",
        description="Version 3 opens with a title, a date and a version number only. It carries no Status row, no approval record and no sign-off, and the realignment run takes no approval stop, so version 4 cannot be issued as approved and is issued as Draft with the approval carried as an open row.",
        evidence="Version 3 line 3: 'E2E Recovery Workbench. SCB Collections and Recovery. Henka Group, 16 November 2026. v3.' No further metadata, no status and no approval anywhere in the document.",
        type="Missing", area="governance", severity="P3", needed_by_wave=0, legacy_ref="",
        owner_role="Programme governance",
        proposed="Record the approval of version 4 when the programme approves it, and state the approved version in the title block at the next issue.",
    ),
    dict(
        title="Version 3 carries no change log and no tool line",
        source=SRC, section="Change log; the source has no change-log section",
        description="Version 3 has no change log, so there is no record of what changed between version 2 and version 3 and no tool line for the source. Version 4 adds a change-log table, records version 3 as the source row with this gap and its assumption, and gives its own row the D-RCV-60 change and the tool line.",
        evidence="The whole of version 3 was read: 18 paragraphs and 5 tables, with no change-log table, no version history and no tool line.",
        type="Missing", area="documentation", severity="P3", needed_by_wave=0, legacy_ref="",
        owner_role="Delivery lead",
        proposed="Keep the change-log table in every later version and add the change log of versions 1 and 2 from the source history if it is ever found.",
    ),
    dict(
        title="Version 3 is written for two squads, while D-RCV-60 works by five team types across 19 services",
        source="%s; %s" % (SRC, TR),
        section="Opening paragraph; How to use it, first and second paragraph",
        description="Version 3 says that RWB-ACE-001 'is not pulled by either squad', that 'the two squads agree the split at the daily board' and that the critical path 'starts outside the squads'. The realignment has one epic per service plus platform and integration epics, and the suggested owner is a team type: TechX, ACE team, SCB IT infrastructure, DevOps team and QA team. No source states how the five team types replace the two squads at the daily board.",
        evidence="Version 3 opening paragraph: 'not pulled by either squad'; How to use it: 'The two squads agree the split at the daily board'; Template and Rules R5.3 and U3; DL46.",
        type="Conflict", area="governance", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Delivery lead",
        proposed="Replace the squad wording with the five team types at the next review of this document, and state the board in team-type terms.",
    ),
    dict(
        title="One module per item in version 3 becomes several services per item in the split",
        source="%s; Recovery Workbench Microservice Ownership Map v1" % SRC,
        section="The five item tables, Module column; the realignment tables, Service column",
        description="Version 3 gives every item one module, for example P2 or P3. The split gives an item up to nine stories in up to six services; RWB-E1-007, the integration adapters, becomes nine stories over P2, P3, P4, P5, P6 and the integration epic. The Module column is kept word for word and no source states which of the services of a multi-service item owns it.",
        evidence="Version 3 item 11 RWB-E1-007 has Module P2; its stories are RWB-P2-E1007-CON, RWB-P2-E1007-APP, RWB-P3-E1007-APP, RWB-P6-E1007-APP, RWB-P5-E1007-APP, RWB-P4-E1007-APP, RWB-P2-E1007-INF, RWB-P2-E1007-OPS and RWB-ITG-E1007-ITG.",
        type="Ambiguous", area="story split", severity="P3", needed_by_wave=1, legacy_ref="RWB-E1-007",
        owner_role="Solution architect",
        proposed="Read the Module column of version 3 as the module that raised the item, and take the owning service of each story from its story key and the Ownership Map v1.",
    ),
    dict(
        title="Two items that version 3 still orders are retired by D-RCV-60, and no source states what a squad does with a retired item in the order",
        source="%s; %s" % (SRC, TR),
        section="Window 2, items 19 and 21; Template and Rules R6 Retired row",
        description="Version 3 orders RWB-E1-014, the decision log copy to the data lake, as item 19 and RWB-TE-007, the scheduled jobs on Quartz, as item 21. R6 retires both: there is no data lake in Architecture v5, and Quartz is replaced by Temporal Schedules. The order of version 3 was not written for retired items, so no source states how a retired item is shown or what happens to an item that waited on it, for example RWB-TE-008 on RWB-TE-007.",
        evidence="Version 3 item 19 'RWB-E1-014 Decision log copy to the data lake' and item 21 'RWB-TE-007 Scheduled jobs on Quartz'; item 24 RWB-TE-008 waits on E1-008, TE-007; Template and Rules R6: E1-014 retired, TE-007 retired, dependencies on TE-007 point to RWB-PLT-E1071-CON.",
        type="Outdated", area="documentation", severity="P3", needed_by_wave=2, legacy_ref="RWB-E1-014; RWB-TE-007",
        owner_role="Solution architect",
        proposed="Keep the item number and the place in the order, carry no story against the item, and repoint a dependency on RWB-TE-007 to RWB-PLT-E1071-CON.",
    ),
    dict(
        title="No source states the board limit of a team type, or how many stories one team type may hold at once",
        source=SRC, section="How to use it, first paragraph",
        description="Version 3 says that work in progress per squad stays within the board limit and gives no limit. The realignment replaces the two squads with five team types and 1034 stories, of which 939 are Day 1, so the board limit per team type decides how much of the Day-1 work can start at once and no source gives a number.",
        evidence="Version 3 How to use it: 'Work in progress per squad stays within the board limit.' No number follows, and the document has no other capacity statement.",
        type="Missing", area="governance", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Delivery lead",
        proposed="Keep the board limit of version 3 unchanged until the programme states a limit per team type, then record it in this document and in the Day-1 Work Allocation.",
    ),
    dict(
        title="Version 3 names no release date for an item beyond the epic its window releases in",
        source=SRC, section="The five window headings; the release line under each heading",
        description="Version 3 states a window with a date range and a release line, 'releasing in Epic 1' to 'releasing in Epic 3', and no release date for an individual item. The story set of this run carries a release date per story, and the two do not line up one to one: the windows end on 22 January 2027 while the story set runs to 30 June 2027. This version keeps the release statement of version 3 and marks it tentative.",
        evidence="Version 3 headings: 'Window 1, 2 to 13 November 2026' with '15 items, releasing in Epic 1'; the last heading 'Epic 3, 28 December 2026 to 22 January 2027' with '3 items, releasing in Epic 3'. No item carries a release date.",
        type="Ambiguous", area="release planning", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Delivery lead",
        proposed="State the release date of each window against the release calendar of the programme, kept tentative, and leave the epic statement as the item-level position until that calendar is agreed.",
    ),
    dict(
        title="The new platform stories N001 to N012 and the harness stories W1J01 to W4J01 sit in no window of version 3",
        source="%s; %s" % (SRC, TR),
        section="Day-1 work that is new in this version",
        description="Version 3 orders the 115 items of Epic 1, Epic 2 and Epic 3 and nothing else. The realignment adds the platform stories N001 to N012 of wave 0 and the integration harness and journey stories W1J01 to W4J01, which are what makes sure every team type has Day-1 work. No source states where they sit in the order of version 3.",
        evidence="Template and Rules R5.7 rule 6 and §R5.1: the platform stories N001 to N012 and W1J01 make sure every team type has Day-1 work. Version 3 has five windows and 115 items, none of them a platform or harness story.",
        type="Missing", area="planning and waves", severity="P3", needed_by_wave=0, legacy_ref="N001; W1J01",
        owner_role="Solution architect",
        proposed="Show the wave 0 platform stories and the harness stories as Day-1 work before window 1, because wave 0 is not a release and the stories unblock every window that follows.",
    ),
    dict(
        title="The waits-on column of version 3 names legacy keys, and the stories that now carry those keys are different work items",
        source="%s; %s" % (SRC, TR),
        section="The five item tables, Waits on column; How this version is read",
        description="Version 3 says 'Waits on names the items that must finish first, by their number within the same family' and lists keys such as E1-044 and TE-001. Those keys are not story keys in the realignment: each one is now a contract group and several stories, with a build dependency (H) that is allowed only inside a service or on a platform contract, a contract dependency (C) that never blocks, an integration dependency (I) that sits only on an integration story and external work (X) that is tracked only. No source translates a waits-on row of version 3 into the dependency classes of the realignment.",
        evidence="Version 3 opening paragraph: 'Waits on names the items that must finish first, by their number within the same family'; Template and Rules R5.4 and R5.7 rules 2 to 8.",
        type="Ambiguous", area="dependency classification", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Solution architect",
        proposed="Keep the waits-on column of version 3 word for word as the item-level position, and read the realigned waits of a story from its Ready to start and its lane.",
    ),
]

assumptions = [
    dict(
        text="Version 4 is issued as Draft with no recorded approval, and the approval is carried as an open row.",
        why="The realignment run takes no approval stop and version 3 records none; a Draft status is the only truthful label.",
        read="AGENTS.md rule 9; Template and Rules U8, R8.1; the title block of version 3",
        applied_in="Title block and opening note", confidence="High", confirm="Programme governance",
        impact="The document can be used to plan and pull work; it cannot be cited as an approved baseline.",
    ),
    dict(
        text="The change log of version 4 starts at version 3 as the source row, records that version 3 has no change log and no tool line, and carries the row '4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash'.",
        why="R8.1 requires a change-log row and the source has none; recording the gap is better than inventing the history of versions 1 and 2.",
        read="Template and Rules R8.1, R8.2; the title line of version 3, dated 16 November 2026",
        applied_in="Change log", confidence="High", confirm="Delivery lead",
        impact="The history of the document is complete from version 3 onwards and honest about what came before.",
    ),
    dict(
        text="The two squads of version 3 are read as the five team types of this version: TechX, ACE team, SCB IT infrastructure, DevOps team and QA team. The daily board agrees the item order as before, the product owner settles a disagreement the same day, and a team type takes any story it can pull.",
        why="D-RCV-60 gives one epic per service and a soft owner by team type; the two squads no longer describe the work, and dropping the board rule would remove the only sequencing governance the source states.",
        read="Template and Rules R5.3, R5.7 rule 6, U3, DL46; version 3 opening paragraph and How to use it",
        applied_in="How this version is read, Owner bullet; How to use it, third paragraph", confidence="Medium",
        confirm="Delivery lead with the programme architecture group",
        impact="Every sentence of version 3 that names a squad is read in team-type terms; no item changes its place in the order.",
    ),
    dict(
        text="The Module column of version 3 is kept unchanged as the module that raised the item, and the owning service of each story is read from the service code in its story key and from the Ownership Map v1.",
        why="The split gives an item several services and no source states which one owns a multi-service item; the story key carries the service of every slice by construction and the Ownership Map gives the same service for its tables, endpoints, events, jobs and workflows.",
        read="Template and Rules R4, R5.2, R5.5; Ownership Map v1; version 3 Module column",
        applied_in="The five realignment tables, Service column", confidence="High",
        confirm="Solution architect",
        impact="A reader keeps the module of version 3 and finds the owner of each story in the Service column without a second document.",
    ),
    dict(
        text="RWB-E1-014 and RWB-TE-007 keep their number and their place in the order of version 3 with no story against them; the work of RWB-E1-014 is dropped because there is no data lake, and a dependency on RWB-TE-007 points at RWB-PLT-E1071-CON.",
        why="R6 retires both items and states the replacement of RWB-TE-007; removing a number from a published order would break the reference of the windows and the critical path paragraph, which both name items by number.",
        read="Template and Rules R6 Retired row, DP-10, DP-17; version 3 items 19, 21 and 24",
        applied_in="Window 2, after the realignment table", confidence="High", confirm="Solution architect",
        impact="Two of the 115 items carry no story; the count of items stays 115 and the count of stories that carry them is 530.",
    ),
    dict(
        text="The board limit of version 3 is kept unchanged and applies to each team type, because no source states a limit per team type and no source states how many stories one team type may hold at once.",
        why="A limit that is not in any source would be invented; keeping the position of the source is the only choice that does not contradict it, and the Day-1 work of 939 stories is pulled under it.",
        read="Template and Rules U7, R5.7 rule 6; version 3 How to use it",
        applied_in="Lanes and Day 1 in this version", confidence="Medium", confirm="Delivery lead",
        impact="The amount of Day-1 work that starts at once is capped by a limit that is not written down; the programme confirms it before window 1.",
    ),
    dict(
        text="The release statement of version 3, 'releasing in Epic 1' to 'releasing in Epic 3' under each window heading, is kept word for word and marked tentative; no release date of an item is added.",
        why="U7 and DL48 keep every date unchanged and tentative and no source gives the release date of an item; the release calendar of the story set runs to 30 June 2027 and would conflict with a date invented here.",
        read="Template and Rules U7, R8.1; version 3 window headings; DL48",
        applied_in="The five window headings and their release lines", confidence="High",
        confirm="Delivery lead",
        impact="The order is read against the release calendar of the programme; nothing in this document moves a release date.",
    ),
    dict(
        text="The platform stories N001 to N012 of wave 0 and the integration harness and journey stories W1J01 to W4J01 are shown before window 1 as Day-1 work, because wave 0 is not a release and these stories are what gives every team type Day-1 work.",
        why="R5.7 rule 6 makes these stories the guarantee of Day-1 work for every team type, and they carry no item of version 3, so they need a place in the order that does not disturb the 115 items.",
        read="Template and Rules R5.1, R5.7 rule 6; Architecture v5 slide 38 note; the fragments of the story set",
        applied_in="Day-1 work that is new in this version", confidence="Medium",
        confirm="Solution architect",
        impact="The order gains a Day-1 block before window 1; the five windows and their dates are unchanged.",
    ),
    dict(
        text="The waits-on column of version 3 is kept word for word as the item-level position, and the realigned waits of a story are its Ready to start and its lane; a waits-on row of version 3 is not translated into dependency classes in this document.",
        why="Translating a waits-on row would change a column of the source, and the dependency classes of every story are already held in its story file under the metadata rows Depends on (build), Contract dependencies, Integration dependencies and External dependencies.",
        read="Template and Rules R5.4, R5.7 rules 2 to 8, R7.1; version 3 opening paragraph",
        applied_in="How this version is read; the five realignment tables", confidence="High",
        confirm="Solution architect",
        impact="A reader who needs the class of a dependency follows the story key into its story file; the order in this document stays comparable with version 3.",
    ),
]

gp = []
for i, g in enumerate(gaps, 1):
    gp.append({"id": "CG-%s-%d" % (WP, i), **g, "asm": "ASM-%s-%d" % (WP, i), "wp": WP})
ap = []
for i, a in enumerate(assumptions, 1):
    ap.append({"id": "ASM-%s-%d" % (WP, i), **a, "gap": "CG-%s-%d" % (WP, i), "wp": WP})

for path, rows in ((os.path.join(WORK, "gaps", WP + ".jsonl"), gp),
                   (os.path.join(WORK, "assumptions", WP + ".jsonl"), ap)):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print("WROTE", path, len(rows), "rows")
