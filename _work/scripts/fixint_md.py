"""Interface Specifications v3.md: ACE field-map targets, INT-35/INT-36, INT-21 iam_group, supersedes line."""
import json, os, re
import fixint_common as c

rows = json.load(open(os.path.join(os.path.dirname(__file__), "fixint_rows.json"), encoding="utf-8"))
md = open(c.MD, encoding="utf-8").read()
orig = md


def sub1(old, new):
    global md
    assert md.count(old) == 1, (md.count(old), old[:80])
    md = md.replace(old, new)


# minor: supersedes line
sub1("| Decision | D-RCV-35 |\n\nThe Workbench loads",
     "| Decision | D-RCV-35 |\n| Supersedes | Recovery Workbench Interface Specifications v2 |\n\nThe Workbench loads")

# summary table
sub1("| INT-12 | AMIS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_npa_asset` and `v_ace_npa_sale` | Monthly |",
     "| INT-12 | AMIS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_asset`, `v_ace_npa_asset` and `v_ace_npa_sale` | Monthly |")
sub1("| INT-21 | Entra ID and the bank IAM | In | ACE team | ACE sign-in | At each sign-in |",
     "| INT-21 | Entra ID and the bank IAM | In | ACE team | ACE sign-in; group-to-role mapping read through `v_ace_iam_group` | At each sign-in |")
sub1("| INT-34 | ACE common module | Both | ACE team | Published module interface | Per request |\n",
     "| INT-34 | ACE common module | Both | ACE team | Published module interface | Per request |\n"
     "| INT-35 | NLEADS | In, into ACE | ACE team | ACE ingestion, read through `v_ace_credit_decision` | As decisions are made |\n"
     "| INT-36 | EasyApp | In, into ACE | ACE team | ACE ingestion, read through `v_ace_esign` | As signatures are requested |\n")

# INT-12 section
sub1("| Approach | ACE ingestion, read through `v_ace_npa_asset` and `v_ace_npa_sale` |\n| ACE object | `npa_asset` and `npa_sale` (new tables) |",
     "| Approach | ACE ingestion, read through `v_ace_asset`, `v_ace_npa_asset` and `v_ace_npa_sale` |\n| ACE object | `asset` for the asset key and type; `npa_asset` and `npa_sale` (new tables) |")

# INT-21 section
sub1("| Approach | ACE sign-in |\n| Trigger | Sign-in |",
     "| Approach | ACE sign-in; group-to-role mapping read through `v_ace_iam_group` |\n| ACE object | `iam_user`; `iam_group` (new table, RWB-ACE-001) |\n| Trigger | Sign-in |")
sub1("User identity and Entra ID group membership.\n",
     "User identity and Entra ID group membership. ACE holds the group-to-role mapping in `iam_group` (`entra_group`, `role_code`) and the Workbench reads it through `v_ace_iam_group.entra_group`.\n")

# New ACE interfaces -> INT-35 / INT-36
start = md.index("## New ACE interfaces")
end = md.index("## Checks ACE ingestion passes")
block = md[start:end]
block = block[block.index("### New ACE interface (number in Interface Specifications v3) NLEADS"):]
block = block.replace("### New ACE interface (number in Interface Specifications v3) NLEADS", "## INT-35 NLEADS")
block = block.replace("### New ACE interface (number in Interface Specifications v3) EasyApp", "---\n\n## INT-36 EasyApp")
block = block.replace("| Purpose | Credit approval result for a restructure plan |",
                      "| Purpose | Credit approval result for a restructure plan, new to ACE and raised in RWB-ACE-001. The officer's submission in NLEADS stays INT-26 |")
block = block.replace("| Purpose | E-signature reference and status for a restructure agreement |",
                      "| Purpose | E-signature reference and status for a restructure agreement, new to ACE and raised in RWB-ACE-001 |")
md = md[:start] + block + md[end:]
assert c.PLACEHOLDER not in md

# field maps
INTRO_IN = ("Table.column is the ACE column that holds the value: Tier 1 exists in ACE today, Tier 2 is added by the ACE team in RWB-ACE-001. "
            "Read path is the `recovery.v_ace_*` view column the Workbench reads. LDM field is the LDM v7 field ID; the mapping follows the LDM v7 ACE mapping sheet.")
INTRO = {
    "INT-14": "Outbound. Table.column is the Workbench (Tier 4) column the file is built from.",
    "INT-25": "Outbound. Table.column is the Workbench (Tier 4) column the file is built from; the outstanding balance is the snapshot of `v_ace_account.total_balance` at the cut-off date.",
    "INT-15": INTRO_IN + " The notice itself stays in the Workbench; the proof of delivery is held in `pod_receipt`.",
    "INT-16": INTRO_IN + " The write-off decision stays in the Workbench; the posting is held in `gl_write_off`.",
}


def table(iface):
    out = ["| Source field | Table.column | Tier | Read path | LDM field | Type | Mandatory | Transformation |",
           "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r[0] == iface:
            _, src, tc, tier, rp, fid, dt, pt, mand, trans, owner = r
            rp_md = rp if rp.startswith(("Workbench", "Snapshot")) else f"`{rp}`"
            out.append(f"| {src} | `{tc}` | {tier} | {rp_md} | {fid} | {pt} | {mand} | {trans} |")
    return "\n".join(out) + "\n"


pat = re.compile(r"\*\*Field mapping\*\*\n\n(?:[^|\n][^\n]*\n\n)?(?:\|[^\n]*\n)+")
parts = re.split(r"(?m)^(## .*)$", md)
done = set()
for i in range(1, len(parts), 2):
    m = re.match(r"## (INT-\d\d)", parts[i])
    if not m:
        continue
    iface = m.group(1)
    if "**Field mapping**" in parts[i + 1]:
        new = f"**Field mapping**\n\n{INTRO.get(iface, INTRO_IN)}\n\n{table(iface)}"
        parts[i + 1], n = pat.subn(lambda _m: new, parts[i + 1])
        assert n == 1, iface
        done.add(iface)
md = "".join(parts)
need = {r[0] for r in rows}
assert done == need, (done ^ need)
open(c.MD, "w", encoding="utf-8", newline="\n").write(md)
print("md updated; field-map sections:", sorted(done))
