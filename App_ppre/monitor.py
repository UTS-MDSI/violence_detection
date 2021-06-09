"""GUI App - Windows Handler"""

# Import required packages
import json
import tkinter as tk
from tkinter import messagebox

# Import classes
from video_frame import tkCamera 

# Class for the 3rd window - GUI App
class Monitor:


    ## Initialisation
    def __init__(self, window, window_title):

        ## Load the sources selected by the user
        with open('data/user_inputs/user_cameras_selection.json', 'r') as f:
            user_sel = json.load(f)
        f.close()

        ## Set the sources
        sources = [
            (user_sel['one']['name'], user_sel['one']['source']), 
            (user_sel['two']['name'], user_sel['two']['source']), 
            (user_sel['three']['name'], user_sel['three']['source']), 
            (user_sel['four']['name'], user_sel['four']['source']), 
        ]

        ### Given characteristics for the window
        self.window = window
        self.window.title(window_title)
        #self.window.iconphoto(True, tk.PhotoImage(file='data/icons/icon.ico'))
        self.window.tk.eval('::msgcat::mclocale en') #> language

        ### Set window page automatically
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f'{screen_width}x{screen_height}')
        self.window.columnconfigure([0,1], minsize=screen_width/2.107)
        self.window.rowconfigure([0,1,2], minsize=screen_height/3)

        ### Initialise an empty list for each video
        self.vids = []

        ### Locate the sourced videos in the grid
        columns = 2
        for number, source in enumerate(sources):
            name, stream = source
            vid = tkCamera(
                           self.window, #>window to be used
                           name, #>text on top
                           stream, #>video source
                           int(screen_width/2.2), #>width
                           int(screen_height/3.1) #>height
                          )

            x = number % columns #>x position (% modulus)
            y = number // columns #>y position (// floor division)
            vid.grid(row=y, column=x, padx=8, pady=6) #>video position
            
            self.vids.append(vid) #>include the video in the grid

        ### Company label
        label = tk.Label(text='Fight Fighters Inc.', fg='#263942')
        label.configure(font='-size 11')
        label.grid(row=2, column=0, sticky='nw', padx=15, pady=15)

        ### Buttons shared size
        bheight = 31
        bwidth = 130
        bx = 0.945

        #### Quit button
        btn_quit = tk.Button(self.window, text='Quit the App', 
                             fg='#263942', bg='#ffffff',
                             command=self.on_closing) #>command contains the func
                                                      #>to be run by this button
        btn_quit.configure(font='-size 10')
        btn_quit.place(relx=0.891, rely=bx, height=bheight, width=bwidth)

        #### Back to login button TODO: back to login
        btn_backlogin = tk.Button(self.window, text='Back to Login', 
                                  fg='#263942', bg='#ffffff',
                                  command=self.on_closing) #>command contains the func
                                                           #>to be run by this button
        btn_backlogin.place(relx=0.786, rely=bx, height=bheight, width=bwidth)

        #### Back to cameras button TODO: back to cameras
        btn_backcameras = tk.Button(self.window, text='Switch Cameras',
                                    fg='#263942', bg='#ffffff',
                                    command=self.on_closing) #>command contains the func
                                                             #>to be run by this button
        btn_backcameras.place(relx=0.681, rely=bx, height=bheight, width=bwidth)                                                     

        ### Delete the window if user closes it
        self.window.protocol('WM_DELETE_WINDOW', #>to identify user closing
                             self.on_closing)  #>on_closing contains the func
                                               #>to be run if the user closes
                                               #>the window
                                               #>(func without parenthesis)

        ### Stop GUI infrastructure
        self.window.mainloop() #>blocks further execution of Python code
    

    ## Function to be applied if the user closes the window
    def on_closing(self):

        """
        Stop the threads and ask for confirmation to close the window
        """

        print('[App] stopping threads')
        for source in self.vids:
            source.vid.running = False #>stop thread, stop reading the video

        print('[App] exit')
        
        self.window.option_add('*Dialog.msg.font', 'Helvetica 12')
        self.window.destroy()
        