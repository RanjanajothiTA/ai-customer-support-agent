from app.database.database import get_connection


def get_order_status(order_id, customer_id):

    if not order_id or not customer_id:
        return {
            "success": False,
            "data": None,
            "error": "order_id and customer_id are required"
        }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM orders WHERE order_id = ? AND customer_id = ?",
        (order_id, customer_id)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return {
            "success": True,
            "data": {
                "order_id": result[0],
                "customer_id": result[1],
                "product_name": result[2],
                "quantity": result[3],
                "order_date": result[4],
                "status": result[5],
                "payment_status": result[6],
                "estimated_delivery": result[7],
                "tracking_number": result[8],
                "return_eligible": result[9],
                "cancellation_eligible": result[10]
            },
            "error": None
        }

    return {
        "success": False,
        "data": None,
        "error": "Order not found"
    }