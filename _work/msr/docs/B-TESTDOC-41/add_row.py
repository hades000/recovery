import json
from pathlib import Path

WP = "B-TESTDOC-41"
SRC = "09 Testing and quality/Recovery Workbench Test Data Plan v3.docx"

gap9 = dict(
    id=f"CG-{WP}-9",
    title="The map gives six tables to the platform library but does not say which schema holds them",
    source="22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx",
    section="2. What the sandbox seeds; 2.1 Rows per schema (row PLT)",
    description="Sheet Tables assigns six tables to PLT: outbox_event, outbox_delivery, processed_event, idempotency_key, feature_flag and feature_flag_change. PLT is not one of the 19 services and owns no schema, so the test data plan cannot seed them from a service row. Architecture v5 slide 20 puts the outbox and inbox in every service schema and says nothing about the two feature-flag tables.",
    evidence="Ownership Map v1 sheet Tables: six rows with owner PLT. Sheet Services: 19 services, none of them PLT. Architecture v5 slide 20: DB own schema: business tables + outbox + inbox + decision_record.",
    type="Ambiguous",
    area="Data",
    severity="P3",
    needed_by_wave=0,
    legacy_ref="",
    owner_role="TechX",
    asm=f"ASM-{WP}-11",
    proposed="Create the four outbox, inbox and idempotency objects in all 19 schemas, as DP-09 requires, and keep feature_flag and feature_flag_change once, in rwb_integration, which serves the feature-flag admin API; the seed treats the four as per-schema tables.",
    wp=WP,
)

asm11 = dict(
    id=f"ASM-{WP}-11",
    text="The four platform library objects outbox_event, outbox_delivery, processed_event and idempotency_key exist in all 19 schemas and are seeded per schema; feature_flag and feature_flag_change exist once, in rwb_integration.",
    why="The map owns the six tables as PLT and PLT has no schema, while DP-09 and Architecture v5 slide 20 make the outbox and inbox part of every service schema. A test needs an outbox row in the schema that publishes the event.",
    read="Ownership Map v1 sheet Tables and sheet Services; Architecture v5 slide 20; Template and Rules v1 R5.5 DP-09.",
    gap=f"CG-{WP}-9",
    applied_in="Section 2, Platform library objects row; section 2.1, row PLT; section 6, Platform library objects row.",
    confidence="Medium",
    confirm="TechX",
    impact="If the library ships as a shared schema or a library, the seed row per schema and the two count rows change; no service row does.",
    wp=WP,
)

gp = Path(f"_work/msr/gaps/{WP}.jsonl")
ap = Path(f"_work/msr/assumptions/{WP}.jsonl")
gaps = [json.loads(l) for l in gp.read_text(encoding="utf-8").splitlines() if l.strip()]
asm = [json.loads(l) for l in ap.read_text(encoding="utf-8").splitlines() if l.strip()]
if gap9["id"] not in [g["id"] for g in gaps]:
    gaps.append(gap9)
if asm11["id"] not in [a["id"] for a in asm]:
    asm.append(asm11)
gp.write_text("".join(json.dumps(g, ensure_ascii=False) + "\n" for g in gaps), encoding="utf-8")
ap.write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a in asm), encoding="utf-8")
print("gaps", len(gaps), [g["id"] for g in gaps])
print("asm", len(asm), [a["id"] for a in asm])
