import re
sql = open("Recovery Workbench ACE Source Views v1.sql", encoding="utf-8").read()
# split per view
parts = re.split(r"CREATE OR REPLACE VIEW recovery\.(v_ace_\w+)", sql)
views = {}
for i in range(1, len(parts), 2):
    name = parts[i]; body = parts[i+1]
    # body until next CREATE or grant
    m = re.search(r"\n\s*AS\s*\n(.*?)(?:\n\s*;)", body, re.S)
    seg = m.group(1) if m else body
    cols = re.findall(r"^\s*(?:public\.)?\w+\.(\w+)\s+AS\s+(\w+)", seg, re.M)
    views[name] = [b for a,b in cols]
for name in ["v_ace_asset","v_ace_score","v_ace_valuation","v_ace_account"]:
    print(name, views.get(name))
