import http.server
import os
import socketserver
import threading
import webbrowser
import tkinter as tk

# Define the directory containing your React app's build files
REACT_APP_DIR = "user_interface/data-dashboard/build"

# Define a global variable to store the server port
server_port = None
server_thread = None
httpd = None

# Define the initial directory
INITIAL_DIR = os.getcwd()

# HTTP server class
class ReactAppServer:
    def __init__(self):
        self.handler = http.server.SimpleHTTPRequestHandler

    def serve(self):
        global server_port, httpd
        try:
            os.chdir(REACT_APP_DIR)
        except FileNotFoundError:
            print(f"Error: Directory '{REACT_APP_DIR}' not found.")
            return

        with socketserver.TCPServer(("", 0), self.handler) as httpd:
            server_port = httpd.server_address[1]
            print(f"Serving React app at http://localhost:{server_port}")

            # Open the browser tab with the React app
            react_app_url = f"http://localhost:{server_port}"
            webbrowser.open_new_tab(react_app_url)

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Server stopped.")

    def stop(self):
        global httpd
        if httpd:
            httpd.shutdown()
            os.chdir(INITIAL_DIR)  # Change back to initial directory
            print("Server terminated.")
        else:
            print("Server is not running.")

# Start the server in a separate thread
def start_server():
    global server_thread
    server_thread = threading.Thread(target=server.serve)
    server_thread.daemon = True
    server_thread.start()

# Terminate the server
def stop_server():
    server.stop()

# Create Tkinter window
root = tk.Tk()
root.title("React App Server")

# Create an instance of the server class
server = ReactAppServer()

# Start server button
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.pack()

# Stop server button
stop_button = tk.Button(root, text="Stop Server", command=stop_server)
stop_button.pack()

# Run Tkinter event loop
root.mainloop()


