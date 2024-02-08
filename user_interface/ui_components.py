import tkinter as tk
from tkinter import ttk 

class MainWindow:
    def __init__(self, master, layout=(1, 1), title='Title Placeholder'):
        self.master = master

        # Title, layout and size of the window
        self.master.title(title)
        self.master.geometry('150x80')
        self.define_grid_layout(*layout)

    def define_grid_layout(self, rows, columns):
        # Define grid based on rows and columns
        for i in range(rows):
            self.master.grid_rowconfigure(i, weight=1)

        for i in range(columns):
            self.master.grid_columnconfigure(i, weight=1)

        # Create buttons in the grid cells with borders
        show_grid=False
        if show_grid:
            for row in range(rows):
                for col in range(columns):
                    # button_text = f"Row {row}, Col {col}"
                    button_text = ""
                    button = tk.Button(self.master, text=button_text, borderwidth=1, relief="solid")
                    button.grid(row=row, column=col, sticky="nsew")

    def add_button(self, text, row, column, func=None):
        # If no function passed, define a function which does nothing
        if not func:
            def func():
                pass

        button = tk.Button(self.master, text=text, command=func)
        button.grid(row=row, column=column)
        return button
    
    def add_text(self, text_messge, row, column):
        text = tk.Text(self.master, height=1, width=len(text_messge))
        text.grid(row=row,column=column)
        text.insert('1.0', text_messge)
        return text
    
    def add_label(self, text_messge, row, column, columnspan=1):
        label = tk.Label(self.master, text=text_messge)
        label.grid(row=row,column=column, columnspan=columnspan)
        return label
    
    def add_entry(self, row, column):
        entry = tk.Entry(self.master)
        entry.grid(row=row,column=column)
        return entry
    
    def add_dropdown(self, options, row, column):
        dropdown = ttk.Combobox(self.master, values=options)
        dropdown.grid(row=row, column=column)
        dropdown.set(options[0]) 
        return dropdown


class NewWindow(MainWindow):
    def __init__(self, master, layout=(1, 1), title='Title Placeholder'):
        self.master = tk.Toplevel(master)
        self.master.title(title)
        self.master.attributes('-topmost', True)
        self.define_grid_layout(*layout)

