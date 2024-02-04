import tkinter as tk
from ui_components.main_window import MainWindow

def main():

    # Initializing the app
    root = tk.Tk()

    # Landing page
    home_page = MainWindow(root, layout=(2,2))
    home_page.add_button('Settings', 0, 0, home_page.open_settings_page)
    home_page.add_button('Collect Data', 0, 1, home_page.collect_data)
    home_page.add_label('Data collected today: yes', 1, 0, 2)

    # Running the app
    root.mainloop()

if __name__ == "__main__":
    main()
