"""class VideoSignboard"""

# Import required packages
import time
import json
import threading
import requests

api_url = "http://34.127.43.192:5000/ViolenceDetection/CurrentDetection"
api_url_put = "http://34.127.43.192:5000/ViolenceDetection/UpdateFrame"

# Class for each sourced video
class VideoSignboard:

    ## Initialisation
    def __init__(self, video_source, vid, video_running=False):      

        self.detection = False
        self.video_running = video_running
        self.video_source = video_source
        self.vid = vid
        self.thread = threading.Thread(target=self.get_detection)
        self.thread.start()

    def get_detection(self):

        while self.video_running:

            if self.video_source[:4] == "http":
                current_frame = self.vid.get_current_frame()
                requests.put(f"{api_url_put}/{current_frame}")
                print("[UpdateFrame] Frame", current_frame)  
                response = requests.get(api_url)
                self.detection = json.loads(response.text)["Violence?"]
                print("[VideoSignboard] Detection", self.video_source, self.detection)    

            ### Otherwise, break
            else:
                break
        
            ### Sleep for next request
            time.sleep(1)
