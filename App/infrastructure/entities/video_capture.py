"""class VideoCapture"""

# Import required packages
import cv2
import pafy
import time
import threading

# Class for each sourced video
class VideoCapture:

    ## Initialisation
    def __init__(self, video_source=0, width=None, height=None, fps=None):
    
        """
        Initialise the class for each sourced video
        video_source: .mp4 file, 0 for webcam
        width: video pixels width
        height: video pixels height
        fps: video frames per second
        """

        ### Given characteristics for each video
        if video_source[:4] == "http":
            stream_source = pafy.new(video_source)
            video_stream = stream_source.getbest(preftype="mp4")
        self.video_source = video_stream.url if video_source[:4] == "http" else video_source
        self.width = width
        self.height = height
        self.fps = fps
        
        ### Open the video source
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("[VideoCapture] Unable to open video source", video_source)
        
        ### Get video width, height and fps, if not specified during the initialisation
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if not self.fps:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))

        ### Initial default values for vid.read()      
        self.ret = False #>ret is True if vid contains a video to work with
        self.frame = None #>the captured video itself
        self.current_frame = 1

        ### Start an independent thread for each sourced video
        self.running = True
        self.detecting = True
        self.detection = False
        self.thread = threading.Thread(target=self.process) #>target contains the func
                                                            #>that handles each thread
                                                            #>(func without parenthesis)
        self.thread.start()
        

    ## Function to be applied to each sourced video (independent thread)
    def process(self):

        """
        Process each video, once the thread for each source is running
        """

        ### Store vid.read() values while the video is running
        while self.running:

            start_at = time.time()

            ret, frame = self.vid.read()
            current_frame = int(self.vid.get(cv2.CAP_PROP_POS_FRAMES))
           
            ### If vid truly contains a video to work with, process size and colour
            if ret:
                frame = cv2.resize(frame, (self.width, self.height)) #>frame is the video
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #>frame is the video           

                #### Add alarm signboard
                if ((self.detecting) and
                    (self.video_source[:4] != 'data') and
                    (self.detection)):

                    signboard = 'Alarm: Violence Detected'
                    snap_time = time.strftime('%Y/%m/%d %H:%M:%S')
                    cv2.putText(frame, signboard, #>text
                                (15, 30), #>position
                                cv2.FONT_HERSHEY_DUPLEX, 0.85, #>font
                                (255, 0, 0), 1) #colour, thickness
                    cv2.putText(frame, snap_time, #>text
                                (15, 50), #>position
                                cv2.FONT_HERSHEY_DUPLEX, 0.55, #>font
                                (255, 0, 0), 1) #colour, thickness
                else:
                    pass

            ### Otherwise, break
            else:
                print('[VideoCapture] stream end:', self.video_source)
                self.running = False
                break
                
            ### Reassign the frame with the processed video
            self.ret = ret #>ret is True if vid contains a video to work with
            self.frame = frame #>the processed captured video itself
            self.current_frame = current_frame

            ### Sleep for next frame
            try:
                time.sleep((1 / self.fps) - (time.time() - start_at))

            except:
                continue

    ## Get a frame from the sourced video  
    def get_frame(self):

        """
        Return the frame from the sourced video
        ret: boolean, True if there is a video to work with
        frame: the captured video itself
        """

        return self.ret, self.frame

    def get_current_frame(self):

        return self.current_frame
    

    ## Release the video source when the object is destroyed
    def __del__(self):

        """
        Release the stream if destroyed
        """

        ### Stop thread
        if self.running:
            self.running = False
            self.thread.join() #>thread into a waiting state

        ### Release (close) the stream
        if self.vid.isOpened():
            self.vid.release()
            