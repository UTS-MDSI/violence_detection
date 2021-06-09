"""class VideoFrame"""

# Import required packages
from threading import current_thread
import time
import tkinter as tk
import PIL.Image, PIL.ImageTk

# Import classes
from infrastructure.entities.video_capture import VideoCapture
from infrastructure.entities.video_signboard import VideoSignboard

# Class for each tkinter frame in the window grid
class VideoFrame(tk.Frame):


    ## Initialisation
    def __init__(self, window, name="", video_source=0, width=None, height=None):

        """
        Initialise the tkinter frame for each video in the grid
        window: window to be used
        name: text on top the frame
        video_source: video source
        width: video width
        height: video height
        """

        super().__init__(window)
        
        ### Given characteristics for the frame
        self.window = window
        self.name = name
        self.video_source = video_source

        ### Default stream state set to running while window is open
        self.running = True

        ### Default detection set to false
        self.detecting = False

        ### Load VideoCapture with an independent thread for each sourced video
        self.vid = VideoCapture(self.video_source,
                                width, 
                                height)

        ### Load violence detection response from API
        self.api = VideoSignboard(self.video_source,  self.vid,
                                  self.vid.running)

        ### Camera name label
        text_detecting = "Detections On" if self.detecting else "Detections Off"
        self.label = tk.Label(self, text=name, fg='#263942')
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
        self.btn_stop.pack(anchor='center', side='left', padx=2, pady=3)
        
        #### Logs button
        self.btn_logs = tk.Button(self, text='Save Logs', 
                                  bg='#263942', fg='#ffffff',
                                  command=self.snapshot) #>command contains the 
                                                         #> func to be run
                                                         #> by this button 
        self.btn_logs.pack(anchor='center', side='right', padx=2, pady=3)

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
        
        ### Start running videos
        self.update_frame()


    ## Function assigned to the start detection button
    def start(self):

        """
        Set detecting to True, so the App receives violence
        predictions and displays the alarm signboard
        """

        if not self.detecting:
            self.detecting = True

    ## Function assigned to the stop detection button
    def stop(self):

        """
        Set detecting to False, so the App no longer receives
        violence predictions nor displays the alarm signboard
        """

        if self.detecting:
           self.detecting = False
    

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
        detection = self.api.detection

        if ret: #>ret is True if vid truly contains a video to work with

            signboard = 'Alarm: Violence Detected'
            snap_time = time.strftime('%d/%m/%Y %H:%M:%S')

            self.image = PIL.Image.fromarray(frame) #>the captured frame itself
            self.photo = PIL.ImageTk.PhotoImage(image=self.image) #>make compatible
            self.canvas.create_image(0, 0, #>position to show the image
                                     image=self.photo, #>PhotoImage object
                                     anchor='nw') #>northwest alignment

            if detection:
                self.canvas.create_text(183, 20, #>position to show the text
                                        fill="red",font="Helvetica 20 bold",
                                        text=signboard)
                self.canvas.create_text(123, 40, #>position to show the text
                                        fill="red",font="Helvetica 16 bold",
                                        text=snap_time)
        
        ### While the App keeps running, loop over the function update_frame
        ### That is, once finished running update_frame, the next function to be run
        ### is that same update_frame, until the App stops
        if self.running:
            self.window.after(self.delay, self.update_frame)
            