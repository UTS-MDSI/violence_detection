from tensorflow.keras.utils import Sequence
from tensorflow.python.keras.utils import np_utils
import os
import random
import numpy as np
import math

class DataGenerator(Sequence):
    """Data Generator inherited from keras.utils.Sequence
    Args: 
        directory: the path of data set, and each sub-folder will be assigned to one class
        batch_size: the number of data points in each batch
        shuffle: whether to shuffle the data per epoch
        data_augmentation: whether to apply random crop or not
        target_frames: Target number of frames to sample. If None dim is kept.
        crop_dim: Shape of the crop (random or not).  Height, Width
        seed: random seed
        flip: whether to apply flip or not
    Note:
        If you want to load file with other data format, please fix the method of "load_data" as you want
    """
    def __init__(self, directory, batch_size=1, shuffle=True, data_augmentation=True, 
                 target_frames = 79, crop_dim = (224, 224), seed = None, flip = True):
        # Initialize the params
        self.batch_size = batch_size
        self.directory = directory
        self.shuffle = shuffle
        self.data_aug = data_augmentation
        self.target_frames = target_frames
        self.seed = seed
        self.crop_dim = crop_dim
        self.flip = True
        # Load all the save_path of files, and create a dictionary that save the pair of "data:label"
        self.X_path, self.Y_dict = self.search_data() 
        # Print basic statistics information
        self.print_stats()
        return None
    
    def search_data(self):
        X_path = []
        Y_dict = {}
        # list all kinds of sub-folders
        self.dirs = sorted(os.listdir(self.directory))
        one_hots = np_utils.to_categorical(range(len(self.dirs)))
        for i,folder in enumerate(self.dirs):
            folder_path = os.path.join(self.directory,folder)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path,file)
                # append the each file path, and keep its label  
                X_path.append(file_path)
                Y_dict[file_path] = one_hots[i]
        return X_path, Y_dict
    
    def print_stats(self):
        # calculate basic information
        self.n_files = len(self.X_path)
        self.n_classes = len(self.dirs)
        self.indexes = np.arange(len(self.X_path))
        # If shuffle true, shuffle indexes
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
        # Output states
        print("Found {} files belonging to {} classes.".format(self.n_files,self.n_classes))
        for i,label in enumerate(self.dirs):
            print('%10s : '%(label),i)
        return None
    
    def __len__(self):
        # calculate the iterations of each epoch
        steps_per_epoch = np.ceil(len(self.X_path) / float(self.batch_size))
        return int(steps_per_epoch)
    
    def __getitem__(self, index):
        """Get the data of each batch
        """
        # get the indexs of each batch
        batch_indexs = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        # using batch_indexs to get path of current batch
        batch_path = [self.X_path[k] for k in batch_indexs]
        # get batch data
        batch_x, batch_y = self.data_generation(batch_path)
        return batch_x, batch_y
    
    def on_epoch_end(self):
        # shuffle the data at each end of epoch
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
            
    def data_generation(self, batch_path):
        # load data into memory, you can change the np.load to any method you want        
        batch_x = [self.load_data(x) for x in batch_path]
        batch_y = [self.Y_dict[x] for x in batch_path]
        # transfer the data format and take one-hot coding for labels
        batch_x = np.array(batch_x)
        batch_y = np.array(batch_y)
        return batch_x, batch_y
    
    def dynamic_crop(self, video):
        video_dim = video.shape
        video_height = video_dim[1]
        video_width = video_dim[2]
        
        if self.data_aug:
            # Max coordinates where we can apply the crop
            x_max = video_width - self.crop_dim[1]
            y_max = video_height - self.crop_dim[0]
            # Coordinates where the crop starts
            x = random.randint(0, x_max)
            y = random.randint(0, y_max)
            
        else:
            # Center coordinates of the video
            x_center = math.ceil(video_width/2)
            y_center = math.ceil(video_height/2)
            # Coordinates where the crop starts            
            x = x_center - math.ceil(self.crop_dim[1]/2)
            y = y_center - math.ceil(self.crop_dim[0]/2)
                        
        return video[:,y:y+self.crop_dim[0],x:x+self.crop_dim[1],:]
        
    
    def frame_sampling(self, video):
        # get total frames of input video
        len_frames = video.shape[0]
        
        # If the video is shorter than needed
        if len_frames < self.target_frames:
            # Times the video need to be looped to get 64 frames
            times = self.target_frames//len_frames
            remainder = self.target_frames%len_frames
            # Creating new array to store cat video
            new_video = video
            
            # Repeat the video as many times as needed
            for n in range(1,times):
                new_video = np.concatenate((new_video, video), axis = 0)
            # Add part of the video if needed
            if remainder > 0:
                new_video = np.concatenate((new_video, video[:remainder,:,:]), axis = 0)
            
            return new_video
               
        # If the video is longer than needed
        elif len_frames > self.target_frames:
            # Set random start
            start_frame = random.randint(0,len_frames - self.target_frames)
            end_frame = start_frame + self.target_frames
            
            new_video = video[start_frame:end_frame,:,:]
            
            return new_video
        
        # If the video is fine
        elif len_frames == self.target_frames:
            return video
    
    def random_flip(self, video): 
        # Flip on width (left-rigth)
        if random.randint(0,1) == 1:
            video = np.flip(video, axis = 2)
                
        return video
    
    def load_data(self, path):
        data = np.load(path)['arr_0']
    
        # Sampling frames
        if self.target_frames is not None:
            data = self.frame_sampling(video = data)
        
        # Center if data_aug is false and random if data_aug is true
        data = self.dynamic_crop(data)
        
        # If it needs flip
        if self.flip:
            data = self.random_flip(data)

        return data