"""class VideoFrame"""

# Import required packages
import json
import time
import requests
import tkinter as tk
import PIL.Image, PIL.ImageTk

# Import classes
from infrastructure.entities.video_capture import VideoCapture
from infrastructure.entities.api_connection import APIConnection

api_url = "http://34.127.43.192:5000/ViolenceDetection/LogsDetections"

# Class for each tkinter frame in the window grid
class VideoFrame(tk.Frame):


    ## Initialisation
    def __init__(self, 
                 window,
                 name="",
                 video_source=0,
                 width=None,
                 height=None):

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

        ### Default detection set to "On"
        if self.video_source[:4] == "http":
            self.detecting = "Detections On"            
        else:
            self.detecting = "Blocked"

        ### Load VideoCapture with an independent thread for each sourced video
        self.vid = VideoCapture(self.video_source,
                                width, 
                                height)

        ### Load violence detection response from API
        self.api = APIConnection(self.video_source, 
                                 self.vid,
                                 self)

        ### Camera name label
        self.label = tk.Label(self, 
                              text=self.name + ": " + self.detecting, 
                              fg='#263942')
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
                                  command=self.logs) #>command contains the 
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
        if self.video_source[:4] == "http":
            self.detecting = "Detections On"
            print("[StartDetection] turn on:", self.detecting) 
        
        else:
            print("[StartDetection] blocked: only detections on YouTube videos allowed")

    ## Function assigned to the stop detection button
    def stop(self):

        """
        Set detecting to False, so the App no longer receives
        violence predictions nor displays the alarm signboard
        """

        if self.video_source[:4] == "http":
            self.detecting = "Detections Off"
            print("[StopDetection] turn off:", self.detecting) 
        
        else:
            print("[StopDetection] blocked: only detections on YouTube videos allowed")
    

    def is_detecting(self):

        return True if self.detecting == "Detections On" else False


    ## Function assigned to the snapshot button
    def snapshot(self):
        
        """
        Save current frame in widget named as per the current time
        """

        ### Set folder and file to save the snapshots
        folder_snap = 'data_storage/snapshots/'
        file_snap = time.strftime(f'%Y.%m.%d %H.%M.%S {self.name}.jpg')

        ### Save current frame as .jpg image
        if self.image:
            self.image.save(folder_snap + file_snap)
            print("[SaveSnapshot] saving: successful", self.name) 

    ## Function assigned to the logs button
    def logs(self):
        
        """
        Save session logs in widget named as per the current time
        """
        if self.video_source[:4] == "http":
            ### Set folder and file to save the snapshots
            folder_logs = 'data_storage/logs/'
            file_logs = time.strftime(f'%Y.%m.%d %H.%M.%S {self.name}.json')

            ### Get logs
            response = requests.get(api_url)
            logs = json.loads(response.text)

            ### Save logs
            with open(folder_logs + file_logs, 'w') as f:
                json.dump(logs, f, indent = 4)
            f.close()

            print("[SaveLogs] saving: successful", self.name) 

        else:
            print("[SaveLogs] blocked: only detections on YouTube videos allowed")
            

    ## Update the frame from the video source each delay milliseconds
    def update_frame(self):
        
        """
        Update the videos in the window by calling the current stream frame
        """

        ### Get a frame from the video source
        ret, frame = self.vid.get_frame()
        detection = self.api.detection

        self.label["text"] = self.name + ": " + self.detecting

        if ret: #>ret is True if vid truly contains a video to work with

            signboard = 'Alarm: Violence Detected'
            snap_time = time.strftime('%d/%m/%Y %H:%M:%S')

            self.image = PIL.Image.fromarray(frame) #>the captured frame itself
            self.photo = PIL.ImageTk.PhotoImage(image=self.image) #>make compatible
            self.canvas.create_image(0, 0, #>position to show the image
                                     image=self.photo, #>PhotoImage object
                                     anchor='nw') #>northwest alignment

            if detection and (self.detecting=="Detections On"):
                self.canvas.create_text(173, 25, #>position to show the text
                                        fill="red",font="Helvetica 20 bold",
                                        text=signboard)
                self.canvas.create_text(113, 45, #>position to show the text
                                        fill="red",font="Helvetica 16 bold",
                                        text=snap_time)
        
        ### While the App keeps running, loop over the function update_frame
        ### That is, once finished running update_frame, the next function to be run
        ### is that same update_frame, until the App stops
        if self.running:
            self.window.after(self.delay, self.update_frame)
            