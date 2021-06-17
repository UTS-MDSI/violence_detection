"""class Login"""

import tkinter as tk
from PIL import Image, ImageTk

from infrastructure.windows.monitor import Monitor
from infrastructure.windows.new_user import NewUser
from infrastructure.windows.cameras_selection import CamerasSelection
from infrastructure.windows.reset_password import ResetPassword
from infrastructure.windows.quit_confirmation import QuitConfirmation

from infrastructure.entities.database_records import validate_credentials


def blue_text(event):
    event.widget.config(fg = 'blue', font = '-size 8')

def black_text(event):
    event.widget.config(fg = '#263942', font = '-size 8')

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

        self.login.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.login.resizable(0, 0)

        self.frame = tk.Frame(self.login)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ### Load home image
        v = Image.open('data_storage/icons/home.png')
        v = v.resize((300, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)

        ### Image
        img = tk.Label(self.login,
                       image=render)
        img.image = render
        img.place(relx=0.55, rely=0.2)

        ## Main label
        self.label_main = tk.Label(self.frame, 
                                   text='Violence Detection', 
                                   fg='#263942')
        self.label_main.place(relx=0.05, rely=0.07)
        self.label_main.configure(font='-size 24 -weight bold')

        ### Login label
        self.label_login = tk.Label(self.frame,
                                    text='Login',
                                    fg='#263942')
        self.label_login.place(relx=0.05, rely=0.23, height=21)
        self.label_login.configure(font='-size 14')

        ### User label
        self.label_user = tk.Label(self.frame,
                                   text='User ID', 
                                   fg='#263942')
        self.label_user.place(relx=0.075, rely=0.3, height=31)
        self.label_user.configure(font='-size 12')

        ### User entry
        self.usernames = tk.StringVar()
        self.entry_user = tk.Entry(self.frame, 
                                   relie=tk.FLAT, 
                                   textvariable=self.usernames)
        self.entry_user.place(relx=0.075, rely=0.37, height=31, width=250)

        ### Password label
        self.label_pass = tk.Label(self.frame,
                                   text='Password', 
                                   fg='#263942')
        self.label_pass.place(relx=0.075, rely=0.49, height=31)
        self.label_pass.configure(font='-size 12')

        ### Password entry
        self.passwords = tk.StringVar()
        self.entry_pass = tk.Entry(self.frame, 
                                   show='*', 
                                   relie=tk.FLAT, 
                                   textvariable=self.passwords)
        self.entry_pass.place(relx=0.075, rely=0.56, height=31, width=250)

        ### Cameras button
        self.cameras = tk.Button(self.frame, 
                                      text = 'Select Cameras',
                                      fg='#ffffff', 
                                      bg='#263942',
                                      command= lambda: self.new_window(CamerasSelection, 
                                                                       "CamerasSelection"))
        self.cameras.place(relx=0.075, rely=0.69, height=31, width=120)

        ### Login button
        self.button_login = tk.Button(self.frame, 
                                      text = 'Start Detecting',
                                      fg='#ffffff', 
                                      bg='#263942',
                                      command=self.verify_user)
        self.button_login.place(relx=0.236, rely=0.69, height=31, width=120)

        ### Quit button
        self.quit = tk.Button(self.frame, 
                              text = 'Safe Quit',
                              fg='#263942', 
                              bg='#ffffff',
                              command=lambda: self.new_window(QuitConfirmation,
                                                              "QuitConfirmation"))
        self.quit.place(relx=0.837, rely=0.917, height=31, width=120)

        ### Forgot password button
        self.label_forgot = tk.Label(self.frame,
                                     text='Forgot password?',
                                     fg='#263942')
        self.label_forgot.configure(font='-size 8')
        self.label_forgot.place(relx=0.075, rely=0.63)
        self.label_forgot.bind("<Enter>", blue_text)
        self.label_forgot.bind("<Leave>", black_text)
        self.label_forgot.bind('<Button-1>', 
                               lambda event: self.new_window(ResetPassword, 
                                                             "ResetPassword"))
        
        ### Request access button
        self.label_access = tk.Label(self.frame,
                                     text = 'Not registered? Request access here', 
                                     fg='#263942')
        self.label_access.place(relx=0.075, rely=0.44)
        self.label_access.configure(font='-size 8')
        self.label_access.bind("<Enter>", blue_text)
        self.label_access.bind("<Leave>", black_text)
        self.label_access.bind("<Button-1>", 
                               lambda event: self.new_window(NewUser, 
                                                             "NewUser"))

        ### Company label
        self.clabel = tk.Label(self.frame,
                               text='Fight Fighters Inc.',
                               fg='#263942')
        self.clabel.configure(font='-size 11')
        self.clabel.place(relx=0.01, rely=0.933)

        ### User outcome
        self.label_outcome = tk.Label(self.frame, 
                                      text = '')
        self.label_outcome.place(relx=0.075, rely=0.775)
        self.label_outcome.configure(font="-size 9 -weight bold")

    def new_window(self, _class, number):
        self.new = tk.Toplevel(self.login)
        self.login.withdraw()
        _class(self.new, number)

    def verify_user(self):
        # Restart outcome
        self.label_outcome.config(text='', fg="#263942")
        # Validate user and password
        msg, outcome = validate_credentials(self.usernames.get(), self.passwords.get())
        self.label_outcome.config(text=msg)
        if outcome:
            self.new_window(Monitor, "Monitor")
        else:
            pass