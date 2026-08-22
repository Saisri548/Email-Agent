import sqlite3
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
DB_PATH=BASE_DIR/"database.db"
def get_connection():
    """
    Create and return a SQLite database connection.
    """
    connection=sqlite3.connect(DB_PATH)
    connection.row_factory=sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection 
def intialize_database():
    """
    Create all required tables if they don't already exist.
    """
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            email_id TEXT PRIMARY KEY,
            sender TEXT,
            subject TEXT,
            body TEXT,
            received_at TEXT
        )
    """)

    # -----------------------------------------
    # Invoices
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id TEXT PRIMARY KEY,
            email_id TEXT,
            vendor TEXT,
            amount REAL,
            currency TEXT,
            status TEXT,
            created_at TEXT,
             FOREIGN KEY (email_id)
        REFERENCES emails(email_id)
        )
    """)

    # -----------------------------------------
    # Payment / Follow-up Tasks
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            email_id TEXT,
            invoice_id TEXT,
            task_type TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT,
             FOREIGN KEY (email_id)
        REFERENCES emails(email_id),

    FOREIGN KEY (invoice_id)
        REFERENCES invoices(invoice_id)
        )
    """)

    # -----------------------------------------
    # Disputes
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disputes (
            dispute_id TEXT PRIMARY KEY,
            email_id TEXT,
            invoice_id TEXT,
            issue TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY (email_id)
        REFERENCES emails(email_id),

    FOREIGN KEY (invoice_id)
        REFERENCES invoices(invoice_id)
        )
    """)

    # -----------------------------------------
    # Audit Trail
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT,
            intent TEXT,
            confidence REAL,
            action TEXT,
            reason TEXT,
            result TEXT,
            timestamp TEXT,
            FOREIGN KEY (email_id)
        REFERENCES emails(email_id)
        )
    """)
    connection.commit()
    connection.close()
if __name__ == "__main__":
    intialize_database()
    print(f"Database initialized successfully: {DB_PATH}")    

