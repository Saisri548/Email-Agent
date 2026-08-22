
from datetime import datetime
from uuid import uuid4

from app.database import get_connection
from app.state import EmailState


# ============================================================
# Helpers
# ============================================================

def get_email_id(state: EmailState) -> str:
    """
    Get the email ID from the original email.
    """
    email_id = state.email.get("id")

    if not email_id:
        raise ValueError("Email ID is required.")

    return email_id


def get_priority(state: EmailState) -> str:
    """
    Convert urgency into task/dispute priority.
    """

    if state.urgency == "high":
        return "HIGH"

    if state.urgency == "medium":
        return "MEDIUM"

    return "LOW"


def ensure_email_exists(state: EmailState) -> None:
    """
    Make sure the email exists before creating any
    invoice, task, dispute, or audit record.

    This prevents foreign-key constraint failures.
    """

    email_id = get_email_id(state)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO emails
            (
                email_id,
                sender,
                subject,
                body,
                received_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                email_id,
                state.email.get("sender"),
                state.email.get("subject"),
                state.email.get("body"),
                datetime.now().isoformat()
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def invoice_exists(invoice_id: str) -> bool:
    """
    Check whether an invoice exists in the database.
    """

    if not invoice_id:
        return False

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM invoices
            WHERE invoice_id = ?
            LIMIT 1
            """,
            (invoice_id,)
        )

        return cursor.fetchone() is not None

    finally:
        connection.close()


# ============================================================
# Invoice Action
# ============================================================

def log_invoice(state: EmailState) -> EmailState:
    """
    Action for invoice_submission emails.

    Stores the email first and then stores the invoice.
    """

    email_id = get_email_id(state)

    # Make sure parent email exists
    ensure_email_exists(state)

    invoice_id = (
        state.invoice_id
        or f"INV-{uuid4().hex[:6].upper()}"
    )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO invoices
            (
                invoice_id,
                email_id,
                vendor,
                amount,
                currency,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                invoice_id,
                email_id,
                state.vendor,
                state.amount,
                state.currency,
                "RECEIVED",
                datetime.now().isoformat()
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    state.action = "log_invoice"

    state.action_result = (
        f"Invoice {invoice_id} logged successfully."
    )

    state.audit_log.append(
        f"Action: log_invoice. "
        f"Result: Invoice {invoice_id} logged successfully."
    )

    return state


# ============================================================
# Payment Follow-up Action
# ============================================================

def create_payment_followup(state: EmailState) -> EmailState:
    """
    Action for payment_query emails.

    Creates a payment follow-up task.

    If an invoice ID is provided, it must already exist
    in the invoices table before the task is created.
    """

    email_id = get_email_id(state)

    # Ensure parent email exists
    ensure_email_exists(state)

    task_id = f"TASK-{uuid4().hex[:6].upper()}"

    priority = get_priority(state)

    invoice_id = state.invoice_id

    # --------------------------------------------------------
    # Validate invoice foreign key
    # --------------------------------------------------------

    if invoice_id and not invoice_exists(invoice_id):
        # Do not create an invalid foreign-key reference.
        invoice_id = None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks
            (
                task_id,
                email_id,
                invoice_id,
                task_type,
                priority,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                email_id,
                invoice_id,
                "PAYMENT_FOLLOWUP",
                priority,
                "OPEN",
                datetime.now().isoformat()
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    state.action = "create_payment_followup"

    state.action_result = (
        f"Payment follow-up {task_id} "
        f"created with {priority} priority."
    )

    state.audit_log.append(
        f"Action: create_payment_followup. "
        f"Result: {task_id} created with {priority} priority."
    )

    return state


# ============================================================
# Dispute Action
# ============================================================

def create_dispute_ticket(state: EmailState) -> EmailState:
    """
    Action for dispute emails.

    Creates a dispute ticket.

    If an invoice ID is provided, it must exist in the
    invoices table before the dispute references it.
    """

    email_id = get_email_id(state)

    # Ensure parent email exists
    ensure_email_exists(state)

    dispute_id = f"DIS-{uuid4().hex[:6].upper()}"

    priority = get_priority(state)

    invoice_id = state.invoice_id

    # --------------------------------------------------------
    # Validate invoice foreign key
    # --------------------------------------------------------

    if invoice_id and not invoice_exists(invoice_id):
        invoice_id = None

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO disputes
            (
                dispute_id,
                email_id,
                invoice_id,
                issue,
                priority,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dispute_id,
                email_id,
                invoice_id,
                state.key_issue,
                priority,
                "OPEN",
                datetime.now().isoformat()
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    state.action = "create_dispute_ticket"

    state.action_result = (
        f"Dispute ticket {dispute_id} "
        f"created with {priority} priority."
    )

    state.audit_log.append(
        f"Action: create_dispute_ticket. "
        f"Result: {dispute_id} created with {priority} priority."
    )

    return state


# ============================================================
# Spam Action
# ============================================================

def mark_as_spam(state: EmailState) -> EmailState:
    """
    Action for spam emails.

    Records the email in the database.
    """

    email_id = get_email_id(state)

    # Ensure email exists
    ensure_email_exists(state)

    state.action = "mark_as_spam"

    state.action_result = "Email marked as spam."

    state.audit_log.append(
        "Action: mark_as_spam. "
        "Result: Email marked as spam."
    )

    return state


# ============================================================
# Human Review
# ============================================================

def request_human_review(state: EmailState) -> EmailState:
    """
    Action for ambiguous or low-confidence emails.
    """

    # Make sure email exists before audit
    ensure_email_exists(state)

    state.requires_human_review = True

    state.action = "request_human_review"

    state.action_result = (
        "Email sent to human review because "
        "the classification is ambiguous or "
        "low confidence."
    )

    state.audit_log.append(
        "Action: request_human_review. "
        "Reason: Classification requires human verification."
    )

    return state


# ============================================================
# Main Action Router
# ============================================================

def execute_action(state: EmailState) -> EmailState:
    """
    Select the correct business action based on intent.
    """

    # --------------------------------------------------------
    # Human review takes priority
    # --------------------------------------------------------

    if state.requires_human_review:
        return request_human_review(state)

    # --------------------------------------------------------
    # Invoice
    # --------------------------------------------------------

    if state.intent == "invoice_submission":
        return log_invoice(state)

    # --------------------------------------------------------
    # Payment query
    # --------------------------------------------------------

    if state.intent == "payment_query":
        return create_payment_followup(state)

    # --------------------------------------------------------
    # Dispute
    # --------------------------------------------------------

    if state.intent == "dispute":
        return create_dispute_ticket(state)

    # --------------------------------------------------------
    # Spam
    # --------------------------------------------------------

    if state.intent == "spam":
        return mark_as_spam(state)

    # --------------------------------------------------------
    # Ambiguous
    # --------------------------------------------------------

    if state.intent == "ambiguous":
        return request_human_review(state)

    # --------------------------------------------------------
    # Unsupported intent
    # --------------------------------------------------------

    ensure_email_exists(state)

    state.action = "no_action"

    state.action_result = "No valid action found."

    state.audit_log.append(
        "Action: no_action. "
        "Reason: Unsupported intent."
    )

    return state
