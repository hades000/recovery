"""Export every Jira issue of project TB0001 / component "E2E Workbench" to Markdown + CSV.

Usage:  python -I jira_export.py <env-file> <out-dir>

  <env-file>  the Jira MCP .env (JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN). Read only; never printed.
  <out-dir>   export folder. Epics/, Stories/, Tasks/, Sub-tasks/, Other/, Attachments/ and the
              CSV/README files inside it are rewritten. Anything else in the folder is left alone.

Every non-empty field of the issue is written out, including the Acceptance Criteria custom field
(customfield_10320), which the first version of this export missed. Attachment files are downloaded.
"""
import base64, csv, json, re, shutil, sys, time
import urllib.error, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

JQL = 'project = TB0001 AND component = "E2E Workbench" ORDER BY key ASC'
AC_FIELD = "customfield_10320"
FOLDERS = {"Epic": "Epics", "Story": "Stories", "Task": "Tasks", "Sub-task": "Sub-tasks"}
# Fields that are written in their own section/row, or are pure noise.
HANDLED = {
    "summary", "description", "status", "issuetype", "parent", "assignee", "reporter", "priority",
    "labels", "components", "fixVersions", "created", "updated", "duedate", "comment", "attachment",
    "issuelinks", "subtasks", "project", "resolution", "votes", "watches", "timetracking",
    AC_FIELD, "customfield_10020", "customfield_10014", "customfield_10001",
    "customfield_10019", "customfield_10000", "customfield_10024",  # Rank, Development, first-response chart
    "lastViewed", "thumbnail", "workratio", "progress", "aggregateprogress", "issuerestriction",
    "statusCategory", "creator", "worklog", "aggregatetimeestimate", "aggregatetimeoriginalestimate",
    "aggregatetimespent", "timeestimate", "timeoriginalestimate", "timespent", "versions",
    "statuscategorychangedate", "security", "environment", "resolutiondate",
}


def load_env(path):
    env = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("\"'")
    return env


class Jira:
    def __init__(self, env):
        self.base = env["JIRA_URL"].rstrip("/")
        tok = base64.b64encode(f"{env['JIRA_EMAIL']}:{env['JIRA_API_TOKEN']}".encode()).decode()
        self.auth = "Basic " + tok
        self.users = {}

    def get(self, path, **q):
        url = self.base + path + (("?" + urllib.parse.urlencode(q)) if q else "")
        for attempt in range(4):
            req = urllib.request.Request(url, headers={"Authorization": self.auth, "Accept": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:
                if e.code in (429, 502, 503) and attempt < 3:
                    time.sleep(2 * (attempt + 1)); continue
                raise
        raise RuntimeError("unreachable")

    def search_all(self):
        out, token, start = [], None, 0
        while True:
            try:
                q = {"jql": JQL, "maxResults": 100, "fields": "*all"}
                if token: q["nextPageToken"] = token
                d = self.get("/rest/api/2/search/jql", **q)
                out += d["issues"]
                token = d.get("nextPageToken")
                if not token or d.get("isLast"): return out
            except urllib.error.HTTPError as e:
                if e.code not in (404, 410): raise
                d = self.get("/rest/api/2/search", jql=JQL, startAt=start, maxResults=100, fields="*all")
                out += d["issues"]; start += len(d["issues"])
                if start >= d["total"] or not d["issues"]: return out

    def all_comments(self, key):
        out, start = [], 0
        while True:
            d = self.get(f"/rest/api/2/issue/{key}/comment", startAt=start, maxResults=100)
            out += d["comments"]; start += len(d["comments"])
            if start >= d["total"] or not d["comments"]: return out

    def user_name(self, account_id):
        if account_id not in self.users:
            try:
                self.users[account_id] = self.get("/rest/api/2/user", accountId=account_id).get("displayName") or ""
            except Exception:
                self.users[account_id] = ""
        return self.users[account_id]

    def download(self, url, dest):
        """Fetch an attachment. Jira redirects to a signed media URL; do not send credentials there."""
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k): return None
        opener = urllib.request.build_opener(NoRedirect)
        req = urllib.request.Request(url, headers={"Authorization": self.auth})
        try:
            resp = opener.open(req, timeout=120)
        except urllib.error.HTTPError as e:
            if e.code not in (301, 302, 303, 307, 308): raise
            resp = urllib.request.urlopen(urllib.request.Request(e.headers["Location"]), timeout=120)
        with resp, open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)


# ---------- formatting helpers ----------
def mentions(jira, text):
    def sub(m):
        name = jira.user_name(m.group(1))
        return "@" + (name if name else "user " + m.group(1)[:8])
    return re.sub(r"\[~accountid:([^\]]+)\]", sub, text or "")


def flat(v):
    if v is None: return ""
    if isinstance(v, (str, int, float, bool)): return str(v)
    if isinstance(v, list): return "; ".join(x for x in (flat(i) for i in v) if x)
    if isinstance(v, dict):
        for k in ("displayName", "value", "name", "key"):
            if v.get(k) not in (None, ""):
                s = str(v[k])
                if v.get("child", {}).get("value"): s += " / " + str(v["child"]["value"])
                return s
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def empty(v):
    return v in (None, "", [], {}) or (isinstance(v, dict) and not any(v.values()))


def cell(s):
    return str(s).replace("|", "\\|").replace("\r", "").replace("\n", " ").strip()


def code_of(summary):
    m = re.match(r"\s*\[([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\]", summary or "")
    return m.group(1) if m else ""


def safe_name(s, n):
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", s).strip().rstrip(". ")
    return re.sub(r"\s+", " ", s)[:n].rstrip(". ")


def sprint_names(f):
    out = []
    for s in f.get("customfield_10020") or []:
        out.append(s.get("name", "") if isinstance(s, dict) else str(s))
    return "; ".join(out)


def main(env_path, out_dir):
    jira = Jira(load_env(env_path))
    jira.field_names = {x["id"]: x["name"] for x in jira.get("/rest/api/2/field")}
    out = Path(out_dir)
    print("searching…", flush=True)
    issues = jira.search_all()
    print(f"{len(issues)} issues", flush=True)
    by_key = {i["key"]: i for i in issues}

    # story code of every issue; sub-tasks without their own code inherit the parent's
    codes = {k: code_of(i["fields"]["summary"]) for k, i in by_key.items()}
    for k, i in by_key.items():
        p = (i["fields"].get("parent") or {}).get("key")
        if not codes[k] and i["fields"]["issuetype"]["name"] == "Sub-task" and p in codes:
            codes[k] = codes[p]

    for d in list(FOLDERS.values()) + ["Other", "Attachments"]:
        if (out / d).exists(): shutil.rmtree(out / d)
        (out / d).mkdir(parents=True, exist_ok=True)
    children = {}
    for k, i in by_key.items():
        p = (i["fields"].get("parent") or {}).get("key")
        if p: children.setdefault(p, []).append(k)

    index_rows, comment_rows = [], []
    totals = Counter()
    for n, (key, issue) in enumerate(by_key.items(), 1):
        f = issue["fields"]
        itype = f["issuetype"]["name"]
        code = codes[key]
        comments = (f.get("comment") or {}).get("comments", [])
        if (f.get("comment") or {}).get("total", len(comments)) > len(comments):
            comments = jira.all_comments(key)
        url = f"{jira.base}/browse/{key}"
        summary = f["summary"]
        title = summary
        if code and code_of(summary) == code:
            title = re.sub(r"^\s*\[[^\]]+\]\s*", "", summary)
        stem = safe_name(f"{key} {code} {title}" if code else f"{key} {title}", 150)
        folder = FOLDERS.get(itype, "Other")
        who = lambda u: (u or {}).get("displayName", "") if u else ""
        parent = (f.get("parent") or {}).get("key", "")
        tt = f.get("timetracking") or {}
        L = [f"# {key} {summary}", "", "| Field | Value |", "|---|---|"]
        rows = [
            ("Jira", f"[{key}]({url})"), ("Type", itype), ("Status", f["status"]["name"]),
            ("Resolution", flat(f.get("resolution")) or "-"), ("Parent", parent or "-"),
            ("Epic link", f.get("customfield_10014") or "-"),
            ("Assignee", who(f.get("assignee")) or "-"), ("Reporter", who(f.get("reporter")) or "-"),
            ("Priority", flat(f.get("priority")) or "-"), ("Labels", ", ".join(f.get("labels") or []) or "-"),
            ("Components", flat(f.get("components")) or "-"), ("Fix versions", flat(f.get("fixVersions")) or "-"),
            ("Affects versions", flat(f.get("versions")) or "-"),
            ("Sprint", sprint_names(f) or "-"), ("Team", flat(f.get("customfield_10001")) or "-"),
            ("Created", f["created"]), ("Updated", f["updated"]), ("Due date", f.get("duedate") or "-"),
            ("Resolved", f.get("resolutiondate") or "-"),
            ("Original estimate", tt.get("originalEstimate", "-")), ("Remaining estimate", tt.get("remainingEstimate", "-")),
            ("Time spent", tt.get("timeSpent", "-")),
            ("Votes", (f.get("votes") or {}).get("votes", 0)), ("Watchers", (f.get("watches") or {}).get("watchCount", 0)),
            ("Comments", len(comments)),
        ]
        L += [f"| {a} | {cell(b)} |" for a, b in rows]
        L += ["", "## Description", "", mentions(jira, f.get("description") or "(none)")]
        ac = f.get(AC_FIELD)
        if ac:
            L += ["", "## Acceptance criteria", "", "```gherkin", ac.replace("\r", "").rstrip(), "```"]
        if f.get("environment"):
            L += ["", "## Environment", "", f["environment"]]

        links = []
        for ln in f.get("issuelinks") or []:
            if "outwardIssue" in ln: rel, o = ln["type"]["outward"], ln["outwardIssue"]
            else: rel, o = ln["type"]["inward"], ln["inwardIssue"]
            links.append(f"- {rel} {o['key']}: {o['fields']['summary']} ({o['fields']['status']['name']})")
        if links: L += ["", "## Linked issues", ""] + links
        subs = f.get("subtasks") or []
        if subs:
            L += ["", "## Sub-tasks", ""]
            L += [f"- {s['key']} [{s['fields']['status']['name']}] {s['fields']['summary']}" for s in subs]
        if itype == "Epic" and children.get(key):
            L += ["", "## Child issues", ""]
            L += [f"- {c} [{by_key[c]['fields']['status']['name']}] {by_key[c]['fields']['summary']}" for c in children[key]]

        atts = f.get("attachment") or []
        if atts:
            L += ["", "## Attachments", ""]
            adir = out / "Attachments" / key
            adir.mkdir(parents=True, exist_ok=True)
            for a in atts:
                fname = safe_name(a["filename"], 120) or a["id"]
                dest = adir / fname
                if dest.exists(): dest = adir / f"{a['id']}-{fname}"
                try:
                    jira.download(a["content"], dest); totals["att_ok"] += 1; note = ""
                except Exception as e:
                    totals["att_fail"] += 1; note = f" — DOWNLOAD FAILED ({e})"
                rel = urllib.parse.quote(f"../../Attachments/{key}/{dest.name}")
                L.append(f"- [{a['filename']}]({rel}) ({a['size']} bytes, {who(a.get('author'))}, {a['created']}){note}")

        L += ["", f"## Comments ({len(comments)})", ""]
        if not comments: L.append("(none)")
        for i, c in enumerate(comments, 1):
            edited = c["updated"] if c["updated"] != c["created"] else ""
            body = mentions(jira, c["body"]).replace("\r\n", "\n")
            head = f"### Comment {i}: {who(c.get('author'))}, {c['created']}" + (f", edited {edited}" if edited else "")
            L += [head, "", f"Comment ID {c['id']}", "", body, ""]
            comment_rows.append([key, code, i, c["id"], who(c.get("author")), c["created"], edited, body])
        totals["comments"] += len(comments)

        other = []
        for fid, v in f.items():
            if fid in HANDLED or empty(v): continue
            s = flat(v)
            if s: other.append((jira.field_names.get(fid, fid), fid, s))
        if other:
            L += ["", "## Other Jira fields", "", "| Field | ID | Value |", "|---|---|---|"]
            L += [f"| {cell(a)} | {b} | {cell(c)[:600]} |" for a, b, c in sorted(other, key=lambda x: x[0].lower())]

        (out / folder / f"{stem}.md").write_text("\n".join(L).rstrip() + "\n", encoding="utf-8", newline="\n")
        totals[folder] += 1
        index_rows.append([
            key, code, itype, f["status"]["name"], summary, parent, who(f.get("assignee")), who(f.get("reporter")),
            flat(f.get("priority")), "; ".join(f.get("labels") or []), flat(f.get("components")),
            flat(f.get("fixVersions")), f["created"], f["updated"], f.get("duedate") or "",
            len(comments), len(atts), len(links), len(subs), url,
            "Y" if ac else "", sprint_names(f), flat(f.get("resolution")), f.get("customfield_10014") or "",
        ])
        if n % 20 == 0: print(f"  {n}/{len(by_key)}", flush=True)

    hdr = ["Key", "Story code", "Type", "Status", "Summary", "Parent", "Assignee", "Reporter", "Priority", "Labels",
           "Components", "Fix versions", "Created", "Updated", "Due date", "Comments", "Attachments", "Links",
           "Sub-tasks", "URL", "Has acceptance criteria", "Sprint", "Resolution", "Epic link"]
    with open(out / "Issues index.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerows(index_rows)
    with open(out / "All comments.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Issue", "Story code", "#", "Comment ID", "Author", "Posted", "Edited", "Text"])
        w.writerows(comment_rows)

    types = Counter(r[2] for r in index_rows)
    commented = len({r[0] for r in comment_rows})
    n_ac = sum(1 for r in index_rows if r[20])
    now = datetime.now().astimezone()
    readme = f"""# {out.name}

Export of every Jira issue in project TB0001 with component "E2E Workbench" ({jira.base.split('//')[1]}), taken on {now:%d %B %Y}, about {now:%H:%M}. It is a full text copy: every non-empty field, the description, the acceptance criteria, linked issues, comments and the attachment files.

## Contents

| Item | What it holds |
|---|---|
| `Issues index.csv` | One row per issue ({len(index_rows)}): key, story code, type, status, parent, assignee, reporter, priority, labels, dates, counts, URL, whether it has acceptance criteria, sprint, resolution, epic link. Opens in Excel. |
| `All comments.csv` | One row per comment ({len(comment_rows)}): issue, comment ID, author, posted and edited time, text. |
| `Epics/` | {types['Epic']} epics, one Markdown file each |
| `Stories/` | {types['Story']} stories |
| `Tasks/` | {types['Task']} tasks |
| `Sub-tasks/` | {types['Sub-task']} sub-tasks |
| `Other/` | {len(index_rows) - types['Epic'] - types['Story'] - types['Task'] - types['Sub-task']} other item(s) |
| `Attachments/<key>/` | {totals['att_ok']} attachment files, named as in Jira |

Each file is named `TB0001-nnnn [story code] title.md` and holds the field table, description, acceptance criteria (Gherkin, when the issue has it), linked issues, sub-tasks, attachments, every comment in order, and an "Other Jira fields" table with the remaining non-empty fields.

## Counts

- {len(index_rows)} issues: {types['Epic']} epics, {types['Story']} stories, {types['Task']} tasks, {types['Sub-task']} sub-tasks, {len(index_rows) - types['Epic'] - types['Story'] - types['Task'] - types['Sub-task']} other.
- {n_ac} issues have acceptance criteria.
- {len(comment_rows)} comments on {commented} issues. {totals['att_ok']} attachments downloaded{f", {totals['att_fail']} failed" if totals['att_fail'] else ""}.

## Notes

- **Replies:** Jira comments are not threaded. A reply is just a later comment, so the order and the @name in each comment show who is answering whom.
- **Formatting:** comment and description text keeps Jira's own markup (`*bold*`, `{{{{code}}}}`, `#` numbered lists). @mentions are replaced with the person's name where Jira could resolve it; otherwise they show as "user" plus the start of the account ID.
- **Not included:** change history, and worklogs (none are logged).
- **Updated times** are as Jira reported them at the time of export.
- This is a snapshot. It does not refresh when Jira changes. To refresh: `python -I _work/scripts/jira_export.py <mcp/jira/.env> "<this folder>"`.
"""
    (out / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print("done", dict(totals), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
