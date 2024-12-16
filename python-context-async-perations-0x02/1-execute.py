import mysql.connector

class ExecuteQuery:
    def __init__(self, db_config, query, params):  
        self.db_config = db_config
        self.query = query
        self.params = params
    
    def __enter__(self):
        self.connection = mysql.connector.connect(**self.db_config)  # create a connection
        self.cursor = self.connection.cursor()  # create a cursor
        return self.cursor  # return the cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, 'cursor') and self.cursor:  # check if cursor is still open
            self.cursor.close()  # close the cursor

        if hasattr(self, 'connection') and self.connection.is_connected():  # check if connection is still open
            self.connection.close()  # close the connection

        if exc_type:
            print(f"Error: {exc_value}")  # print the error
            return True  # swallow the exception


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "",
        "password": "",
        "database": "ALX_prodev"
    }
    
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)
    
    # Using the `with` statement for better resource management
    try:
        with ExecuteQuery(db_config, query, params) as cursor:
            cursor.execute(query, params)  # Execute the query with parameters
            results = cursor.fetchall()  # Fetch all results
            for row in results:
                print(row)  # Process each row
    except Exception as e:
        print(f"An error occurred: {e}")
