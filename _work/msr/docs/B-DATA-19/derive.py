"""Derive the D-RCV-60 owner, schema, route and consuming services for every v4 list and
reference table row, from the v4 workbook text and the Ownership Map. Writes derive.json."""
import json, re
from collections import Counter

import openpyxl

SRC = "06 Data/Recovery Workbench Reference Data and Lists of Values v4.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
OUT = "_work/msr/docs/B-DATA-19/derive.json"

wb = openpyxl.load_workbook(SRC, data_only=True)
ows = openpyxl.load_workbook(OWN, data_only=True)

table_owner, table_schema = {}, {}
for row in ows["Tables"].iter_rows(min_row=2, values_only=True):
    if row and row[0]:
        table_owner[str(row[0])] = str(row[1])
        table_schema[str(row[0])] = str(row[2])
service_name, service_schema, service_wave = {}, {}, {}
for row in ows["Services"].iter_rows(min_row=2, values_only=True):
    if row and row[0]:
        code = str(row[0])
        service_name[code] = str(row[1])
        service_wave[code] = str(row[3])
        service_schema[code] = str(row[4])
service_name["PLT"] = "platform library"
service_schema["PLT"] = "platform library (a library object in each service schema)"
service_wave["PLT"] = "0"

lists = []
for r in wb["Lists"].iter_rows(min_row=5, values_only=True):
    if not r or not r[0]:
        continue
    lists.append([str(c).strip() if c is not None else "" for c in r[:6]])

NO_FIELD_PREFIXES = ("No live field", "ACE batch", "ACE ingestion", "Cutover plan", "Outbound interfaces")
ROUTE = {
    "P3": "rwb-case list read, RWB-P3-E1043-CON (DP-07)",
    "P4": "rwb-access contract RWB-P4-E1037-CON (DP-08)",
    "P5": "rwb-document contract (DP-07)",
    "P6": "rwb-comms contract (DP-07)",
    "P7": "rwb-decision rule packages RWB-P7-E1073-CON (DP-04)",
    "S9": "rwb-partner contract (DP-07)",
    "PLT": "platform library (R-PREC default ruling)",
    "P1": "ACE read through the P1 contract, not loaded (DP-05)",
}
ASSUMED = {}   # code -> note where the source has no Ownership Map row

def source_list_owner(code, source):
    """The holder of a source list, from its Source cell and the Ownership Map."""
    if "v_ace_" in source:
        return "P1", "ACE read through the P1 contract, not loaded (DP-05)"
    best = None
    for t in table_owner:
        if re.search(r"\b" + re.escape(t) + r"\b", source) and (best is None or len(t) > len(best)):
            best = t
    if best:
        o = table_owner[best]
        return o, ROUTE[o]
    if code == "LOV-MATCH-TYPE":
        return "P7", ROUTE["P7"]
    return "P3", ROUTE["P3"]

items = []
for code, kind, values, business_owner, used, source in lists:
    refs = [x.strip() for x in re.sub(r"\([^)]*\)", "", used).split(",") if x.strip()]
    tables, views, nofield, unknown = [], [], [], []
    for ref in refs:
        if ref.startswith(NO_FIELD_PREFIXES):
            nofield.append(ref)
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\.", ref)
        if not m:
            unknown.append(ref)
            continue
        t = m.group(1)
        if t.startswith("v_ace"):
            views.append(t)
        elif t in table_owner:
            tables.append(t)
        else:
            unknown.append(t)
    tables, views = sorted(set(tables)), sorted(set(views))
    consumers = sorted({table_owner[t] for t in tables})
    if views:
        consumers = sorted(set(consumers) | {"P1"})
    consumers = list(consumers)

    if kind == "Closed list":
        owner = "P3"
        route = ROUTE["P3"]
        basis = ("Lists sheet row; lov_value is a P3 table of rwb_case "
                 "(Ownership Map sheet Tables; ASM-A6-tables-5)")
        if source.startswith("v_ace"):
            basis += ("; the codes are confirmed by %s on each release"
                      % source.split()[0])
        if nofield:
            basis += "; no live field after D-RCV-35, the list is kept with its values"
    else:
        owner, route = source_list_owner(code, source)
        if owner == "P1":
            basis = ("Lists sheet Source column; the values are ACE data read through the "
                     "recovery.v_ace_* views (Ownership Map sheet Rulings; DP-05)")
        elif code == "LOV-MATCH-TYPE":
            basis = ("Lists sheet row; payment_match_rule has no Ownership Map row and is dropped in "
                     "the target (ADR-012), so the codes travel with the PAYMENT_MATCH package of "
                     "rwb-decision")
        else:
            tbl = [t for t in table_owner if re.search(r"\b" + re.escape(t) + r"\b", source)]
            tbl = max(tbl, key=len) if tbl else ""
            if owner == "P3" and tbl == "parameter_catalog":
                route = "rwb-case parameters contract RWB-P3-E1042-CON (DP-06)"
            elif owner == "P3" and tbl == "queue":
                route = "rwb-case queue resource (DP-13); the queue rows are reference rows of rwb_case"
            art = "an" if owner.startswith("S") else "a"
            basis = ("Lists sheet Source column; %s is %s %s table "
                     "(Ownership Map sheet Tables)" % (tbl, art, owner))

    # LOV-MATCH-TYPE: payment_match_rule is not an Ownership Map table (ADR-012 drops it)
    if "payment_match_rule" in unknown:
        unknown.remove("payment_match_rule")
        if owner == "P3":
            owner, route = "P7", ROUTE["P7"]
        if "P8" not in consumers:
            consumers.append("P8")
        ASSUMED[code] = "payment_match_rule has no Ownership Map row; P8 rwb-payment and P7 assumed"
    if unknown:
        raise SystemExit("unresolved reference in %s: %s" % (code, unknown))

    items.append(dict(code=code, kind=kind, values=values, business_owner=business_owner,
                      used=used, source=source, owner=owner, schema=service_schema[owner],
                      route=route, basis=basis, consumers=sorted(consumers),
                      tables=tables, views=views, nofield=bool(nofield)))

TABLE_OF_REF = {
    "Routing rules": ("rule_row", "P7"),
    "Allocation table": ("rule_row", "P7"),
    "Delegation of authority": ("delegation_limit", "P4"),
    "Roles": ("role", "P4"),
    "Permission matrix": ("permission", "P4"),
    "Queues": ("queue", "P3"),
    "Service levels and timers": ("timer; reference_row", "P3"),
    "Letter and notice templates": ("template", "P6"),
    "Messages": ("reference_row", "P3"),
    "Document types": ("document_type", "P5"),
    "Retention classes": ("retention_rule", "P5"),
    "Masking rules": ("masking_rule", "P4"),
    "Partner panel": ("partner", "S9"),
    "Feature flags": ("feature_flag; feature_flag_change", "PLT"),
}
refs = []
for r in wb["Reference tables"].iter_rows(min_row=5, values_only=True):
    if not r or not r[0]:
        continue
    name = str(r[0]).strip()
    tbl, owner = TABLE_OF_REF[name]
    refs.append(dict(item=name, table=tbl, owner=owner, schema=service_schema[owner],
                     route=ROUTE[owner],
                     basis=("Reference tables sheet row; %s is %s %s table "
                            "(Ownership Map sheet Tables)"
                            % (tbl.split(";")[0].strip(),
                               "an" if owner.startswith("S") else "a", owner)),
                     holds=str(r[2]).strip(), business_owner=str(r[3]).strip(),
                     specified=str(r[4]).strip() if r[4] else ""))

ORDER = ["P%d" % i for i in range(1, 11)] + ["S%d" % i for i in range(1, 10)] + ["PLT"]
starter = []
for it in items:
    if it["nofield"] or not it["consumers"]:
        continue
    for c in it["consumers"]:
        mode = "Read" if it["owner"] == "P1" else "Load"
        starter.append(dict(service=c, item=it["code"], kind=it["kind"], mode=mode,
                            route=it["route"], wave=service_wave[c], owner=it["owner"],
                            basis=("Lists sheet row %s, 'Used by' %s; Ownership Map sheet Tables"
                                   % (it["code"], it["tables"][0] if it["tables"]
                                      else (it["views"][0] if it["views"] else it["used"])))))
for rf in refs:
    starter.append(dict(service=rf["owner"], item=rf["item"], kind="Reference table",
                        mode="Load", route=rf["route"], wave=service_wave[rf["owner"]],
                        owner=rf["owner"], basis="Reference tables sheet row; Ownership Map sheet Tables"))
starter.sort(key=lambda r: (ORDER.index(r["service"]), r["item"] in [x["code"] for x in items],
                            r["item"]))

json.dump(dict(items=items, refs=refs, starter=starter, assumed=ASSUMED,
               service_name=service_name, service_wave=service_wave,
               service_schema=service_schema), open(OUT, "w", encoding="utf-8"), indent=1)

print("lists", len(items), "refs", len(refs), "starter rows", len(starter))
print("owners", Counter(i["owner"] for i in items))
print("routes", Counter(i["route"] for i in items))
print("no consumer", [i["code"] for i in items if not i["consumers"]])
print("starter per service", Counter(r["service"] for r in starter))
print("modes", Counter(r["mode"] for r in starter))
print("assumed", ASSUMED)
