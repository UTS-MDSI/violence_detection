# TO BE REPLACED: THIS MUST BE DONE BY THE USER DURING THE 2ND WINDOW
import json

user_cameras_selection = {
    'one': {
        'name': 'St. George Square', 
        'source': 'data/church.mp4'
        },
    'two': {
        'name': 'Maiden Lane',
        'source': 'data/street.mp4'
        },
    'three': {
        'name': 'Lexington Avenue',
        'source': 'data/assault.mp4'
        },
    'four': {
        'name': '52nd Street Alley',
        'source': 'data/fight.mp4'
        }     
    }

with open('data/user_inputs/user_cameras_selection.json', 'w') as f:
    json.dump(user_cameras_selection, f)