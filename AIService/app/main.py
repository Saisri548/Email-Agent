from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import get_connection
from app.graph import email_agent
from app.state import EmailState


app = FastAPI(
    title="Autonomous Email Agent API",
    description="AI-powered email classification, extraction, action and audit system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Health Check
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Autonomous Email Agent API is running",
        "status": "healthy"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ============================================================
# Request Models
# ============================================================

class EmailRequest(BaseModel):
    id: str
    sender: str
    subject: str
    body: str


# ============================================================
# Process Email
# ============================================================

@app.post("/api/emails/process")
def process_email(email: EmailRequest):

    try:
        # Convert request into EmailState
        initial_state = EmailState(
            email=email.model_dump()
        )

        # Run LangGraph agent
        final_state = email_agent.invoke(initial_state)

        return {
            "success": True,

            "email": {
                "id": email.id,
                "sender": email.sender,
                "subject": email.subject
            },

            "classification": {
                "intent": final_state["intent"],
                "confidence": final_state["confidence"],
                "reasoning": final_state["reasoning"]
            },

            "extracted_data": {
                "invoice_id": final_state["invoice_id"],
                "vendor": final_state["vendor"],
                "amount": final_state["amount"],
                "currency": final_state["currency"],
                "urgency": final_state["urgency"],
                "key_issue": final_state["key_issue"]
            },

            "action": {
                "name": final_state["action"],
                "result": final_state["action_result"],
                "requires_human_review": (
                    final_state["requires_human_review"]
                )
            },

            "audit_log": final_state["audit_log"]
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# Database Helper
# ============================================================

def fetch_all(query: str, parameters=()):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(query, parameters)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# ============================================================
# Get Emails
# ============================================================

@app.get("/api/emails")
def get_emails():

    rows = fetch_all(
        """
        SELECT *
        FROM emails
        ORDER BY received_at DESC
        """
    )

    return {
        "success": True,
        "count": len(rows),
        "data": rows
    }


# ============================================================
# Get Invoices
# ============================================================

@app.get("/api/invoices")
def get_invoices():

    rows = fetch_all(
        """
        SELECT *
        FROM invoices
        ORDER BY created_at DESC
        """
    )

    return {
        "success": True,
        "count": len(rows),
        "data": rows
    }


# ============================================================
# Get Tasks
# ============================================================

@app.get("/api/tasks")
def get_tasks():

    rows = fetch_all(
        """
        SELECT *
        FROM tasks
        ORDER BY created_at DESC
        """
    )

    return {
        "success": True,
        "count": len(rows),
        "data": rows
    }


# ============================================================
# Get Disputes
# ============================================================

@app.get("/api/disputes")
def get_disputes():

    rows = fetch_all(
        """
        SELECT *
        FROM disputes
        ORDER BY created_at DESC
        """
    )

    return {
        "success": True,
        "count": len(rows),
        "data": rows
    }


# ============================================================
# Get Audit Logs
# ============================================================

@app.get("/api/audit")
def get_audit_logs():
    rows = fetch_all(
        """
        SELECT *
        FROM audit_logs
        ORDER BY timestamp DESC
        """
    )

    return {
        "success": True,
        "count": len(rows),
        "data": rows
    }


# ============================================================
# Dashboard Statistics
# ============================================================

@app.get("/api/dashboard")
def get_dashboard():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # Emails
        cursor.execute(
            "SELECT COUNT(*) AS count FROM emails"
        )
        emails = cursor.fetchone()["count"]

        # Invoices
        cursor.execute(
            "SELECT COUNT(*) AS count FROM invoices"
        )
        invoices = cursor.fetchone()["count"]

        # Tasks
        cursor.execute(
            "SELECT COUNT(*) AS count FROM tasks"
        )
        tasks = cursor.fetchone()["count"]

        # Disputes
        cursor.execute(
            "SELECT COUNT(*) AS count FROM disputes"
        )
        disputes = cursor.fetchone()["count"]

        # Audit logs
        cursor.execute(
            "SELECT COUNT(*) AS count FROM audit_logs"
        )
        audit_logs = cursor.fetchone()["count"]

        return {
            "success": True,
            "statistics": {
                "emails": emails,
                "invoices": invoices,
                "tasks": tasks,
                "disputes": disputes,
                "audit_logs": audit_logs
            }
        }

    finally:
        connection.close()