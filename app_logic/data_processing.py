import pandas as pd
import sqlite3

# from constants import DATABASE_PATH

class DataProcessor:
    def __init__(self):
        self.conn = sqlite3.connect("data/app_database.db")
        self.cur = self.conn.cursor()
    
    def initialise_db(self):
        # I want you to create the following table in my database
        config = {'question': ["What's your name?", "How old are you?"],
                  'colname': ['name', 'age'],
                  'q_type': ['text', 'text']}
        
        # Create a table for storing config data
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                colname TEXT NOT NULL,
                q_type TEXT NOT NULL
            )
        ''')

        # Insert config data into the config_data table
        for question, colname, q_type in zip(config['question'], config['colname'], config['q_type']):
            self.cur.execute('''
                INSERT INTO config (question, colname, q_type)
                VALUES (?, ?, ?)
            ''', (question, colname, q_type))

        # Construct the CREATE TABLE statement for response_data dynamically
        columns_sql = ', '.join([f"{colname} TEXT NOT NULL" for colname in config['colname']])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS response_data (id INTEGER PRIMARY KEY, {columns_sql})"

        # Create the response_data table
        self.cur.execute(create_table_sql)

        # Commit changes
        self.conn.commit()

    def list_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cur.fetchall()
        # Fetchall returns a list of tuples. Extract the first element from each tuple to get table names.
        table_names = [table[0] for table in tables]
        print(table_names)

    def close(self):
        # Close the database connection
        self.conn.close()

    def table_exists(self, table_name):
        # Query to check if the specified table exists in the sqlite_master table
        query = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?"

        # Execute the query, using the table_name parameter to prevent SQL injection
        self.cur.execute(query, (table_name,))

        # Fetch the result. It will be 1 if the table exists, 0 otherwise.
        exists = self.cur.fetchone()[0] == 1

        print(exists)

    def get_config(self):
        config = {'question': ["What's your name?", "How old are you?"],
                  'colname': ['name', 'age'],
                  'q_type': ['text', 'text']}
        
        config = pd.DataFrame(config)

        return config
    
    def append_data(self, data):
        print(data)

# Testing
# processor = DataProcessor()
# processor.list_tables()
# processor.table_exists('config')
# processor.initialise_db()
# processor.list_tables()
# processor.table_exists('config')