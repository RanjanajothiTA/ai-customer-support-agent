from app.database.database import get_connection


def cancel_order(order_id, customer_id):

    if not order_id or not customer_id:
        return {
            "success": False,
            "data": None,
            "error": "order_id and customer_id are required"
        }

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
        connection.close()

        return {
            "success": False,
            "data": None,
            "error": "Order not found"
        }
    if result[5] == "Cancelled":
        connection.close()

        return {
            "success": False,
            "data": None,
            "error": "Order is already cancelled"
        }

    if result[10] == "No":
        connection.close()

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
    connection.commit()
    connection.close()
    return {
        "success": True,
        "data": {
            "order_id": order_id,
            "customer_id": customer_id
        },
        "error": None
    }