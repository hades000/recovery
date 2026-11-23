
Choosing the call type: four questions

Ask in order; the first yes decides

Q1

Is a person waiting on the screen?

no

Q2

Did something happen that others may care about?

no

Q3

Must another service do a step, and we need the result?

no

Q4

Bulk data, or a party outside the bank?

Is it a read, or one quick command in one service?

yes

REST call to the owner
one hop from gateway-bff; 2 s budget

Start a Temporal workflow
return its ID; screen shows progress

yes

no

Publish an event (Kafka)
past tense fact; IDs only; outbox

Temporal activity, child workflow or Nexus
short step / long stage / another workbench

File through rwb-integration
claim-check: link + manifest, never the data

yes

yes

yes

Need ACE data?  Ask rwb-source-data (REST for screens, activity in workflows). Only rwb-source-data reads the SQL views, so a change in ACE is absorbed in one place.

Events announce, Temporal commands, REST answers people: never mix the three.

12

Notes: This decision guide is part of the engineering standard. Typical examples: officer opens a case (REST); a payment is missed (event PaymentMissed); the case workflow needs a route decision (child workflow on rwb-valuation); rwb-litigation needs a law firm instructed (activity issueInstruction on rwb-partner); daily WIN letters (file through rwb-integration); restructure calculation in ACE (Nexus operation).

Anti-patterns rejected in review: REST from one service to another inside a business step (use Temporal); events used as commands (use Temporal); a service reading another service's schema (use its API); a workflow calling REST directly from workflow code (wrap it in an activity).

