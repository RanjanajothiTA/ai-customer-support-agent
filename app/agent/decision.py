from enum import Enum
from pydantic import BaseModel
from typing import Any


class Intent(str, Enum):
    RETURN_POLICY = "return_policy"
    REFUND_POLICY = "refund_policy"
    SHIPPING_POLICY = "shipping_policy"
    WARRANTY = "warranty"
    PRODUCT_FAQ = "product_faq"
    ORDER_STATUS = "order_status"
    CUSTOMER_DETAILS = "customer_details"
    REFUND_STATUS = "refund_status"
    SUPPORT_ISSUE = "support_issue"
    CANCEL_ORDER = "cancel_order"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"

class Route(str, Enum):
    RAG = "rag"
    TOOL = "tool"
    CONFIRMATION = "confirmation"
    CLARIFICATION = "clarification"
    ESCALATION = "escalation"


class ToolName(str, Enum):
    GET_ORDER_STATUS = "get_order_status"
    GET_CUSTOMER_DETAILS = "get_customer_details"
    CHECK_REFUND_STATUS = "check_refund_status"
    CREATE_SUPPORT_TICKET = "create_support_ticket"
    CANCEL_ORDER = "cancel_order"


# Decision rules:
# rag -> tool must be None
# tool -> tool is required
# confirmation -> tool is required
# clarification -> tool is optional
# escalation -> tool must be None

class AgentDecision(BaseModel):
    intent: Intent
    route: Route
    tool: ToolName | None = None
    tool_input: dict[str, Any] | None = None
    needs_confirmation: bool = False
    confirmation_received: bool = False
    needs_clarification: bool = False
    clarification_question: str | None = None