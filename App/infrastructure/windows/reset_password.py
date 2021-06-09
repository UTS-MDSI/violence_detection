"""class ResetPassword"""

# Import required packages
import tkinter as tk
from PIL import Image, ImageTk

class ResetPassword:

    def __init__(self, reset_password, number):

        self.reset_password = reset_password
        self.reset_password.title("Violence Detection - Reset Password")

        self.frame = tk.Frame(self.reset_password)

        screen_width = self.reset_password.winfo_screenwidth()
        screen_height = self.reset_password.winfo_screenheight()
        width = 400
        height = 280
        x = screen_width / 2 - width / 2
        y = screen_height / 2 - height / 2

        self.reset_password.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.reset_password.resizable(0, 0)

        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ### Load home image
        v = Image.open('data/icons/home.png')
        v = v.resize((40, 40), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)

        ### Image
        img = tk.Label(self.reset_password,
                       image=render)
        img.image = render
        img.place(relx=0.1, rely=0.06)
        self.label = tk.Label(self.frame, 
                              text="Please provide your email\nto get a new password",
                              fg="#263942")
        self.label.configure(font='-size 12 -weight bold')
        self.label.place(relx=0.25, rely=0.07)
 
        # Email label
        self.label_email = tk.Label(self.frame,
                                    text="Email", 
                                    fg="#263942")
        self.label_email.place(relx=0.05, rely=0.33, height=31)
        self.label_email.configure(font='-size 12')

        # Email entry
        self.emails = tk.StringVar()
        self.entry_email = tk.Entry(self.frame, 
                                    relie = tk.FLAT, 
                                    textvariable = self.emails)
        self.entry_email.place(relx=0.5, rely=0.34, height=25, width=170)

        # Recover button
        self.button_recover = tk.Button(self.frame,
                                        text = 'Request Password',
                                        fg="#ffffff", 
                                        bg="#263942",
                                        command = self.recover)
        self.button_recover.place(relx=0.52, rely=0.81, height=31, width=142)

        # Return to login button
        self.button_back = tk.Button(self.frame, 
                                     text = 'Back to Login',
                                     bg="#ffffff", 
                                     fg="#263942",
                                     command = self.restore_window)
        self.button_back.place(relx=0.1, rely=0.81, height=31, width=142)

        # Outcome label
        self.label_outcome = tk.Label(self.frame, 
                                      fg="#263942",
                                      text = '')
        self.label_outcome.config(font="-size 10")
        self.label_outcome.place(relx=0.23, rely=0.48)
    
    def recover(self):
        msg = "Request received\n\nIf the email is in our system,\nwe will send you a new password"
        self.clear_page()
        self.label_outcome.config(text = msg)

    def restore_window(self):
        self.reset_password.master.deiconify()
        self.reset_password.destroy()
		
    def clear_page(self):
        self.entry_email.delete(0, 'end')
        self.label_outcome.config(text = '')
