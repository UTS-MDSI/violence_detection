"""class ResetPassword"""

# Import required packages
import tkinter as tk
from PIL import Image, ImageTk

class ResetPassword(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        v = Image.open('data/icons/home.png')
        v = v.resize((40, 40), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(relx=0.1, rely=0.06)
        label = tk.Label(self, text="Please provide your email\nto get a new password",fg="#263942")
        label.configure(font='-size 12 -weight bold')
        label.place(relx=0.25, rely=0.07)
 

        # Email label
        self.label_email = tk.Label(self, text="Email", fg="#263942")
        self.label_email.place(relx=0.05, rely=0.33, height=31)
        self.label_email.configure(font='-size 12')

        # Email entry
        self.emailS = tk.StringVar()
        self.entry_email = tk.Entry(self, relie = tk.FLAT, textvariable = self.emailS)
        self.entry_email.place(relx=0.5, rely=0.34, height=25, width=170)

        # Recover button
        self.button_recover = tk.Button(self, text = 'Request Password',
                                        fg="#ffffff", bg="#263942",
                                        command = self.recover)
        self.button_recover.place(relx=0.52, rely=0.81, height=31, width=142)

        # Return to login button
        self.button_back = tk.Button(self, text = 'Back to Login',
                                      bg="#ffffff", fg="#263942", command = self.back)
        self.button_back.place(relx=0.1, rely=0.81, height=31, width=142)

        # Outcome label
        self.label_outcome = tk.Label(self, fg="#263942",
                                    text = '')
        self.label_outcome.config(font="-size 10")
        self.label_outcome.place(relx=0.23, rely=0.48)
    
    def recover(self):
        msg = "Request received\n\nIf the email is in our system,\nwe will send you a new password"
        self.clear_page()
        self.label_outcome.config(text = msg)

    def back(self):
        self.clear_page()
        self.controller.show_frame("Login")

    def clear_page(self):
        self.entry_email.delete(0, 'end')
        self.label_outcome.config(text = '')
