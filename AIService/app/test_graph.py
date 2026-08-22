import json

from app.graph import email_agent
from app.state import EmailState


# -------------------------------------------------
# Load emails
# -------------------------------------------------

with open("data/emails.json", "r", encoding="utf-8") as file:
    emails = json.load(file)


# -------------------------------------------------
# Process emails sequentially
# -------------------------------------------------

print("\n" + "=" * 70)
print("AUTONOMOUS EMAIL AGENT")
print("=" * 70)

print(f"\nTotal emails to process: {len(emails)}")


for index, email in enumerate(emails):

    print("\n" + "=" * 70)
    print(f"PROCESSING EMAIL {index + 1}/{len(emails)}")
    print("=" * 70)

    print("\nINPUT")
    print("-" * 70)

    print("ID:", email.get("id"))
    print("Sender:", email.get("sender"))
    print("Subject:", email.get("subject"))
    print("Body:", email.get("body"))

    # -------------------------------------------------
    # Initial state
    # -------------------------------------------------

    initial_state = EmailState(
        email=email
    )

    try:

        # -------------------------------------------------
        # Run LangGraph workflow
        # -------------------------------------------------

        final_state = email_agent.invoke(initial_state)

        print("\nCLASSIFICATION")
        print("-" * 70)

        print("Intent:", final_state["intent"])
        print("Confidence:", final_state["confidence"])
        print("Reasoning:", final_state["reasoning"])

        print("\nEXTRACTED INFORMATION")
        print("-" * 70)

        print("Invoice ID:", final_state["invoice_id"])
        print("Vendor:", final_state["vendor"])
        print("Amount:", final_state["amount"])
        print("Currency:", final_state["currency"])
        print("Urgency:", final_state["urgency"])
        print("Key Issue:", final_state["key_issue"])

        print("\nACTION")
        print("-" * 70)

        print("Action:", final_state["action"])
        print("Result:", final_state["action_result"])
        print(
            "Human Review:",
            final_state["requires_human_review"]
        )

        print("\nAUDIT TRAIL")
        print("-" * 70)

        for entry in final_state["audit_log"]:
            print("-", entry)

    except Exception as error:

        print("\n❌ ERROR")
        print("-" * 70)

        print(type(error).__name__, ":", error)

        # Continue with the next email
        continue


print("\n" + "=" * 70)
print("PROCESSING COMPLETE")
print("=" * 70)