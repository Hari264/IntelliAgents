---
doc_id: SCR-CLOSE-01
title: "Script: Claim Closure and Payment Confirmation"
product: HEALTH_GOLD
version: na
effective_from: 2024-01-01
effective_to: 9999-12-31
doc_type: script
audience: [service, adjuster]
sensitivity: General
---

## Section 1 When to Use

Use this script when: (a) an agent is making an outbound call to confirm to the Policyholder that a reimbursement claim has been settled and payment has been made; or (b) a Policyholder contacts the service team to ask about a settlement amount that has appeared in their bank account or about a settlement letter they have received.

Before calling, retrieve from the claims management system: claim reference {claim_id}; policy number {policy_number}; the total settlement amount paid {settlement_amount}; the payment date {payment_date}; a summary of any amounts that were not approved, with the reason for each {unapproved_summary}; and whether the settlement is a full or partial settlement.

If the claim was rejected in full rather than settled, use SOP-REJCOMM-01 and the applicable rejection script from the SCR series rather than this script.

## Section 2 Customer Script

**Part A — Outbound call: payment confirmed:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] from Aarogya Shield General Insurance Ltd. I am calling with reference to your health insurance claim number {claim_id} on policy number {policy_number}.

I am pleased to let you know that your claim has been settled and a payment of ₹{settlement_amount} has been made to your registered bank account on {payment_date}. This amount should appear in your account within the standard bank processing period.

A written settlement letter confirming the breakdown of the settlement has been or will shortly be sent to your registered address or email.

[If a partial settlement with unapproved amounts:]

I would also like to let you know that a part of your claim — {unapproved_summary} — was not approved. The settlement letter explains the reason in detail, with the specific policy clause. If you would like me to explain that now, I am happy to do so.

You have the right to raise a grievance if you disagree with any part of this assessment. I can give you the contact details for our Grievance Redressal Officer, or the information will be in the settlement letter. Would you like those details now?

Is there anything else I can help you with?"

---

**Part B — Inbound enquiry about a received payment:**

"Thank you for calling, {customer_name}. I can see that the settlement for claim {claim_id} was processed on {payment_date} in the amount of ₹{settlement_amount}. A settlement letter explaining the breakdown will be sent to your registered address or email shortly.

If the amount is different from what you expected, I can walk you through the settlement details. Would you like me to do that now, or would you prefer to review the written letter first?"

## Section 3 Do and Do Not

DO: confirm the settlement amount and payment date accurately from the system; explain any unapproved amounts clearly and with the applicable policy clause reference; offer to send a written breakdown; always provide the grievance route when informing the customer of amounts not approved; note the call in the system.

DO NOT: imply that amounts not approved in this claim may be revisited or paid later; make promises about the outcome of a potential grievance; quote the settlement amount from memory without checking the system first; mark a claim as closed in the system before the payment has actually been processed.
