# -*- coding:utf-8 -*-
import os
import re

os.getcwd()
os.chdir("/Users/specialtiger/Downloads/")
dir_name = '终末'
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
def write_html_head(open_file):
    head = '''<!DOCTYPE HTML>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta name="format-detection" content="telephone=no, email=no, date=no, address=no">
    <link rel="stylesheet" type="text/css" href="../css/api.css" />
    <style>
        body {
            background-color: #e4ebf1;
            font-size: 1.5em;
        }
    </style>

</head>'''
    open_file.write(head+'\n')

def write_html_tail(open_file):
    open_file.write('</html>\n')

def main():
    # with open(findall_title[0] + '.txt', 'w+', encoding='utf-8') as open_file:
    with open('index.html', 'w') as open_file:
        write_html_head(open_file)
        fs = ls_dir(dir_name)
       	for i in fs:
        	open_file.write('<img src="%s"/>'%i)
        write_html_tail(open_file)

    print('文件写入完毕')

def test_sort():
	arr = ['1.jpg', '10.jpg', '11.jpg', '12.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg']
	print sorted(arr, key=sort_func)
	arr = ['19 (1).png', '19 (10).png', '19 (11).png', '19 (12).png', '19 (13).png', '19 (14).png', '19 (15).png', '19 (16).png', '19 (17).png', '19 (18).png', '19 (19).png', '19 (2).png', '19 (20).png', '19 (21).png', '19 (22).png', '19 (3).png', '19 (4).png', '19 (5).png', '19 (6).png', '19 (7).png', '19 (8).png', '19 (9).png']
	print sorted(arr, key=sort_func_png)

if __name__ == '__main__':
	main()
	# test_sort()
# bg = Image.open(r"C:\Users\tiger\Pictures\\20160331221957.jpg")
# bg.show()

