"""class tkCamera"""

# Import required packages
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

# Import classes
from domain.entities.video_capture import VideoCapture

# Class for each tkinter frame in the window grid
class tkCamera(tk.Frame):


    ## Initialisation
    def __init__(self, window, text="", video_source=0, width=None, height=None):

        """
        Initialise the tkinter frame for each video in the grid
        window: window to be used
        text: text on top the frame
        video_source: video source
        width: video width
        height: video height
        """

        super().__init__(window)
        
        ### Given characteristics for the frame
        self.window = window
        self.name = text
        self.video_source = video_source

        ### Load VideoCapture with an independent thread for each sourced video
        self.vid = VideoCapture(self.video_source, width, height)   

        ### Camera name label
        self.label = tk.Label(self, text=text, fg='#263942')
        self.label.configure(font='-size 12 -weight bold')
        self.label.pack(pady=4) #>organises widgets in blocks prior placing
                                #>it in the parent widget

        ### Set height and width from each sourced video 
        self.canvas = tk.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack() #>organises widgets in blocks prior placing
                           #>it in the parent widget

        #### Start detection button
        self.btn_start = tk.Button(self, text='Start Detection', 
                                   bg='#263942', fg='#ffffff',
                                   command=self.start) #>command contains the func
                                                       #>to be run by this button
        self.btn_start.pack(anchor='center', side='left', pady=3)
        
        #### Stop detection button
        self.btn_stop = tk.Button(self, text='Stop Detection', 
                                  bg='#263942', fg='#ffffff',
                                  command=self.stop) #>command contains the func
                                                     #>to be run by this button 
        self.btn_stop.pack(anchor='center', side='left', padx=6, pady=3)
         
        #### Snapshot button
        self.btn_snapshot = tk.Button(self, text='Snapshot', 
                                      bg='#263942', fg='#ffffff',
                                      command=self.snapshot) #>command contains the 
                                                             #> func to be run
                                                             #> by this button 
        self.btn_snapshot.pack(anchor='center', side='right', pady=3)
         
        ### Add a time delay between frame updates
        self.delay = int(1000 / self.vid.fps)
        print('[tkCamera] source:', self.video_source)
        print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)
        
        ### Default snapshot image set to None
        self.image = None
        
        ### Default stream state set to running while window is open
        self.running = True
        self.update_frame()


    ## Function assigned to the start detection button
    def start(self):

        """
        Set detecting to True, so the App receives violence
        predictions and displays the alarm signboard
        """

        #TODO: not start video but start detection
        if not self.running:
            self.running = True
            self.update_frame()


    ## Function assigned to the stop detection button
    def stop(self):

        """
        Set detecting to False, so the App no longer receives
        violence predictions nor displays the alarm signboard
        """

        #TODO: not stop video but stop detection
        if self.running:
           self.running = False
    

    ## Function assigned to the snapshot button
    def snapshot(self):
        
        """
        Save current frame in widget named as per the current time
        """

        ### Set folder and file to save the snapshots
        folder_snap = 'data/snapshots/'
        file_snap = time.strftime(f'%Y.%m.%d %H.%M.%S {self.name}.jpg')

        ### Save current frame as .jpg image
        if self.image:
            self.image.save(folder_snap + file_snap)
            

    ## Update the frame from the video source each delay milliseconds
    def update_frame(self):
        
        """
        Update the videos in the window by calling the current stream frame
        """

        ### Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret: #>ret is True if vid truly contains a video to work with
            self.image = PIL.Image.fromarray(frame) #>the captured frame itself
            self.photo = PIL.ImageTk.PhotoImage(image=self.image) #>make compatible
            self.canvas.create_image(0, 0, #>position to show the image
                                     image=self.photo, #>PhotoImage object
                                     anchor='nw') #>northwest alignment
        
        ### While the App keeps running, loop over the function update_frame
        ### That is, once finished running update_frame, the next function to be run
        ### is that same update_frame, until the App stops
        if self.running:
            self.window.after(self.delay, self.update_frame)
            