import pandas as pd
from tkinter import simpledialog, messagebox

from user_interface.ui_components import MainWindow, NewWindow

class HomePage:
    def __init__(self, master):
        self.master = master
        self.window = MainWindow(self.master, layout=(2,2))
        self.window.add_button('Settings', 0, 0, self.open_settings_page)
        self.window.add_button('Collect Data', 0, 1, self.collect_data)
        self.window.add_label('Data collected today: yes', 1, 0, 2)
        self.config = None

    def open_settings_page(self):
        
        if isinstance(self.config, pd.DataFrame):
            questions = self.config.question.to_list()
        else:
            questions = []

        n_questions = len(questions)

        # Settings page
        settings_page = NewWindow(self.master, layout=(n_questions + 1, 1))
        for idx, quest in enumerate(questions):
            settings_page.add_label(quest, idx, 0)
        settings_page.add_button('Add', n_questions, 0)

    def collect_data(self):
        if isinstance(self.config, pd.DataFrame):
            answer = {}
            for _, row in self.config.iterrows():
                answer[row.colname] = simpledialog.askstring("Input", row.question)
            print(answer)
        else:
            messagebox.showerror('Whadupp', "No data to collect")