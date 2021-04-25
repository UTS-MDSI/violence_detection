import os
import re
import random
import shutil
import argparse

def isFinalFolder(path):
    '''
    Returns True if the folder do not have subfolders inside
    '''
    # For each file/folder inside the path
    for file in os.listdir(path):
        # If file is a directy, return False 
        if os.path.isdir(os.path.join(path,file)):
            return False
    # Return True if no folder was inside the path
    return True

def path_to_dict(path):
    '''
    Creates a dictionary of the content of path. If there is a subfolder,
    the funtion is call recursively.
    '''
    # Creates dict to store the structure and files to store the files of the final folder
    fileDict = dict()
    files = []
    
    # For each folder in the path
    for folder in os.listdir(path):
        # Save the new path
        subpath = os.path.join(path,folder)
        # If this is not the final folder
        if not isFinalFolder(subpath):
            # Save it to the dictionary, calling it recursively
            fileDict[folder] = path_to_dict(subpath)
        # If this is the final folder
        else:
            # Save it to the dictionary as a list of the files inside
            fileDict[folder] = os.listdir(subpath)
    
    # Return the dictionary
    return fileDict

def get_unique_values(filesDict):
    '''
    # Return a dictionary with the count of unique values per each video
    '''
    # Creating empty dictionary to store the values
    unique_values = dict()
        
    # Iterate labels and files in the dictionary
    for label, _files in filesDict.items():
        # Creating a empty dictionary to store the unique values and count per label
        files_dict = dict()
        # For each file in the list of files
        for file in _files:
            # Take just the part of the video name
            fileName = re.split('_[0-9]+.avi', file)[0]
            # If that video exists on the dictionary
            if fileName in files_dict.keys():
                # Sum 1
                files_dict[fileName] += 1
            # If not, just put 1
            else:
                files_dict[fileName] = 1
        # When the second for ends, store the dictionary into the other
        unique_values[label] = files_dict
    #Returns
    return unique_values

def suffle_dict(_dict, seed = 1):
    '''
    It returns a suffled dictionary
    '''
    random.seed(seed)
    temp = list(_dict.items())
    random.shuffle(temp)
    _dict = dict(temp)
    return _dict

def validation_videos(unique_files, ratio = 0.2):
    '''
    It returns a list with the videos to put into the validation set
    
    # Arguments
    unique_files: Dictionary with the unique value count
    ratio: ratio of train samples to go into the validation set    
    '''
    # Get the number of videos in the dictionary
    total_videos = 0
    for file, num in unique_files.items():
        total_videos += num
    
    # Create the validation unique files list
    validation = []
    # Counting the number of videos
    videos = 0
    for file, num in unique_files.items():
        videos += num
        # If the video count is more than the ratio of validation set, it stops
        if videos >= total_videos * ratio:
            return validation
        else:
            validation.append(file)

def move_clips(files, validation_set, directory):
    '''
    It moves the files from one directory to another
    '''
    source = os.path.join(directory, 'train')
    destination = os.path.join(directory, 'validation')
    
    # For each label in files
    for label, _files in files.items():
        os.mkdir(os.path.join(destination,label))
        for file in _files:
            video_name = re.split('_[0-9]+.avi', file)[0]
            if video_name in validation_set[label]: 
                source_file = os.path.join(source, label, file)
                dest_folder = os.path.join(destination, label)
                shutil.move(source_file, dest_folder)

def main(args):
    # Check if directory exists
    if not os.path.exists(args.data_directory):
        raise ValueError("Path does not exists")
    
    # Check if train and val are inside the directory
    if not ('train' in os.listdir(args.data_directory) and 'val' in os.listdir(args.data_directory)):
        raise ValueError('train or val directories are not inside the path')

    # Check structure of the train folder
    files = path_to_dict(os.path.join(args.data_directory, 'train'))

    # Get unique video names
    unique_files = get_unique_values(files)

    # Shuffle file order
    unique_files['Fight'] = suffle_dict(unique_files['Fight'], args.seed)
    unique_files['NonFight'] = suffle_dict(unique_files['NonFight'], args.seed)

    # Raname val to test
    os.rename(os.path.join(args.data_directory, 'val'),
                os.path.join(args.data_directory, 'test'))
    
    # Unique names of the videos that go to validation
    unique_files['Fight'] = validation_videos(unique_files['Fight'], args.ratio)
    unique_files['NonFight'] = validation_videos(unique_files['NonFight'], args.ratio)

    # Creates validation folder if not exists
    if not os.path.exists(os.path.join(args.data_directory,'validation')):
        os.mkdir(os.path.join(args.data_directory,'validation'))
    
    move_clips(files, unique_files, args.data_directory)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_directory', type=str, default="../data")
    parser.add_argument('--ratio', type=float, default=0.2)
    parser.add_argument('--seed', type=int, default=1)

    args = parser.parse_args()

    main(args)