from app.database.database import get_connection


def get_customer_details(customer_id):

    if not customer_id:
        return {
            "success": False,
            "data": None,
            "error": "customer_id is required"
        }

    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM customers WHERE customer_id = ?",
            (customer_id,)
        )

        result = cursor.fetchone()

        if not result:
            return {
                "success": False,
                "data": None,
                "error": "Customer not found"
            }

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

    except Exception:
        return {
            "success": False,
            "data": None,
            "error": "Unable to retrieve customer details right now"
        }

    finally:
        if connection is not None:
            connection.close()
