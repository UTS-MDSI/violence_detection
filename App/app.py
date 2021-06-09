"""App"""

import tkinter as tk

from infrastructure.windows.login import Login

## Run the GUI App
root = tk.Tk()
app = Login(root)
root.mainloop()