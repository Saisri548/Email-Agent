import json

from app.state import EmailState
from app.extractor import extract_email_data


# Load emails
with open("data/emails.json", "r", encoding="utf-8") as file:
    emails = json.load(file)


# Select one email
email = emails[10]


# Create initial state
state = EmailState(
    email=email
)


print("\n" + "=" * 60)
print("INPUT EMAIL")
print("=" * 60)

print("ID:", email.get("id"))
print("Sender:", email.get("sender"))
print("Subject:", email.get("subject"))
print("Body:", email.get("body"))


# Run extractor
state = extract_email_data(state)


print("\n" + "=" * 60)
print("EXTRACTED DATA")
print("=" * 60)

print("Invoice ID:", state.invoice_id)
print("Vendor:", state.vendor)
print("Amount:", state.amount)
print("Currency:", state.currency)
print("Urgency:", state.urgency)
print("Key Issue:", state.key_issue)


print("\n" + "=" * 60)
print("AUDIT TRAIL")
print("=" * 60)

for entry in state.audit_log:
    print("-", entry)