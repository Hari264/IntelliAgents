---
doc_id: SCR-DOC-01
title: "Script: Missing Documents"
product: HEALTH_GOLD
version: na
effective_from: 2024-01-01
effective_to: 9999-12-31
doc_type: script
audience: [service, adjuster]
sensitivity: General
---

## Section 1 When to Use

Use this script when a claim is on hold because mandatory or procedure-specific documents have not been received, logged under rejection code CL-104 (Required documents not submitted).

Before making the call, open the deficiency notice in the claims management system and note the exact list of outstanding documents and the submission deadline given to the customer. Retrieve the claim reference {claim_id}.

This script also applies when a customer calls in to enquire about a claim that is pending on CL-104 status.

## Section 2 Customer Script

**Outbound call — proactive follow-up:**

"Good [morning / afternoon / evening]. May I please speak with {customer_name}?

Thank you. This is [your name] calling from Aarogya Shield General Insurance Ltd. regarding your health insurance claim number {claim_id}. Your claim is currently with us under code {rejection_code}.

I am calling because we have reviewed the documents you submitted and we need some additional items before we can complete our assessment. I will read the list for you now — please let me know if you have any questions about any of these items.

[Read each item from the deficiency notice clearly, one at a time.]

You may send these documents by post to our claims address, by email to [email address] quoting your claim number, or by uploading them through our online customer portal. The details are also on the deficiency notice we sent you.

To avoid any further delay, we would appreciate receiving these by [state the deadline from the deficiency notice].

Once we receive all the outstanding documents, we will complete our assessment within the timelines required under the NIR guidelines and will write to you with our decision.

If you have already sent these documents in the last few days, please let me know and I will check our records.

Is there anything else I can help you with today?"

**Inbound call — customer enquiring about claim on CL-104 hold:**

"Thank you for calling Aarogya Shield General Insurance Ltd. I can see your claim {claim_id} is currently on hold because some documents are still outstanding under code {rejection_code}. Let me tell you exactly what we are waiting for.

[Read from the deficiency notice in the system.]

Once we receive these, your claim will move to assessment. You can send them by [describe channels]. Do you have any questions about what is needed or how to send them?"

## Section 3 Do and Do Not

DO: always check the deficiency notice in the claims management system before the call so you know exactly which documents are outstanding; read the list clearly and slowly; offer to send the deficiency notice again in writing; confirm all available submission channels; note in the system that the call was made and what was discussed.

DO NOT: tell the customer the claim will be approved once the documents are received — you can only say it will be assessed; accept verbal confirmation that documents have already been sent without checking the system first; tell the customer that a specific document is optional; extend the submission deadline over the phone without supervisor approval.
