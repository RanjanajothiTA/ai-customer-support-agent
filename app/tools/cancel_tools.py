
from app.database.database import get_connection


def cancel_order(order_id, customer_id):
    if not order_id or not customer_id:
        return {
            "success": False,
            "data": None,
            "error": "order_id and customer_id are required"
        }

    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE order_id = ?
            AND customer_id = ?
            """,
            (order_id, customer_id)
        )

        result = cursor.fetchone()

        if not result:
            return {
                "success": False,
                "data": None,
                "error": "Order not found"
            }

        if result[5] == "Cancelled":
            return {
                "success": False,
                "data": None,
                "error": "Order is already cancelled"
            }

        if result[10] == "No":
            return {
                "success": False,
                "data": None,
                "error": "Order is not eligible for cancellation"
            }

        cursor.execute(
            """
            UPDATE orders
            SET status = ?,
                cancellation_eligible = ?
            WHERE order_id = ?
            AND customer_id = ?
            """,
            ("Cancelled", "No", order_id, customer_id)
        )

        if cursor.rowcount != 1:
            connection.rollback()
            return {
                "success": False,
                "data": None,
                "error": "Order cancellation could not be completed"
            }

        connection.commit()

        return {
            "success": True,
            "data": {
                "order_id": order_id,
                "customer_id": customer_id
            },
            "error": None
        }

    except Exception:
        if connection is not None:
            connection.rollback()

        return {
            "success": False,
            "data": None,
            "error": "Unable to process cancellation right now"
        }

    finally:
        if connection is not None:
            connection.close()
