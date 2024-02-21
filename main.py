from controller.app_controller import AppController
import ctypes

myappid = 'some.random.string.abcdefghijklmnopqrstuvwxyz' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():

    print('Starting app...')
    app = AppController()

    print('Getting last update from response data...')
    app.get_last_update()

    print('Starting background process...')
    app.run_in_background()

    print('Opening home page...')
    app.open_home_page()
    

if __name__ == "__main__":
    main()
