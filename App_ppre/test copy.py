import tkinter as tk
import json
from video_frame import tkCamera 

class Win1:
	def __init__(self, master):
		self.master = master
		self.master.geometry("400x400")
		self.frame = tk.Frame(self.master)
		self.butnew("Click to open Window 2", "2", Win2)
		self.butnew("Click to open Window 3", "3", Win3)
		self.frame.pack()

	def butnew(self, text, number, _class):
		tk.Button(self.frame, text = text, command= lambda: self.new_window(number, _class)).pack()

	def new_window(self, number, _class):
		self.new = tk.Toplevel(self.master)
		_class(self.new, number)

class Win2:
	def __init__(self, master, number):
		self.master = master
		self.master.geometry("400x400+200+200")
		self.frame = tk.Frame(self.master)
		self.quit = tk.Button(self.frame, text = f"Quit this window n. {number}", command = self.close_window)
		self.quit.pack()
		self.frame.pack()

	def close_window(self):
		self.master.destroy()


class Win3:
	def __init__(self, master, number):
		root.withdraw()
		bheight = 31
		bwidth = 130
		bx = 0.945
		
		self.master = master
		self.master.title("TITLE YOU WANT")
		#self.master.geometry("400x400+200+200")
		self.frame = tk.Frame(self.master)
		
		screen_width = self.master.winfo_screenwidth()
		screen_height = self.master.winfo_screenheight()
		self.master.geometry(f'{screen_width}x{screen_height}')
		self.master.columnconfigure([0,1], minsize=screen_width/2.107)
		self.master.rowconfigure([0,1,2], minsize=screen_height/3)

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
			vid = tkCamera(
                           self.master, #>window to be used
                           name, #>text on top
                           stream, #>video source
                           int(screen_width/2.2), #>width
                           int(screen_height/3.1) #>height
                          )
						  
			x = number % columns #>x position (% modulus)
			y = number // columns #>y position (// floor division)
			vid.grid(row=y, column=x, padx=8, pady=6) #>video position
			self.vids.append(vid) #>include the video in the grid


		
		self.label = tk.Label(self.master, text='Fight Fighters Inc.', fg='#263942')
		self.label.configure(font='-size 11')
		self.label.grid(row=2, column=0, sticky='nw', padx=15, pady=15)
		#self.label = tk.Label(self.frame, text="THIS IS ONLY IN THE THIRD WINDOW")
		#self.label.pack()

		self.btn_quit = tk.Button(self.master, text='Quit the App', 
                             fg='#263942', bg='#ffffff',
                             command=self.on_closing) #>command contains the func
                                                      #>to be run by this button
		self.btn_quit.configure(font='-size 10')
		self.btn_quit.place(relx=0.891, rely=bx, height=bheight, width=bwidth)

		
		#self.quit = tk.Button(self.frame, text = f"Quit this window n. {number}", command = self.close_window)
		#self.btn_quit.pack()

		self.btn_backlogin = tk.Button(self.master, text='Back to Login', 
                             fg='#263942', bg='#ffffff',
                             command=self.on_closing) #>command contains the func
                                                      #>to be run by this button
		self.btn_backlogin.configure(font='-size 10')
		self.btn_backlogin.place(relx=0.786, rely=bx, height=bheight, width=bwidth)

		
		#self.quit = tk.Button(self.frame, text = f"Quit this window n. {number}", command = self.close_window)
		#self.btn_quit.pack()

		self.btn_backcameras = tk.Button(self.master, text='Switch Cameras', 
                             fg='#263942', bg='#ffffff',
                             command=self.restore_window) #>command contains the func
                                                      #>to be run by this button
		self.btn_backcameras.configure(font='-size 10')
		self.btn_backcameras.place(relx=0.681, rely=bx, height=bheight, width=bwidth)

		self.master.protocol('WM_DELETE_WINDOW', #>to identify user closing
                             self.on_closing)

		#self.quit = tk.Button(self.frame, text = f"Quit this window n. {number}", command = self.close_window)
		#self.btn_quit.pack()
		
		### Stop GUI infrastructure
		self.master.mainloop()



		#self.frame.pack()


	def close_window(self):
		self.master.destroy()

	def restore_window(self):
		root.deiconify()
		self.master.destroy()
		
	def on_closing(self):
		
		print('[App] stopping threads')
		for source in self.vids:
			source.vid.running = False #>stop thread, stop reading the video
		print('[App] exit')
		self.master.option_add('*Dialog.msg.font', 'Helvetica 12')
		self.master.destroy()


	
root = tk.Tk()
app = Win1(root)
root.mainloop()