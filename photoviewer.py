# -*- coding:utf-8 -*-
from Tkinter import *
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET
import os
import re

os.getcwd()
os.chdir("/Users/specialtiger/Downloads/")
print(os.getcwd())
k_screen_w = 1280
k_screen_h = 1280

def sort_func_png(filename):
	m = re.match(".*\(([0-9]+)\).png", filename)
	if m:
		return int(m.group(1)) or 0
	return filename

def sort_func(filename):
	m = re.match("([0-9]+).(jpg|png)", filename)
	if m:
		return int(m.group(1)) or 0
	return sort_func_png(filename)

def ls_dir(dir):
	fs = []
	for dirpath, dirnames, filenames in os.walk(dir):
		# print filenames
		sfs = sorted(filenames, key=sort_func)
		for f in sfs:
			if ".jpg" in f or "png" in f:
				fs.append(dirpath+'/'+f)
	return fs

class UiViewer(object):
	def __init__(self):
		self.imgs = []
		self.top = Tk()
		self.top.geometry('%sx%s'%(k_screen_w+100, k_screen_h))

		self.ctl_frame = Frame(self.top)
		self.ctl_frame.pack(side=RIGHT)

		self.bt = Button(self.ctl_frame, text = 'reload', command = self.reload_files)
		self.bt.pack()

		self.dir = '终末'

		self.lb = Listbox(self.ctl_frame, width=20, height=30)
		# self.lb.bind('<Double-Button-1>', self.reload_xml)
		self.lb.bind('<Button-1>', self.reload_xml)
		self.lb.bind('<Up>', self.reload_xml)
		self.lb.bind('<Down>', self.reload_xml)
		self.lb.pack()

		self.image_frame = Frame(self.top)
		frame = self.image_frame
		self.image_frame.pack(side=LEFT)
		canvas=Canvas(frame,bg='black',width=k_screen_w,height=k_screen_h,scrollregion=(0,0,1280,1280))
		hbar=Scrollbar(frame,orient=HORIZONTAL)
		hbar.pack(side=BOTTOM,fill=X)
		hbar.config(command=canvas.xview)
		vbar=Scrollbar(frame,orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=canvas.yview)
		canvas.config(width=k_screen_w,height=k_screen_h)
		canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		canvas.pack(side=LEFT,expand=True,fill=BOTH)

		self.canvas = canvas
		# self.canvas = Canvas(self.image_frame, bg="black", width=k_screen_w, height=k_screen_h)
		# self.canvas.pack()

		self.reload_files()

	def reload_files(self):
		self.lb.delete(0, END)
		xmls = ls_dir(self.dir)
		for i in xmls:
			self.lb.insert(END, i)

	def reload_xml(self, event):
		idx = self.lb.curselection()
		if not idx or idx < 0:
			return
		xml = self.lb.get(idx)
		self.mk_widget(xml)

	def mk_widget(self, filename):
		self.canvas.delete(ALL)
		self.add_img(filename)

	def add_img(self, filename, x=0, y=0, scale=1.0):
		image = Image.open(filename).convert('RGB')
		[w, h] = image.size
		# scale = k_screen_h/h
		image = image.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)
		pimage = ImageTk.PhotoImage(image)
		self.canvas.create_image(k_screen_w/2+x, h/2-y, image=pimage)
		self.imgs.append(pimage)

def test_sort():
	arr = ['1.jpg', '10.jpg', '11.jpg', '12.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg']
	print sorted(arr, key=sort_func)
	arr = ['19 (1).png', '19 (10).png', '19 (11).png', '19 (12).png', '19 (13).png', '19 (14).png', '19 (15).png', '19 (16).png', '19 (17).png', '19 (18).png', '19 (19).png', '19 (2).png', '19 (20).png', '19 (21).png', '19 (22).png', '19 (3).png', '19 (4).png', '19 (5).png', '19 (6).png', '19 (7).png', '19 (8).png', '19 (9).png']
	print sorted(arr, key=sort_func_png)

def main():
	ui = UiViewer()
	mainloop()

if __name__ == '__main__':
	main()
	# test_sort()
# bg = Image.open(r"C:\Users\tiger\Pictures\\20160331221957.jpg")
# bg.show()

