# -*- coding: utf-8 -*-
"""Builds Recovery Workbench Document Index v14 from v13. Source is never edited."""
import re, io, json

SRC = '12 Project communication/Recovery Workbench Document Index v13.md'
DST = '12 Project communication/Recovery Workbench Document Index v14.md'

HEADER = [
    'SCB Collections and Recovery. Henka Group, 22 November 2026.',
    '(C) Siam Commercial Bank and Henka Pte Ltd',
    '',
    '# Recovery Workbench document index',
    '',
]

INTRO = ('Every asset in the document set at its current version, who reads it and the file that holds it. '
         'Functional and technical specifications are one file per module, in the two specification archives. '
         'The ACE DB alignment section carries the controlling change for the 15 November 2026 re-base, recorded as D-RCV-35. '
         'The Decisions section carries decision D-RCV-36 of 16 November 2026 and the two records that hold it.')

INTRO2 = ('Version 14 carries the microservice realignment of 22 November 2026, recorded as D-RCV-60: 19 services inside ACE, '
          'one per business module, with 7 platform epics and 5 integration epics, and every document shown at the version it '
          'holds after the realignment. Release dates are unchanged and tentative (U7; DL48). The Microservice realignment '
          'section lists every file the realignment added or moved to a new version; the Document gaps section lists what the '
          'files cannot show.')

SERVICES = [
    ('P1','rwb-source-data','Source data','1','rwb_source_data','/api/recovery/source-data/v1','rwb.source-data.events.v1','rwb-source-data'),
    ('P2','rwb-integration','Integration','1','rwb_integration','/api/recovery/integration/v1','rwb.integration.events.v1','rwb-integration'),
    ('P3','rwb-case','Case and workflow','1','rwb_case','/api/recovery/case/v1','rwb.case.events.v1','rwb-case'),
    ('P4','rwb-access','Access and authority','1','rwb_access','/api/recovery/access/v1','rwb.access.events.v1','rwb-access'),
    ('P5','rwb-document','Document','1','rwb_document','/api/recovery/document/v1','rwb.document.events.v1','rwb-document'),
    ('P6','rwb-comms','Communications','1','rwb_comms','/api/recovery/comms/v1','rwb.comms.events.v1','rwb-comms'),
    ('P7','rwb-decision','Decision and rules','1','rwb_decision','/api/recovery/decision/v1','rwb.decision.events.v1','rwb-decision'),
    ('P8','rwb-payment','Payment','2','rwb_payment','/api/recovery/payment/v1','rwb.payment.events.v1','rwb-payment'),
    ('P9','rwb-reporting','Reporting','1','rwb_reporting','/api/recovery/reporting/v1','rwb.reporting.events.v1','rwb-reporting'),
    ('P10','rwb-agent','Agent','1','rwb_agent','/api/recovery/agent/v1','rwb.agent.events.v1','rwb-agent'),
    ('S1','rwb-valuation','Valuation and route','3','rwb_valuation','/api/recovery/valuation/v1','rwb.valuation.events.v1','rwb-valuation'),
    ('S2','rwb-treatment','Treatment and offer','2','rwb_treatment','/api/recovery/treatment/v1','rwb.treatment.events.v1','rwb-treatment'),
    ('S3','rwb-guarantee','Guarantee','3','rwb_guarantee','/api/recovery/guarantee/v1','rwb.guarantee.events.v1','rwb-guarantee'),
    ('S4','rwb-litigation','Litigation','3','rwb_litigation','/api/recovery/litigation/v1','rwb.litigation.events.v1','rwb-litigation'),
    ('S5','rwb-asset','Asset','2','rwb_asset','/api/recovery/asset/v1','rwb.asset.events.v1','rwb-asset'),
    ('S6','rwb-debtsale','Debt sale','3','rwb_debtsale','/api/recovery/debtsale/v1','rwb.debtsale.events.v1','rwb-debtsale'),
    ('S7','rwb-writeoff','Write-off','4','rwb_writeoff','/api/recovery/writeoff/v1','rwb.writeoff.events.v1','rwb-writeoff'),
    ('S8','rwb-deviation','Deviation','2','rwb_deviation','/api/recovery/deviation/v1','rwb.deviation.events.v1','rwb-deviation'),
    ('S9','rwb-partner','Partner','4','rwb_partner','/api/recovery/partner/v1','rwb.partner.events.v1','rwb-partner'),
]

STORY_SETS = [
    ('RWB-PLT-TPL Service template and repositories', 19),
    ('RWB-PLT-LIB Shared libraries', 18),
    ('RWB-PLT-WF Temporal workflow platform', 16),
    ('RWB-PLT-DB ACE DB schemas and logins', 2),
    ('RWB-PLT-EVT Kafka event platform', 3),
    ('RWB-PLT-EDGE Edge and gateway', 5),
    ('RWB-PLT-OBS Observability', 2),
    ('RWB-SVC-P1 rwb-source-data (Source data)', 62),
    ('RWB-SVC-P2 rwb-integration (Integration)', 27),
    ('RWB-SVC-P3 rwb-case (Case and workflow)', 84),
    ('RWB-SVC-P4 rwb-access (Access and authority)', 111),
    ('RWB-SVC-P5 rwb-document (Document)', 52),
    ('RWB-SVC-P6 rwb-comms (Communications)', 48),
    ('RWB-SVC-P7 rwb-decision (Decision and rules)', 52),
    ('RWB-SVC-P8 rwb-payment (Payment)', 21),
    ('RWB-SVC-P9 rwb-reporting (Reporting)', 12),
    ('RWB-SVC-P10 rwb-agent (Agent)', 40),
    ('RWB-SVC-S1 rwb-valuation (Valuation and route)', 24),
    ('RWB-SVC-S2 rwb-treatment (Treatment and offer)', 47),
    ('RWB-SVC-S3 rwb-guarantee (Guarantee)', 17),
    ('RWB-SVC-S4 rwb-litigation (Litigation)', 45),
    ('RWB-SVC-S5 rwb-asset (Asset)', 51),
    ('RWB-SVC-S6 rwb-debtsale (Debt sale)', 30),
    ('RWB-SVC-S7 rwb-writeoff (Write-off)', 32),
    ('RWB-SVC-S8 rwb-deviation (Deviation)', 31),
    ('RWB-SVC-S9 rwb-partner (Partner)', 36),
    ('RWB-ITG-W1 Wave 1 integration', 52),
    ('RWB-ITG-W2 Wave 2 integration', 43),
    ('RWB-ITG-W3 Wave 3 integration', 9),
    ('RWB-ITG-W4 Wave 4 integration', 41),
    ('RWB-ITG-NFR Non-functional integration', 2),
]

RUN = [
    ('Recovery Workbench Architecture v5 Text Extract v1.md', 'The text of the Architecture v5 deck, slide by slide. The first source in the precedence order (R3).'),
    ('Recovery Workbench Temporal and Drools Design Text Extract v1.md', 'The text of the Temporal and Drools detailed design deck. The second source in the precedence order (R3).'),
    ('Recovery Workbench Microservice Ownership Map v1.xlsx', 'The owner of every table, endpoint, event, workflow, job and ruling, with its basis. The owner table of this run.'),
    ('Recovery Workbench Microservice Story Template and Rules v1.md', 'The decisions U1 to U10, the source precedence, the service naming, the owner table, the dependency classes, the decoupling patterns, the template and the gap rules.'),
    ('Recovery Workbench Microservice Change Register v1.md', 'The change record of the realignment: what moved, which stories were disposed how, and the open points.'),
    ('Recovery Workbench Microservice Realignment Tracker v1.xlsx', 'The working list: documents, stories, decisions and defects with their status.'),
    ('Issue-tracker impact and follow-up v1', 'The issue-tracker impact of the realignment, held in one file in this folder and nowhere else (U6).'),
    ('Recovery Workbench Microservice Architecture by Epic and Story v1.excalidraw, Recovery Workbench Microservice Architecture by Epic and Story v1.svg', 'The large diagram for developers and architects: wave bands, epic frames, lanes and story boxes, by work type (U10).'),
    ('Recovery Workbench Wave 1 Architecture v1.excalidraw, Recovery Workbench Wave 1 Architecture v1.svg', 'The same diagram cut to wave 1.'),
    ('Recovery Workbench Wave 2 Architecture v1.excalidraw, Recovery Workbench Wave 2 Architecture v1.svg', 'The same diagram cut to wave 2.'),
    ('Recovery Workbench Wave 3 Architecture v1.excalidraw, Recovery Workbench Wave 3 Architecture v1.svg', 'The same diagram cut to wave 3.'),
    ('Recovery Workbench Wave 4 Architecture v1.excalidraw, Recovery Workbench Wave 4 Architecture v1.svg', 'The same diagram cut to wave 4.'),
    ('aisdlc/', 'The AI-SDLC context and the BRD and PRD builder inputs used to produce the requirements of R8.5 (U9).'),
]

FILES = {
 '1': 'Recovery Workbench Admin and Access Model v5.docx',
 '2': 'Recovery Workbench Decision Log v11.xlsx',
 '131': 'Recovery Workbench RWB-E1-001 Specification Rulings v2.md',
 '132': 'Recovery Workbench RWB-E1-001 Pre-Build Rulings v2.md',
 '133': 'Recovery Workbench Temporal and Drools Change Register v1.md',
 '134': 'Recovery Workbench Rule Story Retirements v1.md',
 '3': 'Recovery Workbench Engineering Practices v6.docx',
 '19': 'Recovery Workbench Ways of Working and Governance v3.docx, Recovery Workbench Ways of Working and Governance v3.pptx',
 '40': 'Recovery Workbench Release Plan v5.xlsx, Recovery Workbench Release Plan v4.pptx',
 '41': 'Recovery Workbench Dependency Map v5.xlsx',
 '42': 'Recovery Workbench Resource Plan and Team Structure v3.xlsx',
 '53': 'Recovery Workbench Build Sequence Epic 1 and Epic 2 v7.xlsx',
 '123': 'Recovery Workbench Story Build Order v4.docx',
 '67': 'Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx',
 '103': 'Recovery Workbench Benefit Tracking Plan v2.xlsx',
 '104': 'Recovery Workbench Cutover and Go Live Plan v4.docx',
 '105': 'Recovery Workbench Run Operating Model v2.docx, Recovery Workbench Run Operating Model v3.pptx',
 '106': 'Recovery Workbench Training and Change Plan v2.docx, Recovery Workbench Training and Change Plan v2.pptx',
 '4': 'Recovery Workbench AI Assisted Development Approach v1.md, Recovery Workbench AI Assisted Development Approach v3.pptx',
 '56': 'Recovery Workbench AI and Agent Architecture v2.docx, Recovery Workbench AI and Agent Architecture v3.pptx',
 '82': 'Recovery Workbench Agent Catalog and Specifications v2.md, Recovery Workbench Agent Catalog and Specifications v3.xlsx',
 '86': 'Recovery Workbench Model Integration Design v3.docx',
 '93': 'Recovery Workbench AI Decision Governance v2.docx',
 '5': 'Recovery Workbench Process Architecture v3.xlsx, Recovery Workbench Process Architecture v4.pptx',
 '6': 'Recovery Workbench Business Architecture v4.pptx',
 '7': 'Recovery Workbench Business Rules and Routing Logic v4.html, Recovery Workbench Business Rules and Routing Logic v4.xlsx',
 '8': 'Recovery Workbench Case and Workflow Model v5.html, Recovery Workbench Case and Workflow Model v6.xlsx',
 '15': 'Recovery Workbench Target Operating Model v3.pptx',
 '16': 'Recovery Workbench Users Roles and Permissions v5.xlsx',
 '21': 'Recovery Workbench Business Glossary v3.xlsx',
 '22': 'Recovery Workbench Detailed Process Flows v4.html, Recovery Workbench Detailed Process Flows v4.xlsx',
 '23': 'Recovery Workbench Deviation and Exception Catalog v3.xlsx',
 '24': 'Recovery Workbench Feature List v5.xlsx',
 '31': 'Recovery Workbench Case Journeys v3.pptx',
 '33': 'Recovery Workbench Delegation of Authority Matrix v2.xlsx',
 '43': 'Recovery Workbench Role to System Access Matrix v3.xlsx',
 '48': 'Recovery Workbench User Journeys v2.pptx',
 '58': 'Recovery Workbench Business Measures and Targets v2.xlsx',
 '64': 'Recovery Workbench Partner Operating Model v2.docx, Recovery Workbench Partner Operating Model v2.pptx',
 '115': 'Recovery Workbench Process Map v1.html',
 '9': 'Recovery Workbench Conceptual Data Model v6.pptx, Recovery Workbench Conceptual Data Model v7.xlsx',
 '11': 'Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx',
 '12': 'Recovery Workbench Entity Relationship Diagram v6.md',
 '26': 'Recovery Workbench Physical Schema v7 folder: 19 files, one per service schema, plus recovery_views.sql and README.md',
 '27': 'Recovery Workbench Volume and Scale Forecast v3.pptx, Recovery Workbench Volume and Scale Forecast v4.xlsx',
 '32': 'Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx',
 '38': 'Recovery Workbench Reference Data and Lists of Values v5.xlsx',
 '46': 'Recovery Workbench Source to Target Mapping v5.xlsx',
 '60': 'Recovery Workbench Data Ownership and Stewardship v4.xlsx',
 '61': 'Recovery Workbench Data Quality and Reconciliation Rules v4.xlsx',
 '65': 'Recovery Workbench Party and Customer Master Data Design v3.docx, Recovery Workbench Party and Customer Master Data Design v4.xlsx',
 '89': 'Recovery Workbench Reporting and Analytics Data Model v4.xlsx',
 '99': 'Recovery Workbench Data Migration Approach v4.docx',
 '124': 'Recovery Workbench ACE DB Alignment Change Register v1.md',
 '125': 'Recovery Workbench ACE Data Tier Map v1.md',
 '126': 'Recovery Workbench ACE Field Gap List v1.xlsx',
 '127': 'Recovery Workbench ACE Source Views v1.sql',
 '128': 'ACE Schema PostgreSQL v1.sql, ACE Schema Extract v1.csv, ACE-data-schema_20261104.xlsx',
 '129': 'Recovery Workbench ACE DB Alignment Tracker v1.xlsx',
 '10': 'Recovery Workbench Information Flow v6.pptx',
 '14': 'Recovery Workbench Target Architecture v6.docx, Recovery Workbench Target Architecture v7.pptx',
 '20': 'Recovery Workbench Architecture Decision Records v4.md',
 '25': 'Recovery Workbench System Disposition and Integration Inventory v4.xlsx',
 '34': 'Recovery Workbench Environment and Deployment Design v5.docx',
 '36': 'Recovery Workbench Interface Specifications v3.md, Recovery Workbench Interface Specifications v4.xlsx',
 '45': 'Recovery Workbench Security and Access Design v5.docx',
 '57': 'Recovery Workbench API Specification v5 folder: index.yaml, gateway-bff.yaml, 19 service files rwb-access.yaml to rwb-writeoff.yaml, 20 AsyncAPI files; Recovery Workbench API Specification v4.html',
 '63': 'Recovery Workbench Event and Messaging Design v4.md, Recovery Workbench Event and Messaging Design v5.xlsx',
 '68': 'Recovery Workbench Rules Engine Design v4.docx',
 '71': 'Recovery Workbench Workflow Engine Design v4.docx',
 '72': 'Recovery Workbench Audit and Logging Design v3.docx',
 '74': 'Recovery Workbench Batch and Scheduling Design v4.docx, Recovery Workbench Batch and Scheduling Design v5.xlsx',
 '76': 'Recovery Workbench Document Management Design v3.docx',
 '77': 'Recovery Workbench Error Handling and Resilience Standard v4.docx',
 '79': 'Recovery Workbench Notification and Correspondence Design v3.docx',
 '83': 'Recovery Workbench Availability Performance and Recovery Design v3.docx',
 '87': 'Recovery Workbench Observability and Monitoring Design v4.docx',
 '92': 'Recovery Workbench Technical Specifications by Module v6 folder: 19 module files',
 '113': 'Recovery Workbench ACE Architecture Decision v4.docx',
 '13': 'Recovery Workbench Project Overview v4.docx, Recovery Workbench Project Overview v5.pptx',
 '37': 'Recovery Workbench Project Deck v3.pptx',
 '47': 'Recovery Workbench Stakeholder Map and Communication Plan v3.xlsx',
 '54': 'Recovery Workbench Team Start Pack v2.html, Recovery Workbench Team Start Pack v3.pptx',
 '70': 'Recovery Workbench Weekly Status Pack v2.pptx',
 '107': 'Recovery Workbench Executive Presentation CEO v2.pptx',
 '108': 'Recovery Workbench Executive Presentation CTO v4.pptx',
 '110': 'Recovery Workbench Document Index v14.md',
 '114': 'Recovery Workbench Document Control Sheet v13.xlsx',
 '116': '12 Project communication\\Recovery Workbench Project Hub v15.html, 14 Story Updates\\Recovery Workbench Project Hub v17.html',
 '17': 'Recovery Workbench User Story Worked Example v7.md',
 '49': 'Recovery Workbench Administration Stories v4.md, Recovery Workbench Administration Stories v3.xlsx',
 '51': 'Recovery Workbench Technical Enabler Stories v8.md, Recovery Workbench Technical Enabler Stories v7.xlsx',
 '52': 'Recovery Workbench Service Story Files v1 folder, Recovery Workbench User Stories Epic 1 v10.md, Recovery Workbench User Stories Epic 1 v9.xlsx, Recovery Workbench User Stories Epic 1 Story Files v7.zip',
 '55': 'Recovery Workbench Service Story Files v1 folder, Recovery Workbench User Stories Epic 2 v8.md, Recovery Workbench User Stories Epic 2 v7.xlsx, Recovery Workbench User Stories Epic 2 Story Files v5.zip',
 '130': 'Recovery Workbench ACE Team Stories v2.md, Recovery Workbench ACE Team Stories v1.xlsx',
 '101': 'Recovery Workbench Data Migration Stories v4.md, Recovery Workbench Data Migration Stories v3.xlsx',
 '109': 'Recovery Workbench User Stories Epics 3 to 8 v4.md, Recovery Workbench User Stories Epics 3 to 8 v3.xlsx',
 '117': 'Recovery Workbench How To Read The Acceptance Criteria v2.docx',
 '118': 'Recovery Workbench Acceptance Criteria Glossary v2.xlsx',
 '119': 'Recovery Workbench Build Notes Epic 1 v7.md',
 '120': 'Recovery Workbench Build Notes Epic 2 v4.md',
 '122': 'Recovery Workbench Build Notes Technical Enablers v3.md',
 '121': 'Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v5.xlsx',
 '18': 'Recovery Workbench Definition of Ready and Done v4.docx',
 '69': 'Recovery Workbench Test Strategy v3.docx',
 '84': 'Recovery Workbench Defect Management Process v2.docx',
 '95': 'Recovery Workbench Non Functional Test Plan v3.docx',
 '96': 'Recovery Workbench Test Cases v8.xlsx',
 '97': 'Recovery Workbench Requirements Traceability Matrix v7.xlsx',
 '98': 'Recovery Workbench Test Data Plan v4.docx',
 '100': 'Recovery Workbench User Acceptance Test Plan v2.docx, Recovery Workbench User Acceptance Test Scripts v2.xlsx',
 '102': 'Recovery Workbench Regression Suite v7.xlsx',
 '28': 'Recovery Workbench Business Requirements Program v5.docx, Recovery Workbench Business Requirements Program v5.md',
 '29': 'Recovery Workbench Business Requirements Epic 1 v5.docx, Recovery Workbench Business Requirements Epic 1 v5.md',
 '30': 'Recovery Workbench Business Requirements Epic 2 v3.docx, Recovery Workbench Business Requirements Epic 2 v3.md',
 '50': 'Recovery Workbench Non Functional Specification v4.docx',
 '78': 'Recovery Workbench Functional Specifications by Module v7 folder: 19 module files',
 '85': 'Recovery Workbench Epics 3 to 8 Specification v3.docx, Recovery Workbench Epics 3 to 8 Specification v3.xlsx',
 '90': 'Recovery Workbench Reporting and Management Information Requirements v2.docx, Recovery Workbench Reporting and Management Information Requirements v2.xlsx',
 '111': 'Recovery Workbench Lean BRD Epic 1 v3.docx',
 '112': 'Recovery Workbench Lean BRD Epic 2 v2.docx',
 '35': 'Recovery Workbench Error and Message Standard v4.docx',
 '44': 'Recovery Workbench Screen Inventory and Navigation v2.xlsx',
 '62': 'Recovery Workbench Design System and Component Library v1.html',
 '75': 'Recovery Workbench Content and Label Standard v2.xlsx',
 '80': 'Recovery Workbench Screen Specifications v1.html, Recovery Workbench Screen Specifications v1.md',
 '81': 'Recovery Workbench Accessibility Standard v2.docx',
 '91': 'Recovery Workbench Screen Prototype v1.html',
 '94': 'Recovery Workbench Customer and Partner Correspondence Templates v2.docx',
 '39': 'Recovery Workbench Regulatory Requirements Map v3.xlsx',
 '59': 'Recovery Workbench Controls Catalog v4.xlsx',
 '66': 'Recovery Workbench Personal Data Protection Design v3.docx',
 '73': 'Recovery Workbench Audit Findings Response Map v2.xlsx',
 '88': 'Recovery Workbench Records Retention and Archiving v3.docx',
}

NEW_ROWS = {
 'Decisions': [('135', 'Microservice change register',
   'The decision record for D-RCV-60: the 19-service structure, the disposition of every legacy story, the document edit plan and the open points. The controlling document for this realignment.',
   'MADR', 'Recovery Workbench Microservice Change Register v1.md')],
 'Technical': [
   ('136', 'Service catalog', 'The 19 services with their resources, REST operations, events, workflows, naming, waves and call types, one row per service.', 'C4 model, arc42, ISO/IEC/IEEE 42010', 'Recovery Workbench Service Catalog v1.md, Recovery Workbench Service Catalog v1.xlsx'),
   ('137', 'Service template specification', 'The one shape every service is built from: schema and login, REST base, topic, task queue, library set, pipeline and definition of done.', 'C4 model, arc42, ISO/IEC/IEEE 42010', 'Recovery Workbench Service Template Specification v1.md'),
   ('138', 'Service contract catalog', 'Every contract between services: REST operations, events, Temporal contracts and jobs, with the contract pairs, the resources owned and the conformance check.', 'OpenAPI 3.1, AsyncAPI 3.0', 'Recovery Workbench Service Contract Catalog v1.md, Recovery Workbench Service Contract Catalog v1.xlsx'),
   ('139', 'Kafka topic and event catalog', 'Every topic, retry topic and dead-letter topic, every event with its envelope, the outbox and inbox tables, the access rules and the delivery rules.', 'AsyncAPI 3.0', 'Recovery Workbench Kafka Topic and Event Catalog v1.xlsx'),
   ('140', 'Temporal workflow and activity catalog', 'Every workflow, activity and Schedule, the task queues and namespaces, the platform rules and the open points.', 'CMMN 1.1', 'Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx'),
 ],
 'Quality': [('141', 'Integration test plan', 'How the wave integration suites are run: the harness RWB-ITG-W1J01, the environments, the entry and exit criteria and the pass marks.', 'ISO/IEC/IEEE 29119', 'Recovery Workbench Integration Test Plan v1.docx')],
 'Requirements': [
   ('142', 'Business requirements, Epics 3 to 8', 'The business scope of each of Epics 3 to 8 for sign-off, in the same form as the Epic 1 and Epic 2 BRDs.', 'ISO/IEC/IEEE 29148', 'Recovery Workbench Business Requirements Epics 3 to 8 v1.docx, Recovery Workbench Business Requirements Epics 3 to 8 v1.md'),
   ('143', 'PRDs, one per service and Platform', 'The product requirements of each service: scope, contract, data, state, rules, acceptance and traceability, one file per service plus Platform.', 'ISO/IEC/IEEE 29148', '20 files in 03 Requirements and specifications\\PRD: PRD P1 rwb-source-data v1.md to PRD S9 rwb-partner v1.md (19 service files) and PRD PLT Platform v1.md'),
 ],
 'Backlog': [
   ('144', 'Service story files, all epics', 'Every story of the 31 service, platform and integration epics in the 19-section template, one file per story, with an epic overview in each folder.', 'Connextra form, INVEST, Gherkin', 'Recovery Workbench Service Story Files v1 folder: 1,034 story files and 31 epic overviews'),
   ('145', 'Service epics', 'The 31 epics: their service, wave, story count, work-type split and the stories they hold.', 'Connextra form, INVEST, Gherkin', 'Recovery Workbench Service Epics v1.md'),
   ('146', 'Day-1 work allocation', 'The Day-1 work of each team type, story by story, with the contract it builds against.', 'Henka excel rules', 'Recovery Workbench Day-1 Work Allocation v1.xlsx'),
   ('147', 'Service story catalog', 'Every story with its lane, wave, release, suggested owner, dependencies and contract, filtered every way the squads need.', 'Henka excel rules', 'Recovery Workbench Service Story Catalog v1.xlsx'),
 ],
}

def microservice_section():
    L = []
    L.append('## Microservice realignment')
    L.append('')
    L.append('Read by: Sponsors, programme manager, solution architects, tech leads, data steward, squads.')
    L.append('')
    L.append('Decision D-RCV-60 of 22 November 2026 adopts Architecture v5. Recovery stays inside ACE and is split into 19 services, '
             'one per business module P1 to P10 and S1 to S9; each service has its own deployment, schema rwb_<name>, login, REST base '
             '/api/recovery/<short>/v1, topic rwb.<short>.events.v1 with retry and dead-letter topics, Temporal task queue rwb-<short> '
             'and epic RWB-SVC-<code>. Seven platform epics RWB-PLT-* build the template, the libraries, the workflow platform, the '
             'database, the event platform, the edge and observability; four wave integration epics RWB-ITG-W1 to W4 and RWB-ITG-NFR '
             'test them. Every story also carries its business epic EP01 to EP08 as a tag, and the 19 do not replace the eight.')
    L.append('')
    L.append('The realignment holds 1,034 story files in 31 epic folders, one for every legacy key in the split plan: 358 legacy keys, '
             '822 service stories, 65 platform stories and 147 integration stories. 939 stories are ready on Day 1, across the five '
             'team types TechX, ACE, SCB IT infrastructure, DevOps and QA (R5.3, R5.7), in 510 parallel lanes. Epic 1 work already built '
             'keeps its base ID and its text, and the microservice change sits in separate delta stories (U2; R6).')
    L.append('')
    L.append('### The 19 services')
    L.append('')
    L.append('Every value in this table is copied character for character from the Services sheet of the Ownership Map, which is also '
             'the owner of each row: the code in the first column owns the service, the schema, the REST base, the topic and the queue.')
    L.append('')
    L.append('| Code | Service | Name | Wave | Schema | REST base | Topic | Task queue | Epic |')
    L.append('|---|---|---|---|---|---|---|---|---|')
    for c, s, n, w, sc, r, t, q in SERVICES:
        L.append(f'| {c} | {s} | {n} | {w} | {sc} | {r} | {t} | {q} | RWB-SVC-{c} |')
    L.append('')
    L.append('### The story sets')
    L.append('')
    L.append('One folder per epic, under 04 User stories\\Recovery Workbench Service Story Files v1. The suggested owner of every story '
             'inside a folder follows its work type (R5.3); the folder itself belongs to the service or platform epic in its name.')
    L.append('')
    L.append('| Epic folder | Story files |')
    L.append('|---|---|')
    for n, c in STORY_SETS:
        L.append(f'| {n} | {c} |')
    L.append('| Total | 1,034 |')
    L.append('')
    L.append('### Every new and next version')
    L.append('')
    L.append('One row per document whose files were added or moved to a new version in this realignment. The # is the document number '
             'used in the sections below, so the two can be read together. A row that names two or three files keeps the older file '
             'where only one format was rebuilt; the Document gaps section says which.')
    L.append('')
    L.append('| # | Document | Files at this version |')
    L.append('|---|---|---|')
    for k in ORDER:
        L.append(f'| {k} | {DOCNAME[k]} | {FILEMAP[k]} |')
    L.append('')
    L.append('### Run material in folder 22')
    L.append('')
    L.append('The realignment itself, its registers and its diagrams are assets of the document set too. They sit in '
             '22 Microservice Realignment and carry D-RCV-60.')
    L.append('')
    L.append('| File | What it is |')
    L.append('|---|---|')
    for f, d in RUN:
        L.append(f'| {f} | {d} |')
    L.append('')
    return L

GAPS = [
 ('1', 'The story master workbooks are not at the new version',
  'The seven story masters were assembled as Markdown only: User Stories Epic 1 v10.md, User Stories Epic 2 v8.md, User Stories Epics 3 to 8 v4.md, Administration Stories v4.md, Technical Enabler Stories v8.md, ACE Team Stories v2.md and Data Migration Stories v4.md. Their workbooks stay at v9, v7, v3, v3, v7, v1 and v3.',
  'Missing', 'P3', 'Product owner', 'The index lists the Markdown at its new version and the workbook at the version found; the two are not read as one pair.'),
 ('2', 'Some document families advanced in one format only',
  'Batch and Scheduling Design (docx v4, xlsx v5), Event and Messaging Design (md v4, xlsx v5), Interface Specifications (md v3, xlsx v4), Release Plan (pptx v4, xlsx v5), Run Operating Model (docx v2, pptx v3), Agent Catalog (md v2, xlsx v3), Process Architecture (xlsx v3, pptx v4), Case and Workflow Model (html v5, xlsx v6), Conceptual Data Model (pptx v6, xlsx v7) and Volume and Scale Forecast (pptx v3, xlsx v4) each hold two versions in one family.',
  'Ambiguous', 'P3', 'TechX', 'The index lists both files with their own version, so no reader takes the older one for the current text.'),
 ('3', 'The specifications are folders without an archive',
  'Technical Specifications by Module v6, Functional Specifications by Module v7 and Physical Schema v7 exist as folders of module files; the source set carried the first two as .zip archives (v5.zip and v6.zip) and the physical schema as one .sql file (v6.sql).',
  'Missing', 'P3', 'TechX', 'The index names the folder and its contents instead of an archive that does not exist.'),
 ('4', 'The API specification has no single-file rendering at v5',
  'API Specification v5 is a folder of index.yaml, gateway-bff.yaml, 19 service files and 20 AsyncAPI files. The last single-file HTML rendering is API Specification v4.html.',
  'Missing', 'P3', 'TechX', 'The index lists the v5 folder and keeps v4.html named as the previous rendering.'),
 ('5', 'The entity relationship diagram is Markdown only at v6',
  'Entity Relationship Diagram v6.md exists; the HTML and PDF renderings stay at v5.',
  'Missing', 'P3', 'Data steward', 'The index lists v6.md and does not present the v5 rendering as current.'),
 ('6', 'The realignment tracker is at v1',
  'The run material list in R8.3 names a tracker v2; only Microservice Realignment Tracker v1.xlsx is in folder 22.',
  'Missing', 'P3', 'Programme manager', 'The index lists v1 as it stands.'),
 ('7', 'The run summary is not in folder 22',
  'The run material list in R8.3 names a Run Summary v1; no such file is in folder 22 at this version.',
  'Missing', 'P3', 'Programme manager', 'The index lists the run material that exists and records this one as a gap.'),
 ('8', 'Documents outside the realignment keep their previous version',
  'Business Rules and Routing Logic v4, Detailed Process Flows v4, Screen Inventory and Navigation v2, Error and Message Standard v4 and the other Experience documents were not rebuilt under D-RCV-60. The index records the version the files hold.',
  'Outdated', 'P3', 'Business lead', 'The index shows the version on disk; it does not claim the document matches the 19-service target.'),
 ('9', 'The project hub carries two version-15 files',
  'Project Hub v15.html was issued into 12 Project communication by this run, and 14 Story Updates already holds Project Hub v15.html of 12 November 2026, v16.html and v17.html. The same version number therefore names two different files in two folders.',
  'ID collision', 'P3', 'Programme manager', 'The index lists both files with their folders and gives the highest version, v17, as the current project hub.'),
]

CHANGELOG = [
 ('14', '22 November 2026', 'D-RCV-60 microservice realignment', 'T3 Code / OpenCode / DeepSeek v4.1 Flash'),
 ('13', '16 November 2026', 'Document set at version 13, carrying D-RCV-35 and D-RCV-36', 'Source row'),
]

def gaps_section():
    L = []
    L.append('## Document gaps')
    L.append('')
    L.append('Read by: Programme manager, document owners, squads.')
    L.append('')
    L.append('What the files of this set cannot show, at the version recorded above. Each row is a candidate gap: step D1 numbers '
             'them in the Gap Register and the Assumptions Register in folder 23, and the candidate rows of this work package sit in '
             '_work/msr/gaps/D2-IDX.jsonl and _work/msr/assumptions/D2-IDX.jsonl. No row blocks a wave start.')
    L.append('')
    L.append('| Gap | What the index cannot show | Type | Severity | Owner role | How the index handles it |')
    L.append('|---|---|---|---|---|---|')
    for gid, title, desc, typ, sev, role, how in GAPS:
        L.append(f'| CG-D2-IDX-{gid} | {title}. {desc} | {typ} | {sev} | {role} | {how} |')
    L.append('')
    L.append('The assumptions behind these rows and behind the version numbers in this file are ASM-D2-IDX-1 to ASM-D2-IDX-11.')
    L.append('')
    L.append('## Change log')
    L.append('')
    L.append('| Version | Date | Change | Tool |')
    L.append('|---|---|---|---|')
    for v, d, c, t in CHANGELOG:
        L.append(f'| {v} | {d} | {c} | {t} |')
    L.append('')
    L.append('Change-log row: 14, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.')
    L.append('')
    return L

DOCNAME = {}
FILEMAP = dict(FILES)
src = io.open(SRC, encoding='utf-8').read().splitlines()
for line in src:
    if line.startswith('| ') and line.count('|') >= 6:
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == 5 and re.match(r'^\d+$', cells[0]):
            DOCNAME[cells[0]] = cells[1]
for sec, rows in NEW_ROWS.items():
    for r in rows:
        DOCNAME[r[0]] = r[1]
        FILEMAP[r[0]] = r[4]

ORDER = ['2','135',
         '3','40','41','42','53','123','67','104','105',
         '56','82','86',
         '8','16','24',
         '9','11','12','26','27','32','38','46','60','61','65','89','99',
         '10','14','20','25','34','36','45','57','63','68','71','72','74','76','77','79','83','87','92','113',
         '136','137','138','139','140',
         '13','54','108','110','114','116',
         '17','49','51','52','55','130','101','109','117','118','119','120','122','121',
         '144','145','146','147',
         '18','69','95','96','97','98','102','141',
         '28','29','30','50','78','142','143',
         '39','59','66','88']

body = []
i = 0
while i < len(src):
    line = src[i]
    if line.startswith('## '):
        break
    i += 1
cur = None
pending = []
def flush():
    for r in pending:
        body.append('| ' + ' | '.join(r) + ' |')
    del pending[:]

while i < len(src):
    line = src[i]
    if line.startswith('## '):
        flush()
        cur = line[3:].strip()
        body.append(line)
        i += 1
        continue
    m = re.match(r'^\| (\d+) \|', line)
    if m and line.count('|') == 6:
        num = m.group(1)
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        cells[4] = FILES[num]
        body.append('| ' + ' | '.join(cells) + ' |')
        i += 1
        continue
    body.append(line)
    i += 1
flush()

out = []
out += HEADER
out.append(INTRO)
out.append('')
out.append(INTRO2)
out.append('')
out += microservice_section()
out += body
# append new rows at the end of their sections is already handled? no - insert before the next heading
# Rebuild with insertion
text = '\n'.join(out) + '\n'

# Insert new rows at the end of each section: find heading, then last table row of that section
for sec, rows in NEW_ROWS.items():
    marker = '## ' + sec + '\n'
    p = text.index(marker) + len(marker)
    q = text.find('\n## ', p)
    if q == -1:
        q = len(text)
    chunk = text[p:q]
    lines_ = chunk.split('\n')
    # last non-empty line that is a table row
    idx = max(k for k, l in enumerate(lines_) if l.startswith('|'))
    newrows = ['| ' + ' | '.join(r) + ' |' for r in rows]
    lines_[idx + 1:idx + 1] = newrows
    text = text[:p] + '\n'.join(lines_) + text[q:]

text = text.rstrip('\n') + '\n\n' + '\n'.join(gaps_section())

io.open(DST, 'w', encoding='utf-8', newline='\n').write(text)
print('written', DST, len(text.splitlines()), 'lines')

