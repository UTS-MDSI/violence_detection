import cv2
import numpy as np
import time
import argparse
import os
import shutil

# Global variables
SMALLEST_DIM = 256
    
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

def process_rgb_flow(vid, dim):

    # Initialise cuMats and OptFlow
    cuMat_color = cv2.cuda_GpuMat()
    dtvl1 = cv2.cuda_OpticalFlowDual_TVL1.create(nscales=1,epsilon=0.05,warps=1)

    # Initialise array to store frames
    result = np.zeros((1, dim[0], dim[1], 5))
    
    # Loop over video frames
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
            result = np.append(result, rgbflow, axis = 0)
        
        else:
            break

    vid.release()                        
    # Drop first frame (only zeros)
    return result[1:,:,:,:]
             
def process_single_file(video_path, output_path):
    
    start_time = time.time()

    # It stores the video name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    print("Processing {} video".format(video_name))

    # Capture video
    vid = cv2.VideoCapture(video_path)

    # Get dimensions to resize video
    dim = resize_dimension(vid)
    
    # Process RGB and Opt Flow
    output = process_rgb_flow(vid, dim)
    
    # Create name of new npz file    
    output_path = os.path.join(output_path, video_name + ".npz")
    # Save npz file
    np.savez_compressed(output_path, output)
    
    # Print time for one file
    print("Output shape: {}".format(output.shape))
    print("Total time:--- %s seconds ---" % (time.time() - start_time))
            

def process_folder(input_path, output_path):
    # Get full video paths
    list_videos = []
    for video in os.listdir(input_path):
        if video.endswith((".mp4", ".avi")):
            full_video_path = os.path.join(input_path, video)
            list_videos.append(full_video_path)
    
    # Process videos one by one
    for video_path in list_videos:
        process_single_file(video_path, output_path)

    # Print how many videos were processed
    print("Process ended. A total of {} videos were processed".format(len(list_videos)))

def main(args):
    
    # Check if input_path exists
    if not os.path.exists(args.input_path):
        raise ValueError('Input path does not exists')
    
    # Check outputfolder
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
      
    # Processing
    if args.type == 'file':
        process_single_file(args.input_path, args.output_path)
    elif args.type == 'folder':
        process_folder(args.input_path, args.output_path)
    else:
        raise ValueError('Argument type must be file or folder only')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='folder')
    parser.add_argument('--input_path', type=str, default = '../data/')
    parser.add_argument('--output_path', type=str, default='../datai3d/')
    
    args = parser.parse_args()

    main(args)

