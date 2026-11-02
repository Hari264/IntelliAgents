---
doc_id: SCR-SUBLIM-01
title: "Script: Sub-limit or Sum Insured Exhausted"
product: HEALTH_GOLD
version: na
effective_from: 2024-01-01
effective_to: 9999-12-31
doc_type: script
audience: [service, adjuster]
sensitivity: General
---

## Section 1 When to Use

Use this script when a claim has been settled for less than the claimed amount because either the sum insured has been exhausted or a procedure sub-limit applies.

CL-301 — Sum insured exhausted: the total sum insured available to the Insured Person in the current Policy Year has been exhausted by prior claims. The current claim cannot be paid in full or in part.

CL-310 — Procedure sub-limit exceeded: the claim is for a procedure that is subject to a monetary sub-limit under Clause 3.2 of the Policy Wording, and the claimed amount exceeds that sub-limit.

Before calling, retrieve the claim reference {claim_id}, the rejection code {rejection_code}, the applicable clause reference {clause_ref}, and the relevant figures: for CL-301, the total sum insured and the amount already utilised; for CL-310, the applicable sub-limit and the claimed amount. Have the utilisation statement or sub-limit details ready to share with the customer.

## Section 2 Customer Script

**Script for CL-301 — Sum insured exhausted:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding your health insurance claim number {claim_id}. I am calling about the assessment of your claim under rejection code {rejection_code}.

I want to explain why we are unable to pay this claim. Under Clause {clause_ref} of your Policy Wording, the total sum insured represents the maximum amount we can pay in a Policy Year for all your claims combined. Based on the claims already settled this Policy Year, your sum insured has been fully utilised, and no further amount is available for this Policy Year.

I can send you a utilisation statement showing all the claims settled this year and the amounts paid, so you can see exactly how the sum insured has been used. Would you like me to arrange that?

Your sum insured will reset at the start of your next Policy Year upon renewal. At that point, you will have the full sum insured available again.

Is there anything else I can help you with?"

**Script for CL-310 — Sub-limit exceeded:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding your health insurance claim number {claim_id}. I am calling about the settlement amount for your claim under rejection code {rejection_code}.

Your claim is for a procedure that is subject to a monetary sub-limit under Clause {clause_ref} of your Policy Wording. Under your policy, the maximum amount payable for this type of procedure is ₹{sub_limit_amount}. The expenses you claimed were above this sub-limit.

We have paid ₹{sub_limit_amount} — the maximum allowed under the sub-limit. The amount above the sub-limit is not payable from any other benefit under your policy.

I understand this may be more than you expected to pay out of pocket. If you have any questions about the sub-limit or the calculation, I am happy to explain further, or I can send the calculation to you in writing.

If you believe the sub-limit has been applied incorrectly, you have the right to raise a grievance with our Grievance Redressal Officer. Would you like those details?"

## Section 3 Do and Do Not

DO: have the utilisation statement or sub-limit figures ready before calling; offer to send the calculation or utilisation statement in writing; for CL-301, mention that the sum insured resets at renewal; provide the Grievance Redressal Officer contact details on request; keep the tone sympathetic — exhausting a sum insured can be a difficult situation for the customer.

DO NOT: tell the customer there is any way to unlock additional cover mid-year that is not available under the policy; imply that the sub-limit can be increased for the current claim; quote sub-limit amounts from the policy wording without verifying from the system — use {sub_limit_amount} as filled from the claims management system for the applicable policy version.
