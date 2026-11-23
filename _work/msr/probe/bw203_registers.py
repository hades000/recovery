import io, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "_work" / "msr"
WP = "B-ITG-W2-03"

gaps = [
    {
        "id": "CG-B-ITG-W2-03-E2012-1",
        "title": "Gateway-bff composite transfer route, harness environment, seeding, evidence format and gate not specified",
        "source": "Template and Rules v1 R7.2 and R9; Architecture v5 Text Extract v1; legacy RWB-E2-012 sections 12 and 15",
        "section": "12.8 Contract fakes; 13 Solution plan; 15 Screens and states",
        "description": "No source read gives the gateway-bff composite transfer route path and its merge order, the harness repository and environment, its test-data seeding, its evidence format and retention, or its pass/fail gate.",
        "evidence": "No source read gives these values; ownership.json gives owners and operations only",
        "type": "Missing",
        "area": "Integration and test",
        "severity": "P2",
        "needed_by_wave": 2,
        "legacy_ref": "RWB-E2-012",
        "owner_role": "Integration lead",
        "asm": "ASM-B-ITG-W2-03-E2012-1",
        "proposed": "The platform edge story and the integration lead agree the composite route path and merge order, the harness repository and SIT environment, the seeded data, the per-run evidence format and retention, and the pass/fail gate at the wave 2 entry check.",
        "wp": WP,
    },
    {
        "id": "CG-B-ITG-W2-03-E2013-1",
        "title": "Approval-routing harness environment, composite queue route and evidence format are not specified",
        "source": "Template and Rules v1 R7.2 and R9; Architecture v5 Text Extract v1; legacy RWB-E2-013 sections 12 and 15",
        "section": "12.8 Contract fakes; 13 Solution plan; 15 Screens and states",
        "description": "No source read gives the gateway-bff composite approval-queue route path and its merge order, the harness environment and its seeding of delegation versions, holders and service-level clocks, the evidence format and retention, or the pass/fail gate.",
        "evidence": "No source read gives these values; ownership.json gives owners and operations only",
        "type": "Missing",
        "area": "Integration and test",
        "severity": "P2",
        "needed_by_wave": 2,
        "legacy_ref": "RWB-E2-013",
        "owner_role": "Integration lead",
        "asm": "ASM-B-ITG-W2-03-E2013-1",
        "proposed": "Agree the composite route and merge order with the platform edge owner, and the harness environment, seeding, evidence format, retention and gate with QA at the wave 2 entry check; hold the values as data in the harness pack, not in the story.",
        "wp": WP,
    },
    {
        "id": "CG-B-ITG-W2-03-E2014-1",
        "title": "Integration harness values for the D7.1 decision-screen journey are not specified",
        "source": "Template and Rules v1 R7.2 and R9; Architecture v5 Text Extract v1; legacy RWB-E2-014 sections 12 and 15",
        "section": "12.8 Contract fakes; 13 Solution plan; 15 Screens and states",
        "description": "The gateway-bff composite decision-screen route path and its merge order, the notice and input fixtures and their business dates, the harness environment and its seeding, the evidence format and retention, and the pass/fail gate for the 16:00 eligibility assertion are all missing from the sources read.",
        "evidence": "No source read gives these values; ownership.json gives owners and operations only",
        "type": "Missing",
        "area": "Integration and test",
        "severity": "P2",
        "needed_by_wave": 2,
        "legacy_ref": "RWB-E2-014",
        "owner_role": "Integration lead",
        "asm": "ASM-B-ITG-W2-03-E2014-1",
        "proposed": "The integration lead agrees the composite decision-screen route and merge order with the platform edge owner, and the fixture set with business dates, the SIT environment, the evidence format, its retention and the pass/fail gate with QA at the wave 2 entry check.",
        "wp": WP,
    },
    {
        "id": "CG-B-ITG-W2-03-E2015-1",
        "title": "Wave 2 case-record harness: composite route, timer and deviation fixtures, environment and evidence format undefined",
        "source": "Template and Rules v1 R7.2 and R9; Architecture v5 Text Extract v1; legacy RWB-E2-015 sections 12 and 15",
        "section": "12.8 Contract fakes; 13 Solution plan; 15 Screens and states",
        "description": "No source read gives the gateway-bff composite case-record route path or its merge order, the timer and deviation fixtures with their fixed clocks, the harness environment and seeding, the evidence format and retention, or the pass/fail gate.",
        "evidence": "No source read gives these values; ownership.json gives owners and operations only",
        "type": "Missing",
        "area": "Integration and test",
        "severity": "P2",
        "needed_by_wave": 2,
        "legacy_ref": "RWB-E2-015",
        "owner_role": "Integration lead",
        "asm": "ASM-B-ITG-W2-03-E2015-1",
        "proposed": "Agree the route path, merge order, fixtures, seeding, evidence format, retention and pass/fail gate with the platform edge story and QA at the wave 2 entry check, and record them in the harness pack.",
        "wp": WP,
    },
    {
        "id": "CG-B-ITG-W2-03-E2016-1",
        "title": "Gateway-bff composite timeline route, harness environment and evidence gate are not specified",
        "source": "Template and Rules v1 R7.2 and R9; Architecture v5 Text Extract v1; legacy RWB-E2-016 sections 12 and 15",
        "section": "12.8 Contract fakes; 13 Solution plan; 15 Screens and states",
        "description": "No source read gives the gateway-bff composite timeline route path and its merge order, the 4,000-item fixture and its seeding, the harness environment, the evidence format and retention, or the pass/fail gate and its 2 s percentile method, so the harness cannot be completed or accepted without a stated position on all five.",
        "evidence": "No source read gives these values; ownership.json gives owners and operations only",
        "type": "Missing",
        "area": "Integration and test",
        "severity": "P2",
        "needed_by_wave": 2,
        "legacy_ref": "RWB-E2-016",
        "owner_role": "Integration lead",
        "asm": "ASM-B-ITG-W2-03-E2016-1",
        "proposed": "The integration lead agrees the composite timeline route path and merge order with the platform edge story, seeds the 4,000-item case from the fixture pack, and agrees the SIT environment, the evidence format, its retention and the pass/fail gate with QA before the wave 2 exit.",
        "wp": WP,
    },
]

assumptions = [
    {
        "id": "ASM-B-ITG-W2-03-E2012-1",
        "text": "The harness runs in SIT against the published contracts and replaces each fake as its I story lands; its evidence is a per-run report keyed by story and business date; the composite transfer route belongs to the platform edge story.",
        "why": "The sources name no composite route path or merge order and no harness repository, environment, seeding, evidence format, retention or gate, and the run cannot wait for a decision.",
        "read": "Template and Rules v1 R5.5 DP-19, R7.2 and R9; Architecture v5 Text Extract v1 slides 13, 14 and 20; legacy RWB-E2-012 sections 12 and 15",
        "gap": "CG-B-ITG-W2-03-E2012-1",
        "applied_in": "RWB-ITG-E2012-ITG sections 12.8, 13, 15",
        "confidence": "Medium",
        "confirm": "Integration lead and QA lead at the wave 2 entry check",
        "impact": "The harness runs on the fakes from Day 1; only the real-service cut-over and the evidence sign-off wait for confirmation.",
        "wp": WP,
    },
    {
        "id": "ASM-B-ITG-W2-03-E2013-1",
        "text": "The approval-routing harness runs in SIT against the published contracts, replaces each fake as its I story lands, records evidence as a per-run report keyed by story and business date, and drives the escalation with a fixed clock in the harness.",
        "why": "The source documents name no harness environment, seeding, evidence format, retention or gate, and no composite approval-queue route path or merge order, so the harness is defined as contract-first and test-only and the open values are held as data.",
        "read": "Template and Rules v1 R5.5 DP-08 and DP-19, R7.2 and R9; Architecture v5 Text Extract v1 slides 13, 14 and 20; legacy RWB-E2-013 sections 12 and 15",
        "gap": "CG-B-ITG-W2-03-E2013-1",
        "applied_in": "RWB-ITG-E2013-ITG sections 12.8, 13, 15",
        "confidence": "Medium",
        "confirm": "Integration lead and QA lead at the wave 2 entry check",
        "impact": "The harness runs on the published contracts and fakes from Day 1, so no build wait; only the real-service cut-over and the evidence sign-off wait for the route path, seeding and gate to be agreed.",
        "wp": WP,
    },
    {
        "id": "ASM-B-ITG-W2-03-E2014-1",
        "text": "The harness runs in SIT against published contracts, replaces each fake as its I story lands, keeps evidence as a per-run report keyed by story and business date, and asserts the 16:00 eligibility from the notice state and the approval and never from rwb-integration.",
        "why": "The sources fix the owners, the operations and the journey values but give no gateway route path or merge order, no fixture set with business dates, no evidence format or retention and no pass/fail gate.",
        "read": "Template and Rules v1 R5.5 DP-19, R7.2 and R9; Architecture v5 Text Extract v1 slides 13, 14, 17 and 20; legacy RWB-E2-014 sections 12 and 15",
        "gap": "CG-B-ITG-W2-03-E2014-1",
        "applied_in": "RWB-ITG-E2014-ITG sections 12.8, 13, 15",
        "confidence": "Medium",
        "confirm": "Integration lead and QA lead at the wave 2 entry check",
        "impact": "The harness runs on the 12.8 fakes from Day 1 and proves the journey before the I stories land; only the real-service cut-over and the evidence sign-off wait for the confirmation.",
        "wp": WP,
    },
    {
        "id": "ASM-B-ITG-W2-03-E2015-1",
        "text": "The harness runs in SIT against the published contracts, replaces each fake as its I story lands, drives the timers with a fixed clock and seeded timer rows rather than a live scheduler, and its evidence is a per-run report keyed by story and business date.",
        "why": "The sources fix the owners, the operations and the events but give no route path, fixture, environment, evidence or gate definition, and the harness must run from Day 1 on the fakes.",
        "read": "Template and Rules v1 R5.5 DP-10 and DP-19, R7.2 and R9; Architecture v5 Text Extract v1 slides 13, 14, 15, 42 and 44; legacy RWB-E2-015 sections 12 and 15",
        "gap": "CG-B-ITG-W2-03-E2015-1",
        "applied_in": "RWB-ITG-E2015-ITG sections 12.8, 13, 15",
        "confidence": "Medium",
        "confirm": "Integration lead and QA lead at the wave 2 entry check",
        "impact": "The harness runs on fakes and fixed clocks from Day 1 and only the real-service cut-over and evidence sign-off wait; no service behaviour, business rule or release date changes.",
        "wp": WP,
    },
    {
        "id": "ASM-B-ITG-W2-03-E2016-1",
        "text": "The harness runs in SIT against the published contracts, replaces each fake as its I story lands, measures the first page over 20 runs at the 95th percentile, and its evidence is a per-run report keyed by story and business date.",
        "why": "No source read gives the gateway-bff composite timeline route path and merge order, the 4,000-item fixture seeding, the harness environment, the evidence format and retention, or the pass/fail gate; the harness cannot be built or accepted without a stated position.",
        "read": "Template and Rules v1 R5.5 DP-11 and DP-19, R7.2 and R9; Architecture v5 Text Extract v1 slides 13, 14, 16, 17 and 20; legacy RWB-E2-016 sections 12 and 15",
        "gap": "CG-B-ITG-W2-03-E2016-1",
        "applied_in": "RWB-ITG-E2016-ITG sections 12.8, 13, 15",
        "confidence": "Medium",
        "confirm": "Integration lead and QA lead at the wave 2 entry check",
        "impact": "The harness runs on the section 12.8 fakes from Day 1; only the real-service cut-over, the 4,000-item sign-off and the evidence gate wait for the two I stories and the QA agreement.",
        "wp": WP,
    },
]

for name, rows in (("gaps", gaps), ("assumptions", assumptions)):
    p = WORK / name / f"{WP}.jsonl"
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    print(name, len(rows), p)

# validate
for name in ("gaps", "assumptions"):
    p = WORK / name / f"{WP}.jsonl"
    n = 0
    for line in io.open(p, encoding="utf-8"):
        if line.strip():
            json.loads(line); n += 1
    print("valid", name, n)
