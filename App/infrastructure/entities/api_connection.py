"""class APIConnection"""

# Import required packages
import time
import json
import threading
import requests

api_url = "http://34.127.43.192:5000/ViolenceDetection/CurrentDetection"
api_url_put = "http://34.127.43.192:5000/ViolenceDetection/UpdateFrame"

# Class for each sourced video
class APIConnection:

    ## Initialisation
    def __init__(self, video_source, vid, detecting):      

        self.detection = False
        self.video_source = video_source
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
                    requests.put(f"{api_url_put}/{current_frame}")
                    print("[UpdateFrame] frame:", current_frame)  
                    response = requests.get(api_url)
                    self.detection = json.loads(response.text)["Violence?"]
                    print("[GetDetection] detection:", self.video_source, self.detection)    

            ### Otherwise, break
            else:
                break
        
            ### Sleep for next request
            time.sleep(1)
