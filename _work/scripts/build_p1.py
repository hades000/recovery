import re, io, os

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, r"05 Technical architecture\Recovery Workbench Technical Specifications by Module v3\Recovery Workbench TSD P1 Recovery data engine v2.md")
HEAD = os.path.join(ROOT, r"_work\staging\p1_head.md")
OUT = os.path.join(ROOT, r"_work\staging\Recovery Workbench TSD P1 Recovery data engine v2.md")

src = open(SRC, encoding="utf-8").read()
head = open(HEAD, encoding="utf-8").read()
tail = src[src.index("## T4. State machines and workflow"):]

def rep(old, new, s):
    assert old in s, "NOT FOUND: " + old[:80]
    return s.replace(old, new, 1)

# --- T5.1 ---
i = tail.index("### T5.1 External system interfaces")
j = tail.index("### T5.2 Cross-module interfaces")
new_t51 = """### T5.1 External system interfaces

P1 owns no inbound interface. Every inbound interface in Interface Specifications v3 is owned by ACE ingestion, and P1 reads the ACE database through the views in T3.1.1. A P1 job is triggered by an ACE batch-complete record, never by an inbound file.

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-01, INT-02, INT-04, INT-05, INT-06, INT-07, INT-08, INT-09, INT-10, INT-11, INT-12, INT-13, INT-15, INT-16 | Source systems | In, into ACE | ACE ingestion (ACE team). P1 reads the matching `v_ace_*` view and never the source | Per the source cycle in Interface Specifications v3 |
| None | ACE database | In | `recovery.v_ace_*` SELECT-only views, through `ace_view_owner` | As each ACE batch completes |
| INT-19 | Data lake and Power BI | Out | P1 builds the case list snapshot; P2 sends the file | Daily |

The freshness web service is the only P1 screen an operator uses: it shows the last complete ACE business date per selected source from `v_ace_batch_status`, and the STALE reason for each data product.

"""
tail = tail[:i] + new_t51 + tail[j:]

# --- T5.3 ---
i = tail.index("### T5.3 Events")
j = tail.index("## T6. Security and access control")
new_t53 = """### T5.3 Events

| Event | Direction |
|---|---|
| AceDataReady | Published: the ACE batch for a source completed and the data product is LOADED |
| AceDataLate | Published: the ACE batch is incomplete, late or failed and the data product is STALE |

`AceDataReady` replaces `LoadCompleted` and `AceDataLate` replaces `LoadRefused` from version 2. The named and numbered event catalogue is in Event and Messaging Design v3 (EV-26, EV-27).

"""
tail = tail[:i] + new_t53 + tail[j:]

# --- T7 rows ---
old = "| NFR-013 | The daily core system load completes before the working day starts, and a failure raises an alert. | Job runs by 07:00 | Proposed |"
new = "| NFR-013 | The daily ACE batch completes before the working day starts, and an incomplete, late or failed ACE batch raises an alert. | ACE batch complete by 07:00; the stamp written and AceDataLate raised within 5 minutes of the ACE completion record | Proposed, DL43 |"
tail = rep(old, new, tail)

old = "| NFR-014 | Collections data is ingested at start of day. | Start of day | Proposed |"
new = "| NFR-014 | Collections data is readable at start of day. | Start of day, from `v_ace_efs_action` | Proposed, DL43 |"
tail = rep(old, new, tail)

old = "| NFR-015 | The recovery data store is no more than the agreed lag behind its sources, and a decision that must be made the same day uses an event instead. | End of day; in the Workbench the next morning. Same-day needs are named under DL06 | Proposed |"
new = "| NFR-015 | The Workbench reads data no more than the agreed lag behind ACE, and a decision that must be made the same day uses an event instead. | Visible as soon as the ACE batch completes; no Workbench lag. Same-day needs are named under DL06 | Proposed, DL06, DL43 |"
tail = rep(old, new, tail)

old = "| NFR-018 | The case list reconciles to the core system count daily. | No unexplained variance; tolerance per data product under DL25 | Proposed, DL25 |"
new = "| NFR-018 | The case list reconciles to the ACE account view daily. | No unexplained variance; tolerance per data product under DL25 | Proposed, DL25, DL43 |"
tail = rep(old, new, tail)

# --- T8 add row ---
old = "| REQ-RDF-014 | None | Written one epic ahead | With the story |"
new = ("| REQ-RDF-014 | None | Written one epic ahead | With the story |\n"
       "| D-RCV-35 read path | None | RWB-E1-069 (views, grants and boundary rule); RWB-ACE-001 (ACE additions) | With the story |")
tail = rep(old, new, tail)

# --- T-A inventory ---
i = tail.index("| ID | Method | Path | Access | First in |")
i = tail.index("\n", i) + 1
j = tail.index("### T-A.2 Endpoint detail")
new_inv = """|---|---|---|---|---|
| API-P1-001 | GET | /api/recovery/v1/admin/jobs | Platform administration R | E1 |
| API-P1-002 | POST | /api/recovery/v1/admin/jobs/{jobId}/rerun | Platform administration U | E1 |
| API-P1-003 | - | Retired in v3 | - | - |
| API-P1-004 | - | Retired in v3 | - | - |
| API-P1-005 | - | Retired in v3 | - | - |
| API-P1-006 | - | Retired in v3 | - | - |
| API-P1-007 | - | Retired in v3 | - | - |
| API-P1-008 | - | Retired in v3 | - | - |
| API-P1-009 | GET | /api/recovery/v1/data-products/freshness | Case record R | E1 |
| API-P1-010 | GET | /api/recovery/v1/data-products/{productCode}/records | Case record R | E1 |
| API-P1-011 | GET | /api/recovery/v1/admin/data-products | Platform administration R | E1 |
| API-P1-012 | GET | /api/recovery/v1/admin/data-dictionary/fields | Reference data R | E1 |
| API-P1-013 | PATCH | /api/recovery/v1/admin/data-dictionary/fields/{fieldCode} | Reference data U | E1 |
| API-P1-014 | GET | /api/recovery/v1/admin/data-contracts | Reference data R | E1 |
| API-P1-015 | PATCH | /api/recovery/v1/admin/data-contracts/{contractId} | Reference data U | E1 |
| API-P1-016 | POST | /api/recovery/v1/admin/data-contracts/{contractId}/publish | Reference data U | E1 |

API-P1-003 to API-P1-008 are retired by D-RCV-35: there is no load run to list, no data quality exception to clear and no tracker to list, load, sign off, retire or report. Their identifiers are not reused.

"""
tail = tail[:i] + new_inv + tail[j:]

# --- T-A.2: replace 001/002 purposes, remove 003-008 details ---
old = "| Purpose | List loads, files and jobs with status |"
new = "| Purpose | List jobs with status, owner and last run; the ACE ingestion runs are ACE's and are not listed |"
tail = rep(old, new, tail)
old = "| Purpose | Rerun a failed load or job |"
new = "| Purpose | Rerun a failed Workbench job; an ACE ingestion failure is raised with the ACE team, not rerun here |"
tail = rep(old, new, tail)

i = tail.index("#### API-P1-003 GET /admin/data-quality/exceptions")
j = tail.index("#### API-P1-009 GET /data-products/freshness")
retire = """#### API-P1-003 to API-P1-008 (retired)

Version 2 listed data quality exceptions and ran the tracker inventory: list, load a tracker file, sign off its row count, retire it and report the retirement. D-RCV-35 removes the tables, the load and the tracker estate from Workbench scope, so the six endpoints are retired. Data quality is checked by ACE ingestion and by reconciliation rules REC-01 to REC-09; tracker retirement is a Cutover plan procedure (U5).

"""
tail = tail[:i] + retire + tail[j:]

# --- API-P1-010 purpose ---
old = "| Purpose | Read the rows of one data product for a case, masked by role, with its freshness stamp |"
new = "| Purpose | Read the rows of one data product for a case from its Workbench tables or its `v_ace_*` view, masked by role, with its freshness stamp |"
tail = rep(old, new, tail)

# --- T-B ---
old = """| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |"""
new = """| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data. Option A (daily batch through COLLINS) is superseded by D-RCV-35 |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |
| DL43 | ACE team acceptance of the RWB-ACE-001 scope and dates. Blocks the 14 Section B views, the 12 Section B columns and the freshness go-live |"""
tail = rep(old, new, tail)

out = head + "\n" + tail
open(OUT, "w", encoding="utf-8", newline="\n").write(out)
print("written", len(out), "chars")
nonascii = sorted({c for c in out if ord(c) > 127})
print("non-ascii:", nonascii)
