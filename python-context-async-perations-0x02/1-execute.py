import mysql.connector

class ExecuteQuery:
    def __init__(self, db_config, query, params):  
        self.db_config = db_config
        self.query = query
        self.params = params
    
    def __enter__(self):
        self.connection = mysql.connector.connect(**self.db_config)  # create a connection
        self.cursor = self.connection.cursor()  # create a cursor

        return self.cursor # return the cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, 'cursor') and self.cursor:  # check if cursor is still open
            self.cursor.close() # close the cursor

        if hasattr(self, 'connection') and self.connection.is_connected(): # check if connection is still open
            self.connection.close() # close the connection

        if exc_type:
            print(f"Error: {exc_value}") # print the error
            return True  # swallow the exception
        

if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "GabieSE",
        "password": "Shmurdaa3",
        "database": "ALX_prodev"
        }
    
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)