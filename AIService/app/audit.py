
from datetime import datetime

from app.database import get_connection
from app.state import EmailState


def save_audit_log(state: EmailState) -> EmailState:
    """
    Persist one complete audit record for the email-agent execution.

    Ensures the parent email exists before inserting the audit record.
    This prevents FOREIGN KEY constraint failures.
    """

    email_id = state.email.get("id")

    if not email_id:
        raise ValueError("Email ID is required to create an audit log.")

    audit_reason = "\n".join(state.audit_log)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # -------------------------------------------------
        # 1. Make sure the email exists
        # -------------------------------------------------
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

        # -------------------------------------------------
        # 2. Insert audit log
        # -------------------------------------------------
        cursor.execute(
            """
            INSERT INTO audit_logs
            (
                email_id,
                intent,
                confidence,
                action,
                reason,
                result,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                email_id,
                state.intent,
                state.confidence,
                state.action,
                audit_reason,
                state.action_result,
                datetime.now().isoformat()
            )
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return state
