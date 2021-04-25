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

ratio: Ratio of the training data that will be used as validation. Default: `0.2`

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
python SplitData.py --data_directory user/data/tmp --ratio 0.3 --seed 10
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