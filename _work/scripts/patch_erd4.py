import os
p = os.path.join(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14", r"_work\scripts\build_erd_v4.py")
s = open(p, encoding="utf-8").read()
old = """        rels.append({"child": child, "col": "person_key" if child == "party_ext" else
                     "contact_key" if child == "contact_point_ext" else
                     "account_key" if child == "account_ext" else "valuation_key",
                     "parent": r[1], "mand": True, "logical": True, "card": r[3],
                     "kind": "Business key, no foreign key (1:1 extension)"})"""
new = """        card = {"Many to one": "N:1", "Many to zero or one": "N:0..1", "One to one": "1:1"}.get(r[2], r[2])
        rels.append({"child": child, "col": "person_key" if child == "party_ext" else
                     "contact_key" if child == "contact_point_ext" else
                     "account_key" if child == "account_ext" else "valuation_key",
                     "parent": r[1], "mand": True, "logical": True, "card": card,
                     "kind": "Business key, no foreign key (1:1 extension)"})"""
assert old in s
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
