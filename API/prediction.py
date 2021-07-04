import cv2
import numpy as np
import pafy
import time
import tensorflow as tf
import argparse
import requests
import math
import warnings
from datetime import datetime
import json


# Global variables
SMALLEST_DIM = 256
VIDEO_FPS = 30
IMAGE_CROP_SIZE = 224

def get_yt_video(url):
    '''
    It returns the pafy video stream when small dim is greater than SMALLEST DIM.
    It prioritise small dim streams
    Parameters:
    * url: Youtube url
    '''
    stream_source = pafy.new(url)
    for id, s in  enumerate(stream_source.streams):
        # Get the min dimension
        min_dim = min([int(dim) for dim in s.resolution.split('x')])
        # If the dim is greater than smallest_dim return that stream
        if min_dim >= SMALLEST_DIM:
            video_stream = stream_source.streams[id]
            print("Youtube stream found at resolution: {}".format(video_stream.resolution))
            return video_stream
        
def check_video(vid):
    min_dim = min (int(vid.get(3)), int(vid.get(4)))
    fps = int(vid.get(5))

    if min_dim < SMALLEST_DIM:
        raise ValueError('Video resolution is too small. Smallest dimension need to be higher than {} pixels'.format(SMALLEST_DIM))
    elif fps != VIDEO_FPS:
        warnings.warn('Video FPS are {} but it was expected {}'.format(fps, VIDEO_FPS))
    else:
        print('Resolution {}x{} and FPS {} are correct'.format(vid.get(3), vid.get(4), vid.get(5)))
        
def resize_dimension(vid):
    '''
    Get the dimensions to resize frames.
    It should be X x SMALLEST_DIM or SMALLEST_DIM x X
    It returns a tupple (height, width)
    ''' 
    original_width = vid.get(3)
    original_height = vid.get(4)
    aspect_ratio = original_width / original_height
    if original_height < original_width:
        new_height = SMALLEST_DIM
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = SMALLEST_DIM
        new_height = int(original_width / aspect_ratio)
    dim = (new_height, new_width)
    return dim

def get_crop_coordinates(dim):
    # Center coordinates of the video
    x_center = math.ceil(dim[1]/2)
    y_center = math.ceil(dim[0]/2)
    # Coordinates where the crop starts
    x1 = x_center - math.ceil(IMAGE_CROP_SIZE/2)
    y1 = y_center - math.ceil(IMAGE_CROP_SIZE/2)
    # Coordinates where the crop ends
    x2 = x_center + math.floor(IMAGE_CROP_SIZE/2)
    y2 = y_center + math.floor(IMAGE_CROP_SIZE/2)

    return x1, y1, x2, y2

def compute_optflow(cuMat_color, prevcuMat_color, dtvl1):
    '''
    It computes the optical flow based on two frames (BGR)
    It returns a np array with the optical flow
    '''
    # Transform to BW
    cuMat_BW = cv2.cuda.cvtColor(cuMat_color, cv2.COLOR_BGR2GRAY)
    prevcuMat_BW = cv2.cuda.cvtColor(prevcuMat_color, cv2.COLOR_BGR2GRAY)
    
    # Computes optical flow
    cuMat_flow = cv2.cuda_OpticalFlowDual_TVL1.calc(dtvl1, 
                                prevcuMat_BW, cuMat_BW, None)

    # Postprocess
    flow = cuMat_flow.download()
    flow = np.clip(flow, -20, 20)
    flow = flow / 20.0
    return flow

def normalise_rgb(cuMat_color):
    '''
    It normalise a cuMat RGB
    It returns a np array
    '''
    # Download array
    rgb = cuMat_color.download()
    rgb = rgb.astype('float64')
    rgb = (rgb/255) * 2 - 1
    return rgb

def preprocess(vid, dim, x1, x2, y1, y2, cuMat_color, dtvl1, frames):
    result = []
    while vid.isOpened():
        ret, frame = vid.read()
        if ret:
            # Rezise RGB
            cuMat_color.upload(frame)
            cuMat_color = cv2.cuda.resize(cuMat_color, (dim[1],dim[0]), interpolation=cv2.INTER_LINEAR)
            
            # Compute opticalflow with preprocessing if prevcuMat_color exists
            try:
                flow = compute_optflow(cuMat_color, prevcuMat_color, dtvl1)
            except:
                prevcuMat_color = cuMat_color.clone()
                continue
                
            # Normalise RGB
            rgb = normalise_rgb(cuMat_color)
            
            # Concatenate results and shape it
            rgbflow = np.concatenate((rgb,flow), axis = 2)
            rgbflow = np.expand_dims(rgbflow, axis = 0)

            # Crop result
            rgbflow = rgbflow[:,y1:y2,x1:x2,:]

            # Append result
            result.append(rgbflow)
            
            if len(result)>=frames:
                input_array = np.reshape(result, newshape=(len(result), 224 , 224, 5))
                input_array = np.expand_dims(input_array, axis = 0)                
                return input_array
        
        else:
            return None
    return None

def predict(array, model):
    '''
    It returns the prediction
    Probability of positive class
    '''
    prediction = model.predict(array)
    prediction = int(prediction[0][0]*100)
    return prediction
    