
Scale only what is busy: a steady front, an elastic back

All 19 services have the same shape; only the background workers grow

ONE SERVICE, FOR EXAMPLE rwb-document

screen requests

API

API

Front: 2 fixed copies

Its task queue

KEDA
watches the queue

Workers: 0 to many

add / remove

Back: grows with the queue

own schema (ACE DB)

Busy times and places

05:00-07:00 morning run
rwb-case, rwb-payment, rwb-deviation

Document intake and text reading
rwb-document, rwb-agent: bursts of uploads

16:00 letters and notices
rwb-comms, rwb-integration

AI agent runs
rwb-agent: 60 s, or the rule result is used

23.6k → 47k  open cases, today to 2031

~420  concurrent users

64-74k  documents a month

< 2 s  screen target (95%)

Volumes are modest: we split for reuse, ownership and isolation, and add capacity only where work piles up.

33

Notes: Each service is deployed as two parts: an API deployment (2 pods for availability, scaled on CPU or requests if ever needed) and a worker deployment scaled by KEDA on the Temporal task-queue backlog or Kafka consumer lag, down to zero for bursty work such as OCR or agent runs.

Volumes (recovery-architecture.pptx; Volume and Scale Forecast v3; NFR Spec v3): about 23,600 open cases today, 47,389 by 2031; about 420 concurrent users (about 21 requests a second at peak); 64-74k documents a month (2.8 TB by 2031); 283-318k rule evaluations a month.

Cost of 19 services: about 38 small deployments at rest (most workers idle at minimum), one Helm chart and one pipeline template. The ACE database sees capped pools per service.

