import tkinter as tk

from user_interface.ui_views import HomePage
from app_logic.database_manager import DatabaseManager
from constants import DATABASE_PATH


class AppController:
    def __init__(self) -> None:
        pass

    def open_home_page(self):
        # Initializing the app
        root = tk.Tk()

        # Landing page
        home_page = HomePage(root)

        # Get config file
        db = DatabaseManager(DATABASE_PATH)
        config_exists = db.table_exists('config_data')
        if config_exists:
            config_data = db.get_dataframe_from_table('config_data')
            home_page.config = config_data

        # Running the app
        root.mainloop()