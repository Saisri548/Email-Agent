import os
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain_openai import ChatOpenAI
from app.state import EmailState
class ClassificationResult(BaseModel):
    intent:Literal[ "invoice_submission",
        "payment_query",
        "dispute",
        "spam",
        "ambiguous"]
    confidence:float=Field(
        ge=0.0,
        le=1.0
    )
    reasoning:str
load_dotenv()
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
classifier_llm=llm.with_structured_output(ClassificationResult)    
def classify_email(state:EmailState)->EmailState:
    email=state.email
    prompt=f"""
You are an enterprise email classification agent.

Classify the email into exactly ONE of these categories:

1. invoice_submission
The sender is submitting an invoice or asking for an
invoice to be logged/processed.

2. payment_query
The sender is asking about payment status, payment date,
remittance, or an unpaid invoice.

3. dispute
The sender is challenging an invoice, amount, tax,
duplicate charge, unauthorized charge, or billing issue.

4. spam
The email is fraudulent, phishing, suspicious, unsolicited,
or attempting to obtain money or credentials.

5. ambiguous
There is not enough information to safely determine the
intent, or the email could reasonably belong to multiple
categories.

Rules:

- Consider sender, subject, and body.
- Do not invent missing information.
- Do not classify based only on the subject.
- Typos and informal language are allowed.
- Use ambiguous when the evidence is genuinely insufficient.
- Give a confidence score between 0 and 1.
- Keep reasoning short and factual.

EMAIL

Sender:
{email.get("sender", "")}

Subject:
{email.get("subject", "")}

Body:
{email.get("body", "")}
"""
    result=classifier_llm.invoke(prompt)
    state.intent=result.intent
    state.confidence = result.confidence
    state.reasoning = result.reasoning
    if result.confidence<=0.75 or result.intent == "ambiguous":
         state.requires_human_review = True
    state.audit_log.append(
          f"Classified as {result.intent} "
        f"with confidence {result.confidence:.2f}. "
        f"Reason: {result.reasoning}"
    ) 
    return state
