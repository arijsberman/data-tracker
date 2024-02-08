import tkinter as tk
import pandas as pd

from user_interface.ui_views import HomePage, DataCollector
from app_logic.database_manager import DatabaseManager
from constants import DATABASE_PATH


class AppController:
    def __init__(self) -> None:
        self.db = DatabaseManager(DATABASE_PATH)
        self.config_data = self.db.get_dataframe_from_table('config_data')

    def open_home_page(self):
        # Initializing the app
        root = tk.Tk()

        # Landing page
        self.home_page = HomePage(self, root, self.config_data)

        # Running the app
        root.mainloop()

    def run_data_collection(self):
        # Initializing the app
        root = tk.Tk()
        root.withdraw()

        # Landing page
        DataCollector(self, root, self.config_data)

        # Running the app
        root.mainloop()

    def save_new_question(self, question, colname, q_type):
        # Append new question to database
        row_to_append = {'question': question,
                         'colname': colname,
                         'q_type': q_type}
        self.db.append_row_to_table('config_data', row_to_append)

        # Get new config
        self.config_data = self.db.get_dataframe_from_table('config_data')

        # Update view with new config data
        self.home_page.update_config(self.config_data)