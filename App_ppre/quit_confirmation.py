"""class QuitConfirmation"""

# Import required packages
import tkinter as tk
from tkinter import PhotoImage

class QuitConfirmation(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='data/icons/home.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="        Home Page        ",fg="#263942")
        label.grid(row=0, sticky="ew")
        button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=lambda: self.controller.show_frame("Login"))
        button3.grid(row=3, column=0, ipady=3, ipadx=32)