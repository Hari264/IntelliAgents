---
doc_id: SCR-EXCL-01
title: "Script: Exclusions"
product: HEALTH_GOLD
version: na
effective_from: 2024-01-01
effective_to: 9999-12-31
doc_type: script
audience: [service, adjuster]
sensitivity: General
---

## Section 1 When to Use

Use this script when a claim has been declined because an exclusion applies under the Policy Wording. This script covers five rejection codes.

CL-401 — Permanent exclusion applies: the claim relates to a condition or event permanently excluded under Clause 5.1 (e.g. war, nuclear event, self-inflicted injury).

CL-405 — Cosmetic treatment excluded: the treatment is a cosmetic or aesthetic procedure excluded under Clause 5.4.

CL-410 — Experimental or unproven treatment: the treatment is experimental or not approved for the relevant indication under Clause 5.3.

CL-415 — Maternity not covered or within maternity waiting period: the claim is for maternity-related expenses that are either not covered under the applicable policy version (Clause 2.6), or the maternity waiting period under Clause 2.6 had not been completed.

CL-420 — Self-inflicted injury or substance abuse: the claim relates to self-inflicted injury or treatment arising from substance abuse, excluded under Clause 5.2.

Before calling, confirm from the claims management system: the claim reference {claim_id}; the applicable rejection code {rejection_code}; the specific exclusion clause {clause_ref}; and for CL-415, whether the applicable policy version covers maternity and, if so, whether the waiting period applies (check {eligible_date} if a waiting period applies).

## Section 2 Customer Script

**Script for CL-401 — Permanent exclusion:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id}. I am calling to explain the outcome under rejection code {rejection_code}.

We have assessed your claim and found that it relates to a condition or event that is permanently excluded from cover under Clause {clause_ref} of your Policy Wording. This exclusion applies regardless of when the policy was taken out or how long cover has been in place.

I can read the relevant exclusion clause to you if that would help, or I can send the relevant section to you in writing. You also have the right to raise a grievance with our Grievance Redressal Officer. Shall I give you those details?"

**Script for CL-405 — Cosmetic treatment:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under rejection code {rejection_code}.

Your claim has been assessed and the treatment falls within the exclusion for cosmetic or aesthetic procedures under Clause {clause_ref} of your Policy Wording. Procedures whose primary purpose is to alter or improve appearance rather than to treat a diagnosed disease or injury are not covered under your policy.

If you believe the treatment was required for a medical reason that is distinct from cosmetic purposes, you have the right to raise a grievance and request a review. Shall I give you the contact details?"

**Script for CL-410 — Experimental treatment:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under rejection code {rejection_code}.

Your claim has been assessed and the treatment has been classified as experimental or unproven under Clause {clause_ref} of your Policy Wording. Treatments that are not recognised as a standard treatment for the relevant condition by applicable medical authorities, or that are not approved for the relevant indication, are not covered under your policy.

If you believe the treatment meets the standard treatment criteria for your condition, you may raise a grievance and we can refer the matter to an independent medical review. Would you like the Grievance Redressal Officer's contact details?"

**Script for CL-415 — Maternity:**

[Check the applicable policy version before calling. Use the appropriate version below.]

If maternity is not covered under the applicable policy:
"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under rejection code {rejection_code}.

I am calling to let you know that maternity expenses, including expenses related to childbirth and related care, are not covered under your current policy under Clause {clause_ref}. This applies to your policy as it stands.

You have the right to raise a grievance if you wish. Shall I provide those details?"

If maternity is covered but within the waiting period:
"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under rejection code {rejection_code}.

Your policy does include maternity cover under Clause {clause_ref}. However, maternity cover under your policy requires a waiting period that had not been completed as at the date of delivery. Your policy provides maternity cover from {eligible_date}.

If you believe this assessment is incorrect, you have the right to raise a grievance. Shall I give you those contact details?"

**Script for CL-420 — Self-inflicted injury or substance abuse:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. regarding claim {claim_id} under rejection code {rejection_code}.

Your claim has been assessed and the condition relates to a category excluded under Clause {clause_ref} of your Policy Wording. I will send you our written rejection letter which contains the full details of the exclusion that applies.

If you believe this assessment is incorrect, you have the right to raise a grievance with our Grievance Redressal Officer. I can give you those contact details. Would you like them?"

## Section 3 Do and Do Not

DO: always cite the specific clause {clause_ref} in the conversation; offer to send the exclusion wording in writing; provide Grievance Redressal Officer contact details for every code; for CL-415, confirm the applicable policy version in the system before calling; for CL-420, keep the call brief and professional — the written rejection letter provides the full explanation.

DO NOT: volunteer details about why the claim triggered the exclusion assessment beyond what is needed; speculate about the outcome of a grievance; for CL-415, tell the customer their policy version before confirming it in the system; use judgemental language for CL-420; mention fraud or investigation for any code in this script.
