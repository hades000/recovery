"""Writes the C-ACG gap and assumption registers. One JSON object per line, keys of Template and Rules section R9."""
import json
from pathlib import Path

ROOT = Path.cwd()
GAPS = ROOT / "_work/msr/gaps/C-ACG.jsonl"
ASMS = ROOT / "_work/msr/assumptions/C-ACG.jsonl"
SRC = "04 User stories/Recovery Workbench Acceptance Criteria Glossary v1.xlsx"
APPLIED = "04 User stories/Recovery Workbench Acceptance Criteria Glossary v2.xlsx"

gaps = [
    {
        "id": "CG-C-ACG-1",
        "title": "Thai wording for the three rows that D-RCV-60 adds to the glossary",
        "source": SRC,
        "section": "Sentence frames; Code prefixes",
        "description": "Version 1 gives a Thai cell for every keyword, sentence frame and code prefix. The three rows this "
                       "work package adds (the contract mock Given, the acceptance criteria origin tag and the -ITG test "
                       "case suffix) have no Thai wording in any source document, so each of their Thai cells carries the "
                       "placeholder of Template and Rules section R9.",
        "evidence": "The source workbook gives Thai for all 4 keyword rows, all 55 sentence frame rows and all 15 code "
                    "prefix rows; no source document gives Thai for 'contract fake', 'origin tag' or '-ITG'.",
        "type": "Missing",
        "area": "documentation",
        "severity": "P3",
        "needed_by_wave": "1",
        "legacy_ref": "",
        "owner_role": "TechX",
        "asm": "ASM-C-ACG-1",
        "proposed": "Add the Thai wording once it is confirmed; until then the English cell is the authoritative one and "
                    "the placeholder tells the reader that the wording is outstanding.",
        "wp": "C-ACG",
    },
    {
        "id": "CG-C-ACG-2",
        "title": "Origin tag where one legacy criterion is carried by several new stories",
        "source": "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (section "
                  "R7.2 section 7); _work/msr/plan/split_plan.json (legacy)",
        "section": "7 Acceptance criteria",
        "description": "A legacy story that is split repeats its criteria in more than one new story, because one legacy "
                       "story becomes several service stories. The rule fixes one tag form, '(legacy RWB-...-nnn ACn)', and "
                       "does not say whether the repeated criterion keeps that same tag in every story that carries it or "
                       "whether the tag is qualified by the service.",
        "evidence": "split_plan.json: RWB-E1-001 becomes RWB-P1-E1001-APP, RWB-P7-E1001-APP, RWB-P4-E1001-APP, "
                    "RWB-P8-E1001-APP and RWB-ITG-E1001-ITG. Section R7.2 section 7 gives the tag form with no qualifier.",
        "type": "Ambiguous",
        "area": "documentation",
        "severity": "P3",
        "needed_by_wave": "1",
        "legacy_ref": "RWB-E1-001",
        "owner_role": "TechX",
        "asm": "ASM-C-ACG-2",
        "proposed": "Keep the tag unqualified: it names the legacy story and the criterion number only and is repeated word "
                    "for word wherever the criterion appears; the story key already carries the service.",
        "wp": "C-ACG",
    },
    {
        "id": "CG-C-ACG-3",
        "title": "Name, version and location of a contract fake",
        "source": "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (section "
                  "R5.4 class C, section R5.5 DP-11, section R7.2 section 12.8)",
        "section": "12 Contract; 12.8 Contract fakes",
        "description": "A story with a class C dependency builds against the other service's published contract and its "
                       "fake, and section 12.8 of the story has to list that fake. No source document gives the fake a name, "
                       "a version scheme or a place to publish it, so a Given line can only say 'the <service> contract "
                       "fake'.",
        "evidence": "Section R5.5 DP-11 reads 'REST contract with mock; one hop; 2 s timeout'; section R7.2 section 12.8 "
                    "names the table 'Contract fakes' but not the artefact; the Arch v5 text extract and the Service "
                    "Contract Catalog v1 carry contracts, not fakes.",
        "type": "Missing",
        "area": "contract",
        "severity": "P2",
        "needed_by_wave": "1",
        "legacy_ref": "",
        "owner_role": "TechX",
        "asm": "ASM-C-ACG-3",
        "proposed": "Publish the fake with the contract it fakes, as '<service> contract fake' at the contract's version, "
                    "and let the Given line name that artefact.",
        "wp": "C-ACG",
    },
    {
        "id": "CG-C-ACG-4",
        "title": "Level and register place of an -ITG copy of a test case",
        "source": "22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (section "
                  "R7.2 section 16)",
        "section": "16 Test cases",
        "description": "The rule says that an ITG copy of a test case ends in -ITG. It does not say which Level the copy "
                       "takes (Integration or End to end), whether the plain copy stays in section 16, or whether the copy "
                       "is a separate row in the Test Cases master and the RTM.",
        "evidence": "Section R7.2 section 16 reads 'TC ID, Covers, Level (Unit, Component, Contract, Integration, End to end, "
                    "NFR), Data. ITG copies of a TC end in -ITG.' Only the suffix is specified.",
        "type": "Ambiguous",
        "area": "testing",
        "severity": "P3",
        "needed_by_wave": "1",
        "legacy_ref": "",
        "owner_role": "QA team",
        "asm": "ASM-C-ACG-4",
        "proposed": "Keep the plain ID on the unit, component and contract copy; add the -ITG copy as a separate row at "
                    "Level Integration or End to end and carry it into the Test Cases master and the RTM as its own ID.",
        "wp": "C-ACG",
    },
]

asms = [
    {
        "id": "ASM-C-ACG-1",
        "text": "The Thai cell of the three rows that D-RCV-60 adds carries the section R9 placeholder, and the English cell "
                "is authoritative until Thai wording is confirmed.",
        "why": "No source document gives Thai wording for the new rows, and writing a translation would be inventing a value "
               "that the glossary is meant to fix once.",
        "read": "The source workbook, Sentence frames and Code prefixes sheets, Thai column, all 70 populated rows",
        "gap": "CG-C-ACG-1",
        "applied_in": APPLIED + ", Sentence frames and Code prefixes, the appended rows",
        "confidence": "Medium",
        "confirm": "Business analysis lead",
        "impact": "A Thai reader sees the placeholder on three rows only; every other row is unchanged.",
        "wp": "C-ACG",
    },
    {
        "id": "ASM-C-ACG-2",
        "text": "The origin tag names the legacy story key and the criterion number only, unchanged, and is repeated word "
                "for word in every new story that carries the criterion.",
        "why": "Section R7.2 section 7 fixes one tag form; adding a service qualifier would create a second form and a second "
               "way to read the same criterion.",
        "read": "Section R7.2 section 7; section R5.2 story ID pattern; split_plan.json legacy record of RWB-E1-001",
        "gap": "CG-C-ACG-2",
        "applied_in": APPLIED + ", Code prefixes and Realignment additions",
        "confidence": "High",
        "confirm": "Programme architecture lead",
        "impact": "A tester can trace any criterion to its legacy story from any slice, and no criterion number changes.",
        "wp": "C-ACG",
    },
    {
        "id": "ASM-C-ACG-3",
        "text": "A contract fake is called 'the <service> contract fake', is versioned with the contract it fakes, and is "
                "published beside that contract in the Service Contract Catalog v1.",
        "why": "DP-11 requires a mock for every REST contract and section 12.8 requires the fake to be listed, but no source "
               "names the artefact.",
        "read": "Section R5.4 class C; section R5.5 DP-11; section R7.2 section 12.8; Arch v5 text extract",
        "gap": "CG-C-ACG-3",
        "applied_in": APPLIED + ", Sentence frames and Realignment additions",
        "confidence": "Medium",
        "confirm": "Integration lead",
        "impact": "A class C story can be built and accepted before the other service publishes, which is the point of the "
                  "class C dependency; the fake must exist for that story to be Done.",
        "wp": "C-ACG",
    },
    {
        "id": "ASM-C-ACG-4",
        "text": "The -ITG copy is a separate test case row at Level Integration or End to end; the plain ID stays on the "
                "unit, component and contract copy.",
        "why": "Section R7.2 section 16 calls it a copy and fixes only the suffix, so the original ID cannot be taken away "
               "from the original test case.",
        "read": "Section R7.2 section 16; section R5.4 class I",
        "gap": "CG-C-ACG-4",
        "applied_in": APPLIED + ", Code prefixes and Realignment additions",
        "confidence": "High",
        "confirm": "QA lead",
        "impact": "The Test Cases master and the RTM count the -ITG copy as its own ID, and coverage of the original ID is "
                  "not lost.",
        "wp": "C-ACG",
    },
]

for path, rows in ((GAPS, gaps), (ASMS, asms)):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(path.name, len(rows), "rows")
