#!/usr/bin/python3

from seed import Seed

# Connect to the database
connection = Seed.connect_db()
if connection:
    # Create the database
    Seed.create_database(connection)
    connection.close()
    print("Connection successful.")

    # Connect to the 'ALX_prodev' database
    connection = Seed.connect_to_prodev()

    if connection:
        # Create the table
        Seed.create_table(connection)

        # Insert data from the CSV file
        data_gen = Seed.data_generator('user_data.csv')
        Seed.insert_data(connection, data_gen)

        # Check if the database exists
        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database 'ALX_prodev' is present.")

        # Fetch and print the first 5 rows from the 'user_data' table
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        connection.close()