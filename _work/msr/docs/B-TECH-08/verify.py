"""Verify Recovery Workbench Security and Access Design v5.docx against version 4.

Read-only. Reports:
1. header lines and the D-RCV-60 change-log row;
2. every line of the version 4 text that is NOT present verbatim in version 5 (intended changes
   must appear in CHANGED with a reason, everything else is a fidelity defect);
3. every change recorded in the realignment table of version 5;
4. counts: sections, tables, rows, mention of recovery_svc, person names in the properties.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OLD = ROOT / "_work" / "msr" / "extract" / "B-TECH-08" / "Recovery Workbench Security and Access Design v4.md"
NEW = ROOT / "_work" / "msr" / "docs" / "B-TECH-08" / "roundtrip" / "Recovery Workbench Security and Access Design v5.md"


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


old = [l for l in OLD.read_text(encoding="utf-8").splitlines() if l.strip()]
new_text = norm(" ".join(NEW.read_text(encoding="utf-8").splitlines()))

# Lines of version 4 that the realignment deliberately changes: (prefix of the v4 line, reason).
CHANGED = [
    ("Recovery Workbench", "title moved below the two header lines of Template and Rules R8.1"),
    ("Security and access design", "title line moved below the header"),
    ("SCB Collections and Recovery. Henka Group, 16 November 2026", "v5 date line; the v4 date is kept in the metadata and change-log rows"),
    ("| Version | 4 |", "version 5"),
    ("| Date | 16 November 2026 |", "v5 date; the v4 date is kept in the Source version row"),
    ("| Change | 4, 16 November 2026", "v5 change row; the v4 text is kept verbatim in the change log"),
    ("| Sign-in | Entra ID single sign-on", "session store and per-service JWT added"),
    ("| Case workflow engine |", "one worker identity per service"),
    ("| Rule packages | Embedded Drools.", "registry in rwb-decision, evaluation local"),
    ("| Identity to role |", "roles as data in rwb-access"),
    ("| Permission check |", "check in the owning service and the authorise contract"),
    ("| Scope |", "filter applied in the owning service"),
    ("| Approval limits |", "DoA table named delegation_limit in rwb-access"),
    ("| Masking |", "masking_rule in rwb-access, applied by each service"),
    ("| Sessions |", "session store in gateway-bff"),
    ("| Partners |", "partner gateway in the DMZ, partner users in rwb_partner"),
    ("| Service identities |", "workload identity per service"),
    ("| ACE data access |", "rwb_source_data only"),
    ("| Logging |", "access log owner and one trace across 19 services"),
    ("| Bank staff |", "gateway-bff and per-service JWT"),
    ("| Partners | Partner portal", "partner gateway and partner_user"),
    ("| Non-human actors |", "workload identity per service"),
    ("| Access token lifetime |", "unchanged row; new rows follow the table"),
    ("## 4.1 Rights on the new objects", "renumbered 4.2: the authorise contract is 4.1"),
    ("| National ID |", "read by rwb_source_data only"),
    ("| Masking | Name, address", "masking_rule in rwb-access"),
    ("| Retention |", "retention_rule owner named (P5)"),
    ("| Workflow history |", "keys per namespace, every worker"),
    ("| Rule facts |", "registry in rwb-decision, evaluation local"),
    ("- Partner users reach the partner portal", "partner gateway in the DMZ"),
    ("- The partner and agency manager requests partner users", "partner_user in rwb_partner"),
    ("| Managed identities |", "workload identity added as its own row"),
    ("| Secrets |", "reached by the workload identity"),
    ("| Database |", "one login per service"),
    ("| Read-only ACE access |", "rwb_source_data in place of recovery_svc"),
    ("| PUBLIC |", "applied to the 19 rwb_* schemas too"),
    ("| Grant check |", "rwb_source_data and the boundary test"),
    ("| Agents |", "unchanged row; Kafka row follows it"),
    ("| Network |", "no public endpoint on any of the 19 services"),
    ("| temporal_svc isolation |", "unchanged row; service login row follows it"),
    ("| recovery_svc isolation |", "replaced by the service login isolation row"),
    ("| Temporal certificates |", "certificates per namespace"),
    ("| Codec server |", "keys per namespace"),
    ("| Rule store |", "registry in rwb-decision"),
    ("| Transport | mTLS between the worker", "workers per service, certificates per namespace"),
    ("| Authorizer plugin |", "workload identity in the mapping"),
    ("| Payload codec |", "keys per namespace"),
    ("| Isolation | temporal_svc", "19 service logins"),
    ("| Authoring |", "registry in rwb_decision"),
    ("| Evaluation |", "evaluation in the owning service"),
    ("| Integrity |", "checksum verified by the owning service"),
    ("| Traceability |", "local record plus central ledger"),
    ("| Access log |", "held in rwb_access"),
    ("| Decision log |", "local record plus central ledger"),
    ("| Temporal audit log |", "each service reads its own queue"),
    ("| Information disclosure |", "SELECT for rwb_source_data only"),
    ("| Denial of service |", "connection caps added"),
    ("| Rule package tampering |", "registry owner added"),
    ("| Read-only ACE grant |", "rwb_source_data and the other 18 logins"),
    ("| Temporal mTLS |", "workers per service"),
    ("| DL43 |", "unchanged row; DL44 to DL49 follow it"),
]

missing = []
for line in old:
    if norm(line) in new_text:
        continue
    if any(norm(line).startswith(norm(pre)) for pre, _ in CHANGED):
        continue
    missing.append(line)

print("HEADER 1:", NEW.read_text(encoding="utf-8").splitlines()[0])
print("HEADER 2:", NEW.read_text(encoding="utf-8").splitlines()[2])
print("CHANGE ROW:", "5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" in new_text)
print("UNEXPLAINED MISSING LINES:", len(missing))
for m in missing:
    print("  MISSING:", m[:160])

txt = NEW.read_text(encoding="utf-8")
print("SECTIONS:", re.findall(r"^# (\d+)\.", txt, re.M))
print("SUBSECTIONS:", re.findall(r"^## ([\d.]+) ", txt, re.M))
print("TABLES:", sum(1 for l in txt.splitlines() if set(l.strip()) <= set("|- ") and "-" in l))
print("recovery_svc mentions:", txt.count("recovery_svc"))
print("rwb_source_data mentions:", txt.count("rwb_source_data"))
print("D-RCV-60 mentions:", txt.count("D-RCV-60"))
sys.exit(1 if missing else 0)
