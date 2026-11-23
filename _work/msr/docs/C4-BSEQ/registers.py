"""Write the C4-BSEQ gap and assumption rows (candidate rows; D1 numbers them)."""
import json
from pathlib import Path

ROOT = Path(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14")
WORK = ROOT / "_work" / "msr"
WP = "C4-BSEQ"
DEC = "D-RCV-60"
SRC = "11 Delivery and operations/Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx"
CAT = "04 User stories/Recovery Workbench Service Story Catalog v1.xlsx"

gaps = [
    dict(title="The 23 new wave-0 platform stories have no release date",
         source=CAT, section="Stories",
         description=("RWB-PLT-N001 to RWB-PLT-N012 (16 stories with their CON variants) and RWB-PLT-NF01 to RWB-PLT-NF08 (8 stories) carry an empty Release in the Service Story Catalog v1, "
                      "while the 48 platform stories that come from a v6 legacy key carry 30 November 2026 or 31 December 2026 (tentative). The v6 Build Sequence has no platform block, so it does not supply a date either."),
         evidence="Service Story Catalog v1, sheet Stories: Release is empty for the 23 rows whose Story starts RWB-PLT-N; v6 Sequence has 115 items and none of them is RWB-PLT-N001 to RWB-PLT-N012.",
         type="Missing", area="Platform release plan", severity="P2", needed_by_wave="0",
         legacy_ref="N001-N012, NF-01-NF-08", owner_role="Delivery lead",
         asm=f"ASM-{WP}-6",
         proposed="Assign the wave-0 platform stories to the Window 1 release (E1, 30 November 2026, tentative) or name their own wave-0 release date."),
    dict(title="No review window covers the wave-0 platform block",
         source=SRC, section="Sequence and By window",
         description=("v6 opens at Window 1 (2 Nov to 13 Nov) with Epic 1 items. The realignment puts 65 platform stories (wave 0) in front of Window 1 (Template and Rules §R5.6), "
                      "but neither v6 nor the story catalog gives that block a review window or a set of dates."),
         evidence="v6 By window: Window 1 starts 2 Nov; v6 Sequence item 1 is RWB-E1-044 in Window 1; 65 RWB-PLT stories exist in the catalog with wave 0 and no window.",
         type="Ambiguous", area="Delivery schedule", severity="P2", needed_by_wave="0",
         legacy_ref="", owner_role="Delivery lead", asm=f"ASM-{WP}-5",
         proposed="Add a wave-0 window before 2 November, or fold the 65 platform stories into Window 1 and extend it."),
    dict(title="Window dates end in January 2027 while the new stories release through June 2027",
         source=CAT, section="Stories",
         description=("The v6 windows run 2 November 2026 to 22 January 2027 (Window 1 to Epic 3). The service stories that the same 115 items split into carry release dates up to 30 June 2027 (tentative), "
                      "so a story pulled in Window 2 may have a release after the last window of the sheet."),
         evidence="v6 By window: 28 Dec to 22 Jan is the last window. Service Story Catalog v1: Release values include 30 June 2027 (tentative) and 28 February 2027 (tentative).",
         type="Conflict", area="Delivery schedule", severity="P2", needed_by_wave="1",
         legacy_ref="", owner_role="Delivery lead", asm=f"ASM-{WP}-4",
         proposed="Keep the two-week windows as review points and let the per-story release date stand, or re-cut the windows to the release plan."),
    dict(title="Two retired items still carry v6 windows and dependencies",
         source=SRC, section="Sequence",
         description=("RWB-E1-014 (decision log copy to the data lake) and RWB-TE-007 (scheduled jobs on Quartz) are retired under §R6 and have no new story, yet v6 still lists them with a window, "
                      "dates and dependants, and two other items (RWB-E1-056, RWB-E1-017) still name them in Depends on."),
         evidence="v6 Sequence items 19 and 21; Template and Rules §R6 Retired.",
         type="Outdated", area="Delivery schedule", severity="P3", needed_by_wave="1",
         legacy_ref="RWB-E1-014, RWB-TE-007", owner_role="Delivery lead", asm=f"ASM-{WP}-10",
         proposed="Drop the two rows when the tracker is cut over, or keep them struck through with 'retired, not pulled' as this version does."),
    dict(title="The v6 module column cannot show who builds a split row",
         source=SRC, section="Sequence, By module",
         description=("A v6 row carries one monolith module (P1 to P10), one owner and one window. After the split, one v6 item is up to nine stories in up to six services, "
                      "so neither the module column nor the By module counts can show the service or the lane that builds part of the item."),
         evidence="v6 Sequence: 115 rows, 15 distinct module values, one row per item. Catalog: 530 stories carry the 115 legacy keys, across 19 services plus the platform and integration epics.",
         type="Outdated", area="Delivery reporting", severity="P3", needed_by_wave="1",
         legacy_ref="", owner_role="Delivery lead", asm=f"ASM-{WP}-11",
         proposed="Keep the module column for traceability and report load by service and lane, as the new sheet 'By service and lane' does."),
]

asms = [
    dict(text="The source workbook and the story catalog record no approval status, so the next version continues in Draft.",
         why="No status field exists in the v6 workbook or in the catalog; Template and Rules §R1 U8 removes the human verification stop and AGENTS.md rule 9 says to continue in Draft.",
         read=f"{SRC}; {CAT}", gap="", applied_in="Read me (Status row)", confidence="High",
         confirm="Delivery lead", impact="None on content; the version is marked Draft."),
    dict(text="The Day-1 block is all 65 platform stories plus the wave 1 and wave 2 contract groups CG-W1 (44 stories) and CG-W2 (64 stories), pulled before Window 1.",
         why="Template and Rules §R5.7.1 makes every CON story Day 1 and §R5.7.6 asks for Day-1 work in every team type; the platform stories carry the wave-0 platform and the contract groups carry the service contracts.",
         read=f"{CAT}; Template and Rules §R5.7", gap="", applied_in="Sheet 'Day 1 first'", confidence="High",
         confirm="Delivery lead", impact="173 stories are pulled before item 1 of the Sequence sheet."),
    dict(text="Inside each window the pull order is dependency-safe and opens with the items that have a contract story; Order (v6) is kept on every row.",
         why="Pull rule 1 of the source requires an item to be pulled only when its dependencies are done, and §R5.7 asks for Day-1 contract work first.",
         read=f"{SRC} (Pull rules, Depends on)", gap="", applied_in="Sheet Sequence, Order (v7) and Order (v6)", confidence="Medium",
         confirm="Delivery lead", impact="Order (v7) differs from Order (v6) on some rows; both numbers are on the row."),
    dict(text="The Release column keeps the v6 edition label (E1, E2, E3); the per-story release date comes from the catalog and is marked (tentative).",
         why="v6 marks the release of an item as E1, E2 or E3, a release edition, not a date; the catalog gives a date per story.",
         read=f"{SRC}; {CAT}", gap=f"CG-{WP}-3", applied_in="Sheet Sequence, column Release", confidence="High",
         confirm="Delivery lead", impact="Two release notations in one workbook, each labelled."),
    dict(text="The two-week windows stay the sponsor review points with unchanged dates, and the wave-0 block is sequenced before Window 1 without a dated window of its own.",
         why="Template and Rules §R1 U7 keeps dates unchanged and tentative and never raises a date as a gap; the wave-0 block still needs a place in the pull order.",
         read=f"{SRC} (By window)", gap=f"CG-{WP}-2", applied_in="Sheets 'Day 1 first' and 'By window'", confidence="Medium",
         confirm="Delivery lead", impact="Wave 0 has an order but no review window."),
    dict(text="The 23 new wave-0 platform stories are carried as Day-1 wave-0 work with the §R9 placeholder in place of a release date.",
         why="The catalog leaves Release empty for RWB-PLT-N001 to RWB-PLT-N012 and RWB-PLT-NF01 to RWB-PLT-NF08 and no other source gives a date.",
         read=f"{CAT}", gap=f"CG-{WP}-1", applied_in="Sheet 'Day 1 first', column Release", confidence="Medium",
         confirm="Delivery lead", impact="23 rows show the placeholder instead of a date."),
    dict(text="A v6 item whose legacy key has no contract story of its own builds against the contract group of the service that owns its delivery stories (CG-W<service wave>).",
         why="27 of the 115 keys have no CON slice in the split plan, while Template and Rules §R5.7.2 lets an APP story build against a published contract and its fake.",
         read=f"_work/msr/plan/split_plan.json (legacy); {CAT}", gap="", applied_in="Sheet Sequence, column Contract story (v7)", confidence="Medium",
         confirm="Tech lead", impact="27 rows name a contract group instead of a contract story ID."),
    dict(text="RWB-ACE-001 is carried as RWB-P1-ACE001-DB, owned by the ACE team, and stays outside the squads' pull order as v6 states.",
         why="v6 says RWB-ACE-001 gates window 1 and is not pulled by either squad; the split plan gives it the one slice RWB-P1-ACE001-DB and no other.",
         read=f"{SRC} (Sequence note, Critical path); _work/msr/plan/split_plan.json", gap="", applied_in="Sheet Critical path, step 1", confidence="High",
         confirm="Delivery lead", impact="The ACE delivery keeps its window-1 gate and its 21 November date."),
    dict(text="Owners are the work-type owners of Template and Rules §R5.3, spelled as in the Ownership Map; a row that spans services lists every owning team. No names of people.",
         why="Template and Rules §R5.3 fixes the owner phrases and §R1 U3 makes the owner a suggestion; AGENTS.md rule 4 forbids names of people.",
         read="22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx", gap="", applied_in="Sheets Sequence, 'Day 1 first', 'Owners (v7)'", confidence="High",
         confirm="Delivery lead", impact="Owner is a suggestion only; any team may pick up a story."),
    dict(text="The two retired items keep their v6 rows, marked 'No new story' and 'Not pulled'.",
         why="Template and Rules §R6 retires RWB-E1-014 and RWB-TE-007 and forbids a new story for them, while §R8.2 forbids editing the source.",
         read="Template and Rules §R6", gap=f"CG-{WP}-4", applied_in="Sheet Sequence, rows 60 and 61 of Order (v7)", confidence="High",
         confirm="Delivery lead", impact="Two rows are visible but never pulled."),
    dict(text="Where the v6 module and the owning service differ, Service (v7) follows the new stories and Module (v6) is kept unchanged.",
         why="Platform and integration stories move out of the monolith module that raised them (for example RWB-E1-044 is module P3 in v6 and a platform story in the split), and the v6 value still has to be quotable.",
         read=f"{SRC}; {CAT}", gap=f"CG-{WP}-5", applied_in="Sheets Sequence and By service and lane", confidence="High",
         confirm="Tech lead", impact="A row can show Module P3 and Service PLT."),
    dict(text="Order (v7) is derived for this version and is not a source value.",
         why="v6 holds one order; the realignment needs an order that opens with the Day-1 block and stays dependency-safe.",
         read=f"{SRC}", gap="", applied_in="Sheet Sequence, Order (v7)", confidence="High",
         confirm="Delivery lead", impact="Order (v6) is the traceable number; Order (v7) is the pull sequence."),
]

(WORK / "gaps").mkdir(parents=True, exist_ok=True)
(WORK / "assumptions").mkdir(parents=True, exist_ok=True)
with open(WORK / "gaps" / f"{WP}.jsonl", "w", encoding="utf-8") as f:
    for n, g in enumerate(gaps, 1):
        row = {"id": f"CG-{WP}-{n}", "title": g["title"], "source": g["source"], "section": g["section"],
               "description": g["description"], "evidence": g["evidence"], "type": g["type"],
               "area": g["area"], "severity": g["severity"], "needed_by_wave": g["needed_by_wave"],
               "legacy_ref": g["legacy_ref"], "owner_role": g["owner_role"], "asm": g["asm"],
               "proposed": g["proposed"], "wp": WP}
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
with open(WORK / "assumptions" / f"{WP}.jsonl", "w", encoding="utf-8") as f:
    for n, a in enumerate(asms, 1):
        row = {"id": f"ASM-{WP}-{n}", "text": a["text"], "why": a["why"], "read": a["read"],
               "gap": a["gap"], "applied_in": a["applied_in"], "confidence": a["confidence"],
               "confirm": a["confirm"], "impact": a["impact"], "wp": WP}
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("gaps", len(gaps), "asms", len(asms))
