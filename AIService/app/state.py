from typing import Dict,Optional,Any,List
from pydantic import BaseModel,Field
class EmailState(BaseModel):
    email:Dict[str,Any]
    intent:Optional[str]=None
    confidence: float = 0.0
    reasoning:Optional[str]=None
    invoice_id: Optional[str] = None
    vendor: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    urgency: Optional[str] = None
    key_issue: Optional[str] = None
    action:Optional[str]=None
    action_result:Optional[str]=None
    audit_log: List[str] = Field(default_factory=list)
    requires_human_review:bool=False