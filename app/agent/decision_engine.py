import re

from app.agent.decision import AgentDecision


def decide(message: str, customer_id: str, current_order_id: str | None = None
):

    message = message.lower()
    if current_order_id and re.search(
        r"\b(it|that|this)\b",
        message
    ) and any(word in message for word in ["still", "again", "same issue"]):
        return AgentDecision(
            intent="support_issue",
            route="clarification",
            tool_input={
                "order_id": current_order_id
            },
            needs_clarification=True,
            clarification_question="Could you please describe what is still happening?"
        )
    
    if "return policy" in message or "return" in message:
        query = message

        if current_order_id and re.search(
            r"\b(it|that|this)\b",
            message
        ):
            query = f"{message} The referenced order ID is {current_order_id}."

        return AgentDecision(
            intent="return_policy",
            route="rag",
            tool_input={
                "query": query
            }
        )


    if "refund" in message:
        refund_match = re.search(r"\bORD\d+\b", message.upper())

        if refund_match:
            order_id = refund_match.group()

            return AgentDecision(
                intent="refund_status",
                route="tool",
                tool="check_refund_status",
                tool_input={
                    "order_id": order_id,
                    "customer_id": customer_id
                }
            )

        return AgentDecision(
            intent="refund_status",
            route="clarification",
            needs_clarification=True,
            clarification_question="Could you please provide your order ID?"
        )
    if "customer details" in message:
        return AgentDecision(
            intent="customer_details",
            route="tool",
            tool="get_customer_details",
            tool_input={
                "customer_id": customer_id
            }
        )
    if "damaged" in message or "broken" in message or "not working" in message:

        support_order_match = re.search(r"\bORD\d+\b", message.upper())

        if "damaged" in message:
            issue_type = "damaged"
        elif "broken" in message:
            issue_type = "broken"
        else:
            issue_type = "not_working"

        if support_order_match:
            order_id = support_order_match.group()

            return AgentDecision(
                intent="support_issue",
                route="clarification",
                tool_input={
                    "order_id": order_id,
                    "issue_type": issue_type
                },
                needs_clarification=True,
                clarification_question="Could you please describe the issue?"
            )

        return AgentDecision(
            intent="support_issue",
            route="clarification",
            needs_clarification=True,
            clarification_question="Could you please provide your order ID and describe the issue?"
        )
    if "cancel" in message:
        cancel_match = re.search(r"\b(?:ORD\d+|CONFIRM_TEST_\d+)\b", message.upper())

        if cancel_match:
            order_id = cancel_match.group()

            return AgentDecision(
                intent="cancel_order",
                route="confirmation",
                tool="cancel_order",
                tool_input={
                    "order_id": order_id,
                    "customer_id": customer_id
                },
                needs_confirmation=True
            )

        return AgentDecision(
            intent="cancel_order",
            route="clarification",
            needs_clarification=True,
            clarification_question="Could you please provide your order ID?"
        )
    order_match = re.search(r"\bORD\d+\b", message.upper())

    if order_match:
        order_id = order_match.group()

        return AgentDecision(
            intent="order_status",
            route="tool",
            tool="get_order_status",
            tool_input={
                "order_id": order_id,
                "customer_id": customer_id
            }
        )

    if "order" in message:
        if current_order_id:
            return AgentDecision(
                intent="order_status",
                route="tool",
                tool="get_order_status",
                tool_input={
                    "order_id": current_order_id,
                    "customer_id": customer_id
                }
            )

        return AgentDecision(
            intent="order_status",
            route="clarification",
            needs_clarification=True,
            clarification_question="Could you please provide your order ID?"
        )
    return AgentDecision(
        intent="unsupported",
        route="escalation"
    )