import sqlite3
import functools


def with_db_connection(func):
    """Decorator to handle database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            print("Database connection closed.")
    return wrapper


def transactional(func):
    """Decorator to manage database transactions."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to: {e}")
            raise
    return wrapper


@with_db_connection
def create_users_table(conn):
    """Create the users table with the correct schema."""
    cursor = conn.cursor()
    # Drop the table if it already exists
    cursor.execute("DROP TABLE IF EXISTS users")
    # Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()
    print("Table 'users' created (if not already present).")


@with_db_connection
def seed_users_table(conn):
    """Seed the users table with dummy data."""
    cursor = conn.cursor()
    # Insert dummy data
    cursor.executemany("""
        INSERT INTO users (name, email, age) 
        VALUES (?, ?, ?)
    """, [
        ("Alice", "alice@example.com", 25),
        ("Bob", "bob@example.com", 30),
        ("Charlie", "charlie@example.com", 35)
    ])
    conn.commit()
    print("Seeded 'users' table with dummy data.")


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update a user's email."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    if cursor.rowcount == 0:
        raise ValueError(f"No user found with id {user_id}")
    print(f"Updated user {user_id}'s email to {new_email}.")


# Script execution
if __name__ == "__main__":
    create_users_table()  # Create the table
    seed_users_table()    # Seed the table with data
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")  # Update the email