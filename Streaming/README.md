# Installation

## Windows 
Follow the instructions: https://www.youtube.com/watch?v=r1AtmY-RMyQ

### Setting environment variables
We need to add some protocols to the whitelist so we can use RTP with CV2.

* Go to *Edit the system environment variables* in the start menu
* In the tab *Advanced* click on *Environment Variables...*
* In *User variables* click on New
* On *Variable name* write *OPENCV_FFMPEG_CAPTURE_OPTIONS*
* On *Value* write *protocol_whitelist;file,rtp,udp*
* Click ok
* Repeat the same but this time in *System variables*

## Linux

```
sudo apt update
sudo apt install ffmpeg
```

### Setting environment variables
If you are using Linux you do not need to add the environment variables manually. You just need to add the following in your Python Script:

```python
import os
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'
```

# Stream a video

## From file
To stream a video from a file we are going to use the RTP protocol, which stream in real time with no posibility of adding controls (like RTSP). More information here https://www.kurento.org/blog/rtp-ii-streaming-ffmpeg

Use the following command:

```
ffmpeg -re -i [file_path] -an -c:v copy -f rtp -sdp_file [sdp_file_path] [IP and port]
```

Example:

```
ffmpeg -re -i sample.mp4 -an -c:v copy -f rtp -sdp_file video.sdp "rtp://127.0.0.1:5004"
```

Where:
* sample.mp4 is the path of the video file
* video.sdp is the path of the sdp file produced to stream the video
* "rtp://127.0.0.1:5004" is the localhost and port used to stream

## From camera connected to computer
We do not need to stream form cameras because we can easily open the video from CV2.

But if you want to do it please see the following page: http://4youngpadawans.com/stream-camera-video-and-audio-with-ffmpeg/

## Multiple streams
You just need to be careful with the ports. You can't stream two videos to the same port. I have had problems with some ports, so it is like a trial and error.

For two videos I did it with: 5004 and 5020

# Capturing stream with CV2
If you are using RTP with a sdp file, you can do the following:

```python
import cv2
# If our sdp file has the path 'video.sdp'
cap = cv2.VideoCapture('video.sdp')

#Check that is capturing
cap.isOpened()
```

If you want to use a integrated camera or usb device use the following:

```python
import cv2
# If our device is in the position 0
cap = cv2.VideoCapture(0)

#Check that is capturing
cap.isOpened()
```

## Linux Consideration
 If you want to capture a RTP stream with a sdp file and you haven't changed the environment variable, you need to do the following:
 
 ```python
import cv2
import os

# Adding environment variables
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'protocol_whitelist;file,rtp,udp'

# If our sdp file has the path 'video.sdp'
cap = cv2.VideoCapture('video.sdp')

#Check that is capturing
cap.isOpened()
```

# Run sample
The file *stream videos.txt* has the commands to stream the four sample videos in this folder. Then you can run *test.py* to visualise them. 

# Video Source
London snow: https://www.youtube.com/watch?v=kBh7lzKdfQk <br>
Street fight: https://www.youtube.com/watch?v=SHue83Rnvo4 <br>
Assault: https://www.youtube.com/watch?v=74w0vAKyBlo <br>
Krupowki-Srodek: https://imageserver.webcamera.pl/rec/krupowki-srodek/latest.mp4