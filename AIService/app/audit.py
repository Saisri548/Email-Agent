from datetime import datetime

from app.database import get_connection
from app.state import EmailState


def save_audit_log(state: EmailState) -> EmailState:
    """
    Persist one complete audit record for the email-agent execution.
    """

    email_id = state.email.get("id")

    audit_reason = "\n".join(state.audit_log)

    connection = get_connection()

    try:
        cursor = connection.cursor()

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