
The guardrails: industry standards and Bank of Thailand rules

Every choice in this deck traces back to one of these

Industry standards we follow

BIAN
Bank capability map: one service per capability

Microservice patterns
Schema per service, sagas, outbox (microservices.io)

Zero trust (NIST SP 800-204)
Every call encrypted and checked

Standard contracts
OpenAPI 3.1, AsyncAPI 3, CloudEvents 1.0

Decision models (OMG DMN)
Rules in an industry format, not Excel

OpenTelemetry
One trace across REST, Kafka and Temporal

FAPI 2.0 · OWASP API
Secure partner and internal APIs

Azure Well-Architected
Reference design for services on AKS

Bank of Thailand and Thai law

FPG 19/2560 · IT risk
Prior BOT approval for significant change

FPG 19/2559 · outsourcing
Rules for cloud and third parties

Cyber resilience (CRAF)
Protect, detect, respond, recover

AI risk guidelines (Sep 2025)
Human oversight, explainability

PDPA
Personal data: purpose, minimum, security

BOT may need to approve this change before go-live (FPG 19/2560 cl. 5.5, up to 30 business days): plan for it now.

6

Notes: Verified 19 Nov 2026 against primary sources (URLs in the references slide).

BIAN: release 14.0 (Feb 2026); service domains are elemental, mutually exclusive and collectively exhaustive business capabilities - a direct basis for service boundaries.
microservices.io (Chris Richardson): decomposition by business capability and subdomain; data patterns.
NIST SP 800-204 (Aug 2019), 204A service mesh (May 2020), 204B ABAC (Aug 2021), 204C DevSecOps (Mar 2022); 204D software supply chain (Feb 2024) also relevant to pipelines.
FAPI 2.0 Security Profile approved Final 19 Feb 2025. OAuth 2.1 is still an IETF draft, so we cite FAPI 2.0 as the binding profile.
CloudEvents graduated in CNCF Jan 2024. AsyncAPI 3.1 is current. W3C Trace Context Level 1 is a Recommendation (Nov 2021).
DMN 1.6 formal Sep 2026; Apache KIE Drools supports DMN at conformance level 3 and DMN 1.6 since 10.2.0. Note XLS decision tables are a Drools-native format, separate from DMN.
Temporal: ANZ case study (home-loan origination); JPMorgan Chase talk at Replay 2024 (payments modernisation).

FPG 19/2560 (Regulations on IT Risk Management of Financial Institutions), announced 20 Dec 2017, effective 1 Apr 2018. Clause 5.5: first-time use of a technology, or a change that may pose significant risk, needs a board-approved plan submitted to BOT for approval before proceeding; BOT decides within 30 business days. This is a programme dependency: the date for submission belongs in the plan.

FPG 19/2559 (Regulations on IT Outsourcing for Business Operations of Financial Institutions): board-approved outsourcing policy and risk framework; notify BOT for private cloud from providers outside the group, seek approval for public cloud used for critical IT, both 30 days before use. Not checked whether later rules supersede it; Compliance to confirm.

Cyber Resilience Assessment Framework (CRAF), issued around 2018: six areas listed. No standalone CRAF document found on bot.or.th; source is a BOT payment systems report.

BOT AI Risk Management Guidelines issued 12 Sep 2025 after public hearing 12-30 Jun 2025 (date from a secondary source; Compliance to confirm).

These are summaries for architecture purposes, not legal advice; Compliance owns the interpretation.

