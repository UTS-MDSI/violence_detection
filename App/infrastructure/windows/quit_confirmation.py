"""class QuitConfirmation"""

# Import required packages
import tkinter as tk
from PIL import Image, ImageTk

class QuitConfirmation:

    def __init__(self, quit_confirmation, number):

        self.quit_confirmation = quit_confirmation
        self.quit_confirmation.title("Violence Detection - Quit")

        self.frame = tk.Frame(self.quit_confirmation)

        screen_width = self.quit_confirmation.winfo_screenwidth()
        screen_height = self.quit_confirmation.winfo_screenheight()
        width = 320
        height = 150
        x = screen_width / 2 - width / 2
        y = screen_height / 2 - height / 2

        self.quit_confirmation.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.quit_confirmation.resizable(0, 0)

        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        v = Image.open('data_storage/icons/home.png')
        v = v.resize((40, 40), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)
        img = tk.Label(self.quit_confirmation, 
                       image=render)
        img.image = render
        img.place(relx=0.15, rely=0.2)
        self.label = tk.Label(self.frame, 
                              text="Are you sure you\nwant to quit?",
                              fg="#263942")
        self.label.configure(font='-size 12 -weight bold')
        self.label.place(relx=0.35, rely=0.2)

        self.button_quit = tk.Button(self.frame,
                                     text="Confirm",
                                     fg="#ffffff",
                                     bg="#263942",
                                     command=self.on_closing)
        self.button_cancel  = tk.Button(self.frame, 
                                        text="Cancel", 
                                        bg="#ffffff", 
                                        fg="#263942",
                                        command=self.restore_window)
        self.button_quit.place(relx=0.53, rely=0.6, height=31, width=80)
        self.button_cancel.place(relx=0.23, rely=0.6, height=31, width=80)

        

    def on_closing(self):

        self.quit_confirmation.destroy()

    def restore_window(self):
        
        self.quit_confirmation.master.deiconify()
        self.quit_confirmation.destroy()