#!/usr/bin/env python
# coding: utf-8


#libreries
import PIL
from PIL import Image,ImageTk
#import pytesseract
import cv2
from tkinter import *
import subprocess
import os


# This form is writing all the time in the video


# initialize the video stream, pointer to output video file, and
# frame dimensions
vs = cv2.VideoCapture("0lHQ2f0d_3.avi")
writer = None #(I DID NOT WRITE THE OUTPUT IN THE DISK BECAUSE SPACE)
(W, H) = (None, None)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# loop over frames from the video file stream
while True:
    # read the next frame from the file
    (grabbed, frame) = vs.read()
    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed:
        break
    # if the frame dimensions are empty, grab them (WE CAN PUT IT IN LARGE LIKE THE BASIC)
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    output = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #predictions
    pred = H
    label = pred #aca habria que poner if 
    text = "activity: {}".format(label)
    color = (255, 0, 0)
    cv2.putText(output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
        1.25, color, 5)
    
    cv2.imshow("Output", output)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
        
# release the file pointers
print("[INFO] cleaning up...")
#writer.release()
vs.release()

