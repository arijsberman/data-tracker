import pandas as pd
from datetime import datetime 
from tkinter import simpledialog, messagebox

from user_interface.ui_components import MainWindow, NewWindow

class HomePage:
    def __init__(self, controller, master, config):
        self.controller = controller
        self.master = master
        self.config = config
        self.create_layout()
        
    def create_layout(self):
        self.window = MainWindow(self.master, layout=(2,2))
        self.window.add_button('Settings', 0, 0, self.open_settings_page)
        self.window.add_button('Collect Data', 0, 1, self.controller.run_data_collection)
        self.last_update_label = self.window.add_label(f'Last update: {self.controller.last_update}', 1, 0, 2)

    def open_settings_page(self):
        self.settings_page = SettingsPage(self.controller, self.window.master, self.config)

    # DEPRECATED
    # def collect_data(self):
    #     DataCollector(self.controller, self.window.master, self.config)

    def update_config(self, new_config):
        # Update the config of the home page
        self.config = new_config

        # Restart the settings page with added question
        self.settings_page.window.master.destroy()
        self.settings_page = SettingsPage(self.controller, self.window.master, self.config)
 

class SettingsPage(HomePage):
    def create_layout(self):
        # Get number of questions
        if isinstance(self.config, pd.DataFrame):
            questions = self.config.question.to_list()
        else:
            questions = []
        n_questions = len(questions)

        # Settings page
        self.window = NewWindow(self.master, layout=(n_questions + 1, 1))
        for idx, quest in enumerate(questions):
            self.window.add_label(quest, idx, 0)
        self.window.add_button('Add', n_questions, 0, self.get_new_question)

    def get_new_question(self):
        NewQuestionConfig(self.controller, self.window.master, config=None)

class NewQuestionConfig(HomePage):
    def create_layout(self):
        self.window = NewWindow(self.master, title='Configure new question')

        # Question Label and Text Input
        self.window.add_label('Question:', 0, 0)
        self.question = self.window.add_entry(0, 1)

        self.window.add_label('Identifier:', 1, 0)
        self.colname = self.window.add_entry(1, 1)

        self.window.add_label('Question Type:', 2, 0)
        self.q_type = self.window.add_dropdown(['Yes / No'], 2, 1)

        self.window.add_button('Save', 3, 0, self.save_new_question)


    def save_new_question(self):
        validated = self.controller.check_new_question(self.question.get(), self.colname.get(), self.q_type.get())
        if validated == 'NO ERROR':
            self.controller.save_new_question(self.question.get(), self.colname.get(), self.q_type.get())
            self.window.master.destroy()
        else:
            messagebox.showerror('', f'New question invalid: {validated.lower()}')


class DataCollector(HomePage):
    def create_layout(self):
        if isinstance(self.config, pd.DataFrame):
            answer = {}
            answer['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for _, row in self.config.iterrows():
                answer[row.colname] = messagebox.askquestion("Question", row.question)
            self.controller.save_response(answer)
        else:
            messagebox.showerror('', "No data to collect")

            