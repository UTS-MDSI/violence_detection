"""class APIConnection"""

# Import required packages
import time
import threading
import requests

api_url_detect = "/ViolenceDetection/Predict"

# Class for each sourced video
class APIConnection:

    ## Initialisation
    def __init__(self, video_source, ip, vid, detecting):      

        self.detection = False
        self.video_source = video_source
        self.ip = ip
        self.vid = vid
        self.detecting = detecting
        self.thread = threading.Thread(target=self.api_connection)
        self.thread.start()

    def api_connection(self):

        while self.vid.running:

            if (self.video_source[:4] == "http"):
                detecting = self.detecting.is_detecting()

                if detecting:
                    current_frame = self.vid.get_current_frame()
                    response = requests.put(f"{self.ip}{api_url_detect}/{current_frame}")
                    print("[GenerateDetection] frame:", current_frame)
                    self.detection = True if response.text == "1" else False
                    print("[GenerateDetection] detection:", self.video_source, self.detection)    

            ### Otherwise, break
            else:
                break
        
            ### Sleep for next request
            time.sleep(1)
