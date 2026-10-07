from app.database.database import get_connection


def get_customer_details(customer_id):

    if not customer_id:
        return {
            "success": False,
            "data": None,
            "error": "customer_id is required"
        }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE customer_id = ?",
        (customer_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return {
            "success": True,
            "data": {
                "customer_id": result[0],
                "name": result[1],
                "email": result[2],
                "phone": result[3]
            },
            "error": None
        }

    return {
        "success": False,
        "data": None,
        "error": "Customer not found"
    }