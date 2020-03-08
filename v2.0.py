import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import sys
import numpy as np




variabila=0

filters=['self.blur_image_low()','self.blur_image_mid()','self.blur_image_high()','self.black_white()','self.invert_filter()',
'self.sepia_filter()','self.bleached()']
nume=['BlurLow','BlurMid','BlurHigh','Black&White','Inverted','Sepia','Bleached']

 
class App:
	
	def __init__(self,window,window_title,image_path="111.jpg"):

		self.window=window
		self.window.title=(window_title)
		self.cv_img = cv2.cvtColor(cv2.imread("111.jpg"), cv2.COLOR_BGR2RGB)
		#resize
		self.scale_percent = 30
		self.div=(100* self.cv_img.shape[1])/2739
		
		print(self.cv_img.shape[1])
		print(self.cv_img.shape[0])


		self.width = int(self.cv_img.shape[1] * self.scale_percent / self.div)
		self.height = int(self.cv_img.shape[0] * self.scale_percent / self.div)
		self.dim = (self.width, self.height)
		self.resized = cv2.resize(self.cv_img, self.dim, interpolation = cv2.INTER_AREA)

		#show on screen
		self.height, self.width, no_channels = self.resized.shape
		self.canvas = tkinter.Canvas(window, width = self.width, height = self.height)
		self.canvas.pack()
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.resized))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		#buttons
		self.btn_up=tkinter.Button(window, text=">", width=50, command=self.state_up)
		self.btn_up.pack(anchor=tkinter.CENTER, expand=True)
		
		self.btn_down=tkinter.Button(window, text="<", width=50, command=self.state_down)
		self.btn_down.pack(anchor=tkinter.CENTER, expand=True)

		self.filter_name=tkinter.Label(window,text=nume[variabila],width=50)
		self.filter_name.pack(anchor=tkinter.CENTER,expand=True)



		self.window.mainloop()

	def state_up(self):
		global variabila
		global filters
		if(variabila>len(filters)-2):
			variabila=0
		else:
			variabila=variabila+1
		print(variabila)
		self.switch_fun()
	def state_down(self):
		global variabila
		global filters
		if(variabila<1):
			variabila=len(filters)-1
		else:
			variabila=variabila-1
		print(variabila)
		self.switch_fun()

	def switch_fun(self):
		global variabila
		global filters
		global nume
		eval(filters[variabila])
		self.filter_name.config(text=nume[variabila],width=50)

	def check_alpha_channel(self, resized):
		try:
			resized.shape[3]
		except IndexError:
			resized=cv2.cvtColor(self.resized,cv2.COLOR_BGR2BGRA)
		return resized

		
		
	


	def blur_image_low(self):
		self.result = cv2.blur(self.resized, (1, 1))
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.result))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		print('low')

	def blur_image_mid(self):
		self.result = cv2.blur(self.resized, (25, 25))
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.result))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		print("mid")
	def blur_image_high(self):
		self.result = cv2.blur(self.resized, (100, 100))
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.result))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		print("high")
	
	def black_white(self):
		self.result=cv2.cvtColor(self.resized,cv2.COLOR_BGR2GRAY)
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.result))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		print('b&w')

	def invert_filter(self):
		self.result=cv2.bitwise_not(self.resized)
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.result))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		print('invert')

	def sepia_filter(self):
		self.aux_resized=self.check_alpha_channel(self.resized)
		self.width,self.height,self.channel=self.aux_resized.shape
		self.blue=20 
		self.green=66 
		self.red=112 
		self.sepia_rgb=(self.red,self.green,self.blue,1)
		self.overlay=np.full((self.width,self.height,4),self.sepia_rgb, dtype='uint8')
		self.result=cv2.addWeighted(self.overlay,0.8,self.aux_resized,1.0,0,self.aux_resized)
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.result))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		print('sepia')

	def bleached(self):
		self.aux_resized=self.check_alpha_channel(self.resized)
		self.width,self.height,self.channel=self.aux_resized.shape
		self.blue=254
		self.green=223 
		self.red=185
		self.bleached_rgb=(self.red,self.green,self.blue,1)
		self.overlay=np.full((self.width,self.height,4),self.bleached_rgb, dtype='uint8')
		self.result=cv2.addWeighted(self.overlay,0.3,self.aux_resized,1.0,0,self.aux_resized)
		self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.result))
		self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
		print('bleached')




App(tkinter.Tk(), "Image filters ")