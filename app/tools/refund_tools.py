from app.database.database import get_connection

def check_refund_status(order_id, customer_id):

    if not order_id or not customer_id:
        return {
            "success": False,
            "data": None,
            "error": "order_id and customer_id are required"
        }
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM refunds WHERE order_id = ? AND customer_id = ?",
        (order_id, customer_id)
    )
    result = cursor.fetchone()
    connection.close()
    if result:
        return {
            "success": True,
            "data": {
                "refund_id": result[0],
                "order_id": result[1],
                "customer_id": result[2],
                "status": result[3],
                "amount": result[4],
                "requested_date": result[5]
            },
            "error": None
        }
    return {
        "success": False,
        "data": None,
        "error": "Refund not found"
    }