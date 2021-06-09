"""Main GUI"""

# Import required packages
import tkinter as tk

# Import classes
from login import Login 
from monitor import Monitor
from new_user import NewUser
from reset_password import ResetPassword
from cameras_selection import CamerasSelection
from quit_confirmation import QuitConfirmation


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Font
        self.title("Violence Detection")

        # Size
        self.geometry("800x450+980+330")
        self.minsize(300, 225)
        self.maxsize(1200, 900)
        self.resizable(1,  1)

        # Creating the container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login,
                  ResetPassword,
                  NewUser, 
                  QuitConfirmation,
                 # CamerasSelection
                 ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('Login')

    def show_frame(self, page_name):
        
        ### Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()
        

# Run the GUI App
if __name__ == '__main__': 

    ## Run the GUI App
    app = MainUI()
    app.mainloop()
