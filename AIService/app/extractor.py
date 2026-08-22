import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel,Field

from langchain_openai import ChatOpenAI
from app.state import EmailState
load_dotenv()
class ExtractedEmailData(BaseModel):
    """
    Business information extracted from an email.
    """
    invoice_id: Optional[str] = Field(
        default=None,
        description="Invoice ID such as INV-4418."
    )
    vendor: Optional[str] = Field(
        default=None,
        description="Company or vendor mentioned in the email."
    )
    amount: Optional[float] = Field(
        default=None,
        description="Invoice or payment amount."
    )
    currency: Optional[str] = Field(
        default=None,
        description="Currency such as INR, USD, EUR."
    )

    urgency: str = Field(
        description="Urgency: low, medium, or high."
    )

    key_issue: Optional[str] = Field(
        default=None,
    )
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
extractor_llm=llm.with_structured_output(ExtractedEmailData)
def extract_email_data(state: EmailState) -> EmailState:
    email=state.email
    prompt = f"""
You are an enterprise email information extraction agent.

Extract useful business information from the email.

Rules:

- Extract only information explicitly present in the email.
- Never invent an invoice ID, vendor, amount, or currency.
- If information is missing, return null.
- Determine urgency from the language and situation.
- Urgency must be exactly one of:
  low, medium, high.
- Keep key_issue short.

EMAIL

Sender:
{email.get("sender", "")}

Subject:
{email.get("subject", "")}

Body:
{email.get("body", "")}
"""
    result = extractor_llm.invoke(prompt)
    
    state.invoice_id=result.invoice_id
    state.vendor=result.vendor
    state.amount=result.amount
    state.currency=result.currency
    state.urgency=result.urgency
    state.key_issue=result.key_issue
    state.audit_log.append(
        f"Extracted business data: "
        f"invoice={result.invoice_id}, "
        f"vendor={result.vendor}, "
        f"amount={result.amount}, "
        f"urgency={result.urgency}."
    )
    return state  


      