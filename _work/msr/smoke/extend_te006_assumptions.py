"""Extend two TE006 assumption texts so every citation in the stories resolves to the default it uses."""
import json
from pathlib import Path

WORK = Path(__file__).resolve().parents[3] / "_work" / "msr" / "assumptions"
p = WORK / "B-PLT-LIB-02.jsonl"
rows = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
by_id = {r["id"]: r for r in rows}
by_id["ASM-B-PLT-LIB-02-TE006-2"]["text"] += " Each service's own database story applies its copy of the four tables in its own schema."
by_id["ASM-B-PLT-LIB-02-TE006-4"]["text"] += " The column set of processed_event and idempotency_key is the working read of that template until a field list is published; outbox_event and outbox_delivery keep the legacy fields DF-OPS-189 to DF-OPS-206."
p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
print("updated", len(rows), "assumption rows")
