import json
own = json.load(open("_work/msr/plan/ownership.json", encoding="utf-8"))
tables = own["tables"]
print("count tables", len(tables))
keys = sorted(tables)
print(keys)
print("RULINGS:", json.dumps(own.get("rulings"), indent=1)[:4000])
for probe in ["party", "contact", "loan", "payment", "collateral", "valuation", "asset", "score", "collections", "product"]:
    print("--", probe, [k for k in keys if probe in k])
