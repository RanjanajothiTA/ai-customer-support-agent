
from datetime import datetime
from app.database.database import get_connection


def create_support_ticket(customer_id, order_id, issue_type, description):
    if not customer_id or not order_id or not issue_type or not description:
        return {
            "success": False,
            "data": None,
            "error": (
                "customer_id, order_id, issue_type and description are required"
            )
        }

    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Verify that the order belongs to this customer.
        cursor.execute(
            """
            SELECT order_id
            FROM orders
            WHERE order_id = ? AND customer_id = ?
            """,
            (order_id, customer_id)
        )

        if not cursor.fetchone():
            return {
                "success": False,
                "data": None,
                "error": "Order not found for this customer"
            }

        # Generate the next ticket ID.
        cursor.execute(
            """
            SELECT ticket_id
            FROM support_tickets
            WHERE ticket_id LIKE 'TKT%'
            ORDER BY CAST(SUBSTR(ticket_id, 4) AS INTEGER) DESC
            LIMIT 1
            """
        )

        last_ticket = cursor.fetchone()

        if last_ticket:
            last_number = int(last_ticket[0][3:])
            ticket_id = f"TKT{last_number + 1}"
        else:
            ticket_id = "TKT7001"

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO support_tickets (
                ticket_id,
                customer_id,
                order_id,
                issue_type,
                description,
                priority,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket_id,
                customer_id,
                order_id,
                issue_type,
                description,
                "Medium",
                "Open",
                created_at
            )
        )

        connection.commit()

        return {
            "success": True,
            "data": {
                "ticket_id": ticket_id,
                "customer_id": customer_id,
                "order_id": order_id,
                "issue_type": issue_type,
                "description": description,
                "priority": "Medium",
                "status": "Open"
            },
            "error": None
        }

    except Exception:
        if connection is not None:
            connection.rollback()

        return {
            "success": False,
            "data": None,
            "error": "Unable to create support ticket right now"
        }

    finally:
        if connection is not None:
            connection.close()
