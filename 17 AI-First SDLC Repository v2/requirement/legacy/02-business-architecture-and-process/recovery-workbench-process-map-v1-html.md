<!-- source: 02 Business architecture and process/Recovery Workbench Process Map v1.html -->
<!-- converted: 2026-11-16 from HTML -->

> **Source:** `02 Business architecture and process/Recovery Workbench Process Map v1.html`  
> **Converted from:** HTML

Recovery Workbench process map

# Recovery Workbench process map

The case journey from bucket 3 to 4 through charge-off. 82 steps across 7 stages.

## The case journey, stage by stage

Every step from the hand-over out of collections through to write-off, with the capability it needs, where its data comes from, and how it runs.

82Steps47AI autonomous20Manual15AI assisted

## How a step runs

AI autonomous a rule, engine or agent completes the step with no person; a person sees the result in the log. AI assisted an agent or engine prepares, recommends or drafts; a person decides, approves or completes. Manual a person or a partner does the step; the Workbench prepares the task and records the result.

## The stages

| Stage | Stage | Steps | Modules | Decision |
|---|---|---|---|---|
| 0 | Hand-over from collections (bucket 3 to 4) | 8 | P1, P2, P3 | D6 entry |
| 1 | Which route (D6.1 to D6.3) | 11 | S1, P7, P10 |  |
| 2 | Settle, deed in lieu, TDR, guarantees (D6.4 to D6.6; D5 after TDR go-live) | 18 | S2, S3, P6, P8 |  |
| 3 | Litigate and enforce (D7) | 13 | S4, P5, P6, S9 |  |
| 4 | Dispose of assets (D8.1 to D8.3) | 13 | S5, P2, P8 |  |
| 5 | Sell debt (D8.4) | 10 | S6, P2, P8 |  |
| 6 | Write off and after (D9) | 9 | S7, P8 |  |

## Stage 0. Hand-over from collections (bucket 3 to 4)

8 steps. Modules P1, P2, P3. Decision D6 entry.

| Step | Step | What is needed | Data comes from | Mode | Module |
|---|---|---|---|---|---|
| 0.1 | Daily feed of balances, DPD, classification | Data load engine; account and arrears data product | ALS (batch via ADF, Control-M); iCore as accounts migrate | AI autonomous | P1 |
| 0.2 | Collections status and contact history arrives | EFS extract or case.transferred event | EFS (daily file; Kafka event when available); ACE for plan status | AI autonomous | P2 |
| 0.3 | Rule: 90 DPD reached and not excluded (deceased, fraud, bankruptcy, active TDR plan, open dispute) | Rule engine; entry and exclusion rules | Account and arrears; EFS flags; ACE plan status; reference data | AI autonomous | P3 |
| 0.4 | Create the recovery case; pull history | Case engine; case and ownership data product | EFS history; PACMAN customer, product and account 360 | AI autonomous | P3 |
| 0.5 | Assign one case owner by rule | Allocation engine; routing rules (product, region, exposure, workload) | Reference data; case list | AI autonomous | P3 |
| 0.6 | Screen for deviations X1 to X7 | Deviation screening agent; rules | Data products, call notes, documents, NCB, Aric | AI assistedagent flags, owner confirms | S8, P10 |
| 0.7 | Set timers and prescription dates | Timer engine; service levels | Reference data; legal periods | AI autonomous | P3 |
| 0.8 | Owner reviews the case record view and confirms contacts | Case record view screen; contact and promises data product | EFS contacts; PACMAN | Manual | P3, P7 |

## Stage 1. Which route (D6.1 to D6.3)

11 steps. Modules S1, P7, P10.

| Step | Step | What is needed | Data comes from | Mode | Module |
|---|---|---|---|---|---|
| 1.1 | Assemble the case facts | Case data engine; data products | ALS, EFS, CCMS, SVAF, LHS, the Workbench document hub | AI autonomous | P1 |
| 1.2 | Rule: appraisal older than the limit; order appraisal | Rule engine; SVAF adapter | CCMS, SVAF | AI autonomous | S1, P2 |
| 1.3 | Valuer inspects and reports | Partner portal; appraisal callback | SVAF; valuer | Manualpartner | S1 |
| 1.4 | Flag appraisal outliers against market and last value | Valuation agent | SVAF, market data, Land Office prices | AI assisted | P10 |
| 1.5 | Accept the appraisal value (D6.1) | Approval screen; decision log | Workbench | AI assistedperson accepts | S1, P7 |
| 1.6 | Return by route (D6.2) | COLLINS model gateway | COLLINS (Databricks) | AI autonomous | P10 |
| 1.7 | Rule: payoff and settlement range | Rule engine; ranges and floors rules | ALS payoff via EAPI; reference data | AI autonomous | S1 |
| 1.8 | Route agent recommends with reasons (D6.3) | Path recommender agent | Data products; COLLINS; documents | AI assisted | P10 |
| 1.9 | Route to the approver by delegation | Approval router; delegation of authority table | Reference data | AI autonomous | P7 |
| 1.10 | Approver approves, changes, rejects or asks | Decision center screen | Workbench | Manualapprove | P7 |
| 1.11 | Log the decision; start the route flow; set timers | Decision log writer; workflow | Workbench | AI autonomous | P7, P3 |

## Stage 2. Settle, deed in lieu, TDR, guarantees (D6.4 to D6.6; D5 after TDR go-live)

18 steps. Modules S2, S3, P6, P8.

| Step | Step | What is needed | Data comes from | Mode | Module |
|---|---|---|---|---|---|
| 2.1 | Generate the settlement or TDR offer letter | Letter engine; templates | Case facts; rules | AI autonomous | P6 |
| 2.2 | Send by SMS, LINE, registered mail (WIN) | Channel engine; WIN adapter | NSS, LINE, WIN | AI autonomous | P6 |
| 2.3 | Owner explains the offer; negotiates within the range | Negotiation copilot; scripts | Case facts; ranges | AI assisted | S2, P10 |
| 2.4 | Customer responds, counter-offers or accepts | Self-service (LINE, web); phone; field | Customer | Manualcustomer | P6 |
| 2.5 | TDR: pre-assess affordability; calculate the plan | ACE affordability and plan calculation (TDR program waves 1 and 2) | ACE; COLLINS | AI autonomousin ACE | S2 via ACE |
| 2.6 | Approve within delegation; deviation to head of credit | Approval router; rules | Delegation of authority | AI assistedauto-approve pre-approved programs; person for deviation; 44% deviate today | P7 |
| 2.7 | Generate the agreement or contract (TDR, settlement, DIL, mortgage documents) | Document generation; templates (DIL wave 1: auto-gen CA, contract, mortgage documents) | Case facts; CCMS; title data | AI autonomous | P5, P6 |
| 2.8 | Customer signs: e-sign (EasyApp, TDR wave 3), branch, field; DIL stays wet ink (Legal) | E-signature adapter; field app | Customer | Manualcustomer | P6 |
| 2.9 | Book terms in ALS or submit plan to NLEADS; set schedule and timers | ALS and NLEADS adapters; timer engine | ALS, NLEADS | AI autonomous | P8, P2 |
| 2.10 | Match payments to the plan; detect broken plans | Payment matching engine; plan.payment.missed event | ALS payments; CPX | AI autonomous | P8 |
| 2.11 | DIL: early appraisal and eligibility (encumbrance check) before negotiation | Rule-based prioritization; AI preliminary valuation for 90% of leads; fast lane official appraisal for top 10% | SVAF; Land Office; CCMS; photos | AI assisted | S2, P10 |
| 2.12 | DIL: collateral inspection, checklist, bills captured | Field app capture into ACE or the Workbench | FCR, DRO; photos; bills | Manualfield | S2, S9 |
| 2.13 | DIL: unlock the asset as NPA | Rule-based auto-unlock (about 95% qualify); AI summary for the approver on the rest | Inspection data; checklist | AI autonomouswith AI assisted exceptions | S2 |
| 2.14 | DIL: transfer ownership at the Land Office; record the NPA in AMIS | Partner and officer step; AMIS adapter records it | Land Office; AMIS | Manualtransfer) then AI autonomous (register | S2, S5 |
| 2.15 | Settle the debt, close the account, release collateral in CCMS | ALS, GL, CCMS adapters | ALS, GL, CCMS | AI autonomous | P8 |
| 2.16 | DIL buyback: rental record, auto-debit, receipts, arrears follow-up | Fee engine; ATS adapter | AMIS; ATS; Lead | AI autonomous | P8 |
| 2.17 | TCG guarantee claim prepared and submitted | Claim preparation agent; TCG portal | Case facts; TCG | AI assisted | S3 |
| 2.18 | Guarantor and co-borrower notices; negotiation | Letter engine; owner | Party data; DMS | AI autonomousnotices), Manual (negotiate | S3, P6 |

## Stage 3. Litigate and enforce (D7)

13 steps. Modules S4, P5, P6, S9.

| Step | Step | What is needed | Data comes from | Mode | Module |
|---|---|---|---|---|---|
| 3.1 | Generate demand and recall notices (D7.1) | Letter engine; templates approved by Legal | Case facts | AI autonomous | P6 |
| 3.2 | Print, sign, courier; proof of delivery back | WIN adapter; proof-of-delivery callback | WIN | AI autonomousdispatch and proof), Manual (sign where required | P6 |
| 3.3 | Notice period timer | Timer engine | Reference data | AI autonomous | P3 |
| 3.4 | Assemble the litigation pack; check completeness; request missing (D7.2) | Legal document agent; document checklist | Document hub; CCMS; LHS; the Workbench document hub | AI assisted | P5, P10 |
| 3.5 | Legal officer verifies the pack; approves filing | Verification screen | Workbench | Manualapprove | S4 |
| 3.6 | Select the law firm from the panel (D7.3); instruct through the portal | Rule engine (panel performance); portal adapter | Partner performance data; LIT lawyer web | AI autonomous | S4, S9 |
| 3.7 | Law firm files; uploads receipt | Portal | Law firm; courts | Manualpartner | S9 |
| 3.8 | Track hearings, deadlines and fees | Case tracking agent; timer engine; fee engine | LIT; law firm reports | AI autonomous | P10, P8 |
| 3.9 | Settle before judgment, appeal, pay fees (D7.4) | Agent proposes; person approves | Case facts | AI assisted | S4 |
| 3.10 | Judgment received | Portal or LIT event | Courts via law firm | AI autonomousrecord | S4 |
| 3.11 | Trace assets for enforcement | Asset trace agent | NCB, registries, insurers | AI assisted | P10 |
| 3.12 | Writ, seizure, LED auction; bankruptcy petition approval (D7.5) | Legal officer; LED; partner | LED; law firm | Manualpartner and approve | S4 |
| 3.13 | Match proceeds to the case | Reconciliation agent; ALS adapter | ALS; LED | AI autonomous | P8 |

## Stage 4. Dispose of assets (D8.1 to D8.3)

13 steps. Modules S5, P2, P8.

| Step | Step | What is needed | Data comes from | Mode | Module |
|---|---|---|---|---|---|
| 4.1 | Repossession order or DIL transfer | Rule and letter engines | Case facts | AI autonomous | S5, P6 |
| 4.2 | Repossession agent collects (field app) | Field app; RPS | Repossession partner; RPS | Manualpartner | S9 |
| 4.3 | Record the asset; holding age; provision steps (D8.1) | Asset engine; AMIS adapter | AMIS; RPS; CCMS | AI autonomous | S5 |
| 4.4 | Order appraisal; re-appraise on cycle | SVAF adapter | SVAF | AI autonomous | S5 |
| 4.5 | Propose start and floor price (D8.2) | Pricing agent with COLLINS | AMIS; SVAF; market data | AI assisted | P10 |
| 4.6 | NPA head approves the floor price | Approval screen | Workbench | Manualapprove | P7 |
| 4.7 | Publish the listing; schedule rounds | Auction portal adapter; HOME.SCB | Auction portal | AI autonomous | S5 |
| 4.8 | Bidders sign up, view and bid | Portal | Bidders | Manualpartner | S5 |
| 4.9 | Run Dutch auction rounds to the floor; re-list on no bid | Auction engine; rules | Auction portal | AI autonomous | S5 |
| 4.10 | Complete the sale; receive payment | NPA officer | Payments | Manual | S5 |
| 4.11 | Transfer title: DLT via SCIS, or Land Office | SCIS adapter; officer | SCIS; Land Office | AI autonomousvehicle), Manual (property | S5 |
| 4.12 | Apply proceeds; residual to D9 or close | ALS adapter; rules | ALS | AI autonomous | P8 |
| 4.13 | RAMC transfer, buy-back, rental (D8.3) | Agent proposes; person approves | Case facts | AI assisted | S5 |

## Stage 5. Sell debt (D8.4)

10 steps. Modules S6, P2, P8.

| Step | Step | What is needed | Data comes from | Mode | Module |
|---|---|---|---|---|---|
| 5.1 | Rule: eligible accounts for sale | Rule engine | Account and arrears; COLLINS | AI autonomous | S6 |
| 5.2 | Build lots; estimate price | Lot agent with COLLINS | Data products | AI assisted | P10 |
| 5.3 | Approve lots, reserve price and terms | Committee screen | Workbench | Manualapprove | P7 |
| 5.4 | Prepare the data tape and the data room (masked) | Data engine; PII service; portal | Data products | AI autonomous | S6, P1 |
| 5.5 | Buyers sign the NDA, review and bid | Buyer portal | Buyers | Manualpartner | S6 |
| 5.6 | KYC, licensing and eligibility check | Rule engine | Buyer data; registries | AI autonomous | S6 |
| 5.7 | Confirm buyers; award the lot | Approval screen | Workbench | Manualapprove | P7 |
| 5.8 | Generate the sale agreement and notices; sign; receive payment | Letter engine; signatory | Templates | AI autonomousgenerate), Manual (sign | P6 |
| 5.9 | Transfer data; derecognize; post GL | Data engine; ALS and GL adapters | ALS, GL | AI autonomous | P8 |
| 5.10 | Buyer put-back claims reviewed; lot closed | Debt sale officer | Buyer claims | Manual | S6 |

## Stage 6. Write off and after (D9)

9 steps. Modules S7, P8.

| Step | Step | What is needed | Data comes from | Mode | Module |
|---|---|---|---|---|---|
| 6.1 | Rule: eligibility and tax criteria (D9.1) | Rule engine | Account and arrears; COLLINS; tax rules | AI autonomous | S7 |
| 6.2 | Prepare the write-off pack (D9.2) | Write-off agent | Data products; documents | AI assisted | P10 |
| 6.3 | Route to the committee; schedule | Workflow | Reference data | AI autonomous | P3 |
| 6.4 | Committee decides: approve, reject, defer | Committee screen | Workbench | Manualcommittee | P7 |
| 6.5 | Post to ALS and GL; provisions; tax file | ALS, GL, Finance adapters | ALS, GL | AI autonomous | P8 |
| 6.6 | Rule: post charge-off treatment; place with an OA (D9.3) | Rule engine; OA portal | Partner data | AI autonomous | S7, S9 |
| 6.7 | OA works the account; results back | OA portal | Outside agency | Manualpartner | S9 |
| 6.8 | Match recoveries; income; OA fees | Matching and fee engines | ALS; OA files | AI autonomous | P8 |
| 6.9 | Close the case after the retention period | Rule engine | Reference data | AI autonomous | P3 |
