import json
from app.state import EmailState
from app.classifier import classify_email
with open("data/emails.json","r",encoding="utf-8") as file:
    emails=json.load(file)
email=emails[10]    
state=EmailState(email=email)
print("\n" + "=" * 60)
print("INPUT EMAIL")
print("=" * 60)
print("ID:", email.get("id"))
print("Sender:", email.get("sender"))
print("Subject:", email.get("subject"))
print("Body:", email.get("body"))
state = classify_email(state)
print("\n" + "=" * 60)
print("CLASSIFICATION RESULT")
print("=" * 60)

print("Intent:", state.intent)
print("Confidence:", state.confidence)
print("Reasoning:", state.reasoning)
print("Human Review Required:", state.requires_human_review)


print("\n" + "=" * 60)
print("AUDIT TRAIL")
print("=" * 60)
for entry in state.audit_log:
    print("-", entry)