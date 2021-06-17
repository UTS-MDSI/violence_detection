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
    # for filename in os.listdir(video_path):
    if video_path.endswith((".mp4", ".avi")):
        # filename = video_path + filename
        os.system("ffmpeg -i {0} -vf fps={1} -q:v 2 {2}/frame_%05d.jpg".format(video_path, FRAME_RATE,
                                                                          temp_path))
    else:
        raise ValueError("Video path is not the name of video file (.mp4 or .avi)")

# It gets the dimmension of the video after resizing it
def get_dimension(img):
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

    return dim

# the videos are resized preserving aspect ratio so that the smallest dimension is 256 pixels, with bilinear interpolation
def resize(img, dim):
    # resize image
    resized = cv2.resize(img, (dim[1], dim[0]), interpolation=cv2.INTER_LINEAR)
    # print('Resized Dimensions : ', resized.shape)

    return resized


def crop_center(img, new_size):
    y, x, c = img.shape
    (cropx, cropy) = new_size
    startx = x // 2 - (cropx // 2)
    starty = y // 2 - (cropy // 2)
    return img[starty:starty + cropy, startx:startx + cropx]


def rescale_pixel_values(img):
    # print('Data Type: %s' % img.dtype)
    # print('Min: %.3f, Max: %.3f' % (img.min(), img.max()))
    img = img.astype('float32')
    # normalize to the range 0:1
    # img /= 255.0
    # normalize to the range -1:1
    img = (img / 255.0) * 2 - 1
    # confirm the normalization
    # print('Min: %.3f, Max: %.3f' % (img.min(), img.max()))
    return img


# The provided .npy file thus has shape (1, num_frames, 224, 224, 3) for RGB, corresponding to a batch size of 1
def run_rgb(sorted_list_frames, train, dim):

    # Dimensions to initialise the np array
    if train:
        img_width = dim[1]
        img_height = dim[0]
    else:
        img_width = IMAGE_CROP_SIZE
        img_height = IMAGE_CROP_SIZE
    result = np.zeros((1, img_height, img_width, 3))

    # Process image by image and append
    for full_file_path in sorted_list_frames:
        img = cv2.imread(full_file_path, cv2.IMREAD_UNCHANGED)
        img = pre_process_rgb(img, train, dim)
        new_img = np.reshape(img, (1, img_height, img_width, 3))
        result = np.append(result, new_img, axis=0)

    result = result[1:, :, :, :]
    result = np.expand_dims(result, axis=0)
    return result


def pre_process_rgb(img, train, dim):
    # Resize to 256 x X or X x 256
    resized = resize(img, dim)
    # If it is a train image, just rescale
    if train:
        img = rescale_pixel_values(resized)
    # If it is not, crop the image and rescale
    else:
        img_cropped = crop_center(resized, (IMAGE_CROP_SIZE, IMAGE_CROP_SIZE))
        img = rescale_pixel_values(img_cropped)
    return img


def read_frames(temp_path):
    list_frames = []
    for file in os.listdir(temp_path):
        if file.endswith(".jpg"):
            full_file_path = os.path.join(temp_path, file)
            list_frames.append(full_file_path)
    sorted_list_frames = sorted(list_frames)
    return sorted_list_frames


def run_flow(sorted_list_frames, train, dim):
    # Create a np array with the images
    sorted_list_img = []
    for frame in sorted_list_frames:
        img = cv2.imread(frame, cv2.IMREAD_UNCHANGED)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sorted_list_img.append(img_gray)

    # Dimensions to initialise the np array
    if train:
        img_width = dim[1]
        img_height = dim[0]
    else:
        img_width = IMAGE_CROP_SIZE
        img_height = IMAGE_CROP_SIZE
    result = np.zeros((1, img_height, img_width, 2))

    # Process pair of images and append
    prev = sorted_list_img[0]
    for curr in sorted_list_img[1:]:
        flow = compute_optical_flow(prev, curr)
        flow = pre_process_flow(flow, train, dim)
        prev = curr
        result = np.append(result, flow, axis=0)

    result = result[1:, :, :, :]
    result = np.expand_dims(result, axis=0)
    return result


def pre_process_flow(flow_frame, train, dim):
    # Resize to 256 x X or X x 256
    resized = resize(flow_frame, dim)
    # If train just reshape
    if train:
        new_img = np.reshape(resized, (1, dim[0], dim[1], 2)) ##
    # If it is not, crop and reshape
    else:
        img_cropped = crop_center(resized, (IMAGE_CROP_SIZE, IMAGE_CROP_SIZE))
        new_img = np.reshape(img_cropped, (1, IMAGE_CROP_SIZE, IMAGE_CROP_SIZE, 2))
    return new_img


#  Pixel values are truncated to the range [-20, 20], then rescaled between -1 and 1
def compute_optical_flow(prev, curr):
    #Old version
    #optical_flow = cv2.optflow.createOptFlow_DualTVL1()
    optical_flow = cv2.optflow.DualTVL1OpticalFlow_create(nscales=1,epsilon=0.05,warps=1)
    flow_frame = optical_flow.calc(prev, curr, None)
    flow_frame = np.clip(flow_frame, -20, 20)
    flow_frame = flow_frame / 20.0
    return flow_frame

def process_single_file(video_path, output_path, temp_path, preprocess, train):
    # sample all video from video_path at specified frame rate (FRAME_RATE param)
    sample_video(video_path, temp_path)

    # make sure the frames are processed in order (list of sorted frames)
    sorted_list_frames = read_frames(temp_path)

    # get only the video name
    video_name = video_path.split("/")[-1][:-4]

    print(video_name)

    # get video dimension after resizing
    dim = get_dimension(sorted_list_frames[0])

    if preprocess == 'rgb':
        # Create rgb array
        rgb = run_rgb(sorted_list_frames, train, dim)
        # Output path of the array
        npy_rgb_output = os.path.join(output_path, video_name + '_rgb.npz')
        # Save it
        np.savez_compressed(npy_rgb_output, rgb)
    
    elif preprocess == 'flow':
        # Create flow array
        flow = run_flow(sorted_list_frames, train, dim)
        # Output path of the array
        npy_flow_output = os.path.join(output_path, video_name + '_flow.npz')
        # Save it
        np.savez_compressed(npy_flow_output, flow)

    # Delete temp folder
    shutil.rmtree(temp_path)

def process_folder(input_path, output_path, temp_path, preprocess, train):
    # Get full video paths
    list_videos = []
    for video in os.listdir(input_path):
        if video.endswith((".mp4", ".avi")):
            full_video_path = os.path.join(input_path, video)
            list_videos.append(full_video_path)
    
    # Process videos one by one
    for video_path in list_videos:
        process_single_file(video_path, output_path, temp_path, preprocess, train)
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
      
    # Check preprocess
    if not args.preprocess in ['rgb', 'flow']:
        raise ValueError('Argument preprocess must be rgb or flow')   
    if args.type == 'file':
        process_single_file(args.input_path, args.output_path, args.temp_path, args.preprocess, args.train)
    elif args.type == 'folder':
        process_folder(args.input_path, args.output_path, args.temp_path, args.preprocess, args.train)
    else:
        raise ValueError('Argument type must be file or folder only')

    print("--- %s seconds ---" % (time.time() - start_time))

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
    parser.add_argument('--temp_path', type=str, default="../frames/")
    parser.add_argument('--type', type=str, default='file')
    parser.add_argument('--input_path', type=str, default = '../data_storage/input_videos/cricket.avi')
    parser.add_argument('--output_path', type=str, default="../datai3d/")
    parser.add_argument('--preprocess', type=str, default='rgb')
    parser.add_argument('--train' , type=str2bool, nargs='?',
                        const=True, default=True)
    
    args = parser.parse_args()

    main(args)