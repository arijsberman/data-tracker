import tkinter as tk
import os
import ctypes
import time
from datetime import date
import pandas as pd

from user_interface.ui_views import HomePage, DataCollector
from app_logic.database_manager import DatabaseManager
from constants import DATABASE_PATH


class AppController:
    def __init__(self) -> None:
        self.db = DatabaseManager(DATABASE_PATH)
        self.config_data = self.db.get_dataframe_from_table('config_data')
        self.last_update = None
        
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

    def save_response(self, row_to_append):
        # Append user data to responses table
        self.db.append_row_to_table('responses', row_to_append)

        # Update the "last update" parameter of the app
        self.get_last_update()

    def get_idle_duration(self):
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    
    def check_for_interrupt(self):
        if os.path.exists("interrupt.flag"):
            os.remove("interrupt.flag")  # Remove the flag to reset the interrupt
            return True
        return False
    
    def get_last_update(self):
        if self.db.table_exists('responses'):
            responses = self.db.get_dataframe_from_table('responses')
            responses['datetime'] = pd.to_datetime(responses['datetime'])
            self.last_update = responses['datetime'].max().date()

    def run_in_background(self):
        while True:
            # If open menu shortcut is launched, open the main menu
            if self.check_for_interrupt():
                self.open_home_page()

            # If computer is in use and the last response was before today, collect user data
            if self.last_update is not None:
                if self.get_idle_duration() < 5 and self.last_update < date.today():
                    self.run_data_collection()

            time.sleep(1)


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint)]
