"""class Monitor"""

import json
import tkinter as tk
from infrastructure.frames.video_frame import VideoFrame 

class Monitor:

	def __init__(self, monitor, number):

		bheight = 31
		bwidth = 130
		bx = 0.95
		
		self.monitor = monitor
		self.monitor.title("Violence Detection - Monitor")

		self.frame = tk.Frame(self.monitor)
		
		screen_width = self.monitor.winfo_screenwidth()
		screen_height = self.monitor.winfo_screenheight()
		self.monitor.geometry(f'{screen_width}x{screen_height}')
		self.monitor.resizable(1, 1)
		self.monitor.columnconfigure([0,1], minsize=screen_width/2.107)
		self.monitor.rowconfigure([0,1,2], minsize=screen_height/3)

		with open('data/user_inputs/user_cameras_selection.json', 'r') as f:
			user_sel = json.load(f)
		f.close()

		sources = [
            (user_sel['one']['name'], user_sel['one']['source']), 
            (user_sel['two']['name'], user_sel['two']['source']), 
            (user_sel['three']['name'], user_sel['three']['source']), 
            (user_sel['four']['name'], user_sel['four']['source']), 
        ]

		self.vids = []
		columns = 2

		for number, source in enumerate(sources):
			name, stream = source
			vid = VideoFrame(
							 self.monitor, #>window to be used
							 name, #>text on top
							 stream, #>video source
							 int(screen_width/2.2), #>width
							 int(screen_height/3.1) #>height
							 )
						  
			x = number % columns #>x position (% modulus)
			y = number // columns #>y position (// floor division)
			vid.grid(row=y, column=x, padx=8, pady=6) #>video position
			self.vids.append(vid) #>include the video in the grid
		
		self.label = tk.Label(self.monitor, text='Fight Fighters Inc.', fg='#263942')
		self.label.configure(font='-size 11')
		self.label.grid(row=2, column=0, sticky='nw', padx=15, pady=18)

		self.btn_quit = tk.Button(self.monitor, text='Quit the App', 
                             fg='#263942', bg='#ffffff',
                             command=self.on_closing)
		self.btn_quit.configure(font='-size 10')
		self.btn_quit.place(relx=0.891, rely=bx, height=bheight, width=bwidth)

		self.btn_backlogin = tk.Button(self.monitor, text='Back to Login', 
                             fg='#263942', bg='#ffffff',
                             command=self.restore_window)
		self.btn_backlogin.configure(font='-size 10')
		self.btn_backlogin.place(relx=0.786, rely=bx, height=bheight, width=bwidth)

		self.monitor.protocol('WM_DELETE_WINDOW',
                              self.on_closing)

		### Stop GUI infrastructure
		self.monitor.mainloop()


	def restore_window(self):
		self.monitor.master.deiconify()
		self.monitor.destroy()
		
	def on_closing(self):
		
		print('[App] stopping threads')
		for source in self.vids:
			source.vid.running = False #>stop thread, stop reading the video
		print('[App] exit')
		self.monitor.destroy()