from with_text_and_if import main_app
#from create_classifier import train_classifer
#from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from PIL import Image, ImageTk
import json
#from PIL import ImageTk, Image
#from gender_prediction import emotion,ageAndgender
names = set()

#creo que pgae three se puede sacarr

class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names

        names = []
        with open('user_cameras_selection.json', 'r') as f:
            user_sel = json.load(f)
            f.close()
            for number, item in user_sel.items():
                i = item["name"] #choose the names of the camara and not the source, [1] is the source
                names.append(i)

        #self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Violence Detection")
        self.resizable(False, False)
        self.geometry("400x280")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self, padx=5, pady=2)
        container.grid(sticky="s")
       # container.grid_rowconfigure([0,1,2,3], minsize=50)
        #container.grid_columnconfigure([0,1,2,3], minsize=50)

        self.frames = {}
        for F in (QuitConfirmation, StartPage, PageOne, PageTwo, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=0)
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class PageOne(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Page        ",fg="#263942")
            label.grid(row=0, sticky="ew")
         #   button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
          #  button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=lambda: self.controller.show_frame("StartPage"))
          #  button1.grid(row=1, column=0, ipady=3, ipadx=7)
           # button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)

class QuitConfirmation(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.pack(padx=20, pady=20)
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            v = Image.open('homepagepic.png')
            v = v.resize((40, 40), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(v)
            img = tk.Label(self, image=render)
            img.image = render
            img.place(relx=0.05, rely=0.1)
            label = tk.Label(self, text="Are you sure you\nwant to quit?",fg="#263942")
            label.configure(font='-size 12 -weight bold')
            label.place(relx=0.17, rely=0.1)
            button1 = tk.Button(self, text="Confirm Sources", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button1.place(relx=0.32, rely=0.95, height=31, width=120)
            button2.place(relx=0.1, rely=0.35, height=31, width=120)

        def on_closing(self):
            self.controller.destroy()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        self.grid(padx=50, pady=2)
   
        v = Image.open('homepagepic.png')
        v = v.resize((40, 40), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(v)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(relx=0.1, rely=0.06)
        label = tk.Label(self, text="Please select the locations\nto be monitored",fg="#263942")
        label.configure(font='-size 12 -weight bold')
        label.place(relx=0.25, rely=0.07)
        button1 = tk.Button(self, text="Confirm Sources", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Back to Login", bg="#ffffff", fg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
        #button1.pack(side='left', padx=5, pady=20)
        button1.place(relx=0.52, rely=0.87, height=31, width=130)
        button2.place(relx=0.1, rely=0.87, height=31, width=130)
        #button1.grid(padx=50, pady=50)
        label2 = tk.Label(self, text="Camera one", fg="#263942")#.grid(row=0, column=0, padx=10, pady=10)
        label2.configure(font='-size 12')
        label3 = tk.Label(self, text="Camera two", fg="#263942")#.grid(row=0, column=0, padx=10, pady=10)
        label3.configure(font='-size 12')
        label4 = tk.Label(self, text="Camera three", fg="#263942")#.grid(row=0, column=0, padx=10, pady=10)
        label4.configure(font='-size 12')
        label5 = tk.Label(self, text="Camera four", fg="#263942")#.grid(row=0, column=0, padx=10, pady=10)
        label5.configure(font='-size 12')
        label2.place(relx=0.05, rely=0.3, height=31)#, width=120)
        label3.place(relx=0.05, rely=0.42, height=31)#, width=120)
        label4.place(relx=0.05, rely=0.54, height=31)#, width=120)
        label5.place(relx=0.05, rely=0.66, height=31)#, width=120)
        #tk.Label(self, text="Select source", fg="#263942").grid(row=1, column=0, padx=10, pady=10)
        #tk.Label(self, text="Select source", fg="#263942").grid(row=2, column=0, padx=10, pady=10)
        #tk.Label(self, text="Select source", fg="#263942").grid(row=3, column=0, padx=10, pady=10)
        #self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
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
        #self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        #self.dropdown1.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        #self.dropdown2.grid(row=1, column=1, ipadx=8, padx=10, pady=10)
        #self.dropdown3.grid(row=2, column=1, ipadx=8, padx=10, pady=10)
        #self.dropdown4.grid(row=3, column=1, ipadx=8, padx=10, pady=10)
        #self.buttoncanc.grid(row=4, ipadx=5, ipady=4, column=0, pady=10)
        #self.buttonext.grid(row=4, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in self.names_cameras:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

# class PageThree(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
#         self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
#         self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
#         self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
#         self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
#         self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

#     def capimg(self):
#         self.numimglabel.config(text=str("Captured Images = 0 "))
#         messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
#         x = start_capture(self.controller.active_name)
#         self.controller.num_of_images = x
#         self.numimglabel.config(text=str("Number of images captured = "+str(x)))

#     def trainmodel(self):
#         if self.controller.num_of_images < 300:
#             messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
#             return
#         train_classifer(self.controller.active_name)
#         messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
#         self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Violence Detection", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Violence Detection", command=self.openwebcam, fg="#ffffff", bg="#263942")
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)
    #def gender_age_pred(self):
     #  ageAndgender()
    #def emot(self):
     #   emotion()



app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()