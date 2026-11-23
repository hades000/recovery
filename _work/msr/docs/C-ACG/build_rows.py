"""Builds the row JSON that compat/office_write.py xlsx-append reads for WP C-ACG.

Nothing here touches the source workbook. Every string is taken from
Template and Rules v1, the Ownership Map v1 Services sheet, or plan/ids.json.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PH = "Not specified in the source documents (CG-C-ACG-1; ASM-C-ACG-1)"

READ_ME = [
    ["SCB Collections and Recovery. Henka Group, 22 November 2026."],
    ["(C) Siam Commercial Bank and Henka Pte Ltd"],
    [],
    ["Recovery Workbench Acceptance Criteria Glossary v2"],
    ["Next version of Recovery Workbench Acceptance Criteria Glossary v1. Decision D-RCV-60 microservice realignment: "
     "the Workbench moves to 19 services inside ACE, and every acceptance criterion now says where it comes from."],
    [],
    ["Item", "Value"],
    ["Document", "Recovery Workbench Acceptance Criteria Glossary v2"],
    ["Version", "2"],
    ["Date", "22 November 2026"],
    ["Decision", "D-RCV-60"],
    ["Tool", "T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    ["Status", "Draft"],
    ["Source", "04 User stories/Recovery Workbench Acceptance Criteria Glossary v1.xlsx"],
    ["Audience", "Business analysts, testers and developers who write or read a Scenario line"],
    [],
    ["Change log"],
    ["Version", "Date", "Change", "Tool"],
    ["v1", "Not stated in the source document",
     "Baseline glossary: 4 sheets, 4 keyword rows, 55 sentence frames, 168 word rows, 15 code prefixes",
     "Not stated in the source document"],
    ["v2", "22 November 2026", "D-RCV-60 microservice realignment", "T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    ["v2, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"],
    [],
    ["Dates",
     "The source workbook carries no version, date or change log. Version 1 is therefore dated from the file family and no "
     "date is invented. 22 November 2026 is the date of this run (Template and Rules section R8.1). No release date is "
     "changed and no date is raised as a gap (Template and Rules section R1 U7)."],
    [],
    ["What version 2 changes",
     "Three additions, all taken from Template and Rules: the acceptance criteria origin tag (section R7.2, section 7), the "
     "contract mock Given for a dependency of class C (section R5.4 and section R5.5 DP-11, section R7.2 section 12.8), and "
     "the -ITG suffix on the integration copy of a test case (section R7.2 section 16). Two rows are added to 'Sentence "
     "frames' and two to 'Code prefixes', and the new sheet 'Realignment additions' explains them. Every keyword, sentence "
     "frame, word, code prefix, number and example of version 1 is kept as it stands; no row is edited, renumbered or "
     "removed."],
    [],
    ["Sheet index"],
    ["Sheet", "Data rows", "What it holds"],
    ["Keywords", "4",
     "The four line keywords Given, When, Then and Scenario, with the reading label, the Thai word and what the line is "
     "doing. Unchanged."],
    ["Sentence frames", "57",
     "The 55 sentence patterns of version 1 unchanged, plus the contract mock Given and the origin tag at the end of a "
     "Scenario line."],
    ["Words", "168",
     "The words that carry the meaning, in order of how often they appear in the acceptance criteria, with kind and "
     "meaning. Unchanged."],
    ["Code prefixes", "17",
     "The 15 code prefixes of version 1 unchanged, plus the acceptance criteria origin tag and the -ITG test case suffix."],
    ["Realignment additions", "3 blocks",
     "How the three additions work with their source section, example and owner; the contract fake of each of the 19 "
     "services from the Ownership Map; and the four questions this work package leaves open."],
]

SENTENCE_FRAMES = [
    ["the {service} contract fake is published", PH,
     "Given the rwb-case contract fake is published"],
    ["(legacy RWB-\u2026-nnn ACn) or (new, D-RCV-60) at the end of the Scenario line", PH,
     "Scenario: AC2 the case moves to \"IN_LITIGATION\" (legacy RWB-E1-001 AC2)"],
]

CODE_PREFIXES = [
    ["(legacy RWB-\u2026-nnn ACn) / (new, D-RCV-60)", "Acceptance criteria origin tag", PH,
     "The tag at the end of every Scenario line. It says whether the criterion comes from a legacy story, naming that story "
     "and the criterion number, or is new in this realignment decision. No Scenario line is left untagged (Template and "
     "Rules section R7.2, section 7)."],
    ["-ITG", "Integration test case suffix", PH,
     "The suffix on the integration copy of a test case, as in TC-E1-001-01-ITG. The unit, component and contract copy keeps "
     "the plain test case ID (Template and Rules section R7.2, section 16)."],
]

SERVICES = [
    ("P1", "rwb-source-data", 1, "/api/recovery/source-data/v1"),
    ("P2", "rwb-integration", 1, "/api/recovery/integration/v1"),
    ("P3", "rwb-case", 1, "/api/recovery/case/v1"),
    ("P4", "rwb-access", 1, "/api/recovery/access/v1"),
    ("P5", "rwb-document", 1, "/api/recovery/document/v1"),
    ("P6", "rwb-comms", 1, "/api/recovery/comms/v1"),
    ("P7", "rwb-decision", 1, "/api/recovery/decision/v1"),
    ("P8", "rwb-payment", 2, "/api/recovery/payment/v1"),
    ("P9", "rwb-reporting", 1, "/api/recovery/reporting/v1"),
    ("P10", "rwb-agent", 1, "/api/recovery/agent/v1"),
    ("S1", "rwb-valuation", 3, "/api/recovery/valuation/v1"),
    ("S2", "rwb-treatment", 2, "/api/recovery/treatment/v1"),
    ("S3", "rwb-guarantee", 3, "/api/recovery/guarantee/v1"),
    ("S4", "rwb-litigation", 3, "/api/recovery/litigation/v1"),
    ("S5", "rwb-asset", 2, "/api/recovery/asset/v1"),
    ("S6", "rwb-debtsale", 3, "/api/recovery/debtsale/v1"),
    ("S7", "rwb-writeoff", 4, "/api/recovery/writeoff/v1"),
    ("S8", "rwb-deviation", 2, "/api/recovery/deviation/v1"),
    ("S9", "rwb-partner", 4, "/api/recovery/partner/v1"),
]

ADDITIONS = [
    ["The three D-RCV-60 additions"],
    ["Addition", "Where it appears in a story", "The rule", "Example", "Who owns it"],
    ["Acceptance criteria origin tag",
     "Section 7 Acceptance criteria; the end of every Scenario: ACn line",
     "Each Scenario line ends with either (legacy RWB-\u2026-nnn ACn), naming the legacy story and the criterion number, or "
     "(new, D-RCV-60) for a criterion created by this realignment. No Scenario line is left untagged. Source: Template and "
     "Rules section R7.2, section 7.",
     "Scenario: AC2 the case moves to \"IN_LITIGATION\" (legacy RWB-E1-001 AC2)",
     "TechX (suggested; any team may pick up this story)"],
    ["Contract mock Given",
     "Section 7 Acceptance criteria, the Given line of any criterion that reaches another service (dependency class C)",
     "A story builds against the published contract of the other service and its fake, never against the other service at "
     "run time. The Given names the fake and the Then names the published response. Source: Template and Rules section "
     "R5.4 class C, section R5.5 DP-11, section R7.2 section 12.8.",
     "Given the rwb-case contract fake is published",
     "The service that publishes the contract: P3 rwb-case for the rwb-case fake, per the Ownership Map v1 and the default "
     "rulings of section R3"],
    ["-ITG test case suffix",
     "Section 16 Test cases; the TC ID column",
     "The integration copy of a test case ends in -ITG and runs in the integration harness; the unit, component and "
     "contract copy keeps the plain ID. Source: Template and Rules section R7.2 section 16, section R5.4 class I.",
     "TC-E1-001-01-ITG beside TC-E1-001-01",
     "QA team (suggested; any team may pick up this story)"],
    [],
    ["Contract fakes by service (Ownership Map v1, Services sheet)"],
    ["Code", "Service", "Wave (Ownership Map v1)", "REST base (Ownership Map v1)",
     "Contract story pattern (Template and Rules section R5.2)",
     "Contract group of that contract story"],
]
ADDITIONS += [[c, s, w, base, f"RWB-{c}-<legacy compact>-CON",
               "CG-W of the story's own wave, which is the wave of its business epic (section R5.6), not the service wave"]
              for c, s, w, base in SERVICES]
ADDITIONS += [
    [],
    ["Questions this work package leaves open"],
    ["Topic", "Gap row", "Assumption row", "What a reader should do"],
    ["Thai wording of the new rows", "CG-C-ACG-1", "ASM-C-ACG-1",
     "The Thai cell of the three new rows holds the placeholder of section R9. Read the English cell until the Thai "
     "wording is confirmed."],
    ["Origin tag where one legacy criterion is carried by several new stories", "CG-C-ACG-2", "ASM-C-ACG-2",
     "The tag always names the legacy story and the criterion number, unchanged, and is repeated in every new story that "
     "carries the criterion."],
    ["Name, version and location of a contract fake", "CG-C-ACG-3", "ASM-C-ACG-3",
     "The fake is called 'the <service> contract fake'. Its artefact name, version and repository location are not "
     "specified in the source documents."],
    ["Level and register place of an -ITG copy", "CG-C-ACG-4", "ASM-C-ACG-4",
     "The integration copy is a separate row at Level Integration or End to end; the plain ID stays on the unit, component "
     "and contract copy."],
]

for name, rows in (("rows_readme", READ_ME), ("rows_frames", SENTENCE_FRAMES),
                   ("rows_prefixes", CODE_PREFIXES), ("rows_additions", ADDITIONS)):
    (HERE / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(name, len(rows), "rows")
