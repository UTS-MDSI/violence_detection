"""GUI App"""

# Import required packages
import tkinter as tk
import json

# Import classes
from infrastructure.gui_handler import Monitor 

# Run the GUI App
if __name__ == '__main__':     

    ## Load the sources selected by the user
    with open('data/user_inputs/user_cameras_selection.json', 'r') as f:
        user_sel = json.load(f)
    f.close()

    ## Set the sources
    sources = [
        (user_sel['one']['name'], user_sel['one']['source']), 
        (user_sel['two']['name'], user_sel['two']['source']), 
        (user_sel['three']['name'], user_sel['three']['source']), 
        (user_sel['four']['name'], user_sel['four']['source']), 
    ]
        
    ## Run the GUI App

    ### GUI
    Monitor(tk.Tk(), 'Violence Detection', sources)
    