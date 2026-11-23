"""Candidate gap and assumption rows for WP B-REQ-PRD-P3 (PRD P3 rwb-case v1).

Run: python -I "_work/msr/docs/B-REQ-PRD-P3/make_rows.py"
Writes _work/msr/gaps/B-REQ-PRD-P3.jsonl and _work/msr/assumptions/B-REQ-PRD-P3.jsonl.
Numbering (GAP-nnnn / ASM-nnnn) is done only by step D1.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3].parent / "22 Microservice Realignment" / "compat"))
from common import WORK, read_jsonl  # noqa: E402

WP = "B-REQ-PRD-P3"
G = WORK / "gaps" / f"{WP}.jsonl"
A = WORK / "assumptions" / f"{WP}.jsonl"

GAPS = [
    dict(
        title="P3 reads the ACE views directly in the FSD, but Arch v5 gives the ACE read path to rwb-source-data only",
        source="Recovery Workbench FSD P3 Case and workflow v4 (A1.5 Source data read path, D-RCV-35); Recovery Workbench Architecture v5 Text Extract v1 slide 45 and slide 41",
        section="PRD P3 §2 Product overview, §9 Integration points, §12 Open questions",
        description=(
            "FSD P3 A1.5 states that the module reads ACE through the recovery.v_ace_* views only and that a direct read "
            "of a public table is a defect. Arch v5 slide 45 states that only rwb-source-data reads the 30 recovery.v_ace_* "
            "views (ADR-010) and that everyone else asks it through REST or a Temporal activity. Arch v5 is higher in the "
            "source precedence order (Template and Rules §R3, item 1 against item 7), so P3 reads ACE data through the "
            "rwb-source-data contract. The FSD wording is not yet realigned."
        ),
        evidence="FSD P3 A1.5 table 'What P3 needs | View | Key the Workbench holds'; Arch v5 slide 45 'Who reads ACE's data? Only rwb-source-data reads the 30 recovery.v_ace_* views'",
        type="Conflict",
        area="Data read path and integration",
        severity="P1",
        needed_by_wave="1",
        legacy_ref="RWB-E1-018; RWB-E1-002; RWB-E2-001",
        owner_role="Solution architect",
        asm="ASM-B-REQ-PRD-P3-7",
        proposed="Restate the FSD P3 A1.5 read path as a read through the rwb-source-data contract; keep the business-key link rules unchanged.",
        wp=WP,
    ),
    dict(
        title="BRD and FSD approval status is not evidenced in the source documents",
        source="Recovery Workbench Business Requirements Program v4; Recovery Workbench Business Requirements Epic 1 v4; Epic 2 v2; Recovery Workbench FSD P3 Case and workflow v4 (Document control)",
        section="PRD P3 §1 Document control, §13 Approval table",
        description=(
            "The converted BRD text carries no governance table with a Product Owner decision, and the FSD P3 document "
            "control states Status 'In review'. The requirements approval gate (Product Owner and FDA) is therefore not "
            "evidenced for this service. The PRD proceeds as Draft with an empty approval table."
        ),
        evidence="FSD P3 Document control: Status 'In review'; no governance table in BRD Program v4, Epic 1 v4 or Epic 2 v2 converted text",
        type="Missing",
        area="Governance",
        severity="P2",
        needed_by_wave="1",
        legacy_ref="",
        owner_role="Product owner",
        asm="ASM-B-REQ-PRD-P3-1",
        proposed="Record the Product Owner and FDA decisions on the BRD, then on this PRD.",
        wp=WP,
    ),
    dict(
        title="FSD P3 file name is v4 while the document states version 3",
        source="_work/msr/extract/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P3 Case and workflow v4.md (Document control)",
        section="PRD P3 §1 Document control",
        description=(
            "The file is named 'FSD P3 Case and workflow v4' and its change note adds version 3 on 15 November 2026, but "
            "the document control block states Document ID 'P3-RWB-FSD-v3' and Version 3. The PRD cites the document as "
            "the v6 folder copy, document version 3."
        ),
        evidence="Document control: Document ID P3-RWB-FSD-v3, Version 3, Date 15 November 2026; file name ends 'v4'",
        type="Conflict",
        area="Document control",
        severity="P3",
        needed_by_wave="1",
        legacy_ref="",
        owner_role="Business analyst, P3",
        asm="",
        proposed="Renumber the file or the document control block in the next FSD version.",
        wp=WP,
    ),
    dict(
        title="The FSD carries no requirement identifiers, so FR mapping uses the BRD REQ IDs and the FSD FEAT, BR and AC codes",
        source="Recovery Workbench FSD P3 Case and workflow v4 (A1.2 Feature overview, A2.x); BRD Program v4 §5.3",
        section="PRD P3 §6 Functional requirements",
        description=(
            "The work package asks for FR-P3-nnn to be mapped to the FSD requirement IDs, but the FSD P3 uses feature codes "
            "(FEAT-CWC-01 to FEAT-CWC-29, FEAT-CHO-01 to FEAT-CHO-11, FEAT-WKM-01 to FEAT-WKM-12), rule IDs (BR-P3-001 to "
            "BR-P3-052) and acceptance criteria (AC-P3-nnn-nn). The only requirement identifiers for this module are the "
            "BRD REQ-CWC, REQ-CHO and REQ-WKM rows. Each PRD FR therefore cites the BRD REQ ID and the FSD FEAT, BR and AC "
            "codes it derives from."
        ),
        evidence="FSD P3 A1.2 and A2.1 to A2.52 heading set; no REQ-* identifier in the document",
        type="Missing",
        area="Traceability",
        severity="P3",
        needed_by_wave="1",
        legacy_ref="",
        owner_role="Business analyst, P3",
        asm="ASM-B-REQ-PRD-P3-3",
        proposed="Add a REQ row per feature in the next FSD version, or keep the FEAT code as the requirement key.",
        wp=WP,
    ),
    dict(
        title="REQ-WKM-010 capacity view is assigned to rwb-case but has no story in the wave plan",
        source="BRD Program v5 §11 (REQ-WKM-010 to RWB-SVC-P3, wave 1, EP07); BRD Program v5 §5.3 (Could); _work/msr/plan/split_plan.json",
        section="PRD P3 §5 Capabilities, §10 Release slicing, §12 Open questions",
        description=(
            "REQ-WKM-010 asks for a capacity view of inflow by product, bucket and region against available capacity, "
            "priority Could for Epic 7. The business requirement trace in BRD Program v5 assigns it to RWB-SVC-P3 in wave 1 "
            "with business epic EP07, but no P3 story in the wave plan carries it and the FSD P3 has no feature for it. The "
            "PRD lists the capability as Could in the wave 4 slice and records that no story exists."
        ),
        evidence="BRD Program v5 §11: 'REQ-WKM-010 | 1 | RWB-SVC-P3 | rwb-case | 1 | EP07'; split_plan.json: 84 P3 slices, none with REQ-WKM-010 in its reqs",
        type="Missing",
        area="Scope and coverage",
        severity="P3",
        needed_by_wave="4",
        legacy_ref="",
        owner_role="Capacity and workforce planner",
        asm="ASM-B-REQ-PRD-P3-14",
        proposed="Raise the story in the wave 4 plan, or retire the requirement with a recorded decision.",
        wp=WP,
    ),
    dict(
        title="Case closure is one requirement with rwb-writeoff and one case state change with rwb-case",
        source="BRD Program v5 §11 (REQ-S7-008 to RWB-SVC-S7, wave 4, EP06); BRD Epics 3 to 8 v1 BR-057 and RULE-022; Recovery Workbench Epics 3 to 8 Specification v3 (E6, S7, FEAT-WOF-13); split_plan.json slice RWB-P3-E6025-APP",
        section="PRD P3 §5 Capabilities, §6 Functional requirements, §12 Open questions",
        description=(
            "REQ-S7-008 closes a case after its retention period and requires a written rule, a reason and an approver to "
            "reopen it; the business requirement trace assigns it to RWB-SVC-S7. The case state model and the case record "
            "belong to rwb-case, and the wave plan holds a P3 slice for the closure (RWB-P3-E6025-APP, wave 4). The PRD "
            "states the case state transition in this service and leaves the closure rule and the approval to rwb-writeoff."
        ),
        evidence="BRD Program v5 §11 row 'REQ-S7-001 to REQ-S7-008 ... RWB-SVC-S7'; split_plan.json RWB-P3-E6025-APP wave 4",
        type="Conflict",
        area="Scope and ownership",
        severity="P2",
        needed_by_wave="4",
        legacy_ref="",
        owner_role="Solution architect",
        asm="ASM-B-REQ-PRD-P3-6",
        proposed="P3 moves the case to closed and keeps the record; S7 holds the closure rule, the reason and the approver.",
        wp=WP,
    ),
    dict(
        title="No retention period is set for any case record class",
        source="BRD Program v4 §6.5 NFR-031 (Open, DL26); FSD P3 A2.52 and glossary",
        section="PRD P3 §8 Data requirements, §7 Non-functional requirements, §12 Open questions",
        description=(
            "NFR-031 requires a retention and archive rule per record class and a case that closes after its retention "
            "period, but the periods are 'Not set' and DL26 is open. The PRD therefore cannot state a retention period for "
            "the case, its tasks, timers, queue history or decision records."
        ),
        evidence="BRD Program v4 NFR-031: Target 'Not set', Status 'Open, DL26'",
        type="Missing",
        area="Retention and compliance",
        severity="P2",
        needed_by_wave="1",
        legacy_ref="",
        owner_role="Compliance",
        asm="ASM-B-REQ-PRD-P3-15",
        proposed="Set the period per record class under DL26 before the wave 4 closure feature is built.",
        wp=WP,
    ),
    dict(
        title="Non-functional target values are open under DL11",
        source="BRD Program v4 §6.4 NFR-022 and NFR-023; §6.5 NFR-031; §6.11 NFR-060 (Open, DL11)",
        section="PRD P3 §7 Non-functional requirements",
        description=(
            "The recovery point and recovery time objectives carry no value and the accessibility standard carries no "
            "conformance date, because DL11 is open. The PRD records the open value rather than inventing one."
        ),
        evidence="NFR-022 and NFR-023: Target 'The ACE recovery point objective' / 'The ACE recovery time objective', Status 'Open, DL11'",
        type="Ambiguous",
        area="Non-functional",
        severity="P3",
        needed_by_wave="1",
        legacy_ref="",
        owner_role="Solution architect with Risk",
        asm="ASM-B-REQ-PRD-P3-8",
        proposed="Adopt the ACE values for RPO and RTO and record them under DL11.",
        wp=WP,
    ),
    dict(
        title="DL43 is open: the ACE Tier 2 tables, columns and fields are not accepted, so dependent P3 features stay behind flags",
        source="BRD Program v4 §7 Constraints and §9 (DL43); FSD P3 A1.1 Constraints",
        section="PRD P3 §2 Product overview, §7 Non-functional requirements, §10 Release slicing",
        description=(
            "The ACE team has not accepted RWB-ACE-001 (14 tables, 12 columns, 80 source fields) or its dates. The P3 "
            "features that read the Tier 2 additions (batch status, party product, credit decision) stay behind their "
            "feature flags until the additions land. The PRD marks those FRs as flag-gated in wave 1."
        ),
        evidence="BRD Program v4 DL43: 'Open. The build assumes the scope is accepted'; FSD P3 A1.1 Constraints",
        type="Outdated",
        area="Dependency",
        severity="P2",
        needed_by_wave="1",
        legacy_ref="RWB-ACE-001",
        owner_role="ACE team lead",
        asm="ASM-B-REQ-PRD-P3-11",
        proposed="Record the ACE team's acceptance, or state the fallback date for each flag-gated feature.",
        wp=WP,
    ),
    dict(
        title="The parameter and reference-data load interface is claimed by P4 in the API specification and by P3 in the default ruling",
        source="Recovery Workbench API Specification v4 (x-module P4, API-P4-004 to API-P4-010); _work/msr/plan/ownership.json rulings (ASM-A6-api-4)",
        section="PRD P3 §2 Product overview, §9 Integration points, §12 Open questions",
        description=(
            "The API specification puts the list and reference-load paths in rwb-access, while the R-PREC default ruling "
            "in Template and Rules §R3 puts parameters and reference data (E1-042, E1-043) with P3 rwb-case. The ownership "
            "map follows the default ruling and gives P3 the paths, so the PRD states P3 as the owner and records the "
            "specification conflict."
        ),
        evidence="ownership.json: GET /admin/lists/{listCode}, POST /admin/reference-loads and three sibling paths owned by P3 with ruling ASM-A6-api-4",
        type="Conflict",
        area="Contract ownership",
        severity="P2",
        needed_by_wave="1",
        legacy_ref="RWB-E1-042; RWB-E1-043",
        owner_role="Solution architect",
        asm="ASM-B-REQ-PRD-P3-10",
        proposed="Realign the API specification x-module for the five list and reference-load paths to P3.",
        wp=WP,
    ),
    dict(
        title="The encumbrance slice is labelled wave 3 although its business epic is released in the wave 2 window",
        source="_work/msr/plan/split_plan.json slice RWB-P3-E3013-APP; BRD Program v5 §10.3 (EP02 and EP03 in wave 2, released 31 December 2026 and 31 January 2027)",
        section="PRD P3 §10 Release slicing, §12 Open questions",
        description=(
            "Slice RWB-P3-E3013-APP (check encumbrance and eligibility before negotiation) belongs to business epic EP03. "
            "BRD Program v5 places EP03 in wave 2 with a 31 January 2027 release, while the split plan gives the slice wave "
            "3 and the same 31 January 2027 date. The release date agrees; the wave label does not. The PRD slices it in "
            "the wave 2 window at its planned date and records the label conflict."
        ),
        evidence="split_plan.json: RWB-P3-E3013-APP wave 3, business_epic EP03, release 31 January 2027; BRD Program v5 §10.3 wave 2 row",
        type="Conflict",
        area="Release planning",
        severity="P3",
        needed_by_wave="2",
        legacy_ref="",
        owner_role="Program manager",
        asm="ASM-B-REQ-PRD-P3-14",
        proposed="Relabel the slice as wave 2 in the plan, or record why an EP03 slice is delivered outside its wave window.",
        wp=WP,
    ),
    dict(
        title="The queue write interface for models and agents has no approved consumer and no flag removal date",
        source="BRD Program v4 §5.3 REQ-CWC-017 to REQ-CWC-020; FSD P3 FEAT-CWC-29 and A2.52",
        section="PRD P3 §5 Capabilities, §10 Release slicing, §12 Open questions",
        description=(
            "REQ-CWC-019 requires the interface to ship behind a feature flag and to be switched on when the first model "
            "is approved. No model or agent is approved in the source documents, and the flag carries no removal date, "
            "although FEAT-CWC-26 requires every flag to carry the date it must be removed."
        ),
        evidence="FSD P3 A2.52: 'Disabled by feature flag until a consumer exists'; A2.26 dated feature flags",
        type="Missing",
        area="Scope and AI",
        severity="P3",
        needed_by_wave="2",
        legacy_ref="RWB-E2-036",
        owner_role="AI product owner",
        asm="ASM-B-REQ-PRD-P3-13",
        proposed="Name the first approved consumer and the flag removal date before the wave 2 release.",
        wp=WP,
    ),
    dict(
        title="Duplicate case merge has no feature or acceptance criteria in the FSD",
        source="BRD Program v4 §5.3 REQ-CHO-010 (Should, E2); FSD P3 A2.2",
        section="PRD P3 §5 Capabilities, §6 Functional requirements",
        description=(
            "REQ-CHO-010 requires a duplicate case for the same customer and product to merge into the earlier case, "
            "carrying its documents and decision log. The FSD P3 describes one case per customer and product but has no "
            "merge feature, no rule ID and no acceptance criterion for it."
        ),
        evidence="FSD P3 A2.2 business rules table holds BR-P3-002 only; no merge AC in AC-P3-002",
        type="Missing",
        area="Functional coverage",
        severity="P3",
        needed_by_wave="2",
        legacy_ref="",
        owner_role="Case owner",
        asm="ASM-B-REQ-PRD-P3-12",
        proposed="Add a merge feature, rule and acceptance criteria to the next FSD version.",
        wp=WP,
    ),
    dict(
        title="Four P3 slices in the wave plan carry no business requirement row",
        source="_work/msr/plan/split_plan.json slices RWB-P3-E3013-APP, RWB-P3-E5002-APP, RWB-P3-E6017-APP and RWB-P3-E6025-APP",
        section="PRD P3 §10 Release slicing, §6 Functional requirements",
        description=(
            "Four P3 slices carry an empty requirement list: check encumbrance and eligibility before negotiation "
            "(EP03, wave 3), record proof of delivery on a notice (EP05, wave 3), route the population to the committee and "
            "schedule it (EP06, wave 4) and close the case after the retention period (EP06, wave 4). Only the closure "
            "slice can be traced to a live requirement (NFR-031); the other three have no BRD row, so the PRD lists them as "
            "later increments without an FR."
        ),
        evidence="split_plan.json: the four slices have reqs []",
        type="Missing",
        area="Scope and traceability",
        severity="P3",
        needed_by_wave="3",
        legacy_ref="RWB-E3-013; RWB-E5-002; RWB-E6-017; RWB-E6-025",
        owner_role="Product owner",
        asm="ASM-B-REQ-PRD-P3-16",
        proposed="Add a BRD row per slice, or retire the slice with a recorded decision.",
        wp=WP,
    ),
    dict(
        title="The BRD assigns payment matching to rwb-case while Architecture v5 gives it to rwb-payment",
        source="BRD Program v5 §5.3 and §11 (REQ-CHO-009 to RWB-SVC-P3, wave 1, EP02); Architecture v5 slide 41 (rwb-payment owns payment and proceeds matching)",
        section="PRD P3 §5 Capabilities, §6 Functional requirements, §9 Integration points, §12 Open questions",
        description=(
            "REQ-CHO-009 requires payments received to be matched to the plan, the settlement or the fee they belong to and "
            "anything unmatched to reach an exception list. BRD Program v5 keeps the row in module 5.3 and assigns it to "
            "RWB-SVC-P3, while Architecture v5 gives payment and proceeds matching to rwb-payment (P8) and no P3 slice in "
            "the wave plan carries the requirement. The PRD states the case-facing duty (the matched payment and the "
            "unmatched exception on the case, read through the P8 contract) and leaves the matching rule in P8."
        ),
        evidence="BRD Program v5 §11 row 'REQ-CHO-001 to REQ-CHO-010 | 10 | RWB-SVC-P3'; Architecture v5 slide 41 row P8; split_plan.json: no P3 slice carrying REQ-CHO-009",
        type="Conflict",
        area="Scope and ownership",
        severity="P2",
        needed_by_wave="2",
        legacy_ref="RWB-E2-009",
        owner_role="Solution architect",
        asm="ASM-B-REQ-PRD-P3-17",
        proposed="Name the P3 duty (exception visibility on the case) and the P8 duty (the matching rule) in both PRDs.",
        wp=WP,
    ),
]

ASMS = [
    dict(
        text="The BRD and this PRD are treated as not yet approved; the PRD is issued as Draft with an empty approval table.",
        why="No Product Owner or FDA decision is evidenced in the converted BRD text, and the FSD P3 status is 'In review'.",
        read="Status Draft; the approval table stays empty; no requirement is marked approved.",
        gap="CG-B-REQ-PRD-P3-2",
        applied_in="PRD P3 §1, §13",
        confidence="High",
        confirm="Product owner",
        impact="The requirements approval gate is open; the backlog may not be drafted as approved.",
        wp=WP,
    ),
    dict(
        text="PRD identifiers use the module infix: CAP-P3-nnn, FR-P3-nnn, NFR-P3-nnn, AC-P3-nnn. None of them exists in a legacy artefact.",
        why="The work package asks for CAP-, FR-, NFR- and AC- identifiers on a service-scoped PRD and the FSD already uses AC-P3-nnn-nn for its own criteria.",
        read="Four-part FSD criteria are cited as 'AC-P3-nnn-nn (FSD)'; the three-part PRD criteria are new.",
        gap="CG-B-REQ-PRD-P3-4",
        applied_in="PRD P3 §1, §6, §7, §11",
        confidence="High",
        confirm="Business analyst, P3",
        impact="No collision with the legacy or FSD identifier space.",
        wp=WP,
    ),
    dict(
        text="Each FR cites the BRD REQ ID as its business requirement and the FSD FEAT, BR-P3 and AC-P3 codes as its functional detail.",
        why="The FSD carries no REQ identifiers, so the BRD REQ ID is the only requirement key available for traceability.",
        read="Traceability runs BRD REQ -> CAP -> FR -> AC, with the FSD feature and rule codes recorded on the FR row.",
        gap="CG-B-REQ-PRD-P3-4",
        applied_in="PRD P3 §5, §6, §11",
        confidence="High",
        confirm="Business analyst, P3",
        impact="A reader can follow a requirement from the BRD to the FSD feature and back.",
        wp=WP,
    ),
    dict(
        text="The PRD is scoped to P3 rwb-case. Requirements owned by the other 18 services appear only as dependencies and integration points.",
        why="Template and Rules §R8.5 issues one PRD per service plus Platform, so a module requirement is stated once, in its owner's PRD.",
        read="A REQ row owned by P1, P4, P5, P6, P7, P9 or P10 is not restated; the dependency is named instead.",
        gap="",
        applied_in="PRD P3 §2, §5, §9",
        confidence="High",
        confirm="Product owner",
        impact="No duplicate requirements across the twenty PRDs.",
        wp=WP,
    ),
    dict(
        text="Release slicing follows the wave in the split plan and the release dates in BRD Program v4 §8, each marked (tentative).",
        why="Template and Rules §U7 keeps the dates unchanged and tentative and never raises a date as a gap.",
        read="Wave 1 = 30 November 2026; wave 2 = 31 December 2026; waves 3 and 4 = 31 January 2027, 31 March 2027, 30 April 2027 and 30 June 2027, all (tentative).",
        gap="",
        applied_in="PRD P3 §10",
        confidence="High",
        confirm="Program manager",
        impact="A change of date changes the slicing table, not the requirements.",
        wp=WP,
    ),
    dict(
        text="P3 owns the case state and its closure; S7 raises the write-off closure decision through its contract and does not write the case state.",
        why="The case state model and the case record belong to P3 in Arch v5 slide 41 and the ownership map, while the Epics 3 to 8 specification lists closure under S7.",
        read="The closure feature is stated in this PRD; the write-off committee decision stays with S7.",
        gap="CG-B-REQ-PRD-P3-6",
        applied_in="PRD P3 §5, §9",
        confidence="Medium",
        confirm="Solution architect",
        impact="A wave 4 story split that does not duplicate the write-off decision.",
        wp=WP,
    ),
    dict(
        text="P3 reads ACE data through the rwb-source-data contract and never reads recovery.v_ace_* itself, even though FSD P3 A1.5 describes a direct view read.",
        why="Arch v5 slide 45 and ADR-010 give the ACE read path to rwb-source-data only, and Arch v5 precedes the FSD in the source precedence order (Template and Rules §R3).",
        read="The eligible-account list, the account and customer facts and the freshness stamp arrive from P1; P3 holds the business key that links to them.",
        gap="CG-B-REQ-PRD-P3-1",
        applied_in="PRD P3 §2, §9",
        confidence="Medium",
        confirm="Solution architect",
        impact="The FSD P3 A1.5 read path must be restated before wave 1 build.",
        wp=WP,
    ),
    dict(
        text="The recovery point and recovery time objectives adopt the ACE values; the value of each is left open until DL11 is answered.",
        why="BRD NFR-022 and NFR-023 state the target as the ACE objective and mark the row Open, DL11.",
        read="The PRD states the requirement and the dependency; it states no value.",
        gap="CG-B-REQ-PRD-P3-8",
        applied_in="PRD P3 §7, §12",
        confidence="High",
        confirm="IT lead with Operational risk",
        impact="The availability section of the non-functional test plan cannot be baselined.",
        wp=WP,
    ),
    dict(
        text="Data classification is proposed per entity from its content (PII, sensitive financial, confidential) and is treated as unapproved until DL26 sets the scheme.",
        why="BRD NFR-047 states that every data product carries a classification and that the scheme is 'to be applied', and DL26 is open.",
        read="The data requirements table carries a proposed classification with the content that drives it.",
        gap="CG-B-REQ-PRD-P3-7",
        applied_in="PRD P3 §8",
        confidence="Medium",
        confirm="Compliance with security",
        impact="Masking, retention and handling follow the proposed class until Compliance ratifies it.",
        wp=WP,
    ),
    dict(
        text="The five list and reference-load interface paths are P3's, following the R-PREC default ruling, and P4 owns only roles, scope, masking and the delegation of authority.",
        why="The default ruling in Template and Rules §R3 gives parameters and reference data to P3 while the API specification names P4; the ownership map follows the ruling.",
        read="P3 provides the parameter catalog, the reference data service and their load, verify and rollback paths; it consumes P4's authorise contract.",
        gap="CG-B-REQ-PRD-P3-10",
        applied_in="PRD P3 §5, §9",
        confidence="Medium",
        confirm="Solution architect",
        impact="The P3 and P4 contract baselines must agree before wave 1.",
        wp=WP,
    ),
    dict(
        text="The P3 features that read the ACE Tier 2 additions ship behind a dated feature flag in wave 1.",
        why="DL43 is open, so the ACE additions and their dates are not confirmed, and the FSD keeps those features behind their flags.",
        read="The FR is in the wave 1 slice with the flag off; the flag date is the condition for switching it on.",
        gap="CG-B-REQ-PRD-P3-9",
        applied_in="PRD P3 §7, §10",
        confidence="Medium",
        confirm="ACE team lead",
        impact="A late ACE addition does not move the wave 1 release.",
        wp=WP,
    ),
    dict(
        text="Duplicate case merge is kept in scope as a Should at wave 2 with its rule and acceptance criteria to be added to the FSD.",
        why="REQ-CHO-010 is a live BRD requirement but the FSD has no feature, rule or criterion for it.",
        read="The capability appears in §5 and the FR in §6 with the gap noted on the row.",
        gap="CG-B-REQ-PRD-P3-13",
        applied_in="PRD P3 §5, §6",
        confidence="Low",
        confirm="Case owner",
        impact="A wave 2 story cannot be sized until the FSD describes the merge.",
        wp=WP,
    ),
    dict(
        text="The queue write interface for models and agents is built dark in wave 2 and switched on only when a consumer is approved.",
        why="REQ-CWC-019 requires the flag and no approved consumer is named in the sources.",
        read="The interface is a wave 2 deliverable with the flag off; no removal date is asserted.",
        gap="CG-B-REQ-PRD-P3-12",
        applied_in="PRD P3 §5, §10, §12",
        confidence="Medium",
        confirm="AI product owner",
        impact="An unused interface is carried until a consumer is approved.",
        wp=WP,
    ),
    dict(
        text="The capacity view (REQ-WKM-010) is sliced with business epic EP07 in the wave 4 window at 31 May 2027 (tentative) although no story exists for it, and the encumbrance slice keeps its planned 31 January 2027 date inside the wave 2 window.",
        why="The BRD trace gives REQ-WKM-010 to rwb-case with EP07 but the wave plan holds no story; the encumbrance slice is labelled wave 3 while BRD Program v5 releases EP03 on 31 January 2027 in the wave 2 window.",
        read="Both appear in §10 with the conflict recorded; neither moves the wave 1 or wave 2 capability set.",
        gap="CG-B-REQ-PRD-P3-5; CG-B-REQ-PRD-P3-11",
        applied_in="PRD P3 §10",
        confidence="Low",
        confirm="Program manager",
        impact="One requirement has no story and one slice carries the wrong wave label.",
        wp=WP,
    ),
    dict(
        text="No retention period is stated: the case record classes are carried as DL26 open, and the PRD states the requirement and the variable, not a period.",
        why="BRD NFR-031 sets the retention and archive rule per record class but leaves the period 'Not set' under DL26.",
        read="The data requirements table gives the record class and the retention variable; the period is 'Not specified in the source documents (CG-B-REQ-PRD-P3-7; ASM-B-REQ-PRD-P3-15)'.",
        gap="CG-B-REQ-PRD-P3-7",
        applied_in="PRD P3 §8",
        confidence="High",
        confirm="Compliance",
        impact="The retention job and the case closure feature cannot be baselined before DL26.",
        wp=WP,
    ),
    dict(
        text="The three slices with no requirement row (encumbrance check, proof of delivery, committee routing) stay in the later waves as delivery items and are not given an FR in this PRD.",
        why="The split plan gives them an empty requirement list and no BRD row could be found for them in the sources read.",
        read="They appear in §10 as later increments with the gap noted; the wave 1 and wave 2 scope is unaffected.",
        gap="CG-B-REQ-PRD-P3-14",
        applied_in="PRD P3 §10",
        confidence="Low",
        confirm="Product owner",
        impact="Three delivery items are scheduled without a traceable requirement.",
        wp=WP,
    ),
    dict(
        text="The case shows the matched payment and lists the unmatched payment as an exception for the case owner, while the matching rule itself stays with rwb-payment (P8).",
        why="BRD Program v5 assigns REQ-CHO-009 to rwb-case, while Architecture v5 and the wave plan place payment and proceeds matching in rwb-payment.",
        read="The FR states the case-facing duty only; the matching outcome arrives through the P8 contract and no matching rule is held in this service.",
        gap="CG-B-REQ-PRD-P3-15",
        applied_in="PRD P3 §5, §6, §9",
        confidence="Medium",
        confirm="Solution architect",
        impact="One requirement is delivered across two services, so both PRDs must state their half.",
        wp=WP,
    ),
]


def main():
    for p, rows in ((G, GAPS), (A, ASMS)):
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            p.unlink()
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            for i, r in enumerate(rows, 1):
                rid = ("CG-" if p is G else "ASM-") + f"{WP}-{i}"
                r = {"id": rid, **{k: v for k, v in r.items() if k != "id"}}
                f.write(__import__("json").dumps(r, ensure_ascii=False) + "\n")
    print("gaps", len(GAPS), "assumptions", len(ASMS))
    print("ids", [r["id"] for r in read_jsonl(G)] + [r["id"] for r in read_jsonl(A)])


if __name__ == "__main__":
    main()
