# RWB-SVC-S6 rwb-debtsale (Debt sale) - review pack, part 2 of 3 (RWB-S6-E6004-CON to RWB-S6-E6011-CON)

Decision: D-RCV-60. Date: 26 November 2026. Status: Draft (directive resolutions). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Directive run result for this service: every gap and assumption was resolved with the recommended resolution, except business decisions. Review this pack, then the staged story files it lists. Row IDs (ruling R-, item GAP-/ASM-/CG-, CDC-) match the master registers in 23 Document Gaps.

## 1. Summary

| Measure | Count |
|---|---|
| Stories | 15 |
| Resolved in the stories | 293 |
| Cross-document (pending in another document) | 265 |
| Not applied (value not in the sources) | 5 |
| Open business decisions | 74 |
| Register gaps linked | 47 |
| Unconfirmed assumptions | 0 |
| Lint findings | 0 |

## 2. Stories (staged next version)

| Story | Resolved | Cross-document | Not applied | File |
|---|---|---|---|---|
| RWB-S6-E6004-CON | 12 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6004 CON Take buyer bids - contract v2.md |
| RWB-S6-E6005-APP | 35 | 31 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6005 APP Award the lot and test the price v2.md |
| RWB-S6-E6005-CON | 20 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6005 CON Award the lot and test the price - contract v2.md |
| RWB-S6-E6006-APP | 29 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6006 APP Generate the sale agreement and notices v2.md |
| RWB-S6-E6006-CON | 18 | 15 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6006 CON Generate the sale agreement and notices - contract v2.md |
| RWB-S6-E6007-APP | 21 | 22 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6007 APP Transfer the data to the buyer v2.md |
| RWB-S6-E6007-CON | 13 | 16 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6007 CON Transfer the data to the buyer - contract v2.md |
| RWB-S6-E6008-APP | 32 | 16 | 1 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6008 APP Derecognize and post to the general ledger v2.md |
| RWB-S6-E6008-CON | 13 | 18 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6008 CON Derecognize and post to the general ledger - contract v2.md |
| RWB-S6-E6009-APP | 20 | 19 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6009 APP Handle a buyer put-back claim v2.md |
| RWB-S6-E6009-CON | 12 | 15 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6009 CON Handle a buyer put-back claim - contract v2.md |
| RWB-S6-E6010-APP | 18 | 17 | 2 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6010 APP Close a case awarded in a sold lot v2.md |
| RWB-S6-E6010-CON | 12 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6010 CON Close a case awarded in a sold lot - contract v2.md |
| RWB-S6-E6011-APP | 24 | 17 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6011 APP Confirm buyer remittance v2.md |
| RWB-S6-E6011-CON | 14 | 14 | 0 | 04 User stories/Recovery Workbench Service Story Files v2/RWB-SVC-S6 rwb-debtsale (Debt sale)/RWB S6 E6011 CON Confirm buyer remittance - contract v2.md |

## 3. Open business decisions (not resolved; owner decides)

| Story | Ruling | Item | Kind | Owner role | Title | Proposed resolution |
|---|---|---|---|---|---|---|
| RWB-S6-E6005-CON | R-02725 | CG-ALL-10568 | Script gap | Product owner | The story adds BIDS_RECEIVED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6005-CON | R-02726 | CG-ALL-10569 | Script gap | Product owner | The story adds AWARD_PENDING to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6005-CON | R-02727 | CG-ALL-10570 | Script gap | Product owner | The story adds BID_BELOW_RESERVE to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6006-CON | R-02743 | CG-ALL-10603 | Script gap | Product owner | The story adds AWARD_PENDING to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6006-CON | R-02744 | CG-ALL-10604 | Script gap | Product owner | The story adds LOT_AWARDED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6006-CON | R-02745 | CG-ALL-10605 | Script gap | Product owner | The story adds SETTLEMENT_PENDING to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6007-APP | R-02753 | CG-ALL-10621 | Script gap | Product owner | The story adds SETTLEMENT_PENDING to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6007-APP | R-02754 | CG-ALL-10622 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02768 | CG-ALL-10669 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02769 | CG-ALL-10670 | Script gap | Product owner | The story adds DERECOGNISED to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02770 | CG-ALL-10671 | Script gap | Product owner | The story adds GL_POSTED to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02771 | CG-ALL-10672 | Script gap | Product owner | The story adds POSTING_REJECTED_DS to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02772 | CG-ALL-10673 | Script gap | Product owner | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02773 | CG-ALL-10674 | Script gap | Product owner | The story adds GL_ENTRY to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02774 | CG-ALL-10675 | Script gap | Product owner | The story adds PROVISION_INPUT to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02775 | CG-ALL-10676 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02776 | CG-ALL-10677 | Script gap | Product owner | The story adds DERECOGNISED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02777 | CG-ALL-10678 | Script gap | Product owner | The story adds GL_POSTED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02778 | CG-ALL-10679 | Script gap | Product owner | The story adds POSTING_REJECTED_DS to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02779 | CG-ALL-10680 | Script gap | Product owner | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02780 | CG-ALL-10681 | Script gap | Product owner | The story adds GL_ENTRY to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02781 | CG-ALL-10682 | Script gap | Product owner | The story adds PROVISION_INPUT to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02782 | CG-ALL-10683 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02783 | CG-ALL-10684 | Script gap | Product owner | The story adds DERECOGNISED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02784 | CG-ALL-10685 | Script gap | Product owner | The story adds GL_POSTED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02785 | CG-ALL-10686 | Script gap | Product owner | The story adds POSTING_REJECTED_DS to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02786 | CG-ALL-10687 | Script gap | Product owner | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02787 | CG-ALL-10688 | Script gap | Product owner | The story adds GL_ENTRY to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02788 | CG-ALL-10689 | Script gap | Product owner | The story adds PROVISION_INPUT to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02789 | CG-ALL-10690 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02790 | CG-ALL-10691 | Script gap | Product owner | The story adds DERECOGNISED to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02791 | CG-ALL-10692 | Script gap | Product owner | The story adds GL_POSTED to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02792 | CG-ALL-10693 | Script gap | Product owner | The story adds POSTING_REJECTED_DS to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02793 | CG-ALL-10694 | Script gap | Product owner | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02794 | CG-ALL-10695 | Script gap | Product owner | The story adds GL_ENTRY to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6008-CON | R-02795 | CG-ALL-10696 | Script gap | Product owner | The story adds PROVISION_INPUT to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02800 | CG-ALL-10711 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02801 | CG-ALL-10712 | Script gap | Product owner | The story adds PUTBACK_RAISED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02802 | CG-ALL-10713 | Script gap | Product owner | The story adds PUTBACK_UPHELD to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02803 | CG-ALL-10714 | Script gap | Product owner | The story adds PUTBACK_REFUSED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02804 | CG-ALL-10715 | Script gap | Product owner | The story adds LOT_CLOSED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02805 | CG-ALL-10716 | Script gap | Product owner | The story adds GL_POSTED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02806 | CG-ALL-10717 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02807 | CG-ALL-10718 | Script gap | Product owner | The story adds PUTBACK_RAISED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02808 | CG-ALL-10719 | Script gap | Product owner | The story adds PUTBACK_UPHELD to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02809 | CG-ALL-10720 | Script gap | Product owner | The story adds PUTBACK_REFUSED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02810 | CG-ALL-10721 | Script gap | Product owner | The story adds LOT_CLOSED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02811 | CG-ALL-10722 | Script gap | Product owner | The story adds GL_POSTED to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02812 | CG-ALL-10723 | Script gap | Product owner | The story adds BACK_TO_CASE_LIST to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6009-APP | R-02813 | CG-ALL-10724 | Script gap | Product owner | The story adds BACK_TO_CASE_LIST to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6010-APP | R-02826 | CG-ALL-10755 | Script gap | Product owner | The story adds CASE_CLOSED_SOLD to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6010-APP | R-02827 | CG-ALL-10756 | Script gap | Product owner | The story adds CASE_CLOSED_SOLD to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6010-CON | R-02832 | CG-ALL-10770 | Script gap | Product owner | The story adds CASE_CLOSED_SOLD to the closed list LOV-BUYER-CLASS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6010-CON | R-02833 | CG-ALL-10771 | Script gap | Product owner | The story adds CASE_CLOSED_SOLD to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6010-CON | R-02834 | CG-ALL-10772 | Script gap | Product owner | The story adds CASE_CLOSED_SOLD to the closed list LOV-PUTBACK | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6010-CON | R-02835 | CG-ALL-10773 | Script gap | Product owner | The story adds CASE_CLOSED_SOLD to the closed list LOV-SEGMENT | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6011-APP | R-02840 | CG-ALL-10783 | Script gap | Product owner | The story adds SETTLEMENT_PENDING to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6011-APP | R-02841 | CG-ALL-10784 | Script gap | Product owner | The story adds AWARD_CANCELED_DS to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6011-APP | R-02842 | CG-ALL-10785 | Script gap | Product owner | The story adds BIDDING_OPEN to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6011-APP | R-02843 | CG-ALL-10786 | Script gap | Product owner | The story adds DATA_TRANSFERRED to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6011-CON | R-02851 | CG-ALL-10805 | Script gap | Product owner | The story adds AWARD_CANCELED_DS to the closed list LOV-LOT-STATUS | Rule whether the criterion stays (and the list becomes open, with the yaml enum removed) or the criterion uses an existing value. Needs a ruling; no edit until then. |
| RWB-S6-E6005-APP | R-13106 | CG-ALL-10563 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6006-APP | R-13116 | CG-ALL-10599 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6007-APP | R-13128 | CG-ALL-10636 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6008-APP | R-13141 | CG-ALL-10664 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6009-APP | R-13153 | CG-ALL-10738 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6010-APP | R-13162 | CG-ALL-10766 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-S6-E6011-APP | R-13171 | CG-ALL-10801 | Script gap | Compliance | Fields classed as personal data where the story says none is carried | State the handling rule of Data Classification v5 for each field (codec, masking) or drop the field. |
| RWB-PLT-N001-APP, RWB-PLT-N001-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-S6-E6005-APP, RWB-S6-E6012-APP | R-23244 | GAP-3015 | Register gap | Solution architect with the owners of rwb-case (P3), rwb-decision (P7), rwb-access (P4) and rwb-source-data (P1), and the business owner of the debt sale cap | RWB-S6-E6012-APP: the cap slice has no plan row for the five consumed contracts, no cap parameter row, no cap route rule, no published trigger, no headroom column and no service contract baseline | Publish the five consumed operations with their fake; add C rows for rwb-case, rwb-decision, rwb-access and rwb-source-data; add the DP-04, DP-06, DP-07, DP-08 and DP-09 rows the tables need; name the cap row, its version, its basis and its owner; publish one route rule for the cap or confirm that R-DS-19 and R-DS-23 are its only test and which story owns them; publish the trigger or confirm the call from the lot build and award steps; add the cap-position and headroom fields or confirm the decision record as their only home; create the service contract baseline for this legacy key; and carry REQ-S6-001 and BR-050 in the plan |
| RWB-S6-E5024-APP, RWB-S6-E5024-CON, RWB-S6-E6005-APP, RWB-S6-E6005-CON | R-23585 | GAP-1778 | Register gap | Risk with the product heads | The approval bands in the design and the delegation in the FSD are two different statements of who approves an award | Route the lot approval and the award through the P7 approval child on the delegation table of P4, hold the bands as versioned reference data with their valid-from date, and record the level applied and the approving role on the award; the free-text authority column then holds the level name, not a person. |
| RWB-S6-E5025-APP, RWB-S6-E6007-APP, RWB-S6-E6007-CON | R-23590 | GAP-1786 | Register gap | Compliance and PDPA officer | borrower_code and account_key are flagged not personal in the data model, yet they identify a customer on the tape | Treat borrower_code and account_key as personal data in use, mask both on every screen and on the tape and the transfer file by role, and correct the is_personal flag in the next version of the Logical Data Model and the physical schema. |
| RWB-S6-E6003-APP, RWB-S6-E6003-CON, RWB-S6-E6009-APP, RWB-S6-E6009-CON, RWB-S6-E6011-APP, RWB-S6-E6011-CON | R-23607 | GAP-1791 | Register gap | Head of Asset Liquidity | The put-back window, the remediation window and the settlement term are not stated and are business values | Hold the three windows as versioned reference-data rows with their valid-from dates, apply the value in force at the business date of the lot, and record the version applied on the claim and the settlement. |
| RWB-S6-E5023-APP, RWB-S6-E5023-CON, RWB-S6-E6005-APP, RWB-S6-E6005-CON | R-29212 | GAP-1485 | Register gap | Head of Asset Liquidity | The debt sale turnaround has a target and no baseline | Measure the current cycle on the first lot of the release and publish it as the baseline with the target of 45 days unchanged. |
| RWB-S6-E5025-APP, RWB-S6-E6007-APP, RWB-S6-E6007-CON | R-29220 | GAP-1790 | Register gap | Compliance and PDPA officer | Retention, classification and the masking rules a record is held under are open | Give every record a data classification and a retention class and hold the periods as reference data from DL26; apply the class to the tape and to the transfer file through P5 and P2, which own the document and the file. |

## 4. Not applied (the value is not in the source documents)

| Story | Ruling | Item | Section | Title | Reason |
|---|---|---|---|---|---|
| RWB-S6-E6006-CON | R-13120 | CG-ALL-10618 | 7; 16 | Criteria and test data read ACE views directly | The offending AC4 Given line is in section 7 and its test rows are in section 16, both outside this chunk, so the text cannot be copied. Needs those sections. |
| RWB-S6-E6006-CON | R-20704 | DOR-RWB-S6-E6006-CON-4 | 8 | Definition of Ready item 4 Business rules: Partial | Covering AC and TC rows for BR1 to BR12 are in sections 7 and 16, outside this chunk. No AC or TC IDs invented. Needs those sections. |
| RWB-S6-E6008-APP | R-20721 | DOR-RWB-S6-E6008-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | Section 9 text is outside this chunk, so no exact old text. Sources give only loading for SCR-25 and no empty, error or no-access states for SCR-25/26 (E5023, E5024, FSD S6). Needs the section 9 text and a state ruling. |
| RWB-S6-E6010-APP | R-08555 | DOR-RWB-S6-E6010-APP-14 |  | Definition of Ready item 14 Epic design: Fail | No signed epic design sign-off record in the story or the sources (searched story and realignment folder). Sign-off is an approval and cannot be invented. Story stays Draft. |
| RWB-S6-E6010-APP | R-20752 | DOR-RWB-S6-E6010-APP-10 | 9 | Definition of Ready item 10 Screens and states: Partial | SCR-26 empty, loading, error and no-access states belong in section 9, which is not in this chunk, so it cannot be edited here. No states invented. |

## 5. Cross-document changes (pending in the target document)


### API:(service not named) (70)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18616 | RWB-S6-E6004-CON | CG-ALL-10537 | 12.2 | Declare the REST base /api/recovery/partner/v1 for the buyer clearance read, using the provider's base from the Document Index service table. |
| CDC-18617 | RWB-S6-E6004-CON | CG-ALL-10538 | 12.2 | Declare the REST base /api/recovery/case/v1 for the case read, using the provider's base from the Document Index service table. |
| CDC-18618 | RWB-S6-E6004-CON | CG-ALL-10539 | 12.2 | Declare the REST base /api/recovery/access/v1 for the authorise and capability read, using the provider's base from the Document Index service table. |
| CDC-18619 | RWB-S6-E6004-CON | CG-ALL-10540 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rule package read, using the provider's base from the Document Index service table. |
| CDC-18621 | RWB-S6-E6004-CON | DOR-RWB-S6-E6004-CON-8 | 12.2 | Declare the REST bases of the four consumed providers in CG-ALL-10537 to CG-ALL-10540 and the four further gaps in this check. |
| CDC-18632 | RWB-S6-E6005-APP | CG-ALL-10550 | 12.2 | Declare the REST base /api/recovery/case/v1 for the rwb-case provider (P3) using the Document Index service table. |
| CDC-18633 | RWB-S6-E6005-APP | CG-ALL-10551 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rwb-decision provider (P7) using the Document Index service table. |
| CDC-18634 | RWB-S6-E6005-APP | CG-ALL-10552 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the rwb-decision provider (P7) using the Document Index service table. |
| CDC-18635 | RWB-S6-E6005-APP | CG-ALL-10553 | 12.2 | Declare the REST base /api/recovery/access/v1 for the rwb-access provider (P4) using the Document Index service table. |
| CDC-18636 | RWB-S6-E6005-APP | CG-ALL-10554 | 12.2 | Declare the REST base /api/recovery/source-data/v1 for the rwb-source-data provider (P1) using the Document Index service table. |
| CDC-18640 | RWB-S6-E6005-APP | DOR-RWB-S6-E6005-APP-8 | Header | Add yaml files with base paths /api/recovery/case/v1, /api/recovery/decision/v1, /api/recovery/access/v1, /api/recovery/source-data/v1 and the seven more listed by detcheck. |
| CDC-18654 | RWB-S6-E6005-APP | GAP-1773 | n/a | Publish the five operations under /api/recovery/debtsale/v1 as the contract; add the staff bid read when the S6 contract story closes; /lots stays as shorthand for slide 19. |
| CDC-18663 | RWB-S6-E6005-CON | CG-ALL-10571 | 12.2 | Declare REST base /api/recovery/case/v1 for the GET /CASES/{CASEID} family (READ) using the provider's base from the Document Index service table. |
| CDC-18664 | RWB-S6-E6005-CON | CG-ALL-10572 | 12.2 | Declare REST base /api/recovery/decision/v1 for the DS rule package version read using the provider's base from the Document Index service table. |
| CDC-18665 | RWB-S6-E6005-CON | CG-ALL-10573 | 12.2 | Declare REST base /api/recovery/decision/v1 for the GET /APPROVALS and POST /APPROVALS approve/return/refuse operations using the provider's base from the Document Index service table. |
| CDC-18666 | RWB-S6-E6005-CON | CG-ALL-10574 | 12.2 | Declare REST base /api/recovery/access/v1 for GET /DOA-LIMITS using the provider's base from the Document Index service table. |
| CDC-18667 | RWB-S6-E6005-CON | CG-ALL-10575 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the model score read using the provider's base from the Document Index service table. |
| CDC-18670 | RWB-S6-E6005-CON | DOR-RWB-S6-E6005-CON-8 | 1 | Add the base paths /api/recovery/case/v1, /api/recovery/decision/v1, /api/recovery/access/v1, /api/recovery/source-data/v1 and the six further base paths named in the detcheck. |
| CDC-18681 | RWB-S6-E6006-APP | CG-ALL-10587 | 12.2 | Declare REST base /api/recovery/document/v1 for the rwb-document provider, taken from the Document Index service table. |
| CDC-18682 | RWB-S6-E6006-APP | CG-ALL-10588 | 12.2 | Declare REST base /api/recovery/comms/v1 for the rwb-comms provider, taken from the Document Index service table. |
| CDC-18683 | RWB-S6-E6006-APP | CG-ALL-10589 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the rwb-source-data provider, taken from the Document Index service table. |
| CDC-18684 | RWB-S6-E6006-APP | CG-ALL-10590 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case provider, taken from the Document Index service table. |
| CDC-18685 | RWB-S6-E6006-APP | CG-ALL-10591 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rwb-decision provider, taken from the Document Index service table. |
| CDC-18688 | RWB-S6-E6006-APP | DOR-RWB-S6-E6006-APP-8 | Header | Add the base paths /api/recovery/document/v1, /api/recovery/comms/v1, /api/recovery/source-data/v1 and /api/recovery/case/v1, and the six further paths detcheck lists. |
| CDC-18698 | RWB-S6-E6006-CON | CG-ALL-10606 | 12.2 | Declare REST base /api/recovery/document/v1 for P5 rwb-document, taken from the Document Index service table. |
| CDC-18699 | RWB-S6-E6006-CON | CG-ALL-10607 | 12.2 | Declare REST base /api/recovery/comms/v1 for P6 rwb-comms, taken from the Document Index service table. |
| CDC-18700 | RWB-S6-E6006-CON | CG-ALL-10608 | 12.2 | Declare REST base /api/recovery/source-data/v1 for P1 rwb-source-data, taken from the Document Index service table. |
| CDC-18701 | RWB-S6-E6006-CON | CG-ALL-10609 | 12.2 | Declare REST base /api/recovery/case/v1 for P3 rwb-case, taken from the Document Index service table. |
| CDC-18702 | RWB-S6-E6006-CON | CG-ALL-10610 | 12.2 | Declare REST base /api/recovery/decision/v1 for P7 rwb-decision, taken from the Document Index service table. |
| CDC-18704 | RWB-S6-E6006-CON | DOR-RWB-S6-E6006-CON-8 | find it | Add bases /api/recovery/document/v1, /api/recovery/comms/v1, /api/recovery/source-data/v1, /api/recovery/case/v1 and the six further paths in the detcheck. |
| CDC-18713 | RWB-S6-E6007-APP | CG-ALL-10625 | 12.2 | Declare REST base /api/recovery/case/v1 for the case read, using the provider's base from the Document Index service table. |
| CDC-18714 | RWB-S6-E6007-APP | CG-ALL-10626 | 12.2 | Declare REST base /api/recovery/partner/v1 for the buyer organisation read, using the provider's base from the Document Index service table. |
| CDC-18715 | RWB-S6-E6007-APP | CG-ALL-10627 | 12.2 | Declare REST base /api/recovery/access/v1 for the authorise and capability area read, using the provider's base from the Document Index service table. |
| CDC-18716 | RWB-S6-E6007-APP | CG-ALL-10628 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule package in force read, using the provider's base from the Document Index service table. |
| CDC-18720 | RWB-S6-E6007-APP | DOR-RWB-S6-E6007-APP-8 | 8 | Add the base paths /api/recovery/case/v1, /api/recovery/partner/v1, /api/recovery/access/v1, /api/recovery/decision/v1 and the six further bases in the detcheck result. |
| CDC-18735 | RWB-S6-E6007-CON | CG-ALL-10640 | 12.2 | Declare the REST base /api/recovery/case/v1 for the provider named in the Document Index service table. |
| CDC-18736 | RWB-S6-E6007-CON | CG-ALL-10641 | 12.2 | Declare the REST base /api/recovery/partner/v1 for the provider named in the Document Index service table. |
| CDC-18737 | RWB-S6-E6007-CON | CG-ALL-10642 | 12.2 | Declare the REST base /api/recovery/access/v1 for the provider named in the Document Index service table. |
| CDC-18738 | RWB-S6-E6007-CON | CG-ALL-10643 | 12.2 | Declare the REST base /api/recovery/decision/v1 for the provider named in the Document Index service table. |
| CDC-18740 | RWB-S6-E6007-CON | DOR-RWB-S6-E6007-CON-8 | 12.2 | Declare the REST bases /api/recovery/case/v1, /api/recovery/partner/v1, /api/recovery/access/v1 and /api/recovery/decision/v1, and the other P1 bases in the detcheck list. |
| CDC-18767 | RWB-S6-E6008-CON | CG-ALL-10697 | 12.2 | Declare the REST base /api/recovery/source-data/v1 from the Document Index service table. |
| CDC-18768 | RWB-S6-E6008-CON | CG-ALL-10698 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table. |
| CDC-18769 | RWB-S6-E6008-CON | CG-ALL-10699 | 12.2 | Declare the REST base /api/recovery/decision/v1 from the Document Index service table. |
| CDC-18772 | RWB-S6-E6008-CON | DOR-RWB-S6-E6008-CON-8 | find it | Declare the three missing REST bases (source-data/v1, case/v1, decision/v1); the task queue item is fixed in the story. |
| CDC-18785 | RWB-S6-E6009-APP | CG-ALL-10727 | 12.2 | Declare the REST base /api/recovery/partner/v1 from the Document Index service table for the buyer claim read. |
| CDC-18786 | RWB-S6-E6009-APP | CG-ALL-10728 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table for the GET /cases/{caseId} family. |
| CDC-18787 | RWB-S6-E6009-APP | CG-ALL-10729 | 12.2 | Declare the REST base /api/recovery/access/v1 from the Document Index service table for the authorise call and capability area read. |
| CDC-18788 | RWB-S6-E6009-APP | CG-ALL-10730 | 12.2 | Declare the REST base /api/recovery/decision/v1 from the Document Index service table for the rule package in force read. |
| CDC-18789 | RWB-S6-E6009-APP | CG-ALL-10731 | 12.2 | Declare the REST base /api/recovery/case/v1 from the Document Index service table for the claim-window parameter read. |
| CDC-18793 | RWB-S6-E6009-APP | DOR-RWB-S6-E6009-APP-8 | find it | Add the missing base paths named by the detcheck: /api/recovery/partner/v1, /api/recovery/case/v1, /api/recovery/access/v1, /api/recovery/decision/v1 and the four further paths listed in the detcheck. |
| CDC-18804 | RWB-S6-E6009-CON | CG-ALL-10742 | 12.2 | Declare REST base /api/recovery/partner/v1 for the rwb-partner operations. |
| CDC-18805 | RWB-S6-E6009-CON | CG-ALL-10743 | 12.2 | Declare REST base /api/recovery/case/v1 for the rwb-case operations. |
| CDC-18806 | RWB-S6-E6009-CON | CG-ALL-10744 | 12.2 | Declare REST base /api/recovery/access/v1 for the rwb-access operations. |
| CDC-18807 | RWB-S6-E6009-CON | CG-ALL-10745 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rwb-decision operations. |
| CDC-18808 | RWB-S6-E6009-CON | CG-ALL-10746 | 12.2 | Declare REST base /api/recovery/case/v1 for the claim-window parameter operation. |
| CDC-18810 | RWB-S6-E6009-CON | DOR-RWB-S6-E6009-CON-8 | 12.2 | Declare the REST bases for /api/recovery/partner/v1, /case/v1, /access/v1 and /decision/v1. |
| CDC-18819 | RWB-S6-E6010-APP | CG-ALL-10759 | 12.2 | Declare REST base /api/recovery/case/v1 for provider P3 rwb-case, as in the Document Index service table. |
| CDC-18820 | RWB-S6-E6010-APP | CG-ALL-10760 | 12.2 | Declare REST base /api/recovery/access/v1 for provider P4 rwb-access, as in the Document Index service table. |
| CDC-18821 | RWB-S6-E6010-APP | CG-ALL-10761 | 12.2 | Declare REST base /api/recovery/decision/v1 for provider P7 rwb-decision, as in the Document Index service table. |
| CDC-18836 | RWB-S6-E6010-CON | CG-ALL-10774 | 12.2 | Declare REST base /api/recovery/case/v1 for the case family, using the Document Index service table. |
| CDC-18837 | RWB-S6-E6010-CON | CG-ALL-10775 | 12.2 | Declare REST base /api/recovery/access/v1, using the Document Index service table. |
| CDC-18838 | RWB-S6-E6010-CON | CG-ALL-10776 | 12.2 | Declare REST base /api/recovery/decision/v1, using the Document Index service table. |
| CDC-18841 | RWB-S6-E6010-CON | DOR-RWB-S6-E6010-CON-8 | find it | Declare REST bases /api/recovery/case/v1, /api/recovery/access/v1 and /api/recovery/decision/v1. |
| CDC-18850 | RWB-S6-E6011-APP | CG-ALL-10790 | 12.2 | Declare the REST base /api/recovery/source-data/v1 in the provider yaml, as the Document Index service table gives it. |
| CDC-18851 | RWB-S6-E6011-APP | CG-ALL-10791 | 12.2 | Declare the REST base /api/recovery/case/v1 in the provider yaml, as the Document Index service table gives it. |
| CDC-18852 | RWB-S6-E6011-APP | CG-ALL-10792 | 12.2 | Declare the REST base /api/recovery/partner/v1 in the provider yaml, as the Document Index service table gives it. |
| CDC-18853 | RWB-S6-E6011-APP | CG-ALL-10793 | 12.2 | Declare the REST base /api/recovery/access/v1 in the provider yaml, as the Document Index service table gives it. |
| CDC-18854 | RWB-S6-E6011-APP | CG-ALL-10794 | 12.2 | Declare the REST base /api/recovery/decision/v1 in the provider yaml, as the Document Index service table gives it. |
| CDC-18858 | RWB-S6-E6011-APP | DOR-RWB-S6-E6011-APP-8 | header | Add the bases /api/recovery/source-data/v1, /api/recovery/case/v1, /api/recovery/partner/v1, /api/recovery/access/v1 and the five further bases in the detcheck |
| CDC-18874 | RWB-S6-E6011-CON | DOR-RWB-S6-E6011-CON-8 | 12.8 | Add the base paths /api/recovery/source-data/v1, /api/recovery/case/v1, /api/recovery/partner/v1, /api/recovery/access/v1 and the five further bases named in the detcheck output. |

### 09 Testing and quality/Recovery Workbench Test Cases v8.xlsx (25)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18625 | RWB-S6-E6004-CON | DOR-RWB-S6-E6004-CON-12 | 16 | Add rows TC-E6-004-01 to -05, TC-S6-E6004-CON-01 to -04 and TC-S6-E6004-CON-05 on the Story test cases tab. |
| CDC-18630 | RWB-S6-E6004-CON | CG-ALL-10545 | 16 | Add rows for the nine test case IDs, with Given, When and Then copied from the criterion each covers |
| CDC-18645 | RWB-S6-E6005-APP | CG-ALL-10562 | 16 | In the next version, add rows TC-E6-005-01 to TC-E6-005-06 to tab Story test cases, with Given, When and Then copied from the criteria they cover; TC-E6-005-07 and TC-E6-005-08 are added by this story. |
| CDC-18674 | RWB-S6-E6005-CON | DOR-RWB-S6-E6005-CON-12 | 12.7, 16 | Add TC-E6-005-01 to -06 and TC-S6-E6005-CON-01 to -08 under the same IDs, with the Covers and Data of section 16. |
| CDC-18677 | RWB-S6-E6005-CON | CG-ALL-10582 | 16 | Add rows for TC-E6-005-01 to -06 and TC-S6-E6005-CON-01 to -07 with Given, When and Then copied from the criterion each covers. |
| CDC-18693 | RWB-S6-E6006-APP | CG-ALL-10598 | 16 | Add rows for TC-E6-006-01 to TC-E6-006-05 to the Story test cases tab, with Given, When and Then copied from the criteria they cover. |
| CDC-18694 | RWB-S6-E6006-APP | DOR-RWB-S6-E6006-APP-12 | 16 | Add rows for TC-E6-006-01 to TC-E6-006-08 on tab Story test cases; section 16 now lists TC-06 contract and TC-07 boundary rows, plus TC-08. |
| CDC-18710 | RWB-S6-E6006-CON | CG-ALL-10617 | 16 | Add rows for TC-E6-006-01 to -05 and TC-S6-E6006-CON-01 to -06 with Given, When and Then copied from the criterion each covers |
| CDC-18726 | RWB-S6-E6007-APP | CG-ALL-10635 | 16 | Add rows TC-E6-007-01 to TC-E6-007-06 with Given, When and Then copied from the criteria they cover (section 16 of the story). |
| CDC-18727 | RWB-S6-E6007-APP | DOR-RWB-S6-E6007-APP-12 | 12, 12.7, 16 | Add rows in tab Story test cases for TC-E6-007-01 to TC-E6-007-09 under the same IDs. |
| CDC-18744 | RWB-S6-E6007-CON | DOR-RWB-S6-E6007-CON-12 | 16 | Tab Story test cases: add TC-E6-007-01 to -06, TC-S6-E6007-CON-01 to -04 and TC-S6-E6007-CON-05 |
| CDC-18749 | RWB-S6-E6007-CON | CG-ALL-10650 | 16 | Add rows TC-E6-007-01 to TC-E6-007-06 and TC-S6-E6007-CON-01 to TC-S6-E6007-CON-04 with Given, When and Then copied from the criterion each covers. |
| CDC-18761 | RWB-S6-E6008-APP | CG-ALL-10662 | 16 | Add rows TC-E6-008-01 to TC-E6-008-06 to Story test cases, with Given, When and Then copied from the criteria they cover. |
| CDC-18778 | RWB-S6-E6008-CON | DOR-RWB-S6-E6008-CON-12 | 16 | Add rows TC-E6-008-01 to -06 and TC-S6-E6008-CON-01 to -05 under the same IDs. |
| CDC-18784 | RWB-S6-E6008-CON | CG-ALL-10707 | 16 | Add rows for TC-E6-008-01 to -06 and TC-S6-E6008-CON-01 to -04, with Given, When and Then copied from the criteria they cover. |
| CDC-18798 | RWB-S6-E6009-APP | CG-ALL-10737 | 16 | Add rows TC-E6-009-01 to TC-E6-009-06 with Given, When and Then copied from the criteria they cover, in the next Test Cases version. |
| CDC-18799 | RWB-S6-E6009-APP | DOR-RWB-S6-E6009-APP-12 | 12, 12.7, 16 | Add rows TC-E6-009-01 to TC-E6-009-11 on tab Story test cases under the same IDs as section 16. |
| CDC-18814 | RWB-S6-E6009-CON | DOR-RWB-S6-E6009-CON-12 | 12.7, 16 | Add rows TC-E6-009-01 to TC-E6-009-06 and TC-S6-E6009-CON-01 to TC-S6-E6009-CON-03; add TC-S6-E6009-CON-04 for the section 12.7 boundary. |
| CDC-18818 | RWB-S6-E6009-CON | CG-ALL-10752 | 16 | Add rows for TC-E6-009-01 to TC-E6-009-06 and TC-S6-E6009-CON-01 to -03, with Given, When and Then copied from the criterion each covers. |
| CDC-18828 | RWB-S6-E6010-APP | CG-ALL-10765 | 16 | Add rows TC-E6-010-01 to TC-E6-010-04 and TC-S6-E6010-APP-01 with Given, When and Then copied from their criteria; also add TC-S6-E6010-APP-02 and -03. |
| CDC-18844 | RWB-S6-E6010-CON | DOR-RWB-S6-E6010-CON-12 | 16 | Add rows for TC-E6-010-01 to -04 and TC-S6-E6010-CON-01 to -04; the story-side boundary row TC-S6-E6010-CON-05 is added |
| CDC-18846 | RWB-S6-E6010-CON | CG-ALL-10780 | 16 | Add rows for TC-E6-010-01 to -04 and TC-S6-E6010-CON-01 to -04, with Given, When and Then copied from the criteria each row covers. |
| CDC-18863 | RWB-S6-E6011-APP | CG-ALL-10800 | 16 | Story section 16 lists the IDs; new TC-E6-011-07 to TC-E6-011-14 added there. |
| CDC-18877 | RWB-S6-E6011-CON | DOR-RWB-S6-E6011-CON-12 | 16 | Add rows for TC-E6-011-01 to -06 and TC-S6-E6011-CON-01 to -05 under the same IDs. |
| CDC-18880 | RWB-S6-E6011-CON | CG-ALL-10816 |  | Add rows for TC-E6-011-01 to -06 and TC-S6-E6011-CON-01 to -04, with Given, When and Then copied from the criterion each covers. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (17)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18622 | RWB-S6-E6004-CON | CG-ALL-10543 | 12.5 | Add activity takeBid to the Activities sheet, or name a catalogued activity in its place in section 12.5. |
| CDC-18623 | RWB-S6-E6004-CON | CG-ALL-10544 | 12.5 | Add activity closeLotAfterClaimWindow to the Activities sheet, or name a catalogued activity in its place in section 12.5. |
| CDC-18644 | RWB-S6-E6005-APP | CG-ALL-10561 | 12.5 | Add activity recordAward, task queue rwb-debtsale, to the Activities sheet of Temporal Catalog v1. |
| CDC-18668 | RWB-S6-E6005-CON | CG-ALL-10577 | 12.5 | Task queue rwb-debtsale matches the catalog; namespace rwb-recovery differs from the catalog and the story leaves it unchanged. |
| CDC-18691 | RWB-S6-E6006-APP | CG-ALL-10595 | 12.5 | Add activity The document run of rwb-document (queue rwb-document, owner P5) to the Activities sheet. |
| CDC-18692 | RWB-S6-E6006-APP | CG-ALL-10596 | 12.5 | Add activity recordAwardAndIssueNotices (queue rwb-debtsale) to the Activities sheet. |
| CDC-18705 | RWB-S6-E6006-CON | CG-ALL-10614 | 12.5 | Add an Activities row for 'The document run of rwb-document' on queue rwb-document (P5), or name a catalogued activity. |
| CDC-18706 | RWB-S6-E6006-CON | CG-ALL-10615 | 12.5 | Add an Activities row 'recordAwardAndIssueNotices', type Activity, task queue rwb-debtsale, or name a catalogued activity. |
| CDC-18742 | RWB-S6-E6007-CON | CG-ALL-10648 | 12.5 | Activities: add settleAward for rwb-debtsale (R-DS-25 step), or name a catalogued activity in its place |
| CDC-18743 | RWB-S6-E6007-CON | CG-ALL-10649 | 12.5 | Activities: add transferAccounts for rwb-debtsale (R-DS-29 step), or name a catalogued activity in its place |
| CDC-18754 | RWB-S6-E6008-APP | DOR-RWB-S6-E6008-APP-8 | 12.5 | Add activities derecogniseAccounts and postToLedger and the DebtSaleWorkflow ID form and start rule. Story records the ID form as Not specified. |
| CDC-18757 | RWB-S6-E6008-APP | CG-ALL-10657 | 12.5 | Add an Activities row for derecogniseAccounts (rwb-debtsale, R-DS-30 step, queue rwb-debtsale). |
| CDC-18758 | RWB-S6-E6008-APP | CG-ALL-10658 | 12.5 | Add an Activities row for postToLedger (rwb-debtsale, R-DS-31 to R-DS-33 step, queue rwb-debtsale). |
| CDC-18796 | RWB-S6-E6009-APP | CG-ALL-10734 | 12.5 | Add activity reviewPutbackClaim on task queue rwb-debtsale with its contract element, or name a catalogued activity. |
| CDC-18797 | RWB-S6-E6009-APP | CG-ALL-10735 | 12.5 | Add activity closeLotOnClaimWindow on task queue rwb-debtsale with its contract element, or name a catalogued activity. |
| CDC-18827 | RWB-S6-E6010-APP | CG-ALL-10764 | 12.5 | Add activity closeCase on task queue rwb-debtsale with the contract element of section 12.5, or catalogue an existing activity. |
| CDC-18842 | RWB-S6-E6010-CON | CG-ALL-10779 | 12.5 | Add activity closeCase to the Activities sheet, or name a catalogued activity in section 12.5 |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx (13)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18689 | RWB-S6-E6006-APP | CG-ALL-10585 | 11 | Section 11 notes that account_id is not yet a field of LDM v9 or Data Classification v5. |
| CDC-18690 | RWB-S6-E6006-APP | CG-ALL-10586 | 11 | Record decision_record as the library object created in rwb_debtsale by the PLT decision record library. |
| CDC-18695 | RWB-S6-E6006-APP | DOR-RWB-S6-E6006-APP-7 | 11 | Name account_id as a field of debt_sale_account and decision_record as a PLT library entity in LDM v9 and Data Classification v5. |
| CDC-18721 | RWB-S6-E6007-APP | CG-ALL-10623 | 3, 11 | Record decision_record as a platform library object created in rwb_debtsale by the library migration (DP-03), or use the dictionary name. |
| CDC-18722 | RWB-S6-E6007-APP | CG-ALL-10624 | 8 | Record account_id as the identifier of the account fact in debt_sale_account (DF-SAL-031 to DF-SAL-037, TSD S6 T3.1), or use the dictionary name. |
| CDC-18728 | RWB-S6-E6007-APP | DOR-RWB-S6-E6007-APP-7 | 11, 7, 16 | Add or map decision_record and account_id to LDM v9 or Data Classification v5 entries, or name the entries they map to. |
| CDC-18756 | RWB-S6-E6008-APP | CG-ALL-10654 | 12.7 | Record decision_record as a PLT library table created in rwb_debtsale by the DP-03 library migration, not as a dictionary entity. |
| CDC-18762 | RWB-S6-E6008-APP | DOR-RWB-S6-E6008-APP-7 | 12.6 | Add decision_record as an entity or field name for the PLT library's local decision record in rwb_debtsale, or confirm it is a library object outside the LDM. |
| CDC-18795 | RWB-S6-E6009-APP | CG-ALL-10726 | find it | Record decision_record as a PLT library object created in rwb_debtsale by the library migration, as the story already states at the table-note and library rows. |
| CDC-18826 | RWB-S6-E6010-APP | CG-ALL-10758 | 11 | Record decision_record as a platform library object created in rwb_debtsale, or add it to the dictionary. |
| CDC-18860 | RWB-S6-E6011-APP | CG-ALL-10788 | 11 | Record decision_record as a platform library object created in rwb_debtsale, or give its dictionary name |
| CDC-18861 | RWB-S6-E6011-APP | CG-ALL-10789 | 11 | Record inbox_event as a platform library object created in rwb_debtsale, or give its dictionary name |
| CDC-18864 | RWB-S6-E6011-APP | DOR-RWB-S6-E6011-APP-7 | 11 | Add account_id, decision_record and inbox_event as fields or entities, or confirm them as platform library objects (DP-03). |

### Epic design record (11)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18686 | RWB-S6-E6006-APP | DOR-RWB-S6-E6006-APP-14 | none | Record the signed epic design sign-off in the epic design record; the story text cannot confirm it. |
| CDC-18703 | RWB-S6-E6006-CON | DOR-RWB-S6-E6006-CON-14 | header | Record the signed epic design sign-off for RWB-SVC-S6 so the Definition of Ready item 14 can pass. |
| CDC-18717 | RWB-S6-E6007-APP | DOR-RWB-S6-E6007-APP-14 | header | Record the signed epic design sign-off for EP06 / RWB-SVC-S6. No signed record exists in the sources, so none is written here. |
| CDC-18739 | RWB-S6-E6007-CON | DOR-RWB-S6-E6007-CON-14 | none | Record the signed epic design sign-off for RWB-S6-E6007-CON. |
| CDC-18751 | RWB-S6-E6008-APP | DOR-RWB-S6-E6008-APP-14 |  | Record the signed epic design sign-off so this story can cite it. |
| CDC-18770 | RWB-S6-E6008-CON | DOR-RWB-S6-E6008-CON-14 | find it | Record the signed epic design sign-off for RWB-SVC-S6. |
| CDC-18790 | RWB-S6-E6009-APP | DOR-RWB-S6-E6009-APP-14 | header | Confirm the signed epic design sign-off and record it in the epic design record; no signed design is in the source documents. |
| CDC-18809 | RWB-S6-E6009-CON | DOR-RWB-S6-E6009-CON-14 | header | Record the signed epic design sign-off; the story cannot confirm it. |
| CDC-18839 | RWB-S6-E6010-CON | DOR-RWB-S6-E6010-CON-14 | find it | Confirm the sign-off of the epic design and record it as signed. |
| CDC-18855 | RWB-S6-E6011-APP | DOR-RWB-S6-E6011-APP-14 | find it | Record the signed epic design sign-off for RWB-S6-E6011-APP; no sign-off is in the source documents, so none is written into the story. |
| CDC-18872 | RWB-S6-E6011-CON | DOR-RWB-S6-E6011-CON-14 | 14 | Record the signed epic design sign-off in the epic design record. |

### 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx; 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (8)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18641 | RWB-S6-E6005-APP | CG-ALL-10548 | 11 | Record decision_record as a platform library object created in rwb_debtsale, with its fields. |
| CDC-18642 | RWB-S6-E6005-APP | CG-ALL-10549 | 11 | Record account_id as the account identifier field of debt_sale_account (TSD S6 v2 T3.1 field ID). |
| CDC-18646 | RWB-S6-E6005-APP | DOR-RWB-S6-E6005-APP-7 | 11 | Add decision_record and account_id as a field or entity, or name the platform object they resolve to; replace the legacy job and decision-log wording in the section 7 criteria and section 16 tests. |
| CDC-18794 | RWB-S6-E6009-APP | CG-ALL-10725 | find it | Record account_id under its dictionary name (nearest: account) or record the object that carries it in the owning document; align the uses at the BR8 row and the debt_sale_account field list. |
| CDC-18800 | RWB-S6-E6009-APP | DOR-RWB-S6-E6009-APP-7 | 11 | Add field account_id to debt_sale_account and entity decision_record (rwb_debtsale library) to LDM v9 and Data Classification v5. |
| CDC-18825 | RWB-S6-E6010-APP | CG-ALL-10757 | 8 | Give the dictionary field name for debt_sale_account.account_id, or record the owning object in the owning document. |
| CDC-18830 | RWB-S6-E6010-APP | DOR-RWB-S6-E6010-APP-7 | 11 | Add field account_id and entity decision_record to LDM v9 or Data Classification v5, or confirm mapping to existing names. |
| CDC-18859 | RWB-S6-E6011-APP | CG-ALL-10787 | 8, 11 | Record account_id (DF-SAL-033, debt_sale_account) as a dictionary field or give its dictionary name |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities sheet (7)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18671 | RWB-S6-E6005-CON | CG-ALL-10580 | 12.5 | Add the activity testAwardPrice to the Activities sheet, or name a catalogued activity in its place. |
| CDC-18672 | RWB-S6-E6005-CON | CG-ALL-10581 | 12.5 | Add the activity recordAward to the Activities sheet, or name a catalogued activity in its place. |
| CDC-18773 | RWB-S6-E6008-CON | CG-ALL-10702 | 12.5 | Add an Activities row for derecogniseAccounts, or name a catalogued activity in RWB-S6-E6008-CON §12.5. |
| CDC-18774 | RWB-S6-E6008-CON | CG-ALL-10703 | 12.5 | Add an Activities row for postToLedger, or name a catalogued activity in RWB-S6-E6008-CON §12.5. |
| CDC-18775 | RWB-S6-E6008-CON | CG-ALL-10704 | 12.5 | Add an Activities row for the outbound item call (rwb-integration), or name a catalogued activity in RWB-S6-E6008-CON §12.5. |
| CDC-18811 | RWB-S6-E6009-CON | CG-ALL-10749 | 12.5 | Add an Activities row for reviewPutbackClaim on task queue rwb-debtsale, or name a catalogued activity in its place. |
| CDC-18812 | RWB-S6-E6009-CON | CG-ALL-10750 | 12.5 | Add an Activities row for closeLotOnClaimWindow on task queue rwb-debtsale, or name a catalogued activity in its place. |

### 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx; OTHER:Activities (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18643 | RWB-S6-E6005-APP | CG-ALL-10560 | 12.5 | Add activity testAwardPrice on task queue rwb-debtsale with the lot, bids and package in; rule ID with version, price-test outcome and DoA test out. |
| CDC-18724 | RWB-S6-E6007-APP | CG-ALL-10633 | 12.5 | Add activity settleAward on task queue rwb-debtsale, the R-DS-25 step, with its inputs and outputs as stated in section 12.5. |
| CDC-18725 | RWB-S6-E6007-APP | CG-ALL-10634 | 12.5 | Add activity transferAccounts on task queue rwb-debtsale, the R-DS-29 step, with its inputs and outputs as stated in section 12.5. |
| CDC-18759 | RWB-S6-E6008-APP | CG-ALL-10659 | 12.5 | Add an Activities row for the outbound item call, provided by rwb-integration on task queue rwb-integration; name Not specified in the source documents (GAP-3006; ASM-4960). |
| CDC-18862 | RWB-S6-E6011-APP | CG-ALL-10798 | 12.5 | Add activity confirmRemittance on task queue rwb-debtsale with its contract element, or name a catalogued activity |
| CDC-18875 | RWB-S6-E6011-CON | CG-ALL-10814 | 12.5 | Add activity confirmRemittance on task queue rwb-debtsale, or name the catalogued activity that replaces it. |

### 07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx (6)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18760 | RWB-S6-E6008-APP | CG-ALL-10661 | 4, 14 | Add a new message ID for an ALS or general ledger item rejection; the story then cites that ID in section 14 in place of MSG-P2-001. |
| CDC-18763 | RWB-S6-E6008-APP | DOR-RWB-S6-E6008-APP-9 | 14 | Align MSG-P1-001 text with the standard's wording, or the standard to take this text; the standard text is not in this chunk. |
| CDC-18776 | RWB-S6-E6008-CON | CG-ALL-10706 | 4, 14 | Add a new message ID with its text for an ALS or general ledger item rejection by rwb-integration; RWB-S6-E6008-CON §14 then cites that ID in place of MSG-P2-001. |
| CDC-18779 | RWB-S6-E6008-CON | DOR-RWB-S6-E6008-CON-9 | 14 | MSG-P1-001 text updated; MSG-P2-001 row kept as before |
| CDC-18834 | RWB-S6-E6010-APP | GAP-1788 | find it | Carry MSG-S6-001, MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 in the message catalogue with a named owner and a Thai and English version; confirm the wording before wave 4 |
| CDC-18848 | RWB-S6-E6010-CON | GAP-1788 | find it | Carry MSG-S6-001, MSG-P1-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-001 with a named owner and Thai and English versions; confirm the wording before wave 4. |

### RWB-S6-E6009-APP (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18651 | RWB-S6-E6005-APP | GAP-3008 | find it | Keep H, C, I and X rows; record five consumed rows as class C with placeholders; declare no provided operation; read the claim window as a versioned parameter; allocate a reporting contract later; record the W-MAP conflict once. |
| CDC-18729 | RWB-S6-E6007-APP | GAP-3008 | find it | Apply the proposed fix there: declare no provided operation, version the claim window parameter, hold realized recovery on selling_price, and record the W-MAP conflict once. |
| CDC-18765 | RWB-S6-E6008-APP | GAP-3008 |  | Keep the H, C, I and X rows; record the five consumed rows as class C with placeholders; declare no provided operation; read the claim window as a versioned parameter; keep wave 4. |
| CDC-18813 | RWB-S6-E6009-CON | DOR-RWB-S6-E6009-CON-10 | 10 | Add empty, loading, error and no-access states for SCR-26 Award. |
| CDC-18816 | RWB-S6-E6009-CON | GAP-3008 | find it | Record the five consumed rows as class C with their placeholders, keep the H, C, I and X rows, and record the W-MAP conflict once for S6 and EP06. |

### RWB-S6-E6010-APP (5)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18652 | RWB-S6-E6005-APP | GAP-3010 | find it | Keep H, C, I and X rows; record rwb-case, rwb-access and rwb-decision as class C with placeholders; name API-S6-003 of this story as the start signal; run the unattended step under the rwb-debtsale identity; declare no adapter. |
| CDC-18766 | RWB-S6-E6008-APP | GAP-3010 |  | Keep the H, C, I and X rows; record rwb-case, rwb-access and rwb-decision as class C; name API-S6-003 of RWB-S6-E6005-APP as the start signal; run the unattended step under the rwb-debtsale identity. |
| CDC-18831 | RWB-S6-E6010-APP | GAP-3010 | 12.5 | Record rwb-case, rwb-access and rwb-decision as class C rows with placeholders; keep H, C, I and X rows; declare no provided operation. |
| CDC-18843 | RWB-S6-E6010-CON | DOR-RWB-S6-E6010-CON-10 |  | Add empty, loading, error and no-access states of SCR-26 Award to the app story |
| CDC-18845 | RWB-S6-E6010-CON | GAP-3010 |  | The plan row for the four consumed contracts and the closure operation belong to the APP story. The CON story's contract dependencies row is recorded under GAP-3011. |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 06 Data/Recovery Workbench Physical Schema v7 (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18627 | RWB-S6-E6004-CON | GAP-1771 | 12.7 | Add Ownership Map rows for bids, buyer terms, data room state, award and transfer, or hold them as entity groups with key fields; fix physical names with the S6 DB story. |
| CDC-18653 | RWB-S6-E6005-APP | GAP-1771 | n/a | Add Ownership Map rows and entity groups for data room state, buyer terms, bids, award and transfer with the PRD key fields; fix physical names with the S6 DB story. |
| CDC-18730 | RWB-S6-E6007-APP | GAP-1771 | 8 | Add Ownership Map rows and physical entity groups for data room, buyer terms, bids, award and transfer with their key fields; fix physical names with the S6 DB story. |
| CDC-18746 | RWB-S6-E6007-CON | GAP-1771 | 12 | Add owner rows and key-field entity groups for data room state, buyer terms, bids, award and transfer; keep debt_sale_lot and debt_sale_account as physical tables. |

### RWB-S6-E6010-CON (4)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18660 | RWB-S6-E6005-APP | GAP-3011 | header | Declare no provided operation; record API-S6-003 of RWB-S6-E6005-APP as the start signal; settle closure element in baseline review; keep four consumed rows; fix end state and lists; adopt REQ-S6-007 |
| CDC-18822 | RWB-S6-E6010-APP | DOR-RWB-S6-E6010-APP-21 | n/a | Publish the contract and set its build status to Done (currently Not started). |
| CDC-18823 | RWB-S6-E6010-APP | DOR-RWB-S6-E6010-APP-22 | n/a | Publish the contract fake library and record its version. |
| CDC-18832 | RWB-S6-E6010-APP | GAP-3011 |  | Declare no provided operation with API-S6-003 of RWB-S6-E6005-APP as start signal; closure element read-only in lot read and composite route; keep four consumed rows; fix end state and lists as enumerations; no adapter or posting; adopt REQ-S6-007. |

### 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18624 | RWB-S6-E6004-CON | DOR-RWB-S6-E6004-CON-1 | 1 | Add tech lead as a role, or name the URP v5 role this story's user holds in place of tech lead in section 1. |
| CDC-18707 | RWB-S6-E6006-CON | DOR-RWB-S6-E6006-CON-1 | 1 | Persona changed to Tribe lead and squad members (RW-TRIBE) |
| CDC-18876 | RWB-S6-E6011-CON | DOR-RWB-S6-E6011-CON-1 | 1 | Add 'tech lead' as a role name, or the story names an existing role code from the document. |

### RWB-S6-E6004-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18626 | RWB-S6-E6004-CON | GAP-2988 | find it | Add plan rows for the five consumed contracts, guard and outbox libraries, RWB-PLT-TE006-CON as wave 0 library, DP-08/DP-09, and one writer per rule as the item fix states. |
| CDC-18801 | RWB-S6-E6009-APP | GAP-2988 | 8 | Complete the H, C, I and X rows for the five consumed contracts and add the DP-08 and DP-09 entries as the register proposes. |
| CDC-18815 | RWB-S6-E6009-CON | GAP-2988 | find it | Apply the item's proposed fix to the take-bids plan rows: five consumed rows as class C, RWB-PLT-TE006-CON as wave 0, DP-08 guard, API-S6-005 as its operation, one writer per rule. |

### 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18628 | RWB-S6-E6004-CON | GAP-1773 | 7 | Publish the API Specification v4 paths under /api/recovery/debtsale/v1 as the contract, carry /lots as shorthand, and add the staff bid read when the S6 contract story closes |
| CDC-18755 | RWB-S6-E6008-APP | GAP-1770 | 12.5 | P1 path confirmation recorded as still pending before wave 3. |
| CDC-18782 | RWB-S6-E6008-CON | GAP-1779 | find it | Record derecognition as this service's decision; P8 builds and sends the posting and provision input; read the posted position back through the data path; no direct ALS or GL interface. |

### RWB-S6-E6007-APP (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18647 | RWB-S6-E6005-APP | GAP-3004 | find it | Keep the H, C, I and X rows; build against six contract fakes; publish AccountsTransferred via platform outbox; track TE006, E1047 and P2-E1007 as dependencies; serve the transfer element on API-S6-002 and API-S6-004; split R-DS-25 into one saga. |
| CDC-18745 | RWB-S6-E6007-CON | GAP-3004 | header | Add the outbox row for AccountsTransferred and the six consumed plan rows (rwb-case, rwb-partner, rwb-access, rwb-decision, rwb-integration, rwb-case move). |
| CDC-18865 | RWB-S6-E6011-APP | GAP-3004 | none | Keep H, C, I and X rows as they stand; add the AccountsTransferred outbox row; track RWB-PLT-TE006-CON, RWB-PLT-E1047-CON and RWB-P2-E1007-CON as dependencies; split R-DS-25 in one saga. |

### RWB-S6-E6004-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18657 | RWB-S6-E6005-APP | GAP-2989 | n/a | Publish the API-S6-005 baseline with placeholders, bind errors to section 14 message ids, declare the Bid element, confirm the three operation names and record the tag date. |
| CDC-18802 | RWB-S6-E6009-APP | GAP-2989 | 12 | Publish the field-level baseline with placeholders, bind error conditions to section 14 message IDs, confirm the three operation names and publish-first owner, record the tag date. |
| CDC-18817 | RWB-S6-E6009-CON | GAP-2989 | find it | Publish the bid baseline with placeholders, bind each error condition to a section 14 message ID, and confirm the three operation names and the publish-first question before the tag. |

### 06 Data/Recovery Workbench Physical Schema v7 (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18659 | RWB-S6-E6005-APP | GAP-1772 | n/a | Remove the foreign key fk_debt_sale_lot_buyer_partner_id to partner; keep buyer_partner_id as a uuid business key resolved through the S9 contract. |
| CDC-18732 | RWB-S6-E6007-APP | GAP-1772 | 8 | Drop fk_debt_sale_lot_buyer_partner_id on debt_sale_lot.buyer_partner_id; keep it as a uuid business key resolved through the S9 contract; create no constraint naming a table outside rwb_debtsale. |
| CDC-18747 | RWB-S6-E6007-CON | GAP-1772 | 12 | Remove fk_debt_sale_lot_buyer_partner_id to partner; keep buyer_partner_id as a uuid business key with no foreign key, resolved through the S9 contract. |

### RWB-S6-E6007-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18718 | RWB-S6-E6007-APP | DOR-RWB-S6-E6007-APP-21 | header | Bring the contract story to Done with its contract published before this story starts. |
| CDC-18719 | RWB-S6-E6007-APP | DOR-RWB-S6-E6007-APP-22 | header | Publish the contract fake library and record its published version. |
| CDC-18748 | RWB-S6-E6007-CON | GAP-3005 | 8 | Publish the transfer element, the AccountsTransferred schema and payload, and the delivery row; reconcile with TSD S6 and the event catalogue. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18734 | RWB-S6-E6007-APP | GAP-1782 | 8 | Publish LotAwarded and AccountsTransferred as CloudEvents 1.0 on rwb.debtsale.events.v1 keyed by caseId, with BACKWARD-compatible registry schemas and no personal data; give AccountsTransferred its catalogue number. |
| CDC-18750 | RWB-S6-E6007-CON | GAP-1782 | 8 | Publish AccountsTransferred and LotAwarded as CloudEvents 1.0 keyed by caseId with BACKWARD-compatible schemas; give AccountsTransferred its catalogue number. |
| CDC-18849 | RWB-S6-E6010-CON | GAP-1782 | find it | Publish LotAwarded and AccountsTransferred as CloudEvents 1.0 on rwb.debtsale.events.v1 keyed by caseId, with BACKWARD-compatible schemas, no personal data, and a catalogue number for AccountsTransferred. |

### RWB-S6-E6008-CON (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18752 | RWB-S6-E6008-APP | DOR-RWB-S6-E6008-APP-21 |  | Set build status to Done once the contract is published. |
| CDC-18753 | RWB-S6-E6008-APP | DOR-RWB-S6-E6008-APP-22 |  | Publish the contract fake library and record its version. |
| CDC-18764 | RWB-S6-E6008-APP | GAP-3007 | 12.2 | Publish placeholders and the two absence records; confirm the four operation names and interface values with owners; bind each error condition to one message ID of section 14; record the tag date in the README. |

### 06 Data/Recovery Workbench Reference Data and Lists of Values v5.xlsx (3)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18771 | RWB-S6-E6008-CON | DOR-RWB-S6-E6008-CON-5 | 9 | Resolve the P1 detcheck entries: the story adds no value to closed list LOV-BUYER-CLASS; confirm the section 9 states are not list values. |
| CDC-18840 | RWB-S6-E6010-CON | DOR-RWB-S6-E6010-CON-5 | 9 | Add CASE_CLOSED_SOLD to each of the four closed lists the story names. |
| CDC-18873 | RWB-S6-E6011-CON | DOR-RWB-S6-E6011-CON-5 | 9 | Add AWARD_CANCELED_DS to the closed list LOV-LOT-STATUS. |

### RWB-S6-E6005-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18638 | RWB-S6-E6005-APP | DOR-RWB-S6-E6005-APP-21 | Header | Set build status to Done with the contract published before this story starts. |
| CDC-18639 | RWB-S6-E6005-APP | DOR-RWB-S6-E6005-APP-22 | Header | Publish the contract fake and record its library version; no version is in the sources. |

### OTHER:_work/msr/extract (S6 extract pair) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18661 | RWB-S6-E6005-APP | GAP-2992 | header | Add the S6 FSD and TSD extract pair at the next extract pass |
| CDC-18679 | RWB-S6-E6005-CON | GAP-2992 | 18 | Add the S6 extract pair for FSD S6 Debt sale v3 and TSD S6 Debt sale v2 at the next extract pass. |

### OTHER:Work Package B2-S6-009 (plan) (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18708 | RWB-S6-E6006-CON | GAP-2996 | 4, 8, 11 | Add C rows for P5 rwb-document, P6 rwb-comms, P1 rwb-source-data, P3 rwb-case and P7 rwb-decision to the key of RWB-S6-E6006-CON. Story already declares the six consumed rows in 4, 8 and 11. |
| CDC-18709 | RWB-S6-E6006-CON | GAP-3000 | 8, 12.9 | Record the P6 rwb-comms despatch row and the P2 rwb-integration row for INT-14 that the notice channel needs. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18723 | RWB-S6-E6007-APP | CG-ALL-10630 | 12.3 | Record the payload of rwb.debtsale.AccountsTransferred.v1 on the Events row new, using the fields in RWB-S6-E6007-APP section 12.3, replacing 'not specified in the source documents' (GAP-0127; ASM-0204). |
| CDC-18741 | RWB-S6-E6007-CON | CG-ALL-10645 | 12.3 | Events row rwb.debtsale.AccountsTransferred.v1: publish the payload stated in section 12.3 of RWB-S6-E6007-CON |

### RWB-S6-E6009-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18791 | RWB-S6-E6009-APP | DOR-RWB-S6-E6009-APP-21 | header | Bring the contract story to Done with its contract published; its build status is currently Not started. |
| CDC-18803 | RWB-S6-E6009-APP | GAP-3009 | 5 | Publish the baseline with the five placeholder operation names, bind each T-A.2 error condition to a message id, declare the case boundary, the versioned claim-window parameter and the lot-read-only realized recovery, confirm names with owners, record the tag date. |

### RWB-S6-E6011-CON (2)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18856 | RWB-S6-E6011-APP | DOR-RWB-S6-E6011-APP-21 | header | Set the build status of RWB-S6-E6011-CON to Done |
| CDC-18857 | RWB-S6-E6011-APP | DOR-RWB-S6-E6011-APP-22 | header | Publish a contract fake library version and record its version number |

### Epic design record; OTHER:no file found in the source folders (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18620 | RWB-S6-E6004-CON | DOR-RWB-S6-E6004-CON-14 | 14 | Record the signed epic design sign-off for EP06 / RWB-SVC-S6, with the sign-off date, so DoR item 14 can be confirmed. |

### OTHER:TSD S6 T-A.1 and T-A.2; OTHER:contract README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18629 | RWB-S6-E6004-CON | GAP-2989 | 7 | Confirm the three operation names and the publish-first question with their owners, then record the tag date in the contract README |

### OTHER:Edge story (composite route specification named in section 15) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18631 | RWB-S6-E6004-CON | GAP-1787 | 15 | Name the screen owner of SCR-25, SCR-26 and PRT-05 in the edge story |

### RWB-S6-E6005-APP; Epic design record (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18637 | RWB-S6-E6005-APP | DOR-RWB-S6-E6005-APP-14 | header | Record the signed epic design sign-off, confirmed against the epic design record; no sign-off exists in the story or source documents. |

### RWB-S6-E5023-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18648 | RWB-S6-E6005-APP | GAP-2973 | find it | Keep the H, C, I and X rows; record rwb-case, rwb-source-data and rwb-decision as class C; record TE006 as wave 0 library; record E1072 and P7-E1073 as the rule kit; read the cap from the package; declare deviation_open and fraud_flag as inputs; adopt REQ-S6-001. |

### RWB-S6-E6002-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18649 | RWB-S6-E6005-APP | GAP-2984 | find it | Keep the H, C, I and X rows; declare rwb-partner as class C with a placeholder name and 2 s budget; declare the package as an activity on rwb-decision; record the bid as a decision record; raise the bid table for the DB story; adopt REQ-S6-004. |

### RWB-S6-E6003-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18650 | RWB-S6-E6005-APP | GAP-2986 | find it | Keep the H row; build against six contract fakes with a 2 s budget and breaker; declare no provided operation; carry three placeholders; delegate the re-offer to R-DS-28 at RWB-S6-E6005-APP; record the wave conflict once. |

### OTHER:Work Package B-S6-01 and split_plan.json (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18655 | RWB-S6-E6005-APP | GAP-1976 | n/a | Add an H row for the masked tape dependency between RWB-S6-E5025-APP and RWB-S6-E5026-APP; keep plan wave and release values. Section 19 owner naming is not in the text supplied. |

### OTHER:TSD S6 v2 Appendix T-A (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18656 | RWB-S6-E6005-APP | GAP-1970 | n/a | Confirm with the API owner whether a qualification read is added in a later version; legacy rows stay with RWB-S6-E6005-APP and RWB-S6-E5026-APP. |

### OTHER:TSD S6 v2 T3.1 and rwb-source-data contract (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18658 | RWB-S6-E6005-APP | GAP-2995 | n/a | Carry best bid, its time and price achieved in the decision record and operation contracts; confirm the score data product and v_ace field IDs before tagging; read the cap and reserve rule with package version. |

### OTHER:wave map (wave planner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18662 | RWB-S6-E6005-APP | GAP-2993 | header | State that rwb-debtsale delivers EP05 keys in wave 3 and EP06 keys in wave 4; keep wave 4 and 30 April 2027 release |

### Epic design record; OTHER:not found in the source documents (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18669 | RWB-S6-E6005-CON | DOR-RWB-S6-E6005-CON-14 | 14 | Record the signed epic design sign-off for RWB-S6-E6005-CON in the epic design record and confirm it there |

### RWB-S6-E6005-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18673 | RWB-S6-E6005-CON | DOR-RWB-S6-E6005-CON-10 | 15 | SCR-26 is screen content owned by the app story; this contract story declares no screen. |

### OTHER:Plan metadata C row (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18675 | RWB-S6-E6005-CON | GAP-2990 | 11 | Six consumed rows declared in section 11 with owners and placeholder operation names |

### 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18676 | RWB-S6-E6005-CON | GAP-1771 | 11 | Second physical table name and the physical-name source marked Not specified (GAP-1771) |

### RWB-PLT-N001-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18678 | RWB-S6-E6005-CON | GAP-1787 | 15 | Screen routing fixed; the screen owner is not named in the sources and is to be named in the edge story. |

### OTHER:Wave map (wave planner) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18680 | RWB-S6-E6005-CON | GAP-2993 | 8 | State that rwb-debtsale delivers its EP05 keys in wave 3 and its EP06 keys in wave 4; keep wave 4 and the 30 April 2027 release. |

### RWB-S6-E6006-CON (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18687 | RWB-S6-E6006-APP | DOR-RWB-S6-E6006-APP-21 | header | Move the build status from Not started to Done and publish the contract. |

### OTHER:Work Package B2-S6-009 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18696 | RWB-S6-E6006-APP | GAP-2996 | Header, 13 | Add C rows for P5 rwb-document, P6 rwb-comms, P1 rwb-source-data, P3 rwb-case and P7 rwb-decision to story line RWB-S6-E6006-APP. |

### OTHER:_work/msr/extract (S6 extract set) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18697 | RWB-S6-E6006-APP | GAP-3002 |  | Add a flat S6 extract of FSD S6 v3 and TSD S6 v2 to the extract set before the baseline is tagged. Story reads the module files directly; no story edit. |

### OTHER:Wave map document (name not specified in the source documents) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18711 | RWB-S6-E6006-CON | GAP-3001 | header | State once in the wave map that rwb-debtsale delivers its EP05 keys in wave 3 and its EP06 keys in wave 4; wave 4 and 30 April 2027 stay unchanged |

### OTHER:_work/msr/extract (flat S6 extract) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18712 | RWB-S6-E6006-CON | GAP-3002 | header | Add a flat S6 extract of the FSD and TSD files to the extract set before the baseline is tagged |

### OTHER:split_plan.json (Work Package B-S6-01) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18731 | RWB-S6-E6007-APP | GAP-1976 | 19 | Add an H row between RWB-S6-E5025-APP (L-S6-C) and RWB-S6-E5026-APP (L-S6-D); keep the plan wave and release values. |

### RWB-S6-E6007-CON; 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18733 | RWB-S6-E6007-APP | GAP-3005 | 8 | Publish the transfer element as an OpenAPI 3.1 fragment and AccountsTransferred as an AsyncAPI document for rwb-debtsale v1; carry the placeholder on unpublished consumed rows. |

### RWB-S6-E6008-APP; OTHER:SCR-26) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18777 | RWB-S6-E6008-CON | DOR-RWB-S6-E6008-CON-10 | find it | Add empty, loading, error and no-access states for SCR-25 and SCR-26. |

### RWB-S6-E6008-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18780 | RWB-S6-E6008-CON | GAP-3006 | find it | Keep the H, C, I and X rows; add class C rows for the four reads and the interface call with placeholders; adopt REQ-S6-008; add no posting column. |

### OTHER:Wave 4 derecognition and posting harness pack (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18781 | RWB-S6-E6008-CON | GAP-0454 | find it | Agree the ALS and GL answer, posting reference format, rejection codes and retry settings with ACE integration path owners at the wave 4 entry check; hold each as a fixture. |

### OTHER:TSD S6 appendix T-A and the contract README (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18783 | RWB-S6-E6008-CON | GAP-3007 | find it | Publish the baseline with placeholders and absence records; confirm the four operation names and interface values before tag; bind each error condition to a section 14 message ID; record the tag date in the README. |

### OTHER:contract fake library (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18792 | RWB-S6-E6009-APP | DOR-RWB-S6-E6009-APP-22 | header | Publish a contract fake library version for RWB-S6-E6009-CON and record its version. |

### API:(service not named); 05 Technical architecture/Recovery Workbench Temporal Workflow and Activity Catalog v1.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18824 | RWB-S6-E6010-APP | DOR-RWB-S6-E6010-APP-8 | 12 | Add bases /api/recovery/case/v1, /api/recovery/access/v1 and /api/recovery/decision/v1 to the API yaml; align the DebtSaleWorkflow task queue and namespace to the catalog. |

### 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18829 | RWB-S6-E6010-APP | DOR-RWB-S6-E6010-APP-11 | 11 | Reconcile the personal-data class of the debt_sale_account fields read here (for example borrower_code) with the story statement that none is carried. |

### OTHER:FSD S6 (A1.1 and prerequisite lines) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18833 | RWB-S6-E6010-APP | GAP-1789 | header | Map FEAT-APD-01, FEAT-DRI-07, FEAT-RDF-15 and FEAT-OCC-07 to owning contracts; add FEAT-DBS-05 and FEAT-DBS-16 to the A1.1 dependency list. |

### 05 Technical architecture/Recovery Workbench Kafka Topic and Event Catalog v1.xlsx; 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx; 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18835 | RWB-S6-E6010-APP | GAP-1782 | find it | Publish EV-23 LotAwarded and AccountsTransferred as CloudEvents 1.0 on rwb.debtsale.events.v1 keyed by caseId, with BACKWARD-compatible registry schemas, no personal data, and give AccountsTransferred its catalogue number |

### OTHER:FSD S6 (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18847 | RWB-S6-E6010-CON | GAP-1789 | find it | Map FEAT-DRI-07, FEAT-RDF-15, FEAT-APD-01 and FEAT-OCC-07 to the owning services' contracts (P7, P1, P6); add FEAT-DBS-05 and FEAT-DBS-16 to the A1.1 dependency list. |

### RWB-S6-E6011-CON; 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18866 | RWB-S6-E6011-APP | GAP-3013 | none | Tag the baseline with placeholders; publish the OpenAPI fragment for the two elements and the AsyncAPI fragment for ProceedsMatched; derive fakes from them and fail the build on drift; correct rows when owners publish names and envelope. |

### API:(service not named); OTHER:P1) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18867 | RWB-S6-E6011-CON | CG-ALL-10806 | 12.2 | Declare REST base /api/recovery/source-data/v1 for the ACE payment data read. |

### API:(service not named); OTHER:P3) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18868 | RWB-S6-E6011-CON | CG-ALL-10807 | 12.2 | Declare REST base /api/recovery/case/v1 for the case read. |

### API:(service not named); OTHER:S9) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18869 | RWB-S6-E6011-CON | CG-ALL-10808 | 12.2 | Declare REST base /api/recovery/partner/v1 for the buyer scorecard read. |

### API:(service not named); OTHER:P4) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18870 | RWB-S6-E6011-CON | CG-ALL-10809 | 12.2 | Declare REST base /api/recovery/access/v1 for the authorise and capability read. |

### API:(service not named); OTHER:P7) (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18871 | RWB-S6-E6011-CON | CG-ALL-10810 | 12.2 | Declare REST base /api/recovery/decision/v1 for the rule package read. |

### OTHER:Split plan; RWB-S6-E6011-APP (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18878 | RWB-S6-E6011-CON | GAP-3012 |  | Record the six consumed contracts, the inbox library RWB-PLT-TE006-CON, the rule kit RWB-PLT-E1072-CON, the settlement stamp, the GL prerequisite and wave 4 as tracked items; keep the H, C, I and X rows unchanged. |

### 05 Technical architecture/Recovery Workbench Service Contract Catalog v1.md (1)

| CDC ID | Story | Item | Section | Change |
|---|---|---|---|---|
| CDC-18879 | RWB-S6-E6011-CON | GAP-3013 |  | Publish the OpenAPI fragment for the settlement element and the AsyncAPI fragment for ProceedsMatched; correct the placeholder rows once operation names and the envelope are published. |

## 6. Register gaps linked to this service (Gap Register v2 status)

| GAP ID | Title | Owner role | Status |
|---|---|---|---|
| GAP-0454 | The derecognition and general ledger posting harness pack for the debt sale journey is not specified | Integration lead | Resolved (directive) |
| GAP-1484 | The debt sale service wave is earlier than the business epic wave that awards a lot | Solution architect | Resolved (directive) |
| GAP-1770 | FSD S6 reads the ACE views directly, while Architecture v5 allows only rwb-source-data to read them and gives S6 no cell to P1 | Solution architect | Resolved (directive) |
| GAP-1771 | The Ownership Map and the physical schema give this service two tables, while Architecture v5 gives it six things to hold | Data architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1772 | The physical schema keeps a foreign key from debt_sale_lot to partner, which sits in another service's schema | Data architect | Resolved (directive) |
| GAP-1773 | The lot API is named /lots on slide 19 and /debt-sale-lots in the API specification, and no staff read of the bids exists | Solution architect | Resolved (directive) |
| GAP-1774 | The buyer data room is published under /partner, while the architecture admits buyers only through the partner gateway and S6 has no cell to S9 | Solution architect | Resolved (directive) |
| GAP-1775 | The customer notices of a sale have three different homes in three sources | Solution architect | Resolved (directive) |
| GAP-1779 | Derecognition and the general ledger posting have no interface and no clear owner | Solution architect | Resolved (directive) |
| GAP-1780 | DebtSaleWorkflow is a saga per lot across five services, while the v5 case model is one child workflow per case per stage | Solution architect | Resolved (directive) |
| GAP-1782 | AccountsTransferred has no event number and neither debt sale event has a published schema | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1787 | The three screens have no owner in the sources read | Solution architect | Resolved (directive) |
| GAP-1788 | No source states who owns the wording of the debt sale messages and their Thai and English versions | Business analyst, S6 | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-1789 | The FSD's prerequisite feature codes belong to four other modules and two of its own features are missing from its dependency list | Solution architect | Resolved (directive) |
| GAP-1950 | RWB-S6-E5023: the 54 percent cap named in legacy AC1 is carried by R-DS-19, whose criterion and test belong to RWB-S6-E6005-APP | Business analyst | Resolved (directive) |
| GAP-1966 | RWB-S6-E6001: the award operation and the A right are rowed as this story's although the award belongs to RWB-S6-E6005-APP, and the committee approver of the FSD has no role row | Solution architect | Resolved (directive) |
| GAP-1970 | RWB-S6-E6002: TSD S6 T-A publishes no KYC operation and the two legacy endpoint rows belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP | Solution architect | Resolved (directive) |
| GAP-1972 | RWB-S6-E6002: the story is EP06 wave 4 while rwb-debtsale is created in wave 3 | Delivery lead | Resolved (directive) |
| GAP-1976 | WP B-S6-01: the data-room story publishes a masked tape that no story of this Work Package builds, and the EP06 keys carry release 30 April 2027 against a wave 3 service | Solution architect | Resolved (directive) |
| GAP-2973 | RWB-S6-E5023-APP: the eligibility slice has no plan row for its four consumed contracts, its outbox library, its rule kit, the 54 percent cap criterion or the two eligibility inputs | Solution architect | Resolved (directive) |
| GAP-2984 | RWB-S6-E6002-APP: the qualification step has no operation, no bid table, no published names for the buyer read, the case move and the package, and no partner arrow in the connection matrix | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2986 | RWB-S6-E6003-APP: the bar slice has no plan row for its six consumed contracts, no published bar operation, no panel or lot-status vocabulary, no next-bidder field and no window row | Solution architect with the owners of rwb-partner, rwb-case, rwb-access and rwb-decision | Resolved (directive) |
| GAP-2988 | RWB-S6-E6004-APP: the take-bids slice has no plan row for its five consumed contracts, its guard and outbox libraries, the publish-first story of API-S6-005, the bid and realised-recovery columns, the two rules it shares with sibling keys, the reporting destination of R-DS-34, its wave or its requirement id | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2989 | RWB-S6-E6004-CON: the bid operation has no field-level baseline, the consumed operation names are unpublished, the publish-first story of API-S6-005 is contested, the bid fact has no column set and the step has no event, Schedule or requirement row | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2990 | RWB-S6-E6005: the award step carries an empty C row although it consumes rwb-case, rwb-decision, rwb-access and rwb-source-data, and three consumed operations have no published name | Solution architect | Resolved (directive) |
| GAP-2991 | RWB-S6-E6005: the step publishes LotAwarded (EV-23) while DP-09 and its outbox library are absent from the plan's pattern set and H row | Solution architect | Resolved (directive) |
| GAP-2992 | RWB-S6-E6005: the run's extract folder holds no FSD or TSD extract for module S6, so the module files stand in | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2993 | RWB-S6-E6005: EP06 puts the story in wave 4 and release 30 April 2027 while rwb-debtsale is an Architecture v5 wave 3 service | Delivery lead | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2994 | RWB-S6-E6005: the four legacy criteria span three sibling stories, R-DS-23 confirms the award, and the requirement mapping differs between the FSD and the TSD | Business analyst | Resolved (directive) |
| GAP-2995 | RWB-S6-E6005: no column or field holds the bid or the award price, the buyer-class rule and the score field IDs are unstated, and the score is a view only rwb-source-data may read | Data steward | Resolved (directive) |
| GAP-2996 | RWB-S6-E6006: the agreement-and-notices step carries an empty C row although it consumes rwb-document, rwb-comms, rwb-source-data, rwb-case and rwb-decision, and five consumed operations have no published name | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-2997 | RWB-S6-E6006: the legacy endpoint row and R-DS-23 name the award, while API-S6-003 and R-DS-19 are RWB-S6-E6005-APP's and LotAwarded is attributed to that story | Business analyst | Resolved (directive) |
| GAP-2998 | RWB-S6-E6006: the lot has no column for the agreement or the notice references, no source states the lot status at award, and no requirement row names the agreement or the notices | Solution architect | Resolved (directive) |
| GAP-2999 | RWB-S6-E6006: the addressee of the notices is the ACE customer view v_ace_customer, and no source gives the notice types, the templates or the masking rule of the letter | Solution architect | Resolved (directive) |
| GAP-3000 | RWB-S6-E6006: the FSD names WIN as an integration point and FEAT-OCC-07 as the prerequisite, and neither is a row of the C, I or X set of this story | Solution architect | Resolved (directive) |
| GAP-3001 | RWB-S6-E6006: EP06 puts the story in wave 4 and release 30 April 2027 while rwb-debtsale is an Arch v5 wave 3 service | Delivery lead | Resolved (directive) |
| GAP-3002 | RWB-S6-E6006: the extract folder holds no FSD or TSD file whose name contains S6, so the module documents stand in for the extract | Business analyst | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3004 | RWB-S6-E6007-APP: the transfer slice has no plan row for its five consumed contracts or the buyer-file delivery, no outbox row although it publishes AccountsTransferred, no transfer operation and no column set to record the transfer | Solution architect | Resolved (directive) |
| GAP-3005 | RWB-S6-E6007-CON: the transfer element, the AccountsTransferred schema and payload, the buyer-file delivery contract and the consumed operation names have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3006 | RWB-S6-E6008-APP: the derecognition and posting slice has no plan row for its four consumed contracts and its interface call, no posting column, no published operation names and no requirement id | Solution architect | Resolved (directive) |
| GAP-3007 | RWB-S6-E6008-CON: the contract baseline declares no operation and no answer property because TSD S6 T-A publishes no derecognition or posting surface and no column carries the result, and the four operation names and the interface values are unpublished | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3008 | RWB-S6-E6009-APP: the put-back review has no published operation, its claim window, claim reason and realized-recovery figure have no field, column or event, its consumed contracts have no plan row, and two of its four criteria execute rules owned by sibling stories | Solution architect | Resolved (directive) |
| GAP-3009 | RWB-S6-E6009-CON: the claim element, the claim-window parameter, the realized-recovery element, the consumed operation names and the event set have no published baseline | Solution architect | Resolved (directive) |
| GAP-3010 | RWB-S6-E6010-APP: the closure slice has no plan row for its four consumed contracts, no published closure operation, an open-action set no source enumerates, no right for an unattended step and an ALS and GL integration point it does not own | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |
| GAP-3011 | RWB-S6-E6010-CON: the closure baseline has no published closure operation or closure element schema, no plan row for its four consumed contracts, no operation names for the case read, the closure answer or the authorise call, and no right for the unattended step | Solution architect | Resolved (directive) |
| GAP-3012 | RWB-S6-E6011-APP: the settle-and-cancel slice has no plan row for its six consumed contracts, its inbox library, its rule kit, its settlement stamp, its GL prerequisite or its EP06 wave | Solution architect | Resolved (directive) |
| GAP-3013 | RWB-S6-E6011-CON: the consumed operation names, the ProceedsMatched envelope, the settlement element and the field-level types have no published baseline | Solution architect | Accepted (directive); change listed in the Cross-document Change Register v1 |

## 7. Unconfirmed assumptions (tied to a business decision)

None.

## 8. Lint findings on the staged stories

None.
