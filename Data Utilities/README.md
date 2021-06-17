# SplitData

It split the training set into training and validation set.

We recommend the following folder structure in the root (with the folder data in the root directory):

- data
    - train
        - Fight
            - Videos inside
        - NonFight
            - Videos inside
    - val
        - Fight
            - Videos inside
        - NonFight
            - Videos inside

## Arguments
data_directory: Directory where the train and val folder are stored. Default: `../data`

ratio: Ratio of the training data that will be used as validation. Default: `0.25`

seed: Random seed of the split. Default: `1`

## Usage

Using default values:

```
python SplitData.py
```

Using default other values:

```
python SplitData.py --data_directory {} --ratio {} --seed {}

#Example
python SplitData.py --data_directory user/data_storage/tmp --ratio 0.3 --seed 10
```

## Result
The structure of the data folder will be the following:

- data
    - train
        - Fight
            - Videos inside
        - NonFight
            - Videos inside
    - test
        - Fight
            - Videos inside
        - NonFight
            - Videos inside
    - validation
        - Fight
            - Videos inside
        - NonFight
            - Videos inside

# I3DProprocess
It creates the rgb or flow arrays (both in .npy) with the preprocess used in I3D. This is a modified version the [Oanalgnat preprocess code](https://github.com/OanaIgnat/i3d_keras).

## Requirements

### Ubuntu
- ffmpeg

```
sudo apt update
sudo apt install ffmpeg
```
- opencv-contrib. We need this versions because it includes the optical flow DualTVL1 ([see Issue](https://github.com/Rhythmblue/i3d_finetune/issues/2))
```
pip uninstall opencv-python
pip install opencv-contrib-python
```

### Windows
Please follow [this instructions](https://www.youtube.com/watch?v=r1AtmY-RMyQ) to install ffmpeg. Remember to add the path to your environment variables.

Then, install opencv-contrib:
```
pip uninstall opencv-python
pip install opencv-contrib-python
```

## Arguments
temp_path: Path where the temporal files will be stored. Default: `../frames/`

type: It indicates if the input_path is just a single video [`file`] or a folder with multiple videos [`folder`]. Default: `file`

input_path: Path of the video file or folder with multiple videos. Default: `../data_storage/input_videos/cricket.avi`

output_path: Path where the rgb or flow files will be stored (.npy files). Default: `../datai3d/`

preprocess: It indicates the type of preprocess needed. For rgb use [`rgb`] and for optical flow use [`flow`]. Default: `rgb`

train: It indicates if the data is for training or validation/test set. We need to know this because the train data is not center cropped (it will be randomly cropped in the data generator).For train data use [`true`] and for validation/test data use [`false`]. Default: `true`


## Usage

### Single video file

Using default parameters:
```
python i3dpreprocess.py
```

Using other parameters:
```
python i3dpreprocess.py --temp_path ../temp/ --type file --input_path ../data_storage/train/Fight/ --output_path ../datai3d/rgb/train/Fight --preprocess rgb
```

### Folder with multiple videos

Using other parameters:
```
python i3dpreprocess.py --temp_path ../temp/ --type folder --input_path ../data_storage/train/Fight/ --output_path ../datai3d/rgb/train/Fight --preprocess flow
```