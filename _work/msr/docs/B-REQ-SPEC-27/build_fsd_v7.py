"""B-REQ-SPEC-27: build Recovery Workbench Functional Specifications by Module v7.

Reads the v6 folder (read only) and writes the next file version of each module into the v7 folder.
Each output keeps every section, ID, number and date of its source and adds:
  - the two header lines of Template and Rules R8.1,
  - one Service row and one Change row in the document control table,
  - one "Note, Architecture v5 (D-RCV-60)" block before "Existing capability check".
"""
import os
import re
import sys

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, r"03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v6")
DST = os.path.join(ROOT, r"03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v7")

HEADER = ("SCB Collections and Recovery. Henka Group, 22 November 2026.\n"
          "(C) Siam Commercial Bank and Henka Pte Ltd\n")

# code: service, service display name, wave, schema, REST base, topic, queue, java package tail, owns (Arch v5 slide 41)
SVC = {
    "P1": ("rwb-source-data", "Source data", 1, "rwb_source_data", "/api/recovery/source-data/v1",
           "rwb.source-data.events.v1", "rwb-source-data", "sourcedata",
           "ACE view contract, extension tables, freshness, reconciliation"),
    "P2": ("rwb-integration", "Integration", 1, "rwb_integration", "/api/recovery/integration/v1",
           "rwb.integration.events.v1", "rwb-integration", "integration",
           "interface config, file runs, outbound items, ACE integration paths"),
    "P3": ("rwb-case", "Case and workflow", 1, "rwb_case", "/api/recovery/case/v1",
           "rwb.case.events.v1", "rwb-case", "case",
           "case, CMMN state, queues, tasks, allocation, timers"),
    "P4": ("rwb-access", "Access and authority", 1, "rwb_access", "/api/recovery/access/v1",
           "rwb.access.events.v1", "rwb-access", "access",
           "Recovery roles as data, scope, masking policy, DoA table, access log"),
    "P5": ("rwb-document", "Document", 1, "rwb_document", "/api/recovery/document/v1",
           "rwb.document.events.v1", "rwb-document", "document",
           "metadata, custody, OCR text and fields, signatures, retention"),
    "P6": ("rwb-comms", "Communications", 1, "rwb_comms", "/api/recovery/comms/v1",
           "rwb.comms.events.v1", "rwb-comms", "comms",
           "notices, templates, merge fields, proof of delivery"),
    "P7": ("rwb-decision", "Decision and rules", 1, "rwb_decision", "/api/recovery/decision/v1",
           "rwb.decision.events.v1", "rwb-decision", "decision",
           "approvals, central decision ledger, DMN model registry"),
    "P8": ("rwb-payment", "Payment", 2, "rwb_payment", "/api/recovery/payment/v1",
           "rwb.payment.events.v1", "rwb-payment", "payment",
           "payment and proceeds matching, fees, bookings, posting files"),
    "P9": ("rwb-reporting", "Reporting", 1, "rwb_reporting", "/api/recovery/reporting/v1",
           "rwb.reporting.events.v1", "rwb-reporting", "reporting",
           "measures, snapshots, steering dashboard, regulatory reports"),
    "P10": ("rwb-agent", "Agent", 1, "rwb_agent", "/api/recovery/agent/v1",
            "rwb.agent.events.v1", "rwb-agent", "agent",
            "agent policies, prompts, runs, guardrails, evaluations"),
    "S1": ("rwb-valuation", "Valuation and route", 3, "rwb_valuation", "/api/recovery/valuation/v1",
           "rwb.valuation.events.v1", "rwb-valuation", "valuation",
           "valuations, D6 route decision, route agent output"),
    "S2": ("rwb-treatment", "Treatment and offer", 2, "rwb_treatment", "/api/recovery/treatment/v1",
           "rwb.treatment.events.v1", "rwb-treatment", "treatment",
           "treatments, contracts, settlement and deed-in-lieu agreements, plan timers"),
    "S3": ("rwb-guarantee", "Guarantee", 3, "rwb_guarantee", "/api/recovery/guarantee/v1",
           "rwb.guarantee.events.v1", "rwb-guarantee", "guarantee",
           "TCG and insurance claims, guarantor notices and pursuit"),
    "S4": ("rwb-litigation", "Litigation", 3, "rwb_litigation", "/api/recovery/litigation/v1",
           "rwb.litigation.events.v1", "rwb-litigation", "litigation",
           "legal actions, hearings, judgments, enforcement, LED auction ladder"),
    "S5": ("rwb-asset", "Asset", 2, "rwb_asset", "/api/recovery/asset/v1",
           "rwb.asset.events.v1", "rwb-asset", "asset",
           "assets taken on, holding, floor price, listings, auction rounds"),
    "S6": ("rwb-debtsale", "Debt sale", 3, "rwb_debtsale", "/api/recovery/debtsale/v1",
           "rwb.debtsale.events.v1", "rwb-debtsale", "debtsale",
           "lots, data room, buyer terms, bids, award, transfer"),
    "S7": ("rwb-writeoff", "Write-off", 4, "rwb_writeoff", "/api/recovery/writeoff/v1",
           "rwb.writeoff.events.v1", "rwb-writeoff", "writeoff",
           "eligibility, committee, posting, recovery after charge-off"),
    "S8": ("rwb-deviation", "Deviation", 2, "rwb_deviation", "/api/recovery/deviation/v1",
           "rwb.deviation.events.v1", "rwb-deviation", "deviation",
           "X1-X7 screening, pause, handling, return"),
    "S9": ("rwb-partner", "Partner", 4, "rwb_partner", "/api/recovery/partner/v1",
           "rwb.partner.events.v1", "rwb-partner", "partner",
           "panel, partner users, instructions, results, fees, scorecards"),
}

# modules whose version 3 or 4 text still names the data lake / Quartz (evidence recorded in the gap rows)
LAKE = {"P1", "P2", "P4", "P6", "P7", "P9", "P10"}
QUARTZ = {"P3", "P7", "S1", "S4", "S8"}


def note(code, nv, pv):
    svc, disp, wave, schema, base, topic, queue, pkg, owns = SVC[code]
    rows = [
        "| Item | Value |",
        "|---|---|",
        f"| Service | `{svc}` ({disp}) |",
        f"| Owns in Architecture v5 | {owns} |",
        f"| Service epic | `RWB-SVC-{code}` |",
        f"| Wave | {wave} |",
        f"| Schema | `{schema}` |",
        f"| REST base | `{base}` |",
        f"| Kafka topic | `{topic}`, with `.retry` and `.dlt` topics |",
        f"| Event names | `rwb.{svc.split('-', 1)[1]}.<Event>.v1` |",
        f"| Temporal task queue | `{queue}` |",
        f"| Java package | `th.co.scb.ace.workbench.recovery.{pkg}` |",
    ]
    body = [
        f"Version {nv} adds the Service row, the Change row and this note above; nothing else in this document changes. "
        f"Under Architecture v5 the module is delivered "
        f"as the service `{svc}` of the 19 services inside ACE (ADR-013), with its own schema `{schema}` and login "
        f"(ADR-014), in wave {wave}, service epic `RWB-SVC-{code}`; the realignment is D-RCV-60 (DL44), and DL46 keeps "
        f"team-type ownership soft. The functional content of this document is the content of version {pv}, kept word "
        f"for word: every feature, requirement, rule, field, list, message, screen, count and date.",
        "Every owner named in this document is the owner recorded in the Microservice Ownership Map v1, and where the "
        "map carries a ruling of Template and Rules §R3 the ruling is followed: parameters and reference data with "
        "`rwb-case` (DP-06, DP-07), the rule package registry with `rwb-decision` (DP-04), the interaction ledger with "
        "`rwb-source-data` (DP-18) and feature flags with the platform library. Where this document names a table, "
        "endpoint, event, job, workflow or screen that the map gives to another service, that service owns it and this "
        "module reaches it only through the owner's contract (DP-01, DP-11; ADR-020).",
    ]
    if code in LAKE:
        body.append(
            "The extracts, feeds and copies this document addresses to a data lake are removed by Architecture v5: "
            "reporting reads events into `rwb-reporting` (DP-17, ADR-018). The wording of those extracts is kept as "
            "written and carried by CG-B-REQ-SPEC-27-2.")
    if code in QUARTZ:
        body.append(
            "The scheduler references of this document are replaced by Temporal Schedules and event-started workflows "
            "through the workflow kit, with the task queue above (DP-10, ADR-016). The wording is kept as written and "
            "carried by CG-B-REQ-SPEC-27-3.")
    body.append(
        f"Release dates stay as written and are tentative (DL48). No approval of version {nv} is recorded "
        "(ASM-B-REQ-SPEC-27-1); the version is Draft.")
    return ("### Note, Architecture v5 (D-RCV-60)\n\n" + "\n".join(rows) + "\n\n" + "\n\n".join(body) + "\n")


def build(path):
    name = os.path.basename(path)
    m = re.search(r"FSD (P\d+|S\d+) .* v(\d+)\.md$", name)
    code, ver = m.group(1), int(m.group(2))
    nv, pv = ver + 1, ver
    lines = open(path, encoding="utf-8").read().splitlines()
    out = [HEADER.rstrip("\n"), ""] + lines

    # locate the document control attribute table
    start = out.index("| Attribute | Value |")
    end = start + 1
    while end < len(out) and out[end].startswith("|"):
        end += 1
    block = out[start:end]
    newblock, service_row = [], f"| Service | `{SVC[code][0]}` ({SVC[code][1]}) |"
    change_row = f"| Change | {nv}, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |"
    for row in block:
        cell = row.split("|")[1].strip() if row.startswith("|") else ""
        if cell == "Document ID":
            row = re.sub(r"-v\d+", f"-v{nv}", row)
        elif cell == "Version":
            row = f"| Version | {nv} |"
        elif cell == "Status":
            row = "| Status | Draft |"
        newblock.append(row)
        if cell == "Document ID":
            newblock.append(service_row)
    newblock.append(change_row)
    out[start:end] = newblock

    # note goes immediately before "Existing capability check"
    anchor = out.index("## Existing capability check")
    out[anchor:anchor] = note(code, nv, pv).split("\n")

    dst = os.path.join(DST, f"Recovery Workbench FSD {code} "
                             f"{name[len(f'Recovery Workbench FSD {code} '):].rsplit(' v', 1)[0]} v{nv}.md")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("WROTE", os.path.basename(dst), f"(source v{ver})")


def main():
    for p in sorted(os.listdir(SRC)):
        if p.endswith(".md"):
            build(os.path.join(SRC, p))


if __name__ == "__main__":
    main()
