from pathlib import Path
import sqlite3


DATABASE_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "database"
    / "shopease.db"
)


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            payment_status TEXT NOT NULL,
            estimated_delivery TEXT,
            tracking_number TEXT,
            return_eligible TEXT NOT NULL,
            cancellation_eligible TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS refunds (
            refund_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            status TEXT NOT NULL,
            amount REAL NOT NULL,
            requested_date TEXT NOT NULL,

            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            ticket_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_id TEXT,
            issue_type TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id),

            FOREIGN KEY (order_id)
                REFERENCES orders(order_id)
        )
    """)
    connection.commit()
    connection.close()

    print("Customers table created successfully.")
    print("Orders table created successfully.")
    print("Refunds table created successfully.")
    print("Support tickets table created successfully.")

if __name__ == "__main__":
    create_tables()