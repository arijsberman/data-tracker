import tkinter as tk
import os
import ctypes
import time
from datetime import date
import pandas as pd
import threading

from user_interface.ui_views import HomePage, DataCollector
from app_logic.database_manager import DatabaseManager
from constants import DATABASE_PATH


class AppController:
    def __init__(self) -> None:
        self.db = DatabaseManager(DATABASE_PATH)
        self.config_data = self.db.get_dataframe_from_table('config_data')
        self.last_update = None
        self.thread_stop_event = threading.Event()
        
    def open_home_page(self):
        # Initializing the app
        root = tk.Tk()

        # Landing page
        self.home_page = HomePage(self, root, self.config_data)

        # Running the app
        root.mainloop()

        # When home page closed, terminate the background process too
        print('Terminating background process...')
        self.thread_stop_event.set()

    def run_data_collection(self):
        # Landing page
        DataCollector(self, self.home_page.master, self.config_data)

        # Restart the home page after collecting data
        print('Updating last_update label...')
        self.update_home_page_label()
    
    def update_home_page_label(self):
        self.home_page.last_update_label.config(text=f'Last update: {self.last_update}')

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

    def check_new_question(self, question, colname, q_type):
        # Check if colname starts with a digit
        if colname[0].isdigit():
            error = 'Question identifier cannot start with a digit.'
            print(error)
            return error
        
        # If all checks pass, validate new question
        print('New question validated.')
        return 'NO ERROR'

    def save_response(self, row_to_append):
        # Append user data to responses table
        print('Saving response data to database...')
        self.db.append_row_to_table('responses', row_to_append)

        # Update the "last update" parameter of the app
        print('Updating self.last_update value...')
        self.get_last_update()

    def get_idle_duration(self):
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    
    # DEPRECATED
    # def check_for_interrupt(self):
    #     if os.path.exists("interrupt.flag"):
    #         os.remove("interrupt.flag")  # Remove the flag to reset the interrupt
    #         return True
    #     return False
    
    def get_last_update(self):
        if self.db.table_exists('responses'):
            responses = self.db.get_dataframe_from_table('responses')
            responses['datetime'] = pd.to_datetime(responses['datetime'])
            self.last_update = responses['datetime'].max().date()

    def run_in_background(self):
        def listen_for_user_input():
            while not self.thread_stop_event.is_set():
                # Wait until home page is launched
                if hasattr(self, 'home_page'):
                    # print(f'Current idle duration: {self.get_idle_duration()}')
                    # If computer is in use and the last response was before today, collect user data
                    if self.last_update is not None and self.config_data is not None:
                        if self.get_idle_duration() < 5 and self.last_update < date.today():
                            self.run_data_collection()

                    time.sleep(1)
        
        self.thread = threading.Thread(target=listen_for_user_input)
        self.thread.start()


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint)]
