# 🤖 Autonomous Email Agent

An AI-powered email automation system that analyzes incoming emails, determines their intent, selects an appropriate action, executes the action, and maintains a complete audit trail of the agent's decisions.

## 🚀 Overview

The Autonomous Email Agent is designed to automate common email operations using an AI-driven workflow.

Instead of manually processing every email, the system:

1. Receives an email
2. Analyzes the email content
3. Classifies the email intent
4. Calculates a confidence score
5. Determines the appropriate action
6. Executes the action
7. Records the result
8. Stores an audit trail

The application provides a React dashboard for monitoring emails, actions, disputes, invoices, tasks, and audit logs.

---

## 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │   React Client  │
                    │    Dashboard    │
                    └────────┬────────┘
                             │
                             │ REST API
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │     Backend     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    LangGraph    │
                    │  Agent Workflow │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌───────────┐   ┌──────────┐
        │ Intent   │   │  Action   │   │  Audit   │
        │Analysis  │   │ Execution │   │ Logging  │
        └──────────┘   └───────────┘   └──────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ SQLite Database  │
                    └─────────────────┘