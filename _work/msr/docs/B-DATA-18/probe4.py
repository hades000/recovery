import json, collections
d = json.load(open("_work/msr/docs/B-DATA-18/v4_dump.json", encoding="utf-8"))
m = d["Mapping"]
hdr = m[0]
idx = {h: i for i, h in enumerate(hdr)}
stat = collections.Counter(r[idx["Status"]] for r in m[1:])
print("status counts:", stat)
ifs = [r[0] for r in m[1:] if "Interface Specifications v3" in r[idx["Interface"]]]
print("interface v3 rows:", len(ifs), ifs)
ext = [(r[0], r[2], r[8]) for r in m[1:] if "_ext" in str(r[8])]
print("ext rows:", ext)
sw = [r[0] for r in m[1:] if "RWB-ACE-001" in str(r[idx["Status"]])]
print("waiting rows:", len(sw))
src = collections.Counter(r[idx["Source system (ACE ingests it)"]] for r in m[1:])
print("source dist:", src)
# entities per target
ents = collections.Counter((r[2]) for r in m[1:])
print("entities:", len(ents))
print("data product dist:", collections.Counter(r[1] for r in m[1:]))
