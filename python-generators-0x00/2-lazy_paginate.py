#!/usr/bin/python3
from seed import Seed


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    :param page_size: Number of users per page
    :param offset: Offset for pagination
    :return: List of user rows
    """
    connection = Seed.connect_to_prodev()  # Use the Seed class to connect to the database
    if connection is None:
        print("Failed to connect to the database.")
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()


def lazy_paginate(page_size):
    """
    Generator to lazily load pages of users.
    :param page_size: Number of users per page
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop if no more users are found
            break
        yield page
        offset += page_size  # Increment the offset by the page size                                                                    