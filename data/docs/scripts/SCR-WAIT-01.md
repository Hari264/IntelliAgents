---
doc_id: SCR-WAIT-01
title: "Script: Waiting Periods"
product: HEALTH_GOLD
version: na
effective_from: 2024-01-01
effective_to: 9999-12-31
doc_type: script
audience: [service, adjuster]
sensitivity: General
---

## Section 1 When to Use

Use this script when a claim has been declined because a waiting period had not been completed as at the date of loss. This script covers four rejection codes.

CL-101 — Illness within initial waiting period: the date of loss falls within the initial waiting period applicable from the policy start date (Clause 4.1).

CL-201 — Treatment within specific disease waiting period: the claimed condition is subject to a specific waiting period under Clause 4.2, and the waiting period had not been completed.

CL-205 — Joint replacement within waiting period: the claim is for joint replacement surgery (Arthroplasty) and the applicable waiting period under Clause 4.2 had not been completed. Before calling, also check the Policy Schedule for the Waiting Period Waiver Rider (RID-WPW-01); if the rider is present and the claim date falls under its terms, escalate to the adjuster for re-assessment before calling the customer.

CL-510 — Continuity of prior cover not established: the customer's portability credit from a prior insurer has not been confirmed, and the waiting period therefore runs from the current policy start date (Clause 9.2).

Before calling, retrieve from the claims management system: claim reference {claim_id}; rejection code {rejection_code}; the applicable policy clause {clause_ref}; the date from which the customer becomes eligible for the relevant cover {eligible_date}; the applicable waiting period in months {waiting_months}; and for CL-205, whether the Waiting Period Waiver Rider is on the Policy Schedule.

## Section 2 Customer Script

**Script for CL-101 — Initial waiting period:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id}. Is this a convenient time?

I am calling to explain the outcome of your claim assessment under rejection code {rejection_code}. Your claim has been assessed and we found that the date of your hospitalisation falls within the initial waiting period of your policy under Clause 4.1. Under your policy, a waiting period applies from the policy start date for illnesses and diseases. Accidents are covered from day one, but the condition on your claim is not an accidental injury.

Your policy provides illness cover from {eligible_date}. If you have any questions about why your condition is not covered as an accidental injury, I can take a note and arrange for our medical team to review.

You also have the right to raise a grievance with our Grievance Redressal Officer. Would you like those contact details?"

**Script for CL-201 — Specific disease waiting period:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id}. I am calling to explain the assessment outcome under rejection code {rejection_code}.

Your claim is for a condition that is subject to a specific waiting period under Clause {clause_ref} of your Policy Wording. The waiting period for this condition is {waiting_months} months from your policy start date. The waiting period had not been completed as at your date of hospitalisation.

Your policy provides cover for this condition from {eligible_date}.

If you have maintained prior continuous health insurance cover with another insurer, a portability credit may apply under Clause 9.2 of your policy and could reduce your waiting period. If this has not already been considered, please let me know and I will refer it for review.

Would you like the contact details for our Grievance Redressal Officer?"

**Script for CL-205 — Joint replacement waiting period:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id}. I am calling regarding rejection code {rejection_code} on your joint replacement claim.

Under Clause {clause_ref} of your Policy Wording, a waiting period applies to joint replacement surgery. The waiting period for joint replacement cover under your policy is {waiting_months} months. The waiting period had not been completed as at your date of surgery.

Your policy provides cover for joint replacement surgery from {eligible_date}.

One thing I want to flag: if your Policy Schedule includes the Waiting Period Waiver Rider, the joint replacement waiting period may be treated differently. I will check this and call you back if there is a change to our assessment. [If rider confirmed absent:] Our records confirm the rider is not on your policy.

If you have prior continuous cover with another insurer that has not yet been credited, a portability reduction may apply under Clause 9.2. Do let us know.

You may also raise a grievance if you wish to challenge this assessment. Shall I give you those details?"

**Script for CL-510 — Portability continuity not established:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under code {rejection_code}.

Our records show that when your policy was taken out, portability credit from a prior insurer was applied. However, we have not yet been able to confirm continuous cover under your prior policy, which means the full waiting period under Clause 9.2 currently runs from your current policy start date.

To resolve this, we need the following documents from your prior insurer: renewal certificate or policy certificate showing continuous cover, and any relevant policy documents. If you can provide these, we will re-assess your portability credit and may be able to bring forward your eligible date.

Please send these to us at [details] quoting claim {claim_id}."

## Section 3 Do and Do Not

DO: check whether the Waiting Period Waiver Rider is on the Policy Schedule before calling for CL-205 — if it is present, escalate to the adjuster first; use {eligible_date} to explain when cover begins rather than reciting month counts; mention portability credit as an option where applicable; offer to send information in writing.

DO NOT: quote specific waiting period month counts from the policy wording directly — use {waiting_months} (filled from the system) and confirm the month count with the adjuster for the applicable wording version; promise that portability credit will change the outcome before it has been reviewed; tell the customer the decision is final without mentioning the grievance route.
