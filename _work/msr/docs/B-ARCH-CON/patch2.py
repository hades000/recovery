from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
subs = [
    ('LABEL["PARTNER"] = "Partner portal"',
     'LABEL["PARTNER"] = "Partner portal"\nLABEL["REQUESTER"] = "The requesting service"\nLABEL["NOTSPEC"] = "Not specified in the source documents (CG-B-ARCH-CON-4; ASM-B-ARCH-CON-4)"'),
    ('("EV-27", "AceDataLate", "P1", ["ALL"]),', '("EV-27", "AceDataLate", "P1", ["BFF"]),'),
    ('L.append("Not shown in the matrix because every service does it: audit and PII logs to ACE Common on Kafka, DecisionRecorded to rwb-decision on rwb.decision-record.v1, permission data cached from rwb-access, and traces to OpenTelemetry. Those four rows are carried in section 5 as All 19 services so that they are not lost.")',
     'L.append("Not shown in the matrix because every service does it: audit and PII logs to ACE Common on Kafka, DecisionRecorded to rwb-decision on rwb.decision-record.v1, permission data cached from rwb-access, and traces to OpenTelemetry. The first two and the permission cache are carried in section 5 as All 19 services so that they are not lost; traces are a platform contract and are named in section 7.3.")'),
    ('    rows.append([LABEL.get(p, p), LABEL.get(c, c), t, i, artefact(p, t), pair_class(p, c), s])',
     '    rows.append([LABEL.get(p, p), LABEL.get(c, c), t, i, artefact(p, t, i), pair_class(p, c), s])'),
    ('[[t, LABEL.get(c, c), i, artefact(p, t), pair_class(p, c), src] for p, c, t, i, src in prov])',
     '[[t, LABEL.get(c, c), i, artefact(p, t, i), pair_class(p, c), src] for p, c, t, i, src in prov])'),
    ('[[t, LABEL.get(p, p), i, artefact(p, t), pair_class(p, c),',
     '[[t, LABEL.get(p, p), i, artefact(p, t, i), pair_class(p, c),'),
    ('    ["CG-B-ARCH-CON-7", "The request and response content of the Enterprise AI private endpoint (INT-23) is not specified", "Section 8.4 names the edge and the stub, not a payload", "Solution architect"],',
     '    ["CG-B-ARCH-CON-7", "The request and response content of the Enterprise AI private endpoint (INT-23) is not specified", "Section 8.4 names the edge and the stub, not a payload", "Solution architect"],\n    ["CG-B-ARCH-CON-8", "The call-type matrix marks S5 to P6 as Temporal, but the write-off, asset, debt sale, litigation, guarantee and payment contracts name no communications interface for rwb-asset", "Section 6.15 carries the placeholder in its Temporal row and no interface is invented", "Solution architect"],'),
    ('OUT_MD.write_text("\\n".join(L) + "\\n", encoding="utf-8")',
     'TEXT = "\\n".join(L).replace("&lt;", "<").replace("&gt;", ">")\nOUT_MD.write_text(TEXT + "\\n", encoding="utf-8")'),
]
for a, b in subs:
    if a not in t:
        raise SystemExit("NOT FOUND: " + a[:80])
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("patched", len(subs))
