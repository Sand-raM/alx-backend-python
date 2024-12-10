#!/usr/bin/python3

import csv
import uuid
import mysql.connector

class Seed:

    @staticmethod
    def connect_db():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )
            print("Successfully connected to the database.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    @staticmethod
    def create_database(connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
            print("Database 'ALX_prodev' created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating database: {err}")

    @staticmethod
    def connect_to_prodev():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Shmurdaa3",
                database="ALX_prodev"
            )
            print("Successfully connected to the 'ALX_prodev' database.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    @staticmethod
    def create_table(connection):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_data (
                        user_id CHAR(36) PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        age DECIMAL(3, 0) NOT NULL,
                        INDEX (user_id)
                    )
                """)
            print("Table 'user_data' created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")

    @staticmethod
    def insert_data(connection, data_generator):
        try:
            with connection.cursor() as cursor:
                for row in data_generator:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
            connection.commit()
            print("Data inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")

    @staticmethod
    def data_generator(file_path):
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    row['age'] = int(row['age'])  # Convert age to integer
                    yield row
        except FileNotFoundError as e:
            print(f"Error: {e}")

    @staticmethod
    def seed():
        initial_connection = Seed.connect_db()
        if initial_connection:
            Seed.create_database(initial_connection)
            initial_connection.close()

            prodev_connection = Seed.connect_to_prodev()
            if prodev_connection:
                Seed.create_table(prodev_connection)
                data_gen = Seed.data_generator('user_data.csv')
                Seed.insert_data(prodev_connection, data_gen)
                prodev_connection.close()

# To call the seeding method:
seed_instance = Seed()
seed_instance.seed()                   