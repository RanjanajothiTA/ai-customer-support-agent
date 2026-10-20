from app.agent.decision import AgentDecision, Route
from app.agent.handlers import (
    handle_rag,
    handle_order_status,
    handle_customer_details,
    handle_refund_status,
    handle_create_support_ticket,
    handle_cancel_order
)

def route_decision(decision: AgentDecision):

    if decision.route == Route.RAG:
        return handle_rag(decision.tool_input["query"])

    if decision.route == Route.TOOL:
        if decision.tool.value == "get_order_status":
            return handle_order_status(
                decision.tool_input["order_id"],
                decision.tool_input["customer_id"]
            )

        if decision.tool.value == "get_customer_details":
            return handle_customer_details(
                decision.tool_input["customer_id"]
            )
        if decision.tool.value == "check_refund_status":
            return handle_refund_status(
                decision.tool_input["order_id"],
                decision.tool_input["customer_id"]
            )
        if decision.tool.value == "create_support_ticket":
            return handle_create_support_ticket(
                decision.tool_input["customer_id"],
                decision.tool_input["order_id"],
                decision.tool_input["issue_type"],
                decision.tool_input["description"]
            )
    if decision.route == Route.CONFIRMATION:

        if not decision.confirmation_received:

            order_result = handle_order_status(
                decision.tool_input["order_id"],
                decision.tool_input["customer_id"]
            )

            if not order_result["success"]:
                return order_result

            if order_result["data"]["cancellation_eligible"] == "No":
                return {
                    "type": "cancellation_not_allowed",
                    "message": f"Order {decision.tool_input['order_id']} is not eligible for cancellation.",
                    "order_id": decision.tool_input["order_id"],
                    "customer_id": decision.tool_input["customer_id"]
                }

            return {
                "type": "confirmation_required",
                "message": f"Are you sure you want to cancel order {decision.tool_input['order_id']}?",
                "order_id": decision.tool_input["order_id"],
                "customer_id": decision.tool_input["customer_id"]
            }

        return handle_cancel_order(
            decision.tool_input["order_id"],
            decision.tool_input["customer_id"]
        )

    if decision.route == Route.CLARIFICATION:
        return "CLARIFICATION"

    if decision.route == Route.ESCALATION:
        return "ESCALATION"