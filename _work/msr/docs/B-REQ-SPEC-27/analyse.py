"""B-REQ-SPEC-27 analysis: per-module objects named in each FSD and their owner per Ownership Map v1."""
import glob, json, os, re

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, r"03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v6")
JSON_PATH = os.path.join(ROOT, r"_work\msr\plan\ownership.json")

own = json.load(open(JSON_PATH, encoding="utf-8"))
tables = own["tables"]
api = own["api"]
events = own["events"]
jobs = own["jobs"]
wfs = own["workflows"]

SERVICES = {
    "P1": ("rwb-source-data", "Source data", "rwb_source_data", "/api/recovery/source-data/v1", "rwb.source-data.events.v1", "rwb-source-data", "sourcedata", 1),
    "P2": ("rwb-integration", "Integration", "rwb_integration", "/api/recovery/integration/v1", "rwb.integration.events.v1", "rwb-integration", "integration", 1),
    "P3": ("rwb-case", "Case and workflow", "rwb_case", "/api/recovery/case/v1", "rwb.case.events.v1", "rwb-case", "case", 1),
    "P4": ("rwb-access", "Access and authority", "rwb_access", "/api/recovery/access/v1", "rwb.access.events.v1", "rwb-access", "access", 1),
    "P5": ("rwb-document", "Document", "rwb_document", "/api/recovery/document/v1", "rwb.document.events.v1", "rwb-document", "document", 1),
    "P6": ("rwb-comms", "Communications", "rwb_comms", "/api/recovery/comms/v1", "rwb.comms.events.v1", "rwb-comms", "comms", 1),
    "P7": ("rwb-decision", "Decision and rules", "rwb_decision", "/api/recovery/decision/v1", "rwb.decision.events.v1", "rwb-decision", "decision", 1),
    "P8": ("rwb-payment", "Payment", "rwb_payment", "/api/recovery/payment/v1", "rwb.payment.events.v1", "rwb-payment", "payment", 2),
    "P9": ("rwb-reporting", "Reporting", "rwb_reporting", "/api/recovery/reporting/v1", "rwb.reporting.events.v1", "rwb-reporting", "reporting", 1),
    "P10": ("rwb-agent", "Agent", "rwb_agent", "/api/recovery/agent/v1", "rwb.agent.events.v1", "rwb-agent", "agent", 1),
    "S1": ("rwb-valuation", "Valuation and route", "rwb_valuation", "/api/recovery/valuation/v1", "rwb.valuation.events.v1", "rwb-valuation", "valuation", 3),
    "S2": ("rwb-treatment", "Treatment and offer", "rwb_treatment", "/api/recovery/treatment/v1", "rwb.treatment.events.v1", "rwb-treatment", "treatment", 2),
    "S3": ("rwb-guarantee", "Guarantee", "rwb_guarantee", "/api/recovery/guarantee/v1", "rwb.guarantee.events.v1", "rwb-guarantee", "guarantee", 3),
    "S4": ("rwb-litigation", "Litigation", "rwb_litigation", "/api/recovery/litigation/v1", "rwb.litigation.events.v1", "rwb-litigation", "litigation", 3),
    "S5": ("rwb-asset", "Asset", "rwb_asset", "/api/recovery/asset/v1", "rwb.asset.events.v1", "rwb-asset", "asset", 2),
    "S6": ("rwb-debtsale", "Debt sale", "rwb_debtsale", "/api/recovery/debtsale/v1", "rwb.debtsale.events.v1", "rwb-debtsale", "debtsale", 3),
    "S7": ("rwb-writeoff", "Write-off", "rwb_writeoff", "/api/recovery/writeoff/v1", "rwb.writeoff.events.v1", "rwb-writeoff", "writeoff", 4),
    "S8": ("rwb-deviation", "Deviation", "rwb_deviation", "/api/recovery/deviation/v1", "rwb.deviation.events.v1", "rwb-deviation", "deviation", 2),
    "S9": ("rwb-partner", "Partner", "rwb_partner", "/api/recovery/partner/v1", "rwb.partner.events.v1", "rwb-partner", "partner", 4),
}

DP = [
    ("DP-01", [r"recovery\.[a-z_]+", r"recovery schema"]),
    ("DP-02", [r"recovery_svc"]),
    ("DP-03", [r"(?i)decision ?log"]),
    ("DP-04", [r"(?i)rulerevaluator", r"(?i)drools"]),
    ("DP-05", [r"AceSourceQuery", r"v_ace_", r"account_ext"]),
    ("DP-06", [r"(?i)parameters?\b", r"casewf\.config"]),
    ("DP-07", [r"(?i)reference data", r"\bLOV-"]),
    ("DP-08", [r"RecoveryAccessGuard"]),
    ("DP-09", [r"\bEV-\d\d\b", r"(?i)\boutbox\b"]),
    ("DP-10", [r"(?i)quartz", r"\bJOB-\d\d\b"]),
    ("DP-11", [r"(?i)published interface"]),
    ("DP-12", [r"(?i)one workflow per case", r"CaseWorkflow"]),
    ("DP-13", [r"/api/recovery/v1"]),
    ("DP-14", [r"rwb\.p\d+\.", r"rwb\.casewf\."]),
    ("DP-15", [r"V0001", r"(?i)flyway", r"(?i)migration"]),
    ("DP-16", [r"recovery\.integration\.adapter"]),
    ("DP-17", [r"(?i)data lake", r"INT-19", r"INT-20"]),
    ("DP-18", [r"(?i)interaction ledger"]),
    ("DP-19", [r"(?i)ace-web", r"(?i)\bscreens?\b"]),
    ("DP-20", [r"(?i)agent client"]),
]


def main():
    out = []
    for p in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(p)
        t = open(p, encoding="utf-8").read()
        code = re.search(r"FSD (P\d+|S\d+)", name).group(1)
        # tables: backticked or bare table names
        tbl = sorted({k for k in tables if re.search(r"(?<![\w.])" + re.escape(k) + r"(?![\w])", t)})
        eps = sorted({k for k in api if k in t})
        evs = sorted({k for k in events if re.search(r"\b" + k + r"\b", t)})
        jbs = sorted({k for k in jobs if re.search(r"\b" + re.escape(k) + r"\b", t)})
        wfl = sorted({k for k in wfs if re.search(r"\b" + re.escape(k) + r"\b", t)})
        dps = [d for d, pats in DP if any(re.search(x, t) for x in pats)]
        other = {}
        for kind, items in (("table", tbl), ("endpoint", eps), ("event", evs), ("job", jbs), ("workflow", wfl)):
            for i in items:
                o = (tables[i]["owner"] if kind == "table" else api[i]["owner"] if kind == "endpoint"
                     else events[i]["owner"] if kind == "event" else jobs[i]["owner"] if kind == "job" else wfs[i]["owner"])
                if o != code:
                    other.setdefault(o, []).append(f"{kind} {i}")
        out.append(dict(file=name, code=code, own_tables=[x for x in tbl if tables[x]["owner"] == code],
                        own_eps=[x for x in eps if api[x]["owner"] == code],
                        own_events=[x for x in evs if events[x]["owner"] == code],
                        own_jobs=[x for x in jbs if jobs[x]["owner"] == code],
                        own_wf=[x for x in wfl if wfs[x]["owner"] == code],
                        others=other, dp=dps,
                        mentions_case_schema=bool(re.search(r"recovery\.[a-z_]+", t))))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(len(out), "modules analysed")


if __name__ == "__main__":
    main()
