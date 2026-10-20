from app.rag.rag_service import generate_rag_response

def handle_rag(query):
    return generate_rag_response(query)

from app.tools.order_tools import get_order_status


def handle_order_status(order_id, customer_id):
    return get_order_status(order_id, customer_id)

from app.tools.customer_tools import get_customer_details


def handle_customer_details(customer_id):
    return get_customer_details(customer_id)

from app.tools.refund_tools import check_refund_status


def handle_refund_status(order_id, customer_id):
    return check_refund_status(order_id, customer_id)

from app.tools.ticket_tools import create_support_ticket


def handle_create_support_ticket(
    customer_id,
    order_id,
    issue_type,
    description
):
    return create_support_ticket(
        customer_id,
        order_id,
        issue_type,
        description
    )

from app.tools.cancel_tools import cancel_order

def handle_cancel_order(order_id, customer_id):
    return cancel_order(order_id, customer_id)

from app.llm_service import generate_final_response
def handle_final_response(user_message, agent_result):
    return generate_final_response(
        user_message,
        agent_result
    )