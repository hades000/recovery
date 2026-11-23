
What Recovery uses from ACE: the shared ACE Common services

Six connections, each with one owner, one contract and one call type; arrows point from caller to callee

Recovery

ACE Common (ACE team)

1

gateway-bff · rwb-access

REST / OIDC

sign-in, user JWT, group-to-role

Sign-in & access checks

2

all 19 services

Kafka (PII path)

audit and PII access logs → SOC

Audit & PII logging

3

rwb-case

REST

GET /case-summary/{id}

Shared case view (ACE case list)

4

rwb-treatment

Nexus

restructure.calculate (REST fallback)

Restructure calculator

5

rwb-comms

REST

send SMS / LINE message, delivery status

Notification path: NSS SMS, LINE OA

6

rwb-source-data

SQL views

30 recovery.v_ace_* views, read-only

Shared entities in the ACE database

Recovery reuses ACE's sign-in, logging, case view, calculator and notifications instead of building its own.

30

Notes: ACE Common is built and run by the ACE team; Recovery consumes it through versioned contracts (INT-34) with contract tests on both sides.

(1) Sign-in and access checks: gateway-bff and rwb-access use ACE's Entra-based sign-in; Recovery roles, scope, masking and DoA stay as data in rwb-access. (2) Audit and PII logging: every service sends audit and personal-data access logs through ACE's PII Kafka path to the SOC. (3) Shared case view: ACE's case list calls rwb-case GET /case-summary/{id}. (4) Restructure calculator: rwb-treatment calls it as a Nexus operation (REST fallback). (5) Notification path: rwb-comms sends SMS and LINE messages through ACE (NSS, LINE OA); WIN letters go as a file via rwb-integration. (6) Shared entities: customer, account, product, collateral and asset come from the ACE database through the views, read only by rwb-source-data.

