
Security in layers: nobody is trusted by default

Six layers from the network edge to the audit trail

Edge

Shared App Gateway with WAF; partners only through the partner gateway (FAPI 2.0)

Sign-in

ACE Common sign-in (Entra ID, MFA) at the shared gateway-bff; 15-minute idle timeout

Service to service

Every call encrypted and identified both ways (mTLS); Kafka ACLs per service

Inside each service

Checks the user's role, scope and DoA on every action (rwb-access data)

Data

One login per schema; personal data masked and encrypted; never in events or workflow payloads

Audit & monitoring

Hash-chained decision log; ACE PII logging to SOC; one trace across services

AI under BOT AI risk rules
guidelines of 12 Sep 2025

Suggests, never decides: a person approves

Model and prompt versions recorded

Personal data masked before it leaves

60-second limit, then the rules decide

Runs only in rwb-agent, easy to switch off

Built on NIST SP 800-204 (zero trust for microservices), OWASP API Top 10 and FAPI 2.0 for partner access.

35

Notes: Zero trust per NIST SP 800-204 (security strategies for microservices) and 800-204A (service mesh): every service-to-service call is mutually authenticated with workload identity and authorised by policy, deny by default. 800-204B (attribute-based access control) informs data scope and DoA checks; 800-204C/204D inform the DevSecOps pipeline and supply-chain controls.

Baseline: Req 8 (shared BFF: opaque tokens to the browser, one login/logout/timeout), Req 9 (each service authorises its own resources - OWASP API1:2023 Broken Object Level Authorization), Req 10 (W3C trace context).

Partners: FAPI 2.0 Security Profile (final Feb 2025) for the partner API - sender-constrained tokens, PAR, strong client authentication; separate DMZ gateway; penetration test before launch.

PDPA: personal data stays in the owning service; events and workflow histories carry IDs; Temporal payload codec encrypts payloads (AES-GCM) with keys in Key Vault; masking rules (P4) enforced in each service.

AI: BOT AI Risk Management Guidelines (Sep 2025) - accountability, lifecycle risk management, explainability, telling customers and offering a human. NFR v3: 60 s then rule result.

v5 specifics: staff sign-in is ACE Common's (Entra ID, MFA) through the shared gateway-bff; each service has its own database login with grants on its own schema only; Kafka topics have per-service ACLs; Temporal namespaces have their own certificates and codec keys.

