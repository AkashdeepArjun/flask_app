class  MyDatabase:
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = self.connect_to_database(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        
        if exc_type is not None:
            print(f"An exception occurred: {exc_value}")
            return False  # Propagate the exception 
        if self.connection:
            self.close_connection(self.connection)
            return True  # Suppress the exception if any

    def connect_to_database(self, db_name):
        # Logic to connect to the database
        print(f"Connecting to database: {db_name}")
        return f"Connection to {db_name}"

    def close_connection(self, connection):
        # Logic to close the database connection
        print(f"Closing connection: {connection}")


if __name__ == "__main__":
    print("Starting the database context manager example...")

    print("TEST-1")
    with MyDatabase("my_database.db") as db_connection:
        print(f"Using database connection: {db_connection}")


    print("\nTEST-2")
    try:
        with MyDatabase("my_database.db") as db_connection:
            print(f"Using database connection: {db_connection}")
            # Simulate an exception
            raise ValueError("Simulated exception during database operation")
    except ValueError as e:
        print(f"Caught an exception: {e}")