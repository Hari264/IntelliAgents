---
doc_id: SCR-PED-01
title: "Script: Pre-Existing Disease Waiting Period"
product: HEALTH_GOLD
version: na
effective_from: 2024-01-01
effective_to: 9999-12-31
doc_type: script
audience: [service, adjuster]
sensitivity: General
---

## Section 1 When to Use

Use this script when a claim has been declined or put on hold for one of the following reasons.

CL-217 — Treatment for pre-existing disease within PED waiting period: the claimed condition has been assessed as a Pre-Existing Disease under the Policy Wording and the applicable Pre-Existing Disease waiting period had not been completed as at the date of loss.

CL-220 — Pre-existing disease not disclosed at proposal: the claimed condition relates to a condition that was not declared on the proposal form at inception and which the underwriting team has identified as potentially a Pre-Existing Disease.

Before making the call, retrieve the following information from the claims management system: (a) the claim reference {claim_id}; (b) the applicable rejection code {rejection_code}; (c) the clause reference {clause_ref} (Clause 4.3 of the applicable Policy Wording); (d) the eligible date from which Pre-Existing Disease cover applies under the policy {eligible_date}; and (e) for CL-217, the applicable waiting period in months {waiting_months}.

## Section 2 Customer Script

**Script for CL-217 — Pre-Existing Disease within waiting period:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] calling from Aarogya Shield General Insurance Ltd. with reference to your health insurance claim number {claim_id}. Is this a convenient time to speak?

[If yes, continue. If no, offer to call back and note the preferred time.]

I am calling to explain the outcome of our assessment of your claim. We have completed our review and I would like to walk you through our decision.

Your claim has been assessed under rejection code {rejection_code}. Our medical team has reviewed your records and found that the condition for which you were treated is a Pre-Existing Disease under Clause 1.2.1 of your policy wording — that is, a condition for which you had received medical advice or treatment before your policy commenced.

Under Clause {clause_ref} of your Health Insurance Policy Wording, a waiting period applies to Pre-Existing Diseases. Based on your policy, the waiting period for Pre-Existing Disease cover had not been completed as at the date of your hospitalisation. Your policy provides cover for Pre-Existing Disease claims from {eligible_date}.

We understand this is disappointing news. You do have options. You may raise a written grievance with our Grievance Redressal Officer, who will independently review the decision. Additionally, if you have prior continuous insurance cover with another insurer that we have not yet credited to your policy, portability credit under Clause 9.2 may reduce your waiting period. Please let us know if this applies.

Would you like me to give you the contact details for the Grievance Redressal Officer? I can also send this information to you by email if you prefer."

**Script for CL-220 — Pre-Existing Disease not disclosed:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] calling from Aarogya Shield General Insurance Ltd. regarding your health insurance claim number {claim_id}.

I am calling to let you know that during the assessment of your claim under rejection code {rejection_code}, our underwriting team has identified that the condition related to your claim may not have been declared on your proposal form when your policy was taken out. This is being reviewed under Clause {clause_ref} of your Policy Wording.

Our team will be writing to you shortly to explain the next steps and what information we may need from you. If you have documents relating to your prior medical history, it would be helpful to have them ready.

If you have any questions, please call our helpline and quote your claim reference {claim_id}. Thank you for your time."

## Section 3 Do and Do Not

DO: confirm the customer's identity before discussing the claim; be calm and empathetic; read the eligible date {eligible_date} clearly so the customer understands when they will be eligible; offer to send information in writing; provide the Grievance Redressal Officer's contact details for CL-217.

DO NOT: promise to reverse the decision; state specific waiting period figures — use {eligible_date} to explain eligibility instead of reciting month counts; use the words "fraud" or "suspicious" at any point; for CL-220, speculate about the underwriting outcome or suggest that the policy will be cancelled; provide the Grievance Redressal Officer's details for CL-220 before the underwriting review is completed, unless the customer specifically asks.
