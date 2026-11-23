from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
start = t.index("# ---------------------------------------------------------------- REST pairs")
end = t.index("def md_table(head, rows):")
new = '''# ---------------------------------------------------------------- pairs (provider, consumer)
REST_PAIRS = [
    ("P3", "BFF", "GET /cases/{id}; GET /cases?queue=; POST /cases/{id}/actions; GET /tasks; POST /tasks/{id}/complete; GET /case-summary/{id}", "slide 14, slide 20"),
    ("P1", "BFF", "GET /customers/{id}; GET /accounts/{id}; GET /freshness (composite case screen, one hop each in parallel)", "slide 15, slide 20"),
    ("ACE-CMN", "BFF", "Sign-in through ACE Common; session to short-lived user JWT", "slide 20"),
    ("P4", "P3", "POST /authorise (role, scope, DoA), cached in rwb-case", "slide 13, slide 14"),
    ("P4", "P7", "GET /doa-limits (DoA limits)", "slide 13, slide 14"),
    ("ACE-CMN", "P4", "Sign-in, group-to-role (Entra ID)", "slide 13, slide 14"),
    ("P1", "S1", "Collateral and appraisals (GET /collateral/{id})", "slide 13, slide 18"),
    ("P1", "S8", "Party flags", "slide 13, slide 15"),
    ("P1", "S7", "GL outcome", "slide 13, slide 20"),
    ("P1", "P10", "Tool: read case facts (read-only tool-gateway call)", "slide 13, slide 16"),
    ("P5", "P10", "Tool: read extracted fields (read-only tool-gateway call)", "slide 13, slide 16"),
    ("P5", "S9", "Partner uploads (SAS link)", "slide 13, slide 17"),
    ("P5", "P2", "Fetch file by ID (SAS link)", "slide 13, slide 16"),
    ("EXT", "S9", "Partners (law firms, agencies, buyers) through the partner gateway, FAPI 2.0, MFA", "slide 13, slide 17"),
    ("EXT", "P10", "Enterprise AI private endpoint (INT-23), HTTPS", "slide 13, slide 16"),
    ("ACE-CMN", "P6", "Notification path (SMS, LINE OA)", "slide 13, slide 17"),
]
FILE_PAIRS = [
    ("P7", "EXT", "Immutable storage: daily ledger seal (WORM)", "slide 13, slide 14"),
    ("P5", "EXT", "Azure Blob (WORM): files, 2.8 TB by 2031", "slide 13, slide 16"),
    ("P2", "EXT", "WIN registered mail, daily outbound file (INT-14); debt buyers, per lot, encrypted (INT-25)", "slide 13, slide 16"),
]
SQL_PAIRS = [
    ("ACE-DB", "P1", "SELECT on the 30 recovery.v_ace_* views, read only (ADR-010)", "slide 13, slide 15"),
]
NEXUS_PAIRS = [
    ("ACE-CMN", "S2", "restructure.calculate (Nexus operation, namespace ace-collection)", "slide 13, slide 18"),
]
TMP_PAIRS = [
    ("P1", "P3", "Activity: listEligibleAccounts(businessDate)", "slide 14"),
    ("S1", "P3", "Child workflow: RouteDecisionWorkflow", "slide 14, slide 18"),
    ("S2", "P3", "Child workflow: the treatment stage workflows (TreatmentWorkflow)", "slide 14, slide 18"),
    ("S3", "P3", "Child workflow: GuaranteeClaimWorkflow", "slide 14, slide 18"),
    ("S4", "P3", "Child workflow: LitigationWorkflow", "slide 14, slide 19"),
    ("S5", "P3", "Child workflow: AssetDisposalWorkflow", "slide 14, slide 19"),
    ("S6", "P3", "Child workflow: DebtSaleWorkflow", "slide 14, slide 19"),
    ("S7", "P3", "Child workflow: WriteOffWorkflow", "slide 14, slide 20"),
    ("S8", "P3", "Child workflow: DeviationWorkflow", "slide 14, slide 15"),
    ("P7", "S1", "Child workflow: ApprovalWorkflow (kit template)", "slide 13, slide 18"),
    ("P10", "S1", "Child workflow: route agent run", "slide 13, slide 18"),
    ("P7", "S2", "Child workflow: ApprovalWorkflow (DoA)", "slide 13, slide 18"),
    ("P5", "S2", "Contract document generation and e-sign", "slide 13, slide 18"),
    ("P8", "S2", "Activity: postProceeds (saga step)", "slide 13, slide 18"),
    ("P6", "S3", "Child workflow: guarantor notice", "slide 13, slide 18"),
    ("P7", "S3", "Child workflow: ApprovalWorkflow", "slide 13, slide 18"),
    ("S9", "S4", "Activity: issueInstruction (law firm)", "slide 13, slide 19"),
    ("P6", "S4", "Child workflow: demand notice", "slide 13, slide 19"),
    ("P7", "S4", "Child workflow: ApprovalWorkflow", "slide 13, slide 19"),
    ("S9", "S5", "Activity: issueInstruction (auction vendor)", "slide 13, slide 19"),
    ("P7", "S5", "Child workflow: ApprovalWorkflow", "slide 13, slide 19"),
    ("P8", "S5", "Activity: postProceeds", "slide 13, slide 19"),
    ("P6", "S5", "Not specified in the source documents (CG-B-ARCH-CON-8; ASM-B-ARCH-CON-8)", "slide 13"),
    ("P5", "S6", "Document: data room pack", "slide 13, slide 19"),
    ("P7", "S6", "Child workflow: ApprovalWorkflow", "slide 13, slide 19"),
    ("P2", "S6", "Activity: deliverFile (buyer file)", "slide 13, slide 19"),
    ("P8", "S6", "Activity: postProceeds", "slide 13, slide 19"),
    ("P7", "S7", "Child workflow: committee approval", "slide 13, slide 20"),
    ("P8", "S7", "Activity: postProceeds", "slide 13, slide 20"),
    ("P10", "S8", "Child workflow: screening agent run", "slide 13, slide 15"),
    ("P10", "P5", "Child workflow: classify / extract run", "slide 13, slide 16"),
    ("P5", "P6", "Document: generate letter", "slide 13, slide 17"),
    ("P7", "P6", "Child workflow: approval", "slide 13, slide 17"),
    ("P2", "P6", "Activity: deliverFile (WIN letters)", "slide 13, slide 17"),
    ("P1", "P8", "Activity: payments for business date", "slide 13, slide 17"),
    ("P2", "P8", "Activity: deliverFile (posting file)", "slide 13, slide 17"),
    ("P1", "P9", "Activity: snapshot(page) for measures", "slide 13, slide 15"),
    ("P2", "P9", "Activity: deliverFile (regulatory extract)", "slide 13, slide 15"),
]

PAIRS = []
for p_, c, i, s in REST_PAIRS:
    PAIRS.append([p_, c, "REST", i, s])
for p_, c, i, s in TMP_PAIRS:
    PAIRS.append([p_, c, "Temporal", i, s])
for p_, c, i, s in NEXUS_PAIRS:
    PAIRS.append([p_, c, "Nexus", i, s])
for p_, c, i, s in FILE_PAIRS:
    PAIRS.append([p_, c, "File", i, s])
for p_, c, i, s in SQL_PAIRS:
    PAIRS.append([p_, c, "SQL view", i, s])
for eid, name, prod, cons in EVENTS:
    for c in cons:
        if c == "NONE":
            continue
        PAIRS.append([prod, c, "Kafka", name, f"slide 42, slide 43 ({eid})"])
for name, prod, cons in EXTRA_EVENTS:
    for c in cons:
        PAIRS.append([prod, c, "Kafka", name, "slide 43 (event catalogue, not numbered)"])
PAIRS.append(["ALL", "ACE-CMN", "Kafka", "Audit and PII logs", "slide 13 note"])

EDGE = ("BFF", "ACE-CMN", "ACE-DB", "EXT", "PARTNER", "REQUESTER", "NOTSPEC")


def pair_class(p_, c):
    if p_ in EDGE or c in EDGE:
        return "X"
    if p_ == c:
        return "H"
    return "C"


def wave_of(code):
    return 0 if code in EDGE + ("ALL", "PLT") else SVC[code]["wave"]


def itg(p_, c):
    w = max(wave_of(p_), wave_of(c), 1)
    return f"RWB-ITG-W{w} harness"


def artefact(p_, ctype, interface=""):
    if ctype == "REST":
        if p_ in SVC:
            return f"OpenAPI 3.1, {SVC[p_]['base']}"
        return {"ACE-CMN": "ACE Common API (sign-in, notification path)",
                "EXT": "The external API or interface of that party"}.get(p_, "OpenAPI 3.1")
    if ctype == "Kafka":
        if "Audit" in interface:
            return "AsyncAPI 3.0, ACE Common logging topics"
        t = TOPIC.get(p_, "-")
        return f"AsyncAPI 3.0, {t}" if t and t != "-" else "AsyncAPI 3.0"
    if ctype == "Temporal":
        return f"Activity contract jar on task queue {SVC[p_]['queue']}" if p_ in SVC else "Contract jar"
    if ctype == "Nexus":
        return "Nexus operation, ace-collection"
    if ctype == "File":
        return "File manifest (fileId, batchId, sha256, record count)"
    if ctype == "SQL view":
        return "View contract, SELECT only"
    return ""


'''
p.write_text(t[:start] + new + t[end:], encoding="utf-8")
print("patched pairs")
