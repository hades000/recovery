from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
t = t.replace('''OUT_MD.write_text("\\n".join(L) + "\\n", encoding="utf-8")''', '''OUT_MD.write_text("\\n".join(L) + "\\n", encoding="utf-8")''')
app = r'''

# ================================================================ workbook source
X = []
X.append("## Read me")
X.append("")
xr = [
    ["Item", "Value"],
    ["Document", "Recovery Workbench Service Contract Catalog v1"],
    ["Version", "1"],
    ["Date", DATE],
    ["Decision", f"{DEC} microservice realignment"],
    ["Tool", TOOL],
    ["Status", "Draft"],
    ["Owner role", "Solution architect"],
    ["Purpose", "The contract register of the 19 Recovery services: what each service provides and consumes, in which call type, under which artefact, with which dependency class and which test"],
    ["Source of record", "Architecture v5 Text Extract v1 slides 13 to 20 and 41 to 44; Temporal and Drools Design Text Extract v1 slides 11 to 14; Microservice Ownership Map v1"],
    ["Sheets", "Services; Call type matrix; Contract pairs; REST operations; Events; Temporal contracts; Jobs; Resources owned; Conformance; Open points; Change log"],
    ["How to read", "Contract pairs is the flat list behind section 5 of the document; one row per provider and consumer pair, class C for a service pair, X for an edge, H for the one self-subscription"],
    ["Nickname", "Every owner in this workbook comes from the Microservice Ownership Map v1"],
]
for r in xr:
    X.append("| " + " | ".join(r) + " |")
X.append("")

X.append("## Services")
X.append("")
rows = [["Code", "Service", "Name", "Wave", "Schema and login", "REST base", "Kafka topic", "Task queue", "Java package", "Service epic", "Owns (Arch v5 slide 41)"]]
for s in SERVICES:
    rows.append([s["code"], s["svc"], s["name"], s["wave"], s["schema"], s["base"], s["topic"], s["queue"], s["pkg"], f"RWB-SVC-{s['code']}", OWN_ROWS[s["code"]]])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Call type matrix")
X.append("")
rows = [["starts / target"] + MATRIX_COLS]
for r in M:
    rows.append([LABEL[r]] + [M[r].get(c, "") for c in MATRIX_COLS])
for r in rows:
    X.append("| " + " | ".join(r) + " |")
X.append("")

X.append("## Contract pairs")
X.append("")
rows = [["#", "Provider", "Consumer", "Call type", "Interface", "Contract artefact", "Class", "ITG harness", "Source"]]
for n, (p_, c, ty, i, src) in enumerate(sorted(PAIRS, key=lambda x: (x[0], x[1], x[2], x[3])), 1):
    rows.append([n, LABEL.get(p_, p_), LABEL.get(c, c), ty, i, artefact(p_, ty, i), pair_class(p_, c), itg(p_, c), src])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## REST operations")
X.append("")
rows = [["Operation", "Owner", "Contract path", "Base path"]]
for op in sorted(API):
    o = API[op]["owner"]
    rows.append([op, o, f"{SVC[o]['base']}{op.split(' ', 1)[1]}" if o in SVC else op, SVC[o]["base"] if o in SVC else "PLT"])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Events")
X.append("")
rows = [["ID", "Event", "Producer", "Topic", "Consumers", "Numbered in the event catalogue", "Source"]]
for eid, name, prod, cons in EVENTS:
    topic = "rwb.decision-record.v1" if eid == "EV-08" else (TOPIC.get(prod, "-") if prod != "PLT" else "-")
    rows.append([eid, name, LABEL.get(prod, prod), topic, "; ".join(LABEL.get(c, c) for c in cons), "Yes", "Arch v5 slide 42, slide 43"])
for name, prod, cons in EXTRA_EVENTS:
    rows.append(["-", name, LABEL.get(prod, prod), TOPIC.get(prod, "-"), "; ".join(LABEL.get(c, c) for c in cons), "No", "Arch v5 slide 43 (not numbered)"])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Temporal contracts")
X.append("")
rows = [["Type", "Name", "Owner", "Task queue", "Contract artefact", "Consumers", "Source"]]
for name in sorted(WF, key=lambda n: (WF[n]["owner"], n)):
    o = WF[name]["owner"]
    rows.append(["Workflow", name, LABEL.get(o, o), SVC[o]["queue"] if o in SVC else "-", "Activity contract jar", "; ".join(sorted({LABEL.get(c, c) for p_, c, ty, i, src in PAIRS if ty == "Temporal" and i.endswith(name)})), "Ownership Map v1, Workflows and activities"])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Jobs")
X.append("")
rows = [["Job", "Owner", "Contract form", "Source"]]
JOBDESC = {}
for jid in sorted(JOBS):
    o = JOBS[jid]["owner"]
    rows.append([jid, LABEL.get(o, o), JOBS[jid].get("replacement", ""), "Arch v5 slide 44; Ownership Map v1, Jobs"])
for r in rows:
    X.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")
X.append("")

X.append("## Resources owned")
X.append("")
rows = [["Table", "Owner", "Schema", "Basis"]]
for tb in sorted(TABLES):
    o = TABLES[tb]["owner"]
    basis = TABLES[tb]["basis"]
    basis = ("Ownership Map ruling" if TABLES[tb].get("ruling") else "Ownership Map v1, Tables sheet") + (f"; {TABLES[tb]['asm']}" if TABLES[tb].get("asm") else "")
    rows.append([tb, o, TABLES[tb].get("schema", SVC[o]["schema"] if o in SVC else "every rwb_* schema"), basis])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Conformance")
X.append("")
rows = [["#", "Contract rule", "Tested by"]]
conf = [
    "The provider publishes its OpenAPI 3.1, AsyncAPI 3.0 and activity contract jar before the implementation story starts",
    "Every operation in section 6 exists in the published contract, under the service's own base path",
    "Every event the service publishes is in its AsyncAPI document, on its own topic, with CloudEvents 1.0 binary mode and key caseId",
    "Every event the service consumes is deduplicated in processed_event, in the same transaction as the change",
    "Every activity and child workflow the service calls is declared in the provider's contract jar; no service imports another service's code",
    "No REST chain longer than one hop; route services reach shared capabilities through Temporal",
    "No cross-schema read, join, view or foreign key; the boundary test fails the build on any violation",
    "Every POST and PATCH is idempotent through Idempotency-Key, and every consumer of the same key returns the first result",
    "Error responses follow RFC 9457 for REST and the error code form for events",
    "The provider's fake serves every operation and every event of its contract",
    "The pair is proved end to end in the integration story of the later wave",
    "The contract document is registered in section 6 with its version",
]
ctests = ["Contract publication gate in the pipeline", "OpenAPI diff against the Ownership Map Endpoints sheet",
          "AsyncAPI validation plus a schema registry check", "Inbox test", "Activity contract test",
          "Contract test plus trace-depth check", "Architecture test", "Idempotency test", "Contract example test",
          "Fake conformance test in the consumer build", "RWB-ITG-W<n> harness", "Registration check on the CON story"]
for n, (a, b) in enumerate(zip(conf, ctests), 1):
    rows.append([n, a, b])
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Open points")
X.append("")
rows = [["ID", "Point", "Effect in this catalogue", "Owner role"]]
pts = [
    ("CG-B-ARCH-CON-1", "No earlier Service Contract Catalog exists, so v1 carries no inherited sections, IDs, numbers or dates", "Version 1, status Draft; the change-log row is the first", "Delivery lead"),
    ("CG-B-ARCH-CON-2", "The Ownership Map Endpoints sheet holds the monolith operations of API Specification v4, while Architecture v5 slide 41 states a per-service base path; the per-service paths and payloads are written in API Specification v5", "Section 6 lists the operation per owning service under its base path and leaves the final path to API Specification v5", "Solution architect"),
    ("CG-B-ARCH-CON-3", "The coordinates of the activity contract jars (groupId, artifactId, version) are not specified", "Section 7.1 states the artefact and the package root, and leaves the coordinates open", "Tech lead"),
    ("CG-B-ARCH-CON-4", "The event catalogue does not name the consumers of ApprovalDecided or ReportPublished", "The two rows state Not specified in the source documents", "Solution architect"),
    ("CG-B-ARCH-CON-5", "The schema registry product and its deployment are not specified; only the BACKWARD compatibility rule is stated", "Section 7.2 states the compatibility rule and not the product", "Platform architect"),
    ("CG-B-ARCH-CON-6", "The slide 13 rule that route services reach shared capabilities through Temporal sits beside REST cells from S1, S7 and S8 to rwb-source-data", "Section 8.3 reads the rule as covering the five shared capabilities named in the slide note; the rwb-source-data reads stay REST", "Solution architect"),
    ("CG-B-ARCH-CON-7", "The request and response content of the Enterprise AI private endpoint (INT-23) is not specified", "Section 8.4 names the edge and the stub, not a payload", "Solution architect"),
    ("CG-B-ARCH-CON-8", "The call-type matrix marks S5 to P6 as Temporal, but the asset contract on Architecture v5 slide 19 names no communications interface and no other slide supplies one", "Section 6.15 carries the placeholder in its Temporal row and no interface is invented", "Solution architect"),
]
for r in pts:
    rows.append(list(r))
for r in rows:
    X.append("| " + " | ".join(str(x) for x in r) + " |")
X.append("")

X.append("## Change log")
X.append("")
rows = [["Version", "Date", "Change", "Detail"],
        ["1", DATE, f"{DEC} microservice realignment, {TOOL}",
         "First Service Contract Catalog: contract model, call-type matrix, contract inventory, contract by service, shared platform contracts, dependency classes, contract tests and change control"]]
for r in rows:
    X.append("| " + " | ".join(r) + " |")
X.append("")

for line in X:
    if line.startswith("|") and "|" in line[1:]:
        cells = line.strip().strip("|").split("|")
        for cell in cells:
            if "\n" in cell:
                raise SystemExit("NEWLINE IN CELL")
XLSX_MD.write_text("\n".join(X) + "\n", encoding="utf-8")
print("WROTE", XLSX_MD)

# ================================================================ gap and assumption rows
gap_rows = [
    {"id": "CG-B-ARCH-CON-1", "title": "No earlier Service Contract Catalog exists",
     "source": "05 Technical architecture (folder listing); Template and Rules \u00a7R8.4", "section": "Document control; section 12",
     "description": "This family has no earlier version, so v1 cannot inherit sections, IDs, numbers or dates from it.",
     "evidence": "No Service Contract Catalog file exists in folder 05 or anywhere else in the set; Template and Rules \u00a7R8.4 lists Service Contract Catalog v1 as a new architecture output.",
     "type": "Missing", "area": "Document version", "severity": "P3", "needed_by_wave": 0, "legacy_ref": "",
     "owner_role": "Delivery lead", "asm": "ASM-B-ARCH-CON-1",
     "proposed": "Publish v1 as the first version, status Draft, and start the change log with the D-RCV-60 row.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-2", "title": "Ownership Map endpoints are the monolith operations",
     "source": "Recovery Workbench Microservice Ownership Map v1, Endpoints sheet; Architecture v5 Text Extract v1 slide 41", "section": "Section 6",
     "description": "The Endpoints sheet holds 156 operations with the monolith paths of API Specification v4 and a per-module owner, while Architecture v5 slide 41 states a per-service base path. The per-service path and payload of each operation are not written in any source in this read set.",
     "evidence": "Ownership Map v1 Endpoints sheet rows such as GET /cases/{caseId} owned by P3; Architecture v5 slide 41 gives the base /api/recovery/case/v1; API Specification v5 is the document that rewrites them.",
     "type": "Ambiguous", "area": "REST contract", "severity": "P2", "needed_by_wave": 1, "legacy_ref": "RWB-E1-001",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-2",
     "proposed": "List each operation under its owning service and its Architecture v5 base path, and leave the final operation path and payload to API Specification v5.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-3", "title": "Activity contract jar coordinates are not specified",
     "source": "Architecture v5 Text Extract v1 slide 11; Temporal and Drools Design Text Extract v1 slide 12", "section": "Section 7.1",
     "description": "Each service publishes an activity contract jar on its own task queue, but no source states the groupId, artifactId or versioning scheme of those jars.",
     "evidence": "Temporal and Drools Design slide 12 names the L4 activity contracts per service; Architecture v5 says no service imports another's code, only its contract jar; neither gives coordinates.",
     "type": "Missing", "area": "Temporal contract", "severity": "P2", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Tech lead", "asm": "ASM-B-ARCH-CON-3",
     "proposed": "State the artefact and the Java package root now, and allocate the coordinates with the repositories in the service template work.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-4", "title": "Consumers of two events are not named",
     "source": "Architecture v5 Text Extract v1 slides 42 and 43", "section": "Section 5; section 6",
     "description": "The event catalogue names no consumer for ApprovalDecided (rwb.decision.events.v1) or ReportPublished (rwb.reporting.events.v1), although both events are listed in the service contracts of slide 14 as OUT.",
     "evidence": "Slide 14 P7 OUT names ApprovalDecided; slide 15 P9 OUT names ReportPublished; slides 42 and 43 give consumers for every other event and none for these two.",
     "type": "Missing", "area": "Event contract", "severity": "P3", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-4",
     "proposed": "Carry the two rows with the placeholder and settle the consumers with the API and event catalogue owners.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-5", "title": "Schema registry product is not specified",
     "source": "Architecture v5 Text Extract v1 slide 42 notes", "section": "Section 7.2",
     "description": "The sources fix the compatibility rule (BACKWARD) and the AsyncAPI per service, but not the registry product, its deployment or its retention.",
     "evidence": "Architecture v5 slide 42 notes: schemas are versioned in the registry with BACKWARD compatibility. No product is named anywhere in the read set.",
     "type": "Missing", "area": "Event contract", "severity": "P3", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Platform architect", "asm": "ASM-B-ARCH-CON-5",
     "proposed": "State the compatibility rule and the artefact in this catalogue; choose the product in the Kafka event platform work.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-6", "title": "Route-services-through-Temporal rule meets REST cells to rwb-source-data",
     "source": "Architecture v5 Text Extract v1 slide 13", "section": "Section 4; section 8.3",
     "description": "Slide 13 states that route services reach shared capabilities through Temporal, never REST, and the same matrix gives REST cells from S1, S7 and S8 to rwb-source-data.",
     "evidence": "Slide 13 note: route services reach shared capabilities through Temporal, never REST, only rwb-source-data touches ACE's tables. Matrix cells S1 to P1, S7 to P1 and S8 to P1 are R.",
     "type": "Conflict", "area": "Call type", "severity": "P2", "needed_by_wave": 1, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-6",
     "proposed": "Read the rule as covering the five shared capabilities named in the slide note (decision, document, payment, partner, comms); keep the rwb-source-data reference reads as REST, one hop and cached.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-7", "title": "Enterprise AI endpoint contract is not specified",
     "source": "Architecture v5 Text Extract v1 slide 16", "section": "Section 8.4",
     "description": "rwb-agent calls Enterprise AI on an HTTPS private endpoint (INT-23); no source in the read set gives the request, the response, the timeout or the model routing.",
     "evidence": "Slide 16 P10 OUT: Enterprise AI endpoint: HTTPS private endpoint. The System Disposition and Integration Inventory names INT-23 only.",
     "type": "Missing", "area": "External contract", "severity": "P3", "needed_by_wave": 2, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-7",
     "proposed": "Name the edge and the test double here, and settle the payload with the P10 agent work.", "wp": "B-ARCH-CON"},
    {"id": "CG-B-ARCH-CON-8", "title": "Matrix cell S5 to P6 has no named interface",
     "source": "Architecture v5 Text Extract v1 slides 13, 17 and 19", "section": "Section 5; section 6.15",
     "description": "The call-type matrix marks the S5 Asset row against P6 Communications as Temporal, but the asset contract on slide 19 lists no communications call and no other slide names one.",
     "evidence": "Slide 13 S5 row, P6 column: T. Slide 19 S5 OUT: Partner issueInstruction, Decision approval, Payment postProceeds, and no comms entry.",
     "type": "Conflict", "area": "Temporal contract", "severity": "P3", "needed_by_wave": 2, "legacy_ref": "",
     "owner_role": "Solution architect", "asm": "ASM-B-ARCH-CON-8",
     "proposed": "Carry the row with the placeholder in section 6.15 and confirm the interface with the S5 and P6 owners; do not invent an operation.", "wp": "B-ARCH-CON"},
]
GAPS.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in gap_rows) + "\n", encoding="utf-8")

asm_rows = [
    {"id": "ASM-B-ARCH-CON-1", "text": "This is version 1 of the Service Contract Catalog and it inherits no section, ID, number or date.",
     "why": "No earlier version of the family exists.", "read": "Folder 05 listing; Template and Rules \u00a7R8.4", "gap": "CG-B-ARCH-CON-1",
     "applied_in": "Document control; section 12", "confidence": "High", "confirm": "Delivery lead", "impact": "None on content; the change log starts here.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-2", "text": "The Ownership Map Endpoints sheet is read as the operation set per owning service; the per-service base path comes from Architecture v5 slide 41 and Template and Rules \u00a7R4, and the final path and payload belong to API Specification v5.",
     "why": "Two sources describe the REST surface at different levels.", "read": "Ownership Map v1, Endpoints sheet; Architecture v5 slide 41; Template and Rules \u00a7R4", "gap": "CG-B-ARCH-CON-2",
     "applied_in": "Section 6, REST operations owned", "confidence": "Medium", "confirm": "Solution architect", "impact": "No operation is added or removed; only the base path is applied.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-3", "text": "The activity contract jars are named by their task queue and Java package root; the coordinates are left open for allocation.",
     "why": "The coordinates are not stated in any source.", "read": "Architecture v5 slide 11; Temporal and Drools Design slide 12", "gap": "CG-B-ARCH-CON-3",
     "applied_in": "Section 7.1", "confidence": "Medium", "confirm": "Tech lead", "impact": "The build story allocates coordinates; no contract changes.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-4", "text": "ApprovalDecided and ReportPublished are recorded with the placeholder for their consumers rather than an assumed consumer.",
     "why": "The event catalogue names no consumer.", "read": "Architecture v5 slides 14, 15, 42, 43", "gap": "CG-B-ARCH-CON-4",
     "applied_in": "Section 5; section 6", "confidence": "High", "confirm": "Solution architect", "impact": "Two registry rows stay open.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-5", "text": "This catalogue states the AsyncAPI artefact, CloudEvents 1.0 binary mode and BACKWARD compatibility, and does not name a registry product.",
     "why": "The product is not specified in the read set.", "read": "Architecture v5 slide 42 notes", "gap": "CG-B-ARCH-CON-5",
     "applied_in": "Section 7.2", "confidence": "High", "confirm": "Platform architect", "impact": "The platform work chooses the product; the contract rule holds either way.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-6", "text": "The rule that route services reach shared capabilities through Temporal is read as covering decision, document, payment, partner and communications, the five capabilities the slide note names; the rwb-source-data reference reads stay REST, one hop and cached.",
     "why": "The matrix gives both REST cells to rwb-source-data and the rule.", "read": "Architecture v5 slide 13 and its notes", "gap": "CG-B-ARCH-CON-6",
     "applied_in": "Section 4; section 8.3", "confidence": "Medium", "confirm": "Solution architect", "impact": "Three REST pairs stay synchronous; no route service gains a REST call to a shared capability.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-7", "text": "The Enterprise AI call is carried as an edge contract with a recorded-response double; no payload is stated.",
     "why": "The integration contract is not specified.", "read": "Architecture v5 slide 16", "gap": "CG-B-ARCH-CON-7",
     "applied_in": "Section 8.4", "confidence": "Medium", "confirm": "Solution architect", "impact": "P10 tests against the double until the endpoint contract is agreed.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-8", "text": "The S5 to P6 Temporal cell is kept with the placeholder and no interface is invented.",
     "why": "The matrix and the service contract disagree.", "read": "Architecture v5 slides 13 and 19", "gap": "CG-B-ARCH-CON-8",
     "applied_in": "Section 5; section 6.15", "confidence": "Medium", "confirm": "Solution architect", "impact": "One Temporal row stays open in the S5 contract.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-9", "text": "Every cross-service pair is class C for the consuming story and class I for the integration story of the later wave; every pair that touches gateway-bff, ACE Common, the ACE database, Enterprise AI, the bank file channels or partners is class X.",
     "why": "Template and Rules \u00a7R5.4 defines the classes but not the assignment per pair.", "read": "Template and Rules \u00a7R5.4", "gap": "",
     "applied_in": "Section 5; section 8.1", "confidence": "High", "confirm": "Solution architect", "impact": "No consumer story waits for a provider build.", "wp": "B-ARCH-CON"},
    {"id": "ASM-B-ARCH-CON-10", "text": "No release date is held in this catalogue; the dates in the Release Plan are unchanged and every one is tentative.",
     "why": "Decision U7 and DL48 fix this, and the source has no release date.", "read": "Template and Rules \u00a7R1 (U7); Architecture v5 slide 38", "gap": "",
     "applied_in": "Section 1", "confidence": "High", "confirm": "Delivery lead", "impact": "None; this catalogue carries no date but the document date.", "wp": "B-ARCH-CON"},
]
ASMS.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in asm_rows) + "\n", encoding="utf-8")
print("WROTE", GAPS, "and", ASMS, len(gap_rows), len(asm_rows))
'''
t = t + app
p.write_text(t, encoding="utf-8")
print("appended")
