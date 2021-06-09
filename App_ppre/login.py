"""class Login"""

# Import required packages
import tkinter as tk
from PIL import Image, ImageTk

# Import internal functions
from database_records import validate_credentials


def blue_text(event):
    event.widget.config(fg = 'blue')

def black_text(event):
    event.widget.config(fg = '#263942', font = '-size 9')

# Class for Login window
class Login(tk.Frame):


    ## Initialisation
    def __init__(self, parent, controller):
        
        ### Given attributes 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ### Load home image
        v = Image.open('data/icons/home.png')
        v = v.resize((300, 300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)

        ### Image
        img = tk.Label(self,
                       image=render)
        img.image = render
        img.place(relx=0.55, rely=0.2)

        ## Main label
        self.label_main = tk.Label(self, 
                                   text='Violence Detection', 
                                   fg='#263942')
        self.label_main.place(relx=0.05, rely=0.07)
        self.label_main.configure(font='-size 24 -weight bold')

        ### Login label
        self.label_login = tk.Label(self,
                                    text='Login',
                                    fg='#263942')
        self.label_login.place(relx=0.05, rely=0.23, height=21)
        self.label_login.configure(font='-size 14')

        ### User label
        self.label_user = tk.Label(self,
                                   text='User ID', 
                                   fg='#263942')
        self.label_user.place(relx=0.075, rely=0.3, height=31)
        self.label_user.configure(font='-size 12')

        ### User entry
        self.usernameS = tk.StringVar()
        self.entry_user = tk.Entry(self, 
                                   relie=tk.FLAT, 
                                   textvariable=self.usernameS)
        self.entry_user.place(relx=0.075, rely=0.37, height=31, width=250)

        ### Password label
        self.label_pass = tk.Label(self,
                                   text='Password', 
                                   fg='#263942')
        self.label_pass.place(relx=0.075, rely=0.45, height=31)
        self.label_pass.configure(font='-size 12')

        ### Password entry
        self.passwordS = tk.StringVar()
        self.entry_pass = tk.Entry(self, 
                                   show='*', 
                                   relie=tk.FLAT, 
                                   textvariable=self.passwordS)
        self.entry_pass.place(relx=0.075, rely=0.52, height=31, width=250)

        ### Login button
        self.button_login = tk.Button(self, 
                                      text='Start Detecting',
                                      fg='#ffffff', 
                                      bg='#263942',
                                      command=self.validate)
        self.button_login.place(relx=0.236, rely=0.66, height=31, width=120)

        ### Quit button
        self.button_login = tk.Button(self, 
                                      text='Quit the App',
                                      bg='#ffffff',
                                      fg='#263942',
                                      command=self.on_closing)
        self.button_login.place(relx=0.075, rely=0.66, height=31, width=120)

        ### Forgot password button
        self.label_forgot = tk.Label(self,
                                     text='Forgot password?',
                                     fg='#263942')
        self.label_forgot.configure(font='-size 9')
        self.label_forgot.place(relx=0.075, rely=0.59)
        self.label_forgot.bind("<Enter>", blue_text)
        self.label_forgot.bind("<Leave>", black_text)
        self.label_forgot.bind('<Button-1>', self.forgot_password)

        ### Request access button
        self.label_access = tk.Label(self,
                                     text = 'Not registered? Request access here', 
                                     fg='#263942')
        self.label_access.place(relx=0.708, rely=0.933, height=21, width=220)
        self.label_access.configure(font='-size 9')
        self.label_access.bind("<Enter>", blue_text)
        self.label_access.bind("<Leave>", black_text)
        self.label_access.bind("<Button-1>",self.request_access)

        ### Company label
        self.clabel = tk.Label(text='Fight Fighters Inc.',
                               fg='#263942')
        self.clabel.configure(font='-size 11')
        self.clabel.place(relx=0.01, rely=0.933)

        ### User outcome
        self.label_outcome = tk.Label(self, 
                                      text = '')
        self.label_outcome.place(relx=0.117, rely=0.733, height=31, width=334)
        self.label_outcome.configure(font="-size 9 -weight bold")

    
    ## Validation
    def validate(self):

        ### Restart user outcome
#        self.label_outcome.config(text='')

        ### Validate user and password
#        msg, outcome = validate_credentials(self.usernameS.get(), self.passwordS.get())
#        self.label_outcome.config(text=msg)

#        ### Move to cameras selection window if validated
#        if outcome:
#            self.clear_page()
#            self.controller.show_frame('CamerasSelection')
#        else:
#            pass

        self.clear_page()
        self.controller.show_frame('CamerasSelection')


    ## Redirect reset password
    def forgot_password(self, event):

        ### Move to reset password window
        event.widget.config(font = '-size 9 -weight bold')
        self.clear_page()
        self.controller.show_frame('ResetPassword')


    ## Redirect register
    def request_access(self, event):

        ### Move to new user window
        event.widget.config(font = '-size 9 -weight bold')
        self.clear_page()
        self.controller.show_frame('NewUser')


    ## Clear entries
    def clear_page(self):

        ### Clear all current entries
        self.entry_pass.delete(0, 'end')
        self.label_outcome.config(text = '')


    ## Redirect safe quit
    def on_closing(self):

        ### Move to quit confirmation window
        self.clear_page()
        self.controller.show_frame('QuitConfirmation')
