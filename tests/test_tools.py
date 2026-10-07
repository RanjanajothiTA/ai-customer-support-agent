from app.tools.order_tools import get_order_status
from app.tools.customer_tools import get_customer_details
from app.tools.refund_tools import check_refund_status
from app.tools.ticket_tools import create_support_ticket
from app.tools.cancel_tools import cancel_order
from app.database.database import get_connection

## Test cases for order_tools.py
def test_get_order_status_success():
    result = get_order_status("ORD1001", "CUST1001")

    assert result["success"] is True
    assert result["data"]["order_id"] == "ORD1001"
    assert result["data"]["customer_id"] == "CUST1001"
    assert result["data"]["status"] == "Shipped"

def test_get_order_status_not_found():
    result = get_order_status("ORD9999", "CUST1001")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Order not found"

def test_get_order_status_wrong_customer():
    result = get_order_status("ORD1001", "CUST1002")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Order not found"

def test_get_order_status_missing_input():
    result = get_order_status("", "CUST1001")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "order_id and customer_id are required"

### Test cases for customer_tools.py
def test_get_customer_details_success():
    result = get_customer_details("CUST1001")

    assert result["success"] is True
    assert result["data"]["customer_id"] == "CUST1001"
    assert result["data"]["name"] == "Ananya Sharma"
    assert result["data"]["email"] == "ananya@example.com"

def test_get_customer_details_not_found():
    result = get_customer_details("CUST9999")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Customer not found"

def test_get_customer_details_missing_input():
    result = get_customer_details("")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "customer_id is required"


### Test cases for refund_tools.py
def test_check_refund_status_success():
    result = check_refund_status("ORD1005", "CUST1001")

    assert result["success"] is True
    assert result["data"]["refund_id"] == "REF5001"
    assert result["data"]["order_id"] == "ORD1005"
    assert result["data"]["status"] == "Processing"
    assert result["data"]["amount"] == 2499.0

def test_check_refund_status_not_found():
    result = check_refund_status("ORD9999", "CUST1001")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Refund not found"

def test_check_refund_status_wrong_customer():
    result = check_refund_status("ORD1005", "CUST1002")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Refund not found"

def test_check_refund_status_missing_input():
    result = check_refund_status("", "CUST1001")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "order_id and customer_id are required"

### Test cases for ticket_tools.py
def test_create_support_ticket_success():
    result = create_support_ticket(
        "CUST1001",
        "ORD1001",
        "Damaged product",
        "The headphones arrived damaged."
    )

    assert result["success"] is True
    assert result["data"]["customer_id"] == "CUST1001"
    assert result["data"]["order_id"] == "ORD1001"
    assert result["data"]["issue_type"] == "Damaged product"
    assert result["data"]["status"] == "Open"

def test_create_support_ticket_missing_input():
    result = create_support_ticket(
        "",
        "ORD1001",
        "Damaged product",
        "The headphones arrived damaged."
    )

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == (
        "customer_id, order_id, issue_type and description are required"
    )

### Test cases for cancel_tools.py
def test_cancel_order_not_eligible():
    result = cancel_order("ORD1001", "CUST1001")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Order is not eligible for cancellation"

def test_cancel_order_already_cancelled():
    result = cancel_order("ORD1006", "CUST1001")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Order is already cancelled"

def test_cancel_order_wrong_customer():
    result = cancel_order("ORD1001", "CUST1002")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Order not found"

def test_cancel_order_success():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO orders (
            order_id,
            customer_id,
            product_name,
            quantity,
            order_date,
            status,
            payment_status,
            estimated_delivery,
            tracking_number,
            return_eligible,
            cancellation_eligible
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "TEST_CANCEL_001",
            "CUST1001",
            "Test Product",
            1,
            "2026-10-07",
            "Pending",
            "Paid",
            "2026-10-10",
            "TEST_TRACKING_001",
            "Yes",
            "Yes"
        )
    )

    connection.commit()
    connection.close()

    try:
        result = cancel_order(
            "TEST_CANCEL_001",
            "CUST1001"
        )

        assert result["success"] is True
        assert result["data"]["order_id"] == "TEST_CANCEL_001"
        assert result["data"]["customer_id"] == "CUST1001"

    finally:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM orders WHERE order_id = ?",
            ("TEST_CANCEL_001",)
        )

        connection.commit()
        connection.close()