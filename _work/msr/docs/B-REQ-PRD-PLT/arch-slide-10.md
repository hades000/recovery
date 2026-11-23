
Walkthrough: an officer opens a case in about 1.2 seconds

Two services are asked at the same time, one hop each; other tabs load when clicked

Officer browser

App Gateway

gateway-bff

1

ACE Common
sign-in, JWT

2

rwb-case
GET /v1/cases/{id}

rwb-source-data
GET /v1/customers/{id}, /accounts/{id}

3

schema rwb_case (case, stage, tasks)

ACE DB · recovery.v_ace_* views (read-only)

④ merge both answers into the screen

Response budget (95th percentile)

0.15

two calls in parallel 0.6 s

merge 0.3 s

headroom to the 2 s target

gateway and session 0.15 s + slowest call 0.6 s + merge 0.3 s ≈ 1.05 s; budgeted at about 1.2 s

Other tabs load on click, each from its owner, one hop:

Documents
rwb-document

Notices
rwb-comms

Payments
rwb-payment

Legal
rwb-litigation

Screens never chain calls: the gateway asks each owner directly, in parallel, and only for what is on screen.

10

Notes: Steps: (1) the browser calls /api/recovery/cases/{id} through the App Gateway; (2) gateway-bff checks the session in Redis, gets a short-lived JWT through ACE Common sign-in and checks the coarse permission; (3) in parallel it calls rwb-case GET /v1/cases/{id} (case, stage, tasks, timers from schema rwb_case) and rwb-source-data GET /v1/customers/{id} and /v1/accounts/{id} (ACE data through the v_ace_* views, masked by policy); (4) it merges the two answers into the screen model.

Budget (p95): gateway and session 0.15 s, slowest of the two parallel calls 0.6 s, composition and transfer 0.3 s, total about 1.2 s against the 2 s target.

Each service authorises the object itself (OWASP API1 object-level authorisation), using cached permission data from rwb-access. Timeouts 2 s, circuit breaker per downstream, GET retry once with jitter.

