import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", args[0] if args else None)
        if query:
            print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Function to create the 'users' table for testing
def create_users_table():
    conn = sqlite3.connect('users.db')
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

# Function to seed the database with dummy data
def seed_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO users (name, age) VALUES (?, ?)
    """, [
        ("Jon", 25),
        ("Gabie", 30),
        ("Ehrmatraunt", 35)
    ])
    print("Seeded 'users' table with dummy data.")
    conn.commit()
    conn.close()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results