from datetime import datetime
from app.database.database import get_connection

def create_support_ticket(customer_id, order_id, issue_type, description):

    if not customer_id or not order_id or not issue_type or not description:
        return {
            "success": False,
            "data": None,
            "error": "customer_id, order_id, issue_type and description are required"
        }
    connection = get_connection()
    cursor = connection.cursor()
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
    connection.close()
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