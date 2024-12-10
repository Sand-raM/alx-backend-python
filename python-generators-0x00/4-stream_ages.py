#!/usr/bin/python3
from seed import Seed

def stream_user_ages():
    """
    Generator to stream user ages from the database.
    Fetches user ages one by one for memory-efficient processing.
    """
    connection = Seed.connect_to_prodev()  # Corrected to use the Seed class
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT age FROM user_data")  # Query to fetch ages
        for row in cursor:
            yield row['age']  # Yield each age one by one
    finally:
        cursor.close()  # Ensure cursor is closed
        connection.close()  # Ensure connection is closed


def calculate_average_age():
    """
    Calculate the average age of users using the generator `stream_user_ages`.
    Memory-efficient implementation without loading the entire dataset.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    # Avoid division by zero
    if count == 0:
        print("No users found.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")


# Entry point for the script
if __name__ == "__main__":
    calculate_average_age()