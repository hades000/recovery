"""Generate the API Specification v5 folder: 19 service documents, gateway-bff, index, asyncapi.

Read only: API Specification v4 yaml, Ownership Map xlsx, ownership_part_api.json,
Arch v5 extract, Event and Messaging Design v4 extract.
Writes: 05 Technical architecture/Recovery Workbench API Specification v5/...
"""
import json, re, textwrap
from pathlib import Path
import openpyxl, yaml

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v4.yaml"
OUT = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v5"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
HEADER = ["SCB Collections and Recovery. Henka Group, 22 November 2026.",
          "(C) Siam Commercial Bank and Henka Pte Ltd"]
CHANGE = f"{DEC} microservice realignment"
ROW = f"5.0.0, 22 November 2026, {CHANGE}, {TOOL}"

text = SRC.read_text(encoding="utf-8")
lines = text.split("\n")
doc = yaml.safe_load(text)

# ---------------------------------------------------------------- inline YAML anchors
# v4 uses four aliases (*id001, *id002); the documents are split, so every alias is
# expanded in place to keep each file valid on its own. Data is identical.
ANCHOR = {}
for i, ln in enumerate(lines):
    m = re.match(r"^(\s*)([^#]+?: )&(\w+)\s*$", ln)
    if not m:
        continue
    key_indent = len(m.group(1))
    body = []
    j = i + 1
    node_indent = None
    while j < len(lines):
        l = lines[j]
        if not l.strip():
            body.append(l)
            j += 1
            continue
        if len(l) - len(l.lstrip(" ")) <= key_indent:
            break
        if node_indent is None:
            node_indent = len(l) - len(l.lstrip(" "))
        body.append(l)
        j += 1
    while body and not body[-1].strip():
        body.pop()
    ANCHOR[m.group(3)] = (node_indent, body)

expanded = []
for ln in lines:
    m = re.match(r"^(\s*)([^#]*?: )\*(\w+)\s*$", ln)
    if m and m.group(3) in ANCHOR:
        indent_s, key, name = m.group(1), m.group(2), m.group(3)
        node_indent, body = ANCHOR[name]
        shift = len(indent_s) + 2 - node_indent
        expanded.append(f"{indent_s}{key.rstrip()}")
        for b in body:
            expanded.append((" " * shift + b) if shift >= 0 else b[-shift:])
    else:
        expanded.append(ln)
lines = expanded


own = json.loads((ROOT / "_work/msr/plan/ownership_part_api.json").read_text(encoding="utf-8"))
OWNER = {e["id"]: e["owner"] for e in own["api"]}
OWNER_ASM = {e["id"]: e.get("asm") for e in own["api"]}

wb = openpyxl.load_workbook(ROOT / "22 Microservice Realignment" / "Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
ws = wb["Services"]
SERVICES = []
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[0]:
        SERVICES.append({"code": r[0], "service": r[1], "name": r[2], "wave": r[3], "schema": r[4],
                         "base": r[5], "topic": r[6], "queue": r[7]})
BY_CODE = {s["code"]: s for s in SERVICES}

METHODS = ("get", "post", "put", "patch", "delete", "head", "options", "trace")

# ---------------------------------------------------------------- source slicing
pi = lines.index("paths:")
ci = lines.index("components:")


def indent(line):
    return len(line) - len(line.lstrip(" "))


def path_starts():
    return [i for i in range(pi + 1, ci) if lines[i].strip() and indent(lines[i]) == 2]


starts = path_starts() + [ci]
PATH_BLOCK = {}
OP_BLOCK = {}
for a, b in zip(starts, starts[1:]):
    key = lines[a].strip().rstrip(":")
    block = lines[a:b]
    # trailing blank lines belong to the block; trim them
    while block and not block[-1].strip():
        block.pop()
    PATH_BLOCK[key] = block
    op_starts = [j for j in range(len(block)) if indent(block[j]) == 4 and block[j].strip().endswith(":")]
    op_starts.append(len(block))
    for x, y in zip(op_starts, op_starts[1:]):
        method = block[x].strip().rstrip(":")
        if method in METHODS:
            OP_BLOCK[(method.upper(), key)] = block[x:y]

# components
sec_starts = [i for i in range(ci + 1, len(lines)) if lines[i].strip() and indent(lines[i]) == 2]
sec_starts.append(len(lines))
COMP = {}
order = {}
for a, b in zip(sec_starts, sec_starts[1:]):
    name = lines[a].strip().rstrip(":")
    body = lines[a + 1:b]
    ent = [j for j in range(len(body)) if body[j].strip() and indent(body[j]) == 4]
    ent.append(len(body))
    d = {}
    idx = 0
    for x, y in zip(ent, ent[1:]):
        key = body[x].strip().rstrip(":")
        chunk = body[x:y]
        while chunk and not chunk[-1].strip():
            chunk.pop()
        d[key] = chunk
        idx += 1
    COMP[name] = d

OPS = []
for (m, p), blk in OP_BLOCK.items():
    OPS.append({"m": m, "p": p, "id": f"{m} {p}", "block": blk,
                "x-module": OWNER and re.search(r"(?m)^      x-module: *(\S+)", "\n".join(blk)).group(1)})

assert len(OPS) == 141, len(OPS)
for o in OPS:
    o["owner"] = OWNER[o["id"]]


def refs_of(block_text):
    return set(re.findall(r"\$ref: *'#/components/([A-Za-z]+)/([^']+)'", block_text))


def closure(blocks):
    seen = set()
    frontier = set()
    for b in blocks:
        frontier |= refs_of("\n".join(b))
    while frontier:
        nxt = set()
        for sec, name in frontier:
            if (sec, name) in seen:
                continue
            seen.add((sec, name))
            nxt |= refs_of("\n".join(COMP[sec][name]))
        frontier = nxt
    return seen


# ---------------------------------------------------------------- ownership notes
ASM_FOR_OWNER = {"P1": "ASM-A6-api-1", "PLT": "ASM-A6-api-2", "P7": "ASM-A6-api-3", "P3": "ASM-A6-api-4",
                 "S1": "ASM-A6-api-6"}


def asm_of(o):
    return OWNER_ASM.get(o["id"]) or ASM_FOR_OWNER[o["owner"]]


def owner_note(o):
    return (f"API Specification v4 x-module {o['x-module']}; owner {o['owner']} per Microservice Ownership Map v1 "
            f"(sheet Endpoints) and {asm_of(o)}")


def annotate(block, o):
    out = []
    for ln in block:
        out.append(ln)
        if ln.startswith("      x-module:"):
            out.append("      x-owner: " + json.dumps(o["owner"]))
            if o["owner"] != o["x-module"]:
                out.append("      x-owner-note: " + json.dumps(owner_note(o)))
    return out


# ---------------------------------------------------------------- file plan
FILES = {}          # code -> [ops]
for o in OPS:
    FILES.setdefault(o["owner"], []).append(o)

PLT = FILES.pop("PLT")

ORPHANS = {"DocumentVersion": "P5", "FieldCaptureItem": "P5", "FieldCaptureManifest": "P5",
           "Listing": "S5", "PlacementResult": "P3", "QueueOwnerLoad": "P3", "WriteOff": "S7"}

# ---------------------------------------------------------------- render helpers
WIDTH = 112


def folded(key, value, indent="  "):
    out = [f"{indent}{key}: >-"]
    pad = indent + "  "
    for para in value.split("\n"):
        if not para.strip():
            out.append("")
            continue
        out.extend(pad + w for w in textwrap.wrap(para, width=WIDTH - len(pad), break_long_words=False,
                                                  break_on_hyphens=False))
    return out


def doc_head(title):
    return ([f"# {HEADER[0]}", f"# {HEADER[1]}", "# Change log", f"# {ROW}", "",
             "openapi: 3.1.0", "info:", f"  title: {json.dumps(title)}", "  version: 5.0.0"])


def int_or_str(v):
    return v


def xservice_block(s, ops, asyncapi):
    return ["x-service:",
            f"  code: {json.dumps(s['code'])}",
            f"  service: {json.dumps(s['service'])}",
            f"  name: {json.dumps(s['name'])}",
            f"  wave: {s['wave']}",
            f"  schema: {json.dumps(s['schema'])}",
            f"  rest-base: {json.dumps(s['base'])}",
            f"  topic: {json.dumps(s['topic'])}",
            f"  task-queue: {json.dumps(s['queue'])}",
            "  namespace: \"rwb-recovery\"",
            f"  asyncapi: {json.dumps(asyncapi)}",
            f"  operations: {len(ops)}"]


def file_service(owner):
    return "gateway-bff (PLT platform surface)" if owner == "PLT" else BY_CODE[owner]["service"]


def write_doc(path, head_lines, body_lines):
    text_out = "\n".join(head_lines + body_lines) + "\n"
    path.write_text(text_out, encoding="utf-8")
    return path


# ---------------------------------------------------------------- service documents
OUT.mkdir(parents=True, exist_ok=True)
written = []
SUMMARY = []

for s in SERVICES:
    code, short = s["code"], s["service"]
    ops = sorted(FILES.get(code, []), key=lambda o: (list(PATH_BLOCK).index(o["p"]), METHODS.index(o["m"].lower())))
    # path order follows the source document
    paths_order = [p for p in PATH_BLOCK]
    ops = sorted(ops, key=lambda o: (paths_order.index(o["p"]), METHODS.index(o["m"].lower())))
    moved_in = [o for o in ops if o["owner"] != o["x-module"]]
    moved_out = [o for o in OPS if o["x-module"] == code and o["owner"] != code]
    asyncapi = f"asyncapi/{short}.asyncapi.yaml"

    desc = [f"Operations of the Recovery Workbench API that belong to {short} ({s['name']}, module {code}, "
            f"service wave {s['wave']}) under Microservice Ownership Map v1, split from Recovery Workbench API "
            f"Specification v4 (4.0.0, 16 November 2026) by the {DEC} microservice realignment.",
            f"This document holds {len(ops)} operations under REST base {s['base']}; schema {s['schema']}; "
            f"topic {s['topic']}; Temporal task queue {s['queue']} in namespace rwb-recovery. The v4 text of every "
            f"operation, parameter, schema, response, number and date is kept unchanged.",
            "Moved into this document from another module of v4: " +
            ("; ".join(f"{o['id']} (x-module {o['x-module']}, owner {o['owner']})" for o in moved_in) if moved_in else "none") + ".",
            "Moved out of this document to another service: " +
            ("; ".join(f"{o['id']} (now {file_service(o['owner'])}, owner {o['owner']})" for o in moved_out) if moved_out else "none") + ".",
            "The v4 document description, the tag list and the document map are kept in index.yaml; the event "
            f"contract of the service is in {asyncapi}."]

    head = doc_head(f"Recovery Workbench API - {short} ({s['name']})")
    body = folded("description", "\n".join(desc))
    body += ["servers:", f"- url: {json.dumps(s['base'])}",
             f"  description: {json.dumps('Relative to the ' + short + ' service in each environment')}",
             "security:", "- entraId: []"]
    tags = []
    for o in ops:
        for t in re.findall(r"(?m)^      tags:\n      - (.+)$", "\n".join(o["block"])):
            if t not in tags:
                tags.append(t)
    src_tag_order = [t for t in doc["tags"]]
    tags = [t["name"] for t in src_tag_order if t["name"] in tags]
    if tags:
        body.append("tags:")
        body += [f"- name: {json.dumps(t)}" for t in tags]
    body += xservice_block(s, ops, asyncapi)

    # paths
    body.append("paths:")
    by_path = {}
    for o in ops:
        by_path.setdefault(o["p"], []).append(o)
    for p in [x for x in PATH_BLOCK if x in by_path]:
        body.append(f"  {p}:")
        for o in sorted(by_path[p], key=lambda o: METHODS.index(o["m"].lower())):
            body += annotate(o["block"], o)

    # components
    need = closure([o["block"] for o in ops])
    for name, owner in ORPHANS.items():
        if owner == code:
            need.add(("schemas", name))
    body.append("components:")
    body.append("  securitySchemes:")
    body += COMP["securitySchemes"]["entraId"]
    if any(sec == "responses" for sec, _ in need):
        body.append("  responses:")
        for name in COMP["responses"]:
            if ("responses", name) in need:
                body += COMP["responses"][name]
    if any(sec == "schemas" for sec, _ in need):
        body.append("  schemas:")
        for name in COMP["schemas"]:
            if ("schemas", name) in need:
                body += COMP["schemas"][name]

    p = write_doc(OUT / f"{short}.yaml", head, body)
    written.append(p)
    SUMMARY.append({"code": code, "service": short, "name": s["name"], "wave": s["wave"],
                    "schema": s["schema"], "base": s["base"], "topic": s["topic"], "queue": s["queue"],
                    "file": f"{short}.yaml", "asyncapi": asyncapi, "operations": len(ops),
                    "tags": tags})

# ---------------------------------------------------------------- gateway-bff
gw_ops = sorted(PLT, key=lambda o: (list(PATH_BLOCK).index(o["p"]), METHODS.index(o["m"].lower())))
gw_desc = [
    "Edge document of the Recovery Workbench API. The {0} realignment puts every operation in the document of the "
    "service that owns it; this document holds the operations whose owner in Microservice Ownership Map v1 is PLT, "
    "because PLT is the platform library and is not one of the 19 services: the four feature-flag operations "
    "(ASM-A6-api-2) and the platform workflow smoke check (ASM-A6-api-5). No service document repeats them.".format(DEC),
    "The edge rules of DP-19 apply to every document of the set: the browser calls the shared App Gateway, which "
    "routes /recovery/* and /api/recovery/* to the Recovery gateway-bff (Arch v5 slide 34); the BFF checks the "
    "session in Redis, gets a short-lived JWT through ACE Common sign-in, checks the coarse permission and makes one "
    "REST hop to the owning service, 2 s budget (Arch v5 slides 30 and 35). The composite screen routes of the BFF "
    "are not specified in the source documents (CG-B-ARCH-API-1; ASM-B-ARCH-API-2) and are not added here.",
    "The base path of the platform operations under the BFF is not specified in the source documents "
    "(CG-B-ARCH-API-2; ASM-B-ARCH-API-1); the operations keep their v4 paths unchanged."]
head = doc_head("Recovery Workbench API - gateway-bff (edge and platform operations)")
body = folded("description", "\n".join(gw_desc))
body += ["servers:", "- url: \"/api/recovery\"",
         "  description: \"Relative to the Recovery gateway-bff behind the shared App Gateway (Arch v5 slide 34)\"",
         "security:", "- entraId: []", "tags:", "- name: \"Administration\""]
body += ["x-service:", "  code: \"PLT\"", "  service: \"gateway-bff\"",
         "  name: \"Edge and gateway (platform library surface)\"", "  wave: 0",
         "  schema: \"none (no schema of its own; Redis session store, Arch v5 slide 34)\"",
         "  rest-base: \"/api/recovery\"",
         "  topic: \"none (no topic of its own; it consumes ApprovalRequested, TimerBreached and AceDataLate)\"",
         "  task-queue: \"none\"", "  namespace: \"rwb-recovery\"",
         "  asyncapi: \"none (no topic of its own)\"", f"  operations: {len(gw_ops)}"]
body.append("paths:")
by_path = {}
for o in gw_ops:
    by_path.setdefault(o["p"], []).append(o)
for p in [x for x in PATH_BLOCK if x in by_path]:
    body.append(f"  {p}:")
    for o in sorted(by_path[p], key=lambda o: METHODS.index(o["m"].lower())):
        body += annotate(o["block"], o)
need = closure([o["block"] for o in gw_ops])
body.append("components:")
body.append("  securitySchemes:")
body += COMP["securitySchemes"]["entraId"]
body.append("  responses:")
for name in COMP["responses"]:
    if ("responses", name) in need:
        body += COMP["responses"][name]
body.append("  schemas:")
for name in COMP["schemas"]:
    if ("schemas", name) in need:
        body += COMP["schemas"][name]
p = write_doc(OUT / "gateway-bff.yaml", head, body)
written.append(p)
GW = {"file": "gateway-bff.yaml", "operations": len(gw_ops), "ops": [o["id"] for o in gw_ops]}

# ---------------------------------------------------------------- asyncapi
EVENTS = [
    ("EV-01", "CaseCreated", "P3", "rwb.case.events.v1", ["rwb-agent", "rwb-deviation", "rwb-reporting"],
     ["caseId", "caseNo", "productGroup", "accounts", "businessDate"]),
    ("EV-02", "CaseAllocated", "P3", "rwb.case.events.v1", ["rwb-reporting"],
     ["caseId", "queueId", "ownerId", "ruleId", "ruleVersion"]),
    ("EV-03", "CaseAllocationFailed", "P3", "rwb.case.events.v1", ["rwb-case"],
     ["caseId", "reason", "ruleGap"]),
    ("EV-04", "CaseTransferred", "P3", "rwb.case.events.v1", ["rwb-reporting"],
     ["caseId", "fromOwner", "toOwner", "reasonCode"]),
    ("EV-05", "CaseStateChanged", "P3", "rwb.case.events.v1", ["rwb-comms", "rwb-reporting"],
     ["caseId", "fromState", "toState", "ruleId", "decisionLogEntryId"]),
    ("EV-19", "TimerBreached", "P3", "rwb.case.events.v1", ["gateway-bff (inbox)"],
     ["timerId", "caseId", "escalateTo"]),
    ("EV-06", "DeviationRaised", "S8", "rwb.deviation.events.v1", ["rwb-case", "rwb-comms", "rwb-treatment"],
     ["caseId", "deviationCode", "raisedBy"]),
    ("EV-07", "DeviationCleared", "S8", "rwb.deviation.events.v1", ["rwb-case", "rwb-comms"],
     ["caseId", "deviationCode", "outcome"]),
    ("EV-08", "DecisionRecorded", "P7", "rwb.decision-record.v1", ["rwb-decision", "rwb-reporting"],
     ["entryId", "caseId", "decisionCode", "approver"]),
    ("EV-09", "ApprovalRequested", "P7", "rwb.decision.events.v1", ["gateway-bff (inbox)"],
     ["approvalId", "caseId", "level", "amount"]),
    ("EV-30", "RulePackageInForce", "P7", "rwb.decision.events.v1",
     ["rwb-case", "rwb-valuation", "rwb-treatment", "rwb-payment"],
     ["packageCode", "packageVersion", "versionId", "validFrom", "approvedBy"]),
    ("EV-10", "TreatmentApproved", "S2", "rwb.treatment.events.v1", ["rwb-comms", "rwb-payment"],
     ["treatmentId", "caseId", "terms"]),
    ("EV-11", "TreatmentBooked", "P8", "rwb.payment.events.v1", ["rwb-case", "rwb-treatment"],
     ["treatmentId", "bookingRef", "businessDate"]),
    ("EV-12", "PaymentMissed", "P8", "rwb.payment.events.v1", ["rwb-case", "rwb-treatment", "rwb-comms"],
     ["treatmentId", "dueDate", "amountDue"]),
    ("EV-25", "ProceedsMatched", "P8", "rwb.payment.events.v1",
     ["rwb-case", "rwb-asset", "rwb-debtsale", "rwb-writeoff", "rwb-guarantee"],
     ["proceedsId", "caseId", "amount"]),
    ("EV-13", "NoticeGenerated", "P6", "rwb.comms.events.v1", ["rwb-decision"],
     ["noticeId", "caseId", "type", "templateVersion"]),
    ("EV-14", "NoticeDispatched", "P6", "rwb.comms.events.v1", ["rwb-reporting"],
     ["noticeId", "barcode", "sentDate"]),
    ("EV-15", "NoticeDelivered", "P6", "rwb.comms.events.v1", ["rwb-litigation", "rwb-guarantee", "rwb-case"],
     ["noticeId", "deliveredAt", "status"]),
    ("EV-16", "DocumentStored", "P5", "rwb.document.events.v1", ["rwb-agent", "rwb-case"],
     ["documentId", "caseId", "type", "source"]),
    ("EV-17", "DocumentFieldsExtracted", "P5", "rwb.document.events.v1", ["rwb-case"],
     ["documentId", "fields", "confidence"]),
    ("EV-20", "InstructionIssued", "S9", "rwb.partner.events.v1", ["partner portal"],
     ["instructionId", "partnerId", "type", "dueOn"]),
    ("EV-21", "PartnerResultSubmitted", "S9", "rwb.partner.events.v1",
     ["rwb-litigation", "rwb-asset", "rwb-case"],
     ["instructionId", "result", "documents"]),
    ("EV-22", "AssetTakenOn", "S5", "rwb.asset.events.v1", ["rwb-case", "rwb-payment"],
     ["assetId", "caseId", "source"]),
    ("EV-23", "LotAwarded", "S6", "rwb.debtsale.events.v1", ["rwb-case", "rwb-payment"],
     ["lotId", "buyerId", "price"]),
    ("EV-24", "WriteOffApproved", "S7", "rwb.writeoff.events.v1", ["rwb-case", "rwb-payment", "rwb-reporting"],
     ["writeOffId", "caseId", "amount"]),
    ("EV-26", "AceDataReady", "P1", "rwb.source-data.events.v1",
     ["rwb-case", "rwb-payment", "rwb-deviation", "rwb-writeoff"],
     ["sourceSystem", "businessDate", "status", "completedAt"]),
    ("EV-27", "AceDataLate", "P1", "rwb.source-data.events.v1", ["alerts", "gateway-bff banner"],
     ["sourceSystem", "businessDate", "status", "completedAt"]),
    ("EV-28", "AgentRunCompleted", "P10", "rwb.agent.events.v1",
     ["rwb-decision", "rwb-document", "rwb-deviation"],
     ["runId", "agent", "caseId", "outcome", "fallback"]),
    # Arch v5 slide 43 carry-on rows, no EV id and no payload column
    ("", "RouteDecided", "S1", "rwb.valuation.events.v1", ["rwb-case"], []),
    ("", "AssetSold", "S5", "rwb.asset.events.v1", ["rwb-payment", "rwb-case"], []),
    ("", "JudgmentRecorded", "S4", "rwb.litigation.events.v1", ["rwb-asset", "rwb-case"], []),
    ("", "AuctionResult", "S4", "rwb.litigation.events.v1", ["rwb-asset", "rwb-case"], []),
    ("", "TreatmentClosed", "S2", "rwb.treatment.events.v1", ["rwb-case", "rwb-reporting"], []),
    ("", "GuaranteeClaim", "S3", "rwb.guarantee.events.v1", ["rwb-case", "rwb-reporting"], []),
    ("", "AccountsTransferred", "S6", "rwb.debtsale.events.v1", ["rwb-case", "rwb-reporting"], []),
    ("", "AccessPolicyChanged", "P4", "rwb.access.events.v1", ["all (cache refresh)"], []),
    ("", "DoaLimitChanged", "P4", "rwb.access.events.v1", ["all (cache refresh)"], []),
    ("", "FileDelivered", "P2", "rwb.integration.events.v1", ["requesting service"], []),
    ("", "FileFailed", "P2", "rwb.integration.events.v1", ["requesting service"], []),
]

BY_SHORT = {s["service"]: s for s in SERVICES}
EV_BY_FILE = {}
for ev in EVENTS:
    s = BY_SHORT[BY_SHORT and [x for x in SERVICES if x["code"] == ev[2]][0]["service"]]
    EV_BY_FILE.setdefault(s["service"], []).append(ev)

TOPIC_X = {
    "partitions": 12, "replication-factor": 3, "retention": "7 days", "key": "caseId",
    "mode": "CloudEvents 1.0 Kafka binding, binary mode (ce_* headers)",
    "retry": "retry topics 1 min, 10 min, 1 h, then .dlt with alert",
    "schema-registry": "JSON Schema registry, BACKWARD compatibility",
    "fallback": "Event Hubs Premium",
    "source": "Arch v5 slide 35 (Kafka line) and slide 42 notes",
}


def asyncapi_doc(service, events, shared=False):
    s = BY_SHORT[service] if not shared else {"code": "P7", "service": "rwb-decision", "name": "Decision center and log",
                                             "wave": 1, "schema": "rwb_decision",
                                             "topic": "rwb.decision-record.v1", "queue": "rwb-decision"}
    topic = s["topic"] if not shared else "rwb.decision-record.v1"
    head = [f"# {HEADER[0]}", f"# {HEADER[1]}", "# Change log", f"# {ROW}", "", "asyncapi: 3.0.0", "info:",
            f"  title: {json.dumps(('Recovery Workbench events - ' + service) if not shared else 'Recovery Workbench events - shared decision record topic')}",
            "  version: 5.0.0"]
    if shared:
        desc = [
            "AsyncAPI 3.0 contract for the shared Kafka topic rwb.decision-record.v1. Every service writes its "
            "DecisionRecorded event to the local decision-record library and this topic (DP-03, ASM-B-ARCH-API-6); "
            "the topic is read by rwb-decision, which holds the central ledger, and by rwb-reporting (Arch v5 "
            "slides 42 and 14).",
            "One document covers the topic for all 19 services, so that the shared topic is not repeated in 19 "
            "documents; every service document names this file in its x-shared-topics list.",
            "Events carry IDs and facts, never personal data (Arch v5 slide 42 notes)."]
    else:
        desc = [
            f"AsyncAPI 3.0 contract for the business-event topic of {service} ({s['name']}, module {s['code']}). "
            f"One document per service, as Arch v5 slide 42 notes require; the document set is version 5.0.0 of "
            f"22 November 2026 (D-RCV-60 microservice realignment).",
            "Producer and consumer names are those of the Arch v5 event catalogue, slides 42 and 43; payload field "
            "names are those of Event and Messaging Design v4 (sheet Events, payload column). Property types, "
            "required flags and formats are not specified in the source documents (CG-B-ARCH-API-3; "
            "ASM-B-ARCH-API-3).",
            "Events carry IDs and facts, never personal data (Arch v5 slide 42 notes)."]
    body = folded("description", "\n".join(desc))
    body += ["x-topic:", f"  name: {json.dumps(topic)}"]
    body += [f"  {k}: {json.dumps(v) if isinstance(v, str) else v}" for k, v in TOPIC_X.items()]
    if not shared:
        body.append(f"  dead-letter: {json.dumps(topic + '.dlt')}")
        body.append("  dead-letter-note: \"Top-level name derived by appending .dlt to the service topic (Template and Rules R4)\"")
    body.append("defaultContentType: \"application/cloudevents+json\"")

    if events:
        body.append("channels:")
        body.append(f"  {json.dumps(topic)}:")
        body.append(f"    address: {json.dumps(topic)}")
        body.append(f"    title: {json.dumps(topic)}")
        body.append("    messages:")
        for ev in events:
            body.append(f"      {ev[1]}:")
            body.append(f"        $ref: '#/components/messages/{ev[1]}'")
        body.append("operations:")
        for ev in events:
            body.append(f"  publish{ev[1]}:")
            body.append("    action: send")
            body.append(f"    channel:")
            body.append(f"      $ref: '#/channels/{topic}'")
            body.append(f"    summary: {json.dumps('Publish ' + ev[1] + (' (' + ev[0] + ')' if ev[0] else '') + ' to ' + topic)}")
            body.append("    messages:")
            body.append(f"    - $ref: '#/channels/{topic}/messages/{ev[1]}'")
    else:
        body.append("channels: {}")
        body.append(f"x-note: {json.dumps('Arch v5 slide 41 gives ' + service + ' the topic ' + topic + '; slides 42 and 43 catalogue no event for it (CG-B-ARCH-API-4; ASM-B-ARCH-API-4).')}")
    if not shared:
        shared_note = "rwb.decision-record.v1"
        body.append(f"x-shared-topics:")
        body.append(f"- name: {json.dumps(shared_note)}")
        body.append("  asyncapi: \"asyncapi/rwb.decision-record.v1.asyncapi.yaml\"")
        body.append("  note: \"Every service publishes DecisionRecorded (DP-03); the shared contract sits in one document\"")
    body.append("components:")
    body.append("  messages:" if events else "  messages: {}")
    for ev in events:
        body.append(f"    {ev[1]}:")
        body.append(f"      name: {json.dumps(topic.split('.events')[0] + '.' + ev[1] + '.v1' if topic != 'rwb.decision-record.v1' else 'rwb.decision-record.' + ev[1] + '.v1')}")
        body.append(f"      title: {json.dumps(ev[1])}")
        body.append(f"      summary: {json.dumps((ev[0] + ' ' + ev[1]) if ev[0] else ev[1])}")
        body.append(f"      description: {json.dumps('Produced by ' + service + '; consumers: ' + ', '.join(ev[4]) if ev[4] else 'Produced by ' + service)}")
        body.append(f"      x-consumers: [{', '.join(json.dumps(c) for c in ev[4])}]")
        body.append("      contentType: \"application/cloudevents+json\"")
        body.append("      headers:")
        body.append("        $ref: '#/components/schemas/CloudEventsHeaders'")
        body.append("      payload:")
        body.append(f"        $ref: '#/components/schemas/{ev[1]}Event'")
    body.append("  schemas:")
    body += ["    CloudEventsHeaders:",
             "      type: object",
             "      description: \"CloudEvents 1.0 Kafka binding in binary mode; ce_* headers (Arch v5 slide 35)\"",
             "      properties:",
             "        ce_specversion:",
             "          type: string",
             "        ce_id:",
             "          type: string",
             "          description: \"Event ID; also the idempotency key (Event and Messaging Design v4, sheet Rules)\"",
             "        ce_source:",
             "          type: string",
             "        ce_type:",
             "          type: string",
             "        ce_time:",
             "          type: string",
             "          format: date-time",
             "        ce_subject:",
             "          type: string",
             "          description: \"Kafka key: caseId (Arch v5 slide 35)\"",
             "        ce_datacontenttype:",
             "          type: string"]
    for ev in events:
        body.append(f"    {ev[1]}Event:")
        body.append("      allOf:")
        body.append("      - $ref: '#/components/schemas/CloudEventEnvelope'")
        body.append("      - type: object")
        body.append("        properties:")
        body.append("          type:")
        body.append(f"            const: {json.dumps((topic.split('.events')[0] + '.' + ev[1] + '.v1') if topic != 'rwb.decision-record.v1' else 'rwb.decision-record.' + ev[1] + '.v1')}")
        body.append("          data:")
        body.append("            type: object")
        if ev[5]:
            body.append(f"            description: {json.dumps(((ev[0] + ' ') if ev[0] else '') + ev[1] + ' payload; field names from Event and Messaging Design v4 (sheet Events); property types, required flags and formats are not specified in the source documents (CG-B-ARCH-API-3; ASM-B-ARCH-API-3)')}")
            body.append("            properties:")
            for f in ev[5]:
                body.append(f"              {f}: {{}}")
        else:
            body.append(f"            description: {json.dumps('Payload of ' + ev[1] + ' is Not specified in the source documents (CG-B-ARCH-API-3; ASM-B-ARCH-API-3): Arch v5 slide 43 lists the event name only, with no payload column')}")
            body.append("            properties: {}")
    body += ["    CloudEventEnvelope:",
             "      type: object",
             "      description: \"CloudEvents 1.0 envelope (specversion, id, source, type, time, subject, data); Kafka binary mode carries the attributes in ce_* headers (Arch v5 slide 35)\"",
             "      required: [specversion, id, source, type, time, subject, data]",
             "      properties:",
             "        specversion:",
             "          type: string",
             "          const: \"1.0\"",
             "        id:",
             "          type: string",
             "        source:",
             "          type: string",
             "        type:",
             "          type: string",
             "        time:",
             "          type: string",
             "          format: date-time",
             "        subject:",
             "          type: string",
             "        datacontenttype:",
             "          type: string",
             "        data:",
             "          type: object"]
    return head, body


ASYNC = []
for s in SERVICES:
    evs = EV_BY_FILE.get(s["service"], [])
    head, body = asyncapi_doc(s["service"], evs)
    path = OUT / "asyncapi" / f"{s['service']}.asyncapi.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    write_doc(path, head, body)
    written.append(path)
    ASYNC.append({"file": f"asyncapi/{s['service']}.asyncapi.yaml", "service": s["service"],
                  "topic": s["topic"], "events": [e[1] for e in evs]})
head, body = asyncapi_doc("rwb-decision", [e for e in EVENTS if e[1] == "DecisionRecorded"], shared=True)
path = OUT / "asyncapi" / "rwb.decision-record.v1.asyncapi.yaml"
write_doc(path, head, body)
written.append(path)
ASYNC.append({"file": "asyncapi/rwb.decision-record.v1.asyncapi.yaml", "service": "all 19 producers",
              "topic": "rwb.decision-record.v1", "events": ["DecisionRecorded"]})

# ---------------------------------------------------------------- index
idx_desc = [
    "Index and document map of Recovery Workbench API version 5.0.0, 22 November 2026, "
    f"{DEC} microservice realignment. The v4 document (one OpenAPI file for the whole module) is split into one "
    "document per service (19), the gateway-bff document and this index: every operation sits in exactly one "
    "document, and every document carries the same operation, schema, response, parameter, number and date text "
    "as v4.",
    "Owner of every operation is the owner of Microservice Ownership Map v1 (sheet Endpoints); where that owner "
    "differs from the v4 x-module, the operation carries x-owner and x-owner-note and the move is listed under "
    "x-owner-changes. REST base of each service is /api/recovery/<short>/v1, topic rwb.<short>.events.v1, task "
    "queue rwb-<short> in namespace rwb-recovery (Template and Rules R4; Arch v5 slide 41).",
    "Each served topic has an AsyncAPI 3.0 document under asyncapi/, one per service plus one shared document for "
    "rwb.decision-record.v1 (Arch v5 slide 42 notes: the AsyncAPI document per service is the contract).",
    "Version 4.0.0 description follows unchanged.",
    doc["info"]["description"]]
head = doc_head("Recovery Workbench API - index")
body = folded("description", "\n".join(idx_desc))
body += ["servers:",
         "- url: \"/api/recovery\"",
         "  description: \"Shared App Gateway route to the Recovery gateway-bff (Arch v5 slide 34); each service document carries its own base /api/recovery/<short>/v1\"",
         "security:", "- entraId: []", "tags:"]
body += [f"- name: {json.dumps(t['name'])}" for t in doc["tags"]]
body += ["x-source:",
         "  file: \"05 Technical architecture/Recovery Workbench API Specification v4.yaml\"",
         "  title: \"Recovery Workbench API\"", "  version: \"4.0.0\"", "  date: \"16 November 2026\"",
         f"  paths: {len(doc['paths'])}", f"  operations: {len(OPS)}",
         f"  schemas: {len(COMP['schemas'])}", f"  responses: {len(COMP['responses'])}",
         f"  securitySchemes: {len(COMP['securitySchemes'])}",
         "  document: \"05 Technical architecture/Recovery Workbench API Specification v4.yaml\"",
         "  document-set: \"05 Technical architecture/Recovery Workbench API Specification v5\"",
         "x-owner-map: \"22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (sheet Endpoints); _work/msr/plan/ownership.json, section api\"",
         "x-decision: \"D-RCV-60\"",
         f"x-tool: {json.dumps(TOOL)}",
         "x-document-set:"]
for s in SUMMARY:
    body += [f"- code: {json.dumps(s['code'])}",
             f"  service: {json.dumps(s['service'])}",
             f"  name: {json.dumps(s['name'])}",
             f"  wave: {s['wave']}",
             f"  schema: {json.dumps(s['schema'])}",
             f"  rest-base: {json.dumps(s['base'])}",
             f"  topic: {json.dumps(s['topic'])}",
             f"  task-queue: {json.dumps(s['queue'])}",
             f"  file: {json.dumps(s['file'])}",
             f"  asyncapi: {json.dumps(s['asyncapi'])}",
             f"  operations: {s['operations']}",
             f"  tags: [{', '.join(json.dumps(t) for t in s['tags'])}]"]
body += ["- code: \"PLT\"", "  service: \"gateway-bff\"", "  name: \"Edge and gateway (platform library surface)\"",
         "  wave: 0", "  file: \"gateway-bff.yaml\"", "  asyncapi: \"none (no topic of its own)\"",
         f"  operations: {GW['operations']}", "  platform-operations: [" + ", ".join(json.dumps(o) for o in GW["ops"]) + "]"]
body += ["x-totals:",
         f"  documents: {len(SUMMARY) + 2}",
         f"  service-documents: {len(SUMMARY)}",
         f"  operations: {len(OPS)}",
         f"  asyncapi-documents: {len(ASYNC)}",
         "  components-copied-per-document: true"]
body.append("x-owner-changes:")
for o in [x for x in OPS if x["owner"] != x["x-module"]]:
    body += [f"- operation: {json.dumps(o['id'])}",
             f"  x-module: {json.dumps(o['x-module'])}",
             f"  owner: {json.dumps(o['owner'])}",
             f"  file: {json.dumps(BY_CODE[o['owner']]['service'] + '.yaml' if o['owner'] != 'PLT' else 'gateway-bff.yaml')}",
             f"  asm: {json.dumps(asm_of(o))}"]
body.append("x-unreferenced-schemas:")
for name, owner in ORPHANS.items():
    body += [f"- schema: {json.dumps(name)}",
             f"  file: {json.dumps(BY_CODE[owner]['service'] + '.yaml')}",
             "  note: \"Kept from v4; no operation of v4 references it. Placed in the document of the service that owns the domain (CG-B-ARCH-API-5; ASM-B-ARCH-API-5)\""]
body.append("x-tag-index:")
tmap = {}
for s in SUMMARY:
    for t in s["tags"]:
        tmap.setdefault(t, []).append(s["service"])
for t in [x["name"] for x in doc["tags"]]:
    body += [f"  {json.dumps(t)}: [{', '.join(json.dumps(x) for x in tmap.get(t, []))}]"]
body.append("x-asyncapi-documents:")
for a in ASYNC:
    body += [f"- file: {json.dumps(a['file'])}",
             f"  service: {json.dumps(a['service'])}",
             f"  topic: {json.dumps(a['topic'])}",
             f"  events: [{', '.join(json.dumps(e) for e in a['events'])}]"]
body += ["x-change-log:",
         "- version: \"5.0.0\"",
         "  date: \"22 November 2026\"",
         "  decision: \"D-RCV-60 microservice realignment\"",
         f"  tool: {json.dumps(TOOL)}",
         "  change: \"Split into 19 service documents, gateway-bff and this index; owner from Microservice Ownership Map v1; AsyncAPI 3.0 per topic under asyncapi/\"",
         "- version: \"4.0.0\"",
         "  date: \"16 November 2026\"",
         "  decision: \"D-RCV-36 (rule packages in embedded Drools)\"",
         "  tool: \"not stated in the source\""]
body += ["paths: {}"]
p = write_doc(OUT / "index.yaml", head, body)
written.append(p)

print("written:", len(written))
for w in written:
    print("  ", w.relative_to(ROOT))
print("ops per doc:", {k: len(v) for k, v in FILES.items()}, "PLT:", len(PLT))
print("asyncapi docs:", len(ASYNC))
