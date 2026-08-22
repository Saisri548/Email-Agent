import json
from pathlib import Path

from database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
EMAILS_FILE = BASE_DIR / "data" / "emails.json"


def import_emails():
    with open(EMAILS_FILE, "r", encoding="utf-8") as file:
        emails = json.load(file)

    connection = get_connection()
    cursor = connection.cursor()

    inserted = 0
    skipped = 0

    for email in emails:

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
                email["id"],
                email["sender"],
                email["subject"],
                email["body"],
                None
            )
        )

        if cursor.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    connection.commit()
    connection.close()

    print(f"Total emails in JSON : {len(emails)}")
    print(f"Inserted             : {inserted}")
    print(f"Already existed      : {skipped}")


if __name__ == "__main__":
    import_emails()