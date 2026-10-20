from pydantic import BaseModel, Field


class ConversationState(BaseModel):
    customer_id: str
    current_order_id: str | None = None
    current_issue: str | None = None
    last_intent: str | None = None
    pending_cancellation_order_id: str | None = None
    messages: list[dict[str, str]] = Field(default_factory=list)
