# Edit log — WP B-ARCH-EVT (Event and Messaging v-next and Kafka Topic and Event Catalog v1)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- 05 Technical architecture/Recovery Workbench Event and Messaging Design v5.xlsx
- 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx
- _work/msr/gaps/B-ARCH-EVT.jsonl
- _work/msr/assumptions/B-ARCH-EVT.jsonl
- _work/msr/editlog/B-ARCH-EVT.md

Scratch files under `_work/msr/docs/B-ARCH-EVT/` (build and verification only, not an output of the run):
`build.py` (writes both workbooks) and `verify.py` (source-diff, counts, citation check).

## What was done

**Event and Messaging Design v5.xlsx.** The source `Recovery Workbench Event and Messaging Design v4.xlsx`
was never edited. It was copied to v5 with `compat/office_write.py copy`, and only the copy was changed:

1. **Read me sheet added first.** Rows 1 and 2 are the header of Template and Rules §R8.1. Row 10 is the
   change-log row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`;
   row 11 records the source version. Rows 14 to 20 list what the version holds, then counts, then sources.
2. **The source sheets are untouched.** `Events` (34 rows) and `Rules` (14 rows) are identical cell for cell to v4,
   verified against the source (`verify.py`: 0 differences). Every v4 ID, number, date, payload
   word and rule is therefore kept exactly; the version stamp of the v4 table (Version 4, 16 November 2026,
   D-RCV-36) stays with the table it belongs to and the v5 stamp is in the Read me.
3. **Events v5 (new sheet, 45 rows).** The target register. The 30 v4 entries keep their ID, payload words and
   meaning; each gains the event type name `rwb.<short>.<Event>.v1`, its owner code and owner service from the
   Ownership Map, its one topic and the consumer services of Arch v5 slides 42 and 43. Fifteen event types that
   exist only in the Arch v5 service catalogue follow, unnumbered. Totals: 43 event types on 20 topics —
   28 from v4 (EV-18 is retired and EV-29 is a signal, so 30 entries give 28 topic events) and 15 new.
4. **Topics (20 rows), Dead-letter topics (20 rows).** 19 service topics `rwb.<short>.events.v1` plus
   `rwb.decision-record.v1`, with owner, wave, 12 partitions, replication factor 3, 7-day retention, key
   caseId, the events carried and the consumers. The shared topic has no settings in any source and carries the
   §R9 placeholder. Dead-letter topics are named by the `.dlt` suffix the source gives.
5. **Envelope, Outbox and inbox.** CloudEvents 1.0 binary mode: ce_id, ce_type, ce_source, ce_subject,
   traceparent, JSON body, key caseId, idempotency key = ce_id; and the four library objects outbox_event,
   outbox_delivery, processed_event and idempotency_key with the relay JOB-11 every minute.
6. **Rules v5 additions (12 rows).** The Kafka rules the target adds or changes; the ten v4 rules stay where
   they are. The v4 exception queue is read as the retry ladder plus the dead-letter topic.
7. **Realignment changes (16 rows).** One row per change with the v4 value, the v5 value, the basis in source
   precedence (R-PREC) and the gap or assumption that carries it.

**Kafka Topic and Event Catalog v1.xlsx.** A new workbook with 11 sheets: Read me, Topics, Retry topics,
Dead-letter topics, Events (45 rows), Not on Kafka, Envelope, Outbox and inbox, ACLs (19 services plus
gateway-bff, write and read lists derived from the producer and consumer columns), Delivery rules,
Traceability. The set is 100 topics: 20 event topics, 60 retry topics and 20 dead-letter topics, the count the
platform story RWB-PLT-N002-INF fixes.

**Owners.** Every owner of a service, topic, event, table and job is taken from the Microservice Ownership Map v1
and `_work/msr/plan/ownership.json`; no owner is written from the story masters where the Map differs. The three
disagreements between v4 and Arch v5 on direction and owner (EV-18, EV-21, EV-26) are resolved in favour of
Arch v5 and each is a gap row and an assumption row.

**Never edited, never invented.** No source file was changed; `05 Technical architecture/Recovery Workbench
Event and Messaging Design v4.xlsx` still hashes as it did. Where a source is silent the §R9 placeholder is
written and the CG/ASM rows carry it: retry topic names, dead-letter settings, the shared topic settings, the
payload of the 15 catalogue-only event types, the consumers of three event types, the registry subject naming,
the ce_source and ce_subject values, and the derivation of the idempotency key. No release date appears in
either document, so no `(tentative)` mark was needed.

## Registers

- Gap rows written: 12 candidate rows (`GAP-0120` to `GAP-0131`) in `_work/msr/gaps/B-ARCH-EVT.jsonl`.
- Assumption rows written: 14 candidate rows (`ASM-0196` to `ASM-0209`) in
  `_work/msr/assumptions/B-ARCH-EVT.jsonl`.
- Every one of the 26 rows is cited in one of the two workbooks and every citation in the workbooks resolves to
  a row (checked by `verify.py`).
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ARCH-EVT --quick` — C02, C03, C05, C12, C13
and C18 all PASS, 0 findings. Run twice, second run identical.

## Not done, by design

- No ADR, story, requirement, catalogue or register master file was touched; this work package writes the two
  event and topic documents only.
- No issue tracker, wiki, repository, Figma or web call was made; no commit was created.
- No schema registry subject and no JSON Schema was written, because no source names one; the two documents
  record the gap and the owning story.
- The retry and dead-letter topic names are left to RWB-PLT-N002-INF; this work package records the count, the
  windows and the derived `.dlt` suffix only.
