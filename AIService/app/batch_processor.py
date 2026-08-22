import json
from app.graph import email_agent
from app.state import EmailState


def load_emails():
    """
    Load emails from the JSON dataset.
    """

    with open("data/emails.json", "r", encoding="utf-8") as file:
        return json.load(file)


def process_email(email):
    """
    Run one email through the complete LangGraph workflow.
    """

    initial_state = EmailState(
        email=email
    )

    final_state = email_agent.invoke(initial_state)

    return final_state


def process_batch():
    """
    Process all emails in the dataset.
    """

    emails = load_emails()

    results = []

    print("\n" + "=" * 70)
    print("AUTONOMOUS EMAIL AGENT — BATCH PROCESSING")
    print("=" * 70)

    print(f"\nTotal emails: {len(emails)}")

    for index, email in enumerate(emails, start=1):

        print("\n" + "-" * 70)
        print(f"Processing email {index}/{len(emails)}")
        print("-" * 70)

        print("ID:", email.get("id"))
        print("Subject:", email.get("subject"))

        try:

            result = process_email(email)

            results.append(result)

            print("Intent:", result.get("intent"))
            print("Confidence:", result.get("confidence"))
            print("Action:", result.get("action"))
            print("Result:", result.get("action_result"))

            if result.get("requires_human_review"):
                print("⚠ HUMAN REVIEW REQUIRED")

        except Exception as error:

            print("❌ Error processing email:", error)

    return results


def print_summary(results):
    """
    Print batch processing statistics.
    """

    print("\n\n" + "=" * 70)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 70)

    total = len(results)

    intent_counts = {}

    human_review_count = 0

    action_counts = {}

    for result in results:

        intent = result.get("intent", "unknown")

        intent_counts[intent] = (
            intent_counts.get(intent, 0) + 1
        )

        action = result.get("action", "unknown")

        action_counts[action] = (
            action_counts.get(action, 0) + 1
        )

        if result.get("requires_human_review"):
            human_review_count += 1

    print("\nTotal Processed:", total)

    print("\nIntent Distribution:")

    for intent, count in intent_counts.items():

        print(
            f"  {intent:<25} {count}"
        )

    print("\nActions:")

    for action, count in action_counts.items():

        print(
            f"  {action:<25} {count}"
        )

    print(
        "\nHuman Review Required:",
        human_review_count
    )


if __name__ == "__main__":

    results = process_batch()

    print_summary(results)