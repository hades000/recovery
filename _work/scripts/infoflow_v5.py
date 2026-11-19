# Build Information Flow v5.pptx from v4 by replacing text runs only.
import zipfile, re, sys
from xml.sax.saxutils import escape
from xml.dom import minidom

ROOT = "C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14/05 Technical architecture/"
SRC = ROOT + "Recovery Workbench Information Flow v4.pptx"
DST = ROOT + "Recovery Workbench Information Flow v5.pptx"

# Per slide: ordered (old, new) run replacements; each matches the next occurrence after the previous one.
E = {
1: [("Henka Group, 28 October 2026", "Henka Group, 15 November 2026")],
2: [
 ("Through COLLINS", "Into ACE, daily"),
 ("SCBPDM and UDP", "SCBPDM"),
 ("AAL", "LIT"),
 ("LIT", "COLLINS models"),
 ("COLLINS models", "NLEADS, EasyApp, Entra ID, on change"),
 ("By file", "Into ACE, less often"),
 ("COLLINS", "ACE ingestion"),
 ("Databricks ETL batch. Loads each source at the end of the business day",
  "ACE team. Lands each source in ACE tables at the end of its business day"),
 ("File load", "ACE checks"),
 ("A scheduled batch job in ACE checks each file and loads it whole or not at all",
  "ACE ingestion checks each feed, takes it whole or not at all and records it in ace_batch_run"),
 ("ACE database: end of day data and everything the Workbench writes",
  "ACE database: source data in Tier 1 and Tier 2 ACE tables, and everything the Workbench writes"),
 ("Recovery Workbench module: case, rules, decision log, document hub, partner portal",
  "Recovery Workbench module: reads source data only through 30 read-only recovery.v_ace_* views; case, rules, decision log, document hub, partner portal"),
 ("There is no real-time feed today. Everything loaded is end of day or older; everything people and partners enter is current.",
  "The Workbench loads no source data: ACE ingests it and the Workbench reads views. Source data is end of day or older; what people enter is current."),
],
3: [
 ("Not used for data from other systems in Epics 1 and 2. Candidates are listed for decision DL06",
  "Not used for data from other systems in Epics 1 and 2. Same-day candidates stay open under DL06"),
 ("Used for personal data access logging (PII Kafka). Not used for business data in Epics 1 and 2",
  "PII Kafka for personal data access logging. ACE batch status reaches the Workbench as AceDataReady and AceDataLate"),
 ("COLLINS for every source it carries. File loads for CCMS, SVAF, AMIS, RPS, WIN and the GL",
  "ACE ingestion, owned by the ACE team, for every inbound source. The Workbench runs no inbound load and reads 30 views"),
 ("Replaced by file loads with checks. Data the bank does not hold in a system is entered on the case",
  "Trackers leave system scope and retire through the Cutover plan. Data no system holds is entered on the case"),
 ("The Workbench calls no system of record directly. Data comes in through COLLINS or a file load, and leaves through ACE paths that already exist.",
  "The Workbench calls no system of record directly. Data comes in through ACE ingestion and is read through recovery.v_ace_* views; it leaves through ACE paths that already exist."),
],
4: [
 ("Information that comes in through COLLINS", "Information that comes in daily through ACE"),
 ("From", "Source, ACE table"),
 ("Data product", "Read through"),
 ("Core bank (ALS)", "ALS, account"), ("DP01", "v_ace_account"),
 ("Core bank (ALS)", "ALS, payment"), ("DP01, DP13", "v_ace_payment"),
 ("SCBPDM, UDP and the core bank", "SCBPDM, customer and contacts"), ("DP02", "v_ace_customer, v_ace_contact"),
 ("EFS", "EFS, efs_action"), ("DP05", "v_ace_efs_action"),
 ("COLLINS models", "COLLINS, collins_score"), ("DP11", "v_ace_score"),
 ("LIT", "LIT, lawsuit"), ("DP07", "v_ace_lawsuit"),
 ("COLLINS loads each source after the business day closes. The Workbench uses it the next morning, so a payment made today is seen tomorrow.",
  "ACE ingests each source after the business day closes, into Tier 1 tables or the Tier 2 tables and columns in RWB-ACE-001. "
  "The Workbench reads the views the next morning, so a payment made today is seen tomorrow. "
  "Data products: I01 DP01; I02 DP01, DP13; I03 DP02; I04 DP05; I05 DP11; I06 DP07."),
],
5: [
 ("Information that comes in by file or is entered", "Information that comes in weekly or monthly, or is entered"),
 ("Data product", "Read through; data product"),
 ("File load, weekly", "ACE ingestion to collateral_detail, weekly"), ("DP06", "v_ace_collateral; DP06"),
 ("File load, weekly", "ACE ingestion to valuation, weekly"), ("DP06", "v_ace_valuation; DP06"),
 ("File load, monthly", "ACE ingestion to npa_asset and npa_sale, monthly"), ("DP06", "v_ace_npa_asset, v_ace_npa_sale; DP06"),
 ("File load, weekly", "ACE ingestion to npa_asset, weekly"), ("DP06", "v_ace_npa_asset; DP06"),
 ("File load, weekly", "ACE ingestion to pod_receipt, weekly"), ("DP07", "v_ace_pod; DP07"),
 ("File load, monthly", "ACE ingestion to gl_write_off, monthly"), ("DP13", "v_ace_write_off; DP13"),
 ("Sign-in, at each sign-in", "ACE sign-in; groups through ACE ingestion to iam_group"), ("DP14", "v_ace_iam_group; DP14"),
],
6: [
 ("The officer books in the core bank. The Workbench confirms the booking on the next day's load",
  "The officer books in the core bank. The Workbench confirms the booking from ACE on the next business date"),
],
7: [
 ("How fresh they are", "How fresh, per ace_batch_run"),
 ("A case enters the morning after it reaches 90 days past due", "A case enters the morning after ACE shows it at 90 days past due"),
 ("The posting is confirmed against the GL file each month", "The posting is confirmed against the GL data in ACE each month"),
],
8: [
 ("A COLLINS load is late", "An ACE source is late"),
 ("Keeps the previous load in use and marks the data product stale. Checks again each hour until the load window closes",
  "Raises AceDataLate at the source cut-off and marks the data product stale. The previous ACE business date stays in use"),
 ("Data steward, platform administrator", "Data steward, platform administrator, ACE team"),
 ("A load fails its checks", "ACE refuses a feed"),
 ("Refuses the whole load. The previous load stays in use",
  "Reads the last complete business date from ace_batch_run. The previous ACE data stays in use"),
 ("Data steward, platform administrator", "Data steward, ACE team"),
 ("A file is late", "A weekly or monthly source is late"),
 ("Marks the data product stale one business day after the file was due",
  "Raises AceDataLate and marks the data product stale one business day after the ACE batch was due"),
 ("The team that sends the file, data steward", "ACE team, data steward"),
 ("A booking is not seen in the next day's load", "A booking is not seen on the next ACE business date"),
],
9: [
 ("The checks every load passes", "The checks ACE data passes"),
 ("The load is for the expected business date and is not a repeat of a load already taken",
  "ACE ingestion: the feed is for the expected business date and is not a repeat of one already taken"),
 ("Refuse the load", "ACE refuses the feed"),
 ("Refuse the load", "ACE refuses the feed"),
 ("Refuse the load", "ACE refuses the feed"),
 ("Every record has its key, and no key appears twice", "Every record has its business key, and no key appears twice"),
 ("Refuse the load", "ACE refuses the feed"),
 ("References", "View conformance"),
 ("Each account, customer or asset is one the Workbench can match",
  "Workbench build: every v_ace_* view compiles, nothing references public and the role cannot write"),
 ("Hold the record in an exception list and try it again with the next load", "The build fails and nothing deploys"),
 ("Lists of values", "Batch complete"),
 ("Each coded value is in its list of values",
  "ace_batch_run shows the source complete for the expected business date by its cut-off"),
 ("Hold the record in an exception list; add the value through a versioned load if it is new",
  "AceDataLate; the data product is marked stale"),
 ("Movement", "Reconciliation"),
 ("Changes against the previous load are within the expected range",
  "Case accounts reconcile to v_ace_account; every business key resolves"),
 ("Load, and alert the data steward", "Alert the data steward"),
 ("Each load records its business date, record count, control totals and result. Each loaded record carries the business date, so a decision can show the age of every input.",
  "ACE ingestion records each feed's business date, record count and result in ace_batch_run. Each view carries the business date, so a decision can show the age of every input."),
],
10: [
 ("The next step runs on the next day's load", "The next step runs on the next ACE business date"),
 ("Assumed: the daily batch for all Epic 1 and Epic 2 data, with events added later for named same-day triggers. Which interfaces need real-time data is decision DL06.",
  "Assumed: ACE end of day data for all Epic 1 and Epic 2 work (D-RCV-35), with events added later for named same-day triggers. Which interfaces need real-time data stays open under DL06."),
],
11: [
 ("Daily batch for everything loaded; events added later for named triggers",
  "ACE end of day data for every source; events added later for named triggers"),
 ("DL06", "DL06; D-RCV-35"),
 ("None. The Workbench reads and writes through ACE and COLLINS only",
  "None. The Workbench reads ACE through views and writes through ACE paths only"),
 ("DL12", "D-RCV-35, was DL12"),
 ("The difference accepted between a load and its source", "The difference accepted between an ACE feed and its source"),
 ("Zero. A load that does not reconcile is refused whole",
  "Zero. ACE refuses a feed that does not reconcile; cases reconcile to v_ace_account"),
 ("How much EFS history comes in", "How much EFS history ACE holds"),
 ("Who builds SMS and LINE dispatch and the EFS file automation", "Who builds SMS and LINE dispatch"),
 ("When CCMS, SVAF, AMIS and RPS data comes through COLLINS", "Whether the ACE team accepts RWB-ACE-001 and its dates"),
 ("File loads at the frequencies shown until a batch feed exists",
  "Tier 2 tables needed by 21 November; until then the Tier 2 views and their features stay behind flags"),
 ("DL06, DL12", "DL43, open"),
],
}

zin = zipfile.ZipFile(SRC)
zout = zipfile.ZipFile(DST, "w")
for info in zin.infolist():
    data = zin.read(info.filename)
    m = re.match(r"ppt/slides/slide(\d+)\.xml$", info.filename)
    if m and int(m.group(1)) in E:
        x = data.decode("utf-8"); pos = 0
        for old, new in E[int(m.group(1))]:
            o = "<a:t>%s</a:t>" % escape(old); n = "<a:t>%s</a:t>" % escape(new)
            i = x.find(o, pos)
            if i < 0:
                sys.exit("NOT FOUND slide %s: %r" % (m.group(1), old))
            x = x[:i] + n + x[i + len(o):]; pos = i + len(n)
        minidom.parseString(x.encode("utf-8"))  # well-formed check
        data = x.encode("utf-8")
    elif info.filename == "docProps/core.xml":
        data = data.replace(b"Information Flow v4", b"Information Flow v5")
    zout.writestr(info, data)
zout.close()
print("written", DST)
