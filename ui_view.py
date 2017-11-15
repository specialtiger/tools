# -*- coding:utf-8 -*-
from Tkinter import *
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET
import os

os.getcwd()
os.chdir("../client/GameBase/Resources/ClientHN_THJ")
print(os.getcwd())
k_screen_w = 1280
k_screen_h = 720

def parse_widget(wdg):
	attrs = {}
	for elem in wdg:
		if elem.tag == "Property":
			key = elem.attrib.get("Key")
			val = elem.attrib.get("Value")
			if key == 'Pos':
				lst = val.split()
				attrs['x'] = int(lst[0])
				attrs['y'] = int(lst[1])
			else:
				attrs[key] = val
	return attrs

def load_xml(filename):
	tree = ET.ElementTree(file=filename)
	root = tree.getroot()
	parent = None
	for elem in root:
		if elem.tag == "Widget":
			parent = elem
			break
	print filename, parent
	if parent != None:
		print parent.tag, parent.attrib
	parent_attrs = parse_widget(parent) 
	children = []
	for elem in parent:
		if elem.tag == "Widget":
			attrs = parse_widget(elem)
			children.append(attrs)
	return parent_attrs, children

def ls_dir(dir):
	xmls = []
	for dirpath, dirnames, filenames in os.walk(dir):
		for f in filenames:
			if "Scence.xml" in f:
				dirpath = dirpath.replace('Script', '')
				xmls.append(dirpath+'/'+f)
	return xmls

class UiViewer(object):
	def __init__(self):
		self.imgs = []
		self.top = Tk()
		self.top.geometry('%sx%s'%(k_screen_w+100, k_screen_h))

		xmls = ls_dir('Script')
		self.lb = Listbox(self.top, width=20, height=30)
		self.lb.bind('<Double-Button-1>', self.reload_xml)
		for i in xmls:
			self.lb.insert(END, i)
		self.lb.pack(side=RIGHT)

		self.image_frame = Frame(self.top)
		self.image_frame.pack(side=LEFT)
		self.canvas = Canvas(self.image_frame, bg="black", width=k_screen_w, height=k_screen_h)
		self.canvas.pack()

	def reload_xml(self, event):
		xml = self.lb.get(self.lb.curselection())
		self.mk_widget(xml)

	def add_img(self, filename, x=0, y=0, scale=1.0):
		image = Image.open(filename)
		[w, h] = image.size
		image = image.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)
		pimage = ImageTk.PhotoImage(image)
		# self.canvas.create_image(k_screen_w/2+x, k_screen_h/2-y, image=pimage)
		ix,iy = x+self.offset_x, k_screen_h-(y+self.offset_y)
		print(filename, ix, iy)
		self.canvas.create_image(ix, iy, image=pimage)
		self.imgs.append(pimage)

	def add_img_from_xml(self, item, elem_name):
		img_file = item.get(elem_name)
		if img_file != None:
			x = item.get('x') or 0
			y = item.get('y') or 0
			scale = item.get('Scale') or 1.0
			scale = float(scale)
			self.add_img(img_file, x, y, scale)

	def mk_widget(self, filename):
		self.canvas.delete(ALL)
		parent, children = load_xml("Script/"+filename)
		self.offset_x = parent.get('x') or 0
		self.offset_y = parent.get('y') or 0
		for item in children:
			self.add_img_from_xml(item, "ImagicTexture")
			self.add_img_from_xml(item, "NomalTexture")

def main():
	ui = UiViewer()
	ui.mk_widget('HNLogonScence.xml')
	mainloop()

if __name__ == '__main__':
	main()
# bg = Image.open(r"C:\Users\tiger\Pictures\\20160331221957.jpg")
# bg.show()

