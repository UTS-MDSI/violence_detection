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
    
    # If no stream with enough resolution was found: error
    raise ValueError('Video resolution is too small. Smallest dimension need to be higher than {} pixels'.format(SMALLEST_DIM))

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


def process_rgbflow(frame, prevframe):
    cuMat_color = cv2.cuda_GpuMat()
    dtvl1 = cv2.cuda_OpticalFlowDual_TVL1.create(nscales=1,epsilon=0.05,warps=1)
    
    cuMat_color.upload(frame)
    cuMat_color = cv2.cuda.resize(cuMat_color, (dim[1],dim[0]), interpolation=cv2.INTER_LINEAR)


    pass

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

def predict(array, model):
    '''
    It returns the prediction
    Probability of positive class
    '''
    # Get prediction
    prediction = model.predict(array)
    # Transform prediction (probability of positive)
    #prediction = int(prediction[0][0]*100)
    return prediction

def put_results(prediction, api_url):
    '''
    It puts the prediction
    '''
    requests.put(f"{api_url}{prediction}")

def get_frame(api_url):
    '''
    '''
    response = requests.get(api_url)
    current_frame = json.loads(response.text)["Current Frame"]
    return current_frame

def main(args):

    # Capture video
    if args.youtube:
        video_stream = get_yt_video(args.location)
        vid = cv2.VideoCapture(video_stream.url)
    else:
        vid = cv2.VideoCapture(args.location)

    # Check video properties
    check_video(vid) 

    # Get the dimensions to resize the video (height x width)
    dim = resize_dimension(vid)
    # Get the crop coordinates
    x1, y1, x2, y2 = get_crop_coordinates(dim)

    # Read model
    model = tf.keras.models.load_model(args.model)
    
    # Initialise cuMats and OptFlow
    cuMat_color = cv2.cuda_GpuMat()
    dtvl1 = cv2.cuda_OpticalFlowDual_TVL1.create(nscales=1,epsilon=0.05,warps=1)

    # Initialise array to store frames
    result = []
    
    current_frame = 1
    
    print("Waiting for video")
    
    while current_frame == 1:
        current_frame = get_frame(args.getapi)
        vid.set(cv2.CAP_PROP_POS_FRAMES, current_frame + args.advance)
    
    print('Starting to watch video')
    start_time = time.time()

    while vid.isOpened():
   
        ret, frame = vid.read()
        if ret:
            start_st = time.time()

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

            # try:
            #     time.sleep()
            # except:
            #     pass

            # When enough frames has been collected
            if len(result)>args.frames + 1:
                # Reshape results
                input_array = np.reshape(result, newshape=(len(result), IMAGE_CROP_SIZE , IMAGE_CROP_SIZE, 5))
                input_array = np.expand_dims(input_array, axis = 0)
                
                prediction = predict(input_array, model)
                put_results(int(prediction[0][0]*100), args.putapi)

                # Reset variables
                prevcuMat_color = None
                result = result[30:]

                # Set frame after prediction
                current_frame = get_frame(args.getapi)
                vid.set(cv2.CAP_PROP_POS_FRAMES, current_frame + args.advance)  

                print(f"Fight probability: {prediction} - Frame {vid.get(1)}")
                print('It took: %s seconds' % (time.time() - start_time))
                print('#################################################')
                start_time = time.time()
            else:
                pass
        
        else:
            print("Video has ended")
            break
         
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--location', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--putapi', type=str)
    parser.add_argument('--getapi', type=str)
    parser.add_argument('--youtube', type=str2bool, nargs='?',
                        const=True, default=True)
    parser.add_argument('--frames', type=int, default=True)  # Number of frames to append before prediction
    parser.add_argument('--advance', type=int, default=True) 

    args = parser.parse_args()

    main(args)