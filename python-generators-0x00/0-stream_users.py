#!/usr/bin/python3

import mysql.connector

def stream_users():
    """Generator that streams rows from the user_data table one by one."""
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Use your MySQL username
            password="",  # Use your MySQL password
            database="ALX_prodev"  # Use your database name
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all rows from the user_data table
        cursor.execute("SELECT * FROM user_data")

        # Use a generator to yield rows one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Clean up database resources
        if cursor is not None and cursor._executed:
            try:
                cursor.fetchall()  # Fetch any remaining results to clear the cursor
            except mysql.connector.Error:
                pass  # Ignore errors if there are no more results
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()