import sqlite3
import functools

# Global cache dictionary
query_cache = {}

# Implementing the cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')  # Get the query from keyword arguments
        if not query:
            raise ValueError("No 'query' argument provided to the function.")

        # Check if the query result is in the cache
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]

        # If not cached, execute the function and cache the result
        print("Executing and caching query:", query)
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Including the with_db_connection decorator from the previous task
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# Fetching users with caching enabled
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call: Executes the query and caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print("Users fetched:", users)

# Second call: Uses the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Users fetched again:", users_again)