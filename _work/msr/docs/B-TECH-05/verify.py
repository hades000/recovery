"""Verify the v5 text against the v4 source: tokens, counts, header and change-log row."""
import re, sys
from pathlib import Path
src = Path("_work/msr/extract/B-TECH-05/Recovery Workbench Environment and Deployment Design v4.md").read_text(encoding="utf-8")
new = Path("_work/msr/docs/B-TECH-05/Recovery Workbench Environment and Deployment Design v5.md").read_text(encoding="utf-8")

TOKENS = ["RWB-E1-070", "RWB-ACE-001", "RWB-E1-069", "RWB-E1-073", "RWB-E2-039", "D-RCV-28", "D-RCV-35",
          "D-RCV-36", "V0001", "TE-001", "JOB-05", "DL03", "DL04", "DL05", "DL11", "DL27", "DL33", "DL34",
          "DL35", "DL37", "DL43", "21 November 2026", "2 November", "16 November 2026",
          "1.28.1", "1.31.0", "7233", "99.9%", "30 days", "16 Tier 1", "14 Tier 2", "50", "20",
          "case-{caseId}", "platform-smoke-{yyyymmdd}", "ace_batch_run", "v_ace_batch_status",
          "ace_view_owner", "recovery_svc", "temporal_svc", "TemporalSchemaJob", "rwb-temporal",
          "rwb.p3.temporal", "rwb.p3.drools", "rwb-platform", "rwb-case", "rwb-integration",
          "recovery.v_ace_*", "Section A", "Section B", "DEV", "SIT", "UAT", "PROD"]
miss = [t for t in TOKENS if t not in new]
print("missing source tokens:", miss if miss else "none")

head = "\n".join(new.splitlines()[:2])
ok_head = head == "SCB Collections and Recovery. Henka Group, 22 November 2026.\n(C) Siam Commercial Bank and Henka Pte Ltd"
print("header R8.1:", "PASS" if ok_head else "FAIL")
log = "5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
print("change-log row:", "PASS" if log in new else "FAIL")

# source headings kept
sh = re.findall(r"^# (.+)$", src, re.M)
nh = re.findall(r"^# (.+)$", new, re.M)
print("source headings:", sh)
print("headings missing from v5:", [h for h in sh if h not in nh] or "none")

# all cited candidate ids exist in 22.. and 23.. families written by this WP
cites = sorted(set(re.findall(r"\b(?:CG|ASM)-B-TECH-05-\d+\b", new)))
print("citations in v5:", cites)
print("services in table:", len(re.findall(r"^\| (?:P\d+|S\d+) \| rwb-", new, re.M)))
