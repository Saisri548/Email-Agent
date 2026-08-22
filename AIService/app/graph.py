from langgraph.graph import StateGraph, START, END

from app.state import EmailState
from app.classifier import classify_email
from app.extractor import extract_email_data
from app.actions import execute_action
from app.audit import save_audit_log


# --------------------------------------------------
# Build Graph
# --------------------------------------------------

def build_graph():

    graph = StateGraph(EmailState)

    # Add nodes
    graph.add_node("classify", classify_email)
    graph.add_node("extract", extract_email_data)
    graph.add_node("action", execute_action)
    graph.add_node("audit", save_audit_log)

    # Define flow
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "extract")
    graph.add_edge("extract", "action")
    graph.add_edge("action", "audit")
    graph.add_edge("audit", END)

    return graph.compile()


# --------------------------------------------------
# Compiled application
# --------------------------------------------------

email_agent = build_graph()