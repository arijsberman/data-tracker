import pandas as pd
import sqlite3

class DatabaseManager:
    def __init__(self, database_path):
        self.path = database_path
    
    def open(self):
        # Open database connection
        self.conn = sqlite3.connect(self.path)
        self.cur = self.conn.cursor()

    def close(self):
        # Close the database connection
        self.conn.close()

    def table_exists(self, table_name):
        # Open database connection
        self.open()

        # Query to check if the specified table exists in the sqlite_master table
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?"

        # Execute the query, using the table_name parameter to prevent SQL injection
        self.cur.execute(query, (table_name,))

        # Fetch the result. It will be 1 if the table exists, 0 otherwise.
        exists = self.cur.fetchone()[0] == 1

        # Close database connection
        self.close()

        return exists

    def create_table_from_dataframe(self, df, table_name):
        """
        Create an SQLite table from a pandas DataFrame.

        Parameters:
        - df: pandas DataFrame containing the data.
        - table_name: Name of the SQLite table to create.
        - db_path: Path to the SQLite database file.
        - primary_key: The name of the column to use as a primary key. If None, no primary key is set.
        - pk_data_type: Data type of the primary key. Defaults to 'INTEGER AUTOINCREMENT' suitable for numeric IDs.
        """
        # Open database connection
        self.open()

        # Construct the CREATE TABLE SQL statement
        columns_sql = []
        print(df)
        for col_name in df.columns:
            col_type = 'TEXT'
            columns_sql.append(f"{col_name} {col_type}")
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_sql)});"
        
        print(create_table_sql)

        # Execute the CREATE TABLE SQL statement
        self.cur.execute(create_table_sql)

        # Insert DataFrame data into the table
        # Prepare a tuple of question marks placeholders for each column
        placeholders = ', '.join(['?'] * len(df.columns))
        insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
        for _, row in df.iterrows():
            self.cur.execute(insert_sql, tuple(row))

        # Commit the changes and close the connection
        self.conn.commit()
        self.close()
        
    def list_tables(self):
        # Connect to database
        self.open()
        # Query master table to get existing tables
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cur.fetchall()
        # Fetchall returns a list of tuples. Extract the first element from each tuple to get table names.
        table_names = [table[0] for table in tables]
        # Close connection
        self.close()
        
        print(table_names)
        return table_names
    
    def get_dataframe_from_table(self, table_name):
        """
        Query an SQL table and return the results as a pandas DataFrame.

        Parameters:
        - table_name: The name of the SQL table to query.
        - db_path: The path to the SQLite database file.

        Returns:
        - A pandas DataFrame containing the data from the specified SQL table.
        """
        try:
            # Create a connection to the database
            self.open()
            
            # Construct the SQL query
            query = f"SELECT * FROM {table_name}"
            
            # Execute the query and return the results as a DataFrame
            df = pd.read_sql_query(query, self.conn)
            
            # Close the connection to the database
            self.close()

            return df
        except Exception as e:
            print(f"Error: {e}.")
            
            # Close the connection if an error occurs
            self.close()
            
            return None

    def get_table_columns(self, table_name):
        self.open()
        self.cur.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in self.cur.fetchall()]  # Column names are in the second field
        self.close()
        return columns
    
    def append_row_to_table(self, table_name, row):
        # If table doesn't exist, create it first
        if not self.table_exists(table_name):
            # Create table from row
            self.create_table_from_dataframe(pd.DataFrame([row], index=[0]), table_name)
        else:
            # Check that all of the columns in the insert are already in the table
            existing_columns = self.get_table_columns(table_name)
            missing_columns = [col for col in row.keys() if col not in existing_columns]

            # Add any missing columns to the table
            for col in missing_columns:
                self.open()
                self.cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {col} TEXT")
                self.conn.commit()
                self.close()

            
            # Create SQL query for row insert
            columns = ', '.join(row.keys())
            placeholders = ', '.join('?' * len(row))
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # Execute SQL query
            self.open()
            self.cur.execute(insert_sql, tuple(row.values()))
            self.conn.commit()
            self.close()
            

# Testing
# processor = DataProcessor("data/app_database.db")
# processor.list_tables()
# exists = processor.table_exists('config_data')
# if not exists:
#     config = {'question': ["What's your name?", "How old are you?"],
#               'colname': ['name', 'age'],
#               'q_type': ['text', 'text']}
#     config = pd.DataFrame(config)
#     processor.create_table_from_dataframe(config, 'config_data')
# processor.list_tables()
# processor.table_exists('config_data')
# processor.get_dataframe_from_table('config_data')
