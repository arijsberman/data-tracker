from controller.app_controller import AppController

def main():

    app = AppController()
    app.get_last_update()
    app.run_in_background()
    app.open_home_page()
    

if __name__ == "__main__":
    main()
