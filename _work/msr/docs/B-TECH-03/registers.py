"""Write the gap and assumption candidate rows for WP B-TECH-03."""
import json
from pathlib import Path

WP = "B-TECH-03"
WORK = Path(r'_work/msr')

gaps = [
    dict(n=1, title="P1 keeps a lake copy after the data lake is removed",
         source="TSD P1 v3 (T1, T2, T3.1 lake_copy_watermark) against Architecture v5 and DP-17",
         section="T0.2, T3, T5.2",
         description="TSD P1 v3 keeps the decision log copy to the data lake and the lake_copy_watermark table. "
                     "Architecture v5 (ADR-018) and DP-17 remove the data lake, and rwb-reporting reads events "
                     "instead.",
         evidence="Arch v5 slide 41 lists lake_copy_watermark as a P1 table; ADR-018 and Template and Rules R5.5 "
                  "DP-17 remove the data lake; TSD P1 v3 T1 keeps 'the decision log copy to the data lake'.",
         type="Conflict", area="Data", severity="P2", needed_by_wave="1",
         legacy_ref="RWB-E1-014, RWB-E1-002", owner_role="Solution architect", asm="ASM-B-TECH-03-2",
         proposed="Keep lake_copy_watermark as the watermark of the last published reporting projection and drop "
                   "the lake extract INT-19 and INT-20 (DP-17)."),
    dict(n=2, title="TSD P2 names platform tables and one P1 table as its own",
         source="TSD P2 v3 T3.1 against Microservice Ownership Map v1 Tables sheet",
         section="T0.2, T3, T5.2",
         description="T3.1 of TSD P2 lists outbox_event, outbox_delivery, processed_event, idempotency_key, "
                     "feature_flag and feature_flag_change, which are shared-library tables, and efs_ledger_outcome, "
                     "which the Ownership Map places with P1. The map has three P2 business tables only.",
         evidence="Ownership Map Tables sheet: interface_config, job_catalog and outbound_item for P2; Architecture "
                  "v5 slide 41 the same three; TSD P2 v3 T3.1 lists ten objects.",
         type="Conflict", area="Data", severity="P3", needed_by_wave="1",
         legacy_ref="RWB-E1-044, RWB-TE-006", owner_role="Solution architect", asm="ASM-B-TECH-03-3",
         proposed="Build the platform tables once in the shared libraries (RWB-PLT-TE006-CON) and keep "
                   "efs_ledger_outcome with P1."),
    dict(n=3, title="The rule package registry is claimed by P3 and P4 as well as P7",
         source="TSD P3 v3 T2.2 and T3.1; TSD P4 v3 T1, T2, T3.1 against Architecture v5 slide 41 and the "
                "Ownership Map",
         section="T0.2, T2, T3, T5.2",
         description="TSD P3 v3 names rule_test_case as 'owned by P4', and TSD P4 v3 owns rule_package, "
                     "rule_package_version, rule_row and rule_test_case. Architecture v5 slide 41 gives the DMN model "
                     "registry to rwb-decision and the Ownership Map gives all four tables to P7.",
         evidence="Arch v5 slide 41 (P7 owns 'approvals, central decision ledger, DMN model registry'); Ownership "
                  "Map Tables sheet: rule_package, rule_package_version, rule_row and rule_test_case under P7.",
         type="Conflict", area="Rules", severity="P2", needed_by_wave="1",
         legacy_ref="RWB-E1-073, RWB-E2-041", owner_role="Solution architect", asm="ASM-B-TECH-03-4",
         proposed="Build the registry in rwb-decision, keep embedded Drools evaluation in the owning service, and "
                   "read the package and catalogue through the P7 contract (DP-04)."),
    dict(n=4, title="payment_match_rule has no owner in the Ownership Map",
         source="TSD P8 v2 T3.1 against Microservice Ownership Map v1 Tables sheet",
         section="T3, T5.2",
         description="T3.1 of TSD P8 defines payment_match_rule as a NEW table. The Ownership Map has no row for it "
                     "and gives P8 the proceeds table only. The match rules are a decision table, and Template and "
                     "Rules R5.5 DP-04 and ADR-017 put every rule in the registry of rwb-decision.",
         evidence="Ownership Map Tables sheet: proceeds only for P8; TSD P3 v3 T2.2 names PAYMENT_MATCH and "
                  "BOOKING_MATCH as package codes for Epic 2.",
         type="Missing", area="Rules", severity="P3", needed_by_wave="2",
         legacy_ref="RWB-E2-042", owner_role="Solution architect", asm="ASM-B-TECH-03-5",
         proposed="Build the match rules as the PAYMENT_MATCH package in rwb-decision and keep the proceeds rows "
                   "in rwb-payment."),
    dict(n=5, title="S1 owns the valuations but has no table in the Ownership Map",
         source="TSD S1 v2 T3.1 and appendix T-A against the Ownership Map Tables and Endpoints sheets",
         section="T0.2, T3, T5.2.1",
         description="T3.1 of TSD S1 defines the valuation table as a NEW table of S1, and Architecture v5 slide 41 "
                     "says rwb-valuation owns the valuations. The Ownership Map Tables sheet lists no table owned by "
                     "S1 (valuation_ext is P1's), while its Endpoints sheet gives S1 the two valuation paths.",
         evidence="Ownership Map Endpoints ruling POST /assets/{assetKey}/valuations (owner S1, ASM-A6-api-6); "
                  "Tables sheet: no S1 row; Arch v5 slide 41: rwb-valuation owns the valuations.",
         type="Conflict", area="Data", severity="P2", needed_by_wave="3",
         legacy_ref="RWB-S1-001", owner_role="Solution architect", asm="ASM-B-TECH-03-6",
         proposed="Create rwb_valuation with the valuation and route decision tables of T3.1, and keep valuation_ext "
                   "with P1 as the SVAF extension table."),
    dict(n=6, title="Eleven business events have no number in the catalogue and three have no contract",
         source="Architecture v5 slides 42 and 43; per-service AsyncAPI documents of 22 November 2026",
         section="T5.2.1, T5.3",
         description="The numbered catalogue stops at 30, and the plus rows (RouteDecided, AssetSold, "
                     "JudgmentRecorded, AuctionResult, TreatmentClosed, GuaranteeClaimFiled and Settled, "
                     "AccountsTransferred, AccessPolicyChanged, DoaLimitChanged, FileDelivered and FileFailed) carry "
                     "no EV number. ReportPublished (P9), LawsuitFiled (S4), ApprovalDecided (P7) and the two split "
                     "guarantee events (S3) have no AsyncAPI operation.",
         evidence="Arch v5 slide 43 plus rows; asyncapi/rwb-reporting.asyncapi.yaml has no channel; "
                  "asyncapi/rwb-litigation.asyncapi.yaml has no LawsuitFiled; asyncapi/rwb-guarantee.asyncapi.yaml "
                  "has one GuaranteeClaim message.",
         type="Missing", area="Events", severity="P3", needed_by_wave="1",
         legacy_ref="", owner_role="Solution architect", asm="ASM-B-TECH-03-7",
         proposed="Number the plus rows EV-31 onwards and add the missing operations to the four AsyncAPI documents."),
    dict(n=7, title="The Arch v5 contract paths and the published OpenAPI files differ",
         source="Architecture v5 slides 13 to 20 against the per-service OpenAPI files of 22 November 2026",
         section="T5.2.1, T5.2.2, Appendix T-A",
         description="The Arch v5 contract slides name operations that the published per-service files do not carry "
                     "on the same path, for example S1 /cases/{id}/route-proposals against the published "
                     "POST /cases/{caseId}/route, and P3 /cases/{id}/actions, GET /tasks and GET /case-summary/{id} "
                     "against the published /me/tasks and PATCH /tasks/{taskId}.",
         evidence="Arch v5 slide 18 (S1 IN) and slide 14 (P3 IN) against rwb-valuation.yaml and rwb-case.yaml.",
         type="Conflict", area="Contracts", severity="P2", needed_by_wave="1",
         legacy_ref="", owner_role="Solution architect", asm="ASM-B-TECH-03-8",
         proposed="Take the published OpenAPI file as the contract and raise the Arch v5 wording as a correction to "
                   "the architecture pack."),
    dict(n=8, title="Every module specification is still In review and no approval is recorded",
         source="Document control of the 20 module specifications of v5",
         section="Document control",
         description="All 20 source files carry Status In review. D-RCV-60 has no approval round, so the next "
                     "version is issued as Draft with the status recorded. This is not a defect of the "
                     "specification; it is the approval state.",
         evidence="'| Status | In review |' in every file of the v5 family.",
         type="Missing", area="Governance", severity="P3", needed_by_wave="1",
         legacy_ref="", owner_role="Design authority", asm="ASM-B-TECH-03-1",
         proposed="Record the approval of the v6 family at the design authority and move Status to Approved."),
    dict(n=9, title="No squad is named per service",
         source="Document control (Build squad) of the v5 family against Template and Rules R5.3",
         section="Document control, T0.1",
         description="Every file names 'TechX recovery squads' as the build squad. Under 19 services the squad per "
                     "service is not specified, and Template and Rules R5.3 keeps the owner a suggestion only.",
         evidence="'| Build squad | TechX recovery squads |' in every file of the v5 family.",
         type="Ambiguous", area="Delivery", severity="P3", needed_by_wave="1",
         legacy_ref="", owner_role="Delivery lead", asm="ASM-B-TECH-03-9",
         proposed="Assign a squad per service at the design authority; the suggestion stays TechX for app work and "
                   "the ACE team for DB work."),
]

asms = [
    dict(n=1, text="Every module specification of this family is issued as Draft, because no approval of the new "
                   "version is recorded.",
         why="The source status is In review and D-RCV-60 runs without an approval step (AGENTS.md rule 9).",
         read="'Status In review' becomes 'Draft', and the Document control adds a Status note with the gap and this "
              "assumption.", gap="CG-B-TECH-03-8", applied_in="Document control of all 20 files",
         confidence="High", confirm="Design authority", impact="None on content; the approval state is visible."),
    dict(n=2, text="lake_copy_watermark stays with P1 as the watermark of the last published reporting projection; "
                   "the lake extract is not built.",
         why="The data lake is removed (ADR-018; DP-17) while the Ownership Map keeps the table with P1.",
         read="DP-17 in T0.3 of P1 and the T3 note of P1; no interface to a lake appears in T5.1 or T5.2.",
         gap="CG-B-TECH-03-1", applied_in="TSD P1 v4 T0.3, T3", confidence="Medium",
         confirm="Solution architect", impact="P9 reads events; no outbound extract."),
    dict(n=3, text="The platform tables of TSD P2 T3.1 are built once in the shared libraries, and "
                   "efs_ledger_outcome stays with P1.",
         why="The Ownership Map Tables sheet has no per-service row for an outbox, an inbox, an idempotency key or a "
             "feature flag, and it places efs_ledger_outcome with P1.",
         read="T3 note of P2; T0.2 lists the three P2 business tables.", gap="CG-B-TECH-03-2",
         applied_in="TSD P2 v4 T0.2, T3", confidence="High", confirm="Solution architect",
         impact="Platform stories own the library tables; P2 owns the outbound behaviour."),
    dict(n=4, text="The rule package registry is P7's, and P3 and P4 read it through the P7 contract.",
         why="Architecture v5 slide 41 gives the DMN model registry to rwb-decision and the Ownership Map gives the "
             "four tables to P7, while two module specifications still claim them.",
         read="T3 note of P3 and P4; T2 note of P3 and P4; T5.2.2 lists the P7 contract.",
         gap="CG-B-TECH-03-3", applied_in="TSD P3 v4 and TSD P4 v4, T0.2, T2, T3, T5.2", confidence="High",
         confirm="Solution architect", impact="Embedded Drools evaluation stays in the owning service (DP-04)."),
    dict(n=5, text="payment_match_rule becomes the PAYMENT_MATCH rule package of rwb-decision; P8 keeps the "
                   "proceeds rows.",
         why="The Ownership Map has no row for the table and ADR-017 puts every rule in the registry.",
         read="T3 note of P8.", gap="CG-B-TECH-03-4", applied_in="TSD P8 v3 T3", confidence="Medium",
         confirm="Solution architect", impact="P8 holds no rule table; the package is promoted by RW-COE."),
    dict(n=6, text="S1 owns the valuations and the route decision in rwb_valuation, and valuation_ext stays with P1.",
         why="The Ownership Map Endpoints sheet gives S1 the valuation paths and Architecture v5 gives it the "
             "valuations, while the Tables sheet has no S1 row.",
         read="T3 note of S1; T5.2.1 lists both operations.", gap="CG-B-TECH-03-5",
         applied_in="TSD S1 v3 T0.2, T3, T5.2.1", confidence="Medium", confirm="Solution architect",
         impact="A valuation table is created in rwb_valuation; P1 keeps the SVAF extension table."),
    dict(n=7, text="An event with no catalogue number is named in T5.3 and cited in this assumption; the missing "
                   "number and the missing AsyncAPI operation are not invented.",
         why="The Arch v5 catalogue numbers 30 rows and leaves eleven as plus rows, and four events have no AsyncAPI "
             "operation.",
         read="T5.3 footnote of the affected files; T5.2.1 of P9.", gap="CG-B-TECH-03-6",
         applied_in="T5.2.1 and T5.3 of the affected files", confidence="High", confirm="Solution architect",
         impact="Consumers can build against the named message; numbering follows in the next catalogue version."),
    dict(n=8, text="Where the Arch v5 contract slides and the published OpenAPI files differ, the published file is "
                   "the contract cited in T5.2.",
         why="The consumer's fake is generated from the published artefact (ADR-020), and the difference is recorded "
             "as a gap rather than resolved by invention.",
         read="T5.2 intro and the appendix T-A note of every file.", gap="CG-B-TECH-03-7",
         applied_in="T5.2 and Appendix T-A of all 20 files", confidence="Medium", confirm="Solution architect",
         impact="The build follows the published files; the architecture pack needs a correction."),
    dict(n=9, text="The Build squad row keeps the version 5 wording until the design authority assigns a squad per "
                   "service.",
         why="No source names a squad per service and Template and Rules R5.3 keeps the owner a suggestion.",
         read="Document control Build squad row, with the gap and this assumption cited in the row.",
         gap="CG-B-TECH-03-9", applied_in="Document control of all 20 files", confidence="High",
         confirm="Delivery lead", impact="None on content."),
]

def rows(items, kind):
    out = []
    for g in items:
        r = dict(g)
        r.pop("n")
        r["id"] = f"{'CG' if kind == 'gap' else 'ASM'}-{WP}-{g['n']}"
        r["wp"] = WP
        if kind == "gap":
            order = ["id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
                     "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]
        else:
            order = ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]
        out.append({k: r.get(k, "") for k in order})
    return out

gp = rows(gaps, "gap")
asm = rows(asms, "asm")
(WORK / "gaps").mkdir(parents=True, exist_ok=True)
(WORK / "assumptions").mkdir(parents=True, exist_ok=True)
(WORK / "gaps" / f"{WP}.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in gp) + "\n",
                                           encoding="utf-8")
(WORK / "assumptions" / f"{WP}.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in asm) + "\n",
                                                   encoding="utf-8")
print(len(gp), len(asm))
