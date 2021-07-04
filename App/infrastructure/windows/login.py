"""class Login"""

import json
import requests
import tkinter as tk
from PIL import Image, ImageTk

from infrastructure.windows.monitor import Monitor
from infrastructure.windows.new_user import NewUser
from infrastructure.windows.cameras_selection import CamerasSelection
from infrastructure.windows.reset_password import ResetPassword
from infrastructure.windows.quit_confirmation import QuitConfirmation

from infrastructure.entities.database_records import validate_credentials

api_url_initialise = "/ViolenceDetection/Initialise"

def blue_text(event):
    event.widget.config(fg = "blue", font = "-size 8")

def black_text(event):
    event.widget.config(fg = "#263942", font = "-size 8")

class Login:
    
    def __init__(self, login):
        
        self.login = login
        self.login.title("Violence Detection - Login")

        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()
        width = 800
        height = 450
        x = screen_width / 2 - width / 2
        y = screen_height / 2 - height / 2

        self.login.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.login.resizable(0, 0)

        self.frame = tk.Frame(self.login)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ### Load home image
        v = Image.open("data_storage/icons/home.png")
        v = v.resize((300, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)

        ### Image
        img = tk.Label(self.login,
                       image=render)
        img.image = render
        img.place(relx=0.55, rely=0.2)

        ## Main label
        self.label_main = tk.Label(self.frame, 
                                   text="Violence Detection", 
                                   fg="#263942")
        self.label_main.place(relx=0.05, rely=0.07)
        self.label_main.configure(font="-size 24 -weight bold")

        ### Login label
        self.label_login = tk.Label(self.frame,
                                    text="Login",
                                    fg="#263942")
        self.label_login.place(relx=0.05, rely=0.23, height=21)
        self.label_login.configure(font="-size 14")

        ### User label
        self.label_user = tk.Label(self.frame,
                                   text="User ID", 
                                   fg="#263942")
        self.label_user.place(relx=0.075, rely=0.3, height=31)
        self.label_user.configure(font="-size 12")

        ### User entry
        self.usernames = tk.StringVar()
        self.entry_user = tk.Entry(self.frame, 
                                   relie=tk.FLAT, 
                                   textvariable=self.usernames)
        self.entry_user.place(relx=0.075, rely=0.37, height=31, width=250)

        ### Password label
        self.label_pass = tk.Label(self.frame,
                                   text="Password", 
                                   fg="#263942")
        self.label_pass.place(relx=0.075, rely=0.49, height=31)
        self.label_pass.configure(font="-size 12")

        ### Password entry
        self.passwords = tk.StringVar()
        self.entry_pass = tk.Entry(self.frame, 
                                   show="*", 
                                   relie=tk.FLAT, 
                                   textvariable=self.passwords)
        self.entry_pass.place(relx=0.075, rely=0.56, height=31, width=250)

        ### Cameras button
        self.cameras = tk.Button(self.frame, 
                                      text = "Select Cameras",
                                      fg="#ffffff", 
                                      bg="#263942",
                                      command= lambda: self.new_window(CamerasSelection, 
                                                                       "CamerasSelection"))
        self.cameras.place(relx=0.075, rely=0.69, height=31, width=120)

        ### Login button
        self.button_login = tk.Button(self.frame, 
                                      text = "Start Detecting",
                                      fg="#ffffff", 
                                      bg="#263942",
                                      command= lambda: self.start_detections())
                                     # command=self.verify_user)
        self.button_login.place(relx=0.236, rely=0.69, height=31, width=120)

        ### Quit button
        self.quit = tk.Button(self.frame, 
                              text = "Safe Quit",
                              fg="#263942", 
                              bg="#ffffff",
                              command=lambda: self.new_window(QuitConfirmation,
                                                              "QuitConfirmation"))
        self.quit.place(relx=0.837, rely=0.917, height=31, width=120)

        ### Forgot password button
        self.label_forgot = tk.Label(self.frame,
                                     text="Forgot password?",
                                     fg="#263942")
        self.label_forgot.configure(font="-size 8")
        self.label_forgot.place(relx=0.075, rely=0.63)
        self.label_forgot.bind("<Enter>", blue_text)
        self.label_forgot.bind("<Leave>", black_text)
        self.label_forgot.bind("<Button-1>", 
                               lambda event: self.new_window(ResetPassword, 
                                                             "ResetPassword"))
        
        ### Request access button
        self.label_access = tk.Label(self.frame,
                                     text = "Not registered? Request access here", 
                                     fg="#263942")
        self.label_access.place(relx=0.075, rely=0.44)
        self.label_access.configure(font="-size 8")
        self.label_access.bind("<Enter>", blue_text)
        self.label_access.bind("<Leave>", black_text)
        self.label_access.bind("<Button-1>", 
                               lambda event: self.new_window(NewUser, 
                                                             "NewUser"))

        ### Company label
        self.clabel = tk.Label(self.frame,
                               text="Fight Fighters Inc.",
                               fg="#263942")
        self.clabel.configure(font="-size 11")
        self.clabel.place(relx=0.01, rely=0.933)

        ### User outcome
        self.label_outcome = tk.Label(self.frame, 
                                      text = "")
        self.label_outcome.place(relx=0.075, rely=0.775)
        self.label_outcome.configure(font="-size 9 -weight bold")

    def new_window(self, _class, number):
        self.new = tk.Toplevel(self.login)
        self.login.withdraw()
        _class(self.new, number)

    def build_request(self, name, url, delay, frames, threshold):

        req = {
            "url": url,
            "delay": delay,
            "frames": frames,
            "threshold": threshold
        }

        print("[InitialiseAPI] successful initialisation: ", name)
        print(f"[InitialiseAPI] (url, delay, frames, threshold): {url, delay, frames, threshold}")

        return req

    def start_detections(self):
        
        with open("data_storage/user_inputs/user_cameras_selection.json", "r") as f:
            user_sel = json.load(f)
        f.close()
        
        sources = [
            (user_sel["one"]["name"], user_sel["one"]["url"], user_sel["one"]["ip"]), 
            (user_sel["two"]["name"], user_sel["two"]["url"], user_sel["two"]["ip"]), 
            (user_sel["three"]["name"], user_sel["three"]["url"], user_sel["three"]["ip"]),
            (user_sel["four"]["name"], user_sel["four"]["url"], user_sel["four"]["ip"]), 
        ]
        
        for key in user_sel.keys():

            if (user_sel[key]["url"][:4] == "http"):
                req = self.build_request(user_sel[key]["name"],
                                         user_sel[key]["url"],
                                         user_sel[key]["delay"],
                                         user_sel[key]["frames"],
                                         user_sel[key]["threshold"])
                ip = user_sel[key]["ip"]
                requests.Session().put(url=f"{ip}{api_url_initialise}", json=req)

        self.new = tk.Toplevel(self.login)
        self.login.withdraw()
        Monitor(self.new, "Monitor", sources)

    def verify_user(self):
        # Restart outcome
        self.label_outcome.config(text="", fg="#263942")
        # Validate user and password
        msg, outcome = validate_credentials(self.usernames.get(), self.passwords.get())
        self.label_outcome.config(text=msg)
        if outcome:
            self.start_detections()
        else:
            pass