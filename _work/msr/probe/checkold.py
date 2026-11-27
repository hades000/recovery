from pathlib import Path
t = Path(r'_work/msr/directive/mp/out/RWB-ITG-E4045-ITG.md').read_text(encoding='utf-8')
olds = [
    "  Scenario: AC3 Access check (covers exception X11)",
    "| Depends on (build) | None (RWB-P8-E4045-APP is an integration dependency only; the Day-1 run uses the rwb-payment stub in section 12.8) |",
    "Reference data: the harness reads the fee tables and the court fee and charge schedules as reference data through the owning contracts (DP-06, DP-07). The parameter names and keys are not specified in the source documents (DOR-RWB-ITG-E4045-ITG-20).",
    "3. Harness: reads the payment row from `v_ace_payment` through `GET /api/recovery/source-data/v1/data-products/{productCode}/records` and asserts `payment_code`, the amount, the account and the payment date the run was seeded with (DP-05, REQ-CHO-009). The product code is not specified in the source documents (GAP-0431; ASM-0607).",
    "| TC-E4-045-02-ITG | BR7 (negative path only; AC2 run by RWB-P8-E4045-APP) | Integration | Decision log forced to fail; MSG-P7-003 |",
    "SCR-28 Proceeds matching is the screen the legacy key names for this behaviour:",
]
for o in olds:
    print(t.count(o), repr(o[:80]))
