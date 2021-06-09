"""class NewUser"""

# Import required packages
import re
import tkinter as tk
from PIL import Image, ImageTk


class NewUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid(padx=50, pady=2)

        v = Image.open('data/icons/home.png')
        v = v.resize((40, 40), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(relx=0.1, rely=0.06)
        label = tk.Label(self, text="Please enter your details\nto complete registration",fg="#263942")
        label.configure(font='-size 12 -weight bold')
        label.place(relx=0.25, rely=0.07)

        #User ID label
        self.label_user = tk.Label(self, text="User ID", fg="#263942")
        self.label_user.place(relx=0.05, rely=0.29, height=31)
        self.label_user.configure(font='-size 12')

        #User entry
        self.usernameS = tk.StringVar()
        self.entry_user = tk.Entry(self, relie = tk.FLAT, textvariable = self.usernameS)
        self.entry_user.place(relx=0.5, rely=0.3, height=25, width=170)

        #Email label
        self.label_email = tk.Label(self, text="Email", fg="#263942")
        self.label_email.place(relx=0.05, rely=0.41, height=31)
        self.label_email.configure(font='-size 12')
        #self.label_login.configure(background="#d9d9d9")

        #Email entry
        self.emailS = tk.StringVar()
        self.entry_email = tk.Entry(self, relie = tk.FLAT, textvariable = self.emailS)
        self.entry_email.place(relx=0.5, rely=0.42, height=25, width=170)

        #Password label
        self.label_pass1 = tk.Label(self, text="Password", fg="#263942")
        self.label_pass1.place(relx=0.05, rely=0.53, height=31)
        self.label_pass1.configure(font='-size 12')
        #self.label_login.configure(background="#d9d9d9")

        #Password entry
        self.password1S = tk.StringVar()
        self.entry_pass1 = tk.Entry(self, show = "*", 
                            relie = tk.FLAT, textvariable = self.password1S)
        self.entry_pass1.place(relx=0.5, rely=0.54, height=25, width=170)

        #Repeat password label
        self.label_pass2 = tk.Label(self, text="Confirm Password", fg="#263942")
        self.label_pass2.place(relx=0.05, rely=0.65, height=31)
        self.label_pass2.configure(font='-size 12')
        #self.label_login.configure(background="#d9d9d9")

        #Repeat password entry
        self.password2S = tk.StringVar()
        self.entry_pass2 = tk.Entry(self, show = "*", 
                            relie = tk.FLAT, textvariable = self.password2S)
        self.entry_pass2.place(relx=0.5, rely=0.66, height=25, width=170)

        #Register button
        self.button_register = tk.Button(self, text = 'Register', 
                                         fg="#ffffff", bg="#263942", command = self.register)
        self.button_register.place(relx=0.52, rely=0.83, height=31, width=130)

        #Return to login button
        self.button_back = tk.Button(self, text = 'Back to Login', 
                                    bg="#ffffff", fg="#263942", command = self.back)
        self.button_back.place(relx=0.1, rely=0.83, height=31, width=130)

        #Outcome registration
        self.label_outcome =  tk.Label(self, text = '')
        self.label_outcome.place(relx=0.333, rely=0.689)
        #self.label_outcome.configure(background="#d9d9d9")
        self.label_outcome.configure(font="-size 9 -weight bold")
       # self.label_outcome.configure(foreground="#ff0000")

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
            msg = 'Invalid password'
            outcome = False
        else:
            msg = ''
            outcome = True
        
        return msg, outcome

    def register(self):
        # Restart outcome
        self.label_outcome.config(text='', fg="#263942")
        self.label_outcome.config(font="-size 9")
        self.label_outcome.place(relx=0.5, rely=0.75)
        
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
