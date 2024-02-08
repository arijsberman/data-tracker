import tkinter as tk

from controller.app_controller import AppController

def main():

    app = AppController()

    app.open_home_page()
    # app.run_data_collection()

if __name__ == "__main__":
    main()
