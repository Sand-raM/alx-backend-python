import time
import sqlite3
import functools

# Reuse the with_db_connection decorator from the previous task
def with_db_connection(func):
    """Decorator to handle database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Implement the retry_on_failure decorator
def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function if it raises an exception.
    :param retries: Number of times to retry before giving up.
    :param delay: Delay (in seconds) between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    last_exception = e
                    if attempt < retries - 1:
                        time.sleep(delay)
                    else:
                        raise last_exception  # Raise the last exception if all retries fail
        return wrapper
    return decorator

# Apply both decorators to the function
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the 'users' table with retry logic for transient errors.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Test the function
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"Failed to fetch users after retries: {e}")