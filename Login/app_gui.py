import tkinter as tk
from database import validate_credentials, register_new
from tkinter import font as tkfont
import re

class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Font
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        # Size
        self.geometry("600x450+980+330")
        self.minsize(300, 225)
        self.maxsize(1200, 900)
        self.resizable(1,  1)
        #self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Creating the container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Setup, Registration, ForgotPass, VideoScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        #Login label
        self.label_login = tk.Label(self, text="Log In")
        self.label_login.place(relx=0.117, rely=0.178, height=21, width=104)
        #self.label_login.configure(background="#d9d9d9")

        #User label
        self.label_user = tk.Label(self, text="User ID")
        self.label_user.place(relx=0.183, rely=0.244, height=21, width=54)
        #self.label_user.configure(background="#d9d9d9")

        #User entry
        self.usernameS = tk.StringVar()
        self.entry_user = tk.Entry(self, relie = tk.FLAT, textvariable = self.usernameS)
        self.entry_user.place(relx=0.183, rely=0.311, height=30, relwidth=0.44)

        #Password label
        self.label_pass = tk.Label(self, text="Password")
        self.label_pass.place(relx=0.183, rely=0.422, height=21, width=64)
        #self.label_pass.configure(background="#d9d9d9")

        #Password entry
        self.passwordS = tk.StringVar()
        self.entry_pass = tk.Entry(self, show = "*", 
                            relie = tk.FLAT, textvariable = self.passwordS)
        self.entry_pass.place(relx=0.183, rely=0.511, height=30, relwidth=0.44)

        #Login button
        self.button_login = tk.Button(self, text = 'Log In', pady = 5,
                                    padx = 20, command = self.validate)
        self.button_login.place(relx=0.183, rely=0.644, height=24, width=47)

        # Forgot password
        self.label_forgot = tk.Label(self, text = 'Forgot password?')
        self.label_forgot.place(relx=0.45, rely=0.644, height=21, width=104)
        #self.label_forgot.configure(background="#d9d9d9")
        self.label_forgot.bind("<Enter>",blue_text)
        self.label_forgot.bind("<Leave>",black_text)
        self.label_forgot.bind("<Button-1>",self.forgot_password)

        # Request access
        self.label_access = tk.Label(self, text = 'Not registered? request access here')
        self.label_access.place(relx=0.633, rely=0.933, height=21, width=204)
        #self.label_access.configure(background="#d9d9d9")
        self.label_access.bind("<Enter>",blue_text)
        self.label_access.bind("<Leave>",black_text)
        self.label_access.bind("<Button-1>",self.request_access)

        # Outcome login
        self.label_outcome =  tk.Label(self, text = '')
        self.label_outcome.place(relx=0.117, rely=0.733, height=31, width=334)
        #self.label_outcome.configure(background="#d9d9d9")
        self.label_outcome.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.label_outcome.configure(foreground="#ff0000")
        

    def validate(self):
        # Restart outcome
        self.label_outcome.config(text='')
        # Validate user and password
        msg, outcome = validate_credentials(self.usernameS.get(), self.passwordS.get())
        self.label_outcome.config(text=msg)
        if outcome:
            self.clear_page()
            self.controller.show_frame("Setup")
        else:
            pass

    def forgot_password(self, event):
        event.widget.config(font = '-family {Segoe UI} -size 9 -weight bold')
        self.clear_page()
        self.controller.show_frame("ForgotPass")

    def request_access(self, event):
        event.widget.config(font = '-family {Segoe UI} -size 9 -weight bold')
        self.clear_page()
        self.controller.show_frame("Registration")
    
    def clear_page(self):
        self.entry_pass.delete(0, 'end')
        self.label_outcome.config(text = '')


class Setup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Setup", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("Login"))
        button.pack()

class Registration(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Registration label
        self.label_registration = tk.Label(self, text="Registration form")
        self.label_registration.place(relx=0.133, rely=0.111, height=21, width=144)
        #self.label_registration.configure(background="#d9d9d9")

        #User ID label
        self.label_user = tk.Label(self, text="User ID")
        self.label_user.place(relx=0.2, rely=0.289, height=21, width=54)
        #self.label_user.configure(background="#d9d9d9")

        #User entry
        self.usernameS = tk.StringVar()
        self.entry_user = tk.Entry(self, relie = tk.FLAT, textvariable = self.usernameS)
        self.entry_user.place(relx=0.35, rely=0.267, height=30, relwidth=0.373)

        #Email label
        self.label_email = tk.Label(self, text="Email")
        self.label_email.place(relx=0.2, rely=0.4, height=21, width=54)
        #self.label_login.configure(background="#d9d9d9")

        #Email entry
        self.emailS = tk.StringVar()
        self.entry_email = tk.Entry(self, relie = tk.FLAT, textvariable = self.emailS)
        self.entry_email.place(relx=0.35, rely=0.378, height=30, relwidth=0.373)

        #Password label
        self.label_pass1 = tk.Label(self, text="Password")
        self.label_pass1.place(relx=0.167, rely=0.511, height=21, width=94)
        #self.label_login.configure(background="#d9d9d9")

        #Password entry
        self.password1S = tk.StringVar()
        self.entry_pass1 = tk.Entry(self, show = "*", 
                            relie = tk.FLAT, textvariable = self.password1S)
        self.entry_pass1.place(relx=0.35, rely=0.489, height=30, relwidth=0.373)

        #Repeat password label
        self.label_pass2 = tk.Label(self, text="Repeat password")
        self.label_pass2.place(relx=0.15, rely=0.6, height=31, width=114)
        #self.label_login.configure(background="#d9d9d9")

        #Repeat password entry
        self.password2S = tk.StringVar()
        self.entry_pass2 = tk.Entry(self, show = "*", 
                            relie = tk.FLAT, textvariable = self.password2S)
        self.entry_pass2.place(relx=0.35, rely=0.6, height=30, relwidth=0.373)

        #Register button
        self.button_register = tk.Button(self, text = 'Register', pady = 5,
                                    padx = 20, command = self.register)
        self.button_register.place(relx=0.3, rely=0.8, height=34, width=127)

        #Return to login button
        self.button_back = tk.Button(self, text = 'Back to login', pady = 5,
                                    padx = 20, command = self.back)
        self.button_back.place(relx=0.533, rely=0.8, height=34, width=127)

        #Outcome registration
        self.label_outcome =  tk.Label(self, text = '')
        self.label_outcome.place(relx=0.333, rely=0.689, height=21, width=244)
        #self.label_outcome.configure(background="#d9d9d9")
        self.label_outcome.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.label_outcome.configure(foreground="#ff0000")

    def validate_user(self):
        if self.usernameS.get() == '':
            return False
        else:
            return True

    def validate_email(self):
        if not re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', self.emailS.get()):
            return False
        else:
            return True

    def validate_password_format(self):
        if len(self.password1S.get())<8:
            return False
        else:
            return True

    def validate_password_match(self):
        if self.password1S.get() != self.password2S.get():
            return False
        else:
            return True

    def validate_inputs(self):
        if not self.validate_user():
            msg = 'Please provide a username'
            outcome = False
        elif not self.validate_email():
            msg = 'Please provide a valid email'
            outcome = False
        elif not self.validate_password_match():
            msg = 'Passwords do not match'
            outcome = False
        elif not self.validate_password_format():
            msg = 'Password do not follow the require format'
            outcome = False
        else:
            msg = ''
            outcome = True
        
        return msg, outcome

    def register(self):
        # Restart outcome
        self.label_outcome.config(text='')
        
        #Validate inputs
        msg, outcome = self.validate_inputs()
        if not outcome:
            self.label_outcome.config(text=msg)
            self.entry_pass1.delete(0, 'end')
            self.entry_pass2.delete(0, 'end')
        else:
            msg, outcome = register_new(self.usernameS.get(), self.emailS.get(), self.password1S.get())
            self.clear_page()
            self.label_outcome.config(text=msg)

    def back(self):
        self.clear_page()
        self.controller.show_frame("Login")

    def clear_page(self):
        self.entry_user.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_pass1.delete(0, 'end')
        self.entry_pass2.delete(0, 'end')
        self.label_outcome.config(text = '')

class ForgotPass(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Recover password label
        self.label_recover = tk.Label(self, text="Recover password")
        self.label_recover.place(relx=0.15, rely=0.156, height=31, width=154)
        #self.label_login.configure(background="#d9d9d9")

        # Email label
        self.label_email = tk.Label(self, text="email")
        self.label_email.place(relx=0.2, rely=0.267, height=21, width=64)

        # Email entry
        self.emailS = tk.StringVar()
        self.entry_email = tk.Entry(self, relie = tk.FLAT, textvariable = self.emailS)
        self.entry_email.place(relx=0.317, rely=0.267, height=20, relwidth=0.373)

        # Recover button
        self.button_recover = tk.Button(self, text = 'Request password', pady = 5,
                                    padx = 20, command = self.recover)
        self.button_recover.place(relx=0.2, rely=0.556, height=34, width=127)

        # Return to login button
        self.button_back = tk.Button(self, text = 'Back to login', pady = 5,
                                    padx = 20, command = self.back)
        self.button_back.place(relx=0.533, rely=0.556, height=34, width=127)

        # Outcome label
        self.label_outcome = tk.Label(self,
                                    text = '')
        self.label_outcome.place(relx=0.333, rely=0.4, height=41, width=184)
    
    def recover(self):
        msg = "Request received \n If the email is in our systems \n we will send you a new password"
        self.clear_page()
        self.label_outcome.config(text = msg)

    def back(self):
        self.clear_page()
        self.controller.show_frame("Login")

    def clear_page(self):
        self.entry_email.delete(0, 'end')
        self.label_outcome.config(text = '')

class VideoScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the videoscreen", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("Login"))
        button.pack()



# General Labels events
######################################
#https://stackoverflow.com/questions/48212417/can-i-make-labels-clickable-in-tkinter-and-get-the-value-of-label-clicked
#https://stackoverflow.com/questions/34926901/python-tkinter-clickable-text
def blue_text(event):
    event.widget.config(fg = 'blue')

def black_text(event):
    event.widget.config(fg = 'black', font = '-family {Segoe UI} -size 9')
######################################


if __name__ == "__main__":
    app = MainUI()
    app.mainloop()