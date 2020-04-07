import tkinter as tk 
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
		self.master.geometry('500x350')
		self.pack()
		self.create_widgets()
	
	def create_widgets(self):
		self.lbl = tk.Label(self, text="Input stream URL")
		self.lbl.grid(column=0, row=0)

		self.url_input = tk.Entry(self, width=30)
		self.url_input.grid(column=0, row=2)

		self.hi_there = tk.Button(self, text="GET URL", command=self.get_url)
		self.hi_there.grid(column=1, row=2)
rm -rf build dist
		self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
		self.quit.grid(column=3, row=0)
	
	def get_url(self): 
		url = self.url_input.get()
		img = self.get_image(url)
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
			# pil_im.save(temp_file, "JPEG")
			# temp_file.seek(0)
			return pil_im
		else: 
			print("Fail")

root = tk.Tk()
app = App(master=root)
app.mainloop()

# Prep step: Find out the size of the video file 

def find_dimensions(url):
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

        
# CREDIT TO THIS: https://www.learnopencv.com/how-to-find-frame-rate-or-frames-per-second-fps-in-opencv-python-cpp/

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

# Action step 

def save_stream(url, args={'framerate': 10}):
    print("Finding dimensions")
    dimensions = find_dimensions(url)
    
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    writer = cv2.VideoWriter('../output--{0}.mp4'.format(time.strftime('%y-%m-%d-%H-%M')), 
                                 fourcc, args['framerate'],  (dimensions[1], dimensions[0]))
    
    try: 
        if hasattr(args, 'mjpeg') == False or args['mjpeg'] == True:
            cap = cv2.VideoCapture(url)
        
        while(True):
            try: 
                if 'mjpeg' in args and args['mjpeg'] != True:
                    cap = cv2.VideoCapture(url)

                result, frame = cap.read()
                if result == False: 
                    print("Error in cap.read()") # this is for preventing a breaking error 
                    # break; 
                    pass; 
        #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                plt.imshow(frame)
                writer.write(frame)
                plt.show()

                if 'mjpeg' in args and args['mjpeg'] != True:
                    cap.release()

                clear_output(wait=True)

            except Exception as e:  
                print(e)
                clear_output(wait=True)
    except KeyboardInterrupt:
        cap.release()
        writer.release()
        cv2.destroyAllWindows()
