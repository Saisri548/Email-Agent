from app.state import EmailState
from app.actions import execute_action


def print_result(title, state):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("Intent:", state.intent)
    print("Action:", state.action)
    print("Result:", state.action_result)
    print("Human Review:", state.requires_human_review)

    print("\nAudit:")
    for entry in state.audit_log:
        print("-", entry)


# --------------------------------------------------
# 1. Invoice Submission
# --------------------------------------------------

invoice_state = EmailState(
    email={
        "id": "test_invoice_001",
        "sender": "billing@abc-supplies.com",
        "subject": "Invoice INV-9001",
        "body": "Please process invoice INV-9001 for ₹50,000."
    },
    intent="invoice_submission",
    confidence=0.96,
    reasoning="Sender is submitting an invoice.",
    invoice_id="INV-9001",
    vendor="abc-supplies.com",
    amount=50000,
    currency="INR",
    urgency="medium",
    key_issue="Invoice submission"
)

invoice_state = execute_action(invoice_state)

print_result(
    "TEST 1 — INVOICE SUBMISSION",
    invoice_state
)


# --------------------------------------------------
# 2. Payment Query
# --------------------------------------------------

payment_state = EmailState(
    email={
        "id": "test_payment_001",
        "sender": "payments@acme-retail.com",
        "subject": "Payment overdue INV-4418",
        "body": "We have not received payment for INV-4418."
    },
    intent="payment_query",
    confidence=0.95,
    reasoning="Sender is asking about an overdue payment.",
    invoice_id="INV-4418",
    vendor="acme-retail.com",
    amount=None,
    currency=None,
    urgency="high",
    key_issue="Payment overdue"
)

payment_state = execute_action(payment_state)

print_result(
    "TEST 2 — PAYMENT QUERY",
    payment_state
)


# --------------------------------------------------
# 3. Dispute
# --------------------------------------------------

dispute_state = EmailState(
    email={
        "id": "test_dispute_001",
        "sender": "finance@xyz.com",
        "subject": "Incorrect invoice amount",
        "body": "The invoice amount is incorrect."
    },
    intent="dispute",
    confidence=0.94,
    reasoning="Sender is challenging the invoice amount.",
    invoice_id="INV-7777",
    vendor="xyz.com",
    amount=85000,
    currency="INR",
    urgency="high",
    key_issue="Incorrect invoice amount"
)

dispute_state = execute_action(dispute_state)

print_result(
    "TEST 3 — DISPUTE",
    dispute_state
)


# --------------------------------------------------
# 4. Spam
# --------------------------------------------------

spam_state = EmailState(
    email={
        "id": "test_spam_001",
        "sender": "unknown@example.com",
        "subject": "You won ₹5,00,000!",
        "body": "Send your bank details to claim your prize."
    },
    intent="spam",
    confidence=0.99,
    reasoning="Email appears to be a financial scam.",
    urgency="high",
    key_issue="Possible financial scam"
)

spam_state = execute_action(spam_state)

print_result(
    "TEST 4 — SPAM",
    spam_state
)


# --------------------------------------------------
# 5. Ambiguous
# --------------------------------------------------

ambiguous_state = EmailState(
    email={
        "id": "test_ambiguous_001",
        "sender": "customer@example.com",
        "subject": "Invoice issue",
        "body": "There is an issue with our invoice. Please check."
    },
    intent="ambiguous",
    confidence=0.61,
    reasoning="The email does not provide enough information.",
    urgency="medium",
    key_issue="Unclear invoice issue"
)

ambiguous_state = execute_action(ambiguous_state)

print_result(
    "TEST 5 — AMBIGUOUS",
    ambiguous_state
)