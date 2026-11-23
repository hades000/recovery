import json
from pathlib import Path

WP = "B-DELIVDOC-47"
SRC = "Recovery Workbench Run Operating Model v2"
OM = "Recovery Workbench Microservice Ownership Map v1"
TR = "Recovery Workbench Microservice Story Template and Rules v1"
AV5 = "Recovery Workbench Architecture v5 Text Extract v1"

gaps = [
    dict(
        title="No source names a service owner for the run of any of the 19 services",
        source=f"{SRC}; {OM}; {TR}",
        section="Slide 3 Service levels, Owner column; slide 6 Decision needed, DL02; slide 15 Who owns what",
        description=(
            "Version 2 makes the application owner the owner of a severity 1 and leaves the identity open in "
            "DL02 (the Tribe lead, with the ACE team as technical custodian). The realignment makes 19 services, "
            "each with its own schema, topic and task queue, so a run book needs one owner per service. The "
            "Ownership Map v1 assigns tables, endpoints, events, workflows and jobs to the service codes P1 to "
            "P10 and S1 to S9 but names no service owner, and Template and Rules R5.3 gives a suggested team by "
            "work type only. Version 3 therefore states the service code as the owner in the map and leaves the "
            "run-time owner open where it is needed."),
        evidence=(
            "Version 2 slide 3: 'Severity 1 ... Owner: Application owner'; slide 6: 'DL02 | Who the application "
            "owner is | The Tribe lead, with the ACE team as technical custodian'; the Services sheet of the "
            "Ownership Map v1 gives code, service, name, wave, schema, REST base, topic and queue, with no service "
            "owner column; Template and Rules R5.3 gives TechX, ACE team, SCB IT infrastructure, DevOps team and QA "
            "team as suggested owners by work type; R3 default rulings name owners for parameters and reference "
            "data, the case list API, the rule registry, the interaction ledger and feature flags only."),
        type="Missing", area="governance", severity="P2", needed_by_wave=1, legacy_ref="",
        owner_role="Programme governance",
        proposed=(
            "Name one service owner role for each of the 19 services, record it on the Services sheet of the "
            "Ownership Map next to the work-type suggestion, and close DL02 at the same time."),
    ),
    dict(
        title="The tier 2 and tier 3 roles of version 2 are not defined per service now that there are 19 services",
        source=f"{SRC}; {OM}; {TR}",
        section="Slide 2 Who runs the Workbench after go-live; slide 15 Who owns what",
        description=(
            "Version 2 gives tier 2 as the platform administrator, the reference data administrator and the data "
            "steward, and tier 3 as the TechX recovery squads and the ACE team, without saying which person or "
            "which team serves which service. The target has 19 services with their own schema, login, queue and "
            "topic, so a support request has to land on a named role for the service concerned. No source read for "
            "this deck gives that mapping, so version 3 keeps the tier table of version 2 and leaves the per-service "
            "role open."),
        evidence=(
            "Version 2 slide 2: 'Tier 2 ... Platform administrator; reference data administrator; data steward' and "
            "'Tier 3 ... TechX recovery squads; ACE team'; Architecture v5 slide 20 gives every service its own "
            "schema, login, task queue and Schedules; the Rulings sheet of the Ownership Map v1 names P3 rwb-case "
            "for parameters and reference data and P7 rwb-decision for the rule registry, but no tier role for a "
            "service."),
        type="Missing", area="governance", severity="P2", needed_by_wave=1, legacy_ref="",
        owner_role="Programme governance",
        proposed=(
            "State, for each tier, the role that serves each service, for example one platform administrator per "
            "wave, and print that role on the service's run book page."),
    ),
    dict(
        title="Version 2 gives four severity bands but no alert threshold, no SLO and no dashboard per service",
        source=f"{SRC}; {AV5}",
        section="Slide 3 Service levels; slide 9 Run book per service, step 1",
        description=(
            "Version 2 fixes a respond time and a restore time for four severities and nothing else. A run book per "
            "service needs the signal that starts the clock on that service: an error rate, a consumer lag, a "
            "dead-letter count or an outbox age. Architecture v5 gives the health and metrics endpoints, the retry "
            "topics and the dead-letter alert, and ADR-023 makes observability per service, but no source read gives "
            "a threshold, an error budget or a dashboard per service, so version 3 uses the four severity bands and "
            "leaves the threshold open."),
        evidence=(
            "Version 2 slide 3 gives respond and restore times only, with no threshold; Architecture v5 slide 20: "
            "'REST /health, /metrics for the platform'; slide 22: 'retry topics 1 min, 10 min, 1 h, then .dlt + "
            "alert'; no source read gives an alert threshold, an SLO, an error budget or a named dashboard for any "
            "of the 19 services."),
        type="Missing", area="infrastructure", severity="P2", needed_by_wave=1, legacy_ref="",
        owner_role="SCB IT infrastructure",
        proposed=(
            "Publish one alert and dashboard page per service, with latency, error rate, consumer lag, dead-letter "
            "count and outbox age, and cite it from the service's run book page."),
    ),
    dict(
        title="No source gives an on-call rota per service or the hand-off from the tier roles to the 19 services",
        source=f"{SRC}; {TR}",
        section="Slide 4 Hours and shifts; slide 16 Hours, rota and on call, per service",
        description=(
            "Version 2 has business hours with tier 1 and tier 2 on duty, an early shift for the data steward and "
            "outside hours with SCB IT on call for severity 1 and the platform administrator on call by rota. It "
            "gives one rota for one deployable. The target has 19 services in waves 1 to 4, so the rota and the "
            "hand-off point from tier 1 to the service concerned have to be stated per service. No source read for "
            "this deck states either, so version 3 keeps the four rows of version 2 and adds the per-service column "
            "with the open value."),
        evidence=(
            "Version 2 slide 4: 'Outside hours | SCB IT on call for severity 1; platform administrator on call by "
            "rota'; slide 5 gives four escalation rows and no rota; the Services sheet of the Ownership Map v1 gives "
            "the wave of each of the 19 services but no rota; no source read names a paging tool, a rota period or a "
            "hand-off point."),
        type="Missing", area="governance", severity="P2", needed_by_wave=1, legacy_ref="",
        owner_role="DevOps team",
        proposed=(
            "Publish one rota page per service for business hours, the early shift and outside hours, and state the "
            "point at which tier 1 hands a request to the service's owner."),
    ),
    dict(
        title="The source deck carries no change log, no version history and no tool line",
        source=SRC,
        section="Slide 19 Change log; slide 7 What changed in version 3",
        description=(
            "Version 2 is six slides and has no change-log slide, no revision table and no tool line. The cover "
            "carries the date 28 October 2026 and the file properties carry no version history, so the rows before "
            "version 2 cannot be reconstructed from the source. Version 3 keeps the cover date, records version 2 as "
            "the source row and states the gap rather than inventing the history."),
        evidence=(
            "The converted text of the version 2 file has six slides: cover, who runs the Workbench, service levels, "
            "hours and shifts, escalation and the DL02 decision; none is a change log and none carries a tool line; "
            "the cover reads 'Henka Group, 28 October 2026'."),
        type="Missing", area="documentation", severity="P3", needed_by_wave=0, legacy_ref="",
        owner_role="Business analyst",
        proposed=(
            "Keep a change-log slide in every later version and rebuild the rows of versions 1 and 2 from the file "
            "properties and the release record."),
    ),
    dict(
        title="The source deck has no run book per service, although the target has 19 services",
        source=f"{SRC}; {AV5}",
        section="Slides 8 to 17, the run book per service",
        description=(
            "Version 2 describes one operating model for one deployable: tiers, service levels, hours, escalation "
            "and the DL02 decision. It never names a service, a schema, a topic, a task queue or a scheduled job, "
            "so nothing in it tells a person on call what to look at for the service that is failing. Architecture "
            "v5 gives each service its own contract, topic, task queue and Schedules, and the realignment run "
            "requires a run book per service. Version 3 adds the pages on slides 8 to 17 and records the gap here."),
        evidence=(
            "The version 2 deck has six slides and names no service; Architecture v5 slides 14 to 20 give the IN and "
            "OUT contract of every service, each with its own schema, topic and queue rwb-<short>; slide 20 note: "
            "'Every service: built from one template ... its own Schedules'."),
        type="Missing", area="documentation", severity="P3", needed_by_wave=1, legacy_ref="",
        owner_role="Solution architect",
        proposed=(
            "Keep one run book page per service beside that service's contract story, and review it at the start of "
            "the service's wave."),
    ),
    dict(
        title="No approval of version 3 is recorded and the source deck carries no status",
        source=SRC,
        section="Slide 7 What changed in version 3, status note; slide 19 Change log",
        description=(
            "The source has no status line and no approval record, and the realignment run takes no approval stop. "
            "Version 3 therefore carries the status Draft, states that no approval is recorded, and leaves the "
            "approval open here and in the assumption row."),
        evidence=(
            "The version 2 deck has six slides and none has a status, an approver, a sign-off line or a date of "
            "approval; the run rules in AGENTS.md rule 9 forbid waiting for an approval and require an assumption "
            "instead."),
        type="Missing", area="governance", severity="P3", needed_by_wave=0, legacy_ref="",
        owner_role="Programme governance",
        proposed=(
            "Record the approval of version 3 by the programme, the solution architect and the ACE team, with a "
            "date, and keep a status line on the cover and in the change log of every later version."),
    ),
]

assumptions = [
    dict(
        text=(
            "The owner of a service is its service code in the Ownership Map v1, with TechX as the suggested team "
            "for every service, and the run-time service owner stays open until one role is named per service."),
        why=(
            "A run book needs an owner and no source names a service owner; the Ownership Map is the agreed owner "
            "record and R5.3 gives the team as a suggestion only."),
        read=f"{SRC} slide 3 and slide 6; {OM} Services and Rulings sheets; {TR} R3 and R5.3",
        applied_in="Slide 8; slides 10 to 13, footnote; slide 15, service owner row",
        confidence="Medium",
        confirm="Programme governance with the solution architect",
        impact=(
            "A severity 1 call goes to the suggested team of the service until a service owner role is named; the "
            "escalation path on slide 17 is unchanged."),
    ),
    dict(
        text=(
            "The tier 2 and tier 3 roles of version 2 keep serving all 19 services as one pool until the per-service "
            "role is stated, and each service's run book page is read by that pool."),
        why=(
            "Version 2 states the roles once for one deployable and no source splits them across 19 services; keeping "
            "the pool changes nothing that the source says and invents no role."),
        read=f"{SRC} slide 2; {AV5} slide 20; {OM} Rulings sheet",
        applied_in="Slide 15, tier roles row; slides 10 to 13, footnote",
        confidence="Medium",
        confirm="Programme governance with the ACE team",
        impact=(
            "A request that concerns a named service may wait for the pool; the restore times on slide 3 still apply."),
    ),
    dict(
        text=(
            "Until a threshold is published, a service is in trouble when its health endpoint is not green or its "
            "error rate is visibly above its normal band, and the four severity bands of version 2 decide the "
            "response."),
        why=(
            "The run book has to give the person on call a starting signal and no source gives a threshold; the four "
            "bands are the only stated response rule."),
        read=f"{SRC} slide 3; {AV5} slides 20 and 22",
        applied_in="Slide 9, step 1 and its note",
        confidence="Medium",
        confirm="SCB IT infrastructure with the platform team",
        impact=(
            "Two people may judge the same reading differently until the thresholds exist; the restore clock starts "
            "when the severity is chosen."),
    ),
    dict(
        text=(
            "The rota of version 2 stays as the position for all 19 services: SCB IT on call for severity 1 outside "
            "hours and the platform administrator on call by rota, with the service's suggested team named on its "
            "page."),
        why=(
            "The source gives one rota and no per-service rota; keeping the stated rota is the only position that "
            "invents nothing."),
        read=f"{SRC} slide 4 and slide 5; {TR} R5.6 wave map",
        applied_in="Slide 16, outside hours row; slide 14, note",
        confidence="Medium",
        confirm="DevOps team with SCB IT",
        impact=(
            "Outside hours one rota covers every service, so a wave 3 or wave 4 service has no dedicated page until "
            "the per-service rota exists."),
    ),
    dict(
        text=(
            "The change log of version 3 starts at version 2 as the source row, dated 28 October 2026 from the cover, "
            "and no earlier row is reconstructed."),
        why=(
            "R8.1 requires a change-log row and the source has none; recording the gap is better than inventing the "
            "history of the earlier versions."),
        read=f"{SRC} cover and file properties; {TR} R8.1 and R8.2",
        applied_in="Slide 7, version 2 row and note; slide 19, version 2 row",
        confidence="Medium",
        confirm="Business analyst with programme governance",
        impact="A reader who needs the history before version 2 must go to the earlier files.",
    ),
    dict(
        text=(
            "Version 3 adds one run book page per service on slides 8 to 17: the eight steps, the page for each "
            "service, the shared platform, the owners, the hours, the escalation and the decisions."),
        why=(
            "The realignment requires a run book per service and the source has none; the pages are written from the "
            "Architecture v5 contracts and the Ownership Map, not from invented values."),
        read=f"{AV5} slides 12 to 20 and 34; {OM} Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Rulings; {TR} R4, R5.4 and R5.6",
        applied_in="Slides 8 to 17",
        confidence="High",
        confirm="Solution architect with the TechX tech leads",
        impact=(
            "Each service's page can be reviewed with that service's contract story; a change to a contract changes "
            "the page."),
    ),
    dict(
        text=(
            "Version 3 is issued as Draft with no recorded approval, and the approval is carried as an open gap and "
            "this assumption."),
        why=(
            "The run takes no approval stop and the source records none; Draft is the only truthful label."),
        read="AGENTS.md rule 9; Template and Rules U8 and R8.1; the version 2 deck",
        applied_in="Slide 7, status note; slide 19, change log",
        confidence="High",
        confirm="Programme governance",
        impact="The deck can be used for build and review; it cannot be cited as an approved operating model until the approval is recorded.",
    ),
]

gdir = Path("_work/msr/gaps"); adir = Path("_work/msr/assumptions")
gdir.mkdir(parents=True, exist_ok=True); adir.mkdir(parents=True, exist_ok=True)

grows = []
for i, g in enumerate(gaps, 1):
    row = {"id": f"CG-{WP}-{i}"}
    row.update(g)
    row["asm"] = f"ASM-{WP}-{i}"
    row["wp"] = WP
    grows.append(row)

arows = []
for i, a in enumerate(assumptions, 1):
    row = {"id": f"ASM-{WP}-{i}"}
    row.update(a)
    row["gap"] = f"CG-{WP}-{i}"
    row["wp"] = WP
    arows.append(row)

order_g = ["id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
           "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]
order_a = ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]

with open(gdir / f"{WP}.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in grows:
        f.write(json.dumps({k: r[k] for k in order_g}, ensure_ascii=True) + "\n")
with open(adir / f"{WP}.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in arows:
        f.write(json.dumps({k: r[k] for k in order_a}, ensure_ascii=True) + "\n")
print("gaps", len(grows), "assumptions", len(arows))
