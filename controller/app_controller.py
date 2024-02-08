import tkinter as tk
import ctypes
import time

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

    def save_response(self, row_to_append):
        self.db.append_row_to_table('responses', row_to_append)

        print(self.db.get_dataframe_from_table('responses'))

    def get_idle_duration(self):
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        
        return millis / 1000.0

    def run_in_background(self):
        while True:
            idle_time = self.get_idle_duration()
            print(f"System idle for {idle_time} seconds")
            if idle_time < 5:  # For example, if the system has been idle for less than 5 seconds
                print("Possibly just unlocked or still in use.")
                # Place your logic here to launch the Tkinter app if conditions are met
            time.sleep(1)


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint)]


    
