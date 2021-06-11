"""class CamerasSelection"""

# Import required packages
import json
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage

cameras_availability = "data_storage/user_inputs/cameras_availability.json"
user_selection_main = "data_storage/user_inputs/user_cameras_selection.json"
user_selection_default = "data_storage/user_inputs/cameras_default.json"

### Get available sources
names = []
with open(cameras_availability, 'r') as f:
    user_sel = json.load(f)
f.close()

class CamerasSelection:

    def __init__(self, cameras_selection, number):

        self.cameras_selection = cameras_selection
        self.cameras_selection.title("Violence Detection - Cameras Selection")

        self.frame = tk.Frame(self.cameras_selection)

        screen_width = self.cameras_selection.winfo_screenwidth()
        screen_height = self.cameras_selection.winfo_screenheight()
        width = 400
        height = 280
        x = screen_width / 2 - width / 2
        y = screen_height / 2 - height / 2

        self.cameras_selection.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.cameras_selection.resizable(0, 0)

        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ### List available cameras
        names = list(user_sel.keys())
        names.sort()

        ### Load home image
        v = Image.open('data_storage/icons/home.png')
        v = v.resize((40, 40), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)
        img = tk.Label(self.cameras_selection, 
                       image=render)
        img.image = render
        img.place(relx=0.1, rely=0.06)

        ### Title
        self.label = tk.Label(self.frame, 
                              text="Please select the locations\nto be monitored",
                              fg="#263942")
        self.label.configure(font='-size 12 -weight bold')
        self.label.place(relx=0.25, rely=0.07)

        ### Buttons
        self.button1 = tk.Button(self.frame, 
                                 text="Save Selection", 
                                 fg="#ffffff", 
                                 bg="#263942",
                                 command=self.save_selection)
        self.button1.place(relx=0.52, rely=0.82, height=31, width=120)
        self.button2 = tk.Button(self.frame, 
                                 text="Set Default", 
                                 bg="#ffffff", 
                                 fg="#263942",
                                 command=self.set_default)
        self.button2.place(relx=0.13, rely=0.82, height=31, width=120)

        ### Cameras labels
        self.label2 = tk.Label(self.frame, text="Camera one", fg="#263942")
        self.label2.configure(font='-size 12')
        self.label3 = tk.Label(self.frame, text="Camera two", fg="#263942")
        self.label3.configure(font='-size 12')
        self.label4 = tk.Label(self.frame, text="Camera three", fg="#263942")
        self.label4.configure(font='-size 12')
        self.label5 = tk.Label(self.frame, text="Camera four", fg="#263942")
        self.label5.configure(font='-size 12')
        self.label2.place(relx=0.1, rely=0.3, height=31)
        self.label3.place(relx=0.1, rely=0.42, height=31)
        self.label4.place(relx=0.1, rely=0.54, height=31)
        self.label5.place(relx=0.1, rely=0.66, height=31)
        
        ### Dropdown lists
        self.menuvar1 = tk.StringVar(self.frame)
        self.menuvar2 = tk.StringVar(self.frame)
        self.menuvar3 = tk.StringVar(self.frame)
        self.menuvar4 = tk.StringVar(self.frame)
        self.dropdown1 = tk.OptionMenu(self.frame, self.menuvar1, *names)
        self.dropdown2 = tk.OptionMenu(self.frame, self.menuvar2, *names)
        self.dropdown3 = tk.OptionMenu(self.frame, self.menuvar3, *names)
        self.dropdown4 = tk.OptionMenu(self.frame, self.menuvar4, *names)
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

    def set_default(self):

        with open(user_selection_default, 'r') as f:
            default = json.load(f)
        f.close()

        with open(user_selection_main, 'w') as f:
            json.dump(default, f, indent = 4)
        f.close()

        print("[DefaultCameras] set default cameras: successful")
        print("[DefaultCameras] camera one:", default["one"]["name"])
        print("[DefaultCameras] camera two:", default["two"]["name"]) 
        print("[DefaultCameras] camera three:", default["three"]["name"]) 
        print("[DefaultCameras] camera four:", default["four"]["name"])

        self.cameras_selection.master.deiconify()
        self.cameras_selection.destroy()

    def save_selection(self):

        with open(user_selection_default, 'r') as f:
            default = json.load(f)
        f.close()

        default["one"]["name"] = self.menuvar1.get()
        default["two"]["name"] = self.menuvar2.get()
        default["three"]["name"] = self.menuvar3.get()
        default["four"]["name"] = self.menuvar4.get()

        default["one"]["source"] = user_sel[self.menuvar1.get()]
        default["two"]["source"] = user_sel[self.menuvar2.get()]
        default["three"]["source"] = user_sel[self.menuvar3.get()]
        default["four"]["source"] = user_sel[self.menuvar4.get()]

        with open(user_selection_main, 'w') as f:
            json.dump(default, f, indent = 4)
        f.close()

        print("[SelectCameras] save cameras selection: successful")
        print("[SelectCameras] camera one:", default["one"]["name"])
        print("[SelectCameras] camera two:", default["two"]["name"]) 
        print("[SelectCameras] camera three:", default["three"]["name"]) 
        print("[SelectCameras] camera four:", default["four"]["name"])

        self.cameras_selection.master.deiconify()
        self.cameras_selection.destroy()
    