#!/usr/bin/env python
#-*- coding: UTF-8 -*- 
from Tkinter import *
import xlrd
import json
# 设置GBK编码
xlrd.Book.encoding = "gbk"

gm_file = u'gmlist.csv'
files = [
	u'游戏数据/背包/道具表.xlsx',
	]
k_max_field_output = 3
def find_excel(filename, keyword):
	book = xlrd.open_workbook(filename)
	sheet = book.sheet_by_index(0)
	field_names = []
	r = []
	is_digit = keyword.isdigit()
	for row in range(0, sheet.nrows):
		vid = sheet.cell(row, 0).value
		is_found = False
		output = ""
		if type(vid) != float:
			vid = vid.encode("utf-8")
		else:
			vid = int(vid)
			if is_digit and vid == int(keyword):
				is_found = True
				s = json.dumps(sheet.row_values(row)).decode('unicode-escape')
				r.append(s)
				continue
		# 遍历列
		for col in range(0, sheet.ncols):
			field = sheet.cell(row, col).value
			if type(field) != float:
				field = field.encode("utf-8")
				if field.find(keyword) != -1:
					is_found = True
					s = json.dumps(sheet.row_values(row)).decode('unicode-escape')
					r.append(s)
					break
	return r

class DocFinder(object):
	def __init__(self, initkey=None):
		self.top = Tk()
		self.label = Label(self.top, text='Doc Finder v1.1')
		self.label.pack()

		self.keyword = StringVar(self.top)

		# 输入关键字
		self.input = Entry(self.top, width=100, textvariable=self.keyword)
		self.input.bind('<Return>', self.dofind)
		self.input.pack()

		# 视图区域
		self.frame = Frame(self.top)
		# 滚动条
		self.xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
		self.xscroll.pack(side=BOTTOM, fill=X)
		self.yscroll = Scrollbar(self.frame, orient=VERTICAL)
		self.yscroll.pack(side=RIGHT, fill=Y)
		# listbox显示搜索结果
		self.box = Listbox(self.frame, height=20, width=100, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
		self.xscroll.config(command=self.box.xview)
		self.yscroll.config(command=self.box.yview)
		self.box.pack(side=LEFT, fill=BOTH)
		self.frame.pack()

		if initkey:
			self.keyword.set(initkey)
			self.dofind()

	def find_excel(self):
		text = excelpy.excel2json(files[0])
		print text

	def dofind(self, ev=None):
		keyword = self.keyword.get().encode('UTF-8')

		f = open(gm_file, 'r')
		gmlist = f.readlines()
		f.close()
		# gm
		rgm = []
		for i in gmlist:
			if i.find(keyword) != -1:
				rgm.append(i)

		self.box.delete(0, END)
		if len(rgm) > 0:
			self.box.insert(END, "---------- gm -----------")
		for i in rgm:
			text = i.split(',', 1)
			if len(text) > 0:
				head = text[0]
				tail = text[-1]
				self.box.insert(END, "%s%s"%(head.ljust(30), tail.lstrip()))
		for fn in files:
			r = find_excel(fn, keyword)
			if len(r) > 0:
				self.box.insert(END, "---------- %s -----------"%fn)
				for i in r:
					self.box.insert(END, i)

def main():
	finder = DocFinder(u"鱼")
	mainloop()

if __name__ == '__main__':
	main()
