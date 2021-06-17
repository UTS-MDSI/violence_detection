import cv2
import os
import numpy as np
import argparse
import shutil
import time

SMALLEST_DIM = 256
IMAGE_CROP_SIZE = 224
FRAME_RATE = 25
start_time = time.time()

# sample frames at 25 frames per second
def sample_video(video_path, temp_path):
    start_time = time.time()
    # for filename in os.listdir(video_path):
    if video_path.endswith((".mp4", ".avi")):
        os.system("ffmpeg -i {0} -vf fps={1} -q:v 2 {2}/frame_%05d.jpg".format(video_path, FRAME_RATE,
                                                                          temp_path))
    else:
        raise ValueError("Video path is not the name of video file (.mp4 or .avi)")
    print("sampling:--- %s seconds ---" % (time.time() - start_time))

def read_frames(temp_path):
    start_time = time.time()
    list_frames = []
    for file in os.listdir(temp_path):
        if file.endswith(".jpg"):
            full_file_path = os.path.join(temp_path, file)
            list_frames.append(full_file_path)
    sorted_list_frames = sorted(list_frames)
    print("Reading frames:--- %s seconds ---" % (time.time() - start_time))
    return sorted_list_frames

# It gets the dimmension of the video after resizing it
def get_dimension(img):
    start_time = time.time()
    img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    
    original_width = int(img.shape[1])
    original_height = int(img.shape[0])

    aspect_ratio = original_width / original_height

    if original_height < original_width:
        new_height = SMALLEST_DIM
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = SMALLEST_DIM
        new_height = int(original_width / aspect_ratio)

    dim = (new_height, new_width)
    print("Dimensions:--- %s seconds ---" % (time.time() - start_time))
    return dim

#  Pixel values are truncated to the range [-20, 20], then rescaled between -1 and 1
def compute_optical_flow(prev, curr):
    #dtvl1 = cv2.cuda_OpticalFlowDual_TVL1.create(nscales=1,epsilon=0.05,warps=1)
    dtvl1 = cv2.cuda_OpticalFlowDual_TVL1.create()

    flowDTVL1 = cv2.cuda_OpticalFlowDual_TVL1.calc(
                dtvl1, prev, curr, None,
                )
    return flowDTVL1


def runrgbflow(sorted_list_frames, dim):
    start_time = time.time()
    # Dimension of final images 
    img_height = dim[0]
    img_width = dim[1]
    # Creating cuMats
    cuMat_current_img = cv2.cuda_GpuMat()
    #cuMat_prev_bw = cv2.cuda_GpuMat()
    cuMataux1 = cv2.cuda_GpuMat()
    cuMataux2 = cv2.cuda_GpuMat()
    # Fill aux cuMats
    cuMataux1.upload(np.ones((img_height, img_width,3), dtype ='float64')*2/255)
    cuMataux2.upload(np.ones((img_height, img_width,3), dtype ='float64')*-1)

    # Array to store results
    result = np.zeros((1, img_height, img_width, 5))
    
    # Process image by image and append
    for id, full_file_path in enumerate(sorted_list_frames):
        # Read image
        current_img = cv2.imread(full_file_path, cv2.IMREAD_UNCHANGED)
        # To cuMat
        cuMat_current_img.upload(current_img)
        
        # Resize
        cuMat_current_img = cv2.cuda.resize(cuMat_current_img, (img_width,img_height), interpolation=cv2.INTER_LINEAR)
        # Create bw image
        cuMat_current_bw = cv2.cuda.cvtColor(cuMat_current_img, cv2.COLOR_BGR2GRAY)

        # If first pass in for just create prev_img
        if id == 0:
            cuMat_prev_bw = cuMat_current_bw
            continue
        
        # Compute flow
        cuMat_flow = compute_optical_flow(cuMat_prev_bw, cuMat_current_bw)
        cuMat_prev_bw = cuMat_current_bw

        # Normalise RGB
        cuMat_current_img = cuMat_current_img.convertTo(dst = cuMat_current_img, rtype = 22)
        cuMat_current_img = cv2.cuda.multiply(cuMat_current_img, cuMataux1)
        cuMat_current_img = cv2.cuda.add(cuMat_current_img, cuMataux2)

        # Download
        flow = cuMat_flow.download()
        current_img = cuMat_current_img.download()
        
        # Normalise Flow
        flow = np.clip(flow, -20, 20)
        flow = flow / 20.0

        # Concatenate both
        rgbflow = np.concatenate((current_img, flow), axis=2)
        rgbflow = np.reshape(rgbflow, (1, img_height, img_width, 5))
        result = np.append(result, rgbflow, axis=0)

    # Avoid first one with zeros
    result = result[1:, :, :, :]
    print("RGB/FLOW:--- %s seconds ---" % (time.time() - start_time))
    return result

def process_single_file(video_path, output_path, temp_path):
    # sample all video from video_path at specified frame rate (FRAME_RATE param)
    sample_video(video_path, temp_path)

    # make sure the frames are processed in order (list of sorted frames)
    sorted_list_frames = read_frames(temp_path)

    # get only the video name
    video_name = video_path.split("/")[-1][:-4]

    # get video dimension after resizing
    dim = get_dimension(sorted_list_frames[0])

    # run rbg+flow
    output = runrgbflow(sorted_list_frames, dim)
    
    output_path = os.path.join(output_path, video_name + ".npz")
    
    start_time = time.time()
    np.savez_compressed(output_path, output)
    print("Saving:--- %s seconds ---" % (time.time() - start_time))
    
    # Delete temp folder
    shutil.rmtree(temp_path)

def process_folder(input_path, output_path, temp_path):
    # Get full video paths
    list_videos = []
    for video in os.listdir(input_path):
        if video.endswith((".mp4", ".avi")):
            full_video_path = os.path.join(input_path, video)
            list_videos.append(full_video_path)
    
    # Process videos one by one
    for video_path in list_videos:
        process_single_file(video_path, output_path, temp_path)
        os.makedirs(temp_path)

def main(args):
    # Check if input_path exists
    if not os.path.exists(args.input_path):
        raise ValueError('Input path does not exists')
    
    # Check tmp folder
    if not os.path.exists(args.temp_path):
        os.makedirs(args.temp_path)
    else:
        shutil.rmtree(args.temp_path)
        os.makedirs(args.temp_path)
    
    # Check outputfolder
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
      
    # Processing
    if args.type == 'file':
        process_single_file(args.input_path, args.output_path, args.temp_path)
    elif args.type == 'folder':
        process_folder(args.input_path, args.output_path, args.temp_path)
    else:
        raise ValueError('Argument type must be file or folder only')

    print("Total: --- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--temp_path', type=str, default="../frames/")
    parser.add_argument('--type', type=str, default='file')
    parser.add_argument('--input_path', type=str, default = '../data/input_videos/cricket.avi')
    parser.add_argument('--output_path', type=str, default="../datai3d/")
    
    args = parser.parse_args()

    main(args)