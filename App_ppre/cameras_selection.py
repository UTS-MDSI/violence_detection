"""class CamerasSelection"""

# Import required packages
import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from monitor import Monitor

class CamerasSelection(tk.Frame):

   ## def butnew(self, text, number, _class):
    #    tk.Button(self, text = text, command= lambda: self.new_window(number, _class))
        
    def new_window(self, number, _class):
        #self.new = tk.Toplevel(self.master)
        self.new = tk.Tk()
        _class(self.new, number)

    def trigger_monitor(self):
        Monitor(tk.Tk(), 'Violence Detection')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid(padx=50, pady=2)

        names = []
        with open('data/user_inputs/user_cameras_selection.json', 'r') as f:
            user_sel = json.load(f)
            f.close()
            for number, item in user_sel.items():
                i = item["name"]
                names.append(i)
   
        v = Image.open('data/icons/home.png')
        v = v.resize((40, 40), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(relx=0.1, rely=0.06)
        label = tk.Label(self, text="Please select the locations\nto be monitored",fg="#263942")
        label.configure(font='-size 12 -weight bold')
        label.place(relx=0.25, rely=0.07)
        #button1 = tk.Button(self, text="Confirm Sources", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("Monitor"))
        button1 = tk.Button(self, text="Confirm Sources", fg="#ffffff", bg="#263942", command= lambda: self.new_window("2", Monitor)).pack()
        #self.butnew("Confirm Sources", "2", Monitor)
        button2 = tk.Button(self, text="Back to Login", bg="#ffffff", fg="#263942",command=lambda: self.controller.show_frame("Login"))
        button1.place(relx=0.52, rely=0.87, height=31, width=130)
        button2.place(relx=0.1, rely=0.87, height=31, width=130)
        label2 = tk.Label(self, text="Camera one", fg="#263942")
        label2.configure(font='-size 12')
        label3 = tk.Label(self, text="Camera two", fg="#263942")
        label3.configure(font='-size 12')
        label4 = tk.Label(self, text="Camera three", fg="#263942")
        label4.configure(font='-size 12')
        label5 = tk.Label(self, text="Camera four", fg="#263942")
        label5.configure(font='-size 12')
        label2.place(relx=0.05, rely=0.3, height=31)
        label3.place(relx=0.05, rely=0.42, height=31)
        label4.place(relx=0.05, rely=0.54, height=31)
        label5.place(relx=0.05, rely=0.66, height=31)
        self.menuvar1 = tk.StringVar(self)
        self.menuvar2 = tk.StringVar(self)
        self.menuvar3 = tk.StringVar(self)
        self.menuvar4 = tk.StringVar(self)
        self.dropdown1 = tk.OptionMenu(self, self.menuvar1, *names)
        self.dropdown2 = tk.OptionMenu(self, self.menuvar2, *names)
        self.dropdown3 = tk.OptionMenu(self, self.menuvar3, *names)
        self.dropdown4 = tk.OptionMenu(self, self.menuvar4, *names)
        self.dropdown1.config(bg="white")
        self.dropdown2.config(bg="white")
        self.dropdown3.config(bg="white")
        self.dropdown4.config(bg="white")
        self.dropdown1["menu"].config(bg="white")
        self.dropdown2["menu"].config(bg="white")
        self.dropdown3["menu"].config(bg="white")
        self.dropdown4["menu"].config(bg="white")
        self.dropdown1.place(relx=0.47, rely=0.3, height=31, width=170)
        self.dropdown2.place(relx=0.47, rely=0.42, height=31, width=170)
        self.dropdown3.place(relx=0.47, rely=0.54, height=31, width=170)
        self.dropdown4.place(relx=0.47, rely=0.66, height=31, width=170)
        
