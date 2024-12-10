import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator to automatically handle opening and closing of database connections.
    Passes the connection object as the first argument to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open a database connection
        conn = sqlite3.connect("users.db")
        try:
            # Pass the connection to the decorated function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed after function execution
            conn.close()
            print("Database connection closed.")
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by ID from the users table.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Helper function to ensure the 'users' table exists
def create_users_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    print("Table 'users' created (if not already present).")
    conn.commit()
    conn.close()

# Helper function to populate the 'users' table with dummy data
def seed_users_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO users (name, age) VALUES (?, ?)
    """, [
        ("Alice", 25),
        ("Bob", 30),
        ("Charlie", 35),
        ("Jon", 25),
        ("Gabie", 30),
        ("Ehmrmatraunt", 35)
    ])
    print("Seeded 'users' table with dummy data.")
    conn.commit()
    conn.close()

# Main function to test the script
if __name__ == "__main__":
    # Create and seed the table
    create_users_table()
    seed_users_table()

    # Fetch a user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)