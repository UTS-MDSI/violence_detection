# Imports the required packages
import distutils
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify
import requests

# Packages for prediction
import cv2
import numpy as np
import pafy
import time
import tensorflow as tf
import math
import warnings
import json

# Tensorflow configuration
physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
config = tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Auxiliar functions
from prediction import *

# Parameters
model_path = 'weights_fusioni3d.hdf5'

## Initialise Flask
app = Flask(__name__)

# Initialise variables for prediction
video_stream = None
vid = None
dim = None
x1, y1, x2, y2 = (None, None, None, None)
cuMat_color = cv2.cuda_GpuMat()
dtvl1 = cv2.cuda_OpticalFlowDual_TVL1.create(nscales=1,epsilon=0.05,warps=1)
delay = None
frames = None
threshold = None

# Initialise model
model = tf.keras.models.load_model(model_path)

## Initialise the output
detections = {
            "Logs": []
                }

@app.route("/ViolenceDetection/LogsDetections/", methods=["GET"])
def logs_detections():
    
    ## Return information
    return detections

@app.route("/ViolenceDetection/Initialise", methods=["PUT"])
def initialise_watch():
    global vid
    global dim
    global x1
    global x2
    global y1
    global y2
    global cuMat_color
    global dtvl1
    global delay
    global frames
    global detections
    global threshold
    
   
    # Get url
    url = request.json['url']
    delay = request.json['delay']
    frames = request.json['frames']
    threshold = request.json['threshold']
    
    # Capture video
    video_stream = get_yt_video(url)
    vid = cv2.VideoCapture(video_stream.url)
    # Check video properties
    check_video(vid)
    # Get the dimensions to resize the video (height x width)
    dim = resize_dimension(vid)
    # Get the crop coordinates
    x1, y1, x2, y2 = get_crop_coordinates(dim)
    # Initialise cuMats and OptFlow
    cuMat_color = cv2.cuda_GpuMat()
    dtvl1 = cv2.cuda_OpticalFlowDual_TVL1.create(nscales=1,epsilon=0.05,warps=1)
    
    # Reset detections dict ####
    detections = {
                "Logs": []
                }
    
    return "Done"

@app.route("/ViolenceDetection/Predict/<int:current_frame>", methods=["PUT"])
def start_prediction(current_frame):
    global vid
    global dim
    global x1
    global x2
    global y1
    global y2
    global cuMat_color
    global dtvl1
    global delay
    global frames
    global model
    global detections
    global threshold
    
    
    # Set video frame
    vid.set(cv2.CAP_PROP_POS_FRAMES, current_frame + delay)  
    #Start preprocess
    input_array = preprocess(vid, dim, x1, x2, y1, y2, cuMat_color, dtvl1, frames)
    # Prediction
    if input_array is not None:
        prediction = predict(input_array, model)
        
        # Fill detection dict ####
        detections["Logs"] += [(datetime.utcnow().strftime("%d-%m-%Y, %H:%M:%S"),
                                               prediction / 100,
                                               True if prediction >= threshold else False)]
        
        return str(1) if prediction >= threshold else str(0)
    else:
        return str(0)

app.run(host="0.0.0.0" , port=5000, debug=True)

