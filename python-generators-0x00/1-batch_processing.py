#!/usr/bin/python3
import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator function to fetch users from the database in batches.
    :param batch_size: Number of rows per batch
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Use your MySQL username
            password="",  # Use your MySQL password
            database="ALX_prodev"  # Use your database name
        )
        cursor = connection.cursor(dictionary=True)

        # Query to fetch users in batches
        cursor.execute("SELECT * FROM user_data")
        while True:
            batch = cursor.fetchmany(batch_size)  # Fetch a batch of rows
            if not batch:
                break  # Stop if there are no more rows
            yield batch  # Yield the current batch

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Proper cleanup to avoid errors
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(f"Error while closing cursor: {e}")
        try:
            if connection.is_connected():
                connection.close()
        except Exception as e:
            print(f"Error while closing connection: {e}")


def batch_processing(batch_size):
    """
    Process users in batches and print those over the age of 25.
    :param batch_size: Number of rows per batch
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:  # Filter users based on age
                print(user)