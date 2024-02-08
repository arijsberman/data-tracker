from controller.app_controller import AppController

def main():

    app = AppController()
    # app.run_in_background()
    app.open_home_page()
    # app.run_data_collection()

if __name__ == "__main__":
    main()
