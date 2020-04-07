import tkinter as tk 
from tkinter import filedialog as fd

import cv2 as cv2
import time
import numpy as np
import PIL
from PIL import Image, ImageTk
import tempfile
import shutil
import os

class App(tk.Frame): 
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.title("MJPEG App")
		self.master.geometry('800x600')
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.lbl = tk.Label(self, text="Input stream URL")
		self.lbl.grid(column=0, row=0)

		self.url_input = tk.Entry(self, width=30)
		self.url_input.grid(column=0, row=2)

		self.hi_there = tk.Button(self, text="GET URL", command=self.get_url)
		self.hi_there.grid(column=1, row=2)

		self.download = tk.Button(self, text="DOWNLOAD", command=self.save_image)
		self.download.grid(column=2, row=2)

		self.download = tk.Button(self, text="RECORD", command=self.record)
		self.download.grid(column=3, row=2)

		self.download = tk.Button(self, text="STOP RECORD", command=self.stop_record)
		self.download.grid(column=4, row=2)
	
	def get_url(self): 
		url = self.url_input.get()
		img = self.get_image(url)
		self.latest_image = img
		img_tk = ImageTk.PhotoImage(img)
		self.image_lbl = tk.Label(self, image=img_tk)
		self.image_lbl.image = img_tk
		self.image_lbl.grid(column=0, row=3)
  
	def get_image(self, url):
		cap = cv2.VideoCapture(url)
		result, frame = cap.read()
		if result: 
			temp_file = tempfile.TemporaryFile()
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			pil_im = Image.fromarray(frame)
			return pil_im
		else: 
			print("Fail")

	def save_image(self): 
		self.filename = fd.asksaveasfile(mode='w', defaultextension='.jpg')
		self.latest_image.save(self.filename)
	
	def find_dimensions(self, url):
		cap = cv2.VideoCapture(url)
		dimensions = (640, 360) #width, height

		# Let us first figure out the dimensions of the video 
		try:
			result, frame = cap.read()
			if result: 
				return frame.shape
			else: 
				print("Error in first grab")
				return dimensions 
		except Exception as e: 
			print(e)

	def calculate_frame_rate(url):
		cap = cv2.VideoCapture(url)
		num_frames = 30

		# Start time 
		start = time.time()

		for i in range(0, num_frames):
			ret, frame = cap.read()

		# Start time 
			end = time.time()

		return int((num_frames/(end - start)) * 2)
	
	def stop_record(self): 
		self.recording = False

	def record(self, args={'framerate': 10}):
		print("Finding dimensions")
		url = self.url_input.get()
		self.recording = True
		dimensions = self.find_dimensions(url)

		fourcc = cv2.VideoWriter_fourcc(*'MP4V')
		writer = cv2.VideoWriter('../output--{0}.mp4'.format(time.strftime('%y-%m-%d-%H-%M')), fourcc, args['framerate'],  (dimensions[1], dimensions[0]))

		try: 
			if hasattr(args, 'mjpeg') == False or args['mjpeg'] == True:
				cap = cv2.VideoCapture(url)

			while(self.recording):
				try: 
					if 'mjpeg' in args and args['mjpeg'] != True:
						cap = cv2.VideoCapture(url)

						result, frame = cap.read()
						if result == False: 
							print("Error in cap.read()") # this is for preventing a breaking error 
							# break; 
							pass; 
						plt.imshow(frame)
						writer.write(frame)
						plt.show()

					if 'mjpeg' in args and args['mjpeg'] != True:
						cap.release()

				except Exception as e:  
					print(e)
					clear_output(wait=True)
		except KeyboardInterrupt:
			cap.release()
			writer.release()
			cv2.destroyAllWindows()

root = tk.Tk()
app = App(master=root)
app.mainloop()