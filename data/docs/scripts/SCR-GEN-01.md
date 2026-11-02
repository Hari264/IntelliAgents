---
doc_id: SCR-GEN-01
title: "Script: General Claim Queries"
product: HEALTH_GOLD
version: na
effective_from: 2024-01-01
effective_to: 9999-12-31
doc_type: script
audience: [service, adjuster]
sensitivity: General
---

## Section 1 When to Use

Use this script for general claim queries and for situations not covered by the more specific scripts. This script covers seven rejection codes.

CL-120 — Hospitalisation not medically necessary: the claim has been declined because the treating team's assessment indicates the hospitalisation was not Medically Necessary under Clause 2.1.

CL-125 — Treatment could be taken on an outpatient basis: the admission was not necessary because the treatment could have been provided without hospitalisation, under Clause 2.1.

CL-130 — Pre or post hospitalisation expenses outside allowed days: expenses incurred before 30 days before admission or after 60 days after discharge are not payable under Clause 2.2.

CL-140 — Procedure not in day care list: the claim is for a procedure performed as a day care admission but the procedure is not on the Company's Day Care list under Clause 2.3.

CL-501 — Cashless not available at non-network hospital: the Insured Person sought treatment at a hospital that is not on the Company's Network Hospital list, so cashless cannot be processed (Clause 7.1). Reimbursement is available.

CL-505 — Policy not in force on date of loss: the policy was not active on the date of the claimed hospitalisation, including lapses during a grace period (Clause 9.1).

CL-601 — Claim under additional review: the claim is under internal review. No further detail is given to the customer. The script for this code is strictly limited — see Section 2 below.

Before calling, check the claims management system for the claim reference {claim_id} and the applicable rejection code {rejection_code}.

## Section 2 Customer Script

**Script for CL-120 — Hospitalisation not medically necessary:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under rejection code {rejection_code}.

We have assessed your claim and our medical team has determined that, based on the clinical records, the hospitalisation may not meet the Medically Necessary criteria under Clause 2.1 of your Policy Wording. This means the clinical evidence reviewed does not demonstrate that admission as an in-patient was required for the treatment of your condition at the time.

I can share a summary of the medical opinion with you, and you have the right to raise a grievance and request an independent review. The Grievance Redressal Officer can arrange for the matter to be reviewed by a second medical opinion if you wish.

Would you like the Grievance Redressal Officer's contact details?"

**Script for CL-125 — Outpatient treatment:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under code {rejection_code}.

Our medical team has assessed your claim and concluded that the treatment you received could have been provided without in-patient admission — that is, on an outpatient basis. Under Clause 2.1, cover applies when in-patient hospitalisation is Medically Necessary. Where treatment is available as outpatient care, the hospitalisation does not qualify under this clause.

If your policy includes the Outpatient Care Rider, some outpatient expenses may be covered under that rider instead. I can check whether this applies to your policy.

You also have the right to raise a grievance. Shall I give you those details?"

**Script for CL-130 — Pre or post hospitalisation expenses outside allowed days:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under code {rejection_code}.

Under Clause 2.2 of your Policy Wording, expenses before admission are covered for up to 30 days before the date of admission, and expenses after discharge are covered for up to 60 days from the date of discharge. The expenses you have claimed fall outside these windows and are therefore not payable under your policy.

If you have any questions about which expenses were included and which were not, I can walk you through the calculation. You also have the right to raise a grievance."

**Script for CL-140 — Procedure not in day care list:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under code {rejection_code}.

Your claim is for a procedure performed as a day care admission — that is, with less than 24 hours of hospitalisation. Under Clause 2.3 of your Policy Wording, day care cover applies only for procedures listed in the Company's Day Care Procedure list. The procedure in your claim is not on that list.

If your admission lasted less than 24 hours and the procedure is not on the day care list, the claim does not qualify under Clause 2.1 either. If you believe the procedure should be on the list, you may raise a grievance. Shall I give you those details?"

**Script for CL-501 — Cashless at non-network hospital:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under code {rejection_code}.

Cashless treatment under your policy is available only at hospitals on our Network Hospital list, under Clause 7.1. The hospital where you were treated is not currently on our network. For this reason, a cashless facility cannot be processed for this admission.

However, you may still be able to recover your eligible expenses through our reimbursement route under Clause 7.2. To do this, please submit your original bills, discharge summary and other documents as listed in Clause 6.2 within 30 days of your discharge date. Our team will then assess and reimburse the eligible amount.

Would you like me to confirm the documents required and the submission address?"

**Script for CL-505 — Policy not in force:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under code {rejection_code}.

Our records show that your policy was not in force on the date of your hospitalisation. Under Clause 9.1, if the renewal premium was not received before the expiry of the grace period, the policy lapses and no cover is available for losses during that period.

If you believe your policy was in force on the date of your claim, please contact our customer service team and they will be able to check the policy records. If you have a receipt for a premium payment, please share it with us for verification."

**Script for CL-601 — Claim under additional review:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id}.

I am calling to let you know that your claim is currently under additional review. Our team will be in touch with you as soon as the review is complete. If you have any questions in the meantime, please call our helpline and quote your claim reference number {claim_id}.

Thank you for your patience."

## Section 3 Do and Do Not

DO: for CL-120 and CL-125, offer to share the medical opinion summary and the grievance route; for CL-501, actively offer the reimbursement route and document submission guidance; for CL-505, ask if the customer has a payment receipt before ending the call; for all codes, document the call outcome in the claims management system.

DO NOT: for CL-601, say anything beyond what is in the script above — do not mention fraud, investigation, SIU, suspicion or any reason for the additional review under any circumstances; for CL-120 and CL-125, read out the full medical opinion — summarise it only; for CL-505, tell the customer their policy has been cancelled without confirming the lapse details in the system first.
