# Autonomous Email Agent — Architecture Diagrams

## 1. High-Level System Architecture

```mermaid
flowchart TD

    USER[User / Customer]

    FRONTEND[Frontend Application]

    API[FastAPI Backend]

    AGENT[Autonomous Email Agent]

    EMAIL[Email Processing]

    DISPUTE[Dispute Detection]

    DB[(SQLite Database)]

    AUDIT[(Audit Records)]

    LLM[LLM / AI Model]

    USER --> FRONTEND
    FRONTEND --> API
    API --> AGENT

    AGENT --> EMAIL
    AGENT --> DISPUTE
    AGENT --> LLM

    EMAIL --> DB
    DISPUTE --> DB

    AGENT --> AUDIT
    AUDIT --> DB
```

---

## 2. Email Processing Flow

```mermaid
sequenceDiagram

    participant U as User
    participant F as Frontend
    participant A as FastAPI
    participant AG as Email Agent
    participant DB as Database
    participant AU as Audit

    U->>F: Submit Email
    F->>A: POST Email Request
    A->>AG: Process Email

    AG->>AG: Analyze Email
    AG->>AG: Determine Intent

    alt Dispute Detected
        AG->>DB: Store Dispute
    else Normal Email
        AG->>DB: Store Email
    end

    AG->>AU: Record Action
    AU->>DB: Store Audit Record

    AG-->>A: Processing Result
    A-->>F: API Response
    F-->>U: Display Result
```

---

## 3. Agent Workflow

```mermaid
flowchart TD

    START([Incoming Email])

    RECEIVE[Receive Email]

    ANALYZE[Analyze Email]

    INTENT{Determine Intent}

    NORMAL[Normal Email]

    DISPUTE[Dispute Email]

    ACTION[Determine Required Action]

    RESPONSE[Generate Response]

    SAVE[Save Information]

    AUDIT[Create Audit Record]

    END([Completed])

    START --> RECEIVE
    RECEIVE --> ANALYZE
    ANALYZE --> INTENT

    INTENT -->|Normal| NORMAL
    INTENT -->|Dispute| DISPUTE

    NORMAL --> ACTION
    DISPUTE --> ACTION

    ACTION --> RESPONSE
    RESPONSE --> SAVE
    SAVE --> AUDIT
    AUDIT --> END
```

---

## 4. Database Architecture

```mermaid
erDiagram

    EMAILS {
        integer id PK
        string sender
        string subject
        text body
        datetime created_at
    }

    DISPUTES {
        integer id PK
        integer email_id FK
        string reason
        string description
        string status
        datetime created_at
    }

    AUDIT {
        integer id PK
        integer email_id FK
        string action
        string status
        datetime created_at
    }

    EMAILS ||--o{ DISPUTES : contains
    EMAILS ||--o{ AUDIT : generates
```

---

## 5. API Architecture

```mermaid
flowchart LR

    CLIENT[Frontend / API Client]

    ROOT[GET /]

    HEALTH[GET /health]

    EMAILS[Email APIs]

    DISPUTES[Dispute APIs]

    AUDIT[Audit APIs]

    BACKEND[FastAPI Application]

    DB[(SQLite)]

    CLIENT --> BACKEND

    BACKEND --> ROOT
    BACKEND --> HEALTH
    BACKEND --> EMAILS
    BACKEND --> DISPUTES
    BACKEND --> AUDIT

    EMAILS --> DB
    DISPUTES --> DB
    AUDIT --> DB
```

---

## 6. Deployment Architecture

```mermaid
flowchart TD

    USER[User]

    BROWSER[Browser]

    FRONTEND[Frontend]

    RENDER[Render]

    FASTAPI[FastAPI Backend]

    DATABASE[(SQLite Database)]

    AI[AI / LLM Service]

    BROWSER --> FRONTEND
    FRONTEND --> RENDER

    RENDER --> FASTAPI

    FASTAPI --> AI
    FASTAPI --> DATABASE
```

---

## 7. Complete End-to-End Architecture

```mermaid
flowchart TD

    USER[Customer]

    UI[Frontend UI]

    API[FastAPI API]

    AGENT[Autonomous Email Agent]

    ANALYSIS[Email Analysis]

    INTENT[Intent Detection]

    DISPUTE[Dispute Detection]

    DECISION[Action Decision]

    LLM[LLM]

    EMAILDB[(Emails)]

    DISPUTEDB[(Disputes)]

    AUDITDB[(Audit)]

    RESPONSE[Generated Response]

    USER --> UI
    UI --> API
    API --> AGENT

    AGENT --> ANALYSIS
    ANALYSIS --> INTENT

    INTENT --> DISPUTE
    INTENT --> DECISION

    DISPUTE -->|Dispute| DISPUTEDB
    DISPUTE -->|No Dispute| DECISION

    DECISION --> LLM
    LLM --> RESPONSE

    RESPONSE --> EMAILDB
    AGENT --> AUDITDB

    API --> UI
    UI --> USER
```